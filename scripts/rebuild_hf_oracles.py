#!/usr/bin/env python3
"""Build compile-verified, diverse Codeforces oracle bundles from HF parquet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARQUET = ROOT / "data" / "cache_hf" / "0000.parquet"
DEFAULT_PROBLEMS_ROOT = ROOT / "data" / "problems"
COMPILE_TEMP_ROOT = ROOT / "output" / ".hf-oracle-compile"
DEFAULT_PROBLEMS = (
    "cf1008a", "cf1009a", "cf1011a", "cf1006a", "cf1003a",
    "cf1004a", "cf1007a", "cf1008b", "cf1005a", "cf1005b",
    "cf1011b", "cf1000a", "cf1006c", "cf1009b", "cf1006b",
    "cf1004b", "cf1004c", "cf1000b", "cf1003c", "cf1003b",
)


@dataclass(frozen=True)
class Candidate:
    submission_id: str
    source: str
    verdict: str
    dataset_language: str
    language: str
    dialect: str
    extension: str
    standard: str | None
    passed_test_count: int | None


def parse_slug(slug: str) -> str:
    match = re.fullmatch(r"cf(\d+)([a-z][a-z0-9]*)", slug.lower())
    if not match:
        raise ValueError(f"Invalid Codeforces problem slug: {slug}")
    return f"{match.group(1)}/{match.group(2).upper()}"


def runtime_for(dataset_language: str) -> tuple[str, str, str, str | None] | None:
    """Map only languages supported by this repository's runtime catalog."""
    value = dataset_language.strip()
    if value.startswith("MS C++"):
        return None
    if "C++" in value or "Clang++" in value:
        if "20" in value:
            return None
        if "17" in value:
            return "C++", "C++17", ".cpp", "gnu++17"
        if "14" in value:
            return "C++", "C++14", ".cpp", "gnu++14"
        if "11" in value or "0x" in value:
            return "C++", "C++11", ".cpp", "gnu++11"
        return "C++", "C++", ".cpp", "gnu++98"
    if value in {"GNU C", "GNU C11"}:
        return "C", "C", ".c", "gnu11"
    if value == "Python 3" or value.startswith("PyPy 3"):
        return "Python", "Python3", ".py", None
    return None


def canonical_source(source: str) -> str:
    """Remove formatting only, preserving identifiers and algorithm choices."""
    return re.sub(r"\s+", "", source)


def diverse_order(candidates: list[Candidate]) -> list[Candidate]:
    """Interleave runtime and source-size strata after formatting deduplication."""
    unique: dict[str, Candidate] = {}
    for candidate in candidates:
        digest = hashlib.sha256(
            canonical_source(candidate.source).encode("utf-8", errors="replace")
        ).hexdigest()
        unique.setdefault(digest, candidate)

    queues: dict[tuple[str, str, int], deque[Candidate]] = {}
    grouped: dict[tuple[str, str, int], list[Candidate]] = defaultdict(list)
    for candidate in unique.values():
        size_band = min(12, max(0, int(math.log2(max(1, len(candidate.source)))) - 6))
        grouped[(candidate.language, candidate.dialect, size_band)].append(candidate)
    for key, values in grouped.items():
        values.sort(key=lambda item: hashlib.sha256(
            f"{item.submission_id}:{len(item.source)}".encode("ascii", errors="ignore")
        ).hexdigest())
        queues[key] = deque(values)

    keys = sorted(
        queues,
        key=lambda key: hashlib.sha256(repr(key).encode("utf-8")).hexdigest(),
    )
    ordered: list[Candidate] = []
    while keys:
        next_keys = []
        for key in keys:
            queue = queues[key]
            if queue:
                ordered.append(queue.popleft())
            if queue:
                next_keys.append(key)
        keys = next_keys
    return ordered


