"""Input-aware checker for the constructive polygon problem p00954."""

from __future__ import annotations


def _orientation(a, b, c):
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (value > 0) - (value < 0)


def _on_segment(a, b, p):
    return (_orientation(a, b, p) == 0 and
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _segments_intersect(a, b, c, d):
    o1, o2, o3, o4 = (_orientation(a, b, c), _orientation(a, b, d),
                      _orientation(c, d, a), _orientation(c, d, b))
    if o1 != o2 and o3 != o4:
        return True
    return ((o1 == 0 and _on_segment(a, b, c)) or (o2 == 0 and _on_segment(a, b, d)) or
            (o3 == 0 and _on_segment(c, d, a)) or (o4 == 0 and _on_segment(c, d, b)))


def _valid_polygon(points, width, height):
    count = len(points)
    if count < 3 or count > 100 or len(set(points)) != count:
        return False
    if any(not (0 <= x <= width and 0 <= y <= height) for x, y in points):
        return False
    if max(x for x, _ in points) != width or max(y for _, y in points) != height:
        return False
    area2 = abs(sum(points[i][0] * points[(i + 1) % count][1] -
                    points[(i + 1) % count][0] * points[i][1] for i in range(count)))
    if area2 == 0 or area2 > 2_000_000_000:
        return False
    for i in range(count):
        a, b = points[i], points[(i + 1) % count]
        for j in range(i + 1, count):
            if j in {i, (i + 1) % count} or (j + 1) % count in {i, (i + 1) % count}:
                continue
            if _segments_intersect(a, b, points[j], points[(j + 1) % count]):
                return False
    return True


def accepts(input_text: str, actual: str, expected: str) -> bool:
    try:
        input_tokens = list(map(int, input_text.split()))
        if not input_tokens or len(input_tokens) != 1 + 2 * input_tokens[0]:
            return False
        output_tokens = actual.split()
        position = 0
        for case in range(input_tokens[0]):
            width, height = input_tokens[1 + 2 * case:3 + 2 * case]
            count = int(output_tokens[position])
            position += 1
            coordinates = list(map(int, output_tokens[position:position + 2 * count]))
            if len(coordinates) != 2 * count:
                return False
            position += 2 * count
            points = list(zip(coordinates[::2], coordinates[1::2]))
            if not _valid_polygon(points, width, height):
                return False
        return position == len(output_tokens)
    except (IndexError, TypeError, ValueError):
        return False
