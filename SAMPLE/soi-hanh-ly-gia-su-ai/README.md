# Thể loại `soi-hanh-ly-gia-su-ai`: soi hành lý ở sân bay + hội thoại với gia sư AI

Video mẫu: `1510_Betterspeak check luggage EN_003_5 (online-video-cutter.com).mp4` (66,8 giây, quảng cáo app Talka AI, tiếng Anh, phụ đề tiếng Anh). Phân tích từng cảnh: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).
Code riêng: `app/production/types/soi-hanh-ly-gia-su-ai/` (`gen.py`, `post.py`, `config.json`), dùng chung `types/_chung/` với `san-bay-gia-su-ai` và `canh-sat-gia-su-ai`.

## Dạng video: MỘT dự án, hai phần (cùng khuôn `san-bay-gia-su-ai`)

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Soi hành lý | 1–13 | cảnh thường, 2 nhân vật, góc máy như video mẫu: cảnh 1 là **cú lia trong một clip** (cận nhân viên chỉ tay → máy lia theo tay qua vali → dừng ở cận người mẹ), có `Ảnh tổng quan` 16:9 + `Khung đầu cắt: trái`; 2 người mẹ trả lời, nối từ khung cuối cảnh 1; 3–7 toàn cảnh đứng yên; 8–13 cận hai người. Cảnh 3, 8 có `Prompt ảnh` riêng (kèm ảnh tổng quan), còn lại nối khung cuối | nhân viên an ninh (`CANBO`, đứng trái sau băng chuyền) hỏi về vali bị máy soi báo; người mẹ địu con (`HOC`, đứng phải) mở vali, được khen tiếng Anh, giơ điện thoại khoe gia sư AI (cảnh 10), "Let me show you how it works" (cảnh 13) |
| 2. Người mẹ + gia sư AI | 14–28 | **ghép 2 lớp**: người mẹ quay selfie (nền 9:16), robot AI (`DAY`) ở ô bo góc góc trên phải | "I have 48" (❌ viền đỏ) → AI sửa → "I am 48" (✅ viền xanh); hỏi giá, "free", "unlimited… anytime, anywhere" |
| 3. | — | không gen | Video mẫu không có end card. Badge "Talka AI" góc trên trái: Thương hiệu → logo cố định; muốn có end card: Thương hiệu → Outro |

Giữa phần 1 và 2: nhoè chuyển động 0,5 giây. Bố cục phần 2: ô robot x 0,62, y 0,06, rộng 0,30, cao 0,27 (324×518 px → gen 9:16), bo góc 0,03, không viền.

**Khác `san-bay-gia-su-ai`:**
- Phần 1 đổi góc máy như video mẫu (có một cú lia máy ở cảnh 1) thay vì giữ một khung qua vai; cả hai nhân vật đều thấy mặt (nghiêng 3/4), nhân viên đứng.
- Mỗi cảnh phần 1 ghi hành động của **cả hai** người theo từng nhịp (người nghe nhìn theo tay người nói tới đúng vật), chỉ tay chính xác vào nắp vali.
- Có em bé ngủ trong địu (token `DAO_BE`) và hai vali trên băng chuyền (`DAO_VALI`, `DAO_VALI_2`).
- Phụ đề: không có dòng dịch; phần 1 mọi người chữ trắng viền đen, phần 2 AI chữ vàng / người mẹ chữ trắng, cùng độ cao 1125.
- ✅ + viền xanh đặt ở lượt **người mẹ nói lại câu đúng** (như video mẫu), không ở lượt AI.
- Phần 2 người dùng quay selfie (tay duỗi từ góc dưới trái), không ngồi sau quầy.

**Không cần code mới:** `gen.py`, `post.py` chỉ gọi `_chung/nhieu_phan.py` và `_chung/hau_ky.py`; khác nhau ở `config.json`.

## File

