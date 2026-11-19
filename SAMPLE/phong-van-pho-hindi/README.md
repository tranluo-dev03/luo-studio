# Thể loại `phong-van-pho-hindi`: phỏng vấn đường phố rồi chia trên/dưới + gia sư AI, tiếng Hindi xen tiếng Anh

Video mẫu `1510_interview street hindi_005 (11).mp4` (76,9 giây, app Aiva AI; tên file ghi "hindi" nhưng phụ đề gốc là Malayalam), cùng khuôn với
[phong-van-pho-malayalam](../phong-van-pho-malayalam/README.md). Bản này viết lời bằng **tiếng Hindi (chữ Devanagari) xen từ tiếng Anh** (ngôn ngữ yêu cầu: india).
Phân tích video mẫu: xem [PHAN-TICH-VIDEO-MAU.md của malayalam](../phong-van-pho-malayalam/PHAN-TICH-VIDEO-MAU.md) (số đo y hệt: 9 cảnh cắt, giọng 211/254 Hz, máy đứng yên).

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Phỏng vấn | 1–11 | cảnh thường, MỘT góc qua vai, camera đứng yên | Phóng viên nam (PV) quay lưng mép trái cầm micro; người bán nữ (HOC) sau quầy hàng đúng nghề |
| 2. Chia trên/dưới | 12–26 | ghép 2 lớp, cắt cứng khi vào phần | Robot Talka ô trên, người bán selfie ô dưới; sửa "I am <thành phố>" → "I am from <thành phố>" |

| File | Nội dung |
|---|---|
| `KICH-BAN-PHONG-VAN-PHO-HINDI.txt` | Kịch bản 2 phần, sinh bằng `cong-cu/tao_kich_ban.py` |
| `BIEN-THE-PHONG-VAN-PHO-HINDI.json` | 3 biến thể, sinh bằng `cong-cu/tao_bien_the.py` (không sửa tay JSON) |
| `cong-cu/gen_anh.py` | Gen ảnh tham chiếu PV + V1/V2/V3 bằng Muse (photoreal, nền xanh lục phẳng); `[PV V1 ...]` để gen riêng |
| `anh/robot-talka.png` | Robot Talka (ảnh của người dùng, như thể loại Malayalam); `anh/khung-phan*-mau.png` chỉ để so bố cục |
| `PROMPT-CHO-AGENT.txt` | Quy tắc viết thêm biến thể |

Code riêng: `app/production/types/phong-van-pho-hindi/` (`gen.py`, `post.py`, `config.json`), chép từ malayalam.

## Biến thể (3)

| # | Người bán | Quầy | Thành phố (câu sai/sửa) |
|---|---|---|---|
| 01 `bam-sat-video` | nữ ~50, sari nâu kẻ, áo hồng, bindi đỏ, găng nilon | xe đẩy inox nhiều nồi (như video mẫu) | Lucknow |
| 02 `nguoi-ban-tre-puri` | nữ ~28, kurta vàng + dupatta xanh, tóc bím | quầy puri/pani puri | Jaipur |
| 03 `nguoi-ban-lon-tuoi-trai-cay` | nữ ~62, tóc bạc búi, sari xanh ngọc, tay không | xe trái cây giỏ đan | Patna |

PV luôn là cùng một nam trẻ (kịch bản tả "his"); người bán luôn nữ để hai người khác giới trong phần 1 (sổ tay 3.2).

## Quyết định đã chốt (17/11/2026, chạy ngầm)

- Khuôn: nhiều phần, đổi cơ chế ở 25,7 s; không đổi bố cục/góc máy video gốc. Mẫu dùng lại: `phong-van-pho-malayalam`.
- Chọn khuôn ghép 2 lớp (an toàn hơn cửa sổ gọi video to): không bao giờ hai người cùng nói trong một ô.
- Lời viết lại bằng Hindi theo đúng mạch/nhịp; "ba tháng" → "một tháng" như bản malayalam; từ Anh viết Latin; `fx: none` mọi lượt.
- `gen.py` (riêng thể loại): đếm âm tiết Devanagari để chọn độ dài clip (gen_video chỉ đếm Latin + Malayalam); `voice_span` theo năng lượng cho câu `hi`;
  speedfix tắt, cắt sát theo lời, không tua nhanh (người dùng đã cấm ở malayalam).
