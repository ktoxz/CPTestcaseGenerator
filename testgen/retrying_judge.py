"""Retry transient judge infrastructure failures without retrying code verdicts."""

from __future__ import annotations

import time
from typing import Callable, TypeVar

from .domain import Judge, Result, Solution
from .progress import ConsoleProgress


class InfrastructureError(RuntimeError):
    """The judge could not produce a code verdict after bounded retries."""


T = TypeVar("T")


def _is_non_retryable_infrastructure_error(reason: str) -> bool:
    """Return true for deterministic configuration errors that waiting cannot fix."""
    return reason.startswith("No runtime for language/dialect")


def retry_setup(operation: Callable[[], T], *, label: str, max_attempts: int,
                delay_seconds: float, progress: ConsoleProgress | None = None) -> T:
    """Retry remote engine startup/probe failures before pipeline work begins."""
    if max_attempts < 1 or delay_seconds < 0:
        raise ValueError("Retry attempts must be positive and delay non-negative")
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except RuntimeError as exc:
            if attempt == max_attempts:
                raise InfrastructureError(
                    f"{label}: failed after {attempt} attempts: {exc}") from exc
            delay = min(delay_seconds * 2 ** (attempt - 1), 10.0)
            if progress:
                progress.log(f"INFRA {label}, lần {attempt}/{max_attempts}: {exc}; "
                             f"thử lại sau {delay:g}s")
            time.sleep(delay)
    raise AssertionError("unreachable")


class RetryingJudge(Judge):
    def __init__(self, judge: Judge, *, max_attempts: int = 3,
                 delay_seconds: float = 2.0, progress: ConsoleProgress | None = None):
        if max_attempts < 1 or delay_seconds < 0:
            raise ValueError("Retry attempts must be positive and delay non-negative")
        self.judge = judge
        self.max_attempts = max_attempts
        self.delay_seconds = delay_seconds
        self.progress = progress

    def _attempt(self, label: str, operation: Callable[[], Result]) -> Result:
        for attempt in range(1, self.max_attempts + 1):
            result = operation()
            if result.verdict != "INFRA":
                return result
            reason = result.stderr.strip() or "unknown infrastructure error"
            if _is_non_retryable_infrastructure_error(reason):
                raise InfrastructureError(
                    f"{label}: non-retryable infrastructure error: {reason}"
                )
            if attempt == self.max_attempts:
                raise InfrastructureError(
                    f"{label}: INFRA after {attempt} attempts: {reason}")
            delay = min(self.delay_seconds * 2 ** (attempt - 1), 10.0)
            if self.progress:
                self.progress.log(
                    f"INFRA {label}, lần {attempt}/{self.max_attempts}: {reason}; "
                    f"thử lại sau {delay:g}s")
            time.sleep(delay)
        raise AssertionError("unreachable")

    def compile(self, solution: Solution) -> Result:
        return self._attempt(f"compile {solution.id}", lambda: self.judge.compile(solution))

    def execute(self, solution: Solution, case_id: str, input_text: str) -> Result:
        return self._attempt(
            f"run {solution.id}/{case_id}",
            lambda: self.judge.execute(solution, case_id, input_text))

    def execute_many(self, solution: Solution, cases: list[tuple[str, str]]) -> list[Result]:
        results = self.judge.execute_many(solution, cases)
        if len(results) != len(cases):
            raise InfrastructureError(f"run {solution.id}: incomplete batch response")
        return [self.execute(solution, case_id, input_text) if result.verdict == "INFRA" else result
                for (case_id, input_text), result in zip(cases, results)]
