"""Typed provider-neutral requests and classified LLM failures."""
from dataclasses import dataclass
from enum import Enum
from typing import Protocol
from pydantic import BaseModel

class TaskType(str, Enum):
    GENERIC = "generic"
    ANALYZE = "analyze"
    BUILD_TEST_MODEL = "build_test_model"
    GENERATE_SOLUTIONS = "generate_solutions"
    REPLACE_REFERENCE = "replace_reference"
    GENERATE_VALIDATOR = "generate_validator"
    GENERATE_CHECKER = "generate_checker"
    GENERATE_MUTANTS = "generate_mutants"
    GENERATE_WITNESSES = "generate_witnesses"
    REPAIR_WITNESSES = "repair_witnesses"
    GENERATE_CASES = "generate_cases"
    REPAIR_CASE = "repair_case"
    REPAIR_CASES = "repair_cases"
    AUDIT = "audit"
    AUDIT_BATCH = "audit_batch"

class FailurePolicy(str, Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"

class LLMTransportError(RuntimeError):
    """A provider could not complete a transport request."""

class LLMResponseError(ValueError):
    """The provider exhausted response parsing/validation attempts."""

class LLMContractError(TypeError):
    """An invalid caller or adapter contract; never silently degraded."""

@dataclass(frozen=True)
class LLMRequest:
    task_type: TaskType
    prompt: str
    response_model: type[BaseModel] | None = None
    failure_policy: FailurePolicy = FailurePolicy.REQUIRED
    label: str = "LLM"

    def __post_init__(self):
        if not isinstance(self.task_type, TaskType) or not isinstance(self.failure_policy, FailurePolicy):
            raise LLMContractError("task_type and failure_policy must be enum values")
        if not isinstance(self.prompt, str) or not isinstance(self.label, str):
            raise LLMContractError("prompt and label must be strings")
        if self.response_model is not None and (
            not isinstance(self.response_model, type) or not issubclass(self.response_model, BaseModel)
        ):
            raise LLMContractError("response_model must be a Pydantic model class")

class LLMClient(Protocol):
    def ask(self, request: LLMRequest) -> dict: ...

SHAPES = {
    TaskType.BUILD_TEST_MODEL: dict(input_grammar=str, constraints=list, variables=list,
        relations=list, output_partitions=list, sequences=list, fault_model=list,
        warnings=list, coverage_obligations=list),
    TaskType.GENERATE_SOLUTIONS: dict(correct=list, wrong=list, validator_python=str),
    TaskType.REPLACE_REFERENCE: dict(correct=list),
    TaskType.GENERATE_VALIDATOR: dict(validator_python=str),
    TaskType.GENERATE_CHECKER: dict(
        checker_python=str, requires_expected_output=bool, reasoning=str,
    ),
    TaskType.GENERATE_MUTANTS: dict(wrong=list),
    TaskType.GENERATE_WITNESSES: dict(witnesses=list),
    TaskType.REPAIR_WITNESSES: dict(witnesses=list),
    TaskType.REPAIR_CASES: dict(repairs=list),
    TaskType.GENERATE_CASES: dict(cases=list),
    # A repaired case may carry either a short literal input or input_parts;
    # CaseGenerationService enforces that exclusive union after transport.
    TaskType.REPAIR_CASE: dict(family=str),
    TaskType.AUDIT_BATCH: dict(audits=list),
    TaskType.AUDIT: dict(classification=str),
}

def ask_json(client, task_type, prompt, label="LLM", response_model=None,
             failure_policy=None):
    """Bridge existing third-party/fake ask_json clients without inferring task from labels."""
    if failure_policy is None:
        failure_policy = (FailurePolicy.REQUIRED if task_type in {
            TaskType.GENERIC, TaskType.GENERATE_SOLUTIONS, TaskType.REPLACE_REFERENCE,
            TaskType.GENERATE_VALIDATOR} else FailurePolicy.OPTIONAL)
    request = LLMRequest(task_type, prompt, response_model, failure_policy, label)
    if callable(getattr(type(client), "ask", None)):
        return client.ask(request)
    kwargs = {"label": label}
    if response_model is not None:
        kwargs["response_model"] = response_model
    return client.ask_json(prompt, **kwargs)
