"""Strict line-oriented validator for p00061."""


def valid(text: str) -> bool:
    if not isinstance(text, str) or not text.endswith("\n"):
        return False
    lines = text.splitlines()
    teams = set()
    separator = None
    for index, line in enumerate(lines):
        if line == "0,0":
            separator = index
            break
        parts = line.split(",")
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            return False
        team, score = map(int, parts)
        if not 1 <= team <= 100 or not 0 <= score <= 30 or team in teams:
            return False
        teams.add(team)
    if separator is None or not teams or separator == len(lines) - 1:
        return False
    queries = lines[separator + 1:]
    if not queries or any(not value.isdigit() for value in queries):
        return False
    return all(1 <= int(value) <= 30 and int(value) in teams for value in queries)
