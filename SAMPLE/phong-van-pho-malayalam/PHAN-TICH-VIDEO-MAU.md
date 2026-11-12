# Phân tích video mẫu: `1510_interview street hindi_005 (11)`

Công cụ: `SAMPLE/_chung/video-moi.py danh-gia` (ra `...-phan-tich/` cạnh video) + đọc phụ đề từng khung 0,25 s + đo chuyển động miệng ô dưới để biết ai nói ở phần 2.

## Tổng quan

| Mục | Giá trị |
|---|---|
| Độ dài, cỡ | 76,9 s, 720x1280 |
| Ngôn ngữ | **Malayalam** xen từ tiếng Anh (tên file ghi "hindi" là nhầm). Phụ đề chữ Malayalam |
| App | Aiva AI (logo + chữ "Aiva AI" góc trên trái suốt video → Thương hiệu, không gen) |
| Cảnh cắt | 3,97 · 4,83 · 8,27 · 8,9 · 10,97 · 14,13 · 17,8 · 22,6 · **25,7** (vào phần 2) |
| Máy quay | Đứng yên mọi đoạn; rung nhẹ cầm tay 22,6–25,7 s |
| Tốc độ nói | ~2,3 từ/giây (đếm từ phụ đề: câu 12 từ trong 5,1 s; robot 13 từ trong 5,8 s). Số của Whisper không dùng được |
| Giọng | Phóng viên nam ~168 Hz; người bán hàng nữ ~219 Hz; robot giọng nữ trẻ, sáng |
| Whisper | `--lang hi` ra chữ Devanagari vô nghĩa; lời chép tay từ phụ đề |

## Cấu trúc

| Phần | Giây | Cơ chế video gốc | Studio |
|---|---|---|---|
| 1. Phỏng vấn đường phố | 0–25,7 | Hai người chung khung thật, góc qua vai phóng viên; 2 cảnh chèn cận người bán (3,97–4,83; 8,27–8,9) và vài lần đổi cỡ nhẹ | Cảnh thường, MỘT góc, 11 cảnh |
| 2. Gọi AI | 25,7–76,9 | Hai ô tách biệt: robot ô trên (y 0–622), vạch cam (622–654), người bán selfie ô dưới (654–1280) | Ghép 2 lớp, `nen: DAY`, `khung DAY 0,0,1,0.5`, `khung HOC 0,0.5,1,0.5`, cắt cứng |

## Bố cục

- Phần 1: phóng viên tiền cảnh trái, quay lưng (thấy gáy, tai trái, gọng kính, viền râu), áo sơ mi caro hồng trắng, quai ba lô đen, tay chĩa micro đen về ngực người bán. Người bán giữa-phải, nhìn ba phần tư sang trái, áo cánh hồng cánh sen, sari caro nâu xám, bindi đỏ, tóc búi, găng nilon trong; trước mặt xe đẩy inox nhiều nồi (nhân, tương, đồ chiên). Nền: phố cũ, nhà hai tầng, mái hiên xanh, cây, trời âm u.
- Phần 2: robot trắng đeo tai nghe có mic, chữ "AI" trên trán, nền tím than có vòng sáng; ô dưới người bán quay selfie ở chợ đông, khay đồ ăn phía sau.
- Phụ đề: chữ đen ô trắng bo góc, 1–3 từ một lần, tâm y ≈ 640/1280 ở cả hai phần (phần 2 nằm đè lên vạch cam).

## Bảng hành động

