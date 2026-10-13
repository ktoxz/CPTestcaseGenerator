"""Download a bounded CodeNet AC/WA bundle before a WSL-based judge run."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from testgen.codenet import SSHCodeNetSource


def main() -> None:
    settings_path = ROOT / "config" / "oracle.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", required=True)
    parser.add_argument("--limit", type=int, default=settings["max_per_label"])
    parser.add_argument("--host", default=settings["host"])
    parser.add_argument("--root", default=settings["staging_root"])
    parser.add_argument("--runtime-config", type=Path, default=ROOT / "config" / "runtimes.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or ROOT / "data" / "problems" / args.problem / "oracle"
    rows = SSHCodeNetSource(ROOT / "scripts" / "export_codenet.py", args.host,
                            args.root, args.runtime_config, settings_path).fetch(
        args.problem, output, args.limit)
    print(f"Downloaded {len(rows)} submissions to {output}")


if __name__ == "__main__":
    main()
