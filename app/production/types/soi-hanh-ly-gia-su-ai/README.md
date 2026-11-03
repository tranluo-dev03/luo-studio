# Code riêng: soi hành lý + gia sư AI (`soi-hanh-ly-gia-su-ai`)

Kịch bản, biến thể, phân tích: `SAMPLE/soi-hanh-ly-gia-su-ai/`. Studio dùng thư mục này khi kịch bản có khối `[HAU KY]` với dòng `loai: soi-hanh-ly-gia-su-ai`.
Cùng khuôn với `san-bay-gia-su-ai` / `canh-sat-gia-su-ai`: hai file `.py` chỉ gọi code chung, khác nhau ở `config.json`.

| File | Nội dung |
|---|---|
| `gen.py` | Gen: phần 1 cảnh thường (13 cảnh, đổi góc máy, cảnh 1 có cú lia máy giữ lại bằng `Giữ sau lời`; cảnh đổi góc có `Prompt ảnh`), phần 2 ghép 2 lớp, nhoè chuyển cảnh. Logic: `../_chung/nhieu_phan.py` |
| `post.py` | Hậu kỳ: phụ đề theo phần/người nói, ❌/✅, viền + tiếng sai/đúng. Logic: `../_chung/hau_ky.py` + `phu_de.py` |
| `config.json` | `nhoe`; `phu_de`: cỡ chữ 60, độ cao 1125 cả hai phần (khung 1080×1920), `kieu_theo_phan` (phần 1 mọi người chữ trắng viền đen; phần 2 AI chữ vàng, người mẹ chữ trắng), Whisper `small.en` |

Chạy tay hậu kỳ: `runtime\python.exe app\production\types\soi-hanh-ly-gia-su-ai\post.py <run>\raw.mp4 --scenes <run>\scenes.json --out <run>\final.mp4 --variant <run>\variant.json`.
