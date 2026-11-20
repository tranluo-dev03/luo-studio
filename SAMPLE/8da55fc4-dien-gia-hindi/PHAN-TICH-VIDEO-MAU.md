# Phân tích video mẫu: `8da55fc4-Speaker-HINDI-sample.mp4`

Công cụ: `video-moi.py danh-gia --lang hi` → `userdata/studio/claude/_uploads/8da55fc4-Speaker-HINDI-sample-phan-tich/` (`bao-cao.md`, `danh-gia.md`, `luot_01..09.jpg`, `chuyen-dong_01..09.jpg`, `tong-quan_1..2.jpg`). Đã xem ảnh tổng quan 1 khung/giây và các ảnh lượt tiệc (luot_04) + giơ điện thoại (luot_09).
Ghi chú: file này trùng từng byte (md5 `612b43fa…`) với `8eecbce1-Speaker-HINDI-sample.mp4` đã làm ở `SAMPLE/8eecbce1-dien-gia-hindi/`; số đo hai lần chạy khớp nhau. Lần này cấu trúc người dùng chỉ định KHÔNG có demo/CTA nên kịch bản chỉ còn phần sân khấu.

## Tổng quan
- 25,6 s, 1440×2560 (9:16), 30 fps. Hindi xen cụm tiếng Anh. App **Talka AI** (badge logo + chữ "Talka AI" góc trên trái suốt video).
- 9 câu Whisper, **tốc độ nói trung vị 3,42 từ/giây** (cao nhất 3,75), khoảng lặng trung vị 0,55 s. Cảnh cắt cứng: 4,97 s và 9,97 s.
- Máy: đứng yên 0–10 s; 10–25,6 s rung/đẩy rất nhẹ → Studio giữ máy đứng yên.
- Một nhân vật (mặt thứ 2 công cụ đếm = đầu khán giả mờ / vai khách mờ ở tiền cảnh / mặt robot trên điện thoại).
- Giọng: một người nam; công cụ tách 2 cụm (A ~150 Hz: 105–167; B ~205 Hz: 174–241) do lên giọng khi nhấn mạnh (hook, "फ़्री है") → `GIONG_HOC` "around 130–170 Hz, lifts to about 200 Hz on emphasis".
- Không có đoạn quảng cáo/end card; video dừng khi giơ điện thoại nói "देखिए!".

## Cấu trúc phần
| Đoạn | Giây | Nội dung |
|---|---|---|
| Hook | 0:00–0:05 | Sân khấu kiểu TED: rèm xanh navy, khối 3D đỏ phát sáng, bục tròn đỏ, đầu khán giả mờ dưới khung. Diễn giả đứng (từ gối trở lên), nhìn ống kính, giơ ngón trỏ tay phải (tay cầm bút bấm). |
| Nỗi đau | 0:05–0:10 | Cắt sang tiệc sang trọng (đèn chùm vàng, hoa trắng, bàn ly nến). Người hơi xoay sang PHẢI khung, mắt nhìn sang phải về vị khách (vai/gáy mờ ở góc dưới phải), ly champagne tay trái ngang bụng, bút bấm tay phải buông. 3 câu sai hiện lần lượt, gạch đỏ + ô X đỏ. |
| Thú nhận | 0:10–0:14 | Về sân khấu (khung gần hơn), cười tự giễu, nghiêng đầu. *Lỗi liên tục video gốc: vẫn cầm ly champagne tới ~14 s* → Studio bỏ ly. |
| Giải pháp | 0:14–0:25,6 | Tay trái ngửa lòng bàn tay giới thiệu ("Talka AI"), hai tay mở khi nói "ba tuần"; ở "देखिए" tay trái giơ điện thoại ngang vai, màn hình ra ống kính (hình robot). |

## Lời (đối chiếu phụ đề trên hình, sửa chỗ Whisper nghe nhầm)
| Lượt | Giây | Phụ đề trên hình (đúng) | Whisper nghe |
|---|---|---|---|
| 1 | 0,0–4,5 | जब कोई आपसे “Nice to meet you” कहे, तो कभी भी “Me too” मत बोलिए। | …नाइस तो मीटु कहे… |
| 2 | 5,0–8,7 | Me too / You're welcome / I'm fine, thanks (3 dòng chữ gạch) | मीटु / यो वल्क्म / अं फाँई फाँई |
| 3 | 9,9–11,8 | पहले मैं भी ऐसे ही जवाब देता था। | …एसे जवाब… |
| 4 | 14,3–17,9 | लेकिन फिर मैंने Talka AI के साथ प्रैक्टिस करना शुरू किया। | …तल का एएएए… |
| 5 | 17,9–22,8 | सिर्फ़ तीन हफ़्तों में मैं फ़्लुएंटली और कॉन्फ़िडेंस के साथ इंग्लिश बोलने लगा। | (gộp với lượt 4, 23 từ → tách 2 lượt) |
| 6 | 23,0–25,6 | और ये बिल्कुल फ़्री है। देखिए! | |