| File | Dùng làm gì |
|---|---|
| `KICH-BAN-SOI-HANH-LY-GIA-SU-AI.txt` | Kịch bản: `[HAU KY] loai: soi-hanh-ly-gia-su-ai` + `===== PHAN 1 =====` (13 CẢNH) + `===== PHAN 2 ... \| vao: nhoe 0.5 =====` (`[GHEP HAI LOP]`) |
| `BIEN-THE-SOI-HANH-LY-GIA-SU-AI.json` | 2 biến thể (cùng lời, khác nhân vật/đồ vật), 28 lượt; mỗi lượt có `"phan"`, `"c"`, `"fx"`, tuỳ chọn `"icon"` |
| `cong-cu/tao_kich_ban.py` | Sinh lại kịch bản từ bảng 13 cảnh (góc máy, hành động, EYE LINE từng cảnh). Sửa ở đây rồi chạy, không sửa tay file `.txt` |
| `KICH-BAN-SOI-HANH-LY-GIA-SU-AI-KHONG-BE.txt` | Bản kịch bản KHÔNG em bé (hành khách nam hoặc nữ, tay đặt lên quai túi; đại từ thành token `HE_HOC`, `HE_HOC_C`, `HIS_HOC`, `HIM_HOC`, `HIMSELF_HOC`). Sinh bằng `cong-cu/tao_kich_ban.py --khong-be`, không sửa tay |
| `BIEN-THE-SOI-HANH-LY-20-KHONG-BE.json` | Bộ "20 biến thể Check luggage" (05/11/2026), biến thể 1-15 (5 nam, 10 nữ, không địu con): dùng với kịch bản KHONG-BE |
| `BIEN-THE-SOI-HANH-LY-20-DIU-CON.json` | Biến thể 16-20 (người mẹ địu con): dùng với kịch bản có em bé |
| `cong-cu/tao_bien_the_20.py` | Sinh 2 file trên từ bảng: chỉ đổi hành khách + giọng, tuổi trong câu "I have / I am", câu "visiting my ..." hợp tuổi; ảnh tham chiếu `NGUOI_HOC` = link prnt.sc từng biến thể, `NGUOI_DAY` = `ROBOT-GIA-SU-AI.png` |
| `PHAN-TICH-VIDEO-MAU.md` | Bảng từng cảnh, bố cục/vị trí, hiệu ứng, bảng lượt thoại + hành động, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc riêng để agent viết biến thể mới |

## Chạy trong Studio

1. Tab "Loại dự án" → "Loại mới": nhập `KICH-BAN-SOI-HANH-LY-GIA-SU-AI.txt`. Tạo dự án, nhập biến thể bằng file JSON. Ở tab biến thể, người nói mỗi lượt là ô chọn Dạy / mother / officer; nhân viên có thẻ riêng "Nhân vật officer (CANBO)", mỗi nhân vật có ô "Hướng nhìn khi nói".
2. **Gắn ảnh tham chiếu mặt** cho `NGUOI_CANBO` và `NGUOI_HOC` (4 cảnh gen ảnh khung đầu mới ở phần 1 + ảnh gốc phần 2: không có ảnh tham chiếu thì mặt dễ lệch giữa các góc).
3. Thương hiệu của dự án: logo cố định "Talka AI" (góc trên trái); Outro nếu muốn.
4. Gen: Studio thấy `[HAU KY]` nên chạy `gen.py` riêng: phần 1 trong `phan1/`, phần 2 trong `phan2/`, clip nối ra thư mục chạy theo số cảnh chung 1–28, ghép `raw.mp4` có nhoè chuyển cảnh. Hậu kỳ tự chạy `post.py`.
5. Chạy thử MỘT biến thể trước; xem `phan1/scene1_start.png`, `scene2_start.png`, `scene3_start.png`, `scene8_start.png`, clip cảnh 1 (ngón tay có chỉ đúng vali không, khung có đứng yên không) và `phan2/base_HOC.png`, `phan2/base_DAY.png` trước khi chạy cả nhóm.

