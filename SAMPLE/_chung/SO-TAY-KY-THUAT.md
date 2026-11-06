# Sổ tay kỹ thuật: từ video tham chiếu đến kịch bản + biến thể chạy được trong LUO Studio

Tổng hợp mọi kỹ thuật đã dùng và đã kiểm chứng qua 10 thể loại (`talka-bang-tu-vung`, `ai-tutor-ngoi-doc`, `canh-sat-nu`, `xe-tai`, `lam-vuon`,
`ghep-hai-lop`, `san-bay-gia-su-ai`, `canh-sat-gia-su-ai`, `soi-hanh-ly-gia-su-ai`, `chia-doi-gia-su-ai`, `Doi toc`), tính đến 05/11/2026.
Mục đích: khi có video mới, agent đối chiếu video với bảng ở mục 2 để chọn khuôn, rồi lắp các kỹ thuật ở mục 3–6 thành kịch bản và biến thể,
kiểm tra bằng mục 7 và nhập vào Studio bằng mục 8. Quy trình từng bước và công cụ: `video-moi.py` (cùng thư mục) và skill `luo-video-moi`.

Quy tắc làm việc (đã được người dùng chốt):
- Tự làm trong phiên hiện tại, không giao session con.
- Mỗi thể loại chỉ sửa file của chính nó (`SAMPLE/<mã>/`, `app/production/types/<mã>/`). Code dùng chung (`engine.py`, `split.py`, `nhieu_phan.py`) chỉ sửa khi nói rõ phạm vi ảnh hưởng và gắn điều kiện theo loại cảnh.
- Ghi lại mọi quyết định và lần thử vào `SAMPLE/<mã>/README.md` để lần sau không lặp lại.
- **Ảnh tham chiếu (`refs`) CHỈ dùng ảnh AI do người dùng cung cấp** (link hoặc tệp). KHÔNG cắt/chỉnh ảnh nhân vật từ video mẫu làm ảnh tham chiếu (chốt 05/11/2026). Chưa có ảnh → hỏi người dùng, chưa gen. Khung video mẫu chỉ dùng để so bố cục (`anh/khung-*-mau.png`), không gửi cho Muse.
- Sau MỖI lượt gen và MỖI lần sửa: thêm một mục vào `NHAT-KY-TRI-THUC.md` (cùng thư mục; mẫu trong file). Mục đã kiểm chứng, dùng chung được → chưng cất vào sổ tay này (mục 3/6) và skill `luo-video-moi`.

---

## 1. Phân tích video (bắt buộc, trước khi viết chữ nào)

| Kỹ thuật | Cách làm | Dùng kết quả vào đâu |
|---|---|---|
| **Bóc lời + nhịp** | `runtime\python.exe SAMPLE\_chung\phan-tich-video.py <video> [--lang en]` → `bao-cao.md/json`: từng câu, giây, **từ/giây**, khoảng lặng, cảnh cắt cứng, khoảnh khắc chuyển động mạnh, ảnh ghép `tong-quan_N.jpg`, `luot_NN.jpg` (4 khung/giây), `chuyen-dong_NN.jpg` | Tốc độ nói ghi vào `[VIDEO SUFFIX]` ("about N words per second, short lines up to M"); số cảnh cắt + chuyển động → chọn khuôn |
| **Xem TỪNG ảnh lượt** | Mở từng `luot_NN.jpg`, `chuyen-dong_NN.jpg`; không đoán từ lời thoại | Bảng hành động: ai nói, người nói làm gì, người nghe làm gì, vật dụng xuất hiện/đổi tay/biến mất, ánh mắt, camera, **khung cuối** |
| **Đo máy quay bằng số** | `video-moi.py danh-gia` (OpenCV, dịch chuyển/zoom nền theo từng đoạn) hoặc tự đo | Quyết định cảnh nào camera đứng yên, cảnh nào có cú lia/đẩy máy thật (xem 3.5) |
| **Đếm mặt theo thời gian** | `video-moi.py danh-gia`: số khuôn mặt và vị trí (trái/phải/trên/dưới) ở mỗi giây | Phân biệt "hai người chung khung thật" với "hai vùng tách biệt" (ghép 2 lớp), phát hiện phần lồng tiếng không ai nói |
| **Đo cao độ giọng** | `video-moi.py danh-gia`: Hz trung vị từng lượt → gộp theo người | Viết `GIONG_<K>` có số đo ("low baritone around 130–150 Hz", "around 200–230 Hz"); cảnh báo khi hai người cùng giới cùng khung |
| **Đối chiếu phụ đề trên hình** | Phụ đề/màu chữ trong video cho biết ai nói và lời đúng; Whisper nghe nhầm ("IA" → "línea", "Wow" → "How?", "You'll speak like" → "I'm like") | Sửa lời trước khi đưa vào `LUOT`; màu phụ đề theo người nói → cấu hình `kieu_theo_phan` |
| **Bảng "video gốc → kịch bản"** | Mỗi hành động/hiệu ứng của video gốc đi vào cảnh nào, chỗ nào đã đơn giản hoá, chỗ nào không gen (hậu kỳ/Thương hiệu) | Giao người dùng duyệt trước khi gen |

