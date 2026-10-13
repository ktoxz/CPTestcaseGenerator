"""Check the minimum environment needed by the Kaggle smoke-test preset."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problem", required=True)
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--model", default="gemma3:4b")
    parser.add_argument(
        "--runtime-config",
        type=Path,
        default=ROOT / "config" / "kaggle.runtimes.json",
    )
    parser.add_argument("--skip-ollama", action="store_true")
    args = parser.parse_args()

    checks: list[dict] = []

    def record(name: str, ok: bool, detail: str, *, required: bool = True) -> None:
        checks.append({
            "name": name,
            "ok": ok,
            "required": required,
            "detail": detail,
        })

    record(
        "linux",
        sys.platform == "linux",
        f"platform={platform.platform()}",
    )
    record(
        "python",
        sys.version_info >= (3, 12),
        f"python={platform.python_version()} (requires >=3.12)",
    )
    statement = ROOT / "data" / "problems" / args.problem / "statement.md"
    record("statement", statement.is_file(), str(statement))
    record(
        "working-directory",
        ROOT.exists() and ROOT.is_dir() and ROOT.parent.exists(),
        str(ROOT),
    )
    try:
        runtime_data = json.loads(args.runtime_config.read_text(encoding="utf-8"))
        runtime_ids = {
            str(item.get("id", ""))
            for item in runtime_data.get("runtimes", [])
            if isinstance(item, dict)
        }
        tools = {"prlimit"}
        if "c" in runtime_ids:
            tools.add("gcc")
        if any(item.startswith("cpp") for item in runtime_ids):
            tools.add("g++")
        if "java" in runtime_ids:
            tools.update(("javac", "java"))
        if "python2" in runtime_ids:
            tools.add("python2")
        record("runtime-config", True, str(args.runtime_config))
    except (OSError, json.JSONDecodeError, AttributeError) as error:
        tools = {"prlimit"}
        record("runtime-config", False, f"{type(error).__name__}: {error}")
    for tool in sorted(tools):
        location = shutil.which(tool)
        record(tool, bool(location), location or "not found")

    usage = shutil.disk_usage(ROOT)
    free_gib = usage.free / 1024**3
    record(
        "free-disk",
        free_gib >= 5,
        f"{free_gib:.1f} GiB free (5 GiB minimum for model + artifacts)",
    )

    if not args.skip_ollama:
        try:
            with urllib.request.urlopen(
                args.ollama_url.rstrip("/") + "/api/tags", timeout=10
            ) as response:
                payload = json.load(response)
            names = {
                str(item.get("name", ""))
                for item in payload.get("models", [])
                if isinstance(item, dict)
            }
            normalized = {name.removesuffix(":latest") for name in names}
            requested = args.model.removesuffix(":latest")
            record("ollama", True, f"reachable at {args.ollama_url}")
            record(
                "ollama-model",
                args.model in names or requested in normalized,
                f"requested={args.model}; installed={sorted(names)}",
            )
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            record("ollama", False, f"{type(error).__name__}: {error}")

    for item in checks:
        status = "PASS" if item["ok"] else ("WARN" if not item["required"] else "FAIL")
        print(f"[{status}] {item['name']}: {item['detail']}")
    failures = [item for item in checks if item["required"] and not item["ok"]]
    if failures:
        raise SystemExit(1)
    print(
        "Preflight passed. Native judge remains a best-effort smoke-test backend; "
        "it is not equivalent to Docker isolation."
    )


if __name__ == "__main__":
    main()
