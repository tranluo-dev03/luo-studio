# Code riêng: cảnh sát chặn xe + gia sư AI (`canh-sat-gia-su-ai`)

Kịch bản, biến thể, phân tích: `SAMPLE/canh-sat-gia-su-ai/`. Studio dùng thư mục này khi kịch bản có khối `[HAU KY]` với dòng `loai: canh-sat-gia-su-ai`.
Cùng khuôn với `san-bay-gia-su-ai`: hai file `.py` chỉ gọi code chung, khác nhau ở `config.json`.

| File | Nội dung |
|---|---|
| `gen.py` | Gen: phần 1 cảnh thường (12 cảnh, mỗi cảnh một góc máy), phần 2 ghép 2 lớp, nhoè chuyển cảnh. Logic: `../_chung/nhieu_phan.py` |
| `post.py` | Hậu kỳ: phụ đề theo phần/người nói, tô màu từ sai/đúng, ❌/✅/$, viền + tiếng. Logic: `../_chung/hau_ky.py` |
| `config.json` | `nhoe`; `phu_de`: cỡ chữ, độ cao theo phần (phần 1: 1320, phần 2: 645 ngay dưới ô AI), `kieu_theo_phan` (phần 1 ô vàng chữ đen; phần 2 AI chữ xanh ngọc ô đen, tài xế chữ đen ô trắng), Whisper `small` (đa ngôn ngữ vì có câu tiếng Tây Ban Nha) |