Giới hạn đã biết: nhạc nền/tiếng ồn làm Whisper sai; vật nhỏ trong cảnh rộng không tạo đỉnh chuyển động; công cụ không biết ai nói; trên Windows đặt `PYTHONIOENCODING=utf-8` nếu script in tiếng Việt lỗi.
**Video song ngữ** (vd. tiếng Tây Ban Nha xen câu tiếng Anh): `--lang es` làm Whisper bỏ trọn đoạn tiếng Anh (báo khoảng lặng dài bất thường) → chạy thêm ngôn ngữ thứ hai trên `audio.wav`, ghép theo giây, đối chiếu phụ đề trên hình; hậu kỳ dùng Whisper đa ngôn ngữ (`"whisper": "small"`, không `small.en`).
Bản cài không có `runtime\` → dùng `.venv\Scripts\python.exe` và thêm `bin\` (ffmpeg) vào PATH.

---

## 2. Chọn khuôn (quyết định theo đặc điểm video)

Đọc từ trên xuống, lấy dòng đầu tiên khớp. Một video có thể là **nhiều phần**, mỗi phần một khuôn (mục 2.1).

| Đặc điểm nhìn thấy trong video | Khuôn | Mẫu để dùng lại | Cơ chế Studio |
|---|---|---|---|
| Không ai trong hình nói; có giọng đọc ngoài hình; hình đổi (tóc, trang phục, sản phẩm) giữa các câu | **Lồng tiếng + ảnh riêng từng cảnh** | `Doi toc/` | `Voice: "{{LOI_X}}"`, `LUOT: []`, mỗi cảnh `Prompt ảnh`, `Chuyển cảnh: chớp ...`, `Lớp phủ: camera` nếu có giao diện camera |
| Một nhân vật nhìn ống kính, nền có **bảng/tờ giấy có chữ**, bút chỉ chữ, chữ hiện dần | **Nền xanh + hậu kỳ dựng chữ** | `talka-bang-tu-vung/` | Muse chỉ gen robot nền xanh; `post.py` vẽ giấy bằng code, bút, chữ theo Whisper; `[HAU KY] loai:` |
| Một nhân vật đọc cặp câu, phía trên có **bảng hiện câu + phiên âm** | **Chừa trống vùng + bảng gen AI + chữ do code** | `ai-tutor-ngoi-doc/` | Muse gen robot nửa dưới; `post.py` gen khung bảng (Muse, phông xanh) + điền chữ theo `BANG_TU` |
| Hai (ba) người **cùng không gian thật**, tương tác đồ vật (đưa giấy tờ, chỉ vali), một hoặc vài góc máy | **Cảnh thường, khối CẢNH** | `canh-sat-nu/` (1 góc), `soi-hanh-ly-gia-su-ai/` phần 1 (nhiều góc + lia), `canh-sat-gia-su-ai/` phần 1 (4 góc, 3 nhân vật) | Mỗi cảnh một lượt; đổi góc máy = cảnh có `Prompt ảnh`; đạo cụ `DAO_*`; `NGHE_/NHIN_/QUAY_LUNG_` |
| Người học + gia sư trong **cửa sổ gọi video ngang to** phía trên, cùng một clip | **Cảnh thường, bố cục TOP/BOTTOM** | `xe-tai/` | `POS_DAY=TOP`, `POS_HOC=BOTTOM`; đo miệng theo vùng |
| Người học làm việc + **điện thoại dựng cạnh** có gia sư trên màn hình | **Cảnh thường, bố cục LEFT/RIGHT (mẫu gốc)** | `_chung/1-KICH-BAN-MAU.txt` + `lam-vuon/` | Token `VIEC`, `DAO_CU/GIU/NGHI`, `NEN_TRAI/PHAI` |
| Hai nhân vật ở **hai vùng tách biệt**: ô PiP bo góc, badge, split screen, cửa sổ nhỏ | **Ghép 2 lớp** | `ghep-hai-lop/` (ô ngang trên), `chia-doi-gia-su-ai/` (chia đôi dọc), phần 2 của `san-bay`/`soi-hanh-ly` (ô góc trên phải) | `[GHEP HAI LOP]`, gen riêng từng nhân vật, `noi: lien`, `nghe: moi canh`, đo ô bằng `do-vi-tri-dau.py` |
| Tình huống đời thường → người dùng **mở app / gọi AI** → hội thoại với AI | **Nhiều phần** (phần 1 cảnh thường, phần 2 ghép 2 lớp) | `san-bay-gia-su-ai/`, `soi-hanh-ly-gia-su-ai/`, `canh-sat-gia-su-ai/` | `[HAU KY] loai: <mã>` + `===== PHAN n ... | vao: nhoe 0.5 =====`; `gen.py`/`post.py` 5 dòng gọi `_chung/` |
| Robot toàn khung đọc lời kêu gọi + popup cài app, end card, logo/badge, nút cửa hàng | **Không gen** | mọi thể loại | Thương hiệu của dự án: logo cố định, logo bay, Video giới thiệu, Outro |

### 2.1 Chia phần
Cắt phần tại chỗ video đổi **cơ chế** (chung khung → PiP; có người nói → lồng tiếng), không cắt theo cảnh cắt cứng. Hiệu ứng vào phần: `| vao: nhoe 0.5` (whip blur) hoặc chớp màu. Mỗi lượt thoại của biến thể có `"phan"`; lượt phần 1 đứng trước. Mỗi phần chỉ nhận token của nhân vật có mặt trong phần đó (`NHIN_HOC@2` ghi đè riêng cho phần 2).

### 2.2 Đơn giản hoá được phép (ghi vào bảng "video gốc → kịch bản")
- Bỏ cảnh không lời ở đầu/cuối (cảnh sát đi tới, quay lưng đi về xe) hoặc làm bằng `Mở đầu ảnh/video` nếu cần.
- Nhiều cỡ cảnh trong cùng không gian: giữ một khung nếu không có lý do (đổi cỡ cảnh làm mặt/trang phục trôi); giữ nhiều góc khi video gốc cắt liên tục và có ảnh tham chiếu mặt cho mọi nhân vật.
- Người qua lại phía sau → đứng yên, mờ. Mây, xe, băng chuyền → đứng yên trừ khi "In this clip only ...".
- Hai câu liền nhau của cùng một người → một lượt (≤ 20 từ); câu dài hơn → tách hai lượt cùng người. Câu AI "Almost. The best way is to say, I am from Mexico." → tách để hiệu ứng ✅ rơi đúng câu.
- Hai người nói trong một cảnh cận ("Really?" / "Yep.") → tách hai cảnh.
- Hiệu ứng theo âm thanh (vòng sóng nhấp nháy), phụ đề bo tròn, cụm 1–3 từ IN HOA, ❌ dưới chữ → Studio chưa làm; ghi "còn khác video mẫu".

---

## 3. Kỹ thuật viết kịch bản cho Muse

### 3.1 Khung chung của mọi kịch bản
- Khối khoá `[STYLE LOCK]`, `[CHAR LOCK]`, `[SET LOCK]`, `[VIDEO SUFFIX]`, `[NEGATIVE]`; ~300 từ khoá là đủ, 1.000+ từ Muse quên ngữ cảnh. Talka đo được: prompt ~14.000 ký tự làm robot đọc lẫn; bản ~6.000 ký tự ổn.
- Câu **khẳng định, nhìn thấy được**. KHÔNG cấm bằng chính chữ của hành vi: "no talking-like head bobbing, never mirrors the speaker" trong khối NGHE làm 40% clip nghe bị Muse lồng tiếng lẩm bẩm (không có câu đó: 3%, đo 246 clip). Điều cấm để ngắn trong `[NEGATIVE]`.
- Mỗi cảnh = một clip 5–10 giây = một lượt = **một người nói**; người khác im, miệng khép. Nói ngay đầu clip; nói xong về tư thế nghỉ và giữ yên (đuôi im lặng bị cắt).
- **Liên tục khung**: cảnh sau nối từ khung cuối cảnh trước; mọi lệch tư thế truyền sang cảnh sau → cuối cảnh về tư thế nghỉ, cảm xúc chỉ bằng mặt và giọng, không cử chỉ lớn (gãi đầu, nhún vai, che mặt).
- **Hành động phải xảy ra TRONG lúc nói** và xong trước từ cuối (Studio cắt ngay sau từ cuối). Ghi `Diễn biến` (việc gì, ở chữ nào) và `Khung cuối` (ai cầm gì, tay ở đâu). Người nghe **nhìn theo tay** người nói tới đúng vật rồi về mặt người nói.
- Không chữ/logo/giao diện trong hình; mọi chữ do hậu kỳ. Từ vị trí viết hoa (TOP, LEFT) từng bị vẽ thành chữ → đưa vào `[NEGATIVE]`.
- Camera đứng yên, nền tĩnh, ánh sáng cố định, trừ cảnh khai `CAMERA MOVE` (3.5).
- Prompt gửi Muse tiếng Anh; tiêu đề trường và trường mô tả tiếng Việt. Giữ đúng tên trường: Bối cảnh, Voice, Khung đầu, Khung cuối, Diễn biến, Prompt ảnh, Prompt video, Audio, Negative prompt (+ các trường tuỳ chọn ở 3.5).
- Tốc độ nói theo số đo; Muse thường chậm hơn video gốc → nếu vẫn chậm nâng "Tốc độ tăng tối đa" (tối đa 1,35). Giọng "real people caught on camera, not actors"; có thể thêm dòng `DELIVERY` riêng từng cảnh.

### 3.2 Nhân vật và token
- Khoá CHỮ HOA cho mỗi nhân vật (`DAY`, `HOC`, `CANBO`, `BE`, `KHACH`, `THO`...). Token `TEN_/NGUOI_/GIONG_/POS_/VAI_/NGHE_/NHIN_/QUAY_LUNG_/EMO_/BOX_<K>`.
- `VAI_<K>` luôn khai cho thể loại không phải gia sư AI (nếu không, Studio ghi đè giọng `DAY` bằng giọng trợ lý).
- `NHIN_<K>` (hướng nhìn KHI NÓI) khai ngay từ đầu khi nhân vật nói chuyện với người trong khung; không khai thì Muse xoay mặt người nói ra camera. Thêm dòng `EYE LINE` riêng từng cảnh trong `Prompt ảnh`/`Prompt video` ở video nhiều góc.
- `NGHE_<K>` chỉ tả điều NÊN làm khi im: "mouth closed, eyes follow whatever the officer points at, then back to his face". Không dùng `VIEC` ngoài thể loại gia sư AI.
- Đạo cụ: `DAO_<TÊN>` cho vật xuất hiện (vé, giấy tờ, điện thoại, vali, em bé), `DAO_GIU` (cách cầm/giữ nguyên), `DAO_NGHI` (tư thế nghỉ). Vật chỉ xuất hiện đúng cảnh được ghi; không chữ trên giấy, màn hình điện thoại chỉ là chân dung không chữ (rủi ro Muse vẽ chữ → đổi thành màn hình tối).
- Đại từ: khi biến thể có cả nam lẫn nữ cùng một vai, dùng `{{TEN_<K>}}` thay she/he, hoặc token `HE_<K>/HIS_<K>/HIM_<K>` (soi hành lý KHONG-BE).
- Cùng giới, cùng khung: Muse gán giọng cho mặt nào HỢP giọng đó → người nghe nhép và làm động tác người nói. Tách giọng (`pair_voice_split`) không đủ. **Ưu tiên hai nhân vật khác giới hoặc khác hẳn tuổi**; buộc cùng giới thì cảnh báo người dùng, dự phòng `voice_swap: true` (tốn gấp đôi lượt).

### 3.3 Góc qua vai / người quay lưng
Áp đủ 3 việc cùng lúc (sửa từng cái riêng đều thất bại ở sân bay):
1. Tả góc máy bằng hình học: "camera just behind his right shoulder, sees the back of his head, right ear, glasses arm; eyes not visible; face points INTO the scene toward X; never a side profile". Không viết "three-quarter back view".
2. Khai `QUAY_LUNG_<K>` (Studio bỏ mọi câu đòi lộ miệng/nét mặt của người này) và bỏ "with lip-sync", "jaw moves" cho họ trong kịch bản.
3. `NHIN_<K>` + `NGHE_<K>` + luật EYE LINE trong CHAR LOCK; cầm đồ thì "holds X without looking at it".
Người quay lưng là người nói → không có miệng để gán giọng → rủi ro người kia nhép (3.2); chọn cặp khác giới.

### 3.4 Đổi góc máy, đổi bối cảnh
- Cảnh có `Prompt ảnh` sinh khung đầu mới (không nối). Dùng khi đổi góc máy, địa điểm, trang phục, kiểu tóc. Luôn ghi `CAMERA ANGLE:` mô tả rõ ai ở đâu trong khung và `Khung đầu` tương ứng.
- Khi có nhiều khung đầu mới, **bắt buộc gắn ảnh tham chiếu mặt** cho từng nhân vật (`refs` trong biến thể); không có thì mặt/trang phục đổi giữa các góc.
- Khung đầu mới của cảnh chỉ có một người không nhận khung cuối cảnh trước có hai người (Studio chỉ gửi khung cuối khi cùng nhân vật) → bối cảnh khớp nhờ `Ảnh tổng quan` và ảnh tham chiếu.
- Nhãn vị trí lạ (`window-side`, `driver-seat`) → Studio bỏ đo miệng người nghe ở cảnh đó; nghe kỹ các cảnh hai người chung khung, hoặc khai `BOX_<K>`.
- Đổi hình giữa chừng (tóc) KHÔNG giao cho Muse biến hình trong clip: mỗi kiểu một `Prompt ảnh`, chuyển cảnh chớp sáng che chỗ đổi ảnh, câu dài tách làm hai để mỗi hình có một clip có lời.

### 3.5 Chuyển động máy và cảnh không lời (trường tuỳ chọn của cảnh)
| Trường | Khi dùng | Ghi chú đã kiểm chứng |
|---|---|---|
| `Chuyển cảnh: chớp trắng/vàng/đen/#RRGGBB [giây]` | Che chỗ đổi ảnh, nhịp quảng cáo | ffmpeg lúc ghép, không đổi độ dài |
| `Chuyển cảnh: lia phải/trái 0.36` | Cú vụt máy giữa hai góc (chỉ thể loại nhiều phần có `gen.py`) | Chắc hơn giao Muse lia khi có người ngoài khung |
| `Ảnh tổng quan:` (prompt ảnh ngang 16:9 cả bố cục) + `Khung đầu cắt: trái/giữa/phải/0..1` | Cảnh có cú lia trong MỘT clip, Muse cần biết người/vật ngoài khung ở đâu | Ảnh ngang gửi kèm gen video và các khung đầu sau; kiểm tra `scene1_wide.png` |
| Khối `CAMERA MOVE` trong Prompt video | Bắt đầu từ đâu, theo cái gì, nhanh/chậm ở chữ nào, dừng ở ai; khoá chung phải cho phép ("still unless the clip describes a CAMERA MOVE") | KHÔNG để nhân vật "keeps pointing" khi máy lia (tay đi theo máy, chỉ nhầm người); người chỉ xong hạ tay RỒI máy mới vụt |
| `Giữ sau lời: N` | Có việc xảy ra SAU từ cuối mà cảnh sau cần (máy lia sang người kia) | Không có thì mọi chuyển động sau từ cuối bị cắt |
| `Lia nhanh: 3` (+ `Giữ sau lời` đủ dài) | Muse lia chậm đều ~2 s; tua nhanh đoạn lia SAU từ cuối N lần + nhoè ngang | Khung cuối không đổi |
| `Lia theo tay: 1` (đi kèm `Lia nhanh`) | Muse để máy đứng yên khi nhân vật giơ tay chỉ; thêm N giây đẩy máy theo tay về phải-dưới | Đặt vật được chỉ ở phía phải-dưới khung đầu |
| `Mở đầu ảnh/video/dài: 1.5` | Đoạn không lời trước câu nói (vali trôi ra khỏi máy soi) | Ghép cắt cứng, không thêm lượt; chuyển động khác khoá ghi "In this clip only ..." |
| `Lớp phủ: camera [png]` | Giao diện camera điện thoại + viền bám mặt | Muse không vẽ gì; cảnh chỉ MỘT mặt rõ, đầu ở 1/3 trên |
| Cảnh không `{{LUOT_n}}`, Voice trống | Cảnh hành động/b-roll không lời | Đường code có, chưa chạy thật: thử 1 biến thể |
| `Khung đầu từ cảnh: N` | Cảnh quay lại đúng góc máy của cảnh N trước đó (người dùng muốn "y hệt khung cảnh X") | Dùng NGUYÊN ảnh khung đầu của cảnh N, không vẽ lại: nền, vị trí người, khung hình giống hệt (06/11, canh-sat-gia-su-ai). Không cần `Ảnh tổng quan` cho cảnh đó |
| `Mở đầu khung từ cảnh: N` | Đoạn không lời đầu cảnh (đưa giấy tờ...) phải đúng bố cục cảnh N | Như trên, cho `Mở đầu ảnh` |

