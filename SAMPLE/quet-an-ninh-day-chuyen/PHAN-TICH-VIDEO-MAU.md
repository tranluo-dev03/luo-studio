> **Ghi chú (10/11/2026):** bản sao phân tích video mẫu của `soi-hanh-ly-gia-su-ai` (nhịp, bố cục, tốc độ nói, 28 lượt, phần 2). Thể loại `quet-an-ninh-day-chuyen` giữ nhịp/góc máy/28 lượt nhưng ĐỔI bối cảnh phần 1 sang cổng dò kim loại + dây chuyền; mọi chỗ nói về vali, băng chuyền, máy X-ray, em bé ở PHẦN 1 chỉ còn là tham chiếu nhịp, KHÔNG áp dụng. Bảng hành động mới: README.md cùng thư mục.

# Phân tích video mẫu: `1510_Betterspeak check luggage EN_003_5 (online-video-cutter.com).mp4`

- 66,8 giây, 720×1280, 30 fps, quảng cáo app học tiếng Anh (badge "Talka AI" góc trên trái suốt video). Tiếng Anh, phụ đề tiếng Anh, không có dòng dịch, không có end card (video đã bị cắt ở 66,8 giây).
- Công cụ: `runtime\python.exe SAMPLE\_chung\phan-tich-video.py` (ảnh `luot_01..41.jpg` 4 khung/giây cho từng câu, `chuyen-dong_01..05.jpg`, `tong-quan_1..3.jpg`). Trên Windows phải đặt `PYTHONIOENCODING=utf-8`, nếu không công cụ lỗi ngay khi in tiếng Việt.
- **Tốc độ nói:** trung vị 4,55 từ/giây cả video. Phần 1 nhanh (câu thường 5–6 từ/giây, câu ngắn tới 7–8); phần 2 chậm hơn rõ (2–4,5 từ/giây, có ngập ngừng). Khoảng lặng giữa các lượt ~0,3–0,5 giây (phần 1), ~0,5–1 giây (phần 2).
- Cảnh cắt cứng (giây): 0,6 / 0,97 / 2,23 / 12,33; nhoè chuyển cảnh 25,9–26,3 (vào phần 2).

## Cấu trúc

| Phần | Thời gian | Nội dung | Góc máy |
|---|---|---|---|
| 1. Soi hành lý | 0:00–0:26 | Nhân viên an ninh sân bay hỏi người mẹ địu con nhỏ về chiếc vali bị máy soi báo; khen tiếng Anh của cô; cô khoe học với gia sư AI, giơ điện thoại | 3 góc: toàn cảnh (A), cận nhân viên chỉ tay + cận người mẹ (B), cận hai người (C) |
| 2. Người mẹ + gia sư AI | 0:26–1:07 | Người mẹ quay selfie nói chuyện với robot AI ở ô bo góc góc trên phải; nói sai "I have 48" → robot sửa → cô nói lại "I am 48" (viền xanh ✅); hỏi giá, "free", "unlimited... anytime, anywhere" | 1 khung selfie cố định + ô robot |

## Bối cảnh, bố cục, vị trí nhân vật

**Góc A – toàn cảnh (0:00–0:00,6 và 0:02,2–0:12,3).** Cửa soi chiếu an ninh sân bay rất sáng: cửa kính cao, cột trắng, biển treo xanh đậm, dải dây xếp hàng, đoàn khách đứng xa phía sau. Nhân viên (người Latin, 40 tuổi, tóc đen ngắn, râu lún phún, áo đồng phục xanh hoàng gia, cà vạt đen, phù hiệu tròn trên vai, huy hiệu bạc) đứng **bên TRÁI** sau băng chuyền, thấy từ đầu gối trở lên, mặt nghiêng 3/4 sang phải. Người mẹ (người Latin ~48 tuổi, tóc xoăn búi rối, áo thun xám nhạt, quần jean, địu em bé sơ sinh bằng khăn vải màu kem trước ngực, túi da nâu khoác vai) đứng **sát mép PHẢI**, quay 3/4 sang trái nhìn nhân viên. Giữa hai người: máy soi X-quang xám, màn hình nhỏ trên nóc (ảnh X-quang mờ). Băng chuyền chạy chéo nửa dưới khung: **vali xanh than** ngay trước người mẹ, **vali nâu vàng** ở tiền cảnh. Camera ngang ngực, đứng yên.

