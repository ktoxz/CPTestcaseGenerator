"""Special checker for Codeforces 2218A (The 67th Integer Problem)."""

from __future__ import annotations


def _integers(text: str) -> list[int] | None:
    tokens = text.split()
    try:
        return [int(token) for token in tokens]
    except ValueError:
        return None


def accepts(input_text: str, actual: str, expected: str) -> bool:
    """Accept exactly one valid y per input case; expected is non-canonical."""
    input_values = _integers(input_text)
    output_values = _integers(actual)
    if input_values is None or output_values is None or not input_values:
        return False

    test_count = input_values[0]
    if not 1 <= test_count <= 6767:
        return False
    if len(input_values) != test_count + 1:
        return False
    if len(output_values) != test_count:
        return False

    for x, y in zip(input_values[1:], output_values):
        if not -67 <= x <= 67:
            return False
        # min(x, y) is maximized at x, so every y in [x, 67] is valid.
        if not x <= y <= 67:
            return False
    return True
