"""Measure Claude code-generation latency without running the full pipeline."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from testgen.claude import ClaudeClient
from testgen.domain import Solution
from testgen.generation.solutions import SolutionGenerationService
from testgen.llm_contract import LLMRequest, TaskType
from testgen.progress import ConsoleProgress

class ValidatorStub:
    """Keep the benchmark focused on code requests to the selected model."""

    def ask(self, request: LLMRequest) -> dict:
        if request.task_type is TaskType.GENERATE_VALIDATOR:
            return {
                "validator_python": "import sys\nsys.stdin.read()\n",
                "warnings": ["Benchmark-only validator stub."],
            }
        if request.task_type is TaskType.GENERATE_WITNESSES:
            return {
                "witnesses": [
                    {"index": index, "input": "1\n"} for index in range(16)
                ]
            }
        raise AssertionError(f"Unexpected benchmark request: {request.task_type}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problem", default="p02586")
    parser.add_argument("--model", default="haiku")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--max-output-tokens", type=int, default=32768)
    parser.add_argument("--ac", type=int, default=3)
    parser.add_argument("--wa", type=int, default=5)
    parser.add_argument("--skip-ac", action="store_true")
    parser.add_argument("--test-model", type=Path)
    parser.add_argument(
        "--reference",
        type=Path,
        help="Verified AC source used to benchmark WA even if AC generation fails",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "output" / "experiments" / "code-model-latency",
    )
    args = parser.parse_args()

    problem_root = ROOT / "data" / "problems" / args.problem
    statement = (problem_root / "statement.md").read_text(encoding="utf-8")
    if args.test_model:
        test_model = json.loads(args.test_model.read_text(encoding="utf-8"))
    else:
        test_model = {
            "interpretation": "Use the problem statement as authoritative.",
            "constraints": [],
            "correct_strategies": [],
            "validator_requirements": [],
            "warnings": [],
        }

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    output = args.output / f"{args.problem}-{args.model}-{run_id}"
    generated = output / "generated"
    output.mkdir(parents=True, exist_ok=False)

    progress = ConsoleProgress(interval_seconds=15)
    progress.bind_latency_log(output / "latency.jsonl")
    claude = ClaudeClient(
        model=args.model,
        effort="low",
        max_output_tokens=args.max_output_tokens,
        timeout_seconds=args.timeout,
        json_attempts=1,
        progress=progress,
    )

    report = {
        "problem": args.problem,
        "model": args.model,
        "timeout_seconds": args.timeout,
        "requested_ac": args.ac,
        "requested_wa": args.wa,
        "ac": {},
        "wa": {},
    }
    references = []
    if args.skip_ac:
        report["ac"] = {"status": "skipped"}
    else:
        ac_started = time.monotonic()
        try:
            references = SolutionGenerationService(
                claude,
                ac_count=args.ac,
                wa_count=args.wa,
                analysis_client=ValidatorStub(),
                max_rounds=1,
                retry_delay_seconds=0,
            ).generate_with_model(statement, test_model, generated)
            report["ac"] = {
                "status": "ok",
                "wall_ms": round((time.monotonic() - ac_started) * 1000, 3),
                "count": len(references),
            }
        except Exception as error:  # Preserve transport/model failure measurements.
            report["ac"] = {
                "status": "error",
                "wall_ms": round((time.monotonic() - ac_started) * 1000, 3),
                "error": f"{type(error).__name__}: {error}",
            }

    wa_references = references
    if not wa_references and args.reference:
        language_by_suffix = {
            ".py": "Python", ".cpp": "C++", ".cc": "C++",
            ".c": "C", ".java": "Java",
        }
        language = language_by_suffix.get(args.reference.suffix.lower())
        if language is None:
            raise ValueError(f"Unsupported reference suffix: {args.reference.suffix}")
        copied_reference = generated / f"benchmark-reference{args.reference.suffix.lower()}"
        copied_reference.parent.mkdir(parents=True, exist_ok=True)
        copied_reference.write_text(
            args.reference.read_text(encoding="utf-8"), encoding="utf-8",
        )
        wa_references = [Solution(
            "benchmark-reference", "candidate_ac", language, copied_reference,
            strategy_id="verified-codenet-reference",
        )]
        report["wa_reference"] = str(args.reference)

    if wa_references:
        wa_started = time.monotonic()
        try:
            mutants, generation_feedback = SolutionGenerationService(
                claude,
                ac_count=args.ac,
                wa_count=args.wa,
                analysis_client=ValidatorStub(),
                max_rounds=1,
                retry_delay_seconds=0,
            )._request_wrong_batch(
                statement, generated,
                request_count=args.wa,
                needed_count=args.wa,
                rejected=[],
                existing=wa_references,
                round_number=0,
                request_index=1,
            )
            report["wa"] = {
                "status": "ok",
                "wall_ms": round((time.monotonic() - wa_started) * 1000, 3),
                "count": len(mutants),
                "generation_feedback": generation_feedback,
            }
        except Exception as error:
            report["wa"] = {
                "status": "error",
                "wall_ms": round((time.monotonic() - wa_started) * 1000, 3),
                "error": f"{type(error).__name__}: {error}",
            }
    else:
        report["wa"] = {
            "status": "skipped",
            "reason": "No AC candidate was produced for the parent mutation.",
        }

    report["latency_summary"] = progress.latency_summary()
    (output / "benchmark.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), **report}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
