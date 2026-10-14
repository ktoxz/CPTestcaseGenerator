# Runtime and automatic specification implementation

Implemented on 2026-10-14 on branch `Standard`.

## Delivered changes

- Docker stdin is passed as UTF-8 bytes and persisted testcase files force LF newlines.
- `BUILD_TEST_MODEL` now returns bounded checker and sandbox specifications without an additional LLM call.
- Explicit time and memory metadata in statements overrides LLM guesses. Values are clamped to 0.1–60 seconds and 32–4096 MB.
- Generated `PYTHON_SCRIPT` checkers are never executed. Constructive problems require an audited problem-local checker.
- The judge applies a 1.5x time allowance and the statement memory limit, including resumed oracle evaluations.
- The main image includes NumPy, Numba and Boost. C++20 is the default generated C++ dialect, Java heap follows the cgroup, and AtCoder `numba.pycc` submissions receive their required `ONLINE_JUDGE` precompile step.
- Python 3 uses `-s` from `/work`, allowing locally compiled extension modules while disabling the user site directory.
- Ambiguous argparse abbreviation is disabled, so `--judge local` is no longer parsed as `--judge-config local`.

## Verification

| Check | Result |
|---|---|
| Docker `cat -A` with byte input `k\n` | `b'k$\n'`; no `^M` |
| NumPy import | 1.24.2 |
| Boost + GNU C++20 compile | PASS |
| Python 2, network disabled | `hello`, integer division `1/2 == 0` |
| Unit tests for CRLF | 8/8 PASS |
| Test-model and JSON contract tests | 58/58 PASS |
| Auto-spec focused regression | 56/56 PASS |
| Runtime configuration tests | PASS |

The broad `unittest discover` run executed 161 tests. It reported 10 import/fixture errors in the base host environment, including missing `pytest`, an unavailable `scripts.remote_judge_worker` import, and missing special-checker fixture paths. It produced no assertion failure in the changed focused suites.

## Oracle re-judge

### cf1008a

The copied replicate-3 artifacts were re-judged with 20 Accepted and 20 Wrong Answer submissions.

- TPR: **1.00**
- TNR: **1.00**
- CE/INFRA: **0**

This confirms that binary stdin eliminated the Windows CRLF verdict corruption. All 20 WA submissions were killed.

Artifact: `output/verification-20261014/cf1008a/report.json`.

### p02586

All 40 oracle sources now compile. The two previously blocked submissions were smoke-tested directly:

- `s267255158` (`numpy` + `numba.pycc`): compile PASS, run PASS, output `8`.
- `s528208375` (`numpy` + `numba` JIT): compile PASS, run PASS, output `8`.

The 8-worker re-judge produced TPR 0.55 and TNR 0.80. A sequential rerun of the nine Accepted submissions reported as TLE changed eight to PASS; only `s612162917` remained TLE. Therefore the runtime recovery is **19/20 Accepted (effective TPR 0.95)** when resource contention is removed. The remaining discrepancy is wall-clock timeout inflation under eight simultaneous CPU-heavy containers, rather than a missing package, compile failure, or memory cap.

Artifact: `output/verification-20261014/p02586/report.json`.

For final thesis measurements on CPU-heavy problems, use a single judge worker or calibrate concurrency per host. Reporting the 8-worker TPR as model quality would mix testcase quality with host scheduling contention.

## Commits

- `c119d92` Preserve LF input bytes in Docker judge
- `5f6f244` Extract checker and sandbox specs in test model
- `25e4542` Upgrade judge runtimes for contest submissions
- `2873721` Apply generated checker and sandbox specifications
- `6864c6b` Disable ambiguous CLI option abbreviations
- `3c3cde3` Parse explicit statement resource limits
- `5fbd8e0` Apply generated limits when resuming oracle evaluation
- `ba9fe9c` Support AtCoder Numba compilation in judge runtime
- `e689fa9` Allow compiled Python modules in sandbox runtime
