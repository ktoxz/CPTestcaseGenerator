# KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT
## 1. GỘP TẠO SINH CHECKER & SANDBOX VÀO TEST MODEL (ZERO-OVERHEAD)
## 2. TRIỆT TIÊU DỨT ĐIỂM LỖI KÝ TỰ `\r` (WINDOWS CRLF)
## 3. NÂNG CẤP RUNTIME CONTAINER (NUMPY, BOOST & C++20)

**Hệ thống:** Final Testcase Generator  
**Thời điểm lập kế hoạch:** Ngày 14 tháng 10 năm 2026  
**Mục tiêu:** Khắc phục triệt để các sai lệch verdict do môi trường thực thi, đồng thời đưa hệ thống tiến tới trạng thái tự động hóa 100% (chỉ cần nhận file `statement.md`, không phụ thuộc vào `checker.json` hay `sandbox.json` cấu hình thủ công).

---

## MỤC LỤC
1. [Bối cảnh và Nguyên nhân gốc rễ](#1-boi-canh-va-nguyen-nhan-goc-re)
2. [Phần 1: Gộp tạo sinh Checker & Sandbox vào Test Model](#2-phan-1-checker-va-sandbox-trong-test-model)
3. [Phần 2: Triệt tiêu lỗi Windows CRLF (`\r\n`)](#3-phan-2-triet-tieu-loi-crlf)
4. [Phần 3: Nâng cấp Runtime Container (Numpy, Boost, C++20)](#4-phan-3-nang-cap-runtime-container)
5. [Lộ trình triển khai tuần tự](#5-lo-trinh-trien-khai)
6. [Tiêu chuẩn nghiệm thu định lượng](#6-tieu-chuan-nghiem-thu)

---

<a name="1-boi-canh-va-nguyen-nhan-goc-re"></a>
## 1. BỐI CẢNH VÀ NGUYÊN NHÂN GỐC RỄ

Qua 4 thực nghiệm quy mô lớn đã hoàn tất, hệ thống đã đạt độ ổn định cao (Reproducibility $\text{SD} = 0.0\%$ trên TPR), tuy nhiên vẫn tồn tại các điểm nghẽn kỹ thuật bắt nguồn từ môi trường và cơ chế cấu hình tĩnh:

1. **Thiếu cơ chế tự động đọc đề để sinh Checker & Sandbox**:
   - Hiện tại hệ thống dựa vào file tĩnh `checker.json` và `sandbox.json`. Nếu không có, hệ thống gán cứng mặc định `TOKEN` checker và trần cố định `5s / 512MB RAM / JVM 192MB`.
   - Hệ quả: Bài `cf1003c` dính số thực bị sụt giảm TPR xuống 30% do thiếu Float Checker; bài `p02586` dính OOM và TLE vì trần tài nguyên áp đặt thấp hơn đề bài quy định (3000ms, 1024MB).
2. **Lỗi ký tự `\r` (CRLF) do cơ chế Pipe trên Windows**:
   - Khi chạy trên Windows, lệnh `subprocess.run(..., text=True)` trong `testgen/docker_judge.py` tự động chuyển đổi `\n` thành `\r\n`.
   - Vào bên trong container Linux, hàm `input()` của Python chỉ cắt `\n`, giữ lại ký tự `\r`. Trong bài `cf1008a`, điều này khiến các bài nộp sai của học sinh vô tình in `NO` khớp với expected output, giúp 5 bài nộp sai thoát chết (TNR bị kéo lùi về 75%).
3. **Môi trường thực thi thiếu các thư viện thi đấu phổ biến**:
   - Image Docker `testgen-judge:local` thiếu thư viện `numpy` (khiến bài nộp Python trong `p02586` bị `ModuleNotFoundError`), thiếu thư viện `libboost-all-dev` và cờ `-std=gnu++20` (khiến các bài nộp C++ hiện đại bị dính lỗi biên dịch CE).

---

<a name="2-phan-1-checker-va-sandbox-trong-test-model"></a>
## 2. PHẦN 1: GỘP TẠO SINH CHECKER & SANDBOX VÀO TEST MODEL (ZERO-OVERHEAD)

### 2.1 Ý tưởng cốt lõi
Gộp việc trích xuất **Checker Specification** và **Sandbox Specification** trực tiếp vào bước **`BUILD_TEST_MODEL`**.  
LLM đọc đề bài `statement.md` một lần duy nhất để sinh toàn bộ:
- Cấu trúc input, grammar, constraints, fault model, coverage obligations.
- Đặc tả so khớp Checker (`kind`, `epsilon`, `case_sensitive`, `multiple_valid_answers`).
- Đặc tả trần tài nguyên Sandbox (`time_limit_seconds`, `memory_limit_mb`).

👉 **Lợi ích**: Không tốn thêm bất kỳ lượt gọi LLM nào, không tăng thêm độ trễ (zero latency overhead).

### 2.2 Các bước thực hiện chi tiết

- [ ] **Bước 1.1: Mở rộng Schema Pydantic trong `testgen/coverage.py`**
  - Định nghĩa 2 schema con trong `testgen/coverage.py`:
    ```python
    class CheckerSpecModel(BaseModel):
        model_config = ConfigDict(extra="ignore")
        kind: Literal["TOKEN", "FLOAT", "EXACT", "PYTHON_SCRIPT"] = "TOKEN"
        epsilon: float | None = None          # VD: 1e-6 nếu đề yêu cầu sai số số thực
        case_sensitive: bool = True           # False nếu đề cho phép in hoa/thường tự do
        multiple_valid_answers: bool = False  # True nếu đề có nhiều đáp án hợp lệ (constructive)
        reasoning: str = ""

    class SandboxSpecModel(BaseModel):
        model_config = ConfigDict(extra="ignore")
        time_limit_seconds: float = 5.0       # Trích xuất từ "time limit per test"
        memory_limit_mb: int = 512            # Trích xuất từ "memory limit per test"
        reasoning: str = ""
    ```
  - Bổ sung 2 trường này vào `TestModelResponse`:
    ```python
    checker: CheckerSpecModel = Field(default_factory=CheckerSpecModel)
    sandbox: SandboxSpecModel = Field(default_factory=SandboxSpecModel)
    ```

- [ ] **Bước 1.2: Cập nhật Prompt `BUILD_TEST_MODEL` trong `testgen/generation/test_model.py`**
  - Bổ sung yêu cầu trích xuất môi trường vào prompt gửi tới LLM:
    ```text
    Also extract execution specifications:
    - checker:
      * kind: "FLOAT" if problem asks for real number output with error tolerance, "TOKEN" if whitespace-separated tokens, "EXACT" if strict line/character formatting, or "PYTHON_SCRIPT" if multiple valid outputs are accepted.
      * epsilon: float number if FLOAT (e.g. 1e-6), otherwise null.
      * case_sensitive: false if statement explicitly allows printing in any case (upper/lower), otherwise true.
      * multiple_valid_answers: true if constructive problem where any valid output is accepted.
    - sandbox:
      * time_limit_seconds: parsed from "time limit per test" (in seconds, default 5.0).
      * memory_limit_mb: parsed from "memory limit per test" (in megabytes, default 512).
    ```

- [ ] **Bước 1.3: Cập nhật Fallback an toàn trong `testgen/fallback.py`**
  - Đảm bảo trong hàm `neutral_result(TaskType.BUILD_TEST_MODEL)`, nếu LLM gặp sự cố timeout thì luôn có giá trị mặc định:
    ```python
    "checker": {"kind": "TOKEN", "epsilon": None, "case_sensitive": True},
    "sandbox": {"time_limit_seconds": 5.0, "memory_limit_mb": 512}
    ```

- [ ] **Bước 1.4: Đấu nối vào Pipeline Execution (`cli.py` & `run_pipeline.py`)**
  - **Khởi tạo Checker**: Nếu thư mục bài toán không có file `checker.json`, hệ thống tự động khởi tạo `checker` từ `test_model["checker"]`.
  - **Khởi tạo Sandbox**: Truyền `test_model["sandbox"]` vào `DockerJudge`, tự động thiết lập timeout chạy $= \text{time\_limit} \times 1.5$ (hệ số an toàn) và cgroup memory $= \text{memory\_limit\_mb}$.

---

<a name="3-phan-2-triet-tieu-loi-crlf"></a>
## 3. PHẦN 2: TRIỆT TIÊU DỨT ĐIỂM LỖI KÝ TỰ `\r` (WINDOWS CRLF)

### 3.1 Mục tiêu
Loại bỏ hoàn toàn hiện tượng Windows tự ý chèn `\r\n` qua pipe, đảm bảo dữ liệu đưa vào container Linux luôn là chuỗi thuần POSIX LF (`\n`).

### 3.2 Các bước thực hiện chi tiết

- [ ] **Bước 2.1: Chuyển toàn bộ luồng truyền stdin của `subprocess` sang nhị phân (Binary Bytes)**
  - **File chỉnh sửa**: `testgen/docker_judge.py` (hàm `_run`).
  - **Thay đổi**:
    - Thay vì truyền text mode: `input=input_text, text=True`.
    - Chuyển sang truyền nhị phân thuần túy: `input=input_text.encode("utf-8")`.
    - Bỏ cờ `text=True`, `encoding="utf-8"`, `errors="replace"` trong `subprocess.run()`.
    - Decode kết quả đầu ra nhị phân:
      ```python
      stdout_text = proc.stdout.decode("utf-8", errors="replace")
      stderr_text = proc.stderr.decode("utf-8", errors="replace")
      ```
  - **Hiệu quả**: Windows runtime sẽ không can thiệp thay thế `\n` thành `\r\n` khi dữ liệu được truyền dưới dạng `bytes`.

- [ ] **Bước 2.2: Rà soát việc ghi file testcase `.in` và `.out` trên đĩa**
  - Đảm bảo các hàm ghi file trong `testgen/infrastructure/file_run_store.py` và `testgen/pipeline.py` luôn chỉ định `newline="\n"` để file lưu trên đĩa Windows không chứa ký tự byte `0x0D` (`\r`).

- [ ] **Bước 2.3: Xác nhận bằng lệnh `cat -A` bên trong container Linux**
  - Khởi chạy container kiểm tra trực quan dữ liệu truyền qua pipe:
    ```bash
    python -c "import subprocess; p = subprocess.run(['docker', 'run', '--rm', '-i', 'testgen-judge:local', 'cat', '-A'], input=b'k\n', capture_output=True); print(p.stdout)"
    ```
  - **Tiêu chuẩn đạt**: Output phải là `b'k$\n'` (ký hiệu `$` là kết thúc dòng LF), tuyệt đối không xuất hiện ký hiệu `^M$` (CRLF).

- [ ] **Bước 2.4: Viết Test Harness thử nghiệm đa ngôn ngữ (C++, Python 3, Java)**
  - Viết chương trình đọc xâu 1 ký tự (`k`) và in độ dài `len(s)` bằng cả 3 ngôn ngữ:
    - C++: `string s; cin >> s; cout << s.length();`
    - Python 3: `s = input(); print(len(s))`
    - Java: `Scanner sc = new Scanner(System.in); String s = sc.nextLine(); System.out.println(s.length());`
  - Chạy thử nghiệm trên 2 trường hợp:
    1. Input có dòng trống cuối: `"k\n"`
    2. Input không có dòng trống cuối: `"k"`
  - **Tiêu chuẩn đạt**: Cả 3 ngôn ngữ đều phải in ra kết quả là `1`, không bị độ dài `2` do dính `\r`.

- [ ] **Bước 2.5: Chạy lại bài `cf1008a` và nghiệm thu TNR**
  - Chạy lại kiểm định oracle trên bài `cf1008a`.
  - **Tiêu chuẩn đạt**: Toàn bộ 5 bài nộp sai trước đây (`135235851`, `135642311`, `136178688`, `136421896`, `201683702`) **bị tiêu diệt 100%**, đưa TNR từ $75.0\%$ lên **$100.0\%$**.

---

<a name="4-phan-3-nang-cap-runtime-container"></a>
## 4. PHẦN 3: NÂNG CẤP RUNTIME CONTAINER (NUMPY, BOOST & C++20)

### 4.1 Mục tiêu
Đồng bộ môi trường sandbox nội bộ với tiêu chuẩn của các nền tảng lập trình thi đấu (AtCoder, Codeforces), khắc phục triệt để các ca lỗi biên dịch và lỗi thiếu thư viện môi trường.

### 4.2 Các bước thực hiện chi tiết

- [ ] **Bước 3.1: Đối chiếu phiên bản compiler và cờ tối ưu**
  - *Phiên bản hiện hữu trong `testgen-judge:local`:*
    - GCC / G++: `12.2.0` (Debian 12 Bookworm).
    - OpenJDK: `17.0.20.1`.
    - Python 3: `3.11.2`.
    - Python 2: `2.7.18` (trong container riêng `testgen-python2:local`).
  - *Cập nhật cờ biên dịch trong `config/runtimes.json`:*
    - Nâng cấp cấu hình C++ lên `-std=gnu++20 -O2` để hỗ trợ các bài nộp Codeforces hiện đại sử dụng thư viện `<ranges>`, `std::span` hoặc `std::bit_cast`.

- [ ] **Bước 3.2: Cập nhật `docker/Dockerfile` và Rebuild Image**
  - Sửa đổi file `docker/Dockerfile`:
    ```dockerfile
    FROM debian:bookworm-slim
    RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ openjdk-17-jdk-headless python3 python3-numpy \
        libboost-all-dev ca-certificates \
        && rm -rf /var/lib/apt/lists/*
    WORKDIR /work
    ```
  - Chạy build lại image cục bộ:
    ```bash
    docker build -t testgen-judge:local -f docker/Dockerfile docker/
    ```

- [ ] **Bước 3.3: Thống kê và Phân loại toàn bộ lỗi Compilation Error (CE) trên Oracle**
  - Quét toàn bộ kho `report.json` và log: lập bảng thống kê số lượng CE theo ngôn ngữ và phân loại nguyên nhân:
    1. CE do thiếu thư viện ngoài (`numpy`, `boost`).
    2. CE do khác biệt chuẩn ngôn ngữ (`gnu++17` vs `gnu++20`).
    3. CE là lỗi thực sự từ người thi (thí sinh nộp code không biên dịch được).
  - Đọc và trích dẫn ít nhất 10 thông báo lỗi tiêu biểu làm minh chứng cho báo cáo khóa luận.

- [ ] **Bước 3.4: Xác nhận môi trường Python 2 độc lập**
  - Chạy thử nghiệm một mẫu mã nguồn Python 2 lịch sử (sử dụng cú pháp `print "hello"`, phép chia nguyên `1/2 == 0`) trong image `testgen-python2:local`.
  - Xác nhận phân vùng cô lập mạng (`--network none`) và mount volume hoạt động mượt mà.

- [ ] **Bước 3.5: Chạy lại bài `p02586` và nghiệm thu phục hồi TPR**
  - Re-judge bài `p02586` trên môi trường đã có `numpy` và cgroup bộ nhớ nâng cấp theo đề bài ($1024$ MB).
  - **Tiêu chuẩn đạt**: Các code Python nộp trên AtCoder dùng `numpy` (`s267255158`, `s528208375`) không còn bị văng `ModuleNotFoundError`, phục hồi chỉ số TPR.

---

<a name="5-lo-trinh-trien-khai"></a>
## 5. LỘ TRÌNH TRIỂN KHAI TUẦN TỰ

Kế hoạch được triển khai theo 3 giai đoạn rõ ràng:

```
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1: TRIỆT TIÊU LỖI CRLF & FIX PIPE BYTES                      │
│ - Sửa docker_judge.py sang encode/decode bytes nhị phân.               │
│ - Chạy test harness cat -A và đa ngôn ngữ (C++, Python, Java).         │
│ - Re-judge cf1008a -> Xác nhận TNR đạt 100%.                           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2: NÂNG CẤP DOCKER RUNTIME (NUMPY, BOOST, C++20)             │
│ - Bổ sung python3-numpy & libboost-all-dev vào Dockerfile.             │
│ - Rebuild testgen-judge:local.                                         │
│ - Bổ sung -std=gnu++20 vào runtimes.json.                              │
│ - Re-judge p02586 -> Xác nhận các code Python dùng numpy chạy thành công│
│ - Thống kê và trích xuất 10 log CE tiêu biểu.                          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 3: GỘP CHECKER & SANDBOX VÀO TEST MODEL PROMPT               │
│ - Mở rộng TestModelResponse schema (checker_spec, sandbox_spec).       │
│ - Cập nhật prompt BUILD_TEST_MODEL trong test_model.py.                │
│ - Đấu nối tự động áp dụng spec vào cli.py và run_pipeline.py.          │
│ - Thử nghiệm zero-config trên bài toán mới (không tạo checker.json).   │
└────────────────────────────────────────────────────────────────────────┘
```

---

<a name="6-tieu-chuan-nghiem-thu"></a>
## 6. TIÊU CHUẨN NGHIỆM THU ĐỊNH LƯỢNG (ACCEPTANCE CRITERIA)

| Hạng mục | Tiêu chí thành công cụ thể | Lệnh kiểm chứng |
| :--- | :--- | :--- |
| **Kiểm tra Pipe LF** | Container chạy `cat -A` chỉ thấy ký tự `$`, không có bất kỳ ký tự `^M`. | `python -c "import subprocess; p = subprocess.run(['docker', 'run', '--rm', '-i', 'testgen-judge:local', 'cat', '-A'], input=b'test\n', capture_output=True); assert b'\r' not in p.stdout"` |
| **Kiểm tra `cf1008a`** | Toàn bộ 5 code WA thoát chết trước đây bị tiêu diệt; **TNR đạt $100.0\%$**. | Kiểm tra `report.json` của `cf1008a`: `tnr_label_based == 1.0` |
| **Kiểm tra `numpy`** | Python 3 trong container import numpy thành công. | `docker run --rm testgen-judge:local python3 -c "import numpy; print(numpy.__version__)"` |
| **Kiểm tra `boost`** | C++ compile được chương trình `#include <boost/rational.hpp>`. | Biên dịch thử mã nguồn Boost trong container. |
| **Kiểm tra `p02586`** | Code học sinh dùng `import numpy as np` không còn văng `ModuleNotFoundError`. | Kiểm tra verdict của `s267255158` chuyển từ `RE` sang `PASS`. |
| **Tự động trích xuất Spec** | `test-model.json` tự động chứa `checker` và `sandbox` từ đề bài mà không cần file cấu hình ngoài. | Chạy pipeline thử nghiệm và kiểm tra file `test-model.json`. |

---
*Kế hoạch được lập tự động và sẵn sàng thực thi trên codebase `Final_TestcaseGenerator`.*
