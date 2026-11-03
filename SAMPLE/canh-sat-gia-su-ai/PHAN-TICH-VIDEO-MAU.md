# Phân tích video mẫu: `AQM2PsNIOcAQusw…pqPw.mp4` (cảnh sát chặn xe + gia sư AI, hoạt hình 3D)

- 63,9 giây, 9:16, tiếng Anh (một câu tiếng Tây Ban Nha), phong cách **hoạt hình 3D kiểu phim chiếu rạp** (mắt to, da mịn, ánh hoàng hôn). App quảng cáo: **LangLearn**.
- Đã chạy `SAMPLE/_chung/phan-tich-video.py` (Whisper gộp cả video thành 3 câu vì lời liền nhau; đã chạy thêm Whisper theo từng từ để lấy mốc) và xem từng ảnh `tong-quan_N.jpg`, `chuyen-dong_NN.jpg`.
- Cảnh cắt cứng: 2,1 / 4,2 / 5,5 / 6,8 / 9,0 / 12,4 / 14,8 / 16,4 / 18,6 / 21,6 / 23,9 / 26,7 / 27,9 / 28,9 (chuyển sang phần 2) / 60,6 (end card).
- **Tốc độ nói:** phần 1 chậm, có ngập ngừng (~2,5–3 từ/giây); phần 2 ~3 từ/giây.

## So với thể loại đã có

| | Video này | Đã có |
|---|---|---|
| Cấu trúc | Phần 1 tình huống → Phần 2 ghép 2 lớp người dùng + AI → end card | **Giống `san-bay-gia-su-ai`** (cùng cơ chế 2 phần, cùng code `types/_chung/nhieu_phan.py`) |
| Phần 2 | AI trong ô bo góc viền trắng phía trên, tài xế toàn khung | **Chính là video gốc của mẫu `ghep-hai-lop`** (cùng lời thoại, cùng bố cục `khung DAY: 0.02, 0.015, 0.96, 0.32`) |
| Khác `san-bay-gia-su-ai` | Hoạt hình 3D (không phải người thật); phần 1 có **3 nhân vật** (thêm bé gái phiên dịch) và **nhiều góc máy** (4 góc, cắt liên tục); phụ đề kiểu khác (ô vàng chữ đen; phần 2 ô đen chữ xanh ngọc / ô trắng chữ đen, tô màu từng từ sai/đúng); không có dòng dịch | `san-bay`: người thật, 2 nhân vật, một khung qua vai, phụ đề chữ có viền + dòng dịch |
| Khác `canh-sat-nu` | Cùng chủ đề cảnh sát chặn xe nhưng là hoạt hình, có con gái, nhiều góc máy và có phần ghép AI | `canh-sat-nu`: người thật, một khung cố định, không phần AI |

## Cấu trúc

| Phần | Thời gian | Nội dung | Trong LUO Studio |
|---|---|---|---|
| 1. Cảnh sát chặn xe | 0:00–0:28,9 | Cảnh sát nữ hỏi tài xế chạy quá tốc độ; tài xế ấp úng vì kém tiếng Anh; con gái nhỏ đỡ lời, dịch sang tiếng Tây Ban Nha; tài xế đưa giấy tờ; cảnh sát dặn rồi đi; tài xế ước nói được tiếng Anh; bé khoe học 3 tuần với LangLearn, đưa điện thoại | Phần 1 của kịch bản: cảnh thường, 12 cảnh, **mỗi cảnh có `Prompt ảnh` riêng** (đổi góc máy) |
| 2. Tài xế + gia sư AI | 0:28,9–0:60,6 | Gia sư AI hỏi, tài xế nói sai 2 lần ("I go to home", "I am very hurry"), AI sửa; hỏi giá, app miễn phí; tài xế hứa tải app | Phần 2: **ghép 2 lớp** (gen riêng video tài xế và video AI rồi ghép) |
| 3. End card | 0:60,6–1:03,9 | Logo LangLearn, "Best Language Learning App", nút App Store / Google Play, ảnh robot + người phụ nữ; giọng: "Best language learning app. Download now." | Không gen: Thương hiệu → Outro |

