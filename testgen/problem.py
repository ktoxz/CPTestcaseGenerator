"""Statement sample parsing and checker requirements."""
import re
import unicodedata

def _normalized_heading(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    without_accents = "".join(
        character for character in decomposed
        if not unicodedata.combining(character)
    )
    return " ".join(without_accents.split())


def _sample_block_kind(label: str) -> str | None:
    normalized = _normalized_heading(label)
    # Check output first because "Output for the Sample Input" contains both words.
    if "output" in normalized or "dau ra" in normalized or "ket qua" in normalized:
        return "output"
    if "input" in normalized or "dau vao" in normalized or "du lieu vao" in normalized:
        return "input"
    return None


def _has_sample_section(markdown: str) -> bool:
    for heading in re.findall(r"(?m)^\s*#{1,6}\s+([^\r\n]+)", markdown):
        normalized = _normalized_heading(heading)
        if any(marker in normalized for marker in ("sample", "example", "vi du")):
            return True
    return False


def samples(markdown: str) -> list[tuple[str, str]]:
    """Extract ordered sample pairs from common English and Vietnamese Markdown."""
    block_pattern = re.compile(
        r"(?ms)^\s*(?:#{2,6}\s+(?P<heading>[^\r\n]+)"
        r"|\*\*(?P<bold>[^*\r\n]+)\*\*)\s*\r?\n"
        r"(?:[ \t]*\r?\n)*[ \t]*```[^\r\n]*\r?\n"
        r"(?P<body>.*?)\r?\n[ \t]*```[ \t]*$"
    )
    found: list[tuple[str, str]] = []
    pending: str | None = None
    for match in block_pattern.finditer(markdown):
        label = match.group("heading") or match.group("bold")
        kind = _sample_block_kind(label)
        body = match.group("body").rstrip() + "\n"
        if kind == "input":
            pending = body
        elif kind == "output" and pending is not None:
            found.append((pending, body))
            pending = None
    return found


def requires_input_aware_checker(markdown: str) -> bool:
    """Best-effort guard for constructive/multiple-answer problem statements."""
    normalized = " ".join(markdown.lower().split())
    indicators = (
        r"\bany one of them is acceptable\b",
        r"\bany (?:valid|one) (?:answer|output|solution) (?:is|will be) accepted\b",
        r"\boutput any (?:valid )?(?:answer|output|solution|one)\b",
        r"\bprint any (?:valid )?(?:answer|output|solution|one)\b",
        r"\bmore than one .{0,100}\bacceptable\b",
        r"\bif there are multiple valid .{0,80}\byou may output any of them\b",
    )
    return any(re.search(pattern, normalized) for pattern in indicators)


