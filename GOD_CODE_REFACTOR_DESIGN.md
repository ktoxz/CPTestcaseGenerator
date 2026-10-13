# Đánh giá God code và đề xuất refactor system design

Ngày đánh giá: 13/10/2026  
Phạm vi: `Final_TestcaseGenerator`  
Trạng thái: Đề xuất thiết kế, chưa triển khai refactor.

## 1. Kết luận

Codebase có các abstraction hữu ích như `Judge`, `CaseGenerator`, `SolutionGenerator`, `OracleSource` và `Checker`. Tuy nhiên, phần triển khai nghiệp vụ vẫn tập trung vào `Pipeline` và các generator trong `ollama.py`.

Vấn đề chính không chỉ là file dài. Một thành phần đang sở hữu nhiều trách nhiệm, nhiều trạng thái và nhiều lý do để thay đổi. Khi sửa một chính sách nhỏ, người phát triển phải hiểu một vùng code lớn và các tác động gián tiếp của nó.

Hướng phù hợp là **modular monolith**: giữ một ứng dụng Python, tách module theo trách nhiệm nghiệp vụ, truyền dependency tường minh và refactor từng phần. Chưa cần chuyển sang microservices hoặc thêm message broker.

## 2. Thiết kế hiện tại

```text
main.py: parse CLI, cấu hình, khởi tạo backend
    |
    v
Pipeline.run()
    ├── Xây test model
    ├── Sinh references, validator, mutants
    ├── Chứng nhận references và mutants
    ├── Sinh baseline
    ├── Validate, dedup, consensus, repair testcase
    ├── Chấm, cập nhật feedback, adaptive refinement
    ├── Quyết định dừng
    ├── Khóa suite, đánh giá holdout và CodeNet
    └── Ghi artifact, snapshot, metrics và report
```

Các điểm mở rộng hiện có là nền tảng nên giữ lại. Đặc biệt, việc tách external evaluation khỏi generation và khóa suite trước đánh giá là những invariant cần bảo toàn trong quá trình refactor.

## 3. Các điểm tập trung trách nhiệm

### 3.1. `Pipeline`: God class và God method

Tại thời điểm inspect, `testgen/pipeline.py` có khoảng 2.267 dòng; `Pipeline.run()` bắt đầu ở dòng 911 và kéo dài khoảng 1.350 dòng.

| Trách nhiệm hiện tại | Vị trí tham khảo | Thành phần nên sở hữu |
|---|---|---|
| Điều phối toàn workflow | `pipeline.py:911`, `Pipeline.run` | `RunPipeline` |
| Thực thi, batch và cache | `_execute_many`, `_compile_pool`, `_judge_pool` | `ExecutionService` |
| Chọn expected theo reference | `pipeline.py:434`, `_reference_consensus` | `ReferenceConsensus` |
| Chứng nhận reference | Hàm `certify_reference` bên trong `run` | `ReferenceCertification` |
| Chứng nhận và bổ sung mutant | `pipeline.py:557`, `_certify_mutant`, cùng logic trong `run` | `MutantCertification` |
| Chứng nhận testcase | `pipeline.py:1661`, `certify_proposals` | `CaseCertification` |
| Quota, feedback và điều kiện dừng | Logic refinement bên trong `run` | `RefinementPolicy` và `RefinementState` |
| Ghi file và phục hồi | Các lệnh ghi JSON/JSONL, `resume_oracle` | `RunStore` và use case resume |
| Tổng hợp kết quả | Metrics và phần tạo report | `ReportBuilder` |

Các hàm lồng nhau `certify_proposals`, `accept_validated`, `validate_batch` phụ thuộc vào biến của scope bên ngoài, một số dùng `nonlocal`. Vì vậy chữ ký hàm chưa thể hiện đầy đủ dữ liệu mà chúng đọc hoặc thay đổi.

Hệ quả:

