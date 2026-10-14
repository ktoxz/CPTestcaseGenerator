# Báo cáo refactor Final_TestcaseGenerator

Ngày thực hiện: 13/10/2026.

## Kết quả và phạm vi xác minh

Đã trực tiếp refactor source theo các giai đoạn, giữ ứng dụng Python dạng modular monolith. Đã kiểm tra end-to-end bằng fake generation/judge xác định, so sánh report và artifacts với implementation trước refactor. Chưa xác minh một run end-to-end bằng LLM thật, Docker/SSH thật hoặc CodeNet thật. Không coi bộ test hiện tại là hoàn toàn xanh: vẫn còn fixture thiếu và dependency `pyarrow` thiếu.

Thư mục làm việc không có Git metadata. Bản source trước khi sửa được lưu tại `tmp/refactor-original/`; danh sách source tạo/sửa nằm trong `tmp/refactor-file-inventory.json`. Không tạo commit, không thay dữ liệu bài toán để làm test pass.

## Kiến trúc và ownership

```text
main.py (entry point, compatibility cho batch callers)
  -> application/cli.py (parse/validate CLI, cấu hình và invocation)
  -> application/bootstrap.py (nối concrete adapters)
  -> application/run_pipeline.py: RunPipeline
       -> generation/test_model.py
       -> generation/solutions.py: SolutionGenerationService
       -> certification/reference_pool.py: ReferencePoolBuilder
       -> certification/mutant_pool.py: MutantPoolBuilder
       -> application/refinement.py: RefinementRunner
            -> generation/cases.py: CaseGenerationService
            -> certification/cases.py: CaseCertification
            -> application/case_proposals.py: CaseProposalRunner (repair orchestration)
            -> generation/feedback.py
       -> evaluation/holdout.py: HoldoutEvaluator
       -> reporting/report_builder.py
       -> evaluation/external.py: ExternalEvaluator
```

- `domain.py` giữ `Solution`, `Case`, `Result`, các ABC `Judge`, `SolutionGenerator`, `CaseGenerator`, `OracleSource`; không import concrete adapters.
- `llm_contract.py` định nghĩa `LLMClient`, `LLMRequest`, `TaskType`, `FailurePolicy` và các nhóm lỗi. Generation phụ thuộc contract, không import Ollama.
- `infrastructure/llm/ollama.py` sở hữu HTTP, timeout, parsing/retry. Claude và ChatGPT adapter hiện có được tái sử dụng tại `claude.py`, `chatgpt.py`.
- `evaluation/execution.py` sở hữu cache, batching, concurrency, alias kết quả reference và execution telemetry. Certification không truy cập trực tiếp dictionary cache nữa.
- `ReferenceCertification` sở hữu sample checks/quorum; `MutantCertification` sở hữu witness validation và two-trial evidence. Pool builders sở hữu replacement và lựa chọn pool.
- `CandidatePool`, `ReferencePoolResult`, `CaseCertificationResult`, `RefinementResult`, `HoldoutResult` là hợp đồng kết quả stage. `MutantPoolPolicy`, `RefinementPolicy` bất biến.
- `CaseCertificationState` chỉ chứa suite/index/intents/rejections/counters liên quan certification. `RefinementState` chỉ chứa tiến độ giữa các vòng. Không tạo một RunContext chứa toàn hệ thống.
- `CaseCertification` trả accepted/rejected/repair requests; không gọi LLM. `CaseProposalRunner` thực hiện repair và đối chiếu `proposal_index` trước khi chứng nhận lại.
- `policies.py` chứa quota, stop decision và pool splitting thuần; `evaluation/metrics.py` chứa metric computation thuần.
- `persistence.py` định nghĩa `RunStore` và `RunCheckpoint`; `FileRunStore` triển khai serialization/atomic replacement. Factory mặc định chỉ phục vụ compatibility cho các caller cũ; bootstrap truyền cùng store cho pipeline và solution generation.
- Reporting chỉ đọc kết quả đã có; không gọi judge hay LLM.

## Phase 0 — Inspection và baseline

Đã đọc các entry points, generator, provider adapters, pipeline, domain và regression tests liên quan; kiểm tra graph import và các ranh giới generation/certification/evaluation.

Baseline chạy lại trong môi trường hiện tại:

- Chạy toàn bộ `tests`: collection dừng vì `scripts/rebuild_hf_oracles.py` import `pyarrow.parquet` nhưng môi trường chưa cài `pyarrow`.
- Chạy riêng phần còn lại: **142 passed, 6 failed, 5 errors, 1 skipped**, thêm **16 subtests passed**.
- Ba failures do Ollama chưa triển khai `response_model`/schema theo các test hiện có.
- Ba failures và năm errors còn lại liên quan validator/checker fixture thiếu.

