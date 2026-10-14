"""Untrusted solution execution inside a resource-limited, networkless container."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import uuid
from pathlib import Path

from .domain import Judge, Result, Solution
from .runtime import RuntimeCatalog


class DockerJudge(Judge):
    def __init__(self, build_root: Path, catalog: RuntimeCatalog | None = None,
                 sandbox_config: Path | None = None):
        self.build_root = build_root.resolve()
        self.build_root.mkdir(parents=True, exist_ok=True)
        self.run_id = hashlib.sha256(str(self.build_root).encode()).hexdigest()[:20]
        self.catalog = catalog or RuntimeCatalog()
        config_path = sandbox_config or Path(__file__).resolve().parents[1] / "config" / "sandbox.json"
        self.limits = json.loads(config_path.read_text(encoding="utf-8"))
        self._compiled: dict[str, tuple[Path, str, str]] = {}

    def apply_sandbox_spec(self, spec: dict) -> None:
        """Apply bounded per-problem limits extracted before any compilation."""
        time_limit = min(60.0, max(0.1, float(spec["time_limit_seconds"])))
        memory_limit = min(4096, max(32, int(spec["memory_limit_mb"])))
        self.limits["run_timeout_seconds"] = max(1, int(time_limit * 1.5 + 0.999))
        self.limits["memory"] = f"{memory_limit}m"

    def _run(self, image: str, source: Path, work: Path, command: str,
             input_text: str = "", *, timeout: int) -> tuple[int, str, str, bool]:
        container_name = f"tg-{self.run_id[:10]}-{uuid.uuid4().hex[:12]}"
        args = [
            "docker", "run", "--rm", "--name", container_name,
            "--label", "testgen.owner=Final_TestcaseGenerator",
            "--label", f"testgen.run={self.run_id}",
            "-i", "--network", "none", "--read-only",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--pids-limit", str(self.limits["pids_limit"]),
            "--memory", self.limits["memory"], "--memory-swap", self.limits["memory"],
            "--cpus", self.limits["cpus"],
            "--tmpfs", f"/tmp:rw,nosuid,size={self.limits['tmpfs_size']}",
            "--mount", f"type=bind,src={source.resolve()},dst=/src,readonly",
            "--mount", f"type=bind,src={work.resolve()},dst=/work",
            image, "timeout", "-s", "TERM", "-k", "1s", f"{timeout}s",
            "sh", "-lc", command,
        ]
        try:
            proc = subprocess.run(args, input=input_text.encode("utf-8"),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  timeout=timeout + self.limits["docker_startup_grace_seconds"],
                                  check=False)
        except subprocess.TimeoutExpired:
            try:
                cleanup = subprocess.run(["docker", "rm", "-f", container_name],
                                         capture_output=True, text=True, check=False,
                                         timeout=self.limits["container_cleanup_timeout_seconds"])
                detail = cleanup.stderr.strip() or cleanup.stdout.strip()
            except (OSError, subprocess.TimeoutExpired) as exc:
                detail = str(exc)
            return (125, "", f"Docker invocation timed out (not code TLE); "
                    f"cleanup {container_name}: {detail}", False)
        except OSError as exc:
            return 125, "", str(exc), False
        stdout = proc.stdout.decode("utf-8", errors="replace")
        stderr = proc.stderr.decode("utf-8", errors="replace")
        return (proc.returncode,
                stdout[:self.limits["stdout_limit_bytes"]],
                stderr[:self.limits["stderr_limit_bytes"]], proc.returncode == 124)

    def compile(self, solution: Solution) -> Result:
        digest = hashlib.sha256(solution.source.read_bytes()).hexdigest()[:16]
        work = self.build_root / f"{solution.id}-{digest}"
        source = work / "source"
        source.mkdir(parents=True, exist_ok=True)
        try:
            runtime = self.catalog.resolve(solution)
        except ValueError as exc:
            return Result(solution.id, "INFRA", stderr=str(exc))
        image = self.catalog.images[runtime.image]["tag"]
        shutil.copyfile(solution.source, source / runtime.source_file)
        code, _out, err, timed_out = self._run(
            image, source, work, runtime.compile,
            timeout=self.limits["compile_timeout_seconds"])
        if timed_out:
            return Result(solution.id, "INFRA", stderr="compile timeout")
        if code == 125:
            return Result(solution.id, "INFRA", stderr=err)
        if code != 0:
            return Result(solution.id, "CE", stderr=err)
        self._compiled[solution.id] = (work, image, runtime.execute)
        return Result(solution.id, "PASS")

    def execute(self, solution: Solution, case_id: str, input_text: str) -> Result:
        if solution.id not in self._compiled:
            return Result(solution.id, "INFRA", case_id, stderr="solution not compiled")
        work, image, command = self._compiled[solution.id]
        code, out, err, timed_out = self._run(image, work / "source", work, command,
                                              input_text=input_text,
                                              timeout=self.limits["run_timeout_seconds"])
        if timed_out:
            return Result(solution.id, "TLE", case_id, out, err)
        if code == 125:
            return Result(solution.id, "INFRA", case_id, out, err)
        return Result(solution.id, "PASS" if code == 0 else "RE", case_id, out, err)