Bài học camera (soi hành lý, 6 lần sửa): không giao chuyển động máy cho Muse khi có người ngoài khung mà Muse chưa "thấy"; cho Muse ảnh tổng quan; ảnh khung đầu đã ở sẵn tư thế cần (ngón tay trên nắp vali); mép khung trống (không tay/em bé lọt vào); mô tả chỉ tay "points DOWN ... never sideways, never toward the edge of the frame or any person".

### 3.6 Ghép 2 lớp (`[GHEP HAI LOP]`)
- `nen: <K>`; `khung <K>: x, y, RỘNG, CAO` (0..1, góc trên-trái + kích thước; **không phải toạ độ hai góc**; kiểm tra x+RỘNG ≤ 1, y+CAO ≤ 1). Nền cũng có thể có `khung` riêng (chia đôi: `khung HOC: 0.5, 0, 0.5, 1` + `khung DAY: 0, 0, 0.5, 1`).
- Tỉ lệ gen suy từ khung: r = (RỘNG·720)/(CAO·1280): ≥ 1,4 → 16:9; 0,75–1,4 → 1:1; < 0,75 → 9:16. Mô tả nhân vật trong khung phải khớp tỉ lệ đó ("wide call-window, head and shoulders centred" / "portrait-oriented frame, head in the upper third"). Ô hẹp hơn 9:16 → Studio cắt DẢI GIỮA: dặn nhân vật đứng giữa, đồ quan trọng ở nửa giữa.
- **Vị trí ô đo bằng** `runtime\python.exe SAMPLE\_chung\do-vi-tri-dau.py <phan2 của lần chạy | video> --nen HOC --goc tren-phai --noi-ngang 0.15` → dòng `khung DAY:`; sau lần chạy thật đầu tiên đo lại trên người gen thật. Ô che mặt = lỗi người dùng phản ánh; ô 0,20×0,18 bị chê quá bé.
- `noi: lien` (mặc định): clip sau của mỗi nhân vật nối từ khung cuối clip trước của chính nó; Studio căn khớp hình/màu, khoá camera, gen lại nếu Muse phóng > x1,15. KHÔNG dùng `lam moi` (đã bỏ: khựng mạnh).
- `nghe: moi canh` (khuyên dùng) / `nghe: dung lai 3` (rẻ) / `nghe: tinh` (ảnh tĩnh, đứng hình). `khoa mieng` mặc định tắt (trông như dán miệng giả).
- `[NHAN VAT <K>]` tả nhân vật đứng MỘT MÌNH: khung hình, nền, **câu tả cỡ đầu/vị trí phải khớp ảnh gốc** (Muse làm theo chữ hơn khung đầu). Nhân vật nền chừa trống vùng sẽ bị ô đè ("nothing drawn there, no window, no inset"), ánh mắt liếc về phía ô khi nghe. Câu VOICE đứng riêng một câu (Studio lọc khỏi prompt nghe).
- `[NGHE <K>]`: chỉ điều nên làm; "The lips stay gently pressed together the whole clip; the head stays mostly still". Không viết "Reacts visibly... smiles along" (Muse cười hé môi, gật theo nhịp).
- Gắn `refs` ảnh tham chiếu cho **mọi** nhân vật (Studio gửi khung nối + ảnh gốc + ảnh tham chiếu ở mọi clip, từ 05/11/2026).
- Sửa kịch bản sau khi đã chạy dở: xoá `base_<K>.png`, `listen_<K>_*.mp4`, `scene*_spk.mp4`, `scene*_cut.mp4`, `_mask_*`, `_border_*` (Studio dùng lại file có sẵn).
- **Ô không được che mặt nhân vật nền** (06/11: ô AI 1/3 trên + phụ đề che mắt tài xế): `[NHAN VAT <nền>]` ghi rõ "the top of the hair at about N% down from the top edge; the upper M% shows only background". Studio tự dò mặt ảnh `base_<nền>.png`: mặt (cả tóc) nằm trong ô hoặc dải phụ đề 7% dưới ô → gen lại 1 lần kèm yêu cầu số % (Muse thường bỏ qua), vẫn che → dịch ảnh xuống (cách thật sự có tác dụng) (`split.head_span` / `shift_down`).

