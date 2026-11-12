# Split screen vertical · X0045 · bản tiếng Bồ Đào Nha (Brazil), 20 biến thể (`split-screen-vertical-x0045-pt`)

Chia đôi DỌC (robot gia sư AI nửa trái, người học ngồi bàn cà phê nửa phải, ghép 2 lớp), lời thoại tiếng Bồ Đào Nha (Brazil); chỉ "How old are you?", "I have N", "I am N" là tiếng Anh. Từ bảng `X0045_20-bien-the-split-screen-PT.csv`.

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-DOI-GIA-SU-AI-PT.txt` | Kịch bản, `loai: chia-doi-gia-su-ai-pt` (giọng nói Bồ Đào Nha Brazil) |
| `BIEN-THE-X0045-PT-20.json` | 20 biến thể (10 nữ, 10 nam), ảnh robot + ảnh nhân vật gắn sẵn |
| `X0045_20-bien-the-split-screen-PT.csv` | Bảng gốc |
| `anh/nhan-vat/bien-the-01..20.webp` | 20 ảnh tải từ link Drive trong CSV |
| `cong-cu/tao_bien_the.py` | Sinh lại JSON (bảng `BIEN_THE`, hàm `luot(n, gioi)`) |

Code riêng: `app/production/types/chia-doi-gia-su-ai-pt/` (hậu kỳ giống `chia-doi-gia-su-ai`, nhưng căn lời bằng whisper `small` đa ngôn ngữ thay vì `small.en`).

## Tuổi nói theo biến thể (I have N / I am N)
BT1 20, BT2 23, BT3 26, BT4 31, BT5 35, BT6 40, BT7 47, BT8 55, BT9 64, BT10 72, BT11 24, BT12 27, BT13 30, BT14 36, BT15 41, BT16 48, BT17 56, BT18 62, BT19 69, BT20 77.

## Quyết định đã chốt
- Nam (BT 11-20) nói "Obrigado", nữ nói "Obrigada" (CSV chỉ có "Obrigada").
- Lượt 13 rút "Você pode praticar conversas" thành "Pratique conversas" để đủ ≤ 20 từ (22 từ gây cảnh báo).
- Bối cảnh quán cà phê và đồ trên bàn đổi sang kiểu Brazil (tranh dân gian, gạch azulejo, cà phê cafezinho, pão de queijo) thay cho bản Mexico của X0042.
- Mô tả CSV bỏ phần nửa dưới (váy, giày, quần) vì cảnh ngồi chỉ thấy từ ngực trở lên; mũ vành rộng giữ nhưng phải nằm trong khung (kiểm tra `base_HOC.png`).

## Chưa kiểm tra
Chưa gen thật: cần nghe thử cảnh đầu xem Muse nói tiếng Bồ Đào Nha đúng không, và phụ đề căn lời (whisper `small`) có đúng dấu không.
