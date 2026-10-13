"""Select 100 deterministic exact-output CodeNet problems with large AC/WA pools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.materialize_codenet_exact20 import output_section  # noqa: E402
from scripts.pilot20 import html_to_markdown  # noqa: E402


OUTPUT_FORBIDDEN = re.compile(
    r"absolute error|relative error|floating[- ]point|real number|"
    r"print any|output any|any valid|any one|one possible|any order|"
    r"order does not matter|multiple (?:answers|solutions)|interactive|"
    r"decimal places|decimal point|within .{0,30}(?:error|difference)|"
    r"one such|satisf(?:y|ies|ying) (?:all|the following)|"
    r"in the first line.{0,250}(?:second|following|next) line|"
    r"print (?:a |the )?sequence of operations|print the formula you made",
    re.IGNORECASE | re.DOTALL,
)
STATEMENT_FORBIDDEN = re.compile(
    r"multiple correct (?:answers|outputs)|(?:print|output) any (?:one|valid)|"
    r"any (?:answer|output) (?:is|will be) accepted|if there are several answers|"
    r"you may (?:print|output) any|interactive problem",
    re.IGNORECASE,
)
DECIMAL_TOKEN = re.compile(r"(?<![\w.])[+-]?\d+\.\d+(?![\w.])")


def existing_codenet_ids(problems_root: Path) -> set[str]:
    return {
        path.name for path in problems_root.glob("p[0-9][0-9][0-9][0-9][0-9]")
        if path.is_dir()
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pools", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--minimum-pool", type=int, default=45)
    parser.add_argument("--problems-root", type=Path, default=ROOT / "data" / "problems")
    args = parser.parse_args()

    pools = {
        row["problem_id"]: row
        for row in json.loads(args.pools.read_text(encoding="utf-8"))
    }
    descriptions = {
        row["problem_id"]: row
        for row in pq.read_table(ROOT / ".codenet-descriptions.parquet").to_pylist()
    }
    metadata = {
        row["id"]: row
        for row in pq.read_table(ROOT / "data" / "raw" / "problem_list.parquet").to_pylist()
    }
    existing = existing_codenet_ids(args.problems_root)
    eligible = []
    rejected: dict[str, int] = {}
    for problem_id, pool in pools.items():
        problem = metadata.get(problem_id)
        description = descriptions.get(problem_id)
        reason = None
        if problem_id in existing:
            reason = "already_present"
        elif not problem or not description or problem["dataset"] != "AtCoder":
            reason = "metadata"
        elif min(pool["Accepted"], pool["Wrong Answer"]) < args.minimum_pool:
            reason = "small_pool"
        else:
            try:
                markdown = html_to_markdown(description["html"])
                requirement = output_section(markdown)
            except Exception:
                reason = "unparseable_statement"
            else:
                if OUTPUT_FORBIDDEN.search(requirement) or STATEMENT_FORBIDDEN.search(markdown):
                    reason = "non_unique_output"
                else:
                    sample_outputs = re.findall(
                        r"(?ims)^## Output for the Sample Input \d+\s*\n```text\n(.*?)```",
                        markdown,
                    )
                    if not sample_outputs:
                        reason = "missing_samples"
                    elif any(DECIMAL_TOKEN.search(block) for block in sample_outputs):
                        reason = "real_output"
        if reason:
            rejected[reason] = rejected.get(reason, 0) + 1
            continue
        eligible.append({
            "problem_id": problem_id,
            "name": problem["name"],
            "dataset": problem["dataset"],
            "pool": {
                "Accepted": pool["Accepted"],
                "Wrong Answer": pool["Wrong Answer"],
            },
            "available_languages": pool["languages"],
            "official_output_requirement": requirement,
        })

    eligible.sort(key=lambda row: row["problem_id"])
    if len(eligible) < args.count:
        raise RuntimeError(f"Only {len(eligible)} eligible problems; need {args.count}")
    selected = []
    for index in range(args.count):
        start = index * len(eligible) // args.count
        stop = (index + 1) * len(eligible) // args.count
        stratum = eligible[start:stop]
        selected.append(max(
            stratum,
            key=lambda row: (
                min(row["pool"].values()),
                sum(row["pool"].values()),
                row["problem_id"],
            ),
        ))
    payload = {
        "collection": "Project CodeNet exact-output 100x30/30",
        "selection": (
            "One problem from each ordered-ID stratum, maximizing the smaller "
            "supported AC/WA pool within the stratum. Existing local CodeNet problems excluded."
        ),
        "minimum_pool_before_compile": args.minimum_pool,
        "problem_count": len(selected),
        "eligible_count": len(eligible),
        "rejected": rejected,
        "problems": selected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "selected": len(selected),
        "eligible": len(eligible),
        "rejected": rejected,
        "minimum_selected_pool": min(
            min(row["pool"].values()) for row in selected
        ),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
