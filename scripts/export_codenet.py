"""Run on an SSH source host: export a small, deterministic AC/WA CodeNet bundle."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import tarfile
from pathlib import Path

import pyarrow.dataset as ds
import pyarrow.parquet as pq


def rank(problem_id: str, row: dict) -> str:
    return hashlib.sha256(f"{problem_id}:{row['submission_id']}".encode()).hexdigest()


def add_bytes(archive: tarfile.TarFile, name: str, body: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(body)
    archive.addfile(info, io.BytesIO(body))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--problem", required=True)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.problem.startswith("p") or len(args.problem) != 6 or not args.problem[1:].isdigit():
        raise ValueError("Invalid problem id")
    if not 1 <= args.limit <= 100:
        raise ValueError("limit must be 1..100")
    runtime_data = json.loads(args.runtime_config.read_text(encoding="utf-8"))
    extensions = {}
    for row in runtime_data["runtimes"]:
        language, extension = row["language"], row["extension"]
        if language in extensions and extensions[language] != extension:
            raise ValueError(f"Inconsistent extension for {language}")
        extensions[language] = extension
    sub = ds.dataset(str(args.root / "submissions"), format="parquet")
    rows = sub.to_table(filter=(ds.field("problem_id") == args.problem) &
                        ds.field("status").isin(["Accepted", "Wrong Answer"]) &
                        ds.field("language").isin(sorted(extensions))).to_pylist()
    selected = []
    for label in ("Accepted", "Wrong Answer"):
        candidates = sorted((r for r in rows if r["status"] == label), key=lambda r: rank(args.problem, r))
        selected.extend(candidates[:args.limit])
    ids = {row["submission_id"] for row in selected}
    code = ds.dataset(str(args.root / "code"), format="parquet")
    code_rows = code.to_table(filter=ds.field("submission_id").isin(sorted(ids))).to_pylist()
    by_id = {row["submission_id"]: row for row in code_rows}
    if len(by_id) < len(ids):
        raise RuntimeError(f"Missing {len(ids) - len(by_id)} source rows")
    descriptions = pq.read_table(args.root / "descriptions.parquet", filters=[("problem_id", "==", args.problem)]).to_pylist()
    if len(descriptions) != 1:
        raise RuntimeError("Problem statement missing or duplicated")
    manifest = []
    with tarfile.open(args.output, "w:gz") as archive:
        add_bytes(archive, "statement.html", descriptions[0]["html"].encode("utf-8"))
        for row in selected:
            sid = row["submission_id"]
            raw = by_id[sid].get("code_raw")
            raw = bytes(raw) if raw is not None else (by_id[sid].get("code") or "").encode("utf-8")
            label = "AC" if row["status"] == "Accepted" else "WA"
            name = f"sources/{label}/{row['language']}/{sid}{extensions[row['language']]}"
            add_bytes(archive, name, raw)
            manifest.append({"id": sid, "problem_id": args.problem, "label": row["status"], "language": row["language"],
                             "dialect": row.get("original_language") or "", "source": name,
                             "sha256": hashlib.sha256(raw).hexdigest()})
        add_bytes(archive, "manifest.json", json.dumps(manifest, indent=2).encode("utf-8"))
    print(json.dumps({"problem": args.problem, "count": len(manifest),
                      "Accepted": sum(x["label"] == "Accepted" for x in manifest),
                      "Wrong Answer": sum(x["label"] == "Wrong Answer" for x in manifest)}))


if __name__ == "__main__":
    main()
