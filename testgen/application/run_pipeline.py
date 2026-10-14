"""Generate, certify, judge, and report one problem at a time."""

from __future__ import annotations
from testgen.persistence import RunStore, default_run_store, RunCheckpoint

import time
from pathlib import Path

from ..evaluation.execution import ExecutionService
from ..certification.references import ReferenceCertification
from ..certification.mutants import MutantCertification
from ..certification.mutant_pool import MutantPoolBuilder, MutantPoolPolicy
from ..application.refinement import RefinementRunner, RefinementPolicy
from ..evaluation.external import ExternalEvaluator
from ..application.resume_run import ResumeRun
from ..certification.reference_pool import ReferencePoolBuilder
from ..reporting.report_builder import build_report
from ..checker import Checker, checker_from_profile
from ..coverage import normalize_test_model
from ..domain import CaseGenerator, Judge, OracleSource, Solution, SolutionGenerator
from ..progress import ConsoleProgress


from ..problem import samples, requires_input_aware_checker, _has_sample_section

from ..evaluation.holdout import HoldoutEvaluator


from ..suite import suite_lock


class RunPipeline:
    def __init__(self, solution_generator: SolutionGenerator, case_generator: CaseGenerator,
                 judge: Judge, checker: Checker, oracle: OracleSource | None = None,
                 validator_override: Path | None = None,
                 progress: ConsoleProgress | None = None, batch_size: int = 8,
                 judge_workers: int = 1, compile_workers: int = 1,
                 input_repair_attempts: int = 2,
                 mutant_replacement_rounds: int = 4,
                 mutant_replacement_oversampling: float = 1.5,
                 mutant_witness_repair_rounds: int = 2,
                 mutant_witness_candidates: int = 2,
                 min_iterations: int = 2,
                 min_total_cases: int = 18,
                 top_up_rounds: int = 2,
                 critical_coverage_target: float = 1.0,
                 normal_coverage_target: float = 0.9,
                 stall_rounds_to_stop: int = 2,
                 holdout_fraction: float = 0.2,
                 minimum_verified_mutants: int = 3, store: RunStore | None = None,
                 auto_checker: bool = False, auto_sandbox: bool = False):
        if not 1 <= batch_size <= 32:
            raise ValueError("batch_size must be 1..32")
        if not 1 <= judge_workers <= 32:
            raise ValueError("judge_workers must be 1..32")
        if not 1 <= compile_workers <= 8:
            raise ValueError("compile_workers must be 1..8")
        if not 0 <= input_repair_attempts <= 2:
            raise ValueError("input_repair_attempts must be 0..2")
        if not 0 <= mutant_replacement_rounds <= 4:
            raise ValueError("mutant_replacement_rounds must be 0..4")
        if not 1.0 <= mutant_replacement_oversampling <= 3.0:
            raise ValueError("mutant_replacement_oversampling must be between 1 and 3")
        if not 0 <= mutant_witness_repair_rounds <= 2:
            raise ValueError("mutant_witness_repair_rounds must be 0..2")
        if not 1 <= mutant_witness_candidates <= 2:
            raise ValueError("mutant_witness_candidates must be 1..2")
        if not 1 <= min_iterations <= 3:
            raise ValueError("min_iterations must be 1..3")
        if min_total_cases < 1:
            raise ValueError("min_total_cases must be >= 1")
        if not 0 <= top_up_rounds <= 4:
            raise ValueError("top_up_rounds must be 0..4")
        if not 0 <= critical_coverage_target <= 1 or not 0 <= normal_coverage_target <= 1:
            raise ValueError("coverage targets must be between 0 and 1")
        if stall_rounds_to_stop < 1:
            raise ValueError("stall_rounds_to_stop must be >= 1")
        if not 0 <= holdout_fraction < 1:
            raise ValueError("holdout_fraction must be in [0, 1)")
        if minimum_verified_mutants < 1:
            raise ValueError("minimum_verified_mutants must be >= 1")
        self.store = store or default_run_store()
        self.solution_generator, self.case_generator = solution_generator, case_generator
        self.judge, self.checker, self.oracle = judge, checker, oracle
        self.validator_override = validator_override
        self.progress = progress
        self.batch_size = batch_size
        self.judge_workers = judge_workers
        self.compile_workers = compile_workers
        self.input_repair_attempts = input_repair_attempts
        self.mutant_replacement_rounds = mutant_replacement_rounds
        self.mutant_replacement_oversampling = mutant_replacement_oversampling
        self.mutant_witness_repair_rounds = mutant_witness_repair_rounds
        self.mutant_witness_candidates = mutant_witness_candidates
        self.min_iterations = min_iterations
        self.min_total_cases = min_total_cases
        self.top_up_rounds = top_up_rounds
        self.critical_coverage_target = critical_coverage_target
        self.normal_coverage_target = normal_coverage_target
        self.stall_rounds_to_stop = stall_rounds_to_stop
        self.holdout_fraction = holdout_fraction
        self.minimum_verified_mutants = minimum_verified_mutants
        self.auto_checker = auto_checker
        self.auto_sandbox = auto_sandbox
        self.base_cases_per_round = getattr(case_generator, "cases_per_round", 10)
        if self.base_cases_per_round < 1:
            raise ValueError("case generator base quota must be >= 1")
        self.execution = ExecutionService(judge, checker, progress, batch_size,
                                          judge_workers, compile_workers)
        self.references = ReferenceCertification(self.execution, checker)
        self.mutants = MutantCertification(self.execution, self.references, checker)

    def _apply_test_model_specs(self, test_model: dict) -> None:
        if self.auto_checker:
            spec = test_model["checker"]
            if spec.get("multiple_valid_answers") or spec.get("kind") == "PYTHON_SCRIPT":
                raise RuntimeError(
                    "The generated test model requires an input-aware special checker. "
                    "Add an audited problem-local checker.json and checker script."
                )
            kind = spec.get("kind", "TOKEN")
            if kind == "TOKEN" and not spec.get("case_sensitive", True):
                kind = "CASE_INSENSITIVE_TOKEN"
            profile = {"kind": kind}
            if kind == "FLOAT":
                profile["epsilon"] = spec.get("epsilon") or 1e-6
            checker = checker_from_profile(profile)
            self.checker = checker
            self.execution.checker = checker
            self.references.checker = checker
            self.mutants.checker = checker
            self._log(f"Áp dụng checker từ test model: {checker.profile()}")
        if self.auto_sandbox:
            configure = getattr(self.judge, "apply_sandbox_spec", None)
            if configure is not None:
                configure(test_model["sandbox"])
                spec = test_model["sandbox"]
                self._log(
                    "Áp dụng sandbox từ test model: "
                    f"time={spec['time_limit_seconds']}s, memory={spec['memory_limit_mb']}MB"
                )

    @property
    def _execution_log(self):
        return self.execution._execution_log

    @_execution_log.setter
    def _execution_log(self, value):
        self.execution._execution_log = value


    def _log(self, *args, **kwargs):
        return self.execution._log(*args, **kwargs)

    def _waiting(self, *args, **kwargs):
        return self.execution._waiting(*args, **kwargs)

    def _latency(self, *args, **kwargs):
        return self.execution._latency(*args, **kwargs)

    def _latency_report(self, *args, **kwargs):
        return self.execution._latency_report(*args, **kwargs)


    def _compile_pool(self, *args, **kwargs):
        return self.execution._compile_pool(*args, **kwargs)


    def _execute_many(self, *args, **kwargs):
        """Compatibility hook for existing execution-contract callers."""
        return self.execution._execute_many(*args, **kwargs)

    def _judge_pool(self, *args, **kwargs):
        """Compatibility hook for existing concurrency-contract callers."""
        return self.execution._judge_pool(*args, **kwargs)

    def _reference_consensus(self, *args, **kwargs):
        return self.references._reference_consensus(*args, **kwargs)

    def _reference_consensus_many(self, *args, **kwargs):
        return self.references._reference_consensus_many(*args, **kwargs)


    def _append_oracle(self, result, problem_id, output, cases, oracle_limit):
        return ExternalEvaluator(self.oracle, self.execution).evaluate(
            result, problem_id, output, cases, oracle_limit)


    def resume_oracle(self, problem_id: str, output: Path, oracle_limit: int) -> dict:
        return ResumeRun(self.store, self.execution,
                         ExternalEvaluator(self.oracle, self.execution)).run(
                             problem_id, output, oracle_limit)

    def run(self, problem_id: str, statement: str, output: Path, *,
            iterations: int = 3, oracle_limit: int = 100, use_oracle: bool = False,
            started_at: float | None = None) -> dict:
        generation_started = time.monotonic() if started_at is None else started_at
        if not 1 <= iterations <= 3:
            raise ValueError("iterations must be 1..3")
        output.mkdir(parents=True, exist_ok=True)
        self._execution_log = output / "executions-llm.jsonl"
        official_samples = samples(statement)
        if _has_sample_section(statement) and not official_samples:
            raise RuntimeError(
                "Statement contains a sample/example section, but no complete "
                "input/output pair could be parsed. Refusing to certify references "
                "without official sample checks."
            )
        test_model_path = output / "test-model.json"
        test_model = None
        if test_model_path.is_file():
            try:
                cached_test_model = normalize_test_model(
                    self.store.read_json(test_model_path)
                )
            except (OSError, TypeError, ValueError):
                cached_test_model = None
            if (cached_test_model is not None
                    and cached_test_model.get("coverage_obligations")):
                test_model = cached_test_model
                self._log("Tái sử dụng test model đã checkpoint")
        if test_model is None:
            with self._waiting("LLM xây test model độc lập từ đề bài"):
                test_model = normalize_test_model(
                    self.case_generator.build_test_model(statement)
                )
            self.store.write_json(test_model_path, test_model)
        self._apply_test_model_specs(test_model)
        if requires_input_aware_checker(statement) and not self.checker.input_aware:
            raise RuntimeError(
                "Problem statement appears to allow multiple valid outputs, but "
                f"checker {self.checker.kind} compares against one expected output. "
                "Configure an input-aware special checker in checker.json."
            )
        self._log(
            "Test model: "
            f"{len(test_model['coverage_obligations'])} coverage obligations"
        )
        generated = output / "generated"
        with self._waiting("LLM sinh code AC tuần tự và validator độc lập"):
            candidates = self.solution_generator.generate_with_model(statement, test_model, generated)
        self._log(f"Đã sinh {len(candidates)} lời giải ứng viên")
        validator = Solution("validator", "validator", "Python",
                             self.validator_override or generated / "validator.py")
        to_compile = [validator, *candidates]
        all_compiles = self._compile_pool(to_compile, "Biên dịch ứng viên")
        if all_compiles[validator.id].verdict != "PASS":
            raise RuntimeError(f"Generated validator did not compile: {all_compiles[validator.id].stderr}")
        reference_pool = ReferencePoolBuilder(
            self.solution_generator, self.execution, self.references, self.store
        ).build(statement, generated, candidates, all_compiles, official_samples)
        candidates, correct, all_compiles = (
            reference_pool.candidates, reference_pool.correct, reference_pool.compiles)

        pool = MutantPoolBuilder(
            self.solution_generator, self.execution, self.mutants,
            MutantPoolPolicy(self.mutant_replacement_rounds, self.mutant_replacement_oversampling,
                             self.mutant_witness_repair_rounds, self.mutant_witness_candidates,
                             self.minimum_verified_mutants, self.holdout_fraction), store=self.store
        ).build(statement, generated, candidates, validator, correct, all_compiles, official_samples)
        candidates = pool.candidates
        candidate_ac = pool.candidate_ac
        development_wrong = pool.development_wrong
        certification_records = pool.certification_records
        certification_summary = pool.certification_summary
        all_compiles = pool.compiles

        refinement = RefinementRunner(
            self.case_generator, self.execution, self.references, self.checker,
            RefinementPolicy(self.base_cases_per_round, self.input_repair_attempts,
                             self.top_up_rounds, self.critical_coverage_target,
                             self.normal_coverage_target, self.min_iterations,
                             self.min_total_cases, self.stall_rounds_to_stop), store=self.store
        ).run(problem_id, statement, output, iterations, test_model, validator, correct,
              candidates, candidate_ac, development_wrong, all_compiles, official_samples,
              certification_records, certification_summary)
        cases = refinement.cases
        snapshot = refinement.snapshot
        tests_dir = output / "tests"
        tests_dir.mkdir(exist_ok=True)
        for case in cases:
            self.store.write_text(tests_dir / f"{case.id}.in", case.input, encoding="utf-8")
            self.store.write_text(tests_dir / f"{case.id}.out", case.expected, encoding="utf-8")
        locked_suite = suite_lock(cases)
        self.store.write_json(output / "test-suite.lock.json", locked_suite)
        holdout = HoldoutEvaluator(self.execution).evaluate(
            pool, cases, refinement.latest, locked_suite, output)
        result = build_report(
            problem_id, refinement, pool, test_model, locked_suite, holdout.metrics,
            holdout.verdicts, judge_workers=self.judge_workers,
            compile_workers=self.compile_workers, batch_size=self.batch_size,
            latency_summary=self._latency_report())
        elapsed = time.monotonic() - generation_started
        result["generation_latency"] = {
            "elapsed_seconds": round(elapsed, 3),
            "target_seconds": 180,
            "target_met": elapsed <= 180,
            "scope": "startup through certified suite and holdout; excludes optional external oracle",
            "quality_criteria_met": snapshot["stop_criteria"]["met"],
        }
        self._latency("generation.total", generation_started,
                      target_seconds=180, target_met=elapsed <= 180)
        self.store.write_json(output / "report.json", result)
        self.store.checkpoint(output / "checkpoint.json",
                              RunCheckpoint(1, "suite_locked", problem_id, tuple(cases), result))
        if use_oracle:
            self._append_oracle(result, problem_id, output, cases, oracle_limit)
        self.store.write_json(output / "report.json", result)
        self._log(f"Đã ghi báo cáo: {output / 'report.json'}")
        return result
