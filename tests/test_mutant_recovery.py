"""Recovery retries preserve certification and stop after at most four extra rounds."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from test_pipeline import FakeCases, FakeJudge, FakeSolutions
from testgen.domain import Solution, Result
from testgen.pipeline import Pipeline
from testgen.checker import checker_from_profile
from testgen.llm_contract import LLMTransportError

ROOT = Path(__file__).resolve().parents[1]

class RecoverySolutions(FakeSolutions):
    def __init__(self, success_round=None, transport_rounds=(), invalid=False):
        self.success_round = success_round
        self.transport_rounds = transport_rounds
        self.invalid = invalid
        self.rounds = []
        self.counts = []

    def requested_wrong_candidates(self): return 5

    def generate(self, statement, output):
        rows = super().generate(statement, output)
        # Keep two already verified mutants through all recovery attempts.
        return rows[:2] + [Solution(f"wa{i}", "candidate_wa", "Python", rows[0].source,
                                   witness_input="1 2\n") for i in (1, 2)]

    def regenerate_wrong(self, statement, output, count, rejected, existing, round_number):
        if round_number == 0: return []
        self.rounds.append(round_number); self.counts.append(count)
        if round_number in self.transport_rounds: raise LLMTransportError("offline")
        if round_number != self.success_round and not self.invalid: return []
        path = output / f"recovery-{round_number}.py"
        path.write_text("# fake", encoding="utf-8")
        return [Solution(f"recovery-{round_number}", "candidate_wa", "Python", path,
                         witness_input="1 2\n")]

class RecoveryJudge(FakeJudge):
    def __init__(self, invalid=False): self.invalid = invalid
    def execute(self, solution, case_id, input_text):
        if solution.id == "validator": return Result(solution.id, "PASS", case_id)
        wrong = solution.id.startswith("wa") or (
            solution.id.startswith("recovery-") and not self.invalid)
        return Result(solution.id, "PASS", case_id, "2.000\n" if wrong else "1.000\n")

def pipeline(generator):
    return Pipeline(generator, FakeCases(), RecoveryJudge(generator.invalid),
        checker_from_profile({"kind": "TOKEN"}), mutant_replacement_rounds=4,
        mutant_witness_repair_rounds=0, min_iterations=1, min_total_cases=1, top_up_rounds=0)

@pytest.mark.parametrize("success_round", [5, 8])
def test_recovers_with_existing_mutants_and_stops_immediately(success_round):
    generator = RecoverySolutions(success_round)
    with TemporaryDirectory(dir=ROOT / "tmp") as d:
        report = pipeline(generator).run("fixture", "statement", Path(d), iterations=1)
    summary = report["mutant_certification"]
    assert generator.rounds == list(range(1, success_round + 1))
    assert summary["validated_solution_ids"] == ["wa1", "wa2", f"recovery-{success_round}"]
    assert summary["recovery"]["additional_rounds_used"] == success_round - 4
    assert summary["stage_status"] == "ready_minimum"
    assert len(report["cases"]) >= 1

@pytest.mark.parametrize("invalid", [False, True])
def test_exhaustion_is_bounded_and_never_admits_unverified_candidates(invalid):
    generator = RecoverySolutions(invalid=invalid)
    with TemporaryDirectory(dir=ROOT / "tmp") as d:
        with pytest.raises(RuntimeError, match="exhausted 8 replacement rounds"):
            pipeline(generator).run("fixture", "statement", Path(d), iterations=1)
        summary = json.loads((Path(d)/"generated/mutant-certification.json").read_text())
    assert generator.rounds == list(range(1,9))
    assert summary["validated_solution_ids"] == ["wa1", "wa2"]
    assert summary["recovery"]["additional_rounds_used"] == 4
    assert summary["stage_status"] == "failed_minimum_verified_pool"


def test_transport_failure_consumes_one_attempt_and_next_round_can_recover():
    generator = RecoverySolutions(success_round=6, transport_rounds=(5,))
    with TemporaryDirectory(dir=ROOT / "tmp") as d:
        report = pipeline(generator).run("fixture", "statement", Path(d), iterations=1)
    summary = report["mutant_certification"]
    assert generator.rounds == list(range(1,7))
    assert summary["recovery"]["generation_failures"][0]["round"] == 5
    assert summary["recovery"]["generation_failures"][0]["error_type"] == "LLMTransportError"


def test_programming_errors_are_not_retried_as_generation_failures():
    class Broken(RecoverySolutions):
        def regenerate_wrong(self, *args): raise TypeError("programming error")
    with TemporaryDirectory(dir=ROOT / "tmp") as d:
        with pytest.raises(TypeError, match="programming error"):
            pipeline(Broken()).run("fixture", "statement", Path(d), iterations=1)