## Góc máy phần 1 (4 góc lặp lại)

| Góc | Mô tả | Ai trong khung |
|---|---|---|
| A | Từ trong xe, sau vai tài xế (thấy mép tóc xoăn ở mép trái), nhìn ra cửa sổ: cảnh sát đứng ngoài, cúi vào | cảnh sát |
| B | Từ ngoài cửa sổ tài xế nhìn vào xe: tài xế cầm lái gần, bé gái ngồi ghế trẻ em phía ghế phụ | tài xế + bé |
| C | Cận mặt tài xế từ phía ghế phụ (mồ hôi, mặt lo) | tài xế |
| D | Cận bé gái trong ghế trẻ em | bé |

Video gốc còn có: cảnh rộng mở đầu (xe đỏ đỗ lề, cảnh sát đi tới từ xe tuần tra, 0–2,1s), cảnh cảnh sát quay lưng đi về xe (chữ POLICE sau lưng, 21–21,6s), cảnh hai bố con chụm đầu xem điện thoại (27,9–28,9s).

## Bảng từng cảnh

Ký hiệu: **CS** cảnh sát nữ, **TX** tài xế (bố), **BE** bé gái, **AI** gia sư AI.

| # | Thời gian | Góc máy | Nhân vật / hướng / hành động | Hiệu ứng, chữ | Voice (nguyên văn) |
|---|---|---|---|---|---|
| 1 | 0:00–2,1 | Rộng, ngoài đường: xe đỏ bên trái, CS đi tới từ xe tuần tra phía sau, sa mạc hoàng hôn | CS bước tới, cúi vào cửa sổ | — | (CS bắt đầu) "Do you…" |
| 2 | 2,1–4,2 | A (sau vai TX) | CS cúi ở cửa sổ, nhìn TX | Ô vàng chữ đen | CS: "Do you know you were speeding?" |
| 3 | 4,2–5,5 | B | TX quay ra cửa sổ, mặt lo; BE im | — | TX: "Yes." |
| 4 | 5,5–6,8 | A cận | CS nói, nhìn vào xe | Ô vàng | CS: "License and registration, please." |
| 5 | 6,8–9,0 | C cực cận | TX đổ mồ hôi, mắt đảo, ấp úng | Ô vàng | TX: "Uh… I… I… I…" |
| 6 | 9,0–12,4 | D | BE nhìn ra cửa sổ, nói lễ phép | Ô vàng | BE: "Officer, sorry. He's nervous and his English isn't very good." |
| 7 | 12,4–14,8 | A | CS nhìn BE, hỏi lại | Ô vàng | CS: "Does he have his license and registration?" |
| 8 | 14,8–16,4 | D (góc khác, có vai bố) | BE quay sang bố, nói tiếng Tây Ban Nha | Ô vàng | BE: "Tu licencia y los papeles del carro." |
| 9 | 16,4–18,6 | B | TX lấy ví/giấy tờ, chìa ra cửa sổ, tay CS đưa vào nhận | — | — |
| 10 | 18,6–21,6 | A | Tay TX đưa giấy tờ, CS nhận, xem, rồi dặn; CS quay lưng đi về xe tuần tra | Ô vàng | CS: "All right. … Slow down next time." |
| 11 | 21,6–23,9 | B | TX thở phào, quay sang con gái | Ô vàng | TX: "I wish I could speak English like you." |
| 12 | 23,9–26,7 | D | BE giơ điện thoại có màn hình app, nói tự hào | Ô vàng | BE: "Three weeks with LangLearn. Real conversations every day." |
| 13 | 26,7–27,9 | C | TX cầm điện thoại, cười tươi | Ô vàng | TX: "Really?" — BE: "Yep." |
| 14 | 27,9–28,9 | Cận hai bố con chụm đầu xem điện thoại | BE chỉ màn hình | Ô vàng | BE: "Let me show you." |
| — | 28,9–29,1 | Nhoè chuyển động (whip blur) | — | Chuyển cảnh | — |
| 15 | 29,1–60,6 | Ghép 2 lớp: ô AI bo góc viền trắng phía trên (nền đen, vòng sóng âm trắng phát sáng, AI chống cằm); TX toàn khung từ camera trên taplo, hai tay cầm vô lăng, nhìn camera | AI và TX xen kẽ | Phụ đề ngay dưới ô AI: AI **chữ xanh ngọc trên ô đen**, TX **chữ đen trên ô trắng**. Câu sai: từ sai **tô đỏ**, ❌ đỏ, **viền đỏ** nháy toàn khung. Câu sửa đúng: từ đúng **tô xanh**, ✅, **viền xanh lá**. 💰 ở câu "moneys" | AI: "Where are you going?" — TX: "I go to home." ❌ — AI: "You mean: 'I'm going home'?" — TX: "Yes. I'm going home." ✅ — TX: "I am very hurry." ❌ — AI: "I'm in a hurry, is the correct way to say that." — TX: "Oh, okay. Thank you. Wait, who are you?" — AI: "I'm an AI tutor and I'm here to help you practice your English and eventually get better at speaking." — TX: "But I don't have moneys." 💰 — AI: "It's I have no money, but don't worry, LangLearn is a completely free app." — TX: "Seriously?" — AI: "We can practice English anytime, anywhere. Just download LangLearn." — TX: "I will download now. Thank you so much." |
| 16 | 60,6–63,9 | End card tĩnh nền sao đêm | — | Logo, chữ, nút cửa hàng | "Best language learning app. Download now." |