## Đã kiểm tra / chưa kiểm tra

- Script kiểm tra (code Studio thật): token kịch bản = khoá biến thể; `nhieu_phan.plan` ra 2 phần, 13 + 15 = 28 cảnh; điền token từng phần không còn `{{`; phần 1 nhận đúng `CANBO`/`HOC`, phần 2 `DAY`/`HOC` và `NHIN_HOC@2`; `split.parse` ra ô robot đúng, gen 9:16; cảm xúc đều có trong `EMO_CUES`; độ dài prompt video (1.270–1.430 từ) ngang `san-bay`/`canh-sat`.
- Mô phỏng cả luồng qua `engine.run_variant` với Muse giả (ảnh/clip testsrc, giọng Windows đọc đúng câu trong prompt), 03/11/2026: Studio tự chọn `gen.py` riêng; 28/28 cảnh xong (phần 1 trong `phan1/`, phần 2 trong `phan2/`, nối ra số cảnh chung); 6 lệnh gen ảnh đúng dự kiến (bản trước có khung đầu cảnh 1, 2, 3, 8 + ảnh gốc HOC, DAY; bản có cú lia: xem mục dưới); `raw.mp4` có nhoè ở chỗ vào phần 2; `post.py` căn 34 dòng phụ đề đúng màu theo phần/người nói, viền đỏ nháy + ❌ ở "I have 48.", viền xanh + ✅ ở "I am 48."; ô robot bo góc không viền đúng vị trí (đã xem ảnh khung hình).
- Ghi nhận từ mô phỏng: ảnh khung đầu cảnh 3 (toàn cảnh) **không** được gửi kèm khung của cảnh 1/2 (Studio chỉ gửi khung cuối cảnh trước khi cùng nhân vật, mà cảnh 2 chỉ có người mẹ), nên độ khớp giữa cảnh 1 và 3 chỉ dựa vào ảnh tham chiếu gắn trong biến thể. Cảnh 8 thì có gửi khung cuối cảnh 7 (để khớp màu/ánh sáng).
- Mô phỏng lại sau bản cải tiến (camera, tương tác, giọng), 03/11/2026: 28/28 cảnh; cảnh 1 cắt ở 1,6 s (hết lời 1,1 s + 0,5 s `Giữ sau lời`); cú lia sang phải ở 1,6 s (điểm nối cảnh 1→2, đã xem khung hình: phóng to, trượt ngang, nhoè); nhoè vào phần 2 vẫn đúng. Câu phản ứng của người nghe ("eyes drop to the phone screen", "eyes follow her hands"...) còn nguyên sau các bước lọc prompt của Studio.
- **Chưa chạy thật trên Muse.**

## Lỗi từ lần chạy thật và cách đã sửa

- **03/11/2026, cảnh 1: nhân viên chỉ ngang sang phải vào em bé thay vì chỉ xuống vali.** Nguyên nhân: kịch bản cho ông "vừa chỉ vừa liếc sang người mẹ ngoài khung bên phải", ảnh khung đầu để tay ông buông nên Muse tự chọn hướng chỉ, và tay người mẹ ló ở mép phải. Đã sửa:
  - ảnh khung đầu cảnh 1 đã ở sẵn tư thế chỉ: tay phải chĩa XUỐNG, ngón trỏ ngay trên giữa nắp vali; vali ở giữa-dưới khung, ngay dưới tay ông; mép phải khung trống (không người, không tay, không em bé);
  - ông nhìn vali suốt câu (không liếc sang người mẹ); trong clip chỉ ấn nhẹ ngón tay xuống ở chữ "bag";
  - mô tả chỉ tay dùng chung (cảnh 1, 3): "points DOWN … never sideways, never level with the chest, never toward the edge of the frame, the mother or the baby"; NEGATIVE thêm "pointing at the baby, the mother or any person";
  - bỏ cụm "the baby asleep" khỏi cảnh chỉ có nhân viên (kẻo Muse vẽ thêm em bé).
  Làm lại: "Làm lại từ cảnh 1" (Studio xoá cả ảnh khung đầu cũ và đọc kịch bản mới khi chạy).
