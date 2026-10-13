import io
import json
import tempfile
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from testgen.progress import ConsoleProgress


class ProgressLatencyTests(unittest.TestCase):
    def test_latency_events_are_logged_and_summarized(self):
        with tempfile.TemporaryDirectory(
            dir=Path(__file__).resolve().parents[1]
        ) as directory:
            path = Path(directory) / "latency.jsonl"
            progress = ConsoleProgress(interval_seconds=60)
            progress.bind_latency_log(path)
            with redirect_stderr(io.StringIO()):
                progress.latency(
                    "judge.compile", 0.125, solution_id="s1", verdict="PASS"
                )
                progress.latency(
                    "judge.compile", 0.375, solution_id="s2", verdict="PASS"
                )

            rows = [json.loads(line) for line in path.read_text(
                encoding="utf-8"
            ).splitlines()]
            self.assertEqual([row["duration_ms"] for row in rows], [125.0, 375.0])
            summary = progress.latency_summary()["components"]["judge.compile"]
            self.assertEqual(summary["count"], 2)
            self.assertEqual(summary["total_ms"], 500.0)
            self.assertEqual(summary["avg_ms"], 250.0)
            self.assertEqual(summary["max_ms"], 375.0)

    def test_waiting_records_success_and_error(self):
        progress = ConsoleProgress(interval_seconds=60)
        with redirect_stderr(io.StringIO()):
            with progress.waiting("ok stage", component="test.ok"):
                time.sleep(0.001)
            with self.assertRaisesRegex(RuntimeError, "boom"):
                with progress.waiting("bad stage", component="test.bad"):
                    raise RuntimeError("boom")
        summary = progress.latency_summary()["components"]
        self.assertEqual(summary["test.ok"]["count"], 1)
        self.assertEqual(summary["test.bad"]["count"], 1)


if __name__ == "__main__":
    unittest.main()
