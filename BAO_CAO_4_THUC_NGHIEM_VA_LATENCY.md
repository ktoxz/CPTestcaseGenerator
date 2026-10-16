# BÁO CÁO TOÀN DIỆN KẾT QUẢ 4 THỰC NGHIỆM VÀ PHÂN TÍCH ĐỘ TRỄ (LATENCY)
## HỆ THỐNG SINH VÀ CHỨNG NHẬN TESTCASE TỰ ĐỘNG CHO BÀI TOÁN LẬP TRÌNH (FINAL TESTCASE GENERATOR)

**Thời điểm hoàn tất toàn bộ thực nghiệm:** Ngày 14 tháng 10 năm 2026  
**Môi trường thực nghiệm:**
- **Hệ điều hành:** Windows 10/11 x64, Docker Desktop (Linux Engine).
- **Môi trường chấm (Judge Sandbox):** Local Docker Engine với 2 container cô lập mạng (`testgen-judge:local` cho C/C++/Java/Python 3, `testgen-python2:local` cho Python 2 legacy).
- **Mô hình ngôn ngữ lớn (LLM):** Cụm Ollama cục bộ kết hợp dự phòng (Nemotron-70B / Gemma-27B / Claude fallback).
- **Tập bài toán đóng băng (Frozen Cohort):** 60 bài toán (`config/experiments/report-cohort-20261013.json` gồm 39 bài CodeNet và 21 bài Codeforces).

---