- Khó test riêng một bước mà không dựng nhiều trạng thái của pipeline.
- Khó xác định thành phần nào sở hữu và được phép thay đổi một tập dữ liệu.
- Thay đổi quota hoặc certification dễ ảnh hưởng feedback, counters và reporting.
- Việc phục hồi phải tái tạo trạng thái phân tán giữa biến trong RAM và nhiều artifact.

**Không giải quyết bằng cách chỉ chia `run()` thành các hàm `_step_1`, `_step_2` cùng đọc/ghi hàng chục thuộc tính trên `self`.** Cần tách cả trách nhiệm và quyền sở hữu trạng thái.

### 3.2. `ollama.py`: trộn transport và nghiệp vụ

File có khoảng 2.734 dòng, gồm ba khối lớn:

- `OllamaClient`, bắt đầu ở dòng 187: gọi endpoint, timeout, parsing, xử lý response.
- `OllamaSolutionGenerator`, bắt đầu ở dòng 598: sinh code, kiểm tra source, mutation, witness và replacement.
- `OllamaCaseGenerator`, bắt đầu ở dòng 1934: test model, testcase, repair, audit và context compaction.

Tên generator gắn với Ollama nhưng generator thực tế có thể nhận client của provider khác. Đây là dấu hiệu nghiệp vụ chưa được đặt đúng tầng.

Nên tách:

| Nghiệp vụ độc lập provider | Adapter hạ tầng |
|---|---|
| `TestModelBuilder` | `OllamaClient` |
| `SolutionGenerationService` | `ClaudeClient` |
| `CaseGenerationService` | `ChatGPTClient` |
| `WitnessGenerationService` khi cần tách riêng | `FallbackClient` |

Prompt và schema thuộc từng tác vụ. Adapter chịu trách nhiệm chuyển request thành giao thức HTTP/CLI, xử lý lỗi transport và trả dữ liệu đã được validate theo contract.

Không nhất thiết tạo một class cho mỗi prompt. Chỉ tách khi có trách nhiệm, dependency hoặc vòng đời khác biệt.

### 3.3. Dependency ngầm qua filesystem

Trong `ollama.py:843`, generator đọc `output.parent / "test-model.json"` để lấy phân tích đã tạo trước đó.

Interface công khai chỉ nhận `statement` và `output`, nhưng kết quả còn phụ thuộc vào file nằm ngoài tham số nghiệp vụ. Di chuyển artifact hoặc chạy generator độc lập có thể làm hành vi thay đổi.

Thiết kế đề xuất:

```python
def generate_solutions(
    problem: ProblemSpec,
    test_model: TestModel,
    policy: SolutionGenerationPolicy,
) -> GeneratedCandidates:
    ...
```

`RunStore` lưu test model; caller truyền model trực tiếp cho generator. Generator không dò artifact để suy ra context.

### 3.4. Chính sách điều khiển phụ thuộc chuỗi hiển thị

`FallbackLLMClient._neutral_result`, tại `fallback.py:23`, phân biệt tác vụ bằng nội dung `label`. Việc nhận diện shape trong Ollama cũng sử dụng label.

Điều này khiến một thay đổi câu log có thể ảnh hưởng fallback hoặc cách validate response.

Nên có request chứa:

- `task_type`: định danh có kiểu, ví dụ `BUILD_TEST_MODEL`, `GENERATE_CASES`.
- `response_model`: schema kết quả.
- `failure_policy`: tác vụ bắt buộc hay cho phép kết quả degraded.
- `label`: chỉ dùng để hiển thị.

Fallback chỉ xử lý lỗi đã phân loại. Lỗi lập trình hoặc lỗi contract không nên bị biến thành một kết quả rỗng trông giống thành công.

### 3.5. `main.py`: composition root đang quá rộng

`main.py` có khoảng 770 dòng, xử lý CLI, cấu hình, batch, khởi tạo LLM/judge, chuẩn bị output và báo cáo.

Nên giữ CLI mỏng và chuyển phần nối dependency vào `bootstrap.py`. Batch runner là một use case riêng, tái sử dụng cấu hình đã resolve thay vì tiếp tục mở rộng logic xử lý argv trong entry point.

