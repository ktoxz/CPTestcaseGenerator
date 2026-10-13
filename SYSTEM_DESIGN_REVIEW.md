# Rà soát system design: pipeline và kiến trúc code

Ngày: 10/10/2026.

Tài liệu gộp hai phần:

1. **Thiết kế pipeline và hiệu năng:** quan hệ phụ thuộc giữa các bước, điểm nghẽn, ngân sách retry và tính đúng đắn của điều kiện dừng.
2. **Thiết kế kiến trúc code:** phân chia trách nhiệm, interface, dependency, domain model và vòng đời state.

P1 là vấn đề ưu tiên cao do có thể gây lãng phí lớn, thất bại hoặc sai hành vi; P2 là vấn đề cần cải thiện sau các lỗi ưu tiên cao. Mức ưu tiên không đồng nghĩa mọi lỗi đều đã xuất hiện trong log.

## I. Thiết kế pipeline và hiệu năng

Phạm vi: main.py, pipeline, LLM clients/generators, fallback, Docker/remote judge, coverage và latency có sẵn. Không chạy inference, Docker hoặc submission trong lần review này; không sửa mã thực thi. Đã chạy một probe bằng fake client để kiểm tra quota/dedup. Workspace không có Git metadata; nội dung ollama.py đã thay đổi trong lúc đọc, nên số dòng là vị trí quan sát cuối và log cũ không được coi là benchmark của phiên bản hiện tại.

### Bằng chứng thời gian

| Run | Khoảng thời gian giữa event đầu/cuối | Tổng ollama.request | Điểm đáng chú ý |
|---|---:|---:|---|
| output/p02574/20261010-155743 | 1.559,7 s | 1.401,8 s / 15 request | Sinh mutant 480,1 s; audit 298,8 s; baseline 230,5 s |
| output/batches/20261010-160446/problems/p02781 | 1.437,6 s | 1.160,2 s / 17 request | Một stage replacement mất 1.107,8 s |
| output/batches/20261010-162624/problems/p02732 | 1.908,4 s | 1.855,1 s / 19 request | Top-up một testcase mất 335,1 s; không có report khi đọc |

Các tổng thời gian component có thể chồng nhau hoặc chạy song song; không cộng chúng để suy ra wall time. Run p02574 dùng timeout 300 s, khác mặc định hiện tại 50 s. Không có report chưa đủ để kết luận crash. Chi phí output_log trong các log kiểm tra rất nhỏ; không có bằng chứng logging là nút thắt chính.

### 1. P1 — Nhiều request đơn chạy tuần tự, workers không có tác dụng với inference

Vị trí: testgen/ollama.py:989, :1936, :2364, :2555; main.py:149.

AC, testcase, repair, audit đều được tách ra từng sản phẩm rồi gọi đồng bộ. llm_workers được lưu nhưng _run_case_jobs không dùng executor. repair_batch/audit_batch chia danh sách thành từng phần tử vì MAX_REPAIRS_PER_REQUEST và MAX_AUDITS_PER_REQUEST đều bằng 1. Batch nhiều bài cũng đợi từng subprocess kết thúc.

Ở đường thành công thông thường, 1 test model + 3 AC + 1 validator + khoảng 5 mutant + 20 testcase đã khoảng 30 request, chưa tính repair/audit/replacement. Với trung bình giả định 10 s/request, riêng inference đã khoảng 5 phút. Đây là mô hình chi phí, không phải benchmark.

Hướng sửa: scheduler với giới hạn theo backend; local GPU có thể vẫn cần concurrency 1, nhưng cloud có thể dùng concurrency nhỏ hoặc micro-batch. Bật workers một cách thật sự hoặc bỏ tham số gây hiểu nhầm. Không tăng đồng thời số bài và số request mà thiếu giới hạn tổng tài nguyên.

### 2. P1 — Ngân sách retry nhân qua nhiều lớp, không có deadline toàn job

