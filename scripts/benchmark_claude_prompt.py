"""Replay one reconstructed first-AC prompt and preserve timing evidence."""
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from testgen.claude import ClaudeClient
from testgen.ollama import OllamaSolutionGenerator


class Captured(BaseException):
    pass


class Capture:
    def ask_json(self, prompt, label=""):
        self.prompt, self.label = prompt, label
        raise Captured()


def main():
    source = ROOT / "output/batches/20261011-235022/problems/p02732"
    output = ROOT / "output/claude-prompt-benchmark" / time.strftime("%Y%m%d-%H%M%S")
    output.mkdir(parents=True)
    shutil.copyfile(source / "test-model.json", output / "test-model.json")
    capture = Capture()
    try:
        OllamaSolutionGenerator(capture, ac_count=3, wa_count=5).generate(
            (source / "statement.md").read_text(encoding="utf-8"), output / "generated"
        )
    except Captured:
        pass
    (output / "prompt.txt").write_text(capture.prompt, encoding="utf-8")
    original = next(json.loads(line) for line in (source / "latency.jsonl").read_text(encoding="utf-8").splitlines()
                    if json.loads(line)["component"] == "claude.request")
    report = {"source_run": str(source), "label": capture.label,
              "prompt_chars": len(capture.prompt), "original_request_chars": original["request_chars"],
              "original_seconds": original["duration_ms"] / 1000,
              "model": "fable", "effort": "low", "max_output_tokens": 32768, "timeout_seconds": 300}
    client = ClaudeClient(model="fable", effort="low", max_output_tokens=32768, timeout_seconds=300, json_attempts=1)
    run_cli = client._run_cli
    def measured(args, prompt):
        started = time.monotonic()
        completed = run_cli(args, prompt)
        report["cli_seconds"] = round(time.monotonic() - started, 3)
        (output / "cli-output.json").write_text(completed.stdout, encoding="utf-8")
        return completed
    client._run_cli = measured
    started = time.monotonic()
    try:
        response = client.ask_json(capture.prompt, label=capture.label)
        report.update(status="ok", correct_count=len(response.get("correct", [])))
        (output / "response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as error:
        report.update(status="error", error=str(error))
    report["wall_seconds"] = round(time.monotonic() - started, 3)
    (output / "benchmark.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2), flush=True)
    print(str(output), flush=True)


if __name__ == "__main__":
    main()
