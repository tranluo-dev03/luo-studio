# Phân tích video mẫu: `324369fe-X0071-Split-screen-HINDI_003-5.mp4` (mã `san-khau-x0071-hindi`)

## Tổng quan
- 75,0 s, 1080×1920, 18 câu Whisper (tiếng Hindi xen tiếng Anh), 5 cảnh cắt cứng (giây 5.03 / 9.37 / 25.17 / 59.7 / 70.0), tốc độ nói trung vị 3,73 từ/giây.
- Một nhân vật nam Ấn Độ (~28–32 tuổi, vest navy, mic cài tai) + một robot gia sư AI "Talka AI" (đầu trắng bóng, mũ lưỡi trai xám, kính đen, áo khoác bomber, giáp ngực lục giác viền cyan phát sáng).
- Giọng: diễn giả ~118–151 Hz (cụm A, đo được 103–151 Hz tuỳ lượt), robot/giọng tổng hợp ~162–212 Hz (cụm B) ở các câu đầu — nghe lại xác nhận: cụm B là chính giọng diễn giả khi nói to/nhấn ở câu mở đầu và phần cao trào, cụm A là giọng khi nói thường/robot; không có hai người khác nhau cùng khung nên không có rủi ro nhép sai.
- **Đây CHÍNH LÀ video gốc đã dùng để tạo `BIEN-THE-X0057-X0071-HINDI-20.json`** trong `SAMPLE/san-khau-chia-doi-gia-su-ai/` (thể loại "diễn giả sân khấu + thẻ từ vựng chia đôi gia sư AI", xem README của thể loại đó). Thư mục `san-khau-x0071-hindi/` này đóng gói LẠI đúng một biến thể mẫu của video đó theo yêu cầu "hai dạng kịch bản" (goc / đổi hook) + `CAU-TRUC.json`, dùng CHUNG code `app/production/types/san-khau-chia-doi-gia-su-ai/`.

## Cấu trúc phần (đối chiếu công cụ `video-moi.py danh-gia` + xem ảnh `luot_NN.jpg`/`tong-quan_N.jpg`)

| Đoạn | Giây | Nội dung thấy trên hình | Studio |
|---|---|---|---|
| HOOK | 0:00–0:05 | Diễn giả đứng sân khấu hội nghị (phông rèm xanh navy, hoa trắng, khối 3D đỏ mờ phía sau), giơ ngón trỏ, nói nguyên tắc "đừng đáp Me too" | **Phần 1**, cảnh 1 (có Prompt ảnh) |
| NỖI ĐAU | 0:05–0:11 | Cắt sang tiệc sang trọng (đèn chùm vàng, hoa trắng), diễn giả cầm ly champagne, phụ đề liệt kê dần "Me too ❌ / You're welcome ❌ / I'm fine, thanks ❌"; quay lại sân khấu cười tự giễu | **Phần 1**, cảnh 2 (đổi bối cảnh, Prompt ảnh riêng) + cảnh 3 (`Khung đầu từ cảnh: 1`) |
| GIẢI PHÁP | 0:11–0:23,6 | Diễn giả kể đã luyện Talka AI, 3 tuần, miễn phí; giơ điện thoại (màn hình chỉ có ảnh robot, không chữ) | **Phần 1**, cảnh 4–6 |
| KHÔNG GEN | 0:59,7–1:15 | Avatar robot phát sáng giữa khung; popup cài app "Talka AI: Language Tutor" (Cancel/Open, % tải); ảnh màn hình app; end card "GET IT ON Google Play" | **Thương hiệu** (logo / Video giới thiệu / Outro của dự án) |
| DEMO | 0:23,6–0:59,7 | Chuyển cảnh nhoè; màn hình chia đôi DỌC: robot trái / diễn giả phải; 5 vòng robot hỏi "... tiếng Anh là gì?" + đọc mẫu + mời lặp theo → diễn giả lặp lại 1 lần; thẻ chữ trắng viền xanh/vàng phía DƯỚI khung hiện nghĩa Hindi + phiên âm, từ đang đọc tô vàng | **Phần 2**, ghép 2 lớp (`chia-doi-gia-su-ai`), 10 lượt, `noi: cat`, vào bằng nhoè 0,5 s |