## 4. Kiến trúc đích

```text
testgen/
├── application/
│   ├── run_pipeline.py
│   ├── resume_run.py
│   ├── batch_runner.py
│   └── bootstrap.py
├── domain/
│   ├── models.py
│   ├── policies.py
│   └── ports.py
├── generation/
│   ├── test_model.py
│   ├── solutions.py
│   ├── cases.py
│   └── prompts/
├── certification/
│   ├── references.py
│   ├── mutants.py
│   └── cases.py
├── evaluation/
│   ├── execution.py
│   ├── evaluator.py
│   └── metrics.py
├── infrastructure/
│   ├── llm/
│   ├── judges/
│   ├── oracle_sources/
│   └── file_run_store.py
└── reporting/
    └── report_builder.py
```

Đây là cấu trúc đích minh họa, không phải yêu cầu tạo toàn bộ thư mục ngay trong lần sửa đầu tiên.

### Quy tắc dependency

1. Domain không import HTTP, subprocess, CLI hoặc concrete adapter.
2. Các service generation, certification và evaluation dùng port thay vì tự khởi tạo provider.
3. Application điều phối service và checkpoint; không triển khai thuật toán certification.
4. Infrastructure triển khai các port.
5. `bootstrap.py` biết các concrete class để nối chúng lại.
6. Reporting đọc kết quả đã có; không gọi LLM hoặc chạy lại judge.

### Hợp đồng giữa các thành phần

| Thành phần | Input chính | Output chính | Quyền sở hữu |
|---|---|---|---|
| `TestModelBuilder` | Problem specification | Test model và generation evidence | Tạo mô hình kiểm thử |
| `SolutionGenerationService` | Problem, test model, generation policy | Candidate pool | Đề xuất source |
| `ReferenceCertification` | Reference candidates, official samples | Certified references, rejected candidates, evidence | Chứng nhận pool reference |
| `MutantCertification` | Mutants, references, validator, policy | Certified mutant pool, evidence | Chứng nhận mutant và quản lý replacement |
| `CaseCertification` | Proposals, validator, references, suite index | Accepted/rejected cases, evidence, đề nghị repair | Quyết định tính hợp lệ của testcase |
| `ExecutionService` | Source artifact, execution jobs, runtime config | Execution results | Cache, batch, concurrency |
| `RefinementPolicy` | Round results và state | Tiếp tục/dừng, quota, mục tiêu vòng sau | Quyết định chính sách |
| `RunStore` | Stage result hoặc checkpoint | Artifact reference hoặc restored state | Persistence và serialization |

`CaseCertification` có thể trả các trường hợp cần sửa để application gọi `CaseGenerationService.repair`. Cách này giữ việc gọi LLM ra khỏi thuật toán xác nhận tính hợp lệ.

## 5. Quản lý trạng thái

Không gom mọi biến vào một `RunContext` khổng lồ rồi truyền cho tất cả service. Cách đó chỉ di chuyển God object sang một tên mới.

Tách trạng thái theo phạm vi:

- `RunConfig`: cấu hình bất biến đã resolve.
- `ProblemSpec`: statement, samples và các artifact liên quan đến bài.
- `CandidatePool`: references, development mutants, holdout mutants.
- `RefinementState`: cases, coverage, survivors, lịch sử vòng và counters cần cho policy.
- `CertificationEvidence`: kết quả xác nhận và lý do loại.
- `RunCheckpoint`: dữ liệu cần thiết để tiếp tục tại một stage xác định.

Mỗi stage nhận phần dữ liệu cần dùng và trả một result có kiểu. Chỉ orchestrator cập nhật trạng thái xuyên stage. Execution cache là chi tiết của execution service, không phải nơi lưu nghiệp vụ chứng nhận.

Ưu tiên dataclass cho trạng thái nội bộ và schema validation cho dữ liệu tại ranh giới LLM/file. Không cần thay tất cả `dict` trong một lần; bắt đầu từ hợp đồng giữa các stage.