def compile_candidate(candidate: Candidate, timeout: int) -> tuple[bool, str]:
    COMPILE_TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="candidate-", dir=COMPILE_TEMP_ROOT
    ) as raw_temp:
        temp = Path(raw_temp)
        source_path = temp / f"main{candidate.extension}"
        source_path.write_text(candidate.source, encoding="utf-8", errors="replace")
        if candidate.language == "Python":
            command = [sys.executable, "-m", "py_compile", str(source_path)]
        elif candidate.language == "C++":
            compiler = shutil.which("g++")
            if not compiler:
                return False, "g++ not found"
            command = [
                compiler, f"-std={candidate.standard}", "-O0",
                str(source_path), "-o", str(temp / "main.exe"),
            ]
        elif candidate.language == "C":
            compiler = shutil.which("gcc")
            if not compiler:
                return False, "gcc not found"
            command = [
                compiler, "-std=gnu11", "-O0", str(source_path), "-lm",
                "-o", str(temp / "main.exe"),
            ]
        else:
            return False, f"unsupported language: {candidate.language}"
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, f"compile timeout after {timeout}s"
        diagnostic = (completed.stderr or completed.stdout).strip()
        return completed.returncode == 0, diagnostic[-1000:]


def select_verified(
    candidates: list[Candidate], quota: int, workers: int, timeout: int,
) -> tuple[list[Candidate], dict]:
    ordered = diverse_order(candidates)
    selected: list[Candidate] = []
    rejected: list[dict] = []
    attempted = 0
    batch_size = max(workers * 2, 16)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for start in range(0, len(ordered), batch_size):
            batch = ordered[start:start + batch_size]
            results = list(executor.map(
                lambda item: compile_candidate(item, timeout), batch
            ))
            for candidate, (valid, diagnostic) in zip(batch, results):
                attempted += 1
                if valid and len(selected) < quota:
                    selected.append(candidate)
                elif not valid:
                    rejected.append({
                        "submission_id": candidate.submission_id,
                        "dataset_language": candidate.dataset_language,
                        "diagnostic": diagnostic,
                    })
            if len(selected) >= quota:
                break
    if len(selected) < quota:
        raise RuntimeError(
            f"only {len(selected)}/{quota} unique submissions compiled; "
            f"candidates={len(candidates)}, unique={len(ordered)}, attempted={attempted}"
        )
    return selected, {
        "input_candidates": len(candidates),
        "unique_candidates": len(ordered),
        "compile_attempts": attempted,
        "compile_rejections": len(rejected),
        "rejected_examples": rejected[:10],
        "selected": len(selected),
        "languages": dict(Counter(
            f"{item.language}/{item.dialect}" for item in selected
        )),
        "source_bytes": {
            "min": min(len(item.source.encode("utf-8")) for item in selected),
            "max": max(len(item.source.encode("utf-8")) for item in selected),
        },
    }


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def publish_bundle(
    problems_root: Path,
    slug: str,
    selected_by_verdict: dict[str, list[Candidate]],
    audit: dict,
) -> None:
    oracle = (problems_root / slug / "oracle").resolve()
    expected_parent = (problems_root / slug).resolve()
    if oracle.parent != expected_parent:
        raise RuntimeError(f"unsafe oracle path: {oracle}")
    accepted = oracle / "sources" / "Accepted"
    wrong = oracle / "sources" / "WrongAnswer"
    accepted.mkdir(parents=True, exist_ok=True)
    wrong.mkdir(parents=True, exist_ok=True)
    for directory in (accepted, wrong):
        for old_file in directory.iterdir():
            if old_file.is_file():
                old_file.unlink()

    manifest = []
    label_specs = (
        ("OK", "Accepted", accepted, "ac"),
        ("WRONG_ANSWER", "Wrong Answer", wrong, "wa"),
    )
    for verdict, label, directory, short_label in label_specs:
        for index, candidate in enumerate(selected_by_verdict[verdict], 1):
            filename = f"{index:02d}-{candidate.submission_id}{candidate.extension}"
            path = directory / filename
            path.write_text(candidate.source, encoding="utf-8", errors="replace")
            manifest.append({
                "id": f"{slug}-{short_label}-{candidate.submission_id}",
                "problem_id": slug,
                "label": label,
                "language": candidate.language,
                "dialect": candidate.dialect,
                "source": path.relative_to(oracle).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "origin": {
                    "dataset": "open-r1/codeforces-submissions",
                    "submission_id": candidate.submission_id,
                    "programming_language": candidate.dataset_language,
                    "verdict": candidate.verdict,
                    "passed_test_count": candidate.passed_test_count,
                },
            })
    write_json(oracle / "manifest.json", manifest)
    write_json(oracle / "compile-audit.json", audit)