Vị trí: testgen/fallback.py:84; testgen/ollama.py:303, :949, :1313; testgen/pipeline.py:1357; main.py:164.

Mỗi job thử lại chuỗi backend từ đầu. Deadline LLM được khởi tạo lại mỗi JSON attempt. Bên ngoài còn generation rounds, count+2 request cho mutant, replacement rounds, witness repair, testcase repair và top-up. Không có circuit breaker ghi nhớ backend đang hỏng; cũng không có ngân sách tổng request/thời gian cho bài. Subprocess batch không có timeout.

Một job có ba backend timeout 50 s sẽ tốn khoảng 150 s. Nếu backend trả JSON lỗi sát deadline rồi repair tiếp, tổng có thể cao hơn; 150 s không phải trần chung của ask_json. Khi dùng 300 s, riêng chuỗi ba timeout có thể khoảng 15 phút.

Hướng sửa: truyền absolute deadline từ bài → stage → job → backend; mọi attempt dùng phần ngân sách còn lại. Circuit breaker theo endpoint/model, cooldown và phân loại lỗi. Tác vụ tùy chọn cần ngân sách nhỏ riêng.

### 3. P1 — Validator là dependency cốt lõi nhưng fail-fast quá muộn

Vị trí: testgen/pipeline.py:908–911, :1789, :1836; testgen/ollama.py:1041–1075; main.py:656.

Pipeline chỉ áp dụng validator_override sau solution_generator.generate. Generator vẫn bắt buộc sinh validator_python không rỗng và có thể thất bại vì validator LLM dù đã có validator local. Validator được compile sớm, nhưng kiểm tra sample chính thức chỉ diễn ra sau khi đã sinh/chứng nhận mutant và sinh baseline.

Validator sai semantics có thể khiến witness hợp lệ bị loại, dẫn đến repair/replacement tốn nhiều request; cuối cùng mới dừng vì validator từ chối sample. Đây là lãng phí có thể tránh trước inference đắt tiền.

Hướng sửa: resolve validator override trước generator; bỏ hẳn request validator nếu đã có. Compile và kiểm tra toàn bộ sample ngay sau khi có validator, trước mutant. Sample chỉ là sanity check, không chứng minh validator đúng đầy đủ.

### 4. P1 — Quota động có thể lớn hơn số proposal pipeline có khả năng tạo

Vị trí: testgen/pipeline.py:111, phần clamp requested_count trong run; testgen/ollama.py:1830, :2218, :2430.

dynamic_case_bounds cho phép tới 3×base, nhưng baseline/adaptive chỉ tạo tối đa 10 proposal; mỗi top-up cũng tối đa 10. Với top_up_rounds=1 mặc định, quota >20 không thể đạt ngay cả khi mọi proposal đều hợp lệ và khác nhau.

Probe fake client đã chạy: base=10, survivors=4, uncovered_critical=24 → bounds=(26,30), generator chỉ gọi 10 request và trả requested_count=10; pipeline clamp ngược lên 26. Trần 20 proposal không thể đáp ứng 26 accepted. Điều này không tạo vòng lặp vô hạn, nhưng gây thiếu quota có tính cấu trúc và tiêu tốn top-up/vòng sau.

Hướng sửa: tách số case mỗi request khỏi tổng quota; scheduler tiếp tục từng nhóm nhỏ tới quota hoặc budget. Tính feasibility trước khi chạy, và ghi rõ budget_exhausted thay vì mục tiêu không thể đạt.

### 5. P1 — Dedup và chứng nhận đến sau toàn loạt inference

Vị trí: testgen/ollama.py:1936–1985, :1313; testgen/pipeline.py:1342–1356, :1387–1416.

_run_case_jobs thu tất cả response rồi mới merge/dedup. Các prompt đã dựng trước, không nhận input vừa sinh ở các request trước cùng loạt. Fake client trả cùng một input cho mỗi request: 10 lần gọi chỉ giữ được 1 case. Sau đó pipeline phải top-up. Với temperature=0 cho testcase và các focus lặp lại, thiếu phản hồi chống trùng là rủi ro thực tế; probe không khẳng định tỷ lệ trùng của model thật.

