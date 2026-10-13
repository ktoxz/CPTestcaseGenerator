"""Small JSON-over-SSH worker for Docker Desktop on a Windows judge host."""

from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path


def checked_id(value: str) -> str:
    if not re.fullmatch(r"[a-f0-9]{20}", value):
        raise ValueError("Invalid run/work identifier")
    return value


def run_command(args: list[str], *, input_text: str = "", timeout: int = 30) -> dict:
    # SSH logons cannot use Docker Desktop's Windows credential helper. The judge
    # only pulls public images, so use an isolated, unauthenticated CLI config.
    config = Path(tempfile.gettempdir()) / "testgen-remote-judge" / "docker-cli"
    config.mkdir(parents=True, exist_ok=True)
    (config / "config.json").write_text('{"auths":{}}', encoding="utf-8")
    environment = os.environ.copy()
    environment["DOCKER_CONFIG"] = str(config)
    environment["DOCKER_HOST"] = "npipe:////./pipe/dockerDesktopLinuxEngine"
    try:
        proc = subprocess.run(args, input=input_text, text=True, encoding="utf-8",
                              errors="replace", capture_output=True, timeout=timeout,
                              check=False, env=environment)
    except subprocess.TimeoutExpired:
        return {"code": -1, "out": "", "err": "wall timeout", "timed_out": True}
    return {"code": proc.returncode, "out": proc.stdout, "err": proc.stderr,
            "timed_out": False}


def handle(request: dict) -> dict:
    root = Path(tempfile.gettempdir()) / "testgen-remote-judge" / checked_id(request["run_id"])
    action = request["action"]
    if action == "run_many":
        inputs = request["inputs"]
        if not isinstance(inputs, list) or not 1 <= len(inputs) <= 32 or not all(
                isinstance(value, str) for value in inputs):
            raise ValueError("Invalid batch inputs")
        common = {key: value for key, value in request.items() if key not in {"action", "inputs"}}
        return {"runs": [handle({**common, "action": "run", "input": value})
                         for value in inputs]}
    if action == "probe":
        result = run_command(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=15)
        if result["code"]:
            raise RuntimeError(
                "Remote Docker Desktop Linux engine is not running. "
                "Start it in the remote Windows session and confirm `docker info` there. "
                f"Docker said: {result['err'].strip()}")
        return {"version": result["out"].strip()}
    if action == "image":
        tag = request["tag"]
        if run_command(["docker", "image", "inspect", tag], timeout=20)["code"] == 0:
            return {"tag": tag}
        build = root / "images" / re.sub(r"[^A-Za-z0-9_.-]", "_", tag)
        build.mkdir(parents=True, exist_ok=True)
        dockerfile = build / "Dockerfile"
        dockerfile.write_text(request["dockerfile"], encoding="utf-8")
        result = run_command(["docker", "build", "-t", tag, str(build)], timeout=540)
        if result["code"]:
            raise RuntimeError(f"Docker image build failed for {tag}: {result['err'][-1500:]}")
        return {"tag": tag}
    if action != "run":
        raise ValueError("Unknown action")
    work = root / "build" / checked_id(request["work_key"])
    source = work / "source"
    source.mkdir(parents=True, exist_ok=True)
    if "source_b64" in request:
        name = request["source_name"]
        if Path(name).name != name:
            raise ValueError("Invalid source filename")
        (source / name).write_bytes(base64.b64decode(request["source_b64"], validate=True))
    limits = request["limits"]
    container_name = f"tg-{request['run_id'][:10]}-{uuid.uuid4().hex[:12]}"
    args = [
        "docker", "run", "--rm", "--name", container_name,
        "--label", "testgen.owner=Final_TestcaseGenerator",
        "--label", f"testgen.run={request['run_id']}",
        "-i", "--network", "none", "--read-only",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--pids-limit", str(limits["pids_limit"]), "--memory", limits["memory"],
        "--memory-swap", limits["memory"], "--cpus", limits["cpus"],
        "--tmpfs", f"/tmp:rw,nosuid,size={limits['tmpfs_size']}",
        "--mount", f"type=bind,src={source},dst=/src,readonly",
        "--mount", f"type=bind,src={work},dst=/work",
        request["image"], "timeout", "-s", "TERM", "-k", "1s",
        f"{request['timeout']}s", "sh", "-lc", request["command"],
    ]
    outer_timeout = request["timeout"] + limits["docker_startup_grace_seconds"]
    result = run_command(args, input_text=request.get("input", ""), timeout=outer_timeout)
    if result["timed_out"]:
        cleanup = run_command(["docker", "rm", "-f", container_name],
                              timeout=limits["container_cleanup_timeout_seconds"])
        detail = cleanup["err"].strip() or cleanup["out"].strip()
        result = {"code": 125, "out": "", "err":
                  f"Docker invocation timed out (not code TLE); cleanup {container_name}: {detail}",
                  "timed_out": False}
    elif result["code"] == 124:
        result["timed_out"] = True
    result["out"] = result["out"][:limits["stdout_limit_bytes"]]
    result["err"] = result["err"][:limits["stderr_limit_bytes"]]
    return result


if __name__ == "__main__":
    try:
        print(json.dumps(handle(json.load(sys.stdin))))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