Lượt kịch bản: 6 (phần 1: hook 1 + nỗi đau 2 + giải pháp 3) + 10 (phần 2: 5 vòng × 2) = 16 lượt, khớp 16 phần tử mảng `LUOT` của biến thể.

## Bố cục / vị trí nhân vật
- Phần 1: một khung dọc 9:16, diễn giả đứng giữa, từ đùi/ngực trở lên tuỳ cảnh, camera đứng yên tuyệt đối (đo chuyển động: 0/6 đoạn có dịch máy thật, hai đoạn "rung nhẹ/cầm tay" 9,4–25s và 59,7–70s là do cắt cảnh demo + robot phát sáng, không phải lia máy trong một clip).
- Phần 2: chia dọc 50/50 — robot bên trái (đầu ở ~18% bề rộng khung, đỉnh đầu ~20% chiều cao), diễn giả bên phải (đối xứng); mỗi nửa gen riêng 9:16 rồi cắt dải giữa theo khuôn `[GHEP HAI LOP]`. 17% dưới khung mỗi nửa chừa trống cho thẻ từ vựng.

## Giọng
- Diễn giả: nam, ~118–151 Hz lúc nói thường, ~162–212 Hz lúc nhấn giọng mở đầu/cao trào ("và ये बिल्कुल फ्री है! देखिए" ở cường độ cao) — ghi vào `GIONG_HOC`: "natural mid pitch around 120–150 Hz" (đã có trong biến thể, giữ nguyên).
- Robot gia sư (phần 2): giọng tổng hợp trầm, ước lượng 95–120 Hz theo mẫu của toàn bộ gia đình `*-gia-su-ai` (chưa đo trực tiếp robot của video này vì phần 2 lời Whisper nghe lẫn nhiều, đã đối chiếu bằng mắt qua `tong-quan_2/3.jpg`).

## Hiệu ứng / chữ trong hình và cách Studio làm
| Thấy trên hình | Cách làm |
|---|---|
| Phụ đề song ngữ (Hindi karaoke dưới, câu demo trên) | Phần 1: phụ đề do `_chung/phu_de.py` (trắng viền đen, font Nirmala UI + shaping complex vì chữ Devanagari — `post.py` tự bật khi biến thể có `HAU_KY.ngon_ngu == "hi"`) |
| Danh sách "Me too ❌ / You're welcome ❌ / I'm fine, thanks ❌" hiện dần, gạch ngang đỏ + X đỏ + tiếng "sai" (buzz) | Hậu kỳ `gach_lines()` của `post.py` (đã có, dùng `"gach": true` ở lượt 2 của biến thể); giữ nguyên tiếng Anh (`gach.ngon_ngu: "en"`) vì ba câu này luôn là tiếng Anh dù bản lồng tiếng là Hindi |
| Thẻ từ vựng trắng viền xanh/vàng, nhãn hồng câu Hindi, câu Anh chữ xanh, phiên âm đỏ, từ đang đọc tô vàng | Hậu kỳ `render_card()`/`write_ass()` của `post.py` (đã có), dữ liệu lấy từ `HAU_KY.the[]` của biến thể |
| Robot avatar phát sáng, popup cài app, end card Google Play | **Không gen** → Thương hiệu của dự án |
| Badge "Talka AI" góc trên trái xuyên suốt phần 1 | Bỏ (chữ/logo trong hình: Studio không vẽ chữ trong cảnh gen) |

