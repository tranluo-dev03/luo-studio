# Phân tích video mẫu: `oder 6.mp4` (check-hanh-ly-hindi)

Phân tích bằng `SAMPLE/_chung/video-moi.py danh-gia` (08/11/2026) + đọc phụ đề trên hình (cắt vùng phụ đề 2 khung/giây).

## Tổng quan

- 111,2 giây, 720×1280 (9:16). Quảng cáo app **Supernova AI** (gia sư AI tiếng Anh) cho người nói **tiếng Gujarati** (tên dự án ghi "hindi" nhưng lời và phụ đề là Gujarati; người dùng chọn giữ Gujarati như video).
- 0–12 s thuần tiếng Anh; từ "Wow! ..." trở đi Gujarati xen nhiều từ tiếng Anh (English, practice, level, personalized course, mistakes correct, confidently...).
- 41 câu (Whisper), tốc độ nói trung vị 3,28 từ/giây (câu hỏi tiếng Anh ngắn 4,4–6,9; câu Gujarati dài 2–3).
- **Một cảnh cắt cứng duy nhất ở 56,13 s** = chuyển sang phần 2. Máy đứng yên tuyệt đối ở cả hai phần (tổng dịch 39 px / 56 s và 37 px / 55 s, mức "đứng yên").
- Whisper nhận ngôn ngữ `gu` nhưng trả lời dạng **dịch sang tiếng Anh** → lời Gujarati chép từ phụ đề trên hình, Whisper chỉ dùng lấy mốc giây.
- Phụ đề: chữ đen trên ô trắng bo góc, cỡ nhỏ, ở ~81,5% chiều cao khung, hiện từng cụm 2–4 từ; cùng kiểu cho mọi người nói, cả hai phần. Không có ❌/✅ hay viền màu trên hình ở câu "I have 62" (Studio thêm theo khuôn).
- Không có end card / logo / popup trong video (câu kêu gọi tải app do robot nói trong ô).

## Cấu trúc phần

| Phần | Giây | Cơ chế Studio | Nội dung |
|---|---|---|---|
| 1 | 0–56,1 | cảnh thường, 2 nhân vật chung khung, MỘT góc máy | Nhân viên an ninh (trái) hỏi túi, thử tiếng Anh, khen; người phụ nữ (phải) kể luyện nói với Supernova AI ("Miss Nova"), giải thích app |
| 2 | 56,1–111,2 | ghép 2 lớp | Người phụ nữ đứng giữa sảnh nhìn ống kính; robot AI trong ô góc trên phải: hỏi đáp, sửa "I have 62" → "I am 62", giới thiệu, giá, kêu gọi tải app |

Chuyển phần: cắt cứng trong video; Studio dùng nhoè 0,5 s như các thể loại cùng khuôn.

## Bố cục

**Phần 1** (một khung suốt 56 s): cận trung hai người từ eo trở lên, máy ngang ngực, hơi chéo từ phía trước băng chuyền.
- Nhân viên: trái, mặt ở (0,26; 0,20), khuỷu tay trái tì nóc máy soi inox, tay phải thả gần khay; nam Ấn Độ ~28 tuổi, tóc đen dày gợn sóng, râu lún phún, áo sơ mi trắng ngắn tay, gi-lê xanh navy, cà vạt navy, dây đeo thẻ xanh dương thẻ trắng.
- Người phụ nữ: phải, mặt ở (0,74; 0,32) to hơn, quay 3/4 sang trái; ~60 tuổi, tóc búi thấp, bindi đỏ, dây chuyền vàng, sari lụa xanh lá hoạ tiết đỏ viền đỏ-vàng, áo blouse đỏ; túi da nâu lớn đeo vai, tay phải nắm quai.
- Tiền cảnh dưới: khay nhựa xanh dương trên băng chuyền, trong khay túi da nâu kiểu doctor bag (góc dưới trái).
- Nền: nhà ga sáng, cửa kính cao, biển treo xanh navy có hình máy bay, tranh dân gian cam-vàng góc trên phải, cây cọ, hành khách xa sau dải chắn xanh.

**Phần 2**: người phụ nữ giữa khung, từ hông trở lên, đỉnh tóc ~22% từ trên, nhìn thẳng ống kính, tay phải nắm quai túi (túi bên trái hình). Nền sảnh sân bay mờ (đèn trần dải trắng, bảng thông tin vàng).
Ô robot đo bằng OpenCV trên khung 60 s: **x 0,662, y 0,013, rộng 0,300, cao 0,253** (216×324 px trên 720×1280 → gen 9:16), bo góc, **viền trắng mảnh**. Robot: đầu trắng bóng kiểu trẻ con, mắt xanh nhạt to, tai tròn đen-bạc như tai nghe, ngực trắng có đèn tròn xanh, nền xanh dương đậm chuyển sáng.

## Giọng (cao độ đo)

| Người | Hz | Mô tả |
|---|---|---|
| Nhân viên | 105–200, trung vị ~150 | nam trẻ, baritone nhẹ, thân thiện |
| Người phụ nữ | 211–260 | nữ ~60, ấm, giọng Gujarati, tiếng Anh giọng Ấn |
| Robot AI | 230–300 | nữ trẻ sáng, hơi máy (nhóm B cao hơn người phụ nữ ở phần 2) |

## Bảng hành động (phần 1)

