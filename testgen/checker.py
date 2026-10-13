"""Checker interface and plugin registry.

Add a registered class in ``testgen.checkers`` to support a new output format.
The pipeline and CLI do not need changing.
"""

from __future__ import annotations

import importlib
import pkgutil
from abc import ABC, abstractmethod
from dataclasses import asdict, is_dataclass
from typing import ClassVar


class Checker(ABC):
    kind: ClassVar[str]
    input_aware: ClassVar[bool] = False

    @abstractmethod
    def accepts(self, actual: str, expected: str) -> bool: ...

    def accepts_case(self, actual: str, expected: str, input_text: str) -> bool:
        """Check one output with access to stdin when a special judge needs it."""
        return self.accepts(actual, expected)

    def profile(self) -> dict:
        options = asdict(self) if is_dataclass(self) else vars(self).copy()
        return {"kind": self.kind, **options}


_REGISTRY: dict[str, type[Checker]] = {}
_LOADED = False


def register_checker(cls: type[Checker]) -> type[Checker]:
    if not issubclass(cls, Checker) or not getattr(cls, "kind", None):
        raise TypeError("A checker plugin must define a non-empty kind")
    if cls.kind in _REGISTRY:
        raise ValueError(f"Duplicate checker kind: {cls.kind}")
    _REGISTRY[cls.kind] = cls
    return cls


def _load_plugins() -> None:
    global _LOADED
    if _LOADED:
        return
    from . import checkers

    for module in pkgutil.iter_modules(checkers.__path__, checkers.__name__ + "."):
        importlib.import_module(module.name)
    _LOADED = True


def checker_from_profile(profile: dict) -> Checker:
    _load_plugins()
    kind = profile.get("kind")
    if kind not in _REGISTRY:
        raise ValueError(f"Unknown checker {kind!r}; available: {', '.join(sorted(_REGISTRY))}")
    options = {key: value for key, value in profile.items() if key != "kind"}
    try:
        return _REGISTRY[kind](**options)
    except TypeError as exc:
        raise ValueError(f"Invalid options for {kind}: {exc}") from exc
