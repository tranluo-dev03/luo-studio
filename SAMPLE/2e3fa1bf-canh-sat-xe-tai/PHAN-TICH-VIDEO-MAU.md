# Phân tích video mẫu: 2e3fa1bf-canh-sat-xe-tai.mp4

Video 1080x1920, 14,7 s, 6 câu Whisper (gộp thành 4 lượt), 3,39 từ/giây (cao nhất 4,09), 0 cảnh cắt, máy đứng yên (dịch 7,1 px/160x284). Công cụ: `video-moi.py danh-gia` (kết quả ở `userdata/studio/claude/_uploads/2e3fa1bf-canh-sat-xe-tai-phan-tich/`).
Giọng: nữ ~190–220 Hz (tài xế), nam ~112–121 Hz (cảnh sát). Whisper gán lượt 5 "Perfect" 167 Hz nhưng khung hình cho thấy cảnh sát nói (nhiễu cao độ); phụ đề trên hình viết số "fifty" bằng chữ.
Ngôn ngữ: tiếng Anh. Sản phẩm: quảng cáo app học tiếng Anh với gia sư AI (không nêu tên app, không có logo/end card trong 14,7 s).

## Cấu trúc hook / tình huống
- **HOOK** (0:00–0:06, lượt 1–2): tài xế nói sai tuổi "Officer, I have fifty years!" (tự tin, cười), cảnh sát hỏi lại "Ma'am, you mean you are fifty years old?".
- **TÌNH HUỐNG** (0:06–0:14,5, lượt 3–4): tài xế ngượng sửa "Oh no! Yes, I am fifty years old."; cảnh sát "Perfect! Practice English every day with an AI tutor." (lời kêu gọi).
- Quảng cáo/end card: không có.
- Hook mới (kịch bản B): câu sai khác "Officer, my old is fifty!", cùng độ dài, cảnh sát hỏi lại giữ nguyên.

## Bố cục
Một góc máy cố định: xe tải xanh chiếm ~60% trái, tài xế nhoài ra cửa sổ cabin (trái-trên, đầu ~1/3 chiều cao, mặt nhìn xuống), cảnh sát đứng phải dưới đường, nhìn từ hơi sau lưng trái, mặt nghiêng ngẩng lên (đầu ~40% chiều cao). Hoàng hôn cam-hồng, cây cọ xa. Phụ đề trắng viền đen ở ~2/3 dưới; câu sai viền đỏ, câu sửa viền xanh.

## Bảng hành động
| Lượt | Giây | Ai nói | Hành động người nói | Người nghe | Vật dụng | Ánh mắt / camera | Khung cuối |
|---|---|---|---|---|---|---|---|
| 1 | 0–2,5 | tài xế | nhoài tì tay bậu cửa sổ, nói to, cười rạng rỡ | cảnh sát ngẩng nhìn, bình thản | không | tài xế nhìn xuống, cảnh sát nhìn lên; máy đứng yên | tài xế cười, cảnh sát ngẩng |
| 2 | 3,7–5,9 | cảnh sát | nhướn mày, hơi nghiêng đầu, hỏi bối rối | tài xế nghe, nụ cười nhạt dần | không | như trên | cảnh sát mày nhướn |
| 3 | 6,9–9,9 | tài xế | "Oh no!" mắt mở to ngượng, cười, nói lại chậm rõ | cảnh sát nghe, gật | không | như trên | tài xế cười ngượng |
| 4 | 10,6–14,5 | cảnh sát | cười rạng rỡ, gật khen, nhấn "every day" | tài xế cười lại | không | như trên | cả hai cười |

Chuyển động mạnh 0,12–1,75 / 6,88–8,5 / 10,1–11,25 s: biểu cảm và nhấc đầu (không phải cảnh cắt hay đạo cụ).

## Bảng "video gốc → kịch bản"
| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Whisper 6 câu | 4 lượt (gộp "Oh no." + "Yes, I am…", "Perfect." + "Practice…") | mỗi cảnh một người nói |
| Cảnh sát nói số "fifty" | giữ chữ "fifty" | |
| Phụ đề trắng viền đen, viền đỏ/xanh | hậu kỳ `types/2e3fa1bf-canh-sat-xe-tai` (ô đen chữ trắng, fx/icon) | Studio làm ô đen thay vì chỉ viền chữ: còn khác mẫu |
| Cảnh sát nhìn nghiêng sau vai | `Prompt ảnh` + EYE LINE; refs mặt cảnh sát và tài xế | rủi ro Muse xoay mặt người quay lưng |
| Mây, xe, cọ | đứng yên | đơn giản hoá |
Rủi ro: nữ+nam khác giới nên không lo gán giọng; cảnh sát nghiêng ba phần tư ngược camera; chữ trên đồng phục/xe (đã cấm trong NEGATIVE).
