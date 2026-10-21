from pathlib import Path

import pytest

from testgen.application.run_pipeline import RunPipeline
from testgen.checker import checker_from_profile
from testgen.checkers.generated_python import (
    GeneratedCheckerSafetyError,
    strip_unused_imports,
    validate_generated_checker_source,
)
from testgen.domain import CaseGenerator, Judge, Result, SolutionGenerator


SAFE_CHECKER = """
def accepts(input_text, actual, expected):
    try:
        parts = actual.split()
        return len(parts) == 1 and parts[0] in ("YES", "OK")
    except Exception:
        return False
"""


class _Solutions(SolutionGenerator):
    def generate(self, statement, output):
        return []


class _Judge(Judge):
    def compile(self, solution):
        return Result(solution.id, "PASS")

    def execute(self, solution, case_id, input_text):
        return Result(solution.id, "PASS", case_id, "")


class _CheckerCases(CaseGenerator):
    cases_per_round = 1

    def __init__(self):
        self.calls = []

    def generate(self, statement, feedback, iteration, min_cases, max_cases):
        return {"cases": []}

    def generate_output_checker(
        self, statement, test_model, official_samples,
        rejection_feedback=None,
    ):
        self.calls.append(list(rejection_feedback or []))
        if len(self.calls) == 1:
            return {"checker_python": "import os\n", "reasoning": "bad"}
        return {"checker_python": SAFE_CHECKER, "reasoning": "valid alternatives"}


def test_generated_checker_executes_in_subprocess(tmp_path: Path):
    script = (tmp_path / "checker.py").resolve()
    script.write_text(SAFE_CHECKER, encoding="utf-8")
    checker = checker_from_profile({
        "kind": "GENERATED_PYTHON_SCRIPT",
        "script": str(script),
        "timeout_seconds": 1.0,
    })

    assert checker.accepts_case("OK\n", "YES\n", "unused\n")
    assert not checker.accepts_case("NO\n", "YES\n", "unused\n")


@pytest.mark.parametrize("source", [
    "import os\ndef accepts(input_text, actual, expected): return True\n",
    "def accepts(input_text, actual, expected): return open('x').read()\n",
    "def accepts(input_text, actual, expected): return (1).__class__\n",
    "def accepts(input_text, actual, expected): return actual == expected\n",
    "def accepts(input_text, actual, expected): return __builtins__\n",
])
def test_generated_checker_rejects_unsafe_source(source: str):
    with pytest.raises(GeneratedCheckerSafetyError):
        validate_generated_checker_source(source)


def test_unused_import_is_removed_but_used_import_remains_blocked():
    harmless = SAFE_CHECKER.replace("    try:\n", "    import sys\n    try:\n")
    normalized = strip_unused_imports(harmless)
    assert "import sys" not in normalized
    validate_generated_checker_source(normalized)

    used = (
        "import os\n"
        "def accepts(input_text, actual, expected):\n"
        "    return bool(os.environ)\n"
    )
    with pytest.raises(GeneratedCheckerSafetyError):
        validate_generated_checker_source(strip_unused_imports(used))


def test_generated_checker_timeout_is_rejection(tmp_path: Path):
    script = (tmp_path / "loop.py").resolve()
    script.write_text(
        "def accepts(input_text, actual, expected):\n"
        "    while True:\n"
        "        pass\n",
        encoding="utf-8",
    )
    checker = checker_from_profile({
        "kind": "GENERATED_PYTHON_SCRIPT",
        "script": str(script),
        "timeout_seconds": 0.1,
    })
    assert not checker.accepts_case("YES", "YES", "")


def test_pipeline_retries_and_certifies_generated_checker(tmp_path: Path):
    cases = _CheckerCases()
    pipeline = RunPipeline(
        _Solutions(), cases, _Judge(), checker_from_profile({"kind": "TOKEN"})
    )
    model = {"checker": {"kind": "TOKEN", "multiple_valid_answers": True}}

    pipeline._ensure_output_checker(
        "Print any valid answer satisfying the conditions.",
        model,
        [("1\n", "YES\n")],
        tmp_path,
    )

    assert pipeline.checker.kind == "GENERATED_PYTHON_SCRIPT"
    assert pipeline.output_checker_certification["status"] == "accepted"
    assert pipeline.output_checker_certification["attempt"] == 2
    assert cases.calls[1][0]["stage"] == "static_safety"
    assert (tmp_path / "generated" / "checker-certification.json").is_file()
