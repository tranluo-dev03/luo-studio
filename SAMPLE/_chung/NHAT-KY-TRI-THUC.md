# Nhật ký tri thức: mỗi lượt gen / mỗi lần sửa một thể loại

Mục đích: giữ lại MỌI điều học được khi đưa một video mới vào Studio, để định kỳ **chưng cất** thành `SO-TAY-KY-THUAT.md`
(mục 3 kỹ thuật, mục 6 lỗi) và skill `luo-video-moi` (`.claude/skills/luo-video-moi/SKILL.md`).
Nhật ký là dữ liệu thô; sổ tay và skill là bản đã kiểm chứng.

## Khi nào ghi (bắt buộc)
1. **Sau mỗi lượt gen** (chạy thử một biến thể, gen lại từ cảnh N, chạy cả nhóm): một mục, kể cả khi mọi thứ ĐẠT. Kết quả đạt cũng là tri thức (xác nhận kỹ thuật dùng được).
2. **Sau mỗi lần sửa** kịch bản / biến thể / ảnh tham chiếu / code của thể loại: một mục ghi sửa gì, vì sao, và kết quả lượt gen kế tiếp (cập nhật trạng thái mục cũ).
3. **Khi phát hiện công cụ sai hoặc thiếu** (`video-moi.py`, `phan-tich-video.py`, Studio API...): một mục loại `cong-cu`.

Ghi ngay lúc đó, không dồn cuối phiên. Mục mới thêm vào CUỐI file.

## Mẫu một mục
```
### <YYYY-MM-DD> · <mã thể loại> · <lượt/lần sửa> · <loai: phan-tich | kich-ban | anh-tham-chieu | muse | hau-ky | cong-cu | studio>
- Hiện tượng: <thấy gì, ở file nào (scene3_last.png, phan2/base_DAY.png...), số đo nếu có>
- Nguyên nhân (giả thuyết hoặc đã chứng minh): <...>
- Cách làm / sửa: <thay đổi cụ thể: câu prompt, tham số, ảnh, lệnh>
- Kết quả: ĐẠT | CHƯA ĐẠT | CHỜ KIỂM CHỨNG (<lượt gen nào xác nhận>)
- Áp dụng chung?: CÓ (mọi thể loại / mọi ghép 2 lớp / ...) | KHÔNG (riêng thể loại này)
- Đã chưng cất vào: <SO-TAY mục x.y | SKILL bước n | chưa>
```

## Chưng cất (định kỳ hoặc khi người dùng yêu cầu)
- Mục `Kết quả: ĐẠT` + `Áp dụng chung: CÓ` → đưa vào `SO-TAY-KY-THUAT.md` (kỹ thuật → mục 3; lỗi → bảng mục 6), ghi số mục vào dòng "Đã chưng cất vào".
- Quy tắc quy trình (thứ tự bước, việc bắt buộc kiểm tra) → `SKILL.md`.
- Cùng một hiện tượng xuất hiện ≥ 2 thể loại → ưu tiên chưng cất, hoặc viết thành kiểm tra tự động trong `video-moi.py kiem-tra`.
- Mục `CHƯA ĐẠT` không chưng cất thành kỹ thuật; nếu đã biết nguyên nhân thì vào bảng lỗi mục 6 với cách sửa "chưa có".

---

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · phân tích · loai: phan-tich
- Hiện tượng: `danh-gia --lang es` chỉ ra 6 câu; Whisper bỏ trọn đoạn 7,6–22,9 s (câu tiếng Anh xen tiếng Tây Ban Nha), bảng báo "lặng 15,6 s".
- Nguyên nhân: ép một ngôn ngữ cho video song ngữ; Whisper bỏ đoạn không khớp ngôn ngữ.
- Cách làm: chạy thêm `language="en"` trên `audio.wav`, ghép hai bản theo giây, đối chiếu phụ đề trên hình (`tong-quan_N.jpg`) để sửa lời.
- Kết quả: ĐẠT (đủ 12 lượt, khớp phụ đề).
- Áp dụng chung?: CÓ: thấy khoảng lặng dài bất thường giữa video có người nói → nghi song ngữ, chạy lại ngôn ngữ thứ hai.
- Đã chưng cất vào: SO-TAY mục 1 (giới hạn đã biết).

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · phân tích · loai: phan-tich
- Hiện tượng: cao độ gom tự động gán sai người (AI 147–216 Hz, Carla 180–225 Hz, hai cụm lẫn nhau).
- Cách làm: đo lại `pitch_per_turn` theo mốc lượt đã sửa và người nói lấy từ MÀU PHỤ ĐỀ (Carla xanh/trắng, AI vàng).
- Kết quả: ĐẠT. Áp dụng chung?: CÓ (hai giọng cùng giới: không tin cụm tự động). Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · ảnh tham chiếu · loai: anh-tham-chieu
- Hiện tượng: video mẫu có logo, phụ đề cứng, chữ "AI" trên trán robot ở mọi khung.
- Cách làm: cắt khung từ video mẫu làm `refs`, xoá logo/phụ đề/chữ bằng `cv2.inpaint` (vùng chữ nhật), cắt phần dưới dải phụ đề cho phần 1.
- Kết quả: ĐẠT ở phần 1 (`scene1_start.png` khớp bố cục, không chữ). Áp dụng chung?: CÓ. Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · lượt gen 1 (cảnh 1–3) · loai: muse
- Hiện tượng: phần 1 (cảnh thường, robot + người nữ chung khung) đạt: đúng lời Tây Ban Nha, robot im khi Carla nói; cảnh 3 Carla quay sang robot đúng mẫu.
  Lệch nhỏ: cuối cảnh 1 Carla xoay mặt chính diện hơn; cảnh 2 có một khung Carla tròn môi khi robot nói.
- Cách làm: khung đầu bằng `Prompt ảnh` + refs cắt từ video mẫu; `POS_HOC@1/NHIN_HOC@1/NGHE_HOC@1` ghi đè riêng phần 1.
- Kết quả: ĐẠT. Áp dụng chung?: CÓ (refs cắt từ chính video mẫu cho khung đầu rất sát bản gốc). Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · lượt gen 1 → sửa 1, sửa 2 · loai: anh-tham-chieu
- Hiện tượng: chia đôi dọc, `phan2/base_DAY.png` là cận mặt robot: đầu + tai nghe chiếm ~100% bề ngang → sau khi Studio cắt dải giữa (nửa bề ngang) mất hai tai nghe và đỉnh đầu.
  Sửa 1 (chỉ đổi chữ trong `[NHAN VAT DAY]`: "head including ear cups only about HALF of the frame width", NEGATIVE "extreme close-up") → base mới VẪN cận mặt y hệt.
- Nguyên nhân: ảnh tham chiếu `robot-goi-video.png` cắt sát đầu; Muse lấy cỡ/bố cục theo ảnh tham chiếu hơn là theo chữ.
- Cách sửa 2: ảnh tham chiếu mới `robot-goi-video-khung.png` = nửa khung video gốc (360×1280) đặt giữa canvas 9:16 (720×1280), hai bên nền chuyển màu, mép hoà 40 px
  → robot chiếm đúng nửa giữa, đúng tỉ lệ dải mà Studio sẽ cắt.
- Kiểm tra nhanh trước khi chạy tiếp: mô phỏng cắt dải giữa `ffmpeg -i base_DAY.png -i base_HOC.png -filter_complex "[0]crop=iw/2:ih:iw/4:0[a];[1]crop=iw/2:ih:iw/4:0[b];[a][b]hstack"`.
- Kết quả: CHƯA ĐẠT ở lượt gen 2 (base_DAY vẫn hơi to, clip robot lại thu nhỏ cả thân và dính vết inpaint, xem mục dưới); chờ lượt gen 3.
- Áp dụng chung?: CÓ (mọi ghép 2 lớp có ô hẹp hơn 9:16: ảnh tham chiếu phải cùng bố cục với ô, không cắt sát mặt). Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · lượt gen 1 · loai: muse
- Hiện tượng: `phan2/base_HOC.png` có thêm một robot đồ chơi trên sofa (ngoài dải giữa nên bị cắt bỏ).
- Nguyên nhân (giả thuyết): ngữ cảnh "video call with the AI tutor" + ảnh robot gửi kèm.
- Cách sửa: NEGATIVE phần 2 thêm "a toy robot, figurine or any robot in the living room".
- Kết quả: CHỜ KIỂM CHỨNG. Áp dụng chung?: CÓ (ghép 2 lớp có robot). Đã chưng cất vào: chưa.

