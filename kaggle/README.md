# Chạy smoke test trên Kaggle

Kaggle phù hợp để kiểm tra pipeline có chạy hết luồng với một model nhỏ. Không
nên dùng kết quả từ backend `native` làm benchmark cuối cùng: Kaggle Notebook
không cung cấp Docker daemon cho container lồng nhau, còn `native` chỉ đặt
timeout/rlimit và xóa biến môi trường trước khi chạy code sinh bởi LLM; nó
không cách ly filesystem hay network như Docker.

## Thiết lập Notebook

1. Tạo Kaggle Notebook, bật **GPU** và **Internet** trong Settings.
2. Đưa repository vào một Kaggle Dataset rồi Attach vào notebook. Copy nó từ
   `/kaggle/input/...` (read-only) sang `/kaggle/working/...` trước khi chạy.
3. Chạy lần lượt các cell trong `kaggle_smoke.ipynb`. Sửa `SOURCE` và
   `PROBLEM` cho đúng dataset/bài của bạn.

Preset `config/kaggle.pipeline.json` cố ý nhỏ: Gemma 3 4B, 2 AC, 3 WA, 6 test,
1 vòng và tối thiểu 2 mutant được chứng nhận. Đây là smoke test, không phải cấu
hình dùng để báo cáo TPR/TNR. `config/kaggle.judge.json` giảm concurrency để
tránh tranh CPU/RAM với Ollama; `config/kaggle.runtimes.json` chỉ cho model sinh
C++17/Python 3 để không phụ thuộc JDK hay Python 2 trong image Kaggle.

Lệnh chính mà notebook chạy là:

```bash
python main.py \
  --problem p02548 \
  --config config/kaggle.pipeline.json \
  --judge-config config/kaggle.judge.json \
  --runtime-config config/kaggle.runtimes.json \
  --judge native \
  --allow-unsafe-native-judge \
  --output /kaggle/working/testgen-output/p02548
```

Không bật `--oracle` ở lần đầu. Nhánh SSH trong `config/oracle.json` phụ thuộc
máy `ktoxz` và không tái lập được trên Kaggle. Nếu cần oracle, hãy attach bundle
có `manifest.json` như một Kaggle Dataset rồi dùng `--oracle-cache`.

## Khi chuyển từ smoke test sang benchmark

- Dùng `local`/`remote` Docker judge bên ngoài Kaggle để lấy số đo cuối.
- Ghim snapshot repository, model tag/digest, Kaggle image và lưu toàn bộ
  `run-config.json`, `latency.jsonl`, `test-suite.lock.json`, `report.json`.
- Chạy nhiều seed/bài và giữ tập oracle tách khỏi prompt. Một lần chạy 4B không
  đủ để so sánh chất lượng model.
- Với notebook chia sẻ công khai, không in token/secret. Preset local Ollama
  không cần API key.

Nếu muốn chạy offline, attach sẵn Ollama binary và model blobs dưới dạng
Kaggle Dataset; notebook mẫu hiện chọn quy trình đơn giản hơn là tải chúng khi
Internet đang bật.
