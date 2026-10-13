"""Export a compile-checked, diverse multi-problem Project CodeNet bundle.

Run this script on the machine that stores the staged CodeNet parquet files.
Only C, C++ and Python 3 are included because those runtimes can be checked on
the current staging host.  Every exported source has passed a real compile or
Python byte-code compilation command during this export.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import heapq
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

import pyarrow.dataset as ds
import pyarrow.parquet as pq

from export_codenet_diverse import (
    add_bytes,
    diverse_select,
    prepare_candidate,
    source_bytes,
    stable_rank,
)


LABEL_DIR = {"Accepted": "Accepted", "Wrong Answer": "WrongAnswer"}
EXTENSION = {"C": ".c", "C++": ".cpp", "Python": ".py"}


def python3_dialect(original: str) -> bool:
    return not re.search(r"(?:Python|PyPy)\s*\(?2(?:[.)\s]|$)", original)


def supported(row: dict) -> bool:
    language = row.get("language")
    original = row.get("original_language") or ""
    return language in {"C", "C++"} or (
        language == "Python" and python3_dialect(original)
    )


def runtime_dialect(language: str) -> str:
    return {"C": "C", "C++": "C++17", "Python": "Python3"}[language]


def compile_candidate(candidate: dict) -> tuple[dict, dict]:
    language = candidate["language"]
    with tempfile.TemporaryDirectory(prefix="codenet-compile-") as temp:
        root = Path(temp)
        source = root / ("main" + EXTENSION[language])
        source.write_bytes(candidate["raw"])
        if language == "C":
            command = ["gcc", "-std=gnu11", "-O0", str(source), "-lm", "-o", str(root / "main")]
        elif language == "C++":
            command = ["g++", "-std=gnu++17", "-O0", str(source), "-o", str(root / "main")]
        else:
            command = ["python3", "-m", "py_compile", str(source)]
        try:
            done = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                timeout=30, check=False,
            )
            result = {
                "passed": done.returncode == 0,
                "returncode": done.returncode,
                "stderr": done.stderr.decode("utf-8", errors="replace")[-500:],
            }
        except subprocess.TimeoutExpired:
            result = {"passed": False, "returncode": None, "stderr": "compile timeout"}
    return candidate, result


def balanced_candidates(rows: list[dict]) -> list[dict]:
    """Interleave languages before falling back to stable-rank order."""
    by_language: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_language[row["language"]].append(row)
    for language_rows in by_language.values():
        language_rows.sort(key=lambda row: row["rank"])
    result = []
    index = 0
    while True:
        added = False
        for language in sorted(by_language):
            if index < len(by_language[language]):
                result.append(by_language[language][index])
                added = True
        if not added:
            return result
        index += 1


def compile_pool(task: tuple[tuple[str, str], list[dict], int]) -> tuple:
    key, rows, target = task
    passed = []
    failures = Counter()
    unique: set[tuple[str, str]] = set()
    checked = 0
    for candidate in balanced_candidates(rows):
        candidate, result = compile_candidate(candidate)
        checked += 1
        if result["passed"]:
            normalized = (candidate["language"], candidate["normalized_sha256"])
            if normalized not in unique:
                unique.add(normalized)
                passed.append(candidate)
                if len(passed) >= target:
                    break
        else:
            failures[candidate["language"]] += 1
    return key, passed, failures, checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--candidates-per-pool", type=int, default=45)
    parser.add_argument("--candidates-per-language", type=int, default=10)
    parser.add_argument("--jobs", type=int, default=max(1, min(12, os.cpu_count() or 1)))
    parser.add_argument(
        "--candidates-only", action="store_true",
        help="Package the preselected source candidates without compiling them",
    )
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        raise ValueError("limit must be 1..100")

    selection = json.loads(args.selection.read_text(encoding="utf-8"))
    if isinstance(selection, dict):
        selection = selection["problems"]
    problem_ids = [row["problem_id"] if "problem_id" in row else row["id"] for row in selection]
    if len(problem_ids) != len(set(problem_ids)):
        raise ValueError("Selection contains duplicate problem IDs")

    submissions = ds.dataset(str(args.root / "submissions"), format="parquet")
    heaps: dict[tuple[str, ...], list[tuple[int, str, dict]]] = defaultdict(list)
    available: dict[str, Counter] = defaultdict(Counter)
    scanner = submissions.scanner(
        columns=["submission_id", "problem_id", "status", "language", "original_language"],
        filter=(
            ds.field("problem_id").isin(problem_ids)
            & ds.field("status").isin(list(LABEL_DIR))
            & ds.field("language").isin(sorted(EXTENSION))
        ),
        batch_size=32_768,
        use_threads=True,
    )
    for batch in scanner.to_batches():
        for row in batch.to_pylist():
            if not supported(row):
                continue
            problem_id, label, language = row["problem_id"], row["status"], row["language"]
            available[problem_id][label] += 1
            rank = stable_rank(problem_id, label, str(row["submission_id"]))
            item = (-int(rank, 16), str(row["submission_id"]), row)
            for key, limit in (
                ((problem_id, label), args.candidates_per_pool),
                ((problem_id, label, language), args.candidates_per_language),
            ):
                heap = heaps[key]
                if len(heap) < limit:
                    heapq.heappush(heap, item)
                elif item > heap[0]:
                    heapq.heapreplace(heap, item)

    preselected = []
    for problem_id in problem_ids:
        for label in LABEL_DIR:
            candidates_by_id = {
                item[2]["submission_id"]: item[2]
                for item in heaps[(problem_id, label)]
            }
            for language in sorted(EXTENSION):
                candidates_by_id.update({
                    item[2]["submission_id"]: item[2]
                    for item in heaps[(problem_id, label, language)]
                })
            preselected.extend(sorted(
                candidates_by_id.values(),
                key=lambda row: stable_rank(problem_id, label, str(row["submission_id"])),
            ))
    ids = {row["submission_id"] for row in preselected}
    code_rows = ds.dataset(str(args.root / "code"), format="parquet").to_table(
        filter=ds.field("submission_id").isin(sorted(ids))
    ).to_pylist()
    by_id = {row["submission_id"]: source_bytes(row) for row in code_rows}

    candidates = []
    missing_code = 0
    for row in preselected:
        raw = by_id.get(row["submission_id"], b"")
        if not raw.strip():
            missing_code += 1
            continue
        metadata = {
            "submission_id": row["submission_id"],
            "problem_id": row["problem_id"],
            "label": row["status"],
            "language": row["language"],
            "original_dialect": row.get("original_language") or "",
            "rank": stable_rank(row["problem_id"], row["status"], str(row["submission_id"])),
        }
        candidates.append(prepare_candidate(metadata, raw))

    descriptions = {row["problem_id"]: row for row in pq.read_table(
        args.root / "descriptions.parquet", filters=[("problem_id", "in", problem_ids)]
    ).to_pylist()}
    problem_metadata = {row["id"]: row for row in pq.read_table(
        args.root / "problem_list.parquet", filters=[("id", "in", problem_ids)]
    ).to_pylist()}
    if set(descriptions) != set(problem_ids) or set(problem_metadata) != set(problem_ids):
        raise RuntimeError("Missing descriptions or problem metadata")

    if args.candidates_only:
        grouped_candidates: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for candidate in candidates:
            grouped_candidates[(candidate["problem_id"], candidate["label"])].append(candidate)
        with tarfile.open(args.output, "w:gz", compresslevel=6) as archive:
            for problem_id in problem_ids:
                base = f"{problem_id}/oracle"
                add_bytes(archive, f"{base}/statement.html", descriptions[problem_id]["html"].encode("utf-8"))
                add_bytes(archive, f"{problem_id}/codenet-metadata.json", (
                    json.dumps(problem_metadata[problem_id], ensure_ascii=False, indent=2) + "\n"
                ).encode("utf-8"))
                manifest = []
                for label, label_dir in LABEL_DIR.items():
                    rows_for_label = balanced_candidates(grouped_candidates[(problem_id, label)])
                    for index, row in enumerate(rows_for_label, 1):
                        source = f"candidates/{label_dir}/{index:03d}{EXTENSION[row['language']]}"
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
                            "rank": row["rank"],
                            "normalized_sha256": row["normalized_sha256"],
                            "normalized_tokens": len(row["tokens"]),
                            "source_bytes": len(row["raw"]),
                        })
                add_bytes(archive, f"{base}/candidate-manifest.json", (
                    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
                ).encode("utf-8"))
        print(json.dumps({
            "problems": len(problem_ids),
            "candidates": len(candidates),
            "missing_code": missing_code,
            "mode": "candidates-only",
        }, indent=2))
        return

    candidates_by_group: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for candidate in candidates:
        candidates_by_group[(candidate["problem_id"], candidate["label"])].append(candidate)
    compiled: dict[tuple[str, str], list[dict]] = defaultdict(list)
    compile_failures: dict[tuple[str, str], Counter] = defaultdict(Counter)
    checked_counts: dict[tuple[str, str], int] = {}
    tasks = [
        ((problem_id, label), candidates_by_group[(problem_id, label)], args.limit + 6)
        for problem_id in problem_ids for label in LABEL_DIR
    ]
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for index, (key, passed, failures, checked) in enumerate(
            executor.map(compile_pool, tasks), 1
        ):
            compiled[key] = passed
            compile_failures[key] = failures
            checked_counts[key] = checked
            if index % 10 == 0:
                print(
                    f"compile checked {index}/{len(tasks)} pools; "
                    f"sources={sum(checked_counts.values())}", flush=True,
                )

    shortages = []
    selected: dict[tuple[str, str], list[dict]] = {}
    for problem_id in problem_ids:
        for label in LABEL_DIR:
            key = (problem_id, label)
            try:
                selected[key] = diverse_select(compiled[key], args.limit)
            except RuntimeError:
                shortages.append({
                    "problem_id": problem_id,
                    "label": label,
                    "compile_valid_unique": len({
                        (row["language"], row["normalized_sha256"]) for row in compiled[key]
                    }),
                    "compile_failures": dict(compile_failures[key]),
                    "available": available[problem_id][label],
                })
    if shortages:
        print(json.dumps({"shortages": shortages}, ensure_ascii=False, indent=2))
        raise RuntimeError(f"{len(shortages)} pools have fewer than {args.limit} valid unique sources")

    summary = []
    with tarfile.open(args.output, "w:gz", compresslevel=6) as archive:
        for problem_id in problem_ids:
            base = f"{problem_id}/oracle"
            add_bytes(archive, f"{base}/statement.html", descriptions[problem_id]["html"].encode("utf-8"))
            add_bytes(archive, f"{problem_id}/codenet-metadata.json", (
                json.dumps(problem_metadata[problem_id], ensure_ascii=False, indent=2) + "\n"
            ).encode("utf-8"))
            manifest = []
            languages = {}
            for label, label_dir in LABEL_DIR.items():
                chosen = selected[(problem_id, label)]
                languages[label] = dict(Counter(row["language"] for row in chosen))
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
                            "method": "compile-checked greedy normalized-token diversity v2",
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
                "selection_method": "Compile-valid candidates followed by structural diversity selection.",
                "compiler_environment": {
                    "C": "gcc -std=gnu11 -O0",
                    "C++": "g++ -std=gnu++17 -O0",
                    "Python": "python3 -m py_compile",
                },
                "candidate_limit_per_pool": args.candidates_per_pool,
                "candidate_language_floor": args.candidates_per_language,
                "available_supported_submissions": dict(available[problem_id]),
                "compile_failures": {
                    label: dict(compile_failures[(problem_id, label)]) for label in LABEL_DIR
                },
                "compile_checked_candidates": {
                    label: checked_counts[(problem_id, label)] for label in LABEL_DIR
                },
                "selected_languages": languages,
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
                "selected_languages": languages,
                "compile_failures": provenance["compile_failures"],
            })
    print(json.dumps({
        "problems": len(problem_ids),
        "sources": len(problem_ids) * args.limit * 2,
        "missing_code": missing_code,
        "summary": summary,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
