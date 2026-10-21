import unittest

from testgen.llm_contract import (
    FailurePolicy, LLMRequest, LLMTransportError, TaskType,
)
from testgen.task_router import FINETUNED_TESTGEN_TASKS, TaskRoutingLLMClient


class RecordingClient:
    def __init__(self, name: str) -> None:
        self.name = name
        self.requests: list[LLMRequest] = []

    def ask(self, request: LLMRequest) -> dict:
        self.requests.append(request)
        return {"provider": self.name, "task": request.task_type.value}


class RecordingProgress:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def log(self, message: str) -> None:
        self.messages.append(message)


class FailingClient:
    def __init__(self, error: BaseException) -> None:
        self.error = error
        self.requests: list[LLMRequest] = []

    def ask(self, request: LLMRequest) -> dict:
        self.requests.append(request)
        raise self.error


class TaskRoutingLLMClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ollama = RecordingClient("ollama")
        self.finetuned = RecordingClient("gemma4-testgen")
        self.progress = RecordingProgress()
        self.router = TaskRoutingLLMClient(
            self.ollama,
            {task: self.finetuned for task in FINETUNED_TESTGEN_TASKS},
            default_name="Ollama/general",
            task_names={
                task: "llama-server/gemma4-testgen"
                for task in FINETUNED_TESTGEN_TASKS
            },
            progress=self.progress,
        )

    def test_routes_only_finetuned_tasks_to_specialized_model(self) -> None:
        for task in TaskType:
            with self.subTest(task=task):
                result = self.router.ask(LLMRequest(task, "prompt"))
                expected = (
                    "gemma4-testgen"
                    if task in FINETUNED_TESTGEN_TASKS
                    else "ollama"
                )
                self.assertEqual(result["provider"], expected)

        self.assertEqual(
            {request.task_type for request in self.finetuned.requests},
            FINETUNED_TESTGEN_TASKS,
        )
        self.assertNotIn(
            TaskType.BUILD_TEST_MODEL,
            {request.task_type for request in self.finetuned.requests},
        )
        self.assertNotIn(
            TaskType.GENERATE_SOLUTIONS,
            {request.task_type for request in self.finetuned.requests},
        )

    def test_logs_the_selected_provider(self) -> None:
        self.router.ask(LLMRequest(TaskType.GENERATE_CASES, "prompt"))
        self.router.ask(LLMRequest(TaskType.GENERATE_VALIDATOR, "prompt"))

        self.assertEqual(
            self.progress.messages,
            [
                "LLM route: task=generate_cases; provider=llama-server/gemma4-testgen",
                "LLM route: task=generate_validator; provider=Ollama/general",
            ],
        )

    def test_specialized_transport_failure_falls_back_to_ollama(self) -> None:
        failing = FailingClient(LLMTransportError("llama is down"))
        router = TaskRoutingLLMClient(
            self.ollama,
            {TaskType.GENERATE_CASES: failing},
            default_name="Ollama/general",
            task_names={TaskType.GENERATE_CASES: "llama/testgen"},
            progress=self.progress,
        )

        result = router.ask(LLMRequest(TaskType.GENERATE_CASES, "prompt"))

        self.assertEqual(result["provider"], "ollama")
        self.assertEqual(len(failing.requests), 1)
        self.assertEqual(len(self.ollama.requests), 1)
        self.assertTrue(any("fallback=Ollama/general" in row
                            for row in self.progress.messages))

    def test_optional_task_returns_neutral_when_both_routes_fail(self) -> None:
        router = TaskRoutingLLMClient(
            FailingClient(LLMTransportError("ollama down")),
            {TaskType.GENERATE_CASES:
             FailingClient(LLMTransportError("llama down"))},
        )

        result = router.ask(LLMRequest(
            TaskType.GENERATE_CASES, "prompt",
            failure_policy=FailurePolicy.OPTIONAL,
        ))

        self.assertEqual(result["cases"], [])
        self.assertEqual(result["requested_count"], 0)

    def test_required_task_raises_when_both_routes_fail(self) -> None:
        router = TaskRoutingLLMClient(
            FailingClient(LLMTransportError("ollama down")),
            {TaskType.GENERATE_CASES:
             FailingClient(LLMTransportError("llama down"))},
        )

        with self.assertRaisesRegex(LLMTransportError, "All routed"):
            router.ask(LLMRequest(TaskType.GENERATE_CASES, "prompt"))

    def test_programming_error_is_not_swallowed(self) -> None:
        router = TaskRoutingLLMClient(
            self.ollama,
            {TaskType.GENERATE_CASES: FailingClient(AssertionError("bug"))},
        )

        with self.assertRaisesRegex(AssertionError, "bug"):
            router.ask(LLMRequest(TaskType.GENERATE_CASES, "prompt"))


if __name__ == "__main__":
    unittest.main()
