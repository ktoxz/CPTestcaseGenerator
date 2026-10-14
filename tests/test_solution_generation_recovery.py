import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from testgen.domain import Solution
from testgen.generation.solutions import SolutionGenerationService
from testgen.llm_contract import LLMTransportError


class RecoveryClient:
    def __init__(self, fail_rounds=0):
        self.fail_rounds = fail_rounds
        self.solution_calls = 0
        self.validator_calls = 0

    def ask_json(self, prompt, label="LLM"):
        if "validator" in label:
            self.validator_calls += 1
            if self.validator_calls <= self.fail_rounds:
                raise LLMTransportError("temporary validator transport failure")
            return {"validator_python": "raise SystemExit(0)", "warnings": []}
        self.solution_calls += 1
        if self.solution_calls <= self.fail_rounds:
            raise LLMTransportError("temporary solution transport failure")
        return {
            "correct": [{
                "language": "Python",
                "code": "print(1)\n",
                "strategy_id": "direct",
                "approach": "direct",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
            }],
            "wrong": [],
            "validator_python": "",
            "warnings": [],
        }


class SolutionGenerationRecoveryTests(unittest.TestCase):
    def test_uses_recovery_rounds_beyond_the_old_two_round_cap(self):
        client = RecoveryClient(fail_rounds=2)
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generated = Path(temp)
            solutions = SolutionGenerationService(
                client, ac_count=1, wa_count=0, max_rounds=5,
                retry_delay_seconds=0,
            ).generate_with_model("statement", {"warnings": []}, generated)

            self.assertEqual(len(solutions), 1)
            self.assertEqual(client.solution_calls, 3)
            self.assertEqual(client.validator_calls, 3)
            self.assertTrue((generated / "generation-round-03-ac-batch-r3.json").is_file())

    def test_resumes_valid_partial_artifacts_without_regenerating_them(self):
        client = RecoveryClient()
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generated = Path(temp)
            (generated / "generation.json").write_text(json.dumps({
                "correct": [{
                    "language": "Python",
                    "code": "print(1)\n",
                    "strategy_id": "saved",
                    "approach": "direct",
                    "time_complexity": "O(1)",
                    "space_complexity": "O(1)",
                }],
                "wrong": [],
                "validator_python": "",
                "warnings": ["saved checkpoint"],
            }), encoding="utf-8")

            solutions = SolutionGenerationService(
                client, ac_count=1, wa_count=0, max_rounds=3,
                retry_delay_seconds=0,
            ).generate_with_model("statement", {"warnings": []}, generated)

            self.assertEqual(len(solutions), 1)
            self.assertEqual(client.solution_calls, 0)
            self.assertEqual(client.validator_calls, 1)
            saved = json.loads((generated / "generation.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["correct"][0]["strategy_id"], "saved")
            self.assertEqual(saved["validator_python"], "raise SystemExit(0)")

    def test_reference_replacement_retries_transport_failure(self):
        class Client:
            def __init__(self):
                self.calls = 0

            def ask_json(self, prompt, label="LLM"):
                self.calls += 1
                if self.calls == 1:
                    raise LLMTransportError("endpoint cooling down")
                return {"correct": [{
                    "language": "Python", "code": "print(1)\n",
                    "strategy_id": "replacement",
                }]}

        client = Client()
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            replacements = SolutionGenerationService(
                client, ac_count=1, wa_count=0, retry_delay_seconds=0,
            ).regenerate_correct("statement", Path(temp), 1, [], [], 1)

            self.assertEqual(client.calls, 2)
            self.assertEqual(len(replacements), 1)

    def test_reference_replacement_reuses_accepted_checkpoint(self):
        class NoCallClient:
            def ask_json(self, prompt, label="LLM"):
                raise AssertionError("cached accepted replacement should be reused")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generated = Path(temp)
            (generated / "reference-replacement-01.json").write_text(json.dumps({
                "correct": [{
                    "language": "Python", "code": "print(1)\n",
                    "strategy_id": "cached",
                }]
            }), encoding="utf-8")
            (generated / "reference-replacement-01-validation.json").write_text(
                json.dumps({"accepted": 1}), encoding="utf-8",
            )

            replacements = SolutionGenerationService(
                NoCallClient(), ac_count=1, wa_count=0,
            ).regenerate_correct("statement", generated, 1, [], [], 1)

            self.assertEqual(len(replacements), 1)
            self.assertEqual(replacements[0].strategy_id, "cached")

    def test_mutant_recovery_switches_from_unmatched_edits_to_full_source(self):
        class Client:
            def __init__(self):
                self.prompts = []

            def ask_json(self, prompt, label="LLM"):
                self.prompts.append(prompt)
                return {"wrong": []}

        client = Client()
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generated = Path(temp)
            source = generated / "reference.py"
            source.write_text("print(1)\n", encoding="utf-8")
            reference = Solution(
                "reference", "candidate_ac", "Python", source,
                strategy_id="reference",
            )
            SolutionGenerationService(
                client, ac_count=1, wa_count=1,
            ).regenerate_wrong(
                "statement", generated, 1,
                [{"reason": "generator validation rejected: source edit must match exactly once"}],
                [reference], 1,
            )

            self.assertEqual(len(client.prompts), 2)
            self.assertTrue(all(
                "return source_code with the complete mutated program" in prompt
                for prompt in client.prompts
            ))
            self.assertTrue(all("do not return code_edits" in prompt for prompt in client.prompts))


if __name__ == "__main__":
    unittest.main()
