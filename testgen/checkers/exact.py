from dataclasses import dataclass
from typing import ClassVar

from ..checker import Checker, register_checker


@register_checker
@dataclass(frozen=True)
class ExactChecker(Checker):
    kind: ClassVar[str] = "EXACT"

    def accepts(self, actual: str, expected: str) -> bool:
        return actual.replace("\r\n", "\n").rstrip("\n") == expected.replace("\r\n", "\n").rstrip("\n")
