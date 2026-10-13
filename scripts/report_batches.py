#!/usr/bin/env python3
"""Summarize every persisted batch run into Markdown and CSV artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def failure_reason(result: dict) -> str:
    raw_path = result.get("log")
    path = Path(raw_path) if raw_path else None
    text = (
        path.read_text(encoding="utf-8", errors="replace")
        if path and path.is_file()
        else ""
    )
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    exceptions = [
        line for line in lines
        if line.startswith((
            "RuntimeError:", "ValueError:", "TimeoutError:",
            "FileNotFoundError:", "ConnectionError:",
        ))
    ]
    if exceptions:
        detail = exceptions[-1]
    elif not lines:
        return "missing_or_empty_log"
    elif "Remote judge unavailable" in lines[-1]:
        detail = lines[-1]
    elif "đang ch" in lines[-1] or "ang ch" in lines[-1]:
        return "interrupted_while_running"
    else:
        detail = lines[-1]

    if "Generation incomplete" in detail and "validator=False" in detail:
        return "validator_generation_incomplete"
    if "minimum witness-verified wrong-candidate pool" in detail:
        return "witness_verified_mutant_pool_insufficient"
    if "minimum verified wrong-candidate pool" in detail:
        return "verified_mutant_pool_insufficient"
    if "reference candidates passed compilation and official samples" in detail:
        return "reference_pool_failed_samples"
    if "Remote judge unavailable" in detail:
        return "remote_judge_unavailable"
    return re.sub(r"[A-Z]:\\[^ ]+", "<path>", detail)[:240]


def metric(result: dict, name: str):
    return (result.get("oracle_metrics") or {}).get(name)


def fmt(value, digits: int = 3) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches", type=Path, default=ROOT / "output" / "batches")
    parser.add_argument(
        "--markdown", type=Path,
        default=ROOT / "output" / "batch-analysis-all.md",
    )
    parser.add_argument(
        "--csv", type=Path,
        default=ROOT / "output" / "batch-analysis-all.csv",
    )
    args = parser.parse_args()

    batches = []
    attempts = []
    for report_path in sorted(args.batches.glob("*/batch-report.json")):
        data = json.loads(report_path.read_text(encoding="utf-8"))
        batch_id = report_path.parent.name
        rows = []
        for position, result in enumerate(data.get("results", []), 1):
            row = {
                "batch": batch_id,
                "position": position,
                "problem": result.get("problem"),
                "status": result.get("status"),
                "tpr": metric(result, "tpr_label_based"),
                "tnr": metric(result, "tnr_label_based"),
                "positive_pass": metric(result, "positive_pass"),
                "positive_evaluable": metric(result, "positive_evaluable"),
                "negative_killed": metric(result, "negative_killed_logic"),
                "negative_evaluable": metric(result, "negative_evaluable"),
                "cases": result.get("cases"),
                "coverage": (result.get("coverage") or {}).get("coverage_ratio"),
                "stop_reason": result.get("stop_reason"),
                "duration_seconds": result.get("duration_seconds"),
                "failure_reason": (
                    failure_reason(result) if result.get("status") == "failed" else ""
                ),
                "report": result.get("report"),
                "log": result.get("log"),
            }
            rows.append(row)
            attempts.append(row)
        measured = [row for row in rows if row["tpr"] is not None and row["tnr"] is not None]
        meet = [row for row in measured if row["tpr"] >= 0.8 and row["tnr"] >= 0.8]
        strong = [row for row in measured if row["tpr"] >= 0.9 and row["tnr"] >= 0.9]
        batches.append({
            "id": batch_id,
            "started_at": data.get("started_at"),
            "finished_at": data.get("finished_at"),
            "planned": data.get("total", 0),
            "completed": data.get("completed", len(rows)),
            "succeeded": data.get("succeeded", 0),
            "failed": data.get("failed", 0),
            "measured": len(measured),
            "meet": len(meet),
            "strong": len(strong),
            "macro_tpr": (
                sum(row["tpr"] for row in measured) / len(measured) if measured else None
            ),
            "macro_tnr": (
                sum(row["tnr"] for row in measured) / len(measured) if measured else None
            ),
        })

    by_problem = defaultdict(list)
    for row in attempts:
        by_problem[row["problem"]].append(row)
    latest = [rows[-1] for rows in by_problem.values()]
    measured = [row for row in attempts if row["tpr"] is not None and row["tnr"] is not None]
    meet = [row for row in measured if row["tpr"] >= 0.8 and row["tnr"] >= 0.8]
    strong = [row for row in measured if row["tpr"] >= 0.9 and row["tnr"] >= 0.9]
    latest_measured = [row for row in latest if row["tpr"] is not None and row["tnr"] is not None]
    latest_meet = [
        row for row in latest_measured if row["tpr"] >= 0.8 and row["tnr"] >= 0.8
    ]
    failure_counts = Counter(
        row["failure_reason"] for row in attempts if row["status"] == "failed"
    )

    lines = [
        "# Báo cáo toàn bộ batch run",
        "",
        f"- Batch: **{len(batches)}**",
        f"- Lượt dự kiến: **{sum(item['planned'] for item in batches)}**",
        f"- Lượt đã kết thúc: **{len(attempts)}**",
        f"- Thành công/có report: **{len(measured)}**",
        f"- Thất bại trước metric: **{sum(row['status'] == 'failed' for row in attempts)}**",
        f"- Lượt đạt TPR và TNR >= 0.8: **{len(meet)}/{len(measured)}**",
        f"- Lượt đạt cả hai >= 0.9: **{len(strong)}/{len(measured)}**",
        f"- Bài duy nhất: **{len(by_problem)}**",
        f"- Kết quả mới nhất đạt cả hai >= 0.8: **{len(latest_meet)}/{len(latest_measured)}** bài đo được",
        "",
        "TPR/TNR dùng metric oracle theo nhãn. Run thất bại không được gán metric 0.",
        "",
        "## Theo batch",
        "",
        "| Batch | Hoàn tất | OK | Lỗi | Đo được | >=0.8 | >=0.9 | TPR TB | TNR TB | Trạng thái |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for batch in batches:
        state = "complete" if batch["finished_at"] else "incomplete"
        lines.append(
            f"| {batch['id']} | {batch['completed']}/{batch['planned']} | "
            f"{batch['succeeded']} | {batch['failed']} | {batch['measured']} | "
            f"{batch['meet']} | {batch['strong']} | {fmt(batch['macro_tpr'])} | "
            f"{fmt(batch['macro_tnr'])} | {state} |"
        )

    lines.extend([
        "",
        "## Nguyên nhân thất bại",
        "",
        "| Nguyên nhân chuẩn hóa | Số lượt |",
        "|---|---:|",
    ])
    for reason, count in failure_counts.most_common():
        lines.append(f"| {reason} | {count} |")

    lines.extend([
        "",
        "## Kết quả mới nhất theo bài",
        "",
        "| Bài | Batch mới nhất | Trạng thái | TPR | TNR | Cases | Coverage | Phân loại |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ])
    for row in sorted(latest, key=lambda item: item["problem"]):
        if row["status"] != "succeeded":
            classification = "failed: " + row["failure_reason"]
        elif row["tpr"] >= 0.9 and row["tnr"] >= 0.9:
            classification = "strong"
        elif row["tpr"] >= 0.8 and row["tnr"] >= 0.8:
            classification = "pass"
        else:
            classification = "below_threshold"
        lines.append(
            f"| {row['problem']} | {row['batch']} | {row['status']} | "
            f"{fmt(row['tpr'])} | {fmt(row['tnr'])} | {fmt(row['cases'])} | "
            f"{fmt(row['coverage'])} | {classification} |"
        )

    lines.extend([
        "",
        "## Mọi lượt chạy",
        "",
        "Chi tiết đầy đủ nằm trong file CSV đi kèm. Mỗi dòng là một problem-run, không phải một bài duy nhất.",
        "",
    ])
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(attempts[0]) if attempts else []
    with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attempts)
    print(json.dumps({
        "batches": len(batches),
        "planned": sum(item["planned"] for item in batches),
        "completed_attempts": len(attempts),
        "measured_attempts": len(measured),
        "meet_0_8": len(meet),
        "strong_0_9": len(strong),
        "unique_problems": len(by_problem),
        "latest_measured": len(latest_measured),
        "latest_meet_0_8": len(latest_meet),
        "markdown": str(args.markdown.resolve()),
        "csv": str(args.csv.resolve()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
