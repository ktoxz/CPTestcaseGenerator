"""Count compile-checkable CodeNet AC/WA pools for candidate problems.

This script is designed to run on the host containing the staged parquet
snapshot.  It reads only submission metadata; source code is handled by the
separate collection exporter.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

import pyarrow.dataset as ds


def is_supported(row: dict) -> bool:
    language = row.get("language")
    dialect = row.get("original_language") or ""
    if language in {"C", "C++"}:
        return True
    return language == "Python" and not any(
        marker in dialect for marker in ("Python (2", "PyPy2")
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate_rows = json.loads(args.candidates.read_text(encoding="utf-8"))
    candidate_ids = [row["id"] if isinstance(row, dict) else row for row in candidate_rows]
    counts: dict[str, dict[str, Counter]] = defaultdict(
        lambda: defaultdict(Counter)
    )
    scanner = ds.dataset(str(args.root / "submissions"), format="parquet").scanner(
        columns=["problem_id", "status", "language", "original_language"],
        filter=(
            ds.field("problem_id").isin(candidate_ids)
            & ds.field("status").isin(["Accepted", "Wrong Answer"])
            & ds.field("language").isin(["C", "C++", "Python"])
        ),
        batch_size=32_768,
        use_threads=True,
    )
    scanned = 0
    for batch in scanner.to_batches():
        for row in batch.to_pylist():
            if is_supported(row):
                counts[row["problem_id"]][row["status"]][row["language"]] += 1
        scanned += batch.num_rows
        if scanned and scanned % 1_000_000 < batch.num_rows:
            print(f"scanned {scanned} matching submission rows", flush=True)

    result = []
    for problem_id in candidate_ids:
        labels = counts[problem_id]
        result.append({
            "problem_id": problem_id,
            "Accepted": sum(labels["Accepted"].values()),
            "Wrong Answer": sum(labels["Wrong Answer"].values()),
            "languages": {
                label: dict(sorted(labels[label].items()))
                for label in ("Accepted", "Wrong Answer")
            },
        })
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "candidates": len(candidate_ids),
        "with_30_30": sum(
            row["Accepted"] >= 30 and row["Wrong Answer"] >= 30 for row in result
        ),
        "with_45_45": sum(
            row["Accepted"] >= 45 and row["Wrong Answer"] >= 45 for row in result
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
