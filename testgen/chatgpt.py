"""ChatGPT-authenticated Codex CLI JSON client."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

from pydantic import BaseModel
from .llm_contract import LLMRequest, TaskType, SHAPES, LLMResponseError, LLMTransportError

from .infrastructure.llm.ollama import _parse_json_locally
from .progress import ConsoleProgress
from .throttle import default_prompt_throttle


class ChatGPTClient:
    """Use the installed Codex CLI and its existing ChatGPT login."""

    def __init__(
        self,
        executable: str | Path | None = None,
        *,
        model: str = "gpt-5.6-sol",
        timeout_seconds: int = 600,
        json_attempts: int = 2,
        progress: ConsoleProgress | None = None,
        raw_output_dir: Path | None = None,
    ):
        if timeout_seconds < 1:
            raise ValueError("timeout_seconds must be >= 1")
        if json_attempts < 1:
            raise ValueError("json_attempts must be >= 1")
        if not model.strip():
            raise ValueError("model must not be empty")
        resolved = str(executable) if executable else shutil.which("codex")
        if not resolved:
            raise RuntimeError(
                "Codex CLI was not found. Install/login to Codex or select "
                "the Ollama backend."
            )
        self.executable = resolved
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.json_attempts = json_attempts
        self.progress = progress
        self.raw_output_dir = raw_output_dir
        self._raw_output_lock = threading.Lock()
        self._raw_output_counter = 0

    @staticmethod
    def _schema() -> dict:
        """Constrain only a tiny transport envelope, not the task payload.

        OpenAI strict schemas require closed objects.  Describing every task
        field here makes generation brittle and duplicates the prompt/local
        validation contract.  Instead, Structured Outputs guarantees one
        string containing the task JSON; the existing parser validates that
        inner object and can ask the model to repair it.
        """
        return {
            "type": "object",
            "properties": {
                "payload_json": {
                    "type": "string",
                    "description": (
                        "The complete task response encoded as a JSON object "
                        "string, with no Markdown fences."
                    ),
                },
            },
            "required": ["payload_json"],
            "additionalProperties": False,
        }

    @staticmethod
    def _wrap_prompt(prompt: str) -> str:
        return (
            prompt
            + "\n\nTRANSPORT REQUIREMENT:\n"
            + "Produce the requested JSON object normally, then serialize that "
            + "complete object as the string value of `payload_json`. The outer "
            + "response is handled by a strict transport schema. Do not omit "
            + "fields requested by the task and do not add Markdown fences."
        )

    def _save_raw_output(self, raw: str, label: str, attempt: int) -> str | None:
        if self.raw_output_dir is None:
            return None
        safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "-", label).strip("-")[:80]
        with self._raw_output_lock:
            self._raw_output_counter += 1
            counter = self._raw_output_counter
            self.raw_output_dir.mkdir(parents=True, exist_ok=True)
            path = self.raw_output_dir / (
                f"{counter:04d}-{safe_label or 'chatgpt'}-attempt-{attempt}.txt"
            )
            path.write_text(raw, encoding="utf-8")
        return str(path)

    def ask(self, request: LLMRequest) -> dict:
        return self.ask_json(request.prompt, request.label, request.response_model,
                             task_type=request.task_type)

    def ask_json(
        self,
        prompt: str,
        label: str = "ChatGPT",
        response_model: type[BaseModel] | None = None,
        *, task_type: TaskType = TaskType.GENERIC,
    ) -> dict:
        schema_instruction = ""
        if response_model is not None:
            schema_instruction = (
                "\n\nThe inner task payload must conform to this JSON Schema:\n"
                + json.dumps(
                    response_model.model_json_schema(),
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        current_prompt = prompt + schema_instruction
        expected_shape = SHAPES.get(task_type, {})
        last_error: Exception | None = None
        for attempt in range(1, self.json_attempts + 1):
            default_prompt_throttle.wait()
            request_started = time.monotonic()
            try:
                with tempfile.TemporaryDirectory(prefix="testgen-chatgpt-") as temp:
                    temp_dir = Path(temp)
                    schema_path = temp_dir / "output-schema.json"
                    result_path = temp_dir / "result.json"
                    schema = self._schema()
                    schema_path.write_text(
                        json.dumps(schema, ensure_ascii=False),
                        encoding="utf-8",
                    )
                    args = [
                        self.executable,
                        "exec",
                        "--ephemeral",
                        "--ignore-user-config",
                        "--ignore-rules",
                        "--skip-git-repo-check",
                        "--sandbox", "read-only",
                        "--model", self.model,
                        "--cd", str(temp_dir),
                        "--output-schema", str(schema_path),
                        "--output-last-message", str(result_path),
                        "-",
                    ]
                    completed = subprocess.run(
                        args,
                        input=self._wrap_prompt(current_prompt),
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        capture_output=True,
                        timeout=self.timeout_seconds,
                        check=False,
                    )
                    if completed.returncode != 0:
                        detail = (completed.stderr or completed.stdout).strip()[-2000:]
                        raise LLMTransportError(
                            f"Codex CLI exited {completed.returncode}: {detail}"
                        )
                    if not result_path.is_file():
                        raise LLMTransportError("Codex CLI did not write its final response")
                    raw = result_path.read_text(encoding="utf-8").strip()
            except (OSError, subprocess.TimeoutExpired, RuntimeError) as error:
                if self.progress:
                    self.progress.latency(
                        "chatgpt.request", time.monotonic() - request_started,
                        status="error", label=label, model=self.model,
                        attempt=attempt, request_chars=len(current_prompt),
                        error=type(error).__name__,
                    )
                raise LLMTransportError(f"ChatGPT request failed: {error}") from error

            raw_output_path = self._save_raw_output(raw, label, attempt)
            if self.progress:
                self.progress.latency(
                    "chatgpt.request", time.monotonic() - request_started,
                    label=label, model=self.model, attempt=attempt,
                    request_chars=len(current_prompt), response_chars=len(raw),
                    raw_output=raw_output_path,
                )
            try:
                envelope, envelope_repair_mode = _parse_json_locally(raw)
                if not isinstance(envelope, dict):
                    raise ValueError("ChatGPT transport response must be an object")
                payload = envelope.get("payload_json")
                if not isinstance(payload, str):
                    raise ValueError(
                        "ChatGPT transport response is missing string payload_json"
                    )
                result, payload_repair_mode = _parse_json_locally(payload)
                if not isinstance(result, dict):
                    raise ValueError("ChatGPT JSON response must be an object")
                missing = [key for key in expected_shape if key not in result]
                wrong_types = [
                    key for key, kind in expected_shape.items()
                    if key in result and not isinstance(result[key], kind)
                ]
                if missing or wrong_types:
                    raise ValueError(
                        "wrong JSON structure; missing=" + repr(missing)
                        + ", wrong_types=" + repr(wrong_types)
                    )
                if response_model is not None:
                    result = response_model.model_validate(result).model_dump(
                        mode="json"
                    )
                if self.progress:
                    repair_mode = (
                        payload_repair_mode
                        if envelope_repair_mode == "exact"
                        else f"envelope:{envelope_repair_mode};payload:{payload_repair_mode}"
                    )
                    self.progress.latency(
                        "chatgpt.parse", 0.0, label=label, attempt=attempt,
                        valid=True, locally_repaired=repair_mode != "exact",
                        repair_mode=repair_mode,
                    )
                return result
            except (json.JSONDecodeError, ValueError) as error:
                last_error = error
                if self.progress:
                    self.progress.latency(
                        "chatgpt.parse", 0.0, status="invalid_json",
                        label=label, attempt=attempt, valid=False,
                        error=type(error).__name__,
                    )
                if attempt == self.json_attempts:
                    raise LLMResponseError(
                        f"ChatGPT returned invalid JSON after {attempt} attempts: {error}"
                    ) from error
                current_prompt = (
                    "Repair the response below. Return one complete JSON object "
                    "matching the original requested structure, with no Markdown.\n"
                    f"Parser error: {error}\n<invalid_json>\n{raw}\n</invalid_json>"
                    + schema_instruction
                )
        raise AssertionError(f"unreachable: {last_error}")
