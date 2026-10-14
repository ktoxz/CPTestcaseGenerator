"""Build a certified mutant pool and separate development from holdout."""
from __future__ import annotations
from testgen.persistence import RunStore, default_run_store
import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path
from ..llm_contract import LLMTransportError, LLMResponseError
from ..throttle import EndpointBusyError
from ..policies import split_mutant_pool
from ..domain import Solution, Result, SolutionGenerator

@dataclass(frozen=True)
class MutantPoolPolicy:
    mutant_replacement_rounds: int
    mutant_replacement_oversampling: float
    mutant_witness_repair_rounds: int
    mutant_witness_candidates: int
    minimum_verified_mutants: int
    holdout_fraction: float

    @property
    def recovery_rounds(self) -> int:
        """Additional bounded attempts after ordinary replacement is exhausted."""
        return 4

@dataclass(frozen=True)
class CandidatePool:
    candidates: list[Solution]
    candidate_ac: list[Solution]
    active_wrong: list[Solution]
    development_wrong: list[Solution]
    holdout_wrong: list[Solution]
    certification_records: list[dict]
    certification_summary: dict
    requested_wrong: int
    strict_verified_count: int
    fallback_sample_mutants_used: list[str]
    compiles: dict[str, Result]

class MutantPoolBuilder:
    def __init__(self, solution_generator: SolutionGenerator, execution, certifier,
                 policy: MutantPoolPolicy, store: RunStore | None = None):
        self.store = store or default_run_store()
        self.solution_generator, self.execution = solution_generator, execution
        self.certifier, self.policy = certifier, policy

    def build(self, statement: str, generated: Path, candidates: list[Solution],
              validator: Solution, correct: list[Solution],
              all_compiles: dict[str, Result], official_samples) -> CandidatePool:
        all_compiles = dict(all_compiles)
        candidate_ac = [s for s in candidates if s.label == "candidate_ac"]
        initial_wrong = [s for s in candidates if s.label == "candidate_wa"]
        requested_wrong = max(
            len(initial_wrong),
            self.solution_generator.requested_wrong_candidates(),
        )
        required_verified = (
            min(
                requested_wrong,
                max(
                    1,
                    max(
                        self.policy.minimum_verified_mutants,
                        math.ceil(requested_wrong * 0.6),
                    ),
                ),
            )
            if requested_wrong else 0
        )
        all_generated = list(candidates)
        active_wrong: list[Solution] = []
        certification_records: list[dict] = []
        rejected_mutants: list[dict] = []
        sample_fallback_mutants: list[tuple[Solution, dict]] = []
        skipped_mutants: list[dict] = []
        reserve_verified_mutants: list[dict] = []
        witness_early_stop = {
            "repair_witnesses_proposed": 0,
            "repair_witnesses_evaluated": 0,
            "repair_witnesses_skipped_after_verified": 0,
            "repair_witnesses_skipped_after_pool_full": 0,
        }

        def certify_batch(batch: list[Solution]) -> None:
            if len(active_wrong) >= requested_wrong:
                skipped_mutants.extend({
                    "solution_id": solution.id,
                    "reason": "requested verified pool is already full",
                } for solution in batch)
                return

            def certify_one(solution: Solution) -> tuple[Solution, dict]:
                evidence = self.certifier._certify_mutant(
                    solution, validator, correct, all_compiles[solution.id],
                    official_samples,
                )
                return solution, evidence

            workers = min(self.execution.judge_workers, len(batch)) if batch else 1
            if workers == 1:
                certified = [certify_one(solution) for solution in batch]
            else:
                self.execution._log(
                    f"Chứng nhận {len(batch)} mutant với {workers} worker"
                )
                with ThreadPoolExecutor(
                    max_workers=workers, thread_name_prefix="mutant-cert"
                ) as executor:
                    certified = list(executor.map(certify_one, batch))

            def attempt_record(evidence: dict) -> dict:
                return {
                    "witness_input": evidence.get("witness_input"),
                    "verified": evidence.get("verified", False),
                    "reason": evidence.get("reason"),
                    "validator_verdict": evidence.get("validator_verdict"),
                    "reference_expected": evidence.get("reference_expected"),
                    "candidate_verdict": evidence.get("candidate_verdict"),
                    "candidate_actual": evidence.get("candidate_actual"),
                    "candidate_trials": evidence.get("candidate_trials", []),
                }

            repairable_reasons = {
                "missing witness_input",
                "witness rejected by validator",
                "witness did not distinguish candidate from references in both trials",
                "witness failure was not stable across two trials",
            }
            repaired = {solution.id: (solution, evidence)
                        for solution, evidence in certified}
            pending = {
                solution.id
                for solution, evidence in certified
                if not evidence["verified"]
                and evidence["official_samples_passed"]
                and evidence["reason"] in repairable_reasons
            }
            for solution_id in pending:
                solution, evidence = repaired[solution_id]
                evidence["witness_attempts"] = [attempt_record(evidence)]
            repair_generation_counts = {
                solution.id: 0 for solution in batch
            }
            batch_order = {
                solution.id: index for index, solution in enumerate(batch)
            }

            def remaining_needed() -> int:
                verified_in_batch = sum(
                    evidence["verified"] for _, evidence in repaired.values()
                )
                fallback_in_batch = sum(
                    evidence.get("fallback_verified", False)
                    for _, evidence in repaired.values()
                )
                return max(
                    0,
                    required_verified
                    - len(active_wrong)
                    - len(sample_fallback_mutants)
                    - verified_in_batch
                    - fallback_in_batch,
                )

            for witness_attempt in range(
                1, self.policy.mutant_witness_repair_rounds + 1
            ):
                if not pending or remaining_needed() == 0:
                    break
                ordered_pending = [
                    repaired[solution.id][0] for solution in batch
                    if solution.id in pending
                ]
                ordered_pending.sort(key=lambda solution: (
                    repair_generation_counts[solution.id],
                    batch_order[solution.id],
                ))
                # Keep a small batch when the pool only needs a few more and
                # rotate toward candidates without a repair round yet.
                repair_window = min(
                    len(ordered_pending), max(remaining_needed(), 2)
                )
                pending_solutions = ordered_pending[:repair_window]
                for solution in pending_solutions:
                    repair_generation_counts[solution.id] += 1
                self.execution._log(
                    f"Sửa witness lần {witness_attempt}: "
                    f"{len(pending_solutions)}/{len(pending)} mutant, tối đa "
                    f"{self.policy.mutant_witness_candidates} input/mutant"
                )
                proposals = self.solution_generator.generate_mutant_witnesses(
                    statement,
                    generated,
                    pending_solutions,
                    correct,
                    {solution_id: repaired[solution_id][1]
                     for solution_id in {
                         solution.id for solution in pending_solutions
                     }},
                    witness_attempt,
                    self.policy.mutant_witness_candidates,
                )
                proposal_lists = {
                    solution.id: list(proposals.get(solution.id, []))
                    for solution in pending_solutions
                }
                proposed_count = sum(map(len, proposal_lists.values()))
                witness_early_stop["repair_witnesses_proposed"] += proposed_count
                if not proposed_count:
                    self.execution._log("Generator không cung cấp witness sửa đổi")
                    continue
                evaluated_proposals = {
                    solution.id: 0 for solution in pending_solutions
                }

                def certify_repaired_witness(
                    job: tuple[Solution, str]
                ) -> tuple[str, str, dict]:
                    solution, witness = job
                    base_evidence = repaired[solution.id][1]
                    evidence = self.certifier._certify_mutant(
                        solution,
                        validator,
                        correct,
                        all_compiles[solution.id],
                        official_samples,
                        witness_input=witness,
                        certified_samples=base_evidence["official_samples"],
                    )
                    return solution.id, witness, evidence

                # Evaluate one proposal per pending mutant in each wave. Never
                # schedule more jobs concurrently than the number of verified
                # mutants still needed. Failed jobs immediately yield their slot
                # to the next pending mutant, while reaching the requested pool
                # stops the whole repair stage rather than creating reserves.
                wave_count = max(map(len, proposal_lists.values()))
                pool_filled = False
                for proposal_index in range(wave_count):
                    jobs = [
                        (solution, proposal_lists[solution.id][proposal_index])
                        for solution in pending_solutions
                        if solution.id in pending
                        and proposal_index < len(proposal_lists[solution.id])
                    ]
                    if not jobs:
                        continue
                    while jobs:
                        needed = remaining_needed()
                        if needed == 0:
                            pool_filled = True
                            break
                        scheduled, jobs = jobs[:needed], jobs[needed:]
                        witness_early_stop[
                            "repair_witnesses_evaluated"
                        ] += len(scheduled)
                        for scheduled_solution, _ in scheduled:
                            evaluated_proposals[scheduled_solution.id] += 1
                        witness_workers = min(self.execution.judge_workers, len(scheduled))
                        if witness_workers == 1:
                            evaluated = [
                                certify_repaired_witness(job) for job in scheduled
                            ]
                        else:
                            self.execution._log(
                                f"Kiểm tra witness đợt "
                                f"{proposal_index + 1}/{wave_count}: "
                                f"{len(scheduled)} input với "
                                f"{witness_workers} worker"
                            )
                            with ThreadPoolExecutor(
                                max_workers=witness_workers,
                                thread_name_prefix="witness-repair",
                            ) as executor:
                                evaluated = list(
                                    executor.map(certify_repaired_witness, scheduled)
                                )

                        for solution_id, witness, evidence in evaluated:
                            solution, previous_evidence = repaired[solution_id]
                            history = list(
                                previous_evidence.get("witness_attempts", [])
                            )
                            history.append(attempt_record(evidence))
                            evidence["witness_attempts"] = history
                            if evidence["verified"]:
                                evidence["witness_repair_status"] = "verified"
                                repaired[solution_id] = (
                                    replace(solution, witness_input=witness), evidence
                                )
                                pending.remove(solution_id)
                                skipped = (
                                    len(proposal_lists[solution_id])
                                    - proposal_index - 1
                                )
                                witness_early_stop[
                                    "repair_witnesses_skipped_after_verified"
                                ] += skipped
                                self.execution._log(
                                    f"Mutant {solution_id}: witness sửa đổi đã xác nhận "
                                    f"code sai; bỏ qua {skipped} witness còn lại"
                                )
                            else:
                                evidence["witness_repair_status"] = "not_distinguished"
                                repaired[solution_id] = (solution, evidence)
                        if remaining_needed() == 0:
                            pool_filled = True
                            break
                    if pool_filled:
                        break
                if pool_filled:
                    skipped = sum(
                        len(proposal_lists[solution_id])
                        - evaluated_proposals[solution_id]
                        for solution_id in pending
                        if solution_id in proposal_lists
                    )
                    witness_early_stop[
                        "repair_witnesses_skipped_after_pool_full"
                    ] += skipped
                    self.execution._log(
                        "Đã đủ mutant xác nhận; dừng sửa witness và bỏ qua "
                        f"{skipped} đề xuất còn lại"
                    )
                    break

            for solution_id in pending:
                repaired[solution_id][1]["witness_repair_status"] = (
                    "skipped_pool_full"
                    if remaining_needed() == 0 else "exhausted"
                )
            certified = [repaired[solution.id] for solution in batch]

            for solution, evidence in certified:
                certification_records.append(evidence)
                if evidence["verified"]:
                    if len(active_wrong) < requested_wrong:
                        active_wrong.append(solution)
                        self.execution._log(f"Mutant {solution.id}: witness xác nhận code sai")
                    else:
                        reserve_verified_mutants.append({
                            "solution_id": solution.id,
                            "reason": "verified after requested pool became full",
                        })
                        self.execution._log(
                            f"Mutant {solution.id}: đã xác nhận, giữ ngoài pool vì đã đủ quota"
                        )
                elif evidence.get("fallback_verified"):
                    sample_fallback_mutants.append((solution, evidence))
                    self.execution._log(
                        f"Mutant {solution.id}: sai ổn định trên sample chính thức; "
                        "giữ làm dự phòng"
                    )
                elif evidence.get("witness_repair_status") == "skipped_pool_full":
                    skipped_mutants.append({
                        "solution_id": solution.id,
                        "reason": "requested verified pool became full during repair",
                    })
                else:
                    rejected = {
                        **evidence,
                        "language": solution.language,
                        "source_code": self.store.read_text(solution.source,
                            encoding="utf-8", errors="replace"
                        ),
                    }
                    rejected_mutants.append(rejected)
                    self.execution._log(
                        f"Mutant {solution.id}: loại khỏi TNR — {evidence['reason']}"
                    )

        generation_failures: list[dict] = []
        replacement_rounds_used = 0

        def generate_replacements(
            problem_statement: str, artifact_dir: Path, count: int,
            rejected: list[dict], existing: list[Solution], round_number: int,
        ) -> list[Solution]:
            try:
                return self.solution_generator.regenerate_wrong(
                    problem_statement, artifact_dir, count, rejected, existing, round_number,
                )
            except (LLMTransportError, LLMResponseError, TimeoutError, EndpointBusyError) as error:
                generation_failures.append({
                    "round": round_number, "error_type": type(error).__name__, "reason": str(error),
                })
                self.execution._log(
                    f"Sinh mutant vòng {round_number} lỗi {type(error).__name__}: {error}; "
                    "tiếp tục trong giới hạn retry"
                )
                return []

        if len(initial_wrong) < required_verified:
            # Seed enough diversity for the certified minimum. The
            # oversampling factor absorbs duplicates without multiplying the
            # full five-mutant quota before any candidate has been judged.
            missing = required_verified - len(initial_wrong)
            proposal_count = max(
                missing,
                math.ceil(missing * self.policy.mutant_replacement_oversampling),
            )
            with self.execution._waiting(
                f"LLM sinh {proposal_count} mutant ban đầu từ AC đã xác nhận"
            ):
                derived_initial = generate_replacements(
                    statement,
                    generated,
                    proposal_count,
                    [],
                    [*correct, *initial_wrong],
                    0,
                )
            all_generated.extend(derived_initial)
            initial_wrong.extend(derived_initial)
            all_compiles.update(
                self.execution._compile_pool(derived_initial, "Biên dịch mutant ban đầu")
            )

        certify_batch(initial_wrong)
        total_rounds = self.policy.mutant_replacement_rounds + self.policy.recovery_rounds
        for replacement_round in range(1, total_rounds + 1):
            # Stop asking the LLM once the strict pool plus deterministically
            # verified sample-fallback reserve can cover the minimum. Trying
            # to fill the desirable five-item pool before this point wastes
            # expensive inference calls after weak/duplicate rows.
            missing = (
                required_verified
                - len(active_wrong)
                - len(sample_fallback_mutants)
            )
            if missing <= 0:
                if len(active_wrong) < required_verified:
                    self.execution._log(
                        "Đã có đủ mutant sai được kiểm chứng để đạt pool tối thiểu; "
                        "dừng gọi LLM thay thế"
                    )
                break
            replacement_rounds_used = replacement_round
            if replacement_round > self.policy.mutant_replacement_rounds:
                recovery_round = replacement_round - self.policy.mutant_replacement_rounds
                self.execution._log(
                    f"Pool mutant còn thiếu {missing}; vòng bổ sung "
                    f"{recovery_round}/{self.policy.recovery_rounds}"
                )
            proposal_count = max(
                missing,
                math.ceil(missing * self.policy.mutant_replacement_oversampling),
            )
            with self.execution._waiting(
                f"LLM sinh {proposal_count} đề xuất để lấp {missing} mutant "
                f"vòng {replacement_round}"
            ):
                regeneration_context = [
                    *correct,
                    *(solution for solution in all_generated
                      if solution.label == "candidate_wa"),
                ]
                replacements = generate_replacements(
                    statement,
                    generated,
                    proposal_count,
                    [
                        *rejected_mutants,
                        *(
                            {
                                **evidence,
                                "language": solution.language,
                                "source_code": self.store.read_text(solution.source,
                                    encoding="utf-8", errors="replace"
                                ),
                            }
                            for solution, evidence in sample_fallback_mutants
                        ),
                    ],
                    regeneration_context,
                    replacement_round,
                )
            if not replacements:
                self.execution._log(
                    "Vòng này không có mutant thay thế hợp lệ; tiếp tục vòng còn lại"
                )
                continue
            all_generated.extend(replacements)
            all_compiles.update(
                self.execution._compile_pool(replacements, "Biên dịch mutant thay thế")
            )
            certify_batch(replacements)

        # Prefer hard, sample-preserving mutants. If the LLM still cannot
        # produce the minimum after every replacement round, promote only
        # deterministic official-sample failures. Equivalent, flaky,
        # uncompilable, and infrastructure-failing candidates remain rejected.
        strict_verified_count = len(active_wrong)
        fallback_sample_mutants_used: list[str] = []
        for solution, evidence in sample_fallback_mutants:
            if len(active_wrong) >= required_verified:
                break
            promoted = replace(
                solution, witness_input=str(evidence.get("witness_input", ""))
            )
            active_wrong.append(promoted)
            evidence["verified"] = True
            evidence["promoted_to_minimum_pool"] = True
            fallback_sample_mutants_used.append(solution.id)
            self.execution._log(
                f"Mutant {solution.id}: dùng dự phòng sample chính thức để đủ "
                f"pool tối thiểu ({len(active_wrong)}/{required_verified})"
            )

        rejection_reason_counts: dict[str, int] = {}
        for item in rejected_mutants:
            reason = str(item.get("reason", "unknown rejection"))
            rejection_reason_counts[reason] = rejection_reason_counts.get(reason, 0) + 1
        pool_status = (
            "ready_full" if len(active_wrong) == requested_wrong
            else "ready_minimum" if len(active_wrong) >= required_verified
            else "failed_minimum_verified_pool"
        )
        certification_summary = {
            "requested_wrong_candidates": requested_wrong,
            "validated_wrong_candidates": len(active_wrong),
            "validated_solution_ids": [solution.id for solution in active_wrong],
            "strict_sample_preserving_verified": strict_verified_count,
            "official_sample_fallback_available": len(sample_fallback_mutants),
            "official_sample_fallback_used": fallback_sample_mutants_used,
            "verification_policy": {
                "preferred": "sample_preserving_witness",
                "minimum_pool_fallback": "stable_official_sample_failure",
                "fallback_trials": 2,
                "never_accept": [
                    "equivalent mutant", "unstable failure", "CE", "INFRA"
                ],
            },
            "rejected_or_unverified": len(rejected_mutants),
            "rejection_reason_counts": rejection_reason_counts,
            "replacement_rounds_allowed": self.policy.mutant_replacement_rounds,
            "replacement_oversampling": self.policy.mutant_replacement_oversampling,
            "witness_repair_rounds_allowed": self.policy.mutant_witness_repair_rounds,
            "witness_candidates_per_round": self.policy.mutant_witness_candidates,
            "witness_early_stop": {
                "enabled": True,
                "criterion": (
                    "stop after the first witness that produces the same "
                    "deterministic failure in two candidate trials"
                ),
                **witness_early_stop,
            },
            "compile_policy": {
                "compile_once_per_candidate": True,
                "compiled_mutant_candidates": len({
                    solution.id for solution in all_generated
                    if solution.label == "candidate_wa"
                    and solution.id in all_compiles
                }),
            },
            "candidate_trials_per_witness": 2,
            "mutants_verified_by_repaired_witness": sum(
                item.get("witness_repair_status") == "verified"
                for item in certification_records
            ),
            "minimum_required": required_verified,
            "full_requested_pool_built": len(active_wrong) == requested_wrong,
            "stage_status": pool_status,
            "skipped_after_pool_full": skipped_mutants,
            "verified_reserve_not_selected": reserve_verified_mutants,
            "records": certification_records,
            "rejected": rejected_mutants,
        }
        if replacement_rounds_used > self.policy.mutant_replacement_rounds or generation_failures:
            certification_summary["recovery"] = {
                "additional_rounds_allowed": self.policy.recovery_rounds,
                "additional_rounds_used": max(
                    0, replacement_rounds_used - self.policy.mutant_replacement_rounds),
                "total_replacement_rounds_used": replacement_rounds_used,
                "generation_failures": generation_failures,
            }
        self.store.write_json(generated / "mutant-certification.json", certification_summary)
        if len(active_wrong) < required_verified:
            raise RuntimeError(
                "Could not build the minimum verified wrong-candidate pool: "
                f"validated {len(active_wrong)}/{requested_wrong}; minimum "
                f"required {required_verified}; exhausted {replacement_rounds_used} replacement "
                f"rounds (including up to {self.policy.recovery_rounds} additional rounds); inspect "
                f"{generated / 'mutant-certification.json'}"
            )
        if len(active_wrong) < requested_wrong:
            self.execution._log(
                f"Tiếp tục với {len(active_wrong)}/{requested_wrong} mutant đã xác nhận "
                f"({strict_verified_count} vượt sample, "
                f"{len(fallback_sample_mutants_used)} dự phòng sample chính thức)"
            )
        development_wrong, holdout_wrong = split_mutant_pool(active_wrong, self.policy.holdout_fraction)
        certification_summary["development_mutants"] = [
            solution.id for solution in development_wrong
        ]
        certification_summary["holdout_mutants"] = [
            solution.id for solution in holdout_wrong
        ]
        self.store.write_json(generated / "mutant-certification.json", certification_summary)
        candidates = [*candidate_ac, *development_wrong]

        return CandidatePool(candidates, candidate_ac, active_wrong, development_wrong,
                             holdout_wrong, certification_records, certification_summary,
                             requested_wrong, strict_verified_count,
                             fallback_sample_mutants_used, all_compiles)