def build_candidates(rows: list[dict], problem_id: str, verdict: str) -> list[Candidate]:
    candidates = []
    for row in rows:
        if row.get("problem_id") != problem_id or row.get("verdict") != verdict:
            continue
        mapped = runtime_for(str(row.get("programmingLanguage") or ""))
        source = row.get("source")
        if mapped is None or not isinstance(source, str) or len(source.strip()) < 20:
            continue
        if "\x00" in source:
            continue
        language, dialect, extension, standard = mapped
        raw_passed = row.get("passedTestCount")
        passed = int(raw_passed) if raw_passed is not None else None
        candidates.append(Candidate(
            submission_id=str(row["submission_id"]),
            source=source,
            verdict=verdict,
            dataset_language=str(row["programmingLanguage"]),
            language=language,
            dialect=dialect,
            extension=extension,
            standard=standard,
            passed_test_count=passed,
        ))
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    parser.add_argument("--problems-root", type=Path, default=DEFAULT_PROBLEMS_ROOT)
    parser.add_argument("--problems", nargs="+", default=list(DEFAULT_PROBLEMS))
    parser.add_argument("--per-label", type=int, default=20)
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 2))
    parser.add_argument("--compile-timeout", type=int, default=20)
    args = parser.parse_args()
    if args.per_label < 15:
        parser.error("--per-label must be >= 15 (at least 30 total per problem)")
    if args.workers < 1:
        parser.error("--workers must be >= 1")

    columns = [
        "submission_id", "source", "problem_id", "programmingLanguage",
        "verdict", "passedTestCount",
    ]
    print(f"Reading {args.parquet}...", flush=True)
    wanted = {parse_slug(slug) for slug in args.problems}
    rows = [
        row for row in pq.read_table(args.parquet, columns=columns).to_pylist()
        if row.get("problem_id") in wanted
    ]
    print(f"Loaded {len(rows)} relevant parquet rows", flush=True)

    prepared = {}
    for position, slug in enumerate(args.problems, 1):
        problem_id = parse_slug(slug)
        print(f"[{position}/{len(args.problems)}] {slug} ({problem_id})", flush=True)
        chosen = {}
        audit = {
            "problem_id": slug,
            "dataset_problem_id": problem_id,
            "dataset": "open-r1/codeforces-submissions",
            "parquet": str(args.parquet.resolve()),
            "policy": {
                "per_label": args.per_label,
                "total": args.per_label * 2,
                "verdicts": ["OK", "WRONG_ANSWER"],
                "formatting_deduplication": True,
                "diversity": "round-robin by runtime and source-size band",
                "compile_verified": True,
            },
            "labels": {},
        }
        for verdict in ("OK", "WRONG_ANSWER"):
            candidates = build_candidates(rows, problem_id, verdict)
            selected, label_audit = select_verified(
                candidates, args.per_label, args.workers, args.compile_timeout
            )
            chosen[verdict] = selected
            audit["labels"][verdict] = label_audit
            print(
                f"  {verdict}: {len(selected)} selected; "
                f"{label_audit['compile_rejections']} CE rejected; "
                f"languages={label_audit['languages']}",
                flush=True,
            )
        prepared[slug] = (chosen, audit)

    # Publish only after every requested problem has met both quotas.
    for slug, (chosen, audit) in prepared.items():
        publish_bundle(args.problems_root, slug, chosen, audit)
    print(
        f"Published {len(prepared)} bundles, "
        f"{args.per_label * 2} compile-verified submissions each.",
        flush=True,
    )


if __name__ == "__main__":
    main()
