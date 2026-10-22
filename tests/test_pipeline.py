from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import importlib.util
import io
import json
import threading
from contextlib import redirect_stderr

from testgen.checker import Checker, checker_from_profile, register_checker
from testgen.coverage import coverage_summary, normalize_test_model
from testgen.domain import Case, CaseGenerator, Judge, OracleSource, Result, Solution, SolutionGenerator
from testgen.pipeline import Pipeline, dynamic_case_bounds, metrics, samples, merge_certified_coverage
from testgen.progress import ConsoleProgress
from testgen.llm_contract import LLMTransportError
from testgen.runtime import RuntimeCatalog


class FakeSolutions(SolutionGenerator):
    def generate(self, statement: str, output: Path) -> list[Solution]:
        output.mkdir(parents=True)
        (output / "validator.py").write_text("# fake", encoding="utf-8")
        return [Solution("ac1", "candidate_ac", "Python", output / "validator.py"),
                Solution("ac2", "candidate_ac", "Python", output / "validator.py"),
                Solution("wa1", "candidate_wa", "Python", output / "validator.py",
                         bug_class="off-by-one", strategy_id="wa-1",
                         bug_origin="intentional",
                         failure_condition="returns 2 instead of 1",
                         witness_input="1 2\n")]


class FakeCases(CaseGenerator):
    cases_per_round = 10

    def generate(self, statement: str, feedback: dict, iteration: int,
                 min_cases: int, max_cases: int) -> dict:
        return {"requested_count": 1, "rationale": "fake",
                "cases": [{"input": "1 2\n", "family": "boundary"}]}


class FakeJudge(Judge):
    def compile(self, solution: Solution) -> Result:
        return Result(solution.id, "PASS")

    def execute(self, solution: Solution, case_id: str, input_text: str) -> Result:
        if solution.id == "validator":
            return Result(solution.id, "PASS", case_id)
        return Result(solution.id, "PASS", case_id,
                      "2.000\n" if solution.id == "wa1" else "1.000\n")


