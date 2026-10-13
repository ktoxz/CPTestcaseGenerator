"""Trusted, problem-local Python special checker."""

from __future__ import annotations

import hashlib
import importlib.util
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, ClassVar

from ..checker import Checker, register_checker


@register_checker
@dataclass(frozen=True)
class PythonScriptChecker(Checker):
    kind: ClassVar[str] = "PYTHON_SCRIPT"
    input_aware: ClassVar[bool] = True
    script: str
    function: str = "accepts"
    _callback: Callable[[str, str, str], bool] = field(
        init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        path = Path(self.script)
        if not path.is_absolute() or not path.is_file():
            raise ValueError("PYTHON_SCRIPT script must be an existing absolute path")
        name = "testgen_special_checker_" + hashlib.sha256(
            str(path).encode("utf-8")
        ).hexdigest()[:16]
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Cannot load special checker: {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        callback = getattr(module, self.function, None)
        if not callable(callback):
            raise ValueError(
                f"Special checker {path} has no callable {self.function!r}"
            )
        object.__setattr__(self, "_callback", callback)

    def accepts(self, actual: str, expected: str) -> bool:
        return bool(self._callback("", actual, expected))

    def accepts_case(self, actual: str, expected: str, input_text: str) -> bool:
        return bool(self._callback(input_text, actual, expected))

    def profile(self) -> dict:
        return {"kind": self.kind, "script": self.script, "function": self.function}
