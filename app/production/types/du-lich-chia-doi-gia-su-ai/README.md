# Code riêng: du lịch + chia đôi gia sư AI (`du-lich-chia-doi-gia-su-ai`)

Kịch bản, biến thể, phân tích: `SAMPLE/du-lich-chia-doi-gia-su-ai/`. Studio dùng thư mục này khi kịch bản có khối `[HAU KY]` với dòng `loai: du-lich-chia-doi-gia-su-ai`.
Cùng khuôn với `san-bay-gia-su-ai` / `soi-hanh-ly-gia-su-ai`: hai file `.py` chỉ gọi code chung, khác nhau ở `config.json`.

| File | Nội dung |
|---|---|
| `gen.py` | Gen: phần 1 cảnh thường (3 cảnh, Machu Picchu), phần 2 ghép 2 lớp chia đôi dọc, nhoè chuyển cảnh. Logic: `../_chung/nhieu_phan.py` |
| `post.py` | Hậu kỳ: phụ đề theo phần/người nói, ❌/✅, tô cụm đúng, viền + tiếng sai/đúng ở nửa phải. Logic: `../_chung/hau_ky.py` + `phu_de.py` |
| `config.json` | `nhoe`; `phu_de`: cỡ 58; y phần 1 = 360 (trên cao, ô đen), phần 2 = 1065; `kieu_theo_phan` (P1: Carla xanh dương, robot vàng; P2: AI vàng, Carla trắng); `vien` nửa phải; Whisper `small` (đa ngôn ngữ, lời Tây Ban Nha + Anh) |

Chạy tay hậu kỳ: `.venv\Scripts\python.exe app\production\types\du-lich-chia-doi-gia-su-ai\post.py <run>\raw.mp4 --scenes <run>\scenes.json --out <run>\final.mp4 --variant <run>\variant.json`.
