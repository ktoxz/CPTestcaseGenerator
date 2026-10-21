from __future__ import annotations

import io
import http.client
import json
import re
import threading
import time
import unittest
import urllib.error
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from testgen.llm_contract import TaskType
from testgen.coverage import TestModelResponse
from testgen.domain import Solution
from testgen.ollama import OllamaCaseGenerator, OllamaClient, OllamaSolutionGenerator
from testgen.progress import ConsoleProgress
from testgen.throttle import (
    EndpointBusyError,
    default_prompt_throttle,
    reset_endpoint_request_gates,
)


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def response(content: str) -> Response:
    envelope = {"message": {"role": "assistant", "content": content}}
    return Response(json.dumps(envelope).encode("utf-8"))


def openai_response(content: str) -> Response:
    envelope = {
        "choices": [{"message": {"role": "assistant", "content": content}}]
    }
    return Response(json.dumps(envelope).encode("utf-8"))


def valid_test_model() -> dict:
    return {
        "input_grammar": "N\\nA_1 ... A_N",
        "constraints": ["1 <= N <= 100"],
        "variables": [{
            "name": "N",
            "description": "number of values",
            "domain": "integer in [1, 100]",
        }],
        "relations": ["Exactly N values follow N"],
        "output_partitions": ["single integer"],
        "sequences": ["one record"],
        "fault_model": ["off-by-one loop bound"],
        "warnings": [],
        "coverage_obligations": [{
            "id": "minimum-n",
            "category": "boundary",
            "description": "Exercise N = 1",
            "priority": "critical",
            "required": True,
        }],
    }


