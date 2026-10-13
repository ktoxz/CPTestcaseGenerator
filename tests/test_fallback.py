import unittest

from testgen.llm_contract import TaskType, FailurePolicy, LLMTransportError, LLMResponseError
from testgen.coverage import TestModelResponse
from testgen.fallback import FallbackLLMClient


class FakeClient:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = 0
        self.response_model = None

    def ask_json(self, prompt, label="LLM", response_model=None):
        self.calls += 1
        self.response_model = response_model
        if self.error is not None:
            raise self.error
        return self.result


class FallbackLLMClientTests(unittest.TestCase):
    def test_forwards_pydantic_response_model(self):
        backend = FakeClient(result={"ok": True})
        client = FallbackLLMClient([("ollama", backend)])

        self.assertEqual(
            client.ask_json("prompt", response_model=TestModelResponse),
            {"ok": True},
        )
        self.assertIs(backend.response_model, TestModelResponse)

    def test_uses_next_backend_after_timeout(self):
        gemma = FakeClient(error=TimeoutError("50 seconds"))
        nemotron = FakeClient(result={"cases": []})
        claude = FakeClient(result={"cases": [{"input": "unused"}]})
        client = FallbackLLMClient([
            ("gemma", gemma), ("nemotron", nemotron), ("claude", claude)
        ])
        self.assertEqual(
            client.ask_json("prompt", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES, failure_policy=FailurePolicy.OPTIONAL),
            {"cases": []},
        )
        self.assertEqual((gemma.calls, nemotron.calls, claude.calls), (1, 1, 0))

    def test_skips_optional_task_when_every_backend_fails(self):
        client = FallbackLLMClient([
            ("gemma", FakeClient(error=TimeoutError())),
            ("nemotron", FakeClient(error=LLMTransportError())),
            ("claude", FakeClient(error=LLMResponseError())),
        ])
        self.assertEqual(
            client.ask_json("prompt", label="sửa batch testcase lần 1", task_type=TaskType.REPAIR_CASES, failure_policy=FailurePolicy.OPTIONAL),
            {"repairs": []},
        )

    def test_witness_repair_does_not_chain_three_timeouts(self):
        gemma = FakeClient(error=TimeoutError("50 seconds"))
        nemotron = FakeClient(result={"witnesses": [{"unused": True}]})
        claude = FakeClient(result={"witnesses": [{"unused": True}]})
        client = FallbackLLMClient([
            ("gemma", gemma), ("nemotron", nemotron), ("claude", claude)
        ])
        self.assertEqual(
            client.ask_json("prompt", label="sửa witness mutant lần 1 batch 1", task_type=TaskType.REPAIR_WITNESSES, failure_policy=FailurePolicy.OPTIONAL),
            {"witnesses": []},
        )
        self.assertEqual((gemma.calls, nemotron.calls, claude.calls), (1, 0, 0))

    def test_required_generation_fails_after_every_backend(self):
        client = FallbackLLMClient([
            ("gemma", FakeClient(error=TimeoutError())),
            ("nemotron", FakeClient(error=LLMTransportError())),
            ("claude", FakeClient(error=LLMResponseError())),
        ])
        with self.assertRaisesRegex(RuntimeError, "required task"):
            client.ask_json("prompt", label="sinh code AC/WA vòng 1", task_type=TaskType.GENERATE_SOLUTIONS, failure_policy=FailurePolicy.REQUIRED)


if __name__ == "__main__":
    unittest.main()
