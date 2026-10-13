import unittest

from testgen.source_edits import apply_source_edits


class SourceEditTests(unittest.TestCase):
    def test_applies_exact_changes_in_order(self):
        self.assertEqual(apply_source_edits("if n < 3:\n    print(n)\n", [
            {"old": "n < 3", "new": "n <= 3"},
            {"old": "print(n)", "new": "print(n + 1)"},
        ]), "if n <= 3:\n    print(n + 1)\n")

    def test_rejects_missing_ambiguous_noop_and_malformed_changes(self):
        for edits in ([{"old": "x", "new": "y"}],
                      [{"old": "n", "new": "m"}],
                      [{"old": "print(n)", "new": "print(n)"}],
                      [{"old": "print(n)", "new": 3}], []):
            with self.subTest(edits=edits), self.assertRaises(ValueError):
                apply_source_edits("n = 1\nprint(n)\n", edits)
