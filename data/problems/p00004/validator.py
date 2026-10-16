"""Input validator for p00004."""

import math


def valid(text: str) -> bool:
    try:
        tokens = text.split()
        if len(tokens) != 6:
            return False
        x1, y1, x2, y2, x3, y3 = map(float, tokens)
        if not all(math.isfinite(value) and abs(value) <= 1e9
                   for value in (x1, y1, x2, y2, x3, y3)):
            return False
        area2 = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        # The problem specifies the three vertices in counter-clockwise order.
        return area2 > 1e-12
    except (TypeError, ValueError, OverflowError):
        return False
