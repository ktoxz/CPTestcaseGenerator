"""Golden reports and artifacts captured from the pre-refactor implementation.
Only elapsed timings and temporary root paths are normalized.
"""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from test_pipeline import FakeSolutions, FakeCases, FakeJudge
from testgen.pipeline import Pipeline
from testgen.checker import checker_from_profile
from testgen.domain import Solution, Result
ROOT = Path(__file__).resolve().parents[1]

class Pool(FakeSolutions):
    def generate(self, statement, output):
        base = super().generate(statement, output)
        return base[:2] + [Solution(f"wa{i}", "candidate_wa", "Python", base[0].source,
                                   witness_input=f"{i}\n") for i in range(1, 6)]

class Judge(FakeJudge):
    def execute(self, solution, case_id, input_text):
        if solution.id == "validator":
            return Result(solution.id, "PASS", case_id)
        return Result(solution.id, "PASS", case_id, "2.000\n" if solution.id.startswith("wa") else "1.000\n")

class RepairCases(FakeCases):
    def generate(self, *args):
        return {"requested_count": 2, "cases": [{"input": "invalid"}, {"input": "valid"}]}
    def repair_batch(self, statement, feedback, rejected, attempt):
        return [{"proposal_index": r["proposal_index"], "input": "repaired"} for r in rejected]

class RepairJudge(Judge):
    def execute(self, solution, case_id, input_text):
        if solution.id == "validator" and input_text == "invalid\n":
            return Result(solution.id, "RE", case_id, stderr="invalid input")
        return super().execute(solution, case_id, input_text)

def stable(value, root):
    if isinstance(value, dict):
        return {k: stable(v, root) for k,v in value.items() if k not in {"latency_ms", "elapsed_seconds", "target_met"}}
    if isinstance(value, list): return [stable(v, root) for v in value]
    if isinstance(value, str): return value.replace(str(root), "<RUN>")
    return value

def run(cls, scenario):
    with TemporaryDirectory(dir=ROOT / "tmp") as d:
        root=Path(d)
        solutions = Pool() if scenario == "holdout" else FakeSolutions()
        cases = RepairCases() if scenario == "repair" else FakeCases()
        judge = RepairJudge() if scenario == "repair" else Judge()
        report = cls(solutions, cases, judge, checker_from_profile({"kind":"TOKEN"}),
                     min_total_cases=1, min_iterations=1).run("fixture", "statement", root, iterations=2)
        artifacts = {}
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.name == "checkpoint.json": continue
            text=path.read_text(encoding="utf-8")
            if path.suffix == ".json": value=json.loads(text)
            elif path.suffix == ".jsonl": value=[json.loads(line) for line in text.splitlines()]
            else: value=text
            artifacts[path.relative_to(root).as_posix()]=stable(value,root)
        return {"report":stable(report,root), "artifacts":artifacts}

@pytest.mark.parametrize("scenario", ["basic", "holdout", "repair"])
def test_report_and_artifact_parity(scenario):
    expected = json.loads((ROOT / "tests/fixtures/refactor" / (scenario + ".json")).read_text(encoding="utf-8"))
    assert run(Pipeline, scenario) == expected
