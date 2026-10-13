"""Repeat the full pipeline three times on a fixed stratified 12-problem subset."""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from experiment_existing_baselines import ROOT, git_provenance, read_json, selected_reports


# Registered before execution: six Codeforces/open-r1 and six CodeNet problems,
# spanning strong results, low TPR, low TNR, and known run-to-run instability.
DEFAULT_PROBLEMS = [
    "cf1003a", "cf1003c", "cf1005a", "cf1008a", "cf1008b", "cf1949b",
    "p02548", "p02585", "p02586", "p02623", "p02986", "p03274",
]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def summarize(output: Path, problems: list[str], replicates: int) -> dict:
    rows = []
    for replicate in range(1, replicates + 1):
        for problem in problems:
            report_path = output / f"replicate-{replicate}" / problem / "report.json"
            if not report_path.is_file():
                continue
            report = read_json(report_path)
            metric = report.get("oracle_metrics") or {}
            rows.append({
                "replicate": replicate,
                "problem_id": problem,
                "tpr": metric.get("tpr_label_based"),
                "tnr": metric.get("tnr_label_based"),
                "cases": len(report.get("cases", [])),
                "report": str(report_path.relative_to(ROOT)),
            })
    by_problem = []
    for problem in problems:
        values = [row for row in rows if row["problem_id"] == problem]
        tpr = [row["tpr"] for row in values if row["tpr"] is not None]
        tnr = [row["tnr"] for row in values if row["tnr"] is not None]
        by_problem.append({
            "problem_id": problem,
            "completed": len(values),
            "tpr_mean": statistics.mean(tpr) if tpr else None,
            "tpr_sample_sd": statistics.stdev(tpr) if len(tpr) > 1 else None,
            "tnr_mean": statistics.mean(tnr) if tnr else None,
            "tnr_sample_sd": statistics.stdev(tnr) if len(tnr) > 1 else None,
            "case_mean": statistics.mean(row["cases"] for row in values) if values else None,
        })
    summary = {
        "updated_at": datetime.now().astimezone().isoformat(),
        "planned_runs": len(problems) * replicates,
        "completed_runs": len(rows),
        "problems": by_problem,
        "runs": rows,
    }
    write_json(output / "summary.json", summary)
    return summary


def run(args: argparse.Namespace) -> None:
    selected = selected_reports(ROOT / "output")
    missing = sorted(set(args.problems) - set(selected))
    if missing:
        raise SystemExit("Problems are not in the thesis report cohort: " + ", ".join(missing))
    args.output.mkdir(parents=True, exist_ok=True)
    write_json(args.output / "protocol.json", {
        "created_at": datetime.now().astimezone().isoformat(),
        "provenance": git_provenance(),
        "selection": "pre-registered stratified subset: 6 Codeforces/open-r1 + 6 CodeNet; varied original TPR/TNR and instability",
        "problems": args.problems,
        "replicates": args.replicates,
        "judge": "local Docker",
        "pipeline": "unchanged default full pipeline",
        "oracle_per_label": args.oracle_limit,
        "execution_order": "replicate-major",
    })
    status_path = args.output / "status.json"
    status = read_json(status_path) if status_path.is_file() else {"attempts": []}
    for replicate in range(1, args.replicates + 1):
        for problem in args.problems:
            run_output = args.output / f"replicate-{replicate}" / problem
            report_path = run_output / "report.json"
            if report_path.is_file():
                print(f"[replicate {replicate}] {problem}: already complete", flush=True)
                continue
            run_output.mkdir(parents=True, exist_ok=True)
            log_path = run_output / "run.log"
            command = [
                sys.executable, str(ROOT / "main.py"),
                "--problem", problem,
                "--judge", "local",
                "--oracle", "--oracle-limit", str(args.oracle_limit),
                "--iterations", "2",
                "--output", str(run_output),
            ]
            print(f"[replicate {replicate}/{args.replicates}] {problem}: starting", flush=True)
            started = time.monotonic()
            with log_path.open("w", encoding="utf-8") as log:
                completed = subprocess.run(
                    command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                    text=True, check=False,
                )
            attempt = {
                "finished_at": datetime.now().astimezone().isoformat(),
                "replicate": replicate,
                "problem_id": problem,
                "exit_code": completed.returncode,
                "duration_seconds": round(time.monotonic() - started, 3),
                "log": str(log_path.relative_to(ROOT)),
                "report": str(report_path.relative_to(ROOT)) if report_path.is_file() else None,
            }
            status["attempts"].append(attempt)
            write_json(status_path, status)
            summarize(args.output, args.problems, args.replicates)
            print(
                f"[replicate {replicate}/{args.replicates}] {problem}: "
                f"{'complete' if report_path.is_file() else 'failed'} "
                f"({attempt['duration_seconds']:.1f}s)", flush=True,
            )
    print(json.dumps(summarize(args.output, args.problems, args.replicates), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "experiments" / "repeated-runs-20261013")
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--oracle-limit", type=int, default=20)
    parser.add_argument("--problems", nargs="+", default=DEFAULT_PROBLEMS)
    args = parser.parse_args()
    if not 2 <= args.replicates <= 10:
        parser.error("--replicates must be 2..10")
    run(args)


if __name__ == "__main__":
    main()
