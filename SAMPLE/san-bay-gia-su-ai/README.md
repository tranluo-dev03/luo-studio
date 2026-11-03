# Thể loại `san-bay-gia-su-ai`: hỏi chuyện ở sân bay + hội thoại với gia sư AI

Video mẫu: `1410_older airport PT_003 (1).mp4` (73 giây, quảng cáo app Talka AI, phụ đề tiếng Anh + tiếng Bồ Đào Nha). Phân tích từng cảnh: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng của thể loại: `app/production/types/san-bay-gia-su-ai/` (`gen.py` gen, `post.py` hậu kỳ, `config.json`).

## Dạng video: MỘT dự án, hai phần

| Phần | Cảnh | Chế độ gen | Nội dung |
|---|---|---|---|
| 1. Tình huống quầy hải quan | 1–8 | cảnh thường: hai người chung khung, cảnh sau nối từ khung cuối cảnh trước | nhân viên (`CANBO`, quay lưng 3/4, góc qua vai) hỏi "Do you speak English?"; khách (`HOC`) trả lời, đưa vé (cảnh 5), được khen, lấy điện thoại "Here, let me show you." (cảnh 8) |
| 2. Hội thoại người dùng + AI | 9–22 | **ghép 2 lớp**: gen RIÊNG video người dùng (`HOC`, nền toàn khung 9:16) và video AI (`DAY`, robot, ô góc trên phải), rồi ghép | AI hỏi; khách nói sai "I am Mexico" → AI sửa "I am from Mexico"; hỏi đáp về giá, tính năng app |
| 3. Quảng cáo app | — | không gen | Thương hiệu của dự án: Video giới thiệu (robot + popup cài app Google Play, có giọng robot) + Outro (end card) |

Giữa phần 1 và 2: nhoè chuyển động 0,5 giây (như video mẫu). Bố cục phần 2: ô robot x 0,54, y 0, rộng 0,46, cao 0,40 (331×512 px → gen 9:16), không viền, góc vuông.

## File

| File | Dùng làm gì |
|---|---|
| `KICH-BAN-SAN-BAY-GIA-SU-AI.txt` | Kịch bản duy nhất: khối `[HAU KY] loai: san-bay-gia-su-ai` + `===== PHAN 1 =====` (khối CẢNH) + `===== PHAN 2 ... \| vao: nhoe 0.5 =====` (khối `[GHEP HAI LOP]`) |
| `BIEN-THE-SAN-BAY-GIA-SU-AI.json` | 1 biến thể, 22 lượt; mỗi lượt có `"phan"` (1/2), `"c"` (màu phụ đề), `"dich"` (dòng dịch), tuỳ chọn `"icon"`, `"fx"`, `"nhan"` |
| `PHAN-TICH-VIDEO-MAU.md` | Bảng từng cảnh, bảng hành động, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc riêng để agent viết biến thể mới |

## Chạy trong Studio

1. Tab "Loại dự án" → "Loại mới": nhập `KICH-BAN-SAN-BAY-GIA-SU-AI.txt` (Studio hiển thị "Ghép 2 lớp", số lượt tuỳ ý). Tạo dự án, nhập biến thể bằng file JSON (người nói `canbo` chỉ chọn được qua file, nút trên giao diện chỉ có Dạy/Học).
2. Thương hiệu của dự án: logo cố định + chữ "Talka AI" (badge góc trên trái), Video giới thiệu, Outro.
3. Gen: Studio thấy `[HAU KY] loai: san-bay-gia-su-ai` và có `gen.py` nên chạy code riêng: phần 1 trong thư mục con `phan1/`, phần 2 trong `phan2/`, clip từng cảnh được nối ra thư mục chạy theo số cảnh chung 1–22 (xem ảnh, "Làm lại từ cảnh N" dùng như thường), rồi ghép thành `raw.mp4` có nhoè chuyển cảnh.
4. Hậu kỳ tự chạy `post.py` riêng: phụ đề tiếng Anh (người hỏi trắng, khách vàng; phần 1 ở độ cao 1160, phần 2 ở 1330 theo khung 1080×1920), dòng dịch đỏ viền trắng, ❌ / ✅ / túi tiền $, viền đỏ/xanh nháy + tiếng ở câu sai/đúng, "with Talka AI" trên ô vàng. Sau đó Studio gắn Thương hiệu.
5. Muốn video khác (đổi app, đổi ngôn ngữ dịch): sửa biến thể; chỉnh cỡ/độ cao phụ đề, độ nhoè trong `app/production/types/san-bay-gia-su-ai/config.json`.

Trước khi chạy cả nhóm: chạy thử một biến thể, xem khung đầu cảnh 1 (`phan1/scene1_start.png`) và ảnh gốc `phan2/base_HOC.png`, `phan2/base_DAY.png`. Nên gắn ảnh mặt khách vào ô "Ngoại hình" của `HOC` để hai phần cùng một người.

