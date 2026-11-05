---
name: luo-video-moi
description: Quy trình trọn gói cho LUO Studio khi người dùng đưa MỘT VIDEO THAM CHIẾU MỚI (file .mp4, link, hoặc thư mục phân tích) và muốn có kịch bản + biến thể chạy được trong Studio. Dùng ngay khi người dùng nói "import video", "video mới", "làm video này", "phân tích video này rồi viết kịch bản", "thêm thể loại", "remake video này trong Studio", hoặc chỉ đính kèm video kèm vài chữ. Bao gồm phân tích bằng công cụ, đối chiếu với bảng kỹ thuật đã kiểm chứng (SAMPLE/_chung/SO-TAY-KY-THUAT.md) để chọn khuôn thể loại, viết kịch bản + biến thể theo đúng mẫu đã có, kiểm tra bằng code Studio, rồi nhập vào Studio đang chạy và chạy thử một biến thể. KHÔNG dùng cho sửa code Studio thuần kỹ thuật hay hậu kỳ video có sẵn.
---

# Video mới → kịch bản + biến thể → Studio

Mục tiêu: từ một video tham chiếu, ra đủ bộ `SAMPLE/<mã>/` (phân tích, kịch bản, biến thể, README, PROMPT-CHO-AGENT) và dự án đã nằm trong Studio,
đã chạy thử một biến thể. Tri thức nền: **đọc `SAMPLE/_chung/SO-TAY-KY-THUAT.md` trước** (bảng chọn khuôn ở mục 2, kỹ thuật ở mục 3–6).
Quy tắc đã chốt với người dùng: tự làm trong phiên này (không giao session con); mỗi thể loại chỉ sửa file của chính nó; code dùng chung chỉ sửa khi nói rõ phạm vi.

Python của Studio: `runtime\python.exe` (có ffmpeg, Whisper, cv2, mediapipe). Trên Windows đặt `PYTHONIOENCODING=utf-8`.

## Bước 1. Phân tích bằng công cụ (không bỏ qua, không đoán từ vài ảnh)

```
runtime\python.exe SAMPLE\_chung\video-moi.py danh-gia "<video.mp4>" [--lang en|es|pt]
```
Lệnh này tự chạy `phan-tich-video.py` (lời + từ/giây + cảnh cắt + ảnh ghép) rồi đo thêm: số mặt và vị trí theo giây, chuyển động máy theo đoạn, cao độ giọng từng lượt, và in **gợi ý khuôn**. Kết quả trong `<video>-phan-tich/`: `bao-cao.md`, `danh-gia.md`, `tong-quan_N.jpg`, `luot_NN.jpg`, `chuyen-dong_NN.jpg`.

Sau đó BẮT BUỘC:
1. Mở và xem **từng** `luot_NN.jpg`, `chuyen-dong_NN.jpg`, `tong-quan_N.jpg` (dùng Read trên ảnh).
2. Điền **bảng hành động** (mỗi lượt một dòng: ai nói, từ/giây, hành động người nói, người nghe làm gì, vật dụng xuất hiện/đổi tay/biến mất, ánh mắt, camera, trạng thái KHUNG CUỐI).
3. Đối chiếu lời Whisper với phụ đề trên hình (màu phụ đề cho biết ai nói); sửa chỗ nghe nhầm.
4. Ghi ra: sản phẩm/app, phần nào là quảng cáo/end card/popup (không gen), ngôn ngữ, giọng từng người (Hz + âm sắc).

## Bước 2. Chọn khuôn và mẫu dùng lại

Đối chiếu đặc điểm video với bảng **mục 2 của SO-TAY-KY-THUAT.md**. Kết quả phải nêu rõ:
- Video **một phần hay nhiều phần**, mỗi phần dùng cơ chế gì (cảnh thường / ghép 2 lớp / lồng tiếng / không gen).
- **Mẫu dùng lại**: thư mục `SAMPLE/<mẫu>/` gần nhất (đọc `README.md`, `PROMPT-CHO-AGENT.txt`, kịch bản, biến thể, `cong-cu/` của nó). Nếu video thuộc thể loại đã có → chỉ viết biến thể mới theo `PROMPT-CHO-AGENT.txt` của thể loại đó, không tạo thể loại mới.
- Những gì **đơn giản hoá** (mục 2.2) và những gì Studio **chưa làm được**, để ghi vào bảng "video gốc → kịch bản".
- Rủi ro cần cảnh báo người dùng: hai người cùng giới cùng khung, người nói quay lưng, chữ trong hình, camera chuyển động, nhiều góc máy (cần ảnh tham chiếu mặt).

Nếu không chắc giữa hai khuôn (ví dụ cửa sổ gọi video to kiểu `xe-tai` hay ô PiP kiểu `ghep-hai-lop`), chọn khuôn an toàn hơn cho Muse (ghép 2 lớp: không bao giờ hai người cùng nói) và nói rõ lý do.

## Bước 3. Viết hồ sơ thể loại

