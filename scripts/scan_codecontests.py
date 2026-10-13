"""Find Codeforces contest rows in DeepMind's public CodeContests parquet mirror."""

from __future__ import annotations

import argparse

import duckdb


BASE = (
    "https://huggingface.co/datasets/deepmind/code_contests/resolve/"
    "refs%2Fconvert%2Fparquet/default"
)


def urls() -> list[str]:
    return (
        [f"{BASE}/partial-test/0000.parquet"]
        + [f"{BASE}/partial-train/{index:04d}.parquet" for index in range(7)]
        + [f"{BASE}/partial-valid/0000.parquet"]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contest", type=int, nargs="+")
    parser.add_argument("--counts", action="store_true")
    args = parser.parse_args()

    connection = duckdb.connect()
    connection.execute("LOAD httpfs")
    connection.execute("SET enable_progress_bar=false")
    contest_ids = ", ".join(str(value) for value in sorted(set(args.contest)))
    pieces = []
    for url in urls():
        split, filename = url.rsplit("/", 2)[-2:]
        shard = f"{split}/{filename}"
        pieces.append(
            "SELECT cf_contest_id, cf_index, name, "
            f"'{shard}' AS shard FROM read_parquet('{url}') "
            f"WHERE cf_contest_id IN ({contest_ids})"
        )
    rows = connection.execute(" UNION ALL ".join(pieces)).fetchall()
    if not rows:
        print("NO_MATCH")
        return
    by_shard = {url.rsplit("/", 2)[-2] + "/" + url.rsplit("/", 1)[-1]: url for url in urls()}
    for contest_id, index, name, shard in sorted(rows, key=lambda row: (row[0], row[1])):
        suffix = ""
        if args.counts:
            url = by_shard[shard]
            accepted, incorrect = connection.execute(
                "SELECT array_length(solutions.solution), "
                "array_length(incorrect_solutions.solution) "
                f"FROM read_parquet('{url}') WHERE cf_contest_id = ? AND cf_index = ?",
                [contest_id, index],
            ).fetchone()
            suffix = f"\tAC={accepted}\tNON_AC={incorrect}"
        print(f"{contest_id}\t{index}\t{name}\t{shard}{suffix}")


if __name__ == "__main__":
    main()
