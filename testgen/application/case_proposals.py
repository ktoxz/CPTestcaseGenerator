"""Repair orchestration; certification itself has no LLM dependency."""
from ..suite import case_record

class CaseProposalRunner:
    def __init__(self, certifier, generator, execution, statement, feedback, repair_attempts):
        self.certifier, self.generator, self.execution = certifier, generator, execution
        self.statement, self.feedback, self.repair_attempts = statement, feedback, repair_attempts

    def certify(self, items, source):
        accepted_before = self.certifier.state.accepted_generated
        batch = self.certifier.index_proposals(items, source)
        for repair_attempt in range(self.repair_attempts + 1):
            result = self.certifier.validate_batch(source, batch, repair_attempt)
            rejected_for_repair = list(result.repair_requests)
            if not rejected_for_repair or repair_attempt >= self.repair_attempts:
                break
            repair_feedback = dict(self.feedback)
            repair_feedback["current_round"] = {
                "certified_tests": [
                    case_record(case) for case in self.certifier.state.accepted
                ],
                "rejected_tests": self.certifier.state.rejected,
            }
            with self.execution._waiting(
                f"LLM sửa batch {len(rejected_for_repair)} test, "
                f"lần {repair_attempt + 1}"
            ):
                repaired_rows = self.generator.repair_batch(
                    self.statement,
                    repair_feedback,
                    rejected_for_repair,
                    repair_attempt + 1,
                )
            rejected_indices = {
                row["proposal_index"] for row in rejected_for_repair
            }
            repaired_by_index: dict[int, dict] = {}
            for repaired in repaired_rows:
                if not isinstance(repaired, dict):
                    continue
                original_index = repaired.get("proposal_index")
                if (original_index not in rejected_indices
                        or original_index in repaired_by_index
                        or not isinstance(repaired.get("input"), str)):
                    continue
                current = dict(repaired)
                current.pop("proposal_index", None)
                repaired_by_index[original_index] = current
            batch = sorted(repaired_by_index.items())
        return self.certifier.state.accepted_generated - accepted_before
