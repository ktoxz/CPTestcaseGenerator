"""Helpers for rebuilding Codeforces oracle bundles from dataset exports.

Dataset-specific loading is deliberately kept outside import time so the core
selection helpers work without optional packages such as ``pyarrow``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


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
    passed_test_count: int | None = None


RUNTIMES = (
    (re.compile(r"^(?:GNU )?C\+\+11", re.I), ("C++", "C++11", ".cpp", "gnu++11")),
    (re.compile(r"^(?:GNU )?C\+\+14", re.I), ("C++", "C++14", ".cpp", "gnu++14")),
    (re.compile(r"^(?:GNU )?C\+\+17", re.I), ("C++", "C++17", ".cpp", "gnu++17")),
    (re.compile(r"^(?:GNU )?C11|^C$", re.I), ("C", "C11", ".c", "gnu11")),
    (re.compile(r"Python 2|PyPy 2", re.I), ("Python", "Python2", ".py", None)),
    (re.compile(r"Python 3|PyPy 3", re.I), ("Python", "Python3", ".py", None)),
    (re.compile(r"Java (?:8|1\.8)", re.I), ("Java", "Java8", ".java", None)),
    (re.compile(r"Java (?:11|17|21)", re.I), ("Java", "Java17", ".java", None)),
)


def parse_slug(problem_id: str) -> str:
    match = re.fullmatch(r"cf(\d+)([a-z][0-9]?)", problem_id, re.IGNORECASE)
    if not match:
        raise ValueError(f"Not a Codeforces problem id: {problem_id}")
    return f"{int(match.group(1))}/{match.group(2).upper()}"


def runtime_for(dataset_language: str) -> tuple[str, str, str, str | None] | None:
    # Do not silently downgrade unsupported dialects (notably C++20/MSVC).
    for pattern, runtime in RUNTIMES:
        if pattern.search(dataset_language):
            return runtime
    return None


def _normalized_source(source: str) -> str:
    source = re.sub(r"/\*.*?\*/|//[^\n]*", "", source, flags=re.DOTALL)
    return re.sub(r"\s+", "", source)


def diverse_order(candidates: list[Candidate]) -> list[Candidate]:
    """Deduplicate formatting variants and interleave languages/dialects."""
    unique: list[Candidate] = []
    seen: set[str] = set()
    for item in sorted(candidates, key=lambda c: (-int(c.passed_test_count or 0), str(c.submission_id))):
        digest = hashlib.sha256(_normalized_source(item.source).encode("utf-8")).hexdigest()
        if digest not in seen:
            seen.add(digest)
            unique.append(item)
    buckets: dict[tuple[str, str], list[Candidate]] = {}
    for item in unique:
        buckets.setdefault((item.language, item.dialect), []).append(item)
    ordered: list[Candidate] = []
    keys = sorted(buckets)
    while keys:
        next_keys = []
        for key in keys:
            ordered.append(buckets[key].pop(0))
            if buckets[key]:
                next_keys.append(key)
        keys = next_keys
    return ordered


def write_bundle(problem_id: str, accepted: list[Candidate], wrong: list[Candidate], output: Path, limit: int = 100) -> None:
    destination = output / problem_id / "oracle"
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {"problem_id": problem_id, "source": "dataset-export", "solutions": []}
    for label, values in (("Accepted", diverse_order(accepted)), ("WrongAnswer", diverse_order(wrong))):
        directory = destination / "sources" / label
        directory.mkdir(parents=True, exist_ok=True)
        for index, candidate in enumerate(values[:limit], 1):
            filename = f"{index:02d}-{candidate.submission_id}{candidate.extension}"
            (directory / filename).write_text(candidate.source, encoding="utf-8")
            manifest["solutions"].append({**asdict(candidate), "label": label, "path": f"sources/{label}/{filename}", "source": None})
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", help="Codeforces id such as cf1008a")
    parser.add_argument("--input", type=Path, required=True, help="JSONL export containing submissions")
    parser.add_argument("--output", type=Path, default=Path("data/problems"))
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    slug = parse_slug(args.problem)
    accepted, wrong = [], []
    for line in args.input.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("problem") not in {slug, args.problem}:
            continue
        runtime = runtime_for(str(row.get("language", "")))
        if runtime is None:
            continue
        language, dialect, extension, standard = runtime
        item = Candidate(str(row["submission_id"]), str(row["source"]), str(row["verdict"]),
                         str(row["language"]), language, dialect, extension, standard,
                         row.get("passed_test_count"))
        (accepted if item.verdict in {"OK", "Accepted"} else wrong).append(item)
    write_bundle(args.problem.lower(), accepted, wrong, args.output, args.limit)
    print(json.dumps({"problem": args.problem.lower(), "accepted": min(len(accepted), args.limit),
                      "wrong": min(len(wrong), args.limit)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
