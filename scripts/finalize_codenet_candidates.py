"""Compile candidate CodeNet sources locally and emit the final 30/30 bundle."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

from export_codenet_collection import (
    EXTENSION,
    LABEL_DIR,
    add_bytes,
    compile_pool,
    diverse_select,
    prepare_candidate,
    runtime_dialect,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_extract(archive_path: Path, output: Path, expected: set[str]) -> None:
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            path = Path(member.name)
            if (
                member.name.startswith("/") or ".." in path.parts
                or not member.isfile() or not path.parts or path.parts[0] not in expected
            ):
                raise ValueError(f"Unsafe or unexpected archive member: {member.name}")
        archive.extractall(output, filter="data")


def version(command: str, argument: str = "--version") -> str:
    done = subprocess.run(
        [command, argument], capture_output=True, text=True, errors="replace", check=False
    )
    if done.returncode:
        raise RuntimeError(f"Compiler unavailable: {command}: {done.stderr.strip()}")
    return (done.stdout or done.stderr).splitlines()[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--jobs", type=int, default=max(1, min(12, os.cpu_count() or 1)))
    args = parser.parse_args()

    selection = json.loads(args.selection.read_text(encoding="utf-8"))
    if isinstance(selection, dict):
        selection = selection["problems"]
    problem_ids = [row.get("problem_id", row.get("id")) for row in selection]
    expected = set(problem_ids)
    if len(problem_ids) != len(expected):
        raise ValueError("Duplicate problem IDs in selection")

    compiler_environment = {
        "C": version("gcc"),
        "C++": version("g++"),
        "Python": version("python", "--version"),
        "platform_note": "Current local toolchains; original CodeNet WA/AC verdict also proves historical full compilation.",
    }
    with tempfile.TemporaryDirectory(prefix="codenet-candidates-", dir=args.output.parent) as temp:
        stage = Path(temp)
        safe_extract(args.archive, stage, expected)
        tasks = []
        raw_manifests = {}
        for problem_id in problem_ids:
            oracle = stage / problem_id / "oracle"
            rows = json.loads((oracle / "candidate-manifest.json").read_text(encoding="utf-8"))
            raw_manifests[problem_id] = rows
            grouped = defaultdict(list)
            for row in rows:
                source = (oracle / row["source"]).resolve()
                if not source.is_relative_to(oracle.resolve()) or sha256(source) != row["sha256"]:
                    raise ValueError(f"Bad candidate source: {problem_id}/{row['id']}")
                raw = source.read_bytes()
                candidate = prepare_candidate({
                    "submission_id": row["id"],
                    "problem_id": problem_id,
                    "label": row["label"],
                    "language": row["language"],
                    "original_dialect": row["original_dialect"],
                    "rank": row["rank"],
                }, raw)
                if candidate["normalized_sha256"] != row["normalized_sha256"]:
                    raise ValueError(f"Normalized hash mismatch: {problem_id}/{row['id']}")
                grouped[row["label"]].append(candidate)
            for label in LABEL_DIR:
                tasks.append(((problem_id, label), grouped[label], args.limit + 6))

        compiled = {}
        failures = {}
        checked = {}
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            for index, (key, passed, failed, count) in enumerate(
                executor.map(compile_pool, tasks), 1
            ):
                compiled[key] = passed
                failures[key] = failed
                checked[key] = count
                if index % 10 == 0:
                    print(
                        f"compile checked {index}/{len(tasks)} pools; "
                        f"sources={sum(checked.values())}", flush=True,
                    )

        selected = {}
        shortages = []
        for key, rows in compiled.items():
            try:
                selected[key] = diverse_select(rows, args.limit)
            except RuntimeError:
                shortages.append({
                    "problem_id": key[0], "label": key[1],
                    "valid_unique": len(rows),
                    "checked": checked[key],
                    "compile_failures": dict(failures[key]),
                })
        if shortages:
            raise RuntimeError(json.dumps({"shortages": shortages}, indent=2))

        summary = []
        with tarfile.open(args.output, "w:gz", compresslevel=6) as archive:
            for problem_id in problem_ids:
                source_problem = stage / problem_id
                base = f"{problem_id}/oracle"
                add_bytes(archive, f"{base}/statement.html", (source_problem / "oracle" / "statement.html").read_bytes())
                add_bytes(archive, f"{problem_id}/codenet-metadata.json", (source_problem / "codenet-metadata.json").read_bytes())
                manifest = []
                language_summary = {}
                for label, label_dir in LABEL_DIR.items():
                    chosen = selected[(problem_id, label)]
                    language_summary[label] = dict(Counter(row["language"] for row in chosen))
                    for index, row in enumerate(chosen, 1):
                        source = f"sources/{label_dir}/{index:02d}{EXTENSION[row['language']]}"
                        add_bytes(archive, f"{base}/{source}", row["raw"])
                        manifest.append({
                            "id": str(row["submission_id"]),
                            "problem_id": problem_id,
                            "label": label,
                            "language": row["language"],
                            "dialect": runtime_dialect(row["language"]),
                            "original_dialect": row["original_dialect"],
                            "source": source,
                            "sha256": row["sha256"],
                            "selection": {
                                "method": "local full-compile check plus greedy normalized-token diversity v2",
                                "rank": index,
                                "source_bytes": len(row["raw"]),
                                "normalized_tokens": len(row["tokens"]),
                                "normalized_sha256": row["normalized_sha256"],
                                "compile_check": "passed",
                            },
                        })
                provenance = {
                    "problem_id": problem_id,
                    "dataset": "Project CodeNet",
                    "selection_method": "Balanced-language full compile, then structural diversity selection.",
                    "compiler_environment": compiler_environment,
                    "candidate_count": len(raw_manifests[problem_id]),
                    "compile_checked_candidates": {
                        label: checked[(problem_id, label)] for label in LABEL_DIR
                    },
                    "compile_failures": {
                        label: dict(failures[(problem_id, label)]) for label in LABEL_DIR
                    },
                    "selected_languages": language_summary,
                    "labels": {"Accepted": args.limit, "Wrong Answer": args.limit},
                }
                add_bytes(archive, f"{base}/manifest.json", (
                    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
                ).encode("utf-8"))
                add_bytes(archive, f"{base}/provenance.json", (
                    json.dumps(provenance, ensure_ascii=False, indent=2) + "\n"
                ).encode("utf-8"))
                summary.append({
                    "problem_id": problem_id,
                    "languages": language_summary,
                    "compile_failures": provenance["compile_failures"],
                })
    print(json.dumps({
        "problems": len(problem_ids),
        "sources": len(problem_ids) * args.limit * 2,
        "compiler_environment": compiler_environment,
        "summary": summary,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
