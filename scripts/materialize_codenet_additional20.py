"""Verify and install the second CodeNet collection, without replacing old data."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import materialize_codenet_exact20 as common
from scripts.pilot20 import html_to_markdown

SELECTION = {
    "p02554": ("inclusion-exclusion", "integer modulo 1000000007"),
    "p02555": ("composition counting / DP", "integer modulo 1000000007"),
    "p02584": ("greedy / parity", "integer"),
    "p02585": ("permutation cycles", "integer"),
    "p02586": ("grid DP", "integer"),
    "p02596": ("modular arithmetic", "integer or -1"),
    "p02598": ("binary search", "integer (rounded up)"),
    "p02599": ("offline range queries / Fenwick tree", "integer per query"),
    "p02614": ("bitmask enumeration", "integer"),
    "p02623": ("prefix sums / two pointers", "integer"),
    "p02629": ("bijective base 26", "unique lowercase string"),
    "p02642": ("sieve / duplicate counting", "integer"),
    "p02678": ("BFS / shortest-path tree", "any valid shortest-path predecessors"),
    "p02691": ("frequency counting", "integer"),
    "p02702": ("suffix remainders", "integer"),
    "p02714": ("counting / excluded arithmetic progressions", "integer"),
    "p02720": ("BFS enumeration", "integer"),
    "p02762": ("DSU / connected components", "integer sequence"),
    "p02787": ("unbounded knapsack", "integer"),
    "p03044": ("tree distance parity", "any valid binary coloring"),
}
SPECIAL = {"p02678", "p03044"}


def prepare(directory: Path, bundle_hash: str) -> dict:
    pid = directory.name
    oracle = directory / "oracle"
    raw_path = directory / "codenet-metadata.json"
    meta = json.loads(raw_path.read_text(encoding="utf-8"))
    if meta["id"] != pid or meta["dataset"] != "AtCoder":
        raise ValueError(f"Unexpected metadata: {pid}")
    body = html_to_markdown((oracle / "statement.html").read_text(encoding="utf-8"))
    requirement = common.output_section(body)
    profile = ({"kind": "PYTHON_SCRIPT", "script": "output_checker.py", "function": "accepts"}
               if pid in SPECIAL else {"kind": "TOKEN" if pid == "p02762" else "EXACT"})
    if pid not in SPECIAL and re.search(
        r"absolute error|relative error|print any|multiple (?:answers|solutions|colorings)",
        requirement, re.I,
    ):
        raise ValueError(f"Non-exact output: {pid}")
    manifest = json.loads((oracle / "manifest.json").read_text(encoding="utf-8"))
    counts = Counter(row["label"] for row in manifest)
    if counts != {"Accepted": 20, "Wrong Answer": 20}:
        raise ValueError(f"Incorrect pool counts: {pid} {counts}")
    hashes, normalized, languages = set(), set(), Counter()
    for row in manifest:
        source = (oracle / row["source"]).resolve()
        if not source.is_relative_to(oracle.resolve()) or not source.is_file():
            raise ValueError(f"Missing/escaped source: {pid}")
        digest = common.sha256(source)
        key = (row["label"], row["selection"]["normalized_sha256"])
        if digest != row["sha256"] or digest in hashes or key in normalized:
            raise ValueError(f"Corrupt or duplicate source: {pid} {row['id']}")
        if row["problem_id"] != pid:
            raise ValueError(f"Wrong submission problem: {pid}")
        hashes.add(digest)
        normalized.add(key)
        languages[row["language"]] += 1
        row["dialect"] = common.runtime_dialect(row["language"], row["original_dialect"])
    (oracle / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    samples_in = re.findall(r"(?ms)^## Sample Input (\d+)\s*\n```text\n(.*?)```", body)
    samples_out = dict(re.findall(r"(?ms)^## Output for the Sample Input (\d+)\s*\n```text\n(.*?)```", body))
    if not samples_in or {i for i, _ in samples_in} != set(samples_out):
        raise ValueError(f"Incomplete examples: {pid}")
    samples = [{"id": f"sample-{i}", "input": text, "output": samples_out[i]} for i, text in samples_in]
    algorithm, domain = SELECTION[pid]
    curation = {"collection": "CodeNet additional20 20261012", "exact_output": pid not in SPECIAL,
                "real_number_output": False, "algorithm_family": algorithm, "output_domain": domain,
                "official_output_requirement": requirement, "checker": profile}
    metadata = {"problem_id": pid, "name": meta["name"], "dataset": meta["dataset"],
                "time_limit_ms": int(meta["time_limit"]), "memory_limit_kb": int(meta["memory_limit"]),
                "curation": curation, "samples": samples}
    (directory / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (directory / "statement.md").write_text(common.canonical_statement(meta["name"], meta, body), encoding="utf-8")
    (directory / "checker.json").write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    if pid in SPECIAL:
        shutil.copyfile(ROOT / "scripts" / "codenet_checkers" / f"{pid}.py", directory / "output_checker.py")
    raw_path.unlink()
    provenance_path = oracle / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance.update({"bundle_sha256": bundle_hash, "output_screen": curation,
                       "label_note": "Original CodeNet verdicts; not reclassified by local sample tests."})
    provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"problem_id": pid, "name": meta["name"], "checker": profile["kind"],
            "algorithm_family": algorithm, "output_domain": domain, "languages": dict(languages),
            "Accepted": 20, "Wrong Answer": 20, "samples": len(samples)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "problems")
    args = parser.parse_args()
    existing = [p for p in SELECTION if (args.output / p).exists()]
    if existing:
        raise FileExistsError(f"Will not overwrite: {existing}")
    args.output.mkdir(parents=True, exist_ok=True)
    digest = common.sha256(args.archive)
    common.SELECTION = SELECTION
    with tempfile.TemporaryDirectory(dir=args.output.parent, prefix="additional20-") as temp:
        stage = Path(temp)
        common.safe_extract(args.archive, stage)
        if {p.name for p in stage.iterdir()} != set(SELECTION):
            raise ValueError("Archive problem set differs")
        rows = [prepare(stage / pid, digest) for pid in sorted(SELECTION)]
        for pid in sorted(SELECTION):
            common.copytree_with_retry(stage / pid, args.output / pid)
    report = {"collection": "CodeNet additional20 20261012", "problem_count": 20,
              "total_submissions": 800, "bundle_sha256": digest, "problems": rows}
    (args.output / "codenet_additional20.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
