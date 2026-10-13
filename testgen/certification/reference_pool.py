"""Reference pool certification and bounded replacement before mutant generation."""
from __future__ import annotations
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from ..domain import Solution, Result

@dataclass(frozen=True)
class ReferencePoolResult:
    candidates: list[Solution]
    correct: list[Solution]
    compiles: dict[str, Result]
    evidence: list[dict]

class ReferencePoolBuilder:
    def __init__(self, solution_generator, execution, references, store):
        self.solution_generator, self.execution = solution_generator, execution
        self.references, self.store = references, store

    def build(self, statement, generated, candidates, all_compiles, official_samples):
        candidates, all_compiles = list(candidates), dict(all_compiles)
        reference_candidates = [
            solution for solution in candidates if solution.label == "candidate_ac"
        ]

        def certify_reference(solution: Solution) -> tuple[dict, Solution | None]:
            return self.references.certify(solution, all_compiles[solution.id], official_samples)

        reference_workers = min(
            self.execution.judge_workers, len(reference_candidates)
        ) if reference_candidates else 1
        if reference_workers == 1:
            reference_results = [
                certify_reference(solution) for solution in reference_candidates
            ]
        else:
            self.execution._log(
                f"Chứng nhận {len(reference_candidates)} AC với "
                f"{reference_workers} worker"
            )
            with ThreadPoolExecutor(
                max_workers=reference_workers, thread_name_prefix="reference-cert"
            ) as executor:
                reference_results = list(
                    executor.map(certify_reference, reference_candidates)
                )
        reference_certification = [record for record, _ in reference_results]
        correct = [solution for _, solution in reference_results if solution is not None]

        # Consensus needs at least two certified references. Replace failed
        # candidates before aborting; the concrete LLM generator performs this
        # as sequential one-source requests.
        if len(correct) < 2:
            rejected_references = [
                record for record in reference_certification
                if not record["verified_for_consensus"]
            ]
            replacements = self.solution_generator.regenerate_correct(
                statement,
                generated,
                2 - len(correct),
                rejected_references,
                reference_candidates,
                1,
            )
            if replacements:
                replacement_compiles = self.execution._compile_pool(
                    replacements, "Biên dịch AC thay thế"
                )
                all_compiles.update(replacement_compiles)
                candidates.extend(replacements)
                reference_candidates.extend(replacements)
                replacement_results = [
                    certify_reference(solution) for solution in replacements
                ]
                reference_certification.extend(
                    record for record, _ in replacement_results
                )
                correct.extend(
                    solution for _, solution in replacement_results
                    if solution is not None
                )
        self.store.write_json(generated / "reference-certification.json", reference_certification)
        if len(correct) < 2:
            compiled_count = sum(
                row["compile_verdict"] == "PASS"
                for row in reference_certification
            )
            raise RuntimeError(
                f"Only {len(correct)}/{len(reference_candidates)} reference candidates "
                f"passed compilation and official samples ({compiled_count} compiled). "
                f"Inspect {generated / 'reference-certification.json'}"
            )

        return ReferencePoolResult(candidates, correct, all_compiles, reference_certification)
