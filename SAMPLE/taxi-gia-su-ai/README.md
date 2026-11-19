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

## Bản Ấn Độ: 20 biến thể (sheet X0061, 13/11/2026)
Lời theo sheet (tiếng Anh + Hindi), bối cảnh Mumbai (taxi đen-vàng). Kịch bản riêng vì số lượt/người nói khác bản Mexico.
| Phần | Cảnh | Nội dung |
|---|---|---|
| 1 | 1–6 (A), 7 câm (P) | khách NỮ bắt rẽ trái, tài xế không hiểu, khách chê qua điện thoại |
| 1 | 8–9 (G), 10–11 câm (K, X), 12–13 (M), 14 câm (T) | sếp khen Arjun, trao xe mới; tài xế xin xe (Hindi), sếp: "Learn to talk to the customers first" |
| 1 | 15–16 (L), 17–18 (L2), 19 câm (PH), 20 (L3) | Priya hỏi, bố kể (Hindi), Priya giới thiệu Ava AI |
| 2 | 9 lượt ghép 2 lớp | Ava: "Where are you from?", "I am India" ❌ → "I am from India" ✅, hết tiền 💲, luyện câu đón khách sân bay |
| 3 | 2 (A, T3) | tài xế tự tin chào khách bằng tiếng Anh; "अब मुझे English बोलने से डर नहीं लगता" |

File: `KICH-BAN-TAXI-AN-DO.txt` (`cong-cu/tao_kich_ban_an_do.py`), `BIEN-THE-TAXI-AN-DO-20.json` (`cong-cu/tao_bien_the_an_do.py`), ảnh sếp + Priya `anh/an-do/` (`cong-cu/gen_anh_an_do.py`); tài xế + khách = link Drive trong sheet; Arjun `anh/ARJUN.png`; Ava `canh-sat-gia-su-ai/anh/DAY.png`.
Biến thể 2 (tài xế Arjun Mehta): đồng nghiệp đổi thành Rahul. Phụ đề có chữ Devanagari tự dùng font Nirmala UI (`post.py`).
Studio: loại `Taxi-An-Do-gia-su-AI-07ef`, dự án "Taxi Ấn Độ - 20 biến thể" (`Taxi-An-Do---20-bien-the-05ff`), chạy 4 luồng.

## Bản Mexico: 40 biến thể (sheet X0060, 16/11/2026)
- `cong-cu/tao_bien_the_x0060.py` -> `BIEN-THE-TAXI-X0060-40.json` (taxi-es-01-carlos ... taxi-es-40-adrian); ảnh tài xế/khách tải từ Drive về `anh/x0060/`. Chạy lại với `--khong-tai` để dùng link Drive thay ảnh đã tải.
- Lời thoại giữ nguyên biến thể gốc; khách nữ (BT 11-20, 31-40) đặt `HIS_KHACH`/`HIM_KHACH` = "her" (kịch bản dùng token cho đại từ của khách).
- Đã nhập vào dự án Studio "Taxi - Miguel" (Taxi---Miguel-9d63): gốc + 40 biến thể. Chưa chạy.

## Bản toàn tiếng Anh (17/11/2026, chạy ngầm từ Studio)
- Video tham chiếu `435d2a85-0510_cartoon-turn-car_015_1.mp4` trùng video mẫu của thể loại → chỉ thêm biến thể, không đổi kịch bản/code. Đo lại: 95,1 s, 4,12 từ/giây, 9 cảnh cắt, giọng 133 Hz / 225 Hz.
- `cong-cu/tao_bien_the_tieng_anh.py` -> `BIEN-THE-TAXI-TIENG-ANH.json` (taxi-tieng-anh-01): lời cả gia đình và robot bằng tiếng Anh, không có dòng dịch Tây Ban Nha; cặp sửa lỗi "I am Mexico" -> "I am from Mexico" giữ nguyên.
- Quyết định (chạy ngầm, không hỏi): giữ kịch bản và bố cục gốc (khuôn nhiều phần: cảnh thường + ghép 2 lớp, an toàn nhất, không đổi góc); người dùng không đưa ảnh nên dùng lại ảnh `anh/` của thể loại; KHÔNG gen thử.
- Studio: loại `Taxi-gia-su-AI-a6ce`, dự án `Taxi---English-435d2a85-1800`, chưa chạy. Cần người dùng: chọn Thương hiệu (end card app), duyệt/bổ sung ảnh nhân vật nếu muốn khuôn mặt mới, tick biến thể rồi Thêm vào hàng đợi.

## Bản Ấn Độ: 3 biến thể (17/11/2026, chạy ngầm từ Studio, video `f2be28b2-0510_cartoon-turn-car_015_1.mp4`)
- Video trùng video mẫu của thể loại (đo lại: 95,1 s, 42 câu, 4,12 từ/giây, 9 cảnh cắt, giọng 133 / 225 Hz) → không viết thể loại mới, dùng lại `KICH-BAN-TAXI-AN-DO.txt` (khuôn nhiều phần, không đổi bố cục gốc).
- `cong-cu/tao_bien_the_an_do_3.py` → `BIEN-THE-TAXI-AN-DO-3.json`: taxi-in-3-01-ravi (26 t, khách nữ 30 t), 02-gopal (51 t, khách 54 t), 03-sandeep (36 t, khách nữ doanh nhân 40 t). Lời Anh + Hindi như bản 20 biến thể; sếp, Priya, Arjun, Ava dùng ảnh có sẵn.
- Ảnh tài xế/khách gen bằng Muse (`gen-anh-nhan-vat.py`, 6/6 đạt) vào `anh/an-do-3/` (HOC1-3, KHACH1-3); `tao_bien_the_an_do_3.py` tự gắn refs khi có ảnh. Muốn đổi ảnh: gen lại cùng tên rồi chạy lại script.
- `kiem-tra`: 0 lỗi, 0 cảnh báo (P1 20 cảnh, P2 9 cảnh ghép 2 lớp, P3 2 cảnh). Studio: loại `Taxi-An-Do-gia-su-AI-07ef`, dự án `Taxi-An-Do---3-bien-the-f2be28b2-7236`. Chạy thử taxi-in-3-01-ravi: cảnh 1 ĐẠT (bố cục góc A giữ, khách nói điện thoại, tài xế nghe); các cảnh sau chưa kiểm.
- Cần người dùng: Thương hiệu (end card), duyệt khung đầu/clip cảnh 1 và các cảnh sau của biến thể test, rồi chạy tiếp. Rủi ro như bản gốc (hai nam chung khung ở góc A/G/J).
