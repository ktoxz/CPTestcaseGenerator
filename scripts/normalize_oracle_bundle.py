#!/usr/bin/env python3
"""Normalize legacy oracle bundles to the runtime/label schema used by testgen."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def normalize(root: Path) -> None:
    oracle_dir = root / "oracle" if (root / "oracle").is_dir() else root
    manifest_path = oracle_dir / "manifest.json"
    rows = json.loads(manifest_path.read_text(encoding="utf-8"))

    old_dir = oracle_dir / "sources" / "NonAccepted"
    new_dir = oracle_dir / "sources" / "WrongAnswer"
    if old_dir.exists():
        if new_dir.exists():
            raise RuntimeError(f"Both legacy and normalized source directories exist: {oracle_dir}")
        old_dir.rename(new_dir)

    for row in rows:
        if row.get("language") == "C++":
            row["dialect"] = "C++17"
        if row.get("label") == "Non-Accepted":
            row["label"] = "Wrong Answer"
        source = str(row.get("source", ""))
        row["source"] = source.replace("sources/NonAccepted/", "sources/WrongAnswer/")
    write_json(manifest_path, rows)

    provenance_path = oracle_dir / "provenance.json"
    if provenance_path.exists():
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        labels = provenance.get("labels")
        if isinstance(labels, dict) and "Non-Accepted" in labels:
            labels["Wrong Answer"] = labels.pop("Non-Accepted")
        write_json(provenance_path, provenance)

    print(f"normalized {oracle_dir}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", type=Path)
    args = parser.parse_args()
    for root in args.roots:
        normalize(root.resolve())


if __name__ == "__main__":
    main()