| # | Giây | Ai | Lời (phụ đề) | Người nói | Người nghe | Khung cuối |
|---|---|---|---|---|---|---|
| 1 | 0–0,7 | NV | Is this your bag? | ngón trỏ phải chỉ xuống túi trong khay (đã chỉ từ khung đầu) | nhìn NV, cười | tay NV trên túi |
| 2 | 1,0–1,2 | PN | Yes. | gật nhẹ | NV vẫn chỉ | như cũ |
| 3 | 1,5–2,3 | NV | Can you speak English? | rút tay khỏi túi, mỉm cười | nhìn NV | tay NV ở mép khay |
| 4 | 2,8–3,7 | PN | Yes, of course. | gật tự tin | cười | — |
| 5 | 4,2–5,4 | NV | Can you prove it to me? | cười tinh nghịch, nghiêng người | cười | — |
| 6–7 | 5,7–11 | PN | I have come to New York to visit my brother. I will be staying here for 10 days and then I will go back home. | nói rõ, tay khẽ ngửa | NV gật | (tách 2 lượt: 23 từ) |
| 8 | 12–14,3 | NV | Wow! તમારી English તો બહુ સરસ છે. | nhướng mày, khen | cười ngượng | — |
| 9 | 14,9–15,4 | PN | Thank you. | cúi đầu nhẹ | cười | — |
| 10 | 16–22 | PN | Honestly, હું બસ રોજ 15 to 20 minutes Supernova AI પર speaking practice કરું છું. | kể | NV chống khuỷu tay nghe | — |
| 11 | 22–30 | PN | Daily conversationsથી લઈને real life situationsમાં કેવી રીતે વાત કરવી, એ બધું Miss Nova મને શીખવાડે છે. | giải thích | gật | — |
| 12 | 30–37 | PN | અને મારા level પ્રમાણે Supernova AI એક personalized course પણ બનાવે છે, જેનાથી મને English શીખવામાં ઘણી સરળતા રહે છે. | tự hào | tò mò dần | — |
| 13 | 37,3–38,5 | NV | Supernova AI? | chỉ tay xuống túi lần nữa (37,8–38,8 s) | cười gật | tay NV gần túi |
| 14 | 38,9–44 | PN | હા, આ એક AI teacher છે, જેની સાથે તમે રોજ Englishમાં વાત કરીને practice કરી શકો છો. | gật, giải thích | rút tay về | — |
| 15 | 44,6–48 | PN | આ ક્યારેય તમને judge નહીં કરે કે તમારી Englishની મજાક નહીં ઉડાવે. | lắc đầu nhẹ | cười | — |
| 16 | 48–54 | PN | એક સારા friendની જેમ તમારી mistakes correct કરશે અને તમને confidently English બોલવામાં help કરશે. | tự tin | gật | — |
| 17 | 54,7–56 | PN | ચાલો, હું તમને બતાવું. | cười | cười chờ | cắt sang phần 2 |

Khoảnh khắc chuyển động mạnh: 5,1–6,4 s và 14,6–16,4 s (người phụ nữ cử động đầu/tay khi nói), 37,4–39,3 s (NV chỉ tay xuống túi), 55,9–56,5 s (cảnh cắt sang phần 2); còn lại là cử động đầu khi nói.

## Lượt phần 2

AI: "શું તમને English આવડે છે?" → PN: "હા, બસ થોડું ઘણું." → AI: "તમારી ઉંમર કેટલી છે?" → PN: "I have 62." (sai) → AI: "તમારે કહેવું જોઈએ, I am 62." → PN: "I am 62." (đúng) → AI: "Good job." → PN: "Thank you." + "પણ તમે કોણ છો?" (gộp) → AI giới thiệu (2 lượt) → PN: "Really?" → AI: "ચોક્કસ, ..." → PN: "પણ આ તો બહુ મોંઘું હશે ને?" → AI: giá rẻ hơn 7 lần, 1 crore+ người dùng, kêu gọi "Install Now" + tải app (4 lượt).
Trong phần 2 người phụ nữ gần như đứng yên, tay phải nắm quai túi; robot cử động miệng, nghiêng đầu nhẹ.

## Video gốc → kịch bản

| Video gốc | Kịch bản Studio | Lý do |
|---|---|---|
| Phần 1 một clip liền 56 s | 17 cảnh (mỗi lượt một cảnh), cùng một góc, nối khung cuối | Muse một người nói mỗi clip |
| Lượt 6 (23 từ) | tách 2 lượt | ≤ 20 từ/lượt |
| "Thank you." + "પણ તમે કોણ છો?" (cùng người, liền nhau) | gộp 1 lượt | bớt một cảnh |
| Câu AI giới thiệu 3 câu | 2 lượt (16 + 9 từ) | ≤ 20 từ |
| Cắt cứng vào phần 2 | nhoè 0,5 s | khuôn chung |
| Phụ đề từng cụm 2–4 từ | phụ đề cả câu (tự xuống dòng), chữ đen ô trắng, cùng độ cao | Studio chưa làm phụ đề theo cụm |
| Không ❌/✅ | ❌ + viền đỏ ở "I have 62.", ✅ + viền xanh ở "I am 62." | khuôn gia sư AI (bỏ `fx`/`icon` trong `tao_bien_the.py` nếu muốn y video) |
| Tên app "Supernova AI" | giữ, khai một chỗ `APP` trong `tao_bien_the.py` | đổi app chỉ sửa một dòng |