Mutant cũng được sinh hết proposal_count (và request bù định dạng/trùng), compile hết, rồi mới certify. Dừng sớm chỉ có giữa các loạt; không dừng được những request đã sinh thừa trong loạt hiện tại.

Hướng sửa: producer-consumer theo từng kết quả: generate → dedup → validate/compile → certify → cập nhật feedback/quota. Giữ một cửa sổ nhỏ request đang chạy và ngừng cấp việc ngay khi đủ.

### 6. P2 — Container/SSH quá vụn; fail-fast ở pool xảy ra sau khi chạy cả batch

Vị trí: testgen/docker_judge.py:27; testgen/domain.py:230; testgen/remote_judge.py:38; scripts/remote_judge_worker.py:44; testgen/pipeline.py:351, :425, :1749.

Mỗi execution tạo docker run mới. Remote mở ssh + Python worker cho mỗi request; run_many chỉ gộp transport, vẫn lặp tuần tự tạo container. Reference consensus chạy từng reference cho từng input, và accept_validated xử lý input lần lượt: judge_workers không song song hóa đoạn này.

_judge_pool nhận kết quả cả batch trước khi xem testcase đầu tiên fail. Với batch_size=8, một solution TLE mọi case có thể tốn khoảng 8×5=40 s chạy code thay vì 5 s, cộng overhead; sau đó mới dừng solution.

Hướng sửa: worker/connection bền vững; task queue có giới hạn cho reference và validator; batch nhỏ thích nghi cho solution chưa biết, hoặc checker/fail-fast phía worker. Giữ process execution sạch và isolation giữa test; không tái sử dụng trạng thái submission tùy tiện.

### 7. P1 — Giới hạn stdout/stderr chỉ cắt sau khi đã giữ toàn bộ output trong RAM

Vị trí: testgen/docker_judge.py:44–65; scripts/remote_judge_worker.py:32, :109.

subprocess.run capture toàn bộ stdout/stderr, rồi mới slice theo stdout_limit_bytes/stderr_limit_bytes. Submission in vô hạn có thể làm host Python tốn RAM, paging hoặc chết trước khi timeout. Giới hạn memory của container không giới hạn bộ đệm Python phía host. Slice chuỗi cũng không phải giới hạn byte UTF-8.

Đây là lỗi tiềm tàng nghiêm trọng, chưa có bằng chứng log rằng nó gây những run chậm được thống kê ở trên.

Hướng sửa: đọc stream với bộ đếm byte, giới hạn trong lúc đọc, chấm output-limit và hủy execution/container khi vượt giới hạn. Không chỉ truncate sau communicate.

### 8. P2 — Điều kiện dừng dùng tín hiệu chất lượng chưa đủ tin cậy

Vị trí: testgen/coverage.py:147; testgen/pipeline.py:1008, :1980.

Coverage hiện là hợp các tag do LLM khai báo, không có predicate kiểm tra input thật có đạt boundary/stress/partition đó hay không. Tag sai có thể khiến dừng sớm sai; thiếu tag dù case đã phủ thì làm chạy thêm.

candidate_ac giữ cả AC bị loại khỏi reference. Với mặc định 3 AC, chỉ một AC thực chất sai và bị suite bắt sẽ làm TPR còn 2/3, thấp hơn 0.9: thêm testcase không thể giúp AC đó pass lại. Early-stop trở nên bất khả thi, dù tăng vòng vẫn không sửa được nguyên nhân. Số vòng vẫn bị giới hạn, nên không phải loop vô hạn.

Hướng sửa: phân biệt candidate-label metric dùng nghiên cứu với readiness của reference/suite. Coverage cần predicate hoặc evidence có thể kiểm chứng; nếu chỉ là tag thì ghi rõ claimed coverage và không dùng như hard gate tuyệt đối.

### Các vấn đề phụ cần theo dõi

