"""Materialize and verify the curated 20-problem Project CodeNet bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tarfile
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.pilot20 import html_to_markdown  # noqa: E402


SELECTION = {
    "p02548": ("arithmetic/enumeration", "integer"),
    "p02574": ("number theory and sieve", "fixed classification string"),
    "p02580": ("grid frequency counting", "integer"),
    "p02661": ("sorting and median counting", "integer"),
    "p02685": ("modular combinatorics", "integer modulo 998244353"),
    "p02709": ("sorting and interval DP", "integer"),
    "p02732": ("frequency counting and contributions", "one integer per line"),
    "p02768": ("modular combinatorics", "integer modulo 1000000007"),
    "p02781": ("digit DP/combinatorics", "integer"),
    "p02813": ("permutation ranking/enumeration", "integer"),
    "p02839": ("grid DP/bitset DP", "integer"),
    "p02949": ("graph shortest paths/Bellman-Ford", "integer or fixed -1 sentinel"),
    "p02959": ("greedy", "integer"),
    "p02986": ("tree traversal and prefix XOR", "one integer per query"),
    "p03003": ("sequence dynamic programming", "integer modulo 1000000007"),
    "p03040": ("online median/data structure", "two integers per query"),
    "p03274": ("sorted sliding window/greedy", "integer"),
    "p03286": ("negative-base conversion", "unique base -2 digit string"),
    "p03575": ("graph bridge detection", "integer"),
    "p03862": ("greedy", "integer"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256(path)))
    return digest.hexdigest()


def copytree_with_retry(source: Path, destination: Path) -> None:
    last_error = None
    for attempt in range(5):
        try:
            shutil.copytree(source, destination)
            return
        except PermissionError as error:
            last_error = error
            time.sleep(0.5 * (attempt + 1))
    assert last_error is not None
    raise last_error


def runtime_dialect(language: str, original: str) -> str:
    if language == "C":
        return "C"
    if language == "C++":
        return "C++17"
    if language == "Java":
        return "Java"
    if language == "Python":
        return "Python" if re.search(r"(?:Python|PyPy)\s*\(?2[.)\s]", original) else "Python3"
    raise ValueError(f"Unsupported language: {language}")


def output_section(markdown: str) -> str:
    match = re.search(r"(?ims)^## Output\s*\n(.*?)(?=^## |\Z)", markdown)
    if not match:
        raise ValueError("Statement has no Output section")
    return " ".join(match.group(1).split())


def canonical_statement(name: str, problem: dict, body: str) -> str:
    return (
        f"# {name}\n\n"
        f"- CodeNet ID: `{problem['id']}`\n"
        f"- Dataset: `{problem['dataset']}`\n"
        f"- Time limit: `{problem['time_limit']} ms`\n"
        f"- Memory limit: `{problem['memory_limit']} KB`\n\n"
        f"{body.strip()}\n"
    )


def safe_extract(archive_path: Path, output: Path) -> None:
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            path = Path(member.name)
            if (member.name.startswith("/") or ".." in path.parts or not member.isfile()
                    or not path.parts or path.parts[0] not in SELECTION):
                raise ValueError(f"Unsafe or unexpected archive member: {member.name}")
        archive.extractall(output, filter="data")


def verify_and_prepare(problem_dir: Path, bundle_hash: str) -> dict:
    problem_id = problem_dir.name
    oracle = problem_dir / "oracle"
    raw_meta_path = problem_dir / "codenet-metadata.json"
    problem = json.loads(raw_meta_path.read_text(encoding="utf-8"))
    if problem.get("id") != problem_id or problem.get("dataset") != "AtCoder":
        raise ValueError(f"Unexpected metadata for {problem_id}")

    html_path = oracle / "statement.html"
    markdown = html_to_markdown(html_path.read_text(encoding="utf-8"))
    requirement = output_section(markdown)
    forbidden = re.compile(
        r"absolute error|relative error|accepted if|print any|any valid|"
        r"one possible|multiple answers|floating[- ]point|real number",
        re.IGNORECASE,
    )
    if forbidden.search(requirement):
        raise ValueError(f"Non-exact output wording in {problem_id}: {requirement}")
    # Sample outputs must not contain decimal real-number tokens.
    sample_outputs = re.findall(
        r"(?ims)^## (?:Output for the )?Sample (?:Output|Input and Output).*?```text\n(.*?)```",
        markdown,
    )
    if any(re.search(r"(?<![\w.])[+-]?\d+\.\d+(?![\w.])", block)
           for block in sample_outputs):
        raise ValueError(f"Real-valued sample output in {problem_id}")

    manifest_path = oracle / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    counts = Counter(row["label"] for row in manifest)
    if counts != Counter({"Accepted": 20, "Wrong Answer": 20}):
        raise ValueError(f"Incorrect 20/20 pool for {problem_id}: {dict(counts)}")
    languages = Counter()
    source_hashes = set()
    normalized_hashes = {"Accepted": set(), "Wrong Answer": set()}
    for row in manifest:
        source = (oracle / row["source"]).resolve()
        if not source.is_relative_to(oracle.resolve()) or not source.is_file():
            raise ValueError(f"Missing/escaped source in {problem_id}: {row['source']}")
        actual = sha256(source)
        if actual != row["sha256"] or actual in source_hashes:
            raise ValueError(f"Bad or duplicate source hash in {problem_id}: {row['id']}")
        source_hashes.add(actual)
        normalized = row["selection"]["normalized_sha256"]
        if normalized in normalized_hashes[row["label"]]:
            raise ValueError(f"Duplicate normalized structure in {problem_id}: {row['id']}")
        normalized_hashes[row["label"]].add(normalized)
        original = row.get("original_dialect", row.get("dialect", ""))
        row["original_dialect"] = original
        row["dialect"] = runtime_dialect(row["language"], original)
        languages[row["language"]] += 1
    if set(languages) != {"C", "C++", "Java", "Python"}:
        raise ValueError(f"Expected four-language diversity in {problem_id}: {dict(languages)}")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    algorithm, domain = SELECTION[problem_id]
    metadata = {
        "problem_id": problem_id,
        "name": problem["name"],
        "dataset": problem["dataset"],
        "time_limit_ms": int(problem["time_limit"]),
        "memory_limit_kb": int(problem["memory_limit"]),
        "curation": {
            "collection": "Project CodeNet exact-output 20x20",
            "exact_output": True,
            "real_number_output": False,
            "algorithm_family": algorithm,
            "output_domain": domain,
            "official_output_requirement": requirement,
        },
    }
    (problem_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (problem_dir / "statement.md").write_text(
        canonical_statement(problem["name"], problem, markdown), encoding="utf-8", newline="\n"
    )
    raw_meta_path.unlink()

    provenance_path = oracle / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance.update({
        "source": "IBM Project CodeNet staged parquet snapshot",
        "bundle_sha256": bundle_hash,
        "exact_output_screen": {
            "result": "pass",
            "unique_expected_output": True,
            "real_number_output": False,
            "official_output_requirement": requirement,
        },
    })
    provenance_path.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "problem_id": problem_id,
        "name": problem["name"],
        "algorithm_family": algorithm,
        "output_domain": domain,
        "official_output_requirement": requirement,
        "Accepted": counts["Accepted"],
        "Wrong Answer": counts["Wrong Answer"],
        "languages": dict(sorted(languages.items())),
    }


def write_collection(problems_root: Path, rows: list[dict], bundle_hash: str) -> None:
    payload = {
        "collection": "Project CodeNet exact-output 20x20",
        "problem_count": len(rows),
        "submissions_per_problem": {"Accepted": 20, "Wrong Answer": 20},
        "total_submissions": sum(row["Accepted"] + row["Wrong Answer"] for row in rows),
        "bundle_sha256": bundle_hash,
        "screening": (
            "English official Output section manually reviewed for a unique deterministic "
            "integer/fixed-string result; tolerance, real-number, interactive, and "
            "constructive/multiple-valid-output tasks excluded."
        ),
        "submission_selection": (
            "Deterministic stratified sampling by language followed by greedy diversity "
            "over language, source-size band, and normalized token 4-shingles."
        ),
        "problems": rows,
    }
    (problems_root / "codenet_exact20.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Project CodeNet exact-output collection (20 × 20/20)",
        "",
        "Mỗi bài có đúng 20 Accepted và 20 Wrong Answer. Các bài có output số thực, "
        "sai số cho phép, interactive, constructive hoặc nhiều output hợp lệ đã bị loại.",
        "",
        "Submission được chọn có tính tái lập và đa dạng theo ngôn ngữ, dải kích thước "
        "source và khoảng cách Jaccard giữa fingerprint token đã chuẩn hóa.",
        "",
        "| ID | Problem | Algorithm family | Output | AC/WA | Languages |",
        "|---|---|---|---|---:|---|",
    ]
    for row in rows:
        languages = ", ".join(f"{key}:{value}" for key, value in row["languages"].items())
        lines.append(
            f"| {row['problem_id']} | {row['name'].replace('|', '/')} | "
            f"{row['algorithm_family']} | {row['output_domain']} | 20/20 | {languages} |"
        )
    lines.extend(["", f"Bundle SHA-256: `{bundle_hash}`", ""])
    (problems_root / "README_codenet_exact20.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "problems")
    parser.add_argument("--resume", action="store_true",
                        help="Keep an existing directory only when it exactly matches")
    args = parser.parse_args()
    if not args.archive.is_file():
        raise FileNotFoundError(args.archive)
    args.output.mkdir(parents=True, exist_ok=True)
    existing = [problem_id for problem_id in SELECTION if (args.output / problem_id).exists()]
    if existing and not args.resume:
        raise FileExistsError(f"Refusing to overwrite existing problem directories: {existing}")

    bundle_hash = sha256(args.archive)
    with tempfile.TemporaryDirectory(prefix="codenet-exact20-", dir=args.output.parent,
                                     ignore_cleanup_errors=True) as temp:
        staging = Path(temp)
        safe_extract(args.archive, staging)
        if {path.name for path in staging.iterdir() if path.is_dir()} != set(SELECTION):
            raise ValueError("Archive problem set does not match the curated selection")
        rows = [verify_and_prepare(staging / problem_id, bundle_hash)
                for problem_id in sorted(SELECTION)]
        for problem_id in sorted(SELECTION):
            source = staging / problem_id
            destination = args.output / problem_id
            if destination.exists():
                if tree_digest(source) != tree_digest(destination):
                    raise ValueError(f"Existing directory differs from bundle: {destination}")
                continue
            copytree_with_retry(source, destination)
    write_collection(args.output, rows, bundle_hash)
    print(json.dumps({
        "problems": len(rows),
        "Accepted": sum(row["Accepted"] for row in rows),
        "Wrong Answer": sum(row["Wrong Answer"] for row in rows),
        "bundle_sha256": bundle_hash,
    }, indent=2))


if __name__ == "__main__":
    main()
