# Phân tích video mẫu: `1410_older airport PT_003 (1).mp4`

- 73,4 giây, 9:16, tiếng Anh, phụ đề song ngữ (tiếng Anh + tiếng Bồ Đào Nha). App quảng cáo: **Talka AI** (phụ đề có chỗ ghi nhầm "Lingo AI").
- Đã chạy `SAMPLE/_chung/phan-tich-video.py` (36 câu, cảnh cắt cứng ở 13,63 / 57,97 / 68,37 giây) và xem từng ảnh `luot_NN.jpg`, `chuyen-dong_NN.jpg`, `tong-quan_N.jpg`.
- **Tốc độ nói trung vị 3,5 từ/giây**, câu ngắn tới 5,4. Khoảng lặng giữa các lượt ~0,6 giây.

## Cấu trúc 3 phần

| Phần | Thời gian | Nội dung | Cách làm trong LUO Studio |
|---|---|---|---|
| 1. Quầy hải quan | 0:00–0:26,5 | Cô gái (khách) ngồi trước quầy, nhân viên hải quan (quay lưng về camera, góc qua vai) hỏi "Do you speak English?"; cô trả lời trôi chảy, đưa vé khứ hồi, được khen, kể là học bằng app, lấy điện thoại ra "Here, let me show you." | Phần 1 của kịch bản (cảnh thường, khối CẢNH, hai người chung khung) |
| 2. Hội thoại người dùng + AI | 0:26,5–0:58 | Cô gái ngồi trước quầy check-in nhìn thẳng camera; robot gia sư AI ở ô góc trên phải. AI hỏi, cô trả lời, nói sai "I am Mexico" → AI sửa "I am from Mexico", rồi hỏi đáp về giá/tính năng app | Phần 2 của kịch bản, **ghép 2 lớp**: gen RIÊNG video cô gái (nền toàn khung) và video robot (ô góc trên phải) rồi ghép |
| 3. Quảng cáo app | 0:58–1:13,4 | Robot toàn khung, giọng robot kêu gọi tải app; đè popup cài app của Google Play (Installing → Installed → bấm Open), màn hình app trượt vào; 68,4–73,4 end card đen: icon, "Talka AI: Learning Language Tutor", nút Google Play | Không gen: dùng **Video giới thiệu** + **Outro** trong phần Thương hiệu của dự án (file người dùng tự có) |

## Thành phần phủ lên hình (hậu kỳ, không gen)

| Thành phần | Mô tả trong video mẫu | Studio hiện có? |
|---|---|---|
| Badge "Talka AI" góc trên trái | Ô đen bo góc, icon robot + chữ trắng, suốt Phần 1–2 | Có: Thương hiệu → logo cố định + chữ cạnh logo |
| Chữ nhấn tên app | "with Lingo AI" (0:21) trên ô vàng chữ đen | Có (hậu kỳ riêng): `"nhan"` |
| Phụ đề tiếng Anh | Chữ đậm có viền đen, giữa khung (~ngang ngực nhân vật). Người hỏi (nhân viên, AI): **trắng**; cô gái: **vàng** | Có: trường `"c"` của từng lượt (`white` / `yellow`) |
| Phụ đề dịch tiếng Bồ Đào Nha | Dòng thứ hai nhỏ hơn, chữ **đỏ viền trắng**, ngay dưới phụ đề tiếng Anh | Có (hậu kỳ riêng): `"dich"` |
| Câu sai | "I am Mexico" chữ đỏ + ô ❌ đỏ + viền đỏ phát sáng quanh khung | Có: `"fx": "wrong"`, `"c": "red"`, `"icon": "x"` (viền đỏ nháy + tiếng "tè tè") |
| Câu sửa đúng | "I am from Mexico." chữ trắng → viền xanh lá phát sáng + ✅ | Có: `"fx": "right"`, `"c": "green"`, `"icon": "check"` |
| Emoji 💰 | Hiện cạnh chữ "money" ở câu "But I don't have money" | Gần đúng: `"icon": "dollar"` (hình tròn vàng có $) |
| Chuyển Phần 1 → 2 | 26,5–27s: hình nhoè chuyển động (whip blur) rồi vào cảnh có robot | Có (gen riêng): `\| vao: nhoe 0.5` ở dòng chia phần 2 |
| Ô robot | Góc trên phải, không viền, góc vuông, mép dưới mờ dần vào nền | Gần đúng: `vien: khong`, `bo goc: 0` (mép cứng, không mờ dần) |

