"""Smoke-run selected CodeNet sources in the existing networkless Docker judge."""
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from testgen.checker import checker_from_profile
from testgen.docker_judge import DockerJudge
from testgen.domain import Solution


PROBES = {
    "p02678": [
        "4 4\n1 2\n1 3\n2 4\n3 4\n",
        "3 3\n1 2\n2 3\n1 3\n",
        "5 4\n1 2\n2 3\n3 4\n4 5\n",
        "5 4\n1 2\n1 3\n1 4\n1 5\n",
        "2 1\n1 2\n",
    ],
    "p03044": [
        "1\n", "2\n1 2 1\n", "2\n1 2 2\n",
        "5\n1 2 2\n2 3 4\n3 4 6\n4 5 8\n",
        "5\n1 2 1\n2 3 1\n3 4 1\n4 5 1\n",
        "4\n1 2 1000000000\n1 3 999999999\n3 4 1\n",
    ],
}


def verify(task):
    pid, row = task
    directory = ROOT / "data" / "problems" / pid
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    profile = json.loads((directory / "checker.json").read_text(encoding="utf-8"))
    if profile["kind"] == "PYTHON_SCRIPT":
        profile["script"] = str((directory / profile["script"]).resolve())
    checker = checker_from_profile(profile)
    judge = DockerJudge(ROOT / "output" / "codenet-additional20-validation" / "build" / pid / row["id"])
    solution = Solution(row["id"], row["label"], row["language"], directory / "oracle" / row["source"], dialect=row["dialect"])
    compiled = judge.compile(solution)
    result = {"problem_id": pid, "submission_id": row["id"], "label": row["label"],
              "language": row["language"], "compile": compiled.verdict, "cases": []}
    if compiled.verdict != "PASS":
        result["stderr"] = compiled.stderr
        return result
    cases = metadata["samples"] + [
        {"id": f"probe-{i}", "input": text, "output": ""}
        for i, text in enumerate(PROBES.get(pid, []), 1)
    ]
    for case in cases:
        run = judge.execute(solution, case["id"], case["input"])
        verdict = run.verdict
        if verdict == "PASS" and not checker.accepts_case(run.actual, case["output"], case["input"]):
            verdict = "WA"
        result["cases"].append({"id": case["id"], "verdict": verdict, "actual": run.actual, "stderr": run.stderr})
    print(f"{pid} {row['label']} {row['id']}: {dict(Counter(c['verdict'] for c in result['cases']))}", flush=True)
    return result


def main():
    collection = json.loads((ROOT / "data" / "problems" / "codenet_additional20.json").read_text(encoding="utf-8"))
    tasks = []
    for problem in collection["problems"]:
        pid = problem["problem_id"]
        manifest = json.loads((ROOT / "data" / "problems" / pid / "oracle" / "manifest.json").read_text(encoding="utf-8"))
        if pid in PROBES:
            for label in ("Accepted", "Wrong Answer"):
                for language in ("C++", "Python"):
                    eligible = [r for r in manifest if r["label"] == label and r["language"] == language]
                    if not eligible:
                        raise ValueError(f"Missing {pid} {label} {language}")
                    tasks.append((pid, eligible[0]))
        else:
            tasks.append((pid, next(r for r in manifest if r["label"] == "Accepted" and r["language"] == "C++")))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(verify, tasks))
    failures = [r for r in results if r["label"] == "Accepted" and
                (r["compile"] != "PASS" or any(c["verdict"] != "PASS" for c in r["cases"]))]
    report = {"scope": "One C++ AC per unique-output problem; one C++ and one Python AC/WA per special problem. Official examples plus hand-written special-checker probes. Not a full rejudge of 800 sources.",
              "programs": len(results), "executions": sum(len(r["cases"]) for r in results),
              "accepted_program_failures": len(failures), "results": results}
    path = ROOT / "output" / "codenet-additional20-validation" / "report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
