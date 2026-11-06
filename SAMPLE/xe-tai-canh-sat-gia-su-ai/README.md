# Thể loại `xe-tai-canh-sat-gia-su-ai`: cảnh sát chặn xe tải + gia sư AI (người thật + AI hoạt hình 3D)

Video mẫu: `AQPPCRx43ias…LQAw (2) (online-video-cutter.com).mp4` (50 s, quảng cáo app LangLearn). Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng: `app/production/types/xe-tai-canh-sat-gia-su-ai/` (`gen.py`, `post.py`, `config.json`), dùng chung `types/_chung/`.

## Dạng video: MỘT dự án, hai phần (khuôn `canh-sat-gia-su-ai` / `soi-hanh-ly-gia-su-ai`)

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Chặn xe tải | 1–9 | Cảnh thường, 2 nhân vật chung khung, MỘT góc máy đứng yên; cảnh 1 `Prompt ảnh`, cảnh sau nối khung cuối | Cảnh sát (`CANHSAT`, phải) hỏi nữ tài xế (`HOC`, nhoài ra cửa sổ cabin, trái-trên); giấy tờ (cảnh 5–6); khoe LangLearn, cầm điện thoại (cảnh 9) |
| 2. Tài xế + gia sư AI | 10–22 | Ghép 2 lớp: AI (`DAY`) trong ô ngang viền trắng phía trên (0.03, 0.012, 0.94, 0.32 → gen 16:9), tài xế selfie toàn khung; `noi: lien`, `nghe: moi canh` | 2 câu sai được sửa, hỏi tiền, tải app |

Vào phần 2: nhoè 0,5 s. Phần 2 dùng lại lời thoại `canh-sat-gia-su-ai` / `xe-tai` (cùng một chiến dịch quảng cáo).

**Khác `canh-sat-gia-su-ai`:** người thật (không hoạt hình) ở phần 1; 2 nhân vật thay vì 3; một góc máy nối khung (không gen ảnh mới mỗi cảnh); phụ đề phần 1 theo người nói.
**Khác `xe-tai`:** `xe-tai` chỉ là phần 2 và gen chung một clip (TOP/BOTTOM); ở đây phần 2 ghép 2 lớp nên hai người không bao giờ cùng nói.

## Phụ đề (`config.json` → `phu_de.kieu_theo_phan`)

| Phần | Cảnh sát / AI | Tài xế | Tâm y |
|---|---|---|---|
| 1 | chữ trắng ô đen | chữ đen ô vàng | 1560 |
| 2 | AI chữ xanh ngọc ô đen | chữ đen ô trắng | 1560 |

Tâm y 1560 (ngang ngực) để phụ đề không che mặt; mẫu đặt cao hơn (1260 / 650).

Lượt: `"to"` tô từ sai (đỏ) / đúng (xanh), `"icon"` x / check / dollar, `"fx"` wrong / right (viền + tiếng).

## File

| File | Dùng làm gì |
|---|---|
| `KICH-BAN-XE-TAI-CANH-SAT-GIA-SU-AI.txt` | Kịch bản (sinh bằng `cong-cu/tao_kich_ban.py`: sửa ở đó rồi chạy lại) |
| `BIEN-THE-XE-TAI-CANH-SAT-GIA-SU-AI.json` | 3 biến thể (sinh bằng `cong-cu/tao_bien_the.py`), 22 lượt (9 phần 1 + 13 phần 2) |
| `anh/khung-phan1-mau.png`, `anh/khung-phan2-mau.png` | Khung video mẫu để SO bố cục (không gửi Muse, không làm refs) |
| `PROMPT-CHO-AGENT.txt` | Quy tắc viết biến thể mới |

Biến thể: `01-goc` (bám sát video: tài xế nữ ~55–60 tuổi, xe xanh cờ Mỹ, đường cao tốc cây cọ), `02-xe-do-sa-mac` (tài xế Mỹ gốc Mexico 40+, cảnh sát da đen, sa mạc), `03-xe-xanh-la-rung-thong` (tài xế 60+ đeo kính, cảnh sát gốc Latin, rừng thông). Lời thoại giống nhau.