## Bảng hành động (18 lượt Whisper → 16 lượt kịch bản)
| # Whisper | Giây | Ai nói | Hành động người nói | Vật dụng | Ánh mắt | → Lượt kịch bản |
|---|---|---|---|---|---|---|
| 1–2 | 0.0–4.82 | Diễn giả | Giơ ngón trỏ tay trái, nghiêm nghị, nhìn ống kính | mic cài tai | ống kính | Lượt 1 (HOOK) |
| 3–5 | 5.06–9.14 | Diễn giả | Cầm ly champagne, gật nhẹ từng câu, cười xã giao gượng | ly champagne | người đối diện ngoài khung trái | Lượt 2 (gạch, 3 câu) |
| 6 | 9.96–11.3 | Diễn giả | Về sân khấu, cười tự giễu, gật nhẹ | — | ống kính | Lượt 3 |
| 7 | 13.52–21.78 | Diễn giả | Tay trái đưa ra giới thiệu rồi mở hai tay tự tin | — | ống kính | Lượt 4–5 (câu dài > 20 từ, tách hai lượt cùng người theo mục 2.2 sổ tay) |
| 8–9 | 22.02–25.06 | Diễn giả | Giơ điện thoại lên ngang ngực ở chữ "देखिए" | điện thoại (màn hình chỉ có ảnh robot) | ống kính | Lượt 6 |
| 10–16 | 25.4–44.78 | Robot + diễn giả xen kẽ | Robot: hỏi + đọc mẫu, tay có thể nhấc nhẹ khi mời lặp; Diễn giả: lặp lại 1 lần, gật đầu, cười | — | nhau (qua ống kính, không chung khung thật) | Lượt 7–16 (5 vòng × 2, nội dung lấy từ bản đã nghe kỹ của `BIEN-THE-X0057-X0071-HINDI-20.json`, không chép lại theo Whisper vì Whisper nghe phần này rất lẫn, xem "Còn khác/rủi ro" bên dưới) |
| 17–18 | 55.74–72.38 | (không rõ, Whisper lẫn) | Avatar robot + màn hình cài app | điện thoại/app | — | KHÔNG GEN (Thương hiệu) |

## Bảng "video gốc → kịch bản" (đơn giản hoá / chưa làm được)
| Video gốc | Kịch bản | Loại |
|---|---|---|
| Hai lượt mở đầu (turns 1–2) nói liền mạch | Gộp thành 1 lượt (≤ 20 từ) | Đơn giản hoá cho phép (mục 2.2) |
| 3 câu "Me too / You're welcome / I'm fine, thanks" hiện X đỏ CÙNG một lượt, không có lượt "sửa đúng" đi kèm ngay | Giữ 3 câu trong MỘT lượt `"gach": true`; không ép cặp `fx: wrong → right` (nhịp sửa lỗi thật sự đến ở demo phần 2, không phải ngay sau câu sai) | Giữ đúng video; `kiem-tra` sẽ chỉ CẢNH BÁO (không lỗi) vì không thấy cặp wrong/right — lý do ghi ở README |
| Diễn giả xuất hiện ở HAI vẻ ngoài khác nhau trong phần demo (một đoạn blazer sân khấu, một đoạn kính râm/mũ ngoài trời, xen kẽ) | Giữ MỘT vẻ ngoài xuyên suốt phần 2 (như kịch bản `-6CANH` gốc đã làm) | Đơn giản hoá cho phép (mục 2.2: nhiều cỡ cảnh/outfit trong cùng danh mục → giữ một khung nếu không có lý do bắt buộc) |
| Robot phần 2 đưa tay lên khi nói "Repita comigo" (mẫu tiếng Bồ gốc của khuôn `san-khau-chia-doi-gia-su-ai`) | Đổi thành "khi mời lặp theo" chung chung (không neo từ tiếng Bồ) vì bản Hindi không có cụm đó | Sửa lỗi template (mục 6 sổ tay: mốc "Diễn biến" neo từ ngôn ngữ khác) |
| Robot avatar phát sáng + popup cài app + end card (59,7–75s) | Không gen, dùng Thương hiệu dự án | Theo mục 2 sổ tay (popup/end card → Thương hiệu) |
| Badge "Talka AI" cố định góc trên trái suốt phần 1 | Bỏ (chữ trong hình) | Theo mục 3.1 (không chữ/logo trong cảnh gen) |

