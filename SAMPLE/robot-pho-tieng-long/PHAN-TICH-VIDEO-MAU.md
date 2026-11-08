# Phân tích video mẫu: `2610_IG learna AI EN_003_8 (1) (online-video-cutter.com).mp4`

- 25,1 giây, 720×1280, tiếng Anh (Mỹ), quảng cáo app học tiếng Anh (badge "Talka AI" góc trên trái suốt video). Không có end card (video bị cắt ở 25 s; cảnh cắt cứng duy nhất ở 25,0 s là điểm cắt).
- Công cụ: `runtime\python.exe SAMPLE\_chung\video-moi.py danh-gia "<video>" --lang en` → `bao-cao.md`, `danh-gia.md`, `luot_01..12.jpg`, `chuyen-dong_01..03.jpg`, `tong-quan_1..2.jpg` (đã xem từng ảnh).
- **Tốc độ nói:** trung vị 4,0 từ/giây (2,7–5,0); khoảng lặng giữa các câu ~0,8 s. **Camera đứng yên tuyệt đối** (tổng dịch 6 px/160 px cả 25 s, không zoom).
- **Giọng:** một người, 134–186 Hz (trung vị 165 Hz): nữ trung-trầm ấm, tiếng Anh Mỹ, kiểu host vui vẻ, lên xuống giọng rõ, cười trong giọng. Công cụ đếm "2 mặt" ở 80% thời gian là mặt robot + huy hiệu tròn trên ngực/icon badge, không phải người thứ hai.

## Cấu trúc: MỘT phần, MỘT khung, MỘT nhân vật

| Thời gian | Nội dung | Cơ chế Studio |
|---|---|---|
| 0:00–0:25 | Robot nữ (mặt người, đầu trắng, cổ máy, giáp trắng) đội mũ cao bồi nâu, khoác sơ mi denim xanh nhạt, đứng giữa phố cổ Texas lúc hoàng hôn, nhìn thẳng ống kính, dạy 4 từ lóng Texas rồi hỏi người xem | Cảnh thường, 1 nhân vật, 6 cảnh nối liên tục, hậu kỳ riêng vẽ chữ |

## Bố cục (đo trên khung 720×1280 → tỉ lệ)

| Thành phần | Vị trí | Studio |
|---|---|---|
| Robot | đỉnh mũ ~0,12; mặt 0,24–0,37 (cằm 0,37), tâm mặt x 0,50, đầu rộng ~0,22 bề ngang; vai 0,45; huy hiệu xanh trên ngực 0,53; thân bị cắt ở đùi; hai tay buông dọc thân, bàn tay ở hông, gần như không cử động | `[STYLE LOCK]` + `Prompt ảnh` cảnh 1 (đỉnh mũ ~10%, đầu 22%, vai 60%, cắt ở đùi) |
| Badge "Talka AI" | góc trên trái, icon robot + chữ | **Không gen** → Thương hiệu: logo cố định |
| Tiêu đề "F1 IS IN TEXAS / TALK LIKE A TEXAN" | ô xanh chuyển sắc bo góc, x 0,19–0,81, y 0,156–0,227; dòng 1 trắng, dòng 2 xanh nhạt; suốt video | `post.py` (`HAU_KY.tieu_de`) |
| Badge sự kiện "OCT 23-25 / US GRAND PRIX" | ô cam + ô trắng, x 0,15–0,60, y 0,564–0,592; suốt video | `post.py` (`HAU_KY.badge`) |
| Thẻ từ lóng | x 0,15–0,85, y 0,598–0,703: đầu xanh (nhãn nhỏ "TEXANS SAY", từ IN HOA to, đếm "1/4" góc phải), thân trắng ("IT MEANS" + nghĩa). Thẻ hiện đúng lúc robot nói từ; thân hiện "..." cho tới khi robot nói nghĩa; thẻ giữ tới thẻ kế | `post.py` (`HAU_KY.the`, mốc theo Whisper) |
| Phụ đề | cụm 2–4 từ trên ô xanh bo góc, chữ trắng đậm, **từ đang nói đổi sang xanh nhạt**, tâm y ~0,735 | `post.py` (karaoke ASS, mốc từng từ theo Whisper) |

