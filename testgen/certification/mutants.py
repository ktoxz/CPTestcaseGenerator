from __future__ import annotations

import hashlib
import time

from ..domain import Result, Solution


class MutantCertification:
    """Certify stable witness failures; CE/INFRA never constitute evidence."""
    def __init__(self, execution, references, checker):
        self.execution, self.references, self.checker = execution, references, checker

    def _certify_mutant(
        self,
        solution: Solution,
        validator: Solution,
        correct: list[Solution],
        compile_result: Result,
        official_samples: list[tuple[str, str]],
        witness_input: str | None = None,
        certified_samples: list[dict] | None = None,
    ) -> dict:
        started = time.monotonic()
        selected_witness = (
            solution.witness_input if witness_input is None else witness_input
        )
        evidence = {
            "solution_id": solution.id,
            "strategy_id": solution.strategy_id,
            "bug_class": solution.bug_class,
            "bug_origin": solution.bug_origin,
            "failure_condition": solution.failure_condition,
            "witness_input": selected_witness,
            "parent_ac_id": solution.parent_ac_id,
            "mutation_operator": solution.mutation_operator,
            "target_behavior": solution.target_behavior,
            "sample_preservation_reason": solution.sample_preservation_reason,
            "verified": False,
            "fallback_verified": False,
            "verification_tier": "unverified",
            "promoted_to_minimum_pool": False,
            "reason": "",
            "validator_verdict": None,
            "reference_expected": None,
            "candidate_verdict": None,
            "candidate_actual": None,
            "candidate_trials": [],
            "official_samples": [],
            "official_samples_passed": False,
        }

        def finish() -> dict:
            evidence["latency_ms"] = round(
                (time.monotonic() - started) * 1000, 3
            )
            self.execution._latency(
                "mutant.certify", started, solution_id=solution.id,
                verified=evidence["verified"], reason=evidence["reason"],
            )
            return evidence

        if compile_result.verdict != "PASS":
            evidence["reason"] = f"candidate compile verdict {compile_result.verdict}"
            return finish()
        evidence["official_samples"] = (
            certified_samples
            if certified_samples is not None
            else self.references._sample_results(
                solution, official_samples, f"mutant-certification-{solution.id}"
            )
        )
        evidence["official_samples_passed"] = all(
            row["accepted"] for row in evidence["official_samples"]
        )
        if not evidence["official_samples_passed"]:
            # A mutant that deterministically fails a published sample is
            # indisputably wrong, even though it is less useful than a hard
            # sample-preserving mutant. Keep it as a last-resort reserve so a
            # weak LLM batch cannot abort the whole pipeline after all
            # replacement rounds. Two fresh trials protect the pool from
            # flaky/undefined behaviour; INFRA and CE are never accepted.
            failed_sample = next(
                row for row in evidence["official_samples"]
                if not row["accepted"]
            )
            input_text = str(failed_sample["input"]).rstrip() + "\n"
            expected = str(failed_sample["expected"])
            sample_number = failed_sample["sample"]
            case_id = f"official-sample-witness-{solution.id}-{sample_number}"
            evidence["witness_input"] = input_text
            evidence["validator_verdict"] = "OFFICIAL_SAMPLE"
            evidence["reference_expected"] = expected
            runs = [
                self.execution._execute_many(
                    solution, [(case_id + f"-trial-{trial}", input_text)],
                    purpose="mutant.official_sample_trial",
                )[0]
                for trial in (1, 2)
            ]
            evidence["candidate_trials"] = [
                {"verdict": run.verdict, "actual": run.actual,
                 "stderr": run.stderr}
                for run in runs
            ]
            evidence["candidate_verdict"] = runs[0].verdict
            evidence["candidate_actual"] = runs[0].actual

            def fails_sample(run: Result) -> bool:
                return (
                    run.verdict in {"WA", "RE", "TLE"}
                    or (
                        run.verdict == "PASS"
                        and not self.checker.accepts_case(
                            run.actual, expected, input_text
                        )
                    )
                )

            stable_signature = all(
                (run.verdict, run.actual if run.verdict == "PASS" else "")
                == (
                    runs[0].verdict,
                    runs[0].actual if runs[0].verdict == "PASS" else "",
                )
                for run in runs[1:]
            )
            if all(fails_sample(run) for run in runs) and stable_signature:
                evidence["fallback_verified"] = True
                evidence["verification_tier"] = "official_sample_fallback"
                evidence["reason"] = (
                    "official sample produced the same deterministic failure "
                    "in two trials"
                )
            elif any(run.verdict in {"INFRA", "CE"} for run in runs):
                evidence["reason"] = (
                    "official-sample verification contained CE/INFRA"
                )
            elif all(fails_sample(run) for run in runs):
                evidence["reason"] = (
                    "official-sample failure was not stable across two trials"
                )
            else:
                evidence["reason"] = (
                    "candidate failed an official sample initially but the "
                    "failure was not reproduced"
                )
            return finish()
        if not selected_witness.strip():
            evidence["reason"] = "missing witness_input"
            return finish()
        input_text = selected_witness.rstrip() + "\n"
        witness_hash = hashlib.sha256(input_text.encode()).hexdigest()[:12]
        case_id = f"witness-{solution.id}-{witness_hash}"
        validation = self.execution._execute_many(
            validator, [(case_id + "-validator", input_text)],
            purpose="mutant.validator",
        )[0]
        evidence["validator_verdict"] = validation.verdict
        if validation.verdict != "PASS":
            evidence["reason"] = "witness rejected by validator"
            return finish()
        consensus = self.references._reference_consensus(
            correct, case_id + "-reference", input_text
        )
        if consensus is None:
            evidence["reason"] = "references did not agree on witness"
            return finish()
        evidence["reference_expected"] = consensus.actual
        runs = [
            self.execution._execute_many(
                solution, [(case_id + f"-trial-{trial}", input_text)],
                purpose="mutant.candidate_trial",
            )[0]
            for trial in (1, 2)
        ]
        evidence["candidate_trials"] = [
            {"verdict": run.verdict, "actual": run.actual, "stderr": run.stderr}
            for run in runs
        ]
        evidence["candidate_verdict"] = runs[0].verdict
        evidence["candidate_actual"] = runs[0].actual

        def kills(run: Result) -> bool:
            return (
                run.verdict in {"WA", "RE", "TLE"}
                or (run.verdict == "PASS"
                    and not self.checker.accepts_case(
                        run.actual, consensus.actual, input_text
                    ))
            )

        stable_signature = all(
            (run.verdict, run.actual if run.verdict == "PASS" else "")
            == (runs[0].verdict,
                runs[0].actual if runs[0].verdict == "PASS" else "")
            for run in runs[1:]
        )
        if all(kills(run) for run in runs) and stable_signature:
            evidence["verified"] = True
            evidence["verification_tier"] = "sample_preserving_witness"
            evidence["reason"] = (
                "witness produced the same deterministic failure in two trials"
            )
        elif any(run.verdict in {"INFRA", "CE"} for run in runs):
            evidence["reason"] = "witness evaluation contained CE/INFRA"
        elif all(kills(run) for run in runs):
            evidence["reason"] = "witness failure was not stable across two trials"
        else:
            evidence["reason"] = (
                "witness did not distinguish candidate from references in both trials"
            )
        return finish()