## Rủi ro / cần xác nhận khi gen thật
- Whisper nghe tiếng Hindi phần demo (10 lượt 25–45s) rất lẫn (xem `luot_10..16.jpg` → chữ phiên âm sai be bét trong `bao-cao.md`); nội dung 5 câu + thẻ lấy từ bản đã được người review trước đó nghe kỹ và gõ lại trong `BIEN-THE-X0057-X0071-HINDI-20.json`, không gõ lại từ Whisper của lần chạy này. Nên nghe lại một lần khi có thời gian.
- `post.py.highlights()` tìm neo "ingles" trong lời robot để biết đoạn tiếng Anh bắt đầu từ đâu; lời Hindi dùng "इंग्लिश" (Devanagari) nên neo này sẽ KHÔNG khớp và rơi về tìm từ đầu lượt — thẻ vẫn tô được vì câu tiếng Anh xuất hiện đúng 1–2 lần, nhưng cần xem `card*.png`/video gen thật để chắc chắn tô đúng lần "mời lặp" chứ không phải lần robot tự đọc trước đó.
- Ảnh tham chiếu tái dùng từ `SAMPLE/san-khau-chia-doi-gia-su-ai/anh/` (đã có sẵn, không gen mới, không cắt từ video mẫu) — xem README mục quyết định.
- Cặp wrong→right không khớp 1-1 ở lượt gạch: `kiem-tra` sẽ in CẢNH BÁO, ĐÃ CHỦ ĐỘNG GIỮ vì đúng với video gốc (xem bảng trên).

## Insight (người dùng cung cấp, chép nguyên văn)

