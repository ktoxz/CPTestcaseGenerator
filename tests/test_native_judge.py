from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from testgen.domain import Solution
from testgen.native_judge import NativeJudge, _bytes_from_limit
from testgen.runtime import RuntimeCatalog


ROOT = Path(__file__).resolve().parents[1]


class NativeJudgeConfigurationTests(unittest.TestCase):
    def test_parses_docker_style_memory_limits(self) -> None:
        self.assertEqual(_bytes_from_limit("512m"), 512 * 1024**2)
        self.assertEqual(_bytes_from_limit("1gb"), 1024**3)
        with self.assertRaises(ValueError):
            _bytes_from_limit("many")

    def test_requires_explicit_unsafe_acknowledgement(self) -> None:
        with patch("testgen.native_judge.sys.platform", "linux"):
            with self.assertRaisesRegex(RuntimeError, "not a security boundary"):
                NativeJudge(ROOT / ".test-tmp" / "native-no-ack")

    def test_native_compile_commands_are_argument_lists(self) -> None:
        catalog = RuntimeCatalog(ROOT / "config" / "runtimes.json")
        source = Path("/tmp/source/main.cpp")
        work = Path("/tmp/build")
        runtime = next(item for item in catalog.runtimes if item.id == "cpp17")
        command = NativeJudge._compile_command(runtime, source, work)
        self.assertEqual(command[0:3], ["g++", "-std=gnu++17", "-O2"])
        self.assertEqual(command[-1], str(work / "main"))


@unittest.skipUnless(sys.platform == "linux", "Kaggle native judge is Linux-only")
class NativeJudgeLinuxSmokeTests(unittest.TestCase):
    def test_compiles_and_runs_python_with_scrubbed_environment(self) -> None:
        with TemporaryDirectory(dir=ROOT / ".test-tmp") as directory:
            root = Path(directory)
            config = root / "sandbox.json"
            config.write_text(json.dumps({
                "memory": "512m",
                "pids_limit": 32,
                "compile_timeout_seconds": 20,
                "run_timeout_seconds": 2,
                "stdout_limit_bytes": 65536,
                "stderr_limit_bytes": 8192,
            }), encoding="utf-8")
            source = root / "candidate.py"
            source.write_text(
                "import os, sys\n"
                "print(os.environ.get('KAGGLE_TEST_SECRET', 'clean'))\n"
                "print(sys.stdin.read().strip())\n",
                encoding="utf-8",
            )
            judge = NativeJudge(
                root / "build",
                RuntimeCatalog(ROOT / "config" / "runtimes.json"),
                config,
                allow_unsafe=True,
            )
            solution = Solution("candidate", "candidate_ac", "Python", source)
            self.assertEqual(judge.compile(solution).verdict, "PASS")
            with patch.dict("os.environ", {"KAGGLE_TEST_SECRET": "do-not-leak"}):
                result = judge.execute(solution, "case-1", "hello\n")
            self.assertEqual(result.verdict, "PASS")
            self.assertEqual(result.actual, "clean\nhello\n")


if __name__ == "__main__":
    unittest.main()
