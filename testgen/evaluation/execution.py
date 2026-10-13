from __future__ import annotations

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from dataclasses import replace

from ..domain import Case, Result, Solution


class ExecutionService:
    """Own execution batching, cache, concurrency and execution telemetry."""
    def __init__(self, judge, checker, progress=None, batch_size=8,
                 judge_workers=1, compile_workers=1):
        self.judge, self.checker, self.progress = judge, checker, progress
        self.batch_size = batch_size
        self.judge_workers, self.compile_workers = judge_workers, compile_workers
        self._execution_log = None
        self._run_cache = {}
        self._state_lock = threading.RLock()

    def _log(self, message: str) -> None:
        if self.progress:
            self.progress.log(message)


    def _waiting(self, label: str, *, component: str = "stage", **details):
        return (
            self.progress.waiting(label, component=component, **details)
            if self.progress else nullcontext()
        )


    def _latency(self, component: str, started: float, *,
                 status: str = "ok", **details) -> None:
        if self.progress:
            self.progress.latency(
                component, time.monotonic() - started, status=status, **details
            )


    def _latency_report(self) -> dict:
        return self.progress.latency_summary() if self.progress else {
            "event_count": 0, "components": {}
        }


    def _record(self, solution: Solution, case: Case, result: Result) -> None:
        if self._execution_log is None:
            return
        row = {"solution_id": solution.id, "label": solution.label, "case_id": case.id,
               "input": case.input, "expected": case.expected, "actual": result.actual,
               "stderr": result.stderr, "verdict": result.verdict}
        with self._state_lock:
            with self._execution_log.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")


    def _execute_many(self, solution: Solution, cases: list[tuple[str, str]], *,
                      purpose: str = "judge") -> list[Result]:
        started = time.monotonic()
        with self._state_lock:
            missing = [(case_id, input_text) for case_id, input_text in cases
                       if (solution.id, case_id, input_text) not in self._run_cache]
        try:
            if missing:
                results = self.judge.execute_many(solution, missing)
                if len(results) != len(missing):
                    raise RuntimeError("Judge returned an incomplete batch")
                with self._state_lock:
                    for (case_id, input_text), result in zip(missing, results):
                        self._run_cache[(solution.id, case_id, input_text)] = result
            with self._state_lock:
                returned = [self._run_cache[(solution.id, case_id, input_text)]
                            for case_id, input_text in cases]
        except BaseException:
            self._latency(
                "judge.execute_batch", started, status="error", purpose=purpose,
                solution_id=solution.id, requested=len(cases), executed=len(missing),
                cache_hits=len(cases) - len(missing),
            )
            raise
        verdicts = {
            verdict: sum(result.verdict == verdict for result in returned)
            for verdict in sorted({result.verdict for result in returned})
        }
        self._latency(
            "judge.execute_batch", started, purpose=purpose,
            solution_id=solution.id, requested=len(cases), executed=len(missing),
            cache_hits=len(cases) - len(missing), verdicts=verdicts,
        )
        return returned


    def _compile_pool(self, solutions: list[Solution], stage: str) -> dict[str, Result]:
        if not solutions:
            return {}

        def compile_one(solution: Solution) -> tuple[str, Result]:
            started = time.monotonic()
            try:
                result = self.judge.compile(solution)
            except BaseException:
                self._latency(
                    "judge.compile", started, status="error", stage=stage,
                    solution_id=solution.id, language=solution.language,
                )
                raise
            self._latency(
                "judge.compile", started, stage=stage, solution_id=solution.id,
                language=solution.language, verdict=result.verdict,
            )
            return solution.id, result

        workers = min(self.compile_workers, len(solutions))
        with self._waiting(
            f"{stage}: {len(solutions)} code với {workers} worker",
            component="judge.compile_pool", stage=stage,
            solutions=len(solutions), workers=workers,
        ):
            if workers == 1:
                compiled = [compile_one(solution) for solution in solutions]
            else:
                with ThreadPoolExecutor(
                    max_workers=workers, thread_name_prefix="compile"
                ) as executor:
                    compiled = list(executor.map(compile_one, solutions))
        results = dict(compiled)
        for index, solution in enumerate(solutions, 1):
            self._log(
                f"{stage} {index}/{len(solutions)} {solution.id}: "
                f"{results[solution.id].verdict}"
            )
        return results


    def _judge_pool(self, solutions: list[Solution], cases: list[Case],
                    compile_results: dict[str, Result], stage: str) -> dict[str, Result]:
        def judge_one(item: tuple[int, Solution]) -> tuple[str, Result]:
            index, solution = item
            started = time.monotonic()
            if compile_results[solution.id].verdict != "PASS":
                verdict = compile_results[solution.id]
                self._log(f"{stage} {index}/{len(solutions)} {solution.id}: "
                          f"{verdict.verdict}")
                self._latency(
                    "judge.solution", started, stage=stage, solution_id=solution.id,
                    cases=0, verdict=verdict.verdict,
                )
                return solution.id, verdict
            first = Result(solution.id, "PASS")
            last_update = time.monotonic()
            for offset in range(0, len(cases), self.batch_size):
                batch = cases[offset:offset + self.batch_size]
                runs = self._execute_many(
                    solution, [(case.id, case.input) for case in batch],
                    purpose=f"{stage}.candidate",
                )
                for case_index, (case, run) in enumerate(zip(batch, runs), offset + 1):
                    if run.verdict == "PASS" and not self.checker.accepts_case(
                        run.actual, case.expected, case.input
                    ):
                        run = Result(solution.id, "WA", case.id, run.actual, run.stderr)
                    self._record(solution, case, run)
                    if time.monotonic() - last_update >= 10:
                        self._log(f"{stage} {index}/{len(solutions)} {solution.id}: "
                                  f"test {case_index}/{len(cases)}")
                        last_update = time.monotonic()
                    if run.verdict != "PASS":
                        first = run
                        break
                if first.verdict != "PASS":
                    break
            self._log(f"{stage} {index}/{len(solutions)} {solution.id}: {first.verdict}")
            self._latency(
                "judge.solution", started, stage=stage, solution_id=solution.id,
                cases=len(cases), verdict=first.verdict,
            )
            return solution.id, first

        pool_started = time.monotonic()
        indexed = list(enumerate(solutions, 1))
        workers = min(self.judge_workers, len(indexed)) if indexed else 1
        if workers == 1:
            judged = [judge_one(item) for item in indexed]
        else:
            self._log(
                f"{stage}: chạy song song {len(indexed)} code với {workers} worker"
            )
            with ThreadPoolExecutor(
                max_workers=workers, thread_name_prefix="judge"
            ) as executor:
                judged = list(executor.map(judge_one, indexed))
        result = dict(judged)
        self._latency(
            "judge.pool", pool_started, stage=stage, solutions=len(solutions),
            cases=len(cases), workers=workers,
        )
        return result


    def _checked_result(self, solution: Solution, case: Case) -> Result | None:
        raw = self._run_cache.get((solution.id, case.id, case.input))
        if raw is None:
            return None
        if raw.verdict == "PASS" and not self.checker.accepts_case(
            raw.actual, case.expected, case.input
        ):
            return Result(solution.id, "WA", case.id, raw.actual, raw.stderr)
        return raw


    def alias_reference_results(self, references, validation_id, case_id, input_text):
        with self._state_lock:
            for reference in references:
                run = self._run_cache.get((reference.id, validation_id, input_text))
                if run is not None:
                    self._run_cache[(reference.id, case_id, input_text)] = replace(run, case_id=case_id)
