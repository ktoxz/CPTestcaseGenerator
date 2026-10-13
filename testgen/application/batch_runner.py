"""Sequential batch execution with an independent report per problem."""
from __future__ import annotations

from ..infrastructure.file_run_store import FileRunStore
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


SAFE_PROBLEM_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")
RANGE_PROBLEM_ID = re.compile(r"p(\d{5})")

def discover_problem_range(problems_root: Path, start: str, end: str) -> list[str]:
    """Return existing pNNNNN problem directories in the inclusive numeric range."""
    start_match = RANGE_PROBLEM_ID.fullmatch(start)
    end_match = RANGE_PROBLEM_ID.fullmatch(end)
    if not start_match or not end_match:
        raise ValueError("range endpoints must use the pNNNNN format")
    start_number = int(start_match.group(1))
    end_number = int(end_match.group(1))
    if start_number > end_number:
        raise ValueError("range start must not be greater than range end")
    return [
        path.name
        for path in sorted(problems_root.iterdir(), key=lambda item: item.name)
        if path.is_dir()
        and (match := RANGE_PROBLEM_ID.fullmatch(path.name)) is not None
        and start_number <= int(match.group(1)) <= end_number
        and (path / "statement.md").is_file()
    ]


def child_cli_args(raw_args: list[str]) -> list[str]:
    """Remove batch selection/output flags while preserving ordinary run options."""
    result: list[str] = []
    index = 0
    while index < len(raw_args):
        token = raw_args[index]
        if token == "--problem-range":
            index += 3
            continue
        if token == "--problems":
            index += 1
            while index < len(raw_args) and not raw_args[index].startswith("-"):
                index += 1
            continue
        if token in {"--batch-fail-fast"}:
            index += 1
            continue
        if token == "--output":
            index += 2
            continue
        if token.startswith("--output="):
            index += 1
            continue
        result.append(token)
        index += 1
    return result


def write_batch_report(path: Path, report: dict) -> None:
    FileRunStore().write_json(path, report)


def run_batch(args: argparse.Namespace, raw_args: list[str], parser: argparse.ArgumentParser, *, root: Path) -> None:
    ROOT = root
    if args.statement or args.resume_oracle or args.oracle_cache:
        parser.error(
            "--statement, --resume-oracle and --oracle-cache only apply to a single problem"
        )
    if args.problem_range:
        try:
            problems = discover_problem_range(
                ROOT / "data" / "problems", *args.problem_range
            )
        except ValueError as error:
            parser.error(str(error))
        selection = {
            "kind": "range",
            "start": args.problem_range[0],
            "end": args.problem_range[1],
        }
    else:
        problems = args.problems
        selection = {"kind": "list", "problems": problems}
        invalid = [problem for problem in problems if not SAFE_PROBLEM_ID.fullmatch(problem)]
        if invalid:
            parser.error(f"unsafe problem ID(s): {', '.join(invalid)}")
        missing = [
            problem for problem in problems
            if not (ROOT / "data" / "problems" / problem / "statement.md").is_file()
        ]
        if missing:
            parser.error(f"missing statement for: {', '.join(missing)}")
    if not problems:
        parser.error("no problem directories with statement.md were found in the selection")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_output = args.output or ROOT / "output" / "batches" / timestamp
    batch_output.mkdir(parents=True, exist_ok=True)
    logs_dir = batch_output / "logs"
    logs_dir.mkdir(exist_ok=True)
    report_path = batch_output / "batch-report.json"
    batch_report: dict = {
        "selection": selection,
        "started_at": datetime.now().astimezone().isoformat(),
        "finished_at": None,
        "output": str(batch_output),
        "total": len(problems),
        "completed": 0,
        "succeeded": 0,
        "failed": 0,
        "results": [],
    }
    write_batch_report(report_path, batch_report)
    common_args = child_cli_args(raw_args)

    print(
        f"Batch: {len(problems)} bài; output={batch_output}",
        flush=True,
    )
    for position, problem in enumerate(problems, start=1):
        problem_output = batch_output / "problems" / problem
        problem_output.parent.mkdir(parents=True, exist_ok=True)
        log_path = logs_dir / f"{problem}.log"
        command = [
            sys.executable,
            str(ROOT / "main.py"),
            *common_args,
            "--problem",
            problem,
            "--output",
            str(problem_output),
        ]
        print(f"[{position}/{len(problems)}] Starting {problem}", flush=True)
        started = time.monotonic()
        with log_path.open("w", encoding="utf-8") as log_file:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
        duration = round(time.monotonic() - started, 3)
        problem_report_path = problem_output / "report.json"
        result: dict = {
            "problem": problem,
            "status": "succeeded" if completed.returncode == 0 else "failed",
            "exit_code": completed.returncode,
            "duration_seconds": duration,
            "log": str(log_path),
            "report": str(problem_report_path) if problem_report_path.is_file() else None,
        }
        if problem_report_path.is_file():
            problem_report = json.loads(problem_report_path.read_text(encoding="utf-8"))
            result.update({
                "cases": len(problem_report.get("cases", [])),
                "stop_reason": problem_report.get("stop_reason"),
                "llm_metrics": problem_report.get("llm_metrics"),
                "llm_holdout_metrics": problem_report.get("llm_holdout_metrics"),
                "coverage": problem_report.get("coverage"),
                "oracle_metrics": problem_report.get("oracle_metrics"),
                "generation_latency": problem_report.get("generation_latency"),
            })
        batch_report["results"].append(result)
        batch_report["completed"] += 1
        batch_report[result["status"]] += 1
        write_batch_report(report_path, batch_report)
        print(
            f"[{position}/{len(problems)}] {problem}: {result['status']} "
            f"({duration:.1f}s); log={log_path}",
            flush=True,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        if completed.returncode != 0 and args.batch_fail_fast:
            break

    batch_report["finished_at"] = datetime.now().astimezone().isoformat()
    write_batch_report(report_path, batch_report)
    print(json.dumps({
        "batch_report": str(report_path),
        "total": batch_report["total"],
        "completed": batch_report["completed"],
        "succeeded": batch_report["succeeded"],
        "failed": batch_report["failed"],
    }, ensure_ascii=False, indent=2))
    if batch_report["failed"]:
        raise SystemExit(1)


