import json
import subprocess
import unittest
from unittest.mock import patch

from testgen.claude import ClaudeClient
from testgen.progress import ConsoleProgress


class ClaudeClientTests(unittest.TestCase):
    @patch.object(ClaudeClient, "_run_cli")
    def test_uses_cli_login_and_structured_output(self, run) -> None:
        run.return_value = subprocess.CompletedProcess(
            ["claude"], 0,
            stdout=json.dumps({
                "type": "result",
                "structured_output": {"answer": 42},
            }),
            stderr="",
        )
        progress = ConsoleProgress()
        client = ClaudeClient(
            executable="claude.cmd", progress=progress
        )
        self.assertEqual(client.ask_json("prompt", label="test"), {"answer": 42})
        args = run.call_args.args[0]
        submitted_prompt = run.call_args.args[1]
        self.assertIn("--print", args)
        self.assertNotIn("--json-schema", args)
        self.assertIn("--safe-mode", args)
        self.assertIn("--disable-slash-commands", args)
        self.assertEqual(args[args.index("--prompt-suggestions") + 1], "false")
        self.assertIn("--system-prompt", args)
        self.assertNotIn("--append-system-prompt", args)
        self.assertIn("--no-session-persistence", args)
        self.assertEqual(args[args.index("--model") + 1], "fable")
        self.assertEqual(args[args.index("--effort") + 1], "low")
        self.assertEqual(submitted_prompt, "prompt")
        self.assertNotIn("prompt", args)
        self.assertEqual(
            progress.latency_summary()["components"]["claude.request"]["count"],
            1,
        )

    @patch.object(ClaudeClient, "_run_cli")
    def test_accepts_result_text_envelope(self, run) -> None:
        run.return_value = subprocess.CompletedProcess(
            ["claude"], 0,
            stdout=json.dumps({"type": "result", "result": '{"ok":true}'}),
            stderr="",
        )
        result = ClaudeClient(executable="claude.cmd").ask_json("prompt")
        self.assertEqual(result, {"ok": True})

    @patch.object(ClaudeClient, "_run_cli")
    def test_reports_cli_failure(self, run) -> None:
        run.return_value = subprocess.CompletedProcess(
            ["claude"], 1, stdout="", stderr="authentication required"
        )
        with self.assertRaisesRegex(RuntimeError, "authentication required"):
            ClaudeClient(executable="claude.cmd").ask_json("prompt")

    @patch("testgen.claude.shutil.which", return_value=None)
    @patch.object(ClaudeClient, "_run_cli")
    def test_reports_cli_failure_from_stdout(self, run, which) -> None:
        run.return_value = subprocess.CompletedProcess(
            ["claude"], 1, stdout=json.dumps({"type": "result", "result": "rate limit reached"}), stderr=""
        )
        with self.assertRaisesRegex(RuntimeError, "rate limit reached"):
            ClaudeClient(executable="claude.cmd").ask_json("prompt")

    @patch("testgen.claude.shutil.which", return_value=None)
    def test_requires_installed_cli(self, which) -> None:
        with self.assertRaisesRegex(RuntimeError, "not found"):
            ClaudeClient()

    def test_rejects_unsupported_effort(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported Claude effort"):
            ClaudeClient(executable="claude.cmd", effort="fastest")

    @patch.object(ClaudeClient, "_terminate_process_tree")
    @patch("testgen.claude.subprocess.Popen")
    def test_hard_timeout_terminates_the_cli_process_tree(
        self, popen, terminate
    ) -> None:
        process = popen.return_value
        process.communicate.side_effect = subprocess.TimeoutExpired(
            cmd=["claude"], timeout=50
        )
        client = ClaudeClient(executable="claude.cmd", timeout_seconds=50)
        with self.assertRaises(subprocess.TimeoutExpired):
            client._run_cli(["claude.cmd", "--print"], "prompt")
        terminate.assert_called_once_with(process)
        self.assertEqual(popen.call_args.kwargs["env"]["CLAUDE_CODE_MAX_OUTPUT_TOKENS"], "32768")


if __name__ == "__main__":
    unittest.main()