## Bảng hành động
| Lượt | Ai nói | Hành động người nói | Người nghe | Vật dụng | Ánh mắt | Camera | Khung cuối |
|---|---|---|---|---|---|---|---|
| 1 | Diễn giả | Giơ ngón trỏ tay phải ngang vai từ 0,5 s, giữ suốt câu, hạ ở ~4,5 s | Khán giả mờ, im | Bút bấm tay phải, micro cài tai | Ống kính | Đứng yên | Hai tay ngang bụng, miệng khép |
| 2 | Diễn giả | Đáp xã giao đều đều, gật nhẹ, cười gượng | Khách tiền cảnh phải (vai mờ), im | Ly champagne tay trái, bút bấm tay phải | Sang phải, về vị khách | Đứng yên | Cười gượng, cầm ly |
| 3 | Diễn giả | Cười tự giễu, nghiêng đầu, gật nhẹ | — | (Ly champagne – lỗi video gốc, bỏ) | Ống kính | Đứng yên | Cười, tay ngang bụng |
| 4 | Diễn giả | Tay trái ngửa lòng bàn tay ra trước như giới thiệu, rồi hạ | — | Bút bấm | Ống kính | Đẩy rất nhẹ | Tươi cười, tay ngang bụng |
| 5 | Diễn giả | Hai bàn tay mở nhẹ ngang bụng | — | Bút bấm | Ống kính | Rung nhẹ | Tay về ngang bụng |
| 6 | Diễn giả | Ở "देखिए" tay trái giơ điện thoại ngang vai, màn hình ra ống kính | — | Điện thoại (hình robot) | Ống kính | Rung nhẹ | Điện thoại vẫn giơ, cười |

## Hiệu ứng / chữ và cách Studio làm
| Thành phần | Studio |
|---|---|
| Phụ đề Hindi trắng viền đen giữa khung | Hậu kỳ dùng chung `types/san-khau-chia-doi-gia-su-ai/post.py` (Nirmala UI + shaping complex vì `HAU_KY.ngon_ngu = hi`) |
| 3 câu sai gạch đỏ + ô X đỏ + tiếng sai | `"gach": true` ở lượt 2 (post.py `gach_lines`) |
| Badge "Talka AI" góc trên trái | Thương hiệu: logo cố định |
| Màn hình điện thoại hình robot | Muse gen (`DAO_DIENTHOAI`, không chữ) |

## Bảng "video gốc → kịch bản"
| Video gốc | Kịch bản Studio | Ghi chú |
|---|---|---|
| Hook sân khấu 0–5 s | Cảnh 1 (Prompt ảnh sân khấu) | Giữ ngón trỏ tay phải |
| Tiệc 5–10 s | Cảnh 2 (Prompt ảnh mới, khung trung, khách mờ tiền cảnh phải) | Chữ gạch do hậu kỳ; thêm nét nhăn mặt ngượng cuối câu theo insight |
| Thú nhận 10–14 s | Cảnh 3 (`Khung đầu từ cảnh: 1`) | Bỏ ly champagne lọt lên sân khấu; bỏ đổi cỡ cảnh |
| Giải pháp 14–23 s | Cảnh 4 + 5 (câu 23 từ tách 2 lượt) | Máy đứng yên (bỏ đẩy/rung nhẹ) |
| "Miễn phí, xem này" + giơ điện thoại | Cảnh 6 | Màn hình chỉ có mặt robot, không chữ |
| Badge Talka AI | Không gen → Thương hiệu | |

## Insight (người dùng nhập, chép nguyên văn)

