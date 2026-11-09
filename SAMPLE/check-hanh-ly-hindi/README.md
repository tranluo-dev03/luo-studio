# Thể loại `check-hanh-ly-hindi`: check hành lý ở sân bay + gia sư AI, tiếng Gujarati xen tiếng Anh

Nhân bản từ `soi-hanh-ly-gia-su-ai` (08/11/2026) rồi sửa theo video mẫu `oder 6.mp4` (111 giây, quảng cáo app Supernova AI). Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng: `app/production/types/check-hanh-ly-hindi/` (`gen.py`, `post.py`, `config.json`), gọi `types/_chung/`.

> Tên thư mục là "hindi" theo yêu cầu, nhưng video mẫu nói **Gujarati** (phụ đề chữ Gujarati); người dùng đã chọn giữ Gujarati như video.

## Dạng video: MỘT dự án, hai phần

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Check hành lý | 1–17 | cảnh thường, 2 nhân vật, **một góc máy đứng yên** (như video mẫu: 56 s không cắt, không lia). Chỉ cảnh 1 có `Prompt ảnh`; cảnh 2–17 nối khung cuối | nhân viên an ninh (`CANBO`, trái, khuỷu tay tì máy soi) chỉ túi trong khay xanh, thử tiếng Anh, khen; người phụ nữ ~60 mặc sari (`HOC`, phải) kể luyện nói với Supernova AI |
| 2. Người phụ nữ + gia sư AI | 18–34 | **ghép 2 lớp**: người phụ nữ đứng giữa sảnh nhìn ống kính (nền 9:16), robot AI (`DAY`) ô bo góc viền trắng góc trên phải | "I have 62" (❌) → AI sửa → "I am 62" (✅); giới thiệu, giá, kêu gọi tải app |

Ô robot: `khung DAY: 0.662, 0.013, 0.300, 0.253` (đo trên video mẫu), bo góc 0,03, viền trắng 4 px. Nhoè 0,5 s vào phần 2.

## Đã sửa so với `soi-hanh-ly-gia-su-ai`

| Mục | soi-hanh-ly-gia-su-ai | check-hanh-ly-hindi |
|---|---|---|
| Ngôn ngữ | tiếng Anh | 12 giây đầu tiếng Anh, sau đó Gujarati xen tiếng Anh (`Voice:` ghi rõ từng cảnh) |
| Nhân vật | người mẹ Latin địu con, nhân viên Latin | phụ nữ Gujarati ~60 tuổi mặc sari, đeo túi da; nhân viên an ninh Ấn Độ trẻ, gi-lê navy; không em bé |
| Phần 1 | 13 cảnh, 3 góc máy, cú lia, đoạn mở đầu vali trôi, ảnh tổng quan | 17 cảnh, 1 góc máy khoá, không lia/không mở đầu/không ảnh tổng quan |
| Đạo cụ | vali xanh + vali nâu trên băng chuyền, điện thoại | khay nhựa xanh (`DAO_KHAY`) + túi da nâu (`DAO_VALI`), túi đeo vai (`DAO_TUI`); không điện thoại |
| Phần 2 | người mẹ quay selfie | người phụ nữ đứng nhìn ống kính, tay nắm quai túi |
| Robot | robot nữ trắng, nền trắng có vòng sáng | robot trắng mặt trẻ con, tai tròn, đèn ngực xanh, nền xanh dương đậm |
| Ô robot | 0.691, 0.025, 0.284, 0.258, không viền | 0.662, 0.013, 0.300, 0.253, viền trắng |
| Phụ đề | trắng viền đen / vàng (AI), y 1125, Arial | chữ đen trên ô trắng cho mọi người, y 1565, font **Nirmala UI** (Arial không có chữ Gujarati) |
| Whisper hậu kỳ | `small.en` | `small` (đa ngôn ngữ) |
| Tuổi câu sửa lỗi | 48 | 62 (biến thể 2: 58) |

## File

| File | Dùng làm gì |
|---|---|
| `KICH-BAN-CHECK-HANH-LY-HINDI.txt` | Kịch bản: `[HAU KY] loai: check-hanh-ly-hindi` + PHAN 1 (17 CẢNH) + PHAN 2 (`[GHEP HAI LOP]`) |
| `BIEN-THE-CHECK-HANH-LY-HINDI.json` | 2 biến thể, 34 lượt: (1) bám sát video (sari xanh, 62 tuổi), (2) đổi nhân vật (sari tím, kính, 58 tuổi) |
| `cong-cu/tao_kich_ban.py` | Sinh kịch bản từ bảng `SC` 17 cảnh. Sửa ở đây rồi chạy, không sửa tay `.txt` |
| `cong-cu/tao_bien_the.py` | Sinh biến thể: lời thoại (Gujarati chép từ phụ đề video), tên app một chỗ (`APP`), tuổi theo từng biến thể |
| `PHAN-TICH-VIDEO-MAU.md` | Số đo, bố cục, bảng hành động, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc riêng để agent viết biến thể mới |

