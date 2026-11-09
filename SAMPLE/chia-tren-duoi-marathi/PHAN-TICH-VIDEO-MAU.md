# Phân tích video mẫu: `oder 3.mp4`

## Tổng quan

| Mục | Số đo |
|---|---|
| Độ dài, cỡ | 71,3 s; 720×1280; 30 fps |
| Sản phẩm | App học nói tiếng Anh **Supernova AI** (end card: "Hi, I'm Nova. Your 24/7 AI English teacher!", nút "Download now") |
| Ngôn ngữ | **Marathi xen từ tiếng Anh**. Whisper dịch sang tiếng Anh, không chép được: lời trong hồ sơ này đọc từ phụ đề trên hình |
| Cảnh cắt cứng | 0 trong phần hội thoại; đổi sang end card ở ~67,1 s |
| Lượt thoại | 66,5 s hội thoại, 21 lượt sau khi gộp câu liền nhau |
| Tốc độ nói | ~3 từ/giây (đo theo lời thật trên phụ đề, vd. lượt 15: 16 từ / 5,5 s). Con số 4,24 của `bao-cao.md` tính trên chữ Whisper dịch nên KHÔNG dùng |
| Chuyển động máy | Đứng yên ở cả hai ô. Công cụ báo "có chuyển động" do cú chuyển sang end card (67 s) |

## Bố cục

- Khung chia **trên/dưới**, đường chia đo được y = 679/1280 = **0,531**. Không viền, không bo góc.
- **Ô trên (robot):** robot nữ mặt người, tóc đen ngắn, tai nghe viền xanh, cổ cơ khí đen, giáp trắng. Đỉnh tóc sát mép trên, tâm mặt y ≈ 0,15 toàn khung (≈ 28% ô). Thấy tới ngang eo. Nền: phòng làm việc hiện đại, kệ gỗ đèn ấm, cửa kính thành phố bên trái.
- **Ô dưới (người học):** nam Ấn Độ ~25 tuổi, tóc rối, ria mép, áo sơ mi kaki cũ. Tâm mặt y ≈ 0,73 toàn khung (≈ 42% ô), khung từ ngực trở lên. Nền: phòng cũ, tường vữa, kệ hộp thép bên trái, tranh thờ nhỏ, áo khoác treo bên phải.
- Phụ đề: chữ đen trên ô trắng bo góc, tâm y ≈ 0,50 (mép dưới ô robot), cụm 2–4 từ, tô đậm dần từng từ.

## Giọng

| Người | Hz đo được | Âm sắc |
|---|---|---|
| Robot AI (`DAY`) | 240–300 | nữ trẻ, sáng, ấm, rõ, nhanh nhẹn |
| Người học (`HOC`) | 145–190 | nam trẻ, baritone nhẹ, mộc, hơi khàn |

Bộ gom tự động của công cụ tách sai (xếp nhiều câu của robot vào cụm A) nên số trên là đọc lại theo từng lượt đã biết người nói. Hai nhân vật khác giới và gen riêng: không có rủi ro nhép nhầm.

## Bảng hành động

Không có vật dụng nào xuất hiện/đổi tay trong phần hội thoại. Cả hai nhìn thẳng ống kính suốt video, camera đứng yên, khung cuối của mọi lượt: người nói về tư thế nghỉ, miệng khép.