### 3.7 Lồng tiếng ngoài khung
`Voice: (Lồng tiếng ngoài khung hình, người trong hình KHÔNG nói) "{{LOI_MO}}"`; Prompt video "the off-screen narrator says: ... The man never speaks"; biến thể `"LUOT": []`; phụ đề lấy từ lời trong ngoặc kép. Tránh token đánh số liên tiếp (`LOI_1`, `LOI_2`: Studio coi là chuỗi).

### 3.8 Chữ, bảng, đồ hoạ trong hình → tách lớp, hậu kỳ ghép

Nguyên tắc: **Muse chỉ gen thứ Muse làm tốt (nhân vật nói)**; mọi thứ cần chính xác (chữ, bảng, bút, đồ hoạ, nền cố định) tách thành lớp riêng, do code vẽ hoặc gen AI một lần rồi ghép bằng ffmpeg/PIL theo mốc Whisper. Thứ tự ưu tiên (rút từ 6 cách thử ở Talka): (1) **code vẽ** > (2) **gen AI một lần trên phông màu, cắt phông, dùng lại** > (3) Muse tự vẽ chữ (sai hàng, đè chữ, không bám nhịp lời, chữ có dấu méo, lan sang cảnh sau).

| Kỹ thuật | Cách làm đã chạy | Chỗ dùng | Lưu ý đã kiểm chứng |
|---|---|---|---|
| **Nhân vật gen trên phông xanh lục phẳng, mọi cảnh** | Kịch bản bắt "flat chroma-key green background" ở mọi cảnh; hậu kỳ `ffmpeg colorkey (similarity 0.22, blend 0.08) + despill green` rồi ghép lên lớp nền | `talka-bang-tu-vung` (`post.py` → `compose`) | Lấy **màu xanh thật** từ góc trên/mép trái khung để key (Muse không ra xanh phẳng tuyệt đối: gradient, vệt sáng); viền robot khuyết/lẫn xanh → gen lại cảnh đó; kiểm `is_green_bg` trước khi key (video kịch bản cũ không phải nền xanh thì giữ nguyên). Robot được đo (đỉnh đầu, tâm đầu, bề rộng đầu) rồi **phóng/thu và dời ở hậu kỳ** cho khớp bố cục video mẫu (`config.json` → `bo_cuc`), thân luôn chạm đáy khung |
| **Chừa trống vùng khung thay vì phông xanh** | Kịch bản bắt vùng trên khung "only background, nothing important" (bảng ghép sau); không cần key | `ai-tutor-ngoi-doc` (bảng đè lên 1/3 trên) | Dùng khi nền thật (quán cà phê) cần giữ và lớp ghép là ô đặc không cần lộ nền phía sau |
| **Bảng/khung gen AI MỘT lần trên phông magenta, cắt phông, cache** | Prompt ảnh Muse: "wide landscape board, huge blank white panel ~80%, decoration small on top edge, isolated on flat pure chroma-key magenta #FF00FF"; cắt phông, tìm lòng trắng (`find_inner`), ép về cỡ/vị trí cố định (`fit_board`: kéo phần giữa, giới hạn phần trang trí), lưu `board.png`/`board_raw.png` cạnh `raw.mp4`, lần sau dùng lại; không gen được → vẽ bảng đơn giản bằng code (`fallback_board`) | `ai-tutor-ngoi-doc` | **Magenta chứ không xanh lá**: xanh lá làm mất phần xanh của cờ (Bồ Đào Nha, Brazil); khử ám hồng chỉ ở viền. Trang trí quá cao → gen lại bảng. Muốn bảng khác: xoá `board.png` rồi Hậu kỳ lại |
| **Giấy/bảng vẽ hoàn toàn bằng code** | `giay.py` vẽ checklist / giấy kẻ hai cột / sổ lò xo từ `HAU_KY.bang` của biến thể: biết **toạ độ từng từ** nên bút và chữ không bao giờ lệch hàng; ảnh mẫu trong `SAMPLE/talka-bang-tu-vung/anh-mau/` | `talka-bang-tu-vung` | Giấy không gửi cho Muse. Từ vựng lấy từ chính biến thể (`bien_the.py`): biến thể mới không cần sửa code |
| **Chữ do code điền, đổi đúng lúc theo lời** | Whisper từng cảnh (ngôn ngữ theo biến thể) → mốc từ; `find_seq` tìm cụm trong lời → thẻ chữ đổi tại thời điểm đó (ai-tutor: cặp câu + phiên âm; Talka: chữ tiếng Anh hiện khi bút chạm, ô quảng cáo hiện đúng cụm robot đang nói, tô đỏ tên app/số/đơn vị) | cả hai | Studio cắt sát lời nên **không dùng giây của video gốc**, luôn căn theo video đã gen. Robot đọc sai/thiếu cặp → chữ lệch → gen lại cảnh đó |
| **Đạo cụ nhỏ gen AI trên phông xanh rồi cắt, dùng làm sprite** | Cây bút: Muse gen trên phông xanh, cắt phông, lưu `assets/marker.png` + `marker.json` (toạ độ ngòi); `pointer.py` di chuyển bút trượt êm theo từ đang đọc, nằm **dưới** lớp robot | `talka-bang-tu-vung` | Thử cho Muse vẽ tay + bút trong clip → viết đè hàng, không bám nhịp; bàn tay vẽ bằng code → người dùng chê không tự nhiên, bỏ |
| **Nền động gen AI riêng (video)** | Hậu kỳ gọi Muse gen video nền (thành phố hoàng hôn) theo `NEN_PHO`, lưu `nen_pho.mp4` cạnh `raw.mp4`, dùng lại; xoá để gen nền khác | `talka-bang-tu-vung` cảnh quảng cáo | Xếp lớp từ dưới lên: nền video → ô bảng cố định → robot đã key |
| **Ghép 2 lớp nhân vật** (PiP/chia đôi) | Mỗi nhân vật gen riêng, ffmpeg ghép theo `[GHEP HAI LOP]` (3.6) | ghép 2 lớp, phần 2 các dự án | Không key phông: ô hình chữ nhật/bo góc đè thẳng |
| **Lớp giao diện đè theo mặt** | `Lớp phủ: camera`: giao diện camera + viền trứng bám mặt bằng mediapipe | `Doi toc` | Muse không vẽ gì; cảnh một mặt rõ |

