"""Bounded execution adapter for LLM-generated output checkers."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from ..checker import Checker, register_checker


class GeneratedCheckerSafetyError(ValueError):
    """Generated source violates the restricted checker contract."""


def strip_unused_imports(source: str) -> str:
    """Remove decorative imports only when no imported binding is read."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source
    loaded_names = {
        node.id for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    class _Stripper(ast.NodeTransformer):
        changed = False

        def _keep(self, node, bindings: set[str]):
            if bindings & loaded_names:
                return node
            self.changed = True
            return None

        def visit_Import(self, node: ast.Import):
            bindings = {
                alias.asname or alias.name.split(".", 1)[0]
                for alias in node.names
            }
            return self._keep(node, bindings)

        def visit_ImportFrom(self, node: ast.ImportFrom):
            bindings = {alias.asname or alias.name for alias in node.names}
            return self._keep(node, bindings)

    stripper = _Stripper()
    tree = stripper.visit(tree)
    if not stripper.changed:
        return source
    ast.fix_missing_locations(tree)
    return ast.unparse(tree) + "\n"


_BANNED_NAMES = {
    "__import__", "breakpoint", "compile", "delattr", "dir", "eval", "exec",
    "getattr", "globals", "help", "input", "locals", "memoryview", "open",
    "print", "setattr", "super", "type", "vars",
}

_BANNED_NODES = (
    ast.AsyncFunctionDef,
    ast.Await,
    ast.ClassDef,
    ast.Delete,
    ast.Global,
    ast.Import,
    ast.ImportFrom,
    ast.Lambda,
    ast.Nonlocal,
    ast.Raise,
    ast.With,
    ast.AsyncWith,
    ast.Yield,
    ast.YieldFrom,
)


def validate_generated_checker_source(source: str) -> ast.Module:
    if not isinstance(source, str) or not source.strip():
        raise GeneratedCheckerSafetyError("checker source is empty")
    if len(source) > 30000:
        raise GeneratedCheckerSafetyError("checker source exceeds 30000 characters")
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise GeneratedCheckerSafetyError(f"checker syntax error: {error}") from error
    nodes = list(ast.walk(tree))
    if len(nodes) > 5000:
        raise GeneratedCheckerSafetyError("checker AST exceeds 5000 nodes")
    for node in nodes:
        if isinstance(node, _BANNED_NODES):
            raise GeneratedCheckerSafetyError(
                f"checker contains forbidden syntax: {type(node).__name__}"
            )
        if isinstance(node, ast.Name) and node.id in _BANNED_NAMES:
            raise GeneratedCheckerSafetyError(
                f"checker uses forbidden name: {node.id}"
            )
        if isinstance(node, ast.Name) and node.id.startswith("_"):
            raise GeneratedCheckerSafetyError(
                f"checker uses private name: {node.id}"
            )
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise GeneratedCheckerSafetyError(
                f"checker uses private attribute: {node.attr}"
            )
        if isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, (str, bytes)) and len(value) > 10000:
                raise GeneratedCheckerSafetyError("checker contains oversized constant")
            if isinstance(value, int) and value.bit_length() > 256:
                raise GeneratedCheckerSafetyError("checker contains oversized integer")
    accepts = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "accepts"
    ]
    if len(accepts) != 1:
        raise GeneratedCheckerSafetyError(
            "checker must define exactly one accepts function"
        )
    function = accepts[0]
    if (len(function.args.args) != 3 or function.args.vararg is not None
            or function.args.kwarg is not None
            or [argument.arg for argument in function.args.args]
            != ["input_text", "actual", "expected"]):
        raise GeneratedCheckerSafetyError(
            "accepts must take exactly input_text, actual, expected"
        )
    if any(
        isinstance(node, ast.Name)
        and node.id == "expected"
        and isinstance(node.ctx, ast.Load)
        for node in ast.walk(function)
    ):
        raise GeneratedCheckerSafetyError(
            "generated checker must validate from input_text and actual; "
            "reading the non-canonical expected output is forbidden"
        )
    for definition in [node for node in tree.body if isinstance(node, ast.FunctionDef)]:
        if definition.decorator_list:
            raise GeneratedCheckerSafetyError("function decorators are forbidden")
        for default in (*definition.args.defaults, *definition.args.kw_defaults):
            if default is None:
                continue
            try:
                ast.literal_eval(default)
            except (ValueError, TypeError):
                raise GeneratedCheckerSafetyError(
                    "function defaults must be literal values"
                ) from None
    allowed_top_level = (ast.FunctionDef, ast.Assign, ast.AnnAssign, ast.Expr)
    for node in tree.body:
        if not isinstance(node, allowed_top_level):
            raise GeneratedCheckerSafetyError(
                f"forbidden top-level statement: {type(node).__name__}"
            )
        if isinstance(node, ast.Expr) and not (
            isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            raise GeneratedCheckerSafetyError("top-level expression is forbidden")
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value = node.value
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError):
                raise GeneratedCheckerSafetyError(
                    "top-level assignments must contain literal values"
                ) from None
    return tree


@register_checker
@dataclass(frozen=True)
class GeneratedPythonScriptChecker(Checker):
    kind: ClassVar[str] = "GENERATED_PYTHON_SCRIPT"
    input_aware: ClassVar[bool] = True
    script: str
    function: str = "accepts"
    timeout_seconds: float = 2.0

    def __post_init__(self) -> None:
        path = Path(self.script)
        if not path.is_absolute() or not path.is_file():
            raise ValueError(
                "GENERATED_PYTHON_SCRIPT script must be an existing absolute path"
            )
        if not 0.1 <= self.timeout_seconds <= 5:
            raise ValueError("generated checker timeout must be between 0.1 and 5s")
        validate_generated_checker_source(path.read_text(encoding="utf-8"))

    def accepts(self, actual: str, expected: str) -> bool:
        return self.accepts_case(actual, expected, "")

    def accepts_case(self, actual: str, expected: str, input_text: str) -> bool:
        runner = Path(__file__).with_name("generated_runner.py")
        payload = json.dumps({
            "input": input_text,
            "actual": actual,
            "expected": expected,
        })
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-S", str(runner), self.script, self.function],
                input=payload,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        if completed.returncode != 0 or len(completed.stdout) > 1000:
            return False
        try:
            response = json.loads(completed.stdout)
        except (json.JSONDecodeError, TypeError):
            return False
        return response.get("accepted") is True

    def profile(self) -> dict:
        return {
            "kind": self.kind,
            "script": self.script,
            "function": self.function,
            "timeout_seconds": self.timeout_seconds,
            "trust": "generated_unreviewed",
        }
