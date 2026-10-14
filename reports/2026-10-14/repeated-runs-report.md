# Báo cáo thực nghiệm chạy lặp ba lần

Ngày chốt số liệu: 14/10/2026  
Nguồn dữ liệu: `output/experiments/repeated-runs-20261013`  
Ngưỡng đạt: `TPR >= 0.8` và `TNR >= 0.8`

## 1. Trạng thái thực nghiệm

Thực nghiệm dự kiến 12 bài x 3 replicate, tương ứng 36 run. Hiện có 35
`report.json` hợp lệ, đạt 97.2%. Replicate 1 và 2 đủ 12 bài; replicate 3 có
11 bài. Run còn thiếu là `replicate-3/p02586`.

Hai attempt đầu của `p02586` replicate 3 dừng ở chứng nhận reference: chỉ 1/5
candidate AC vượt qua compile và toàn bộ official samples. Hai attempt bổ sung
không vào pipeline vì Docker local không sẵn sàng. Báo cáo không nội suy kết quả
cho run này.

Protocol thực tế không đồng nhất hoàn toàn:

- Replicate 1 dùng chuỗi Gemma4 -> Nemotron -> Fable.
- Bảy bài đầu replicate 2, từ `cf1003a` đến `p02548`, dùng chuỗi fallback trên.
- Năm bài cuối replicate 2, từ `p02585` đến `p03274`, chỉ dùng Gemma4.
- Replicate 3 chỉ dùng Gemma4.
- Các run đã ghi nhận đều dùng hard timeout Ollama 60 giây từ snapshot protocol.
  Cấu hình 120 giây được đặt sau thực nghiệm và không áp dụng cho số liệu này.

Vì thay đổi model routing xảy ra giữa thực nghiệm, ba replicate không phải ba
lần lặp hoàn toàn đồng nhất. So sánh giữa replicate chỉ mang tính mô tả. Phân
tích độ ổn định theo từng bài vẫn có giá trị để nhận diện lỗi có tính hệ thống.

## 2. Kết quả tổng hợp

| Replicate | Hoàn thành | Macro TPR | Macro TNR | Đạt cả hai ngưỡng | Tổng test | Test/bài | Pipeline thành công trung bình |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 12/12 | 0.7485 | 0.8577 | 5/12 | 261 | 21.75 | 285.1 giây |
| 2 | 12/12 | 0.7443 | 0.8662 | 5/12 | 253 | 21.08 | 279.3 giây |
| 3 | 11/12 | 0.7756 | 0.8856 | 5/11 | 226 | 20.55 | 191.0 giây |
| Toàn bộ report hợp lệ | 35/36 | 0.7556 | 0.8694 | 15/35 | 740 | 21.14 | 253.5 giây |

Do replicate 3 thiếu `p02586`, so sánh công bằng hơn dùng 11 bài chung giữa cả
ba replicate:

| Replicate | Macro TPR trên 11 bài | Macro TNR trên 11 bài | Đạt cả hai ngưỡng |
|---|---:|---:|---:|
| 1 | 0.7756 | 0.8584 | 5/11 |
| 2 | 0.7711 | 0.8677 | 5/11 |
| 3 | 0.7756 | 0.8856 | 5/11 |

Trên cohort ghép cặp này, TPR gần như không đổi. TNR replicate 3 cao hơn
replicate 1 khoảng 0.0273, nhưng chưa thể quy hoàn toàn cho Gemma-only vì code
và model routing đã thay đổi trong quá trình chạy.

## 3. Kết quả theo bài

`SD` là độ lệch chuẩn mẫu giữa các replicate đã hoàn thành.

| Bài | Số run | TPR trung bình +/- SD | TNR trung bình +/- SD | Số lần đạt cả hai | Số test R1/R2/R3 |
|---|---:|---:|---:|---:|---:|
| cf1003a | 3 | 0.900 +/- 0.000 | 1.000 +/- 0.000 | 3/3 | 21 / 19 / 21 |
| cf1003c | 3 | 0.300 +/- 0.000 | 1.000 +/- 0.000 | 0/3 | 21 / 21 / 21 |
| cf1005a | 3 | 1.000 +/- 0.000 | 1.000 +/- 0.000 | 3/3 | 23 / 21 / 22 |
| cf1008a | 3 | 0.900 +/- 0.000 | 0.750 +/- 0.000 | 0/3 | 21 / 23 / 22 |
| cf1008b | 3 | 1.000 +/- 0.000 | 0.550 +/- 0.087 | 0/3 | 22 / 19 / 22 |
| cf1949b | 3 | 0.000 +/- 0.000 | 1.000 +/- 0.000 | 0/3 | 21 / 21 / 21 |
| p02548 | 3 | 0.950 +/- 0.000 | 0.983 +/- 0.029 | 3/3 | 16 / 15 / 15 |
| p02585 | 3 | 0.684 +/- 0.000 | 0.860 +/- 0.030 | 0/3 | 24 / 23 / 24 |
| p02586 | 2 | 0.450 +/- 0.000 | 0.850 +/- 0.000 | 0/2 | 22 / 23 / thiếu |
| p02623 | 3 | 0.950 +/- 0.000 | 0.567 +/- 0.115 | 0/3 | 23 / 23 / 23 |
| p02986 | 3 | 0.947 +/- 0.000 | 0.917 +/- 0.058 | 3/3 | 23 / 21 / 11 |
| p03274 | 3 | 0.883 +/- 0.029 | 0.950 +/- 0.050 | 3/3 | 24 / 24 / 24 |

