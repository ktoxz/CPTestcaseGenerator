import unittest

from testgen.input_recipe import expand_input
from testgen.ollama import OllamaCaseGenerator


class InputRecipeTests(unittest.TestCase):
    def test_expands_large_sorted_sequence_with_exact_count(self):
        text = expand_input(["100000 1\n", {
            "start": -50000, "step": 1, "count": 100000, "separator": " "
        }, "\n"])
        lines = text.splitlines()
        values = list(map(int, lines[1].split()))
        self.assertEqual(len(values), 100000)
        self.assertEqual((values[0], values[-1]), (-50000, 49999))

    def test_repeated_rows(self):
        self.assertEqual(expand_input(["2\n", {"text": "1 2\n", "repeat": 2}]),
                         "2\n1 2\n1 2\n")

    def test_rejects_oversized_invalid_and_executable_recipes(self):
        for part in ({"text": "x", "repeat": 10**12},
                     {"text": "x" * 100, "repeat": 200000},
                     {"code": "print(123)"},
                     {"start": 0, "step": 1, "count": True, "separator": " "}):
            with self.subTest(part=str(part)[:50]), self.assertRaises(ValueError):
                expand_input([part])

    def test_normalizes_recipes_and_drops_invalid_case(self):
        rows = OllamaCaseGenerator._valid_rows([
            {"input_parts": ["2\n", {"text": "1 ", "repeat": 2}], "family": "stress"},
            {"input_parts": [{"code": "unsafe"}], "family": "invalid"},
        ], 10)
        self.assertEqual(rows, [{"input": "2\n1 1 ", "family": "stress"}])

    def test_large_literal_input_is_rejected_but_large_recipe_is_expanded(self):
        literal = "1 " * 1001
        rows = OllamaCaseGenerator._valid_rows([
            {"input": literal, "family": "raw-large"},
            {
                "input_parts": [{"text": "1 ", "repeat": 1001}],
                "family": "recipe-large",
            },
        ], 10)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["family"], "recipe-large")
        self.assertEqual(rows[0]["input"], literal)

    def test_rejects_ambiguous_input_and_input_parts(self):
        rows = OllamaCaseGenerator._valid_rows([{
            "input": "1\n",
            "input_parts": ["1\n"],
            "family": "ambiguous",
        }], 10)
        self.assertEqual(rows, [])