Log: `tmp/refactor-baseline.txt`, `tmp/refactor-baseline-runnable.txt`.

## Phase 1 — Transport và generation

Tạo `generation/solutions.py`, `generation/cases.py`, sau đó tách `generation/test_model.py`; chuyển HTTP/parser Ollama sang `infrastructure/llm/ollama.py`. Giữ alias `OllamaClient`, `OllamaSolutionGenerator`, `OllamaCaseGenerator` trong `testgen.ollama` cho caller cũ.

Lần kiểm tra ngay sau extraction: **61 passed, 3 failed**, thêm 2 subtests passed; ba failures là schema baseline đã xác định. Prompt/generation policy không đổi trong bước extraction này.

Log: `tmp/refactor-phase1.txt`.

## Phase 2 — Contracts và pure policies

- Call sites truyền `TaskType` tường minh. `label` chỉ dùng hiển thị, logging và tên raw-output artifact.
- `LLMRequest` kiểm tra loại task, failure policy, prompt/label và response model trước khi gọi provider.
- Fallback dùng task/policy để quyết định degraded response và witness backend limit. `TypeError`, `KeyError`, generic `ValueError`/`RuntimeError` từ lỗi lập trình không bị chuyển thành thành công rỗng.
- `LLMTransportError` và `LLMResponseError` tách transport với response validation; `LLMContractError` không thuộc nhóm được fallback nuốt lỗi.
- `generate_with_model(statement, test_model, output)` truyền model trực tiếp; generator không dò `output.parent/test-model.json` nữa. Method mới trong ABC mặc định gọi `generate(statement, output)` để hỗ trợ implementation cũ không cần model.
- Quota, stopping và pool splitting đã tách thành pure functions.

Các test cũ dùng label làm task hoặc tạo file lân cận để truyền context được migrate sang tham số tường minh. Giữ nguyên assertions về kết quả/prompt/số lần gọi; các lỗi giả lập provider đổi sang exception đã phân loại. Bổ sung test chứng minh thay label không đổi behavior, và model lân cận không được đọc.

## Phase 3 — Case certification

Tạo `certification/cases.py` và `application/case_proposals.py`; loại bỏ toàn bộ `nonlocal` khỏi workflow testcase. Giữ quy tắc normalization, hash dedup, coverage merge, consensus, official sample checks, repair limit và identity mapping.

Sau extraction, pipeline tests: **35 passed, 1 failed** do validator fixture baseline. Fixture repair trong golden regression kiểm tra cả rejection, repair và artifacts.

Log: `tmp/refactor-case-certification.txt`.

## Phase 4 — Reference/mutant certification và evaluation

Tạo các module `references.py`, `reference_pool.py`, `mutants.py`, `mutant_pool.py`; tách execution cache/batching vào `evaluation/execution.py`. Giữ ordered quorum, reference replacement, sample-preserving witness, stable official-sample fallback, replacement oversampling, minimum pool và witness early stop.

Holdout nhận suite đã lock; external evaluator kiểm tra hash trước/sau evaluation. Refinement chỉ nhận development candidates cho generation/feedback; holdout source không được đưa vào feedback.

Pipeline regression tiếp tục giữ 35 test pass và một fixture failure. Các tests về two-trial verification, witness early stop, holdout isolation, external lock, batching/concurrency và CE/INFRA semantics được chạy lại trong bộ cuối.

Log: `tmp/refactor-services.txt`, `tmp/refactor-stage-results.txt`.

## Phase 5 — Persistence và resume

`FileRunStore` ghi file tạm trong cùng thư mục, flush/fsync rồi `os.replace`. Khi replace lỗi, artifact đã commit giữ nguyên và file tạm được dọn. Các JSON artifacts của generation/certification/refinement/report dùng store serialization; prompt JSON vẫn thuộc tác vụ generation.

Checkpoint mới `checkpoint.json` có:

- `schema_version: 1`;
- `stage: suite_locked`;
- `problem_id`;
- toàn bộ cases gồm family, iteration, coverage_tags;
- report tại thời điểm suite đã hoàn tất, trước optional external evaluation.

Restore kiểm tra version/stage, kiểu dữ liệu case, ID trùng, problem ID và suite hash. `ResumeRun` đối chiếu cả exported `.in/.out` trước external evaluation. Artifact cũ không có checkpoint vẫn đi qua validation path cũ.

Checkpoint này hỗ trợ **resume external evaluation từ suite đã commit**, phù hợp CLI `--resume-oracle` hiện có. Không tuyên bố hỗ trợ tiếp tục một vòng generation dở dang: trước suite commit, cần chạy generation lại. Atomicity là mỗi file/checkpoint; không phải transaction cho cả thư mục. Execution JSONL vẫn là append telemetry, không phải checkpoint transaction.