- Cache execution dùng (solution.id, case_id, input), nên cùng input qua sample certification/witness/final suite có ID khác sẽ chạy lại. Có thể cache theo source hash + input + runtime/limits, với bypass riêng cho hai trial kiểm tra ổn định. Tuyệt đối không gộp hai trial thành một kết quả cache.
- Chỉ có resume-oracle. Lỗi trước suite lock không có checkpoint/resume tổng quát để tận dụng test model, AC và mutant đã chứng nhận.
- _input_contract và _problem_core cắt theo heading/giới hạn ký tự. Constraints ở phần khác có thể biến mất khỏi prompt, khiến repair lặp sai. Cần representation của input contract đã kiểm chứng, không chỉ substring.
- HTTP timeout đóng response đồng bộ và không xác nhận inference phía server đã được hủy. Cần kiểm tra cancellation thực tế trước khi coi đây là hard cancellation của workload, đặc biệt backend local.
- README mô tả sửa testcase theo batch chung nhưng implementation hiện giới hạn một item/request. Cần đồng bộ tài liệu và CLI với hành vi thật.

### Thứ tự sửa đề xuất

1. Fail-fast validator, bỏ sinh validator khi có override; chặn output trong lúc đọc.
2. Deadline/ngân sách tổng và circuit breaker; lưu checkpoint sau mỗi stage đã chứng nhận.
3. Sửa quota, dedup online và generate/certify theo cửa sổ nhỏ.
4. Đo concurrency phù hợp mỗi backend rồi mới bật workers; giảm SSH/container overhead và batch chạy thừa.
5. Tách metric nghiên cứu khỏi stop gate, kiểm chứng coverage.

Đo lại cùng bài, cùng backend/config và nhiều lần chạy: thời gian tới testcase hợp lệ đầu tiên; tổng request/token; latency từng stage; tỷ lệ duplicate/invalid; số execution/container; thời gian tới suite lock; chất lượng suite. Giữ oracle holdout độc lập, không dùng oracle để giảm giả tạo thời gian bằng cách rò dữ liệu vào generation.

### Vấn đề ở mức kiến trúc luồng xử lý

**Mutant chặn baseline dù baseline không cần mutant.** Luồng hiện tại đi từ test model, AC/validator, chứng nhận reference, sinh/chứng nhận/sửa mutant rồi mới sinh baseline. Baseline vốn chỉ cần statement và test model để sinh proposal, và validator/reference để chứng nhận. Nên tách baseline và mutant thành hai nhánh sau khi dependency tương ứng sẵn sàng; adaptive generation mới chờ mutant. Nếu thí nghiệm yêu cầu đủ mutant, vẫn lưu suite hợp lệ và ghi trạng thái thí nghiệm chưa đầy đủ khi thiếu pool.

**Các thành phần kiểm chứng có thể cùng chia sẻ một sai lầm.** Test model, validator, reference và mutant có thể đều do cùng LLM sinh từ một cách hiểu đề. Hai source khác nhau cùng pass sample và đồng thuận output chưa chứng minh độc lập về sai sót. Cần phân cấp độ tin cậy của artifact, dùng validator/reference đã kiểm toán khi có, và ghi rõ consensus chỉ là đồng thuận. Oracle dùng đánh giá cuối phải tiếp tục độc lập với generation.

**Feedback loop chưa luôn phân biệt lỗi dependency với thiếu proposal.** Validator sai, reference sai, input contract bị cắt mất constraint và backend lỗi cần cách xử lý khác nhau. Tăng quota hoặc gọi repair/replacement không giải quyết được mọi nguyên nhân. Cần chẩn đoán và fail-fast trước khi cấp thêm ngân sách.

## II. Thiết kế kiến trúc code

### 1. Pipeline là God Object, chứa quá nhiều trách nhiệm

**Vị trí:** `testgen/pipeline.py`, class `Pipeline`, đặc biệt `run()` (khoảng dòng 876 ở lần kiểm tra).

