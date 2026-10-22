"""Coverage-model normalization and progress accounting."""

from __future__ import annotations

import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from .domain import Case


_PRIORITIES = {"critical", "normal"}
_CATEGORIES = {
    "equivalence",
    "boundary",
    "decision",
    "pairwise",
    "domain",
    "sequence",
    "scenario",
    "output",
    "stress",
    "format",
    "fault",
}


NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
ObligationId = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=80,
        pattern=r"^[a-z0-9][a-z0-9_-]*$",
    ),
]


class TestVariableModel(BaseModel):
    """One input variable described by the specification-derived test model."""

    model_config = ConfigDict(extra="forbid")

    name: NonEmptyText = Field(description="Variable name used in the statement")
    description: str = Field(default="", description="Meaning of the variable")
    domain: NonEmptyText = Field(
        description="Allowed values, including explicit bounds when stated"
    )


class CoverageObligationModel(BaseModel):
    """A concrete black-box behavior that at least one testcase should cover."""

    model_config = ConfigDict(extra="forbid")

    id: ObligationId = Field(
        description="Stable lowercase identifier using letters, digits, _ or -"
    )
    category: Literal[
        "equivalence",
        "boundary",
        "decision",
        "pairwise",
        "domain",
        "sequence",
        "scenario",
        "output",
        "stress",
        "format",
        "fault",
    ]
    description: NonEmptyText = Field(
        description="Concrete behavior that can be covered by a valid stdin payload"
    )
    priority: Literal["critical", "normal"] = Field(
        description="Critical for essential correctness; otherwise normal"
    )
    required: bool = Field(
        description="Whether the generated suite is expected to cover this obligation"
    )


class CheckerSpecModel(BaseModel):
    """Output-comparison requirements extracted during test modelling."""

    model_config = ConfigDict(extra="ignore")

    kind: Literal["TOKEN", "FLOAT", "EXACT", "PYTHON_SCRIPT"] = "TOKEN"
    epsilon: float | None = Field(default=None, gt=0, le=1)
    case_sensitive: bool = True
    multiple_valid_answers: bool = False
    reasoning: str = ""


class SandboxSpecModel(BaseModel):
    """Contest limits extracted from the problem statement."""

    model_config = ConfigDict(extra="ignore")

    time_limit_seconds: float = Field(default=5.0, gt=0, le=60)
    memory_limit_mb: int = Field(default=512, ge=32, le=4096)
    reasoning: str = ""


class TestModelResponse(BaseModel):
    """Strict LLM response contract for specification-only test modelling."""

    model_config = ConfigDict(extra="forbid")

    checker: CheckerSpecModel = Field(default_factory=CheckerSpecModel)
    sandbox: SandboxSpecModel = Field(default_factory=SandboxSpecModel)

    input_grammar: NonEmptyText = Field(
        description="Compact grammar for one complete valid stdin payload"
    )
    constraints: list[NonEmptyText] = Field(
        description="Only input constraints explicitly stated by the problem"
    )
    variables: list[TestVariableModel] = Field(
        description="Input variables and their stated domains"
    )
    relations: list[NonEmptyText] = Field(
        description="Cross-field, length, ordering, uniqueness, or dependency rules"
    )
    output_partitions: list[NonEmptyText] = Field(
        description="Semantically distinct output behaviors worth testing"
    )
    sequences: list[NonEmptyText] = Field(
        description="Multi-record, ordering, state-transition, or EOF behaviors"
    )
    fault_model: list[NonEmptyText] = Field(
        description="Plausible implementation mistakes implied by this specification"
    )
    warnings: list[NonEmptyText] = Field(
        description="Specification ambiguities or modelling limitations"
    )
    coverage_obligations: list[CoverageObligationModel] = Field(
        min_length=1,
        max_length=80,
        description="Concrete non-overlapping black-box coverage targets",
    )

    @field_validator("variables", mode="before")
    @classmethod
    def normalize_variable_shapes(cls, value):
        """Accept compact LLM variable forms without discarding the test model."""
        if not isinstance(value, list):
            return value
        normalized = []
        for item in value:
            if isinstance(item, str):
                normalized.append({
                    "name": item,
                    "description": "",
                    "domain": "unspecified by model",
                })
            elif isinstance(item, dict):
                normalized_item = dict(item)
                if "domain" not in normalized_item and "type" in normalized_item:
                    normalized_item["domain"] = normalized_item.pop("type")
                normalized.append(normalized_item)
            else:
                normalized.append(item)
        return normalized


def _string_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _safe_id(value: str, fallback: str) -> str:
    normalized = re.sub(r"[^a-z0-9_-]+", "-", value.strip().lower()).strip("-")
    return normalized[:80] or fallback


