# Lịch sử phiên bản LUO Studio

Số phiên bản theo dạng `x.y.z` (semantic versioning): `x` đổi khi có thay đổi không tương thích, `y` khi thêm tính năng, `z` khi chỉ sửa lỗi.
Nguồn sự thật của số phiên bản: dòng đầu của `version.txt` (cũng là tag git `vx.y.z` và `AppVer` trong `release-tools/installer.iss`; ba nơi phải khớp nhau khi phát hành).

## [Chưa phát hành]

### Thêm
- **Hiện tài khoản Muse đang gen video/cảnh:** LUO-API trả thêm `account` (id) và `account_label` (tên gợi nhớ, không lộ cookie) ngay khi task nhận được tài khoản (kể cả khi tự chuyển tài khoản dự phòng); Studio lưu vào `account` của từng cảnh trong hàng đợi, ghi nhật ký "Cảnh N: gen bằng tài khoản X", hiện trên thẻ video (tài khoản của cảnh đang chạy) và trên từng thẻ cảnh.
- **Cập nhật không mất dữ liệu:** `update.ps1` và `Cap nhat.bat` (sao lưu nhẹ dữ liệu quan trọng vào `userdata-backup/`, `git pull` hoặc tải ZIP mới rồi chép đè, không đụng `userdata/`, `.venv`, `bin`; chạy lại `setup.ps1`). Có tuỳ chọn `-ZipFile` cho máy không có git hoặc mạng hạn chế.
- **`Chan doan.bat`** (`app/chan_doan.py`): kiểm tra máy (CPU có AVX không, máy ảo, Visual C++ Redistributable, phiên bản thư viện, thử nạp từng thư viện nhị phân trong tiến trình riêng) và lưu báo cáo vào `userdata\logs\chan-doan.txt`; `setup.ps1` cảnh báo sớm nếu thiếu Visual C++ Redistributable.
- `setup.ps1` tự cài Python 3.11 khi thiếu (winget, nếu không được thì bộ cài chính thức từ python.org).

### Sửa
- **Bấm Gen bị "mất kết nối API" (Studio chết giữa chừng):** máy có Microsoft Visual C++ Redistributable x64 cũ (< 14.40, vd. 14.29) làm ctranslate2/onnxruntime crash cứng trong `MSVCP140.dll`, mà Whisper khi Gen chạy ngay trong tiến trình Studio. Whisper khi Gen giờ chạy trong một tiến trình con riêng (nạp mô hình một lần, chết thì tự bật lại; cảnh đó cắt theo cách thường); `setup.ps1` kiểm tra phiên bản file DLL và tự tải + cài bản mới (hỏi UAC); trình khởi động cảnh báo khi phát hiện bản cũ; `Chan doan.bat` báo "QUÁ CŨ" và in `crash.log` (stack Python lúc crash, ghi bằng `faulthandler`).
- **Tiến trình treo từ các lần mở trước tranh chấp cổng:** trình khởi động đưa mình vào Job Object "tắt cùng nhau" nên LUO-API, trình duyệt con, Whisper chết theo kể cả khi crash; lúc mở thì dọn trình khởi động/LUO-API cũ ghi trong `running.json` và LUO-API mồ côi của bất kỳ bản cài nào. `setup.ps1` tắt tiến trình đang chạy từ `.venv` của thư mục trước khi cài thư viện (tránh "Access is denied").
- **`setup.ps1` báo "No module named venv":** chọn nhầm Python embeddable (bản rút gọn, không có venv/pip). Giờ chỉ chọn Python có `venv` + `ensurepip`, và thay `Sort-Object` (PowerShell 5.1 không giữ thứ tự phần tử bằng nhau, nhiều Python cùng 3.12 thì chọn ngẫu nhiên) bằng chọn tuần tự ổn định.
- `setup.ps1` cảnh báo trước thư mục cài có dấu / trong OneDrive / quá dài / ổ đĩa còn dưới 5 GB, và gỡ dấu "tải từ Internet" khỏi file (SmartScreen chặn `.bat`).
- **Hậu kỳ không còn chết khi thư viện nhận dạng giọng hỏng cứng** (lỗi "Hậu kỳ lỗi, xem nhật ký" sau cảnh báo `pkg_resources`, mã thoát `0xC0000005`, gặp trên một số máy): Whisper giờ chạy trong tiến trình con; thử có VAD trước, nếu VAD hỏng thì tự chuyển sang không VAD (nhớ lại để lần sau bỏ qua), nếu cả Whisper hỏng thì vẫn ra video với phụ đề ước lượng kèm cảnh báo. Chất lượng căn phụ đề trên máy chạy được VAD giữ nguyên.
- **Phụ đề lệch tiếng nói ở video trộn tiếng Tây Ban Nha + tiếng Anh:** Whisper chỉ đoán ngôn ngữ MỘT lần cho cả video nên bỏ sót hoặc nghe sai các câu ngắn của ngôn ngữ còn lại, rồi cách gán tuần tự trên cả video làm các câu sau bị dồn cục và chồng lấn (đã tái hiện: ép sai ngôn ngữ thì 8/11 dòng không khớp). Hậu kỳ giờ căn phụ đề theo từng cảnh: mỗi cảnh được nhận dạng riêng (tự nhận ngôn ngữ riêng, câu có ¿ ¡ ñ thì chốt tiếng Tây Ban Nha) và chỉ gán cho phụ đề của lượt thoại đó; cảnh Whisper không nghe thấy thì ước lượng trong khoảng của chính cảnh, không ảnh hưởng cảnh khác. Mốc từng cảnh trong `raw.mp4` được xác định bằng khớp âm thanh; điểm bắt đầu tiếng nói dò theo năng lượng âm thanh nên dòng đầu mỗi cảnh chính xác hơn cả cách cũ (cách cũ bị VAD đệm sớm 0,25–0,4 giây).
- **`setup.ps1` / `Cap nhat.bat` không nhận ra Python đã cài (rồi bộ cài báo lỗi 1603):** khi đã có `.venv` dùng được thì không còn đòi tìm Python hệ thống (đúng với lúc cập nhật); nếu cần tìm thì dò nhiều cách (py launcher, registry PEP 514 kể cả thư mục cài tuỳ ý, thư mục mặc định, PATH) và, nếu không thấy bản dùng được, liệt kê các Python đã thấy kèm lý do (3.13/3.14, 32-bit...). Bộ cài Python giờ cài song song, không sửa PATH, không cài py launcher (tránh xung đột gây lỗi 1603), ghi log và báo chi tiết khi lỗi; bỏ `winget` (lỗi nguồn `0x8a15000f`). Thêm `-CheckOnly` (chỉ kiểm tra Python) và `-PythonInstaller` (dùng bộ cài tải sẵn). `.venv` hỏng được báo rõ và tạo lại.
- **Kiểm tra miệng người nghe và tự gen lại là một công tắc trong Cài đặt**, tự kiểm tra máy có chạy được không: khi bật thì thử thật trong tiến trình riêng, nếu không khả dụng thì tự tắt và hiện lý do; lúc chạy video cũng kiểm tra và tự tắt (không báo lỗi lặp ở từng cảnh). Độ nhạy và số lần tự gen lại chỉ hiện khi công tắc bật.
- **Lỗi "No such file or directory ... sceneN_last.png"**: khi âm thanh của clip đã cắt dài hơn hình vài chục mili giây, `ffmpeg -sseof` nhảy tới mốc sau khung hình cuối, không ghi khung nào mà vẫn báo thành công. `grab_frame` giờ tính mốc theo thời lượng của luồng hình, kiểm tra file thật sự được ghi, thử lùi dần và cuối cùng giải mã hết để lấy khung cuối (đã thử trên 103 clip thật, trước đây 2 clip lỗi, nay 0).
- Cảnh báo "bỏ qua kiểm tra miệng ... DLL load failed" (mediapipe) nay kèm gợi ý nguyên nhân (thiếu Visual C++ Redistributable hoặc CPU/máy ảo không có AVX) và hướng dẫn chạy `Chan doan.bat`.
- Ghim `faster-whisper`, `ctranslate2`, `onnxruntime` đúng phiên bản đã chạy ổn trong `requirements.txt` để máy cài mới không bị trôi phiên bản.