**Mở đầu 0:00,6–0:02,2 (đoạn duy nhất camera chuyển động).** 0,6: cắt sang cận trung nhân viên (từ đùi trở lên) đứng cạnh máy soi, đang duỗi tay chỉ ngón trỏ xuống vali xanh. 0,6–0,8: máy **lia xuống theo cánh tay tới đúng chiếc vali** (nhoè chuyển động). 1,0–1,4: máy **lia nhanh sang phải** và dừng ở **cận người mẹ một mình** (từ eo trở lên), quay 3/4 về mép trái, mặt lo, mắt nhìn xuống vali rồi nhìn nhân viên ngoài khung; cô trả lời "Yes, it is", tay ngửa chỉ xuống vali. 2,23: cắt về toàn cảnh.

**Chuyển động camera đo bằng số** (OpenCV, theo điểm đặc trưng của nền, dịch chuyển tính trên khung 720×1280):

| Đoạn | Kết quả | Kết luận |
|---|---|---|
| 0–0,5 s toàn cảnh | dịch < 2 px, zoom +0,4% | coi như đứng yên |
| 0,6–0,8 s | dịch −60 px ngang, −21 px dọc | lia xuống/sang theo tay nhân viên tới vali |
| 1,0–1,4 s | dịch thêm −40 px, nhoè mạnh | lia nhanh sang người mẹ |
| 1,5–2,2 s | rung nhẹ 5–15 px | cầm tay, gần như đứng yên |
| 2,3–12,2 s toàn cảnh | tổng dịch < 1 px, zoom 0,999 | **đứng yên tuyệt đối** |
| 12,4–25,8 s cận hai người | rung 1–10 px, zoom ±1% | gần như đứng yên (cầm tay rất nhẹ) |

**Tương tác (xem ảnh 6 khung/giây):** người nghe luôn nhìn theo tay người nói. Nhân viên chỉ ngón trỏ thẳng vào nắp vali xanh (đầu ngón cách nắp một chút, 0,7 s và 2,2–2,8 s), đến "Please open your bag" thì ngửa bàn tay về phía vali (3,5–3,8 s); người mẹ nhìn theo xuống vali. "Of course" (4,4 s): người mẹ bước sát, đặt hai tay lên nắp vali, liếc xuống rồi nhìn nhân viên; nhân viên nhìn tay cô. Trong lúc nhân viên hỏi "Is this your first time…" (7,8–8,8 s) người mẹ nhấc tay khỏi vali, đưa về lưng em bé. Cảnh cận: người mẹ giơ điện thoại về phía nhân viên, mắt ông nhìn xuống màn hình; khi cô xoay điện thoại và chạm màn hình, ông nghiêng người lại, cả hai cùng nhìn.

**Âm thanh và giọng** (đo cao độ từng câu):

| Nhân vật | Cao độ trung vị | Chất giọng nghe/đo được |
|---|---|---|
| Nhân viên | ~130–150 Hz | nam trầm (baritone), giọng Mỹ, ngắn gọn, kiểu làm việc thường ngày, hơi ấm khi khen |
| Người mẹ | ~200–230 Hz | nữ trung, giọng Anh có âm sắc Latin, nhanh và hơi gấp khi lo, vui và tự hào khi kể; phần 2 chậm hơn, ngập ngừng khi nghĩ từ |
| AI (robot) | ~230–280 Hz | nữ cao, sáng, nhẹ hơn người mẹ, kiểu cô giáo kiên nhẫn |

Phần 1 có độ vang tự nhiên của sảnh lớn (khoảng lặng giữa câu −22 đến −40 dB so với giọng −15 dB), không nhạc, không tiếng loa. Phần 2 sạch như cuộc gọi video (khoảng lặng −40 đến −54 dB).

**Góc C – cận hai người (0:12,3–0:26).** Máy gần hơn, ngang đầu: nhân viên ở **mép TRÁI** bị khung cắt ngang ngực, đầu nghiêng 3/4 sang phải; người mẹ **giữa-phải**, từ ngực trở lên, mặt to rõ, quay 3/4 sang trái nhìn nhân viên. Nền xa mờ (hàng người xếp hàng đứng im, cửa kính). Camera đứng yên.

**Phần 2 – selfie + ô robot.** Người mẹ tự quay bằng camera trước điện thoại, **tay phải duỗi thẳng từ góc dưới trái** (không thấy điện thoại), tay trái đặt trên lưng em bé, túi da nâu trên vai trái, góc hơi cao, đầu hơi lệch trái và ở khoảng 1/5–1/3 trên khung. Nền: sảnh làm thủ tục gần như trống, cửa kính cao, cột trắng, sàn bóng loáng phản chiếu, dãy quầy xám xa. Hầu như không rung. **Ô robot**: x 0,622, y 0,059, rộng 0,296, cao 0,267 (213×342 px trên 720×1280 → 320×513 trên 1080×1920), bo góc ~0,03, **không viền**. Robot nữ giáp trắng bóng, khớp đen, mặt sứ, mắt xanh nhạt, đứng thẳng từ hông trở lên, nền trắng có vòng hào quang tròn sau đầu; nhìn thẳng ống kính.

