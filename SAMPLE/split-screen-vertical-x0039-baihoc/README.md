# Split screen vertical · X0039 · BÀI HỌC "Where are you from?", 20 biến thể (`split-screen-vertical-x0039-baihoc`)

Chia đôi DỌC (robot gia sư AI nửa trái, người học ngồi bàn cà phê nửa phải, ghép 2 lớp), lời thoại tiếng Anh. Từ bảng `X0039_20-bien-the-split-screen-BAI-HOC.csv`. Dùng loại hậu kỳ có sẵn `chia-doi-gia-su-ai` (whisper `small.en`).

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-DOI-GIA-SU-AI-BAI-HOC.txt` | Kịch bản (`loai: chia-doi-gia-su-ai`; giọng người học tiếng Anh giọng Brazil) |
| `BIEN-THE-X0039-BAI-HOC-20.json` | 20 biến thể (10 nữ, 10 nam), ảnh robot + ảnh nhân vật gắn sẵn |
| `X0039_20-bien-the-split-screen-BAI-HOC.csv` | Bảng gốc |
| `anh/nhan-vat/bien-the-01..20.webp` | 20 ảnh tải từ link Drive trong CSV (giống hệt 20 ảnh của X0045) |
| `cong-cu/tao_bien_the.py` | Sinh lại JSON (bảng `BIEN_THE`, `PLACE`, hàm `luot`) |

## Lời thoại (15 lượt)
Hi! Are you ready to practice English? / Yes, I'm ready! / Where are you from? / **I am Mexico.** (sai, đỏ) / You should say, I'm from Mexico. / **I'm from Mexico.** (đúng, xanh) / Good job! / Thank you, but who are you? / ... / Just download Talka AI!

## Quyết định cần biết
- CSV ghi quê "Mexico" trong kịch bản nhưng 20 nhân vật gốc Brazil; tôi giữ đúng kịch bản. Muốn đổi quê (vd. "Brazil"): sửa `PLACE` trong `cong-cu/tao_bien_the.py`, chạy lại, nhập lại.
- Cột "Kiểu biến thể" của CSV vẫn ghi "đổi I am 28 thành I am N" (sót từ bản cũ) nhưng kịch bản X0039 không có câu tuổi, nên không áp dụng.
- Bối cảnh quán cà phê và đồ trên bàn kiểu Brazil (như X0045). Mô tả CSV bỏ nửa dưới vì cảnh ngồi chỉ thấy từ ngực trở lên.
