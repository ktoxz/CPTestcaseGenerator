"""Pure assembly of the existing report schema from completed stage results."""
from ..suite import case_record
from ..evaluation.metrics import metrics

def build_report(problem_id, refinement, pool, test_model, locked_suite,
                 holdout_metrics, holdout_verdicts, *, judge_workers, compile_workers,
                 batch_size, latency_summary):
    degradation_reasons = list(getattr(refinement, "degradation_reasons", []))
    stop_met = bool(refinement.snapshot["stop_criteria"]["met"])
    quality_status = "qualified" if stop_met and not degradation_reasons else "degraded"
    result = {"problem_id": problem_id, "iterations_used": refinement.iteration + 1,
              "quality_status": quality_status,
              "degradation_reasons": degradation_reasons,
              "oracle_status": "not_requested",
              "llm_metrics": metrics(pool.candidates, refinement.latest, "candidate_ac", "candidate_wa"),
              "llm_holdout_metrics": holdout_metrics,
              "cases": [case_record(case) for case in refinement.cases], "quarantined": refinement.quarantined,
              "llm_verdicts": {key: value.__dict__ for key, value in refinement.latest.items()},
              "llm_holdout_verdicts": {
                  key: value.__dict__ for key, value in holdout_verdicts.items()
              },
              "test_model": test_model,
              "coverage": refinement.coverage_state,
              "stop_reason": refinement.stop_reason,
              "stop_criteria": refinement.snapshot["stop_criteria"],
              "mutant_certification": pool.certification_summary,
              "candidate_contexts": refinement.candidate_contexts,
              "test_suite_lock": locked_suite,
              "experiment_protocol": {
                  "baseline_generation_pool": "statement and test model only",
                  "test_generation_pool": "LLM development candidates only",
                  "tnr_denominator": (
                      "two-trial verified development mutants; sample-preserving "
                      "preferred, official-sample fallback disclosed"
                  ),
                  "llm_holdout_pool": (
                      "two-trial verified mutants hidden until suite lock"
                  ),
                  "external_evaluation_pool": "CodeNet oracle",
                  "oracle_used_for_generation_or_refinement": False,
                  "llm_execution_log": "executions-llm.jsonl",
                  "llm_holdout_execution_log": "executions-holdout.jsonl",
                   "oracle_execution_log": "oracle/executions.jsonl",
                   "execution_concurrency": {
                       "judge_workers": judge_workers,
                       "compile_workers": compile_workers,
                       "batch_size": batch_size,
                   },
               },
              "latency": {
                  "log": "latency.jsonl",
                  "summary": latency_summary,
              }}
    return result
