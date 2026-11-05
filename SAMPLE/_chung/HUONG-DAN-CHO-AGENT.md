# Hướng dẫn cho agent: viết kịch bản và biến thể cho LUO Studio (mọi thể loại video)

Bạn tạo ra 2 file mà Studio nhập được và Muse gen đúng ý, cho **bất kỳ thể loại nào** (hội thoại, tư vấn, review, kể chuyện, tình huống đời thường, quảng cáo nhiều cảnh...):
1. **Kịch bản** (`.txt`): khung prompt có token `{{...}}` → tab "Loại dự án" → "Loại mới".
2. **Biến thể** (`.json`): mảng các video, mỗi phần tử điền token + lời thoại.

File mẫu: `1-KICH-BAN-MAU.txt`, `2-BIEN-THE-MAU.json`; ví dụ bố cục khác: thư mục `SAMPLE/xe-tai/`. Hai file mẫu chỉ là **một thể loại** (người học + gia sư AI), không phải khuôn bắt buộc.

## Đọc trước: sổ tay kỹ thuật và công cụ một lệnh

- **`SO-TAY-KY-THUAT.md`** (cùng thư mục): tổng hợp mọi kỹ thuật đã kiểm chứng (bảng chọn khuôn theo đặc điểm video, kỹ thuật viết kịch bản, ghép 2 lớp, camera, lỗi đã gặp và cách sửa). Tài liệu này là chi tiết cơ chế Studio; sổ tay là cách dùng chúng cho video mới.
- **`video-moi.py`**: `danh-gia <video>` (phân tích + đo mặt/máy quay/giọng + gợi ý khuôn), `kiem-tra <kịch bản> <biến thể>` (kiểm bằng code Studio), `nhap ... --chay-thu` (tạo loại dự án + dự án trong Studio và chạy thử).
- Skill `luo-video-moi` (`.claude/skills/luo-video-moi/SKILL.md`): quy trình từng bước cho agent khi người dùng đưa video mới.

## Prompt riêng cho từng thể loại

Mỗi thư mục thể loại trong `SAMPLE/` có file `PROMPT-CHO-AGENT.txt`: quy tắc riêng của thể loại đó, lỗi thường gặp và danh sách tự kiểm tra. **Nếu video thuộc một thể loại đã có, đọc file đó trước** rồi mới đọc phần chung bên dưới. Hiện có: `ghep-hai-lop/`, `canh-sat-nu/`, `xe-tai/`, `lam-vuon/`, `san-bay-gia-su-ai/`, `canh-sat-gia-su-ai/`, `soi-hanh-ly-gia-su-ai/`, `chia-doi-gia-su-ai/`. Thể loại mới: tạo thư mục mới với đủ kịch bản mẫu, biến thể mẫu và `PROMPT-CHO-AGENT.txt` cùng cấu trúc.

## 0. Phân tích video tham chiếu (BẮT BUỘC, làm trước khi viết bất cứ thứ gì)

Không phân tích video bằng vài ảnh chụp thưa hay chỉ lời thoại: hành động nhỏ (đưa giấy tờ, lấy điện thoại), tốc độ nói và tư thế khung cuối sẽ bị bỏ sót hoặc hiểu sai. (Đã từng xảy ra: nhìn thưa nên mô tả sai cảnh "tài xế cầm điện thoại".) Luôn chạy công cụ:

```
runtime\python.exe SAMPLE\_chung\phan-tich-video.py "C:\duong-dan\video.mp4" [thu-muc-ra]
```

Công cụ sinh `bao-cao.md` và các ảnh ghép: `tong-quan_N.jpg` (1 khung/giây cả video), **`luot_NN.jpg` (4 khung/giây cho từng câu nói, có số giây)**, **`chuyen-dong_NN.jpg` (các khoảnh khắc chuyển động mạnh)**. Báo cáo có: thời điểm và lời từng câu, **tốc độ nói từng câu (từ/giây)** và trung vị, khoảng lặng giữa các câu, danh sách cảnh cắt cứng.

Quy trình:
1. Đọc `bao-cao.md`. Điền cột "Ai nói" (công cụ không biết); ghép các câu liền nhau của cùng một người thành một lượt.
2. **Xem TỪNG ảnh `luot_NN.jpg` và `chuyen-dong_NN.jpg`** (đọc ảnh, không đoán từ lời thoại). Điền **bảng hành động**, mỗi lượt một dòng:

| Lượt | Ai nói | Từ/giây | Hành động người nói | Người nghe làm gì | Vật dụng (xuất hiện / đổi tay / biến mất) | Ánh mắt | Camera | Trạng thái KHUNG CUỐI (tay, vật, tư thế) |
|---|---|---|---|---|---|---|---|---|

