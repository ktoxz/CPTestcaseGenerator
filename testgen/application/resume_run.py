"""Resume external evaluation from committed artifacts without generation."""
import json
from pathlib import Path
from ..domain import Case
from ..suite import suite_lock, case_record

class ResumeRun:
    def __init__(self, store, execution, external):
        self.store, self.execution, self.external = store, execution, external

    def run(self, problem_id: str, output: Path, oracle_limit: int) -> dict:
        """Continue an interrupted run from certified tests without calling the LLM."""
        checkpoint_path = output / "checkpoint.json"
        if checkpoint_path.is_file():
            checkpoint = self.store.restore(checkpoint_path)
            if checkpoint.problem_id != problem_id:
                raise ValueError("Resume output belongs to another problem")
            cases = list(checkpoint.cases)
            result = dict(checkpoint.report)
            # Detect changed or missing exported files; do not silently judge a different suite.
            for case in cases:
                for suffix, expected in (("in", case.input), ("out", case.expected)):
                    path = output / "tests" / f"{case.id}.{suffix}"
                    if not path.is_file() or self.store.read_text(path) != expected:
                        raise ValueError("Certified test files do not match committed checkpoint")
            self.execution._execution_log = output / "executions-llm.jsonl"
            self.external.evaluate(result, problem_id, output, cases, oracle_limit)
            self.store.write_json(output / "report.json", result)
            return result
        snapshots = sorted(output.glob("iteration-*.json"))
        if not snapshots:
            raise ValueError(f"No completed iteration in {output}")
        snapshot = self.store.read_json(snapshots[-1])
        if snapshot["problem_id"] != problem_id:
            raise ValueError("Resume output belongs to another problem")
        cases = []
        for input_path in sorted((output / "tests").glob("*.in")):
            output_path = input_path.with_suffix(".out")
            if not output_path.is_file():
                raise ValueError(f"Missing expected output for {input_path.name}")
            cases.append(Case(input_path.stem, self.store.read_text(input_path, encoding="utf-8"),
                              self.store.read_text(output_path, encoding="utf-8"), "certified", 0))
        if len(cases) != snapshot["cases"]:
            raise ValueError("Certified test count does not match iteration snapshot")
        self.execution._execution_log = output / "executions-llm.jsonl"
        locked_suite = suite_lock(cases)
        report_path = output / "report.json"
        if report_path.is_file():
            result = self.store.read_json(report_path)
            existing_lock = result.get("test_suite_lock", {}).get("sha256")
            if existing_lock and existing_lock != locked_suite["sha256"]:
                raise ValueError("Existing report does not match certified test files")
            result["test_suite_lock"] = locked_suite
        else:
            result = {"problem_id": problem_id,
                      "iterations_used": snapshot["iteration"] + 1,
                      "llm_metrics": snapshot["llm_metrics"],
                      "cases": [case_record(case) for case in cases],
                      "quarantined_count": snapshot["quarantined"],
                      "llm_verdicts": snapshot["verdicts"],
                      "test_suite_lock": locked_suite,
                      "experiment_protocol": {
                          "test_generation_pool": "LLM candidates only",
                          "external_evaluation_pool": "CodeNet oracle",
                          "oracle_used_for_generation_or_refinement": False,
                      }}
        result["latency"] = {
            "log": "latency.jsonl",
            "summary": self.execution._latency_report(),
        }
        self.store.write_json(output / "test-suite.lock.json", locked_suite)
        self.store.write_json(report_path, result)
        self.external.evaluate(result, problem_id, output, cases, oracle_limit)
        self.store.write_json(report_path, result)
        self.execution._log(f"Đã ghi báo cáo: {output / 'report.json'}")
        return result