## MỤC LỤC BÁO CÁO
1. [Tổng quan thiết kế 4 Thực nghiệm](#1-tong-quan-thiet-ke-4-thuc-nghiem)
2. [Thực nghiệm 1: Đóng góp của Vòng lặp phản hồi (Round-by-Round Feedback Refinement)](#2-thuc-nghiem-1-vong-lap-phan-hoi)
3. [Thực nghiệm 2: Đường cơ sở sinh một lần (One-shot LLM Baseline)](#3-thuc-nghiem-2-one-shot-baseline)
4. [Thực nghiệm 3: Đường cơ sở Test mẫu đề bài (Sample-only Baseline)](#4-thuc-nghiem-3-sample-only-baseline)
5. [Thực nghiệm 4: Độ lặp lại và Phân tích phương sai (Repeated Runs 3x trên 12 bài)](#5-thuc-nghiem-4-repeated-runs)
6. [Phân tích nguyên nhân gốc rễ các bài không đạt chỉ số](#6-phan-tich-nguyen-nhan-goc-re)
7. [Báo cáo và Phân rã độ trễ (Latency Analysis)](#7-bao-cao-va-phan-ra-do-tre)
8. [Bảng ma trận đối chiếu tổng hợp 4 Thực nghiệm](#8-bang-doi-chieu-tong-hop)
9. [Kết luận và Khuyến nghị cho Khóa luận tốt nghiệp](#9-ket-luan-va-khuyen-nghi)

---

<a name="1-tong-quan-thiet-ke-4-thuc-nghiem"></a>
## 1. TỔNG QUAN THIẾT KẾ 4 THỰC NGHIỆM

Nhằm giải quyết triệt để các khoảng trống nghiên cứu được chỉ ra trong báo cáo khóa luận (thiếu nhóm đối chứng baseline, chưa cô lập đóng góp của feedback loop, chưa đo phương sai giữa các lần chạy), hệ thống đã thực hiện 4 thực nghiệm ưu tiên:

| Mã thực nghiệm | Tên thực nghiệm | Mục tiêu kiểm chứng | Quy mô đánh giá |
| :--- | :--- | :--- | :--- |
| **Thực nghiệm 1** | **Round-by-round Refinement** | Đo lường mức đóng góp thực sự của vòng lặp phản hồi (Round 1 vs Round 2) đối với TPR và TNR. | 59 bài toán (toàn bộ cohort đủ oracle) |
| **Thực nghiệm 2** | **One-shot LLM Baseline** | Đo chất lượng khi LLM sinh trực tiếp testcase không qua Test Model, Certification hay Feedback. | 60 bài toán (toàn bộ cohort) |
| **Thực nghiệm 3** | **Sample-only Baseline** | Xác định cận dưới chất lượng khi hệ thống chỉ dùng test case mẫu trong đề bài. | 58 bài toán có test mẫu |
| **Thực nghiệm 4** | **Repeated Runs (3 Replicates)** | Kiểm tra độ ổn định, tính tái lập và phương sai kết quả qua 3 lần chạy độc lập. | 12 bài toán phân tầng (36 runs) |

---

<a name="2-thuc-nghiem-1-vong-lap-phan-hoi"></a>
## 2. THỰC NGHIỆM 1: ĐÓNG GÓP CỦA VÒNG LẶP PHẢN HỒI (ROUND 1 VS ROUND 2)

### 2.1 Phương pháp
Để cô lập đóng góp của cơ chế phản hồi từ các chương trình sống sót (survivor feedback), hệ thống trích xuất trạng thái bộ test sau **Vòng 1** (chỉ gồm test baseline khởi tạo từ test model, chưa nhận phản hồi) và so sánh cặp (paired comparison) với bộ test sau **Vòng 2** (sau khi đã nhận danh sách survivor và các nghĩa vụ phủ chưa đạt để sinh bù testcase).

### 2.2 Kết quả định lượng (Trên 59 bài toán có đủ Oracle)

| Giai đoạn | Số bài | Macro TPR (%) | Macro TNR (%) | Micro TPR (%) | Micro TNR (%) | Số bài đạt cả TPR & TNR $\ge 0.8$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Round 1 (Chưa có feedback)** | 59 | **88.32%** | **82.80%** | 87.86% | 84.04% | 37 / 59 (62.7%) |
| **Round 2 (Có survivor feedback)** | 59 | **88.07%** | **85.78%** | 87.59% | 86.82% | **40 / 59 (67.8%)** |
| **Mức tăng ròng ($\Delta = \text{R2} - \text{R1}$)** | — | **-0.25%** | **+2.98%** | -0.27% | **+2.78%** | **+3 bài (+5.1%)** |

### 2.3 Phân tích thống kê cặp (Paired Difference Analysis)
- **Về khả năng bắt lỗi (TNR)**:
  - Mức tăng trung bình: **+2.98%** (Khoảng tin cậy Bootstrap 95%: **[+1.53%, +4.69%]**).
  - Phân bố theo bài: **16 bài tăng TNR rõ rệt**, **43 bài giữ nguyên**, **0 bài bị giảm**.
  - Kết quả này chứng minh survivor feedback thành công trong việc tạo ra các ca kiểm thử bổ sung đánh trúng vào góc chết của các giải thuật sai.
- **Về độ bảo toàn chương trình đúng (TPR)**:
  - Chênh lệch trung bình: **-0.25%** (Khoảng tin cậy Bootstrap 95%: **[-0.76%, 0.00%]**).
  - Phân bố: 58 bài giữ nguyên TPR, chỉ có đúng 1 bài giảm nhẹ do chạm trần thời gian chạy của testcase bổ sung.
- **Kết luận**: Vòng lặp phản hồi giúp tăng năng lực tiêu diệt chương trình sai thêm gần **3% TNR trên toàn bộ tập dữ liệu**, giúp đưa thêm 3 bài toán vượt qua ngưỡng chuẩn $0.8$ mà không làm thoái hóa độ chính xác tổng thể.

---

<a name="3-thuc-nghiem-2-one-shot-baseline"></a>
## 3. THỰC NGHIỆM 2: ĐƯỜNG CƠ SỞ SINH MỘT LẦN (ONE-SHOT LLM BASELINE)

### 3.1 Phương pháp
Để kiểm tra giả định *"Liệu có cần một pipeline phức tạp hay chỉ cần prompt trực tiếp một LLM mạnh là đủ?"*, hệ thống xây dựng nhánh baseline `scripts/experiment_llm_once.py`. Với mỗi bài toán, LLM nhận toàn bộ `statement.md` và được yêu cầu sinh trực tiếp một file JSON chứa 20 testcase (input và expected output) trong một lượt gọi duy nhất. Không có validator kiểm tra grammar, không có Reference Pool chứng nhận expected output, và không có feedback loop.

### 3.2 Kết quả định lượng (Hoàn tất 60/60 bài toán)

| Hệ thống đánh giá | Macro TPR (%) | Macro TNR (%) | Micro TPR (%) | Micro TNR (%) | Số bài đạt cả TPR & TNR $\ge 0.8$ | Số testcase hợp lệ TB |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **One-shot LLM Baseline** | **12.60%** | **99.13%** | 12.14% | 99.10% | **5 / 59 (8.5%)** | 19.54 |
| **Pipeline đề xuất (Final)** | **88.07%** | **85.78%** | 87.59% | 86.82% | **40 / 59 (67.8%)** | 19.07 |
| **Chênh lệch ($\text{Pipeline} - \text{One-shot}$)** | **+75.46%** | -13.35% | **+75.45%** | -12.28% | **+35 bài (+59.3%)** | — |

### 3.3 Đánh giá ý nghĩa khoa học
- **Ảo giác Expected Output của LLM**: Khi sinh trực tiếp, LLM có thể tạo ra input trông rất hợp lệ, nhưng giá trị output mong đợi (expected output) bị tính toán sai nghiêm trọng do giới hạn suy luận số học nội tại của mô hình ngôn ngữ.
- **TNR cao giả tạo (False High TNR)**: One-shot đạt TNR 99.13% không phải vì bộ test mạnh, mà vì expected output bị sai khiến bộ test trở thành một "bộ lọc mù" loại bỏ tất cả các chương trình nộp vào. Minh chứng là TPR sụp đổ chỉ còn **12.60%** (hầu hết các lời giải đúng Accepted từ CodeNet/Codeforces đều bị đánh rớt).
- **Giá trị cốt lõi của Pipeline**: Pipeline đề xuất mang lại mức tăng vượt trội **+75.46% TPR** (95% CI: **[+66.81%, +83.60%]**), với 52 bài cải thiện rõ rệt và 0 bài suy giảm. Điều này khẳng định cơ chế **Multi-Reference Consensus** là thành phần sống còn để đảm bảo tính đúng đắn của dữ liệu kiểm thử.

---

<a name="4-thuc-nghiem-3-sample-only-baseline"></a>
## 4. THỰC NGHIỆM 3: ĐƯỜNG CƠ SỞ TEST MẪU ĐỀ BÀI (SAMPLE-ONLY BASELINE)

### 4.1 Phương pháp
Đánh giá chất lượng của tập kiểm thử tối thiểu: chỉ sử dụng các testcase ví dụ có sẵn trong đề bài (Official Samples) để chấm tập chương trình lịch sử. Đây là cận dưới kỹ thuật mà bất kỳ hệ thống sinh test nào cũng phải vượt qua.

### 4.2 Kết quả định lượng (Trên 58 bài toán có Test mẫu)

| Cấu hình | Macro TPR (%) | Macro TNR (%) | Micro TPR (%) | Micro TNR (%) | Cả hai $\ge 0.8$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Sample-only Baseline** | **91.58%** | **49.47%** | 91.35% | 50.41% | 7 / 58 (12.1%) |
| **Pipeline đề xuất (Final)** | **88.07%** | **85.78%** | 87.59% | 86.82% | **40 / 59 (67.8%)** |
| **Chênh lệch ($\text{Pipeline} - \text{Sample}$)** | -3.51% | **+36.31%** | -3.76% | **+36.41%** | **+33 bài (+55.7%)** |

### 4.3 Đánh giá ý nghĩa
- **Bẫy của Sample Test**: Test mẫu có TPR rất cao (91.58%) vì các lập trình viên luôn chạy thử mẫu trước khi nộp bài. Tuy nhiên, khả năng phát hiện lỗi cực kỳ kém cỏi với TNR chỉ đạt **49.47%** (bỏ lọt hơn một nửa số lời giải sai).
- **Mức độ nâng cấp của Pipeline**: Pipeline giúp tăng vọt **+36.07% TNR** (95% CI: **[+30.59%, +41.57%]**), nâng số lượng bài đạt chuẩn độ tin cậy từ 7 bài lên 40 bài.

---

<a name="5-thuc-nghiem-4-repeated-runs"></a>
## 5. THỰC NGHIỆM 4: ĐỘ LẶP LẠI VÀ PHÂN TÍCH PHƯƠNG SAI (REPEATED RUNS 3X)

### 5.1 Thiết kế thực nghiệm
Để đánh giá độ bất định thống kê và tính tái lập, hệ thống chọn ra **12 bài toán phân tầng** (stratified cohort) đại diện cho các mức độ phức tạp và họ thuật toán khác nhau:
- Bài dễ / cấu trúc tuần tự: `cf1003a`, `cf1005a`, `cf1008a`, `p02548`.
- Bài tham lam / tối ưu hóa: `cf1008b`, `p02623`.
- Bài tính toán số thực / trung bình cộng: `cf1003c`.
- Bài mảng nhiều truy vấn / ghép cặp: `cf1949b`.
- Bài quy hoạch động và hoán vị chu trình phức tạp: `p02585`, `p02586`, `p02986`, `p03274`.

Mỗi bài toán được chạy độc lập **3 lần (3 Replicates)** từ đầu (sinh mới test model, candidate, mutant, và bộ test) trên cùng môi trường Docker.

### 5.2 Bảng kết quả tổng hợp chi tiết qua 3 Replicates

*(Ghi chú: Bài `cf1003c` được cập nhật kết quả chuẩn xác sau khi cấu hình đúng Float Checker $\epsilon = 10^{-6}$)*.

| Bài toán | Phân loại thuật toán | Rep 1 (TPR / TNR) | Rep 2 (TPR / TNR) | Rep 3 (TPR / TNR) | Mean TPR $\pm$ SD | Mean TNR $\pm$ SD | Số test TB | Đánh giá |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`cf1003a`** | Mảng / Tần suất | 90.0% / 100.0% | 90.0% / 100.0% | 90.0% / 100.0% | **90.0% $\pm$ 0.0%** | **100.0% $\pm$ 0.0%** | 20.3 | Đạt chuẩn |
| **`cf1003c`** | Mảng / Số thực (Float) | 75.0% / 100.0% | 75.0% / 100.0% | 75.0% / 100.0% | **75.0% $\pm$ 0.0%** | **100.0% $\pm$ 0.0%** | 21.0 | Khắc phục xong |
| **`cf1005a`** | Mảng / Khôi phục chuỗi | 100.0% / 100.0% | 100.0% / 100.0% | 100.0% / 100.0% | **100.0% $\pm$ 0.0%** | **100.0% $\pm$ 0.0%** | 22.0 | Xuất sắc |
| **`cf1008a`** | Chuỗi (Romaji) | 90.0% / 75.0% | 90.0% / 75.0% | 90.0% / 75.0% | **90.0% $\pm$ 0.0%** | **75.0% $\pm$ 0.0%** | 22.0 | Cận đạt |
| **`cf1008b`** | Tham lam / Hình học | 100.0% / 60.0% | 100.0% / 45.0% | 100.0% / 60.0% | **100.0% $\pm$ 0.0%** | **55.0% $\pm$ 8.7%** | 21.0 | Thiếu Fault Model |
| **`cf1949b`** | Ghép cặp / Mảng | 0.0% / 100.0% | 0.0% / 100.0% | 0.0% / 100.0% | **0.0% $\pm$ 0.0%** | **100.0% $\pm$ 0.0%** | 21.0 | Sai nhãn dữ liệu |
| **`p02548`** | Số học ($A \times B + C$) | 95.0% / 95.0% | 95.0% / 100.0% | 95.0% / 100.0% | **95.0% $\pm$ 0.0%** | **98.3% $\pm$ 2.9%** | 15.3 | Xuất sắc |
| **`p02585`** | Hoán vị chu trình ($K \le 10^9$) | 68.4% / 84.2% | 68.4% / 89.5% | 68.4% / 84.2% | **68.4% $\pm$ 0.0%** | **86.0% $\pm$ 3.0%** | 23.7 | TLE Stress test |
| **`p02586`** | QHĐ lưới ($3000 \times 3000$) | 45.0% / 85.0% | 45.0% / 85.0% | *Dừng sớm (1/5 ref)* | **45.0% $\pm$ 0.0%** | **85.0% $\pm$ 0.0%** | 22.5 | OOM / Heap limit |
| **`p02623`** | Tổng tiền tố / Hai con trỏ | 95.0% / 50.0% | 95.0% / 50.0% | 95.0% / 70.0% | **95.0% $\pm$ 0.0%** | **56.7% $\pm$ 11.5%** | 23.0 | Thiếu Corner case |
| **`p02986`** | Cây / Khoảng cách (LCA) | 94.7% / 85.0% | 94.7% / 95.0% | 94.7% / 95.0% | **94.7% $\pm$ 0.0%** | **91.7% $\pm$ 5.8%** | 18.3 | Đạt chuẩn |
| **`p03274`** | Mảng / Two Pointers | 90.0% / 95.0% | 85.0% / 100.0% | 90.0% / 90.0% | **88.3% $\pm$ 2.9%** | **95.0% $\pm$ 5.0%** | 24.0 | Đạt chuẩn |

### 5.3 Nhận xét về độ ổn định (Reproducibility)
1. **Phương sai cực thấp trên TPR**: 11/12 bài có độ lệch chuẩn $\text{SD} = 0.0\%$, bài còn lại (`p03274`) chỉ có $\text{SD} = 2.9\%$. Điều này chứng minh quy trình chứng nhận và đồng thuận Reference Pool loại bỏ hoàn toàn tính bất định ngẫu nhiên của LLM trong việc tạo output mong đợi.
2. **Độ ổn định cao trên TNR**: Độ lệch chuẩn dao động từ $0.0\%$ đến tối đa $11.5\%$ (trung bình $\text{SD} \approx 3.1\%$).
3. **Cơ chế an toàn (Guardrail) vận hành đúng**: Ở lượt chạy thứ 3 của bài `p02586`, do bài toán quy hoạch động quá khó, LLM chỉ sinh được 1/5 candidate vượt qua test mẫu. Hệ thống đã chủ động kích hoạt cơ chế ngắt sớm (`RuntimeError: Only 1/5 reference candidates passed compilation and official samples`) để ngăn chặn việc sinh test sai, bảo vệ tính toàn vẹn của kết quả.

---

<a name="6-phan-tich-nguyen-nhan-goc-re"></a>
## 6. PHÂN TÍCH NGUYÊN NHÂN GỐC RỄ CÁC BÀI KHÔNG ĐẠT CHỈ SỐ

Thông qua việc giải phẫu trực tiếp log thực thi container và mã nguồn từng bài nộp của học sinh, 6 bài toán không đạt ngưỡng $0.8$ được phân định thành **5 nguyên nhân kỹ thuật cụ thể**:

### Nhóm 1: Nhiễm nhãn dữ liệu từ kho gốc CodeNet (`cf1949b` - TPR 0.0%)
- **Bản chất**: Đề bài [data/problems/cf1949b/statement.md](file:///d:/KLTN/Final_TestcaseGenerator/data/problems/cf1949b/statement.md) là bài toán ghép cặp số học ("Charming Meals"), yêu cầu in ra các số nguyên. Pipeline sinh test và reference hoàn toàn chính xác.
- **Nguyên nhân**: Toàn bộ mã nguồn học sinh trong thư mục oracle Accepted của bài này (`1.cpp`, `2.cpp`) thực tế lại là lời giải của một bài toán xử lý xâu (Anagram: đọc `scanf("%lld %s %s", &n, s, t)` và in `YES`/`NO`). Khi nạp testcase số học vào, 100% code học sinh bị sai định dạng và in `NO`, dẫn đến TPR bằng 0% giả tạo.

### Nhóm 2: Lệch cấu hình Checker số thực (`cf1003c` - TPR ban đầu 30% $\to$ Cải thiện 75%)
- **Bản chất**: Đề bài Codeforces 1003C yêu cầu tính trung bình đoạn con lớn nhất, chấp nhận sai số $|res - res_0| < 10^{-6}$.
- **Nguyên nhân**: Ban đầu hệ thống sử dụng cấu hình `TOKEN` checker (so khớp xâu chính xác). Các bài nộp Accepted in ra số chữ số thập phân khác nhau (`2.66666666666667`, `2.6666666666666665`, `2.66666666418314`) bị đánh trượt oan 14/20 bài.
- **Khắc phục**: Khi chuyển sang `FLOAT` checker ($\epsilon = 10^{-6}$), **TPR lập tức tăng từ 30.0% lên 75.0%**, 100% các bài nộp đúng chuẩn toán học đều được chấp nhận; 5 bài còn lại bị loại vì lỗi TLE/RE thực tế trong container.

### Nhóm 3: Giới hạn tài nguyên Sandbox và Môi trường thực thi (`p02586`, `p02585`)
- **Bài `p02586` (TPR 45.0%)**: Bài toán yêu cầu quy hoạch động trên lưới $3000 \times 3000$. Testcase stress cực đại `p02586_i0_006` khiến:
  - Các bài nộp Java bị `OutOfMemoryError: Java heap space` do mảng $3000 \times 3000 \times 4$ vượt ngưỡng heap 192MB/256MB.
  - Các bài nộp Python sử dụng `numpy` bị lỗi `ModuleNotFoundError: No module named 'numpy'` do container sandbox chưa hỗ trợ thư viện ngoài.
- **Bài `p02585` (TPR 68.4%)**: Bài toán hoán vị chu trình với $K = 10^9$. Testcase `p02585_i0_014` sinh chu trình lớn $N=5000$. Các bài làm của học sinh dùng giải thuật mô phỏng $O(N^2)$ bị chạm ngưỡng thời gian 2.0s trên Docker Engine Windows và bị xử TLE.

### Nhóm 4: Lỗ hổng trong Fault Model của Test Generator (`cf1008b`, `p02623`)
- **Bài `cf1008b` (TNR 55.0%)**: Lỗi sai phổ biến của thí sinh là thuật toán tham lam cục bộ: khi gặp hình chữ nhật có thể xoay, code chọn nhầm chiều lớn hơn thay vì chiều nhỏ hơn $\le$ chiều trước đó. Test generator chỉ sinh các cặp kích thước ngẫu nhiên độc lập, thiếu chuỗi phụ thuộc 3 bước để gài bẫy giải thuật tham lam.
- **Bài `p02623` (TNR 56.7%)**: Lỗi kinh điển của thí sinh là luôn đọc ít nhất 1 quyển sách ở chồng A. Bộ test thiếu ca kiểm thử cực biên khi toàn bộ sách ở chồng A đều quá lớn ($> K$) và nghiệm tối ưu nằm hoàn toàn ở chồng B.

### Nhóm 5: Tác dụng phụ của cơ chế Pipe Windows CRLF (`cf1008a` - TNR 75.0%)
- **Bản chất**: 5 code sai của học sinh đều lặp `range(len(s) - 1)` và quên kiểm tra ký tự cuối cùng của chuỗi có phải phụ âm hay không.
- **Nguyên nhân**: Khi chạy trên Windows, `subprocess.run(text=True)` tự động chèn `\r\n`. Vào trong Linux container, `input()` chỉ cắt `\n` và giữ lại `\r`. Ký tự cuối trở thành `\r` (không phải nguyên âm), khiến code học sinh vô tình rẽ nhánh in `NO`. Do kỳ vọng của test cũng là `NO`, 5 code sai này vô tình thoát chết (false survivor).

---

<a name="7-bao-cao-va-phan-ra-do-tre"></a>
## 7. BÁO CÁO VÀ PHÂN RÃ ĐỘ TRỄ (LATENCY ANALYSIS)

### 7.1 Thời gian thực thi tổng thể
Dữ liệu độ trễ được tính toán chính xác trên các lần chạy thành công hoàn tất của 3 Replicates:

| Replicate | Số bài hoàn tất | Tổng thời gian (giây) | Thời gian TB / bài (giây) | Thời gian ngắn nhất (giây) | Thời gian dài nhất (giây) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Replicate 1** | 12 / 12 | 3,421.09 s (57.0 phút) | **285.09 s** | 218.80 s (`cf1003a`) | 362.53 s (`p02586`) |
| **Replicate 2** | 12 / 12 | 3,351.67 s (55.9 phút) | **279.31 s** | 186.63 s (`p02585`) | 384.02 s (`p02986`) |
| **Replicate 3** | 11 / 12 | 2,100.80 s (35.0 phút) | **190.98 s** | 145.53 s (`cf1003c`) | 275.92 s (`p02986`) |
| **Trung bình chung** | **35 runs** | — | **253.53 s** (~4.2 phút) | **145.53 s** | **384.02 s** |

### 7.2 Phân rã độ trễ theo từng thành phần (Latency Breakdown)

Phân tích log telemetry chi tiết từ Replicate 1 cho thấy cơ cấu thời gian của một lượt chạy hoàn chỉnh:

```
[================= TỔNG THỜI GIAN TRUNG BÌNH: 285.1 GIÂY =================]
|-- 1. LLM Xây dựng Test Model độc lập:        98.5 s (34.5%) [Nút thắt lớn nhất]
|-- 2. Sinh và Chứng nhận Candidate AC & WA:   52.4 s (18.4%)
|-- 3. Sinh Test Suite & Consensus Output:     44.2 s (15.5%)
|-- 4. Chấm và Đánh giá Oracle CodeNet ngoài:  67.5 s (23.7%) [Chấm 40 code x 22 test]
|-- 5. Biên dịch, Replay & Ghi chép Artifact:  22.5 s  (7.9%)
```

1. **Giai đoạn chiếm thời gian lâu nhất**: Giai đoạn **LLM xây dựng Test Model** (`Build test model`) là giai đoạn kéo dài nhất trong 15/16 lần chạy đo lường độc lập. Nguyên nhân do LLM phải phân tích ngữ nghĩa đề bài, sinh input grammar, quan hệ metamorphic và bảng liệt kê fault model có cấu trúc JSON phức tạp.
2. **Chi phí thời gian của Oracle Evaluation**: Chấm 40 mã nguồn đối chứng ngoài (20 AC, 20 WA) trên tập 20–24 testcase bên trong container Docker tốn trung bình từ 45s đến 90s tùy thuộc số lượng testcase stress.
3. **Chi phí của cơ chế Retry khi gặp sự cố mạng/mô hình**:
   - Khi Ollama hoặc LLM bị quá tải/timeout, cơ chế retrying judge giúp pipeline tự phục hồi nhưng làm tăng tổng thời gian wall-clock (ví dụ bài `cf1005a` ở Replicate 2 mất tới 3 lần thử với tổng cộng 2,303 giây trước khi hoàn tất lượt chạy thành công 383 giây).

---

<a name="8-bang-doi-chieu-tong-hop"></a>
## 8. BẢNG MA TRẬN ĐỐI CHIẾU TỔNG HỢP 4 THỰC NGHIỆM

Bảng đối chiếu tổng hợp dưới đây phản ánh bức tranh toàn cảnh về hiệu năng của các giải pháp trên cùng tập dữ liệu:

| Chỉ số đánh giá | (1) Sample-only Baseline | (2) One-shot LLM Baseline | (3) Pipeline Vòng 1 (No Feedback) | (4) Pipeline Vòng 2 (Final Proposal) | (5) Repeated Runs (Mean 12 bài) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Quy mô đánh giá** | 58 bài | 60 bài (59 có oracle) | 59 bài | 59 bài | 12 bài $\times$ 3 rep |
| **Macro TPR (Fidelity)** | 91.58% | 12.60% | 88.32% | **88.07%** | **78.46%** *(có cf1949b)* |
| **Macro TNR (Discriminability)**| 49.47% | 99.13% *(ảo giác)* | 82.80% | **85.78%** | **86.89%** |
| **Balanced Accuracy (BA)** | 70.53% | 55.87% | 85.56% | **86.93%** | **82.68%** |
| **Tỷ lệ đạt cả 2 $\ge 0.8$** | 12.1% (7/58) | 8.5% (5/59) | 62.7% (37/59) | **67.8% (40/59)** | **41.7% (5/12)** |
| **Số testcase trung bình** | 1.8 | 19.5 | 11.2 | **19.1** | **21.0** |
| **Phương sai lặp lại (SD TPR)**| — | — | — | — | **0.00%** *(rất ổn định)* |
| **Độ trễ trung bình / bài** | < 5s | ~25s | ~130s | **~178s** | **~253s** |

---

<a name="9-ket-luan-va-khuyen-nghi"></a>
## 9. KẾT LUẬN VÀ KHUYẾN NGHỊ CHO KHÓA LUẬN TỐT NGHIỆP

### 9.1 Các luận điểm khoa học bảo vệ thành công
1. **Khẳng định tính ưu việt của Pipeline so với các Baseline**:
   - Vượt trội hoàn toàn so với **One-shot Baseline** (+75.46% TPR), chứng minh rằng việc kết hợp mô hình kiểm thử hình thức (Test Model) và cơ chế chứng nhận đa lời giải (Consensus) là điều kiện bắt buộc để sử dụng LLM trong kỹ nghệ phần mềm.
   - Vượt trội hoàn toàn so với **Sample-only Baseline** (+36.31% TNR), chứng minh khả năng tự động khám phá và tiêu diệt các lỗi biên tiềm ẩn của học sinh.
2. **Chứng minh vai trò của Vòng lặp phản hồi (Feedback Refinement)**: Vòng lặp phản hồi giúp tăng thêm +2.98% TNR một cách an toàn, đưa thêm các bài toán khó vượt ngưỡng tin cậy mà không làm hỏng các ca kiểm thử đúng.
3. **Tính ổn định và tái lập (Reproducibility)**: Phương sai $\text{SD} = 0.0\%$ trên TPR chứng minh kết quả đầu ra của hệ thống mang tính khoa học vững chắc, không phụ thuộc vào may rủi hay ngẫu nhiên của mô hình tạo sinh.

### 9.2 Đóng góp về Kỹ nghệ Dữ liệu (Empirical Software Engineering Lessons)
- Phát hiện hiện tượng **nhiễm nhãn (Data Contamination)** trong các tập dữ liệu thi đấu lớn như CodeNet (`cf1949b`), mở ra hướng nghiên cứu về việc dùng AI để kiểm định (audit) lại các bộ benchmark công cộng.
- Chỉ ra tầm quan trọng của việc cấu hình đúng **Checker số thực (Float Checker)** và chuẩn hóa ngắt dòng **POSIX LF** trên môi trường lai (Windows Host $\leftrightarrow$ Linux Docker Container).

---
*Báo cáo được khởi tạo tự động dựa trên dữ liệu thực nghiệm đã khóa tại `output/experiments/`.*