3. **Đối chiếu trước khi viết kịch bản:**
   - Mỗi dòng của bảng phải có chỗ trong kịch bản: `Diễn biến` (việc gì, trong lúc nào), `Khung cuối` (ai cầm gì, ở đâu), và token đạo cụ nếu là vật dụng mới (ví dụ `DAO_GIAY_TO`, `DAO_DIEN_THOAI`).
   - Mỗi khoảnh khắc chuyển động mạnh trong báo cáo phải được giải thích: hành động nào, hay chỉ là cảnh cắt/chuyển cảnh.
   - **Hành động phải xảy ra TRONG lúc nói** (Studio cắt clip ngay sau từ cuối) và xong trước từ cuối; khung cuối là trạng thái sau hành động, vì cảnh sau nối từ khung đó.
   - **Tốc độ nói:** lấy trung vị từ/giây của báo cáo (ví dụ ~4,5 từ/giây, câu ngắn tới 6) và ghi số đó vào `[VIDEO SUFFIX]` và phần đuôi `Prompt video` của từng cảnh. Muse hay nói chậm hơn video gốc; nếu chạy thử vẫn chậm thì nâng "Tốc độ tăng tối đa" trong Cài đặt (tối đa 1,35).
   - Chỗ nào Muse khó làm (nhiều vật dụng, đổi địa điểm, camera chuyển động, nhiều người) thì đơn giản hoá và ghi rõ vào bảng "video gốc → kịch bản".
4. **Giao cho người dùng kèm theo kịch bản:** bảng hành động và bảng "video gốc → kịch bản" (mỗi hành động của video gốc đi vào cảnh nào, chỗ nào đã đơn giản hoá). Người dùng duyệt bảng trước khi chạy gen.

Giới hạn của công cụ: không biết ai đang nói (agent điền); chuyển động mạnh chỉ là gợi ý (vật nhỏ trong cảnh rộng có thể không tạo đỉnh, nên vẫn phải xem ảnh từng lượt); nhạc nền hoặc tiếng ồn lớn làm nhận dạng lời sai; video dài vài phút chạy khá lâu.

## 1. Quy tắc nền (đúng với mọi thể loại)

1. **Mỗi cảnh = một clip Muse 5–10 giây = một lượt thoại.** Mỗi clip chỉ MỘT người nói; người còn lại im, miệng khép.
2. **Liên tục khung hình:** cảnh sau bắt đầu từ *khung cuối* cảnh trước. Mọi tư thế, nét mặt, cử chỉ lệch ở một cảnh **truyền sang tất cả cảnh sau**. Vì vậy: cuối mỗi cảnh về tư thế nghỉ trung tính và đứng im; không cho cảm xúc dùng cử chỉ tay/thân lớn (gãi đầu, nhún vai, che mặt).
3. **Prompt ngắn, đơn giản, câu khẳng định.** Khối khoá ~300 từ là đủ; 1.000+ từ làm Muse quên ngữ cảnh và nói chồng. Điều cấm để trong `[NEGATIVE]` ngắn; đừng liệt kê hàng loạt "no smile, no nod..." vì nó gợi đúng hành vi đó.
4. **Mô tả nhìn thấy được, không trừu tượng** ("đẹp", "dễ thương" → vô nghĩa với Muse). Không dùng thương hiệu thật của người khác, không mô tả người thật.
5. **Không để chữ lọt vào hình:** không chữ/logo/phụ đề/giao diện app trong khung. Từ vị trí viết hoa (TOP, LEFT...) từng bị Muse vẽ thành chữ: thêm vào `[NEGATIVE]` khi dùng.
6. Camera đứng yên, bối cảnh phía sau đứng yên (không xe chạy, mây trôi), ánh sáng cố định.
7. Hai giọng phải **khác hẳn nhau** (cao/sáng/nhanh vs trầm/khàn/chậm), nhất là cùng giới.

## 2. Studio xử lý gì (đã đọc code, để biết chỗ nào linh hoạt)