## Bảng từng cảnh (góc máy, hướng nhân vật, hiệu ứng, chữ, voice)

Ký hiệu người nói: **NV** = nhân viên hải quan, **CG** = cô gái, **AI** = robot gia sư.

| # | Thời gian | Góc máy | Hướng nhân vật / hành động | Hiệu ứng, chữ trên màn hình | Voice (nguyên văn) |
|---|---|---|---|---|---|
| 1 | 0:00–1,0 | Qua vai NV (NV tiền cảnh phải, quay lưng ¾, thấy gáy + kính), CG giữa-trái phía xa, quầy gỗ, giấy tờ + bút tiền cảnh trái, túi xách trên bàn trái; nền: sảnh làm thủ tục đông người (mờ), màn hình "NEXT: B12" | NV cầm hộ chiếu xanh đen, tay trái chìa ra hướng CG. CG ngồi, hai tay đan trên bàn, nhìn NV, mặt nghiêm | Phụ đề trắng | NV: "Do you speak English?" |
| 2 | 1,7–2,5 | như trên | CG nhìn NV, gật nhẹ | Phụ đề vàng | CG: "Yes, I do." |
| 3 | 2,9–3,5 | như trên | NV chìa tay ngửa (mời nói) | Phụ đề trắng | NV: "Prove it." |
| 4 | 4,1–10,5 | như trên | CG mỉm cười, nói tự tin, tay trên bàn, nhìn NV; NV lật hộ chiếu | Phụ đề vàng, chia cụm | CG: "Sure. I'm visiting my brother in New York. I'm staying for 10 days, then I fly home." |
| 5 | 11,8–13,0 | như trên | CG với tay sang túi xách bên trái, rút tờ vé, đưa qua bàn cho NV; NV nhận vé | Phụ đề vàng | CG: "Here's my return ticket." |
| 6 | 13,6–17,4 | **Cắt cứng 13,63** sang cận hơn: CG chiếm giữa khung, NV chỉ còn tay cầm hộ chiếu ở tiền cảnh phải | NV xem hộ chiếu; CG mỉm cười nhìn NV | Phụ đề trắng | NV: "OK. … How? Your English is good." (bản dịch: "Haha, sao tiếng Anh của cô tốt thế") |
| 7 | 17,5–24,7 | **Đẩy máy vào nhanh** (17,5–19) thành trung cảnh CG | CG ngạc nhiên vui, cười tươi, hai tay đan trên bàn, nhìn NV | Phụ đề vàng; chữ "with Lingo AI" trên **nền ô vàng chữ đen** (nhấn tên app) | CG: "Honestly? Just 10 minutes a day with Lingo AI. Real conversations, exactly like this one." |
| 8 | 25,2–26,5 | như trên | CG cúi xuống túi xách bên trái, lấy điện thoại, nhìn màn hình | Phụ đề vàng | CG: "Here, let me show you." |
| — | 26,5–27,0 | **Nhoè chuyển động** (whip blur) | — | Chuyển cảnh | — |
| 9 | 27,0–27,7 | Chính diện ngang ngực CG, camera cố định ở tầm quầy; CG ngồi sau quầy đá xám, hộ chiếu + tờ khai trên quầy; nền sảnh check-in sân bay (bảng DEPARTURES, biển CHECK-IN, SECURITY CHECKPOINT, khách kéo vali). Ô robot góc trên phải (~x 54–100%, y 0–40%) | CG nhìn thẳng camera, hai bàn tay úp trên quầy; robot nói, đầu nghiêng nhẹ | Phụ đề trắng | AI: "Do you speak English?" |
| 10 | 27,8–28,7 | như trên | CG nhún vai, hai lòng bàn tay ngửa rồi úp lại xuống quầy | Phụ đề vàng | CG: "More or less." |
| 11 | 29,1–30,0 | như trên | CG nghe, mỉm cười nhìn camera; robot nói | Phụ đề trắng | AI: "Where are you from?" |
| 12 | 30,6–31,3 | như trên | CG nói tự tin, tay hơi dang | **Chữ đỏ + ❌ + viền đỏ phát sáng** | CG: "I am Mexico." |
| 13 | 31,7–34,0 | như trên | CG mỉm cười nghe | Phụ đề trắng | AI: "Almost. The best way is to say," |
| 14 | 34,5–35,6 | như trên | CG cười | Chữ trắng → **viền xanh lá phát sáng + ✅** | AI: "I am from Mexico." |
| 15 | 36,3–38,5 | như trên | CG cười, hơi ngả đầu | Phụ đề vàng | CG: "Ah, I always get confused about that." |
| 16 | 38,9–41,5 | như trên | CG cười nghe; robot nói, mắt nhắm mở | Phụ đề trắng | AI: "That's what I'm here for, to help you speak correctly." |
| 17 | 42,1–43,2 | như trên | CG dang tay nhẹ, mặt hơi lo | Phụ đề vàng + **emoji 💰** | CG: "But I don't have money." |
| 18 | 43,5–44,8 | như trên | CG nghe | Phụ đề trắng | AI: "What? You don't need money." |
| 19 | 45,3–45,7 | như trên | CG giơ hai tay trước ngực, ngạc nhiên | Phụ đề vàng | CG: "Really?" |
| 20 | 46,2–51,0 | như trên | CG đặt tay lại xuống quầy, mỉm cười nghe | Phụ đề trắng | AI: "Of course. No tricks. It's real English conversation practice with an AI tutor." |
| 21 | 51,6–52,7 | như trên | CG nghiêng đầu tò mò | Phụ đề vàng | CG: "Like a real tutor?" |
| 22 | 53,0–57,8 | như trên | CG cười nghe | Phụ đề trắng | AI: "That's right. It corrects your grammar and pronunciation and helps you speak with confidence." |
| 23 | 58,0–68,4 | **Cắt cứng 57,97**: robot toàn khung, chính diện, nền trắng xanh tương lai, vòng sáng sau đầu | Robot đứng yên, miệng mấp máy nhẹ (lồng tiếng) | Không phụ đề. Popup Google Play "Talka AI: Language Tutor" (Pending → % → Installing → Installed), con trỏ bấm Open, màn hình app trượt vào từ phải | AI: "Want to speak English with confidence? Download Talka AI today. Practice real conversations with your AI tutor. Install now and start speaking." |
| 24 | 68,4–73,4 | **Cắt cứng 68,37**: end card nền đen | — | Icon app, "Talka AI: Learning Language Tutor", nút "GET IT ON Google Play" | (im lặng) |

