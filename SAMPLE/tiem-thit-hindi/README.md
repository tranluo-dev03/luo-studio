# Thể loại `tiem-thit-hindi`: tiệm thịt học tiếng Anh, lời Hindi xen tiếng Anh

Video mẫu: `0610_Cut meat ES_015_02.mp4` (177 s), CHÍNH là video của `tiem-thit-tieng-anh`; thể loại này là bản **Hindi** (mẹ đẻ Hindi thay Tây Ban Nha, bối cảnh Ấn Độ).
Khuôn, 50 cảnh (38 có lời + 12 không lời), góc máy, cảnh không lời: xem [../tiem-thit-tieng-anh/README.md](../tiem-thit-tieng-anh/README.md) và `PHAN-TICH-VIDEO-MAU.md` ở đó (đã đo lại 17/11/2026: 177 s, 65 câu, 28 cảnh cắt, 4,24 từ/giây, giọng 152/239 Hz, khớp phân tích cũ).
Code riêng: `app/production/types/tiem-thit-hindi/` (`post.py` chép từ tiem-thit-tieng-anh, `config.json` thêm `font: Nirmala UI` + `shaping: complex` cho chữ Devanagari).

## File
| File | Dùng làm gì |
|---|---|
| `cong-cu/tao_kich_ban.py` | import bảng cảnh của tiem-thit-tieng-anh, đổi Spanish -> Hindi, loại hậu kỳ -> `tiem-thit-hindi`; không sửa file thể loại gốc |
| `cong-cu/tao_bien_the.py` | 3 biến thể (bảng `BT`): `raju-tiem-thit-goc` (Raju/chú "चाचा", biến thể test), `kabir-tiem-thit-lucknow` (Kabir/"मामा"), `arjun-tiem-thit-delhi` (Arjun/"ताऊजी"); đổi tên, ngoại hình cậu bé + ông chú, nền chợ |
| `anh/TAVO_<A|B|C>.png`, `anh/TIO_<A|B|C>.png` | ảnh tham chiếu cần gen (CHƯA CÓ, xem dưới); KHACH, CHU, ROBOT dùng lại ảnh `tiem-thit-tieng-anh/anh/` |

## Quyết định (17/11/2026, chạy ngầm)
- Lời Hindi viết bằng chữ Devanagari; lượt tiếng Anh có `dich` Hindi; khách + bà chủ vẫn nói tiếng Anh (người nước ngoài), "I'm sorry, I don't speak Hindi."
- Lượt robot 27 là câu lẫn Anh + Hindi, không có `dich`.
- Kịch bản, cảnh không lời, giữ nguyên bố cục video gốc; 3 biến thể khác nhau ở tên/ngoại hình/cách gọi chú/nền chợ (cùng giới vì kịch bản tả "the boy").
- Tách thể loại riêng để không đổi font/phụ đề của bản Tây Ban Nha.

## Tình trạng (17/11/2026, cập nhật)
- `kiem-tra --tai-anh`: 0 lỗi, 0 cảnh báo, 23 mục đạt. Dự án Studio `Tiem-thit---Hindi-17790cf1-127c` (loại `Tiem-thit-hoc-tieng-Anh-Hindi-1bc6`).
- Muse có lại tài khoản: gen 6 ảnh TAVO_A/B/C, TIO_A/B/C (nền xanh, một người, không chữ, đã xem từng ảnh); `refs` đủ 5 nhân vật, đã cập nhật vào dự án cũ qua PUT (không tạo dự án mới).
- Chạy thử biến thể `raju-tiem-thit-goc`: cảnh 1 ĐẠT (`scene1_start.png`: khách áo polo trắng đứng một mình, chợ Ấn Độ, cận nghiêng về quầy; clip cuối cảnh khách cười nói). Các cảnh sau đang gen tiếp trong Studio.
- Cần làm: xem tiếp scene2_start (góc A), clip cảnh 6/11/17/18/24, montage 32-38; chọn Thương hiệu (end card app); duyệt rồi chạy 2 biến thể còn lại.
- Rủi ro: phụ đề Devanagari (đã bật `shaping: complex`), Whisper `small` nghe Hindi xen Anh có thể gen lại nhiều; cảnh 9 hai người cùng giới chung khung.

## Phân tích lại (17/11/2026, lần 2)
Đo lại video, đối chiếu từng lượt với kịch bản: khớp, không đổi kịch bản/biến thể, không gen lại. Dự án cũ giữ nguyên, chạy thử `raju-tiem-thit-goc` tiếp tục; `scene2_start.png` (góc A) đạt.

## Phân tích lại (17/11/2026, lần 3)
Kịch bản/biến thể không đổi (`kiem-tra`: 0 lỗi, 0 cảnh báo). Phát hiện hàng đợi mất mục `raju-tiem-thit-goc` sau khi Studio khởi động lại (cảnh 1-2 đã xong, dừng ở cảnh 3). Đã đưa lại vào hàng đợi qua `/api/queue/add` + `/api/queue/start` (id `a70f667f`): chạy tiếp từ cảnh 3, dùng lại file cảnh 1-2, không gen lại.