**Tổng quát, dùng cho mọi thể loại:**
- Bố cục, nhân vật, bối cảnh, đạo cụ, tông màu: toàn bộ nằm trong **kịch bản + giá trị token**. Studio không ép bố cục.
- Token mới thành trường mới ở tab "Loại dự án"; luôn kiểm tra danh sách trường sau khi nhập.
- **Cảnh có ảnh riêng:** cảnh nào có trường `Prompt ảnh` sẽ sinh khung đầu mới (không nối từ cảnh trước). Dùng để **đổi bối cảnh/địa điểm/trang phục** giữa chừng. Cảnh không có `Prompt ảnh` luôn nối từ khung cuối cảnh trước.
- **Cảnh không có lời thoại** (cảnh hành động, cảnh chuyển, b-roll ngắn): không dùng `{{LUOT_n}}` ở cảnh đó; trường Voice để trống thì Studio ghi "No speech". (Đường code này có, nhưng chưa chạy thử: chạy thử một biến thể trước.)
- **Lồng tiếng ngoài khung** (giọng đọc không phải người trong hình, kiểu quảng cáo có người dẫn): không dùng `{{LUOT_n}}`; viết lời bằng token thường (ví dụ `{{LOI_MO}}`) trong ngoặc kép ở trường `Voice`, và ghi rõ trong `Prompt video` "the off-screen narrator says ... The man never speaks". Studio chỉ bắt buộc clip có tiếng, không tự ép nhép miệng; ai nói và có nhép miệng hay không là do kịch bản (thể loại có người nói trong hình phải tự ghi "clear lip-sync" như các mẫu). Biến thể để `"LUOT": []`; phụ đề Hậu kỳ khi đó lấy từ lời trong ngoặc kép ở `Voice` của từng cảnh. Tránh token đánh số liên tiếp (`LOI_1`, `LOI_2`): Studio coi là chuỗi và không hiện thành trường ở tab biến thể. Mẫu: `SAMPLE/Doi toc/`.
- **Trường `Chuyển cảnh`** (tuỳ chọn, mỗi cảnh): hiệu ứng khi VÀO cảnh này lúc ghép: `chớp trắng`, `chớp vàng`, `chớp đen` hoặc `chớp #RRGGBB`, có thể kèm số giây tổng (mặc định 0,4; ví dụ `chớp trắng 0.3`). Cuối cảnh trước mờ sang màu đó rồi cảnh này hiện ra; không làm đổi độ dài video. Để trống hoặc `cắt thẳng` = cắt thẳng.
- **Kiểm tra lời nói** (mọi chế độ, từ 03/11/2026; chặt từng chữ từ 04/11/2026): gen xong mỗi clip có lời, Studio nghe lại bằng Whisper; nói lặp từ/cụm, **thừa dù 1 từ hoặc thiếu dù 1 từ** (mọi câu, kể cả câu 1–2 chữ) thì gen lại kèm yêu cầu "nói đúng một lần, từng chữ" (opts `speech_retries`, mặc định 2) và giữ lần ít lỗi nhất. Viết tắt ("I'm" = "I am"), số ("sixty-eight" = "68"), tiếng ừm/à được chuẩn hoá; chữ Whisper bịa ở đoạn im cách xa câu (> 1,2 giây) không tính. Sau khi cắt sát lời, Studio kiểm lại bản cắt: mất chữ thì cắt lại rộng hơn. Tắt bằng `check_speech: false`.
- **Dòng dịch** (`"dich"`, hậu kỳ `types/_chung/phu_de.py`): chia theo câu, mỗi câu dịch hiện cùng câu tiếng Anh tương ứng (khớp theo vị trí ký tự khi số câu hai bên khác nhau).
- **Trường `Giữ sau lời`** (tuỳ chọn, mỗi cảnh, số giây, ví dụ `Giữ sau lời: 1.3`): Studio vẫn cắt clip sau lời nói nhưng giữ thêm khoảng đó sau từ cuối (rồi chọn khung yên nhất ngay sau). Dùng khi có việc xảy ra SAU câu nói mà cảnh sau cần, ví dụ camera lia sang người kia (mẫu: cảnh 1 của `SAMPLE/soi-hanh-ly-gia-su-ai/`). Không có trường này thì mọi chuyển động sau từ cuối đều bị cắt.
- **Trường `Ảnh tổng quan` + `Khung đầu cắt`** (tuỳ chọn, cảnh có camera lia trong clip): `Ảnh tổng quan:` là prompt (tiếng Anh) của một ảnh NGANG 16:9 chứa cả bố cục (ai đứng đâu, đồ vật ở đâu, từ trái sang phải); `Khung đầu cắt: trái | giữa | phải | 0..1` là vị trí khung dọc cắt ra làm khung đầu. Studio gen ảnh ngang trước (`scene<n>_wide.png`), cắt khung đầu từ đó (ảnh ngang nhỏ thì cho Muse vẽ lại khung cắt cho nét, cần thêm `Prompt ảnh`), gửi kèm ảnh ngang làm ảnh tham chiếu #2 khi gen video để Muse lia đúng tới người/vật đã thấy trong ảnh, và gửi kèm nó cho các khung đầu gen mới sau đó (giữ cùng bối cảnh, đạo cụ). Prompt video của cảnh tả cú lia bằng khối `CAMERA MOVE` (bắt đầu từ đâu, theo cái gì, nhanh/chậm ở chữ nào, dừng ở ai), khoá chung phải cho phép ("camera still unless the clip describes a CAMERA MOVE"), thêm `Giữ sau lời` nếu cú lia kéo qua cuối câu. Cảnh này không đo miệng người nghe. Mẫu: cảnh 1 của `SAMPLE/soi-hanh-ly-gia-su-ai/`.
- **Trường `Lia nhanh`** (tuỳ chọn, số lần, ví dụ `Lia nhanh: 3`): Muse thường lia máy chậm và đều (~2 giây), không có lực như cú vụt máy thật. Sau khi cắt clip, Studio dò đoạn camera lia mạnh nhất NẰM SAU từ cuối (mốc từ cuối lấy bằng Whisper, nên không làm mất lời), tua nhanh đoạn đó N lần kèm nhoè ngang và bỏ bớt đoạn im lặng tương ứng; khung cuối không đổi nên cảnh sau vẫn nối đúng. Vì chỉ tua sau lời, kịch bản phải cho cú lia xảy ra SAU câu nói (kèm `Giữ sau lời` đủ dài để giữ trọn cú lia). Không để nhân vật "keeps pointing" trong lúc máy lia: Muse cho cánh tay đi theo camera và chỉ nhầm vào người khác.
- **Trường `Lia theo tay`** (tuỳ chọn, số giây, đi kèm `Lia nhanh`, ví dụ `Lia theo tay: 1`): Muse thường để máy đứng yên khi nhân vật giơ tay chỉ. Studio thêm N giây máy đẩy vào (tới 1,35 lần) và trôi về phía phải-dưới theo cánh tay ngay trước cú vụt (bắt đầu không sớm hơn đầu câu nói), rồi trả dần về khung gốc trong lúc vụt. Vì vậy kịch bản nên đặt vật được chỉ ở phía phải-dưới của khung đầu.
- **Trường `Mở đầu ảnh` + `Mở đầu video` + `Mở đầu dài`** (tuỳ chọn): đoạn KHÔNG LỜI ghép (cắt cứng) trước clip của cảnh, không cần thêm lượt thoại, ví dụ hành lý trôi ra khỏi máy soi rồi mới tới câu hỏi. Studio gen ảnh khung đầu riêng từ `Mở đầu ảnh` (kèm ảnh tổng quan nếu cảnh có), gen clip 5 giây từ `Mở đầu video`, tua cho vừa `Mở đầu dài` giây (mặc định 1,5; nhanh tối đa 3 lần), lấy tiếng nền của chính clip đó. Khoá chung của kịch bản vẫn áp dụng, nên nếu cần chuyển động khác khoá (băng chuyền chạy, máy di chuyển) thì ghi rõ "In this clip only ...".
- **Trường `Lớp phủ: camera`** (tuỳ chọn, mỗi cảnh): khi ghép, Studio đè giao diện camera điện thoại (lưới, 1x, hàng chế độ, nút chụp) và một viền trắng hình trứng bám theo khuôn mặt từng khung hình (mediapipe). Muse không vẽ gì: trong prompt cảnh đó cấm giao diện/khung/vòng tròn, cho nhân vật nhìn thẳng, xoay đầu chậm, đầu ở khoảng 1/3 trên khung. Muốn giao diện riêng: `Lớp phủ: camera D:\duong-dan\giao-dien.png` (PNG trong suốt 9:16). Chỉ hợp cảnh có MỘT khuôn mặt rõ.
- Có thể đính kèm ảnh tham chiếu (mặt, trang phục) hoặc mp3 mẫu giọng cho từng ô ở giao diện. Trong file biến thể: `"refs": {"NGUOI_HOC": ["<link>"]}`. Link nhận được: ảnh trực tiếp, prnt.sc, Google Drive dạng chia sẻ (`.../file/d/<id>/view`, file để "bất kỳ ai có liên kết"; Studio tự đổi sang link tải), hoặc đường dẫn tệp trên máy (tuyệt đối, hoặc tính từ thư mục gốc, vd. `SAMPLE/chia-doi-gia-su-ai/anh/robot-ai.webp`).
- Số lượt thoại nhiều hơn số cảnh trong kịch bản: Studio tự nhân bản cảnh cuối.

