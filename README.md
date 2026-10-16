# Final Testcase Generator

Một lệnh Python xử lý **một bài**: backend LLM được chọn sinh code AC/WA ứng viên và input, hai reference độc lập kiểm tra expected output, Docker chấm các ứng viên; thêm `--oracle` để trích tối đa 100 CodeNet Accepted + 100 Wrong Answer từ VPS rồi chấm bằng cùng bộ test. Mỗi vòng ghi báo cáo riêng vào `output/` (tối đa 3 vòng). CodeNet/LLM labels là nhãn ban đầu, không mặc nhiên là chân lý.

## Cài nhanh

```powershell
git clone https://github.com/ktoxz/CPTestcaseGenerator.git
cd CPTestcaseGenerator
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Trên Windows cần Docker Desktop chạy Linux containers. Với Ollama, khởi động
server và tải model ghi trong `config/pipeline.json` trước khi sinh test. Không
commit API key, token, output chạy hoặc virtual environment; các đường dẫn này
đã được loại qua `.gitignore`.

## Batch 50 bài trên máy KHOI

Script [`scripts/run_khoi_50.ps1`](scripts/run_khoi_50.ps1) chạy cohort cố định
gồm 25 bài Codeforces và 25 bài CodeNet có statement cùng oracle bundle. Sau khi
clone/pull repository và chép các thư mục `oracle` (chúng không được lưu trên
Git), chạy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File scripts\run_khoi_50.ps1
```

Có thể giảm chi phí cho lần thử đầu bằng
`-Iterations 1 -CasesPerRound 5 -OracleLimit 10`, hoặc truyền cờ CLI bổ sung ở
cuối lệnh, ví dụ `--ollama-timeout 300`. Kết quả từng bài nằm trong `output/`,
còn báo cáo tổng batch nằm trong `output/batches/<timestamp>/batch-report.json`.

## Yêu cầu

- Python ≥ 3.12 trên máy chạy lệnh; cài dependency bằng
  `python -m pip install -r requirements.txt`. Pydantic được dùng để sinh và
  validate JSON Schema cho test model.
- Mặc định: Ollama đang chạy và có model `gemma4:31b-cloud`. Toàn bộ tác vụ LLM dùng Gemma và provider fallback bị tắt. Claude Code CLI chỉ cần đăng nhập khi chủ động dùng `--model claude`, `--code-model claude` hoặc bật `--llm-fallback`.
- Docker **Linux engine** chạy được trên máy local hoặc KHOI. Mặc định `--judge auto`: thử local trước rồi SSH tới KHOI nếu local lỗi. Không chạy code submission ngoài container.
- Với `--oracle`: pipeline ưu tiên `--oracle-cache`, sau đó tự tìm `data/problems/<id>/oracle/manifest.json`. Vì vậy các ID như `cf2275d` dùng được khi đã có bundle local. Chỉ khi không có cache local, pipeline mới tải CodeNet từ VPS và khi đó ID bắt buộc có dạng `pNNNNN`; điều kiện này được kiểm tra trước Docker/LLM. Nhánh tải remote cần SSH key tới `ktoxz`, `scp`, Internet từ VPS để `pip` cài `pyarrow` vào venv tạm trong `/tmp`. Kho parquet mặc định `/srv/guidelet/staging/codenet`; pipeline không tải toàn bộ kho.

## Chạy

Trong thư mục này:

### Kaggle smoke test

Kaggle không có Docker daemon lồng nhau theo luồng chạy hiện tại của dự án.
Repository có thêm backend `--judge native` dành cho **smoke test trên Linux**,
hai preset nhẹ trong `config/kaggle.*.json`, preflight và notebook mẫu tại
[`kaggle/kaggle_smoke.ipynb`](kaggle/kaggle_smoke.ipynb). Native judge đặt
timeout/rlimit và xóa environment trước khi chạy submission, nhưng không cách
ly filesystem/network; vì vậy bắt buộc truyền `--allow-unsafe-native-judge` và
không dùng backend này cho code/đề không tin cậy hay số đo cuối. Xem hướng dẫn
đầy đủ ở [`kaggle/README.md`](kaggle/README.md).

