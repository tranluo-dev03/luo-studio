# Thể loại `tiem-thit-tieng-anh`: tiệm thịt học tiếng Anh (hoạt hình 3D kể chuyện)

Video mẫu: `0610_Cut meat ES_015_02.mp4` (177 giây, quảng cáo app học tiếng Anh có gia sư AI). Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng: `app/production/types/tiem-thit-tieng-anh/` (chỉ `post.py` + `config.json`; gen dùng chế độ cảnh thường chung).

## Dạng video: MỘT phần, cảnh thường, 46 cảnh (37 có lời + 9 KHÔNG LỜI), 23 góc máy

| Cảnh | Góc | Nội dung |
|---|---|---|
| 1–5 | K (cận khách), A (quầy rộng) | khách khen thịt; ông chú nhận công "20 năm", chê Tavo "không trường, không tiếng Anh", bắt chào |
| 6 | T (cận Tavo) | **không lời** ~3,5 s: Tavo ngơ ngác, hé miệng không ra tiếng (`Cắt còn: 3.5`) |
| 7–10 | B (cận hai chú cháu, nối khung) | "như nói với bức tường"; 2 đồng xu "tiền nước"; Tavo đòi lương; "trả bằng chỗ ở và cơm" |
| 11 | X (lối đi trong chợ) | **không lời** ~4 s: bà chủ nhà hàng vào chợ ráo riết tìm quầy thịt |
| 12–16 | C (phòng sau quầy), D (thớt) | bà cần thịt gấp; Tavo "Yo le ayudo"; "I'm sorry, I don't speak Spanish"; "Aquí, siéntese" vội vã, chộp dao |
| 17–18 | D2 (chặt), Y (tay gói) | **không lời**: chặt thịt rất nhanh (clip 10 s, `Tua: 1.3`), gói giấy hồng thoăn thoắt (`Tua: 1.3`) |
| 19–23 | W (4 gói thịt), E (quầy cân), E1 (cận bà chủ) | "Oh my God. Ten minutes?"; hỏi tên; "Hey, take this app. Talka AI."; "một tháng nữa quay lại" |
| 24–25 | E | **không lời**: bà hôn lên trán Tavo; rồi "You saved me today" (nối khung) |
| 26–31 | N (đêm, cận Tavo), P (điện thoại có robot AI nói) | học "You saved me today"; cảnh 28 Tavo ngỡ ngàng hiểu ra "Me salvaste hoy"; "Again tomorrow?" |
| 32–35 | Q1–Q4 | **không lời** montage nhiều ngày (chớp trắng): chặt thịt nghe bài, quét sạp tối, luyện trong kho, sáng sớm tự tin |
| 36–44 | M, M2 (một tháng sau), F (hai người đối mặt), G (cận Tavo) | ông chú nhận vơ; Tavo nói tiếng Anh, được nhận việc; "Ahora sí me llamo Tavo, tío" |
| 45–46 | H (Tavo nhìn ống kính) | kêu gọi tải app |
| — | — | end card app: Thương hiệu → Outro (không gen) |

**Cảnh không lời**: lượt n của biến thể có `"text": ""` (who = người có mặt) → `{{LUOT_n}}` rỗng, Voice trống; engine tạo clip câm (bỏ SPEAKER MAP, lọc câu nói về giọng), giữ nguyên độ dài clip theo mốc tiêu đề, `Cắt còn: N` giữ N giây đầu, `Tua: K` tua nhanh K lần. Mô tả không được chứa say/speak/talk/voice/lời/nói/giọng (câu chứa chúng bị lọc). Hậu kỳ (`post.py`) map lượt có lời về đúng cảnh.

Khung đầu: cảnh có `Prompt ảnh` sinh ảnh mới; cảnh cùng góc liền sau nối khung cuối (`Khung đầu: Chính là khung cuối của cảnh trước`, giữ đạo cụ như đồng xu); quay lại góc cũ dùng `Khung đầu từ cảnh: N` (3←1, 4←2, 24←20, 28/30←26, 29/31←27).
Biến thể bật `"nguoi_theo_canh": true` (chỉ tả người có tên trong cảnh).