## Chạy trong Studio

1. **Khởi động lại Studio** (lần đầu sau 08/11/2026: `engine.py` có sửa để nhận câu Gujarati).
2. Nhập: `.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\check-hanh-ly-hindi\KICH-BAN-CHECK-HANH-LY-HINDI.txt SAMPLE\check-hanh-ly-hindi\BIEN-THE-CHECK-HANH-LY-HINDI.json --ten-loai "check-hanh-ly-hindi" --ten-du-an "check-hanh-ly-hindi"` (thêm `--chay-thu` để chạy biến thể 1).
3. **Gắn ảnh tham chiếu mặt** (`refs`) cho `NGUOI_HOC` (và nên có `NGUOI_CANBO`): phần 1 và phần 2 là hai ảnh gen khác nhau, không có ảnh tham chiếu thì mặt người phụ nữ dễ lệch giữa hai phần.
4. Thương hiệu: logo app (nếu muốn), Outro nếu cần end card (video mẫu không có).
5. Chạy thử MỘT biến thể; xem `phan1/scene1_start.png` (tay chỉ đúng túi, khay xanh ở dưới, không chữ trên biển), clip cảnh 1–2, `phan2/base_HOC.png`, `phan2/base_DAY.png` trước khi chạy cả nhóm.

## Code chung đã sửa (08/11/2026, phục vụ thể loại này, không đổi hành vi thể loại khác)

- `app/luo-studio/engine.py`: `speech_lang` trả `gu`/`hi` khi câu có chữ Gujarati/Devanagari (Whisper đa ngôn ngữ cho `voice_span`); `speech_issues` bỏ kiểm từng chữ cho câu đó (trước đây chỉ giữ chữ Latin → báo thừa/thiếu sai, gen lại vô ích). Câu thuần tiếng Anh kiểm như cũ.
- `app/production/types/_chung/hau_ky.py`: đọc `phu_de.font` trong `config.json` (mặc định Arial như cũ).
- Bản sao trước khi sửa: thư mục scratchpad của phiên (không nằm trong repo).

## Đã kiểm tra / chưa kiểm tra

- `video-moi.py kiem-tra`: 0 lỗi, 1 cảnh báo ("[NHAN VAT HOC] chưa nói đầu nằm dưới ô"): giữ, vì ô robot chỉ chiếm 30% bên phải, đầu người phụ nữ ở giữa-trái như video mẫu (không nằm dưới ô); kịch bản đã ghi "đầu luôn ở bên trái góc đó".
- `nhieu_phan.plan`: 2 phần, 17 + 17 = 34 cảnh, cả 2 biến thể. Cảm xúc đều trong `EMO_CUES`. Lượt dài nhất 20 từ.
- Phụ đề: đốt thử chữ Gujarati + ô trắng + ❌ bằng `phu_de.burn` với font Nirmala UI: hiển thị và ghép chữ đúng.
- **Chưa chạy thật trên Muse** (chờ ảnh tham chiếu nhân vật).

## Rủi ro

- Muse nói Gujarati: chưa kiểm chứng; nếu đọc sai/lơ lớ, cân nhắc viết lời Gujarati bằng chữ Latin (phiên âm) trong `text` và giữ chữ Gujarati cho phụ đề (cần thêm trường riêng).
- Kiểm lời từng chữ tắt với câu Gujarati → câu nói lặp/thiếu không tự gen lại; nghe lại clip.
- 17 cảnh nối khung liên tiếp cùng một góc: tư thế/ánh sáng có thể trôi dần; lệch thì "Chỉ làm lại cảnh này" từ cảnh đầu tiên lệch.
- Biển treo có hình máy bay: Muse có thể vẽ thêm chữ → gen lại cảnh 1.

## Còn khác video mẫu

- Phụ đề hiện cả câu (video: cụm 2–4 từ).
- Có ❌/✅ + viền màu ở nhịp sửa lỗi (video không có).
- Chuyển phần bằng nhoè thay cắt cứng.