### Chuẩn bị và dịch đề

`scripts/prepare_statement.py` nhận một đề Markdown hoặc cả thư mục bài. Công cụ
đọc metadata từ `metadata.json` hay phần đầu của đề, tự nhận diện ngôn ngữ, và
dùng Ollama để dịch đề không phải tiếng Anh. Mặc định lấy model và URL từ
`config/pipeline.json` (`gemma4:31b-cloud`). Nội dung đề luôn được coi là dữ
liệu không tin cậy; các code block mẫu phải được model giữ nguyên từng byte.

```powershell
python scripts/prepare_statement.py `
  --statement path\to\p00004\statement.md `
  --metadata path\to\p00004\metadata.json `
  --output data\problems\p00004

python scripts/prepare_statement.py `
  --input-root path\to\codenet-even-20\problems `
  --output-root data\problems
```

Mỗi bài xuất `statement.md` với header chuẩn (CodeNet ID, dataset, time/memory
limit), `metadata.json`, các hình được tham chiếu và, nếu có dịch,
`statement.original.md`. Dùng `--target-language Vietnamese` nếu cần tiếng
Việt, `--translate never` để chỉ chuẩn hóa/copy, và `--force` để ghi đè các
file đã được công cụ tạo. Công cụ không tự sinh `checker.json` hoặc
`validator.py`; hai file này cần được xác định và kiểm toán riêng theo đề.

Với `--model ollama --code-model claude`, Claude chỉ sinh code AC/WA (kể cả mutant thay thế). Ollama sinh validator, phân tích, witness và testcase; chế độ này không fallback các tác vụ đó sang Claude. `--claude-max-tokens` mặc định 32768 và `--claude-timeout` mặc định 300 giây/request.

```powershell
python main.py --problem p00004
python main.py --problem p00004 --model claude
python main.py --problem cf1949b --oracle --oracle-limit 20 --model ollama --code-model claude --claude-max-tokens 32768 --claude-timeout 300
python main.py --problem p00004 --model claude --claude-model sonnet --claude-effort low
python main.py --problem p00004 --ollama-model gemma4:31b-cloud
python main.py --problem p00004 --ollama-timeout 30 --ollama-max-tokens 16384
python main.py --problem p00004 --llm-timeout 50
python main.py --problem p00004 --oracle --oracle-limit 10
python main.py --problem p00005 --oracle --oracle-limit 100 --iterations 3
python main.py --problem p00005 --oracle --oracle-limit 20 --judge remote --resume-oracle output/p00005/20261007-190945
python main.py --problem p00005 --judge remote
```

Chạy nhiều bài tuần tự trong một lệnh (chỉ lấy các thư mục `pNNNNN` có
`statement.md` trong khoảng, tiếp tục bài kế tiếp nếu một bài lỗi):

```powershell
python main.py --problem-range p02580 p03862 --oracle --llm-timeout 300
python main.py --problems p02580 p02661 p02685 --oracle --llm-timeout 300
```

Mỗi batch ghi output riêng của từng bài, log và `batch-report.json` vào
`output/batches/<timestamp>/`. Thêm `--batch-fail-fast` nếu muốn dừng ngay ở lỗi
đầu tiên; `--output <path>` có thể dùng để chọn thư mục gốc của batch.

Lệnh mặc định sinh 3 AC, 5 WA. Trước khi tính TNR, pipeline ưu tiên WA vượt toàn bộ sample chính thức, tự cung cấp witness hợp lệ, được validator chấp nhận, có ít nhất hai AC reference thống nhất expected và tạo cùng một output sai hoặc RE/TLE trong hai lần chạy độc lập. Consensus dừng sau cặp reference đầu tiên nếu chúng đồng ý; nếu cặp đầu bất đồng, pipeline chạy toàn bộ pool để giữ quy tắc chọn reference ổn định. Nếu pool vẫn thiếu mức tối thiểu, WA sai ngay trên sample chính thức chỉ được giữ làm dự phòng sau khi tái hiện cùng lỗi ổn định trong hai lần chạy mới; loại này được ghi rõ là `official_sample_fallback`, không bị nhập nhằng với mutant khó vượt sample. Mutant tương đương, lỗi không ổn định, CE và INFRA luôn bị loại. Ollama sinh mutant thay thế tối đa 4 vòng mặc định; đổi bằng `--mutant-replacement-rounds 0|1|2|3|4`. Mỗi vòng chỉ lấp phần còn thiếu và pipeline ngừng gọi LLM ngay khi mutant khó cộng dự phòng đã đủ pool tối thiểu; hệ số đề xuất mặc định 1.5 bù cho proposal trùng hoặc không hợp lệ. Mỗi nhiệm vụ sinh mutant gửi AC ngắn nhất một lần và yêu cầu cả batch mutant còn thiếu; witness của các mutant cùng chế độ sửa cũng được gom vào một prompt. Nếu cả hai tầng chứng nhận vẫn không đạt số mutant tối thiểu sau toàn bộ ngân sách replacement thì run mới dừng; nếu đạt tối thiểu nhưng thiếu quota yêu cầu, run tiếp tục và ghi rõ pool thiếu thay vì vứt bỏ toàn bộ thời gian đã chạy.

Trước khi nhìn vào candidate, pipeline gọi backend LLM đã chọn riêng để tạo `test-model.json`: grammar, constraints, quan hệ, output partition, fault model và các coverage obligation thuộc equivalence/boundary/decision/pairwise/domain/sequence/scenario/output/stress/format/fault. Khi dùng Ollama, Pydantic sinh JSON Schema và schema này được truyền thẳng qua `format`; response còn được Pydantic validate trước khi normalize. Bản phân tích này được tái sử dụng khi sinh code, thay vì gọi LLM lần thứ hai để phân tích lại cùng một đề. Vòng đầu chỉ nhận statement + test model để tạo baseline, không nhận source mutant, execution hay CodeNet. Các vòng sau mới là adaptive, vừa nhắm survivor vừa lấp coverage gap.

`--cases-per-round 10` là quota **test được chấp nhận**, không phải số đề xuất. Quota động vẫn có thể tăng theo survivor, thiếu TNR, coverage critical chưa đạt, số input trùng/bị từ chối và số vòng đứng yên. Mỗi phase baseline, adaptive hoặc top-up dùng một prompt để sinh cả batch cần thiết; AC, mutant, audit và sửa input cũng được gom theo nhiệm vụ thay vì tách một request cho từng item. Nếu validator, reference hoặc dedup làm thiếu quota, pipeline gọi top-up tối đa 1 lần mặc định. Feedback vòng sau chỉ gửi source survivor cần thiết, các attempt gần nhất và lịch sử testcase đã rút gọn; output/chuỗi evidence dài được giới hạn trước khi đưa lại vào prompt.

Validator kiểm tra hết các đề xuất trong batch trước. Mọi input bị từ chối ở cùng một lượt được gom vào một request sửa chung; pipeline không gọi LLM tuần tự cho từng testcase. Sau khi sửa, chỉ nhóm còn bị từ chối mới đi vào request batch của lượt kế tiếp.

Mặc định không dừng chỉ vì TPR/TNR ≥0.90. Dừng sớm cần đồng thời: ít nhất 2 vòng, ít nhất 18 testcase, 100% critical obligations, 90% normal obligations, TPR/TNR development ≥0.90 và không còn survivor hoặc hai vòng không có coverage/kill mới. Có thể đổi sàn bằng `--min-iterations`, `--min-total-cases`, và số top-up bằng `--top-up-rounds`. Tối đa vẫn là `--iterations`.

Không truyền `--model` thì mọi tác vụ dùng `gemma4:31b-cloud` và không chuyển sang Nemotron hay Claude. Mỗi request Ollama có hard-timeout riêng 120 giây theo cấu hình hiện tại, đổi bằng `--ollama-timeout`; khi Gemma lỗi, tác vụ tùy chọn được bỏ qua còn tác vụ bắt buộc để sinh AC/WA hoặc validator dừng rõ ràng. Có thể chủ động bật lại chuỗi provider bằng `--llm-fallback` và chọn model Ollama thứ hai qua `--ollama-fallback-model`; Claude chỉ được thêm vào cuối chuỗi khi code backend không được tách riêng bằng `--code-model claude`. Request timeout không được gửi lại ngay trên cùng endpoint. Sau mỗi response Ollama hoàn tất, pipeline chờ 1 giây trước request Ollama kế tiếp (`--ollama-throttle`); sau timeout endpoint được cách ly theo `--ollama-timeout-cooldown`. Pipeline không tạo worker LLM: một prompt đảm nhiệm trọn một nhiệm vụ và trả về mảng kết quả của nhiệm vụ đó.

Dùng `--model claude` để chỉ gọi Claude Code CLI bằng phiên đăng nhập hiện có, hoặc `--model chatgpt` để chỉ gọi Codex CLI qua phiên ChatGPT hiện có; hai chế độ chọn trực tiếp này không chạy chuỗi fallback Ollama. Claude được ghim mặc định ở `fable` với `--claude-effort low`, tránh để CLI tự chọn model suy luận lâu. `--claude-model sonnet` đổi sang model mạnh hơn khi ưu tiên chất lượng hơn thời gian; `--claude-effort low|medium|high|xhigh|max` điều chỉnh thời gian suy luận. Ngoài ra có thể chọn `--ac`, `--wa`, `--cases-per-round`, `--min-iterations`, `--min-total-cases`, `--top-up-rounds`, `--input-repair-attempts`, `--mutant-replacement-rounds`, `--ollama-url`, `--statement` và `--output`. `--judge local|remote|auto` chọn nơi chấm; `--judge-host` ghi đè SSH host fallback KHOI. Hai đề mẫu tải từ VPS nằm ở `data/problems/p00004` và `data/problems/p00005`. Nếu đề khác, đặt `data/problems/pNNNNN/statement.md` và (khuyến nghị) `checker.json` trước khi chạy.

Dùng `--model llama-server` để gọi API OpenAI-compatible tại `--llama-server-url` (mặc định `http://localhost:8080`) với model `--llama-server-model`. Chế độ này gọi trực tiếp một backend, không chạy chuỗi fallback Ollama/Claude. Mỗi request có timeout riêng theo `--llm-timeout`; output batch được phép tới `--llama-server-max-tokens` (mặc định 8192).