## Hiệu ứng, chữ

| Thứ | Mô tả | Trong LUO Studio |
|---|---|---|
| Badge "Talka AI" | icon robot + chữ, góc trên trái, suốt video | Thương hiệu của dự án → logo cố định |
| Phụ đề | Chữ IN HOA đậm, viền đen, cụm 1–3 từ hiện lần lượt, tâm ở ~58% chiều cao. Phần 1: mọi người chữ **trắng**. Phần 2: AI chữ **vàng**, người mẹ chữ **trắng** | `post.py` (config `kieu_theo_phan`, y 1125). **Khác:** hiện cả câu, chữ thường (không IN HOA, không tách cụm) |
| Câu sai "I have 48." | viền đỏ dày nháy quanh khung + ❌ dưới chữ, hiện ở cuối câu | `"fx": "wrong"`, `"icon": "x"` (❌ đặt bên phải chữ, không phải bên dưới) |
| Câu nói lại đúng "I am 48." (người mẹ) | viền xanh lá nháy + ✅ dưới chữ | `"fx": "right"`, `"icon": "check"` đặt ở lượt của **người mẹ** (khác `san-bay-gia-su-ai`: ở đó đặt ở lượt AI) |
| Lia máy 0,6–1,4 s | theo tay nhân viên xuống vali rồi lia nhanh sang người mẹ (cắt ở 0,97 s ngay giữa cú lia) | Cảnh 1 camera đứng yên (Muse làm cú nghiêng thành lia sang mẹ con nên đã bỏ); cảnh 2 ảnh riêng + `Chuyển cảnh: lia phải 0.36` (ffmpeg, nhoè ngang) |
| Nhoè vào phần 2 | 25,9–26,3 s | `| vao: nhoe 0.5` |
| Màn hình điện thoại | hiện chân dung hoạt hình cô gái tóc đỏ (app), quay ra ngoài | Token `DAO_DIEN_THOAI` mô tả màn hình chỉ có chân dung, không chữ (rủi ro: Muse vẽ chữ/giao diện) |
| Ô AI 0,1 s đầu phần 2 | thoáng hiện cô gái tóc đỏ rồi mới là robot | **Bỏ** |

## Bảng lượt thoại và hành động

