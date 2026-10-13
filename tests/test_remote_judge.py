"""Remote transport tests that do not require Docker or SSH."""

import base64
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from scripts import remote_judge_worker as worker
from testgen.remote_judge import RemoteDockerJudge


class RemoteJudgeTests(TestCase):
    def test_worker_runs_with_isolated_mounts_and_source(self):
        with TemporaryDirectory() as directory, patch.object(worker.tempfile, "gettempdir", return_value=directory):
            calls = []

            def fake_run(args, **kwargs):
                calls.append((args, kwargs))
                return {"code": 0, "out": "answer\n", "err": "", "timed_out": False}

            request = {
                "action": "run", "run_id": "a" * 20, "work_key": "b" * 20,
                "source_name": "main.py", "source_b64": base64.b64encode(b"print(1)\n").decode(),
                "image": "test:local", "command": "python3 /src/main.py", "input": "1\n",
                "timeout": 5,
                "limits": {"pids_limit": 64, "memory": "512m", "cpus": "1",
                           "tmpfs_size": "32m", "stdout_limit_bytes": 65536,
                           "stderr_limit_bytes": 8192,
                           "docker_startup_grace_seconds": 30,
                           "container_cleanup_timeout_seconds": 15},
            }
            with patch.object(worker, "run_command", side_effect=fake_run):
                result = worker.handle(request)
            self.assertEqual(result["out"], "answer\n")
            self.assertEqual(calls[0][1]["input_text"], "1\n")
            self.assertIn("--network", calls[0][0])
            self.assertIn("none", calls[0][0])
            self.assertIn("--label", calls[0][0])
            self.assertIn("timeout", calls[0][0])
            self.assertTrue((Path(directory) / "testgen-remote-judge" / ("a" * 20) /
                             "build" / ("b" * 20) / "source" / "main.py").exists())

    def test_client_sends_source_once(self):
        with TemporaryDirectory() as directory:
            work = Path(directory) / "build"
            source = work / "source"
            source.mkdir(parents=True)
            (source / "main.py").write_text("print(1)\n")
            judge = RemoteDockerJudge.__new__(RemoteDockerJudge)
            judge.limits = {"stdout_limit_bytes": 65536, "stderr_limit_bytes": 8192,
                            "docker_startup_grace_seconds": 30,
                            "container_cleanup_timeout_seconds": 15}
            judge._synced = set()
            sent = []

            def request(payload, *, timeout):
                sent.append(payload)
                return {"code": 0, "out": "1\n", "err": "", "timed_out": False}

            judge._request = request
            judge._run("test:local", source, work, "python3 /src/main.py", timeout=5)
            judge._run("test:local", source, work, "python3 /src/main.py", timeout=5)
            self.assertIn("source_b64", sent[0])
            self.assertNotIn("source_b64", sent[1])

    def test_worker_cleans_exact_container_on_docker_timeout(self):
        with TemporaryDirectory() as directory, patch.object(worker.tempfile, "gettempdir", return_value=directory):
            calls = []

            def fake_run(args, **kwargs):
                calls.append(args)
                if args[:3] == ["docker", "rm", "-f"]:
                    return {"code": 0, "out": args[3], "err": "", "timed_out": False}
                return {"code": -1, "out": "", "err": "wall timeout", "timed_out": True}

            request = {
                "action": "run", "run_id": "a" * 20, "work_key": "b" * 20,
                "source_name": "main.py", "source_b64": base64.b64encode(b"print(1)\n").decode(),
                "image": "test:local", "command": "python3 /src/main.py", "input": "1\n",
                "timeout": 5,
                "limits": {"pids_limit": 64, "memory": "512m", "cpus": "1",
                           "tmpfs_size": "32m", "stdout_limit_bytes": 65536,
                           "stderr_limit_bytes": 8192,
                           "docker_startup_grace_seconds": 30,
                           "container_cleanup_timeout_seconds": 15},
            }
            with patch.object(worker, "run_command", side_effect=fake_run):
                result = worker.handle(request)
            self.assertEqual(result["code"], 125)
            self.assertFalse(result["timed_out"])
            self.assertEqual(calls[1][:3], ["docker", "rm", "-f"])
            self.assertEqual(calls[0][calls[0].index("--name") + 1], calls[1][3])

    def test_worker_batches_inputs_with_individual_containers(self):
        with TemporaryDirectory() as directory, patch.object(worker.tempfile, "gettempdir", return_value=directory):
            inputs = []

            def fake_run(args, **kwargs):
                inputs.append(kwargs["input_text"])
                return {"code": 0, "out": kwargs["input_text"],
                        "err": "", "timed_out": False}

            request = {
                "action": "run_many", "run_id": "a" * 20, "work_key": "b" * 20,
                "source_name": "main.py", "source_b64": base64.b64encode(b"print(1)\n").decode(),
                "image": "test:local", "command": "python3 /src/main.py",
                "inputs": ["1\n", "2\n"], "timeout": 5,
                "limits": {"pids_limit": 64, "memory": "512m", "cpus": "1",
                           "tmpfs_size": "32m", "stdout_limit_bytes": 65536,
                           "stderr_limit_bytes": 8192,
                           "docker_startup_grace_seconds": 30,
                           "container_cleanup_timeout_seconds": 15},
            }
            with patch.object(worker, "run_command", side_effect=fake_run):
                result = worker.handle(request)
            self.assertEqual(inputs, ["1\n", "2\n"])
            self.assertEqual([run["out"] for run in result["runs"]], inputs)