## 6. Hình dạng orchestrator sau refactor

Ví dụ sau chỉ minh họa trách nhiệm; chưa thể thay trực tiếp implementation hiện tại:

```python
model = test_model_builder.build(problem)
candidates = solution_generator.generate(problem, model)
references = reference_certifier.certify(problem, candidates)
mutants = mutant_certifier.certify(problem, references, candidates)

state = refinement.initialize(problem, model, references, mutants)

while refinement.should_continue(state):
    proposals = case_generator.generate(state.generation_context())
    certified = case_certifier.certify(proposals, references)
    evaluation = evaluator.evaluate(state.development_pool, certified)

    state = refinement.advance(state, certified, evaluation)
    run_store.checkpoint(state)

suite = suite_locker.lock(state.cases)
holdout_result = holdout_evaluator.evaluate(suite, state.holdout_pool)
external_result = external_evaluator.evaluate(suite)
return report_builder.build(state, holdout_result, external_result)
```

Trong implementation đầy đủ, validator, repair, budget, optional external evaluation và error handling cần được biểu diễn tường minh. Orchestrator vẫn chịu trách nhiệm thứ tự và điều kiện chạy các stage.

## 7. Lộ trình refactor

### Bước 0 — Thiết lập baseline

- Xác định các test đang fail do implementation, fixture thiếu hoặc môi trường.
- Chọn fixture nhỏ và fake LLM/judge có kết quả xác định cho regression tests.
- Ghi nhận cấu trúc report, suite hash và các quyết định certification cần bảo toàn.

Không dùng một lần gọi LLM thật làm chuẩn so sánh duy nhất vì response có thể thay đổi.

### Bước 1 — Tách module khỏi `ollama.py`

- Chuyển client, solution generator và case generator sang module riêng.
- Giữ re-export tại đường import cũ trong giai đoạn chuyển tiếp.
- Chưa thay prompt hoặc chính sách generation trong cùng thay đổi này.

Tiêu chí hoàn thành: các caller tiếp tục hoạt động; chỉ thay cấu trúc module.

### Bước 2 — Chuẩn hóa hợp đồng và tách policy thuần

- Thống nhất `LLMClient` protocol và task type.
- Truyền test model trực tiếp thay việc dò file.
- Tách quota, stop criteria, pool splitting và metrics thành hàm hoặc policy không I/O.

Tiêu chí hoàn thành: có thể test policy chỉ với dữ liệu trong RAM; thay câu log không đổi hành vi.

### Bước 3 — Tách `CaseCertification`

- Đưa logic validate, dedup và consensus ra khỏi các hàm lồng nhau.
- Biểu diễn accepted cases, rejection reasons, coverage claims và repair requests bằng result có kiểu.
- Loại các phụ thuộc `nonlocal` bằng input/output tường minh.

Tiêu chí hoàn thành: kiểm tra được certification của một batch mà không chạy toàn pipeline.

### Bước 4 — Tách reference và mutant certification

- Di chuyển sample checks, witness checks và replacement policy vào các service tương ứng.
- Giữ phân biệt mutant vượt sample và official-sample fallback.
- Trả pool cùng evidence, không tự ghi report của toàn run.

Tiêu chí hoàn thành: thay chính sách mutant không cần chỉnh serializer hoặc reporting.

### Bước 5 — Gom persistence và checkpoint

- Tạo `FileRunStore` trước, chưa cần database.
- Gom quy ước tên artifact và serialization vào một nơi.
- Bổ sung schema version cho checkpoint và cách ghi atomic.
- Tách use case resume khỏi thuật toán generation.

Tiêu chí hoàn thành: stage nghiệp vụ không tự dựng đường dẫn JSON hoặc gọi `write_text`.

### Bước 6 — Thu gọn application và CLI

- `RunPipeline` điều phối các service đã tách.
- `main.py` parse CLI, dựng config và gọi use case.
- `bootstrap.py` khởi tạo concrete adapters.
- Xóa compatibility wrappers sau khi tất cả caller đã chuyển đổi.