`run()` dài hơn 1.300 dòng, đồng thời điều phối generation/compile/certification/repair, quản lý mutant pool, coverage, quota, điều kiện dừng, context và ghi snapshot/report. Class còn quản lý execution cache, lock và thread pool. Các closure `certify_batch`, `certify_proposals`, `validate_batch` đọc/ghi state của hàm ngoài.

**Tác động:** thay đổi scheduling phải hiểu cả certification và persistence; khó test từng bước độc lập; thêm concurrency dễ làm sai state. Tách file nhưng giữ nguyên state chia sẻ ngầm chưa giải quyết vấn đề.

**Hướng sửa:** tách `ReferenceCertifier`, `MutantCertifier`, `CaseCertifier`, `StopPolicy` và `ArtifactStore`. `Pipeline` chỉ điều phối stage và cập nhật `RunState` thông qua kết quả có kiểu rõ ràng.

### 2. Logic nghiệp vụ phụ thuộc chuỗi hiển thị log — đã tái hiện lỗi

**Vị trí:** `testgen/ollama.py::_expected_ollama_shape`, `testgen/fallback.py::_neutral_result` và các label do generator tạo.

Loại tác vụ được nhận diện bằng substring của `label`. Label vừa là nội dung hiển thị vừa điều khiển schema validation, fallback và một số tùy chọn generation.

Probe local, không gọi LLM, cho kết quả:

| Label | Shape bắt buộc | Kết quả fallback khi các backend thất bại |
|---|---|---|
| `sinh baseline 1/10` | `cases: list` | Có `requested_count`, `rationale`, `cases` |
| `sinh 1 baseline 1/10` | Không có shape bắt buộc | `{}` |
| `sinh testcase vòng 1` | `cases: list` | Có `requested_count`, `rationale`, `cases` |
| `sinh 1 testcase vòng 1` | Không có shape bắt buộc | `{}` |

Generator dùng dạng có `1` giữa `sinh` và tên tác vụ. Thay đổi câu log đã làm mất kiểm tra shape dự kiến và đổi cấu trúc fallback. Các kiểm tra phía sau có thể vẫn loại response sai, nhưng lỗi bị phát hiện muộn hơn hoặc biến thành thiếu proposal.

**Hướng sửa:** dùng `TaskKind.BASELINE`, `TaskKind.MUTANT`, v.v. trong request. Schema và policy được chọn bằng loại tác vụ; `label` chỉ dùng để hiển thị.

### 3. Interface không mô tả đủ đầu vào và đầu ra thật

**Vị trí:** `testgen/domain.py::SolutionGenerator.generate`, `testgen/ollama.py::OllamaSolutionGenerator.generate`, `testgen/pipeline.py::run`.

Interface `generate(statement, output) -> list[Solution]` không thể hiện việc pipeline còn kỳ vọng generator tạo `generated/validator.py`. Ngược lại, generator tự tìm `output.parent / "test-model.json"` để lấy dữ liệu pipeline đã ghi.

Hai module giao tiếp bằng quy ước thư mục và side effect ẩn ngoài interface.

**Tác động:** implementation mới có thể đúng chữ ký hàm nhưng vẫn không chạy được. Đổi thư mục output có thể thay đổi hành vi, chẳng hạn khiến generator gọi lại analysis vì không tìm thấy test model.

**Hướng sửa:** truyền `GenerationRequest` chứa statement, test model, validator có sẵn và quota; trả `GenerationResult` chứa solutions, validator và diagnostics. `ArtifactStore` chịu trách nhiệm lưu file. Không tự dò dữ liệu nghiệp vụ trong thư mục cha.

### 4. Nghiệp vụ generation bị trộn với adapter backend

**Vị trí:** `testgen/ollama.py`, imports trong `testgen/chatgpt.py`, `testgen/claude.py`, phần dựng dependency trong `main.py`.