```
"Insight 1: Priya - Người phụ nữ công sở Ấn Độ “biết tiếng Anh” nhưng mở miệng là lộ tiếng Anh sách vở

Nhân khẩu học: 28–55 tuổi, chủ yếu là nữ (8/9 video; 1 video là nam khoảng 30 tuổi mặc vest). Người Ấn Độ sống tại Ấn Độ, tiếng mẹ đẻ là Hindi, dùng điện thoại Android. Thuộc tầng lớp trung lưu thành thị đang đi lên, có học, có nghề. Dải tuổi trải từ cô gái trẻ tóc bob đến người phụ nữ tóc bạc đeo kính mặc saree, trọng tâm rơi vào 35–50.

Hình ảnh xuất hiện: “chỉn chu, thành đạt”, ngược hẳn với Maria. Trang phục là saree lụa viền vàng, anarkali thêu, blazer với chân váy, suit trắng hoặc đỏ mận, kurta khoác blazer. Tóc gọn, có bindi, trang sức vàng nhỏ, đeo micro cài tai và cầm bút bấm slide. Đây là hình ảnh mà user muốn trở thành: người đứng trên sân khấu, được cả khán phòng lắng nghe. Cảnh nỗi đau vẫn là con người đó, vẫn đẹp và sang, nhưng mặt nhăn lại vì ngượng giữa bữa tiệc.

Công việc chính:

Nhân viên hoặc quản lý cấp trung ở công ty có khách hay sếp nước ngoài (IT, dịch vụ, ngân hàng, bảo hiểm)
Giáo viên, giảng viên, hiệu phó trường tư
Chủ doanh nghiệp nhỏ như boutique, xuất khẩu hàng thủ công, trung tâm đào tạo
Nhân sự, hành chính, sales, chăm sóc khách hàng doanh nghiệp
Bác sĩ, kế toán, luật sư học bằng tiếng Hindi rồi lên thành phố lớn
Người hay đi hội nghị, sự kiện ngành, tiệc công ty, đám cưới thượng lưu
Điểm chung của cụm việc này: làm chuyên môn thì không cần tiếng Anh giỏi, nhưng muốn thăng tiến thì phải qua những khoảnh khắc xã giao bằng tiếng Anh, và đó là lúc nỗi đau nổ ra.

Trình độ: A2–B1. Học tiếng Anh nhiều năm ở trường, đọc hiểu được, viết email được. Khi nói thì chỉ có một kho câu thuộc lòng từ sách giáo khoa và bật ra theo phản xạ: “Nice to meet you” → “Me too”, “How are you” → “I’m fine, thanks”, cái gì cũng “You’re welcome”. Câu không sai ngữ pháp nặng nhưng nghe cứng và “rất Ấn Độ học trường làng”. Thiếu hẳn lớp tiếng Anh đời thường mà người bản ngữ dùng mỗi ngày, đúng 5 câu video dạy. Vẫn cần nghĩa tiếng Hindi và phiên âm đọc-sao-viết-vậy, tức là chưa đọc được IPA và chưa tự tin phát âm. Đau nhất là cô không biết mình sai: cô tưởng “Me too” là đúng, cho đến khi thấy người đối diện khựng lại.

Nỗi đau cốt lõi:

Tiếng Anh sách vở làm cô trông kém hơn năng lực thật, trong khi cô giỏi nghề
Sợ mất mặt trước người ngang hàng và cấp trên; ở Ấn Độ tiếng Anh là thước đo đẳng cấp
Không biết mình sai ở đâu, vì chưa từng ai sửa, chỉ thấy người ta cười lịch sự rồi quay đi
Không có ai để luyện nói mà không bị phán xét; đi học lớp giao tiếp ở tuổi này thì ngại
Đã học tiếng Anh cả chục năm mà vẫn không nói được, nên mất niềm tin vào cách học cũ

Động lực thật:

Được nhìn nhận đúng tầm: nói tiếng Anh tự nhiên để người ta thấy cô là người có trình độ
Thăng tiến: được giao tiếp khách, thuyết trình, đại diện công ty
Tự tin ở những nơi sang trọng (tiệc, hội nghị, khách sạn, sân bay) mà không phải đứng nép
Hình mẫu mơ ước là đứng trên sân khấu nói trước đám đông
Muốn nhanh và không tốn tiền: “ba tuần”, “hoàn toàn miễn phí”

10 tình huống chạm vào nỗi đau của Priya:

Tiệc networking — đối tác nước ngoài bắt tay nói “Nice to meet you”, Priya đáp “Me too”, người kia khựng nửa giây rồi quay sang người khác → lộ tiếng Anh sách vở + mất cơ hội kết nối (cảnh gốc của video).
Hành lang công ty — sếp người nước ngoài hỏi “How’s it going?”, Priya đáp như trả bài “I’m fine, thank you, and you?”, đồng nghiệp trẻ bên cạnh nhịn cười → bị coi là “quê” trước người kém tuổi mình.
Họp online với khách — khách nói nhanh, Priya không nghe kịp nhưng không biết nói “I didn’t catch that”, đành gật và “yes, yes”, sau đó làm sai yêu cầu → không dám hỏi lại + hậu quả công việc thật.
Đồng nghiệp gọi lúc cô đang trên đường — cô muốn nói “I’m on my way” mà bật ra “I am coming, I am in the road” → câu đơn giản nhất cũng không tự nhiên.
Quầy check-in hội nghị — lễ tân nói “Thank you for coming”, Priya đáp “You’re welcome”, người xếp hàng sau liếc nhìn → dùng sai câu thuộc lòng nơi công cộng.
Thuyết trình nội bộ — slide chuẩn bị kỹ, nhưng đến phần hỏi đáp có người hỏi vặn, cô cần câu giờ mà không biết nói “Give me a second”, đứng im trước cả phòng → giỏi chuyên môn nhưng sụp ở phần nói tự do.
Đưa tài liệu cho khách — cô nói “Please take” thay vì “Here you go”, khách vẫn hiểu nhưng cô tự thấy mình nói như người giúp việc chứ không như quản lý → câu nói hạ thấp vị thế.
Họp phụ huynh ở trường quốc tế của con — các phụ huynh khác nói tiếng Anh trơn tru, Priya chỉ cười và gật, con cô nói nhỏ “Mẹ đừng nói gì nhé” → nỗi đau nhân đôi vì bị chính con mình ngại.
Phỏng vấn thăng chức — hội đồng chuyển sang tiếng Anh ở phần trao đổi tự do, Priya trả lời bằng những câu ngắn cứng đờ, suất quản lý về tay người kém kinh nghiệm hơn nhưng nói trôi chảy → tiếng Anh chặn trần sự nghiệp.
Bữa tối với đối tác — ai đó rủ “Let’s grab coffee tomorrow?”, cô muốn nói “Sounds good” mà chỉ ra được “Yes, okay, I will come”, cả bàn nói đùa bằng tiếng Anh còn cô ngồi im cầm ly → ngồi giữa bàn tiệc mà đứng ngoài cuộc trò chuyện.

Lưu ý về dàn nhân vật trong 9 video:

Nhóm trẻ 25–32 (video 1, 6, 7): gắn với nỗi lo thăng tiến đầu sự nghiệp.
Nhóm trung niên 40–55 (video 2, 4, 8, 9): gắn với giữ thể diện ở vị trí quản lý.
Nhóm lớn tuổi 55–65 (video 3, saree, tóc bạc): thông điệp “học lúc nào cũng chưa muộn”.
Nam giới (video 5): cùng nỗi đau, bối cảnh công sở."
```