- Phụ đề: font Nirmala UI + `shaping: complex` (nguyên âm Devanagari đúng chỗ), chữ đen ô trắng, như malayalam.
- Không sửa mã dùng chung; `gen_anh.py` bọc `_chung/gen-anh-nhan-vat.py` và đổi STYLE sang photoreal (script chung mặc định hoạt hình Pixar).

## Trạng thái (phân tích lại 17/11/2026)

- Phân tích lại video `23be8c7e-1510_interview-street-hindi_005-11-onlin.mp4`: số đo y hệt bản đầu (9 cảnh cắt, giọng 211/254 Hz, máy đứng yên, đổi cơ chế ở 25,7 s); đã xem toàn bộ tong-quan/chuyen-dong. Cấu trúc kịch bản giữ nguyên, **không đổi kịch bản**.
- Chi tiết mới: robot trong video gốc đeo tai nghe trắng có mic và có chữ "AI" trên trán, ô dưới/ô trên ngăn bằng vạch cam. Đã thêm tai nghe + mic vào `NGUOI_DAY` (tao_bien_the.py); không thêm chữ "AI" (quy tắc không chữ trong hình); vạch cam vẫn chưa có.
- Muse đã có tài khoản: gen xong `anh/PV.png`, `V1.png`, `V2.png`, `V3.png` (đã xem: một người, nền xanh phẳng, không chữ; V3 trông hơi già hơn 62 tuổi, chấp nhận).
- `kiem-tra`: 0 lỗi, 0 cảnh báo. Dự án cũ `Interview-street-Hindi---Talka-d288` sửa tại chỗ (PUT: biến thể mới + refs ảnh), không tạo dự án trùng.
- Chạy thử biến thể 01: cảnh 1–2 xong, `phan1/scene1_start.png` đạt (PV quay lưng, không lộ mặt, người bán nhìn PV). Chưa nghe Hindi; cần người dùng duyệt.
- Việc còn lại: nghe cảnh 1–3 (Hindi, người bán có nhép theo PV không), xem `phan2/base_DAY.png` (robot có tai nghe chưa), chọn Thương hiệu (logo Aiva AI, Outro).

- Phân tích lại lần 2 (cùng ngày, file `23be8c7e-...`): `danh-gia` cho kết quả y hệt (15 lượt, giọng A 211 Hz / B 254 Hz, 10 đoạn máy đứng yên trừ 22,6–25,7 s rung nhẹ, đổi cơ chế ở 25,7 s). `kiem-tra` lại: 0 lỗi, 0 cảnh báo. Không có gì mới để sửa nên **không đổi kịch bản/biến thể/dự án, không gen lại**. Dự án `Interview-street-Hindi---Talka-d288` giữ nguyên; lượt chạy thử biến thể 01 đã gen xong cảnh 1–3 (`phan1/scene1-3_clip.mp4`), không bị chạy lại.

## Rủi ro / còn khác video mẫu

- **Muse nói Hindi: chưa kiểm chứng**; câu Hindi không được kiểm lời từng chữ (phải nghe tay). Whisper không căn được chữ Devanagari: phụ đề rải theo độ dài chữ nếu Whisper không trả lời.
- Phóng viên quay lưng là người nói: Muse có thể xoay mặt anh ra camera hoặc cho người bán nhép theo (xem cảnh 1, 3, 5, 9).
- Câu một từ ("Suddenly.", "तुरंत?") rất ngắn: Muse có thể nói thêm chữ.
- Chưa có vạch cam giữa hai ô, chữ "AI" trên trán robot, tai nghe robot (ảnh Talka không có); phụ đề theo câu, phần 2 cụm ≤ 3 từ.
- Bỏ 2 cảnh chèn cận mặt người bán và rung cầm tay cuối phần 1 (như malayalam).

## Nhật ký

- 17/11/2026: chạy ngầm từ Studio; tạo thể loại, kiểm tra 0 lỗi, nhập Studio; gen ảnh thất bại vì Muse không có tài khoản (xem NHAT-KY-TRI-THUC.md).