def normalize_test_model(raw: dict) -> dict:
    """Keep a bounded, predictable subset of an untrusted LLM test model."""
    raw = raw if isinstance(raw, dict) else {}
    obligations = []
    seen = set()
    rows = raw.get("coverage_obligations", [])
    if isinstance(rows, list):
        for index, row in enumerate(rows[:80], 1):
            if not isinstance(row, dict):
                continue
            description = row.get("description")
            if not isinstance(description, str) or not description.strip():
                continue
            obligation_id = _safe_id(str(row.get("id", "")), f"obligation-{index}")
            if obligation_id in seen:
                suffix = 2
                while f"{obligation_id}-{suffix}" in seen:
                    suffix += 1
                obligation_id = f"{obligation_id}-{suffix}"
            seen.add(obligation_id)
            category = str(row.get("category", "scenario")).strip().lower()
            priority = str(row.get("priority", "normal")).strip().lower()
            obligations.append({
                "id": obligation_id,
                "category": category if category in _CATEGORIES else "scenario",
                "description": description.strip(),
                "priority": priority if priority in _PRIORITIES else "normal",
                "required": row.get("required", True) is not False,
            })
    checker = raw.get("checker") if isinstance(raw.get("checker"), dict) else {}
    checker_kind = str(checker.get("kind", "TOKEN")).strip().upper()
    if checker_kind not in {"TOKEN", "FLOAT", "EXACT", "PYTHON_SCRIPT"}:
        checker_kind = "TOKEN"
    epsilon = checker.get("epsilon")
    try:
        epsilon = float(epsilon) if epsilon is not None else None
    except (TypeError, ValueError):
        epsilon = None
    if epsilon is not None and not 0 < epsilon <= 1:
        epsilon = None

    sandbox = raw.get("sandbox") if isinstance(raw.get("sandbox"), dict) else {}
    try:
        time_limit = min(60.0, max(0.1, float(sandbox.get("time_limit_seconds", 5.0))))
    except (TypeError, ValueError):
        time_limit = 5.0
    try:
        memory_limit = min(4096, max(32, int(sandbox.get("memory_limit_mb", 512))))
    except (TypeError, ValueError):
        memory_limit = 512

    return {
        "model_version": 1,
        "checker": {
            "kind": checker_kind,
            "epsilon": epsilon,
            "case_sensitive": checker.get("case_sensitive", True) is not False,
            "multiple_valid_answers": checker.get("multiple_valid_answers", False) is True,
            "reasoning": str(checker.get("reasoning", "")).strip(),
        },
        "sandbox": {
            "time_limit_seconds": time_limit,
            "memory_limit_mb": memory_limit,
            "reasoning": str(sandbox.get("reasoning", "")).strip(),
        },
        "input_grammar": str(raw.get("input_grammar", "")).strip(),
        "constraints": _string_list(raw.get("constraints", [])),
        "variables": raw.get("variables", []) if isinstance(raw.get("variables"), list) else [],
        "relations": _string_list(raw.get("relations", [])),
        "output_partitions": _string_list(raw.get("output_partitions", [])),
        "sequences": _string_list(raw.get("sequences", [])),
        "fault_model": _string_list(raw.get("fault_model", [])),
        "coverage_obligations": obligations,
        "warnings": _string_list(raw.get("warnings", [])),
    }


def known_coverage_tags(value, test_model: dict) -> tuple[str, ...]:
    known = {row["id"] for row in test_model.get("coverage_obligations", [])}
    tags = _string_list(value)
    return tuple(dict.fromkeys(tag for tag in tags if tag in known))


def evidenced_coverage_tags(
    value, evidence, input_text: str, test_model: dict
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Verify coverage claims against explicit, input-anchored evidence.

    A generated tag is not coverage by itself.  Each retained tag must have a
    separate evidence row whose excerpt occurs verbatim in the certified input.
    Validator acceptance and reference consensus are enforced by the caller.
    """
    claimed = known_coverage_tags(value, test_model)
    rows = evidence if isinstance(evidence, list) else []
    evidenced: set[str] = set()
    for row in rows[:80]:
        if not isinstance(row, dict):
            continue
        tag = row.get("tag")
        excerpt = row.get("input_excerpt")
        rationale = row.get("rationale")
        if (
            tag in claimed
            and isinstance(excerpt, str)
            and excerpt.strip()
            and len(excerpt) <= 240
            and excerpt in input_text
            and isinstance(rationale, str)
            and rationale.strip()
            and len(rationale) <= 600
        ):
            evidenced.add(tag)
    accepted = tuple(tag for tag in claimed if tag in evidenced)
    rejected = tuple(tag for tag in claimed if tag not in evidenced)
    return accepted, rejected


def coverage_summary(test_model: dict, cases: list[Case]) -> dict:
    obligations = [
        row for row in test_model.get("coverage_obligations", [])
        if row.get("required", True)
    ]
    covered_tags = {
        tag for case in cases for tag in case.coverage_tags
    }
    covered = [row["id"] for row in obligations if row["id"] in covered_tags]
    critical = [row["id"] for row in obligations if row["priority"] == "critical"]
    normal = [row["id"] for row in obligations if row["priority"] == "normal"]
    covered_critical = [item for item in critical if item in covered_tags]
    covered_normal = [item for item in normal if item in covered_tags]
    return {
        "obligations": len(obligations),
        "covered": len(covered),
        "coverage_ratio": len(covered) / len(obligations) if obligations else 1.0,
        "critical_total": len(critical),
        "critical_covered": len(covered_critical),
        "critical_ratio": len(covered_critical) / len(critical) if critical else 1.0,
        "normal_total": len(normal),
        "normal_covered": len(covered_normal),
        "normal_ratio": len(covered_normal) / len(normal) if normal else 1.0,
        "covered_ids": covered,
        "uncovered_critical": [item for item in critical if item not in covered_tags],
        "uncovered_normal": [item for item in normal if item not in covered_tags],
    }


def coverage_meets_targets(
    summary: dict,
    critical_target: float = 1.0,
    normal_target: float = 0.9,
) -> bool:
    return (
        summary["critical_ratio"] >= critical_target
        and summary["normal_ratio"] >= normal_target
    )
