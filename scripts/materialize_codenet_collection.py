"""Verify and install a compile-checked CodeNet collection into data/problems."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.materialize_codenet_exact20 import (  # noqa: E402
    canonical_statement,
    output_section,
    sha256,
)
from scripts.pilot20 import html_to_markdown  # noqa: E402


def safe_extract(archive_path: Path, output: Path, expected: set[str]) -> None:
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            path = Path(member.name)
            if (
                member.name.startswith("/")
                or ".." in path.parts
                or not member.isfile()
                or not path.parts
                or path.parts[0] not in expected
            ):
                raise ValueError(f"Unsafe or unexpected archive member: {member.name}")
        archive.extractall(output, filter="data")


def sample_pairs(markdown: str) -> list[dict]:
    inputs = re.findall(
        r"(?ms)^## Sample Input (\d+)\s*\n```text\n(.*?)```", markdown
    )
    outputs = dict(re.findall(
        r"(?ms)^## Output for the Sample Input (\d+)\s*\n```text\n(.*?)```", markdown
    ))
    if not inputs or {index for index, _ in inputs} != set(outputs):
        raise ValueError("Statement has incomplete sample input/output pairs")
    return [
        {"id": f"sample-{index}", "input": input_text, "output": outputs[index]}
        for index, input_text in inputs
    ]


def verify_problem(directory: Path, archive_hash: str) -> dict:
    problem_id = directory.name
    oracle = directory / "oracle"
    raw_meta_path = directory / "codenet-metadata.json"
    raw_meta = json.loads(raw_meta_path.read_text(encoding="utf-8"))
    if raw_meta.get("id") != problem_id or raw_meta.get("dataset") != "AtCoder":
        raise ValueError(f"Unexpected problem metadata for {problem_id}")

    markdown = html_to_markdown(
        (oracle / "statement.html").read_text(encoding="utf-8")
    )
    requirement = output_section(markdown)
    forbidden = re.compile(
        r"absolute error|relative error|floating[- ]point|real number|"
        r"print any|output any|any valid|any one|one possible|any order|"
        r"order does not matter|multiple (?:answers|solutions)|interactive|"
        r"decimal places|decimal point|within .{0,30}(?:error|difference)",
        re.IGNORECASE | re.DOTALL,
    )
    if forbidden.search(requirement):
        raise ValueError(f"Non-exact output wording in {problem_id}: {requirement}")
    samples = sample_pairs(markdown)
    if any(
        re.search(r"(?<![\w.])[+-]?\d+\.\d+(?![\w.])", sample["output"])
        for sample in samples
    ):
        raise ValueError(f"Real-valued sample output in {problem_id}")

    manifest_path = oracle / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    counts = Counter(row["label"] for row in manifest)
    if counts != Counter({"Accepted": 30, "Wrong Answer": 30}):
        raise ValueError(f"Expected 30/30 for {problem_id}; got {dict(counts)}")
    hashes: set[str] = set()
    normalized: set[tuple[str, str]] = set()
    languages = Counter()
    for row in manifest:
        source = (oracle / row["source"]).resolve()
        if not source.is_relative_to(oracle.resolve()) or not source.is_file():
            raise ValueError(f"Missing or escaped source: {problem_id}/{row['source']}")
        digest = sha256(source)
        normalized_key = (row["label"], row["selection"]["normalized_sha256"])
        if digest != row["sha256"] or digest in hashes or normalized_key in normalized:
            raise ValueError(f"Corrupt or duplicate source: {problem_id}/{row['id']}")
        if row["selection"].get("compile_check") != "passed":
            raise ValueError(f"Source lacks compile evidence: {problem_id}/{row['id']}")
        if row["dialect"] not in {"C", "C++17", "Python3"}:
            raise ValueError(f"Unsupported dialect: {problem_id}/{row['id']}")
        hashes.add(digest)
        normalized.add(normalized_key)
        languages[row["language"]] += 1

    metadata = {
        "problem_id": problem_id,
        "name": raw_meta["name"],
        "dataset": raw_meta["dataset"],
        "time_limit_ms": int(raw_meta["time_limit"]),
        "memory_limit_kb": int(raw_meta["memory_limit"]),
        "curation": {
            "collection": "Project CodeNet exact-output 100x30/30",
            "exact_output": True,
            "real_number_output": False,
            "official_output_requirement": requirement,
            "checker": {"kind": "TOKEN"},
            "compile_checked": True,
        },
        "samples": samples,
    }
    (directory / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (directory / "checker.json").write_text(
        json.dumps({"kind": "TOKEN"}, indent=2) + "\n", encoding="utf-8"
    )
    (directory / "statement.md").write_text(
        canonical_statement(raw_meta["name"], raw_meta, markdown), encoding="utf-8"
    )
    raw_meta_path.unlink()

    provenance_path = oracle / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance.update({
        "source": "IBM Project CodeNet staged parquet snapshot",
        "bundle_sha256": archive_hash,
        "output_screen": {
            "result": "pass",
            "unique_expected_output": True,
            "real_number_output": False,
            "official_output_requirement": requirement,
        },
        "label_note": "Original CodeNet verdicts; every source was compile-checked, not fully rejudged.",
    })
    provenance_path.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "problem_id": problem_id,
        "name": raw_meta["name"],
        "Accepted": 30,
        "Wrong Answer": 30,
        "languages": dict(sorted(languages.items())),
        "samples": len(samples),
        "official_output_requirement": requirement,
    }


def write_collection(output: Path, rows: list[dict], archive_hash: str) -> None:
    payload = {
        "collection": "Project CodeNet exact-output 100x30/30",
        "problem_count": len(rows),
        "submissions_per_problem": {"Accepted": 30, "Wrong Answer": 30},
        "total_submissions": len(rows) * 60,
        "compile_checked": True,
        "bundle_sha256": archive_hash,
        "problems": rows,
    }
    (output / "codenet_exact100_30x30.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Project CodeNet exact-output collection (100 × 30/30)",
        "",
        "Mỗi bài có 30 Accepted và 30 Wrong Answer. Tất cả source đã qua kiểm tra "
        "biên dịch/cú pháp trên GCC, G++ hoặc Python 3 trước khi được chọn.",
        "",
        "| ID | Problem | AC/WA | Languages | Samples |",
        "|---|---|---:|---|---:|",
    ]
    for row in rows:
        languages = ", ".join(f"{key}:{value}" for key, value in row["languages"].items())
        lines.append(
            f"| [{row['problem_id']}]({row['problem_id']}/statement.md) | "
            f"{row['name'].replace('|', '/')} | 30/30 | {languages} | {row['samples']} |"
        )
    lines += ["", f"Bundle SHA-256: `{archive_hash}`", ""]
    (output / "README_codenet_exact100_30x30.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "problems")
    args = parser.parse_args()
    selection = json.loads(args.selection.read_text(encoding="utf-8"))
    if isinstance(selection, dict):
        selection = selection["problems"]
    expected = {
        row["problem_id"] if "problem_id" in row else row["id"] for row in selection
    }
    if len(expected) != 100:
        raise ValueError(f"Expected exactly 100 selected problems; got {len(expected)}")
    existing = sorted(problem_id for problem_id in expected if (args.output / problem_id).exists())
    if existing:
        raise FileExistsError(f"Refusing to overwrite existing problem directories: {existing}")
    archive_hash = sha256(args.archive)
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="codenet100-", dir=args.output.parent) as temp:
        stage = Path(temp)
        safe_extract(args.archive, stage, expected)
        actual = {path.name for path in stage.iterdir() if path.is_dir()}
        if actual != expected:
            raise ValueError(f"Archive set mismatch: missing={expected-actual}, extra={actual-expected}")
        rows = [verify_problem(stage / problem_id, archive_hash) for problem_id in sorted(expected)]
        for problem_id in sorted(expected):
            shutil.copytree(stage / problem_id, args.output / problem_id)
    write_collection(args.output, rows, archive_hash)
    print(json.dumps({
        "problems": len(rows),
        "Accepted": len(rows) * 30,
        "Wrong Answer": len(rows) * 30,
        "bundle_sha256": archive_hash,
    }, indent=2))


if __name__ == "__main__":
    main()