Terminal hiển thị tiến độ theo giai đoạn, số code/test đã xử lý, verdict từng code và TPR/TNR sau mỗi vòng. Mỗi response nguyên văn của backend LLM cũng được in giữa marker `LLM OUTPUT BEGIN/END`, kèm tên tác vụ, model, lần thử JSON và số ký tự; response lỗi cú pháp trước khi retry cũng được in đầy đủ. Các bước lâu như inference, tải CodeNet và build image in nhịp trạng thái mỗi 15 giây. Mỗi công đoạn nhỏ còn có dòng `LATENCY` theo mili giây: từng request/parse/log output LLM, từng compile, batch chạy Docker, reference consensus, mutant certification, pool judge và từng bước SSH/export CodeNet. Toàn bộ tiến độ và output LLM ghi ra stderr, JSON tóm tắt cuối cùng vẫn ở stdout; không cần thêm cờ CLI.

Với Ollama, response gốc của từng attempt còn được lưu trong `llm-raw/`. Trước khi gọi model sửa lại, parser tự xử lý Markdown fence, phần giải thích thừa trước/sau JSON, control character chưa escape, trailing comma và root array ở các tác vụ có thể suy ra key. Kết quả sau đó phải có đủ key và đúng kiểu tối thiểu theo từng tác vụ; JSON đúng cú pháp nhưng sai cấu trúc cũng bị từ chối. Chỉ lỗi không thể sửa cục bộ mới tiêu tốn thêm một request repair với temperature 0; tổng cộng tối đa hai attempt JSON trên mỗi Ollama backend.

