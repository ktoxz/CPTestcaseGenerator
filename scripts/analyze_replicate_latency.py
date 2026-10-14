"""Summarize final-attempt latency and oracle results for repeated runs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def successful_segment(events: list[dict]) -> list[dict]:
    end = next(
        (index for index in range(len(events) - 1, -1, -1)
         if events[index].get("component") == "pipeline.total"
         and events[index].get("status") == "ok"),
        None,
    )
    if end is None:
        return []
    start = 0
    for index in range(end - 1, -1, -1):
        # A process can be interrupted before writing pipeline.total. The next
        # retry appends to the same latency file, so its startup probe is the
        # reliable boundary of the successful invocation.
        if events[index].get("component") == "startup.docker_probe":
            start = index
            break
        if events[index].get("component") == "pipeline.total":
            start = index + 1
            break
    return events[start:end + 1]


def phase_name(event: dict) -> str:
    component = event.get("component", "")
    label = event.get("label") or event.get("stage") or ""
    if component == "stage":
        return f"stage: {label}"
    if component == "judge.pool":
        return f"judge pool: {event.get('stage', label)}"
    if component == "judge.compile_pool":
        return f"compile pool: {event.get('stage', label)}"
    if component in {"claude.request", "ollama.request"}:
        return f"{component}: {label}"
    return f"{component}: {label}".rstrip(": ")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--replicates", type=int, nargs="+", default=[1, 2])
    args = parser.parse_args()

    status_path = args.root / "status.json"
    attempts = read_json(status_path).get("attempts", []) if status_path.is_file() else []
    rows = []
    for replicate in args.replicates:
        rep_root = args.root / f"replicate-{replicate}"
        if not rep_root.is_dir():
            continue
        for problem_root in sorted(path for path in rep_root.iterdir() if path.is_dir()):
            report_path = problem_root / "report.json"
            latency_path = problem_root / "latency.jsonl"
            if not report_path.is_file() or not latency_path.is_file():
                continue
            events = [
                json.loads(line) for line in latency_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            segment = successful_segment(events)
            if not segment:
                continue
            report = read_json(report_path)
            oracle = report.get("oracle_metrics") or {}
            pipeline_ms = next(
                event["duration_ms"] for event in reversed(segment)
                if event.get("component") == "pipeline.total"
            )
            phase_events = [
                event for event in segment
                if event.get("component") in {
                    "stage", "judge.pool", "judge.compile_pool",
                    "claude.request", "ollama.request",
                }
            ]
            longest = max(phase_events, key=lambda event: event["duration_ms"])
            llm_events = [
                event for event in segment
                if event.get("component") in {"claude.request", "ollama.request"}
            ]
            oracle_pool = [
                event for event in segment
                if event.get("component") == "judge.pool"
                and event.get("stage") == "CodeNet"
            ]
            matching_attempts = [
                attempt for attempt in attempts
                if attempt.get("replicate") == replicate
                and attempt.get("problem_id") == problem_root.name
            ]
            rows.append({
                "replicate": replicate,
                "problem_id": problem_root.name,
                "pipeline_seconds": round(pipeline_ms / 1000, 3),
                "longest_phase": phase_name(longest),
                "longest_phase_seconds": round(longest["duration_ms"] / 1000, 3),
                "llm_request_seconds_sum": round(
                    sum(event["duration_ms"] for event in llm_events) / 1000, 3
                ),
                "llm_request_count": len(llm_events),
                "oracle_pool_seconds": round(
                    max((event["duration_ms"] for event in oracle_pool), default=0) / 1000,
                    3,
                ),
                "recorded_attempts": len(matching_attempts),
                "failed_attempts": sum(attempt.get("exit_code") != 0 for attempt in matching_attempts),
                "attempt_wall_seconds_sum": round(
                    sum(float(attempt.get("duration_seconds", 0)) for attempt in matching_attempts), 3
                ),
                "cases": len(report.get("cases", [])),
                "tpr": oracle.get("tpr_label_based"),
                "tnr": oracle.get("tnr_label_based"),
            })

    output_json = args.root / "replicate-1-2-latency-analysis.json"
    output_csv = args.root / "replicate-1-2-latency-analysis.csv"
    output_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with output_csv.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)

    summary = {}
    for replicate in args.replicates:
        subset = [row for row in rows if row["replicate"] == replicate]
        summary[str(replicate)] = {
            "completed": len(subset),
            "pipeline_seconds_sum": round(sum(row["pipeline_seconds"] for row in subset), 3),
            "pipeline_seconds_mean": round(
                sum(row["pipeline_seconds"] for row in subset) / len(subset), 3
            ) if subset else None,
            "macro_tpr": sum(row["tpr"] for row in subset) / len(subset) if subset else None,
            "macro_tnr": sum(row["tnr"] for row in subset) / len(subset) if subset else None,
            "both_at_least_08": sum(row["tpr"] >= .8 and row["tnr"] >= .8 for row in subset),
            "longest_phase_counts": Counter(row["longest_phase"].split(":", 1)[0] for row in subset),
        }
    print(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