class PipelineTests(unittest.TestCase):
    def test_validator_must_reject_generated_semantic_probes(self):
        class ProbedSolutions(FakeSolutions):
            def generate(self, statement, output):
                solutions = super().generate(statement, output)
                (output / "generation.json").write_text(json.dumps({
                    "validator_semantic_probes": [{
                        "input": "unreachable\n",
                        "rule": "state must be reachable",
                        "expected_valid": False,
                    }],
                }), encoding="utf-8")
                return solutions

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            with self.assertRaisesRegex(
                RuntimeError, "mismatched semantic probes"
            ):
                Pipeline(
                    ProbedSolutions(), FakeCases(), FakeJudge(),
                    checker_from_profile({"kind": "TOKEN"}),
                ).run("p00004", "statement", Path(temp), iterations=1)

    def test_validator_may_accept_positive_semantic_probe(self):
        class ProbedSolutions(FakeSolutions):
            def generate(self, statement, output):
                solutions = super().generate(statement, output)
                (output / "generation.json").write_text(json.dumps({
                    "validator_semantic_probes": [{
                        "input": "1 2\n",
                        "rule": "positive sanity input",
                        "expected_valid": True,
                    }],
                }), encoding="utf-8")
                return solutions

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            Pipeline(
                ProbedSolutions(), FakeCases(), FakeJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                min_total_cases=1,
                top_up_rounds=0,
            ).run("p00004", "statement", output, iterations=1)
            audit = json.loads((
                output / "generated" / "validator-semantic-audit.json"
            ).read_text(encoding="utf-8"))
            self.assertTrue(audit[0]["matched_expectation"])

    def test_duplicate_proposal_preserves_sample_coverage_without_counting_new_case(self):
        cases = [Case("sample", "1\n", "7\n", "official-sample", 0, ("old",))]
        updated = merge_certified_coverage(cases, "1\n", ("boundary", "old"))
        self.assertEqual(len(cases), 1)
        self.assertEqual(updated.coverage_tags, ("old", "boundary"))
        self.assertEqual(updated.expected, "7\n")
        self.assertIsNone(merge_certified_coverage(cases, "rejected\n", ("unearned",)))
        self.assertEqual(cases[0].coverage_tags, ("old", "boundary"))

    def test_batched_consensus_matches_scalar_with_disagreement(self):
        class BatchJudge(FakeJudge):
            def __init__(self):
                self.batches = []

            def execute_many(self, solution, cases):
                self.batches.append((solution.id, len(cases)))
                return [Result(solution.id, "PASS", case_id,
                               "8" if solution.id == "ac2" and text == "split" else "7")
                        for case_id, text in cases]

        judge = BatchJudge()
        pipeline = Pipeline(FakeSolutions(), FakeCases(), judge,
                            checker_from_profile({"kind": "TOKEN"}), judge_workers=2)
        references = [Solution(name, "candidate_ac", "Python", Path(name))
                      for name in ("ac1", "ac2", "ac3")]
        result = pipeline._reference_consensus_many(
            references, [("one", "agree"), ("two", "split")])
        self.assertEqual([result[key].actual for key in ("one", "two")], ["7", "7"])
        self.assertCountEqual(judge.batches, [("ac1", 2), ("ac2", 2), ("ac3", 1)])

    def test_reference_consensus_stops_after_first_agreeing_pair(self):
        class ConsensusJudge(FakeJudge):
            def __init__(self):
                self.calls = []

            def execute(self, solution, case_id, input_text):
                self.calls.append(solution.id)
                outputs = {"ac1": "7\n", "ac2": "7\n", "ac3": "999\n"}
                return Result(solution.id, "PASS", case_id, outputs[solution.id])

        judge = ConsensusJudge()
        pipeline = Pipeline(
            FakeSolutions(), FakeCases(), judge,
            checker_from_profile({"kind": "TOKEN"}),
        )
        references = [
            Solution(name, "candidate_ac", "Python", Path(f"{name}.py"))
            for name in ("ac1", "ac2", "ac3")
        ]
        result = pipeline._reference_consensus(references, "case", "input\n")
        self.assertEqual(result.actual, "7\n")
        self.assertEqual(judge.calls, ["ac1", "ac2"])

    def test_reference_consensus_expands_after_disagreement(self):
        class ConsensusJudge(FakeJudge):
            def __init__(self):
                self.calls = []

            def execute(self, solution, case_id, input_text):
                self.calls.append(solution.id)
                outputs = {"ac1": "7\n", "ac2": "8\n", "ac3": "7\n"}
                return Result(solution.id, "PASS", case_id, outputs[solution.id])

        judge = ConsensusJudge()
        pipeline = Pipeline(
            FakeSolutions(), FakeCases(), judge,
            checker_from_profile({"kind": "TOKEN"}),
        )
        references = [
            Solution(name, "candidate_ac", "Python", Path(f"{name}.py"))
            for name in ("ac1", "ac2", "ac3")
        ]
        result = pipeline._reference_consensus(references, "case", "input\n")
        self.assertEqual(result.actual, "7\n")
        self.assertEqual(judge.calls, ["ac1", "ac2", "ac3"])

    def test_reference_consensus_preserves_reference_order_after_split(self):
        class ConsensusJudge(FakeJudge):
            def __init__(self):
                self.calls = []

            def execute(self, solution, case_id, input_text):
                self.calls.append(solution.id)
                outputs = {
                    "ac1": "7\n", "ac2": "8\n",
                    "ac3": "8\n", "ac4": "7\n",
                }
                return Result(solution.id, "PASS", case_id, outputs[solution.id])

        judge = ConsensusJudge()
        pipeline = Pipeline(
            FakeSolutions(), FakeCases(), judge,
            checker_from_profile({"kind": "TOKEN"}),
        )
        references = [
            Solution(name, "candidate_ac", "Python", Path(f"{name}.py"))
            for name in ("ac1", "ac2", "ac3", "ac4")
        ]
        result = pipeline._reference_consensus(references, "case", "input\n")
        self.assertEqual(result.actual, "7\n")
        self.assertEqual(judge.calls, ["ac1", "ac2", "ac3", "ac4"])

    def test_judge_pool_runs_solutions_concurrently(self):
        class ParallelJudge(Judge):
            def __init__(self):
                self.lock = threading.Lock()
                self.barrier = threading.Barrier(4)
                self.active = 0
                self.max_active = 0

            def compile(self, solution):
                return Result(solution.id, "PASS")

            def execute(self, solution, case_id, input_text):
                with self.lock:
                    self.active += 1
                    self.max_active = max(self.max_active, self.active)
                try:
                    self.barrier.wait(timeout=2)
                finally:
                    with self.lock:
                        self.active -= 1
                return Result(solution.id, "PASS", case_id, "1\n")

        judge = ParallelJudge()
        solutions = [
            Solution(f"s{index}", "candidate_ac", "Python", Path(f"s{index}.py"))
            for index in range(4)
        ]
        pipeline = Pipeline(
            FakeSolutions(), FakeCases(), judge,
            checker_from_profile({"kind": "TOKEN"}), judge_workers=4,
        )
        verdicts = pipeline._judge_pool(
            solutions,
            [Case("case", "input\n", "1\n", "parallel", 0)],
            {solution.id: Result(solution.id, "PASS") for solution in solutions},
            "parallel-test",
        )
        self.assertEqual(judge.max_active, 4)
        self.assertTrue(all(result.verdict == "PASS" for result in verdicts.values()))

    def test_survivor_audits_are_batched_into_one_call(self):
        class AuditSolutions(SolutionGenerator):
            def generate(self, statement, output):
                output.mkdir(parents=True)
                rows = []
                for name in ("validator", "ac1", "ac2", "wa1", "wa2"):
                    path = output / f"{name}.py"
                    path.write_text("# fake", encoding="utf-8")
                    if name != "validator":
                        rows.append(Solution(
                            name,
                            "candidate_wa" if name.startswith("wa") else "candidate_ac",
                            "Python",
                            path,
                            witness_input="witness\n" if name.startswith("wa") else "",
                        ))
                return rows

        class AuditCases(CaseGenerator):
            cases_per_round = 1

            def __init__(self):
                self.batch_calls = 0
                self.batch_sizes = []

            def generate(self, statement, feedback, iteration,
                         min_cases, max_cases):
                return {
                    "requested_count": 1,
                    "rationale": "keep mutants alive",
                    "cases": [{
                        "input": f"case-{iteration}\n",
                        "family": "audit",
                    }],
                }

            def audit_batch(self, statement, candidate_contexts, iteration):
                self.batch_calls += 1
                self.batch_sizes.append(len(candidate_contexts))
                return [{
                    "solution_id": context["id"],
                    "classification": "insufficient_evidence",
                    "revised_bug_hypothesis": "",
                    "reasoning": "",
                    "confidence": 0.0,
                    "failed_hypotheses": [],
                    "counterexample": None,
                } for context in candidate_contexts]

        class AuditJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                actual = (
                    "2.000\n"
                    if solution.id.startswith("wa") and input_text == "witness\n"
                    else "1.000\n"
                )
                return Result(solution.id, "PASS", case_id, actual)

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            cases = AuditCases()
            Pipeline(
                AuditSolutions(), cases, AuditJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                min_total_cases=99,
                top_up_rounds=0,
            ).run("p00004", "statement", Path(temp), iterations=2)
            self.assertEqual(cases.batch_calls, 1)
            self.assertEqual(cases.batch_sizes, [2])

    def test_dynamic_case_bounds_grow_with_survivors_and_low_tnr(self):
        self.assertEqual(dynamic_case_bounds(10, 0, None), (10, 10))
        self.assertEqual(dynamic_case_bounds(10, 8, 0.2), (10, 25))
        self.assertEqual(dynamic_case_bounds(10, 2, 0.8), (10, 13))
        self.assertEqual(dynamic_case_bounds(10, 3, 0.7), (10, 15))
        self.assertEqual(dynamic_case_bounds(
            10, 3, 0.9, uncovered_critical=2,
            rejected_count=4, stalled_rounds=1), (10, 21))

    def test_float_formats_and_signed_zero(self):
        checker = checker_from_profile({"kind": "FLOAT", "epsilon": 0.0005,
                                        "decimal_places": 3, "values_per_line": 2})
        self.assertTrue(checker.accepts("-0.000 3.000\n", "0.000 3.000\n"))
        self.assertFalse(checker.accepts("0.001 3.000\n", "0.000 3.000\n"))
        self.assertFalse(checker.accepts("0.0000 3.0000\n", "0.000 3.000\n"))
        self.assertFalse(checker.accepts("0.000\n3.000\n", "0.000 3.000\n"))
        self.assertTrue(checker_from_profile({"kind": "FLOAT", "epsilon": 0.0005})
                        .accepts("0.0015", "0.0010"))
        self.assertFalse(checker_from_profile({"kind": "FLOAT", "epsilon": 0.0005})
                         .accepts("0.001501", "0.0010"))
        relative = checker_from_profile({"kind": "FLOAT", "epsilon": 1e-6})
        self.assertTrue(relative.accepts(
            "3.2732646578712519e91", "3.2732646578712497e91"
        ))
        self.assertFalse(relative.accepts("1000002", "1000000"))

    def test_sample_parser(self):
        statement = "## Sample Input\n\n```text\n1 2\n```\n\n## Output for the Sample Input\n\n```text\n1.000\n```\n"
        self.assertEqual(samples(statement), [("1 2\n", "1.000\n")])

    def test_sample_parser_vietnamese_example_section(self):
        statement = (
            "## Ví dụ\n\n"
            "**Input**\n\n```text\n1\n2 4\n0 0 5\n1 2 3\n```\n\n"
            "**Output**\n\n```text\n6\n```\n"
        )
        self.assertEqual(
            samples(statement),
            [("1\n2 4\n0 0 5\n1 2 3\n", "6\n")],
        )

    def test_pipeline_rejects_unparsed_sample_section(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            with self.assertRaisesRegex(RuntimeError, "no complete input/output pair"):
                Pipeline(
                    FakeSolutions(), FakeCases(), FakeJudge(),
                    checker_from_profile({"kind": "TOKEN"}),
                ).run(
                    "p00004", "## Ví dụ\n\nKhông có block mẫu hợp lệ.\n",
                    Path(temp), iterations=1,
                )

    def test_iteration_and_report(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            report = Pipeline(FakeSolutions(), FakeCases(), FakeJudge(),
                              checker_from_profile({"kind": "FLOAT", "epsilon": 0.0005}),
                              min_iterations=1, min_total_cases=1,
                              top_up_rounds=0).run(
                "p00004", "not a real statement", output, iterations=3)
            self.assertEqual(report["iterations_used"], 1)
            self.assertEqual(report["llm_metrics"]["tpr_label_based"], 1.0)
            self.assertEqual(report["llm_metrics"]["tnr_label_based"], 1.0)
            self.assertTrue((output / "report.json").exists())

    def test_generation_failure_returns_locked_degraded_samples_and_runs_oracle(self):
        class UnavailableSolutions(SolutionGenerator):
            def generate(self, statement, output):
                raise LLMTransportError("all generation providers unavailable")

        class FakeOracle:
            def fetch(self, problem_id, output, per_label):
                output.mkdir(parents=True, exist_ok=True)
                source = output / "oracle.py"
                source.write_text("# oracle", encoding="utf-8")
                return [
                    Solution("oracle-ac", "CodeNet Accepted", "Python", source),
                    Solution("oracle-wa", "CodeNet Wrong Answer", "Python", source),
                ]

        statement = (
            "## Sample Input\n\n```text\n1 2\n```\n\n"
            "## Output for the Sample Input\n\n```text\n1.000\n```\n"
        )
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            report = Pipeline(
                UnavailableSolutions(), FakeCases(), FakeJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                oracle=FakeOracle(),
            ).run(
                "p00004", statement, output, iterations=1,
                use_oracle=True, oracle_limit=1,
            )

            self.assertEqual(report["quality_status"], "degraded")
            self.assertEqual(report["stop_reason"], "degraded_official_samples")
            self.assertEqual(report["oracle_status"], "completed")
            self.assertEqual(len(report["cases"]), 1)
            self.assertEqual(report["cases"][0]["family"], "official-sample")
            self.assertIn("oracle_metrics", report)
            self.assertTrue((output / "test-suite.lock.json").is_file())
            self.assertTrue((output / "tests" / "p00004_official_001.in").is_file())

    def test_oracle_failure_keeps_degraded_testcases_and_report(self):
        class UnavailableSolutions(SolutionGenerator):
            def generate(self, statement, output):
                raise LLMTransportError("generation unavailable")

        class UnavailableOracle:
            def fetch(self, problem_id, output, per_label):
                raise RuntimeError("oracle host unavailable")

        statement = (
            "## Sample Input\n\n```text\n1 2\n```\n\n"
            "## Output for the Sample Input\n\n```text\n1.000\n```\n"
        )
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            report = Pipeline(
                UnavailableSolutions(), FakeCases(), FakeJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                oracle=UnavailableOracle(),
            ).run(
                "p00004", statement, output, iterations=1,
                use_oracle=True, oracle_limit=1,
            )

            self.assertEqual(report["quality_status"], "degraded")
            self.assertEqual(report["oracle_status"], "failed")
            self.assertEqual(len(report["cases"]), 1)
            self.assertEqual(report["degradation_reasons"][-1]["stage"], "oracle")
            persisted = json.loads(
                (output / "report.json").read_text(encoding="utf-8")
            )
            self.assertEqual(persisted["oracle_status"], "failed")

    def test_failed_references_are_replenished_before_pipeline_aborts(self):
        class ReferenceReplacingSolutions(SolutionGenerator):
            def __init__(self):
                self.replacement_calls = 0

            def generate(self, statement, output):
                output.mkdir(parents=True)
                rows = []
                for name in ("validator", "good", "bad1", "bad2"):
                    source = output / f"{name}.py"
                    source.write_text("# fake", encoding="utf-8")
                    if name != "validator":
                        rows.append(Solution(
                            name, "candidate_ac", "Python", source,
                        ))
                return rows

            def regenerate_correct(
                self, statement, output, count, rejected, existing, round_number,
            ):
                self.replacement_calls += 1
                source = output / "replacement.py"
                source.write_text("# replacement", encoding="utf-8")
                return [Solution(
                    "replacement", "candidate_ac", "Python", source,
                )]

        class ReferenceJudge(FakeJudge):
            def compile(self, solution):
                verdict = "CE" if solution.id.startswith("bad") else "PASS"
                stderr = "syntax error" if verdict == "CE" else ""
                return Result(solution.id, verdict, stderr=stderr)

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            solutions = ReferenceReplacingSolutions()
            output = Path(temp)
            report = Pipeline(
                solutions, FakeCases(), ReferenceJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                min_iterations=1,
                min_total_cases=1,
                top_up_rounds=0,
            ).run("p00004", "statement", output, iterations=1)
            self.assertEqual(solutions.replacement_calls, 1)
            certification = json.loads(
                (output / "generated" / "reference-certification.json")
                .read_text(encoding="utf-8")
            )
            verified = [
                row["solution_id"] for row in certification
                if row["verified_for_consensus"]
            ]
            self.assertEqual(verified, ["good", "replacement"])
            self.assertEqual(report["llm_metrics"]["positive_evaluable"], 2)

    def test_console_progress(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            stream = io.StringIO()
            with redirect_stderr(stream):
                Pipeline(FakeSolutions(), FakeCases(), FakeJudge(),
                         checker_from_profile({"kind": "TOKEN"}),
                          progress=ConsoleProgress(), min_total_cases=1,
                          top_up_rounds=0).run("p00004", "statement", Path(temp), iterations=1)
            output = stream.getvalue()
            self.assertIn("LLM sinh code", output)
            self.assertIn("Test 1 p00004_i0_001", output)
            self.assertIn("LLM 3/3", output)
            self.assertIn("Đã ghi báo cáo", output)

    def test_ce_not_counted_as_bug_detection(self):
        pool = [Solution("ac", "candidate_ac", "Python", Path("ac.py")),
                Solution("wa", "candidate_wa", "Python", Path("wa.py"))]
        result = metrics(pool, {"ac": Result("ac", "PASS"), "wa": Result("wa", "CE")},
                         "candidate_ac", "candidate_wa")
        self.assertIsNone(result["tnr_label_based"])
        self.assertEqual(result["ce_infra"]["negative"], 1)

    def test_sample_validators(self):
        root = Path(__file__).resolve().parents[1] / "data" / "problems"
        for problem in ("p00004", "p00005"):
            spec = importlib.util.spec_from_file_location(problem, root / problem / "validator.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.assertTrue(module.valid(samples((root / problem / "statement.md").read_text())[0][0]))
            self.assertFalse(module.valid(""))
        spec = importlib.util.spec_from_file_location("p00004", root / "p00004" / "validator.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(module.valid("0.1 0 0.2 0 0.1 0.3\n"))
        self.assertFalse(module.valid("1 1 1 2 2 2\n"))

    def test_checker_registry_is_extensible(self):
        @register_checker
        class AlwaysChecker(Checker):
            kind = "TEST_ALWAYS"

            def accepts(self, actual: str, expected: str) -> bool:
                return True

        self.assertTrue(checker_from_profile({"kind": "TEST_ALWAYS"}).accepts("a", "b"))
        self.assertEqual(checker_from_profile({"kind": "TEST_ALWAYS"}).profile(),
                         {"kind": "TEST_ALWAYS"})
        with self.assertRaisesRegex(ValueError, "Unknown checker"):
            checker_from_profile({"kind": "MISSING"})
        self.assertTrue(checker_from_profile({"kind": "DECIMAL_EXACT"}).accepts("1.00", "1"))
        self.assertFalse(checker_from_profile({"kind": "DECIMAL_EXACT", "decimal_places": 2})
                         .accepts("1.0", "1.00"))

    def test_runtime_catalog_selects_dialect_without_judge_branches(self):
        catalog = RuntimeCatalog()
        source = Path("sample.cpp")
        self.assertEqual(catalog.resolve(Solution("x", "CodeNet Accepted", "C++", source,
                                                  dialect="C++11")).id, "cpp11")
        self.assertEqual(catalog.resolve(Solution(
            "dc", "CodeNet Accepted", "C++", source,
            dialect="DeepMind CodeContests CPP",
        )).id, "cpp20")
        self.assertEqual(catalog.resolve(Solution("x", "CodeNet Accepted", "Python",
                                                  Path("sample.py"), dialect="Python")).id,
                         "python2")
        self.assertEqual(catalog.extensions["Java"], ".java")
        self.assertEqual(catalog.resolve(Solution("j", "CodeNet Accepted", "Java",
                                                  Path("Main.java"), dialect="JAVA")).id, "java")

    def test_repeated_solution_case_uses_cached_execution(self):
        class CountingJudge(FakeJudge):
            calls = 0

            def execute(self, solution: Solution, case_id: str, input_text: str) -> Result:
                self.calls += 1
                return super().execute(solution, case_id, input_text)

        judge = CountingJudge()
        pipeline = Pipeline(FakeSolutions(), FakeCases(), judge,
                            checker_from_profile({"kind": "TOKEN"}))
        solution = Solution("ac1", "candidate_ac", "Python", Path("ac.py"))
        first = pipeline._execute_many(solution, [("case-1", "1 2\n")])
        second = pipeline._execute_many(solution, [("case-1", "1 2\n")])
        self.assertEqual(first, second)
        self.assertEqual(judge.calls, 1)

    def test_refinement_feedback_contains_survivor_source_and_previous_tests(self):
        class RecordingCases(CaseGenerator):
            cases_per_round = 4

            def __init__(self):
                self.calls = []

            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                self.calls.append((feedback, min_cases, max_cases))
                return {"requested_count": 1, "rationale": "target survivor",
                        "cases": [{"input": f"{iteration + 1} 2\n", "family": "targeted"}]}

        class SurvivorJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "wa1" and case_id.startswith("witness-"):
                    return Result(solution.id, "PASS", case_id, "2.000\n")
                return Result(solution.id, "PASS", case_id, "1.000\n")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            cases = RecordingCases()
            Pipeline(FakeSolutions(), cases, SurvivorJudge(),
                     checker_from_profile({"kind": "TOKEN"}),
                     top_up_rounds=0).run(
                "p00004", "statement", Path(temp), iterations=2)
            self.assertEqual(len(cases.calls), 2)
            feedback, minimum, maximum = cases.calls[1]
            survivor = feedback["surviving_wrong_candidates"][0]
            self.assertEqual(survivor["id"], "wa1")
            self.assertEqual(survivor["source_code"], "# fake")
            self.assertEqual(feedback["previous_round"]["certified_tests"][0]["input"],
                             "1 2\n")
            self.assertFalse(feedback["oracle_used"])
            self.assertGreater(maximum, cases.cases_per_round)
            self.assertLessEqual(minimum, maximum)

    def test_validator_rejected_input_is_repaired(self):
        class RepairCases(CaseGenerator):
            cases_per_round = 2

            def __init__(self):
                self.repairs = 0

            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                return {"requested_count": 1, "rationale": "repair test",
                        "cases": [{"input": "bad\n", "family": "malformed"}]}

            def repair(self, statement, feedback, rejected, attempt):
                self.repairs += 1
                return {"input": "1 2\n", "family": "repaired"}

        class RepairJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator" and input_text == "bad\n":
                    return Result(solution.id, "WA", case_id)
                if solution.id == "wa1" and case_id.startswith("witness-"):
                    return Result(solution.id, "PASS", case_id, "2.000\n")
                return Result(solution.id, "PASS", case_id, "1.000\n")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generator = RepairCases()
            report = Pipeline(FakeSolutions(), generator, RepairJudge(),
                              checker_from_profile({"kind": "TOKEN"}),
                              input_repair_attempts=2).run(
                "p00004", "statement", Path(temp), iterations=1)
            self.assertEqual(generator.repairs, 1)
            self.assertEqual(report["cases"][0]["input"], "1 2\n")
            self.assertEqual(report["cases"][0]["family"], "repaired")
            self.assertEqual(report["quarantined"][0]["reason"], "validator rejected")

    def test_validator_rejected_inputs_are_repaired_in_one_batch(self):
        class BatchRepairCases(CaseGenerator):
            cases_per_round = 2

            def __init__(self):
                self.batch_calls = 0
                self.batch_sizes = []

            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                return {
                    "requested_count": 2,
                    "rationale": "batch repair test",
                    "cases": [
                        {"input": "bad one\n", "family": "malformed"},
                        {"input": "bad two\n", "family": "malformed"},
                    ],
                }

            def repair_batch(self, statement, feedback, rejected, attempt):
                self.batch_calls += 1
                self.batch_sizes.append(len(rejected))
                return [
                    {
                        "proposal_index": item["proposal_index"],
                        "input": f"{item['proposal_index']} 2\n",
                        "family": "batch-repaired",
                    }
                    for item in rejected
                ]

        class BatchRepairJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator" and input_text.startswith("bad"):
                    return Result(solution.id, "WA", case_id)
                if solution.id == "wa1" and case_id.startswith("witness-"):
                    return Result(solution.id, "PASS", case_id, "2.000\n")
                return Result(solution.id, "PASS", case_id, "1.000\n")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generator = BatchRepairCases()
            report = Pipeline(
                FakeSolutions(), generator, BatchRepairJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                input_repair_attempts=2,
                top_up_rounds=0,
            ).run("p00004", "statement", Path(temp), iterations=1)
            self.assertEqual(generator.batch_calls, 1)
            self.assertEqual(generator.batch_sizes, [2])
            self.assertEqual(len(report["cases"]), 2)
            self.assertTrue(all(
                row["family"] == "batch-repaired" for row in report["cases"]
            ))

    def test_unverified_mutant_is_replaced_before_tnr(self):
        class ReplacingSolutions(SolutionGenerator):
            def __init__(self):
                self.replacement_calls = 0

            def generate(self, statement, output):
                output.mkdir(parents=True)
                for name in ("validator.py", "ac1.py", "ac2.py", "bad.py"):
                    (output / name).write_text("# fake", encoding="utf-8")
                return [
                    Solution("ac1", "candidate_ac", "Python", output / "ac1.py"),
                    Solution("ac2", "candidate_ac", "Python", output / "ac2.py"),
                    Solution("bad", "candidate_wa", "Python", output / "bad.py",
                             witness_input="1 2\n", failure_condition="not observable"),
                ]

            def regenerate_wrong(self, statement, output, count, rejected,
                                 existing, round_number):
                self.replacement_calls += 1
                if self.replacement_calls == 1:
                    return []
                source = output / "replacement.py"
                source.write_text("# replacement", encoding="utf-8")
                return [Solution(
                    "replacement", "candidate_wa", "Python", source,
                    bug_class="wrong answer", strategy_id="replacement",
                    bug_origin="intentional", failure_condition="returns 2",
                    witness_input="1 2\n",
                )]

        class ReplacementJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                actual = "2.000\n" if solution.id == "replacement" else "1.000\n"
                return Result(solution.id, "PASS", case_id, actual)

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            solutions = ReplacingSolutions()
            report = Pipeline(
                solutions, FakeCases(), ReplacementJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                mutant_replacement_rounds=2,
            ).run("p00004", "statement", Path(temp), iterations=1)
            certification = report["mutant_certification"]
            self.assertEqual(certification["requested_wrong_candidates"], 1)
            self.assertEqual(certification["validated_wrong_candidates"], 1)
            self.assertEqual(certification["rejected_or_unverified"], 1)
            self.assertIn("replacement", report["llm_verdicts"])
            self.assertNotIn("bad", report["llm_verdicts"])
            self.assertEqual(solutions.replacement_calls, 2)

    def test_replacement_rounds_stop_after_minimum_three_are_verified(self):
        class MinimumPoolSolutions(SolutionGenerator):
            def __init__(self):
                self.replacement_rounds = []
                self.replacement_counts = []

            def requested_wrong_candidates(self):
                return 5

            def generate(self, statement, output):
                output.mkdir(parents=True)
                rows = []
                for name in ("validator", "ac1", "ac2"):
                    path = output / f"{name}.py"
                    path.write_text(f"# {name}", encoding="utf-8")
                    if name != "validator":
                        rows.append(Solution(
                            name, "candidate_ac", "Python", path,
                        ))
                return rows

            def regenerate_wrong(self, statement, output, count, rejected,
                                 existing, round_number):
                if round_number == 0:
                    rows = []
                    for index in range(5):
                        name = f"initial-{index}"
                        path = output / f"{name}.py"
                        path.write_text(f"# {name}", encoding="utf-8")
                        rows.append(Solution(
                            name, "candidate_wa", "Python", path,
                            witness_input="witness\n",
                        ))
                    return rows
                self.replacement_rounds.append(round_number)
                self.replacement_counts.append(count)
                name = f"replacement-{round_number}"
                path = output / f"{name}.py"
                path.write_text(f"# {name}", encoding="utf-8")
                return [Solution(
                    name, "candidate_wa", "Python", path,
                    witness_input="witness\n",
                )]

        class MinimumPoolJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                actual = (
                    "2.000\n"
                    if solution.id.startswith("replacement-")
                    else "1.000\n"
                )
                return Result(solution.id, "PASS", case_id, actual)

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            solutions = MinimumPoolSolutions()
            report = Pipeline(
                solutions, FakeCases(), MinimumPoolJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                mutant_replacement_rounds=4,
                mutant_replacement_oversampling=1.0,
                mutant_witness_repair_rounds=0,
                min_iterations=1,
                min_total_cases=1,
                top_up_rounds=0,
            ).run("p00004", "statement", Path(temp), iterations=1)
            certification = report["mutant_certification"]
            self.assertEqual(certification["validated_wrong_candidates"], 3)
            self.assertEqual(solutions.replacement_rounds, [1, 2, 3])
            self.assertEqual(solutions.replacement_counts, [3, 2, 1])

    def test_unverified_mutant_gets_new_witness_before_replacement(self):
        class WitnessRepairSolutions(SolutionGenerator):
            def __init__(self):
                self.witness_calls = 0
                self.replacement_calls = 0

            def generate(self, statement, output):
                output.mkdir(parents=True)
                for name in ("validator.py", "ac1.py", "ac2.py", "wa1.py"):
                    (output / name).write_text("# fake", encoding="utf-8")
                return [
                    Solution("ac1", "candidate_ac", "Python", output / "ac1.py"),
                    Solution("ac2", "candidate_ac", "Python", output / "ac2.py"),
                    Solution(
                        "wa1", "candidate_wa", "Python", output / "wa1.py",
                        failure_condition="fails only on the repaired boundary",
                        witness_input="bad\n",
                    ),
                ]

            def generate_mutant_witnesses(
                self, statement, output, mutants, references, evidence,
                attempt, candidates_per_mutant,
            ):
                self.witness_calls += 1
                self.asserted_reference_ids = [item.id for item in references]
                return {"wa1": ["good\n", "unused-1\n", "unused-2\n"]}

            def regenerate_wrong(self, statement, output, count, rejected,
                                 existing, round_number):
                self.replacement_calls += 1
                return []

        class WitnessRepairJudge(FakeJudge):
            def __init__(self):
                self.mutant_witness_inputs = []

            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                if solution.id == "wa1" and case_id.startswith("witness-"):
                    self.mutant_witness_inputs.append(input_text)
                actual = (
                    "2.000\n"
                    if solution.id == "wa1" and input_text == "good\n"
                    else "1.000\n"
                )
                return Result(solution.id, "PASS", case_id, actual)

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            solutions = WitnessRepairSolutions()
            judge = WitnessRepairJudge()
            report = Pipeline(
                solutions, FakeCases(), judge,
                checker_from_profile({"kind": "TOKEN"}),
                mutant_replacement_rounds=1,
                mutant_witness_repair_rounds=2,
                mutant_witness_candidates=2,
            ).run("p00004", "statement", Path(temp), iterations=1)
            certification = report["mutant_certification"]
            self.assertEqual(certification["validated_wrong_candidates"], 1)
            self.assertEqual(solutions.witness_calls, 1)
            self.assertEqual(solutions.replacement_calls, 0)
            self.assertEqual(solutions.asserted_reference_ids, ["ac1", "ac2"])
            record = certification["records"][0]
            self.assertEqual(record["witness_input"], "good\n")
            self.assertEqual(record["witness_repair_status"], "verified")
            self.assertEqual(len(record["witness_attempts"]), 2)
            self.assertFalse(record["witness_attempts"][0]["verified"])
            self.assertTrue(record["witness_attempts"][1]["verified"])
            self.assertEqual(
                judge.mutant_witness_inputs,
                ["bad\n", "bad\n", "good\n", "good\n"],
            )
            early_stop = certification["witness_early_stop"]
            self.assertEqual(early_stop["repair_witnesses_proposed"], 3)
            self.assertEqual(early_stop["repair_witnesses_evaluated"], 1)
            self.assertEqual(
                early_stop["repair_witnesses_skipped_after_verified"], 2
            )
            self.assertTrue(
                certification["compile_policy"]["compile_once_per_candidate"]
            )

    def test_witness_repair_stops_as_soon_as_requested_pool_is_full(self):
        class QuotaSolutions(SolutionGenerator):
            def __init__(self):
                self.witness_calls = 0
                self.witness_mutants = []

            def generate(self, statement, output):
                output.mkdir(parents=True)
                rows = []
                for name in ("validator", "ac1", "ac2"):
                    path = output / f"{name}.py"
                    path.write_text("# fake", encoding="utf-8")
                    if name != "validator":
                        rows.append(Solution(
                            name, "candidate_ac", "Python", path,
                        ))
                return rows

            def requested_wrong_candidates(self):
                return 1

            def regenerate_wrong(self, statement, output, count, rejected,
                                 existing, round_number):
                if round_number != 0:
                    return []
                rows = []
                for name in ("wa1", "wa2", "wa3", "wa4", "wa5", "wa6"):
                    path = output / f"{name}.py"
                    path.write_text("# fake", encoding="utf-8")
                    rows.append(Solution(
                        name, "candidate_wa", "Python", path,
                        witness_input="bad\n",
                    ))
                return rows

            def generate_mutant_witnesses(
                self, statement, output, mutants, references, evidence,
                attempt, candidates_per_mutant,
            ):
                self.witness_calls += 1
                self.witness_mutants.append([
                    solution.id for solution in mutants
                ])
                return {solution.id: [f"good-{solution.id}\n"] for solution in mutants}

        class QuotaJudge(FakeJudge):
            def __init__(self):
                self.repaired_candidates = []

            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                if solution.id.startswith("wa") and input_text.startswith("good-"):
                    self.repaired_candidates.append(solution.id)
                actual = (
                    "2.000\n"
                    if solution.id == "wa2" and input_text == "good-wa2\n"
                    else "1.000\n"
                )
                return Result(solution.id, "PASS", case_id, actual)

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            solutions = QuotaSolutions()
            judge = QuotaJudge()
            report = Pipeline(
                solutions, FakeCases(), judge,
                checker_from_profile({"kind": "TOKEN"}),
                mutant_replacement_rounds=0,
                mutant_replacement_oversampling=3.0,
                mutant_witness_repair_rounds=1,
                min_iterations=1,
                min_total_cases=1,
                top_up_rounds=0,
            ).run("p00004", "statement", Path(temp), iterations=1)
            certification = report["mutant_certification"]
            self.assertEqual(certification["validated_wrong_candidates"], 1)
            self.assertEqual(certification["validated_solution_ids"], ["wa2"])
            self.assertEqual(solutions.witness_calls, 1)
            self.assertEqual(
                solutions.witness_mutants,
                [["wa1", "wa2"]],
            )
            self.assertEqual(judge.repaired_candidates, ["wa1", "wa1", "wa2", "wa2"])
            self.assertNotIn("wa3", judge.repaired_candidates)
            self.assertEqual(
                certification["witness_early_stop"][
                    "repair_witnesses_skipped_after_pool_full"
                ],
                0,
            )
            self.assertEqual(certification["candidate_trials_per_witness"], 2)

    def test_initial_mutants_are_derived_only_after_reference_certification(self):
        class DerivedSolutions(SolutionGenerator):
            def __init__(self):
                self.calls = []

            def requested_wrong_candidates(self):
                return 1

            def generate(self, statement, output):
                output.mkdir(parents=True)
                for name in ("validator.py", "ac1.py", "ac2.py"):
                    (output / name).write_text("# fake", encoding="utf-8")
                return [
                    Solution("ac1", "candidate_ac", "Python", output / "ac1.py"),
                    Solution("ac2", "candidate_ac", "Python", output / "ac2.py"),
                ]

            def regenerate_wrong(self, statement, output, count, rejected,
                                 existing, round_number):
                self.calls.append({
                    "round": round_number,
                    "parents": [solution.id for solution in existing],
                    "count": count,
                })
                source = output / "wa1.py"
                source.write_text("# derived", encoding="utf-8")
                return [Solution(
                    "wa1", "candidate_wa", "Python", source,
                    bug_class="boundary", strategy_id="derived-wa",
                    bug_origin="intentional", failure_condition="returns 2",
                    witness_input="1 2\n", parent_ac_id="ac1",
                    mutation_operator="boundary mutation",
                    target_behavior="non-sample boundary",
                    sample_preservation_reason="no official samples in fixture",
                )]

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            solutions = DerivedSolutions()
            report = Pipeline(
                solutions, FakeCases(), FakeJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                mutant_replacement_rounds=0,
            ).run("p00004", "statement", Path(temp), iterations=1)
            self.assertEqual(solutions.calls[0]["round"], 0)
            self.assertEqual(solutions.calls[0]["parents"], ["ac1", "ac2"])
            self.assertEqual(report["mutant_certification"]["validated_wrong_candidates"], 1)

    def test_nondeterministic_witness_is_not_certified(self):
        class FlakyWitnessJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                if solution.id == "wa1" and case_id.endswith("trial-1"):
                    return Result(solution.id, "PASS", case_id, "2.000\n")
                return Result(solution.id, "PASS", case_id, "1.000\n")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            with self.assertRaisesRegex(RuntimeError, "minimum verified"):
                Pipeline(
                    FakeSolutions(), FakeCases(), FlakyWitnessJudge(),
                    checker_from_profile({"kind": "TOKEN"}),
                    mutant_replacement_rounds=0,
                ).run("p00004", "statement", output, iterations=1)
            certification = json.loads(
                (output / "generated" / "mutant-certification.json")
                .read_text(encoding="utf-8")
            )
            self.assertFalse(certification["records"][0]["verified"])
            self.assertIn("both trials", certification["records"][0]["reason"])
            self.assertEqual(certification["minimum_required"], 1)
            self.assertEqual(
                certification["stage_status"], "failed_minimum_verified_pool"
            )

    def test_feedback_accumulates_attempts_and_survivor_audit(self):
        class ContextCases(CaseGenerator):
            cases_per_round = 4

            def __init__(self):
                self.feedbacks = []

            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                self.feedbacks.append(feedback)
                return {
                    "requested_count": 1,
                    "rationale": "context test",
                    "cases": [{
                        "input": f"{iteration + 1} 2\n",
                        "family": "targeted",
                        "target_solution_ids": ["wa1"],
                        "hypothesis_id": f"h-{iteration}",
                        "predicted_expected": "1.000",
                        "predicted_candidate_output": "2.000",
                        "reason_for_difference": "predicted bug",
                    }],
                }

            def audit(self, statement, candidate_context, iteration):
                return {
                    "classification": "counterexample_found",
                    "revised_bug_hypothesis": "try another boundary",
                    "reasoning": "the prior targeted prediction was false",
                    "confidence": 0.8,
                    "failed_hypotheses": ["predicted bug"],
                    "counterexample": {"input": "3 2\n"},
                }

        class ContextJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                if solution.id == "wa1" and case_id.startswith("witness-"):
                    return Result(solution.id, "PASS", case_id, "2.000\n")
                return Result(solution.id, "PASS", case_id, "1.000\n")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generator = ContextCases()
            output = Path(temp)
            report = Pipeline(
                FakeSolutions(), generator, ContextJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                top_up_rounds=0,
            ).run("p00004", "statement", output, iterations=2)
            first_feedback = generator.feedbacks[0]
            self.assertEqual(first_feedback["surviving_wrong_candidates"], [])
            self.assertEqual(first_feedback["generation_mode"], "coverage_baseline")
            second_feedback = generator.feedbacks[1]
            context = second_feedback["surviving_wrong_candidates"][0]
            self.assertTrue(context["certification"]["verified"])
            self.assertEqual(context["attempts"][0]["case_id"], "p00004_i0_001")
            self.assertTrue(context["attempts"][0]["targeted"])
            self.assertFalse(context["attempts"][0]["killed"])
            self.assertEqual(context["latest_audit"]["classification"],
                             "counterexample_found")
            self.assertIn("predicted bug", context["failed_hypotheses"])
            self.assertEqual(len(second_feedback["experiment_history"]
                                 ["certified_tests"]), 1)
            self.assertTrue((output / "context" / "candidates" / "wa1.json").is_file())
            self.assertEqual(report["mutant_certification"]
                             ["validated_wrong_candidates"], 1)

    def test_oracle_runs_only_after_llm_suite_is_locked_and_uses_separate_log(self):
        events = []

        class EventCases(FakeCases):
            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                events.append(("llm-generate", feedback))
                return super().generate(statement, feedback, iteration, min_cases, max_cases)

        class FakeOracle(OracleSource):
            def fetch(self, problem_id, output, per_label):
                events.append(("oracle-fetch", None))
                output.mkdir(parents=True, exist_ok=True)
                ac = output / "ac.py"
                wa = output / "wa.py"
                ac.write_text("# oracle ac", encoding="utf-8")
                wa.write_text("# oracle wa", encoding="utf-8")
                return [Solution("oracle-ac", "CodeNet Accepted", "Python", ac),
                        Solution("oracle-wa", "CodeNet Wrong Answer", "Python", wa)]

        class AllPassJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "wa1" and case_id.startswith("witness-"):
                    return Result(solution.id, "PASS", case_id, "2.000\n")
                return Result(solution.id, "PASS", case_id, "1.000\n")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            report = Pipeline(FakeSolutions(), EventCases(), AllPassJudge(),
                              checker_from_profile({"kind": "TOKEN"}),
                              oracle=FakeOracle(), top_up_rounds=0).run(
                "p00004", "statement", output, iterations=1,
                use_oracle=True, oracle_limit=1)
            self.assertEqual(events[0][0], "llm-generate")
            self.assertEqual(events[-1][0], "oracle-fetch")
            self.assertFalse(events[0][1]["oracle_used"])
            self.assertFalse(report["experiment_protocol"]
                             ["oracle_used_for_generation_or_refinement"])
            self.assertTrue((output / "test-suite.lock.json").is_file())
            self.assertTrue((output / "executions-llm.jsonl").is_file())
            self.assertTrue((output / "oracle" / "executions.jsonl").is_file())

    def test_coverage_model_is_normalized_and_reported(self):
        class CoverageCases(FakeCases):
            cases_per_round = 1

            def build_test_model(self, statement):
                return {
                    "coverage_obligations": [{
                        "id": "Zero Boundary",
                        "category": "boundary",
                        "description": "exercise the valid zero boundary",
                        "priority": "critical",
                        "required": True,
                    }]
                }

            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                return {"requested_count": 1, "rationale": "cover zero", "cases": [{
                    "input": "1 2\n", "family": "boundary",
                    "coverage_tags": ["zero-boundary"],
                    "coverage_evidence": [{
                        "tag": "zero-boundary",
                        "input_excerpt": "1",
                        "rationale": "the first field is the exercised boundary",
                    }],
                }]}

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            report = Pipeline(
                FakeSolutions(), CoverageCases(), FakeJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                min_iterations=1, min_total_cases=1, top_up_rounds=0,
            ).run("p00004", "statement", Path(temp), iterations=1)
            self.assertEqual(report["coverage"]["critical_ratio"], 1.0)
            self.assertEqual(report["cases"][0]["coverage_tags"], ["zero-boundary"])
            self.assertEqual(report["stop_reason"], "all_quality_criteria_met")

    def test_top_up_targets_accepted_case_count(self):
        class TopUpCases(FakeCases):
            cases_per_round = 3

            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                return {"requested_count": 3, "rationale": "short batch",
                        "cases": [{"input": "1 2\n", "family": "first"}]}

            def top_up(self, statement, feedback, iteration, missing_cases,
                       baseline=False):
                return {
                    "requested_count": missing_cases,
                    "rationale": "replace missing",
                    "cases": [
                        {"input": f"{index + 2} 2\n", "family": "top-up"}
                        for index in range(missing_cases)
                    ],
                }

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            report = Pipeline(
                FakeSolutions(), TopUpCases(), FakeJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                min_iterations=1, min_total_cases=3, top_up_rounds=1,
            ).run("p00004", "statement", Path(temp), iterations=1)
            self.assertEqual(len(report["cases"]), 3)

    def test_stable_official_sample_failure_fills_minimum_as_fallback(self):
        statement = (
            "## Sample Input\n\n```text\n1 2\n```\n\n"
            "## Output for the Sample Input\n\n```text\n1.000\n```\n"
        )
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            output = Path(temp)
            Pipeline(
                FakeSolutions(), FakeCases(), FakeJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                mutant_replacement_rounds=0,
            ).run("p00004", statement, output, iterations=1)
            certification = json.loads(
                (output / "generated" / "mutant-certification.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(
                certification["records"][0]["reason"],
                "official sample produced the same deterministic failure in two trials",
            )
            self.assertEqual(
                certification["records"][0]["verification_tier"],
                "official_sample_fallback",
            )
            self.assertTrue(
                certification["records"][0]["promoted_to_minimum_pool"]
            )
            self.assertEqual(certification["validated_wrong_candidates"], 1)
            self.assertEqual(certification["strict_sample_preserving_verified"], 0)
            self.assertEqual(certification["official_sample_fallback_used"], ["wa1"])

    def test_minimum_three_uses_strict_then_sample_fallback_without_more_llm(self):
        statement = (
            "## Sample Input\n\n```text\nsample\n```\n\n"
            "## Output for the Sample Input\n\n```text\n1.000\n```\n"
        )

        class MixedMutants(SolutionGenerator):
            def __init__(self):
                self.replacement_calls = 0

            def requested_wrong_candidates(self):
                return 5

            def generate(self, statement, output):
                output.mkdir(parents=True)
                rows = []
                for name in (
                    "validator", "ac1", "ac2", "strict",
                    "sample-bad-1", "sample-bad-2", "equivalent-1", "equivalent-2",
                ):
                    path = output / f"{name}.py"
                    path.write_text(f"# {name}", encoding="utf-8")
                    if name != "validator":
                        rows.append(Solution(
                            name,
                            "candidate_ac" if name.startswith("ac") else "candidate_wa",
                            "Python",
                            path,
                            witness_input="witness\n" if not name.startswith("ac") else "",
                        ))
                return rows

            def regenerate_wrong(self, statement, output, count, rejected,
                                 existing, round_number):
                self.replacement_calls += 1
                return []

        class MixedMutantJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                is_sample_bad = solution.id.startswith("sample-bad-")
                is_strict_witness = (
                    solution.id == "strict" and input_text == "witness\n"
                )
                actual = "2.000\n" if is_sample_bad or is_strict_witness else "1.000\n"
                return Result(solution.id, "PASS", case_id, actual)

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generator = MixedMutants()
            report = Pipeline(
                generator, FakeCases(), MixedMutantJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                mutant_replacement_rounds=4,
                mutant_witness_repair_rounds=0,
                min_iterations=1,
                min_total_cases=1,
                top_up_rounds=0,
            ).run("p00004", statement, Path(temp), iterations=1)
            certification = report["mutant_certification"]
            self.assertEqual(certification["validated_wrong_candidates"], 3)
            self.assertEqual(certification["strict_sample_preserving_verified"], 1)
            self.assertEqual(
                certification["official_sample_fallback_used"],
                ["sample-bad-1", "sample-bad-2"],
            )
            self.assertEqual(generator.replacement_calls, 0)
            self.assertEqual(
                set(certification["validated_solution_ids"]),
                {"strict", "sample-bad-1", "sample-bad-2"},
            )

    def test_holdout_mutant_is_hidden_until_suite_lock(self):
        class FiveMutants(SolutionGenerator):
            def generate(self, statement, output):
                output.mkdir(parents=True)
                rows = []
                for name in ("validator", "ac1", "ac2", "wa1", "wa2", "wa3", "wa4", "wa5"):
                    path = output / f"{name}.py"
                    path.write_text(f"# {name}", encoding="utf-8")
                    if name != "validator":
                        rows.append(Solution(
                            name,
                            "candidate_ac" if name.startswith("ac") else "candidate_wa",
                            "Python",
                            path,
                            witness_input="9 9\n" if name.startswith("wa") else "",
                        ))
                return rows

        class RecordingCases(FakeCases):
            cases_per_round = 1

            def __init__(self):
                self.feedbacks = []

            def generate(self, statement, feedback, iteration, min_cases, max_cases):
                self.feedbacks.append(feedback)
                return {"requested_count": 1, "rationale": "record",
                        "cases": [{"input": f"{iteration + 1} 2\n",
                                   "family": "record"}]}

        class HoldoutJudge(FakeJudge):
            def execute(self, solution, case_id, input_text):
                if solution.id == "validator":
                    return Result(solution.id, "PASS", case_id)
                if solution.id.startswith("wa") and case_id.startswith("witness-"):
                    return Result(solution.id, "PASS", case_id, "2.000\n")
                return Result(solution.id, "PASS", case_id, "1.000\n")

        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp:
            generator = RecordingCases()
            report = Pipeline(
                FiveMutants(), generator, HoldoutJudge(),
                checker_from_profile({"kind": "TOKEN"}),
                min_total_cases=99, top_up_rounds=0, holdout_fraction=0.2,
            ).run("p00004", "statement", Path(temp), iterations=2)
            adaptive_feedback = generator.feedbacks[1]
            visible_ids = {
                row["id"] for row in adaptive_feedback["surviving_wrong_candidates"]
            }
            self.assertEqual(visible_ids, {"wa1", "wa2", "wa3", "wa4"})
            self.assertNotIn("wa5", visible_ids)
            self.assertEqual(
                report["mutant_certification"]["holdout_mutants"], ["wa5"]
            )
            self.assertIn("wa5", report["llm_holdout_verdicts"])
            self.assertTrue((Path(temp) / "executions-holdout.jsonl").is_file())


if __name__ == "__main__":
    unittest.main()
