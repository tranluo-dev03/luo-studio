# Thể loại: diễn giả sân khấu + thẻ từ vựng chia đôi gia sư AI (`san-khau-chia-doi-gia-su-ai`)

Video mẫu: `Lurnia_ Learn Language with AI` (89,5 s, 720×1280, tiếng Bồ Đào Nha Brazil xen tiếng Anh, app YayTalk).

| Đoạn video mẫu | Giây | Studio |
|---|---|---|
| Diễn giả đứng sân khấu nói thẳng ống kính ("đừng đáp Me too...", giơ điện thoại) | 0–22 | **Phần 1**, cảnh thường, 7 cảnh (cảnh 1 có Prompt ảnh) |
| Dựng quảng cáo (robot + bảng 3 tuần, cửa hàng app, lưới phụ nữ, đồng hồ 10 phút) | 22–38 | **KHÔNG gen** → Thương hiệu / Video giới thiệu; lời rút gọn vào lượt 6–7 |
| Chia đôi dọc: robot (mũ, kính đen) trái, diễn giả phải, thẻ từ vựng phía trên, 5 vòng | 38–83 | **Phần 2**, ghép 2 lớp (khuôn `chia-doi-gia-su-ai`), 10 lượt; thẻ do `post.py` vẽ |
| End card tải app | 83–89 | **KHÔNG gen** → Outro |

Lượt: 7 (phần 1) + 10 (phần 2: robot "X. Em inglês, Y. Repita comigo." → diễn giả "Y. Y."). Vào phần 2 bằng nhoè 0,5 s.

| File | Nội dung |
|---|---|
| `KICH-BAN-SAN-KHAU-CHIA-DOI-GIA-SU-AI.txt` | Kịch bản 2 phần |
| `BIEN-THE-SAN-KHAU-CHIA-DOI-GIA-SU-AI.json` | Biến thể 01 bám video mẫu (sinh bằng `cong-cu/tao_bien_the.py`) |
| `anh/khung-phan1-mau.png`, `anh/khung-phan2-mau.png` | Khung video mẫu chỉ để so bố cục (không gửi Muse) |

Code riêng: `app/production/types/san-khau-chia-doi-gia-su-ai/` (`gen.py`, `post.py`, `config.json`).
Hậu kỳ: phần 1 phụ đề trắng viền đen giữa khung; phần 2 thẻ (nền PNG + chữ tiếng Anh/ô tô vàng bằng ASS theo mốc từ Whisper `small`); `HAU_KY.the[]` trong biến thể.

## Phân tích (công cụ + xem ảnh)
- 11 câu Whisper, 9 cảnh cắt cứng; giọng: diễn giả ~140–160 Hz, robot ~95–120 Hz (trầm). Whisper `en` nghe lời Bồ thành tiếng Anh sai → dùng `pt` + `en` đối chiếu.
- Chia đôi dọc: vạch giữa nổi 8,4. Thẻ video mẫu ở trên (y ≈ 4–16%); Studio đặt thẻ Ở DƯỚI (y 1520–1775 trên 1920) vì thẻ trên che mặt (16/11/2026).
- Còn khác video mẫu: cảnh tiệc xen 5,8–8,8 s + chữ gạch ngang ✕ (bỏ), đẩy máy nhẹ (bỏ), phụ đề karaoke 1–3 từ (làm theo câu), chấm vàng dưới phiên âm, logo/tab yaytalk trên thẻ (bỏ).

## Rủi ro / cần xác nhận
- **Ai nói câu tiếng Bồ trên thẻ** (robot hay diễn giả) chưa chắc: đo cao độ + miệng mâu thuẫn; kịch bản chọn robot đọc. Nghe lại video mẫu một lần.
- Thẻ + hậu kỳ phần 2 **chưa chạy thử** (chưa có video gen): chạy `post.py` trên bản gen đầu, xem thẻ có che đầu và ô tô vàng có khớp chữ không.
- Cần ảnh AI người dùng: diễn giả (áo blazer kem) và robot (mũ xám, kính đen, áo khoác bomber). Chưa có → chưa gen.

## Nhật ký
- 12/11/2026: phân tích, viết hồ sơ, nhập Studio (chưa chạy thử vì thiếu ảnh tham chiếu).

## 16/11/2026 — 4 bộ biến thể từ CSV người dùng (X0056–X0059)
| File biến thể | CSV | Số | Kịch bản |
|---|---|---|---|
| `BIEN-THE-X0056-X0070-BRAZIL-40.json` | Nhân vật Brazil | 40 (20 nam, 20 nữ) | `KICH-BAN-SAN-KHAU-CHIA-DOI-GIA-SU-AI.txt` (7 cảnh, lời Bồ) |
| `BIEN-THE-X0058-X0072-BRAZIL-ROBOT-40.json` | Brazil + Robot | 40, robot đổi trang phục theo từng biến thể | như trên |
| `BIEN-THE-X0057-X0071-HINDI-20.json` | Hindi | 20 (10 nam, 10 nữ) | `...-6CANH.txt` (6 cảnh, lời Hindi từ CSV) |
| `BIEN-THE-X0059-X0073-MEXICO-40.json` | Mexico | 40 | `...-6CANH.txt` (6 cảnh, lời Tây Ban Nha từ CSV) |
Ảnh tải về `anh/brazil/`, `anh/brazil-robot/` (bien-the-NN + robot-NN), `anh/hindi/`, `anh/mexico/` bằng `cong-cu/tai_anh_csv.py`; file sinh bằng `cong-cu/tao_bien_the_csv.py`. Kịch bản đổi sang token đại từ ({{HE}}, {{HIS}}, {{HIM}}), {{NGON_NGU}}, {{TU_OLHA}}. Hindi: hậu kỳ dùng Nirmala UI + shaping complex. Đã `video-moi.py kiem-tra`: 0 lỗi. CHƯA gen thử.