- **03/11/2026, lần 2: ảnh khung đầu đã đúng (ngón tay trên nắp vali) nhưng trong clip máy LIA SANG PHẢI** thay vì nghiêng xuống: mẹ con lọt vào mép phải, vali trôi khỏi chỗ ngón tay, cuối clip trông như chỉ vào em bé. Muse hiểu "camera tilts down along his arm" thành đi theo hướng tay/hướng người kia. Đã sửa: bỏ hẳn chuyển động máy ở cảnh 1 (LOCKED CAMERA: không lia, không nghiêng, không zoom; khung giữ như ảnh đầu, vali luôn dưới ngón tay, mẹ con không vào khung), bỏ `Giữ sau lời`; khoá chung đổi thành camera đứng yên ở mọi cảnh. Cú lia sang người mẹ chỉ còn do `Chuyển cảnh: lia phải 0.36` (ffmpeg) làm.
  **Bài học:** không giao chuyển động máy cho Muse khi cảnh có người ngoài khung; chuyển động giữa hai người làm bằng chuyển cảnh khi ghép.
- **03/11/2026, lần 3 (user yêu cầu): cú lia làm lại thành MỘT cảnh có ảnh tổng quan.** Đo lại video mẫu 15 khung/giây (0,5–1,7 s): cắt sang cận nhân viên ở 0,63 s, máy trôi theo cánh tay sang phải-xuống (chậm rồi nhanh), vụt qua máy soi và vali (nhoè ngang, 0,85–1,05 s), chậm lại và dừng ở cận người mẹ (~1,25 s); câu "Is this your bag?" nằm trọn trong cú lia. Lần 2 hỏng vì Muse không biết người mẹ và vali ở đâu nên tự bịa. Nay:
  - cảnh 1 có `Ảnh tổng quan` (ảnh ngang 16:9: nhân viên ở 30% trái, vali giữa, người mẹ ở 30% phải) + `Khung đầu cắt: trái`: khung đầu là phần trái ảnh đó (ngón tay chĩa ra mép phải dưới về vali ngoài khung); ảnh ngang gửi kèm bước gen video; khối `CAMERA MOVE` tả cú lia theo từng chữ; `Giữ sau lời: 1.2`; bỏ `Chuyển cảnh: lia phải`;
  - cảnh 2 (người mẹ trả lời) nối từ khung cuối cảnh 1 (đã là cận người mẹ), không gen ảnh mới;
  - cảnh 3 và 8 (khung đầu mới) được gửi kèm ảnh tổng quan để giữ cùng bối cảnh, đạo cụ, quần áo;
  - khoá chung: camera đứng yên trừ cảnh có `CAMERA MOVE`;
  - tương tác chi tiết theo video mẫu: cảnh 3 cuối câu người mẹ đã đưa tay về phía vali, tay trái nhân viên trên nóc máy soi; cảnh 7 ngửa MỘT bàn tay khen; cảnh 8 "Thank you" hai tay trên lưng bé rồi tay phải ngửa ra khi kể; cảnh 12 nhân viên liếc điện thoại, tay phải ngửa thấp; cảnh 13 xoay điện thoại về mình ở "it's free", chạm màn hình ở "Let me show you", nhân viên nghiêng lại nhìn, nửa giây cuối máy đẩy nhẹ vào.
  Rủi ro còn lại: Muse có thể lia chậm hơn (cảnh 1 bị cắt khi máy chưa tới người mẹ → tăng `Giữ sau lời`), hoặc vẽ người mẹ khác ảnh tổng quan. Kiểm tra `phan1/scene1_wide.png` (đủ 3 vùng trái/giữa/phải, mặt đúng tham chiếu) và `scene1_start.png` trước khi chờ cả video.
