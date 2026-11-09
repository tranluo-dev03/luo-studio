# Thể loại: du lịch + chia đôi gia sư AI (`du-lich-chia-doi-gia-su-ai`)

Video mẫu: `2310_face to face ES_005_2` (30,2 giây, tiếng Tây Ban Nha xen tiếng Anh). Carla hỏi robot ở Machu Picchu "quy tắc đầu tiên để học tiếng Anh?",
robot đáp "đừng học, hãy dùng; chỉ cần nói với người bản xứ" → cắt nhoè sang **gọi video chia đôi dọc**: robot gia sư AI nửa trái, Carla ngồi sofa nửa phải;
Carla nói sai "I have 22", "I'm Mexico", AI sửa, Carla nói lại đúng.

| Phần | Cảnh | Chế độ |
|---|---|---|
| 1. Machu Picchu | 3 (Carla – robot – Carla) | Cảnh thường, một khung, camera đứng yên |
| 2. Gọi video | 9 (AI/Carla xen kẽ) | Ghép 2 lớp chia đôi (khuôn `chia-doi-gia-su-ai`), vào bằng nhoè 0,5 s |

| File | Nội dung |
|---|---|
| `KICH-BAN-DU-LICH-CHIA-DOI-GIA-SU-AI.txt` | Kịch bản 2 phần |
| `BIEN-THE-DU-LICH-CHIA-DOI-GIA-SU-AI.json` | Biến thể 01 bám sát video gốc (sinh bằng `cong-cu/tao_bien_the.py`, không sửa tay) |
| `cong-cu/tao_bien_the.py` | Bảng `BIEN_THE` (tên, ngoại hình, giọng, ảnh, tuổi, quê) + `luot()` |
| `PHAN-TICH-VIDEO-MAU.md` | Bảng hành động, phụ đề, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc viết thêm biến thể |
| `anh/carla.png`, `anh/robot-machu-picchu.png`, `anh/robot-goi-video.png` | Ảnh tham chiếu cắt từ video mẫu (đã bỏ logo, phụ đề, chữ "AI" trên trán robot) |
| `anh/khung-phan1-mau.png` | Khung phần 1 của video mẫu để so bố cục |

Code riêng: `app/production/types/du-lich-chia-doi-gia-su-ai/` (`gen.py`, `post.py`, `config.json`).

## Chạy
```
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\du-lich-chia-doi-gia-su-ai\KICH-BAN-DU-LICH-CHIA-DOI-GIA-SU-AI.txt SAMPLE\du-lich-chia-doi-gia-su-ai\BIEN-THE-DU-LICH-CHIA-DOI-GIA-SU-AI.json --tai-anh
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\du-lich-chia-doi-gia-su-ai\KICH-BAN-DU-LICH-CHIA-DOI-GIA-SU-AI.txt SAMPLE\du-lich-chia-doi-gia-su-ai\BIEN-THE-DU-LICH-CHIA-DOI-GIA-SU-AI.json --ten-loai "Du lịch + chia đôi gia sư AI" --ten-du-an "Machu Picchu - Carla" --chay-thu
```
(Bản cài này dùng `.venv\Scripts\python.exe`, không có thư mục `runtime\`.)

Sau cảnh đầu: xem `scene1_start.png` (bố cục phần 1 so với `anh/khung-phan1-mau.png`) và `phan2/base_HOC.png`, `phan2/base_DAY.png` (người ở giữa, cốc trong nửa giữa).

## Quyết định đã chốt (05/11/2026)
- Bỏ logo "Aiva AI": không gen, không cài logo Thương hiệu.
- Lời giữ nguyên văn video mẫu (người dùng yêu cầu "y hệt"), sửa theo phụ đề trên hình chỗ Whisper nghe nhầm.
- Hai khoá robot: `ROBOT` (phần 1, không tai nghe) và `DAY` (phần 2, tai nghe), cùng mô tả giọng.
- Thêm màu chữ `blue` vào `app/production/types/_chung/phu_de.py` (chỉ bổ sung một khoá màu; thể loại khác không đổi).
- Whisper hậu kỳ `small` (đa ngôn ngữ) thay `small.en`.

## Rủi ro / còn khác video mẫu
- Phần 1 hai giọng nữ cùng khung (robot + Carla): Studio tự tách giọng cao/thấp; nếu Carla vẫn nhép lời robot ở cảnh 2 → bật `voice_swap` hoặc gen lại cảnh 2.
- Robot phần 1 bị mép khung cắt, nhìn nghiêng: Muse có thể đưa robot vào giữa khung → so `scene1_start.png`, lệch thì gen lại ảnh đầu.
- Phụ đề phần 1 là ô đen theo dòng (video gốc: dải mờ cả bề ngang, chia cụm 2–4 từ); viền đỏ/xanh nháy ở nửa phải (video gốc không có).

## Nhật ký chạy
- 05/11/2026: nhập Studio (loại `Du-lich-chia-doi-gia-su-AI-7863`, dự án `Machu-Picchu---Carla-2ba9`), chạy thử biến thể 01.
  `scene1_start.png` đạt: robot mép trái bị cắt vai, nhìn nghiêng về Carla, tay đan; Carla nửa phải, áo vàng mù tạt, tay đút túi, nhìn đỉnh núi.
  Khác nhẹ: Carla đứng thấp hơn video mẫu (đầu ở ~1/3 thay vì ~1/4 chiều cao).
- 05/11/2026 lượt 1–2: robot phần 2 bị phóng to (ảnh tham chiếu cắt sát mặt), rồi dính vệt inpaint từ ảnh tham chiếu → bỏ.
- 05/11/2026: người dùng chốt KHÔNG lấy ảnh tham chiếu từ video. Robot = ảnh AI người dùng (`anh/ai-robot.png`) cho cả hai phần (không tai nghe);
  Carla = ảnh Muse gen lại hoàn chỉnh (`anh/ai-carla.png`, `cong-cu/gen_anh_carla.py`). Xoá bản chạy cũ, gen lại từ cảnh 1.
- 05/11/2026 lượt 3: `final.mp4` 59,2 s, bố cục và phụ đề đạt. Lỗi: cảnh 5 Carla nói "I have twenty-two" HAI lần; mỗi clip lặng đầu 0,5–2 s nên video dài gấp đôi bản gốc (30,2 s).
- 05/11 sửa 7: cảnh 2 Carla nhép + nhắm mắt theo robot. Bỏ "sculpted closed lips" khỏi mô tả robot; prompt cảnh 2 tả Carla im trước; engine đo miệng bắt được người nghe nghiêng mặt. Cần bật Cài đặt → Kiểm tra miệng người nghe (đang tắt). Chờ gen lại để kiểm chứng.
- 05/11 17:18 kiểm chứng sửa 7: cảnh 2 gen lại ĐẠT ngay lần đầu (Carla mím môi suốt clip, robot nói rõ).
- 06/11: thêm 20 biến thể theo CSV người dùng (`BIEN-THE-DU-LICH-CHIA-DOI-20-BIEN-THE.json`, sinh bằng `cong-cu/tao_bien_the.py`): 1–10 nền Chichén Itzá, 11–20 nền Tulum; kịch bản phần 1 chuyển sang token (GIOI_HOC, ANH_SANG, NEN_ROBOT, DIEM_NHIN, TAY_HOC). Dự án Studio: "Face to face Mexico - 20 bien the".
