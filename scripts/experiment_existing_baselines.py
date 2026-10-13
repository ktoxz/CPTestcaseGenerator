"""Reconstruct sample-only and per-iteration oracle metrics from locked runs.

The final oracle log is sufficient because cases are evaluated in suite order and
the judge stops at the first non-PASS verdict.  Official samples and iteration-0
cases are prefixes of the final locked suite, so their verdicts can be recovered
without executing untrusted submissions again.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDALONE_EXCLUSIONS = {"batches", "codenet-additional20-validation", "pilot20-20261007"}


def read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def selected_reports(output_root: Path) -> dict[str, Path]:
    candidates: list[Path] = []
    batches = output_root / "batches"
    if batches.is_dir():
        for batch_report in batches.glob("*/batch-report.json"):
            data = read_json(batch_report)
            if not data.get("finished_at") or data.get("completed") != data.get("total"):
                continue
            for item in data.get("results", []):
                if item.get("status") != "succeeded" or not item.get("report"):
                    continue
                report = Path(item["report"])
                if not report.is_absolute():
                    report = ROOT / report
                if report.is_file():
                    candidates.append(report)
    for problem_dir in output_root.iterdir():
        if not problem_dir.is_dir() or problem_dir.name in STANDALONE_EXCLUSIONS:
            continue
        candidates.extend(problem_dir.glob("*/report.json"))

    selected: dict[str, tuple[float, Path]] = {}
    for path in candidates:
        try:
            report = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(report, dict) or not report.get("test_suite_lock"):
            continue
        problem_id = report.get("problem_id")
        if not problem_id or not report.get("oracle_metrics"):
            continue
        stamp = path.stat().st_mtime
        if problem_id not in selected or stamp > selected[problem_id][0]:
            selected[problem_id] = (stamp, path)
    return {problem: item[1] for problem, item in selected.items()}


def metric(labels: dict[str, str], verdicts: dict[str, str]) -> dict:
    accepted = [verdicts[sid] for sid, label in labels.items() if label == "Accepted"]
    wrong = [verdicts[sid] for sid, label in labels.items() if label == "Wrong Answer"]
    positive_evaluable = sum(v not in {"CE", "INFRA"} for v in accepted)
    negative_evaluable = sum(v not in {"CE", "INFRA"} for v in wrong)
    positive_pass = accepted.count("PASS")
    negative_killed = sum(v in {"WA", "RE", "TLE"} for v in wrong)
    return {
        "positive_pass": positive_pass,
        "positive_evaluable": positive_evaluable,
        "negative_killed_logic": negative_killed,
        "negative_evaluable": negative_evaluable,
        "tpr": positive_pass / positive_evaluable if positive_evaluable else None,
        "tnr": negative_killed / negative_evaluable if negative_evaluable else None,
        "ce_infra_positive": sum(v in {"CE", "INFRA"} for v in accepted),
        "ce_infra_negative": sum(v in {"CE", "INFRA"} for v in wrong),
    }


def reconstruct(report_path: Path, case_ids: set[str]) -> dict:
    run = report_path.parent
    report = read_json(report_path)
    manifest = read_json(run / "oracle" / "manifest.json")
    labels = {row["id"]: row["label"] for row in manifest}
    rows_by_solution: dict[str, list[dict]] = defaultdict(list)
    execution_path = run / "oracle" / "executions.jsonl"
    for line in execution_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows_by_solution[row["solution_id"]].append(row)

    verdicts: dict[str, str] = {}
    final = report["oracle_verdicts"]
    for solution_id in labels:
        final_verdict = final[solution_id]["verdict"]
        if final_verdict in {"CE", "INFRA"}:
            verdicts[solution_id] = final_verdict
            continue
        relevant = [row for row in rows_by_solution[solution_id] if row["case_id"] in case_ids]
        failure = next((row["verdict"] for row in relevant if row["verdict"] != "PASS"), None)
        verdicts[solution_id] = failure or "PASS"
    return metric(labels, verdicts)


def unavailable_metric() -> dict:
    return {
        "positive_pass": 0, "positive_evaluable": 0,
        "negative_killed_logic": 0, "negative_evaluable": 0,
        "tpr": None, "tnr": None,
        "ce_infra_positive": 0, "ce_infra_negative": 0,
    }


def aggregate(rows: list[dict], variant: str) -> dict:
    eligible = [row[variant] for row in rows
                if row["final"]["tpr"] is not None and row["final"]["tnr"] is not None
                and row[variant]["tpr"] is not None and row[variant]["tnr"] is not None]
    if not eligible:
        return {"problems": 0}
    tpr = [row["tpr"] for row in eligible]
    tnr = [row["tnr"] for row in eligible]
    return {
        "problems": len(eligible),
        "macro_tpr": sum(tpr) / len(tpr),
        "macro_tnr": sum(tnr) / len(tnr),
        "micro_tpr": sum(row["positive_pass"] for row in eligible) / sum(row["positive_evaluable"] for row in eligible),
        "micro_tnr": sum(row["negative_killed_logic"] for row in eligible) / sum(row["negative_evaluable"] for row in eligible),
        "both_at_least_0_8": sum(row["tpr"] >= .8 and row["tnr"] >= .8 for row in eligible),
    }


def paired_bootstrap(rows: list[dict], first: str, second: str, field: str, *, seed: int = 20261013) -> dict:
    pairs = [(row[first][field], row[second][field]) for row in rows
             if row["final"]["tpr"] is not None and row["final"]["tnr"] is not None
             and row[first][field] is not None and row[second][field] is not None]
    deltas = [after - before for before, after in pairs]
    rng = random.Random(seed)
    samples = sorted(sum(rng.choices(deltas, k=len(deltas))) / len(deltas) for _ in range(10_000))
    return {
        "problems": len(deltas),
        "mean_delta": sum(deltas) / len(deltas),
        "bootstrap_95_ci": [samples[250], samples[9749]],
        "improved": sum(delta > 0 for delta in deltas),
        "unchanged": sum(delta == 0 for delta in deltas),
        "worsened": sum(delta < 0 for delta in deltas),
    }


def run(output: Path) -> dict:
    reports = selected_reports(ROOT / "output")
    rows = []
    for problem_id, report_path in sorted(reports.items()):
        report = read_json(report_path)
        cases = report["cases"]
        sample_ids = {case["id"] for case in cases if case.get("family") == "official-sample"}
        round0_ids = {case["id"] for case in cases if case.get("iteration") == 0}
        if not round0_ids:
            raise RuntimeError(f"{problem_id}: missing iteration-0 cases")
        rows.append({
            "problem_id": problem_id,
            "report": str(report_path.relative_to(ROOT)),
            "sample_cases": len(sample_ids),
            "round0_cases": len(round0_ids),
            "final_cases": len(cases),
            "sample": reconstruct(report_path, sample_ids) if sample_ids else unavailable_metric(),
            "round0": reconstruct(report_path, round0_ids),
            "final": {
                "positive_pass": report["oracle_metrics"]["positive_pass"],
                "positive_evaluable": report["oracle_metrics"]["positive_evaluable"],
                "negative_killed_logic": report["oracle_metrics"]["negative_killed_logic"],
                "negative_evaluable": report["oracle_metrics"]["negative_evaluable"],
                "tpr": report["oracle_metrics"]["tpr_label_based"],
                "tnr": report["oracle_metrics"]["tnr_label_based"],
                "ce_infra_positive": report["oracle_metrics"]["ce_infra"]["positive"],
                "ce_infra_negative": report["oracle_metrics"]["ce_infra"]["negative"],
            },
        })
    summary = {
        "created_at": datetime.now().astimezone().isoformat(),
        "protocol": "Latest successful locked run per problem from completed batches and standalone runs; reconstructed prefix verdicts from final oracle execution logs.",
        "official_hidden_tests": {
            "available": False,
            "problems_with_local_assets": 0,
            "note": "The 60 report problem directories contain statements, checker profiles/scripts, and oracle submissions, but no official hidden testcase assets. Official samples embedded in statements are evaluated separately.",
        },
        "variants": {name: aggregate(rows, name) for name in ("sample", "round0", "final")},
        "round0_to_final": {
            "tpr": paired_bootstrap(rows, "round0", "final", "tpr"),
            "tnr": paired_bootstrap(rows, "round0", "final", "tnr"),
        },
        "sample_to_final": {
            "tpr": paired_bootstrap(rows, "sample", "final", "tpr"),
            "tnr": paired_bootstrap(rows, "sample", "final", "tnr"),
        },
        "problems": rows,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "per-problem.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["problem_id", "sample_cases", "round0_cases", "final_cases",
                         "sample_tpr", "sample_tnr", "round0_tpr", "round0_tnr", "final_tpr", "final_tnr", "report"])
        for row in rows:
            writer.writerow([row["problem_id"], row["sample_cases"], row["round0_cases"], row["final_cases"],
                             row["sample"]["tpr"], row["sample"]["tnr"], row["round0"]["tpr"], row["round0"]["tnr"],
                             row["final"]["tpr"], row["final"]["tnr"], row["report"]])
    lines = ["# Existing-run baselines", "", summary["protocol"], "",
             "| Variant | Problems | Macro TPR | Macro TNR | Micro TPR | Micro TNR | Both ≥ 0.8 |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for name, label in (("sample", "Official samples only"), ("round0", "After iteration 1"), ("final", "After iteration 2")):
        item = summary["variants"][name]
        lines.append(f"| {label} | {item['problems']} | {item['macro_tpr']:.2%} | {item['macro_tnr']:.2%} | {item['micro_tpr']:.2%} | {item['micro_tnr']:.2%} | {item['both_at_least_0_8']} |")
    lines += ["", "## Paired change from iteration 1 to iteration 2", "",
              "| Metric | Mean change | Bootstrap 95% CI | Improved | Same | Worsened |",
              "|---|---:|---:|---:|---:|---:|"]
    for key in ("tpr", "tnr"):
        item = summary["round0_to_final"][key]
        lines.append(f"| {key.upper()} | {item['mean_delta']:+.2%} | {item['bootstrap_95_ci'][0]:+.2%} to {item['bootstrap_95_ci'][1]:+.2%} | {item['improved']} | {item['unchanged']} | {item['worsened']} |")
    lines += ["", "## Official hidden-test inventory", "",
              summary["official_hidden_tests"]["note"]]
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "experiments" / "existing-baselines-20261013")
    args = parser.parse_args()
    summary = run(args.output)
    print(json.dumps({"output": str(args.output), "variants": summary["variants"],
                      "round0_to_final": summary["round0_to_final"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