Lỗi `INFRA` ở bước kết nối KHOI hoặc lúc compile/chạy sẽ được thử lại tối đa 3 lần (chờ 2 giây, rồi 4 giây; chỉnh trong `config/judge.json`). Nếu vẫn `INFRA`, run dừng và giữ output đã có để kiểm tra, **không tính TPR/TNR trên kết quả chấm thiếu**. Verdict của code như `CE`, `WA`, `RE`, `TLE` không retry. Lỗi build image trong bước chuẩn bị được báo riêng, không coi là verdict của submission.

Nếu run đã xong các vòng LLM nhưng dừng ở phần CodeNet, dùng `--resume-oracle <output cũ>` cùng `--problem ... --oracle`. Lệnh này đọc lại testcase đã chứng nhận và `iteration-*.json`, ưu tiên `oracle/manifest.json` đã tải, không gọi Ollama hoặc xuất lại CodeNet. `report.json` được ghi ngay sau phần LLM và cập nhật khi CodeNet hoàn tất. Mỗi batch tối đa `batch_size` testcase (mặc định 8 trong `config/judge.json`) đi qua một phiên SSH; từng testcase vẫn có container và timeout riêng. Kết quả code–test đã chạy được tái dùng trong cùng run, tránh chấm lại qua các vòng sinh test.

