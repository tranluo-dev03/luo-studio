# Split screen vertical · X0044 · bản tiếng Bồ Đào Nha, robot đổi trang phục theo biến thể, 20 biến thể (`split-screen-vertical-x0044-botskin`)

Giống X0045 (chia đôi DỌC, lời thoại Bồ Đào Nha Brazil, 20 nhân vật Brazil, nhân vật và tuổi y hệt), khác ở chỗ **robot gia sư AI mặc trang phục riêng cho từng biến thể** (cột "Link ảnh AI" của CSV). Dùng loại hậu kỳ `chia-doi-gia-su-ai-pt` (whisper `small`).

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-DOI-GIA-SU-AI-PT.txt` | Kịch bản (`loai: chia-doi-gia-su-ai-pt`); đã dặn bỏ nền xanh lá trong ảnh robot |
| `BIEN-THE-X0044-BOT-SKIN-20.json` | 20 biến thể (10 nữ, 10 nam), mỗi biến thể: ảnh nhân vật + ảnh robot riêng, mô tả robot theo trang phục |
| `X0044_20-bien-the-split-screen-BOT-skin.csv` | Bảng gốc |
| `anh/nhan-vat/bien-the-01..20.webp` | 20 ảnh nhân vật (giống hệt X0045) |
| `anh/robot-skin/robot-01..20.webp` | 20 ảnh robot, mỗi con một trang phục (nền xanh lá) |
| `cong-cu/tao_bien_the.py` | Sinh lại JSON (`BIEN_THE`, `TRANG_PHUC_ROBOT`, `luot`) |

## Ghi chú
- Mô tả robot (`NGUOI_DAY`) = thân robot chung + trang phục tả từ ảnh robot-skin (bảng `TRANG_PHUC_ROBOT`, xem từng ảnh để đối chiếu). Giọng, bối cảnh Brazil và lời thoại như X0045.
- Tuổi nói: BT1-10 là 20, 23, 26, 31, 35, 40, 47, 55, 64, 72; BT11-20 là 24, 27, 30, 36, 41, 48, 56, 62, 69, 77. Nam nói "Obrigado", nữ "Obrigada". Lượt 13 rút còn 20 từ.
- Mũ vành rộng ở robot BT 4, 7, 8, 12-16, 18, 20 và ở người học: kiểm tra `base_DAY.png` / `base_HOC.png` xem mũ có bị cắt không (mỗi bên chỉ giữ nửa giữa bề ngang).

## Chưa kiểm tra
Chưa gen thật: giọng Bồ Đào Nha, phụ đề, robot có mặc đúng trang phục không.