| # | Giây | Ai | Lời (từ phụ đề) | Người nói | Người nghe |
|---|---|---|---|---|---|
| 1 | 0,0–0,9 | AI | काल कुठे गेला होतास? | hỏi vui, tay phải vừa hạ ở góc trái | yên, cau mày nhẹ |
| 2 | 1,3–2,1 | HOC | I go to the market. | nói chậm, nhíu mày, nhắm mắt một nhịp | robot mỉm cười khép miệng |
| 3 | 2,4–6,3 | AI | कालची गोष्ट आहे त्यामुळे go नाही went बोल. I went to the market yesterday. | giảng, môi tròn ở "go", cười ở "yesterday" | gật nhẹ, mỉm cười |
| 4 | 6,7–7,7 | HOC | I went to the market yesterday. | tự tin hơn, nghiêng đầu, cười | robot khép miệng |
| 5 | 8,0–9,7 | AI | Yesterday तू market मध्ये कसा गेला होतास? | hỏi, mắt sáng | yên |
| 6 | 9,8–10,5 | HOC | I go by bus. | nheo mắt, ngập ngừng | robot mỉm cười |
| 7 | 10,7–14,4 | AI | Almost बरोबर आहे. पण चांगलं होईल जर तू बोलशील, I went by bus. | nghiêng đầu, nháy mắt một nhịp | yên, chăm chú |
| 8 | 14,6–16,5 | HOC | ओह, माझी English खरंच खूप weak आहे. | nhắm mắt, nhăn mặt, than | robot đang đưa tay rồi hạ; mỉm cười |
| 9 | 16,8–19,6 | AI | काही हरकत नाही. Supernova AI try केलंस का? | cười tươi, vui | yên, mỉm cười |
| 10 | 19,9–21,2 | HOC | Supernova AI, ते काय आहे? | nhướn mày, tò mò | robot khép miệng |
| 11 | 21,4–28,0 | AI | Supernova AI app वर माझ्यासोबत English बोलण्याची practice करु शकतोस. मी तुझी personal AI teacher आहे. | hào hứng, miệng mở to ở "AI" | cau mày nghe rồi dãn ra |
| 12 | 28,0–32,5 | AI | तू रोज फक्त पंधरा वीस मिनिटं माझ्याशी बोल आणि हळूहळू English बोलण्याचा confidence वाढव. | ấm áp | gật nhẹ |
| 13 | 32,7–34,0 | HOC | पण माझी English तर खूप weak आहे. | nhăn mày, than | robot khép miệng |
| 14 | 34,7–39,8 | AI | काही हरकत नाही. तुझी English level कशीही असो, मी त्यानुसार तुझ्यासोबत practice करेन. | trấn an | mỉm cười |
| 15 | 40,0–45,5 | AI | आणि सर्वात चांगली गोष्ट म्हणजे तुला सगळं समजून घेण्यासाठी फक्त English मध्ये बोलण्याची गरज नाही. | giơ tay ở đầu câu, nhắm mắt một nhịp, cười | nheo mắt rồi cười |
| 16 | 45,9–48,9 | AI | मी तुला मराठीच्या माध्यमातून सुद्धा English समजावून सांगेन. | ấm áp, cười | yên |
| 17 | 49,2–50,6 | HOC | आणि मी चुकीची English बोललो तर? | lo lắng, nhướn mày | robot khép miệng |
| 18 | 51,0–55,5 | AI | तर काहीच tension नाही. तू जितक्या वेळा चुकीचं बोलशील, मी तितक्या वेळा तुला योग्य पद्धतीने समजावेन. | trấn an | mỉm cười |
| 19 | 55,8–60,0 | AI | आणि तुझ्या mistakes correct करेन. तुला कोणी judge करणार सुद्धा नाहीये. | nhấn "judge", nét mặt nghiêm nhẹ | yên |
| 20 | 60,3–61,4 | HOC | मग मी आत्ताच download करतो. | quyết định, ngẩng đầu | robot khép miệng |
| 21 | 61,7–67,2 | AI | योग्य निर्णय. तू खाली दिलेल्या install now button वर click कर आणि Supernova AI download करून घे. | giơ tay ở "तू खाली" | mỉm cười, yên |

## Khoảnh khắc chuyển động mạnh

| Giây | Giải thích |
|---|---|
| 14,25–14,75; 21,12–21,62; 39,88–40,38; 49,12–49,62 | Bàn tay robot giơ lên ở góc trái ô trên, đầu người học cử động khi đổi lượt |
| 32,62–32,75; 57,88–58,12; 60,25–60,5 | Người học bắt đầu nói / đổi tư thế đầu |
| 67,0–70,4 | Chuyển sang end card: điện thoại bay vào kèm chớp sáng, nút "Download now" sáng nhấp nháy |

Các "mặt thứ 3/4" trong `danh-gia.md` là nhận nhầm (kệ, tay robot, tranh nền); chỉ có hai người.

## Bảng thành phần → cách làm

| Thành phần | Cách làm |
|---|---|
| Robot, người học | Muse gen riêng từng người (1:1), ghép 2 lớp |
| Đường chia trên/dưới | `[GHEP HAI LOP]` khung cố định |
| Phụ đề Marathi/Anh | `post.py` + `config.json`, font Nirmala UI |
| End card điện thoại | KHÔNG gen, Thương hiệu → Outro |

## Bảng "video gốc → kịch bản"

| Video gốc | Trong kịch bản | Ghi chú |
|---|---|---|
| Hội thoại 66 s, 17 đổi lượt | 21 lượt / 21 cảnh | Câu liền của một người gộp lại, tách khi > 20 từ |
| Bàn tay robot thỉnh thoảng giơ lên ở góc khung | **Bỏ**, tay ngoài khung | Đơn giản hoá: tay giơ dễ méo và lệch khi nối khung |
| Đầu robot sát mép trên | Đỉnh tóc ~4% ảnh 1:1 | Giữ an toàn khi cắt |
| Sửa lỗi "go → went" chỉ bằng lời | `fx: none` mọi lượt | Như video, không ❌/✅ |
| "Supernova AI? ते काय आहे?" hai câu | Một câu có dấu phẩy | Tránh câu chỉ gồm tên app (nhật ký: Muse ngân nốt trong khoảng lặng) |
| Phụ đề cụm 2–4 từ, tô đậm dần từng từ | Phụ đề theo câu, không tô dần | **Studio chưa làm được**; câu dài tới 4 dòng |
| End card 4 s | Outro | Người dùng chọn trong Thương hiệu |