## Bảng hành động (mỗi lượt một dòng; ảnh `luot_NN.jpg`)

| # | Giây | Từ/s | Lời (đã đối chiếu phụ đề trên hình) | Hành động robot | Mắt | Camera | Khung cuối |
|---|---|---|---|---|---|---|---|
| 1 | 0,0–3,8 | 2,9 | F1 is coming to Texas. So let's talk like a Texan. | cười tươi, mở miệng rõ, đầu hơi nghiêng; tay buông | ống kính | yên | đứng thẳng, cười mím |
| 2 | 4,3–4,7 | 2,8 | Howdy. | mở miệng vui, đầu hơi hất | ống kính | yên | cười |
| 3 | 5,3–6,0 | 4,4 | That means hello. | nói, mặt sáng | ống kính | yên | cười mím |
| 4 | 7,1–7,5 | 5,0 | Y'all. | miệng mở tròn | ống kính | yên | cười |
| 5–6 | 8,1–10,3 | 2,7–4,8 | That means you, all of you. | nói, nhắm mắt nhẹ một nhịp rồi mở, đầu nghiêng | ống kính | yên | cười mím |
| 7 | 11,3–11,9 | 3,3 | Fixin' to. | nói, mặt vui | ống kính | yên | cười mím |
| 8 | 12,7–13,8 | 3,6 | That means about to. | nói | ống kính | yên | cười mím |
| 9 | 15,0–15,9 | 4,2 | And bless your heart. | nói ngọt, đầu nghiêng nhẹ | ống kính | yên | cười |
| 10 | 16,7–19,3 | 3,9 | It sounds sweet, but it can mean you poor thing. | nói, mặt tinh nghịch ở nửa sau | ống kính | yên | cười mím |
| 11 | 20,3–21,4 | 4,9 | Would you say y'all? | hỏi, lông mày nhướng | ống kính | yên | cười |
| 12 | 22,1–23,2 | 4,6 | Tell me in the comments. | nói, cười tươi | ống kính | yên | cười mím, đứng yên tới 25 s |

Không có đạo cụ, không ai khác, không đổi góc máy. Khoảnh khắc "chuyển động mạnh" 4,1 s và 15,0 s là robot hất đầu/đổi nét mặt khi bắt đầu từ mới; 24,8 s là điểm cắt video.

## Video gốc → kịch bản

| Video gốc | Kịch bản / biến thể | Ghi chú |
|---|---|---|
| 12 câu, nhiều câu 1–3 từ | **6 lượt** (gộp "Từ. That means nghĩa." thành một lượt): 1 mở đầu, 2–4 ba từ ngắn, 5 từ dài có giải thích, 6 câu hỏi kêu gọi bình luận | Mỗi cảnh 1 lượt ~5 s; thẻ và nghĩa vẫn hiện đúng lúc vì căn theo từ Whisper trong cảnh |
| Lời thoại | Viết lại theo mạch (không chép nguyên văn): "F1 is rolling into Texas…" | Biến thể 1 bám sát video; biến thể 2–3 đổi vùng (Sydney, London) |
| Robot mũ cao bồi + sơ mi denim | `NGUOI_DAY` (robot) + `TRANG_PHUC` (mũ, áo) tách riêng để đổi theo vùng | |
| Phố Texas hoàng hôn | `NEN_PHO`; nền đứng yên, không người qua lại | Đơn giản hoá: dây đèn, người xa → tĩnh và mờ |
| Chữ/thẻ/phụ đề | Toàn bộ do `post.py` vẽ | Muse không vẽ chữ (`[NEGATIVE]`) |
| Badge "Talka AI" | Thương hiệu → logo cố định, trên trái | Studio không vẽ |
| Phụ đề: từ đang nói đổi màu | Có (karaoke ASS) | Khác mẫu: cụm cắt ở dấu câu / tối đa 3 từ, không tay chỉnh từng cụm |
| Huy hiệu xanh phát sáng trên ngực | Tả trong `NGUOI_DAY` | Bị thẻ che một phần như video gốc |
