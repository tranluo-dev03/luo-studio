# `tiem-thit-tieng-anh`: hậu kỳ riêng

Thể loại phim hoạt hình 3D kể chuyện "tiệm thịt học tiếng Anh" (kịch bản + biến thể: `SAMPLE/tiem-thit-tieng-anh/`).

- Không có `gen.py`: một phần cảnh thường, dùng gen chung của Studio.
- `post.py`: gọi `_chung/hau_ky.py`; phụ đề trắng viền đen (y 1290), lượt tiếng Anh có dòng dịch tiếng Tây Ban Nha (`"dich"`, kiểu dòng dịch chung: chữ đỏ viền trắng).
- `config.json`: font, cỡ chữ, độ cao, Whisper đa ngôn ngữ `small` (lời Tây Ban Nha xen tiếng Anh).
- End card app: Thương hiệu → Outro của dự án.

- Có cảnh KHÔNG LỜI (lượt `"text": ""`): `post.py` map lượt có lời thứ i về đúng cảnh của nó (hau_ky dùng chung coi lượt có lời i = cảnh i).