## Chạy

```
.venv\Scripts\python.exe SAMPLE\xe-tai-canh-sat-gia-su-ai\cong-cu\tao_kich_ban.py
.venv\Scripts\python.exe SAMPLE\xe-tai-canh-sat-gia-su-ai\cong-cu\tao_bien_the.py
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\xe-tai-canh-sat-gia-su-ai\KICH-BAN-XE-TAI-CANH-SAT-GIA-SU-AI.txt SAMPLE\xe-tai-canh-sat-gia-su-ai\BIEN-THE-XE-TAI-CANH-SAT-GIA-SU-AI.json --tai-anh
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap <kịch bản> <biến thể> --ten-loai "Cảnh sát chặn xe tải + gia sư AI" --ten-du-an "Xe tải cảnh sát gia sư AI" --chay-thu
```
Sau cảnh đầu: so `scene1_start.png` với `anh/khung-phan1-mau.png`; xem `phan2/base_HOC.png` (mặt khớp phần 1, phần trên trống), `phan2/base_DAY.png`.

## Quyết định đã chốt

- Ảnh tham chiếu `refs` CHỈ từ ảnh AI người dùng cung cấp (tài xế, cảnh sát, AI); không cắt từ video mẫu. Gia sư AI = robot trắng của app Talka (`anh/ai-robot-talka.png`, người dùng gửi, cùng robot `du-lich-chia-doi-gia-su-ai`), refs `NGUOI_DAY` mọi biến thể; tài xế, cảnh sát chưa có ảnh.
- Phần 2: đầu tài xế ghi bằng số (đỉnh đầu ~38%, mắt ~48%, cằm ~60% chiều cao) để nằm dưới ô AI; NEGATIVE chặn đồ chơi trên xe và chữ trên bảng tên.
- Ô AI nền đen: dựa vào `_camera_lock` trong `split.py` đã sửa (chỉ đo dải nền, neo khung 0); bản cũ làm vỡ đáy ô.
- Cặp nhân vật phần 1 luôn khác giới (tài xế nữ, cảnh sát nam); kịch bản không dùng đại từ cho tài xế.
- Cảnh báo `kiem-tra` "fx 11:wrong, 13:right, 14:wrong" giữ nguyên: video gốc có câu sai thứ hai "I am very hurry" mà AI sửa không kèm viền xanh.
- Một góc máy đứng yên cho phần 1 (bỏ máy trôi + cắt ẩn); xe đỗ ở phần 2 (video gốc xe chạy).

## Còn khác video mẫu / chưa làm được

Vòng sóng âm sau đầu AI tĩnh; phụ đề ô chữ nhật (mẫu bo tròn); máy phần 1 đứng yên; cảnh sát không lùi ra khung rộng; cảnh ngoài cabin đứng yên.

## Nhật ký chạy

- 05/11/2026: tạo thể loại, `kiem-tra` 0 lỗi / 3 cảnh báo (fx, giữ). Chờ ảnh tham chiếu AI của người dùng trước khi gen.
- 05/11/2026: chạy thử `bien-the-01-goc` KHÔNG refs (dự án `Xe-tai-canh-sat-gia-su-AI-031a`), `final.mp4` 82,4 s. Phần 1 đạt. Phần 2 chưa đạt: ô AI che trán–mũi tài xế
  (`base_HOC` đầu quá cao), thú bông + chữ "YETI" trên bảng tên, vệt vỡ đáy ô AI do khoá camera trong `split.py` (xem nhật ký tri thức). Video dài hơn mẫu ~1,6 lần.
- 05/11/2026: sửa khoá camera (`split.py`, dùng chung), đầu tài xế, phụ đề y 1560, đổi gia sư AI sang robot Talka (refs). Làm lại từ cảnh 10: 13 cảnh phần 2 đạt (robot đúng ảnh, ô AI đứng yên, đáy sạch, mặt tài xế dưới ô).