### Giải thích các khoảnh khắc chuyển động mạnh
13,4–13,9: cắt cứng sang cận cảnh. 17,5–19: máy đẩy vào. 24,6–27,1: CG lấy điện thoại + nhoè chuyển cảnh sang Phần 2. 27,9–28,4 và 30,6–31: CG nhún vai / dang tay. 37,0; 42,3–43; 45,4–46: cử chỉ tay của CG ("about that", "money", "Really?"). 57,8–58,3: cắt sang robot toàn khung. 68,1–68,6: cắt sang end card.

## Bảng hành động (theo lượt của kịch bản)

| Lượt | Ai nói | Từ/giây | Hành động người nói | Người nghe làm gì | Vật dụng | Ánh mắt | Camera | Khung cuối |
|---|---|---|---|---|---|---|---|---|
| P1-1 | NV | 3,9 | tay trái chìa nhẹ về CG | CG ngồi, tay đan trên bàn | NV cầm hộ chiếu | nhìn nhau | qua vai NV, cố định | NV cầm hộ chiếu, CG tay đan |
| P1-2 | CG | 3,7 | gật nhẹ | NV im | — | nhìn NV | như trên | như trên |
| P1-3 | NV | 3,3 | tay ngửa mời | CG im | hộ chiếu | nhìn nhau | như trên | như trên |
| P1-4 | CG | 3,3 | cười, nói tự tin | NV lật hộ chiếu | hộ chiếu | nhìn NV | như trên | CG tay trên bàn |
| P1-5 | CG | 3,5 | lấy vé từ túi xách trái, đưa NV | NV nhận vé | **vé** xuất hiện → sang tay NV | nhìn NV | như trên | NV cầm vé + hộ chiếu, CG tay trên bàn |
| P1-6 | NV | 2,6–3,8 | nhìn giấy tờ rồi ngẩng lên cười | CG mỉm cười | vé, hộ chiếu | NV → giấy → CG | (gốc: cắt cận; kịch bản: giữ khung) | như trên |
| P1-7 | CG | 2,2–3,4 | ngạc nhiên vui, cười tươi | NV im | — | nhìn NV | (gốc: đẩy máy vào; kịch bản: giữ khung) | CG tay đan, cười |
| P1-8 | CG | 3,6 | lấy điện thoại từ túi xách, nhìn màn hình | NV nhìn | **điện thoại** xuất hiện | nhìn điện thoại | như trên | CG cầm điện thoại trước ngực |
| P2-1…14 | AI/CG xen kẽ | 3–5,4 | CG: nói với camera, cử chỉ tay nhỏ rồi úp tay lại xuống quầy. AI: nói, đầu nghiêng nhẹ | người kia im, mỉm cười | hộ chiếu + tờ khai nằm yên trên quầy | CG nhìn thẳng camera | cố định chính diện | CG hai tay úp trên quầy |

