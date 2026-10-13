# Architecture

## Mục tiêu và ranh giới

Input chính là đề bài của một problem. Pipeline tạo ứng viên code đúng/sai, testcase và expected output, chạy judge Linux cục bộ, rồi tùy chọn lấy pool CodeNet AC/WA từ `ktoxz` để kiểm tra độ tổng quát. `output/` chứa toàn bộ artifact của từng run, `data/` chứa đề/checker/snapshot oracle, `docker/` chứa cấu hình runtime. Không sửa kho CodeNet gốc.

## Thành phần và design pattern

| Thành phần | Vai trò |
| --- | --- |
| `domain.py` | `Solution`, `Case`, `Result` bất biến; abstract interfaces `SolutionGenerator`, `CaseGenerator`, `Judge`, `OracleSource` (Strategy/Dependency Inversion). |
| `ollama.py` | Hai strategy sinh code/test thông qua Ollama `gemma4:31b-cloud`; prompt, response và source được lưu để audit. |
| `docker_judge.py` + `runtime.py` | Adapter `Judge` và runtime catalog từ `config/runtimes.json`; không có bảng lệnh compile theo ngôn ngữ trong judge. |
| `checker.py` + `checkers/` | Abstract `Checker`, registry/factory và các plugin riêng cho EXACT, TOKEN, CASE_INSENSITIVE_TOKEN, DECIMAL_EXACT, FLOAT. Plugin mới tự được phát hiện; FLOAT bật kiểm tra precision/dòng theo đề và coi signed zero tương đương về số học. |
| `codenet.py` + `scripts/export_codenet.py` | Adapter `OracleSource`: trích đúng problem và số lượng AC/WA từ parquet VPS, tải tar nhỏ, kiểm SHA-256, dọn venv/temp remote. |
| `pipeline.py` | Orchestrator/template method: sinh → validate → reference consensus → chấm → feedback tối đa 3 vòng → oracle metrics. |
| `main.py` | Composition root và CLI; phụ thuộc concrete classes chỉ ở đây. |

## Luồng dữ liệu

```text
statement.md + checker.json
    → Ollama: AC/WA candidates + validator.py
    → Docker compile
    → official samples + Ollama cases (≤3 iterations)
    → validator (Docker) → ≥2 reference outputs agree → certified cases
    → Docker judge candidate pool → feedback → iteration reports
    → [--oracle] SSH export CodeNet AC/WA → Docker judge same cases
    → report.json (label-based TPR/TNR + gap + per-source verdict)
```

## Trust và failure isolation

- Đề và response LLM là dữ liệu không tin cậy. Không chạy source/validator LLM trên host; tất cả chạy trong Docker không mạng, filesystem root chỉ đọc, cap-drop, no-new-privileges, giới hạn CPU/RAM/PID/timeout. Docker socket không mount vào container.
- Hai reference đồng ý chỉ là **đồng thuận**, không phải chứng minh nghiệm đúng. Các mẫu official được đối chiếu. Test bất đồng bị quarantine; metric cuối vẫn phải rà bằng oracle độc lập/human.
- Validator do LLM sinh cũng chỉ là ứng viên. Với bài đã có validator kiểm toán tại `data/problems/<id>/validator.py`, pipeline ưu tiên script đó; vẫn lưu bản LLM để đối chiếu. p00004 cho hệ số thập phân và bắt determinant khác 0, p00005 kiểm giới hạn LCM/dataset.
- `CE`, `INFRA` không bị gộp vào WA; lỗi Docker/host không được xem là testcase bắt bug.
- Nhãn CodeNet Accepted/Wrong Answer là verdict lịch sử, có thể không trùng với checker, toolchain và tập input hiện tại. Báo cả `tpr_label_based`/`tnr_label_based` lẫn từng `verdict`/`actual`/`stderr` để người dùng lọc.
- `--oracle` dùng export ở `/tmp/testgen-export.*` trên VPS, giới hạn 100 mỗi nhãn và kiểm hash khi tải. Dữ liệu nằm trong `output/.../oracle`; script xóa temp remote. Kho staging parquet không bị sửa.

## Mở rộng

Thay provider LLM bằng class khác thực thi `SolutionGenerator`/`CaseGenerator`; thay nguồn CodeNet bằng class `OracleSource`; thay judge bằng class `Judge` khác. Profile checker theo bài ở `data/problems/<id>/checker.json`, không hard-code p00004 trong core. Khi cần validator chính xác hơn, thay validator LLM bằng script người viết nhưng vẫn thực thi trong sandbox. Thêm metric verified sau khi có quy trình xác nhận nhãn độc lập; đừng đổi tên metric provisional thành verified.

Checker là Strategy plugin: `checker_from_profile()` nạp module trong `testgen/checkers`, tìm class theo `kind` và khởi tạo từ option profile. Thêm/xóa checker không làm đổi orchestration. Ngôn ngữ/dialect là cấu hình khai báo (`config/runtimes.json`), dùng chung cho tên source, prompt LLM, Docker image/compile/run và exporter CodeNet. `config/sandbox.json` tách giới hạn tài nguyên khỏi implementation; các rào bảo mật `--network none`, root FS read-only và cap-drop vẫn cố định để người dùng không vô tình tắt.

Các giá trị còn cố định có chủ đích: `Accepted`/`Wrong Answer` là tên verdict gốc trong CodeNet, giới hạn tối đa 3 vòng là giao thức thí nghiệm, parser sample đọc heading Markdown đã quy ước, và `scripts/smoke_judge.py` là fixture cụ thể của p00005. Chúng không phải bảng dispatch checker/runtime. Nếu thay nguồn verdict hoặc format đề, thêm adapter ở boundary tương ứng thay vì sửa core judge.
## Judge backend

`Judge` trong `testgen/domain.py` là interface của pipeline. `DockerJudge` chấm local; `RemoteDockerJudge` kế thừa cùng logic compile/execute nhưng chuyển lệnh Docker sang `scripts/remote_judge_worker.py` trên KHOI qua JSON-over-SSH. `main.py` chọn backend bằng `--judge auto|local|remote` trước khi gọi Ollama. CodeNet oracle vẫn lấy từ host cấu hình riêng trong `config/oracle.json`.

Worker lưu source/build tạm theo run ID trên KHOI và chạy Docker với cùng giới hạn network, bộ nhớ, CPU, process và read-only root như local. Kết quả/metrics vẫn được tạo trên local. Lỗi SSH/Docker trả `INFRA`; `CE` chỉ dành cho lỗi compile source. Không tự động fallback giữa chừng khi một run đã bắt đầu, để không trộn artifact của hai judge.

`RetryingJudge` là Decorator bao quanh local/remote `Judge`: chỉ `INFRA` được retry theo `config/judge.json`; các verdict của code giữ nguyên. Khi hết lượt, nó ném `InfrastructureError` để pipeline dừng trước khi tính metric trên tập kết quả thiếu. Preflight kết nối KHOI cũng dùng cùng chính sách retry.

Để giảm độ trễ, `Judge.execute_many()` là phương thức mặc định lặp tuần tự; `RemoteDockerJudge` ghi đè và gửi một batch qua một phiên SSH. Worker vẫn tạo một container cho mỗi input, nên không thay đổi ranh giới timeout/sandbox. `Pipeline` cache kết quả thô theo solution/case/input trong cùng run và chỉ gửi các cặp chưa chấm. `resume_oracle()` đọc snapshot vòng cuối và testcase đã chứng nhận để tiếp tục phần CodeNet sau lỗi hạ tầng, không sinh lại code/test; pool oracle đã tải được tái dùng.