> Insight 1: Priya - Người phụ nữ công sở Ấn Độ "biết tiếng Anh" nhưng mở miệng là lộ tiếng Anh sách vở
>
> Nhân khẩu học: 28–55 tuổi, chủ yếu là nữ (8/9 video; 1 video là nam khoảng 30 tuổi mặc vest). Người Ấn Độ sống tại Ấn Độ, tiếng mẹ đẻ là Hindi, dùng điện thoại Android. Thuộc tầng lớp trung lưu thành thị đang đi lên, có học, có nghề. Dải tuổi trải từ cô gái trẻ tóc bob đến người phụ nữ tóc bạc đeo kính mặc saree, trọng tâm rơi vào 35–50.
>
> Hình ảnh xuất hiện: "chỉn chu, thành đạt", ngược hẳn với Maria. Trang phục là saree lụa viền vàng, anarkali thêu, blazer với chân váy, suit trắng hoặc đỏ mận, kurta khoác blazer. Tóc gọn, có bindi, trang sức vàng nhỏ, đeo micro cài tai và cầm bút bấm slide. Đây là hình ảnh mà user muốn trở thành: người đứng trên sân khấu, được cả khán phòng lắng nghe. Cảnh nỗi đau vẫn là con người đó, vẫn đẹp và sang, nhưng mặt nhăn lại vì ngượng giữa bữa tiệc.
>
> Công việc chính:
> - Nhân viên hoặc quản lý cấp trung ở công ty có khách hay sếp nước ngoài (IT, dịch vụ, ngân hàng, bảo hiểm)
> - Giáo viên, giảng viên, hiệu phó trường tư
> - Chủ doanh nghiệp nhỏ như boutique, xuất khẩu hàng thủ công, trung tâm đào tạo
> - Nhân sự, hành chính, sales, chăm sóc khách hàng doanh nghiệp
> - Bác sĩ, kế toán, luật sư học bằng tiếng Hindi rồi lên thành phố lớn
> - Người hay đi hội nghị, sự kiện ngành, tiệc công ty, đám cưới thượng lưu
>
> Điểm chung của cụm việc này: làm chuyên môn thì không cần tiếng Anh giỏi, nhưng muốn thăng tiến thì phải qua những khoảnh khắc xã giao bằng tiếng Anh, và đó là lúc nỗi đau nổ ra.
>
> Trình độ: A2–B1. Học tiếng Anh nhiều năm ở trường, đọc hiểu được, viết email được. Khi nói thì chỉ có một kho câu thuộc lòng từ sách giáo khoa và bật ra theo phản xạ: "Nice to meet you" → "Me too", "How are you" → "I'm fine, thanks", cái gì cũng "You're welcome". Câu không sai ngữ pháp nặng nhưng nghe cứng và "rất Ấn Độ học trường làng". Thiếu hẳn lớp tiếng Anh đời thường mà người bản ngữ dùng mỗi ngày, đúng 5 câu video dạy. Vẫn cần nghĩa tiếng Hindi và phiên âm đọc-sao-viết-vậy, tức là chưa đọc được IPA và chưa tự tin phát âm. Đau nhất là cô không biết mình sai: cô tưởng "Me too" là đúng, cho đến khi thấy người đối diện khựng lại.
>
> Nỗi đau cốt lõi:
> - Tiếng Anh sách vở làm cô trông kém hơn năng lực thật, trong khi cô giỏi nghề
> - Sợ mất mặt trước người ngang hàng và cấp trên; ở Ấn Độ tiếng Anh là thước đo đẳng cấp
> - Không biết mình sai ở đâu, vì chưa từng ai sửa, chỉ thấy người ta cười lịch sự rồi quay đi
> - Không có ai để luyện nói mà không bị phán xét; đi học lớp giao tiếp ở tuổi này thì ngại
> - Đã học tiếng Anh cả chục năm mà vẫn không nói được, nên mất niềm tin vào cách học cũ
>
> Động lực thật:
> - Được nhìn nhận đúng tầm: nói tiếng Anh tự nhiên để người ta thấy cô là người có trình độ
> - Thăng tiến: được giao tiếp khách, thuyết trình, đại diện công ty
> - Tự tin ở những nơi sang trọng (tiệc, hội nghị, khách sạn, sân bay) mà không phải đứng nép
> - Hình mẫu mơ ước là đứng trên sân khấu nói trước đám đông
> - Muốn nhanh và không tốn tiền: "ba tuần", "hoàn toàn miễn phí"
>
> 10 tình huống chạm vào nỗi đau của Priya:
> 1. Tiệc networking — đối tác nước ngoài bắt tay nói "Nice to meet you", Priya đáp "Me too", người kia khựng nửa giây rồi quay sang người khác → lộ tiếng Anh sách vở + mất cơ hội kết nối (cảnh gốc của video).
> 2. Hành lang công ty — sếp người nước ngoài hỏi "How's it going?", Priya đáp như trả bài "I'm fine, thank you, and you?", đồng nghiệp trẻ bên cạnh nhịn cười → bị coi là "quê" trước người kém tuổi mình.
> 3. Họp online với khách — khách nói nhanh, Priya không nghe kịp nhưng không biết nói "I didn't catch that", đành gật và "yes, yes", sau đó làm sai yêu cầu → không dám hỏi lại + hậu quả công việc thật.
> 4. Đồng nghiệp gọi lúc cô đang trên đường — cô muốn nói "I'm on my way" mà bật ra "I am coming, I am in the road" → câu đơn giản nhất cũng không tự nhiên.
> 5. Quầy check-in hội nghị — lễ tân nói "Thank you for coming", Priya đáp "You're welcome", người xếp hàng sau liếc nhìn → dùng sai câu thuộc lòng nơi công cộng.
> 6. Thuyết trình nội bộ — slide chuẩn bị kỹ, nhưng đến phần hỏi đáp có người hỏi vặn, cô cần câu giờ mà không biết nói "Give me a second", đứng im trước cả phòng → giỏi chuyên môn nhưng sụp ở phần nói tự do.
> 7. Đưa tài liệu cho khách — cô nói "Please take" thay vì "Here you go", khách vẫn hiểu nhưng cô tự thấy mình nói như người giúp việc chứ không như quản lý → câu nói hạ thấp vị thế.
> 8. Họp phụ huynh ở trường quốc tế của con — các phụ huynh khác nói tiếng Anh trơn tru, Priya chỉ cười và gật, con cô nói nhỏ "Mẹ đừng nói gì nhé" → nỗi đau nhân đôi vì bị chính con mình ngại.
> 9. Phỏng vấn thăng chức — hội đồng chuyển sang tiếng Anh ở phần trao đổi tự do, Priya trả lời bằng những câu ngắn cứng đờ, suất quản lý về tay người kém kinh nghiệm hơn nhưng nói trôi chảy → tiếng Anh chặn trần sự nghiệp.
> 10. Bữa tối với đối tác — ai đó rủ "Let's grab coffee tomorrow?", cô muốn nói "Sounds good" mà chỉ ra được "Yes, okay, I will come", cả bàn nói đùa bằng tiếng Anh còn cô ngồi im cầm ly → ngồi giữa bàn tiệc mà đứng ngoài cuộc trò chuyện.
>
> Lưu ý về dàn nhân vật trong 9 video:
> - Nhóm trẻ 25–32 (video 1, 6, 7): gắn với nỗi lo thăng tiến đầu sự nghiệp.
> - Nhóm trung niên 40–55 (video 2, 4, 8, 9): gắn với giữ thể diện ở vị trí quản lý.
> - Nhóm lớn tuổi 55–65 (video 3, saree, tóc bạc): thông điệp "học lúc nào cũng chưa muộn".
> - Nam giới (video 5): cùng nỗi đau, bối cảnh công sở.