`ollama.py` chứa HTTP client, JSON repair, prompt, sinh AC/mutant/witness/testcase, audit và xử lý artifact. Claude/ChatGPT cũng được dùng thông qua `OllamaSolutionGenerator` và `OllamaCaseGenerator`. ChatGPT import helper private từ `.ollama`; Claude cũng import helper JSON từ đó.

**Tác động:** module mang tên backend nhưng chứa phần lõi dùng chung; thay parser hoặc adapter có thể ảnh hưởng backend khác; khó thay prompt/policy độc lập.

**Hướng sửa:** tách `LLMClient` protocol, các transport adapter, JSON codec/schema dùng chung và dịch vụ generation độc lập backend. Đổi tên generator theo trách nhiệm thay vì nhà cung cấp.

### 5. Dict được dùng thay domain model ở quá nhiều boundary

**Vị trí:** các interface trong `testgen/domain.py`, feedback/certification/audit/context trong `testgen/pipeline.py` và `testgen/ollama.py`.

Nhiều dữ liệu nghiệp vụ đi qua `dict` với key và quy tắc ngầm. Certification có đồng thời `verified`, `fallback_verified`, `verification_tier`, `reason`; kiểu dữ liệu hiện tại không ngăn tổ hợp mâu thuẫn. Nhiều `.get()` với default che dữ liệu thiếu thành kết quả rỗng.

**Tác động:** lỗi contract chỉ lộ khi chạy, đôi khi sau inference đắt tiền; refactor đổi key khó kiểm soát; downstream có thể mở thêm repair vì hiểu response hỏng là thiếu kết quả.

**Hướng sửa:** dùng model có kiểu cho `CertificationResult`, `GenerationPlan`, `CandidateContext`, `AuditResult`. Dùng enum cho trạng thái. Validate payload không tin cậy ở boundary; core xử lý domain object đã chuẩn hóa.

### 6. Không hỗ trợ, backend lỗi và kết quả rỗng chưa được phân biệt rõ

**Vị trí:** default method của `SolutionGenerator`/`CaseGenerator` trong `testgen/domain.py`; neutral result trong `testgen/fallback.py`.

Một số method mặc định trả `[]`, `{}` hoặc `None` khi không hỗ trợ. Khi tất cả backend lỗi, fallback cũng có thể trả dữ liệu rỗng. Caller khó phân biệt tác vụ thành công nhưng không tìm ra kết quả với implementation không hỗ trợ hoặc backend không khả dụng.

**Tác động:** pipeline có thể tiếp tục top-up/replacement dù sinh thêm không giải quyết nguyên nhân; báo cáo thiếu thông tin để xác định thất bại ở đâu.

**Hướng sửa:** trả outcome có trạng thái như `SUCCESS`, `UNSUPPORTED`, `UNAVAILABLE`, `BUDGET_EXHAUSTED`, kèm diagnostics. Application policy quyết định tiếp tục hay dừng; adapter không tự biến lỗi hạ tầng thành dữ liệu nghiệp vụ thành công.

### 7. Vòng đời state và compiled artifact chưa được biểu diễn rõ

**Vị trí:** state của `Pipeline`; `DockerJudge._compiled`, `compile()` và `execute()`; interface `Judge` trong `testgen/domain.py`.

Cache/log/lock nằm trên instance pipeline, nhưng phần lớn state của một run nằm trong biến local và closure. `compile()` trả `Result(PASS)` trong khi artifact thực tế nằm ngầm trong `_compiled`. `execute()` đòi hỏi compile đã được gọi trên đúng instance trước đó.

**Tác động:** khó resume, tái sử dụng instance an toàn và phân phối execution sang worker khác. Một verdict compile không đủ thông tin để khôi phục execution sau khi process kết thúc.

**Hướng sửa:** tạo `RunState` riêng cho mỗi run. Compile trả `CompiledArtifact` hoặc artifact handle có identity rõ ràng; execute nhận artifact đó. Cache, checkpoint và log có lifecycle xác định. Cache identity cần bao gồm source/runtime/limits phù hợp, đồng thời hỗ trợ bypass cho trial kiểm tra ổn định.

