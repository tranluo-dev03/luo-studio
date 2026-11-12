# Thể loại `taxi-gia-su-ai`: tài xế taxi + gia sư AI (hoạt hình 3D kể chuyện)

Video mẫu: `0510_cartoon turn car_015_1.mp4` (95 giây, quảng cáo app học tiếng Anh có gia sư AI). Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng: `app/production/types/taxi-gia-su-ai/` (`gen.py`, `post.py`, `config.json`), dùng chung `types/_chung/`.

## Dạng video: MỘT dự án, HAI phần (43 cảnh)
| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1 | 1–6 | cảnh thường, góc A (qua kính chắn gió) | khách vest gọi điện bắt rẽ trái, tài xế không hiểu, lỡ chỗ rẽ, khách chê qua điện thoại |
| 1 | 7 | **không lời** (P) | tài xế một mình nhìn điện thoại đánh giá tệ, chớp đen vào cảnh |
| 1 | 8–9 | G (gara 3 người) | quản lý khen Arjun, rút chìa khoá xe mới |
| 1 | 10–11 | **không lời** (K, X) | cận tay trao khoá; toàn cảnh taxi mới, đồng nghiệp vỗ tay |
| 1 | 12 | J (hai người đối mặt, như gốc) | Arjun chế giễu "Learn to talk to the customers first" |
| 1 | 13 | **không lời** (T) | cận tài xế buồn |
| 1 | 14–16 | L (phòng khách rộng) | con gái hỏi, bố kể không hiểu khách |
| 1 | 17–20 | L2 (sofa) | con động viên; "¿Con quién estás hablando?"; rút điện thoại |
| 1 | 21 | **không lời** (PH) | cận điện thoại có robot, ngón tay chỉ |
| 1 | 22–25 | L3 (sofa, cầm điện thoại) | giới thiệu gia sư AI, "las clases son muy caras", "No necesitas tomar clases" |
| 2 | 26–43 | ghép 2 lớp, ô robot `0.135, 0.03, 0.73, 0.28` (16:9), vào bằng nhoè 0,5 s | hội thoại với robot, sửa "I am Mexico" → "I am from Mexico", "no tengo dinero" 💲, "gratis", "Vamos a hablar inglés juntos" |
| — | — | không gen | end card app: Thương hiệu → Outro |

## Cảnh không lời trong dự án NHIỀU phần (kỹ thuật mới của thể loại này)
`nhieu_phan.py` (dùng chung) bỏ qua lượt `"text"` rỗng, nên cách của `tiem-thit-tieng-anh` (lượt rỗng) không dùng được cho phần 1.
Biến thể đặt `"text": "[KHONG LOI]"` (MARKER) ở lượt của cảnh không lời; `gen.py` của thể loại bọc `engine.run_variant`, đổi đúng MARKER thành chuỗi rỗng ngay trước khi engine chạy
→ engine tạo clip câm (bỏ SPEAKER MAP, `Cắt còn: N`); `post.py` bỏ các lượt MARKER khỏi phụ đề. Không sửa code dùng chung; thể loại khác không bị ảnh hưởng (chỉ lượt có đúng MARKER bị đổi).
Đã thử bằng code thật: phần 1 nhận 25 lượt (5 rỗng ở cảnh 7, 10, 11, 13, 21), phần 2 18 lượt; phụ đề 47 dòng, không dòng MARKER.

## Phụ đề (`config.json`)
Phần 1: ô trắng chữ đen (y 1190) + dòng dịch (câu tiếng Anh → dịch Tây Ban Nha; câu Tây Ban Nha → dịch Anh). Phần 2: chữ vàng viền đen (y 1290), không dịch; ❌/✅ + viền ở cặp sửa lỗi. Whisper `small` (đa ngôn ngữ).

## File
| File | Dùng làm gì |
|---|---|
| `KICH-BAN-TAXI-GIA-SU-AI.txt` | kịch bản (sinh bằng `cong-cu/tao_kich_ban.py`: bảng góc `ANG` + bảng cảnh `S` + khối `PART2`) |
| `BIEN-THE-TAXI-GIA-SU-AI.json` | biến thể `taxi-mexico-goc`, 43 lượt (5 MARKER) (sinh bằng `cong-cu/tao_bien_the.py`) |
| `anh/<KHOÁ>.png` | ảnh tham chiếu HOC, KHACH, QUANLY, ARJUN, CON gen bằng Muse (`cong-cu/gen_anh_tham_chieu.py`, người dùng đồng ý 11/11/2026); robot DAY dùng `SAMPLE/canh-sat-gia-su-ai/anh/DAY.png` |
| `PROMPT-CHO-AGENT.txt` | quy tắc viết biến thể mới |