Thứ tự lớp chuẩn (Talka): nền (ảnh code vẽ hoặc video gen AI) → bảng/ô chữ cố định → bút/sprite → **nhân vật đã key trên cùng**; chữ "sau lưng" nhân vật thì đặt dưới lớp nhân vật. Mọi lớp dựng ở 1080×1920 rồi mới ghép.

Khi phân tích video mới: liệt kê từng thành phần trên hình (nhân vật, nền, bảng, chữ, bút, badge, giao diện, popup) và quyết định cho mỗi thành phần: Muse gen / code vẽ / gen AI một lần / Thương hiệu / bỏ. Ghi vào bảng "video gốc → kịch bản". Thành phần nào Muse phải gen cùng nhân vật (ví dụ đồ vật nhân vật cầm) thì mới để Muse làm.

---

## 4. Biến thể (.json)

- Mảng JSON; mỗi biến thể = `name` + `LUOT` + **đúng** tập token của kịch bản (+ `refs`). Giá trị tiếng Anh, cụ thể, 1–2 dòng.
- `LUOT`: `{"who", "text" (3–12 từ, ≤ 20), "emo" (1–3 từ trong `EMO_CUES` của `app/production/prompt_parts.py`)}` + tuỳ hậu kỳ: `"phan"`, `"c"` (màu chữ), `"fx"` (`wrong`/`right`/`none`), `"icon"` (`x`/`check`/`dollar`), `"dich"`, `"nhan"`, `"to"`. Video không có nhịp sửa lỗi: `"fx": "none"` ở mọi lượt.
- Nhịp sửa lỗi: câu sai của người dùng (`fx: wrong`, `c: red`, `icon: x`) → câu đúng (`fx: right`, `c: green`, `icon: check`) đặt ở lượt **như video mẫu** (san-bay: ở lượt AI; soi-hanh-ly/chia-doi: ở lượt người dùng nói lại đúng).
- **Sinh bằng script** `SAMPLE/<mã>/cong-cu/tao_bien_the*.py` từ một bảng (tên, ngoại hình EN, giọng EN, link ảnh, tham số như tuổi), không sửa tay JSON: đổi tuổi thì câu sai/sửa/đúng cùng đổi; câu "visiting my ..." hợp tuổi.
- `refs`: `{"NGUOI_HOC": ["<link>"]}`; nhận ảnh trực tiếp, prnt.sc, Google Drive chia sẻ, đường dẫn tệp tương đối từ gốc repo. Ảnh tham chiếu đứng nền xanh → kịch bản dặn bỏ nền và tư thế đứng.
- Cùng nhóm: khác rõ khuôn mặt (hình mặt, mắt, kính, râu, tóc, màu áo), cùng tuổi/giới/phong cách; giọng hai bên khác hẳn (cao độ, âm sắc, tốc độ).
- Hậu kỳ theo phần/người nói: `app/production/types/<mã>/config.json` → `phu_de.kieu_theo_phan`, `y_theo_phan`, `co_chu`, `vien`, `whisper`.