- **03/11/2026, lần 4 (sau lần chạy thật 15:08): nhân viên chỉ nhầm vào em bé, cú lia nhẹ, giọng chưa thật.** Ảnh tổng quan và khung đầu đúng, nhưng khi máy lia ông nhấc tay ngang ngực chĩa theo hướng máy, cuối cú lia ngón tay dừng trước em bé; máy trôi đều ~2 s. Nguyên nhân: "keeps pointing" + "camera follows his pointing arm". Đã sửa:
  - ảnh tổng quan: vali nằm ngay dưới tay ông TRONG phần trái (khung đầu thấy luôn vali), chỉ MỘT vali xanh; trong câu nói ông chỉ dốc xuống vali, tay không nhấc, không chĩa ngang, không đi theo máy; nói xong hạ tay về hông, RỒI máy mới vụt sang người mẹ; tay ông không lọt vào khung người mẹ;
  - `Giữ sau lời: 2.5` + trường mới `Lia nhanh: 3` (engine `whip_speedup`: dò đoạn lia sau từ cuối, tua nhanh 3 lần + nhoè ngang). Thử trên clip 15:08: đoạn lia sau lời 1,33–3,42 s còn 0,69 s, lời nói giữ nguyên;
  - giọng: `GIONG_CANBO`/`GIONG_HOC` (biến thể mẫu + dự án Du-an-moi-dc18, cả 2 biến thể) viết lại theo người thật (cao độ đo trên video mẫu, câu kể hạ giọng cuối, câu hỏi yes/no lên giọng, giọng Mexico/Ấn tự nhiên không cường điệu); VIDEO SUFFIX thêm "real people caught on camera, not actors"; mỗi cảnh có dòng `DELIVERY` riêng (bảng `DELIV` trong `cong-cu/tao_kich_ban.py`); lượt 1 đổi `emo` thành "routine, calm".
- **03/11/2026, lần 5 (user: cú lia sang người mẹ đã ổn; máy phải lia THEO TAY khi ông giơ tay chỉ; trước câu hỏi có cảnh hành lý trôi ra).** Đã sửa cảnh 1:
  - ảnh tổng quan: ông tay buông, nhìn xuống vali vừa trôi ra ở phía trước-bên phải (25–50% chiều ngang), người mẹ ở 30% bên phải; khung đầu (cắt trái) là ông tay buông;
  - `CAMERA MOVES`: trong câu nói ông giơ tay chỉ dốc xuống vali, máy đi CÙNG cánh tay tới đầu ngón tay và vali (tốc độ thường), ngón tay luôn chĩa vào nắp vali, tay dừng khi đã chỉ trúng; nói xong hạ tay, rồi máy vụt sang người mẹ (`Lia nhanh: 3` chỉ tua đoạn sau lời này);
  - đoạn mở đầu không lời (trường mới `Mở đầu ảnh` / `Mở đầu video` / `Mở đầu dài: 1.5`, engine `prepend_preroll`): cận đầu ra máy soi, vali xanh trôi ra qua rèm cao su rồi dừng, ghép cắt cứng trước câu hỏi. Không thêm lượt thoại, nên số cảnh và lượt giữ nguyên 13.
  Rủi ro: khi máy đi theo tay, Muse có thể lại để tay đi theo máy về phía mẹ con (lần 4); nếu thấy vậy, xem `phan1/scene1_clip.mp4` 0–2 s và báo.
