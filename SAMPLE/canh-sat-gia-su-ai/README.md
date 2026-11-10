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

## Lần chạy thật đầu tiên (06/11/2026, v1 → v7) — bài học

Chạy thử biến thể `bo-con-xe-do-gia-su-ai` end-to-end, so từng cảnh với video gốc bằng `cong-cu/so_sanh.py` (8 khung gốc ↔ 8 khung gen).

| Lỗi thấy khi so | Nguyên nhân | Sửa |
|---|---|---|
| Bé ngồi sai ghế / bị vẽ ra ngoài cửa sổ ở góc A | Câu "bé luôn ngồi cạnh bố" nằm trong khoá chung, gửi cho MỌI cảnh | Bỏ khỏi khoá chung; vị trí bé chỉ ghi ở góc có bé (B, D, E, F); góc A/A2 ghi "không có trẻ em" |
| Cảnh 2 ra góc nhìn qua kính chắn gió | Ảnh bố cục chung (`anh/TOANCANH.png`) gắn vào `XE`: Muse chép nguyên khung hình | Bỏ ảnh bố cục chung khỏi `refs`; chỉ giữ 4 ảnh nhân vật (`anh/<KHOÁ>.png`, gen bằng `cong-cu/gen_anh_tham_chieu.py`) |
| Góc máy khác gốc | Kịch bản cũ dùng 4 góc chung | `cong-cu/goc_may.py`: bảng 14 shot gốc → góc A, A2, B, C, C2, D, E, F cho 12 cảnh; thêm shot không lời bố đưa giấy tờ (đầu cảnh 8), cảnh sát đi về nhìn từ trong xe (đầu cảnh 9) |
| Mặt gần người thật | Khoá phong cách yếu | STYLE LOCK: "Pixar-style 3D CARTOON exactly like the reference images", cấm mặt bán thực |
| Cảnh cận bị thêm cảnh sát/bé ở cửa sổ, máy lia lộ người khác | (1) Engine tả MỌI nhân vật "đang im lặng trong khung" (SPEAKER MAP); (2) hướng nhìn ghi "nhìn cảnh sát ở cửa sổ" | (1) `engine.py`: biến thể bật `"nguoi_theo_canh": true` → chỉ tả người có tên trong cảnh, bỏ qua dòng "Mở đầu"; (2) hướng nhìn cảnh cận chỉ tả hướng mắt; `CAMERA LOCK` cho cảnh cận và A2 |
| Cảnh cận bị lỏng khung | Ảnh tổng quan 16:9 rồi cắt giữa | Ảnh tổng quan chỉ cho góc rộng (A, A2, B) |
| Clip "mới" giống từng byte clip cũ | Muse lỗi 502, LUO-API xin "gắn file" → Muse gắn file cũ trong chat | `luo-muse-api/engine.py`: `GEN_FAILED_RE` → báo lỗi để Studio gen lại |

Đã đạt (so với gốc): cảnh 1–8. Còn khác: cảnh 4 cận vừa (gốc cận cực sát), cảnh 3/6 phía sau có thể nhiều xe cảnh sát. Cảnh 9–12 và phần 2 đang chạy.
Sửa kịch bản giữa chừng: chạy `cong-cu/goc_may.py`, chép kịch bản đè `userdata/studio/types/<loại>.txt`, xoá `phan1/scene<N>_*` từ cảnh cần làm lại, bấm chạy tiếp.

## Phản hồi người dùng sau bản v7 hoàn chỉnh (06/11/2026 chiều) và cách sửa tận gốc

| Phản hồi | Sửa |
|---|---|
| Nền đổi nhiều lần trong 1 cảnh | Engine: `start_jump` + `hold_after_jump` (bỏ cú nhảy hình 0,4-0,9 s đầu clip) |
| Cảnh "Yes" và "I wish…" thừa cảnh sát ngoài cửa phía bé | `nguoi_theo_canh` (engine) + gen lại; cảnh 9 trước đó là clip cũ nhận nhầm (LUO-API 502) |
| Cảnh bé nói "Officer, sorry…" thừa cánh tay | Góc D chỉ có bé, cấm tay người khác |
| "Tu licencia…" đảo vị trí, muốn y hệt khung "Yes" | Cảnh 7 = góc B, `Khung đầu từ cảnh: 2` |
| Đưa giấy tờ đảo vị trí; bố phải tự lấy và đưa giấy tờ | `Mở đầu khung từ cảnh: 2` + bố lấy ví ở hộc giữa đưa ra cửa sổ |
| Phụ đề "I wish…" nhanh hơn lời | Phụ đề căn từ sau đoạn "Mở đầu" (`.pre` → `scenes.json` `speech`) |
| LangLearn → Talka AI → **Aiva AI** (10/11/2026) | Lời thoại 10, 22, 24 |
| Đổi robot AI (10/11/2026) | Ảnh `anh/DAY-aiva.png` (robot tai nghe, mắt xanh, nền tím than); `NGUOI_DAY`, `NEN_DAY` tả lại theo ảnh mới. Ảnh cũ `anh/DAY.png` giữ lại |
| Phần gọi AI: ô AI che mặt bố | `[NHAN VAT HOC]` ghi đầu ở ~45%; `split.py` dò mặt `base_HOC`, gen lại / dịch xuống nếu bị ô + phụ đề che |

Cùng góc máy dùng nguyên khung đầu: 6, 8 ← 3; 7, 9 ← 2; 10 ← 5 (`cong-cu/goc_may.py` → `FROM`).

## 20 biến thể đổi người lái xe (10/11/2026)

File `BIEN-THE-20-TAI-XE.json` (sinh bằng `cong-cu/tao_bien_the_20.py`), dùng chung kịch bản `KICH-BAN-CANH-SAT-GIA-SU-AI.txt`.

| | Nam (01–10) | Nữ (11–20) |
|---|---|---|
| Mexico | 01–04 | 11–13 |
| Ấn Độ | 05–07 | 14–17 |
| Mỹ | 08–10 | 18–20 |

- Ảnh tài xế: `anh/20-tai-xe/tai-xe-XX.png` (3D, phông xanh, gen Muse bằng `cong-cu/gen_20_tai_xe.py`, người dùng duyệt `BANG-DUYET.png`); mô tả ở `danh-sach.csv`.
- Tài xế nữ: "the mother" + **nam cảnh sát** (`canh-sat-nam.png`), lời 5–6 đổi She/her. Tài xế nam: nữ cảnh sát gốc.
- Bé giống bố/mẹ: Mexico `anh/BE.png`, Ấn Độ `be-an.png` (câu cảnh 7 bằng tiếng Hindi chữ Devanagari), Mỹ da trắng `be-trang.png`, Mỹ gốc Phi `be-phi.png`.
- Tài xế Mỹ: giữ y lời gốc (vẫn "tiếng Anh kém", bé dịch tiếng Tây Ban Nha) theo ý người dùng.
- Kịch bản giờ có token giới tính (`cong-cu/gioi_tinh.py`): `CHA`, `CHA_ANH`, `CHA_CUA`, `CHA_O`, `CHA_VN`, `NET_HOC`, `CS_ANH`, `CS_CUA`, `CS_O`, `TIENG_BE`. Biến thể gốc đã được thêm các khoá này. `goc_may.py` tự bỏ/đặt lại token nên chạy lại vẫn được.
- `config.json` phụ đề đổi font sang **Nirmala UI** (có chữ Devanagari cho câu Hindi).
- `kiem-tra`: 0 lỗi (cảnh báo cặp wrong/right ở phần 2 có từ biến thể gốc). **Chưa gen video.**