### Giải thích các khoảnh khắc chuyển động mạnh
1,9–2,4; 3,9–4,4; 5,3–5,8; 12,1–12,6; 14,5–15; 23,6–24,1; 60,4–60,9: cắt cảnh. 7,9–9,5: TX ấp úng + cắt sang BE. 18,4–19,5: đưa giấy tờ qua cửa sổ. 20,3–21,9: CS quay lưng đi + cắt. 26,5–27,4: TX cầm điện thoại. 27,6–29,4: nhoè chuyển cảnh sang phần 2.

## Video gốc → kịch bản (chỗ đã đơn giản hoá)

| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Cảnh rộng mở đầu (CS đi tới), cảnh CS quay lưng đi về xe | Bỏ | Cảnh không lời, thêm lượt gen; có thể thêm cảnh không thoại sau |
| "Really?" (TX) và "Yep." (BE) trong cùng một cảnh cận TX | Tách: cảnh 11 TX "Really?", cảnh 12 BE "Yep. Let me show you." | Mỗi clip chỉ một người nói |
| Cảnh 9 không lời (lấy giấy tờ) + cảnh 10 (đưa giấy tờ, dặn) | Hành động lấy giấy tờ đưa vào cảnh 7 (BE nói tiếng Tây Ban Nha), đưa giấy tờ vào cảnh 8 (CS nói) | Hành động phải xảy ra trong lúc nói |
| Góc D có hai biến thể (thẳng, nghiêng có vai bố) | Một góc D | |
| AI sửa "You mean: 'I'm going home'?" rồi TX lặp lại đúng | Giữ nguyên; viền xanh + ✅ ở câu TX lặp lại đúng | |
| Vòng sóng âm sau đầu AI có thể nhấp nháy theo giọng | Vòng sóng âm tĩnh trong mô tả nền | Studio chưa làm hiệu ứng theo âm thanh |
| Phụ đề AI/TX dạng viên thuốc bo tròn | Ô chữ nhật (ASS không bo góc ô chữ) | |
