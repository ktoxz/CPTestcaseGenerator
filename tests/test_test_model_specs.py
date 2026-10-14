import unittest

from testgen.coverage import TestModelResponse, normalize_test_model
from testgen.fallback import neutral_result
from testgen.llm_contract import TaskType


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


if __name__ == "__main__":
    unittest.main()
