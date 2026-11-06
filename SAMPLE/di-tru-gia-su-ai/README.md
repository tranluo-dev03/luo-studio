# Thể loại `di-tru-gia-su-ai`: cuộc gọi báo động → cảnh sát hỏi → gia sư AI (tiếng Tây Ban Nha xen tiếng Anh)

Video mẫu: `1410_immigration ES_003 (2) (online-video-cutter.com).mp4` (67 s, quảng cáo app Talka AI). Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng: `app/production/types/di-tru-gia-su-ai/` (`gen.py`, `post.py`, `config.json`), dùng chung `types/_chung/`.

## Dạng video: MỘT dự án, BA phần
| Phần | Cảnh chung | Chế độ | Nội dung |
|---|---|---|---|
| 1. Gọi điện | 1–5 | Cảnh thường, mỗi cảnh MỘT người, mỗi cảnh `Prompt ảnh` mới | Valeria (`AMIGA`, căn hộ cao tầng) báo Diego (`HOC`, trước cửa hàng) đừng về nhà: có agentes de inmigración |
| 2. Cảnh sát | 6–15 | Cảnh thường, 3 khung: rộng hai người (6–8), cận Diego + robot nhỏ trên vai (9–10), rộng + robot (11–15) | Cảnh sát (`CANHSAT`) hỏi; Diego nói sai "I am Mexico", robot chibi (`ROBO`) nhắc, Diego nói lại đúng ✅ |
| 3. Gia sư AI | 16–28 | Ghép 2 lớp: Diego toàn khung (nền), AI (`DAY`) ô dọc bo góc viền trắng góc trên phải `0.615, 0.012, 0.37, 0.32` (→ gen 9:16); vào bằng nhoè 0,5 s | Hỏi đáp, sửa "I am Mexico", hỏi tiền 💰, giới thiệu gia sư AI |

Phụ đề (`config.json`): phần 1–2 chữ trắng, phần 3 chữ vàng; câu sai đỏ (+ viền đỏ), câu đúng xanh + ✅; cụm đúng trong lời robot tô xanh (`to`).

## File
| File | Dùng làm gì |
|---|---|
| `KICH-BAN-DI-TRU-GIA-SU-AI.txt` | Kịch bản (sinh bằng `cong-cu/tao_kich_ban.py`) |
| `BIEN-THE-DI-TRU-GIA-SU-AI.json` | Biến thể (sinh bằng `cong-cu/tao_bien_the.py`; thêm biến thể = thêm dict vào `BIEN_THE`, chỉ ghi khoá muốn đổi) |
| `cong-cu/gen_anh_nhan_vat.py` | Nhờ Muse gen ảnh tham chiếu từ chữ (mô tả lấy từ biến thể 01) → `anh/ai-<amiga|hoc|canhsat|robo|day>.png` |
| `PROMPT-CHO-AGENT.txt` | Quy tắc viết biến thể mới |

## Chạy
```
.venv\Scripts\python.exe SAMPLE\di-tru-gia-su-ai\cong-cu\tao_kich_ban.py
.venv\Scripts\python.exe SAMPLE\di-tru-gia-su-ai\cong-cu\tao_bien_the.py
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\di-tru-gia-su-ai\KICH-BAN-DI-TRU-GIA-SU-AI.txt SAMPLE\di-tru-gia-su-ai\BIEN-THE-DI-TRU-GIA-SU-AI.json --tai-anh
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap <kịch bản> <biến thể> --ten-loai "Di trú + gia sư AI" --ten-du-an "Di tru - Diego" --chay-thu
```
Studio: loại `Di-tru-gia-su-AI-46a2`, dự án `Di-tru---Diego-c294`.

## Quyết định đã chốt
- Ảnh tham chiếu: người dùng cho Claude tự nhờ Muse gen ảnh nhân vật (05/11/2026) → gen từ CHỮ, không dùng khung video mẫu.
- Lời giữ theo phụ đề video mẫu (biến thể 01 "giống hệt"); danh sách biến thể người dùng đưa sau khi duyệt video đầu.
- Cảnh báo `kiem-tra` "fx 8:wrong, 10:right, 19:wrong" giữ: phần 3 gốc AI sửa câu nhưng Diego không nói lại.
- Phần 1→2 cắt cứng (như gốc); 2→3 nhoè.

## Rủi ro
- Phần 2 hai nam cùng khung (Diego ~20 tuổi / cảnh sát ~45): Muse có thể gán nhầm giọng → nghe cảnh 6–15; dự phòng `voice_swap`.
- Robot nhỏ trên vai trong khung người thật: có thể nhép khi người khác nói, hoặc to/nhỏ thất thường.
- Phần 1 cắt xen hai nơi: mỗi cảnh ảnh mới, mặt giữ nhờ refs.

## Còn khác video mẫu
Dòng "POV: …" và badge Talka (Thương hiệu); máy trôi/đẩy ở phần 1–2 → đứng yên; cảnh sát 4 góc → 3 khung; cảnh không lời đầu video bỏ; phụ đề theo câu (gốc chia cụm).

## Nhật ký chạy
- 05/11/2026: tạo thể loại, gen 5 ảnh tham chiếu bằng Muse (đạt, không chữ), `kiem-tra` 0 lỗi / 1 cảnh báo (giữ). Nhập Studio, chạy thử `bien-the-01-goc`.
- 05/11/2026 lượt gen 1 xong (98,3 s): phần 1–2 đạt; phần 3 ảnh nền Diego có robot thừa bay góc trên phải (do STYLE LOCK chung nhắc "CGI robot") → sửa kịch bản (robot chỉ tả trong khối DAY, Diego "the only figure in the whole frame"), làm lại từ cảnh 16; `base_HOC.png` mới sạch.
- 05/11/2026 gen lại phần 3: hết robot thừa; máy tiến dần làm mặt Diego vào ô AI ở cảnh 25 → khoá khoảng cách máy trong khối HOC, làm lại từ cảnh 24.
- 05/11/2026 làm lại từ cảnh 24: mặt Diego vẫn trôi vào ô AI; nguyên nhân là bước khớp/khoá camera của split.py (clip Muse gốc đúng chỗ, bản _khop dời phải + phóng). Cần sửa code chung, chờ người dùng.