---

## 5. Thể loại mới cần code riêng?

| Cần | Làm | Không cần code mới khi |
|---|---|---|
| Nhiều phần / trộn chế độ | `app/production/types/<mã>/gen.py` 5 dòng gọi `_chung/nhieu_phan.run` | Một phần cảnh thường hoặc một phần ghép 2 lớp (Studio tự chạy) |
| Phụ đề 2 màu, dòng dịch, icon, viền theo phần | `post.py` 3 dòng gọi `_chung/hau_ky.main(HERE)` + `config.json` | Phụ đề chung (`postprocess.py`) đủ |
| Đồ hoạ riêng (bảng, giấy, bút) | `post.py` riêng (xem `talka-bang-tu-vung/`, `ai-tutor-ngoi-doc/`) | — |
Khai trong kịch bản: `[HAU KY]:\nloai: <mã>` (token chỉ dùng cho hậu kỳ cũng đặt trong khối này).

---

## 6. Lỗi đã gặp và cách sửa (tra trước khi đoán)

| Hiện tượng | Nguyên nhân thật | Cách sửa đã kiểm chứng |
|---|---|---|
| Người nói quay mặt ra camera/ra ngoài khung | Prompt hệ thống + kịch bản đòi thấy miệng người nói; không khoá hướng nhìn | 3.3 (hình học + `QUAY_LUNG_` + `NHIN_`/EYE LINE). Dựng lại prompt thật trước khi sửa |
| Người nghe nhép miệng/gật theo nhịp (ghép 2 lớp) | Khối NGHE nhắc tới nói/người nói (dù để cấm); "Reacts visibly... smiles" | Chỉ tả điều nên làm; Studio lọc `_calm_listen`, đo tiếng > −45 dB gen lại |
| Người nghe nhép + làm động tác người nói (chung khung) | Cùng giới; người nói quay lưng | Đổi cặp khác giới; `voice_swap` dự phòng |
| Nhân vật to/nhỏ, nền đổi giữa các cảnh ghép | Câu tả khung trong `[NHAN VAT]` khác ảnh gốc; Muse tự phóng | Sửa câu tả khớp ảnh gốc; Studio khoá camera, gen lại > x1,15 |
| Khựng ở chỗ nối, lệch màu | `lam moi` vẽ lại khung | Bỏ `lam moi`; `noi: lien` căn khớp |
| Ô robot che mặt | Ô đặt theo cảm tính | `do-vi-tri-dau.py` đo trên clip thật |
| Chỉ tay nhầm vào người/em bé; máy lia sai hướng | Ảnh khung đầu chưa ở tư thế chỉ; "camera follows his arm"; người ngoài khung Muse chưa thấy | 3.5: ảnh tổng quan, tay chỉ xong mới lia, mép khung trống |
| Chữ sai hàng, đè chữ, hiện sớm | Muse vẽ chữ | 3.8: chữ do code; gen lại từ cảnh đầu sai |
| Robot đọc lẫn từ tiếng Anh vào câu hỏi | Prompt quá dài, từ lặp nhiều lần | Rút gọn prompt; gen lại cảnh + cảnh sau |
| Lời lặp/thừa/thiếu từ | Muse | Studio kiểm lời từng chữ, gen lại (`speech_retries`) |
| Tư thế lạ lặp ở mọi cảnh sau | Một cảnh lệch, cảnh sau nối | Gen lại từ cảnh đầu tiên lệch; cấm cử chỉ đó |
| Chữ lạ trong khung | Từ viết hoa trong prompt | `[NEGATIVE]` |
| Lặng 2–3 s sau câu tiếng Tây Ban Nha/ngôn ngữ khác, video dài gấp đôi | Whisper kiểm lời cố định `small.en` báo "thiếu chữ" sai → bỏ cắt sát | Đã sửa trong engine: `speech_lang` chọn Whisper theo ngôn ngữ câu (05/11/2026). Câu lẫn hai thứ tiếng: dấu ¿¡/từ TBN quyết định |
| Người nghe nhép dù đo miệng dưới ngưỡng (ghép 2 lớp) | Clip nghe có tiếng lẩm bẩm, chưa có clip câm dự phòng | Đã sửa: clip nghe có tiếng → khoá miệng / khung nối đứng yên |
| Khung nửa ghép rung lắc | Khoá camera nắn từng khung theo ước lượng nhiễu | Đã sửa: khớp đa thức bậc 2 theo thời gian; đo rung bằng `phaseCorrelate` vùng nền trước/sau |
| Ting ting/viền sai/đúng rơi vào câu đầu của lượt nhiều câu | `fx` luôn gắn dòng đầu | Đã sửa: gắn vào dòng chứa cụm `to`; lượt nhiều câu có fx thì PHẢI khai `to` |
| Câu nói lặp hai lần vẫn được giữ | Chọn lần gen "ít lỗi nhất" theo số lỗi | Đã sửa: luôn ưu tiên bản không lặp |
| Người thật nhép + nhắm mắt/đổi nét mặt y hệt robot đang nói (chung khung, chỉ cảnh robot nói) | (1) Mô tả robot có "sculpted closed lips" → Muse coi môi robot là chi tiết cứng, đẩy khẩu hình sang mặt người duy nhất; (2) người nghe nghiêng ba phần tư/nghiêng hẳn nên khe môi nhỏ, luật đo cũ đòi "há rộng ≥ 18% khung" nên lọt; (3) Cài đặt "Kiểm tra miệng người nghe" đang tắt | Robot/nhân vật không phải người: tả môi "open and move naturally with every word whenever it speaks", KHÔNG viết "closed/sculpted/painted lips"; prompt cảnh robot nói tả người nghe TRƯỚC (môi mím, mắt mở, đầu yên, "does not copy"), robot không làm cử chỉ đầu; engine thêm luật nghiêng mặt (đo theo nhịp mở-khép + biên độ, 05/11/2026); bật kiểm tra miệng + tự gen lại ≥ 2 |
| Lỗi đột ngột đổi kiểu | Phiên khác sửa engine/split | `git diff` trước; thống kê theo câu chữ prompt trong `userdata/api/data/tasks.json` |
| Nền/khung hình nhảy ở 0,4-0,9 s đầu mọi cảnh ("background đổi nhiều lần trong 1 cảnh") | Muse chiếu khung đầu một lát rồi tự cắt sang khung khác | Engine tự dò (`start_jump`, chênh khung ≥ 12 và ≥ 5× trung vị) và giữ khung sau cú nhảy cho đoạn trước (`hold_after_jump`), tiếng giữ nguyên; bỏ qua cảnh lia máy |
| Người không có trong cảnh vẫn hiện ra (cảnh sát ở cửa sổ cảnh cận, cảnh "Yes") | Engine (SPEAKER MAP) tả MỌI nhân vật là "đang im lặng trong khung"; hướng nhìn ghi "nhìn cảnh sát ở cửa sổ"; câu thoại gọi tên người kia ("Officer, ...") | Biến thể từ 3 nhân vật: `"nguoi_theo_canh": true` (kiem-tra báo LỖI nếu thiếu) → chỉ tả người có tên trong cảnh (bỏ qua dòng "Mở đầu"); hướng nhìn cảnh cận chỉ tả hướng mắt; `CAMERA LOCK` (không lia/thu xa, người được nói chuyện luôn ngoài khung) |
| Vị trí người đảo lộn giữa các cảnh cùng góc; cảnh không lời sai chỗ ngồi | Mỗi cảnh tự vẽ khung đầu; câu "bé luôn ngồi cạnh bố" trong khoá chung bị áp cả cho góc không có bé; ảnh bố cục chung bị Muse chép nguyên khung hình | `Khung đầu từ cảnh: N` / `Mở đầu khung từ cảnh: N`; vị trí người chỉ ghi trong CAMERA ANGLE của góc có người đó; không gắn ảnh bố cục chung vào `refs` |
| Tay/chi tiết lạ ở mép khung | Chép chi tiết video gốc ("cẳng tay bố ở mép dưới") | Cảnh cận: "ONLY <người> is in the frame: no hands or arms of anyone else" |
| Phụ đề hiện sớm, chạy trong đoạn không lời đầu cảnh | Căn phụ đề từ đầu cảnh, không biết có đoạn "Mở đầu" | Engine ghi `scene<N>_cut.mp4.pre`; `scenes.json` có `speech`; căn phụ đề từ mốc đó |
| Clip "mới" giống từng byte clip cũ | Muse lỗi 502, LUO-API xin "gắn file" → Muse gắn file cũ trong chat | LUO-API: `GEN_FAILED_RE` → báo lỗi để gen lại. Nghi ngờ: `md5sum` clip mới với bản cũ |
| Làm lại vài cảnh rời rạc mà mất cả cảnh tốt | `nhieu_phan` coi `scene<N>_cut.mp4` ở THƯ MỤC GỐC lượt chạy là "cảnh đã xong"; thiếu file đó thì xoá file cảnh trong `phan<k>/` | Chỉ xoá đúng cảnh cần làm lại ở CẢ thư mục gốc lẫn `phan<k>/`; không dọn hết thư mục gốc |