## Chạy
```
runtime\python.exe SAMPLE\taxi-gia-su-ai\cong-cu\tao_kich_ban.py
runtime\python.exe SAMPLE\taxi-gia-su-ai\cong-cu\tao_bien_the.py
runtime\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\taxi-gia-su-ai\KICH-BAN-TAXI-GIA-SU-AI.txt SAMPLE\taxi-gia-su-ai\BIEN-THE-TAXI-GIA-SU-AI.json --tai-anh
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\taxi-gia-su-ai\KICH-BAN-TAXI-GIA-SU-AI.txt SAMPLE\taxi-gia-su-ai\BIEN-THE-TAXI-GIA-SU-AI.json --ten-loai "Taxi + gia sư AI" --ten-du-an "Taxi - Miguel" --chay-thu
```
Trước khi chạy hết: xem `phan1/scene1_start.png` (A), clip cảnh 1–2 (tài xế có nhép theo khách không), clip cảnh 7 (không lời), `scene8_start.png` (G), clip 10–11, `scene12_start.png` (J: hai người đối mặt), `scene14_start.png` (L), `scene17_start.png`, `scene21_start.png`, `scene22_start.png`, `phan2/base_HOC.png`, `phan2/base_DAY.png`.

## Quyết định đã chốt (11/11/2026)
- Khuôn: nhiều phần như `canh-sat-gia-su-ai` (phần 1 nhiều góc, phần 2 ghép 2 lớp ô ngang trên) + cảnh không lời như `tiem-thit-tieng-anh`. Người dùng yêu cầu ĐỦ cả cảnh không lời.
- Khách và quản lý giữ NAM như video gốc (người dùng chọn, dù đã cảnh báo rủi ro nhép nhầm). Bố cục mọi cảnh giữ như gốc (người dùng bác các góc mình tự đổi).
- Ảnh tham chiếu người gen bằng Muse (người dùng chọn); robot dùng ảnh có sẵn giống robot video mẫu.
- Bỏ: biển "4.9 STARS · TOP DRIVER", chữ trên màn hình điện thoại, chữ "TAXI/NYC" trên xe, đoạn Arjun bỏ đi.
- Thêm câu mở phần 2 "¡Hola! ¿Qué tal tu inglés?" (video gốc vào thẳng "Más o menos").

## Rủi ro Muse
- Hai nam cùng khung: góc A (khách nói, tài xế nghe), góc G (quản lý nói, tài xế + Arjun nghe) → nghe kỹ, dự phòng `voice_swap: true` hoặc đổi giới tính.
- Khung đầu phòng khách đổi 3 góc (L, L2, L3) → mặt con gái giữ nhờ ảnh tham chiếu.
- Cảnh K (cận tay) có thể vẽ thêm mặt người; cảnh X có thể có chữ trên taxi.

## Lần chạy (dự án Studio "Taxi - Miguel", loại `Taxi-gia-su-AI-a6ce`, mục hàng đợi 83bafa6f)
| Lần | Kết quả | Sửa |
|---|---|---|
| 1 | `scene1_start.png` sát gốc, nhưng Muse giữ khung đầu ~1,5 s rồi tự cắt sang bố cục khách ở giữa | (thư mục `taxi-mexico-goc-lan1-loi-cat-goc`) |
| 2 | mình đổi sang góc A2 (khách giữa, tài xế quay lưng) → **người dùng bác**: phải bám bố cục gốc | bỏ A2; góc J qua vai cũng về hai người đối mặt như gốc |
| 3 | cảnh 1–6 ĐẠT (bố cục gốc giữ suốt clip nhờ `Khung đầu từ cảnh: 1` + khoá "ONE continuous shot"); cảnh 7 câm bị điền câu quản lý | lỗi gen.py: hàm bọc `engine.run_variant` đổi MARKER cả ở lệnh gọi gốc → chỉ đổi khi `opts["_part"]`; khởi động lại Studio |
| 4 | phần 1 ĐẠT 25/25 (lời đúng, 5 cảnh câm đúng chỗ, bố cục gốc); phần 2 ĐẠT 17/18 (ghép 2 lớp, ❌/✅, 💲); `final.mp4` 152,9 s | cảnh 28: robot lặp "Where are you? Are you from?…" → gen lại riêng cảnh đó: ĐẠT, `final.mp4` 149,9 s (final cũ: `_cu-canh28/final-lan4.mp4`) |
| — | lệch còn lại: cảnh 22–25 điện thoại sang tay bố, màn hình tối (gốc con gái cầm, màn hình robot); video dài hơn gốc (mỗi cảnh +1–1,5 s) | chờ người dùng quyết |

Quyết định thêm (11/11): KHÔNG tự đổi bố cục/vị trí nhân vật so với video gốc để né rủi ro Muse; mọi cảnh taxi dùng nguyên khung đầu cảnh 1.