## Cấu trúc hook / tình huống (theo người dùng chỉ định, đối chiếu video)
Người dùng chỉ định:
> Hook: nhân vật đứng trên sân khấu kiểu TED nói “Khi ai đó nói Nice to meet you, đừng bao giờ đáp Me too”.
> Nỗi đau: cảnh tiệc sang trọng, tay cầm ly champagne, mặt ngượng, ba câu bị gạch đỏ là “Me too”, “You’re welcome”, “I’m fine, thanks”, kèm lời thú nhận “Trước đây tôi cũng trả lời y như vậy”.
> Giải pháp: “Rồi tôi bắt đầu luyện với Talka AI. Chỉ ba tuần tôi đã nói tiếng Anh trôi chảy và tự tin. Và nó hoàn toàn miễn phí.”

| Phần | Video | Lượt kịch bản | Khớp? |
|---|---|---|---|
| Hook | 0:00–0:05 | 1 | Khớp |
| Tình huống: nỗi đau | 0:05–0:14 (tiệc 0:05–0:10 + thú nhận trên sân khấu 0:10–0:14) | 2–3 | Khớp; lời thú nhận nói trên SÂN KHẤU chứ không ở tiệc |
| Tình huống: giải pháp | 0:14–0:25,6 | 4–6 | Khớp; video có thêm "देखिए!" + giơ điện thoại (giữ) |
| Quảng cáo / end card | không có (chỉ badge Talka AI) | — | `quang_cao: null`; badge = Thương hiệu |

Chi tiết mốc giây + lời: `CAU-TRUC.json`. Hook mới kịch bản B: tình huống "hành lang công ty" của insight ("How's it going?" → đừng đáp "I'm fine, thank you").
