"""Count verdicts for selected contests in the public Python submissions dataset."""

from __future__ import annotations

import argparse

import duckdb


BASE = (
    "https://huggingface.co/datasets/MatrixStudio/Codeforces-Python-Submissions/"
    "resolve/refs%2Fconvert%2Fparquet/default"
)


def urls() -> list[str]:
    return [f"{BASE}/test/0000.parquet"] + [
        f"{BASE}/train/{index:04d}.parquet" for index in range(9)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contest", type=int, nargs="*")
    args = parser.parse_args()
    ids = ", ".join(str(value) for value in sorted(set(args.contest)))

    connection = duckdb.connect()
    connection.execute("LOAD httpfs")
    connection.execute("SET enable_progress_bar=false")
    condition = f" WHERE contestId IN ({ids})" if ids else ""
    pieces = [
        "SELECT contestId, index, verdict, programmingLanguage "
        f"FROM read_parquet('{url}'){condition}" for url in urls()
    ]
    if not ids:
        summary = connection.execute(
            "SELECT min(contestId), max(contestId), count(DISTINCT contestId), count(*) "
            f"FROM ({' UNION ALL '.join(pieces)}) rows"
        ).fetchone()
        print("SUMMARY\t" + "\t".join(str(value) for value in summary))
        return
    query = (
        "SELECT contestId, index, verdict, programmingLanguage, count(*) AS amount "
        f"FROM ({' UNION ALL '.join(pieces)}) rows "
        "GROUP BY ALL ORDER BY contestId, index, verdict, programmingLanguage"
    )
    for row in connection.execute(query).fetchall():
        print("\t".join(str(value) for value in row))


if __name__ == "__main__":
    main()
