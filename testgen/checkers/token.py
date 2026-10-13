from dataclasses import dataclass
from typing import ClassVar

from ..checker import Checker, register_checker


@register_checker
@dataclass(frozen=True)
class TokenChecker(Checker):
    kind: ClassVar[str] = "TOKEN"

    def accepts(self, actual: str, expected: str) -> bool:
        return actual.split() == expected.split()


@register_checker
@dataclass(frozen=True)
class CaseInsensitiveTokenChecker(Checker):
    kind: ClassVar[str] = "CASE_INSENSITIVE_TOKEN"

    def accepts(self, actual: str, expected: str) -> bool:
        return [value.casefold() for value in actual.split()] == [value.casefold() for value in expected.split()]
