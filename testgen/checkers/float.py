from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import ClassVar

from ..checker import Checker, register_checker
from .formatting import valid_numeric_layout


@register_checker
@dataclass(frozen=True)
class FloatChecker(Checker):
    kind: ClassVar[str] = "FLOAT"
    epsilon: float
    decimal_places: int | None = None
    values_per_line: int | None = None

    def accepts(self, actual: str, expected: str) -> bool:
        try:
            epsilon = Decimal(str(self.epsilon))
        except InvalidOperation as exc:
            raise ValueError("FLOAT epsilon must be finite and positive") from exc
        if not epsilon.is_finite() or epsilon <= 0:
            raise ValueError("FLOAT epsilon must be finite and positive")
        left, right = actual.split(), expected.split()
        if len(left) != len(right):
            return False
        try:
            pairs = [(Decimal(a), Decimal(e)) for a, e in zip(left, right)]
        except InvalidOperation:
            return False
        if not all(
            a.is_finite()
            and e.is_finite()
            and abs(a - e) <= epsilon * max(Decimal(1), abs(e))
            for a, e in pairs
        ):
            return False
        return valid_numeric_layout(actual, expected, self.decimal_places, self.values_per_line)
