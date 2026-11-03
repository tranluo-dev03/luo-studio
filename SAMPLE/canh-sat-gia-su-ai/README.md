# Thể loại `canh-sat-gia-su-ai`: cảnh sát chặn xe + gia sư AI (hoạt hình 3D)

Video mẫu: `AQM2PsNIOcAQusw…pqPw.mp4` (64 giây, quảng cáo app LangLearn). Phân tích từng cảnh: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng: `app/production/types/canh-sat-gia-su-ai/` (`gen.py`, `post.py`, `config.json`), dùng chung `types/_chung/` với `san-bay-gia-su-ai`.

## Dạng video: MỘT dự án, hai phần (cùng khuôn `san-bay-gia-su-ai`)

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Cảnh sát chặn xe | 1–12 | cảnh thường, 3 nhân vật, **4 góc máy**: mỗi cảnh có `Prompt ảnh` riêng | cảnh sát (`CANHSAT`) hỏi; tài xế (`HOC`) ấp úng; con gái (`BE`) đỡ lời, dịch sang tiếng Tây Ban Nha; đưa giấy tờ; bé khoe app |
| 2. Tài xế + gia sư AI | 13–25 | **ghép 2 lớp**, bố cục giống `ghep-hai-lop`: AI (`DAY`) trong ô bo góc viền trắng phía trên (691×410 px → gen 16:9), tài xế toàn khung | 2 câu sai được sửa, hỏi giá, tải app |
| 3. End card | — | không gen | Thương hiệu → Outro (end card LangLearn có giọng "Best language learning app. Download now.") |

Giữa phần 1 và 2: nhoè chuyển động 0,5 giây.

**Khác `san-bay-gia-su-ai`:** hoạt hình 3D; phần 1 có 3 nhân vật và đổi góc máy liên tục (nên mỗi cảnh gen ảnh khung đầu riêng thay vì nối khung cuối cảnh trước); phụ đề kiểu khác (xem dưới); không có dòng dịch.
**Phần 2 dùng lại `ghep-hai-lop`:** cùng bố cục và lời thoại (mẫu `ghep-hai-lop` được làm từ chính video này), chỉ đổi tài xế thành ông bố trong xe đỏ.

## Phụ đề (hậu kỳ riêng, `config.json` → `phu_de.kieu_theo_phan`)

| Phần | Kiểu | Vị trí |
|---|---|---|
| 1 | Ô vàng, chữ đen, cho mọi người nói | y 1320 (2/3 dưới khung) |
| 2 | AI: chữ xanh ngọc trên ô đen; tài xế: chữ đen trên ô trắng | y 645 (ngay dưới ô AI) |

Thêm theo từng lượt trong biến thể: `"to"` tô màu đúng từ sai (đỏ, khi `"fx": "wrong"`) hoặc từ đúng (xanh, khi `"fx": "right"`), `"icon"` x / check / dollar, `"fx"` viền nháy + tiếng.

## File

| File | Dùng làm gì |
|---|---|
| `KICH-BAN-CANH-SAT-GIA-SU-AI.txt` | Kịch bản duy nhất: `[HAU KY] loai: canh-sat-gia-su-ai` + `===== PHAN 1 =====` (12 CẢNH) + `===== PHAN 2 … \| vao: nhoe 0.5 =====` (`[GHEP HAI LOP]`) |
| `BIEN-THE-CANH-SAT-GIA-SU-AI.json` | 1 biến thể `bo-con-xe-do-gia-su-ai`, 25 lượt, mỗi lượt có `"phan"` |
| `PHAN-TICH-VIDEO-MAU.md` | Bảng từng cảnh, góc máy, so sánh với thể loại đã có, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc riêng để agent viết biến thể mới |

## Chạy trong Studio

Giống `san-bay-gia-su-ai` (xem `SAMPLE/san-bay-gia-su-ai/README.md`):
1. Mở lại Studio nếu vừa cập nhật code. Tab "Loại dự án" → "Loại mới": nhập kịch bản, chọn luôn file biến thể JSON (người nói `canhsat`, `be` chỉ nhập được qua file).
2. **Gắn ảnh tham chiếu cho 3 nhân vật phần 1** (ô "Ngoại hình" của CANHSAT, HOC, BE): mỗi cảnh phần 1 gen ảnh khung đầu mới theo góc máy, không có ảnh tham chiếu thì mặt và trang phục dễ đổi giữa các góc. Ảnh HOC cũng dùng cho phần 2.
3. Gen → hậu kỳ tự chạy. Thương hiệu: Outro = end card.
4. Trước khi chạy hết: xem `phan1/scene1_start.png`, `phan1/scene2_start.png` (góc A, B) và `phan2/base_HOC.png`, `phan2/base_DAY.png`.

## Studio chưa làm được / khác video mẫu

- Mỗi cảnh phần 1 là một ảnh khung đầu mới: tốn 12 lượt gen ảnh, mặt nhân vật giữ được hay không phụ thuộc ảnh tham chiếu.
- Phần 1 không đo miệng người nghe (vị trí nhân vật đổi theo góc máy nên nhãn vị trí là `window-side`, `driver-seat`, `child-seat`, Studio bỏ qua đo miệng và ghi cảnh báo): nghe kỹ các cảnh hai bố con cùng trong khung (góc B).
- Bỏ cảnh rộng mở đầu và cảnh cảnh sát đi về xe (cảnh không lời).
- Ô phụ đề hình chữ nhật (video mẫu bo tròn); vòng sóng âm sau đầu AI tĩnh (video mẫu nhấp nháy).
- End card không gen (Outro).
- **Chưa chạy thật trên Muse**; đã mô phỏng luồng gen 2 phần, làm lại cảnh, hậu kỳ.
- Hướng nhìn: mỗi cảnh phần 1 có dòng "Hướng nhìn" và EYE LINE riêng trong Prompt ảnh / Prompt video (người nói nhìn người mình đang nói chuyện, không quay ra camera), thêm sau lỗi quay mặt đi ở san-bay-gia-su-ai.
- Biến thể khai `NHIN_<khoá>` (hướng nhìn khi nói; Studio chèn vào câu lệnh người nói) và `NHIN_HOC@2` (hướng nhìn của người dùng ở phần 2: nhìn ống kính).
