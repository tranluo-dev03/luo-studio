# Thể loại: chia đôi màn hình + gia sư AI (`chia-doi-gia-su-ai`)

Video mẫu: `2110_langlearn vertical EN` (44,5 giây). Màn hình 9:16 chia đôi dọc: **robot gia sư AI nửa trái**, **người dùng ngồi bàn cà phê nửa phải**.
Hai bên nói chuyện, người dùng nói sai "I have 28", AI sửa "I am 28", người dùng nói lại đúng, rồi AI giới thiệu app học miễn phí. Một phần duy nhất, chế độ **ghép 2 lớp**.

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-DOI-GIA-SU-AI.txt` | Kịch bản (nhập ở tab "Loại dự án" → "Loại mới") |
| `BIEN-THE-CHIA-DOI-GIA-SU-AI.json` | 3 biến thể (BT 1, 12, 19 của bảng), mỗi biến thể có ảnh tham chiếu gắn sẵn cho robot và người dùng |
| `cong-cu/tao_bien_the.py` | Sinh lại file biến thể: sửa bảng `BIEN_THE` / lời thoại trong đó rồi chạy, không sửa tay JSON |
| `PHAN-TICH-VIDEO-MAU.md` | Bảng hành động từng lượt, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc riêng, lỗi hay gặp, danh sách tự kiểm tra khi viết thêm biến thể |
| `anh/robot-ai.webp` | Ảnh robot (gắn vào `NGUOI_DAY` của mọi biến thể) |
| `anh/khung-video-mau.png` | Một khung của video mẫu để so bố cục |

Code riêng: `app/production/types/chia-doi-gia-su-ai/` (chỉ hậu kỳ `post.py` + `config.json`; phần gen dùng thẳng chế độ ghép 2 lớp của Studio).

## Chạy

1. **Khởi động lại Studio** (lần đầu sau khi cập nhật code: ô nền chia đôi, link Drive, viền nửa khung).
2. Tab **Loại dự án** → **Loại mới** → chọn `KICH-BAN-CHIA-DOI-GIA-SU-AI.txt`. Studio hiện nhãn "Ghép 2 lớp".
3. Tạo dự án theo loại đó → **nhập** `BIEN-THE-CHIA-DOI-GIA-SU-AI.json`. Studio tự tải ảnh tham chiếu:
   - link Google Drive dạng chia sẻ (`.../file/d/<id>/view`) dán thẳng được;
   - ảnh robot là tệp `SAMPLE/chia-doi-gia-su-ai/anh/robot-ai.webp`.
   Mở từng biến thể, xem thẻ nhân vật đã có ảnh (không có dòng báo lỗi đỏ).
4. **Thương hiệu** của dự án: logo cố định "Talka AI" ở vị trí **Dưới trái** (như video mẫu).
5. Gen **một** biến thể trước, xem ảnh gốc `base_HOC.png` / `base_DAY.png` trong thư mục chạy: người phải ngồi giữa ảnh, đầu và cốc nằm trong nửa giữa bề ngang.

## Cấu hình đáng chú ý

- `[GHEP HAI LOP]`: `nen: HOC` + `khung HOC: 0.5, 0, 0.5, 1` + `khung DAY: 0, 0, 0.5, 1`, `bo goc: 0`, `vien: khong`, `noi: lien`, `nghe: moi canh`.
  Nhân vật nền có `khung` riêng nên chỉ chiếm nửa phải (code `split.compose`, từ 04/11/2026).
- Hậu kỳ (`config.json`): ô đen, AI chữ trắng, người dùng chữ vàng, cỡ 56, tâm y 1300; `vien`: viền sai/đúng chỉ ở x 0,5–1, nháy ở cuối câu.
- Lời thoại đổi được trong `cong-cu/tao_bien_the.py` (hàm `luot(tuoi)`); tuổi trong câu sai/sửa/đúng là cột cuối của `BIEN_THE`.
