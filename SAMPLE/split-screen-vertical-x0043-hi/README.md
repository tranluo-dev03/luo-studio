# Split screen vertical · X0043 · bản tiếng Hindi (Ấn Độ), 20 biến thể (`split-screen-vertical-x0043-hi`)

Chia đôi DỌC (robot gia sư AI nửa trái, người học ngồi bàn cà phê nửa phải, ghép 2 lớp), lời thoại tiếng Hindi (chữ Devanagari); "How old are you?", "I have N", "I am N", "Talka AI", "AI Tutor" giữ tiếng Anh. Từ bảng `X0043_20-bien-the-split-screen-HINDI.csv`.

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-DOI-GIA-SU-AI-HI.txt` | Kịch bản, `loai: chia-doi-gia-su-ai-hi` |
| `BIEN-THE-X0043-HI-20.json` | 20 biến thể (10 nữ, 10 nam), ảnh robot + ảnh nhân vật gắn sẵn |
| `X0043_20-bien-the-split-screen-HINDI.csv` | Bảng gốc |
| `anh/nhan-vat/bien-the-01..20.webp` | 20 ảnh tải từ link Drive trong CSV |
| `cong-cu/tao_bien_the.py` | Sinh lại JSON (bảng `BIEN_THE`, hàm `luot(n, gioi)`) |

Code riêng: `app/production/types/chia-doi-gia-su-ai-hi/` (hậu kỳ như `chia-doi-gia-su-ai`, thêm font Nirmala UI cho chữ Devanagari và whisper `small` đa ngôn ngữ).

## Tuổi nói theo biến thể (I have N / I am N)
BT1 21, BT2 24, BT3 27, BT4 30, BT5 34, BT6 39, BT7 46, BT8 54, BT9 63, BT10 71, BT11 22, BT12 26, BT13 29, BT14 33, BT15 38, BT16 43, BT17 50, BT18 58, BT19 66, BT20 75.

## Quyết định đã chốt
- Lượt 12: nữ "मज़ाक कर रही हो ना?", nam "मज़ाक कर रहे हो ना?" (CSV chỉ có dạng nữ).
- Lượt 13 rút còn 18 từ (bản gốc 25 từ vượt giới hạn 20): "नहीं, बिल्कुल सच! असली AI अवतार के साथ कभी भी, कहीं भी जितनी चाहें अंग्रेज़ी बातचीत की प्रैक्टिस करें।"
- Bối cảnh và đồ trên bàn kiểu Ấn Độ (quán chai, tranh Madhubani, kulhad masala chai, samosa) thay cho bản Mexico.
- Mô tả CSV bỏ nửa dưới (dhoti, ghagra, giày, sari phần dưới) vì cảnh ngồi chỉ thấy từ ngực trở lên; khăn, mũ, turban, odhni giữ.

## Chưa kiểm tra
Chưa gen thật: cần nghe thử giọng Hindi, xem phụ đề Devanagari (font Nirmala UI, cỡ 56) có ghép đúng chữ và vừa ô không.
