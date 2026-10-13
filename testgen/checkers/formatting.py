"""Presentation constraints shared by numeric checker plugins."""

from __future__ import annotations

import re


def valid_numeric_layout(actual: str, expected: str, decimal_places: int | None,
                         values_per_line: int | None) -> bool:
    if decimal_places is not None:
        if decimal_places < 0:
            raise ValueError("decimal_places must be nonnegative")
        pattern = re.compile(rf"[+-]?\d+\.\d{{{decimal_places}}}")
        if not all(pattern.fullmatch(token) for token in actual.split()):
            return False
    if values_per_line is not None:
        if values_per_line < 1:
            raise ValueError("values_per_line must be positive")
        lines = actual.strip().splitlines()
        if len(lines) != len(expected.strip().splitlines()):
            return False
        if any(len(line.split()) != values_per_line for line in lines):
            return False
    return True