Năm bài đạt cả hai ngưỡng ổn định là `cf1003a`, `cf1005a`, `p02548`,
`p02986` và `p03274`.

TPR gần như không có phương sai. Ngoài `p03274`, TPR của mỗi bài giống hệt ở
mọi lần chạy có kết quả. Các mức thấp vì vậy là lỗi hệ thống thay vì nhiễu:

- `cf1949b`: TPR 0.00, bộ test loại toàn bộ AC oracle.
- `cf1003c`: TPR 0.30.
- `p02586`: TPR 0.45 ở cả hai run hoàn thành.
- `p02585`: TPR 0.684 ở cả ba run.

TNR yếu nhất ở `cf1008b` (trung bình 0.55), `p02623` (0.567) và `cf1008a`
(0.75). `p02623` có phương sai TNR lớn nhất, từ 0.50 ở hai replicate đầu lên
0.70 ở replicate 3. Đây là nhóm cần tăng testcase phân biệt mutant.

## 4. Latency và độ ổn định vận hành

| Replicate | Tổng pipeline thành công | Trung bình/bài | Tổng thời gian mọi attempt | Attempt lỗi |
|---|---:|---:|---:|---:|
| 1 | 57.0 phút | 285.1 giây | 93.9 phút | 26 |
| 2 | 55.9 phút | 279.3 giây | 92.0 phút | 4 |
| 3 | 35.0 phút cho 11 bài | 191.0 giây | 48.5 phút | 5 |

Số attempt lỗi của replicate 1 gồm nhiều lần chạy lại thủ công trước khi cơ chế
retry hiện tại ổn định. Replicate 2 chỉ có bốn attempt lỗi, nhưng hai timeout dài
của `cf1005a` lần lượt khoảng 957 và 961 giây làm tổng wall time tăng mạnh.
Replicate 3 có một attempt `p02986` lỗi sau khoảng 697 giây và bốn attempt lỗi
của `p02586`.

Ở replicate 1, bước xây test model là phase lâu nhất trong 11/12 bài. Sang
replicate 3, oracle CodeNet là phase lâu nhất trong 10/11 bài hoàn thành. Pipeline
thành công trung bình giảm từ 285.1 xuống 191.0 giây, tương đương 33.0%. Phần
lớn mức giảm đến từ việc không gọi Nemotron/Fable sau khi Gemma trả response
không hợp lệ.

Ba run thành công chậm nhất:

- Replicate 1: `p02586` 362.5 giây, `cf1008b` 319.5 giây, `p02585` 313.7 giây.
- Replicate 2: `p02986` 384.0 giây, `cf1005a` 383.5 giây, `cf1008b` 332.4 giây.
- Replicate 3: `p02986` 275.9 giây, `p03274` 210.6 giây, `cf1008b` 210.5 giây.

## 5. Khoảng cách giữa đánh giá nội bộ và oracle

| Replicate | Internal TPR | Oracle TPR | Internal TNR | Oracle TNR |
|---|---:|---:|---:|---:|
| 1 | 0.8222 | 0.7485 | 1.0000 | 0.8577 |
| 2 | 0.8306 | 0.7443 | 1.0000 | 0.8662 |
| 3 | 0.9455 | 0.7756 | 0.9697 | 0.8856 |

Candidate pool nội bộ đánh giá quá lạc quan. Replicate 3 có khoảng cách TPR lớn
nhất: 0.1699. Việc pipeline báo đạt tiêu chí nội bộ không đảm bảo chất lượng
trên oracle. Trường hợp rõ nhất là `cf1949b`: replicate 2 và 3 dừng với
`all_quality_criteria_met`, nhưng oracle TPR vẫn bằng 0.00.

## 6. Vấn đề test model và coverage

Replicate 1 có 8/12 bài không sinh được coverage obligation. Replicate 2 và mọi
run thành công của replicate 3 đều có 0 obligation. Hệ thống vẫn ghi
`coverage_ratio = 1.0` cho trường hợp tập obligation rỗng. Đây là giá trị rỗng
0/0, không phải bằng chứng đạt coverage.

Hiện tượng latency giảm ở replicate 3 đi cùng việc test model bị bỏ qua nhanh
sau response Gemma không đạt schema. Vì vậy không nên diễn giải toàn bộ mức giảm
33% là cải tiến hiệu năng thuần túy; một phần công việc phân tích coverage đã
không được thực hiện thành công.

## 7. Kết luận

Thực nghiệm cho thấy chất lượng có tính ổn định cao theo bài nhưng chưa đạt yêu
cầu chung. Chỉ 5/12 bài đạt đồng thời TPR và TNR tối thiểu 0.8. Các lỗi TPR thấp
lặp lại gần như chính xác qua ba replicate, cho thấy cần sửa validator, expected
output hoặc chiến lược tạo test của từng bài thay vì chỉ chạy thêm lần nữa.

Gemma-only giảm latency rõ rệt và tránh timeout dây chuyền qua Nemotron, nhưng
đồng thời làm test model/coverage thất bại ở toàn bộ run quan sát được sau thay
đổi. Cần sửa schema/prompt test model và coi obligation rỗng là trạng thái
`unavailable` hoặc lỗi bắt buộc trước khi dùng coverage trong luận văn.

Số liệu hiện đủ để báo cáo xu hướng và độ ổn định trên 11 bài hoàn chỉnh. Để
khẳng định thực nghiệm 3 lần trên đủ 12 bài, vẫn cần hoàn tất `p02586` replicate
3 khi Docker local hoạt động trở lại. Sau đó phải tái tạo summary và bảng thống
kê, không dùng nội suy.
