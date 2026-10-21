"""Domain models and the small extension points of the pipeline."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Solution:
    id: str
    label: str  # candidate_ac, candidate_wa, CodeNet Accepted, CodeNet Wrong Answer
    language: str
    source: Path
    bug_class: str = ""
    dialect: str = ""
    strategy_id: str = ""
    bug_origin: str = ""
    failure_condition: str = ""
    witness_input: str = ""
    parent_ac_id: str = ""
    mutation_operator: str = ""
    target_behavior: str = ""
    sample_preservation_reason: str = ""


@dataclass(frozen=True)
class Case:
    id: str
    input: str
    expected: str
    family: str
    iteration: int
    coverage_tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Result:
    solution_id: str
    verdict: str  # PASS, WA, RE, CE, TLE, INFRA
    case_id: str | None = None
    actual: str = ""
    stderr: str = ""


class SolutionGenerator(ABC):
    @abstractmethod
    def generate(self, statement: str, output: Path) -> list[Solution]: ...

    def generate_with_model(self, statement: str, test_model: dict, output: Path) -> list[Solution]:
        """Explicit model entry point; legacy generators can ignore this context."""
        return self.generate(statement, output)

    def requested_wrong_candidates(self) -> int:
        """Return how many certified wrong candidates the pipeline should build."""
        return 0

    def regenerate_correct(
        self,
        statement: str,
        output: Path,
        count: int,
        rejected: list[dict],
        existing: list[Solution],
        round_number: int,
    ) -> list[Solution]:
        """Generate replacement references; unsupported generators return none."""
        return []

    def regenerate_wrong(
        self,
        statement: str,
        output: Path,
        count: int,
        rejected: list[dict],
        existing: list[Solution],
        round_number: int,
    ) -> list[Solution]:
        """Generate replacement wrong candidates; unsupported generators return none."""
        return []

    def generate_mutant_witnesses(
        self,
        statement: str,
        output: Path,
        mutants: list[Solution],
        references: list[Solution],
        evidence: dict[str, dict],
        attempt: int,
        candidates_per_mutant: int,
    ) -> dict[str, list[str]]:
        """Propose additional valid inputs that expose existing mutants."""
        return {}


class CaseGenerator(ABC):
    def generate_output_checker(
        self,
        statement: str,
        test_model: dict,
        official_samples: list[tuple[str, str]],
        rejection_feedback: list[dict] | None = None,
    ) -> dict:
        """Generate an input-aware output checker; unsupported generators opt out."""
        raise NotImplementedError("output-checker generation is unsupported")

    def build_test_model(self, statement: str) -> dict:
        """Build a specification-derived model without candidate or oracle data."""
        return {
            "model_version": 1,
            "input_grammar": "",
            "constraints": [],
            "variables": [],
            "relations": [],
            "output_partitions": [],
            "sequences": [],
            "fault_model": [],
            "coverage_obligations": [],
            "warnings": ["Test-model generation is unsupported by this generator."],
        }

    def generate_baseline(
        self,
        statement: str,
        test_model: dict,
        iteration: int,
        min_cases: int,
        max_cases: int,
    ) -> dict:
        """Generate specification tests without receiving candidate source code."""
        return self.generate(
            statement,
            {
                "generation_mode": "coverage_baseline",
                "test_model": test_model,
                "oracle_used": False,
                "surviving_wrong_candidates": [],
            },
            iteration,
            min_cases,
            max_cases,
        )

    @abstractmethod
    def generate(
        self,
        statement: str,
        feedback: dict,
        iteration: int,
        min_cases: int,
        max_cases: int,
    ) -> dict: ...

    def repair(
        self,
        statement: str,
        feedback: dict,
        rejected: dict,
        attempt: int,
    ) -> dict | None:
        """Return one repaired case, or None when repair is unsupported."""
        return None

    def repair_batch(
        self,
        statement: str,
        feedback: dict,
        rejected: list[dict],
        attempt: int,
    ) -> list[dict]:
        """Repair rejected cases; subclasses may override with one batched call."""
        repaired = []
        for item in rejected:
            candidate = self.repair(statement, feedback, item, attempt)
            if candidate:
                repaired.append({
                    **candidate,
                    "proposal_index": item.get("proposal_index"),
                })
        return repaired

    def top_up(
        self,
        statement: str,
        feedback: dict,
        iteration: int,
        missing_cases: int,
        baseline: bool = False,
    ) -> dict:
        """Generate replacements after invalid, duplicate, or disputed proposals."""
        if missing_cases < 1:
            return {"requested_count": 0, "rationale": "quota already met", "cases": []}
        if baseline:
            return self.generate_baseline(
                statement,
                feedback.get("test_model", {}),
                iteration,
                missing_cases,
                missing_cases,
            )
        return self.generate(
            statement, feedback, iteration, missing_cases, missing_cases
        )

    def audit(
        self,
        statement: str,
        candidate_context: dict,
        iteration: int,
    ) -> dict:
        """Audit one survivor before another test-generation round."""
        return {
            "classification": "insufficient_evidence",
            "revised_bug_hypothesis": "",
            "reasoning": "Audit is unsupported by this case generator.",
            "counterexample": None,
            "confidence": 0.0,
        }

    def audit_batch(
        self,
        statement: str,
        candidate_contexts: list[dict],
        iteration: int,
    ) -> list[dict]:
        """Audit survivors; subclasses may override with one batched call."""
        return [
            {
                "solution_id": context.get("id", "unknown"),
                **self.audit(statement, context, iteration),
            }
            for context in candidate_contexts
        ]


class Judge(ABC):
    @abstractmethod
    def compile(self, solution: Solution) -> Result: ...

    @abstractmethod
    def execute(self, solution: Solution, case_id: str, input_text: str) -> Result: ...

    def execute_many(self, solution: Solution, cases: list[tuple[str, str]]) -> list[Result]:
        """Execute a small batch; transports may override this to reduce round trips."""
        return [self.execute(solution, case_id, input_text) for case_id, input_text in cases]


class OracleSource(ABC):
    @abstractmethod
    def fetch(self, problem_id: str, output: Path, per_label: int) -> list[Solution]: ...