**Mô hình nhân vật tổng quát (số nhân vật bất kỳ, khoá bất kỳ):**
- Mỗi nhân vật có một **khoá** chữ HOA không dấu, ví dụ `MC`, `KHACH`, `THO`, hoặc `DAY`/`HOC` (hai khoá cũ). Lượt thoại ghi `"who": "<khoá viết thường>"` (ví dụ `"who": "mc"`); `day`/`hoc` chỉ là hai khoá đặc biệt, không còn bắt buộc.
- Các token của nhân vật đặt theo quy ước `<LOẠI>_<KHOÁ>`:
  - `TEN_<K>` (bắt buộc; tên gọi ngắn dùng trong prompt), `NGUOI_<K>` (ngoại hình), `GIONG_<K>` (giọng, nên khác hẳn giọng người khác);
  - `POS_<K>` (nhãn vị trí viết vào prompt, chữ bất kỳ, ví dụ `LEFT`, `TOP`, `center-right`);
  - `BOX_<K>` (tuỳ chọn): hộp khuôn mặt `"x0,y0,x1,y1"` theo tỉ lệ khung hình 0..1, **dùng cho bộ đo miệng ở bố cục bất kỳ**. Nếu không có `BOX_<K>`, `POS_<K>` phải là `LEFT`/`RIGHT`/`TOP`/`BOTTOM`; nhãn lạ mà không có `BOX_` thì Studio bỏ qua đo miệng cho nhân vật đó (không đo nhầm mặt);
  - `VAI_<K>` (tuỳ chọn; tên vai trong prompt, ví dụ `host`; mặc định `tutor`/`learner` cho `DAY`/`HOC`, `character` cho khoá khác), `NGHE_<K>` (tuỳ chọn; tư thế khi im lặng, ví dụ "nhìn người nói, miệng khép"; mặc định "eyes on the camera" chỉ hợp khi nhân vật nhìn vào ống kính), `NHIN_<K>` (tuỳ chọn; hướng nhìn KHI NÓI, câu tiếng Anh dạng động từ, ví dụ "keeps looking at the traveller, face turned away from the camera"; Studio chèn vào câu lệnh của người nói ở mọi chế độ. Nên khai khi nhân vật nói chuyện với người khác trong khung: không khai thì Muse hay xoay mặt người nói ra camera để khoe khẩu hình. Ở dự án nhiều phần, khoá `NHIN_HOC@2` ghi đè riêng cho phần 2), `QUAY_LUNG_<K>` (tuỳ chọn; ghi bất kỳ chữ nào cho nhân vật quay lưng về camera, vd. góc qua vai: khi người này nói, Studio bỏ mọi câu đòi lộ miệng / nét mặt ("coming from the mouth", gợi ý nhướng mày, mím môi...) và chỉ tả giọng + cử động nhẹ của đầu, vai; khi họ nghe cũng không tả mặt. Không khai thì Muse hay xoay mặt người quay lưng ra để khoe khẩu hình), `EMO_<K>` (cảm xúc mặc định khi lượt không ghi `emo`).
