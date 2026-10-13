"""Export a deterministic 20:20 C++ bundle from DeepMind CodeContests."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import duckdb


BASE = (
    "https://huggingface.co/datasets/deepmind/code_contests/resolve/"
    "refs%2Fconvert%2Fparquet/default"
)
CPP = 2


def unique_cpp(pool: dict) -> list[tuple[str, str]]:
    result: dict[str, str] = {}
    for language, source in zip(pool["language"], pool["solution"], strict=True):
        if language != CPP:
            continue
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
        result.setdefault(digest, source)
    return sorted(result.items())


def write_sources(
    problem_id: str,
    problem_dir: Path,
    label: str,
    pool: dict,
    limit: int,
) -> list[dict]:
    selected = []
    for digest, source in unique_cpp(pool):
        compiled = subprocess.run(
            ["g++", "-std=gnu++17", "-fsyntax-only", "-x", "c++", "-"],
            input=source.encode("utf-8"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if compiled.returncode == 0:
            selected.append((digest, source))
        if len(selected) == limit:
            break
    if len(selected) < limit:
        raise RuntimeError(
            f"{problem_id}/{label}: only {len(selected)} unique, locally compilable C++ sources"
        )
    directory_name = "Accepted" if label == "Accepted" else "WrongAnswer"
    relative_dir = Path("oracle") / "sources" / directory_name
    output_dir = problem_dir / relative_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for ordinal, (digest, source) in enumerate(selected, 1):
        filename = f"{ordinal:02d}.cpp"
        relative_path = relative_dir / filename
        (problem_dir / relative_path).write_text(source, encoding="utf-8", newline="\n")
        short_label = "ac" if label == "Accepted" else "wa"
        manifest.append(
            {
                "id": f"{problem_id}-{short_label}-{ordinal:02d}",
                "problem_id": problem_id,
                "label": label,
                "language": "C++",
                # The upstream dataset name is provenance, not a compiler
                # dialect.  Keep the runtime-facing value resolvable by the
                # local judge.
                "dialect": "C++17",
                "source": relative_path.as_posix().removeprefix("oracle/"),
                "sha256": digest,
            }
        )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contest", type=int)
    parser.add_argument("index")
    parser.add_argument("shard", help="For example: partial-train/0003.parquet")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--root", type=Path, default=Path("data/problems"))
    args = parser.parse_args()
    index = args.index.upper()
    problem_id = f"cf{args.contest}{index.lower()}"
    problem_dir = args.root / problem_id
    problem_dir.mkdir(parents=True, exist_ok=True)

    url = f"{BASE}/{args.shard}"
    connection = duckdb.connect()
    connection.execute("LOAD httpfs")
    connection.execute("SET enable_progress_bar=false")
    row = connection.execute(
        "SELECT name, description, cf_rating, cf_tags, public_tests, "
        "solutions, incorrect_solutions "
        f"FROM read_parquet('{url}') WHERE cf_contest_id = ? AND cf_index = ?",
        [args.contest, index],
    ).fetchone()
    if row is None:
        raise RuntimeError(f"No CodeContests row for {args.contest}{index} in {args.shard}")
    name, description, rating, tags, public_tests, accepted, incorrect = row

    statement = (
        f"# {index}. {name.split('. ', 1)[-1]}\n\n"
        f"Source: https://codeforces.com/contest/{args.contest}/problem/{index}\n\n"
        f"{description.strip()}\n"
    )
    (problem_dir / "statement.md").write_text(statement, encoding="utf-8", newline="\n")
    metadata = {
        "problem_id": problem_id,
        "contest_id": args.contest,
        "index": index,
        "name": name,
        "url": f"https://codeforces.com/contest/{args.contest}/problem/{index}",
        "rating": rating,
        "tags": tags,
        "public_tests": public_tests,
    }
    (problem_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    manifest = write_sources(problem_id, problem_dir, "Accepted", accepted, args.limit)
    manifest += write_sources(problem_id, problem_dir, "Wrong Answer", incorrect, args.limit)
    oracle_dir = problem_dir / "oracle"
    (oracle_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    provenance = {
        "problem_id": problem_id,
        "dataset": "DeepMind CodeContests",
        "dataset_url": "https://huggingface.co/datasets/deepmind/code_contests",
        "upstream_repository": "https://github.com/google-deepmind/code_contests",
        "parquet_shard": args.shard,
        "selection": (
            "First 20 unique C++ sources that compile locally with gnu++17 after "
            "sorting by SHA-256, per label"
        ),
        "labels": {"Accepted": args.limit, "Wrong Answer": args.limit},
        "note": "CodeContests labels these as correct and incorrect human submissions.",
    }
    (oracle_dir / "provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {"problem": problem_id, "Accepted": args.limit, "Wrong Answer": args.limit}
        )
    )


if __name__ == "__main__":
    main()
