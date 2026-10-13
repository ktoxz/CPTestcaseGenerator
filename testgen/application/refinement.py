"""Adaptive refinement use case; holdout and external pools are not inputs."""
from __future__ import annotations
from testgen.persistence import RunStore, default_run_store
from pathlib import Path
from dataclasses import dataclass
from ..evaluation.metrics import metrics
from ..domain import Case, Result
from ..coverage import coverage_summary
from ..policies import dynamic_case_bounds, stop_status as evaluate_stop
from ..certification.cases import CaseCertification, CaseCertificationState
from .case_proposals import CaseProposalRunner
from ..generation.feedback import record_round_feedback
from ..generation.feedback import candidate_context as build_candidate_context, feedback as build_feedback, source_feedback as build_source_feedback

@dataclass(frozen=True)
class RefinementPolicy:
    base_cases_per_round: int
    input_repair_attempts: int
    top_up_rounds: int
    critical_coverage_target: float
    normal_coverage_target: float
    min_iterations: int
    min_total_cases: int
    stall_rounds_to_stop: int

@dataclass
class RefinementState:
    previous_tnr: float | None = None
    survivor_count: int = 0
    previous_covered: int = 0
    previous_killed: int = 0
    previous_rejected_count: int = 0
    stalled_rounds: int = 0

@dataclass(frozen=True)
class RefinementResult:
    cases: list[Case]
    quarantined: list[dict]
    latest: dict[str, Result]
    coverage_state: dict
    stop_reason: str
    snapshot: dict
    candidate_contexts: dict[str, dict]
    iteration: int

def write_candidate_contexts(store, context_dir: Path, contexts: dict[str, dict]) -> None:
    candidates_dir = context_dir / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    for candidate_id, candidate_context in contexts.items():
        store.write_json(candidates_dir / f"{candidate_id}.json", candidate_context)


