# Technical specs và pipeline sinh testcase

## Input/CLI

`python main.py --problem pNNNNN [--oracle]`. `--iterations` ∈ {1,2,3}; `--oracle-limit` ∈ [1,100] mỗi nhãn; mặc định 3 candidate AC, 5 candidate WA, quota cơ sở 10 test được chấp nhận/vòng, tối thiểu 2 vòng và 18 test, model `gemma4:31b-cloud`. Source statement là Markdown UTF-8. p00004 dùng FLOAT `epsilon=0.0005`, đúng 3 chữ số thập phân và 2 giá trị/dòng; p00005 dùng TOKEN. Đề khác không có profile dùng TOKEN, cần rà trước khi tin metrics.

## Sinh và chứng nhận test

1. Ollama tạo test model chỉ từ statement, trước nhánh candidate. `test-model.json` chứa input grammar, constraints, variables/relations, output partitions, sequences, fault model và coverage obligations có ID/category/priority. Vòng baseline không nhận source, execution hoặc oracle.
2. Ollama phân tích đề, sinh các lời giải độc lập, mutant có `strategy_id`, `bug_origin`, `bug_class`, `failure_condition`, witness và validator Python. Response lưu nguyên JSON.
3. Pipeline chứng nhận từng mutant trước khi tính TNR: code phải compile, qua mọi sample chính thức, witness qua validator, ít nhất hai AC reference qua sample và thống nhất expected, và mutant phải tạo cùng một output khác hoặc RE/TLE trong hai trial riêng. Mutant không ổn định bị loại và được thay thế trong số vòng giới hạn. Cần đạt `minimum_verified_mutants`; thiếu quota nhưng vẫn đạt sàn thì tiếp tục và báo pool thực tế.
4. Docker biên dịch các source. Validator được biên dịch/chạy trong Docker, không chạy trên host. Nếu `data/problems/<id>/validator.py` có sẵn, dùng bản kiểm toán đó thay vì validator LLM; bản LLM vẫn được lưu trong `generated/`.
5. Gộp official samples và input LLM sinh. Chuẩn hóa newline, loại input trùng theo SHA-256. Input LLM không qua validator được đưa lại cho model sửa theo cùng ý đồ test tối đa `input_repair_attempts` (0–2, mặc định 2); mỗi lần thất bại vẫn được quarantine. Official sample bị validator từ chối làm run dừng ngay vì đó là dấu hiệu validator sai.
6. Chạy các candidate AC trên input. Cần ít nhất 2 reference chạy thành công và output đồng ý theo checker của bài. Nếu official sample có expected output, phải khớp. Các trường hợp khác bị quarantine; expected dùng sample hoặc output reference.
7. Vòng 1 sinh baseline theo coverage. Vòng sau chấm development mutants, cập nhật hồ sơ tích lũy và audit survivor. Quota accepted-case dùng survivor, khoảng thiếu TNR, critical gap, reject/duplicate và stalled rounds. Pipeline top-up khi số test được chứng nhận thấp hơn `requested_count`; input validator từ chối được sửa tối đa hai lần.
8. Dừng sớm là hội của các điều kiện: TPR/TNR development ≥0.90, coverage critical/normal đạt cấu hình, đủ `min_iterations`, đủ `min_total_cases`, và không còn survivor hoặc đã đứng yên đủ vòng. `iterations` vẫn là trần cứng; report nêu rõ từng điều kiện và `stop_reason`.
9. Nếu pool đủ lớn, mutant được tách development/holdout trước khi sinh test. Holdout không có trong context/prompt, chỉ chấm sau `test-suite.lock.json`. `--oracle` CodeNet cũng chỉ tải/chấm sau suite lock. Ba log `executions-llm.jsonl`, `executions-holdout.jsonl`, `oracle/executions.jsonl` tách biệt.

## Checker

`checker_from_profile()` đọc `kind` trong JSON và tạo plugin tương ứng; không có chuỗi `if/elif` theo loại chấm trong core. Mỗi loại nằm ở `testgen/checkers/`. Thêm một loại mới chỉ cần class `Checker` với `@register_checker`; thiếu hoặc sai option profile sẽ báo lỗi rõ ràng.