### 2026-11-05 · (chung) · studio · loai: cong-cu
- Bản cài không có `runtime\`: dùng `.venv\Scripts\python.exe`, ffmpeg ở `bin\` (thêm `bin` vào PATH khi gọi công cụ).
- Sửa kịch bản khi dự án đã nhập: `PUT /api/types/<id>` (giữ `fields/turns/defaults`); Studio đọc kịch bản từ loại dự án lúc chạy.
  Đổi ảnh tham chiếu: `PUT /api/projects/<id>` với `variants[].refs` (Studio tải lại). Dừng: `POST /api/stop {"ids": [...]}`. Gen lại: `POST /api/queue/redo {"id", "from": N}` (xoá `scene>=N_*` ở thư mục chạy; ghép 2 lớp phải tự xoá `phan<k>/base_<K>.png`, `scene*_spk*`, `scene*_listen_*`).
- Kết quả: ĐẠT. Áp dụng chung?: CÓ. Đã chưng cất vào: chưa (nên thêm lệnh `video-moi.py cap-nhat` / `lam-lai`).

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · lượt gen 2 (từ cảnh 4) → sửa 3 · loai: anh-tham-chieu
- Hiện tượng: clip robot phần 2 (`phan2/scene1_spk.mp4`) có một mảng xám nhoè ở cổ/vai phải robot; người dùng tưởng là "kỹ thuật đè hình" (`lam moi`).
  Thật ra `lam moi` đã tắt (split.py bỏ qua, log cảnh báo); `base_DAY.png` sạch.
- Nguyên nhân (đã chứng minh): ảnh tham chiếu `robot-goi-video-khung.png` có vết `cv2.inpaint` (TELEA) ở chỗ xoá phụ đề trên vùng có chi tiết (cổ cáp đen + giáp trắng);
  Studio gửi ảnh tham chiếu kèm MỌI clip nên Muse chép lại vết đó vào video.
- Cách sửa: vùng có chi tiết → lấp bằng ẢNH GƯƠNG nửa đối xứng của nhân vật (trục giữa thân), hoà mép Gaussian 6 px; inpaint chỉ dùng cho nền phẳng (logo trên nền tối, chữ trên trán/ngực trơn).
  Xoá `phan2/base_DAY.png`, `phan2/scene*`, gen lại từ cảnh 4. Lưu ý: đổi `refs` phải gửi lại dạng CHUỖI đường dẫn thì Studio mới tải tệp mới (mục đã có `file` sẽ không tải lại).
- Kết quả: CHỜ KIỂM CHỨNG (lượt gen 3).
- Áp dụng chung?: CÓ: ảnh tham chiếu phải sạch tuyệt đối; xem phóng to vùng đã xoá chữ trước khi gắn; Muse sao chép cả khuyết tật của ảnh tham chiếu. Đã chưng cất vào: chưa.

### 2026-11-05 · (chung) · quy tắc người dùng · loai: anh-tham-chieu
- Hiện tượng: người dùng không cho lấy ảnh tham chiếu từ video mẫu; sẽ tự cung cấp ảnh AI.
- Cách làm: dừng lượt gen; gỡ mọi refs cắt từ video khỏi biến thể và dự án Studio, xoá tệp `anh/carla.png`, `robot-machu-picchu.png`, `robot-goi-video*.png` và bản tải trong `userdata/studio/assets/<dự án>/`.
  `tao_bien_the.py` giờ chỉ đưa vào refs link hoặc tệp có thật, thiếu thì cảnh báo. Các mục "ảnh tham chiếu cắt từ video" ở trên KHÔNG còn áp dụng; bài học về BỐ CỤC ảnh tham chiếu (cùng tỉ lệ ô, không cắt sát mặt, không khuyết tật) vẫn đúng với ảnh AI.
- Kết quả: ĐẠT (quy tắc). Áp dụng chung?: CÓ. Đã chưng cất vào: SO-TAY (quy tắc làm việc), SKILL (quy tắc đã chốt).

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · sửa 4 · loai: kich-ban
- Hiện tượng: người dùng chốt dùng MỘT robot (ảnh AI, không tai nghe, nền trắng + vòng sáng) cho cả hai phần.
- Cách sửa: `ROBOT` chung cho `NGUOI_ROBOT` và `NGUOI_DAY`, một tệp refs `anh/ai-robot.png`; `[NHAN VAT DAY]` bỏ tai nghe, thêm câu "the reference photo shows only the robot's design: its white backdrop and glowing halo ring are NOT part of the scene" (giữ nền tối như video mẫu); đẩy lên Studio (PUT type + project).
- Kết quả: CHỜ KIỂM CHỨNG (chưa có tệp ảnh). Áp dụng chung?: CÓ (ảnh tham chiếu có nền khác cảnh → nói rõ nền ảnh không thuộc cảnh).
- Công cụ: `video-moi.py kiem-tra` báo "có refs" cả khi refs rỗng → nên cảnh báo nhân vật thiếu ảnh tham chiếu. Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · sửa 5 (ảnh AI) · loai: anh-tham-chieu
- Robot: ảnh AI người dùng (`anh/ai-robot.png`, 1086×1448, robot giữa khung, nền trắng + vòng sáng) cho cả hai phần.
- Carla: người dùng cho phép lấy hình hiện tại NHƯNG phải gen lại thành ảnh hoàn chỉnh → `cong-cu/gen_anh_carla.py` gọi Muse (`E.Api.generate("image", ...)`)
  với 2 khung video làm ĐẦU VÀO (mặt, trang phục), prompt "studio portrait, head to knees, plain light-grey background, no text"; kết quả `anh/ai-carla.png` sạch, đủ đầu–gối.
  Gọi API ngoài Studio cần `MUSE2API_HOME=userdata/api` (khoá ở `userdata/api/.env`), cổng lấy `api_port` trong `userdata/running.json`.
- Kịch bản `[NHAN VAT HOC]` thêm "its plain grey background and standing pose are NOT part of the scene". Xoá toàn bộ thư mục chạy cũ, gen lại từ cảnh 1.
- Kết quả: CHỜ KIỂM CHỨNG (lượt gen 3). Áp dụng chung?: CÓ (ảnh tham chiếu thiếu → gen ảnh hoàn chỉnh bằng Muse từ ảnh người dùng cho phép, không cắt ghép). Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · lượt gen 3 (cả video, ảnh AI) · loai: muse
- Kết quả chung: ĐẠT bố cục. Phần 1 robot (ảnh AI người dùng) + Carla (ảnh Muse gen lại) khớp khung mẫu; nhoè chuyển phần; phần 2 chia đôi đúng, robot vừa nửa trái
  (ảnh tham chiếu robot đứng giữa khung, không cắt sát mặt → không còn phóng to như lượt 1–2), không vệt nhoè. Phụ đề P1 xanh/vàng trên ô đen, P2 vàng/trắng, câu sai đỏ + ❌, cụm đúng xanh, ✅, viền xanh nửa phải.
  → các mục "CHỜ KIỂM CHỨNG" về bố cục ảnh tham chiếu và ảnh AI ở trên: ĐẠT.
- Lỗi còn lại:
  1. Cảnh 5 ("Eh, I have 22."): Muse nói câu HAI lần, mất "Eh", clip 8,0 s. Kiểm lời của Studio không bắt (lặp đủ chữ). Cách sửa: gen lại từ cảnh 5.
  2. Độ dài 59,2 s so với 30,2 s gốc: mỗi clip có 0,5–2,0 s lặng ĐẦU (cảnh 3: 2,0 s; cảnh 5: 1,6 s; cảnh 9: 1,4 s) + Muse nói chậm hơn. Studio chỉ cắt đuôi.
     Hướng sửa (chưa thử): cắt cả lặng đầu clip; nâng "Tốc độ tăng tối đa".
  3. Whisper đa ngôn ngữ nghe "How old are you?" thành "¿Cómo estás?" (đoạn tiếng Anh ngắn giữa video tiếng Tây Ban Nha); phụ đề vẫn đúng vì lấy chữ từ biến thể, chỉ mốc thời gian. "¿Cómo?" hiện trễ ~0,6 s.
- Áp dụng chung?: CÓ (kiểm tra lặp câu trong clip; lặng đầu clip làm video dài gấp đôi). Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · phân tích + tạo thể loại · loai: phan-tich
- Hiện tượng: `danh-gia` trên bản Studio không có `runtime\` → lỗi "runtime/python.exe: No such file"; chạy bằng `.venv\Scripts\python.exe` + `bin\` vào PATH thì đạt (đã có trong sổ tay mục 1).
  Gom cao độ tự động: cảnh sát nam và tài xế nữ rơi chung cụm A (125–221 Hz); tài xế hào hứng (lượt 9–11) bị tách thành cụm B 291 Hz.
- Nguyên nhân: tiếng nền đường cao tốc + một người lên giọng khi hào hứng.
- Cách làm: người nói lấy từ MÀU PHỤ ĐỀ (phần 1: cảnh sát ô đen chữ trắng, tài xế ô vàng chữ đen; phần 2: AI chữ xanh ngọc, tài xế ô trắng).
  Cắt ẩn ở 9,6 s (khung rộng hơn) công cụ không báo là cảnh cắt; thấy nhờ đỉnh chuyển động 38,5 ở 9,38–10,12 s + xem `chuyen-dong_02.jpg`.
  Video thuộc chiến dịch đã có (`canh-sat-gia-su-ai`, `xe-tai`): phần 2 dùng lại nguyên lời; tạo thể loại mới vì phần 1 khác (người thật, 2 nhân vật, 1 góc máy).
- Kết quả: ĐẠT (`kiem-tra` 0 lỗi, 3 cảnh báo fx giữ có lý do).
- Áp dụng chung?: CÓ: đỉnh chuyển động mạnh không trùng cảnh cắt cứng → kiểm tra cắt ẩn/đổi cỡ cảnh; cao độ gom tự động không tin khi có tiếng nền.
- Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · lượt gen 1 (chạy thử biến thể 01, KHÔNG refs) · loai: anh-tham-chieu
- Hiện tượng: chưa có ảnh AI của người dùng cho tài xế / cảnh sát / AI; người dùng chọn "Gen không ảnh refs".
- Cách làm: `nhap --chay-thu` biến thể `bien-the-01-goc`, Muse dựng mặt từ mô tả.
- Kết quả: CHỜ KIỂM CHỨNG (xem `scene1_start.png`, `phan2/base_HOC.png` có khớp mặt tài xế phần 1 không).
- Áp dụng chung?: CHỜ. Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · lượt gen 1, cảnh 1 · loai: muse
- Hiện tượng: `phan1/scene1_start.png` khớp bố cục `anh/khung-phan1-mau.png` (xe xanh cờ Mỹ trái, tài xế ở cửa sổ trái-trên, cảnh sát phải mặt nghiêng ngẩng lên, cọ + hoàng hôn), không chữ trên áo/xe.
  Tài xế to hơn mẫu (đầu ~20% bề ngang so với 11%), cảnh sát thấp hơn (đầu ~0,53 chiều cao so với 0,43). `scene1_cut.mp4` 2,1 s, Whisper đúng nguyên văn, chỉ cảnh sát nói; máy trôi rất nhẹ (giống mẫu).
  Xe xa trên đường vẫn có (prompt bảo đứng yên).
- Cách làm: Prompt ảnh tả bằng hình học (tỉ lệ khung xe 60%, đầu ở 1/3 và 40% chiều cao, mặt nghiêng trái từ hơi sau lưng), không refs.
- Kết quả: ĐẠT (cảnh 1).
- Áp dụng chung?: CÓ: tả vị trí đầu theo phần trăm chiều cao + "seen from slightly behind the left side, face in left profile turned up" cho người đứng dưới nhìn lên ra đúng góc mà không cần ảnh tham chiếu.
- Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · sửa 6 (người dùng duyệt lượt gen 3) · loai: studio
Người dùng báo 6 lỗi; nguyên nhân đã chứng minh bằng số đo trên chính các clip, cách sửa đã chạy thử lại trên clip cũ (chưa gen lại):
1. Lặng dài sau câu (video 59 s / gốc 30 s). Nguyên nhân: Whisper trong Studio cố định `small.en`; câu tiếng Tây Ban Nha → `speech_issues` báo "thiếu chữ" sai
   → Studio bỏ bản cắt sát, cắt lại rộng theo khoảng lặng (P1 cảnh 1 lời 1,0–4,1 s nhưng cắt 7,1 s; cảnh 3 3,75 s cho câu 1 chữ).
   Sửa (`engine.py`): `speech_lang(text)` (¿¡ñ/dấu hoặc ≥30% từ chức năng TBN → 'es'); tiến trình Whisper nạp thêm `small` đa ngôn ngữ, `_transcribe(..., lang)`;
   `voice_span`/`speech_issues` dùng ngôn ngữ của câu; bỏ dấu khi so chữ; "eh" vào `_FILLERS`. Thử lại: cảnh 1 7,10 → 3,67 s, cảnh 3 3,75 → 1,21 s, không báo thiếu.
2. 0:08 robot nhép khi Carla nói: chính là 3 s đuôi lặng của clip Carla (Muse cho robot mấp máy câu kế) → hết khi cắt sát (1). Thêm khoá môi `NGHE_ROBOT` + NEGATIVE P1.
3. 0:18 Carla nhép khi AI nói: clip nghe đầu tiên có tiếng −23 dB (`_talky`), mức miệng 0,018 < ngưỡng 0,020; chưa có clip câm dự phòng nên giữ bản có tiếng.
   Sửa (`split.py listen_take`): clip nghe có tiếng HOẶC vượt ngưỡng → khoá miệng; không khoá được (không dò được mặt) → khung nối đứng yên.
4. Từ 0:19 nửa phải rung: `_camera_lock` nắn TỪNG khung theo ước lượng ORB nhiễu (người cử động, nền mờ), làm mượt 7 khung → rung gấp 2–3 lần clip gốc
   (nền 0,24 → 0,60–0,73 px/khung). Thử khớp điểm chỉ trên nền: tệ hơn (nền bokeh). Sửa: khớp đa thức bậc 2 theo thời gian cho (phóng, dời x, dời y)
   → bù phóng/trôi chậm của Muse, không thêm rung (đo lại 0,23–0,30, ngang clip gốc).
5–6. 0:33 / 0:50 ting ting sai câu: `phu_de.units_from_variant` luôn gắn "fx" vào dòng ĐẦU của lượt ("Ah, sí, es verdad.") → gắn vào dòng chứa cụm "to"
   ("I'm 22.", "I'm from Mexico."); lượt không có "to" như cũ. Đã rà mọi BIEN-THE: chỉ 2 lượt của thể loại này đổi.
+ Lặp câu (cảnh 5 "I have 22. I have 22."): `speech_retry` giữ "lần ít lỗi nhất" theo SỐ lỗi → lần lặp thắng vì lần khác bị tính "thiếu eh". Sửa: luôn ưu tiên bản KHÔNG lặp.
- Phạm vi: code dùng chung (engine/split/phu_de) – áp cho mọi thể loại; câu tiếng Anh vẫn đi `small.en` như cũ. Cần KHỞI ĐỘNG LẠI Studio để nạp.
- Kết quả: CHỜ KIỂM CHỨNG (lượt gen 4). Áp dụng chung?: CÓ. Đã chưng cất vào: SO-TAY mục 6.

### 2026-11-05 · di-tru-gia-su-ai · phân tích + tạo thể loại · loai: phan-tich
- Hiện tượng: `danh-gia --lang es` đủ 40 câu (video song ngữ nhưng Whisper không bỏ đoạn tiếng Anh lần này). Gợi ý khuôn đưa ra 7 "mốc đổi cơ chế" vì robot nhỏ + badge logo góc trên trái làm số mặt nhảy; thực tế chỉ 3 phần (xem ảnh).
  Cao độ: gia sư AI phần 3 rơi chung cụm với Diego (~140 Hz); robot nhỏ ~310 Hz tách rõ.
- Cách làm: chia phần theo ảnh `tong-quan_N.jpg` (gọi điện / cảnh sát / ô PiP); người nói theo hình + phụ đề. Lần đầu dùng 3 phần trong `nhieu_phan` (plan đạt, 28 cảnh).
- Kết quả: ĐẠT (`kiem-tra` 0 lỗi; cảnh báo fx giữ). Áp dụng chung?: CÓ: badge/logo có mặt người (avatar) làm bộ đếm mặt báo PiP giả → luôn xem ảnh. Đã chưng cất vào: chưa.

### 2026-11-05 · di-tru-gia-su-ai · ảnh tham chiếu · loai: anh-tham-chieu
- Cách làm: người dùng cho Claude tự nhờ Muse gen ảnh → `cong-cu/gen_anh_nhan_vat.py` gen 5 ảnh từ CHỮ (mô tả lấy thẳng từ `tao_bien_the.py` để ảnh và chữ khớp), 0 ảnh đầu vào, chạy song song 5 luồng, ~1 phút.
  Prompt: "studio portrait, head to knees, plain light-grey background, no text"; robot nhỏ "sitting with legs dangling as if on a ledge" (đúng tư thế ngồi trên vai).
- Kết quả: ĐẠT (5 ảnh sạch, không chữ trên huy hiệu cảnh sát, đúng trang phục). Áp dụng chung?: CÓ. Đã chưng cất vào: chưa.

### 2026-11-05 · di-tru-gia-su-ai · lượt gen 1 (chạy thử biến thể 01) · loai: muse
- Cách làm: `nhap --chay-thu`, loại `Di-tru-gia-su-AI-46a2`, dự án `Di-tru---Diego-c294`.
- Hiện tượng: `final.mp4` 98,3 s (mẫu 67 s). Phần 1 đạt: mỗi khung một người, điện thoại áp tai, mặt Valeria/Diego giữ qua 5 ảnh mới. Phần 2 đạt: robot chibi ngồi vai trái từ cảnh 9, cảnh sát/Diego đứng đúng chỗ; cao độ đo tự động cảnh sát 116–170 Hz, Diego 120–125 Hz, robot 320 Hz (chưa nghe bằng tai để chắc không đổi giọng).
  Phần 3: `phan3/base_HOC.png` có thêm một robot trắng mắt xanh bay ở góc trên phải; ô AI che phần lớn, nhưng Muse cho nó lớn dần và lòi tay/thân ra dưới ô ở cảnh 18–28. Giọng AI 177–235 Hz, Diego 113–130 Hz (cảnh 25 câu hỏi ngạc nhiên 192 Hz).
- Nguyên nhân: STYLE LOCK dùng chung cho cả hai ảnh nền có câu "the AI tutor is a ... CGI robot", và khối HOC có câu "as if talking to the AI tutor", nên Muse vẽ robot vào cảnh của Diego.
- Kết quả: CHƯA ĐẠT (phần 3). Áp dụng chung?: CÓ, xem mục sửa 1 dưới.

### 2026-11-05 · di-tru-gia-su-ai · sửa 1: robot thừa trong nền phần 3 · loai: kich-ban
- Cách sửa: bỏ mô tả robot khỏi STYLE LOCK phần 3, chuyển "clean, glossy ... CGI robot" vào khối NHAN VAT DAY; khối HOC thay "talking to the AI tutor" bằng "talking to a friend on a video call", thêm "He is the only figure in the whole frame; the sky and the street behind him hold no other figure or object in the air". PUT kịch bản, xoá `phan3/base_*`, `scene*_` phần 3, làm lại từ cảnh 16.
- Kết quả: ĐẠT. `base_HOC.png` mới SẠCH (chỉ Diego, góc trên phải trời + cột điện); video cuối (104,5 s) không còn robot thừa ở cảnh 16–28.

### 2026-11-05 · di-tru-gia-su-ai · sửa 2: máy tiến dần, mặt Diego vào ô AI · loai: kich-ban
- Hiện tượng: `noi: lien` phần 3, khung cuối Diego `scene8/9/10_tail_HOC.png` mỗi cảnh gần hơn và lệch phải (từ ngang đùi → ngang ngực); cảnh 25 (`¿Es en serio?`) nửa mặt nằm dưới ô AI; cảnh 24 sát mép ô. Cảnh 17 phụ đề hiện muộn (Muse nói trễ ~2 s trong clip 3,7 s).
- Nguyên nhân: Studio chỉ gen lại khi MỘT clip phóng > x1,15; trôi cộng dồn qua nhiều clip nối không bị bắt.
- Cách sửa: khối HOC thêm "keeps the same distance the whole clip: it never moves closer, the framing stays head to thighs, his head stays in the left two thirds ... never enters the upper-right quarter"; xoá `phan3/scene9+_*`, làm lại từ cảnh 24 (khung cuối cảnh 23 còn ổn).
- Kết quả lần làm lại từ cảnh 24: CHƯA ĐẠT. Cảnh 24, 25 cuối clip nửa mặt Diego vẫn dưới ô AI. So khung cuối: clip Muse gốc `phan3/scene9_listen_HOC.mp4` Diego đứng giữa-trái, đúng khoảng cách; bản đã khớp `scene9_listen_HOC_khop.mp4` bị dời PHẢI + phóng to; `scene10_spk.mp4` → `scene10_spk_khop.mp4` cũng vậy. Tức là lỗi do bước khớp/khoá camera của `split.py` (cùng lỗi mục xe-tai "VỆT VỠ"), không phải Muse; câu khoá chữ không sửa được. Muse thêm: tài khoản 2d7b55910002 treo 92% hết giờ 5 lần liền ở cảnh 27 (~60 phút).
- Áp dụng chung?: CÓ (ghép 2 lớp nối liền nhiều cảnh: khoá khoảng cách máy bằng chữ; đề xuất code chung: so khung cuối với `base_<K>` theo tỉ lệ cộng dồn, chưa làm). Đã chưng cất vào: chưa.
- Áp dụng chung?: CÓ: ghép 2 lớp, STYLE LOCK và khối của nhân vật nền không bao giờ nhắc nhân vật trong ô (robot/AI); STYLE LOCK đi vào mọi ảnh nền. Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · lượt gen 1, vào phần 2 · loai: muse
- Hiện tượng: phần 1 xong 9 cảnh lúc 15:21; `phan2/base_HOC.png` 15:22; ảnh `base_DAY` (task `task_194420…`, tài khoản 414) treo ở 92% từ 15:22:25, người dùng thấy "cảnh bắt đầu P2 mãi chưa gen".
  15:27:37 Studio gửi lại trên tài khoản 415, xong 15:28:16 (39 s). Ảnh thường 30–45 s.
- Nguyên nhân: phía Muse/tài khoản (task không lỗi, chỉ đứng tiến độ); không phải kịch bản.
- Cách làm: không làm gì, Studio tự gửi lại. Cách xem: `userdata/api/data/tasks.json` (status/progress/updated_at từng task).
- Kết quả: ĐẠT (tự gỡ sau ~5 phút).
- Áp dụng chung?: CÓ: "kẹt ở cảnh X" → xem tasks.json trước khi sửa kịch bản. Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · lượt gen 1, ảnh gốc phần 2 · loai: muse
- Hiện tượng: `base_DAY.png` đạt (AI 3D tóc vàng, cằm tì tay, vòng sóng trắng nền đen, 16:9). `base_HOC.png`: mặt khớp phần 1 dù không refs,
  tay selfie từ góc dưới-trái đúng; NHƯNG đầu quá cao (đỉnh đầu ~0,17, mắt ~0,33 chiều cao) → ô AI (y 0,012–0,332) sẽ che trán tới mắt; thêm thú bông lạ trên bậu cửa.
- Nguyên nhân: "the face at about half of the frame height" không đủ; Muse đặt đầu theo thói quen selfie (1/3 trên).
- Cách sửa đề xuất (chưa làm, người dùng chọn chạy hết rồi xem): ghi số "top of the head at about 35% of the frame height, eyes at about 45%",
  "the upper third shows only the cab ceiling", NEGATIVE "toys, figurines, dashboard ornaments"; xoá `phan2/base_*`, `listen_*`, `scene*_spk`, làm lại từ cảnh 10.
- Kết quả: CHƯA ĐẠT, video cuối xác nhận: ô AI che từ trán xuống mũi tài xế suốt phần 2; thú bông còn; bảng tên ra chữ "YETI" ở vài cảnh. Áp dụng chung?: CÓ (ghép 2 lớp ô phía trên: luôn ghi % đỉnh đầu, đối chiếu `soi-hanh-ly` "top of the head at about one fifth" cho ô góc). Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · lượt gen 1, video cuối · loai: studio
- Hiện tượng: `final.mp4` 82,4 s (mẫu 50 s; phần 1 30,8 s / mẫu 18,4; phần 2 51,6 s / mẫu 31,6). Phần 1 đạt: bố cục, giấy tờ đổi tay đúng cảnh 5–6, phụ đề trắng/vàng.
  Phần 2: đáy ô AI có VỆT VỠ (dải ngang lệch, lặp cầu vai + cánh tay) từ cảnh 10 tới hết. Clip Muse gốc `phan2/scene1_spk.mp4` SẠCH; vỡ có từ `scene1_spk_khop.mp4` → `scene1_tail_DAY.png`,
  rồi Muse vẽ lại vết vỡ thành nội dung ở mọi clip nối sau (`noi: lien`).
- Nguyên nhân: `split.py` `_camera_lock` (thêm trong 3423a55): AI nền đen ít điểm nền, ORB bắt vào người đang gật đầu → tưởng camera dời; đo `scene1_spk` dời y −76…−97 px, `scene3_spk` phóng x0,91.
  Đường cong bậc 2 không neo khung 0 = đứng yên (khung đầu đã dời −76 px). Mép hụt lấy từ `tail_png` (tư thế khác) → dải vỡ ở đáy.
- Cách sửa đề xuất (code DÙNG CHUNG, chưa làm, chờ người dùng): neo khung 0 về đơn vị (trừ tham số khung 0 khỏi đường cong), bỏ khoá camera khi điểm khớp nằm chủ yếu trên người / nền gần như một màu; hoặc tắt khoá camera cho nhân vật nền phẳng.
- Kết quả: CHƯA ĐẠT. Áp dụng chung?: CÓ (mọi ghép 2 lớp có nhân vật nền phẳng: AI/robot nền đen). Đã chưng cất vào: chưa.

### 2026-11-05 · du-lich-chia-doi-gia-su-ai · sửa 7: cảnh 2 Carla nhép + làm y hệt robot · loai: muse + studio
- Hiện tượng: chỉ cảnh 2 (cảnh duy nhất của phần 1 robot nói, hai nhân vật chung khung) lần gen nào Carla cũng nhép theo lời robot, nhắm mắt/đổi nét mặt cùng lúc với robot.
  Đo `phan1/scene2_clip.mp4`: robot std 0.039, Carla std 0.031, há rộng 0.025, nhịp mở-khép 0.020 (= nhịp lúc chính Carla nói ở cảnh 1). Ảnh lưới 3 khung/giây xác nhận Carla mấp máy 0–3 s.
- Nguyên nhân: (1) mô tả robot "softly sculpted closed lips" → Muse coi môi robot là chi tiết cứng, đẩy khẩu hình sang mặt người thật duy nhất; câu prompt cũ cho robot "nghiêng đầu" nên Carla chép luôn cử chỉ.
  (2) Luật đo miệng cũ đòi người nghe "há rộng ≥ 18% số khung"; Carla nghiêng ba phần tư nên khe môi nhỏ → lọt. (3) Cài đặt Studio `check_overlap: false` (tắt tay, `mouth_note` rỗng) nên không đo, không gen lại.
  Cảnh 2 phần 2 (ghép 2 lớp) không bị vì mỗi nhân vật gen riêng clip.
- Cách sửa: `tao_bien_the.py` ROBOT: "soft flexible porcelain lips that open and move naturally with every word whenever the robot itself speaks"; kịch bản cảnh 2: tả người nghe TRƯỚC (môi mím, mắt mở, đầu yên, "does not copy the robot's face or movements"), robot chỉ cử động môi, NEGATIVE thêm nhắm mắt/bắt chước.
  `engine.mouth_check` (dùng chung): luật thứ ba cho người nghe nghiêng mặt: std ≥ abs_t và ≥ 0.7×người nói, nhịp ≥ 0.55×người nói, có khung mở > OPEN_GAP; bỏ qua ô trùng ô người nói.
  Thử trên clip thật: cảnh 2 → bắt; cảnh 1, 3 (robot im, std 0.017–0.019) → không bắt. Tập thử còn nhỏ (dự án khác chưa có cặp hai ô khác nhau đo được).
- Kết quả: ĐẠT ngay lần gen đầu (17:18, Studio khởi động lại 17:09, kiểm tra miệng bật). Robot std 0.045, há rộng 0.24, nhịp 0.043 (robot nói thật); Carla std 0.038 do nụ cười tắt dần nhưng nhịp 0.012, há 0.01 → luật mới không bắt nhầm; ảnh lưới: Carla mím môi suốt clip, chỉ chớp mắt một lần.
- Áp dụng chung?: CÓ: nhân vật không phải người (robot, thú, tượng) nói cạnh người thật → không bao giờ tả môi là "closed/sculpted/painted"; người nghe tả trước trong prompt cảnh đó. Đã chưng cất vào: SO-TAY mục 6.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · sửa 1: khoá camera chỉ đo trên nền + neo khung 0 · loai: studio (code chung)
- Hiện tượng: vệt vỡ đáy ô AI + ô AI trôi lên xuống (mục "lượt gen 1, video cuối").
- Cách sửa: `app/luo-studio/split.py` `_camera_lock`: chỉ lấy điểm ORB trên dải nền (25% mép trái, 25% mép phải, 10% trên), < 60 điểm thì bỏ khoá;
  đường cong bậc 2 neo khung 0 = đơn vị (lstsq trên `t, t²` của độ lệch so với đơn vị).
- Kết quả: ĐẠT. Clip AI sạch → không khoá; clip Machu Picchu và Di-trú vẫn khoá, khung 0 dời (0, 0). Lượt gen 2 (robot Talka) 13 cảnh phần 2: ô AI đứng yên, đáy ô sạch.
- Áp dụng chung?: CÓ (mọi ghép 2 lớp). Đã chưng cất vào: chưa (đề xuất SO-TAY mục 6: "khoá camera chỉ đo nền, neo khung 0").

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · sửa 2: đầu tài xế + đồ chơi + phụ đề · loai: kich-ban + hau-ky
- Cách sửa: `[NHAN VAT HOC]` ghi số "top of the head at about 38% of the frame height, eyes at about 48%, chin at about 60%";
  NEGATIVE phần 2 thêm "lettering on the name patch; toys, plush toys, figurines, dashboard ornaments"; `config.json` `phu_de.y_theo_phan` 1260/650 → 1560/1560.
- Kết quả: ĐẠT với `base_HOC` và 13 cảnh phần 2 (mặt tài xế dưới ô AI, không thú bông, bảng tên trơn). Phụ đề: xem mục "lượt gen 2, video cuối".
- Áp dụng chung?: CÓ: ghép 2 lớp ô phía trên → ghi % đỉnh đầu/mắt/cằm bằng số. Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · sửa 3: gia sư AI → robot Talka (có refs) · loai: anh-tham-chieu
- Cách sửa: ảnh người dùng gửi = robot trắng của `du-lich-chia-doi-gia-su-ai` → `anh/ai-robot-talka.png`, refs `NGUOI_DAY`; mô tả robot như du-lich
  (môi sứ mềm, cử động khi nói); STYLE LOCK "photorealistic CGI humanoid robot"; NEGATIVE "human skin, hair or clothing on the robot"; giọng nữ trẻ 190–230 Hz.
  Làm lại từ cảnh 10 (xoá `phan2/base_*`, `listen_*`, `scene*_spk*`).
- Kết quả: ĐẠT: `base_DAY` và 13 cảnh giống ảnh mẫu (mặt sứ, mắt xanh, giáp trắng viền cyan, tay chống cằm, vòng sóng trắng), đồng nhất suốt phần 2.
- Áp dụng chung?: CÓ: đổi nhân vật trong ô ghép 2 lớp chỉ cần gen lại từ cảnh đầu phần đó. Đã chưng cất vào: không cần.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · sửa 4: "same file" khi làm lại · loai: studio (code chung)
- Hiện tượng: "Làm lại" báo `...phan1\scene1_cut.mp4 and ...\scene1_cut.mp4 are the same file`.
- Nguyên nhân: `nhieu_phan._link` xoá dst thất bại (tệp đang mở) mà dst đã là hardlink của src → `shutil.copyfile` ném SameFileError.
- Cách sửa: `_link` kiểm `os.path.samefile` trước, trùng thì bỏ qua. Lần này gỡ tay bằng cách xoá `scene[1-9]_cut/last` ở thư mục gốc.
- Kết quả: ĐẠT (06/11 sau khi Studio khởi động lại, "Làm lại từ cảnh 8" chạy không lỗi). Áp dụng chung?: CÓ. Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · lượt gen 2 (robot Talka), video cuối · loai: studio
- Hiện tượng: `final.mp4` 82,6 s (18:42). Phần 1 giữ nguyên lượt 1. Phần 2: robot đúng ảnh mẫu suốt 13 cảnh, ô AI đứng yên, đáy sạch, mặt tài xế dưới ô;
  phụ đề y 1560 nằm ngang ngực ở cả hai phần, không che mặt; viền đỏ cảnh "I am very hurry", icon ✓ / ✗ / $ đúng chỗ.
- Kết quả: ĐẠT (sửa 1, 2, 3 xác nhận). Còn khác mẫu: dài ~1,6 lần mẫu; lời thoại vẫn gọi app "LangLearn".
- Áp dụng chung?: xem các mục sửa 1–3. Đã chưng cất vào: chưa.

### 2026-11-06 · di-tru-gia-su-ai · sửa 3: 9 góp ý của người dùng sau video đầu · loai: kich-ban + studio
- Hiện tượng (người dùng xem bản 98 s): (1) cảnh 1 thừa ~3 s lặng sau "No regreses a casa todavía."; (2) cảnh 3 Valeria cười; (3) muốn robot nhỏ trên vai là robot của người dùng (ảnh `anh/robo-nguoi-dung.png`);
  (4) cảnh sát nhìn camera; (5) hai người tiến sát nhau; (6) gật đầu vô lý; (7) 0:37–0:43 (cảnh 14–15) Diego mọc râu; (8) thêm câu Diego "I practice with Talka AI ten minutes a day." cùng khung cuối phần 2; (9) từ 0:44 ô AI che mặt Diego.
- Nguyên nhân + cách sửa:
  (1) `phan1/scene1_cut.mp4` = nguyên clip 5,0 s; Whisper đo lời 0–1,86 s. Cảnh 1 là câu tiếng Tây Ban Nha đầu tiên của lượt chạy: tiến trình Whisper phải nạp mô hình "small" đa ngôn ngữ → `voice_span` lỗi/hết giờ → cắt theo khoảng lặng, mà clip có tiếng nền liên tục nên không có lặng cuối → giữ cả clip.
      Code chung `engine.py`: thử `voice_span` lại một lần; cắt lại khi mất chữ thì vẫn theo mốc lời (span, lo 0,45 / hi 1,1) thay vì span=None.
  (2) cảnh 3 emo "worried", hành động "serious, calm, reassuring face with no smile at any moment", negative riêng "smiling; a grin".
  (3) NGUOI_ROBO = robot người dùng thu nhỏ (~25 cm, giáp trắng viền xanh băng, mắt xanh nhạt, vòng hào quang), refs ảnh người dùng; môi tả "soft flexible lips that open ... whenever the robot itself speaks" (mục 6 sổ tay).
  (4) NHIN/NGHE_CANHSAT "never looks at the camera", EYE LINE "only the tiny robot ever looks into the lens", negative.
  (5) STYLE LOCK + ANH_RONG "about one metre apart ... nobody steps toward the other"; bỏ "bước tới" ở cảnh 6.
  (6) Bảng cảm xúc dùng chung `prompt_parts.EMO_CUES` tự chèn "nods" (excited, encouraging, reassuring, impressed, decisive) + mặc định người nghe "tiny nod" (`engine.py`, `make_variants.py`, `split.py`, `prompt_parts` attentive/patient/listening) → bỏ hết, thay "the head steady". Kịch bản: VIDEO SUFFIX "no nodding", NEGATIVE "repeated nodding or head bobbing".
  (7) NGUOI_HOC "completely clean-shaven ... no beard, no stubble, no moustache", negative phần 2–3; cảnh 8 phần 2 (lượt 13) ảnh mới cùng góc để mặt về đúng ảnh tham chiếu (5 cảnh nối liền trôi mặt).
  (8) thêm lượt 16 (phần 2 cảnh 11, khung "rong_robo" nối từ khung cuối cảnh trước); tổng 29 lượt.
  (9) code chung `split.py`: `align_to_tail` thêm bước (1c) kéo dần khung cuối về bố cục `base_<K>` (chỉ trong phần ảnh thật, không lộ mép); `face_under_panels()` đo mặt nhân vật nền nằm dưới ô khác (> 12% → gen lại, cả clip nói lẫn clip nghe; sau khi khớp còn che thì cảnh báo).
      Đo trên clip cũ: `scene10_spk.mp4` 50%, `_khop` 62%, `scene9_listen_HOC_khop` 44%, `scene11_spk` 7%. Kịch bản: mặt ở ~38% bề ngang, đỉnh đầu ~12%.
- Kết quả (gen lại toàn bộ 06/11, 97,2 s, 29 cảnh): ĐẠT (1) cảnh 1 còn 2,0 s; (2) Valeria nghiêm, không cười; (3) robot người dùng trên vai; (5) hai người cách ~1 m suốt; (6) không thấy gật đầu; (7) không râu ở cảnh 13–16; (8) câu Talka AI có phụ đề, giữ khung cuối;
  (9) phần 3 cảnh 17–29 mặt Diego luôn ngoài ô AI. CHƯA ĐẠT (4): cảnh 13 cảnh sát quay mặt thẳng ống kính 33,3–34,5 s dù prompt ghi "never looks at the camera" hơn 10 lần → sửa 4.
- Áp dụng chung?: CÓ: (1) câu đầu ngôn ngữ mới của lượt chạy; (6) không bao giờ đưa "nod" vào cue mặc định; (9) mọi ghép 2 lớp nền toàn khung. Đã chưng cất vào: SO-TAY mục 3.6 + 6.

### 2026-11-06 · di-tru-gia-su-ai · sửa 4: cảnh sát vẫn nhìn ống kính (cảnh 13) · loai: studio (code chung)
- Hiện tượng: `phan2/scene8_clip.mp4` (cảnh chung 13, "Your English is really good.", emo impressed) cảnh sát cười rồi quay mặt thẳng ống kính 1,5–2,5 s; khung cuối lỗi nối sang đầu cảnh 14.
- Nguyên nhân: Muse bỏ qua khoá ánh mắt bằng chữ khi nhân vật cười/khen (cảm xúc ấm áp kéo mặt về ống kính). Chữ không đủ.
- Cách sửa: `engine.py` thêm `gaze_frontal()` + `gaze_retry()`: nhân vật có NHIN_/NGHE_ khớp "never looks ... camera/lens" thì đo hướng mặt (mediapipe: lệch mũi so với giữa hai mắt / khoảng cách hai mắt)
  trong đoạn được giữ (tới hết từ cuối theo Whisper + 0,4 s); quay thẳng (< 0,35) liên tục ≥ 0,5 s → gen lại kèm ghi chú (tối đa 2 lần, giữ lần ít nhất).
  Đo trên clip cũ: nhìn người kia 0,6–1,0; nhìn ống kính 0,10–0,27; cảnh 8 bị bắt 0,83 s, cảnh 9 0,5 s (khung đầu thừa hưởng), 9 cảnh còn lại 0. Tắt bằng opts check_gaze.
- Kết quả: ĐẠT (gen lại cảnh chung 13–16, video 97,6 s): đo lại bản cắt cảnh sát yaw 0,68–1,03 mọi khung, không khung nào quay ống kính; xem ảnh: không râu, hai người cách ~1 m. Ghi nhận nhỏ: khuyên tai Diego cảnh 16 hơi khác (khuyên thả thay vòng tròn).
- Áp dụng chung?: CÓ: mọi cảnh thường có nhân vật "không bao giờ nhìn camera" (cảnh sát, nhân viên soi hành lý...). Đã chưng cất vào: SO-TAY mục 6.

### 2026-11-06 · du-lich-chia-doi-gia-su-ai · 20 biến thể từ CSV người dùng (đổi nhân vật + nền) · loai: studio
- Hiện tượng: CSV 20 dòng (10 nữ/10 nam, 22–78 tuổi; ảnh nhân vật toàn thân phông xanh; 2 ảnh nền: Chichén Itzá cho 1–10, Tulum cho 11–20). Kịch bản phần 1 viết cứng "the woman/she", "Machu Picchu/the peak", "hands in the pockets of the mustard coat".
- Cách làm: phần 1 chuyển sang token GIOI_HOC, ANH_SANG, NEN_ROBOT, DIEM_NHIN, TAY_HOC; câu tả dùng {{TEN_HOC}} thay đại từ. Ảnh nền gắn refs NEN_ROBOT:
  đuôi `_ROBOT` để `nhieu_phan.sub_variant` bỏ ảnh nền ở phần 2 (không có ROBOT); tên trung tính (NEN_CANH) thì split.py `owner()` = None → gửi ảnh Chichén Itzá cho cả base_HOC phòng khách.
  Nhãn trường NEN_ROBOT đặt câu tiếng Anh (chú thích ảnh gửi Muse lấy từ nhãn). Tuổi trong lời thoại ("I'm 25") lấy từ CSV; giọng sinh theo giới + tuổi. Ref note: phông xanh/xám KHÔNG thuộc cảnh.
- Kết quả: kiểm tra 0 lỗi (164 mục, tải đủ 22 ảnh); dự án `Face-to-face-Mexico---20-bien-the-b3d8` 20 biến thể × 4 ảnh. CHƯA GEN THỬ.
- Áp dụng chung?: CÓ: ảnh nền riêng một phần trong dự án nhiều phần → token phải có đuôi `_<khoá nhân vật chỉ có ở phần đó>`. Đổi giới/tuổi người học → kịch bản không được có đại từ/trang phục cứng. Đã chưng cất vào: SO-TAY mục 6.

### 2026-11-06 · du-lich-chia-doi-gia-su-ai · lỗi "chưa điền: Tư thế khi nghe (HOC)" · loai: studio
- Hiện tượng: bấm "Thêm vào hàng đợi (20)" → toast đỏ `"bien-the-01-lucia" chưa điền: Tư thế khi nghe (HOC)`.
- Nguyên nhân: biến thể chỉ có NGHE_HOC@1 / NHIN_HOC@1 / VAI_HOC@1; `ui/app.js` (dòng ~492) chỉ kiểm khoá gốc. `kiem-tra` coi "@1" là đủ nên không bắt. Carla không bị chặn vì vào hàng đợi bằng `nhap --chay-thu` (API).
- Cách sửa: `tao_bien_the.py` ghi thêm khoá gốc cùng giá trị phần 1 (phần 2 ghép 2 lớp không đọc NGHE_/NHIN_/VAI_); cập nhật 2 dự án qua API, giữ refs; `video-moi.py kiem-tra` thêm LỖI "chỉ có khoá @phần".
- Kết quả: ĐẠT (cả 21 biến thể không còn trường trống; công cụ bắt được bản lỗi). Áp dụng chung?: CÓ. Đã chưng cất vào: SO-TAY mục 6 + kiem-tra.
- Lưu ý: sửa dự án qua API khi trang dự án đang mở → nút hàng đợi lưu bản cũ của trình duyệt đè lại (06/11, lỗi tái diễn lần 2). Luôn bảo người dùng F5 trước.

### 2026-11-06 · du-lich-chia-doi-gia-su-ai · 20 biến thể: AI cao, người thấp ở phần 2 · loai: studio (code 1.2.2)
- Hiện tượng: biến thể 01–03 phần 2 robot đầu sát mép trên, người học đầu ở ~45% khung; dải trên ảnh người bị kéo giãn mờ.
- Nguyên nhân: `split.py` 1.2.2 bước chống "ô che mặt" (`panel_clear_y` + `shift_down`) cho mọi nhân vật nền, kể cả khi nền có khung riêng (chia đôi).
  Toạ độ mặt đo trong ảnh 9:16 riêng (mặt giữa ảnh x 0,4–0,6) bị so với ô DAY x 0–0,5 của màn ghép → "che" → gen lại kèm "COMPOSITION FIX" rồi dịch 35%.
  Đo: base_HOC gốc đỉnh đầu 0,08–0,12 / DAY 0,07 (vốn ngang nhau); sau dịch 0,44–0,45.
- Cách sửa: `panel_clear_y` trả 0 khi `cfg["bg"] in cfg["panels"]` (thử: chia đôi → 0, ô góc vẫn 0,4). Video đang chạy: dừng, khôi phục `base_HOC.png.truoc-dich.png`, xoá clip phần 2, làm lại từ cảnh 4; cần khởi động lại Studio.
- Kết quả: CHỜ KIỂM CHỨNG. Áp dụng chung?: CÓ (mọi bước đo theo toạ độ màn ghép phải bỏ qua nền có khung riêng). Đã chưng cất vào: SO-TAY mục 6.

### 2026-11-06 · du-lich-chia-doi-gia-su-ai · bỏ "đè mồm" (khoá miệng clip nghe) · loai: studio (code dùng chung)
- Hiện tượng: người dùng thấy miệng bị đè ở cảnh 4 biến thể 2 (`phan2/scene1_listen_HOC_khop_khoa.mp4`); biến thể 3 bị ở cảnh 4, 6, 8.
- Nguyên nhân: split.py nhánh dự phòng "clip nghe vẫn mấp máy sau khi gen lại → `_locked` dán môi khép" (thêm 03/11 soi hành lý).
- Cách sửa: `_lock_on` luôn False; nhánh dự phòng chỉ cảnh báo, giữ nguyên clip Muse (người dùng sửa lại: chỉ bỏ dán miệng, không thay bằng khung đứng yên). Cần khởi động lại Studio; cảnh đã đè phải "Chỉ làm lại cảnh này".
- Kết quả: CHỜ KIỂM CHỨNG. Áp dụng chung?: CÓ: người dùng cấm mọi kỹ thuật đè/dán lên mặt (cùng loại với "đè hình" đã bỏ). Đã chưng cất vào: SO-TAY mục 6.

### 2026-11-06 · xe-tai-canh-sat-gia-su-ai · sửa 5: "LangLearn" → "Talka AI" trong lời thoại · loai: bien-the
- Cách sửa: `tao_bien_the.py` thay 3 câu (lượt 8 tài xế, 19 và 21 robot), sinh lại JSON, PUT vào dự án. Gen lại phần 1 từ cảnh 8 (cảnh 9 nối khung);
  phần 2 xoá `phan2/scene1[0-3]_*` + `phan2/raw.mp4` (= cảnh 19–22), giữ `base_*` và cảnh 10–18. Bản cũ lưu ở scratchpad `final02/final-luot2-langlearn.mp4`.
- Kết quả: CHỜ KIỂM CHỨNG (đang chờ sau hàng Face-to-face). Mục sửa 4 (`_link`): Studio đã khởi động lại, lần "Làm lại" này không còn lỗi same file → ĐẠT.
- Áp dụng chung?: CÓ: đổi lời ở cảnh N của phần ghép 2 lớp nối liền → chỉ xoá `phan<k>/scene<local≥N>_*`, giữ ảnh gốc và cảnh trước. Đã chưng cất vào: chưa.

### 2026-11-06 · du-lich-chia-doi-gia-su-ai · luật trái/phải phần 2 · loai: kịch bản
- Yêu cầu người dùng: từ cảnh 4, robot AI luôn bên TRÁI, người học bên PHẢI; lượt robot thì bên phải ngồi im, và ngược lại.
- Cách làm: ghép 2 lớp vốn gen riêng từng người nên luật được ghi vào [NHAN VAT DAY/HOC] (vị trí trên màn gọi) và [NGHE DAY/HOC] ("<bên kia> has the turn; <tên>, on the RIGHT/LEFT, sits completely still and quiet").
  Tránh chữ speak/talk/voice trong khối NGHE (`_calm_listen` cũng tự lọc). Đã xem lại listen_prompt dựng ra: câu luật có mặt.
- Kết quả: kiểm tra 0 lỗi; đã đẩy vào loại dự án (áp dụng cho các cảnh gen sau đó). CHỜ KIỂM CHỨNG trên video.

### 2026-11-06 · xe-tai-canh-sat-gia-su-ai · sửa 6: 20 biến thể từ CSV người dùng (đêm, nữ cảnh sát, đổi tài xế) · loai: bien-the + kich-ban
- Đầu vào: `anh/20-bien-the/20-bien-the-xe-tai.csv` (20 tài xế Mexico, 10 biến thể đi với 1 nữ cảnh sát Mỹ, 5 biến thể ban đêm), 21 link Google Drive.
  Tải thử cả 21 link: đều là ảnh webp 1152×2048 nền xanh lá, khớp mô tả; ảnh tài xế 01 có chữ trên miếng vá áo → prompt ghi "plain chest patches without lettering".
- Cách làm: kịch bản thêm token `{{HE_/HIS_/HIM_CANHSAT}}` (thay 9 chỗ "he/his/him" của cảnh sát) và `{{SANG_P1}}` / `{{SANG_P2}}` (ánh hoàng hôn ghi cứng ở STYLE LOCK, Prompt ảnh);
  giá trị mặc định trong `CHUNG` của `tao_bien_the.py` = chữ cũ (dự án 031a không đổi). "sir" → "ma'am" khi cảnh sát nữ. Công cụ mới `cong-cu/tao_bien_the_20.py`
  → `BIEN-THE-XE-TAI-20-BIEN-THE.json`; cặp khác giới kiểm bằng assert (tài xế nữ + cảnh sát nam không ảnh; tài xế nam + nữ cảnh sát có ảnh).
  Biến thể 20: CSV "cầm găng tay trên tay" → để găng giắt thắt lưng, vì tay phải cầm giấy tờ / điện thoại (tránh đạo cụ thừa).
- Kiểm tra: `kiem-tra --tai-anh` 0 lỗi, 20 cảnh báo fx (đã biết). Dự án Studio `Xe-tai-Check-license---20-bien-the-e0ae`, 20 biến thể, refs tải đủ (0 lỗi). Chưa gen.
- Lưu ý: chép kịch bản mới vào loại `Canh-sat-chan-xe-tai-gia-su-AI-c7b5` TRƯỚC khi PUT biến thể có token cho dự án cũ = có khoảng hở token trống; lần này 031a đã ghi `phan2/script.txt` trước nên không bị.
  Thứ tự đúng: PUT biến thể có giá trị token cho mọi dự án dùng loại đó, rồi mới đổi kịch bản loại.
- Kết quả: CHỜ KIỂM CHỨNG (chưa chạy thử biến thể đêm / nữ cảnh sát). Áp dụng chung?: CÓ (thêm token vào kịch bản loại dùng chung: PUT biến thể trước). Đã chưng cất vào: chưa.

### 2026-11-07 · xe-tai-canh-sat-gia-su-ai · sửa 7: robot AI thừa ngồi ghế phụ cạnh tài xế (phần 2) · loai: kich-ban + studio (code dùng chung)
- Hiện tượng: dự án 20 biến thể, `phan2/base_HOC.png` của biến thể 01, 03, 04 có robot trắng ngồi ghế phụ bên phải tài xế → mọi cảnh 10+ đều có robot thừa
  (ngoài robot đúng trong ô gọi video). Biến thể 02 và dự án 031a sạch (Muse không vẽ lần nào cũng như nhau). Ảnh lỗi lưu ở scratchpad `robo/backup/`.
- Nguyên nhân: [STYLE LOCK] phần 2 dùng chung cho cả hai lớp có mệnh đề "the AI tutor is a sleek photorealistic CGI humanoid robot (glossy white porcelain armour…)";
  `split.py` ghép STYLE LOCK + [NEGATIVE] nguyên văn vào prompt ảnh gốc / clip của tài xế → prompt lớp nền tả robot. Thêm "as if talking to the AI tutor on the phone"
  trong [NHAN VAT HOC], "robot" trong NEGATIVE. Ban đêm cabin tối, ghế phụ trống dễ bị lấp.
- Cách sửa: (1) kịch bản: bỏ mệnh đề robot khỏi STYLE LOCK phần 2 (dời vào [NHAN VAT DAY]), HOC "completely alone in the cab: the passenger seat beside the driver is empty",
  "as if on a video call", NGHE HOC "waits for the reply", NEGATIVE bỏ các mục nhắc robot. (2) `split.py` (dùng chung, mọi thể loại ghép 2 lớp): `_style` / `_neg`
  bỏ các mệnh đề (ngăn bởi . ;) của STYLE LOCK và NEGATIVE có nhắc tên ngắn TEN_ của NHÂN VẬT KHÁC → mỗi lớp chỉ thấy mô tả của chính nó. Kiểm: prompt HOC không còn "robot/tutor"
  (chỉ "robotic voice"), prompt DAY giữ nguyên robot. Dữ liệu: xoá phần 2 biến thể 01/03/04 (giữ `base_DAY.png`, phần 1), làm lại từ cảnh 10; 05–20 chạy với kịch bản mới.
- Kết quả: ĐẠT bước đầu (07/11 14:45): base_HOC mới của 01/03/04 (cả lần gen đầu lẫn lần gen lại vì ô che) không còn robot, ghế phụ trống; cảnh 10–12 cả 3 biến thể sạch. Cảnh 13–22 và biến thể 05–20 CHỜ KIỂM CHỨNG. Áp dụng chung?: CÓ: khối dùng chung (STYLE LOCK, NEGATIVE, VIDEO SUFFIX) KHÔNG tả ngoại hình nhân vật; mô tả nhân vật chỉ nằm trong [NHAN VAT <KHOÁ>].
  Đã chưng cất vào: SO-TAY mục 6.

### 2026-11-07 · canh-sat-gia-su-ai · dự án mới "canh-sat-speeding" (chạy lại mẫu, 1 video) · loai: chay-thu
- Đầu vào: kịch bản + biến thể có sẵn `SAMPLE/canh-sat-gia-su-ai/` (biến thể `bo-con-xe-do-gia-su-ai`, refs 4 ảnh `anh/<KHOÁ>.png`).
- Cách làm: `video-moi.py kiem-tra --tai-anh` (0 lỗi, 1 cảnh báo fx đã biết: 14 wrong, 16 right, 17 wrong) → `nhap --ten-loai/--ten-du-an "canh-sat-speeding" --chay-thu`.
  Loại `canh-sat-speeding-ab37` (24 trường, ghép 2 lớp), dự án `canh-sat-speeding-d8a7`, hàng đợi `ff6ea408` (đang chờ sau dự án Xe tải 20 biến thể).
  Lưu ý: máy này không có `runtime\python.exe`, dùng `.venv\Scripts\python.exe` + `PYTHONIOENCODING=utf-8`.
- Kết quả: CHỜ KIỂM CHỨNG (chưa gen xong). Áp dụng chung?: KHÔNG. Đã chưng cất vào: chưa.

### 2026-11-09 · canh-sat-gia-su-ai · sửa: khoảng trống trước lời thoại đầu cảnh (phần 2, cảnh 23 "Seriously?" dự án canh-sat-speeding) · loai: studio (engine dùng chung)
- Hiện tượng: thẻ cảnh "[P2] Seriously?" (cảnh 23, lượt thứ 11 của phần 2) trong Studio có khoảng im dài trước khi tài xế bắt đầu nói.
- Nguyên nhân (đã chứng minh): mặc định `[GHEP HAI LOP]` không khai `noi:` → `noi: lien` (nối khung): mỗi cảnh sau của cùng nhân vật phải bắt đầu ĐÚNG khung cuối cảnh
  trước của chính nó, nên `split.py` gọi `engine.smart_cut(..., head_margin=99.0)` để KHÔNG cắt đầu clip (cắt đầu sẽ đổi khung đầu, lệch chỗ nối). `smart_cut` do đó luôn để
  `head=0` và chỉ tua nhanh các khoảng ngắt GIỮA câu (`inner`, tính từ `speech_start` trở đi); đoạn im TRƯỚC `speech_start` (khi `head` không được nhích lên) không được
  đưa vào danh sách tua nhanh, nên giữ nguyên tốc độ → nghe là một khoảng trống dài trước khi nói ở mọi cảnh nối tiếp (không riêng cảnh 23 hay dự án này).
- Cách sửa: `app/luo-studio/engine.py` hàm `smart_cut` — thêm đoạn `[head, speech_start)` (nếu dài ≥ 0,55 s) vào `longs` (danh sách tua nhanh, như khoảng ngắt giữa câu, tối đa x2)
  thay vì bỏ qua; tua nhanh không cắt khung nào nên khung đầu clip vẫn y hệt (vẫn nối đúng khi `noi: lien`). Không sửa kịch bản `.txt`/biến thể `.json` vì phần 2 không có tham số
  thời lượng "Mở đầu" theo cảnh (như phần 1); nguyên nhân nằm ở engine dùng chung cho MỌI dự án ghép 2 lớp nối khung, không phải ở kịch bản.
- Kết quả: CHỜ KIỂM CHỨNG (cần bấm "Chỉ làm lại cảnh này" cho cảnh 23 trong Studio rồi nghe lại; dự án `canh-sat-speeding-d8a7`, chưa chạy lại do cần Studio đang mở/Muse credit).
- Áp dụng chung?: CÓ: mọi thể loại nhiều phần ghép 2 lớp dùng `noi: lien` (mặc định khi không khai `noi:`) được lợi, không cần sửa kịch bản từng thể loại.
- Đã chưng cất vào: chưa (đưa vào SO-TAY mục 6 ở lượt chưng cất kế tiếp, bảng "Nền/khung hình nhảy..." / "Lặng 2–3 s sau câu..." cùng nhóm lỗi căn thời gian clip).
### 2026-11-06 · (chung) · thử nghiệm độ dài prompt Muse · loai: muse
- Hiện tượng: prompt video Studio gửi Muse cho một cảnh 4 giây ("Yes, it is.", soi hành lý) dài ~1.800–2.100 từ: khối Voice lặp 3 lần
  (trường Voice, chép lại trong Prompt video, Studio ghép thêm "Spoken audio"), CHAR LOCK tả cả người ngoài khung, >60 mệnh lệnh phủ định.
- Cách làm: A/B cùng cảnh 2, cùng khung đầu, 3 độ dài (A đầy đủ ~2.090 từ / B rút gọn ~470 / C tối giản ~180), mỗi độ dài 3 người khác nhau
  (biến thể 02,05,08 / 01,04,07 / 03,06,09), chấm bằng Whisper + đo chuyển động (`userdata/thu-nghiem-prompt/`).
- Kết quả: A gen 116/151/168 s, lời đúng 2/3, 2/3 lần tay áo cảnh sát (người ngoài khung) lọt vào mép; B gen 44–82 s, đúng 2/3, không lỗi hình;
  C gen 41–131 s, đúng 3/3, bắt đầu nói ở 0,0 s cả 3 lần, chuyển động đều. ĐẠT (xu hướng nhất quán; chỉ 3 mẫu/nhóm nên chênh nhỏ chưa chắc).
- Áp dụng chung?: CÓ: viết khoá ngắn, câu khẳng định, chỉ tả người có trong khung, không lặp Voice/hành động; bỏ chữ đánh dấu "STYLE LOCK, SET LOCK, CHAR LOCK, VIDEO SUFFIX"
  trong Prompt video (Studio tự ghép khối khoá, chữ đánh dấu chỉ là nhiễu).
- Đã chưng cất vào: chưa. 07/11/2026: người dùng quyết định không chuyển kịch bản sang bản rút gọn; bản thử trong SAMPLE/canh-sat-gia-su-ai đã gỡ, kết luận A/B giữ lại làm tham khảo.

### 2026-11-06 · (chung) · Muse trả lại video cũ · loai: muse
- Hiện tượng: gửi cùng ảnh khung đầu + prompt gần giống (khác hội thoại Muse, khác session LUO-API) → Muse trả đúng video cũ (cùng md5) sau ~20 s, không gen mới.
  Đổi 1 điểm ảnh vẫn trúng; đổi hẳn nội dung prompt (hành động khác) mới gen mới (114 s). Dọn media tài khoản (admin cleanup) có thể phá đệm nhưng xoá hội thoại trên Muse.
- Nguyên nhân: Muse có bộ nhớ đệm theo nội dung (ảnh + ý prompt), không theo byte.
- Hệ quả: "gen lại cảnh" cùng khung đầu, prompt chỉ thêm ghi chú sửa ngắn có thể nhận lại đúng clip lỗi. CHỜ KIỂM CHỨNG trong Studio (so md5 clip gen lại với clip cũ).
- Áp dụng chung?: CÓ. Đã chưng cất vào: chưa.

### 2026-11-08 · robot-pho-tieng-long · phân tích + kịch bản · loai: phan-tich
- Hiện tượng: `danh-gia` báo "2 mặt ở 80% thời gian, 1 cụm cao độ" và gợi ý khuôn "hai người chung khung"; xem ảnh `luot_NN.jpg` thì chỉ có MỘT robot nói thẳng ống kính; "mặt" thứ hai là huy hiệu tròn phát sáng trên ngực / icon badge góc trên trái.
- Nguyên nhân: Haar cascade bắt hình tròn có tương phản như mặt. Gợi ý khuôn tự động không đáng tin khi có huy hiệu/logo hình mặt.
- Cách làm: đối chiếu số mặt với vị trí (mặt "phải, 0.52" cố định ở đúng chỗ huy hiệu) và với cụm cao độ duy nhất → một nhân vật; chọn khuôn cảnh thường 1 nhân vật + hậu kỳ riêng vẽ chữ (gần `talka-bang-tu-vung`, không cần phông xanh vì lớp chữ là ô đặc).
- Kết quả: ĐẠT (kiem-tra 0 lỗi 0 cảnh báo; 361 từ khoá).
- Áp dụng chung?: CÓ (mọi video có logo/huy hiệu hình mặt: đếm mặt theo VỊ TRÍ cố định trước khi tin số mặt).
- Đã chưng cất vào: chưa.

### 2026-11-08 · robot-pho-tieng-long · kịch bản · loai: kich-ban
- Quyết định: gộp 12 câu ngắn của video mẫu thành 6 lượt (một cảnh một lượt ~5 s), vì thẻ từ lóng và nghĩa căn theo TỪ Whisper trong cảnh (`post.py words_of_turns`) nên không cần mỗi câu một cảnh; ít cảnh nối → ít trôi mặt/mũ/áo.
- Kết quả: CHỜ KIỂM CHỨNG (lượt chạy thử biến thể `texan-f1-austin`).
- Áp dụng chung?: CÓ cho mọi thể loại có hậu kỳ căn theo từ: số cảnh theo nhịp ~5 s, không theo số câu của video mẫu.
- Đã chưng cất vào: chưa.

### 2026-11-08 · robot-pho-tieng-long · hậu kỳ chạy thử trên video mẫu · loai: hau-ky
- Cách làm: chạy `post.py` trên chính video mẫu với `scenes.json` giả (6 cảnh theo mốc lượt gộp) + biến thể 1, trước khi Muse gen xong, để kiểm lớp chữ sớm.
- Kết quả: ĐẠT: Whisper nghe đủ 6 lượt (lời biến thể khác lời gốc vài từ vẫn khớp mờ), 4 thẻ hiện đúng từ ("Howdy" 4,30 s, nghĩa 5,55 s...), 51 mốc từ karaoke; bố cục trùng khung mẫu (so `anh/khung-mau.png`).
- Áp dụng chung?: CÓ: mọi thể loại có hậu kỳ riêng nên thử `post.py` trên video mẫu với scenes.json giả trước khi gen (phát hiện lỗi vẽ/căn lời mà không tốn lượt Muse).
- Đã chưng cất vào: chưa.

### 2026-11-08 · robot-pho-tieng-long · lượt gen 1, cảnh 1 (texan-f1-austin) · loai: muse
- Hiện tượng: `scene1_start.png` sát video mẫu (mũ cao bồi, áo denim, phố gạch đỏ + dây đèn, robot giữa khung, đỉnh mũ ~8%); `scene1_cut.mp4` 4,8 s, Whisper nghe đúng 11/11 từ, môi mở khi nói, kết thúc về tư thế nghỉ, nền tĩnh. Áo denim thành kiểu gi-lê không tay (mẫu là sơ mi dài tay xắn): chấp nhận.
- Tốc độ nói 2,4 từ/giây (mẫu 4,0) dù prompt ghi "about 4 words per second".
- Cách sửa (nếu người dùng muốn nhanh hơn): nâng "Tốc độ tăng tối đa" trong Cài đặt Studio; không sửa kịch bản.
- Kết quả: ĐẠT (cảnh 1); các cảnh 2–6 + hậu kỳ: CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ (một nhân vật nhìn ống kính + khối khoá ~360 từ: khung đầu đúng bố cục ngay lần đầu, không cần refs).
- Đã chưng cất vào: SO-TAY mục 2 (dòng khuôn `robot-pho-tieng-long`).

### 2026-11-08 · robot-pho-tieng-long · lượt gen 1 hoàn chỉnh (6 cảnh + hậu kỳ) · loai: muse + hau-ky
- Hiện tượng 1: `final.mp4` 23,9 s; 4 thẻ và phụ đề karaoke bám đúng lời; nhưng **ô tiêu đề che mắt robot**: trong clip gen, mặt bắt đầu ở y≈322/1920 (mẫu ≈ 460) vì Muse đặt robot cao/gần hơn khung đầu một chút và mũ thấp hơn.
- Cách sửa 1: `post.py` dò mặt (Haar, 6 khung) → nếu đáy ô tiêu đề thấp hơn mép mặt − 24 px thì dời ô lên (`tieu_de_y_min` 110). Chạy lại hậu kỳ: tiêu đề y=163, không che mắt. ĐẠT.
- Hiện tượng 2: cảnh 3 Muse đọc "That means you. All of you. All of you." (lặp cụm cuối); kiểm lời của Studio không bắt vì mọi từ đều có mặt. Phụ đề vẫn đúng (căn theo từ của biến thể) nhưng tiếng thừa.
- Cách sửa 2: "Chỉ làm lại cảnh này" (POST /api/queue/redo {"only": true, "from": 3}) kèm ghi chú "Say the line exactly once". Kết quả: CHỜ KIỂM CHỨNG.
- Hiện tượng 3: tốc độ nói 2,4–3 từ/giây (mẫu 4,0). Chưa sửa; gợi ý nâng "Tốc độ tăng tối đa".
- Áp dụng chung?: (1) CÓ cho mọi hậu kỳ có ô chữ gần mặt: đo mặt trên video gen rồi mới đặt ô, không tin toạ độ video mẫu. (2) CÓ: kiểm lời nên bắt cụm ≥ 2 từ lặp liền nhau (đề xuất cho engine, chưa làm).
- Đã chưng cất vào: chưa.

### 2026-11-09 · robot-pho-tieng-long · làm lại riêng cảnh 3 + hậu kỳ lại · loai: muse + hau-ky
- Kết quả: cảnh 3 mới 3,5 s, lời đúng một lần ("Y'all. That means you, all of you."); `final.mp4` 23,0 s, tiêu đề tự dời lên trên mắt, thẻ/phụ đề đúng. ĐẠT.
- "Chỉ làm lại cảnh này" giữ cảnh 4–6; chỗ nối 3→4 chấp nhận được vì cả hai cảnh kết thúc/bắt đầu ở tư thế nghỉ giống nhau (một nhân vật đứng yên: rủi ro khựng thấp).
- Áp dụng chung?: CÓ (thể loại một nhân vật tư thế nghỉ cố định: làm lại riêng một cảnh an toàn hơn thể loại có hành động).
- Đã chưng cất vào: chưa.

### 2026-11-09 · robot-pho-tieng-long · 30 biến thể từ CSV + ảnh Drive · loai: cong-cu + kich-ban
- Cách làm: CSV → `cong-cu/_csv30.json`; tải 60 ảnh Drive bằng `uc?export=download&id=` (file < 25 MB tải thẳng, có nhánh confirm cho file lớn) về `anh/bt/`; xem 6 bảng ghép (PIL, 10 ảnh/bảng) để tả trang phục/nền; `tao_30_bien_the.py` sinh JSON, `refs` gắn cả `NGUOI_DAY` (robot) lẫn `NEN_PHO` (nền) – engine `attachments` chấp nhận token không phải nhân vật (chú thích bằng nhãn trường).
- Lỗi gặp: regex bang bắt nhầm cụm "F1 is coming to Texas" đứng TRƯỚC (câu gốc trong cột "Kiểu biến thể") → phải neo vào `thành "F1 is coming to ..."`.
- Kết quả: `kiem-tra --tai-anh` 0 lỗi; dự án `Giai-do-30-bien-the-4737` 30 biến thể đủ 2 ảnh. CHỜ KIỂM CHỨNG (chưa gen).
- Áp dụng chung?: CÓ (quy trình CSV + link Drive → refs; xem ảnh bằng bảng ghép thay vì mở 60 ảnh lẻ).
- Đã chưng cất vào: chưa.

### 2026-11-08 · check-hanh-ly-hindi · phân tích + tạo thể loại (nhân bản soi-hanh-ly-gia-su-ai) · loai: phan-tich
- Hiện tượng: video "oder 6.mp4" nói Gujarati xen tiếng Anh; Whisper (mặc định en, và tự dò `gu` 0,41) đều trả lời DẠNG DỊCH sang tiếng Anh, không chép được chữ Gujarati.
- Nguyên nhân: Whisper small yếu với Gujarati, có xu hướng dịch.
- Cách làm: cắt vùng phụ đề (y≈1010–1080 trên 720×1280) 2 khung/giây, ghép lưới `tile=2x28`, đọc chữ Gujarati từ hình; Whisper chỉ để lấy mốc giây và cao độ. Ô robot đo bằng mặt nạ màu nền xanh (x 0.662, y 0.013, w 0.300, h 0.253).
- Kết quả: ĐẠT (đủ 34 lượt, khớp phụ đề).
- Áp dụng chung?: CÓ: video ngôn ngữ ít tài nguyên (Gujarati, Tamil, Telugu...) → lấy lời từ phụ đề trên hình, không tin chữ Whisper.
- Đã chưng cất vào: chưa

### 2026-11-08 · (chung) · câu chữ Gujarati/Devanagari · loai: cong-cu
- Hiện tượng (đọc code, chưa gen): `speech_lang` chỉ biết en/es; `_speech_tokens` chỉ giữ chữ Latin → câu Gujarati bị báo "thừa từ" → gen lại 2 lần vô ích. Phụ đề Arial không có chữ Gujarati.
- Cách sửa: `engine.speech_lang` trả `gu`/`hi` theo dải Unicode; `speech_issues` trả None (bỏ kiểm từng chữ) cho câu đó; `hau_ky.py` đọc `phu_de.font` (config thể loại `"font": "Nirmala UI"`). Đốt thử phụ đề Gujarati + ô trắng + ❌ qua `phu_de.burn`: ĐẠT.
- Kết quả: CHỜ KIỂM CHỨNG (lượt gen thật đầu tiên; cần khởi động lại Studio để nạp engine mới).
- Áp dụng chung?: CÓ (mọi thể loại lời chữ Ấn Độ).
- Đã chưng cất vào: chưa

### 2026-11-08 · di-tru-aiva-ai · tạo thể loại từ CSV biến thể (nhân bản di-tru-gia-su-ai) · loai: kich-ban
- Hiện tượng: CSV "oder 7" = kịch bản di trú (gọi điện → cảnh sát → gia sư AI) + 20 biến thể hành khách nam/nữ, trẻ/già; link ảnh Google Drive.
  Tải ảnh: curl `uc?export=download` và `drive.usercontent.google.com/download` đều trả trang "Google Drive: Sign-in"; Chrome (support@nexax.global) báo "You need access".
- Cách làm: kịch bản mới (phần 2 bỏ robot vai, một góc; phần 3 15 lượt), đại từ hành khách bằng token `HE_HOC`/`HIM_HOC`/`VAI_HOC` để một kịch bản chạy cả nam và nữ;
  hành khách ≥ 50 tuổi thì người gọi là con trai thay vì bố. `kiem-tra`: 0 lỗi (cảnh báo fx 19 và "đầu dưới ô" giữ).
- Kết quả: CHỜ KIỂM CHỨNG (chưa gen). Sau khi người dùng mở quyền: `drive.usercontent.google.com/download?id=..&export=download&confirm=t` tải được 18/20 (WebP, đổi sang PNG); 2 file vẫn chặn.
  Nhập Studio: loại di-tru-aiva-ai-37c0 (Studio nhận HE_HOC/HIM_HOC là trường), dự án di-tru-aiva-ai-c663, 18 biến thể. Cần kiểm token đại từ có được thay đúng trong prompt gửi Muse.
- Áp dụng chung?: CÓ: link Drive trong CSV phải "Anyone with the link" mới tải tự động được; biến thể đổi giới → dùng token đại từ, không viết he/she trong kịch bản.
- Đã chưng cất vào: chưa

### 2026-11-08 · di-tru-aiva-ai · nút chạy báo "chưa điền: Tư thế khi nghe (HOC)" · loai: bien-the
- Hiện tượng: Studio từ chối chạy `hk-01`; biến thể chỉ có `NGHE_HOC@1`, `NGHE_HOC@2`, `NHIN_HOC@1`, `NHIN_HOC@2`, không có khoá gốc.
- Nguyên nhân: `runSelected` (ui/app.js) đòi mọi trường không tuỳ chọn có giá trị theo khoá gốc, không tính khoá `@phần`. `video-moi.py kiem-tra` không kiểm điều này nên báo 0 lỗi.
- Cách sửa: thêm `NHIN_HOC`, `NGHE_HOC` gốc trong `tao_bien_the.py` (giá trị cho phần 3); cập nhật 18 biến thể của dự án qua PUT API, chỉ thêm 2 khoá. Mô phỏng phép kiểm của nút chạy: 0 trường thiếu.
- Lần 1 chưa đạt: `runSelected` gọi `save()` TRƯỚC khi kiểm, trang đang mở giữ bản cũ nên ghi đè dữ liệu vừa PUT (file còn 0 khoá `NGHE_HOC`).
- Sửa lần 2: đặt `optional: true` cho `NGHE_HOC`, `NHIN_HOC` trong loại dự án (PUT types, không bị bản lưu của trang ghi đè), rồi PUT lại khoá gốc. Đọc `S.project` + `typ()` trên trang Studio vừa tải: 18 biến thể, 0 trường thiếu.
- Kết quả: CHỜ KIỂM CHỨNG (người dùng tải lại trang rồi chạy). Bài học: sửa dự án qua API khi trang Studio đang mở dễ bị ghi đè; cổng Studio đổi sau mỗi lần khởi động, đọc `userdata/running.json`.
- Áp dụng chung?: CÓ: mọi token có `@phần` phải có thêm khoá gốc. `di-tru-gia-su-ai` cũng chỉ khai khoá `@` nên chạy từ nút trong Studio có thể gặp lỗi này.
- Đã chưng cất vào: chưa

### 2026-11-08 · di-tru-aiva-ai · tiếng hát trong khoảng lặng sau tên app · loai: am-thanh
- Hiện tượng: hk-01 cảnh 15 (phan2/scene10_clip.mp4), sau "Aiva AI." có nốt ngân ~0,9 s, 253–266 Hz, -30 dB, phổ hoạ âm đều (giây 1,1–1,9). 14 clip còn lại không có.
- Nguyên nhân (suy luận): câu chỉ có tên app + dấu chấm tạo khoảng lặng ~1 s giữa clip 8 s, Muse lấp bằng giọng ngân; cue emo "happy, proud" có "voice is confident and full".
- Cách sửa: lời đổi thành "Aiva AI, I just practice..." + emo "confident" + dặn nói liền; thêm cấm hát/ngân vào VIDEO SUFFIX, NEGATIVE, Audio cả 3 phần. Lưới an toàn: `types/di-tru-aiva-ai/post.py` tắt đoạn < -22 dB có cao độ đều ≥ 0,6 s trước khi làm phụ đề.
- Kết quả: gen lại cảnh 15 (md5 khác, không dính đệm Muse): nói liền, không còn đoạn có cao độ trong khoảng lặng: ĐẠT trên 1 mẫu. Thử bước tắt trên phan2/raw.mp4 cũ: chỉ trúng 26,6–27,5 s, Whisper trước/sau giống hệt; quét 15 clip hk-01 không trúng nhầm. Hát to bằng lời nói thì bước tắt không bắt được.
- Áp dụng chung?: CÓ: tránh câu chỉ gồm tên riêng + dấu chấm ngay đầu lượt dài; cân nhắc đưa bước tắt vào `_chung/hau_ky.py` sau khi kiểm chứng thêm.
- Đã chưng cất vào: chưa

### 2026-11-08 · di-tru-aiva-ai · camera zoom giật ở phần 3, ô AI che mặt · loai: khung-hinh
- Hiện tượng: hk-01 cảnh 17 ("Más o menos", phan3/scene2_spk.mp4) Muse zoom nhảy bậc 1,0 → 1,33 → 1,67 (_zoom_of 1,40); bản khoá camera vỡ chân (lấp mép từ khung nối) và còn zoom vào/ra. Lọc đa thức bậc 2 trong `_camera_lock` không bù được bước nhảy.
- Nguyên nhân: ảnh tham chiếu toàn thân phông xanh → base_HOC vẽ toàn thân, trong khi prompt ghi "head to thighs" + "short-form social video look" + "light handheld": Muse zoom để khớp chữ (khớp mục 185 sổ tay).
- Cách sửa: prompt "MEDIUM SHOT... cuts across mid-thigh; knees, feet outside", "fixed tripod, one continuous shot, no punch-in", bỏ "short-form"/"handheld"; đứng bên trái (mặt ~30%, đầu và tóc trái vạch 55%). `types/di-tru-aiva-ai/gen.py` chen vào `head_span`: đầu chạm ô AI thì cắt mép trái ảnh nền rồi phóng lại (chỉ file của thể loại này; không cần khởi động lại Studio vì gen.py nạp mới mỗi lần chạy).
- Kết quả: gen lại từ cảnh 16: cảnh 17 zoom 1,005; mép phải mặt ≤ 48,7% (ô AI từ 61,5%); Muse vẫn vẽ lệch phải (60,7%) và bước căn đã đưa về 49,9%. ĐẠT trên 1 mẫu (2 clip).
- Áp dụng chung?: CÓ: ảnh tham chiếu toàn thân thì prompt phải nói rõ phần nào ra ngoài khung; câu tả khung phải khớp ảnh nền.
- Đã chưng cất vào: chưa