### Đổi
- Tài liệu cài đặt (`README.md`, `HUONG-DAN.txt`): cài từ GitHub (ZIP hoặc git) bằng `setup.ps1`; bỏ hướng dẫn tắt/loại trừ chống virus.

## [1.1.0] - 2026-10-23

### Thêm
- **Nhân vật tổng quát:** mỗi nhân vật có khoá bất kỳ (không chỉ `day`/`hoc`) với các token `TEN_`, `NGUOI_`, `GIONG_`, `POS_`, `VAI_`, `NGHE_`, `EMO_`, `BOX_<khoá>`; số nhân vật bất kỳ, vị trí khuôn mặt tuỳ ý cho bộ đo miệng. Prompt của các loại dự án cũ giữ nguyên từng ký tự.
- **Cảnh không có lời thoại** (hành động, chuyển cảnh) không đòi tiếng, không cắt theo lời, không đo miệng.
- **`SAMPLE/phan-tich-video.py`:** phân tích video tham chiếu (tốc độ nói từng câu, cảnh cắt, chuyển động mạnh, ảnh ghép dày từng lượt).
- **`SAMPLE/HUONG-DAN-CHO-AGENT.md`:** hướng dẫn agent viết kịch bản và biến thể cho mọi thể loại, có quy trình phân tích video bắt buộc.
- Kịch bản và biến thể mẫu: cảnh sát và tài xế xe tải (`SAMPLE/Canh sat nu/`), xe tải và gia sư AI (`SAMPLE/Xe tai/`).
- Hiển thị số phiên bản ở thanh bên trái của giao diện.

### Sửa
- Clip Muse trả về không có tiếng: tự gen lại; nếu còn sót thì chèn im lặng khi ghép (trước đây lỗi `matches no streams`).
- Studio dùng đúng cổng LUO-API mà launcher đã bật khi cổng 18610 bị chiếm (trước đây lỗi "Không kết nối được LUO-API").
- Bộ đo miệng báo nhầm khi người nghe chỉ cười: thêm vùng khuôn mặt cho bố cục TOP/BOTTOM, tiêu chí há miệng rộng và nhịp mở-khép; hạ số lần tự gen lại mặc định từ 5 xuống 2.
- Bảng cảm xúc không còn chỉ dẫn cử chỉ tay/thân (gãi đầu, nhún vai) làm tư thế lệch lan sang các cảnh sau.

## [1.0.0] - 2026-10-21

- Bản mã nguồn đầu tiên, kèm script cài đặt; tách bước viết kịch bản từ video khỏi bước tạo biến thể trong prompt cho Claude; ghim `av>=14` để hậu kỳ mở được âm thanh.