Giới hạn `run_timeout_seconds` áp dụng **bên trong container** cho code; thời gian Docker tạo container có khoảng chờ riêng `docker_startup_grace_seconds`. Nếu chính lệnh Docker vượt giới hạn ngoài, judge trả `INFRA`, thử `docker rm -f` đúng container vừa tạo rồi mới retry; không gán nhầm thành `TLE`. Container mới có nhãn `testgen.owner=Final_TestcaseGenerator` và `testgen.run=<id>` để kiểm kê an toàn. Không dùng `docker system prune` để xử lý container cũ không rõ chủ sở hữu.

Remote judge cần SSH key tới KHOI, Python và Docker Desktop **Linux engine đang chạy trên KHOI**. Source được truyền qua SSH; Docker trên KHOI compile/chạy trong container, kết quả và báo cáo vẫn lưu local. Nếu cả hai Docker engine đều không sẵn sàng, chương trình dừng trước khi sinh code/test và báo lỗi hạ tầng; không tính thành WA. Không tự khởi động Docker Desktop hoặc sửa disk. Worker và build tạm trên KHOI nằm trong `%TEMP%/testgen-remote-judge/`.

Nếu báo thiếu pipe `dockerDesktopLinuxEngine`, trên KHOI hãy mở Docker Desktop (hoặc chạy tác vụ có sẵn `schtasks /run /tn CodeNet-Start-Docker`) rồi kiểm tra `docker info` trước khi chạy lại. Docker trong Ubuntu WSL của KHOI không phải backend của worker Windows này; nếu WSL báo filesystem read-only thì không dùng nó làm máy chấm khi chưa sửa ổ.

Trên Windows nên dùng Docker Desktop Linux engine. Nếu chạy trong WSL, dùng Python và Docker trong cùng distro; đặt `--ollama-url` tới endpoint Ollama mà WSL truy cập được. Không coi `ollama list` trên Windows là bằng chứng WSL truy cập được endpoint.

Nếu Ollama Windows chỉ bind `127.0.0.1`, có thể chạy `scripts/ollama_bridge.py --bind <Windows-vEthernet-IP> --allow <WSL-IP>` trên Windows rồi truyền `--ollama-url http://<Windows-vEthernet-IP>:11435` khi chạy trong WSL. Bridge chỉ nhận `/api/chat` từ IP WSL đã chỉ định; tắt process sau khi chạy. Nếu đã tải pool oracle trên Windows, WSL có thể dùng `--oracle --oracle-cache /mnt/d/.../data/problems/p00004/oracle` để không SSH lần nữa.