## Video gốc → kịch bản (chỗ đã đơn giản hoá)

| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Phần 1 có 3 cỡ cảnh (qua vai → cận → trung cảnh đẩy máy) | Giữ **một** khung qua vai suốt Phần 1 | Muse nối khung cuối → khung đầu, đổi cỡ cảnh giữa chừng làm mặt/trang phục trôi. Muốn cận cảnh: thêm `Prompt ảnh` cho cảnh 6 (tốn thêm ảnh, dễ lệch mặt) |
| Người qua lại phía sau | Người phía xa đứng yên, mờ | Quy tắc nền tĩnh |
| "OK." và "How? Your English is good." là 2 câu cách nhau | Gộp thành một lượt NV: "Okay. Wow, your English is good." | "How?" nhiều khả năng Whisper nghe nhầm tiếng cười/"Wow" (bản dịch là "Hahaha como seu inglês é bom") |
| "with Lingo AI" | "with Talka AI" | Video mẫu ghi nhầm tên app |
| AI: "Almost. The best way is to say, I am from Mexico." (một mạch) | Tách 2 lượt AI liền nhau | Để viền xanh + "tinh tinh" rơi đúng câu "I am from Mexico." |
| Phần 2: hai nhân vật một khung | Gen riêng 2 video (CG nền 9:16, robot ô 9:16 góc trên phải) rồi ghép | Không bao giờ có chuyện hai người cùng nói; robot dùng clip nghe dùng lại |
| Phần 3: robot toàn khung + popup Google Play + end card | Không gen; dùng Video giới thiệu + Outro của dự án | Giọng robot ở Phần 3 phải có sẵn trong video giới thiệu |