Tạo `SAMPLE/<mã>/` (mã chữ thường không dấu, nối `-`) với:
1. `PHAN-TICH-VIDEO-MAU.md`: tổng quan (độ dài, cỡ, tốc độ nói, cảnh cắt), cấu trúc phần, bố cục/vị trí nhân vật, giọng (Hz), hiệu ứng/chữ và cách Studio làm, **bảng hành động**, **bảng "video gốc → kịch bản"**. Theo mẫu `SAMPLE/soi-hanh-ly-gia-su-ai/PHAN-TICH-VIDEO-MAU.md`.
2. Kịch bản `KICH-BAN-<MÃ>.txt`: sao từ kịch bản mẫu gần nhất rồi sửa; nhiều cảnh (≥ 8) thì viết `cong-cu/tao_kich_ban.py` sinh từ bảng cảnh (như soi hành lý) để sửa một chỗ. Áp các kỹ thuật mục 3 của sổ tay: khối khoá ngắn, câu khẳng định, một người nói mỗi cảnh, hành động trong lúc nói, khung cuối, tốc độ nói theo số đo, `NHIN_/NGHE_/QUAY_LUNG_`, `Prompt ảnh` khi đổi góc, `[GHEP HAI LOP]` đúng định dạng x,y,RỘNG,CAO, `[HAU KY] loai:` khi nhiều phần/hậu kỳ riêng.
3. Biến thể `BIEN-THE-<MÃ>.json`: sinh bằng `cong-cu/tao_bien_the.py` từ bảng (tên, ngoại hình EN, giọng EN, link ảnh, tham số). Lời thoại viết lại theo mạch video (không chép nguyên văn nếu người dùng không yêu cầu), 3–12 từ, ≤ 20; `emo` trong `EMO_CUES`; `fx`/`c`/`icon`/`phan`/`dich` theo hậu kỳ; `refs` ảnh tham chiếu cho mọi nhân vật khi có nhiều khung đầu mới hoặc ghép 2 lớp. Biến thể đầu tiên bám sát video gốc; các biến thể sau đổi đúng thứ người dùng yêu cầu (nhân vật, nền, ngôn ngữ, tuổi...).
4. Cần gen/hậu kỳ riêng (nhiều phần, phụ đề theo phần/người, đồ hoạ): `app/production/types/<mã>/gen.py` + `post.py` (vài dòng gọi `_chung/`, chép từ `soi-hanh-ly-gia-su-ai/`) + `config.json`; không sửa code của thể loại khác.
5. `README.md` (dạng video, bảng phần/cảnh/chế độ, file, cách chạy, quyết định đã chốt, còn khác video mẫu) và `PROMPT-CHO-AGENT.txt` (quy tắc riêng, lỗi hay gặp, tự kiểm tra) theo cấu trúc các thể loại đã có. Thêm dòng vào bảng thể loại của `SAMPLE/README.md`.

## Bước 4. Kiểm tra bằng code Studio

```
runtime\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\<mã>\KICH-BAN-<MÃ>.txt SAMPLE\<mã>\BIEN-THE-<MÃ>.json --tai-anh
```
Sửa cho hết LỖI; đọc từng CẢNH BÁO và quyết định (ghi lý do nếu giữ). Ngoài công cụ, tự rà: mọi dòng bảng hành động có chỗ trong `Diễn biến`/`Khung cuối`; không chữ/logo/người thật/thương hiệu người khác trong prompt; khối NGHE không nhắc tới nói/người nói; cặp cùng giới đã cảnh báo.

## Bước 5. Nhập vào Studio và chạy thử

Studio phải đang mở (`userdata/running.json` có địa chỉ). Lần đầu mỗi thể loại:
```
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\<mã>\KICH-BAN-<MÃ>.txt SAMPLE\<mã>\BIEN-THE-<MÃ>.json --ten-loai "<Tên thể loại>" --ten-du-an "<Tên dự án>" --chay-thu
```
(`--loai <id>` để dùng loại dự án đã có; bỏ `--chay-thu` nếu người dùng chỉ muốn nhập.) Lệnh tạo loại dự án, dự án (Studio tải ảnh `refs`), thêm biến thể đầu vào hàng đợi và bắt đầu.
Nhắc người dùng chọn Thương hiệu (logo cố định/bay, Video giới thiệu, Outro) trong trang dự án nếu video có badge/end card.

Sau khi cảnh đầu gen xong: xem `userdata/studio/runs/<dự án>/<biến thể>/scene1_start.png` (và `scene<n>_start.png` của cảnh đổi góc, `scene1_wide.png`, `phan2/base_<K>.png`) và clip cảnh 1; lệch thì sửa kịch bản/biến thể, "Làm lại từ cảnh N" (ghép 2 lớp: xoá `base_*`, `listen_*`, `scene*_spk` trước). Ổn rồi mới chạy cả nhóm.

## Bước 6. Giao cho người dùng

Báo cáo ngắn gồm: khuôn đã chọn và vì sao; bảng "video gốc → kịch bản" (chỗ đơn giản hoá, chỗ chưa làm được); rủi ro Muse; tên loại dự án/dự án trong Studio và biến thể đang chạy thử; việc người dùng cần làm (Thương hiệu, duyệt khung đầu). Ghi lại mọi quyết định và lần thử vào `SAMPLE/<mã>/README.md`. Phát hiện kỹ thuật mới hoặc lỗi mới → bổ sung vào `SAMPLE/_chung/SO-TAY-KY-THUAT.md` (mục 3 hoặc 6).
