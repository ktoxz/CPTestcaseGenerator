# Errors Found

## 2026-10-21 — Multiple-answer problems are evaluated with an exact TOKEN checker

Status: Fixed in `Standard_v1` (pending full 50-problem rerun)

Severity: High. Valid accepted solutions are rejected, reference certification
can fail completely, and a degraded official-sample suite can report misleading
oracle metrics.

### Affected runs

- Retry batch: `output/retries/ollama-20261021-190921`
- Confirmed problems: `cf1003b`, `cf1004b`
- Likely affected and requiring a problem-local checker: `cf1006b`

### Symptoms

`cf1003b`:

- All five generated reference candidates compiled.
- None passed exact comparison against all official sample outputs.
- Several candidates produced different but potentially valid constructive
  strings, for example `0011` instead of the sample output `1100`.
- The pipeline fell back to three official samples and labelled the result
  `degraded`.
- Oracle result on that fallback suite: TPR `7/20 = 0.35`, TNR `20/20 = 1.0`.

`cf1004b`:

- All four generated reference candidates compiled.
- Every candidate produced `01010` and `010101` for the two official samples,
  instead of the sample outputs `01100` and `110010`.
- These alternating strings are optimal: for every requested interval they
  maximize `number_of_zeroes * number_of_ones`. They are valid alternative
  answers, but the TOKEN checker rejected them.
- The pipeline fell back to two official samples and labelled the result
  `degraded`.
- Oracle result on that fallback suite: TPR `0/20 = 0.0`, TNR `20/20 = 1.0`.
  Rejecting every accepted oracle solution confirms that the output semantics,
  rather than the generated algorithms, are the primary failure.

### Root cause

Both problem directories configure:

```json
{
  "kind": "TOKEN"
}
```

However, both statements permit multiple correct outputs:

- `cf1003b`: any binary string satisfying the requested counts and transition
  count is accepted.
- `cf1004b`: if multiple optimal flower arrangements exist, any may be printed.

The TOKEN checker compares the candidate output with the non-canonical sample
output. It therefore treats a different valid construction as wrong.

### Original pipeline gap

The pipeline could execute a trusted problem-local `PYTHON_SCRIPT` checker, but
could not generate and certify one. The LLM-generated test model could only
recommend checker semantics.

The heuristic in `testgen/problem.py::requires_input_aware_checker` also misses
wording used by these problems, including:

- `any binary string satisfying conditions`
- `if there are multiple answers, print any`
- `if there are many possible answers, you may print any of them`

### Why the degraded fallback is not sufficient

The resilience path worked mechanically: it preserved official samples, locked
the suite, ran the oracle, returned exit code zero, and labelled the result
`degraded`. But an official expected output is not a canonical oracle for a
multiple-answer problem. Reusing it with TOKEN comparison preserves testcase
files while still producing invalid verdicts.

### Implemented fix

1. Added the typed `GENERATE_CHECKER` LLM task. It is routed to the default
   Ollama model, not the fine-tuned testcase model.
2. LLM checker source is statically restricted, cannot read the non-canonical
   `expected` output, and runs in a fresh isolated Python process with timeout.
   Imports, files, network, subprocesses, reflection, dynamic execution and
   private attributes/names are blocked. Unused decorative imports are removed.
3. A checker is activated only after accepting every official output twice and
   rejecting malformed/extra-token probes. Up to three generation attempts are
   allowed with rejection feedback.
4. If checker certification still fails, only official samples are returned as
   `degraded`; generation stops and oracle evaluation is skipped with
   `skipped_uncertified_checker`, avoiding misleading TOKEN-based metrics.
5. Generated checker source and certification are saved under `generated/` and
   restored for `--resume-oracle`.
6. Extended multiple-answer wording detection and added safety, timeout, retry,
   and alternative-output tests.

### Smoke verification

- `cf1003b`: checker certified on the first attempt and accepted valid
  alternatives `0011`, `001011`, and `00101010` for the three samples.
- `cf1004b`: checker certified on the first attempt and accepted alternative
  optimal outputs `01010` and `010101`.
- Full test suite: 225 passed, 1 skipped, 35 subtests passed.

### Acceptance criteria

- Official outputs and alternative valid outputs are accepted.
- Invalid or suboptimal outputs are rejected.
- Reference certification no longer fails solely because output differs from
  the sample.
- Oracle TPR no longer collapses due to exact-output comparison.
- The suite remains locked before oracle evaluation.