## Phụ đề (`config.json`)
Chữ trắng viền đen ở y 1290; lượt tiếng Anh có `"dich"` → dòng dịch tiếng Tây Ban Nha ngay dưới (kiểu dòng dịch chung: chữ đỏ viền trắng; video mẫu: vàng nghiêng). Whisper `small` (đa ngôn ngữ).

## File
| File | Dùng làm gì |
|---|---|
| `KICH-BAN-TIEM-THIT-TIENG-ANH.txt` | kịch bản (sinh bằng `cong-cu/tao_kich_ban.py`: bảng góc `ANG` + bảng cảnh `S`; sửa ở đó rồi chạy lại) |
| `BIEN-THE-TIEM-THIT-TIENG-ANH.json` | biến thể `tavo-tiem-thit-goc` bám video mẫu, 46 lượt (9 lượt rỗng = cảnh không lời) (sinh bằng `cong-cu/tao_bien_the.py`; tên app ở hằng `APP`) |
| `anh/<KHOÁ>.png` | ảnh tham chiếu nhân vật do người dùng cung cấp (TAVO, TIO, KHACH, CHU; ROBOT mặc định dùng `SAMPLE/soi-hanh-ly-gia-su-ai/ROBOT-GIA-SU-AI.png`). Đặt ảnh vào rồi chạy lại `tao_bien_the.py` → `refs` tự thêm |
| `PROMPT-CHO-AGENT.txt` | quy tắc viết biến thể mới |

## Chạy
```
runtime\python.exe SAMPLE\tiem-thit-tieng-anh\cong-cu\tao_kich_ban.py
runtime\python.exe SAMPLE\tiem-thit-tieng-anh\cong-cu\tao_bien_the.py
runtime\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\tiem-thit-tieng-anh\KICH-BAN-TIEM-THIT-TIENG-ANH.txt SAMPLE\tiem-thit-tieng-anh\BIEN-THE-TIEM-THIT-TIENG-ANH.json --tai-anh
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\tiem-thit-tieng-anh\KICH-BAN-TIEM-THIT-TIENG-ANH.txt SAMPLE\tiem-thit-tieng-anh\BIEN-THE-TIEM-THIT-TIENG-ANH.json --ten-loai "Tiệm thịt học tiếng Anh" --ten-du-an "Tiệm thịt - Tavo" [--chay-thu]
```
Trước khi chạy hết: xem `scene1_start.png` (K), `scene2_start.png` (A), clip cảnh 6 (T, Tavo ấp úng không ra tiếng), `scene7_start.png` (B), clip cảnh 11 (bà chủ đi trong chợ, máy không lia), `scene12_start.png` (C), clip cảnh 17–18 (chặt/gói nhanh), clip cảnh 24 (hôn trán), `scene26_start.png` (N), clip cảnh 27 (robot trên điện thoại), clip 32–35 (montage), `scene36_start.png` (M).

## Quyết định đã chốt (11/11/2026)
- Khuôn: cảnh thường nhiều góc (như `canh-sat-gia-su-ai` phần 1), một phần, không ghép 2 lớp (video mẫu không có ô PiP; AI chỉ xuất hiện trên màn hình điện thoại).
- Giọng AI phát ra từ robot trên màn hình điện thoại (góc P, không thấy mặt Tavo) thay vì giọng ngoài khung trong cảnh cận Tavo: Muse gán giọng cho mặt nhìn thấy.
- Khách chỉ lộ mặt ở góc K (một mình); ở góc A chỉ là vai + gáy → không có hai đàn ông trưởng thành cùng lộ mặt trong một khung.
- Bỏ: cảnh không lời mở đầu (cận tay cắt thịt), khách bỏ đi, ghi tên app vào sổ; giao diện app không gen.
- (11/11, theo góp ý người dùng sau bản 37 cảnh) Thêm lại các cảnh không lời: Tavo ấp úng, bà chủ tìm quầy, chặt + gói thịt nhanh, hôn trán, montage học nhiều ngày; "I'm sorry, I don't speak Spanish"; app đổi thành Talka AI; cảnh 16 vội vã; cảnh 28 Tavo ngỡ ngàng.
- Lời giữ sát video gốc (biến thể đầu).

