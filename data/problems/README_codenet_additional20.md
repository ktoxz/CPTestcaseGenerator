# CodeNet — thêm 20 bài (12/10/2026)

Đã tải qua SSH từ `ktoxz:/srv/guidelet/staging/codenet`. Không trùng 20 bài của đợt exact-output trước.

Mỗi bài có đúng **20 Accepted + 20 Wrong Answer**, tổng **800 source**, đa dạng C, C++, Java và Python. Nhãn được giữ nguyên từ CodeNet; không phải kết quả chấm lại toàn bộ 800 source.

Có **17 EXACT, 1 TOKEN và 2 PYTHON_SCRIPT**. Cả 18 bài EXACT/TOKEN có đáp án duy nhất; TOKEN của Friend Suggestions chấp nhận khác biệt khoảng trắng/xuống dòng. Hai bài nhiều đáp án dùng loại checker PYTHON_SCRIPT đã có, với logic riêng theo đề.

| ID | Bài | Thuật toán | Checker | AC/WA |
|---|---|---|---|---|
| [p02554](p02554/statement.md) | ABC 178 - Ubiquity | inclusion-exclusion | EXACT | 20/20 |
| [p02555](p02555/statement.md) | ABC 178 - Redistribution | composition counting / DP | EXACT | 20/20 |
| [p02584](p02584/statement.md) | ABC 175 - Walking Takahashi | greedy / parity | EXACT | 20/20 |
| [p02585](p02585/statement.md) | ABC 175 - Moving Piece | permutation cycles | EXACT | 20/20 |
| [p02586](p02586/statement.md) | ABC 175 - Picking Goods | grid DP | EXACT | 20/20 |
| [p02596](p02596/statement.md) | ABC 174 - Repsept | modular arithmetic | EXACT | 20/20 |
| [p02598](p02598/statement.md) | ABC 174 - Logs | binary search | EXACT | 20/20 |
| [p02599](p02599/statement.md) | ABC 174 - Range Set Query | offline range queries / Fenwick tree | EXACT | 20/20 |
| [p02614](p02614/statement.md) | ABC 173 - H and V | bitmask enumeration | EXACT | 20/20 |
| [p02623](p02623/statement.md) | ABC 172 - Tsundoku | prefix sums / two pointers | EXACT | 20/20 |
| [p02629](p02629/statement.md) | ABC 171 - One Quadrillion and One Dalmatians | bijective base 26 | EXACT | 20/20 |
| [p02642](p02642/statement.md) | ABC 170 - Not Divisible | sieve / duplicate counting | EXACT | 20/20 |
| [p02678](p02678/statement.md) | ABC 168 - .. (Double Dots) | BFS / shortest-path tree | PYTHON_SCRIPT | 20/20 |
| [p02691](p02691/statement.md) | ABC 166 - This Message Will Self-Destruct in 5s | frequency counting | EXACT | 20/20 |
| [p02702](p02702/statement.md) | ABC 164 - Multiple of 2019 | suffix remainders | EXACT | 20/20 |
| [p02714](p02714/statement.md) | ABC 162 - RGB Triplets | counting / excluded arithmetic progressions | EXACT | 20/20 |
| [p02720](p02720/statement.md) | ABC 161 - Lunlun Number | BFS enumeration | EXACT | 20/20 |
| [p02762](p02762/statement.md) | ABC 157 - Friend Suggestions | DSU / connected components | TOKEN | 20/20 |
| [p02787](p02787/statement.md) | ABC 153 - Crested Ibis vs Monster | unbounded knapsack | EXACT | 20/20 |
| [p03044](p03044/statement.md) | ABC 126 - Even Relation | tree distance parity | PYTHON_SCRIPT | 20/20 |

## Kiểm tra

- Đủ 800 source, checksum từng file khớp manifest; không trùng source trong từng bài và không trùng fingerprint chuẩn hóa trong từng nhóm nhãn.
- Cả 20 checker nạp được; chấp nhận đủ 60 output mẫu chính thức.
- Ba nhóm unit test checker đều qua: vét cạn cây nhỏ và cách tô màu; đồ thị liên thông nhỏ và cách chọn biển chỉ dẫn; đáp án thay thế và output lỗi.
- Docker chạy 26 chương trình đại diện, tổng 116 lượt: 22 source AC đều qua các ca đã chọn; cả 4 source WA của hai bài nhiều đáp án đều bị phát hiện ít nhất một ca (3 do WA, 1 do RE).
- Ban đầu EXACT loại source AC của p02762 do in mỗi số một dòng. Đã chuyển sang TOKEN và chấm lại output Docker đã ghi; nội dung số khớp cả 3 sample.
- Chưa chạy toàn bộ pipeline sinh test bằng LLM và chưa rejudge toàn bộ 800 source.

Báo cáo chạy: [report.json](../../output/codenet-additional20-validation/report.json).

## Hai bài nhiều đáp án

- **p02678 — Double Dots**: tự BFS từ phòng 1; mỗi biển phải chỉ sang phòng kề có khoảng cách ngắn nhất giảm đúng 1. Chấp nhận mọi cây đường đi ngắn nhất hợp lệ, không phụ thuộc output mẫu.
- **p03044 — Even Relation**: kiểm tra mọi đỉnh cùng màu có cùng parity khoảng cách từ gốc. Khi mọi cạnh chẵn, mọi cách tô đều hợp lệ. Chấp nhận cả đảo màu và sample có màu xen kẽ trên cây toàn cạnh chẵn.

## Chạy lại

```powershell
python -m unittest discover -s tests -p test_codenet_additional20_checkers.py -v
python scripts/verify_codenet_additional20.py
python main.py --problem p02678 --oracle --oracle-limit 20
python main.py --problem p03044 --oracle --oracle-limit 20
```

Để tái tạo vào thư mục mới (script từ chối ghi đè bài có sẵn):

```powershell
python scripts/materialize_codenet_additional20.py --archive data/codenet-additional20-20261012.tar.gz --output output/rebuilt-additional20
```

Các ID của bộ mới:

```text
p02554 p02555 p02584 p02585 p02586 p02596 p02598 p02599 p02614 p02623 p02629 p02642 p02678 p02691 p02702 p02714 p02720 p02762 p02787 p03044
```

Bundle SHA-256: `a024a49b36bda96a5304ccfa5a1a8011d566665e13f2f531319dd1bff6ce8fae`