- **03/11/2026, lần 6 (sau lần chạy 15:43; user gửi ảnh cảnh đầu video mẫu).** Lỗi: đoạn mở đầu có tấm rèm dải đen khổng lồ treo ngang mép trên khung; bố cục và góc máy khác video mẫu; máy đứng yên khi ông giơ tay; tay ông duỗi ngang về phía mẹ con nên trông như chỉ vào em bé. Đã sửa:
  - đoạn mở đầu = TOÀN CẢNH góc A như ảnh mẫu (nhân viên trái, máy soi giữa, vali nâu tiền cảnh, người mẹ phải), vali xanh lăn ra khỏi hầm máy soi, cả hai cùng nhìn theo, chưa ai chỉ; rèm chỉ nằm trong miệng hầm, cấm mọi thứ treo ngang trên; `Mở đầu dài: 1.2`;
  - cận nhân viên: máy thấp và gần ở phía trước-bên phải ông, từ eo trở lên; vali nằm THẤP ngay trước mặt ông (gần máy quay), ông chỉ dốc xuống về phía máy quay, không duỗi ngang; người mẹ đứng xa hơn bên kia băng chuyền;
  - trường mới `Lia theo tay: 1.0` (engine `follow_push`): 1 giây máy đẩy vào và trôi xuống-phải theo tay tới vali trước cú vụt. Thử trên clip 15:43: máy đẩy vào theo tay ông tới vali rồi mới vụt sang người mẹ.

- **03/11/2026, góp ý sau video "hộ chiếu" (cùng khuôn):** phần ghép 2 lớp bị khựng ở mỗi chỗ nối (mọi clip bắt đầu lại từ ảnh gốc nên tư thế nhảy), ô robot che mặt khi người dùng nghiêng sang phải, giọng nói lặp từ ("10 -10", "what I'm here for, what I'm here for"). Đã sửa trong code chung: nối khung (`noi: lien`), kiểm tra lời nói tự gen lại, dòng dịch theo câu; ô robot đo lại bằng `SAMPLE/_chung/do-vi-tri-dau.py` trên phần 2 của video mẫu: `khung DAY: 0.788, 0.025, 0.187, 0.17` (nhỏ hơn, sát góc). Sau lần chạy thật đầu tiên nên đo lại trên `phan2/` của lần chạy và chỉnh nếu cần.

- **03/11/2026, video "hộ chiếu" chạy kiểu nối khung:** (1) ô robot 0,20 x 0,18 quá bé; (2) người dùng hé môi như đang nói trong lúc AI nói, dù hai người gen riêng.
  Lý do (2): gen riêng chỉ chặn được TIẾNG người kia; clip "đang nghe" vẫn do Muse dựng một người sống động, Muse hay cho môi mấp máy khi nhân vật liếc đi hay cười.
  Đo được mức 0,025 (người im thật 0,008-0,019) nhưng ngưỡng cũ 0,029 nên lọt. Đã sửa (split.py): đo đúng đoạn được dùng, ngưỡng clip nghe 0,020, gen lại tối đa 2 lần
  kèm yêu cầu giữ đầu yên/môi mím, giữ bản ít cử động nhất; prompt nghe thêm "môi hé ở khung đầu thì khép ngay"; bỏ "thỉnh thoảng liếc lên sang phải" khỏi [NGHE HOC] của sân bay.
  Ô robot đo lại với `--noi-ngang 0.15` (chỉ tránh MẶT): sân bay `0.669, 0.025, 0.306, 0.278`, soi hành lý `0.691, 0.025, 0.284, 0.258` (đo trên người mẹ gen thật).

## Code chung đã sửa cho thể loại này (chưa commit)

- `app/production/gen_video.py`: thêm `Giữ sau lời` vào danh sách trường của cảnh (không đưa vào prompt).
- `app/luo-studio/engine.py` (chỗ gọi `smart_cut`): cảnh có `Giữ sau lời: N` thì cửa sổ cắt dời ra sau từ cuối N giây (tối đa 4), vẫn chọn khung yên nhất ngay sau đó. Cảnh không có trường này cắt như cũ.
- `gen_video.py` + `engine.py`: trường `Ảnh tổng quan` / `Khung đầu cắt` (ảnh ngang 16:9 cả bố cục, cắt khung đầu, gửi kèm bước gen video và các khung đầu sau). Xem `SAMPLE/_chung/HUONG-DAN-CHO-AGENT.md`.
- Dùng lại (không sửa): `Chuyển cảnh: lia phải|trái <giây>` trong `types/_chung/nhieu_phan.py` (chỉ chạy ở thể loại nhiều phần có `gen.py` riêng).

