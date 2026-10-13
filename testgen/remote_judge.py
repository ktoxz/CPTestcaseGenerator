"""Run the existing Docker judge on a Windows host reached over SSH."""

from __future__ import annotations

import base64
import hashlib
import json
import subprocess
from pathlib import Path

from .docker_judge import DockerJudge
from .domain import Result, Solution
from .runtime import RuntimeCatalog


WORKER = Path(__file__).resolve().parents[1] / "scripts" / "remote_judge_worker.py"
REMOTE_WORKER = ".testgen_remote_judge_worker.py"


class RemoteDockerJudge(DockerJudge):
    def __init__(self, build_root: Path, host: str, catalog: RuntimeCatalog | None = None,
                 sandbox_config: Path | None = None):
        super().__init__(build_root, catalog, sandbox_config)
        self.host = host
        self.run_id = hashlib.sha256(str(self.build_root).encode()).hexdigest()[:20]
        self._synced: set[str] = set()
        try:
            staged = subprocess.run(
                ["scp", "-q", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                 str(WORKER), f"{host}:{REMOTE_WORKER}"],
                capture_output=True, text=True, timeout=30, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"Cannot stage judge worker on {host}: {exc}") from exc
        if staged.returncode:
            raise RuntimeError(f"Cannot stage judge worker on {host}: {staged.stderr.strip()}")
        self._request({"action": "probe"}, timeout=20)

    def _request(self, payload: dict, *, timeout: int) -> dict:
        payload = {**payload, "run_id": self.run_id}
        try:
            proc = subprocess.run(
                ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                 self.host, "python", REMOTE_WORKER],
                input=json.dumps(payload), capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"SSH judge unavailable: {exc}") from exc
        if proc.returncode:
            raise RuntimeError(f"SSH judge failed: {proc.stderr.strip() or proc.stdout.strip()}")
        try:
            response = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid SSH judge response: {proc.stdout[:300]}") from exc
        if "error" in response:
            raise RuntimeError(response["error"])
        return response

    def ensure_images(self, images: list[dict], docker_dir: Path) -> None:
        for image in images:
            dockerfile = docker_dir / image["dockerfile"]
            self._request({"action": "image", "tag": image["tag"],
                           "dockerfile": dockerfile.read_text(encoding="utf-8")}, timeout=600)

    def _run(self, image: str, source: Path, work: Path, command: str,
             input_text: str = "", *, timeout: int) -> tuple[int, str, str, bool]:
        work_key = hashlib.sha256(str(work).encode()).hexdigest()[:20]
        payload = {"action": "run", "work_key": work_key, "image": image,
                   "command": command, "input": input_text, "timeout": timeout,
                   "limits": self.limits}
        if work_key not in self._synced:
            files = list(source.iterdir())
            if len(files) != 1 or not files[0].is_file():
                return 125, "", "Expected exactly one source file", False
            payload["source_name"] = files[0].name
            payload["source_b64"] = base64.b64encode(files[0].read_bytes()).decode("ascii")
        try:
            result = self._request(
                payload, timeout=timeout + self.limits["docker_startup_grace_seconds"]
                + self.limits["container_cleanup_timeout_seconds"] + 25)
        except RuntimeError as exc:
            return 125, "", str(exc), False
        self._synced.add(work_key)
        return result["code"], result["out"], result["err"], result["timed_out"]

    def execute_many(self, solution: Solution, cases: list[tuple[str, str]]) -> list[Result]:
        if not cases:
            return []
        if solution.id not in self._compiled:
            return [Result(solution.id, "INFRA", case_id, stderr="solution not compiled")
                    for case_id, _ in cases]
        work, image, command = self._compiled[solution.id]
        source = work / "source"
        work_key = hashlib.sha256(str(work).encode()).hexdigest()[:20]
        payload = {"action": "run_many", "work_key": work_key, "image": image,
                   "command": command, "inputs": [value for _, value in cases],
                   "timeout": self.limits["run_timeout_seconds"], "limits": self.limits}
        if work_key not in self._synced:
            files = list(source.iterdir())
            if len(files) != 1 or not files[0].is_file():
                return [Result(solution.id, "INFRA", case_id,
                               stderr="Expected exactly one source file") for case_id, _ in cases]
            payload["source_name"] = files[0].name
            payload["source_b64"] = base64.b64encode(files[0].read_bytes()).decode("ascii")
        per_case = (self.limits["run_timeout_seconds"]
                    + self.limits["docker_startup_grace_seconds"]
                    + self.limits["container_cleanup_timeout_seconds"] + 25)
        try:
            runs = self._request(payload, timeout=len(cases) * per_case)["runs"]
            if len(runs) != len(cases):
                raise RuntimeError("Incomplete judge batch response")
        except (KeyError, RuntimeError) as exc:
            return [Result(solution.id, "INFRA", case_id, stderr=str(exc))
                    for case_id, _ in cases]
        self._synced.add(work_key)
        results = []
        for (case_id, _), run in zip(cases, runs):
            code, out, err = run["code"], run["out"], run["err"]
            verdict = ("TLE" if run["timed_out"] else "INFRA" if code == 125 else
                       "PASS" if code == 0 else "RE")
            results.append(Result(solution.id, verdict, case_id, out, err))
        return results
