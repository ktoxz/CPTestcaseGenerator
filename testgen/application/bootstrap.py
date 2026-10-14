"""Composition root for concrete provider, judge and oracle adapters."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from testgen.chatgpt import ChatGPTClient
from testgen.claude import ClaudeClient
from testgen.codenet import LocalCodeNetSource, SSHCodeNetSource
from testgen.docker_judge import DockerJudge
from testgen.fallback import FallbackLLMClient
from testgen.native_judge import NativeJudge
from testgen.remote_judge import RemoteDockerJudge
from ..infrastructure.llm.ollama import OllamaClient
from ..generation.cases import CaseGenerationService
from ..generation.solutions import SolutionGenerationService
from .run_pipeline import RunPipeline
from ..infrastructure.file_run_store import FileRunStore
from testgen.retrying_judge import RetryingJudge, retry_setup


def ensure_image(tag: str, dockerfile: Path, root: Path) -> None:
    if subprocess.run(["docker", "image", "inspect", tag], capture_output=True, check=False).returncode == 0:
        return
    subprocess.run(["docker", "build", "-t", tag, "-f", str(dockerfile), str(root / "docker")], check=True)


def build_pipeline(args, parser, settings, judge_settings, catalog, checker, progress,
                   output, problem_oracle_cache, oracle_settings_path, root):
    ROOT = root
    local_error = None
    if args.judge == "native":
        try:
            judge = NativeJudge(
                output / "build",
                catalog,
                args.sandbox_config,
                allow_unsafe=True,
            )
        except RuntimeError as exc:
            parser.error(str(exc))
        progress.log(
            "Judge backend: native Linux (smoke test only; no container isolation)"
        )
    elif args.judge != "remote":
        progress.log("Kiểm tra Docker local")
        docker_probe_started = time.monotonic()
        try:
            subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"],
                           capture_output=True, text=True, timeout=15, check=True)
            progress.latency(
                "startup.docker_probe", time.monotonic() - docker_probe_started,
                backend="local", available=True,
            )
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            local_error = exc
            progress.latency(
                "startup.docker_probe", time.monotonic() - docker_probe_started,
                status="error", backend="local", available=False,
                error=type(exc).__name__,
            )
            progress.log("Docker local không sẵn sàng; sẽ thử KHOI" if args.judge == "auto"
                         else "Docker local không sẵn sàng")
    if args.judge == "local" and local_error:
        parser.error(f"Local Docker Linux engine unavailable: {local_error}")
    if args.judge != "native" and (args.judge == "remote" or local_error):
        try:
            with progress.waiting(
                f"Kiểm tra judge SSH {args.judge_host}",
                component="startup.remote_judge_probe", host=args.judge_host,
            ):
                judge = retry_setup(
                    lambda: RemoteDockerJudge(output / "build", args.judge_host,
                                              catalog, args.sandbox_config),
                    label="kết nối judge KHOI",
                    max_attempts=judge_settings["infra_max_attempts"],
                    delay_seconds=judge_settings["infra_retry_delay_seconds"],
                    progress=progress)
            for image in catalog.images_to_build(include_oracle=args.oracle):
                with progress.waiting(
                    f"Chuẩn bị image {image['tag']} trên KHOI",
                    component="startup.ensure_image", backend="remote",
                    image=image["tag"],
                ):
                    judge.ensure_images([image], ROOT / "docker")
        except RuntimeError as exc:
            parser.error(f"Remote judge unavailable ({args.judge_host}): {exc}")
        progress.log(f"Judge backend: remote ({args.judge_host})")
    elif args.judge != "native":
        for image in catalog.images_to_build(include_oracle=args.oracle):
            with progress.waiting(
                f"Chuẩn bị image local: {image['tag']}",
                component="startup.ensure_image", backend="local",
                image=image["tag"],
            ):
                ensure_image(image["tag"], ROOT / "docker" / image["dockerfile"], ROOT)
        judge = DockerJudge(output / "build", catalog, args.sandbox_config)
        progress.log("Judge backend: local Docker")

    if args.model == "claude":
        client = ClaudeClient(
            max_output_tokens=args.claude_max_tokens,
            model=args.claude_model,
            effort=args.claude_effort,
            timeout_seconds=args.claude_timeout,
            progress=progress,
        )
    elif args.model == "chatgpt":
        client = ChatGPTClient(
            model=args.chatgpt_model,
            timeout_seconds=args.llm_timeout,
            progress=progress,
            raw_output_dir=output / "llm-raw",
        )
    elif args.model == "llama-server":
        client = OllamaClient(
            args.llama_server_url,
            args.llama_server_model,
            progress=progress,
            timeout_seconds=args.llm_timeout,
            raw_output_dir=output / "llm-raw" / "llama-server",
            api_style="openai",
            max_output_tokens=args.llama_server_max_tokens,
            post_request_cooldown_seconds=args.ollama_throttle,
            timeout_cooldown_seconds=args.ollama_timeout_cooldown,
        )
    else:
        primary = OllamaClient(
            args.ollama_url, args.ollama_model,
            progress=progress, timeout_seconds=args.ollama_timeout,
            max_output_tokens=args.ollama_max_tokens,
            raw_output_dir=output / "llm-raw" / "primary",
            post_request_cooldown_seconds=args.ollama_throttle,
            timeout_cooldown_seconds=args.ollama_timeout_cooldown,
        )
        fallback_clients: list[tuple[str, object]] = [
            (f"Ollama/{args.ollama_model}", primary)
        ]
        if (args.llm_fallback and
                args.ollama_fallback_model != args.ollama_model):
            fallback_clients.append((
                f"Ollama/{args.ollama_fallback_model}",
                OllamaClient(
                    args.ollama_url, args.ollama_fallback_model,
                    progress=progress, timeout_seconds=args.ollama_timeout,
                    max_output_tokens=args.ollama_max_tokens,
                    raw_output_dir=output / "llm-raw" / "nemotron",
                    post_request_cooldown_seconds=args.ollama_throttle,
                    timeout_cooldown_seconds=args.ollama_timeout_cooldown,
                ),
            ))
        if args.llm_fallback and args.code_model != "claude":
            fallback_clients.append((
                f"Claude/{args.claude_model}",
                ClaudeClient(
                    max_output_tokens=args.claude_max_tokens,
                    model=args.claude_model,
                    effort=args.claude_effort,
                    timeout_seconds=args.claude_timeout,
                    progress=progress,
                ),
            ))
        client = FallbackLLMClient(fallback_clients, progress=progress)
    if args.model == "claude":
        progress.log(
            f"LLM backend: Claude Code CLI ({args.claude_model}, "
            f"effort={args.claude_effort})"
        )
    elif args.model == "chatgpt":
        progress.log(
            f"LLM backend: ChatGPT login via Codex CLI ({args.chatgpt_model})"
        )
    elif args.model == "llama-server":
        progress.log(
            f"LLM backend: llama-server/{args.llama_server_model} "
            f"({args.llama_server_url}); timeout={args.llm_timeout}s"
        )
    else:
        fallback_label = f"Ollama/{args.ollama_model}"
        if (args.llm_fallback and
                args.ollama_fallback_model != args.ollama_model):
            fallback_label += f" → Ollama/{args.ollama_fallback_model}"
        progress.log(
            f"LLM chain: {fallback_label}"
            + (f" → Claude/{args.claude_model}"
               if args.llm_fallback and args.code_model != "claude" else "")
            + f"; Ollama timeout={args.ollama_timeout}s; "
            f"Claude timeout={args.claude_timeout}s; "
            f"Ollama cooldown={args.ollama_throttle:g}s, "
            f"timeout cooldown={args.ollama_timeout_cooldown:g}s; "
            "Ollama think=false"
        )
    judge = RetryingJudge(
        judge, max_attempts=judge_settings["infra_max_attempts"],
        delay_seconds=judge_settings["infra_retry_delay_seconds"], progress=progress)
    cached_oracle = (
        args.oracle_cache
        or (output / "oracle" if args.resume_oracle and
            (output / "oracle" / "manifest.json").is_file() else None)
        or problem_oracle_cache
    )
    oracle_source = (LocalCodeNetSource(cached_oracle, progress) if cached_oracle else
                     SSHCodeNetSource(ROOT / "scripts" / "export_codenet.py",
                                      args.oracle_host, args.oracle_root, args.runtime_config,
                                      oracle_settings_path, progress)) if args.oracle else None
    if args.oracle and cached_oracle:
        progress.log(f"Oracle source: local cache ({cached_oracle})")
    validator_override = ROOT / "data" / "problems" / args.problem / "validator.py"
    code_client = client
    if args.code_model == "claude" and args.model != "claude":
        code_client = ClaudeClient(
            max_output_tokens=args.claude_max_tokens,
            model=args.claude_model, effort=args.claude_effort,
            timeout_seconds=args.claude_timeout, progress=progress,
        )
        progress.log(f"Code generation backend: Claude/{args.claude_model}")
    store = FileRunStore()
    pipeline = RunPipeline(
        SolutionGenerationService(
            code_client, args.ac, args.wa, catalog,
            analysis_client=client,
            max_rounds=args.solution_generation_rounds,
            retry_delay_seconds=args.solution_generation_retry_delay,
            store=store,
        ),
        CaseGenerationService(client, args.cases_per_round),
        judge, checker,
        oracle_source,
        validator_override if validator_override.exists() else None,
        progress,
        batch_size=judge_settings["batch_size"],
        judge_workers=judge_settings.get("judge_workers", 1),
        compile_workers=judge_settings.get("compile_workers", 1),
        input_repair_attempts=args.input_repair_attempts,
        mutant_replacement_rounds=args.mutant_replacement_rounds,
        mutant_replacement_oversampling=args.mutant_replacement_oversampling,
        mutant_witness_repair_rounds=args.mutant_witness_repair_rounds,
        mutant_witness_candidates=args.mutant_witness_candidates,
        min_iterations=args.min_iterations,
        min_total_cases=args.min_total_cases,
        top_up_rounds=args.top_up_rounds,
        critical_coverage_target=settings.get("critical_coverage_target", 1.0),
        normal_coverage_target=settings.get("normal_coverage_target", 0.9),
        stall_rounds_to_stop=settings.get("stall_rounds_to_stop", 2),
        holdout_fraction=settings.get("holdout_fraction", 0.2),
        minimum_verified_mutants=settings.get("minimum_verified_mutants", 3),
        store=store,
    )
    return pipeline
