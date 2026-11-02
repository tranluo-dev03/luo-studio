# Thể loại: AI tutor ngồi đọc (`ai-tutor-ngoi-doc`)

Robot AI ngồi bàn quán cà phê, đọc từng cặp câu: **câu tiếng mẹ đẻ** rồi **câu tiếng học**. Phía trên là một **bảng** hiện cặp câu đang đọc kèm **phiên âm**, không gắn logo hay nhãn. Video khoảng 30 giây, 4 cảnh, không có phần quảng cáo / end card.

## Cách làm (đã chốt)
- **Muse** chỉ gen robot ngồi đọc; phần trên khung để trống.
- **Hậu kỳ** (`app/production/types/ai-tutor-ngoi-doc/post.py`):
  - **khung bảng gen bằng AI** (Muse) theo ô `CO` của biến thể (cờ, linh vật), trên phông xanh rồi cắt phông. Lưu `board.png` trong thư mục chạy, lần sau dùng lại;
  - **chữ trong bảng do code điền** theo ô `BANG_TU`, đổi đúng lúc robot đọc từng cặp (Whisper);
- Kịch bản tự khai báo hậu kỳ bằng dòng `loai: ai-tutor-ngoi-doc` trong khối `[HAU KY]`, nên đặt tên loại dự án tuỳ ý.

## File
| File | Dùng để |
|---|---|
| `HUONG-DAN-NHANH.md` | Hướng dẫn từng bước + prompt nhờ AI viết biến thể |
| `KICH-BAN-AI-TUTOR-NGOI-DOC.txt` | Kịch bản (4 cảnh, mỗi cảnh 3 cặp câu; cảnh cuối có câu kết) |
| `BIEN-THE-AI-TUTOR-NGOI-DOC.json` | 16 biến thể mẫu (xem dưới) |
| `cong-cu/tao-kich-ban.py` | Tạo lại kịch bản + biến thể |

## Ô trong biến thể
| Ô | Ý nghĩa |
|---|---|
| `NGUOI_DAY`, `TEN_DAY` | Ngoại hình robot (đổi AI), tên gọi ngắn |
| `GIONG_DAY` | Giọng (người bản xứ ngôn ngữ mẹ đẻ) |
| `NEN` | Nền phía sau (đổi nền) |
| `TU_THE` | Tư thế và đạo cụ của robot (ngồi bàn, ngồi sofa, đứng cầm giỏ hàng...) |
| `NGON_NGU_ME`, `NGON_NGU_HOC` | Ngôn ngữ mẹ đẻ và ngôn ngữ học (đổi ngôn ngữ) |
| `BANG_TU` | Mỗi dòng `tiếng mẹ đẻ \| tiếng học \| phiên âm`; dòng cuối không có `\|` là câu kết |
| `CO` | Trang trí bảng: cờ + linh vật (đổi cờ) |
| `refs` | Ảnh tham chiếu theo ô: `{"NGUOI_DAY": ["<link ảnh>"]}`. Studio tải về khi tạo dự án và gắn như ảnh đính kèm |
| `LUOT` | Lời đọc từng cảnh, phải khớp `BANG_TU` (3 cặp mỗi cảnh, đọc "mẹ đẻ. học.") |

## 16 biến thể mẫu
1. `ai-tutor-pt-hoc-anh`: giống video gốc: người Brazil học tiếng Anh, cờ Mỹ, robot áo Bồ Đào Nha, quán cà phê.
2. `ai-tutor-pt-hoc-anh-nen-lisbon`: **đổi nền** sang quán cà phê ngoài trời ở Lisbon.
3. `ai-tutor-anh-hoc-bdn`: **đổi ngôn ngữ**: người nói tiếng Anh học tiếng Bồ Đào Nha, **cờ Bồ Đào Nha** + linh vật gà Barcelos.
4. `ai-tutor-pt-hoc-anh-robot-moi`: **đổi AI**: robot bạc mặt màn hình, áo Brazil.
5. `ai-tutor-es-hoc-anh-robot-hoodie`: **đổi AI + bộ từ**: robot áo hoodie thêu hoa văn Mexico, người nói tiếng Tây Ban Nha học tiếng Anh, 7 cặp (Hola, Buenos días...).
6–16. `ai-tutor-es-hoc-anh-bt03…bt13`: người nói tiếng Tây Ban Nha học tiếng Anh, mỗi biến thể một robot/bối cảnh và 7 cặp từ theo chủ đề (buổi sáng, buổi tối, mệnh lệnh, gia đình, bữa sáng, nhà hàng, siêu thị, mua áo, trả tiền, văn phòng, thời tiết). Dữ liệu ở `cong-cu/them-bien-the.py` (chạy lại sau khi chạy `tao-kich-ban.py`). 7 cặp + câu kết chia thành 4 cảnh (2, 2, 2, 1).
