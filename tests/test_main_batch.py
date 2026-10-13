from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import argparse
import io
import json
import subprocess
from contextlib import redirect_stdout
from unittest.mock import patch

from main import child_cli_args, discover_problem_range, run_batch

TEST_TMP = Path(__file__).resolve().parents[1] / ".test-tmp"


def make_problem(root: Path, name: str, *, statement: bool = True) -> None:
    problem = root / name
    problem.mkdir()
    if statement:
        (problem / "statement.md").write_text("# Problem", encoding="utf-8")


class MainBatchTests(unittest.TestCase):
    def test_batch_emits_and_saves_result_before_starting_next_problem(self):
        TEST_TMP.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=TEST_TMP) as directory:
            root = Path(directory)
            problems = root / "data" / "problems"
            problems.mkdir(parents=True)
            for name in ("p02548", "p03862"):
                make_problem(problems, name)
            output = root / "output"
            console = io.StringIO()
            args = argparse.Namespace(statement=None, resume_oracle=None, oracle_cache=None,
                problem_range=["p02548", "p03862"], output=output, batch_fail_fast=False)
            def fake_run(command, **kwargs):
                problem = command[command.index("--problem") + 1]
                if problem == "p03862":
                    self.assertIn('"cases": 2', console.getvalue())
                    self.assertIn('"oracle_metrics"', console.getvalue())
                    saved = json.loads((output / "batch-report.json").read_text(encoding="utf-8"))
                    self.assertEqual(saved["completed"], 1)
                dest = Path(command[command.index("--output") + 1])
                dest.mkdir(parents=True)
                (dest / "report.json").write_text(json.dumps({"cases": [{}, {}],
                    "oracle_metrics": {"tpr": 1}, "generation_latency": {"seconds": 120}}), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0)
            with patch("main.ROOT", root), patch("main.subprocess.run", side_effect=fake_run), redirect_stdout(console):
                run_batch(args, [], argparse.ArgumentParser())
            self.assertIn('"generation_latency"', console.getvalue())
            self.assertIn('"problem": "p03862"', console.getvalue())

    def test_discover_problem_range_uses_existing_problem_directories(self) -> None:
        TEST_TMP.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=TEST_TMP) as directory:
            root = Path(directory)
            make_problem(root, "p02580")
            make_problem(root, "p02661")
            make_problem(root, "p02685", statement=False)
            make_problem(root, "p03862")
            make_problem(root, "p03863")
            make_problem(root, "notes")

            self.assertEqual(
                discover_problem_range(root, "p02580", "p03862"),
                ["p02580", "p02661", "p03862"],
            )

    def test_discover_problem_range_rejects_invalid_endpoints(self) -> None:
        TEST_TMP.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=TEST_TMP) as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "pNNNNN"):
                discover_problem_range(root, "2580", "p03862")
            with self.assertRaisesRegex(ValueError, "greater"):
                discover_problem_range(root, "p03862", "p02580")

    def test_child_cli_args_removes_batch_only_arguments(self) -> None:
        self.assertEqual(child_cli_args([
            "--problem-range", "p02580", "p03862",
            "--oracle",
            "--output", "custom",
            "--llm-timeout", "300",
            "--batch-fail-fast",
        ]), ["--oracle", "--llm-timeout", "300"])

    def test_child_cli_args_removes_explicit_problem_list(self) -> None:
        self.assertEqual(child_cli_args([
            "--problems", "p02580", "p02661", "p03862",
            "--judge=remote",
            "--output=custom",
        ]), ["--judge=remote"])


if __name__ == "__main__":
    unittest.main()
