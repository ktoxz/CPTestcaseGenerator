"""Export diverse Accepted/Wrong Answer pools for several CodeNet problems.

This script is intended to run beside the staged Project CodeNet parquet files.
It never modifies the source dataset.  Selection is deterministic and favours
different languages, source-size bands, and normalized token fingerprints.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import tarfile
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.dataset as ds
import pyarrow.parquet as pq


LABEL_DIR = {"Accepted": "Accepted", "Wrong Answer": "WrongAnswer"}
KEEP_IDENTIFIERS = {
    "and", "array", "auto", "bool", "break", "case", "char", "class",
    "const", "continue", "def", "deque", "dict", "double", "elif", "else",
    "false", "float", "for", "from", "gcd", "heapq", "if", "import", "in",
    "int", "lambda", "list", "long", "lower_bound", "map", "max", "min",
    "multiset", "not", "or", "priority_queue", "queue", "range", "return",
    "set", "sort", "sorted", "stack", "static", "string", "struct", "sum",
    "switch", "true", "tuple", "upper_bound", "vector", "while",
}
TOKEN_RE = re.compile(
    r"[A-Za-z_]\w*|\d+(?:\.\d+)?|==|!=|<=|>=|<<|>>|&&|\|\||\*\*|//|"
    r"[-+*/%<>=!&|^~?:;,.()\[\]{}]"
)


def stable_rank(problem_id: str, label: str, submission_id: str) -> str:
    return hashlib.sha256(
        f"codenet-exact20-v1:{problem_id}:{label}:{submission_id}".encode()
    ).hexdigest()


def source_bytes(row: dict) -> bytes:
    raw = row.get("code_raw")
    if raw is not None:
        return bytes(raw)
    return (row.get("code") or "").encode("utf-8")


def runtime_dialect(language: str, original: str) -> str:
    """Map historical CodeNet toolchain labels to this repository's runtimes."""
    if language == "C":
        return "C"
    if language == "C++":
        return "C++17"
    if language == "Java":
        return "Java"
    if language == "Python":
        return "Python" if re.search(r"(?:Python|PyPy)\s*\(?2[.)\s]", original) else "Python3"
    raise ValueError(f"Unsupported language: {language}")


def normalized_tokens(raw: bytes) -> tuple[str, ...]:
    text = raw.decode("utf-8", errors="replace")
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    text = re.sub(r"(?m)//.*$|#.*$", " ", text)
    text = re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"", " STR ", text)
    result = []
    for token in TOKEN_RE.findall(text):
        lowered = token.lower()
        if re.fullmatch(r"[A-Za-z_]\w*", token):
            result.append(lowered if lowered in KEEP_IDENTIFIERS else "ID")
        elif re.fullmatch(r"\d+(?:\.\d+)?", token):
            result.append("NUM")
        else:
            result.append(token)
    return tuple(result)


def fingerprint(tokens: tuple[str, ...]) -> frozenset[str]:
    width = 4
    if len(tokens) < width:
        return frozenset({" ".join(tokens)})
    return frozenset(
        hashlib.blake2s(" ".join(tokens[i:i + width]).encode(), digest_size=6).hexdigest()
        for i in range(len(tokens) - width + 1)
    )


def distance(left: frozenset[str], right: frozenset[str]) -> float:
    union = len(left | right)
    return 1.0 if not union else 1.0 - len(left & right) / union


def prepare_candidate(meta: dict, raw: bytes) -> dict:
    tokens = normalized_tokens(raw)
    return {
        **meta,
        "raw": raw,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "tokens": tokens,
        "normalized_sha256": hashlib.sha256(" ".join(tokens).encode()).hexdigest(),
        "fingerprint": fingerprint(tokens),
        "length_bin": int(math.log2(max(len(raw), 1))),
    }


