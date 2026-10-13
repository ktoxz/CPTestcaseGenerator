"""Behavior contracts for independently callable refactored stages."""
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest
from testgen.checker import checker_from_profile
from testgen.domain import Case, Result, Solution
from testgen.evaluation.execution import ExecutionService
from testgen.certification.references import ReferenceCertification
from testgen.certification.cases import CaseCertification, CaseCertificationState
from testgen.fallback import FallbackLLMClient
from testgen.llm_contract import (LLMRequest, TaskType, FailurePolicy, LLMTransportError,
                                 LLMContractError)
from testgen.infrastructure.file_run_store import FileRunStore
from testgen.infrastructure.llm.ollama import OllamaClient
from testgen.persistence import RunCheckpoint
from testgen.suite import suite_lock
from testgen.application.resume_run import ResumeRun
from testgen.generation.solutions import SolutionGenerationService

ROOT = Path(__file__).resolve().parents[1]

class TimeoutClient:
    def ask(self, request):
        raise LLMTransportError("offline")

@pytest.mark.parametrize("label", ["renamed", "sinh code AC/WA", "xây test model"])
def test_fallback_uses_task_and_policy_not_label(label):
    client = FallbackLLMClient([("offline", TimeoutClient())])
    assert client.ask(LLMRequest(TaskType.REPAIR_CASES, "p", failure_policy=FailurePolicy.OPTIONAL,
                                  label=label)) == {"repairs": []}
    with pytest.raises(LLMTransportError, match="required task"):
        client.ask(LLMRequest(TaskType.REPAIR_CASES, "p", label=label))

@pytest.mark.parametrize("error", [TypeError("bug"), ValueError("bug"), KeyError("bug"),
                                  LLMContractError("bad contract")])
def test_programming_errors_are_not_degraded(error):
    class Broken:
        def ask(self, request):
            raise error
    with pytest.raises(type(error)):
        FallbackLLMClient([("broken", Broken()), ("offline", TimeoutClient())]).ask(
            LLMRequest(TaskType.REPAIR_CASES, "p", failure_policy=FailurePolicy.OPTIONAL))

@pytest.mark.parametrize("label", ["renamed", "sinh validator"])
def test_transport_shape_depends_on_task_not_label(label):
    class Response(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *args): self.close()
    envelope = {"message": {"content": '[{"input":"1\n","family":"boundary"}]'}}
    with patch("urllib.request.urlopen", return_value=Response(json.dumps(envelope).encode())):
        result = OllamaClient("http://typed-test", "model").ask(
            LLMRequest(TaskType.GENERATE_CASES, "p", label=label))
    assert result["cases"][0]["input"] == "1\n"


def checkpoint():
    cases = (Case("p_i0_001", "1\n", "2\n", "boundary", 0, ("min",)),)
    report = {"problem_id": "p", "test_suite_lock": suite_lock(list(cases)),
              "cases": [dict(c.__dict__) for c in cases]}
    return RunCheckpoint(1, "suite_locked", "p", cases, report)


def test_atomic_write_keeps_previous_commit_when_replace_fails():
    with TemporaryDirectory(dir=ROOT / "tmp") as directory:
        path = Path(directory) / "checkpoint.json"
        store = FileRunStore()
        store.checkpoint(path, checkpoint())
        before = path.read_bytes()
        with patch("testgen.infrastructure.file_run_store.os.replace", side_effect=OSError("disk")):
            with pytest.raises(OSError):
                store.write_json(path, {"partial": True})
        assert path.read_bytes() == before
        assert list(Path(directory).glob("*.tmp")) == []
        restored = store.restore(path)
        assert restored.cases == checkpoint().cases
        assert restored.stage == "suite_locked"

@pytest.mark.parametrize("field,value", [("schema_version", 999), ("stage", "refining"),
                                          ("problem_id", "other")])
def test_checkpoint_rejects_incompatible_metadata(field, value):
    with TemporaryDirectory(dir=ROOT / "tmp") as directory:
        path = Path(directory) / "checkpoint.json"
        store = FileRunStore(); store.checkpoint(path, checkpoint())
        payload = store.read_json(path); payload[field] = value; store.write_json(path, payload)
        with pytest.raises(ValueError): store.restore(path)


