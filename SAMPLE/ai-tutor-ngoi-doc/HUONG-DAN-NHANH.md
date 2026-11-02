# Hướng dẫn nhanh: video "AI tutor ngồi đọc"

Robot ngồi đọc câu tiếng mẹ đẻ rồi câu tiếng học; bảng phía trên hiện cặp câu + phiên âm. Bảng và chữ do **hậu kỳ tự làm**.

## Bước 1: Nhập kịch bản (làm 1 lần)
Tab **Loại dự án** → **Loại mới** → chọn `SAMPLE\ai-tutor-ngoi-doc\KICH-BAN-AI-TUTOR-NGOI-DOC.txt` → **Tạo** (đặt tên tuỳ ý).

## Bước 2: Tạo dự án
**Dự án mới** → chọn loại vừa nhập → chọn `SAMPLE\ai-tutor-ngoi-doc\BIEN-THE-AI-TUTOR-NGOI-DOC.json` (4 biến thể mẫu).

## Bước 3: Gen
Tick biến thể → **Thêm vào hàng đợi** → **Bắt đầu**. Xem nhanh từng cảnh:
- ✅ Robot ngồi yên, phần trên khung không có chữ hay biển hiệu.
- ✅ Đọc đúng thứ tự, đúng ngôn ngữ. Sai → **gen lại cảnh đó** và cảnh ngay sau.

## Bước 4: Hậu kỳ
Bấm **Hậu kỳ**. Lần đầu mỗi video, máy gen **khung bảng** bằng AI (mất thêm 1–2 phút), rồi điền chữ và ghép. Không có phụ đề, không có end card.

---

## Tạo biến thể mới bằng AI
1. Mở **Claude** / **ChatGPT**, đính kèm `BIEN-THE-AI-TUTOR-NGOI-DOC.json`.
2. Dán đoạn sau, sửa phần `[ ]`:

```
File đính kèm là biến thể mẫu. Viết [3] biến thể mới, trả về MỘT mảng JSON cùng cấu trúc, cùng tên khoá.
Yêu cầu: ngôn ngữ mẹ đẻ [tiếng Tây Ban Nha], ngôn ngữ học [tiếng Anh], chủ đề [chào hỏi],
robot [mô tả hoặc giữ nguyên], nền [mô tả hoặc giữ nguyên], cờ trên bảng [cờ nước của ngôn ngữ học].

Bắt buộc:
- "name" mới, không dấu, không trùng.
- "BANG_TU": đúng 10 dòng "câu mẹ đẻ | câu tiếng học | phiên âm theo cách đọc của người nói tiếng mẹ đẻ",
  rồi 1 dòng cuối là câu kết bằng tiếng mẹ đẻ (không có dấu |). Câu ngắn (tối đa ~4 từ).
- "LUOT": đúng 4 lượt; lượt 1–3 mỗi lượt 3 cặp, lượt 4 có 1 cặp + câu kết. Mỗi cặp đọc là "<câu mẹ đẻ>. <câu tiếng học>."
  (giữ "?" nếu là câu hỏi), đúng thứ tự trong BANG_TU. Mỗi lượt: {"who":"day","text":...,"emo":"warm, encouraging","fx":"none"}.
- "NGON_NGU_ME", "NGON_NGU_HOC": tên ngôn ngữ bằng tiếng Anh (vd "Mexican Spanish", "American English").
- "GIONG_DAY": giọng người bản xứ của ngôn ngữ mẹ đẻ.
- "CO": hai lá cờ nhỏ ở hai góc trên + một linh vật hoạt hình, theo nước của ngôn ngữ học (viết bằng tiếng Anh).
- Giữ nguyên các khoá khác nếu tôi không yêu cầu đổi. Chỉ trả về JSON.
```

3. Lưu kết quả thành `.json` → **Dự án mới** (hoặc nút **mũi tên lên** dưới danh sách biến thể) → chạy thử 1 biến thể trước.

### Tự kiểm tra
- [ ] `BANG_TU` có 10 dòng cặp + 1 dòng câu kết.
- [ ] `LUOT` có đúng 4 lượt, đọc đúng các cặp theo thứ tự `BANG_TU`.
- [ ] Mọi biến thể trong cùng dự án có cùng số lượt (4).

## Lỗi thường gặp
| Lỗi | Làm gì |
|---|---|
| Bảng là khung gỗ đơn giản, không có cờ | Máy không gen được khung bảng (mất kết nối API) → mở lại Studio, xoá `board.png` trong thư mục chạy, Hậu kỳ lại |
| Muốn đổi khung bảng khác | Xoá `board.png` và `board_raw.png` trong thư mục chạy rồi Hậu kỳ lại |
| Chữ trên bảng đổi lệch lời đọc | Robot đọc sai / thiếu cặp → gen lại cảnh đó |
| Video có phụ đề | Loại dự án dùng kịch bản cũ → nhập lại kịch bản |