- Mỗi clip chỉ MỘT nhân vật nói, **tất cả nhân vật còn lại im lặng**. Studio tự lập "SPEAKER MAP" (VOICE A, B, C... theo thứ tự `DAY`, `HOC`, rồi các khoá còn lại), bỏ khoá giọng của người im lặng, và đo miệng **từng người nghe** (có lỗi thì gen lại kèm yêu cầu sửa).
- Cảnh không có lời thoại (không dùng `{{LUOT_n}}`, trường Voice trống): Studio không đòi tiếng, không cắt theo lời, không đo miệng. Nếu clip câm, khi ghép sẽ chèn im lặng.
- Chỉ dùng `VIEC` (việc người học đang làm) cho loại "người học + gia sư AI": nó khiến người học nghe "cúi xuống làm việc, quay mặt đi", không hợp thể loại khác. Thể loại khác **bỏ `VIEC`** và dùng `NGHE_<K>`.
- Nếu hai vai `DAY`/`HOC` **cùng giới** và biến thể không khai `VAI_DAY`/`VAI_HOC`, Studio (bật "Tách giọng") ghi đè giọng `DAY` bằng giọng "trợ lý gọi video tươi sáng". Chỉ hợp gia sư AI; thể loại khác hãy khai `VAI_*` (khi đó Studio không ghi đè) hoặc chọn các nhân vật có giọng khác hẳn nhau.
- **Hai nhân vật cùng giới, khoá tự đặt** (vd. khách + nhân viên hộ chiếu, đều là nam): Studio (bật "Tách giọng") tự gắn một giọng THẤP (bên có mô tả trầm / khô / cứng hơn) và một giọng CAO vào `GIONG_<K>` và nhắc lại trong khối SPEAKER MAP của mỗi cảnh (`pair_voice_split` trong `engine.py`). Không gen thêm. Khi cả hai mặt đều hiện thì đủ để Muse ghép đúng giọng với khuôn mặt; nên vẫn mô tả giọng thật khác nhau (tuổi, âm sắc, giọng vùng miền) trong `GIONG_<K>`.
- **Người nói quay lưng** (`QUAY_LUNG_<K>`, góc qua vai): không có miệng nào hiện ra để nói, Muse gán lời và cả động tác của người này cho khuôn mặt duy nhất nhìn thấy (người kia nhép miệng, làm động tác của nhân viên; hộ chiếu 04/11/2026, khách nam). Tính năng gen 2 clip cho cảnh loại này hiện **TẮT mặc định** (bật bằng `voice_swap: true`; chưa có nút trong giao diện); mặc định chỉ tách giọng cùng giới. Khi bật, Studio gen 2 clip: clip có giọng chỉ lấy TIẾNG, clip câm (prompt bỏ mọi câu về nói / giọng, giữ động tác của người quay lưng) lấy HÌNH, rồi ghép (`silent_prompt` + khối `voice_swap` trong `engine.py`; `voice_swap` mặc định tắt). Tốn thêm 1 lượt gen cho mỗi cảnh người quay lưng nói; không đo miệng clip giọng vì hình không lấy từ đó. Gen dở (huỷ giữa chừng) làm tiếp được: file `scene<N>_swap.todo` đánh dấu clip giọng đã xong, `scene<N>_voice.mp4` là bản giọng gốc.
- Video không có nhịp "sửa lỗi": đặt `"fx": "none"` ở **mọi** lượt thoại để tắt viền đỏ/xanh tự động (chỉ áp cho khoá `hoc`/`day`).

**Giới hạn hiện còn:**
- Giao diện Studio (tab biến thể): loại chỉ có `day`/`hoc` giữ hai nút "Dạy"/"Học"; loại có nhân vật khác (vd. `canbo`) thì người nói của từng lượt là ô chọn trong danh sách nhân vật (lấy từ trường `TEN_/NGUOI_<KHOÁ>` của kịch bản, `TEN_<KHOÁ>` của biến thể và `who` đã có), hiện theo `VAI_<KHOÁ>` nếu có. Trường `TEN_/NGUOI_/GIONG_/POS_/VAI_/NGHE_<KHOÁ>` của mỗi nhân vật gom vào thẻ riêng "Nhân vật …"; mỗi thẻ có thêm ô tuỳ chọn "Hướng nhìn khi nói" (`NHIN_<KHOÁ>`, và `NHIN_<KHOÁ>@n` nếu biến thể đã có). "Thêm lượt" chọn nhân vật kế tiếp trong danh sách.
- Chưa chạy thử trên Muse với thể loại nhiều hơn hai nhân vật; mô hình prompt và đo miệng đã kiểm tra bằng mô phỏng và trên clip hai nhân vật.
- Nhiều nhân vật trong một khung làm Muse dễ lẫn giọng/mấp máy hơn: giữ mô tả giọng khác hẳn nhau và ưu tiên bố cục chỉ có hai khuôn mặt rõ nét.

## 3. Thiết kế một thể loại mới (làm theo thứ tự)

