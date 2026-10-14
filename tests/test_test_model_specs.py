import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from testgen.application.run_pipeline import RunPipeline
from testgen.checker import checker_from_profile
from testgen.coverage import TestModelResponse, normalize_test_model
from testgen.docker_judge import DockerJudge
from testgen.fallback import neutral_result
from testgen.llm_contract import TaskType
from testgen.retrying_judge import RetryingJudge


class TestModelSpecTests(unittest.TestCase):
    def test_schema_accepts_checker_and_sandbox(self):
        payload = {
            "checker": {"kind": "FLOAT", "epsilon": 1e-6},
            "sandbox": {"time_limit_seconds": 3, "memory_limit_mb": 1024},
            "input_grammar": "n followed by n integers",
            "constraints": [], "variables": [], "relations": [],
            "output_partitions": [], "sequences": [], "fault_model": [],
            "warnings": [],
            "coverage_obligations": [{
                "id": "minimum", "category": "boundary",
                "description": "minimum valid input", "priority": "critical",
                "required": True,
            }],
        }
        model = TestModelResponse.model_validate(payload)
        self.assertEqual(model.checker.kind, "FLOAT")
        self.assertEqual(model.sandbox.memory_limit_mb, 1024)

    def test_normalizer_bounds_untrusted_specs(self):
        normalized = normalize_test_model({
            "checker": {"kind": "FLOAT", "epsilon": "0.000001"},
            "sandbox": {"time_limit_seconds": 1000, "memory_limit_mb": 99999},
        })
        self.assertEqual(normalized["checker"]["epsilon"], 1e-6)
        self.assertEqual(normalized["sandbox"]["time_limit_seconds"], 60.0)
        self.assertEqual(normalized["sandbox"]["memory_limit_mb"], 4096)

    def test_optional_fallback_contains_safe_specs(self):
        result = neutral_result(TaskType.BUILD_TEST_MODEL)
        normalized = normalize_test_model(result)
        self.assertEqual(normalized["checker"]["kind"], "TOKEN")
        self.assertEqual(normalized["sandbox"]["memory_limit_mb"], 512)

    def test_pipeline_applies_generated_specs_before_execution(self):
        class Generator:
            cases_per_round = 10

        with TemporaryDirectory() as directory:
            backend = DockerJudge(Path(directory))
            judge = RetryingJudge(backend)
            pipeline = RunPipeline(
                Generator(), Generator(), judge,
                checker_from_profile({"kind": "TOKEN"}),
                auto_checker=True, auto_sandbox=True,
            )
            model = normalize_test_model({
                "checker": {"kind": "FLOAT", "epsilon": 1e-5},
                "sandbox": {"time_limit_seconds": 3, "memory_limit_mb": 1024},
            })
            pipeline._apply_test_model_specs(model)
            self.assertEqual(pipeline.checker.kind, "FLOAT")
            self.assertEqual(pipeline.execution.checker.kind, "FLOAT")
            self.assertEqual(backend.limits["run_timeout_seconds"], 5)
            self.assertEqual(backend.limits["memory"], "1024m")

    def test_generated_special_checker_is_never_executed(self):
        class Generator:
            cases_per_round = 10

        with TemporaryDirectory() as directory:
            pipeline = RunPipeline(
                Generator(), Generator(), DockerJudge(Path(directory)),
                checker_from_profile({"kind": "TOKEN"}), auto_checker=True,
            )
            model = normalize_test_model({
                "checker": {"kind": "PYTHON_SCRIPT", "multiple_valid_answers": True}
            })
            with self.assertRaisesRegex(RuntimeError, "audited problem-local checker"):
                pipeline._apply_test_model_specs(model)


if __name__ == "__main__":
    unittest.main()
