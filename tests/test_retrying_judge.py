"""Infrastructure retry policy must not reinterpret code verdicts."""

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
import subprocess
from tempfile import TemporaryDirectory

from testgen.docker_judge import DockerJudge
from testgen.domain import Judge, Result, Solution
from testgen.infrastructure.file_run_store import FileRunStore
from testgen.retrying_judge import InfrastructureError, RetryingJudge, retry_setup


class SequenceJudge(Judge):
    def __init__(self, compile_verdicts, run_verdicts):
        self.compile_verdicts = iter(compile_verdicts)
        self.run_verdicts = iter(run_verdicts)
        self.compiles = 0
        self.runs = []

    def compile(self, solution):
        self.compiles += 1
        verdict = next(self.compile_verdicts)
        return Result(solution.id, verdict, stderr="docker unavailable" if verdict == "INFRA" else "")

    def execute(self, solution, case_id, input_text):
        self.runs.append((solution.id, case_id, input_text))
        verdict = next(self.run_verdicts)
        return Result(solution.id, verdict, case_id, stderr="ssh timeout" if verdict == "INFRA" else "")


class RetryTests(TestCase):
    def setUp(self):
        self.solution = Solution("s", "candidate_ac", "Python", Path("main.py"))

    @patch("testgen.retrying_judge.time.sleep")
    def test_infra_retries_and_then_succeeds(self, sleep):
        backend = SequenceJudge(["INFRA", "INFRA", "PASS"], ["INFRA", "PASS"])
        judge = RetryingJudge(backend, max_attempts=3, delay_seconds=2)
        self.assertEqual(judge.compile(self.solution).verdict, "PASS")
        self.assertEqual(judge.execute(self.solution, "case-1", "1\n").verdict, "PASS")
        self.assertEqual(backend.compiles, 3)
        self.assertEqual(backend.runs, [("s", "case-1", "1\n")] * 2)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [2, 4, 2])

    @patch("testgen.retrying_judge.time.sleep")
    def test_code_verdicts_are_not_retried(self, sleep):
        backend = SequenceJudge(["CE"], ["TLE"])
        judge = RetryingJudge(backend)
        self.assertEqual(judge.compile(self.solution).verdict, "CE")
        self.assertEqual(judge.execute(self.solution, "case-1", "1\n").verdict, "TLE")
        self.assertEqual(backend.compiles, 1)
        self.assertEqual(len(backend.runs), 1)
        sleep.assert_not_called()

    @patch("testgen.retrying_judge.time.sleep")
    def test_exhausted_infra_stops_run(self, sleep):
        backend = SequenceJudge(["INFRA", "INFRA", "INFRA"], [])
        judge = RetryingJudge(backend, max_attempts=3, delay_seconds=0)
        with self.assertRaisesRegex(InfrastructureError, "after 3 attempts"):
            judge.compile(self.solution)
        self.assertEqual(backend.compiles, 3)

    @patch("testgen.retrying_judge.time.sleep")
    def test_missing_runtime_fails_without_retry_delay(self, sleep):
        backend = SequenceJudge(["INFRA"], [])

        def compile_with_missing_runtime(solution):
            backend.compiles += 1
            return Result(
                solution.id, "INFRA", stderr=(
                    "No runtime for language/dialect "
                    "('C++', 'Unknown external dialect')"
                )
            )

        backend.compile = compile_with_missing_runtime
        judge = RetryingJudge(backend, max_attempts=3, delay_seconds=2)
        with self.assertRaisesRegex(InfrastructureError, "non-retryable"):
            judge.compile(self.solution)
        self.assertEqual(backend.compiles, 1)
        sleep.assert_not_called()

    @patch("testgen.retrying_judge.time.sleep")
    def test_remote_setup_retries_runtime_error(self, sleep):
        calls = []

        def probe():
            calls.append(1)
            if len(calls) < 3:
                raise RuntimeError("Docker not ready")
            return "ready"

        self.assertEqual(retry_setup(probe, label="KHOI", max_attempts=3,
                                     delay_seconds=2), "ready")
        self.assertEqual(len(calls), 3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [2, 4])

    def test_local_docker_timeout_is_infra_and_forces_cleanup(self):
        with TemporaryDirectory() as directory:
            judge = DockerJudge(Path(directory))
            calls = []

            def fake_run(args, **kwargs):
                calls.append(args)
                if args[:3] == ["docker", "rm", "-f"]:
                    return subprocess.CompletedProcess(args, 0, args[3], "")
                raise subprocess.TimeoutExpired(args, kwargs["timeout"])

            with patch("testgen.docker_judge.subprocess.run", side_effect=fake_run):
                code, _out, err, timed_out = judge._run(
                    "test:local", Path(directory), Path(directory), "true", timeout=5)
            self.assertEqual(code, 125)
            self.assertFalse(timed_out)
            self.assertIn("not code TLE", err)
            self.assertEqual(calls[0][calls[0].index("--name") + 1], calls[1][3])

    def test_local_docker_stdin_uses_exact_utf8_bytes(self):
        with TemporaryDirectory() as directory:
            judge = DockerJudge(Path(directory))
            captured = {}

            def fake_run(args, **kwargs):
                captured.update(kwargs)
                return subprocess.CompletedProcess(args, 0, b"k\n", b"")

            with patch("testgen.docker_judge.subprocess.run", side_effect=fake_run):
                code, out, err, timed_out = judge._run(
                    "test:local", Path(directory), Path(directory), "cat",
                    input_text="k\n", timeout=5,
                )

            self.assertEqual(captured["input"], b"k\n")
            self.assertNotIn("text", captured)
            self.assertNotIn("encoding", captured)
            self.assertEqual((code, out, err, timed_out), (0, "k\n", "", False))

    def test_file_store_preserves_lf_on_windows(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "case.in"
            FileRunStore().write_text(target, "first\nsecond\n")
            self.assertEqual(target.read_bytes(), b"first\nsecond\n")