**Đối chiếu insight ↔ video này:** video `X0071` chính là "video 5" (nhân vật nam ~30 tuổi mặc vest) mà insight nhắc tới, và tình huống gốc (tiệc networking, "Nice to meet you" → "Me too") là **tình huống 1** trong danh sách 10 tình huống. 5 câu demo của video (Sounds good / I'm on my way / Give me a second / I didn't catch that / Here you go) khớp đúng 5 câu "giải pháp" mà insight liệt kê rải rác ở các tình huống 10, 4, 6, 3, 7. Hook mới của kịch bản B dùng đúng nỗi đau của **tình huống 3** (không nghe kịp, chỉ biết gật "yes, yes") — vẫn trong insight này, không suy ra insight khác.

## Cấu trúc hook / tình huống (theo chỉ định của người dùng, đối chiếu mốc thời gian thật của video — xem `CAU-TRUC.json`)
- **Hook** (0:00–0:05, lượt 1): nhân vật đứng trên sân khấu kiểu TED nói "Khi ai đó nói Nice to meet you, đừng bao giờ đáp Me too" — khớp hoàn toàn với video, không lệch.
- **Nỗi đau** (0:05–0:11, lượt 2–3): cảnh tiệc sang trọng, tay cầm ly champagne, mặt ngượng, ba câu bị gạch đỏ "Me too", "You're welcome", "I'm fine, thanks", kèm lời thú nhận "Trước đây tôi cũng trả lời y như vậy" — khớp hoàn toàn.
- **Giải pháp** (0:11–0:23,6, lượt 4–6): "Rồi tôi bắt đầu luyện với Talka AI. Chỉ ba tuần tôi đã nói tiếng Anh trôi chảy và tự tin. Và nó hoàn toàn miễn phí." — khớp hoàn toàn (câu dài 20+ từ tách thành 2 lượt theo mục 2.2 sổ tay, không đổi nội dung).
- **Demo** (0:23,6–0:59,7, lượt 7–16): màn hình chia đôi, robot đọc mẫu và nhân vật nhắc lại đúng 5 câu Sounds good / I'm on my way / Give me a second / I didn't catch that / Here you go, mỗi câu có nghĩa Hindi + phiên âm — khớp hoàn toàn (xác nhận qua `tong-quan_2.jpg`/`tong-quan_3.jpg`).
- **CTA** (0:59,7–1:15, không gen): cài app trên Google Play — khớp hoàn toàn.
- Không có điểm lệch đáng kể giữa cấu trúc người dùng chỉ định và video thật; các khác biệt nhỏ (vẻ ngoài đổi giữa phần demo, mốc neo từ của khuôn gốc) đã ghi ở bảng "video gốc → kịch bản" phía trên.
