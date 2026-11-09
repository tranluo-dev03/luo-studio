# Thể loại `chia-tren-duoi-marathi`: chia trên/dưới + gia sư AI, tiếng Marathi xen tiếng Anh

Video mẫu `oder 3.mp4` (71,3 giây, quảng cáo app Supernova AI). Khung 9:16 chia **trên/dưới**: robot gia sư AI ô trên, người học ô dưới. AI sửa "I go" thành "I went", người học than tiếng Anh yếu, AI giới thiệu app, kêu gọi tải. Một phần duy nhất, chế độ **ghép 2 lớp**, 21 lượt = 21 cảnh. Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-TREN-DUOI-MARATHI.txt` | Kịch bản (`[GHEP HAI LOP]`, ô trên DAY, ô dưới HOC) |
| `BIEN-THE-CHIA-TREN-DUOI-MARATHI.json` | 1 biến thể bám sát video, sinh bằng script |
| `cong-cu/tao_bien_the.py` | Sửa lời thoại, tên app (`APP`), nhân vật, `refs` ở đây rồi chạy, không sửa tay JSON |
| `PHAN-TICH-VIDEO-MAU.md` | Số đo, bảng hành động, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc viết thêm biến thể |
| `anh/khung-video-mau.png` | Khung video mẫu để so bố cục, KHÔNG gửi cho Muse |

Code riêng: `app/production/types/chia-tren-duoi-marathi/` (`post.py` + `config.json`, chỉ hậu kỳ; phần gen dùng thẳng ghép 2 lớp).

## Quyết định đã chốt

- Khuôn: ghép 2 lớp, không dùng cảnh thường, vì hai nhân vật ở hai vùng tách biệt.
- `nen: DAY`, không phải `HOC`: kiểm tra "ô che mặt nhân vật nền" so toạ độ ảnh gốc với ô; để `nen: HOC` thì mặt người học bị coi là nằm dưới ô DAY, ảnh bị gen lại và dịch xuống oan.
- `khung DAY: 0, 0, 1, 0.531` + `khung HOC: 0, 0.531, 1, 0.469` (đo trên video). Cả hai gen 1:1; ô dưới mất ~8% mỗi mép trên/dưới nên kịch bản đặt đỉnh tóc người học ở 18% ảnh.
- Lời lấy từ phụ đề trên hình. Tốc độ ghi "about 3 words per second" theo lời thật.
- `fx: none` mọi lượt (video không có ❌/✅).
- Hậu kỳ: font Nirmala UI, chữ đen ô trắng, tâm y 958, cỡ 52.
- End card không gen → Outro.

## Chạy trong Studio

Đã nhập ngày 09/11/2026: loại dự án "Chia trên dưới Marathi" (`Chia-tren-duoi-Marathi-e194`), dự án "oder 3 - Supernova Marathi" (`oder-3---Supernova-Marathi-7986`), chưa gen. Nhập lại khi cần:

```
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\chia-tren-duoi-marathi\KICH-BAN-CHIA-TREN-DUOI-MARATHI.txt SAMPLE\chia-tren-duoi-marathi\BIEN-THE-CHIA-TREN-DUOI-MARATHI.json --ten-loai "Chia trên dưới Marathi" --ten-du-an "oder 3 - Supernova Marathi"
```

Trước khi chạy thử:
1. Gắn **ảnh tham chiếu AI** do người dùng cung cấp cho `NGUOI_DAY` và `NGUOI_HOC` (cột `refs` trong `tao_bien_the.py`, chạy lại rồi nhập lại, hoặc gắn trên trang biến thể).
2. Thương hiệu: Outro = end card app, logo nếu muốn.
3. Chạy MỘT biến thể; xem `base_DAY.png`, `base_HOC.png` (đầu đủ, không bị cắt), nghe cảnh 1–3 xem Muse nói Marathi có đúng không, rồi mới chạy cả nhóm.

## Ảnh tham chiếu (09/11/2026)

- Robot: `anh/robot-ai.webp`, người dùng gửi, đầu trắng không tóc (khác robot video mẫu, phòng làm việc phía sau giữ như video). Đã gắn vào dự án.
- Người học: `anh/nguoi-hoc.png`, người dùng gửi (prnt.sc), bác trai Ấn Độ ~65 tuổi, tóc và râu bạc, áo kurta kem, nền xanh lá. Khác video mẫu (chàng trai ~25 tuổi); mô tả và giọng đã đổi theo ảnh. Vẫn là nam nên lời thoại không đổi.
- Đổi ảnh hoặc lời: chạy `cong-cu/tao_bien_the.py` rồi `cong-cu/cap_nhat_studio.py` (đẩy vào đúng dự án cũ).

## Đã kiểm tra / chưa kiểm tra

- `video-moi.py kiem-tra`: 0 lỗi, 0 cảnh báo.
- Đốt thử phụ đề Devanagari + ô trắng trên chính video mẫu: chữ ghép đúng. Câu dài nhất (16 từ) chiếm 4 dòng, mép dưới ô chạm đỉnh ô người học, không che mặt.
- **Chưa chạy thật trên Muse** (chờ ảnh tham chiếu).

## Rủi ro

- **Muse nói Marathi: chưa kiểm chứng** (thể loại Gujarati trước đó cũng chưa chạy thật). Nếu đọc sai, cân nhắc phiên âm Latin trong `text` và cần trường riêng cho chữ phụ đề.
- Studio coi chữ Devanagari là `hi` (cùng dải Unicode), `speech_issues` bỏ kiểm từng chữ → câu nói lặp/thiếu không tự gen lại, phải nghe tay. Whisper căn phụ đề với Marathi có thể lệch mốc.
- 21 clip nối khung: tư thế/ánh sáng có thể trôi dần; lệch thì "Chỉ làm lại cảnh này".
- Lời viết cho người học nam và gia sư nữ; đổi giới phải sửa động từ.

## Còn khác video mẫu

- Phụ đề theo câu, không theo cụm 2–4 từ, không tô đậm dần.
- Bỏ cử chỉ tay của robot.