### 8. Retry, quota và scheduling thiếu một chủ sở hữu chung

**Vị trí:** retry JSON trong client, fallback client, vòng generation trong generator, replacement/repair/top-up trong pipeline, retry judge trong decorator.

Các tầng có giới hạn riêng nhưng chưa chia sẻ ngân sách tổng. Interface trả cả danh sách sau một loạt công việc, khiến orchestration không nhìn thấy đủ trạng thái để dừng sớm hay cấp việc theo kết quả đã chứng nhận.

**Tác động:** thay timeout một tầng khó dự đoán tổng thời gian; hủy công việc, early-stop và backpressure khó triển khai nhất quán. Đây là điểm nối trực tiếp giữa thiết kế code và hiệu năng pipeline.

**Hướng sửa:** application scheduler sở hữu deadline, ngân sách và concurrency. Client xử lý một attempt hoặc retry cục bộ trong ngân sách được cấp; generator mô tả tác vụ; certifier trả kết quả. Không cần dịch vụ phân tán để làm việc này.

### Cấu trúc module đề xuất

Đây là hướng tổ chức, không phải yêu cầu tạo ngay tất cả file hoặc class:

```text
testgen/
  domain/
    models.py          # Solution, Case, CompiledArtifact, CertificationResult
    requests.py        # TaskKind, GenerationRequest, GenerationResult
    ports.py           # LLMClient, Judge, ArtifactStore
  application/
    pipeline.py        # Điều phối stage
    state.py           # RunState, checkpoint schema
    scheduler.py       # Deadline, budget, concurrency, cancellation
    certification.py   # Reference, mutant, testcase certification
    policies.py        # Quota, stop criteria, retry decisions
  generation/
    solutions.py       # Nghiệp vụ sinh AC/mutant
    cases.py           # Baseline, adaptive, repair, audit
    prompts.py
    schemas.py
  adapters/
    llm/               # Ollama, OpenAI-compatible, Claude CLI, Codex CLI
    judge/             # Docker, remote, native
    storage/           # Filesystem artifacts và checkpoints
  observability/
    progress.py
    latency.py
```

Dependency nên đi từ application/generation tới domain và interface; adapter implement interface. Module dùng chung không import helper private từ một backend cụ thể. `main.py` giữ vai trò dựng config và nối dependency.

### Thứ tự refactor kiến trúc code

1. Sửa dispatch bằng `label`, thêm probe/test đảm bảo đổi wording log không đổi hành vi.
2. Làm rõ request/result và lỗi typed tại boundary; giữ adapter tương thích trong giai đoạn chuyển tiếp.
3. Đưa state vào `RunState`, persistence vào `ArtifactStore`, compiled artifact thành giá trị/handle rõ ràng.
4. Tách các certifier và policy khỏi `Pipeline.run()` bằng từng thay đổi nhỏ, giữ nguyên quy tắc chứng nhận.
5. Gom ngân sách/scheduling, rồi chuyển từ xử lý cả loạt sang xử lý kết quả liên tục.
6. Di chuyển code độc lập backend ra khỏi `ollama.py`; đồng bộ CLI, config và tài liệu.

Không cần microservices. Mục tiêu là một ứng dụng Python có module và contract rõ ràng, kiểm thử từng thành phần được, rồi mới tối ưu thực thi.

## Giới hạn và trạng thái của review

- Chưa sửa mã thực thi hoặc triển khai kiến trúc đề xuất.
- Có phân tích tĩnh, đọc log có sẵn và probe bằng fake client/helper local; không chạy benchmark LLM/Docker mới hay full test suite.
- Lỗi quota và dispatch bằng label đã được tái hiện bằng probe. Các rủi ro như output làm cạn RAM chưa được kết luận là đã xảy ra trong các run thống kê.
- Workspace có thay đổi trong thời gian review; cần kiểm tra lại vị trí dòng và hành vi trước khi áp dụng patch.
