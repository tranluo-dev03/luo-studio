# LUO Studio

Ứng dụng desktop gen video nhiều cảnh bằng LUO-API. Thay `gen_video.py` + chế độ 2b của extension, nhưng vẫn dùng LUO-API (phải đang chạy).

## Chạy
Nhấp đúp **run.bat** (hoặc `python app.py`). Mở cửa sổ ứng dụng riêng (Edge/Chrome ở chế độ app). Thoát bằng cách đóng cửa sổ.

## Quy trình
1. **Dự án** → tạo hoặc mở dự án; chọn **loại dự án** (script + bảng trường). Có sẵn 2 loại: điện thoại + người học, chia đôi 2 nhân vật.
2. Mỗi **biến thể** = một video: điền các trường (nhân vật, bối cảnh, giọng…) và lời thoại. Điền nhanh bằng nút **Từ file** (xem dưới).
3. Tick các biến thể → **Chạy**. Mỗi cảnh: ảnh khung đầu → video → **tự cắt đuôi, giữ khung ít chuyển động nhất** → khung cuối đó là khung đầu cảnh sau.
4. Xong → **Hậu kỳ**: phụ đề màu tự tạo từ lời thoại, logo, end card → `final.mp4`.
5. **Kết quả**: xem, xuất lại, mở thư mục.

## Giọng, biểu cảm và độ dài clip
- Mỗi lượt có ô **cảm xúc** (gợi ý sẵn, ví dụ `surprised, excited`). Cảm xúc được đổi thành chỉ dẫn cụ thể cho nét mặt và giọng (lông mày, ánh mắt, cao độ giọng…) trong prompt. Không điền thì tự suy từ dấu câu: `?` tò mò, `!` hào hứng, `...` ngập ngừng.
- Prompt yêu cầu giọng như người nói chuyện tự nhiên (không giống đọc máy/TTS), nhân vật robot vẫn có khuôn mặt biểu cảm như người. Sửa câu chữ ở `..\production\prompt_parts.py` rồi chạy `gen_turns_script.py` / `gen_phone_script.py` và chép script mới vào `templates\`; loại có sẵn tự cập nhật khi mở app.
- Muse luôn trả đủ độ dài đã xin và hay kéo giãn lời cho đủ. App xin độ dài ngắn nhất đủ nói (5/6/8/10s theo số âm tiết), cắt đuôi sau lời nói, và nếu lời nói chậm hơn tự nhiên thì **tăng tốc tối đa ×1,35** (Cài đặt, mục Gen video). Khung cuối không đổi nên vẫn nối đúng clip sau.

## Điền từ file hoặc bảng (nút **Từ file** cạnh danh sách biến thể)
Chọn file CSV, XLSX hoặc JSON, hoặc dán bảng từ Excel/Google Sheets (dòng đầu là tên cột). App tự khớp cột với trường (theo tên token hoặc nhãn), bạn chỉnh lại nếu cần, rồi chọn:
- **Ghép dòng với biến thể**: theo tên (cột Tên) hoặc theo thứ tự dòng.
- **Ô đã có chữ**: giữ nguyên (chỉ điền ô trống) hoặc ghi đè.
- **Dòng không khớp**: thêm biến thể mới hoặc bỏ qua.
Có dòng xem trước số ô sẽ được điền. **Tải bảng mẫu** xuất CSV đúng cột của dự án để điền trong Excel rồi nạp lại.

## Thêm loại dự án mới (menu **Loại dự án**, hoặc "Loại mới" khi tạo dự án)
1. **Script**: tải file .txt (hoặc dán). Script là văn bản dạng `[STYLE LOCK]: … CẢNH 1 (0:00–0:05): …` (định dạng như `templates\*.txt`), phần thay đổi viết `{{TOKEN}}`. App tự đọc: số cảnh, các token, và các **chuỗi** `KEY_1, KEY_2…` (ví dụ `CAU_1..CAU_3` thành danh sách câu; `LUOT_1..LUOT_n` thành bảng lời thoại có người nói, cảm xúc, màu phụ đề).
2. **Bảng trường**: mỗi token là một ô trong form biến thể. Đặt nhãn, nhóm (người dạy, người học, bối cảnh, khác), ô ngắn/dài, gợi ý, bắt buộc hay không. Nhập nhanh bằng CSV (cột `key, label, group, kind, placeholder, default, required`).
3. **Danh sách biến thể** (tuỳ chọn): JSON `[{"name": "...", "TOKEN": "..."}]` hoặc CSV (dòng đầu = key hoặc nhãn trường); tạo luôn dự án đầu tiên.
4. Sửa hoặc nhân bản loại bất kỳ ở menu Loại dự án; chỉ xoá được khi chưa có dự án nào dùng. Mẫu: `dev\sample-script-ke-chuyen.txt`.

## Cài đặt
- Địa chỉ LUO-API và khoá (để trống khoá = dùng `MUSE2API_KEY` trong `luo-muse-api\.env`).
- Logo / end card mặc định, số lần thử lại, thời gian chờ.

## File
| | |
|---|---|
| `engine.py` | Gen + cắt thông minh + ghép + đọc script |
| `server.py` | Máy chủ cục bộ, quản lý loại, dự án, tác vụ |
| `ui\` | Giao diện |
| `templates\` | Script có sẵn |
| `data\` | `types`, `projects`, `runs\<dự án>\<biến thể>\`, cài đặt |
| `dev\mock_api.py` | API giả lập Muse để thử không tốn credit: `python dev\mock_api.py`, rồi đặt địa chỉ API `http://127.0.0.1:18699` |
| `dev\make_logo.py` | Đổi logo: `python dev\make_logo.py anh.png` |

Phụ thuộc thư mục `..\production` (`gen_video.py`, `postprocess.py`, `make_variants.py`, `prompt_parts.py`): giữ hai thư mục cạnh nhau.

## Cập nhật mới
- **Hàng đợi**: nút "Thêm vào hàng đợi" ở dự án; sang tab Hàng đợi tick và Bắt đầu. Thẻ gom theo dự án, bấm thẻ để xem từng cảnh; có đồng hồ thời gian mỗi video và tổng.
- **Cảm xúc**: mỗi lượt thoại có cảm xúc người nói và phản ứng người nghe.
- **Màu**: khung hình trích bằng swscale chính xác + chuẩn hoá độ sáng theo clip đầu, hết hiện tượng tối dần.
- **Nói chồng**: prompt khoá một giọng; Cài đặt "Chống 2 nhân vật cùng nói" chỉ nghe lại và ghi cảnh báo (không tự gen lại).
- **Đính kèm theo token**: dưới mỗi ô có "Ảnh / mp3". Ảnh vào ảnh tham chiếu bước tạo ảnh (kèm chú thích theo tên ô); mp3 vào `reference_audios` bước video cho cảnh mà bên đó nói. Muse có thể bỏ qua tham chiếu.