def test_resume_restores_case_metadata_and_rejects_changed_exports():
    class External:
        calls = 0
        def evaluate(self, report, problem_id, output, cases, limit):
            self.calls += 1
            assert cases == list(checkpoint().cases)
            report["oracle_metrics"] = {"checked": True}
    class Execution: pass
    with TemporaryDirectory(dir=ROOT / "tmp") as directory:
        output = Path(directory); store = FileRunStore(); saved = checkpoint()
        store.checkpoint(output / "checkpoint.json", saved)
        for case in saved.cases:
            store.write_text(output / "tests" / (case.id + ".in"), case.input)
            store.write_text(output / "tests" / (case.id + ".out"), case.expected)
        external = External(); resume = ResumeRun(store, Execution(), external)
        assert resume.run("p", output, 1)["oracle_metrics"] == {"checked": True}
        store.write_text(output / "tests" / "p_i0_001.in", "tampered")
        with pytest.raises(ValueError, match="committed checkpoint"):
            resume.run("p", output, 1)
        assert external.calls == 1


def test_certification_batch_preserves_identity_and_requests_repair_without_llm():
    class Judge:
        def execute_many(self, solution, jobs):
            return [Result(solution.id, "RE" if solution.id == "validator" and text == "bad\n"
                           else "PASS", case_id, "7\n", "invalid" if text == "bad\n" else "")
                    for case_id, text in jobs]
    checker = checker_from_profile({"kind": "TOKEN"})
    execution = ExecutionService(Judge(), checker)
    refs = [Solution(name, "candidate_ac", "Python", Path(name)) for name in ("a", "b")]
    state = CaseCertificationState([], set(), {}, [])
    certifier = CaseCertification(execution, ReferenceCertification(execution, checker), checker,
        Solution("validator", "validator", "Python", Path("v")), refs, {}, "p", 0, state)
    result = certifier.validate_batch("initial", certifier.index_proposals([
        {"input": "good", "family": "boundary"}, {"input": "bad", "family": "boundary"}], "initial"), 0)
    assert result.accepted[0].expected == "7\n"
    assert result.repair_requests[0]["proposal_index"] == 2
    assert result.repair_requests[0]["reason"] == "validator rejected"
    duplicate = certifier.validate_batch("topup", certifier.index_proposals([{"input": "good"}], "topup"), 0)
    assert duplicate.rejected[0]["reason"] == "duplicate input"
    assert len(state.cases) == 1


def test_standalone_generator_does_not_read_neighbor_model():
    class StopAnalysis(Exception): pass
    class Client:
        def ask(self, request):
            assert request.task_type == TaskType.ANALYZE
            assert "UNTRUSTED_NEIGHBOR" not in request.prompt
            raise StopAnalysis()
    with TemporaryDirectory(dir=ROOT / "tmp") as directory:
        root = Path(directory)
        (root / "test-model.json").write_text('{"marker":"UNTRUSTED_NEIGHBOR"}')
        with pytest.raises(StopAnalysis):
            SolutionGenerationService(Client()).generate("statement", root / "generated")


def test_legacy_resume_without_checkpoint_preserves_supported_output():
    class External:
        def evaluate(self, report, problem_id, output, cases, limit):
            assert report["test_suite_lock"] == suite_lock(cases)
            report["oracle_metrics"] = {"checked": True}
    class Execution:
        def _latency_report(self): return {}
        def _log(self, message): pass
    with TemporaryDirectory(dir=ROOT / "tmp") as directory:
        output = Path(directory); store = FileRunStore()
        store.write_json(output / "iteration-0.json", {
            "problem_id": "p", "iteration": 0, "cases": 1,
            "llm_metrics": {}, "quarantined": 0, "verdicts": {}})
        store.write_text(output / "tests" / "p_001.in", "1\n")
        store.write_text(output / "tests" / "p_001.out", "2\n")
        result = ResumeRun(store, Execution(), External()).run("p", output, 1)
        assert result["oracle_metrics"] == {"checked": True}
        assert store.read_json(output / "report.json") == result


def test_invalid_request_contract_is_rejected_before_transport():
    with pytest.raises(LLMContractError):
        LLMRequest("guess-from-label", "p")
    with pytest.raises(LLMContractError):
        LLMRequest(TaskType.GENERIC, "p", response_model=dict)
