from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from testgen.pipeline import samples


ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT / "data" / "problems" / "p00061"


def load_validator():
    spec = importlib.util.spec_from_file_location("p00061_validator", PROBLEM / "validator.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class P00061ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_accepts_official_sample(self) -> None:
        statement = (PROBLEM / "statement.md").read_text(encoding="utf-8")
        sample_input = samples(statement)[0][0]
        self.assertTrue(self.validator.valid(sample_input))

    def test_accepts_boundaries_and_multiple_queries(self) -> None:
        self.assertTrue(self.validator.valid("1,0\n30,30\n100,15\n0,0\n1\n30\n"))

    def test_rejects_unconsumed_or_missing_separator(self) -> None:
        self.assertFalse(self.validator.valid("1,20\n0,0\n"))
        self.assertFalse(self.validator.valid("1,20\n1\n"))

    def test_rejects_duplicate_or_unknown_team(self) -> None:
        self.assertFalse(self.validator.valid("1,20\n1,10\n0,0\n1\n"))
        self.assertFalse(self.validator.valid("1,20\n0,0\n2\n"))

    def test_rejects_out_of_range_values(self) -> None:
        self.assertFalse(self.validator.valid("101,20\n0,0\n1\n"))
        self.assertFalse(self.validator.valid("1,31\n0,0\n1\n"))
        self.assertFalse(self.validator.valid("31,20\n0,0\n31\n"))


if __name__ == "__main__":
    unittest.main()