1. **Phân tích video tham chiếu:** số nhân vật, bố cục khung, góc máy, bối cảnh, nhịp kể (hook → diễn biến → cao trào → kêu gọi), chỗ Muse khó làm (chữ, nhiều người nói, camera chuyển động, đám đông).
2. **Đơn giản hoá cho Muse:** một khung, camera cố định, tối đa hai người trong khung, cảnh ngoài cửa sổ đứng yên. Chỗ nào video gốc phức tạp (camera đi, nhiều người, chữ) thì thay bằng tương đương đơn giản và ghi rõ trong phân tích.
3. **Gán nhân vật:** mỗi người một khoá (ví dụ `MC`, `KHACH`), đặt `TEN_/NGUOI_/GIONG_/POS_<khoá>` và `BOX_<khoá>` nếu bố cục không phải LEFT/RIGHT/TOP/BOTTOM.
4. **Chia cảnh:** mỗi lượt thoại một cảnh. Nếu cần đổi địa điểm → cảnh đó có `Prompt ảnh` riêng. Cảnh phụ không thoại → không có `{{LUOT_n}}`.
5. **Chọn token:** dùng lại tên token của file mẫu khi nghĩa khớp (`NGUOI_HOC, TEN_HOC, GIONG_HOC, NGUOI_DAY, TEN_DAY, GIONG_DAY, POS_DAY, POS_HOC, VIEC, DAO_CU, DAO_GIU, DAO_NGHI, NEN_TRAI, NEN_PHAI`). Chỉ thêm token mới khi video thật sự cần (CHỮ HOA, không dấu, nối `_`). Mọi thứ thay đổi theo từng video (nhân vật, bối cảnh, đạo cụ, tông màu) là token; mọi thứ cố định (bố cục, quy tắc) viết thẳng.
6. **Viết kịch bản:** `[STYLE LOCK]`, `[CHAR LOCK]`, `[SET LOCK]`, `[VIDEO SUFFIX]`, `[NEGATIVE]`, rồi các cảnh `CẢNH n (m:ss–m:ss): Lượt n` với: Bối cảnh, Voice, Khung đầu, Khung cuối, Diễn biến, Prompt ảnh (cảnh đầu và cảnh đổi bối cảnh), Prompt video, Audio, Negative prompt. Prompt gửi Muse viết **tiếng Anh**; tiêu đề trường và các trường mô tả viết tiếng Việt.
7. **Viết biến thể (.json)** theo mục 4, rồi kiểm tra (mục 5).

## 3b. Thể loại "ghép 2 lớp" (nhân vật ở hai vùng tách biệt của khung)

Dùng khi các nhân vật KHÔNG cần đứng chung một khung thật: ví dụ gia sư AI trong khung gọi video bo góc phía trên + người học quay selfie phía dưới,
hoặc hai người chia đôi màn hình. Studio gen RIÊNG từng nhân vật (mỗi clip chỉ có một người, nên không bao giờ có chuyện hai người cùng nói),
rồi ghép bằng ffmpeg. Mỗi lượt thoại là một cảnh, số lượt tuỳ ý, KHÔNG viết khối CẢNH. Mẫu: `SAMPLE/ghep-hai-lop/`.