---

## 7. Kiểm tra trước khi giao (bằng code Studio, không đoán)

`runtime\python.exe SAMPLE\_chung\video-moi.py kiem-tra <kịch bản.txt> <biến thể.json>` kiểm:
JSON hợp lệ; token kịch bản = khoá biến thể; số cảnh = số lượt (cảnh thường) hoặc `[GHEP HAI LOP]` đọc được (`split.parse`); nhiều phần: `nhieu_phan.plan` không lỗi, mọi lượt có `phan`, đúng thứ tự; `who` thuộc nhân vật của phần; `emo` trong `EMO_CUES`; text ≤ 20 từ; đúng một cặp `wrong` → `right` (nếu có); không còn `{{` sau khi điền; độ dài prompt; link `refs` tải được (tuỳ chọn `--tai-anh`).
Sau đó: **chạy thử MỘT biến thể**, xem `scene1_start.png` (và `scene<n>_start.png` của mọi cảnh đổi góc, `scene1_wide.png` nếu có ảnh tổng quan), `base_<K>.png` của ghép 2 lớp, clip cảnh đầu; rồi mới chạy cả nhóm.
So từng cảnh với video gốc bằng ảnh ghép 8 khung gốc ↔ 8 khung gen (mẫu: `SAMPLE/canh-sat-gia-su-ai/cong-cu/so_sanh.py`, bảng shot → giây), sửa kịch bản cảnh lệch rồi gen lại riêng cảnh đó trước khi đi tiếp. `kiem-tra` còn báo: `Khung đầu từ cảnh` trỏ sai, ≥3 nhân vật thiếu `nguoi_theo_canh`, cảnh cận nhắc người khác, ghép 2 lớp chưa ghi vị trí đầu dưới ô.