Trên cấu hình local đã thử, Docker daemon hoạt động trong Ubuntu WSL khi chạy bằng root. Có thể dùng quy trình thực tế sau (điền đúng IP gateway và IP WSL hiện tại):

```powershell
wsl -d Ubuntu -u root -- systemctl start docker
python scripts/fetch_oracle.py --problem p00004 --limit 100
# Chạy scripts/ollama_bridge.py trên Windows với --bind <gateway> --allow <WSL-IP>.
wsl -d Ubuntu -u root -- python3 /mnt/d/KLTN/Final_TestcaseGenerator/main.py --problem p00004 --oracle --oracle-limit 100 --oracle-cache /mnt/d/KLTN/Final_TestcaseGenerator/data/problems/p00004/oracle --ollama-url http://<gateway>:11435
```

Lệnh `fetch_oracle.py` tải source qua SSH từ VPS, có thể chạy lại cho p00005. Để chấm thuần Windows, bật Docker Desktop Linux engine và dùng trực tiếp `python main.py --problem ... --oracle`.

Chạy kiểm thử không cần LLM/Docker:

```powershell
python -m unittest discover -s tests -v
```

## Cấu hình và mở rộng

- `config/pipeline.json`: model/URL Ollama, model/effort Claude, số code/test mặc định, và checker mặc định.
- `config/oracle.json`: SSH host, parquet root, phiên bản pyarrow và giới hạn AC/WA.
- `config/judge.json`: chế độ chọn judge, concurrency và SSH host fallback KHOI
  (độc lập với host CodeNet oracle); có thể chọn preset khác bằng
  `--judge-config`.
- `config/runtimes.json`: image, Dockerfile, đuôi file, dialect, lệnh compile/chạy và danh sách ngôn ngữ cho Ollama. `config/sandbox.json`: tài nguyên/timeout.
- `data/problems/<id>/checker.json`: profile checker riêng cho từng bài. Nếu không có, dùng `default_checker` của `config/pipeline.json`.

Thêm kiểu chấm mới: tạo một module trong `testgen/checkers/` có class kế thừa `Checker`, định nghĩa `kind` và `accepts()`, gắn `@register_checker`. Plugin được tự phát hiện; không sửa `main.py`, `pipeline.py` hoặc chuỗi nhánh trong `checker.py`. Ví dụ profile: `{"kind":"FLOAT","epsilon":0.0005,"decimal_places":3,"values_per_line":2}`. Thêm dialect/ngôn ngữ: thêm một entry vào `config/runtimes.json` và bảo đảm Dockerfile của image có compiler/runtime đó; generator, judge và exporter cùng đọc catalog. Có thể chọn file khác bằng `--runtime-config`.

## Kết quả

Mỗi run ở `output/<problem>/<timestamp>/` chứa `test-model.json`, `generated/` (source ứng viên, validator, response JSON, reference/mutant certification), `context/candidates/*.json`, `context/audits/*.json`, `build/`, `tests/`, `refinement/feedback-*.json`, plan ban đầu và plan top-up, `iteration-0.json`…, `test-suite.lock.json`, `latency.jsonl` và `report.json`. `latency.jsonl` được append ngay trong lúc chạy nên vẫn dùng được khi tiến trình bị ngắt; `report.json.latency.summary` tổng hợp count/total/avg/p50/p95/max theo component. `executions-llm.jsonl` chỉ chứa development candidates. Khi đủ ít nhất 5 mutant, một phần được giữ kín khỏi prompt và chỉ chấm sau suite lock; kết quả nằm trong `executions-holdout.jsonl` và `llm_holdout_metrics`. Khi bật `--oracle`, `oracle/` chứa pool CodeNet và `oracle/executions.jsonl` riêng.

