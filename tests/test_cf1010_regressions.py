import importlib.util
import unittest
from pathlib import Path

from testgen.checker import checker_from_profile


ROOT = Path(__file__).resolve().parents[1]


def load_cf1010a_validator():
    path = ROOT / "data" / "problems" / "cf1010a" / "validator.py"
    spec = importlib.util.spec_from_file_location("cf1010a_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cf1010RegressionTests(unittest.TestCase):
    def test_border_uses_token_whitespace_semantics(self):
        checker = checker_from_profile({"kind": "TOKEN"})
        self.assertTrue(checker.accepts("2\n0 4 ", "2\n0 4\n"))

    def test_fly_validator_accepts_official_samples(self):
        validator = load_cf1010a_validator()
        for value in (
            "2\n12\n11 8\n7 5\n",
            "3\n1\n1 4 1\n2 5 3\n",
            "6\n2\n4 6 3 3 5 6\n2 6 3 6 5 3\n",
        ):
            self.assertTrue(validator.valid_input(value))

    def test_fly_validator_rejects_feasible_fuel_above_guaranteed_bound(self):
        validator = load_cf1010a_validator()
        invalid = (
            "1000\n1\n"
            + " ".join(["10"] * 1000)
            + "\n"
            + " ".join(["10"] * 1000)
            + "\n"
        )
        self.assertFalse(validator.valid_input(invalid))

    def test_fly_validator_keeps_impossible_flights(self):
        validator = load_cf1010a_validator()
        self.assertTrue(validator.valid_input("2\n1\n1 2\n2 2\n"))


if __name__ == "__main__":
    unittest.main()
