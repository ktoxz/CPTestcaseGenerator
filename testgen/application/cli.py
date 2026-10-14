"""CLI argument parsing and single-run invocation; flags remain unchanged."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from testgen.checker import checker_from_profile
from testgen.codenet import find_local_oracle_bundle, validate_codenet_request
from testgen.progress import ConsoleProgress
from testgen.retrying_judge import InfrastructureError
from testgen.runtime import RuntimeCatalog


from ..infrastructure.file_run_store import FileRunStore
from .bootstrap import build_pipeline
from .batch_runner import run_batch
ROOT = Path(__file__).resolve().parents[2]
SAFE_PROBLEM_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")

def main() -> None:
    store = FileRunStore()
    invocation_started = time.monotonic()
    bootstrap = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    bootstrap.add_argument("--config", type=Path, default=ROOT / "config" / "pipeline.json")
    bootstrap.add_argument(
        "--judge-config", type=Path, default=ROOT / "config" / "judge.json"
    )
    initial, _ = bootstrap.parse_known_args()
    settings = json.loads(initial.config.read_text(encoding="utf-8"))
    oracle_settings_path = ROOT / "config" / "oracle.json"
    oracle_settings = json.loads(oracle_settings_path.read_text(encoding="utf-8"))
    judge_settings = json.loads(initial.judge_config.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(
        description=__doc__, parents=[bootstrap], allow_abbrev=False
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--problem", help="Run one safe problem ID, e.g. p00004")
    selection.add_argument(
        "--problems", nargs="+", metavar="ID",
        help="Run an explicit list of problem IDs sequentially",
    )
    selection.add_argument(
        "--problem-range", nargs=2, metavar=("START", "END"),
        help="Run existing pNNNNN problem directories in the inclusive range",
    )
    parser.add_argument("--statement", type=Path, help="Override Markdown statement path")
    parser.add_argument("--oracle", action="store_true", help="Fetch bounded CodeNet AC/WA pool from configured SSH host")
    parser.add_argument("--resume-oracle", type=Path,
                        help="Resume CodeNet judging from an existing output with certified tests")
    parser.add_argument("--oracle-host", default=oracle_settings["host"])
    parser.add_argument("--oracle-root", default=oracle_settings["staging_root"])
    parser.add_argument("--oracle-cache", type=Path, help="Use an already downloaded oracle bundle")
    parser.add_argument("--oracle-limit", type=int, default=oracle_settings["max_per_label"])
    parser.add_argument("--iterations", type=int, default=settings["iterations"], choices=(1, 2, 3))
    parser.add_argument("--ac", type=int, default=settings["correct_candidates"])
    parser.add_argument("--wa", type=int, default=settings["wrong_candidates"])
    parser.add_argument("--solution-generation-rounds", type=int,
                        default=settings.get("solution_generation_rounds", 5),
                        help="Bounded rounds used to fill missing AC references and validator")
    parser.add_argument("--solution-generation-retry-delay", type=float,
                        default=settings.get("solution_generation_retry_delay_seconds", 10),
                        help="Seconds to wait after a generation round makes no progress")
    parser.add_argument("--cases-per-round", type=int, default=settings["cases_per_round"])
    parser.add_argument("--min-iterations", type=int,
                        default=settings.get("min_iterations", 2), choices=(1, 2, 3),
                        help="Minimum refinement rounds before an early stop")
    parser.add_argument("--min-total-cases", type=int,
                        default=settings.get("min_total_cases", 18),
                        help="Minimum certified suite size before an early stop")
    parser.add_argument("--top-up-rounds", type=int,
                        default=settings.get("top_up_rounds", 1), choices=(0, 1, 2, 3, 4),
                        help="Replace invalid or duplicate proposals until accepted quota is met")
    parser.add_argument("--input-repair-attempts", type=int,
                        default=settings.get("input_repair_attempts", 1), choices=(0, 1, 2),
                        help="Retry validator-rejected inputs with the selected LLM")
    parser.add_argument("--mutant-replacement-rounds", type=int,
                        default=settings.get("mutant_replacement_rounds", 1),
                        choices=(0, 1, 2, 3, 4),
                        help="Ordinary mutant replacement rounds; up to 4 extra recovery rounds run if the minimum pool is still missing")
    parser.add_argument("--mutant-replacement-oversampling", type=float,
                        default=settings.get("mutant_replacement_oversampling", 1.0),
                        help="Proposal multiplier used to fill the verified mutant pool (1..3)")
    parser.add_argument("--mutant-witness-repair-rounds", type=int,
                        default=settings.get("mutant_witness_repair_rounds", 1),
                        choices=(0, 1, 2),
                        help="Ask the selected LLM for new counterexamples before replacement")
    parser.add_argument("--mutant-witness-candidates", type=int,
                        default=settings.get("mutant_witness_candidates", 2),
                        choices=(1, 2),
                        help="Candidate witness inputs per mutant (capped at 2)")
    parser.add_argument("--ollama-url", default=settings["ollama_url"])
    parser.add_argument(
        "--model", choices=("ollama", "llama-server", "claude", "chatgpt"),
        default="ollama",
        help=(
            "LLM backend; omit for Ollama, or select llama-server/claude/chatgpt"
        ),
    )
    parser.add_argument(
        "--ollama-model",
        default=settings.get("ollama_model", settings.get("model", "gemma4:31b-cloud")),
        help="Ollama model name when the Ollama backend is selected",
    )
    parser.add_argument(
        "--ollama-fallback-model",
        default=settings.get("ollama_fallback_model", "gemma4:31b-cloud"),
        help="Second Ollama model used only when provider fallback is enabled",
    )
    parser.add_argument(
        "--llm-fallback",
        action=argparse.BooleanOptionalAction,
        default=settings.get("llm_fallback_enabled", False),
        help="Allow fallback from the primary Ollama model to another provider",
    )
    parser.add_argument(
        "--llama-server-url",
        default=settings.get("llama_server_url", "http://localhost:8080"),
        help="OpenAI-compatible llama-server base URL",
    )
    parser.add_argument(
        "--llama-server-model",
        default=settings.get("llama_server_model", "local"),
        help="Model id reported by llama-server /v1/models",
    )
    parser.add_argument(
        "--llama-server-max-tokens", type=int,
        default=settings.get("llama_server_max_tokens", 8192),
        help="Maximum completion tokens per llama-server request",
    )
    parser.add_argument(
        "--llm-timeout", type=int, default=settings.get("llm_timeout_seconds", 50),
        help="Timeout in seconds for non-Ollama backend requests",
    )
    parser.add_argument(
        "--ollama-timeout", type=int,
        default=settings.get("ollama_timeout_seconds", 50),
        help="Hard timeout in seconds for each Ollama request",
    )
    parser.add_argument(
        "--ollama-max-tokens", type=int,
        default=settings.get("ollama_max_tokens", 16384),
        help="Maximum completion tokens per Ollama request",
    )
    parser.add_argument(
        "--ollama-throttle", type=float,
        default=settings.get("ollama_post_request_cooldown_seconds", 5),
        help="Quiet seconds after an Ollama request fully completes",
    )
    parser.add_argument(
        "--ollama-timeout-cooldown", type=float,
        default=settings.get("ollama_timeout_cooldown_seconds", 60),
        help="Seconds to skip an Ollama endpoint after a hard timeout",
    )
    parser.add_argument("--claude-timeout", type=int,
                        default=settings.get("claude_timeout_seconds", 300),
                        help="Timeout in seconds per Claude CLI request (independent of --llm-timeout)")
    parser.add_argument("--claude-max-tokens", type=int,
                        default=settings.get("claude_max_tokens", 32768),
                        help="Maximum output tokens per Claude request")
    parser.add_argument(
        "--claude-model", default=settings.get("claude_model", "fable"),
        help="Claude Code model alias/name when --model claude is selected",
    )
    parser.add_argument(
        "--code-model", choices=("same", "claude"),
        default=settings.get("code_model", "same"),
        help="Backend for AC and WA mutant code; same uses --model. With claude, other tasks use Ollama without Claude fallback",
    )
    parser.add_argument(
        "--claude-effort",
        choices=("low", "medium", "high", "xhigh", "max"),
        default=settings.get("claude_effort", "low"),
        help="Claude reasoning effort; low is the fast pipeline default",
    )
    parser.add_argument(
        "--chatgpt-model", default=settings.get("chatgpt_model", "gpt-5.6-sol"),
        help="Codex model used through the existing ChatGPT login",
    )
    parser.add_argument("--runtime-config", type=Path, default=ROOT / "config" / "runtimes.json")
    parser.add_argument("--sandbox-config", type=Path, default=ROOT / "config" / "sandbox.json")
    parser.add_argument(
        "--judge", choices=("auto", "local", "remote", "native"),
        default=judge_settings["mode"],
        help=(
            "Judge backend; auto uses local Docker then remote, while native is "
            "an explicitly unsafe Linux-only smoke-test mode"
        ),
    )
    parser.add_argument("--judge-host", default=judge_settings["ssh_host"],
                        help="SSH host for remote Windows Docker judge")
    parser.add_argument(
        "--allow-unsafe-native-judge",
        action="store_true",
        help=(
            "Acknowledge that --judge native runs generated code as the current "
            "Linux user and is only suitable for an isolated smoke test"
        ),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--batch-fail-fast", action="store_true",
        help="Stop a batch after its first failed problem (default: continue)",
    )
    raw_args = sys.argv[1:]
    args = parser.parse_args(raw_args)
    if args.llm_timeout < 1:
        parser.error("--llm-timeout must be >= 1")
    if args.ollama_timeout < 1:
        parser.error("--ollama-timeout must be >= 1")
    if not 1 <= args.solution_generation_rounds <= 10:
        parser.error("--solution-generation-rounds must be between 1 and 10")
    if not 0 <= args.solution_generation_retry_delay <= 300:
        parser.error("--solution-generation-retry-delay must be between 0 and 300")
    if args.ollama_max_tokens < 256:
        parser.error("--ollama-max-tokens must be >= 256")
    if args.claude_max_tokens < 1:
        parser.error("--claude-max-tokens must be >= 1")
    if args.claude_timeout < 1:
        parser.error("--claude-timeout must be >= 1")
    if args.judge == "native" and not args.allow_unsafe_native_judge:
        parser.error("--judge native requires --allow-unsafe-native-judge")
    if args.problem_range or args.problems:
        run_batch(args, raw_args, parser, root=ROOT)
        return
    if args.resume_oracle and not args.oracle:
        parser.error("--resume-oracle requires --oracle")
    if not SAFE_PROBLEM_ID.fullmatch(args.problem):
        parser.error("--problem must be a safe ID (letters, digits, underscore or hyphen)")
    if args.oracle and not 1 <= args.oracle_limit <= oracle_settings["max_per_label"]:
        parser.error(
            f"--oracle-limit must be between 1 and "
            f"{oracle_settings['max_per_label']}"
        )
    problem_oracle_cache = find_local_oracle_bundle(
        ROOT / "data" / "problems", args.problem
    )
    if args.oracle and args.oracle_cache is None and problem_oracle_cache is None:
        try:
            validate_codenet_request(
                args.problem, args.oracle_limit, oracle_settings["max_per_label"]
            )
        except ValueError as error:
            parser.error(
                f"{error}. Provide --oracle-cache or add "
                f"data/problems/{args.problem}/oracle/manifest.json."
            )
    statement_path = args.statement or ROOT / "data" / "problems" / args.problem / "statement.md"
    if not statement_path.is_file():
        parser.error(f"Missing statement: {statement_path}")
    profile_path = ROOT / "data" / "problems" / args.problem / "checker.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8")) if profile_path.exists() else settings["default_checker"]
    if profile.get("kind") == "PYTHON_SCRIPT":
        raw_script = profile.get("script")
        if not isinstance(raw_script, str) or not raw_script.strip():
            parser.error(f"Invalid PYTHON_SCRIPT profile: {profile_path}")
        relative_script = Path(raw_script)
        if relative_script.is_absolute():
            parser.error("PYTHON_SCRIPT path must be relative to checker.json")
        checker_root = profile_path.parent.resolve()
        script_path = (checker_root / relative_script).resolve()
        if not script_path.is_relative_to(checker_root) or not script_path.is_file():
            parser.error(
                f"PYTHON_SCRIPT must name an existing file inside {checker_root}"
            )
        profile = {**profile, "script": str(script_path)}
    checker = checker_from_profile(profile)
    catalog = RuntimeCatalog(args.runtime_config)
    progress = ConsoleProgress()
    progress.log(f"Bài {args.problem}: khởi tạo; output={args.output or 'mặc định'}")
    output = args.resume_oracle or args.output or ROOT / "output" / args.problem / datetime.now().strftime("%Y%m%d-%H%M%S")
    output.mkdir(parents=True, exist_ok=True)
    progress.bind_latency_log(output / "latency.jsonl")
    store.write_text(output / "statement.md", statement_path.read_text(encoding="utf-8"), encoding="utf-8")
    run_config_path = output / (
        "resume-config.json" if args.resume_oracle else "run-config.json"
    )
    store.write_json(run_config_path, {
            "problem": args.problem,
            "statement": str(statement_path),
            "pipeline_config": str(args.config),
            "judge_config": str(args.judge_config),
            "runtime_config": str(args.runtime_config),
            "sandbox_config": str(args.sandbox_config),
            "model": args.model,
            "code_model": args.model if args.code_model == "same" else args.code_model,
            "code_claude_model": args.claude_model if args.code_model == "claude" else None,
            "ollama_model": args.ollama_model if args.model == "ollama" else None,
            "ollama_url": args.ollama_url if args.model == "ollama" else None,
            "ollama_fallback_model": (
                args.ollama_fallback_model if args.model == "ollama" else None
            ),
            "llm_fallback_enabled": (
                args.llm_fallback if args.model == "ollama" else False
            ),
            "ollama_think": False if args.model == "ollama" else None,
            "llama_server_url": (
                args.llama_server_url if args.model == "llama-server" else None
            ),
            "llama_server_model": (
                args.llama_server_model if args.model == "llama-server" else None
            ),
            "llama_server_max_tokens": (
                args.llama_server_max_tokens
                if args.model == "llama-server" else None
            ),
            "llm_timeout_seconds": args.llm_timeout,
            "ollama_timeout_seconds": args.ollama_timeout,
            "ollama_max_tokens": args.ollama_max_tokens,
            "ollama_post_request_cooldown_seconds": args.ollama_throttle,
            "ollama_timeout_cooldown_seconds": args.ollama_timeout_cooldown,
            "llm_fallback_chain": (
                [args.ollama_model]
                + ([args.ollama_fallback_model]
                   if args.llm_fallback and
                   args.ollama_fallback_model != args.ollama_model else [])
                + ([args.claude_model]
                   if args.llm_fallback and args.code_model != "claude" else [])
                if args.model == "ollama" else [
                    args.llama_server_model
                    if args.model == "llama-server" else args.model
                ]
            ),
            "claude_model": (
                args.claude_model
                if args.model == "claude" or args.code_model == "claude" else None
            ),
            "claude_effort": (
                args.claude_effort
                if args.model == "claude" or args.code_model == "claude" else None
            ),
            "claude_max_tokens": args.claude_max_tokens,
            "claude_timeout_seconds": args.claude_timeout,
            "chatgpt_model": args.chatgpt_model if args.model == "chatgpt" else None,
            "judge": args.judge,
            "judge_host": args.judge_host if args.judge in {"auto", "remote"} else None,
            "unsafe_native_judge_acknowledged": (
                args.allow_unsafe_native_judge if args.judge == "native" else None
            ),
            "oracle": args.oracle,
            "oracle_limit": args.oracle_limit,
            "oracle_cache": str(args.oracle_cache or problem_oracle_cache)
            if args.oracle and (args.oracle_cache or problem_oracle_cache) else None,
            "correct_candidates": args.ac,
            "wrong_candidates": args.wa,
            "solution_generation_rounds": args.solution_generation_rounds,
            "solution_generation_retry_delay_seconds": args.solution_generation_retry_delay,
            "iterations": args.iterations,
            "cases_per_round": args.cases_per_round,
            "min_iterations": args.min_iterations,
            "min_total_cases": args.min_total_cases,
            "top_up_rounds": args.top_up_rounds,
            "input_repair_attempts": args.input_repair_attempts,
            "mutant_replacement_rounds": args.mutant_replacement_rounds,
            "mutant_replacement_oversampling": args.mutant_replacement_oversampling,
            "mutant_witness_repair_rounds": args.mutant_witness_repair_rounds,
            "mutant_witness_candidates": args.mutant_witness_candidates,
            "judge_workers": judge_settings.get("judge_workers", 1),
            "compile_workers": judge_settings.get("compile_workers", 1),
            "batch_size": judge_settings["batch_size"],
        })

    pipeline = build_pipeline(
        args, parser, settings, judge_settings, catalog, checker,
        progress, output, problem_oracle_cache, oracle_settings_path, ROOT,
        auto_checker=not profile_path.exists(),
        auto_sandbox=args.sandbox_config.resolve() == (ROOT / "config" / "sandbox.json").resolve(),
    )
    try:
        with progress.waiting(
            "Toàn bộ pipeline", component="pipeline.total",
            problem_id=args.problem, resume_oracle=bool(args.resume_oracle),
        ):
            statement_text = statement_path.read_text(encoding="utf-8")
            report = (pipeline.resume_oracle(
                          args.problem, output, args.oracle_limit, statement_text)
                      if args.resume_oracle else
                      pipeline.run(args.problem, statement_text,
                                   output, iterations=args.iterations,
                                   oracle_limit=args.oracle_limit, use_oracle=args.oracle,
                                   started_at=invocation_started))
        report["latency"] = {
            "log": "latency.jsonl",
            "summary": progress.latency_summary(),
        }
        store.write_json(output / "report.json", report)
    except InfrastructureError as exc:
        raise SystemExit(f"Judge infrastructure failed; partial output: {output}\n{exc}") from None
    print(json.dumps({"report": str(output / "report.json"), "cases": len(report["cases"]),
                      "llm_metrics": report["llm_metrics"],
                      "llm_holdout_metrics": report.get("llm_holdout_metrics"),
                      "coverage": report.get("coverage"),
                      "stop_reason": report.get("stop_reason"),
                      "oracle_metrics": report.get("oracle_metrics")}, ensure_ascii=False, indent=2))


