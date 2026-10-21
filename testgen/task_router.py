"""Route typed LLM tasks to task-specialized providers."""
from __future__ import annotations

from collections.abc import Mapping

from .fallback import neutral_result
from .llm_contract import (
    FailurePolicy,
    LLMClient,
    LLMRequest,
    LLMResponseError,
    LLMTransportError,
    TaskType,
)
from .throttle import EndpointBusyError


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
        provider = self.task_names.get(request.task_type, self.default_name)
        if self.progress:
            self.progress.log(
                f"LLM route: task={request.task_type.value}; provider={provider}"
            )
        try:
            return client.ask(request)
        except (LLMTransportError, LLMResponseError, EndpointBusyError,
                TimeoutError, OSError) as error:
            if client is not self.default_client:
                if self.progress:
                    self.progress.log(
                        f"LLM {provider} lỗi ở {request.label}: "
                        f"{type(error).__name__}; fallback={self.default_name}"
                    )
                try:
                    return self.default_client.ask(request)
                except (LLMTransportError, LLMResponseError, EndpointBusyError,
                        TimeoutError, OSError) as fallback_error:
                    error = fallback_error
            if request.failure_policy == FailurePolicy.OPTIONAL:
                if self.progress:
                    self.progress.log(
                        f"Degraded LLM task {request.label}: mọi provider đều lỗi"
                    )
                return neutral_result(request.task_type)
            raise LLMTransportError(
                f"All routed LLM providers failed for required task "
                f"{request.label!r}: {type(error).__name__}: {error}"
            ) from error
