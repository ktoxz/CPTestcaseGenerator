"""Small JSON-over-stdin worker used by :mod:`testgen.remote_judge`.

The worker intentionally depends only on the Python standard library so it can
be copied to a fresh Linux judge host.  Each invocation handles one request and
prints one JSON response.
"""

from __future__ import annotations

import base64
import json
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path


OWNER_LABEL = "testgen.owner=Final_TestcaseGenerator"
SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def run_command(args: list[str], *, input_text: str = "", timeout: float = 30) -> dict:
    """Run a command and return a bounded, JSON-serializable result."""
    try:
        proc = subprocess.run(
            args,
            input=input_text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return {
            "code": proc.returncode,
            "out": proc.stdout.decode("utf-8", errors="replace"),
            "err": proc.stderr.decode("utf-8", errors="replace"),
            "timed_out": proc.returncode == 124,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "code": -1,
            "out": (exc.stdout or b"").decode("utf-8", errors="replace"),
            "err": (exc.stderr or b"").decode("utf-8", errors="replace") or "wall timeout",
            "timed_out": True,
        }
    except OSError as exc:
        return {"code": 125, "out": "", "err": str(exc), "timed_out": False}


def _required_id(request: dict, key: str) -> str:
    value = request.get(key)
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value):
        raise ValueError(f"Invalid {key}")
    return value


def _work_paths(request: dict) -> tuple[Path, Path, Path]:
    run_id = _required_id(request, "run_id")
    work_key = _required_id(request, "work_key")
    root = Path(tempfile.gettempdir()) / "testgen-remote-judge" / run_id / "build" / work_key
    source = root / "source"
    source.mkdir(parents=True, exist_ok=True)
    return root, source, root


def _stage_source(request: dict, source: Path) -> None:
    encoded = request.get("source_b64")
    if encoded is None:
        if not any(source.iterdir()):
            raise ValueError("Source was not staged")
        return
    name = request.get("source_name")
    if not isinstance(name, str) or Path(name).name != name or name in {".", ".."}:
        raise ValueError("Invalid source_name")
    try:
        content = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("Invalid source_b64") from exc
    if len(content) > 4 * 1024 * 1024:
        raise ValueError("Source file is too large")
    for existing in source.iterdir():
        if existing.is_file() and existing.name != name:
            existing.unlink()
    (source / name).write_bytes(content)


def _container_args(request: dict, source: Path, work: Path, input_index: int = 0) -> tuple[list[str], str, float]:
    limits = request.get("limits") or {}
    timeout = max(1.0, min(float(request.get("timeout", 5)), 120.0))
    run_id = _required_id(request, "run_id")
    image = request.get("image")
    command = request.get("command")
    if not isinstance(image, str) or not image or not isinstance(command, str) or not command:
        raise ValueError("Invalid image or command")
    container = f"tg-{run_id[:10]}-{input_index:04d}-{uuid.uuid4().hex[:8]}"
    args = [
        "docker", "run", "--rm", "--name", container,
        "--label", OWNER_LABEL, "--label", f"testgen.run={run_id}",
        "-i", "--network", "none", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--pids-limit", str(limits.get("pids_limit", 64)),
        "--memory", str(limits.get("memory", "512m")),
        "--memory-swap", str(limits.get("memory", "512m")),
        "--cpus", str(limits.get("cpus", "1")),
        "--tmpfs", f"/tmp:rw,nosuid,size={limits.get('tmpfs_size', '32m')}",
        "--mount", f"type=bind,src={source.resolve()},dst=/src,readonly",
        "--mount", f"type=bind,src={work.resolve()},dst=/work",
        image, "timeout", "-s", "TERM", "-k", "1s", f"{timeout:g}s",
        "sh", "-lc", command,
    ]
    grace = max(1.0, min(float(limits.get("docker_startup_grace_seconds", 30)), 120.0))
    return args, container, timeout + grace


def _run_one(request: dict, source: Path, work: Path, input_text: str, index: int) -> dict:
    args, container, wall_timeout = _container_args(request, source, work, index)
    result = run_command(args, input_text=input_text, timeout=wall_timeout)
    limits = request.get("limits") or {}
    if result["timed_out"] and result["code"] == -1:
        cleanup = run_command(
            ["docker", "rm", "-f", container],
            timeout=max(1.0, min(float(limits.get("container_cleanup_timeout_seconds", 15)), 60.0)),
        )
        detail = cleanup["err"].strip() or cleanup["out"].strip()
        return {"code": 125, "out": "", "err": f"Docker invocation timed out; cleanup {container}: {detail}", "timed_out": False}
    result["out"] = result["out"][: int(limits.get("stdout_limit_bytes", 65536))]
    result["err"] = result["err"][: int(limits.get("stderr_limit_bytes", 8192))]
    return result


def handle(request: dict) -> dict:
    action = request.get("action")
    if action == "probe":
        probe = run_command(["docker", "version", "--format", "{{.Server.Version}}"], timeout=15)
        if probe["code"]:
            raise RuntimeError(probe["err"].strip() or "Docker is unavailable")
        return {"ok": True, "docker": probe["out"].strip()}
    if action == "image":
        _required_id(request, "run_id")
        tag, dockerfile = request.get("tag"), request.get("dockerfile")
        if not isinstance(tag, str) or not tag or not isinstance(dockerfile, str):
            raise ValueError("Invalid image request")
        root = Path(tempfile.gettempdir()) / "testgen-remote-judge" / request["run_id"] / "images"
        root.mkdir(parents=True, exist_ok=True)
        path = root / f"Dockerfile-{uuid.uuid4().hex}"
        path.write_text(dockerfile, encoding="utf-8")
        try:
            result = run_command(["docker", "build", "-t", tag, "-f", str(path), str(root)], timeout=600)
        finally:
            path.unlink(missing_ok=True)
        if result["code"]:
            raise RuntimeError(result["err"].strip() or result["out"].strip())
        return {"ok": True}
    if action not in {"run", "run_many"}:
        raise ValueError("Unknown action")
    _root, source, work = _work_paths(request)
    _stage_source(request, source)
    if action == "run":
        return _run_one(request, source, work, str(request.get("input", "")), 0)
    inputs = request.get("inputs")
    if not isinstance(inputs, list) or len(inputs) > 1000 or not all(isinstance(item, str) for item in inputs):
        raise ValueError("Invalid inputs")
    return {"runs": [_run_one(request, source, work, value, index) for index, value in enumerate(inputs)]}


def main() -> int:
    try:
        request = json.load(sys.stdin)
        response = handle(request)
    except Exception as exc:  # keep the transport response machine-readable
        response = {"error": f"{type(exc).__name__}: {exc}"}
    json.dump(response, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
