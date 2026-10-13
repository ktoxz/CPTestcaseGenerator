"""Ordered provider fallback for explicitly optional typed tasks."""
from .llm_contract import (
    LLMRequest, TaskType, FailurePolicy, LLMTransportError, LLMResponseError,
    LLMContractError, ask_json,
)
from .throttle import EndpointBusyError


def neutral_result(task: TaskType) -> dict:
    if task == TaskType.BUILD_TEST_MODEL:
        return {"input_grammar": "", "constraints": [], "variables": [], "relations": [],
                "output_partitions": [], "sequences": [], "fault_model": [],
                "warnings": ["all configured LLM backends were unavailable"],
                "coverage_obligations": []}
    keys = {TaskType.GENERATE_MUTANTS: "wrong", TaskType.REPAIR_WITNESSES: "witnesses",
            TaskType.REPAIR_CASES: "repairs", TaskType.AUDIT_BATCH: "audits"}
    if task in keys:
        return {keys[task]: []}
    if task == TaskType.GENERATE_CASES:
        return {"requested_count": 0, "rationale": "LLM unavailable", "cases": []}
    if task == TaskType.AUDIT:
        return {"classification": "insufficient_evidence", "revised_bug_hypothesis": "",
                "reasoning": "all configured LLM backends were unavailable", "confidence": 0.0,
                "failed_hypotheses": [], "counterexample": None}
    if task in {TaskType.REPAIR_CASE, TaskType.GENERATE_WITNESSES, TaskType.ANALYZE}:
        return {}
    raise LLMContractError(f"Task {task} has no optional degraded result")


class FallbackLLMClient:
    def __init__(self, clients, *, progress=None):
        if not clients:
            raise ValueError("at least one LLM client is required")
        self.clients, self.progress = clients, progress

    def ask_json(self, prompt, label="LLM", response_model=None, *,
                 task_type=TaskType.GENERIC, failure_policy=FailurePolicy.REQUIRED):
        return self.ask(LLMRequest(task_type, prompt, response_model, failure_policy, label))

    def ask(self, request: LLMRequest) -> dict:
        failures = []
        clients = self.clients[:1] if request.task_type == TaskType.REPAIR_WITNESSES else self.clients
        for name, client in clients:
            try:
                return ask_json(client, request.task_type, request.prompt, request.label,
                                request.response_model, request.failure_policy)
            except (LLMTransportError, LLMResponseError, EndpointBusyError, TimeoutError, OSError) as error:
                failures.append(f"{name}: {type(error).__name__}: {error}")
                if self.progress:
                    self.progress.log(f"LLM {name} lỗi ở {request.label}: {type(error).__name__}")
        if request.failure_policy == FailurePolicy.OPTIONAL:
            if self.progress:
                self.progress.log(f"Bỏ tác vụ LLM tùy chọn {request.label}: các backend đều lỗi")
            return neutral_result(request.task_type)
        raise LLMTransportError(
            f"All LLM backends failed for required task {request.label!r}: " + " | ".join(failures))