| # | Giây | Ai nói | Lời (từ phụ đề) | Người nói làm gì | Người nghe | Vật dụng | Ánh mắt | Camera | Khung cuối |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0–2,9 | PV | അപ്രതീക്ഷിതമായി എന്നതിന് ഇംഗ്ലീഷിൽ എന്താ പറയുക? | hỏi đố, micro giữ yên | người bán nặn nhân bằng tay đeo găng, nghĩ | micro, găng, xe đẩy | nhìn nhau | qua vai, đứng yên | tay cô trên nồi |
| 2 | 3–3,6 | Bán | Suddenly. | trả lời ngay | PV gật | | | | |
| 3 | 3,75–4,1 | PV | ഉടനെ. | đố tiếp | | | | | |
| 4 | 4,25–4,8 | Bán | Immediately. | trả lời | | | | cận cô (3,97–4,83), bỏ | |
| 5 | 5–6,9 | PV | ഇത് പറ...നോക്കട്ടെ, അല്ലെങ്കിൽ... | đố, bỏ lửng | cô cười | | | | |
| 6 | 7–7,9 | Bán | Otherwise. | trả lời | | | | | |
| 7 | 8–8,4 | PV | അതുകൊണ്ട് | đố | | | | | |
| 8 | 8,5–9,1 | Bán | Therefore. | trả lời, tự hào | | | | cận cô (8,27–8,9), bỏ | |
| 9 | 9,25–14,4 | PV | ഒരു മാസം മുൻപ് വരെ ... പറഞ്ഞിരുന്നല്ലോ. | thán phục, tay trái mở ra | cô cười ngượng | | | | |
| 10 | 14,5–19,6 | Bán | Yeah, three months ago the only English ever heard was from TV and now I am talking fluently. | kể tự hào | PV gật | | | | |
| 11 | 19,75–25,7 | Bán | ശരിക്കും ... സീക്രട്ട് എന്താണെന്നോ? ആദ്യദിവസം മുതൽക്കേ സംസാരിച്ച് തുടങ്ങണം. വാ ഞാൻ കാണിച്ചുതരാം. | nghiêng người kể bí mật, cuối câu vẫy tay đeo găng rủ lại | PV nghe | | | rung nhẹ từ 22,6 | → cắt cứng |
| 12 | 26–31,8 | Robot | വെറും ഒരു മാസത്തിനുള്ളിൽ ... എന്നറിയാമോ? ഇതൊരു മാജിക് ഒന്നുമല്ല. | nói thẳng ống kính | cô nghe | | nhìn ống kính | ô trên/dưới | |
| 13 | 32–37,8 | Robot | നിങ്ങൾ സംസാരിക്കുമ്പോൾ തന്നെ ... ആപ്പ് ആണിത്. | | | | | | |
| 14 | 38–40,2 | Robot | നമുക്കൊന്ന് ട്രൈ ചെയ്യാം. ... അറിയാമോ? | | | | | | |
| 15 | 40,5–41 | Bán | കുറച്ച്. കുറച്ച്. | ngập ngừng | | | | | |
| 16 | 41,25–41,6 | Robot | Where are you from? | | | | | | |
| 17 | 41,75–42,6 | Bán | I am Kannur. (phụ đề "I am കണ്ണൂർ") | câu sai | | | | không ❌/✅ | |
| 18 | 42,75–46,6 | Robot | ഏകദേശം ശരിയാണ്. പക്ഷേ I am from Kannur എന്ന് പറയുന്നതായിരിക്കും കുറച്ചുകൂടി നല്ലത്. | sửa câu | | | | | |
| 19 | 46,75–49 | Bán | അയ്യോ, എനിക്ക് എപ്പോഴും ഇവിടെയാണ് കൺഫ്യൂസ് ആകുന്നത്. | ngượng | | | | | |
| 20 | 49,25–52,4 | Robot | അതുകൊണ്ടാണല്ലോ ഞാൻ ഇവിടെ ഉള്ളത്. ... സഹായിക്കാൻ. | | | | | | |
| 21 | 52,5–54,6 | Bán | പക്ഷേ, ഇതിന് expensive ആയിരിക്കില്ലേ? | lo lắng | | | | | |
| 22 | 54,75–58,2 | Robot | നോർമൽ ഇംഗ്ലീഷ് ക്ലാസ്സിനേക്കാൾ ഏഴു മടങ്ങ് ... ലഭിക്കും. | | | | | | |
| 23 | 58,25–61,3 | Robot | ദിവസവും വെറും പതിനഞ്ച് ... practice ചെയ്താൽ മതി. | | | | | | |
| 24 | 61,5–68,3 | Robot | മലയാളത്തിലൂടെ practice ... confident ആകും. വെറും ഒരു AI ടീച്ചർടെ കൂടെയുള്ള അസ്സൽ ഇംഗ്ലീഷ് practice. | | | | | | |
| 25 | 68,5–71 | Bán | അതായത്, ഒരു real ടീച്ചറിനെ പോലെയാണോ? | tò mò | | | | | |
| 26 | 71,25–76,9 | Robot | അതെ, ഇത് നിങ്ങളുടെ grammar-ഉം pronunciation-ഉം ശരിയാക്കും. ഒപ്പം confidence-യോടെ ... സഹായിക്കും. | | | | | | hết video |

Khoảnh khắc chuyển động mạnh trong `bao-cao.md`: 3,4–5,1 s và 8–11,3 s là cảnh chèn cận; 13,9–26,1 s là đổi cỡ cảnh + rung tay + cắt vào phần 2; 42,1 s là người bán nói "I am Kannur". Không có hành động đồ vật nào khác.

## Video gốc → kịch bản

| Video gốc | Kịch bản | Lý do |
|---|---|---|
| 8 cảnh cắt trong phần 1 (2 cận người bán + đổi cỡ nhẹ) | MỘT góc qua vai đứng yên, 11 cảnh nối khung | Sổ tay 2.2: đổi cỡ cảnh làm mặt/trang phục trôi |
| Rung cầm tay 22,6–25,7 s | Máy đứng yên | Muse rung máy dễ trôi khung |
| PV nói "một tháng", người bán nói "ba tháng" | Thống nhất "one month" | Mạch lời khớp với robot "trong một tháng" |
| Hai câu liền của một người | Gộp một lượt (≤ 20 từ) | Lượt 10, 11, 12, 24, 26 |
| Robot đeo tai nghe, chữ "AI" trên trán, nền tím | Robot Talka theo ảnh người dùng + tai nghe; không chữ trên trán; nền tím có vòng sáng | Người dùng chọn robot Talka; không chữ trong hình |
| Vạch cam ngang giữa hai ô | Chưa làm | Hậu kỳ chung chưa vẽ vạch; ghi "còn khác" |
| Phụ đề 1–3 từ/lần | Phụ đề theo câu | Hậu kỳ chung |
| Logo "Aiva AI" góc trên trái | Thương hiệu (logo cố định) | Không gen |
