"""Evaluate hidden mutants only after the suite is locked."""
from dataclasses import dataclass
from ..domain import Result
from ..suite import suite_lock
from .metrics import metrics

@dataclass(frozen=True)
class HoldoutResult:
    verdicts: dict[str, Result]
    metrics: dict | None

class HoldoutEvaluator:
    def __init__(self, execution):
        self.execution = execution

    def evaluate(self, pool, cases, development_verdicts, locked_suite, output) -> HoldoutResult:
        if suite_lock(cases) != locked_suite:
            raise ValueError("Holdout evaluation requires the locked suite")
        if not pool.holdout_wrong:
            return HoldoutResult({}, None)
        previous_log = self.execution._execution_log
        self.execution._execution_log = output / "executions-holdout.jsonl"
        try:
            self.execution._log(f"Đánh giá kín {len(pool.holdout_wrong)} mutant trên suite đã khóa")
            verdicts = self.execution._judge_pool(
                pool.holdout_wrong, cases, pool.compiles, "LLM holdout")
        finally:
            self.execution._execution_log = previous_log
        combined = {solution.id: development_verdicts[solution.id] for solution in pool.candidate_ac}
        combined.update(verdicts)
        return HoldoutResult(verdicts, metrics([*pool.candidate_ac, *pool.holdout_wrong],
                                             combined, "candidate_ac", "candidate_wa"))