---

## 8. Đưa vào Studio

`runtime\python.exe SAMPLE\_chung\video-moi.py nhap <kịch bản.txt> <biến thể.json> --ten-loai "<tên>" --ten-du-an "<tên>" [--chay-thu]`
đọc `userdata/running.json` lấy địa chỉ Studio đang chạy, `POST /api/types` (Studio phân tích token, tạo trường), `POST /api/projects` (tải `refs`), tuỳ chọn thêm biến thể đầu vào hàng đợi và bắt đầu. Studio phải đang mở. Thương hiệu (logo, intro, outro) người dùng chọn trong trang dự án.

---

## 9. Hồ sơ một thể loại (để lần sau dùng lại)
```
SAMPLE/<mã>/
  README.md               dạng video, bảng phần/cảnh/chế độ, file, cách chạy, quyết định đã chốt, lỗi đã gặp
  PHAN-TICH-VIDEO-MAU.md  tổng quan, bảng hành động, bảng "video gốc → kịch bản"
  KICH-BAN-*.txt          kịch bản (sinh bằng cong-cu/tao_kich_ban.py nếu nhiều cảnh)
  BIEN-THE-*.json         biến thể (sinh bằng cong-cu/tao_bien_the*.py)
  PROMPT-CHO-AGENT.txt    quy tắc riêng, lỗi hay gặp, danh sách tự kiểm tra
  cong-cu/, anh/, phien-ban-cu/
app/production/types/<mã>/  gen.py, post.py, config.json, README.md (nếu cần)
```
