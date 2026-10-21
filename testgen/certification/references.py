from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor

from ..domain import Result, Solution


class ReferenceCertification:
    """Official sample checks and ordered reference quorum, independent of candidates."""
    def __init__(self, execution, checker):
        self.execution, self.checker = execution, checker

    def certify(self, solution, compile_result, official_samples):
        sample_results = (self._sample_results(
            solution, official_samples, f"reference-certification-{solution.id}"
        ) if compile_result.verdict == "PASS" else [])
        verified = compile_result.verdict == "PASS" and all(
            row["accepted"] for row in sample_results)
        return {
            "solution_id": solution.id,
            "compile_verdict": compile_result.verdict,
            "official_samples": sample_results,
            "verified_for_consensus": verified,
        }, solution if verified else None

    def _reference_consensus(
        self, correct: list[Solution], case_id: str, input_text: str
    ) -> Result | None:
        started = time.monotonic()
        runs: list[Result] = []
        consensus = None
        # Two independently generated references are sufficient for the
        # pipeline's consensus rule. Evaluate the first pair progressively so
        # the common case does not pay for every available reference. If that
        # pair disagrees or fails, evaluate the full pool before applying the
        # original first-reference-with-quorum selection rule; this preserves
        # deterministic behavior in ambiguous multi-cluster cases.
        for solution in correct:
            run = self.execution._execute_many(
                solution, [(case_id, input_text)], purpose="reference.consensus"
            )[0]
            runs.append(run)
            if (
                len(runs) == 2
                and runs[0].verdict == "PASS"
                and run.verdict == "PASS"
                and self.checker.accepts_case(
                    run.actual,
                    (runs[0].actual
                     if self.checker.requires_expected_output else None),
                    input_text,
                )
            ):
                consensus = run
                break
        if consensus is None:
            consensus = next((
                run for run in runs
                if run.verdict == "PASS"
                and sum(
                    other.verdict == "PASS"
                    and self.checker.accepts_case(
                        other.actual,
                        (run.actual
                         if self.checker.requires_expected_output else None),
                        input_text,
                    )
                    for other in runs
                ) >= 2
            ), None)
        self.execution._latency(
            "reference.consensus", started, case_id=case_id,
            references=len(runs), available_references=len(correct),
            early_stopped=len(runs) < len(correct),
            agreed=consensus is not None,
        )
        return consensus


    def _reference_consensus_many(
        self, correct: list[Solution], jobs: list[tuple[str, str]]
    ) -> dict[str, Result | None]:
        """Batch the common agreeing pair, retaining the original quorum rule."""
        if not jobs:
            return {}

        def prime(solution: Solution) -> None:
            for offset in range(0, len(jobs), self.execution.batch_size):
                self.execution._execute_many(
                    solution, jobs[offset:offset + self.execution.batch_size],
                    purpose="reference.consensus_batch",
                )

        pair = correct[:2]
        if self.execution.judge_workers > 1 and len(pair) > 1:
            with ThreadPoolExecutor(max_workers=2) as executor:
                list(executor.map(prime, pair))
        else:
            for solution in pair:
                prime(solution)
        return {
            case_id: self._reference_consensus(correct, case_id, input_text)
            for case_id, input_text in jobs
        }


    def _sample_results(
        self,
        solution: Solution,
        official_samples: list[tuple[str, str]],
        prefix: str,
    ) -> list[dict]:
        rows = []
        for index, (input_text, expected) in enumerate(official_samples, 1):
            case_id = f"{prefix}-sample-{index}"
            run = self.execution._execute_many(
                solution, [(case_id, input_text)], purpose="reference.sample"
            )[0]
            accepted = run.verdict == "PASS" and self.checker.accepts_case(
                run.actual,
                expected if self.checker.requires_expected_output else None,
                input_text,
            )
            rows.append({
                "sample": index,
                "input": input_text,
                "expected": expected,
                "verdict": run.verdict,
                "actual": run.actual,
                "accepted": accepted,
            })
        return rows

