"""Suite identities and certified coverage operations."""
import hashlib
import json
from dataclasses import replace
from .domain import Case

def suite_lock(cases: list[Case]) -> dict:
    entries = []
    for case in cases:
        entries.append({
            "id": case.id,
            "input_sha256": hashlib.sha256(case.input.encode()).hexdigest(),
            "expected_sha256": (
                hashlib.sha256(case.expected.encode()).hexdigest()
                if case.expected is not None else None
            ),
        })
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "cases": entries}


def case_record(case: Case) -> dict:
    return {
        "id": case.id,
        "input": case.input,
        "expected": case.expected,
        "family": case.family,
        "iteration": case.iteration,
        "coverage_tags": list(case.coverage_tags),
    }


def merge_certified_coverage(cases: list[Case], input_text: str,
                             tags: tuple[str, ...]) -> Case | None:
    """Attach proposal coverage to identical certified input without duplicating it."""
    for index, case in enumerate(cases):
        if case.input == input_text:
            updated = replace(case, coverage_tags=tuple(dict.fromkeys(
                (*case.coverage_tags, *tags)
            )))
            cases[index] = updated
            return updated
    return None

