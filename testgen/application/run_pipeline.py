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
from ..checkers.generated_python import (
    GeneratedCheckerSafetyError, strip_unused_imports,
    validate_generated_checker_source,
)
from ..coverage import coverage_summary, normalize_test_model
from ..evaluation.metrics import metrics
from ..llm_contract import LLMResponseError, LLMTransportError
from ..throttle import EndpointBusyError
from ..generation.test_model import _statement_sandbox_limits
from ..domain import Case, CaseGenerator, Judge, OracleSource, Solution, SolutionGenerator
from ..progress import ConsoleProgress


from ..problem import samples, requires_input_aware_checker, _has_sample_section

from ..evaluation.holdout import HoldoutEvaluator


from ..suite import case_record, suite_lock


DEGRADABLE_PIPELINE_ERRORS = (
    LLMTransportError,
    LLMResponseError,
    EndpointBusyError,
    TimeoutError,
    ConnectionError,
    OSError,
    RuntimeError,
)


class CheckerProvisioningError(RuntimeError):
    """A multiple-answer problem has no certified input-aware checker."""


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
        self.output_checker_certification: dict | None = None
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
                if not self.checker.input_aware:
                    raise CheckerProvisioningError(
                        "The generated test model requires an audited problem-local "
                        "checker, but checker provisioning did not produce one."
                    )
            else:
                kind = spec.get("kind", "TOKEN")
                if kind == "TOKEN" and not spec.get("case_sensitive", True):
                    kind = "CASE_INSENSITIVE_TOKEN"
                profile = {"kind": kind}
                if kind == "FLOAT":
                    profile["epsilon"] = spec.get("epsilon") or 1e-6
                checker = checker_from_profile(profile)
                self._set_checker(checker)
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

    def _set_checker(self, checker: Checker) -> None:
        self.checker = checker
        self.execution.checker = checker
        self.references.checker = checker
        self.mutants.checker = checker

    @staticmethod
    def _checker_source(value: object) -> str:
        if not isinstance(value, str):
            raise CheckerProvisioningError("LLM checker_python must be a string")
        source = value.strip()
        if source.startswith("```"):
            source = source.split("\n", 1)[1] if "\n" in source else ""
            if source.rstrip().endswith("```"):
                source = source.rstrip()[:-3].rstrip()
        return strip_unused_imports(source + "\n")

    def _ensure_output_checker(
        self,
        statement: str,
        test_model: dict,
        official_samples: list[tuple[str, str]],
        output: Path,
    ) -> None:
        spec = test_model.get("checker", {})
        requires_special = (
            requires_input_aware_checker(statement)
            or spec.get("multiple_valid_answers") is True
            or spec.get("kind") == "PYTHON_SCRIPT"
        )
        if not requires_special or self.checker.input_aware:
            return
        generated_dir = output / "generated"
        generated_dir.mkdir(parents=True, exist_ok=True)
        certification_path = generated_dir / "checker-certification.json"
        if not official_samples:
            raise CheckerProvisioningError(
                "Cannot certify an input-aware special checker without official "
                "samples"
            )
        rejection_feedback: list[dict] = []
        last_reason = "unknown checker certification failure"
        for attempt in range(1, 4):
            with self._waiting(
                f"LLM sinh input-aware output checker (lần {attempt}/3)"
            ):
                try:
                    candidate = self.case_generator.generate_output_checker(
                        statement, test_model, official_samples,
                        rejection_feedback=rejection_feedback,
                    )
                except NotImplementedError as error:
                    raise CheckerProvisioningError(str(error)) from error
            requires_expected_output = (
                candidate.get("requires_expected_output")
                if isinstance(candidate, dict) else None
            )
            if not isinstance(requires_expected_output, bool):
                last_reason = (
                    "LLM checker requires requires_expected_output as a boolean"
                )
                rejection_feedback.append({
                    "attempt": attempt, "stage": "contract",
                    "reason": last_reason,
                })
                self.store.write_json(certification_path, {
                    "status": "retrying" if attempt < 3 else "rejected",
                    "attempts": rejection_feedback,
                })
                continue
            try:
                source = self._checker_source(
                    candidate.get("checker_python")
                    if isinstance(candidate, dict) else None
                )
                validate_generated_checker_source(
                    source, allow_expected=requires_expected_output
                )
            except (CheckerProvisioningError, GeneratedCheckerSafetyError) as error:
                last_reason = str(error)
                rejection_feedback.append({
                    "attempt": attempt, "stage": "static_safety",
                    "reason": last_reason,
                })
                self.store.write_json(certification_path, {
                    "status": "retrying" if attempt < 3 else "rejected",
                    "attempts": rejection_feedback,
                })
                continue

            checker_path = generated_dir / "output_checker.py"
            self.store.write_text(checker_path, source, encoding="utf-8")
            checker = checker_from_profile({
                "kind": "GENERATED_PYTHON_SCRIPT",
                "script": str(checker_path.resolve()),
                "function": "accepts",
                "timeout_seconds": 2.0,
                "requires_expected_output": requires_expected_output,
            })
            probes = []
            accepted = True
            for index, (input_text, expected) in enumerate(official_samples, 1):
                checker_expected = (
                    expected if requires_expected_output else None
                )
                official_ok = checker.accepts_case(
                    expected, checker_expected, input_text
                )
                deterministic_ok = checker.accepts_case(
                    expected, checker_expected, input_text
                )
                invalid_outputs = [
                    "__invalid_output__\n",
                    expected.rstrip() + "\n__extra_invalid_token__\n",
                ]
                rejected_invalid = [
                    not checker.accepts_case(value, checker_expected, input_text)
                    for value in invalid_outputs
                ]
                row_ok = official_ok and deterministic_ok and all(rejected_invalid)
                accepted = accepted and row_ok
                probes.append({
                    "sample": index,
                    "official_output_accepted": official_ok,
                    "deterministic_repeat_accepted": deterministic_ok,
                    "invalid_outputs_rejected": rejected_invalid,
                    "passed": row_ok,
                })
            certification = {
                "status": "accepted" if accepted else "rejected",
                "trust": "generated_unreviewed",
                "attempt": attempt,
                "checker": checker.profile(),
                "requires_expected_output": requires_expected_output,
                "reasoning": candidate.get("reasoning", ""),
                "probes": probes,
                "rejected_attempts": rejection_feedback,
            }
            self.store.write_json(certification_path, certification)
            if accepted:
                self._set_checker(checker)
                self.output_checker_certification = certification
                self._log(
                    "Áp dụng checker do LLM sinh, đã qua static safety và "
                    "sample probes "
                    f"(requires_expected_output={requires_expected_output}, "
                    "trust=generated_unreviewed)"
                )
                return
            last_reason = "generated checker failed official/negative probes"
            rejection_feedback.append({
                "attempt": attempt, "stage": "sample_probes",
                "reason": last_reason, "probes": probes,
            })
        raise CheckerProvisioningError(
            f"Could not certify an LLM-generated output checker after 3 attempts: "
            f"{last_reason}. Inspect {certification_path}"
        )

    def _restore_generated_checker(self, output: Path) -> bool:
        checker_path = output / "generated" / "output_checker.py"
        certification_path = output / "generated" / "checker-certification.json"
        if not checker_path.is_file() or not certification_path.is_file():
            return False
        try:
            certification = self.store.read_json(certification_path)
            if certification.get("status") != "accepted":
                return False
            requires_expected_output = certification.get(
                "requires_expected_output", False
            )
            if not isinstance(requires_expected_output, bool):
                return False
            checker = checker_from_profile({
                "kind": "GENERATED_PYTHON_SCRIPT",
                "script": str(checker_path.resolve()),
                "function": "accepts",
                "timeout_seconds": 2.0,
                "requires_expected_output": requires_expected_output,
            })
        except (OSError, TypeError, ValueError):
            return False
        self._set_checker(checker)
        self.output_checker_certification = certification
        return True

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


    def resume_oracle(self, problem_id: str, output: Path, oracle_limit: int,
                      statement: str | None = None) -> dict:
        self._restore_generated_checker(output)
        if statement is not None:
            model_path = output / "test-model.json"
            raw_model = self.store.read_json(model_path) if model_path.is_file() else {}
            model = normalize_test_model(raw_model)
            model["sandbox"].update(_statement_sandbox_limits(statement))
            self._apply_test_model_specs(model)
        return ResumeRun(self.store, self.execution,
                         ExternalEvaluator(self.oracle, self.execution)).run(
                             problem_id, output, oracle_limit)

    @staticmethod
    def _degradation_reason(stage: str, error: BaseException) -> dict:
        return {
            "stage": stage,
            "error_type": type(error).__name__,
            "message": str(error),
        }

    def _write_cases_and_lock(self, output: Path, cases: list[Case]) -> dict:
        tests_dir = output / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        for case in cases:
            self.store.write_text(
                tests_dir / f"{case.id}.in", case.input, encoding="utf-8"
            )
            expected_path = tests_dir / f"{case.id}.out"
            if case.expected is None:
                if expected_path.is_file():
                    expected_path.unlink()
            else:
                self.store.write_text(
                    expected_path, case.expected, encoding="utf-8"
                )
        locked_suite = suite_lock(cases)
        self.store.write_json(output / "test-suite.lock.json", locked_suite)
        return locked_suite

    def _append_oracle_safely(
        self, result: dict, problem_id: str, output: Path,
        cases: list[Case], oracle_limit: int,
    ) -> None:
        result["oracle_status"] = "running"
        try:
            self._append_oracle(result, problem_id, output, cases, oracle_limit)
        except (RuntimeError, ValueError, TimeoutError, OSError,
                ConnectionError) as error:
            result["oracle_status"] = "failed"
            result["quality_status"] = "degraded"
            result.setdefault("degradation_reasons", []).append(
                self._degradation_reason("oracle", error)
            )
            self._log(
                f"Oracle lỗi; vẫn giữ test suite đã khóa: "
                f"{type(error).__name__}: {error}"
            )
        else:
            result["oracle_status"] = "completed"

    def _degraded_from_official_samples(
        self, problem_id: str, statement: str, output: Path,
        official_samples: list[tuple[str, str]], error: BaseException,
        *, use_oracle: bool, oracle_limit: int, generation_started: float,
    ) -> dict:
        cases = [
            Case(
                f"{problem_id}_official_{index:03d}",
                input_text.rstrip("\n") + "\n",
                (
                    expected.rstrip("\n") + "\n"
                    if self.checker.requires_expected_output else None
                ),
                "official-sample",
                0,
            )
            for index, (input_text, expected) in enumerate(official_samples, 1)
        ]
        locked_suite = self._write_cases_and_lock(output, cases)
        model_path = output / "test-model.json"
        try:
            test_model = normalize_test_model(
                self.store.read_json(model_path) if model_path.is_file() else {}
            )
        except (OSError, TypeError, ValueError):
            test_model = normalize_test_model({})
        checker_unavailable = isinstance(error, CheckerProvisioningError)
        reason = self._degradation_reason(
            "checker_provisioning" if checker_unavailable else "generation", error
        )
        stop_criteria = {
            "met": False,
            "reason": "generation_failed_official_samples_preserved",
        }
        result = {
            "problem_id": problem_id,
            "iterations_used": 0,
            "quality_status": "degraded",
            "degradation_reasons": [reason],
            "oracle_status": "not_requested",
            "llm_metrics": metrics([], {}, "candidate_ac", "candidate_wa"),
            "llm_holdout_metrics": metrics([], {}, "candidate_ac", "candidate_wa"),
            "cases": [case_record(case) for case in cases],
            "quarantined": [],
            "llm_verdicts": {},
            "llm_holdout_verdicts": {},
            "test_model": test_model,
            "coverage": coverage_summary(test_model, cases),
            "stop_reason": "degraded_official_samples",
            "stop_criteria": stop_criteria,
            "mutant_certification": {
                "stage_status": "skipped_due_to_degraded_generation",
                "requested_wrong_candidates": 0,
                "validated_wrong_candidates": 0,
                "strict_sample_preserving_verified": 0,
                "official_sample_fallback_used": [],
                "holdout_mutants": [],
            },
            "candidate_contexts": {},
            "test_suite_lock": locked_suite,
            "experiment_protocol": {
                "baseline_generation_pool": "statement and test model only",
                "test_generation_pool": "official samples only after generation failure",
                "external_evaluation_pool": "CodeNet oracle",
                "oracle_used_for_generation_or_refinement": False,
                "llm_execution_log": "executions-llm.jsonl",
                "oracle_execution_log": "oracle/executions.jsonl",
                "degraded_fallback": "official samples copied verbatim and suite locked",
            },
            "latency": {"log": "latency.jsonl", "summary": self._latency_report()},
        }
        if checker_unavailable:
            result["output_checker"] = {
                "status": "uncertified",
                "trust": "none",
                "reason": str(error),
            }
        elapsed = time.monotonic() - generation_started
        result["generation_latency"] = {
            "elapsed_seconds": round(elapsed, 3),
            "target_seconds": 180,
            "target_met": elapsed <= 180,
            "scope": "startup through locked degraded official-sample suite",
            "quality_criteria_met": False,
        }
        self.store.write_json(output / "report.json", result)
        self.store.checkpoint(
            output / "checkpoint.json",
            RunCheckpoint(1, "suite_locked", problem_id, tuple(cases), result),
        )
        if use_oracle and not checker_unavailable:
            self._append_oracle_safely(
                result, problem_id, output, cases, oracle_limit
            )
        elif use_oracle:
            result["oracle_status"] = "skipped_uncertified_checker"
        self.store.write_json(output / "report.json", result)
        self._log(
            f"Degraded: trả {len(cases)} official testcase; "
            f"báo cáo={output / 'report.json'}"
        )
        return result

    def run(self, problem_id: str, statement: str, output: Path, *,
            iterations: int = 3, oracle_limit: int = 100, use_oracle: bool = False,
            started_at: float | None = None) -> dict:
        generation_started = time.monotonic() if started_at is None else started_at
        try:
            return self._run_primary(
                problem_id, statement, output, iterations=iterations,
                oracle_limit=oracle_limit, use_oracle=use_oracle,
                started_at=generation_started,
            )
        except DEGRADABLE_PIPELINE_ERRORS as error:
            official_samples = samples(statement)
            if not official_samples:
                raise
            output.mkdir(parents=True, exist_ok=True)
            self._execution_log = output / "executions-llm.jsonl"
            self._log(
                f"Pipeline generation lỗi; chuyển sang official-sample degraded: "
                f"{type(error).__name__}: {error}"
            )
            return self._degraded_from_official_samples(
                problem_id, statement, output, official_samples, error,
                use_oracle=use_oracle, oracle_limit=oracle_limit,
                generation_started=generation_started,
            )

    def _run_primary(self, problem_id: str, statement: str, output: Path, *,
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
        self._ensure_output_checker(statement, test_model, official_samples, output)
        self._apply_test_model_specs(test_model)
        if requires_input_aware_checker(statement) and not self.checker.input_aware:
            raise CheckerProvisioningError(
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
        generation_path = generated / "generation.json"
        if self.validator_override is None and generation_path.is_file():
            generation_payload = self.store.read_json(generation_path)
            probes = generation_payload.get("validator_semantic_probes", [])
            if probes:
                valid_probes = [
                    probe for probe in probes
                    if isinstance(probe, dict)
                    and isinstance(probe.get("input"), str)
                    and isinstance(probe.get("rule"), str)
                ]
                jobs = [
                    (f"validator-semantic-probe-{index:03d}", probe["input"])
                    for index, probe in enumerate(valid_probes, 1)
                ]
                results = self.execution._execute_many(
                    validator, jobs, purpose="validator.semantic_probe"
                )
                audit = [
                    {
                        "case_id": result.case_id,
                        "rule": probe.get("rule", ""),
                        "verdict": result.verdict,
                        # Validators signal invalid input with a deliberate
                        # non-zero exit (RE). INFRA/TLE are audit failures, not
                        # successful rejection evidence.
                        "rejected": result.verdict == "RE",
                        "stderr": result.stderr,
                    }
                    for probe, result in zip(valid_probes, results)
                ]
                self.store.write_json(generated / "validator-semantic-audit.json", audit)
                accepted_invalid = [row for row in audit if not row["rejected"]]
                if accepted_invalid:
                    rules = "; ".join(
                        row["rule"] for row in accepted_invalid[:3]
                    )
                    raise RuntimeError(
                        "Generated validator accepted semantic-invalid probes: " + rules
                    )
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
        locked_suite = self._write_cases_and_lock(output, cases)
        holdout = HoldoutEvaluator(self.execution).evaluate(
            pool, cases, refinement.latest, locked_suite, output)
        result = build_report(
            problem_id, refinement, pool, test_model, locked_suite, holdout.metrics,
            holdout.verdicts, judge_workers=self.judge_workers,
            compile_workers=self.compile_workers, batch_size=self.batch_size,
            latency_summary=self._latency_report())
        if self.output_checker_certification is not None:
            result["output_checker"] = self.output_checker_certification
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
            self._append_oracle_safely(
                result, problem_id, output, cases, oracle_limit
            )
        self.store.write_json(output / "report.json", result)
        self._log(f"Đã ghi báo cáo: {output / 'report.json'}")
        return result
