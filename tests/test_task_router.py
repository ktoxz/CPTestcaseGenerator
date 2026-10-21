import unittest

from testgen.llm_contract import LLMRequest, TaskType
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


if __name__ == "__main__":
    unittest.main()
