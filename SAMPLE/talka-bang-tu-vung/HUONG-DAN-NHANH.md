# Hướng dẫn nhanh: video "Talka bảng từ vựng"

Robot dạy từ Tây Ban Nha → tiếng Anh trước tờ giấy, bút đỏ chỉ chữ, cuối video quảng cáo app.
Bạn chỉ cần: **nhập kịch bản → tạo dự án → gen → hậu kỳ**. Bút, chữ tiếng Anh, ô quảng cáo, logo, end card đều **tự động**.

---

## Bước 0: Cập nhật (mỗi khi có bản mới)
1. Đóng LUO Studio.
2. Chạy **`Cap nhat.bat`**.
3. Mở lại LUO Studio.

## Bước 1: Nhập kịch bản (làm 1 lần)
1. Tab **Loại dự án** → **Loại mới**.
2. Chọn file: `SAMPLE\talka-bang-tu-vung\KICH-BAN-TALKA-CO-CHU.txt` → bấm **Tạo**.
   (Đặt tên loại tuỳ ý, ví dụ "Talka từ vựng".)

## Bước 2: Tạo dự án
1. **Dự án mới** → chọn loại vừa nhập.
2. Chọn file biến thể: `SAMPLE\talka-bang-tu-vung\BIEN-THE-TALKA-CO-CHU.json` (hoặc file biến thể mới, xem Bước 5).

## Bước 3: Gen video
1. Bấm **Thêm vào hàng đợi** → chạy.
2. Xem nhanh từng cảnh khi xong:
   - ✅ Tờ giấy **trống** ở các vạch xám (không chữ tiếng Anh, không tay, không bút).
   - ✅ Robot đọc **đúng lời**.
   - ❌ Sai (ví dụ robot nói "¿Cómo se dice **please**?") → **gen lại cảnh đó và cảnh ngay sau**.

## Bước 4: Hậu kỳ
Bấm **Hậu kỳ** → xong. Video xuất ra có bút chỉ chữ, chữ tiếng Anh, ô quảng cáo, logo, end card (không phụ đề).

> Lần hậu kỳ đầu tiên có thể lâu hơn (máy tải mô hình nhận giọng nói ~1,5 GB).

---

## Bước 5: Tạo biến thể mới bằng AI (đổi từ vựng / app / nhân vật)

1. Mở **Claude** hoặc **ChatGPT**, **đính kèm** file `BIEN-THE-TALKA-CO-CHU.json`.
2. Dán đoạn sau, sửa phần trong `[ ]`:

```
File đính kèm là biến thể mẫu. Viết [3] biến thể mới, trả về MỘT mảng JSON cùng cấu trúc, cùng tên khoá.
Chủ đề từ vựng: [chào hỏi]. Tên app: [Talka] (đọc là [TAWK-ah]).

Bắt buộc:
- "name" mới, không dấu, không trùng.
- "LUOT" đúng 9 lượt:
  + Lượt 1,2,3,5,6 đúng mẫu: "¿Cómo se dice <từ TBN>? Se dice, <tiếng Anh>. Repite conmigo. <tiếng Anh>."
  + Lượt 4: một câu động viên ngắn tiếng Tây Ban Nha.
  + Lượt 7,8,9: quảng cáo tiếng Tây Ban Nha; lượt 8 phải có "Descarga <Tên app>".
- "NEN_BANG": giữ nguyên mô tả, chỉ thay 8 từ trong ngoặc kép: 5 từ đầu = đúng 5 từ TBN của lượt 1,2,3,5,6, đúng thứ tự; 3 từ sau cùng chủ đề.
- Đổi tên app thì sửa "PHAT_AM" theo tên mới.
- Giữ nguyên các khoá khác. Chỉ trả về JSON.
```

3. Lưu kết quả thành file `.json` (ví dụ `BIEN-THE-CHAO-HOI.json`).
4. Làm lại **Bước 2** với file này. **Chạy thử 1 biến thể trước** rồi mới chạy nhiều.

### Tự kiểm tra file biến thể (30 giây)
- [ ] Có đúng **9** lượt.
- [ ] Lượt 1, 2, 3, 5, 6 đúng mẫu câu ở trên.
- [ ] 5 từ đầu trong `NEN_BANG` **giống hệt và đúng thứ tự** với từ Tây Ban Nha trong 5 lượt đó.
- [ ] Lượt 8 có "Descarga <Tên app>".

---

## Gặp lỗi?

| Lỗi | Làm gì |
|---|---|
| Robot đọc sai / lẫn tiếng Anh vào câu hỏi | Gen lại cảnh đó + cảnh sau |
| Giấy có chữ / tay / bút | Gen lại cảnh đó |
| Bút chỉ sai hàng | Sửa 5 từ đầu trong `NEN_BANG` cho khớp thứ tự lời đọc |
| Video có phụ đề, không có bút | Loại dự án đang dùng kịch bản cũ → làm lại Bước 1 với file mới |

Chi tiết hơn: `HUONG-DAN-SU-DUNG.md` (cùng thư mục).
