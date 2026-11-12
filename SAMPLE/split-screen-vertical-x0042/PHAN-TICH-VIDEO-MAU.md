# Phân tích video mẫu: `2110_langlearn vertical EN_003_5` (thể loại `chia-doi-gia-su-ai`)

Chạy `runtime\python.exe SAMPLE\_chung\phan-tich-video.py <video>`, xem từng ảnh `luot_NN.jpg` / `chuyen-dong_NN.jpg` / `tong-quan_N.jpg` và khung gốc (`anh/khung-video-mau.png`).

## Tổng quan

- 44,5 giây, 720×1280, 30 khung/giây. **Không có cảnh cắt cứng**: cả video là MỘT bố cục cố định, máy quay không chuyển động.
- **Màn hình chia đôi dọc**, mỗi nửa rộng 360 px, cao toàn khung:
  - **Nửa TRÁI: robot gia sư AI.** Robot nữ màu trắng, mặt sứ, mắt xanh nhạt, cổ là dây cáp đen, ngực là các tấm lục giác trắng viền xanh ngọc. Robot đứng thẳng, nhìn thẳng ống kính. Đỉnh đầu sát mép trên, mặt ở 1/3 trên, ngực lấp phần giữa và dưới, vai bị mép ô cắt. Nền trắng xanh nhạt có vòng hào quang sau đầu, chính là robot trong ảnh `anh/robot-ai.webp`.
  - **Nửa PHẢI: người dùng.** Cô gái Mexico ngồi ở bàn gỗ quán cà phê, quay từ ngực trở lên, mặt chính giữa ô và nhìn thẳng ống kính như đang gọi video. Không thấy tay, không thấy điện thoại. Trên bàn, phía trước có cốc sô-cô-la nóng gốm talavera (lệch trái) và bánh concha trên đĩa gỗ (góc dưới phải). Phía sau là tường kem treo thảm dệt Mexico nhiều màu, mép phải có dải gạch talavera xanh trắng. Ánh sáng ban ngày ấm.
- **Phụ đề:** ô đen chữ đậm, căn giữa khung, tâm ở khoảng 68% chiều cao (y ≈ 868/1280 → 1300/1920).
  - Lời AI chữ **trắng**, lời người dùng chữ **vàng**.
  - Câu sai "I have 28" chữ **đỏ**; câu người dùng nói lại đúng "I am 28" chữ **xanh lá**.
  - Không có dòng dịch, không có icon ❌/✅.
- **Hiệu ứng sai/đúng:** viền sáng màu **chỉ ở nửa PHẢI** (nửa người dùng), loé ở **cuối câu**. Đỏ ở "I have 28" (≈7,0 s, câu 5,5–7,2 s); xanh lá ở "I am 28" (≈11,5 s, câu 10,1–11,7 s). Nửa robot không có viền.
- **Badge** "Talka AI" góc dưới trái: ảnh đại diện robot vuông + chữ trắng. Studio không vẽ, gắn ở Thương hiệu → logo cố định của dự án.
- **Tiếng:** hai giọng sạch, gần mic, không nhạc nền, không tiếng quán. AI nữ, giọng sáng, nói nhanh. Người dùng nữ có giọng Mexico, nói chậm và ngập ngừng.
- **Tốc độ nói** (báo cáo công cụ): trung vị 4,67 từ/giây. AI nói 4,4–5,3 từ/giây, câu hỏi ngắn tới 5. Người dùng chỉ 1,7–2,8 từ/giây (ngập ngừng, kéo "Um"). Khoảng lặng giữa các lượt ~0,4–1,6 giây.

## Bảng hành động (mỗi lượt một dòng)

