# Hậu kỳ riêng: AI tutor ngồi đọc (`ai-tutor-ngoi-doc`)

Kịch bản, biến thể, hướng dẫn: `SAMPLE/ai-tutor-ngoi-doc/`.

`post.py` (Studio gọi kèm `--variant`):
1. **Khung bảng**: gen bằng AI (Muse) theo ô `CO` trên phông xanh → cắt phông → tìm lòng trắng. Lưu `board.png`, `board_raw.png` cạnh `raw.mp4` để dùng lại; không gen được thì vẽ bảng đơn giản bằng code. Có thể đưa bảng có sẵn bằng `--board`.
2. **Chữ trong bảng** theo ô `BANG_TU`: câu tiếng mẹ đẻ (đen, gạch chân), câu tiếng học (đỏ, to), phiên âm (đỏ, nhỏ); câu kết (vàng viền nâu). Đổi theo lúc robot đọc câu tiếng mẹ đẻ của từng cặp (Whisper theo từng cảnh, ngôn ngữ theo `NGON_NGU_ME`).
3. Không gắn logo, nhãn hay end card.
Không phụ đề, không end card.
