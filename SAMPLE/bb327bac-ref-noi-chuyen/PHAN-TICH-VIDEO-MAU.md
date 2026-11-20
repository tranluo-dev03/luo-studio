# Phân tích video mẫu bb327bac-ref-noi-chuyen

Video dọc 1080x1920, 43,8 s, KHÔNG có cảnh cắt, camera đứng yên (đo: dịch 27 px/160x284 cả video). 20 câu Whisper → 13 lượt sau khi gộp. Tốc độ trung vị 2,92 từ/giây.
Ngôn ngữ gốc: người học nói tiếng Tây Ban Nha (phụ đề vàng), robot nói tiếng Tây Ban Nha xen câu tiếng Anh (phụ đề trắng). Bản mới: toàn tiếng Anh (người học tiếng Anh vụng).

## Cấu trúc hook / tình huống
- HOOK 0:00-0:07.5 (lượt 1-3): robot hỏi "Where are you from?", người học "I am Mexico" ❌, robot "Casi, mejor di: I am from Mexico".
- TÌNH HUỐNG 0:07.5-0:43.8 (lượt 4-13): "hay nhầm" → "không có tiền" → app miễn phí → "gia sư thật?" → "sửa ngữ pháp, phát âm" → "tôi tải app" → khen.
- Quảng cáo/end card: không thấy trong video (logo/outro do Thương hiệu).

## Bố cục
Ô robot ngang bo góc viền trắng phía trên (x 0.015-0.985, y 0.005-0.33), nền đen có vòng sóng âm trắng, robot người máy trắng mắt xanh. Nền toàn khung: người học nữ (~50 tuổi, đồng phục xanh navy, băng đô) đứng rửa bát trong bếp kem, mặt ở y≈0.54. Phụ đề ô trắng (robot) / ô vàng (người học) chữ đen dưới ô robot; ❌ cạnh câu sai. Giọng: robot ~130-175 Hz (A), người học ~195-230 Hz (B).

## Bảng hành động (rút gọn)
| Lượt | Ai | Hành động |
|---|---|---|
| 1 | robot | hỏi, miệng mở; người học liếc lên ô, cười |
| 2 | người học | "I am Mexico" tự tin, mặt tươi; ❌ |
| 3 | robot | sửa; người học gật, cười |
| 4 | người học | cười ngượng, nhắm mắt |
| 5 | robot | an ủi; người học nghe, mắt lên ô |
| 6-8 | người học/robot | lo tiền, ngạc nhiên; robot giải thích |
| 9-13 | luân phiên | hỏi lại, đồng ý, quyết định tải app, khen |
Tay người học luôn ở bồn rửa (không đổi). Mọi nhịp chuyển động mạnh (đo) là cử động đầu/miệng khi nói, không có cảnh cắt.

## Video gốc → kịch bản
| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Ô robot + nền người học | `[GHEP HAI LOP]` nền HOC, khung DAY 0.02,0.01,0.96,0.32 (gen 16:9) | khuôn an toàn: không bao giờ hai người cùng nói |
| Vòng sóng âm quanh robot, dải sóng nháy | bỏ (nền đen phẳng) | Studio chưa làm |
| Phụ đề 2 màu + ❌ | hậu kỳ thể loại (`config.json`), fx wrong/right | khác kiểu cụm 1-3 từ của gốc |
| Tiếng Tây Ban Nha | đổi toàn tiếng Anh | theo yêu cầu |
| Chữ "Más o menos" ở 0:00 (trả lời câu trước) | bỏ, mở bằng robot hỏi | |
| Ảnh thật | hoạt hình 3D (người) + robot dùng lại ảnh `robot-talka.png` | gen-anh-nhan-vat chỉ có phong cách Pixar |