def diverse_select(candidates: list[dict], limit: int) -> list[dict]:
    unique = {}
    for row in candidates:
        unique.setdefault((row["language"], row["normalized_sha256"]), row)
    pool = sorted(unique.values(), key=lambda row: row["rank"])
    if len(pool) < limit:
        raise RuntimeError(f"Only {len(pool)} structurally unique sources; need {limit}")

    selected = []
    # Seed with one median-sized source from each available language.
    by_language = defaultdict(list)
    for row in pool:
        by_language[row["language"]].append(row)
    for language in sorted(by_language, key=lambda key: (len(by_language[key]), key)):
        rows = sorted(by_language[language], key=lambda row: (len(row["raw"]), row["rank"]))
        selected.append(rows[len(rows) // 2])
        if len(selected) == limit:
            break

    selected_ids = {row["submission_id"] for row in selected}
    while len(selected) < limit:
        language_counts = Counter(row["language"] for row in selected)
        bin_counts = Counter(row["length_bin"] for row in selected)
        best = None
        best_key = None
        for row in pool:
            if row["submission_id"] in selected_ids:
                continue
            structural = min(distance(row["fingerprint"], old["fingerprint"])
                             for old in selected)
            language_bonus = 1.0 / (1 + language_counts[row["language"]])
            size_bonus = 1.0 / (1 + bin_counts[row["length_bin"]])
            key = (0.75 * structural + 0.15 * language_bonus + 0.10 * size_bonus,
                   row["rank"])
            if best_key is None or key > best_key:
                best, best_key = row, key
        assert best is not None
        selected.append(best)
        selected_ids.add(best["submission_id"])
    return selected


def add_bytes(archive: tarfile.TarFile, name: str, body: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(body)
    info.mtime = 0
    archive.addfile(info, io.BytesIO(body))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--problems", required=True, help="Comma-separated pNNNNN IDs")
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--candidates-per-language", type=int, default=80)
    args = parser.parse_args()

    problem_ids = args.problems.split(",")
    if len(problem_ids) != len(set(problem_ids)) or any(
        not re.fullmatch(r"p\d{5}", value) for value in problem_ids
    ):
        raise ValueError("Problems must be unique pNNNNN IDs")
    if not 1 <= args.limit <= 100:
        raise ValueError("limit must be between 1 and 100")

    runtime_data = json.loads(args.runtime_config.read_text(encoding="utf-8"))
    extensions = {}
    for row in runtime_data["runtimes"]:
        language, extension = row["language"], row["extension"]
        extensions.setdefault(language, extension)

    submissions = ds.dataset(str(args.root / "submissions"), format="parquet")
    table = submissions.to_table(
        filter=(ds.field("problem_id").isin(problem_ids)
                & ds.field("status").isin(list(LABEL_DIR))
                & ds.field("language").isin(sorted(extensions)))
    )
    rows = table.to_pylist()
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["problem_id"], row["status"], row["language"])].append(row)

    preselected = []
    shortages = []
    available_counts = defaultdict(Counter)
    for problem_id in problem_ids:
        for label in LABEL_DIR:
            for language in sorted(extensions):
                candidates = grouped[(problem_id, label, language)]
                available_counts[problem_id][label] += len(candidates)
                candidates.sort(key=lambda row: stable_rank(
                    problem_id, label, str(row["submission_id"])))
                preselected.extend(candidates[:args.candidates_per_language])
            if available_counts[problem_id][label] < args.limit:
                shortages.append({
                    "problem": problem_id,
                    "label": label,
                    "available": available_counts[problem_id][label],
                    "required": args.limit,
                })

    if shortages:
        print(json.dumps({
            "shortages": shortages,
            "available": {key: dict(value) for key, value in available_counts.items()},
        }, ensure_ascii=False, indent=2))
        raise RuntimeError(f"{len(shortages)} problem/verdict pools are too small")

    ids = {row["submission_id"] for row in preselected}
    code = ds.dataset(str(args.root / "code"), format="parquet")
    code_rows = code.to_table(filter=ds.field("submission_id").isin(sorted(ids))).to_pylist()
    by_id = {row["submission_id"]: source_bytes(row) for row in code_rows}
    if len(by_id) != len(ids):
        raise RuntimeError(f"Missing {len(ids) - len(by_id)} source rows")

    candidates_by_group = defaultdict(list)
    for row in preselected:
        sid = row["submission_id"]
        raw = by_id[sid]
        if not raw.strip():
            continue
        meta = {
            "submission_id": sid,
            "problem_id": row["problem_id"],
            "label": row["status"],
            "language": row["language"],
            "dialect": row.get("original_language") or "",
            "rank": stable_rank(row["problem_id"], row["status"], str(sid)),
        }
        candidates_by_group[(row["problem_id"], row["status"])].append(
            prepare_candidate(meta, raw)
        )

    descriptions = {
        row["problem_id"]: row for row in
        pq.read_table(args.root / "descriptions.parquet",
                      filters=[("problem_id", "in", problem_ids)]).to_pylist()
    }
    problem_meta = {
        row["id"]: row for row in
        pq.read_table(args.root / "problem_list.parquet",
                      filters=[("id", "in", problem_ids)]).to_pylist()
    }
    if set(descriptions) != set(problem_ids) or set(problem_meta) != set(problem_ids):
        raise RuntimeError("Missing problem statement or problem metadata")

    summary = []
    with tarfile.open(args.output, "w:gz", compresslevel=6) as archive:
        for problem_id in problem_ids:
            base = f"{problem_id}/oracle"
            add_bytes(archive, f"{base}/statement.html",
                      descriptions[problem_id]["html"].encode("utf-8"))
            add_bytes(archive, f"{problem_id}/codenet-metadata.json",
                      (json.dumps(problem_meta[problem_id], ensure_ascii=False, indent=2)
                       + "\n").encode("utf-8"))
            manifest = []
            language_summary = {}
            for label, label_dir in LABEL_DIR.items():
                chosen = diverse_select(candidates_by_group[(problem_id, label)], args.limit)
                language_summary[label] = dict(Counter(row["language"] for row in chosen))
                for index, row in enumerate(chosen, 1):
                    extension = extensions[row["language"]]
                    source = f"sources/{label_dir}/{index:02d}{extension}"
                    add_bytes(archive, f"{base}/{source}", row["raw"])
                    manifest.append({
                        "id": str(row["submission_id"]),
                        "problem_id": problem_id,
                        "label": label,
                        "language": row["language"],
                        "dialect": runtime_dialect(row["language"], row["dialect"]),
                        "original_dialect": row["dialect"],
                        "source": source,
                        "sha256": row["sha256"],
                        "selection": {
                            "method": "greedy normalized-token diversity v1",
                            "rank": index,
                            "source_bytes": len(row["raw"]),
                            "normalized_tokens": len(row["tokens"]),
                            "length_bin_log2": row["length_bin"],
                            "normalized_sha256": row["normalized_sha256"],
                        },
                    })
            provenance = {
                "problem_id": problem_id,
                "dataset": "Project CodeNet",
                "staging_root": str(args.root),
                "selection_method": (
                    "Per verdict, deterministic stratified candidate sampling by language, "
                    "then greedy diversity over language, source-size band, and normalized "
                    "4-token-shingle Jaccard distance."
                ),
                "candidate_limit_per_language": args.candidates_per_language,
                "available_supported_submissions": dict(available_counts[problem_id]),
                "selected_languages": language_summary,
                "labels": {"Accepted": args.limit, "Wrong Answer": args.limit},
            }
            add_bytes(archive, f"{base}/manifest.json",
                      (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode())
            add_bytes(archive, f"{base}/provenance.json",
                      (json.dumps(provenance, ensure_ascii=False, indent=2) + "\n").encode())
            summary.append({
                "problem": problem_id,
                "available": dict(available_counts[problem_id]),
                "selected_languages": language_summary,
            })
    print(json.dumps({"problems": summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