CodeNet oracle là tập đánh giá ngoài: chỉ được tải/chấm sau khi mọi vòng LLM hoàn tất và hash của bộ test đã ghi vào `test-suite.lock.json`. Kết quả hay source oracle không đi vào prompt sinh test, feedback hoặc cơ chế sửa input. Pipeline kiểm tra lại hash trước và sau khi chấm oracle; đây là ranh giới bắt buộc để tránh rò rỉ giữa hai nhánh thực nghiệm.

`tpr_label_based` và `tnr_label_based` là tỷ lệ **theo nhãn hiện có**, không phải metric đã xác minh hoàn toàn. `CE` và `INFRA` tách riêng, không được tính là WA bị phát hiện. Các ca tham chiếu bất đồng hoặc validator từ chối được cách ly trong `quarantined`. Đọc [Specs.md](Specs.md) trước khi dùng tỷ lệ này để kết luận chất lượng testcase.

## Trạng thái kiểm thử bàn giao

Unit tests cho checker, sample parser, validator, orchestration và CE isolation đã chạy. Docker smoke p00005 với một source AC và một source WA đã chạy thành công trong Ubuntu WSL local. Việc chấm end-to-end phụ thuộc Docker Linux engine và Ollama có thể truy cập từ cùng môi trường; kiểm tra từng môi trường bằng `docker info` và `/api/tags` trước khi chạy thực tế. Không có tuyên bố TPR/TNR ≥90% nếu chưa chạy và rà lại nhãn.

Một run nhỏ p00004 đã được thử end-to-end với 2 AC + 2 WA do Ollama sinh và 2 Accepted + 2 Wrong Answer lấy từ VPS: 4 testcase, LLM label-based TPR 2/2, TNR 1/2; CodeNet sample TPR 2/2, TNR 2/2. File nằm ở `output/p00004/smoke-oracle/`. **Mẫu 2+2 quá nhỏ để xác nhận ngưỡng 90%** và chưa thay thế run 100+100/3 vòng.


### Latency tạo testcase

Mục tiêu đo là 180 giây, tính từ lúc vào CLI (gồm thiết lập judge) đến khi ghi bộ
case đã chứng nhận và đánh giá holdout, trước bước oracle ngoài tùy chọn.
`report.json` ghi `generation_latency.elapsed_seconds`, `target_met` và
`quality_criteria_met` riêng: nhanh không đồng nghĩa đạt đủ chất lượng.

Gemma4 mặc định timeout 120 giây/request, cooldown thành công 1 giây, cooldown
sau timeout 10 giây, tối đa 16384 token (`--ollama-max-tokens`). Cleanup HTTP
không chặn luồng timeout. Test lớn dùng `input_parts` (literal, lặp hoặc dãy số)
được mở rộng có giới hạn tại máy; không chạy mã từ recipe. Mutant dùng
`code_edits` thay thế chuỗi duy nhất trên AC đã xác nhận; vẫn phải qua biên dịch,
sample và witness. Validator và reference consensus chạy theo batch; top-up,
repair và audit cũng được gom batch để giảm số lượt LLM/SSH.


Kết quả kiểm chứng ngày 2026-10-11 trên `p03274`:
`output/p03274/latency180-v3/report.json` ghi 169.390 giây, 18 testcase,
TPR/TNR trên pool LLM 1.0/1.0, coverage khai báo 11/11, đầy đủ tiêu chí dừng.
Bộ này có test N=100000; kiểm tra độc lập theo thuật toán Candles xác nhận
input và expected output của cả 18 case. Đây là số đo thực nghiệm với
Ollama cloud và remote Docker judge đã cấu hình, không phải bảo đảm latency
cho mọi bài hoặc khi backend mạng/cloud lỗi. Chưa bao gồm đánh giá CodeNet oracle.

Lần xác nhận bản cuối: `output/p03274/latency180-confirmed/report.json`,
125.922 giây, 24 testcase, coverage 11/11, đạt đủ tiêu chí chất lượng.
`verification.json` lưu kết quả kiểm tra độc lập 24/24 input và expected output.
