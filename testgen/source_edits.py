"""Apply exact, unambiguous model-proposed source mutations locally."""


def apply_source_edits(source: str, edits: object) -> str:
    if not isinstance(edits, list) or not 1 <= len(edits) <= 4:
        raise ValueError("code_edits must contain 1..4 exact replacements")
    for edit in edits:
        if (not isinstance(edit, dict) or set(edit) != {"old", "new"}
                or not isinstance(edit["old"], str) or not edit["old"]
                or not isinstance(edit["new"], str)
                or edit["old"] == edit["new"]
                or len(edit["new"]) > 10000):
            raise ValueError("invalid source edit")
        if source.count(edit["old"]) != 1:
            raise ValueError("source edit must match exactly once")
        source = source.replace(edit["old"], edit["new"], 1)
    return source