| Lượt | Thời gian | Ai nói | Từ/giây | Lời (nguyên văn) | Góc | Hành động người nói | Người nghe | Vật dụng | Ánh mắt | KHUNG CUỐI |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,42–1,2 | Nhân viên | 5,1 | Is this your bag? | A → cận NV (đẩy máy) | chỉ tay phải xuống vali xanh | mẹ im, nhìn NV | vali xanh, vali nâu | NV nhìn vali rồi mẹ | NV tay chỉ vali |
| 2 | 1,54–2,12 | Mẹ | 5,2 | Yes, it is. | B cận mẹ | gật nhẹ, mặt lo, một tay trên lưng bé | (NV ngoài khung) | — | nhìn về mép trái | tay trên lưng bé |
| 3 | 2,26–4,12 | NV | 4,3–6,1 | The scanner detected something. Please open your bag. | A | chỉ tay vào vali, rồi hạ tay | mẹ im, nhìn NV, tay trên lưng bé | vali xanh | NV nhìn mẹ | NV đứng thẳng |
| 4 | 4,42–7,04 | Mẹ | 5,3–8,3 | Of course. It might be batteries. Would you like me to take them out? | A | cúi người, đặt hai tay lên nắp vali xanh | NV im, nhìn mẹ | vali xanh | mẹ nhìn NV | hai tay mẹ trên vali |
| 5 | 7,2–8,76 | NV | 3,3–7,0 | Yes. Is this your first time in America? | A | gật, ngửa tay trái về phía mẹ | mẹ im, rút dần tay khỏi vali | — | nhìn nhau | NV đứng thẳng |
| 6 | 9,12–10,62 | Mẹ | 3,3–5,3 | Yes. I'm here visiting my daughter. | A | một tay đặt lại lưng bé, cười nhẹ | NV im | — | nhìn nhau | tay trên lưng bé |
| 7 | 11,04–12,3 | NV | 6,4 | Your English is really good, by the way. | A | ngửa hai bàn tay như khen | mẹ im, cười | — | nhìn nhau | NV hạ tay |
| 8 | 12,46–14,52 | Mẹ | 5,0–5,3 | Thank you. I've been practicing with an AI tutor. | **C** (cắt 12,33) | cười tươi, tay rảnh đưa trước ngực | NV im, nhìn mẹ | — | nhìn nhau | tay trên lưng bé |
| 9 | 14,98–15,3 | NV | 6,3 | What's that? | C | nghiêng đầu tò mò | mẹ im, cười | — | nhìn mẹ | như cũ |
| 10 | 15,6–18,82 | Mẹ | 5,3 | I talk to it for about 15 minutes a day and it corrects me while I speak. | C | **giơ điện thoại** tay phải, màn hình quay về NV (chân dung app), tay trái ngửa giải thích | NV cúi nhìn điện thoại | **điện thoại xuất hiện** (~15,8 s) | mẹ nhìn NV, NV nhìn đt | mẹ giơ đt |
| 11 | 19,32–21,6 | Mẹ | 4,0 | After just three weeks, I started speaking this confidently. | C | tiếp tục giơ đt, tự hào | NV nhìn đt rồi nhìn mẹ | đt | nhìn nhau | mẹ giơ đt |
| 12 | 22,22–23,12 | NV | 4,4 | Is it expensive, though? | C | hơi nghi ngờ, liếc đt | mẹ im, cười | đt | NV nhìn mẹ | như cũ |
| 13 | 23,46–25,78 | Mẹ | 4,7–7,5 | No, no, it's free. Let me show you how it works. | C | lắc đầu cười, xoay đt về mình, chạm màn hình | NV cúi nhìn đt | đt | cả hai nhìn đt | cả hai nhìn đt; nhoè 25,9 |
| 14 | 26,12–27,28 | AI | 3,5 | Do you speak English? | selfie + ô robot | robot nói, nhìn ống kính | mẹ nghe, cười nhẹ | — | mẹ nhìn ống kính | |
| 15 | 28,06–29,16 | Mẹ | 2,7 | More or less. | | liếc sang bên khi nghĩ, tay trái ngửa nhẹ | robot nghe | | liếc phải → ống kính | |
| 16 | 29,78–30,66 | AI | 4,6 | How old are you? | | | | | | |
| 17 | 30,92–32,38 | Mẹ | 2,1 | I have 48. | | nói chậm, mắt liếc sang bên | | | | **viền đỏ + ❌** cuối câu |
| 18 | 33,42–35,56 | AI | 3,3 | You have to say, I am 48. | | | mẹ nghe, cười | | | chữ vàng |
| 19 | 36,06–37,66 | Mẹ | 1,9 | I am 48. | | nói rõ, tự tin | | | | **viền xanh + ✅** |
| 20 | 38,32–39,06 | AI | 2,7 | Good job. | | | mẹ cười | | | |
| 21 | 39,64–41,54 | Mẹ | 3,2 | Thank you, but who are you? | | | | | | |
| 22 | 42,44–46,66 | AI | 3,3–4,1 | Me? I'm an AI tutor. I'll help you improve your English skills. | | | mẹ cười | | | |
| 23 | 47,4–49,12 | Mẹ | 4,1 | Thank you, but I don't have money. | | | | | | (mẫu không có icon $) |
| 24 | 49,82–51,92 | AI | 3,5–4,6 | What money? You can study for free. | | | | | | |
| 25 | 52,52–54,9 | Mẹ | ~3 | For free? You're joking, right? | | tay trái ngửa ra, ngạc nhiên | | | | |
| 26 | 55,3–63,06 | AI | 2,4 | Nope, I'm serious. You can practice unlimited English conversations with a real AI avatar, anytime, anywhere. | | | mẹ cười, nghe | | | |
| 27 | 63,72–64,04 | Mẹ | 3,1 | Really? | | | | | | |
| 28 | 64,56–66,8 | AI | 2,8–6,6 | Yes, really. You'll speak like a native in no time. | | | mẹ cười | | | hết video |

Ghi chú lời: Whisper nghe câu cuối là "I'm like a native in no time"; phụ đề video chỉ có "LIKE A NATIVE / IN NO TIME" nên lời đầy đủ nhiều khả năng là "You'll speak like a native in no time" (đã dùng câu này). Whisper gộp "You're joking, right? Nope, I'm serious." thành một câu; phụ đề vàng/trắng cho thấy "Nope, I'm serious." là của AI.