## Còn khác video mẫu / chưa làm được
- Dòng dịch đỏ viền trắng (mẫu: vàng nghiêng) — cần thêm tuỳ chọn màu dòng dịch vào `_chung/phu_de.py` (code dùng chung, chưa làm).
- Không có chuyển động máy (máy đứng yên mọi cảnh, kể cả montage).
- Màn hình app chỉ là robot, không bong bóng chat/nút.
- Ánh sáng ngày/đêm: Studio cân màu theo cảnh làm chuẩn → cảnh đêm có thể bị kéo sáng; nếu thấy, tắt cân màu ("normalize") cho dự án.

## Lần chạy thử đầu (11/11/2026)
- Ảnh tham chiếu TAVO/TIO/KHACH/CHU gen bằng Muse từ mô tả NGUOI_ (`cong-cu/gen_anh_tham_chieu.py`), người dùng đồng ý gen bằng Muse.
- Dự án Studio "Tiệm thịt - Tavo" (loại "Tiệm thịt học tiếng Anh"), biến thể `tavo-tiem-thit-goc` đang chạy.
- Cảnh 1–2: ĐẠT (khung đầu sát video mẫu, đúng lời, đúng hành động). Cuối cảnh 1 khách hơi xoay mặt về ống kính.
- Chạy xong biến thể đầu 12:39: `userdata/studio/exports/Tiệm thịt - Tavo/tavo-tiem-thit-goc.mp4` (143 s). Đạt: lời cả 37 cảnh, mặt giữ qua 15 góc, cảnh đêm giữ tối, robot trên điện thoại nhép miệng không giao diện.
- Còn sửa được: dòng dịch đỏ nhỏ khó đọc (cần tuỳ chọn màu dòng dịch ở `_chung/phu_de.py`); nền sau điện thoại góc P là quầy thịt thay vì kho tối; cảnh 36–37 màn hình điện thoại có nhãn chữ nhỏ; chưa gắn Thương hiệu/Outro.

## Bản 46 cảnh (11/11/2026, sau góp ý của người dùng)
- Sửa theo 10 góp ý: cắt khoảng im sau "Twenty years, my friend" (lỗi engine nới điểm cắt theo tiếng cười, đã sửa chung), thêm cảnh Tavo ấp úng, bà chủ vào chợ tìm quầy, "I'm sorry, I don't speak Spanish", cảnh 16 vội vã, chặt thịt dài + nhanh và gói thịt nhanh trước "Oh my God, ten minutes", Talka AI, hôn trán trước "You saved me today", Tavo ngỡ ngàng ở "Me salvaste hoy", montage học nhiều ngày sau "Again tomorrow".
- Đã gen thật bản 46 cảnh 11/11: final 172 s, 9 cảnh không lời đạt (xem nhật ký tri thức). Xuất: `userdata/studio/exports/Tiệm thịt - Tavo 46 cảnh/`.

## Bản 50 cảnh (12/11/2026, sau góp ý lần 2)
- 38 cảnh có lời + 12 không lời. Thay đổi so với bản 46 cảnh: cảnh 9 Tavo mặt hướng máy (tránh giọng gán cho ông chú); chặt/gói nhanh hơn (Tua 1,5); 4 gói giấy hồng trên nóc tủ ở mọi cảnh góc E (cảm ơn, hôn trán); montage 7 cảnh x 2,5 s có điện thoại hiện app (góc Q1–Q7); thêm cảnh 41 bà chủ "No, the young guy." (khung đầu từ cảnh 39); bà chủ vui mừng, nhẹ nhàng khi nói với Tavo ở cuối truyện.
- Đã gen 12/11: final 178,7 s. Còn lỗi nhỏ: cảnh 18 lộ đỉnh đầu Tavo ở mép dưới; dòng dịch đỏ nhỏ; chưa Thương hiệu/Outro. Số cảnh trong bảng ở trên là của bản 46 cảnh: cộng thêm 3 cảnh montage và 1 cảnh bà chủ ở các cảnh sau 31.
