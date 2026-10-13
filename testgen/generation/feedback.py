"""Build adaptive feedback exclusively from development executions."""
from ..domain import Solution, Result, Case
from ..suite import case_record

def candidate_context(solution: Solution, certification: dict, source_code: str) -> dict:
    return {
        "id": solution.id,
        "label": solution.label,
        "language": solution.language,
        "bug_class": solution.bug_class,
        "strategy_id": solution.strategy_id,
        "bug_origin": solution.bug_origin,
        "failure_condition": solution.failure_condition,
        "witness_input": solution.witness_input,
        "parent_ac_id": solution.parent_ac_id,
        "mutation_operator": solution.mutation_operator,
        "target_behavior": solution.target_behavior,
        "sample_preservation_reason": solution.sample_preservation_reason,
        "source_code": source_code,
        "certification": certification,
        "status": "active",
        "attempts": [],
        "audits": [],
        "failed_hypotheses": [],
    }


def feedback(
    metrics_llm: dict | None,
    survivors: list[Solution],
    failed_correct: list[dict],
    contexts: dict[str, dict],
    all_cases: list[Case],
    all_rejected: list[dict],
    round_certified: list[Case],
    round_rejected: list[dict],
    test_model: dict,
    coverage: dict,
    quota_basis: dict | None = None,
) -> dict:
    return {
        "context_version": 3,
        "provenance": "LLM candidates and LLM-stage executions only",
        "oracle_used": False,
        "instruction": (
            "Use accumulated evidence. Do not repeat a failed hypothesis. "
            "If an audit says likely_equivalent or nondeterministic_ub, do "
            "not keep producing the same test family."
        ),
        "generation_mode": "adaptive_fault_and_coverage",
        "test_model": test_model,
        "coverage": coverage,
        "quota_basis": quota_basis or {},
        "metrics": metrics_llm,
        "surviving_wrong_candidates": [contexts[s.id] for s in survivors],
        "failed_correct_candidates": failed_correct,
        "previous_round": {
            "certified_tests": [case_record(case) for case in round_certified],
            "rejected_tests": round_rejected,
        },
        "experiment_history": {
            "certified_tests": [case_record(case) for case in all_cases],
            "rejected_tests": all_rejected,
        },
    }


def source_feedback(solution: Solution, result: Result, source_code: str) -> dict:
    return {
        "id": solution.id,
        "label": solution.label,
        "language": solution.language,
        "bug_class": solution.bug_class,
        "verdict": result.verdict,
        "first_failing_case": result.case_id,
        "source_code": source_code,
    }


def record_round_feedback(development_wrong, candidate_contexts, round_certified,
                          case_intents, latest, iteration, checked_result):
    """Update only development candidate history from already cached results."""
    for solution in development_wrong:
        candidate_context = candidate_contexts[solution.id]
        known_case_ids = {
            attempt["case_id"] for attempt in candidate_context["attempts"]
        }
        for case in round_certified:
            checked = checked_result(solution, case)
            if checked is None or case.id in known_case_ids:
                continue
            intent = case_intents.get(case.id, {})
            targets = intent.get("target_solution_ids", [])
            targeted = solution.id in targets
            killed = checked.verdict != "PASS"
            lesson = (
                f"Candidate was distinguished: expected {case.expected!r}, "
                f"observed verdict={checked.verdict}, output={checked.actual!r}."
                if killed else
                f"Targeted prediction failed: candidate output "
                f"{checked.actual!r} matched expected {case.expected!r}."
                if targeted else
                f"Candidate matched expected output {case.expected!r} on "
                "this general coverage test."
            )
            candidate_context["attempts"].append({
                "round": iteration,
                "case_id": case.id,
                "family": case.family,
                "coverage_tags": list(case.coverage_tags),
                "targeted": targeted,
                "target_solution_ids": targets,
                "hypothesis_id": intent.get("hypothesis_id", ""),
                "input": case.input,
                "predicted_expected": intent.get("predicted_expected", ""),
                "predicted_candidate_output": intent.get(
                    "predicted_candidate_output", ""
                ),
                "reason_for_difference": intent.get(
                    "reason_for_difference", ""
                ),
                "observed_expected": case.expected,
                "observed_candidate_output": checked.actual,
                "observed_verdict": checked.verdict,
                "killed": killed,
                "lesson": lesson,
            })
        result_for_candidate = latest[solution.id]
        candidate_context["status"] = (
            "survived" if result_for_candidate.verdict == "PASS" else "killed"
        )
        candidate_context["first_failing_case"] = result_for_candidate.case_id

