# Code riêng: check hành lý + gia sư AI, tiếng Gujarati (`check-hanh-ly-hindi`)

Nhân bản từ `soi-hanh-ly-gia-su-ai` (08/11/2026). Kịch bản, biến thể, phân tích: `SAMPLE/check-hanh-ly-hindi/`. Studio dùng thư mục này khi kịch bản có khối `[HAU KY]` với dòng `loai: check-hanh-ly-hindi`.
Hai file `.py` chỉ gọi code chung, khác thể loại gốc ở `config.json`.

| File | Nội dung |
|---|---|
| `gen.py` | Gen: phần 1 cảnh thường (17 cảnh, MỘT góc máy đứng yên, chỉ cảnh 1 có `Prompt ảnh`), phần 2 ghép 2 lớp, nhoè chuyển cảnh. Logic: `../_chung/nhieu_phan.py` |
| `post.py` | Hậu kỳ: phụ đề, ❌/✅, viền + tiếng sai/đúng. Logic: `../_chung/hau_ky.py` + `phu_de.py` |
| `config.json` | `phu_de`: font `Nirmala UI` (có chữ Gujarati; Arial không có), cỡ 54, độ cao 1565 cả hai phần (≈ 81,5% khung như video mẫu), mọi người chữ đen trên ô trắng, Whisper đa ngôn ngữ `small` |

Chạy tay hậu kỳ: `.venv\Scripts\python.exe app\production\types\check-hanh-ly-hindi\post.py <run>\raw.mp4 --scenes <run>\scenes.json --out <run>\final.mp4 --variant <run>\variant.json`.
