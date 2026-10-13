from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from testgen.checker import checker_from_profile
from testgen.pipeline import Pipeline, requires_input_aware_checker

from test_pipeline import FakeCases, FakeJudge, FakeSolutions


class SpecialCheckerTests(unittest.TestCase):
    @staticmethod
    def checker():
        script = (
            Path(__file__).resolve().parents[1]
            / "data" / "problems" / "p00954" / "output_checker.py"
        )
        return checker_from_profile({
            "kind": "PYTHON_SCRIPT",
            "script": str(script.resolve()),
        })

    def test_default_accepts_case_delegates_to_regular_checker(self):
        checker = checker_from_profile({"kind": "TOKEN"})
        self.assertTrue(checker.accepts_case("1 2\n", "1 2\n", "ignored\n"))
        self.assertFalse(checker.accepts_case("1 3\n", "1 2\n", "ignored\n"))

    def test_p00954_accepts_official_and_alternative_outputs(self):
        input_text = "2\n5 6\n1000000000 2\n"
        official = (
            "4\n5 6\n0 6\n0 0\n5 0\n"
            "3\n1000000000 0\n0 2\n999999999 0\n"
        )
        alternative = (
            "3\n0 0\n5 6\n4 5\n"
            "3\n0 0\n1000000000 2\n499999999 1\n"
        )
        checker = self.checker()
        self.assertTrue(checker.accepts_case(official, official, input_text))
        self.assertTrue(checker.accepts_case(alternative, official, input_text))

    def test_p00954_rejects_invalid_geometry_or_format(self):
        checker = self.checker()
        one_case = "1\n5 6\n"
        invalid_outputs = (
            "3\n0 0\n6 6\n5 0\n",  # coordinate outside the bounding box
            "3\n0 0\n5 5\n4 4\n",  # misses y=6 and has zero area
            "4\n0 0\n5 6\n0 6\n5 0\n",  # self-intersecting
            "3\n0 0\n5 6\n4 5\n99\n",  # trailing token
        )
        for actual in invalid_outputs:
            with self.subTest(actual=actual):
                self.assertFalse(checker.accepts_case(actual, "", one_case))
        huge_rectangle = "4\n0 0\n100000 0\n100000 100000\n0 100000\n"
        self.assertFalse(checker.accepts_case(
            huge_rectangle, "", "1\n100000 100000\n"
        ))

    def test_multiple_answer_statement_requires_special_checker(self):
        statement = (
            "When more than one polygon satisfies the conditions, "
            "any one of them is acceptable."
        )
        self.assertTrue(requires_input_aware_checker(statement))
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            with self.assertRaisesRegex(RuntimeError, "input-aware special checker"):
                Pipeline(
                    FakeSolutions(), FakeCases(), FakeJudge(),
                    checker_from_profile({"kind": "TOKEN"}),
                ).run("p00954", statement, Path(temp), iterations=1)

    def test_cf2218a_checker_accepts_all_optimal_outputs(self):
        script = (
            Path(__file__).resolve().parents[1]
            / "data" / "problems" / "cf2218a" / "output_checker.py"
        )
        checker = checker_from_profile({
            "kind": "PYTHON_SCRIPT",
            "script": str(script.resolve()),
        })
        input_text = "4\n-67\n-1\n66\n67\n"
        self.assertTrue(checker.accepts_case(
            "-67\n0\n67\n67\n", "ignored\n", input_text
        ))
        for invalid in (
            "-67\n-2\n67\n67\n",  # y < x
            "-67\n0\n68\n67\n",   # y outside the allowed range
            "-67\n0\n67\n",       # missing answer
            "-67\n0\n67\n67\n0\n",  # trailing answer
            "-67\nnope\n67\n67\n",
        ):
            with self.subTest(invalid=invalid):
                self.assertFalse(checker.accepts_case(
                    invalid, "ignored\n", input_text
                ))

    def test_cf2218a_wording_requires_special_checker(self):
        self.assertTrue(requires_input_aware_checker(
            "If there are multiple valid y, you may output any of them."
        ))


if __name__ == "__main__":
    unittest.main()