Các test độc lập bảo vệ interrupted replacement, checkpoint round-trip, incompatible metadata, altered export và legacy resume.

## Phase 6 — Application, CLI và reporting

- `main.py` là entry point nhỏ.
- `application/cli.py` giữ parsing/validation/config/invocation; các định nghĩa `add_argument` được so sánh AST và **khớp nguyên bản**.
- `application/bootstrap.py` khởi tạo concrete LLM/judge/oracle/store.
- `application/batch_runner.py` điều phối subprocess theo bài; sử dụng lại toàn bộ CLI flags và report behavior cũ.
- `RunPipeline` gọi stage services; không chứa thuật toán consensus/case certification/mutant certification.
- `reporting/report_builder.py` lắp report từ stage results.
- `testgen.pipeline.Pipeline` vẫn là alias đến `RunPipeline`; một số execution/consensus hooks được giữ vì regression callers đang dùng. Không giữ các forwarding method đã không còn caller.

## Thay đổi behavior tách biệt với extraction

1. **Sửa lỗi schema đã có ở baseline:** Ollama hỗ trợ `response_model`, gửi JSON schema theo Ollama/OpenAI transport và validate/retry theo Pydantic. Test model task truyền `TestModelResponse`. Câu dẫn schema trong prompt đổi từ “with keys” sang “containing”; phần yêu cầu nghiệp vụ không thay đổi. Ba tests schema có sẵn từ failed thành passed. Đây là sửa contract bug, không phải thay đổi thuật toán sinh testcase/consensus.
2. **Contract migration theo yêu cầu:** gọi `ask_json` trực tiếp muốn task-specific semantics phải truyền `task_type`; chỉ truyền label không còn chọn task. Custom legacy clients chỉ có `ask_json` vẫn được bridge để nhận prompt/label/response_model.
3. **Filesystem context migration theo yêu cầu:** caller muốn tái sử dụng model phải truyền `generate_with_model`; không còn tự suy ra từ file cạnh thư mục output.
4. **Checkpoint mới:** additive artifact có schema riêng; report schema và các artifacts cũ giữ nguyên trên deterministic fixtures.

## Kết quả kiểm thử cuối

Lệnh (PowerShell, chạy từ repository):

```powershell
$env:TEMP = "$PWD\tmp"
$env:TMP = "$PWD\tmp"
.\.venv\Scripts\python.exe -m pytest tests -q --ignore=tests/test_rebuild_hf_oracles.py --tb=short
```

Kết quả thực tế: **166 passed, 3 failed, 5 errors, 1 skipped**, thêm **16 subtests passed**. Hai pytest collection warnings về class Pydantic `TestModelResponse` không phải test class.

Failures/errors còn lại, đều đã xuất hiện trước refactor:

- `tests/test_pipeline.py::PipelineTests::test_sample_validators`: thiếu `data/problems/p00004/validator.py`; test này còn cần fixture p00005.
- Hai tests p00954 trong `tests/test_special_checker.py`: checker script fixture không tồn tại.
- Năm errors trong `tests/test_p00061_validator.py`: setup không tải được validator fixture p00061.
- `tests/test_rebuild_hf_oracles.py` không được thu thập trong lệnh trên vì thiếu `pyarrow`; việc loại module được ghi rõ, không coi là pass.
- Native judge integration có một test skip trong môi trường hiện tại.

Log đầy đủ: `tmp/refactor-final-tests.txt`.

Kiểm tra bổ sung:

- `compileall` cho `testgen` và `main.py`: pass.
- `main.py --help`: pass; log `tmp/refactor-cli-help.txt`.
- Batch + new contracts + artifact parity sau thay đổi cuối của CLI: **26 passed**, log `tmp/refactor-final-focused.txt`.
- Quét symbol table các module mới không phát hiện global reference chưa định nghĩa. Không có mypy/ruff trong môi trường; không tuyên bố đã chạy static type checker.

### Deterministic artifact parity

Đã chạy cùng fake dependencies qua bản `tmp/refactor-original/testgen/pipeline.py` và implementation mới:

| Fixture | Artifacts cũ so sánh | Kết quả |
|---|---:|---|
| basic | 15 | Report và artifacts khớp |
| holdout | 19 | Report và artifacts khớp |
| repair | 17 | Report và artifacts khớp |

So sánh JSON theo cấu trúc, JSONL theo thứ tự, file source/input/output theo text. Chỉ chuẩn hóa temporary root và các trường thời gian `latency_ms`, `elapsed_seconds`, `target_met`. Suite hash, metrics, evidence, rejection reasons, feedback, pool membership và stop decisions không bị loại khỏi so sánh. Checkpoint mới có tests riêng.