Kịch bản gồm các khối:
- `[GHEP HAI LOP]:` bố cục, mỗi dòng một khoá (có dấu hay không đều được):
  - `nen: HOC` nhân vật làm nền toàn khung 9:16;
  - `khung DAY: 0.02, 0.015, 0.96, 0.32` khung của nhân vật khác: x, y, rộng, cao theo tỉ lệ khung hình (0..1). Có thể nhiều dòng `khung <KHOÁ>`.
    Nhân vật NỀN cũng có thể có `khung` riêng (vd. màn hình chia đôi: `khung HOC: 0.5, 0, 0.5, 1` + `khung DAY: 0, 0, 0.5, 1`): khi đó nền chỉ chiếm ô của nó (mẫu: `SAMPLE/chia-doi-gia-su-ai/`). Ô hẹp hơn 9:16 thì Studio gen 9:16 rồi cắt DẢI GIỮA: kịch bản phải dặn nhân vật đứng giữa, mọi thứ quan trọng nằm trong phần giữa.
    Studio gen nhân vật trong khung ở tỉ lệ Muse hỗ trợ gần nhất (16:9, 1:1 hoặc 9:16) rồi cắt vừa khung;
  - `bo goc: 0.05` bán kính bo góc (theo bề rộng khung hình); `vien: #FFFFFF, 3` màu và độ dày viền (`vien: khong` = không viền);
  - `noi: lien` (mặc định từ 03/11/2026): **nối khung**: clip sau của mỗi nhân vật bắt đầu từ khung cuối clip trước của chính nhân vật đó (cả người nói lẫn người nghe),
    không cắt đầu clip. Khi nối khung, clip nghe không dùng thư viện dùng lại (`nghe: dung lai` bị bỏ qua; dùng `nghe: tinh` hoặc `nghe: moi canh`).
    Mỗi clip mới được CĂN KHỚP về đúng khung cuối người xem vừa thấy: bù phóng/dời nếu Muse tự thu khung, chỉnh màu Lab (khung đầu đúng màu khung nối,
    cuối clip kéo ~35% về ảnh gốc để màu không trôi qua nhiều cảnh), hoà 0,2s đầu. Đo 03/11/2026 trên clip thật: lệch ở chỗ nối 6,7 -> 2,1 (mức nén video).
    Chống mặt SẦN dần (Muse vẽ vệt nén thành tàn nhang/vân da): gửi kèm ảnh gốc làm tham chiếu nhận dạng/da, khử nhiễu + kéo màu ảnh gửi Muse về ảnh gốc.
    `lam moi: N` ĐÃ BỎ (Studio bỏ qua, báo trong nhật ký): ảnh vẽ lại làm đổi tư thế + màu, gây khựng mạnh (lệch 37/255 ở cảnh 12->13 video hộ chiếu).
    `noi: morph 0.24` = cách cũ (mọi clip bắt đầu từ ảnh gốc) + hình chuyển mượt ngắn ở chỗ nối; `noi: cat` = cách cũ, cắt thẳng (tư thế nhảy ở mỗi chỗ nối).
  - Vị trí ô: đo bằng `runtime\python.exe SAMPLE\_chung\do-vi-tri-dau.py <thư mục phan2 của lần chạy | video>`: công cụ dò khuôn mặt nhân vật nền trên mọi khung,
    nới ra thành vùng đầu (kèm tóc) và in dòng `khung DAY: ...` lớn nhất đặt sát góc mà không chạm vùng đầu. Ô che mặt là lỗi người dùng phản ánh (03/11/2026).
  - `nghe: moi canh` (khuyên dùng cho ghép 2 lớp, từ 03/11/2026): mỗi cảnh gen 2 video, một cho người nói và một cho người nghe; với `noi: lien`, cả hai đều bắt đầu từ khung cuối video trước của chính nhân vật đó. **Nguyên nhân người nghe nhép miệng (đã sửa):** prompt NGHE chèn nguyên khối [NHAN VAT], mà khối này viết cho lúc NÓI ("while speaking…", "moves its lips in clear sync with the words", "VOICE: …"), phần Avoid cũng tả chất giọng, nên Muse làm theo. Giờ Studio tự lọc mọi câu về nói/giọng/khẩu hình khỏi prompt NGHE (`_no_speech`). Vẫn nên viết khối [NHAN VAT] tách bạch: câu "while speaking"/VOICE đứng riêng thành câu. Khối `[NGHE <KHOÁ>]` tả phản ứng rõ (gật đầu, nhướn mày, cười, nghiêng đầu) bằng câu khẳng định, không nhắc tới việc nói. Đo miệng + gen lại (tối đa 2 lần) vẫn là lưới an toàn. **Nguyên nhân chính còn lại (04/11/2026): khối `[NGHE <KHOÁ>]` nhắc tới việc nói, dù để CẤM** ("no talking-like head bobbing, never mirrors the speaker"): Muse đọc chữ "talking"/"speaker" là lồng tiếng lẩm bẩm vào clip nghe rồi cho mặt nhép, gật gù đúng nhịp tiếng đó (môi hé ít nên bộ đo miệng không bắt được). Đo trên 246 clip nghe: có câu đó 40% clip có tiếng, không có 3%. **Khối NGHE chỉ tả điều NÊN làm** (miệng khép mỉm cười, gật nhẹ, chớp mắt), không viết talk/speak/speaker/mirror/voice/word; Studio cũng tự bỏ các mệnh đề như vậy (`split._calm_listen`). Lưới an toàn: Studio LUÔN đo tiếng clip nghe (kể cả khi tắt kiểm tra miệng), to hơn −45 dB thì gen lại (tối đa 2 lần, 4 lần nếu chưa có clip câm nào của nhân vật đó), vẫn có tiếng thì dùng lại clip nghe câm gần nhất của chính nhân vật đó, chưa có thì dựng từ ảnh khung đầu (`split._talky`, `_gen_listen`). `khoa mieng: co` (mặc định TẮT) dán vùng môi khép lên từng khung, nên chỉ dùng khi bí vì môi trông cứng. `nghe: tinh` = người nghe là ảnh tĩnh: không nhép miệng nhưng đứng hình. **Giữ đúng nhân vật qua các cảnh (05/11/2026):** mỗi clip gửi khung nối (#1), ảnh gốc (#2) và ảnh tham chiếu gốc của chính nhân vật trong biến thể (#3, tối đa 2 ảnh), nên luôn gắn ảnh tham chiếu `..._<KHOÁ>` cho từng nhân vật. Clip nói được cắt muộn tới lúc người nói khép miệng (tối đa 0,7 giây) để clip nghe cảnh sau bắt đầu từ khung khép miệng.
  - `khoa mieng: co` (mọi nhân vật) hoặc `khoa mieng: HOC` (chỉ các KHOÁ được kể): dán vùng môi khép lên từng khung clip nghe. Mặc định để TẮT: chia-doi bật thử 05/11/2026 thì trông như dán miệng giả; từ khi Muse nhận lệnh nguyên văn, người nghe đã tự khép miệng. Câu tả khung hình (cỡ đầu, tới đâu) trong [NHAN VAT] PHẢI khớp ảnh gốc: Muse làm theo chữ hơn khung đầu, lệch là nhân vật to/nhỏ giữa các cảnh. Khi nối khung, camera luôn được khoá về khung đầu mỗi clip, clip Muse tự phóng quá x1,15 được gen lại.
  - `nghe: dung lai 3` mỗi nhân vật có 3 clip "đang nghe" ~10 giây dùng lại cho mọi cảnh (tiết kiệm lượt), hoặc `nghe: moi canh` gen clip nghe riêng từng cảnh (tự nhiên hơn, tốn gấp đôi lượt).
- `[STYLE LOCK]:` phong cách chung.
- `[NHAN VAT <KHOÁ>]:` mô tả nhân vật khi đứng MỘT MÌNH trong khung của mình: ngoại hình, nền, cách đặt khung hình (nhân vật trong khung ngang: đầu vai ở giữa; nhân vật nền: chừa trống phần bị khung che), giọng.
- `[NGHE <KHOÁ>]:` (tuỳ chọn) dáng nghe: ánh mắt nhìn về đâu, nụ cười, gật nhẹ. Luôn kèm "lips stay sealed".
- `[VIDEO SUFFIX]:` nhịp nói (từ/giây đo được ở mục 0), `[NEGATIVE]:`.

Studio tự lo: ảnh gốc mỗi nhân vật (mọi clip bắt đầu từ ảnh này nên mặt/màu không trôi), câu thoại và cảm xúc lấy từ `LUOT`, cắt sát lời, cân màu,
ghép theo bố cục, tiếng chỉ từ người nói. Biến thể dùng `TEN_/NGUOI_/GIONG_/NEN_<KHOÁ>` như thường.

## 4. Biến thể (.json)

```json
[{
  "name": "ten-bien-the-1",
  "NGUOI_HOC": "...", "TEN_HOC": "...", "GIONG_HOC": "...",
  "NGUOI_DAY": "...", "TEN_DAY": "...", "GIONG_DAY": "...",
  "POS_DAY": "TOP", "POS_HOC": "BOTTOM",
  "VIEC": "...", "DAO_CU": "...", "DAO_GIU": "...", "DAO_NGHI": "...",
  "NEN_TRAI": "...", "NEN_PHAI": "...",
  "LUOT": [ {"who": "day", "text": "...", "emo": "curious, friendly"} ]
}]
```

- Một mảng JSON hợp lệ, không comment, không dấu phẩy thừa. `name`: chữ thường không dấu, nối `-`, mỗi biến thể một tên.
- Mọi biến thể có **đúng** tập khoá = token của kịch bản + `name` + `LUOT`.
- Giá trị token bằng tiếng Anh, cụ thể, **ngắn** (1–2 dòng mỗi ô): chúng chèn vào prompt của mọi cảnh.
- `text`: 3–12 từ (tối đa 20). `emo`: 1–3 từ tiếng Anh tả cảm xúc của **người nói**, chọn từ bảng `EMO_CUES` trong `app/production/prompt_parts.py`; bảng này chỉ nên chứa nét mặt và giọng, không cử chỉ tay/thân.
- Các biến thể cùng nhóm khác nhau rõ về nhân vật (khuôn mặt, tóc, kính, trang phục) nhưng cùng phong cách chung; giữ lời thoại giống nhau trừ khi được yêu cầu khác.

## 5. Kiểm tra trước khi giao (viết script Python nhỏ, không đoán)

- JSON đọc được; mỗi biến thể có đúng tập khoá cần; số `LUOT` = số cảnh có thoại.
- Không còn `{{{`/`}}}` thừa; kịch bản không chứa lời thoại thật.
- `POS_DAY`/`POS_HOC` thuộc bộ khoá engine biết.
- Cuối cùng: **chạy thử MỘT biến thể**, xem ảnh khung đầu cảnh 1 trước khi chạy cả nhóm.

## 6. Lỗi thường gặp

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| Hai nhân vật cùng nói/mấp máy | Prompt dài, luật lặp; hai mặt trong một khung | Rút gọn prompt, câu khẳng định; "Gen lại cảnh" kèm yêu cầu sửa; bật "Kiểm tra miệng người nghe và tự gen lại", "Tự gen lại" 1–2 |
| Tư thế lạ lặp lại ở mọi cảnh sau | Một cảnh lệch, cảnh sau nối từ khung đó | Gen lại **từ cảnh đầu tiên lệch**; cấm cử chỉ đó trong `DAO_GIU` và `[NEGATIVE]` |
| Nhân vật này bắt chước nhân vật kia | Cảm xúc dùng cử chỉ lớn | Cảm xúc chỉ bằng mặt và giọng; ghi "giữ đầu thẳng, không bắt chước" |
| Chữ lạ hiện trong khung | Từ viết hoa trong prompt bị vẽ ra | Thêm vào `[NEGATIVE]` |
| Mất tiếng một cảnh | Muse trả clip câm | Studio tự gen lại; nếu còn sót thì chèn im lặng khi ghép |
| "Không kết nối được LUO-API" | Cổng 18610 bị chiếm, API chạy cổng khác | Mở lại app; hoặc sửa Địa chỉ API trong Cài đặt |
| Báo mấp máy khi người nghe chỉ cười | Ngưỡng đo miệng | Đã chỉnh ở `engine.mouth_check`; đo trên clip thật rồi mới đổi thêm |

Khi sửa code đo miệng hay bảng cảm xúc: **đo trên clip thật** trong `userdata/studio/runs/...` trước và sau khi đổi, xem hình các cảnh bị báo; đừng chỉnh ngưỡng bằng cảm giác.