## Đã kiểm tra / chưa kiểm tra

- Đã mô phỏng (thay Muse bằng clip giả): phân phần, biến thể con của từng phần (phần 1 không thấy robot, phần 2 không thấy nhân viên), prompt phần 1, số cảnh chung, làm lại từ cảnh 12 (chỉ gen lại phần 2 từ cảnh 4 của nó, ghi chú sửa chuyển đúng cảnh), ghép + nhoè, hậu kỳ riêng (xem ảnh từng hiệu ứng).
- **Chưa chạy thật trên Muse.**

## Quyết định đã chốt

- Phần 1 giữ một khung qua vai (video mẫu có thêm cận cảnh và đẩy máy): đổi cỡ cảnh giữa chừng làm Muse trôi mặt/trang phục.
- Tốc độ nói đo được: trung vị 3,5 từ/giây (câu ngắn tới 5,4).
- Câu AI "Almost. The best way is to say, I am from Mexico." tách 2 lượt để viền xanh + ✅ rơi đúng câu "I am from Mexico."
- "OK. … How? Your English is good." gộp thành "Okay. Wow, your English is good." ("How?" nhiều khả năng Whisper nghe nhầm).
- Nhân viên dùng khoá `CANBO` (không dùng `DAY`) vì `DAY` là robot ở phần 2; mỗi phần chỉ nhận token của nhân vật có mặt trong phần đó.
- Còn khác video mẫu: ô robot mép cứng (video mẫu mờ dần mép dưới); túi tiền vẽ bằng hình tròn + $, không phải emoji.
- Hướng nhìn (EYE LINE, sửa 03/11/2026): lần chạy đầu ông nhân viên quay mặt ra ngoài khung khi nói, vì kịch bản đòi "clear lip-sync" cho người đang quay lưng mà không giữ hướng nhìn của người NÓI (Studio chỉ khoá tư thế người nghe qua NGHE_*). Đã thêm luật EYE LINE vào CHAR LOCK, VIDEO SUFFIX, Prompt video từng cảnh và Prompt ảnh: hai người luôn nhìn nhau, ông nhân viên giữ góc quay lưng 3/4.
- Biến thể khai `NHIN_<khoá>` (hướng nhìn khi nói; Studio chèn vào câu lệnh người nói) và `NHIN_HOC@2` (hướng nhìn của người dùng ở phần 2: nhìn ống kính).
- Góc qua vai (sửa lần 3): "quay lưng 3/4" bị Muse vẽ thành mặt nghiêng hẳn, mắt ông nhân viên chĩa sang mép trái, lướt qua cô gái ngồi sâu trong cảnh (dù prompt ghi nhìn cô). Kịch bản giờ tả đúng như video gốc: camera ngay sau vai phải ông, thấy gáy, tai phải, gọng kính, một chút má, KHÔNG thấy mắt; mặt ông hướng vào trong cảnh; cấm vẽ nghiêng. Ông vẫn cầm hộ chiếu nhưng không nhìn vào nó.
- Lộ miệng (sửa lần 4): ảnh khung đầu đúng nhưng video vẫn xoay mặt ông nhân viên ra, vì prompt (cả hệ thống lẫn kịch bản) đòi miệng / nét mặt người nói: "coming from the mouth of", gợi ý cảm xúc "eyebrow raised, lips pressed", "expression grows", "with lip-sync", "jaw moves". Đã thêm khoá `QUAY_LUNG_CANBO` (Studio bỏ các câu đó cho người quay lưng, cả khi nói và khi nghe) và bỏ lip-sync của ông trong kịch bản.
- Phần 2, các chỗ nối (sửa 03/11/2026): cảnh 12->13 khựng mạnh (lệch 37/255) và 3 cảnh cuối lệch màu, vì `lam moi: 3` vẽ lại khung nối làm đổi tư thế và màu áo. Đã bỏ `lam moi`. Ở chế độ nối khung, mỗi clip giờ được căn khớp hình và màu về đúng khung cuối người xem vừa thấy, rồi hoà 0,2s đầu. Đo trên clip thật: chỗ nối lệch 6,7 -> 2,1. Thêm `nghe: tinh`: người nghe là ảnh tĩnh nên không thể nhép miệng.
- Người nghe đứng hình hoặc nhép miệng (sửa 03/11/2026): gốc lỗi nằm ở prompt NGHE. Prompt này chèn khối [NHAN VAT] có "while speaking… VOICE…" và câu robot "moves its lips in clear sync with the words", nên Muse cho người nghe nói theo. Studio giờ lọc các câu đó khỏi prompt nghe. Kịch bản dùng `nghe: moi canh` (mỗi cảnh 2 video nối khung); khối [NGHE] bỏ "head still", thêm phản ứng (gật đầu, nhướn mày, cười). Không dùng ảnh tĩnh, không khoá miệng.