Golden fixtures nằm tại `tests/fixtures/refactor/`; `tests/test_refactor_parity.py` chạy độc lập, không cần bản backup. Log đối chiếu trực tiếp bản cũ/mới: `tmp/refactor-parity.txt`.

## Cách chạy và mở rộng

CLI không đổi:

```powershell
.\.venv\Scripts\python.exe main.py --help
.\.venv\Scripts\python.exe main.py --problem <problem-id> --model ollama
.\.venv\Scripts\python.exe main.py --problem <problem-id> --oracle --resume-oracle <output-dir>
```

Các lệnh chạy thật vẫn cần statement/config, provider và judge khả dụng như trước. Không chạy LLM thật chỉ để tạo baseline.

Để thêm provider, triển khai `ask(LLMRequest) -> dict` và phân loại lỗi tại adapter; nối vào bootstrap. Generation không cần sửa để biết provider mới. Để thay quota/stop/split, sửa pure policies và tests tương ứng. Để thay storage, triển khai RunStore và inject qua composition root.

## Giới hạn và technical debt còn lại

- Chưa chạy Docker/SSH/LLM/CodeNet thật; golden fixtures không chứng minh parity cho mọi phản hồi ngẫu nhiên, transport hoặc mọi bài toán.
- Cần phục hồi fixture validator/checker và dependency pyarrow từ nguồn dự án trước khi có full green suite; không tự bịa fixture thay thế.
- Không hỗ trợ resume giữa một iteration LLM đang dang dở. Chỉ checkpoint stage `suite_locked` được khai báo hỗ trợ.
- Nhiều payload nội bộ vẫn là dict có schema cũ, nhất là candidate evidence/feedback; typed dataclass được ưu tiên ở stage boundaries, không rewrite mọi payload trong lần này.
- Prompt/source-validation trong `SolutionGenerationService` vẫn khá dài; giữ cùng module theo trách nhiệm để giảm nguy cơ thay prompt trong structural refactor.
- Artifact filenames vẫn được chọn tại một số stage call sites; bytes/JSON serialization và atomic writes đã tập trung trong store. Chưa tạo registry artifact hoàn chỉnh hoặc storage độc lập filesystem cho toàn hệ thống.
- Coverage claims chưa được chứng minh độc lập, output limits và execution isolation là các vấn đề của review ban đầu; không đổi các thuật toán đó trong refactor này.
- Một số rejection branch consensus/official-sample của implementation cũ không có `proposal_index`; refactor giữ nguyên report schema. Repair hiện chỉ tiêu thụ validator rejection và giữ identity của các item đó. Nếu cần identity cho mọi rejection, nên thay schema có version và test riêng.

Các giới hạn trên là phần chưa xác minh/chưa mở rộng, không được diễn giải thành tính năng đã hoàn thành.


## Cập nhật 14/10/2026 — Recovery cho pool mutant

Theo yêu cầu mới, nếu vẫn thiếu pool tối thiểu sau các replacement rounds cấu hình,
MutantPoolBuilder tự thử thêm tối đa 4 vòng. Với mặc định 4 replacement rounds,
vòng bổ sung dùng số vòng 5–8 để giữ ID/artifact riêng, tránh ghi đè vòng cũ.
Dừng ngay khi strict pool và verified sample fallback đủ minimum. Các mutant đã
chứng nhận được giữ lại; mọi đề xuất mới vẫn phải compile và chứng nhận như trước.

Lỗi transport/response/timeout/endpoint-busy ở lời gọi sinh mutant được ghi nhận
và tiêu thụ một attempt; lỗi lập trình và lỗi judge không bị che. Nếu hết cả bốn
vòng bổ sung vẫn thiếu minimum, stage lưu evidence và báo lỗi rõ số vòng đã thử.
Không thể bảo đảm LLM luôn sinh thành công trong một số lượt hữu hạn.

Chỉ khi recovery được dùng hoặc có generation failure, artifact mutant-certification
thêm trường recovery chứa additional_rounds_allowed, additional_rounds_used,
total_replacement_rounds_used và generation_failures. Các run đủ pool trong vòng
thường giữ nguyên artifact và đã pass golden parity.

Kiểm thử: tests/test_mutant_recovery.py, tests/test_pipeline.py và
 tests/test_refactor_parity.py: 44 passed, 1 failed do fixture p00004/validator.py
thiếu từ baseline. Log: tmp/mutant-recovery-tests.txt. Chưa chạy LLM thật hoặc
chạy lại experiment repeated-runs trong thay đổi này.
