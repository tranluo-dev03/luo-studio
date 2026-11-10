# Code riêng: quét an ninh cơ thể + dây chuyền + gia sư AI (`quet-an-ninh-day-chuyen`)

Kịch bản, biến thể, ảnh tham chiếu, phân tích: `SAMPLE/quet-an-ninh-day-chuyen/`. Studio dùng thư mục này khi kịch bản có khối `[HAU KY]` với dòng `loai: quet-an-ninh-day-chuyen`.
Nhân bản từ `soi-hanh-ly-gia-su-ai` (10/11/2026): hai file `.py` chỉ gọi code chung (`../_chung/`), `config.json` giữ nguyên giá trị của bản gốc. Code **không** phụ thuộc vali/băng chuyền: cổng dò kim loại, dây chuyền, khay đồ chỉ là chữ trong kịch bản.

| File | Nội dung |
|---|---|
| `gen.py` | Gen: phần 1 cảnh thường (13 cảnh, đổi góc máy, cảnh 1 có cú lia máy vụt sang hành khách bằng `Giữ sau lời`; cảnh đổi góc có `Prompt ảnh`), phần 2 ghép 2 lớp, nhoè chuyển cảnh. Logic: `../_chung/nhieu_phan.py` |
| `post.py` | Hậu kỳ: phụ đề theo phần/người nói, ❌/✅, viền + tiếng sai/đúng. Logic: `../_chung/hau_ky.py` + `phu_de.py` |
| `config.json` | `nhoe` 1.0; `phu_de`: cỡ chữ 60, độ cao 1125 cả hai phần, phần 1 chữ trắng viền đen, phần 2 AI vàng / hành khách trắng, Whisper `small.en` |
