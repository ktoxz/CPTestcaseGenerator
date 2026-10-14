"""Best-effort native Linux judge for constrained notebook environments.

This backend exists for Kaggle smoke tests, where a Docker daemon is normally
not available.  It applies process resource limits and a scrubbed environment,
but it is not a security boundary: submissions still run as the notebook user.
Use DockerJudge or RemoteDockerJudge for measurements involving untrusted code.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import signal
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path

from .domain import Judge, Result, Solution
from .runtime import RuntimeCatalog, RuntimeSpec


def _bytes_from_limit(value: str) -> int:
    units = {
        "": 1,
        "b": 1,
        "k": 1024,
        "kb": 1024,
        "m": 1024**2,
        "mb": 1024**2,
        "g": 1024**3,
        "gb": 1024**3,
    }
    normalized = str(value).strip().lower()
    number = normalized.rstrip("abcdefghijklmnopqrstuvwxyz")
    unit = normalized[len(number):]
    if not number or unit not in units:
        raise ValueError(f"Unsupported memory limit: {value!r}")
    return int(float(number) * units[unit])


@dataclass(frozen=True)
class _NativeArtifact:
    root: Path
    runtime: RuntimeSpec


class NativeJudge(Judge):
    """Compile and execute directly on Linux with best-effort rlimits.

    Deliberately Linux-only.  The explicit ``allow_unsafe`` acknowledgement is
    required so callers cannot silently downgrade from the container judge.
    """

    def __init__(
        self,
        build_root: Path,
        catalog: RuntimeCatalog | None = None,
        sandbox_config: Path | None = None,
        *,
        allow_unsafe: bool = False,
    ):
        if sys.platform != "linux":
            raise RuntimeError("NativeJudge is supported only on Linux")
        if not allow_unsafe:
            raise RuntimeError(
                "NativeJudge is not a security boundary; pass allow_unsafe=True "
                "only for an isolated Kaggle smoke test"
            )
        import json

        self.build_root = build_root.resolve()
        self.build_root.mkdir(parents=True, exist_ok=True)
        self.catalog = catalog or RuntimeCatalog()
        config_path = (
            sandbox_config
            or Path(__file__).resolve().parents[1] / "config" / "sandbox.json"
        )
        self.limits = json.loads(config_path.read_text(encoding="utf-8"))
        self.memory_bytes = _bytes_from_limit(self.limits["memory"])
        self.prlimit = shutil.which("prlimit")
        if self.prlimit is None:
            raise RuntimeError(
                "NativeJudge requires the Linux util-linux 'prlimit' command"
            )
        self._compiled: dict[str, _NativeArtifact] = {}

    def apply_sandbox_spec(self, spec: dict) -> None:
        time_limit = min(60.0, max(0.1, float(spec["time_limit_seconds"])))
        memory_limit = min(4096, max(32, int(spec["memory_limit_mb"])))
        self.limits["run_timeout_seconds"] = max(1, int(time_limit * 1.5 + 0.999))
        self.limits["memory"] = f"{memory_limit}m"
        self.memory_bytes = memory_limit * 1024**2

    @staticmethod
    def _tool(runtime: RuntimeSpec) -> str:
        return {
            "c": "gcc",
            "cpp20": "g++",
            "cpp17": "g++",
            "cpp14": "g++",
            "cpp11": "g++",
            "cpp98": "g++",
            "java": "javac",
            "python3": sys.executable,
            "python2": "python2",
        }.get(runtime.id, "")

    @staticmethod
    def _compile_command(runtime: RuntimeSpec, source: Path, work: Path) -> list[str]:
        if runtime.id == "c":
            return ["gcc", "-std=gnu11", "-O2", str(source), "-lm", "-o", str(work / "main")]
        if runtime.id.startswith("cpp"):
            standard = {
                "cpp20": "gnu++20",
                "cpp17": "gnu++17",
                "cpp14": "gnu++14",
                "cpp11": "gnu++11",
                "cpp98": "gnu++98",
            }[runtime.id]
            return ["g++", f"-std={standard}", "-O2", str(source), "-o", str(work / "main")]
        if runtime.id == "java":
            return ["javac", "-encoding", "UTF-8", "-d", str(work), str(source)]
        if runtime.id == "python3":
            return [sys.executable, "-m", "py_compile", str(source)]
        if runtime.id == "python2":
            return ["python2", "-m", "py_compile", str(source)]
        raise ValueError(f"Native judge does not support runtime {runtime.id!r}")

    @staticmethod
    def _execute_command(runtime: RuntimeSpec, run_root: Path) -> list[str]:
        if runtime.id in {"c", "cpp17", "cpp14", "cpp11", "cpp98"}:
            return [str(run_root / "main")]
        if runtime.id == "java":
            return ["java", "-Xmx192m", "-cp", str(run_root), "Main"]
        if runtime.id == "python3":
            return [sys.executable, "-I", str(run_root / "main.py")]
        if runtime.id == "python2":
            return ["python2", str(run_root / "main.py")]
        raise ValueError(f"Native judge does not support runtime {runtime.id!r}")

    @staticmethod
    def _clean_environment() -> dict[str, str]:
        # Do not pass notebook/API secrets to generated programs.
        return {
            "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "HOME": "/nonexistent",
            "PYTHONNOUSERSITE": "1",
        }

    def _limited_command(self, command: list[str]) -> list[str]:
        cpu_seconds = max(1, int(self.limits["run_timeout_seconds"]) + 1)
        output_limit = max(
            int(self.limits["stdout_limit_bytes"]),
            int(self.limits["stderr_limit_bytes"]),
        )
        return [
            self.prlimit,
            f"--cpu={cpu_seconds}:{cpu_seconds}",
            f"--as={self.memory_bytes}:{self.memory_bytes}",
            f"--nproc={self.limits['pids_limit']}:{self.limits['pids_limit']}",
            "--nofile=64:64",
            f"--fsize={output_limit}:{output_limit}",
            "--",
            *command,
        ]

    def compile(self, solution: Solution) -> Result:
        try:
            runtime = self.catalog.resolve(solution)
            tool = self._tool(runtime)
            if not tool or shutil.which(tool) is None:
                return Result(
                    solution.id,
                    "INFRA",
                    stderr=f"Required native runtime tool is unavailable: {tool or runtime.id}",
                )
            digest = hashlib.sha256(solution.source.read_bytes()).hexdigest()[:16]
            work = self.build_root / f"{solution.id}-{digest}"
            source_root = work / "source"
            source_root.mkdir(parents=True, exist_ok=True)
            source = source_root / runtime.source_file
            shutil.copyfile(solution.source, source)
            command = self._compile_command(runtime, source, work)
            completed = subprocess.run(
                command,
                cwd=work,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.limits["compile_timeout_seconds"],
                env=self._clean_environment(),
                check=False,
            )
        except subprocess.TimeoutExpired:
            return Result(solution.id, "INFRA", stderr="native compile timeout")
        except (OSError, ValueError) as error:
            return Result(solution.id, "INFRA", stderr=str(error))
        stderr = completed.stderr[: self.limits["stderr_limit_bytes"]]
        if completed.returncode != 0:
            return Result(solution.id, "CE", stderr=stderr)
        self._compiled[solution.id] = _NativeArtifact(work, runtime)
        return Result(solution.id, "PASS")

    def _copy_artifact(self, artifact: _NativeArtifact, run_root: Path) -> None:
        runtime = artifact.runtime
        if runtime.id in {"c", "cpp17", "cpp14", "cpp11", "cpp98"}:
            shutil.copy2(artifact.root / "main", run_root / "main")
        elif runtime.id == "java":
            for path in artifact.root.glob("*.class"):
                shutil.copy2(path, run_root / path.name)
        else:
            shutil.copy2(
                artifact.root / "source" / runtime.source_file,
                run_root / runtime.source_file,
            )

    def execute(self, solution: Solution, case_id: str, input_text: str) -> Result:
        artifact = self._compiled.get(solution.id)
        if artifact is None:
            return Result(solution.id, "INFRA", case_id, stderr="solution not compiled")
        runs_root = artifact.root / "runs"
        run_root = runs_root / uuid.uuid4().hex
        run_root.mkdir(parents=True, exist_ok=False)
        stdout_path = run_root / "stdout.txt"
        stderr_path = run_root / "stderr.txt"
        timed_out = False
        return_code = 125
        try:
            self._copy_artifact(artifact, run_root)
            command = self._limited_command(
                self._execute_command(artifact.runtime, run_root)
            )
            with stdout_path.open("wb") as stdout_file, stderr_path.open("wb") as stderr_file:
                process = subprocess.Popen(
                    command,
                    cwd=run_root,
                    stdin=subprocess.PIPE,
                    stdout=stdout_file,
                    stderr=stderr_file,
                    env=self._clean_environment(),
                    start_new_session=True,
                )
                try:
                    process.communicate(
                        input=input_text.encode("utf-8"),
                        timeout=self.limits["run_timeout_seconds"],
                    )
                except subprocess.TimeoutExpired:
                    timed_out = True
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait(timeout=2)
                return_code = process.returncode
            stdout = stdout_path.read_text(
                encoding="utf-8", errors="replace"
            )[: self.limits["stdout_limit_bytes"]]
            stderr = stderr_path.read_text(
                encoding="utf-8", errors="replace"
            )[: self.limits["stderr_limit_bytes"]]
        except (OSError, subprocess.SubprocessError, ValueError) as error:
            return Result(solution.id, "INFRA", case_id, stderr=str(error))
        finally:
            shutil.rmtree(run_root, ignore_errors=True)
        if timed_out:
            return Result(solution.id, "TLE", case_id, stdout, stderr)
        return Result(
            solution.id,
            "PASS" if return_code == 0 else "RE",
            case_id,
            stdout,
            stderr,
        )
