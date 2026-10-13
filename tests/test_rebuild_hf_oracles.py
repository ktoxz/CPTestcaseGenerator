import unittest

from scripts.rebuild_hf_oracles import Candidate, diverse_order, parse_slug, runtime_for


def candidate(submission_id: str, source: str, dialect: str = "C++17") -> Candidate:
    return Candidate(
        submission_id=submission_id,
        source=source,
        verdict="OK",
        dataset_language=dialect,
        language="C++",
        dialect=dialect,
        extension=".cpp",
        standard="gnu++17",
        passed_test_count=1,
    )


class RebuildHfOraclesTests(unittest.TestCase):
    def test_parse_slug(self) -> None:
        self.assertEqual(parse_slug("cf1008a"), "1008/A")
        self.assertEqual(parse_slug("CF1006c"), "1006/C")
        with self.assertRaises(ValueError):
            parse_slug("p01008")

    def test_runtime_mapping_preserves_cpp_dialect(self) -> None:
        self.assertEqual(runtime_for("GNU C++11")[1], "C++11")
        self.assertEqual(runtime_for("C++14 (GCC 6-32)")[1], "C++14")
        self.assertEqual(runtime_for("C++17 (GCC 7-32)")[1], "C++17")
        self.assertIsNone(runtime_for("MS C++ 2017"))
        self.assertIsNone(runtime_for("C++20 (GCC 13-64)"))

    def test_diverse_order_deduplicates_formatting_only_variants(self) -> None:
        values = [
            candidate("1", "int main(){return 0;}"),
            candidate("2", "int main() { return 0; }"),
            candidate("3", "int main(){return 1;}"),
        ]
        ordered = diverse_order(values)
        self.assertEqual(len(ordered), 2)
        ids = {item.submission_id for item in ordered}
        self.assertEqual(len(ids & {"1", "2"}), 1)
        self.assertIn("3", ids)


if __name__ == "__main__":
    unittest.main()