## 8. Kiểm chứng trong quá trình refactor

Các regression test cần bảo vệ hành vi có ý nghĩa:

- Baseline không nhận source hoặc execution feedback của mutants.
- Holdout không đi vào adaptive feedback; external evaluation chỉ chạy sau suite lock.
- Refactor không làm mất bằng chứng chứng nhận hoặc nhập nhằng các loại mutant.
- CE/INFRA không được tính thành phát hiện lỗi logic.
- Case bị từ chối giữ nguyên lý do và liên kết proposal để repair đúng item.
- Local và remote judge tuân theo cùng execution contract.
- Checkpoint đọc lại khôi phục đúng stage và state đã commit.

Không viết test chỉ để kiểm tra một method gọi method khác đúng một lần nếu điều đó không bảo vệ một invariant nghiệp vụ.

Tại lần kiểm tra ngày 13/10/2026, sau khi chuyển thư mục tạm vào workspace: **142 passed, 6 failed, 5 errors, 1 skipped**; có thêm 16 subtests passed. Một module bị loại khỏi lần chạy này vì thiếu `pyarrow`. Ba failure liên quan contract schema Ollama; các failure/error còn lại liên quan fixture validator/checker thiếu. Đây là baseline cần phân loại trước khi đánh giá regression, không phải chứng nhận toàn hệ thống đã chạy đúng.

Log: [design-review-tests-workspace-temp.txt](tmp/design-review-tests-workspace-temp.txt).

## 9. Tách refactor cấu trúc khỏi thay đổi hành vi

Các vấn đề đã phát hiện như coverage chưa được xác minh, coverage model rỗng, isolation giữa executions và giới hạn output cần được xử lý. Tuy nhiên, nên thực hiện bằng thay đổi riêng với test mô tả hành vi mới.

Ví dụ:

1. Tách `ReferenceConsensus` và giữ nguyên quy tắc hiện tại.
2. Sau khi có test độc lập, đánh giá thay đổi quy tắc consensus hoặc bổ sung provenance.

Nếu vừa di chuyển code vừa đổi thuật toán trong một thay đổi lớn, khi kết quả khác đi sẽ khó xác định nguyên nhân.

## 10. Tiêu chí hoàn thành

- Thay provider LLM không cần sửa workflow generation/certification.
- Thay quota hoặc stop policy không cần sửa judge hay persistence.
- Thay cấu trúc lưu checkpoint không cần sửa thuật toán chứng nhận.
- Test được từng stage bằng fake dependency nhỏ.
- Không còn dependency ngầm vào vị trí artifact.
- Không còn dùng label hiển thị để quyết định nghiệp vụ.
- Trạng thái có owner rõ ràng; stage không tùy ý sửa toàn bộ run.
- Orchestrator thể hiện được workflow khi đọc từ trên xuống, không chứa các thuật toán chi tiết.

Mục tiêu là giảm phạm vi kiến thức cần có khi sửa một chức năng. Số dòng giảm là hệ quả, không phải tiêu chí duy nhất.

## 11. Tham chiếu mã nguồn

Các số dòng dưới đây theo snapshot đã inspect và có thể thay đổi sau refactor:

- [testgen/pipeline.py](testgen/pipeline.py): `Pipeline` dòng 176; `run` dòng 911; certification testcase từ dòng 1661.
- [testgen/ollama.py](testgen/ollama.py): client dòng 187; solution generator dòng 598; case generator dòng 1934; đọc test model ngầm dòng 843.
- [testgen/domain.py](testgen/domain.py): domain models và các extension point hiện có.
- [testgen/fallback.py](testgen/fallback.py): phân loại tác vụ theo label tại `_neutral_result`, dòng 23.
- [main.py](main.py): CLI và phần khởi tạo dependencies.

Tài liệu này tập trung vào tổ chức code và ranh giới trách nhiệm. Nó không thay thế một đợt kiểm thử end-to-end bằng LLM/Docker thật.
