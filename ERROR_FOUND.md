# Errors Found

## 2026-10-21 — Multiple-answer problems are evaluated with an exact TOKEN checker

Status: Open

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

### Pipeline gap

The pipeline can execute a trusted problem-local `PYTHON_SCRIPT` checker, but it
does not currently generate and certify such a checker. The LLM-generated test
model can only recommend checker semantics. Executable output checkers must be
provided as audited files under `data/problems/<problem_id>/`.

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

### Required fix

1. Add audited `output_checker.py` files and configure `PYTHON_SCRIPT` for:
   - `cf1003b`: validate length, alphabet, zero/one counts, and adjacent
     transition count from the input.
   - `cf1004b`: validate a binary string of length `n`, calculate its objective
     over all intervals, and require the global optimum
     `sum(floor((r_i-l_i+1)^2 / 4))`.
   - `cf1006b`: validate the declared profit and positive segment lengths, then
     require an optimal partition whose profit equals the sum of the `k`
     greatest difficulties.
2. Extend multiple-answer wording detection in `testgen/problem.py`.
3. Treat `multiple-answer + non-input-aware checker` as a configuration error.
   Do not convert it into an official-output degraded suite.
4. Add positive tests with alternative valid outputs and negative tests with
   malformed, infeasible, or suboptimal outputs.
5. Rerun reference certification and the CodeNet oracle. Previously completed
   degraded reports must not be promoted or reused automatically.

### Acceptance criteria

- Official outputs and alternative valid outputs are accepted.
- Invalid or suboptimal outputs are rejected.
- Reference certification no longer fails solely because output differs from
  the sample.
- Oracle TPR no longer collapses due to exact-output comparison.
- The suite remains locked before oracle evaluation.