## Quyết định đã chốt

- Camera (đo bằng OpenCV trên video mẫu): chỉ đoạn mở đầu có chuyển động; toàn cảnh đứng yên tuyệt đối; cận hai người chỉ rung vài px. Video mẫu cũng cắt ngay giữa cú lia (0,97 s), nên làm giống vậy: cảnh 1 (cận nhân viên) và cảnh 2 (cận người mẹ) mỗi cảnh một ảnh riêng, nối bằng `Chuyển cảnh: lia phải 0.36` (ffmpeg, `types/_chung/nhieu_phan.whip_pan` do phiên kịch bản sân bay viết: phóng 1,4 lần, khung cũ trượt ra, khung mới trượt vào, nhoè ngang). Cách này chắc chắn hơn để Muse tự lia rồi tự dựng mặt người mẹ.
- Cảnh 1 ban đầu có thêm cú nghiêng máy theo tay (Muse) và trường `Giữ sau lời: 0.5`; đã bỏ sau lần chạy thật thứ hai (xem "Lỗi từ lần chạy thật"). Trường `Giữ sau lời` vẫn còn trong Studio cho thể loại khác dùng.
- Giọng theo số đo cao độ: nhân viên nam trầm ~140 Hz kiểu làm việc thường ngày; người mẹ ~210 Hz giọng Latin; AI cao, sáng hơn người mẹ. Phần 1 có độ vang tự nhiên của sảnh lớn, phần 2 sạch như cuộc gọi video.
- Tốc độ nói: phần 1 "about 4.5 to 5 words per second (short lines up to 6)", phần 2 "about 3.5 (up to 4.5)" (đo: trung vị 4,55 cả video; phần 1 nhanh hơn hẳn phần 2).
- Lượt 10 và 11 (người mẹ nói 2 câu liền, 26 từ) tách 2 cảnh: một clip không đủ.
- "Nope, I'm serious." thuộc AI (phụ đề vàng), gộp với câu "unlimited… anytime, anywhere" (17 từ).
- Câu cuối dùng "Yes, really. You'll speak like a native in no time." (Whisper nghe nhầm "I'm like a native").
- Hướng nhìn (bài học từ lỗi quay mặt ra ngoài khung): khai `NHIN_CANBO`, `NHIN_HOC`, `NHIN_HOC@2`, `NHIN_DAY` ngay từ đầu; mỗi cảnh phần 1 có EYE LINE riêng trong `Prompt ảnh` và `Prompt video`; CHAR LOCK cấm người nói quay mặt ra camera/ra ngoài khung.
- Màn hình điện thoại (cảnh 10–13) mô tả là chân dung hoạt hình không chữ, như video mẫu; nếu Muse vẽ chữ/giao diện thì đổi `DAO_DIEN_THOAI` thành màn hình tối.

## Còn khác video mẫu (Studio chưa làm được)

- Phụ đề hiện cả câu, chữ thường; video mẫu chữ IN HOA, cụm 1–3 từ hiện lần lượt.
- ❌/✅ đặt bên phải dòng phụ đề; video mẫu đặt bên dưới.
- Cú lia máy giao cho Muse làm trong một clip: tốc độ và điểm dừng không chính xác như video mẫu. Không có khoảnh khắc ô AI thoáng hiện cô gái tóc đỏ ở đầu phần 2.
- Video bắt đầu thẳng ở cận nhân viên (bỏ 0,5 giây toàn cảnh đầu tiên của video mẫu).
- Cảnh 2 (cận người mẹ một mình): Studio vẫn lập SPEAKER MAP cho cả nhân viên (không có trong khung) và đo miệng vùng bên trái; kịch bản ghi rõ nhân viên ngoài khung. Cùng tình trạng với các góc cận của `canh-sat-gia-su-ai`.
