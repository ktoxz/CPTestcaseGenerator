"""Testcase validation, deduplication and consensus with explicit certification state."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from ..domain import Case, Result, Solution
from ..coverage import evidenced_coverage_tags
from ..suite import merge_certified_coverage

@dataclass
class CaseCertificationState:
    cases: list[Case]
    hashes: set[str]
    intents: dict[str, dict]
    quarantined: list[dict]
    accepted: list[Case] = field(default_factory=list)
    rejected: list[dict] = field(default_factory=list)
    accepted_generated: int = 0
    proposal_counter: int = 0

@dataclass(frozen=True)
class CaseCertificationResult:
    accepted: tuple[Case, ...]
    rejected: tuple[dict, ...]
    repair_requests: tuple[dict, ...]

class CaseCertification:
    def __init__(self, execution, references, checker, validator: Solution,
                 correct: list[Solution], test_model: dict, problem_id: str,
                 iteration: int, state: CaseCertificationState):
        self.execution, self.references, self.checker = execution, references, checker
        self.validator, self.correct, self.test_model = validator, correct, test_model
        self.problem_id, self.iteration, self.state = problem_id, iteration, state

    def index_proposals(self, items, source):
        indexed = []
        for item in items:
            self.state.proposal_counter += 1
            if not isinstance(item, dict) or not isinstance(item.get("input"), str):
                rejected = {"iteration": self.iteration,
                            "proposal_index": self.state.proposal_counter,
                            "source": source, "reason": "malformed proposal"}
                self.state.rejected.append(rejected)
                self.state.quarantined.append(rejected)
            else:
                indexed.append((self.state.proposal_counter, dict(item)))
        return indexed

    def accept_validated(
        self, source: str,
        original_index: int,
        current: dict,
        input_text: str,
        consensus: Result | None,
        validation_id: str,
    ) -> None:
        case_id = f"{self.problem_id}_i{self.iteration}_{len(self.state.cases)+1:03d}"
        if consensus is None:
            rejected = {
                "case_id": case_id,
                "iteration": self.iteration,
                "source": source,
                "reason": "reference disagreement or unusable empty output",
                "family": current.get("family", "llm"),
                "coverage_tags": current.get("coverage_tags", []),
                "input": input_text,
            }
            self.state.quarantined.append(rejected)
            self.state.rejected.append(rejected)
            self.execution._log(
                f"Test {original_index} {case_id}: reference bất đồng"
            )
            return
        reference_output = current.get("official_expected", consensus.actual)
        if (
            self.checker.requires_expected_output
            and (
                not isinstance(reference_output, str)
                or not reference_output.strip()
            )
        ):
            rejected = {
                "case_id": case_id,
                "iteration": self.iteration,
                "source": source,
                "reason": "empty expected output",
                "family": current.get("family", "llm"),
                "coverage_tags": current.get("coverage_tags", []),
                "input": input_text,
            }
            self.state.quarantined.append(rejected)
            self.state.rejected.append(rejected)
            self.execution._log(
                f"Test {original_index} {case_id}: expected output rỗng"
            )
            return
        expected = (
            reference_output
            if self.checker.requires_expected_output
            else None
        )
        if not self.checker.accepts_case(
            consensus.actual, expected, input_text
        ):
            rejected = {
                "case_id": case_id,
                "iteration": self.iteration,
                "source": source,
                "reason": "official sample disagreement",
                "input": input_text,
            }
            self.state.quarantined.append(rejected)
            self.state.rejected.append(rejected)
            self.execution._log(f"Test {original_index} {case_id}: lệch sample")
            return
        tags, rejected_tags = evidenced_coverage_tags(
            current.get("coverage_tags", []),
            current.get("coverage_evidence", []),
            input_text,
            self.test_model,
        )
        accepted = Case(
            case_id,
            input_text,
            expected,
            current.get("family", "llm"),
            self.iteration,
            tags,
        )
        self.state.cases.append(accepted)
        # Reuse certified executions when the final suite is judged.
        self.execution.alias_reference_results(self.correct, validation_id, case_id, input_text)
        self.state.accepted.append(accepted)
        if current.get("family") != "official-sample":
            self.state.accepted_generated += 1
        targets = current.get("target_solution_ids", [])
        if not isinstance(targets, list):
            targets = []
        self.state.intents[case_id] = {
            "target_solution_ids": [
                target for target in targets if isinstance(target, str)
            ],
            "hypothesis_id": current.get("hypothesis_id", ""),
            "predicted_expected": current.get("predicted_expected", ""),
            "predicted_candidate_output": current.get(
                "predicted_candidate_output", ""
            ),
            "reason_for_difference": current.get(
                "reason_for_difference", ""
            ),
            "coverage_tags": list(tags),
            "coverage_evidence": current.get("coverage_evidence", []),
            "rejected_coverage_claims": list(rejected_tags),
        }
        self.execution._log(
            f"Test {original_index} {case_id}: nhận; tổng {len(self.state.cases)}"
        )

    def validate_batch(
        self, source: str,
        batch: list[tuple[int, dict]], repair_attempt: int
    ) -> CaseCertificationResult:
        accepted_start = len(self.state.accepted)
        rejected_start = len(self.state.rejected)
        if not batch:
            return CaseCertificationResult((), (), ())
        validation_rows: list[tuple[int, dict, str, str]] = []
        validation_jobs: list[tuple[str, str]] = []
        for original_index, current in batch:
            input_text = current["input"].rstrip() + "\n"
            digest = hashlib.sha256(input_text.encode()).hexdigest()
            validation_id = (
                f"{self.problem_id}_i{self.iteration}_p{original_index:03d}"
                f"_r{repair_attempt}"
            )
            if digest in self.state.hashes:
                tags, rejected_tags = evidenced_coverage_tags(
                    current.get("coverage_tags", []),
                    current.get("coverage_evidence", []),
                    input_text,
                    self.test_model,
                )
                updated = merge_certified_coverage(
                    self.state.cases, input_text, tags,
                )
                if updated is not None:
                    for index, case in enumerate(self.state.accepted):
                        if case.id == updated.id:
                            self.state.accepted[index] = updated
                    self.state.intents.setdefault(updated.id, {})["coverage_tags"] = list(
                        updated.coverage_tags
                    )
                    intent = self.state.intents.setdefault(updated.id, {})
                    intent["coverage_evidence"] = current.get("coverage_evidence", [])
                    intent["rejected_coverage_claims"] = list(rejected_tags)
                rejected = {
                    "case_id": validation_id,
                    "iteration": self.iteration,
                    "proposal_index": original_index,
                    "repair_attempt": repair_attempt,
                    "source": source,
                    "reason": "duplicate input",
                    "family": current.get("family", "llm"),
                    "coverage_tags": current.get("coverage_tags", []),
                    "input": input_text,
                }
                self.state.rejected.append(rejected)
                self.execution._log(
                    f"Test {original_index}: trùng, yêu cầu top-up"
                )
                continue
            self.state.hashes.add(digest)
            validation_rows.append(
                (original_index, current, input_text, validation_id)
            )
            validation_jobs.append((validation_id, input_text))

        validations = self.execution._execute_many(
            self.validator, validation_jobs, purpose="testcase.validator"
        ) if validation_jobs else []
        rejected_for_repair: list[dict] = []
        consensuses = self.references._reference_consensus_many(self.correct, [
            (row[3], row[2])
            for row, validation in zip(validation_rows, validations)
            if validation.verdict == "PASS"
        ])
        for row, validation in zip(validation_rows, validations):
            original_index, current, input_text, validation_id = row
            if validation.verdict == "PASS":
                self.accept_validated(
                    source,
                    original_index, current, input_text,
                    consensuses[validation_id], validation_id,
                )
                continue
            rejected = {
                "case_id": validation_id,
                "iteration": self.iteration,
                "proposal_index": original_index,
                "repair_attempt": repair_attempt,
                "source": source,
                "reason": "validator rejected",
                "validator_verdict": validation.verdict,
                "validator_stderr": validation.stderr,
                "family": current.get("family", "llm"),
                "coverage_tags": current.get("coverage_tags", []),
                "target_solution_ids": current.get(
                    "target_solution_ids", []
                ),
                "hypothesis_id": current.get("hypothesis_id", ""),
                "input": input_text,
            }
            self.state.quarantined.append(rejected)
            self.state.rejected.append(rejected)
            self.execution._log(
                f"Test {original_index} {validation_id}: "
                f"validator từ chối (lần {repair_attempt + 1})"
            )
            if current.get("family") == "official-sample":
                raise RuntimeError(
                    "Validator rejected an official sample; inspect the validator"
                )
            rejected_for_repair.append(rejected)

        return CaseCertificationResult(
            tuple(self.state.accepted[accepted_start:]),
            tuple(self.state.rejected[rejected_start:]), tuple(rejected_for_repair))
