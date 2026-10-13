"""External evaluation requires a locked suite and never invokes generation."""
from pathlib import Path
from ..domain import Case
from ..suite import suite_lock
from .metrics import metrics

class ExternalEvaluator:
    def __init__(self, oracle, execution):
        self.oracle, self.execution = oracle, execution

    def evaluate(self, result: dict, problem_id: str, output: Path,
                       cases: list[Case], oracle_limit: int) -> None:
        if self.oracle is None:
            raise ValueError("--oracle requires an oracle source")
        locked = result.get("test_suite_lock", {}).get("sha256")
        if not locked or suite_lock(cases)["sha256"] != locked:
            raise RuntimeError("Refusing oracle evaluation: LLM test suite is not locked")
        previous_log = self.execution._execution_log
        oracle_dir = output / "oracle"
        oracle_dir.mkdir(parents=True, exist_ok=True)
        self.execution._execution_log = oracle_dir / "executions.jsonl"
        try:
            with self.execution._waiting(
                "Tải pool AC/WA CodeNet", component="oracle.fetch.total",
                problem_id=problem_id, per_label=oracle_limit,
            ):
                pool = self.oracle.fetch(problem_id, oracle_dir, oracle_limit)
            self.execution._log(f"Đã tải {len(pool)} source CodeNet")
            oracle_compiles = self.execution._compile_pool(pool, "Biên dịch CodeNet")
            self.execution._log(f"Chấm {len(pool)} code CodeNet trên {len(cases)} testcase")
            oracle_verdicts = self.execution._judge_pool(pool, cases, oracle_compiles, "CodeNet")
            result["oracle_metrics"] = metrics(pool, oracle_verdicts,
                                               "CodeNet Accepted", "CodeNet Wrong Answer")
            result["oracle_verdicts"] = {key: value.__dict__ for key, value in oracle_verdicts.items()}
            result["metric_gap"] = {
                key: (result["oracle_metrics"][key] - result["llm_metrics"][key])
                if result["oracle_metrics"][key] is not None and result["llm_metrics"][key] is not None else None
                for key in ("tpr_label_based", "tnr_label_based")
            }
            if suite_lock(cases)["sha256"] != locked:
                raise RuntimeError("Oracle evaluation mutated the locked LLM test suite")
            result["latency"] = {
                "log": "latency.jsonl",
                "summary": self.execution._latency_report(),
            }
        finally:
            self.execution._execution_log = previous_log