class OllamaJsonTests(unittest.TestCase):
    def test_initial_mutant_witness_uses_analysis_backend(self):
        from unittest.mock import Mock
        code = Mock()
        analysis = Mock()
        analysis.ask_json.return_value = {"witnesses": [
            {"index": 0, "input": "2\n"}, {"index": 99, "input": "ignored"}
        ]}
        rows = [{"code": "print(1)", "witness_input": "untrusted code-backend witness"}]
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generator = OllamaSolutionGenerator(code, analysis_client=analysis)
            generator._populate_mutant_witnesses("statement", [], rows, Path(temp), "batch")
        code.ask_json.assert_not_called()
        analysis.ask_json.assert_called_once()
        self.assertEqual(rows[0]["witness_input"], "2\n")
        self.assertNotIn("untrusted code-backend witness", analysis.ask_json.call_args.args[0])

    def setUp(self) -> None:
        # The process-wide prompt throttle must not carry delay state between
        # tests (or into a tight wall-clock timeout assertion below).
        default_prompt_throttle._last_dispatch = None
        reset_endpoint_request_gates()

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_test_model_uses_pydantic_schema_as_ollama_format(
        self, urlopen
    ) -> None:
        urlopen.return_value = response(json.dumps(valid_test_model()))
        client = OllamaClient("http://ollama.test", "model")

        result = OllamaCaseGenerator(client).build_test_model("Problem statement")

        payload = json.loads(urlopen.call_args.args[0].data)
        self.assertEqual(payload["format"], TestModelResponse.model_json_schema())
        self.assertNotIn("with keys", payload["messages"][1]["content"])
        self.assertEqual(result["model_version"], 1)
        self.assertEqual(result["coverage_obligations"][0]["id"], "minimum-n")

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_openai_style_uses_strict_pydantic_json_schema(self, urlopen) -> None:
        urlopen.return_value = openai_response(json.dumps(valid_test_model()))
        client = OllamaClient(
            "http://llama.test", "model", api_style="openai"
        )

        client.ask_json(
            "prompt",
            label="xây test model độc lập", task_type=TaskType.BUILD_TEST_MODEL,
            response_model=TestModelResponse,
        )

        payload = json.loads(urlopen.call_args.args[0].data)
        response_format = payload["response_format"]
        self.assertEqual(response_format["type"], "json_schema")
        self.assertIs(response_format["json_schema"]["strict"], True)
        self.assertEqual(
            response_format["json_schema"]["schema"],
            TestModelResponse.model_json_schema(),
        )

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_pydantic_validation_failure_retries_test_model(self, urlopen) -> None:
        invalid = valid_test_model()
        del invalid["variables"][0]["domain"]
        urlopen.side_effect = [
            response(json.dumps(invalid)),
            response(json.dumps(valid_test_model())),
        ]
        client = OllamaClient("http://ollama.test", "model")

        result = client.ask_json(
            "ORIGINAL PROBLEM",
            label="xây test model độc lập", task_type=TaskType.BUILD_TEST_MODEL,
            response_model=TestModelResponse,
        )

        self.assertEqual(urlopen.call_count, 2)
        self.assertEqual(
            result,
            TestModelResponse.model_validate(valid_test_model()).model_dump(),
        )
        retry = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertIn("ORIGINAL PROBLEM", retry["messages"][1]["content"])
        self.assertIn("Field required", retry["messages"][-1]["content"])

    def test_source_quality_rejects_repeated_decoder_loop(self) -> None:
        repeated = "import sys\n" + ("# Let's sort the A_i values? No.\n" * 20)
        reason = OllamaSolutionGenerator._source_quality_error(
            "Python", repeated
        )
        self.assertIn("decoder repetition loop", reason)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_source_retry_discards_large_degenerate_response(self, urlopen) -> None:
        bad = '{"correct":[{"code":"' + ("REPEATED_GARBAGE " * 100)
        valid = {
            "correct": [{"language": "Python", "code": "print(1)\n"}],
            "wrong": [],
            "validator_python": "",
        }
        urlopen.side_effect = [
            openai_response(bad),
            openai_response(json.dumps(valid)),
        ]
        client = OllamaClient(
            "http://llama.test", "gemma-local", api_style="openai"
        )
        result = client.ask_json(
            "ORIGINAL SOURCE TASK", label="sinh code AC/WA vòng 1", task_type=TaskType.GENERATE_SOLUTIONS
        )
        self.assertEqual(result, valid)
        retry_payload = json.loads(urlopen.call_args_list[1].args[0].data)
        retry_text = "\n".join(
            message["content"] for message in retry_payload["messages"]
        )
        self.assertIn("ORIGINAL SOURCE TASK", retry_text)
        self.assertNotIn("REPEATED_GARBAGE", retry_text)
        self.assertEqual(retry_payload["temperature"], 0.15)
        self.assertEqual(retry_payload["repeat_penalty"], 1.12)

    def test_code_generation_uses_one_batch_prompt_per_task(self) -> None:
        class FakeClient:
            api_style = "openai"

            def __init__(self):
                self.labels = []
                self.prompts = []

            def ask_json(self, prompt, label="Ollama"):
                self.labels.append(label)
                self.prompts.append(prompt)
                if "validator" in label:
                    return {
                        "validator_python": "raise SystemExit(0)\n",
                        "warnings": [],
                    }
                return {
                    "correct": [{
                        "language": "Python",
                        "code": f"print({index})\n",
                        "strategy_id": f"strategy-{index}",
                        "approach": "independent",
                        "time_complexity": "O(1)",
                        "space_complexity": "O(1)",
                    } for index in range(3)],
                    "wrong": [],
                    "validator_python": "",
                    "warnings": [],
                }

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            run_output = Path(temp)
            generated = run_output / "generated"
            (run_output / "test-model.json").write_text(
                json.dumps({"warnings": [], "correct_strategies": []}),
                encoding="utf-8",
            )
            client = FakeClient()
            solutions = OllamaSolutionGenerator(
                client, ac_count=3, wa_count=0, max_rounds=1
            ).generate_with_model("statement", {"warnings": [], "correct_strategies": []}, generated)
            self.assertEqual(len(solutions), 3)
            self.assertEqual(sum("sinh code AC/WA" in x for x in client.labels), 1)
            self.assertEqual(sum("sinh validator" in x for x in client.labels), 1)
            self.assertIn("exactly 3", client.prompts[0])

    def test_baseline_uses_one_batch_prompt(self) -> None:
        class FakeClient:
            api_style = "openai"

            def __init__(self):
                self.calls = 0

            def ask_json(self, prompt, label="Ollama"):
                self.calls += 1
                self.prompt = prompt
                return {
                    "requested_count": 6,
                    "rationale": "batch",
                    "cases": [{
                        "input": f"{item}\n",
                        "family": f"item-{item}",
                        "coverage_tags": [],
                    } for item in range(1, 7)],
                }

        client = FakeClient()
        plan = OllamaCaseGenerator(client, cases_per_round=6).generate_baseline(
            "# Input\nN\n",
            {"coverage_obligations": []},
            iteration=0,
            min_cases=6,
            max_cases=6,
        )
        self.assertEqual(plan["mode"], "coverage_baseline_batch")
        self.assertEqual(plan["requested_count"], 6)
        self.assertEqual(len(plan["cases"]), 6)
        self.assertEqual(client.calls, 1)
        self.assertIn("exactly 6", client.prompt)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_test_model_retry_keeps_original_problem_and_requires_full_shape(
        self, urlopen
    ) -> None:
        incomplete = '{"input_grammar":"N\\n"}'
        complete = {
            "input_grammar": "N\\n",
            "constraints": ["N >= 1"],
            "variables": [{"name": "N"}],
            "relations": [],
            "output_partitions": ["one integer"],
            "sequences": [],
            "fault_model": ["off by one"],
            "warnings": [],
            "coverage_obligations": [{
                "id": "minimum",
                "category": "boundary",
                "description": "minimum N",
                "priority": "critical",
                "required": True,
            }],
        }
        urlopen.side_effect = [
            response(incomplete),
            response(json.dumps(complete)),
        ]
        result = OllamaClient("http://ollama.test", "model").ask_json(
            "ORIGINAL PROBLEM TEXT", label="xây test model độc lập", task_type=TaskType.BUILD_TEST_MODEL
        )
        self.assertEqual(result, complete)
        second_payload = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertEqual(len(second_payload["messages"]), 4)
        self.assertIn(
            "ORIGINAL PROBLEM TEXT", second_payload["messages"][1]["content"]
        )
        self.assertEqual(
            second_payload["messages"][2],
            {"role": "assistant", "content": incomplete},
        )

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_llama_server_uses_openai_chat_endpoint(self, urlopen) -> None:
        urlopen.return_value = openai_response('{"cases":[]}')
        result = OllamaClient(
            "http://llama.test", "gemma-local", api_style="openai"
        ).ask_json("prompt", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES)
        self.assertEqual(result, {"cases": []})
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url, "http://llama.test/v1/chat/completions"
        )
        payload = json.loads(request.data)
        self.assertEqual(payload["model"], "gemma-local")
        self.assertEqual(payload["temperature"], 0)
        self.assertEqual(payload["max_tokens"], 32768)
        self.assertEqual(payload["response_format"], {"type": "json_object"})
        self.assertNotIn("format", payload)

    @patch("testgen.infrastructure.llm.ollama.time.sleep")
    @patch("testgen.ollama.urllib.request.urlopen")
    def test_transient_gateway_error_is_retried(self, urlopen, sleep) -> None:
        urlopen.side_effect = [
            urllib.error.HTTPError(
                "http://llama.test/v1/chat/completions", 502,
                "Bad Gateway", {}, None,
            ),
            openai_response('{"cases":[]}'),
        ]

        result = OllamaClient(
            "http://llama.test", "gemma-local", api_style="openai",
        ).ask_json("prompt", task_type=TaskType.GENERATE_CASES)

        self.assertEqual(result, {"cases": []})
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(0.5)

    @patch("testgen.infrastructure.llm.ollama.time.sleep")
    @patch("testgen.ollama.urllib.request.urlopen")
    def test_remote_disconnect_is_retried(self, urlopen, sleep) -> None:
        urlopen.side_effect = [
            http.client.RemoteDisconnected("closed"),
            openai_response('{"cases":[]}'),
        ]

        result = OllamaClient(
            "http://llama.test", "gemma-local", api_style="openai",
        ).ask_json("prompt", task_type=TaskType.GENERATE_CASES)

        self.assertEqual(result, {"cases": []})
        self.assertEqual(urlopen.call_count, 2)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_openai_api_key_is_sent_as_bearer_token(self, urlopen) -> None:
        urlopen.return_value = openai_response('{"cases":[]}')

        OllamaClient(
            "http://llama.test", "gemma-local", api_style="openai",
            api_key="secret-token",
        ).ask_json("prompt", task_type=TaskType.GENERATE_CASES)

        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer secret-token")

    def test_compact_mutant_rejection_keeps_actionable_sample_input(self) -> None:
        compact = OllamaSolutionGenerator._compact_mutant_rejection({
            "solution_id": "wa1",
            "reason": "candidate failed an official sample",
            "mutation_operator": "subtract two at an occupied intersection",
            "target_behavior": "occupied maximum row/column pair",
            "official_samples": [{
                "sample": 3,
                "input": "5 5 1\n2 3\n",
                "expected": "1\n",
                "actual": "0\n",
                "verdict": "PASS",
                "accepted": False,
            }],
        })
        self.assertEqual(
            compact["failed_official_samples"][0]["input"],
            "5 5 1\n2 3\n",
        )
        self.assertEqual(
            compact["mutation_operator"],
            "subtract two at an occupied intersection",
        )

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_retries_malformed_json_with_repair_context(self, urlopen) -> None:
        urlopen.side_effect = [
            response('{"analysis":"missing quote}'),
            response('```json\n{"analysis":"repaired"}\n```'),
        ]
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = OllamaClient("http://ollama.test", "model").ask_json("analyze")
        self.assertEqual(result, {"analysis": "repaired"})
        self.assertEqual(urlopen.call_count, 2)
        second_request = urlopen.call_args_list[1].args[0]
        payload = json.loads(second_request.data)
        self.assertEqual(payload["options"], {"temperature": 0, "num_predict": 32768})
        self.assertIs(payload["think"], False)
        self.assertEqual(len(payload["messages"]), 2)
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertIn("not valid JSON", payload["messages"][-1]["content"])
        self.assertIn('{"analysis":"missing quote}',
                      payload["messages"][-1]["content"])
        self.assertNotIn("analyze", payload["messages"][-1]["content"])
        self.assertIn("đang yêu cầu model sửa", stderr.getvalue())
        self.assertIn("LLM OUTPUT BEGIN", stderr.getvalue())
        self.assertIn("attempt=1/2", stderr.getvalue())
        self.assertIn('{"analysis":"missing quote}', stderr.getvalue())
        self.assertIn('{"analysis":"repaired"}', stderr.getvalue())
        self.assertIn("LLM OUTPUT END", stderr.getvalue())

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_case_json_retry_discards_raw_and_requires_compact_recipe(self, urlopen) -> None:
        oversized_invalid = '{"cases":[{"input":"' + ("2 " * 5000)
        urlopen.side_effect = [
            response(oversized_invalid),
            response('{"cases":[]}'),
        ]

        result = OllamaClient(
            "http://ollama.test", "model", max_output_tokens=32768,
        ).ask_json(
            "ORIGINAL CASE TASK", task_type=TaskType.GENERATE_CASES,
        )

        self.assertEqual(result, {"cases": []})
        second = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertEqual(second["options"]["num_predict"], 32768)
        retry_text = second["messages"][-1]["content"]
        self.assertIn("ORIGINAL CASE TASK", second["messages"][1]["content"])
        self.assertIn("input_parts", retry_text)
        self.assertIn("repeat or numeric sequence", retry_text)
        self.assertIn("predicted_expected", retry_text)
        self.assertIn("at most 256 characters", retry_text)
        self.assertNotIn("2 2 2 2 2 2", retry_text)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_logs_response_label_and_full_content_to_stderr(self, urlopen) -> None:
        urlopen.return_value = response('{"cases":[],"answer":"full response"}')
        stderr = io.StringIO()
        progress = ConsoleProgress()
        with redirect_stderr(stderr):
            result = OllamaClient(
                "http://ollama.test", "gemma-test", progress=progress
            ).ask_json("prompt", label="sinh testcase vòng 2", task_type=TaskType.GENERATE_CASES)
        self.assertEqual(result, {"cases": [], "answer": "full response"})
        logged = stderr.getvalue()
        self.assertIn("sinh testcase vòng 2", logged)
        self.assertIn("model=gemma-test", logged)
        self.assertIn('{"cases":[],"answer":"full response"}', logged)
        components = progress.latency_summary()["components"]
        self.assertEqual(components["ollama.request"]["count"], 1)
        self.assertEqual(components["ollama.parse"]["count"], 1)
        self.assertEqual(components["ollama.output_log"]["count"], 1)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_passes_configured_timeout_to_each_http_request(self, urlopen) -> None:
        urlopen.return_value = response('{"cases":[]}')
        OllamaClient(
            "http://ollama.test", "model", timeout_seconds=37
        ).ask_json("prompt", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES)
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 37)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_enforces_hard_wall_clock_timeout(self, urlopen) -> None:
        release = threading.Event()

        def stalled_request(*args, **kwargs):
            release.wait(2)
            return response('{"cases":[]}')

        urlopen.side_effect = stalled_request
        # No soft-timeout retry budget left, so the first soft timeout is
        # immediately raised for real instead of being retried.
        client = OllamaClient(
            "http://ollama.test", "model", timeout_seconds=1,
            soft_timeout_seconds=1, soft_timeout_budget_seconds=1,
        )
        started = time.monotonic()
        try:
            with self.assertRaisesRegex(TimeoutError, "hard timeout"):
                client.ask_json("prompt", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES)
        finally:
            release.set()
        self.assertLess(time.monotonic() - started, 1.5)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_timeout_does_not_retry_the_same_ollama_endpoint(
        self, urlopen
    ) -> None:
        calls = {"count": 0}
        release = threading.Event()

        def stalled_request(*args, **kwargs):
            calls["count"] += 1
            release.wait(2)
            return response('{"cases":[]}')

        urlopen.side_effect = stalled_request
        progress = ConsoleProgress()
        client = OllamaClient(
            "http://ollama.test", "model",
            timeout_seconds=0.05,
            timeout_cooldown_seconds=1,
            progress=progress,
        )
        try:
            with self.assertRaisesRegex(TimeoutError, "hard timeout"):
                client.ask_json(
                    "prompt", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES
                )
        finally:
            release.set()
        self.assertEqual(calls["count"], 1)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_timeout_does_not_wait_for_buffered_response_close(self, urlopen):
        reading = threading.Event()
        release = threading.Event()

        class BlockedRaw(io.RawIOBase):
            def readable(self):
                return True

            def readinto(self, buffer):
                reading.set()
                release.wait(2)
                return 0

        buffered = io.BufferedReader(BlockedRaw())
        urlopen.return_value = buffered
        client = OllamaClient("http://blocked.test", "model", timeout_seconds=0.1)
        started = time.monotonic()
        try:
            with self.assertRaisesRegex(TimeoutError, "hard timeout"):
                client.ask_json("prompt")
            self.assertTrue(reading.is_set())
            self.assertLess(time.monotonic() - started, 0.6)
        finally:
            release.set()
            buffered.close()

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_ollama_limits_completion_tokens(self, urlopen):
        for label in ("sinh mutant", "sinh baseline theo coverage"):
            with self.subTest(label=label):
                urlopen.return_value = response('{"wrong":[],"cases":[]}')
                OllamaClient(
                    "http://bounded.test", "model", max_output_tokens=2048
                ).ask_json("prompt", label=label)
                payload = json.loads(urlopen.call_args.args[0].data)
                self.assertEqual(payload["options"]["num_predict"], 2048)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_late_response_is_closed_without_reading(self, urlopen):
        release = threading.Event()
        closed = threading.Event()
        reads = []

        class LateResponse(Response):
            def read(self, *args):
                reads.append(True)
                return super().read(*args)

            def close(self):
                super().close()
                closed.set()

        late_response = LateResponse(b'{}')

        def delayed_open(*args, **kwargs):
            release.wait(2)
            return late_response

        urlopen.side_effect = delayed_open
        try:
            with self.assertRaises(TimeoutError):
                OllamaClient(
                    "http://late.test", "model", timeout_seconds=0.05
                ).ask_json("prompt")
        finally:
            release.set()
        self.assertTrue(closed.wait(1))
        self.assertEqual(reads, [])

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_timed_out_endpoint_rejects_second_model_without_queueing(
        self, urlopen
    ) -> None:
        release = threading.Event()
        urlopen.side_effect = lambda *a, **k: (release.wait(5), response("{}"))[1]
        primary = OllamaClient(
            "http://shared-ollama.test", "primary",
            timeout_seconds=0.05,
            timeout_cooldown_seconds=1,
        )
        fallback = OllamaClient(
            "http://shared-ollama.test", "fallback",
            timeout_seconds=0.05,
            timeout_cooldown_seconds=1,
        )
        try:
            with self.assertRaises(TimeoutError):
                primary.ask_json("prompt", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES)
            started = time.monotonic()
            with self.assertRaises(EndpointBusyError):
                fallback.ask_json("prompt", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES)
            self.assertLess(time.monotonic() - started, 0.2)
        finally:
            release.set()
        self.assertEqual(urlopen.call_count, 1)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_repairs_raw_newlines_inside_json_strings_without_model_retry(
        self, urlopen
    ) -> None:
        urlopen.return_value = response(
            '{"code":"line one\nline two","validator":"ok\tvalue"}'
        )
        progress = ConsoleProgress()
        result = OllamaClient(
            "http://ollama.test", "model", progress=progress
        ).ask_json("generate code")
        self.assertEqual(
            result,
            {"code": "line one\nline two", "validator": "ok\tvalue"},
        )
        self.assertEqual(urlopen.call_count, 1)
        parse_events = [
            event for event in progress._latency_events
            if event["component"] == "ollama.parse"
        ]
        self.assertTrue(parse_events[0]["locally_repaired"])

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_repairs_preamble_suffix_and_trailing_comma_without_retry(
        self, urlopen
    ) -> None:
        urlopen.return_value = response(
            'Here is the JSON:\n```json\n{"cases": [{"input": "1\\n",}],}\n```\nDone.'
        )
        result = OllamaClient("http://ollama.test", "model").ask_json(
            "generate", label="sinh testcase vòng 2", task_type=TaskType.GENERATE_CASES
        )
        self.assertEqual(result, {"cases": [{"input": "1\n"}]})
        self.assertEqual(urlopen.call_count, 1)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_wraps_root_array_for_known_task_without_retry(self, urlopen) -> None:
        urlopen.return_value = response('[{"code":"print(0)"}]')
        result = OllamaClient("http://ollama.test", "model").ask_json(
            "generate", label="sinh mutant thay thế vòng 1", task_type=TaskType.GENERATE_MUTANTS
        )
        self.assertEqual(result, {"wrong": [{"code": "print(0)"}]})
        self.assertEqual(urlopen.call_count, 1)

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_retries_valid_json_with_wrong_structure(self, urlopen) -> None:
        urlopen.side_effect = [
            response('{"answer": 1}'),
            response('{"cases": []}'),
        ]
        result = OllamaClient("http://ollama.test", "model").ask_json(
            "generate", label="sinh baseline theo coverage", task_type=TaskType.GENERATE_CASES
        )
        self.assertEqual(result, {"cases": []})
        self.assertEqual(urlopen.call_count, 2)
        payload = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertIn("wrong structure", payload["messages"][-1]["content"])

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_persists_raw_response_for_diagnosis(self, urlopen) -> None:
        urlopen.return_value = response('{"answer": 1}')
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            raw_dir = Path(temp) / "raw"
            result = OllamaClient(
                "http://ollama.test", "model", raw_output_dir=raw_dir
            ).ask_json("prompt")
            self.assertEqual(result, {"answer": 1})
            files = list(raw_dir.glob("*.txt"))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].read_text(encoding="utf-8"), '{"answer": 1}')

    @patch("testgen.ollama.urllib.request.urlopen")
    def test_reports_bounded_failure_without_dumping_full_response(self, urlopen) -> None:
        urlopen.side_effect = [response("{"), response("{")]
        with self.assertRaisesRegex(ValueError, "after 2 attempts"):
            OllamaClient("http://ollama.test", "model").ask_json("analyze")
        self.assertEqual(urlopen.call_count, 2)

    def test_rejects_invalid_attempt_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "json_attempts"):
            OllamaClient("http://ollama.test", "model", json_attempts=0)

    def test_rejects_invalid_timeout(self) -> None:
        with self.assertRaisesRegex(ValueError, "timeout_seconds"):
            OllamaClient("http://ollama.test", "model", timeout_seconds=0)

    def test_regenerated_mutant_preserves_witness_metadata(self) -> None:
        class FakeClient:
            def __init__(self):
                self.label = ""
                self.prompt = ""

            def ask_json(self, prompt, label="Ollama"):
                self.label = label
                self.prompt = prompt
                return {"wrong": [{
                    "language": "Python",
                    "source_code": "print(0)",
                    "strategy_id": "replacement-strategy",
                    "approach": "constant wrong output",
                    "bug_class": "wrong answer",
                    "bug_origin": "intentional",
                    "failure_condition": "correct answer is not zero",
                    "witness_input": "1\n",
                    "parent_ac_id": "reference",
                    "mutation_operator": "replace computed result with zero",
                    "target_behavior": "non-zero result outside public samples",
                    "sample_preservation_reason": "the public sample still prints zero",
                }]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            old_source = output / "old.py"
            old_source.write_text("print(1)", encoding="utf-8")
            reference_source = output / "reference.py"
            reference_source.write_text("print(1)", encoding="utf-8")
            client = FakeClient()
            generator = OllamaSolutionGenerator(client, ac_count=1, wa_count=1)
            replacements = generator.regenerate_wrong(
                "statement", output, 1, [{"reason": "witness passed"}],
                [
                    Solution("reference", "candidate_ac", "Python", reference_source),
                    Solution("old", "candidate_wa", "Python", old_source),
                ], 1,
            )
            self.assertEqual(len(replacements), 1)
            replacement = replacements[0]
            self.assertEqual(replacement.strategy_id, "replacement-strategy")
            self.assertEqual(replacement.failure_condition,
                             "correct answer is not zero")
            self.assertEqual(replacement.witness_input, "1\n")
            self.assertEqual(replacement.parent_ac_id, "reference")
            self.assertEqual(
                replacement.mutation_operator,
                "replace computed result with zero",
            )
            self.assertIn("verified_reference_solutions", client.prompt)
            self.assertIn("mutant thay thế", client.label)
            self.assertTrue((output / "mutant-replacement-01.json").is_file())
            validation = json.loads(
                (output / "mutant-replacement-01-validation.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(validation["accepted"], 1)

    def test_mutant_generation_uses_shortest_reference_in_one_batch(
        self,
    ) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = []
                self.next_index = 1

            def ask_json(self, prompt, label="Ollama"):
                self.calls.append((label, prompt))
                requested = 5
                rows = []
                for _ in range(requested):
                    index = self.next_index
                    self.next_index += 1
                    rows.append({
                        "language": "Python",
                        "code": f"print({index})",
                        "strategy_id": f"strategy-{index}",
                        "approach": f"mutation {index}",
                        "bug_class": "wrong answer",
                        "bug_origin": "intentional",
                        "failure_condition": f"condition-{index}",
                        "witness_input": f"{index}\n",
                        "parent_ac_id": "short-reference",
                        "mutation_operator": f"operator-{index}",
                        "target_behavior": f"target-{index}",
                        "sample_preservation_reason": "samples preserved",
                    })
                return {"wrong": rows}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            short_source = output / "short.py"
            short_source.write_text("SHORT_REFERENCE_MARKER", encoding="utf-8")
            long_source = output / "long.py"
            long_source.write_text("LONG_REFERENCE_MARKER" * 1000, encoding="utf-8")
            client = FakeClient()
            replacements = OllamaSolutionGenerator(
                client, ac_count=2, wa_count=5
            ).regenerate_wrong(
                "statement",
                output,
                5,
                [],
                [
                    Solution(
                        "long-reference", "candidate_ac", "Python", long_source
                    ),
                    Solution(
                        "short-reference", "candidate_ac", "Python", short_source
                    ),
                ],
                0,
            )
            self.assertEqual(len(client.calls), 1)
            self.assertEqual(len(replacements), 5)
            self.assertEqual(len({solution.id for solution in replacements}), 5)
            prompt = client.calls[0][1]
            self.assertIn("SHORT_REFERENCE_MARKER", prompt)
            self.assertNotIn("LONG_REFERENCE_MARKER", prompt)
            self.assertIn("exactly 7 NEW items", prompt)
            self.assertTrue((output / "mutant-initial.json").is_file())
            self.assertTrue((output / "mutant-initial-validation.json").is_file())

    def test_mutant_requests_continue_after_an_empty_model_response(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = 0

            def ask_json(self, prompt, label="Ollama"):
                self.calls += 1
                return {"wrong": []}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            reference = output / "reference.py"
            reference.write_text("print(1)", encoding="utf-8")
            client = FakeClient()
            replacements = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=5
            ).regenerate_wrong(
                "statement",
                output,
                5,
                [],
                [Solution("reference", "candidate_ac", "Python", reference)],
                0,
            )
            self.assertEqual(replacements, [])
            # One batch request plus one follow-up request for the still-missing
            # quota; a single prompt no longer loops per-mutant.
            self.assertEqual(client.calls, 2)

    def test_mutant_batch_validation_drops_duplicate_sources(self) -> None:
        class FakeClient:
            def __init__(self):
                self.prompts = []

            def ask_json(self, prompt, label="Ollama"):
                self.prompts.append(prompt)
                codes = ["print(10)", "print(10)", "print(11)"]
                return {"wrong": [{
                    "language": "Python",
                    "code": code,
                    "strategy_id": f"strategy-{index}",
                    "approach": "real mutation",
                    "bug_class": "wrong answer",
                    "bug_origin": "intentional",
                    "failure_condition": f"condition-{index}",
                    "witness_input": f"{index}\n",
                    "parent_ac_id": "reference",
                    "mutation_operator": f"operator-{index}",
                    "target_behavior": f"target-{index}",
                    "sample_preservation_reason": "sample preserved",
                } for index, code in enumerate(codes, 1)]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            reference = output / "reference.py"
            reference.write_text("print(1)", encoding="utf-8")
            client = FakeClient()
            replacements = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=3
            ).regenerate_wrong(
                "statement", output, 3, [],
                [Solution("reference", "candidate_ac", "Python", reference)],
                0,
            )
            # The fake client always returns the same 3 fixed rows regardless of
            # how many were requested, so one duplicate is dropped and the
            # generator issues one follow-up request for the still-missing slot.
            self.assertEqual(len(client.prompts), 2)
            self.assertEqual(len(replacements), 2)
            validation = json.loads(
                (output / "mutant-initial-validation.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertIn(
                "duplicate source code",
                validation["items"][1]["issues"],
            )

    def test_python_mutant_fingerprint_ignores_comment_only_changes(self) -> None:
        generator = OllamaSolutionGenerator(
            object(), ac_count=1, wa_count=1
        )
        self.assertEqual(
            generator._fingerprint("Python", "x = 1\n"),
            generator._fingerprint("Python", "# mutation\nx = 1  # unchanged\n"),
        )

    def test_initial_generation_defers_wrong_candidates_until_ac_is_verified(self) -> None:
        class FakeClient:
            def __init__(self):
                self.generation_prompt = ""

            def ask_json(self, prompt, label="Ollama"):
                if "phân tích" in label:
                    return {
                        "correct_strategies": [],
                        "wrong_strategies": [],
                        "warnings": [],
                    }
                if "validator" not in label:
                    self.generation_prompt = prompt
                return {
                    "correct": [{
                        "language": "Python",
                        "code": "print(1)",
                        "strategy_id": "reference",
                        "approach": "direct",
                        "time_complexity": "O(1)",
                        "space_complexity": "O(1)",
                    }],
                    "wrong": [],
                    "validator_python": "raise SystemExit(0)",
                    "warnings": [],
                }

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            client = FakeClient()
            generator = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=2, max_rounds=1
            )
            solutions = generator.generate("statement", Path(temp))
            self.assertEqual([solution.label for solution in solutions], ["candidate_ac"])
            self.assertEqual(generator.requested_wrong_candidates(), 2)
            self.assertIn("wrong must be []", client.generation_prompt)

    def test_initial_generation_normalizes_languages_and_fills_metadata(self) -> None:
        class FakeClient:
            def ask_json(self, prompt, label="Ollama"):
                return {
                    "correct": [
                        {"language": "cpp", "code": "int main(){}"},
                        {"language": "python", "code": "print(1)"},
                        {"language": "java", "code": "class Main {}"},
                    ],
                    "wrong": [],
                    "validator_python": "raise SystemExit(0)",
                    "warnings": [],
                }

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            solutions = OllamaSolutionGenerator(
                FakeClient(), ac_count=3, wa_count=0, max_rounds=1
            ).generate("statement", Path(temp))
            self.assertEqual(
                [solution.language for solution in solutions],
                ["C++", "Python", "Java"],
            )
            generation = json.loads(
                (Path(temp) / "generation.json").read_text(encoding="utf-8")
            )
            for row in generation["correct"]:
                self.assertTrue(row["strategy_id"])
                self.assertTrue(row["approach"])
                self.assertTrue(row["time_complexity"])
                self.assertTrue(row["space_complexity"])

    def test_initial_generation_reuses_pipeline_test_model(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = []

            def ask_json(self, prompt, label="Ollama"):
                self.calls.append((label, prompt))
                return {
                    "correct": [{
                        "language": "Python",
                        "code": "print(1)",
                        "strategy_id": "reference",
                        "approach": "direct",
                        "time_complexity": "O(1)",
                        "space_complexity": "O(1)",
                    }],
                    "wrong": [],
                    "validator_python": "raise SystemExit(0)",
                    "warnings": [],
                }

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            run_output = Path(temp)
            generated = run_output / "generated"
            (run_output / "test-model.json").write_text(
                json.dumps({"marker": "reuse-me", "warnings": []}),
                encoding="utf-8",
            )
            client = FakeClient()
            solutions = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=0, max_rounds=1
            ).generate_with_model("statement", {"marker": "reuse-me", "warnings": []}, generated)
            self.assertEqual(len(solutions), 1)
            self.assertEqual(len(client.calls), 2)
            self.assertNotIn("phân tích", client.calls[0][0])
            self.assertNotIn("reuse-me", client.calls[0][1])
            saved_analysis = json.loads(
                (generated / "analysis.json").read_text(encoding="utf-8")
            )
            self.assertEqual(saved_analysis["analysis_source"],
                             "pipeline_test_model")

    def test_missing_validator_uses_small_validator_only_follow_up(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = []

            def ask_json(self, prompt, label="Ollama"):
                self.calls.append((label, prompt))
                if "phân tích" in label:
                    return {
                        "correct_strategies": [],
                        "wrong_strategies": [],
                        "warnings": [],
                    }
                if "validator" in label:
                    return {
                        "validator_python": "raise SystemExit(0)",
                        "warnings": [],
                    }
                return {
                    "correct": [{
                        "language": "Python",
                        "code": "print('large accepted source')",
                        "strategy_id": "reference",
                        "approach": "direct",
                        "time_complexity": "O(1)",
                        "space_complexity": "O(1)",
                    }],
                    "wrong": [],
                    "validator_python": "",
                    "warnings": [],
                }

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            client = FakeClient()
            analysis_client = FakeClient()
            generator = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=0, max_rounds=2,
                analysis_client=analysis_client,
            )
            solutions = generator.generate("statement", Path(temp))
            self.assertEqual(len(solutions), 1)
            self.assertFalse(any("validator" in label for label, _ in client.calls))
            validator_calls = [
                (label, prompt) for label, prompt in analysis_client.calls
                if "validator" in label
            ]
            self.assertEqual(len(validator_calls), 1)
            label, prompt = validator_calls[0]
            self.assertIn("sinh validator", label)
            self.assertNotIn("large accepted source", prompt)
            self.assertNotIn("accepted_candidates", prompt)
            self.assertTrue((Path(temp) / "validator-round-01.json").is_file())

    def test_invalid_validator_syntax_uses_validator_only_follow_up(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = []
                self.validator_calls = 0

            def ask_json(self, prompt, label="Ollama"):
                self.calls.append((label, prompt))
                if "phân tích" in label:
                    return {
                        "correct_strategies": [],
                        "wrong_strategies": [],
                        "warnings": [],
                    }
                if "validator" in label:
                    self.validator_calls += 1
                    return {
                        "validator_python": (
                            "except Exception:\n    pass\n"
                            if self.validator_calls == 1
                            else "raise SystemExit(0)"
                        ),
                        "warnings": [],
                    }
                return {
                    "correct": [{
                        "language": "Python",
                        "code": "print(1)",
                        "strategy_id": "reference",
                        "approach": "direct",
                        "time_complexity": "O(1)",
                        "space_complexity": "O(1)",
                    }],
                    "wrong": [],
                    "validator_python": "",
                    "warnings": [],
                }

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            client = FakeClient()
            generator = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=0, max_rounds=2
            )
            solutions = generator.generate("statement", Path(temp))

            self.assertEqual(len(solutions), 1)
            generation_calls = [
                call for call in client.calls if "phân tích" not in call[0]
            ]
            self.assertEqual(len(generation_calls), 3)
            label, prompt = generation_calls[2]
            self.assertIn("sinh validator", label)
            self.assertIn("not valid Python 3", prompt)
            self.assertEqual(
                (Path(temp) / "validator.py").read_text(encoding="utf-8"),
                "raise SystemExit(0)",
            )

    def test_mutant_generation_does_not_reject_a_reused_witness(self) -> None:
        class FakeClient:
            def ask_json(self, prompt, label="Ollama"):
                return {"wrong": [{
                    "language": "Python",
                    "code": "print(0)",
                    "strategy_id": "new-strategy",
                    "approach": "new mutation",
                    "bug_class": "wrong answer",
                    "bug_origin": "intentional",
                    "failure_condition": "new condition",
                    "witness_input": "same input\n",
                    "parent_ac_id": "reference",
                    "mutation_operator": "new operator",
                    "target_behavior": "new target",
                    "sample_preservation_reason": "sample preserved",
                }]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            reference = output / "reference.py"
            reference.write_text("print(1)", encoding="utf-8")
            old = output / "old.py"
            old.write_text("print(2)", encoding="utf-8")
            generator = OllamaSolutionGenerator(
                FakeClient(), ac_count=1, wa_count=1
            )
            replacements = generator.regenerate_wrong(
                "statement", output, 1, [], [
                    Solution("reference", "candidate_ac", "Python", reference),
                    Solution(
                        "old", "candidate_wa", "Python", old,
                        failure_condition="old condition",
                        witness_input="same input\n",
                        mutation_operator="old operator",
                        target_behavior="old target",
                    ),
                ], 1,
            )
            self.assertEqual(len(replacements), 1)
            self.assertEqual(replacements[0].witness_input, "same input\n")

    def test_regenerates_reference_from_compile_failure(self) -> None:
        class FakeClient:
            def __init__(self):
                self.prompt = ""

            def ask_json(self, prompt, label="Ollama"):
                self.prompt = prompt
                return {"correct": [{
                    "language": "python",
                    "code": "print(1)",
                }]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            failed_source = output / "failed.cpp"
            failed_source.write_text("broken", encoding="utf-8")
            client = FakeClient()
            replacements = OllamaSolutionGenerator(
                client, ac_count=3, wa_count=0
            ).regenerate_correct(
                "statement",
                output,
                1,
                [{
                    "solution_id": "correct-01",
                    "compile_verdict": "CE",
                    "compile_stderr": "missing closing brace",
                    "official_samples": [],
                }],
                [Solution(
                    "correct-01", "candidate_ac", "C++", failed_source,
                )],
                1,
            )
            self.assertEqual(len(replacements), 1)
            self.assertEqual(replacements[0].language, "Python")
            self.assertEqual(replacements[0].id, "correct-replacement-r1-01")
            self.assertIn("missing closing brace", client.prompt)
            self.assertTrue(
                (output / "reference-replacement-01-validation.json").is_file()
            )

    def test_generates_multiple_repaired_witnesses_and_deduplicates_them(self) -> None:
        class FakeClient:
            def __init__(self):
                self.prompt = ""

            def ask_json(self, prompt, label="Ollama"):
                self.prompt = prompt
                return {"witnesses": [{
                    "solution_id": "wa1",
                    "candidates": [
                        {"input": "old\n", "reasoning": "already tried"},
                        {"input": "new 1\n", "reasoning": "boundary"},
                        {"input": "new 1\n", "reasoning": "duplicate"},
                        {"input": "new 2\n", "reasoning": "near boundary"},
                    ],
                }]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            ac_source = output / "ac.py"
            ac_source.write_text("print(1)", encoding="utf-8")
            wa_source = output / "wa.py"
            wa_source.write_text("print(2)", encoding="utf-8")
            ac = Solution("ac1", "candidate_ac", "Python", ac_source)
            wa = Solution(
                "wa1", "candidate_wa", "Python", wa_source,
                witness_input="old\n", parent_ac_id="ac1",
                failure_condition="boundary",
            )
            client = FakeClient()
            generated = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=1
            ).generate_mutant_witnesses(
                "statement", output, [wa], [ac],
                {"wa1": {"witness_input": "old\n", "witness_attempts": []}},
                attempt=1, candidates_per_mutant=3,
            )
            self.assertEqual(generated, {"wa1": ["new 1\n"]})
            self.assertIn("Do NOT write or modify program source code", client.prompt)
            self.assertTrue(
                (output / "mutant-witness-repair-a01-b01-wa1.json").is_file()
            )

    def test_witness_repair_sends_one_batch_per_repair_mode(self) -> None:
        class FakeClient:
            def __init__(self):
                self.prompts = []

            def ask_json(self, prompt, label="Ollama"):
                self.prompts.append(prompt)
                ids = [
                    solution_id for solution_id in ("wa1", "wa2", "wa3")
                    if f'"solution_id": "{solution_id}"' in prompt
                ]
                return {"witnesses": [
                    {
                        "solution_id": solution_id,
                        "candidates": [
                            {"input": f"{solution_id}-a\n", "reasoning": "a"},
                            {"input": f"{solution_id}-b\n", "reasoning": "b"},
                        ],
                    }
                    for solution_id in ids
                ]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            parent_source = output / "parent.py"
            parent_source.write_text("PARENT_SOURCE_MARKER", encoding="utf-8")
            parent = Solution(
                "ac1", "candidate_ac", "Python", parent_source
            )
            mutants = []
            evidence = {}
            for index in range(1, 4):
                source = output / f"wa{index}.py"
                source.write_text(f"MUTANT_{index}", encoding="utf-8")
                solution = Solution(
                    f"wa{index}", "candidate_wa", "Python", source,
                    parent_ac_id="ac1",
                )
                mutants.append(solution)
                evidence[solution.id] = {"witness_attempts": []}
            client = FakeClient()
            code_client = FakeClient()
            proposals = OllamaSolutionGenerator(
                code_client, ac_count=1, wa_count=3, analysis_client=client
            ).generate_mutant_witnesses(
                "statement", output, mutants, [parent], evidence,
                attempt=1, candidates_per_mutant=4,
            )
            self.assertEqual(len(client.prompts), 1)
            self.assertEqual(code_client.prompts, [])
            self.assertEqual(set(proposals), {"wa1", "wa2", "wa3"})
            self.assertTrue(all(len(values) == 1 for values in proposals.values()))
            prompt = client.prompts[0]
            self.assertIn("PARENT_SOURCE_MARKER", prompt)
            self.assertEqual(
                sum(f'"solution_id": "wa{index}"' in prompt
                    for index in range(1, 4)),
                3,
            )

    def test_validator_rejected_witness_uses_small_format_only_prompt(self) -> None:
        class FakeClient:
            def __init__(self):
                self.prompt = ""

            def ask_json(self, prompt, label="Ollama"):
                self.prompt = prompt
                return {"witnesses": [{
                    "solution_id": "wa1",
                    "candidates": [{
                        "input": "1\n1 1\n1 2 3\n",
                        "reasoning": "add missing test count",
                    }],
                }]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            parent_source = output / "parent.py"
            parent_source.write_text("PARENT_SOURCE_MARKER", encoding="utf-8")
            mutant_source = output / "wa.py"
            mutant_source.write_text("MUTANT_SOURCE_MARKER", encoding="utf-8")
            client = FakeClient()
            proposals = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=1
            ).generate_mutant_witnesses(
                "## Input\nFirst t, then n k.\n\n## Output\nAnswer.\n",
                output,
                [Solution(
                    "wa1", "candidate_wa", "Python", mutant_source,
                    witness_input="1 1\n1 2 3\n", parent_ac_id="ac1",
                    failure_condition="boundary",
                )],
                [Solution("ac1", "candidate_ac", "Python", parent_source)],
                {"wa1": {
                    "reason": "witness rejected by validator",
                    "witness_input": "1 1\n1 2 3\n",
                    "validator_verdict": "RE",
                    "witness_attempts": [],
                }},
                attempt=1,
                candidates_per_mutant=2,
            )
            self.assertEqual(proposals, {"wa1": ["1\n1 1\n1 2 3\n"]})
            self.assertIn("Repair only the stdin framing/format", client.prompt)
            self.assertIn("First t, then n k.", client.prompt)
            self.assertNotIn("PARENT_SOURCE_MARKER", client.prompt)
            self.assertNotIn("MUTANT_SOURCE_MARKER", client.prompt)

    def test_witness_batches_stop_after_empty_response(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = 0

            def ask_json(self, prompt, label="Ollama"):
                self.calls += 1
                return {"witnesses": []}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            parent_source = output / "parent.py"
            parent_source.write_text("print(1)", encoding="utf-8")
            parent = Solution("ac1", "candidate_ac", "Python", parent_source)
            mutants = []
            for index in range(3):
                source = output / f"wa{index}.py"
                source.write_text("print(0)", encoding="utf-8")
                mutants.append(Solution(
                    f"wa{index}", "candidate_wa", "Python", source,
                    parent_ac_id="ac1",
                ))
            client = FakeClient()
            proposals = OllamaSolutionGenerator(
                client, ac_count=1, wa_count=3
            ).generate_mutant_witnesses(
                "statement", output, mutants, [parent], {}, 1, 2
            )
            self.assertEqual(proposals, {})
            self.assertEqual(client.calls, 1)

    def test_repairs_validator_rejections_in_one_batch(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = 0
                self.prompt = ""

            def ask_json(self, prompt, label="Ollama"):
                self.calls += 1
                self.prompt = prompt
                return {"repairs": [
                    {
                        "proposal_index": 4,
                        "input": "1 2\n",
                        "family": "repaired",
                        "coverage_tags": [],
                    },
                    {
                        "proposal_index": 7,
                        "input": "2 3\n",
                        "family": "repaired",
                        "coverage_tags": [],
                    },
                ]}

        client = FakeClient()
        repaired = OllamaCaseGenerator(client).repair_batch(
            "statement",
            {"test_model": {}},
            [
                {"proposal_index": 4, "input": "bad one\n"},
                {"proposal_index": 7, "input": "bad two\n"},
            ],
            attempt=1,
        )
        self.assertEqual(client.calls, 1)
        self.assertEqual([row["proposal_index"] for row in repaired], [4, 7])
        self.assertIn("<rejected_cases>", client.prompt)

    def test_repair_batch_does_not_include_candidate_sources(self) -> None:
        class FakeClient:
            def __init__(self):
                self.prompts = []

            def ask_json(self, prompt, label="Ollama"):
                self.prompts.append(prompt)
                indices = [
                    index for index in range(1, 7)
                    if f'"proposal_index": {index}' in prompt
                ]
                return {"repairs": [
                    {
                        "proposal_index": index,
                        "input": f"{index}\n",
                        "family": "repaired",
                        "coverage_tags": [],
                    }
                    for index in indices
                ]}

        client = FakeClient()
        feedback = {
            "surviving_wrong_candidates": [{
                "id": "wa1", "source_code": "SOURCE_MUST_NOT_BE_SENT",
                "attempts": [],
            }],
            "test_model": {},
        }
        repaired = OllamaCaseGenerator(client).repair_batch(
            "statement",
            feedback,
            [
                {"proposal_index": index, "input": "bad\n"}
                for index in range(1, 7)
            ],
            attempt=1,
        )
        self.assertEqual(len(client.prompts), 1)
        self.assertEqual(len(repaired), 6)
        self.assertTrue(all(
            "SOURCE_MUST_NOT_BE_SENT" not in prompt
            for prompt in client.prompts
        ))

    def test_adaptive_prompt_keeps_only_recent_attempts_and_ten_cases(self) -> None:
        class FakeClient:
            prompt = ""

            def __init__(self):
                self.calls = 0

            def ask_json(self, prompt, label="Ollama"):
                self.calls += 1
                self.prompt = prompt
                return {
                    "requested_count": 10,
                    "rationale": "many",
                    "cases": [{
                        "input": f"{index}\n",
                        "family": "f",
                        "coverage_tags": [],
                    } for index in range(1, 11)],
                }

        client = FakeClient()
        plan = OllamaCaseGenerator(client).generate(
            "statement",
            {
                "test_model": {},
                "surviving_wrong_candidates": [{
                    "id": "wa1",
                    "source_code": "SURVIVOR_SOURCE",
                    "attempts": [
                        {"lesson": f"attempt-{index}"} for index in range(10)
                    ],
                }],
                "experiment_history": {
                    "certified_tests": [{
                        "id": "old", "input": "1\n",
                        "expected": "EXPECTED_SECRET",
                    }],
                    "rejected_tests": [],
                },
            },
            iteration=1,
            min_cases=10,
            max_cases=30,
        )
        self.assertEqual(plan["requested_count"], 10)
        self.assertEqual(len(plan["cases"]), 10)
        self.assertNotIn("SURVIVOR_SOURCE", client.prompt)
        self.assertNotIn("attempt-7", client.prompt)
        self.assertIn("attempt-8", client.prompt)
        self.assertNotIn("EXPECTED_SECRET", client.prompt)

    def test_survivor_audit_returns_structured_classification(self) -> None:
        class FakeClient:
            prompt = ""

            def ask_json(self, prompt, label="Ollama"):
                self.prompt = prompt
                return {
                    "classification": "likely_equivalent",
                    "revised_bug_hypothesis": "none",
                    "reasoning": "prior prediction was disproved",
                    "confidence": 0.9,
                    "failed_hypotheses": ["zero score"],
                    "counterexample": None,
                }

        client = FakeClient()
        audit = OllamaCaseGenerator(client).audit(
            "statement",
            {"id": "wrong-08", "attempts": [{"lesson": "prediction failed"}]},
            1,
        )
        self.assertEqual(audit["classification"], "likely_equivalent")
        self.assertEqual(audit["confidence"], 0.9)
        self.assertIn("prediction failed", client.prompt)
        self.assertIn("CodeNet oracle", client.prompt)

    def test_survivor_audits_are_sent_in_one_batch(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = 0
                self.label = ""

            def ask_json(self, prompt, label="Ollama"):
                self.calls += 1
                self.label = label
                return {"audits": [
                    {
                        "solution_id": "wrong-01",
                        "classification": "counterexample_found",
                        "confidence": 0.8,
                        "counterexample": {"input": "1\n"},
                    },
                    {
                        "solution_id": "wrong-02",
                        "classification": "likely_equivalent",
                        "confidence": 0.6,
                        "counterexample": None,
                    },
                ]}

        client = FakeClient()
        audits = OllamaCaseGenerator(client).audit_batch(
            "statement",
            [{"id": "wrong-01"}, {"id": "wrong-02"}],
            1,
        )
        self.assertEqual(client.calls, 1)
        self.assertEqual(len(audits), 2)
        self.assertEqual(audits[0]["solution_id"], "wrong-01")
        self.assertIn("audit batch survivor (2 item)", client.label)

    def test_survivor_audits_batch_and_trim_old_attempts(self) -> None:
        class FakeClient:
            def __init__(self):
                self.prompts = []

            def ask_json(self, prompt, label="Ollama"):
                self.prompts.append(prompt)
                ids = [
                    solution_id for solution_id in ("wrong-01", "wrong-02", "wrong-03")
                    if f'"id": "{solution_id}"' in prompt
                ]
                return {"audits": [
                    {
                        "solution_id": solution_id,
                        "classification": "insufficient_evidence",
                        "confidence": 0.1,
                    }
                    for solution_id in ids
                ]}

        client = FakeClient()
        contexts = [
            {
                "id": f"wrong-0{index}",
                "source_code": f"SOURCE_{index}",
                "attempts": [
                    {"lesson": f"candidate-{index}-attempt-{attempt}"}
                    for attempt in range(10)
                ],
            }
            for index in range(1, 4)
        ]
        audits = OllamaCaseGenerator(client).audit_batch(
            "statement", contexts, 1
        )
        self.assertEqual(len(client.prompts), 1)
        self.assertEqual(len(audits), 3)
        self.assertNotIn("candidate-1-attempt-7", client.prompts[0])
        self.assertIn("candidate-1-attempt-8", client.prompts[0])


if __name__ == "__main__":
    unittest.main()
