"""Route typed LLM tasks to task-specialized providers."""
from __future__ import annotations

from collections.abc import Mapping

from .llm_contract import LLMClient, LLMRequest, TaskType


FINETUNED_TESTGEN_TASKS = frozenset({
    TaskType.GENERATE_CASES,
    TaskType.REPAIR_WITNESSES,
})


class TaskRoutingLLMClient:
    """Delegate requests by ``TaskType`` and use a default for every other task."""

    def __init__(
        self,
        default_client: LLMClient,
        task_clients: Mapping[TaskType, LLMClient],
        *,
        default_name: str = "default",
        task_names: Mapping[TaskType, str] | None = None,
        progress=None,
    ) -> None:
        self.default_client = default_client
        self.task_clients = dict(task_clients)
        self.default_name = default_name
        self.task_names = dict(task_names or {})
        self.progress = progress

    def ask(self, request: LLMRequest) -> dict:
        client = self.task_clients.get(request.task_type, self.default_client)
        if self.progress:
            provider = self.task_names.get(request.task_type, self.default_name)
            self.progress.log(
                f"LLM route: task={request.task_type.value}; provider={provider}"
            )
        return client.ask(request)
