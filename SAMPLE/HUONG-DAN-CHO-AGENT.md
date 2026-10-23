# Hướng dẫn cho agent: viết kịch bản và biến thể cho LUO Studio (mọi thể loại video)

Bạn tạo ra 2 file mà Studio nhập được và Muse gen đúng ý, cho **bất kỳ thể loại nào** (hội thoại, tư vấn, review, kể chuyện, tình huống đời thường, quảng cáo nhiều cảnh...):
1. **Kịch bản** (`.txt`): khung prompt có token `{{...}}` → tab "Loại dự án" → "Loại mới".
2. **Biến thể** (`.json`): mảng các video, mỗi phần tử điền token + lời thoại.

File mẫu: `1-KICH-BAN-MAU.txt`, `2-BIEN-THE-MAU.json`; ví dụ bố cục khác: thư mục `Xe tai/`. Hai file mẫu chỉ là **một thể loại** (người học + gia sư AI), không phải khuôn bắt buộc.

## 0. Phân tích video tham chiếu (BẮT BUỘC, làm trước khi viết bất cứ thứ gì)

Không phân tích video bằng vài ảnh chụp thưa hay chỉ lời thoại: hành động nhỏ (đưa giấy tờ, lấy điện thoại), tốc độ nói và tư thế khung cuối sẽ bị bỏ sót hoặc hiểu sai. (Đã từng xảy ra: nhìn thưa nên mô tả sai cảnh "tài xế cầm điện thoại".) Luôn chạy công cụ:

```
runtime\python.exe SAMPLE\phan-tich-video.py "C:\duong-dan\video.mp4" [thu-muc-ra]
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
- Có thể đính kèm ảnh tham chiếu (mặt, trang phục) hoặc mp3 mẫu giọng cho từng ô ở giao diện.
- Số lượt thoại nhiều hơn số cảnh trong kịch bản: Studio tự nhân bản cảnh cuối.

**Mô hình nhân vật tổng quát (số nhân vật bất kỳ, khoá bất kỳ):**
- Mỗi nhân vật có một **khoá** chữ HOA không dấu, ví dụ `MC`, `KHACH`, `THO`, hoặc `DAY`/`HOC` (hai khoá cũ). Lượt thoại ghi `"who": "<khoá viết thường>"` (ví dụ `"who": "mc"`); `day`/`hoc` chỉ là hai khoá đặc biệt, không còn bắt buộc.
- Các token của nhân vật đặt theo quy ước `<LOẠI>_<KHOÁ>`:
  - `TEN_<K>` (bắt buộc; tên gọi ngắn dùng trong prompt), `NGUOI_<K>` (ngoại hình), `GIONG_<K>` (giọng, nên khác hẳn giọng người khác);
  - `POS_<K>` (nhãn vị trí viết vào prompt, chữ bất kỳ, ví dụ `LEFT`, `TOP`, `center-right`);
  - `BOX_<K>` (tuỳ chọn): hộp khuôn mặt `"x0,y0,x1,y1"` theo tỉ lệ khung hình 0..1, **dùng cho bộ đo miệng ở bố cục bất kỳ**. Nếu không có `BOX_<K>`, `POS_<K>` phải là `LEFT`/`RIGHT`/`TOP`/`BOTTOM`; nhãn lạ mà không có `BOX_` thì Studio bỏ qua đo miệng cho nhân vật đó (không đo nhầm mặt);
  - `VAI_<K>` (tuỳ chọn; tên vai trong prompt, ví dụ `host`; mặc định `tutor`/`learner` cho `DAY`/`HOC`, `character` cho khoá khác), `NGHE_<K>` (tuỳ chọn; tư thế khi im lặng, ví dụ "nhìn người nói, miệng khép"; mặc định "eyes on the camera" chỉ hợp khi nhân vật nhìn vào ống kính), `EMO_<K>` (cảm xúc mặc định khi lượt không ghi `emo`).
- Mỗi clip chỉ MỘT nhân vật nói, **tất cả nhân vật còn lại im lặng**. Studio tự lập "SPEAKER MAP" (VOICE A, B, C... theo thứ tự `DAY`, `HOC`, rồi các khoá còn lại), bỏ khoá giọng của người im lặng, và đo miệng **từng người nghe** (có lỗi thì gen lại kèm yêu cầu sửa).
- Cảnh không có lời thoại (không dùng `{{LUOT_n}}`, trường Voice trống): Studio không đòi tiếng, không cắt theo lời, không đo miệng. Nếu clip câm, khi ghép sẽ chèn im lặng.
- Chỉ dùng `VIEC` (việc người học đang làm) cho loại "người học + gia sư AI": nó khiến người học nghe "cúi xuống làm việc, quay mặt đi", không hợp thể loại khác. Thể loại khác **bỏ `VIEC`** và dùng `NGHE_<K>`.
- Nếu hai vai `DAY`/`HOC` **cùng giới** và biến thể không khai `VAI_DAY`/`VAI_HOC`, Studio (bật "Tách giọng") ghi đè giọng `DAY` bằng giọng "trợ lý gọi video tươi sáng". Chỉ hợp gia sư AI; thể loại khác hãy khai `VAI_*` (khi đó Studio không ghi đè) hoặc chọn các nhân vật có giọng khác hẳn nhau.
- Video không có nhịp "sửa lỗi": đặt `"fx": "none"` ở **mọi** lượt thoại để tắt viền đỏ/xanh tự động (chỉ áp cho khoá `hoc`/`day`).

**Giới hạn hiện còn:**
- Giao diện Studio: nút chọn người nói ở từng lượt chỉ có "Dạy"/"Học". Biến thể có khoá khác phải nhập từ file JSON (giao diện vẫn hiển thị và chạy được, nhưng bấm đổi người nói sẽ chuyển về `day`/`hoc`). Các trường token của khoá lạ hiện ở nhóm "khác" trong tab biến thể.
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
