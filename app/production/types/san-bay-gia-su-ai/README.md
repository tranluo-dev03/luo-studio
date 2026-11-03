# Code riêng: sân bay + gia sư AI (`san-bay-gia-su-ai`)

Kịch bản, biến thể, phân tích: `SAMPLE/san-bay-gia-su-ai/`. Studio dùng thư mục này khi kịch bản có khối `[HAU KY]` với dòng `loai: san-bay-gia-su-ai`.

| File | Nội dung |
|---|---|
| `gen.py` | Gen: một dự án hai phần (phần 1 cảnh thường, phần 2 ghép 2 lớp, nhoè chuyển cảnh). Toàn bộ logic ở `../_chung/nhieu_phan.py` |
| `post.py` | Hậu kỳ: phụ đề trắng/vàng theo phần, dòng dịch, ❌/✅/$, viền + tiếng sai/đúng, cụm tên app trên ô vàng. Logic ở `../_chung/hau_ky.py` + `phu_de.py`. Không logo/end card (phần Thương hiệu của dự án làm) |
| `config.json` | `nhoe`: độ mạnh nhoè chuyển cảnh; `phu_de`: cỡ chữ, cỡ dòng dịch, độ cao theo phần (khung 1080×1920), model Whisper |

Chạy tay hậu kỳ: `runtime\python.exe app\production\types\san-bay-gia-su-ai\post.py <run>\raw.mp4 --scenes <run>\scenes.json --out <run>\final.mp4 --variant <run>\variant.json` (đọc `<run>\phan.json` để biết cảnh nào thuộc phần nào).
