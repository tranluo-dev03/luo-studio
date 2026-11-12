# `taxi-gia-su-ai`: gen + hậu kỳ riêng

Thể loại hoạt hình 3D "tài xế taxi + gia sư AI" (kịch bản + biến thể: `SAMPLE/taxi-gia-su-ai/`). Hai phần: cảnh thường (có cảnh KHÔNG LỜI) → ghép 2 lớp.

- `gen.py`: gọi `_chung/nhieu_phan.run`; trước đó bọc `engine.run_variant` để đổi lượt có `"text": "[KHONG LOI]"` thành rỗng (engine tạo clip câm).
  Lý do: `nhieu_phan.plan` bỏ lượt rỗng nên cảnh không lời phải mang MARKER để giữ đúng số cảnh. Chỉ lượt có đúng MARKER bị đổi.
- `post.py`: gọi `_chung/hau_ky.py`, bỏ lượt MARKER khỏi phụ đề.
- `config.json`: phần 1 ô trắng chữ đen + dòng dịch, phần 2 chữ vàng; nhoè vào phần 2; Whisper `small`.
- End card app: Thương hiệu → Outro.