class RefinementRunner:
    def __init__(self, case_generator, execution, references, checker, policy: RefinementPolicy, store: RunStore | None = None):
        self.store = store or default_run_store()
        self.case_generator, self.execution, self.references = case_generator, execution, references
        self.checker, self.policy = checker, policy

    def run(self, problem_id, statement, output, iterations, test_model, validator,
            correct, candidates, candidate_ac, development_wrong, all_compiles,
            official_samples, certification_records, pool_summary) -> RefinementResult:
        requested_wrong = pool_summary["requested_wrong_candidates"]
        active_wrong_count = pool_summary["validated_wrong_candidates"]
        strict_verified_count = pool_summary["strict_sample_preserving_verified"]
        fallback_sample_mutants_used = pool_summary["official_sample_fallback_used"]
        holdout_count = len(pool_summary["holdout_mutants"])
        cases: list[Case] = []
        quarantined: list[dict] = []
        hashes: set[str] = set()
        case_intents: dict[str, dict] = {}
        context_dir = output / "context"
        audits_dir = context_dir / "audits"
        audits_dir.mkdir(parents=True, exist_ok=True)
        certification_by_id = {
            row["solution_id"]: row for row in certification_records if row["verified"]
        }
        candidate_contexts = {
            solution.id: build_candidate_context(
                solution, certification_by_id[solution.id],
                self.store.read_text(solution.source, errors="replace")
            )
            for solution in development_wrong
        }
        write_candidate_contexts(self.store, context_dir, candidate_contexts)
        feedback = build_feedback(
            None, development_wrong, [], candidate_contexts,
            cases, quarantined, [], [], test_model,
            coverage_summary(test_model, cases), {},
        )
        latest = {}
        state = RefinementState()
        state.previous_tnr = None
        state.survivor_count = len(development_wrong)
        refinement_dir = output / "refinement"
        refinement_dir.mkdir(exist_ok=True)
        state.previous_covered = 0
        state.previous_killed = 0
        state.previous_rejected_count = 0
        state.stalled_rounds = 0
        stop_reason = "iteration_limit"
        coverage_state = coverage_summary(test_model, cases)
        for iteration in range(iterations):
            self.execution._log(f"Vòng {iteration + 1}/{iterations}: sinh và chứng nhận testcase")
            coverage_before = coverage_summary(test_model, cases)
            quota_basis = {
                "survivors": state.survivor_count,
                "previous_tnr": state.previous_tnr,
                "uncovered_critical": len(coverage_before["uncovered_critical"]),
                "previous_rejected_or_duplicate": state.previous_rejected_count,
                "stalled_rounds": state.stalled_rounds,
            }
            min_cases, max_cases = dynamic_case_bounds(
                self.policy.base_cases_per_round,
                state.survivor_count,
                state.previous_tnr,
                uncovered_critical=len(coverage_before["uncovered_critical"]),
                rejected_count=state.previous_rejected_count,
                stalled_rounds=state.stalled_rounds,
            )
            feedback["coverage"] = coverage_before
            feedback["quota_basis"] = quota_basis
            self.store.write_json(refinement_dir / f"feedback-{iteration}.json", feedback)
            with self.execution._waiting(
                "LLM sinh baseline theo coverage" if iteration == 0
                else f"LLM sinh testcase thích nghi vòng {iteration + 1}"
            ):
                plan = (
                    self.case_generator.generate_baseline(
                        statement, test_model, iteration, min_cases, max_cases
                    )
                    if iteration == 0 else
                    self.case_generator.generate(
                        statement, feedback, iteration, min_cases, max_cases
                    )
                )
            if not isinstance(plan, dict):
                raise ValueError("Case generator must return a plan object")
            generated_cases = plan.get("cases", [])
            if not isinstance(generated_cases, list):
                raise ValueError("Case plan cases must be a list")
            requested_count = plan.get("requested_count", min_cases)
            if not isinstance(requested_count, int) or isinstance(requested_count, bool):
                requested_count = min_cases
            requested_count = max(min_cases, min(max_cases, requested_count))
            self.store.write_json(refinement_dir / f"case-plan-{iteration}.json", plan)
            self.execution._log(
                f"Vòng {iteration + 1}: quota accepted {min_cases}–{max_cases}, "
                f"mục tiêu {requested_count}, nhận {len(generated_cases)} đề xuất"
            )
            round_certified: list[Case] = []
            round_rejected: list[dict] = []
            accepted_generated = 0
            proposal_counter = 0

            certification_state = CaseCertificationState(
                cases, hashes, case_intents, quarantined, round_certified, round_rejected)
            case_certifier = CaseCertification(
                self.execution, self.references, self.checker, validator, correct,
                test_model, problem_id, iteration, certification_state)
            proposal_runner = CaseProposalRunner(
                case_certifier, self.case_generator, self.execution, statement,
                feedback, self.policy.input_repair_attempts)

            if iteration == 0:
                proposal_runner.certify([
                    {
                        "input": input_text,
                        "family": "official-sample",
                        "official_expected": expected,
                        "coverage_tags": [],
                    }
                    for input_text, expected in official_samples
                ], "official-sample")
            proposal_runner.certify(generated_cases[:requested_count], "initial-plan")

            for top_up_round in range(1, self.policy.top_up_rounds + 1):
                missing = requested_count - certification_state.accepted_generated
                if missing <= 0:
                    break
                top_up_feedback = build_feedback(
                    None,
                    development_wrong if iteration == 0 else [
                        solution for solution in development_wrong
                        if candidate_contexts[solution.id]["status"] in {"active", "survived"}
                    ],
                    [],
                    candidate_contexts,
                    cases,
                    quarantined,
                    round_certified,
                    round_rejected,
                    test_model,
                    coverage_summary(test_model, cases),
                    quota_basis,
                )
                top_up_feedback["top_up"] = {
                    "round": top_up_round,
                    "missing_accepted_cases": missing,
                    "instruction": (
                        "Replace rejected or duplicate proposals with distinct valid "
                        "inputs; prioritize uncovered obligations."
                    ),
                }
                with self.execution._waiting(
                    f"LLM top-up {missing} testcase vòng {iteration + 1}, "
                    f"lần {top_up_round}"
                ):
                    top_up_plan = self.case_generator.top_up(
                        statement,
                        top_up_feedback,
                        iteration,
                        missing,
                        baseline=iteration == 0,
                    )
                self.store.write_json(refinement_dir / f"case-plan-{iteration}-topup-{top_up_round}.json", top_up_plan)
                top_up_cases = top_up_plan.get("cases", []) if isinstance(top_up_plan, dict) else []
                if not isinstance(top_up_cases, list) or not top_up_cases:
                    self.execution._log("Top-up không cung cấp thêm testcase")
                    break
                gained = proposal_runner.certify(top_up_cases[:missing], f"top-up-{top_up_round}")
                if gained == 0:
                    self.execution._log("Top-up không tạo được testcase hợp lệ mới")

            if not cases:
                raise RuntimeError("No certified cases; inspect validator and references")
            self.execution._log(f"Chấm {len(candidates)} code LLM trên {len(cases)} testcase")
            latest = self.execution._judge_pool(candidates, cases, all_compiles, "LLM")
            metrics_llm = metrics(candidates, latest, "candidate_ac", "candidate_wa")
            survivors = [
                solution for solution in development_wrong
                if latest[solution.id].verdict == "PASS"
            ]
            failed_correct_solutions = [
                solution for solution in candidate_ac
                if latest[solution.id].verdict != "PASS"
            ]
            coverage_state = coverage_summary(test_model, cases)
            killed_count = len(development_wrong) - len(survivors)
            if iteration > 0:
                if (coverage_state["covered"] <= state.previous_covered
                        and killed_count <= state.previous_killed):
                    state.stalled_rounds += 1
                else:
                    state.stalled_rounds = 0
            state.previous_covered = coverage_state["covered"]
            state.previous_killed = killed_count
            self.execution._log(
                f"Vòng {iteration + 1}: TPR={metrics_llm['tpr_label_based']}, "
                f"TNR={metrics_llm['tnr_label_based']}; coverage="
                f"{coverage_state['covered']}/{coverage_state['obligations']}; "
                f"accepted={certification_state.accepted_generated}/{requested_count}; "
                f"cách ly {len(quarantined)} test"
            )

            record_round_feedback(development_wrong, candidate_contexts, round_certified,
                                  case_intents, latest, iteration, self.execution._checked_result)

            stop_status = evaluate_stop(
                metrics_llm, coverage_state, iteration=iteration, iterations=iterations,
                case_count=len(cases), survivor_count=len(survivors), stalled_rounds=state.stalled_rounds,
                min_iterations=self.policy.min_iterations, min_total_cases=self.policy.min_total_cases,
                critical_coverage_target=self.policy.critical_coverage_target,
                normal_coverage_target=self.policy.normal_coverage_target,
                stall_rounds_to_stop=self.policy.stall_rounds_to_stop)
            meets_stop_criteria = stop_status["met"]

            if not meets_stop_criteria and iteration < iterations - 1:
                if survivors:
                    with self.execution._waiting(
                        f"LLM audit batch {len(survivors)} survivor sau vòng "
                        f"{iteration + 1}"
                    ):
                        batch_audits = self.case_generator.audit_batch(
                            statement,
                            [candidate_contexts[item.id] for item in survivors],
                            iteration,
                        )
                    audits_by_id = {
                        row.get("solution_id"): row
                        for row in batch_audits if isinstance(row, dict)
                    }
                    audit_results = []
                    for survivor in survivors:
                        audit = audits_by_id.get(survivor.id, {
                            "classification": "insufficient_evidence",
                            "revised_bug_hypothesis": "",
                            "reasoning": "batch audit returned no item",
                            "confidence": 0.0,
                            "failed_hypotheses": [],
                            "counterexample": None,
                        })
                        audit_results.append((survivor, audit))
                else:
                    audit_results = []

                for survivor, audit in audit_results:
                    candidate_context = candidate_contexts[survivor.id]
                    audit_record = {"round": iteration, **audit}
                    candidate_context["audits"].append(audit_record)
                    candidate_context["latest_audit"] = audit_record
                    for hypothesis in audit.get("failed_hypotheses", []):
                        if (isinstance(hypothesis, str)
                                and hypothesis not in candidate_context["failed_hypotheses"]):
                            candidate_context["failed_hypotheses"].append(hypothesis)
                    self.store.write_json(audits_dir / f"{survivor.id}-round-{iteration}.json", audit_record)
                    self.execution._log(
                        f"Audit {survivor.id}: {audit['classification']} "
                        f"(confidence={audit['confidence']})"
                    )
            write_candidate_contexts(self.store, context_dir, candidate_contexts)
            snapshot = {
                "problem_id": problem_id,
                "iteration": iteration,
                "checker": self.checker.profile(),
                "cases": len(cases),
                "quarantined": len(quarantined),
                "llm_metrics": metrics_llm,
                "coverage": coverage_state,
                "stop_criteria": stop_status,
                "dynamic_case_quota": {
                    "minimum": min_cases,
                    "maximum": max_cases,
                    "requested": requested_count,
                    "generated": len(generated_cases),
                    "accepted": certification_state.accepted_generated,
                    "top_up_rounds": self.policy.top_up_rounds,
                    "basis": quota_basis,
                },
                "mutant_pool": {
                    "requested": requested_wrong,
                    "verified": active_wrong_count,
                    "witness_verified": strict_verified_count,
                    "official_sample_fallback": len(
                        fallback_sample_mutants_used
                    ),
                    "development": len(development_wrong),
                    "holdout": holdout_count,
                    "survivors": len(survivors),
                },
                "verdicts": {key: value.__dict__ for key, value in latest.items()},
            }
            self.store.write_json(output / f"iteration-{iteration}.json", snapshot)
            if meets_stop_criteria:
                stop_reason = "all_quality_criteria_met"
                break
            state.survivor_count = len(survivors)
            state.previous_tnr = metrics_llm["tnr_label_based"]
            state.previous_rejected_count = len(round_rejected)
            feedback = build_feedback(
                metrics_llm,
                survivors,
                [build_source_feedback(solution, latest[solution.id],
                     self.store.read_text(solution.source, errors="replace"))
                 for solution in failed_correct_solutions],
                candidate_contexts,
                cases,
                quarantined,
                round_certified,
                round_rejected,
                test_model,
                coverage_state,
                quota_basis,
            )

        return RefinementResult(cases, quarantined, latest, coverage_state, stop_reason,
                                snapshot, candidate_contexts, iteration)