## Khoảnh khắc chuyển động mạnh

| Giây | Giải thích |
|---|---|
| 0,38–2,5 | Cắt + đẩy máy về vali (0,6–0,97), cắt sang cận người mẹ (0,97), cắt về toàn cảnh (2,23) |
| 12,12–12,62 | Cắt sang góc C (cận hai người) |
| 15,38–15,88 | Điện thoại xuất hiện trong tay người mẹ (nhảy hình, như một cảnh cắt nhỏ) |
| 19,38–19,5 | Người mẹ đổi tư thế tay cầm điện thoại |
| 24,5–26,5 | Người mẹ xoay điện thoại về mình, rồi nhoè chuyển sang phần 2 |

## Video gốc → kịch bản

| Video gốc | Kịch bản (`KICH-BAN-SOI-HANH-LY-GIA-SU-AI.txt`) | Đơn giản hoá / khác |
|---|---|---|
| Lượt 1, cận nhân viên + lia theo tay tới vali | Cảnh 1, góc A1 (Prompt ảnh: cận trung nhân viên một mình); ảnh đầu đã ở tư thế chỉ ngón trỏ xuống giữa nắp vali; camera khoá | Bỏ 0,5 giây toàn cảnh đầu tiên và cú nghiêng máy theo tay (video bắt đầu thẳng ở cận nhân viên đang chỉ) |
| Lia nhanh sang người mẹ + lượt 2 | Cảnh 2, góc B (Prompt ảnh), `Chuyển cảnh: lia phải 0.36`; gật, ngửa tay chỉ xuống vali | Cú lia làm bằng ffmpeg khi ghép (phóng 1,4 lần + trượt + nhoè), không phải máy thật |
| Lượt 3–7, toàn cảnh đứng yên | Cảnh 3 góc A (Prompt ảnh), 4–7 nối khung cuối; ACTION theo từng nhịp của CẢ HAI người: chỉ vali → ngửa tay mời mở, mẹ nhìn theo (3); mẹ đặt hai tay lên nắp vali, NV nhìn tay cô (4); NV gật + ngửa tay, mẹ nhấc tay về lưng bé (5); mẹ cử chỉ nhẹ, NV gật (6); NV ngửa hai tay khen, mẹ cười (7) | Ảnh góc A gen mới nên vali có thể lệch nhẹ so với cảnh 1 (vali chỉ thấy một phần ở cảnh 1) |
| Lượt 8–13, cận hai người | Cảnh 8 góc C (Prompt ảnh), 9–13 nối; ACTION: mẹ cười chạm ngực (8); NV nghiêng đầu tò mò (9); mẹ giơ đt về phía NV, mắt NV xuống màn hình (10); NV ngước lên gật (11); NV liếc đt, nghi ngờ (12); mẹ lắc đầu, xoay đt chạm màn hình, NV nghiêng người lại, cả hai nhìn đt (13) | Điện thoại được giơ lên trong lúc nói (video gốc nhảy hình); camera đứng yên (rung tay rất nhẹ của video gốc bỏ qua) |
| Giọng | `GIONG_CANBO` nam trầm kiểu nhân viên làm việc; `GIONG_HOC` nữ trung giọng Latin, gấp khi lo, tự hào khi kể; `GIONG_DAY` cao, sáng hơn người mẹ; phần 1 "natural acoustics of a large airport hall", phần 2 sạch như cuộc gọi video | Studio không đo được cao độ: chỉ mô tả bằng lời |
| Lượt 10 + 11 của người mẹ (2 câu liền, 26 từ) | Hai lượt riêng (10, 11) cùng người nói | Một clip ≤ 10 giây không đủ cho 26 từ |
| Nhoè 25,9 s | `===== PHAN 2 ... | vao: nhoe 0.5 =====` | — |
| Phần 2, selfie + ô robot | `[GHEP HAI LOP]`: `khung DAY: 0.62, 0.06, 0.30, 0.27`, `bo goc: 0.03`, `vien: khong` | Ô robot gen 9:16 rồi cắt vừa (ô thật 0,62 rộng/cao) |
| Lượt 14–28 | 15 lượt phần 2; "Nope, I'm serious." gộp vào lượt AI dài (17 từ) | — |
| Phụ đề cụm từ IN HOA | Phụ đề cả câu | Chưa có kiểu "cụm 1–3 từ IN HOA" trong `phu_de.py` |
| Badge "Talka AI" | Thương hiệu → logo cố định | — |
| Không có end card | Không gen; muốn có thì Thương hiệu → Outro | — |