- EXACT: chuẩn hóa CRLF/LF, bỏ khác biệt newline cuối.
- TOKEN: tách whitespace rồi so token đúng thứ tự.
- CASE_INSENSITIVE_TOKEN: TOKEN + Unicode casefold.
- DECIMAL_EXACT: parse Decimal arbitrary precision; có thể bắt buộc số chữ số thập phân.
- FLOAT: parse token số hữu hạn bằng `Decimal` để tránh sai số nhị phân ở đúng ranh giới epsilon, so `|actual-expected| ≤ epsilon`, token count bằng nhau. Tùy bài có `decimal_places` và `values_per_line`. `NaN`/Infinity fail; `-0.000` bằng `0.000` về mặt số học. Định dạng là ràng buộc độc lập, không tự bật cho mọi bài.

## Verdict và metrics

`PASS`, `WA`, `RE`, `CE`, `TLE`, `INFRA`. Một submission nhận verdict lỗi đầu tiên theo thứ tự testcase; output/stderr được lưu trong report. `CE`/`INFRA` không nằm trong mẫu số logic. `tpr_label_based = candidate/original AC PASS / AC evaluable`; `tnr_label_based = candidate/original WA bị WA/RE/TLE / WA evaluable`. TLE phản ánh thất bại hiệu năng, không đồng nghĩa lỗi logic; báo verdict để tách khi phân tích. Nếu mẫu số 0 trả `null`. Các nhãn do LLM/CodeNet gán đều provisional; một mutant chưa bị bắt không được tự chứng nhận là WA, một CodeNet AC bị bắt không tự kết luận oracle sai.

## Sandbox và giới hạn

Image chính build từ `docker/Dockerfile` (Debian, gcc/g++, Java 17, Python 3); Python 2 từ `docker/Dockerfile.python2` chỉ cho source CodeNet có nhãn Python cũ. Mỗi container: `--network none`, `--read-only`, `--cap-drop ALL`, `no-new-privileges`, `--pids-limit 64`, 512 MiB RAM, 1 CPU, `/tmp` tmpfs 32 MiB, source read-only. Compile timeout 90 s, mỗi input timeout 5 s (mặc định). Đây là sandbox thực dụng cho khảo sát, **không phải** cô lập tương đương hạ tầng thi chính thức; cần profile toolchain/time limit cụ thể nếu đối chiếu verdict gốc.

Các con số tài nguyên trên là **mặc định** trong `config/sandbox.json`, không còn nằm trong `docker_judge.py`. Image/dialect/command nằm trong `config/runtimes.json`; host/root của CodeNet trong `config/oracle.json`; Ollama và số lượng ứng viên/test trong `config/pipeline.json`. Các option CLI ghi đè giá trị mặc định tương ứng.

## Giới hạn cần lưu ý

Consensus của code LLM có thể cùng sai; validator LLM có thể quá hẹp (p00004 từng bị áp đặt số nguyên dù đề không nói rõ). Cơ chế sửa input chỉ sửa dữ liệu test, không tự sửa validator và không biến một test bị từ chối thành test hợp lệ. Cần rà input boundaries và dùng oracle độc lập trước khi công bố TPR/TNR verified. `--oracle` phụ thuộc quyền SSH, cài pyarrow tạm từ pip và Docker engine hoạt động. Không chạy tiếp bài khác chỉ dựa trên metric label-based nếu nhãn chưa lọc.
## Chọn máy chấm

Ở chế độ `auto`, preflight `docker info` trên local. Nếu không có Linux engine, `main.py` kiểm tra Docker trên KHOI qua SSH và chuẩn bị image ở đó. Việc chọn diễn ra **trước** khi sinh code/test; một run chỉ sử dụng một judge. Remote worker nhận source của mỗi solution một lần, giữ binary trong thư mục build tạm trên KHOI, rồi chấm từng input bằng Docker không mạng. Nếu remote engine chưa chạy, dừng với thông báo hạ tầng thay vì biến lỗi đó thành WA hay TNR.

Remote judge nhận tối đa `batch_size` input trong một SSH request (mặc định 8); mỗi input vẫn chạy một container với giới hạn riêng. Kết quả thô của từng cặp solution/case/input được cache trong tiến trình để các vòng tiếp theo không chấm lại. `--resume-oracle` chỉ chạy phần CodeNet trên output đã có `tests/` và snapshot vòng cuối, giúp tiếp tục sau lỗi INFRA mà không gọi LLM lần nữa.

`timeout` bên trong container giới hạn thời gian chương trình. `docker run` có thêm thời gian khởi động riêng; quá giới hạn ngoài là `INFRA`, không phải `TLE`. Mỗi container được đặt tên/nhãn riêng, và khi Docker CLI timeout, worker cố xóa chính container đó bằng `docker rm -f`. Điều này ngăn leak ở các lần chấm mới; container cũ trước bản sửa cần kiểm kê khi Docker engine hoạt động trở lại.