| Lượt | Thời gian | Ai nói | Từ/giây | Lời (nguyên văn) | Người nói làm gì | Người nghe làm gì | Ánh mắt | Camera | Khung cuối |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,0–0,8 | AI | 5,1 | Do you speak English? | Hỏi nhanh, mỉm cười, đầu nghiêng nhẹ | Cô gái mỉm cười, khép miệng | Cả hai nhìn ống kính | Đứng yên | Robot khép miệng cười |
| 2 | 1,4–3,3 | Người dùng | 2,1 | Um, more or less. | Nhắm mắt kéo "Um", nghĩ, rồi nói, nhún nhẹ đầu, cười ngượng | Robot cười khép miệng, chớp mắt | Cô gái liếc lên khi nghĩ rồi về ống kính | Đứng yên | Cô gái cười nhẹ |
| 3 | 4,0–4,9 | AI | 4,4 | How old are you? | Hỏi, nhướn mày tò mò | Cô gái nghe, mỉm cười | Ống kính | Đứng yên | Robot khép miệng |
| 4 | 5,5–7,2 | Người dùng | 1,7 | I have 28. | Nói chậm, tự tin nhưng sai ngữ pháp; nhắm mắt ở đầu câu | Robot nghe, mặt bình thản | Ống kính | Đứng yên | **Viền đỏ** nửa phải ở cuối câu; chữ đỏ |
| 5 | 7,9–9,4 | AI | 4,7 | You have to say, I am 28. | Sửa câu, giọng ấm, nhấn "I am" | Cô gái nghe, gật nhẹ | Ống kính | Đứng yên | Robot cười |
| 6 | 10,1–11,7 | Người dùng | 2,0 | I am 28. | Nói lại đúng, cười tươi, tự hào | Robot cười | Ống kính | Đứng yên | **Viền xanh lá** nửa phải ở cuối câu; chữ xanh |
| 7 | 12,5–13,1 | AI | 3,3 | Good job. | Khen, cười rộng | Cô gái cười | Ống kính | Đứng yên | Robot cười khép miệng |
| 8 | 13,8–16,1 | Người dùng | 2,7 | Thank you, but who are you? | Cảm ơn, rồi tò mò hỏi, chu môi ở "who", nhướn mày | Robot nghe | Ống kính | Đứng yên | Cô gái khép miệng |
| 9 | 16,4–19,8 | AI | 3,3–5,0 | Me? I'm an AI tutor. I'll help you improve your English skills. | "Me?" ngạc nhiên vui, rồi giới thiệu, cười | Cô gái nghe, cười | Ống kính | Đứng yên | Robot cười |
| 10 | 21,4–23,9 | Người dùng | 2,8 | Thank you, but I don't have money. | Cảm ơn, rồi lo lắng nhẹ, nhíu mày | Robot nghe | Ống kính | Đứng yên | Cô gái khép miệng |
| 11 | 24,4–26,2 | AI | 5,0 | What money? You can study for free. | Trêu nhẹ "What money?", rồi vui vẻ nói miễn phí | Cô gái mắt mở to | Ống kính | Đứng yên | Robot cười |
| 12 | 27,2–30,4 | Người dùng | 2,0 | For free? You're joking, right? | Ngạc nhiên, rồi nghi ngờ nửa đùa | Robot nghe | Ống kính | Đứng yên | Cô gái khép miệng |
| 13 | 31,4–38,8 | AI | 2,9–3,0 | Nope, I'm serious. You can practice unlimited English conversations with a real AI avatar. Anytime, anywhere. | Tự tin, nhiệt tình, nháy mắt nhẹ | Cô gái cười tươi dần | Ống kính | Đứng yên | Robot cười |
| 14 | 40,1–40,6 | Người dùng | 1,9 | Really? | Nhắm mắt lại rồi mở to, phấn khởi | Robot nghe | Ống kính | Đứng yên | Cô gái cười |
| 15 | 41,3–44,4 | AI | 1,7–5,3 | Yes, really. You'll sound like a native in no time. | Khẳng định, rồi nói nhanh, hào hứng | Cô gái cười | Ống kính | Đứng yên | Robot cười khép miệng |

**Khoảnh khắc chuyển động mạnh** (báo cáo): 5,8; 6,9; 11,9; 13,5; 15,4; 17,9; 21,4; 23,9; 27,4; 30,0; 39,8; 42,3 s. Không có cảnh cắt hay hành động bằng tay. Các mốc này là lúc đổi người nói: robot mở miệng to, đầu người dùng nhún. Hai mốc 6,9 và 11,9 còn trùng lúc loé viền đỏ/xanh.

## Video gốc → kịch bản

| Video gốc | Trong kịch bản / biến thể | Ghi chú |
|---|---|---|
| Màn hình chia đôi dọc, robot trái, người phải | `[GHEP HAI LOP]`: `nen: HOC`, `khung HOC: 0.5, 0, 0.5, 1`, `khung DAY: 0, 0, 0.5, 1`, không bo góc, không viền | Studio gen RIÊNG mỗi nhân vật ở 9:16 rồi cắt DẢI GIỮA (nửa bề ngang) cho vừa ô. Mỗi clip chỉ có một người, nên không bao giờ hai người cùng nói |
| 23 câu → 15 lượt | 15 lượt `LUOT`, câu liền nhau của cùng một người gộp thành một lượt (vd. lượt 13 gồm 3 câu của AI) | Lượt dài nhất 18 từ (dưới mức 20) |
| Robot nhìn ống kính, nói cười, nghe khép miệng | `[NHAN VAT DAY]` + `[NGHE DAY]`, ảnh tham chiếu `anh/robot-ai.webp` gắn vào `NGUOI_DAY` | Robot giống hệt video mẫu |
| Người dùng ngồi bàn cà phê, cốc + bánh, thảm Mexico | `[NHAN VAT HOC]`, token `NEN_HOC`, `DAO_BAN`; ảnh tham chiếu từng biến thể gắn vào `NGUOI_HOC` | Ảnh tham chiếu là ảnh đứng nền xanh lá: kịch bản dặn bỏ nền xanh và tư thế đứng của ảnh |
| Không thấy tay, không thấy điện thoại | "camera is a phone propped on the table… no arm, no hand and no phone in the frame" | |
| Người dùng ngập ngừng ("Um"), nói chậm | `[VIDEO SUFFIX]`: người học ~2,5 từ/giây, AI ~4,5 | Muse hay nói chậm hơn: AI chậm thì nâng "Tốc độ tăng tối đa" |
| Phụ đề ô đen, AI trắng / người dùng vàng | `config.json` → `kieu_theo_phan` (`o: black`), cỡ chữ 56, y 1300 | Video mẫu chia phụ đề thành cụm ngắn hơn ("You have to say" / "I am 28"); hậu kỳ chung chia theo câu |
| Câu sai chữ đỏ + viền đỏ nửa phải; câu đúng chữ xanh + viền xanh nửa phải | Lượt 4 `"c": "red", "fx": "wrong"`; lượt 6 `"c": "green", "fx": "right"`; `config.json` → `vien` (x 0,5, rộng 0,5, cuối câu) | Viền của Studio là khung sáng nháy 3 nhịp; video mẫu là quầng màu mềm hơn |
| Badge "Talka AI" góc dưới trái | Không gen: Thương hiệu → logo cố định (vị trí "Dưới trái") | |
| Biến thể 19: tuổi đổi 28 → 68 | `tao_bien_the.py`: cột tuổi; câu sai, câu sửa và câu đúng cùng đổi | |
