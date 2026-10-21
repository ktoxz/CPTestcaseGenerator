from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from testgen.codenet import (
    find_local_oracle_bundle,
    LocalCodeNetSource,
    validate_codenet_request,
)


ROOT = Path(__file__).resolve().parents[1]


class CodeNetValidationTests(unittest.TestCase):
    def test_remote_exporter_exists(self) -> None:
        self.assertTrue((ROOT / "scripts" / "export_codenet.py").is_file())

    def test_accepts_codenet_problem_id_and_limit(self) -> None:
        validate_codenet_request("p00004", 100, 100)

    def test_rejects_non_codenet_problem_before_remote_work(self) -> None:
        with self.assertRaisesRegex(ValueError, "requires a CodeNet problem id"):
            validate_codenet_request("cf2275d", 100, 100)

    def test_rejects_limit_outside_configured_bound(self) -> None:
        with self.assertRaisesRegex(ValueError, "between 1 and 100"):
            validate_codenet_request("p00004", 101, 100)

    def test_finds_problem_local_oracle_manifest(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            root = Path(temp)
            bundle = root / "cf2275d" / "oracle"
            bundle.mkdir(parents=True)
            (bundle / "manifest.json").write_text("[]", encoding="utf-8")
            self.assertEqual(
                find_local_oracle_bundle(root, "cf2275d"), bundle
            )
            self.assertIsNone(find_local_oracle_bundle(root, "missing"))

    def test_finds_and_loads_raw_problem_oracle_sources(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            root = Path(temp)
            bundle = root / "cf2218b" / "oracle"
            accepted = bundle / "sources" / "Accepted"
            wrong = bundle / "sources" / "WrongAnswer"
            accepted.mkdir(parents=True)
            wrong.mkdir(parents=True)
            (accepted / "1.cpp").write_text("int main() {}", encoding="utf-8")
            (accepted / "2.cpp").write_text("int main() {}", encoding="utf-8")
            (wrong / "1.py").write_text("print(0)", encoding="utf-8")

            self.assertEqual(find_local_oracle_bundle(root, "cf2218b"), bundle)

            output = root / "output"
            solutions = LocalCodeNetSource(bundle).fetch("cf2218b", output, 1)
            self.assertEqual(len(solutions), 2)
            self.assertTrue((output / "manifest.json").is_file())
            self.assertEqual(
                {solution.label for solution in solutions},
                {"CodeNet Accepted", "CodeNet Wrong Answer"},
            )
            self.assertEqual(
                {solution.dialect for solution in solutions},
                {"C++17", "Python3"},
            )

    def test_normalizes_non_accepted_manifest_label(self) -> None:
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            root = Path(temp)
            raw_bundle = root / "raw"
            accepted = raw_bundle / "sources" / "Accepted"
            wrong = raw_bundle / "sources" / "WrongAnswer"
            accepted.mkdir(parents=True)
            wrong.mkdir(parents=True)
            (accepted / "1.cpp").write_text("int main() {}", encoding="utf-8")
            (wrong / "1.cpp").write_text("int main() {}", encoding="utf-8")

            bundle = root / "bundle"
            LocalCodeNetSource(raw_bundle).fetch("cf1352c", bundle, 1)
            manifest_path = bundle / "manifest.json"
            rows = json.loads(manifest_path.read_text(encoding="utf-8"))
            rows[1]["label"] = "Non-Accepted"
            manifest_path.write_text(json.dumps(rows), encoding="utf-8")

            solutions = LocalCodeNetSource(bundle).fetch(
                "cf1352c", root / "output", 1
            )
            self.assertEqual(
                [solution.label for solution in solutions],
                ["CodeNet Accepted", "CodeNet Wrong Answer"],
            )


if __name__ == "__main__":
    unittest.main()
