# Split screen vertical · X0042 · 20 biến thể nhân vật (`split-screen-vertical-x0042`)

Dự án mới dựng từ thể loại `chia-doi-gia-su-ai` (robot gia sư AI nửa trái, người dùng ngồi bàn cà phê nửa phải, ghép 2 lớp) và bảng `X0042_20-bien-the-split-screen.csv` (20 biến thể).

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-DOI-GIA-SU-AI.txt` | Kịch bản (loại `chia-doi-gia-su-ai`, nhập ở tab "Loại dự án" → "Loại mới") |
| `BIEN-THE-X0042-20.json` | 20 biến thể, mỗi biến thể gắn sẵn ảnh robot + ảnh nhân vật (đường dẫn tệp trong dự án) |
| `X0042_20-bien-the-split-screen.csv` | Bảng gốc (STT, kiểu, mô tả tiếng Việt, link Drive) |
| `anh/nhan-vat/bien-the-01..20.webp` | 20 ảnh nhân vật tải từ link Drive trong CSV |
| `anh/robot-ai.webp`, `anh/khung-video-mau.png` | Ảnh robot, khung video mẫu |
| `cong-cu/tao_bien_the.py` | Sinh lại JSON: sửa bảng `BIEN_THE` (mô tả tiếng Anh, giọng, tuổi) rồi chạy |
| `PHAN-TICH-VIDEO-MAU.md` | Phân tích video mẫu |

## Đổi lời thoại (theo cột "Kiểu biến thể" của CSV)
- BT 1-7, 11-15: giữ `I have 28` / `I am 28`.
- BT 8-10: đổi thành **35** (lượt 4, 5, 6; phụ đề tự theo).
- BT 16-20: đổi thành **68**.

## Chạy
1. Tab **Loại dự án** → **Loại mới** → `KICH-BAN-CHIA-DOI-GIA-SU-AI.txt`.
2. Tạo dự án theo loại đó → nhập `BIEN-THE-X0042-20.json` (ảnh tự gắn từ `anh/`).
3. Thương hiệu: logo cố định "Talka AI", vị trí Dưới trái. Gen một biến thể trước, xem `base_HOC.png` / `base_DAY.png`.

Lưu ý: mô tả CSV có đồ nửa dưới (váy, giày, quần) — đã bỏ trong bản tiếng Anh vì cảnh ngồi chỉ thấy từ ngực trở lên; ảnh tham chiếu là ảnh đứng, Studio đã dặn bỏ nền và tư thế đứng.
