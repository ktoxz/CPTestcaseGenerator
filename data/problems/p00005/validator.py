"""Input validator for p00005."""


def valid(text: str) -> bool:
    try:
        tokens = text.split()
        if len(tokens) != 2:
            return False
        values = [int(token) for token in tokens]
        return all(-10**9 <= value <= 10**9 for value in values)
    except (TypeError, ValueError):
        return False
