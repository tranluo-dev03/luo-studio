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

### 2026-11-11 · robot-pho-tieng-long · 60 biến thể (bài học / Ấn Độ Hindi / Brazil) + ảnh Muse · loai: kich-ban + anh-tham-chieu + hau-ky
- Cách làm: `cong-cu/tao_60_bien_the.py` (20 bộ bài học dùng chung 3 nhóm), `gen_anh_60.py` (Muse gen robot nền xanh lá + nền trống từ chữ, 3 luồng, ~15 s/ảnh tính bình quân), `tao_trang_duyet.py` (trang duyệt HTML).
- Hậu kỳ chữ Ấn Độ: Pillow của runtime KHÔNG có raqm → không vẽ đúng Devanagari bằng PIL; thẻ dùng Hinglish chữ Latin, phụ đề Devanagari qua ASS (`ass=...:shaping=complex`, Nirmala UI). Chạy thử trên video giả: ĐẠT.
- Rủi ro đã thấy khi đọc code: `engine.voice_span` với câu "English! <Hindi>" coi câu trọn khi khớp từ tiếng Anh cuối → có thể cắt mất phần Hindi; `speech_lang` không nhận tiếng Bồ Đào Nha. CHƯA sửa (code chung, chờ người dùng).
- Kết quả: `kiem-tra` 0 lỗi cả 3 file. Muse gen video: CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ (câu trộn tiếng Anh + chữ Ấn Độ ở mọi thể loại: kiểm `voice_span` trước khi chạy cả nhóm).
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

### 2026-11-09 · chia-tren-duoi-marathi · phân tích video "oder 3" + tạo thể loại · loai: phan-tich
- Hiện tượng: video nói Marathi xen tiếng Anh; Whisper trả chữ dịch sang tiếng Anh (vd. "It's a matter of time" cho "कालची गोष्ट आहे"). `bao-cao.md` báo 4,24 từ/giây và tới 16,67 từ/giây vì đếm trên chữ dịch; bộ gom giọng 2 cụm xếp nhiều câu robot vào cụm của người học; `danh-gia` báo "có chuyển động máy" chỉ do cú chuyển sang end card; "mặt thứ 3/4" là nhận nhầm kệ/tay robot.
- Nguyên nhân: Whisper small yếu với ngôn ngữ Ấn Độ; số đo phái sinh từ chữ Whisper sai theo.
- Cách làm: lời đọc từ phụ đề trên hình qua `luot_NN.jpg`; tốc độ tính lại theo lời thật (~3 từ/giây); Hz đọc theo lượt đã biết người nói; đường chia đo bằng cạnh ngang trung vị nhiều khung (y 679/1280). Khung trên/dưới là "ghép 2 lớp", đặt `nen: DAY` vì `panel_clear_y` so toạ độ ảnh gốc của nền với ô khác, `nen: HOC` sẽ làm mặt người học bị coi là bị ô DAY che.
- Kết quả: `kiem-tra` 0 lỗi, 0 cảnh báo; đốt thử phụ đề Devanagari Nirmala UI ĐẠT; đã nhập Studio (loại `Chia-tren-duoi-Marathi-e194`, dự án `oder-3---Supernova-Marathi-7986`). Muse nói Marathi: CHỜ KIỂM CHỨNG (chưa gen, chờ ảnh tham chiếu người dùng).
- Áp dụng chung?: CÓ: video ngôn ngữ ít tài nguyên thì không dùng từ/giây và cụm giọng của công cụ; khung chia ngang dùng nhân vật ô TRÊN làm `nen`. Công cụ `danh-gia` chưa dò vạch chia NGANG (chỉ dò dọc), nên gợi ý nhầm "chung khung thật".
- Đã chưng cất vào: chưa

### 2026-11-09 · chia-tren-duoi-marathi · gắn ảnh robot, gen ảnh người học · loai: anh-tham-chieu
- Hiện tượng: người dùng gửi ảnh robot đầu trắng không tóc (khác robot video mẫu) và bảo tự gen ảnh người. `gen_anh_hoc.py` lần 1: HTTP 401 (script ngoài Studio không thấy khoá); lần 2 và 3: `CDP Storage.setCookies 超时` trên cả 5 tài khoản, `userdata/logs/api.log` có lỗi này ở dọn tài khoản và làm nóng tab từ ít nhất 22:14.
- Nguyên nhân: 401 do thiếu `MUSE2API_HOME=userdata\api` (đã sửa trong script). CDP: trình duyệt nền của LUO-API không trả lời (giả thuyết, chưa chứng minh).
- Cách làm / sửa: sửa `NGUOI_DAY` theo ảnh (không tóc), thêm câu "ảnh tham chiếu chỉ cho ngoại hình" ở cả hai `[NHAN VAT]`; `cong-cu/cap_nhat_studio.py` đẩy kịch bản + biến thể vào đúng dự án cũ (PUT, Studio tự tải refs).
- Kết quả: robot đã gắn vào dự án. Ảnh người học: CHƯA ĐẠT, chờ LUO-API hoạt động lại. Chạy thử: chưa.
- Áp dụng chung?: CÓ: script gen ảnh ngoài Studio phải đặt `MUSE2API_HOME`; lỗi CDP trên mọi tài khoản thì dừng gen, không thử lại nhiều lần.
- Đã chưng cất vào: chưa

### 2026-11-09 · chia-tren-duoi-marathi · ảnh người học do người dùng gửi · loai: anh-tham-chieu
- Hiện tượng: LUO-API vẫn lỗi CDP nên người dùng gửi ảnh qua prnt.sc: bác trai Ấn Độ ~65 tuổi, áo kurta kem, nền xanh lá.
- Cách làm / sửa: `NGUOI_HOC`, `GIONG_HOC` đổi theo ảnh (cùng giới nên giữ nguyên động từ Marathi); `[NHAN VAT HOC]` dặn bỏ nền xanh và tư thế đứng; bỏ script gen ảnh.
- Kết quả: `kiem-tra --tai-anh` đạt; dự án có đủ refs. Gen thật: CHỜ KIỂM CHỨNG (LUO-API lỗi CDP chưa xử lý).
- Áp dụng chung?: KHÔNG
- Đã chưng cất vào: chưa

### 2026-11-10 · chia-tren-duoi-bengali · phân tích video "oder 5" + tạo thể loại · loai: phan-tich
- Hiện tượng: video nói Bengali xen tiếng Anh; Whisper trả chữ dịch sang tiếng Anh ("Don't make it difficult" cho "এটাকে মুখস্থ করবেন না"). `bao-cao.md` báo tới 13,89 từ/giây vì đếm trên chữ dịch. `speech_lang` chưa biết chữ Bengali nên câu Bengali bị coi là tiếng Anh.
- Nguyên nhân (đã chứng minh): `_INDIC` trong engine chỉ có Gujarati và Devanagari.
- Cách làm / sửa: lời đọc từ phụ đề trên hình; tốc độ thật ~3,3 từ/giây. `engine.py`: thêm `bn` (chữ Bengali) vào `_INDIC` và vào nhánh bỏ kiểm từng chữ của `speech_issues`; chỉ ảnh hưởng câu có chữ Bengali.
- Kết quả: `kiem-tra` 0 lỗi, 0 cảnh báo; đã nhập Studio. Muse nói Bengali: CHỜ KIỂM CHỨNG (chưa gen, chờ ảnh tham chiếu người dùng).
- Áp dụng chung?: CÓ (mọi video chữ Bengali)
- Đã chưng cất vào: chưa

### 2026-11-10 · chia-tren-duoi-bengali · đốt thử phụ đề Bengali · loai: hau-ky
- Hiện tượng: đốt thử trên video mẫu, "কিন্তু" hiện như "কনি্তু", "করবেন" hiện như "করবনে". Thử thêm Devanagari và Gujarati: "किताब" hiện như "कतिाब", cùng lỗi.
- Nguyên nhân (đã chứng minh): bộ lọc `subtitles` mặc định dựng chữ đơn giản; so ba cách trên cùng một tệp ASS, chỉ `ass=...:shaping=complex` đúng.
- Cách làm / sửa: `phu_de.burn` thêm tham số `shaping`, `hau_ky` đọc `phu_de.shaping` trong `config.json`, mặc định tắt. Bật cho `chia-tren-duoi-bengali`.
- Kết quả: ĐẠT (đốt lại trên video mẫu, cụm chữ ghép đúng). `chia-tren-duoi-marathi` và `check-hanh-ly-hindi` có cùng lỗi, CHƯA sửa, chờ người dùng quyết định.
- Áp dụng chung?: CÓ (mọi thể loại phụ đề chữ Ấn Độ)
- Đã chưng cất vào: SO-TAY mục 6

### 2026-11-10 · chia-tren-duoi-bengali · chạy thử biến thể 01, Whisper treo ở tiếng Bengali · loai: cong-cu
- Hiện tượng: cảnh 1 mất 18 phút dù Muse gen clip chỉ 52 giây. Ba lần gọi Whisper hết 300 giây chờ: kiểm tra hướng mặt (không ghi log), tìm mốc lời lần 1 và lần 2.
- Nguyên nhân: Whisper `small` không trả lời khi `language=bn` hoặc tự nhận ngôn ngữ (thử riêng trên âm thanh cảnh 1: quá 60 giây); `language=hi` xong trong ~20 giây. Lý do bên trong mô hình chưa rõ.
- Cách làm / sửa: `engine.voice_span` với câu Bengali lấy mốc theo năng lượng âm thanh, không gọi Whisper; `postprocess.align_by_scene` nghe câu Bengali bằng `hi`.
- Kết quả: tìm mốc lời ĐẠT (10 giây ở cảnh 2 và 4). Căn phụ đề: CHỜ KIỂM CHỨNG. Cảnh 3 cảnh báo đầu câu có thể mất, cảnh 2 lời sát cuối clip 5 giây: CHỜ nghe lại.
- Áp dụng chung?: CÓ (mọi video chữ Bengali)
- Đã chưng cất vào: chưa

### 2026-11-10 · chia-tren-duoi-bengali · ảnh tham chiếu và kiểm tra hướng mặt trên robot · loai: anh-tham-chieu
- Hiện tượng: người dùng gửi robot trắng đầu không tóc, khác nhân vật hoạt hình của video mẫu; ảnh chàng trai do Muse gen từ lời tả theo yêu cầu người dùng. Khung đầu phần 1 đạt: hai người nhìn nghiêng, đúng ảnh tham chiếu. Cảnh 2 bị báo "quay mặt nhìn thẳng ống kính" hai lần dù ảnh ghép khung cho thấy robot chỉ xoay nhẹ.
- Nguyên nhân (giả thuyết): đo hướng mặt bằng mediapipe không tin cậy trên mặt robot.
- Cách làm / sửa: bỏ "never looks at the camera" khỏi `NHIN_NOVA`, `NGHE_NOVA` để tắt kiểm tra riêng cho robot; vẫn giữ "exact side profile" và cấm ở NEGATIVE. Người học giữ kiểm tra.
- Kết quả: ĐẠT ở phần 1 (cảnh 2-4 không còn gen lại vì hướng mặt, xong phần 1 lúc 01:59). Lượt chạy dừng ở cảnh 12/20 theo yêu cầu người dùng để quét mã độc trên máy, chưa có video thành phẩm.
- Áp dụng chung?: CÓ (nhân vật robot: không dùng "never looks at the camera" để tránh báo nhầm)
- Đã chưng cất vào: chưa

### 2026-11-10 · chia-tren-duoi-bengali · hậu kỳ treo ở câu Bengali, nguyên nhân Whisper · loai: cong-cu
- Hiện tượng: hậu kỳ chạy 15 phút chưa xong, toàn bộ ở tiến trình Whisper căn phụ đề. Câu tiếng Anh 10 giây, câu Bengali quá 100 giây; video có 18 câu chữ Bengali.
- Nguyên nhân (đo trên âm thanh cảnh 1): Whisper `small` với `language=bn` sinh một ký tự lặp vô nghĩa ("ༀ") tới hết độ dài cho phép, tỉ lệ nén 15,86. Chỉ riêng một lượt mất 16,3 giây; cấu hình mặc định còn thử lại ở nhiều nhiệt độ nên không xong sau 80 giây. Token hoá Bengali bình thường. Tự nhận ngôn ngữ cũng rơi vào đây. `hi` không kèm prompt xong trong 3-5 giây; `hi` kèm prompt chữ Bengali quá 100 giây (lý do chưa đo).
- Cách làm / sửa: `postprocess.align_by_scene` không gửi câu chữ Bengali cho Whisper, phụ đề căn theo khoảng lời đã cắt sát của cảnh.
- Kết quả: ĐẠT (hậu kỳ 104 giây, có final). Độ khớp phụ đề từng câu: CHỜ người dùng xem.
- Áp dụng chung?: CÓ (mọi video chữ Bengali)
- Đã chưng cất vào: chưa

### 2026-11-10 · chia-tren-duoi-bengali · phụ đề Bengali hiện muộn, có video thành phẩm · loai: hau-ky
- Hiện tượng: sau khi bỏ Whisper, câu Bengali hiện muộn và quá ngắn (câu 14 từ chỉ 1,8 giây). Đang hậu kỳ mà gọi /api/post lúc item "tự xếp lại hàng chờ" đang ghép: lượt ghép bị dừng, raw.mp4 còn 48 byte.
- Nguyên nhân (đã chứng minh): `align()` chỉ đọc chữ Latin nên lấy mốc theo mấy từ tiếng Anh trong câu.
- Cách làm / sửa: `align_by_scene` rải thẳng câu Bengali theo độ dài chữ trong khoảng lời của cảnh. raw.mp4 hỏng: bấm chạy tiếp item gen, Studio ghép lại từ các scene_cut, không gen lại.
- Kết quả: ĐẠT (final 79,4 s). Video mẫu 58,8 s nên bản gen dài hơn ~20 s. Muse nói Bengali nghe được qua Whisper `hi`. CHỜ người dùng duyệt: khớp phụ đề, môi robot đỏ dần, cảnh 2 có thể hụt chữ cuối.
- Áp dụng chung?: CÓ (mọi video chữ Bengali; đừng gọi /api/post khi item đang chờ tự chạy lại)
- Đã chưng cất vào: chưa

### 2026-11-10 · chia-tren-duoi-bengali · bộ 20 biến thể theo CSV · loai: kich-ban
- Hiện tượng: CSV người dùng (tên ghi 40, thực có 20 dòng, chưa có link ảnh) đổi lời: phần 1 robot nói hết, app Aiva AI, bỏ vài câu; người học nam/nữ, trẻ/già.
- Cách làm / sửa: kịch bản riêng `KICH-BAN-...-ROBOT-MO-DAU.txt` (phần 1 không dùng đại từ của người học, phần 2 lấy nguyên), `cong-cu/tao_bo_csv.py` sinh cả kịch bản và biến thể. Tuổi trong câu sửa lỗi theo từng biến thể (`TUOI_THEO_BIEN_THE`).
- Kết quả: `kiem-tra` 0 lỗi, 0 cảnh báo. Chưa gen: CHỜ ảnh người học. Rủi ro chờ kiểm chứng: phần 1 chỉ robot nói, người thật có thể nhép theo, nhất là biến thể nữ.
- Áp dụng chung?: KHÔNG (riêng thể loại này)
- Đã chưng cất vào: chưa

### 10/11/2026 — chia-tren-duoi-bengali: chạy 20 biến thể, 4 luồng (kiểm tra cảnh đầu)
- **Hiện tượng:** bt-01 (nam-25-so-mi-trang) cảnh 1–2 xong sau ~2 phút mỗi cảnh; khung cuối `scene1_last.png`, `scene2_last.png`: robot nói, người học nhìn nghiêng, miệng khép, không nhép theo robot; ảnh người học khớp ảnh tham chiếu `bien-the/01.png`.
- **Nguyên nhân/cách sửa:** phần 1 robot nói cả 4 lượt (kịch bản ROBOT-MO-DAU) nên người học chỉ nghe, tránh lỗi Muse gán giọng.
- **Kết quả:** ĐẠT ở 2 cảnh đầu bt-01; bt-02..04 và các cảnh sau CHỜ KIỂM CHỨNG. Riêng thể loại. Chưa chưng cất.

### 10/11/2026 — chia-tren-duoi-bengali: tổng kết lô 20 biến thể (máy 6 nhân/16 GB/HDD, 2→4→5→6 luồng)
- **Số đo:** 20/20 video xong, 03:53–12:26 = 8 h 33 phút (kể cả 7 video chờ lỗi WinError 32 nhiều giờ và 1 lần Studio bị tắt làm dừng 2 video). Video chạy liền mạch 67–86 phút; chậm nhất 132–158 phút (bt-06, bt-19, bt-20, do tranh tài khoản/chạy lại).
- **Theo cảnh (TB):** phần 1 robot 62 s/cảnh (trung vị 29 s); phần 2 người nói 265 s/cảnh; clip nghe 176 s/cảnh (max ~1000 s). Hậu kỳ + ghép TB 8,4 phút (max 23).
- **Vấn đề:** WinError 32 (file đang bị tiến trình khác dùng) ở bước ghép cảnh 16 của 7 video; Studio mở lại thì số luồng về 2; hai video cùng tài khoản Muse.
- **Kết quả:** CHỜ KIỂM CHỨNG chất lượng từng video; áp dụng chung (độ dài/luồng); chưa chưng cất.

### 2026-11-09 · chia-tren-duoi-marathi · 40 biến thể từ CSV "Horizontal HINDI" (đổi Aiva AI -> Talka AI) · loai: bien-the
- Hiện tượng: CSV có 40 dòng (mô tả người học + mô tả nền tiếng Việt, link ảnh người học + link ảnh nền) và lời thoại Marathi (Robot/Nam, 18 lượt).
- Cách làm: `cong-cu/tao_bien_the_40.py` (bảng ANH = bản tiếng Anh các mô tả, đọc link từ CSV); refs `NGUOI_HOC` = ảnh người, `NEN_HOC` = ảnh nền (token kết thúc _HOC nên chỉ gửi cho người học). Kịch bản viết cho người học NAM: 18 biến thể NỮ đổi động từ nói về người học (गेली होतीस, कशी, म्हणालीस). Tạo loại + dự án qua API với timeout dài (tải 80 ảnh Drive).
- Kết quả: CHỜ KIỂM CHỨNG (chưa gen). Tải được 80/80 ảnh Drive, 0 lỗi, đều là WebP hợp lệ; Studio chưa thử gửi ảnh nền kèm NEN_HOC.
- Áp dụng chung?: CÓ: `video-moi.py nhap` có timeout 120 s, CSV nhiều ảnh thì gọi API trực tiếp với timeout dài.
- Đã chưng cất vào: chưa

### 2026-11-10 · quet-an-ninh-day-chuyen · nhập thể loại từ thư mục Drive NHIPTY · loai: nhap-studio
- Hiện tượng: người dùng chỉ đường dẫn thư mục Drive đã có sẵn kịch bản + biến thể + 4 ảnh refs (nhân bản từ soi-hanh-ly-gia-su-ai, bản không bé).
- Cách làm: chép thư mục vào `SAMPLE/quet-an-ninh-day-chuyen/`; `kiem-tra` báo LỖI thiếu `app/production/types/quet-an-ninh-day-chuyen/gen.py` nên tạo `gen.py`, `post.py`, `config.json` bằng cách sao từ soi-hanh-ly-gia-su-ai (đổi tên loại); nhập Studio (loại `QUET-AN-NINH-CO-THE---DAY-CHUYEN-c421`, dự án `quet-an-ninh-day-chuyen-a018`, 1 biến thể, 28 lượt).
- Kết quả: `kiem-tra` 0 lỗi, 3 cảnh báo (nghe/nói ở phần 2, đầu dưới ô); không có refs lỗi. Chưa gen thật: CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ: thư mục thể loại nhận từ ngoài thiếu code riêng thì sao 3 file từ thể loại gốc trước khi kiểm tra.
- Đã chưng cất vào: chưa

### 2026-11-10 · quet-an-ninh-day-chuyen · cảnh 1: nhân viên đứng SAU cổng, máy báo lúc cô bước qua · loai: kich-ban
- Hiện tượng: người dùng yêu cầu cảnh đầu nhân viên đứng sau cổng dò, máy chỉ báo khi hành khách vừa bước qua (trước đó nhân viên đứng TRÁI cạnh cổng, bà đã qua cổng rồi mới báo).
- Cách làm / sửa: sửa `cong-cu/tao_kich_ban.py` (WIDE[1], PRE[1], ANGLE P, CAM_PAN, mô tả VN cảnh 1), sinh lại kịch bản, đẩy vào loại dự án qua PUT /api/types.
- Kết quả: `kiem-tra` 0 lỗi. Gen thật: CHỜ KIỂM CHỨNG. Các cảnh 3+ (góc A/C) vẫn để nhân viên TRÁI cạnh cổng nên có thể lệch vị trí khi cắt.
- Áp dụng chung?: KHÔNG
- Đã chưng cất vào: chưa

### 2026-11-10 · quet-an-ninh-day-chuyen · Muse dựng sai cảnh 1 (nhân viên đứng trong/cạnh cổng, cô gái đứng cạnh cổng) · loai: kich-ban
- Hiện tượng: `scene1_wide.png` nhân viên đứng cạnh cổng phía trước, cô đứng ngoài cổng; `scene1_pre_start.png` nhân viên đứng TRONG khung cổng, cô đứng ngoài. Lời "BEHIND the gate" mơ hồ nên Muse hiểu sai.
- Cách làm / sửa: viết lại WIDE[1], PRE[1] theo hình học rõ: máy quay chính diện cổng, cô ở TRONG ô cổng đang bước qua, nhân viên cách cổng ~2 m phía xa, cổng nằm giữa ông và máy quay, "không ở trong, không ở trước cổng". Đẩy kịch bản vào Studio, gen lại từ cảnh 1 bằng `POST /api/queue/redo {id, from:1}`.
- Kết quả: CHỜ KIỂM CHỨNG (đang gen lại).
- Áp dụng chung?: CÓ: gen lại từ cảnh n dùng queue/redo, không add lượt mới (lượt mới dùng lại ảnh cũ).
- Đã chưng cất vào: chưa

### 2026-11-11 · quet-an-ninh-day-chuyen · 40 biến thể từ CSV "Sân bay_Quét an ninh" (nữ + nam) · loai: bien-the
- Hiện tượng: CSV 40 biến thể (mô tả người học tiếng Việt, link ảnh prnt.sc/Drive, đổi "visiting my daughter" thành brother/husband/mother/son/wife/sister). 20 biến thể là NAM nhưng kịch bản viết cho nữ (~175 chỗ she/her).
- Cách làm: `cong-cu/tao_bien_the_40.py` (bảng ANH = bản tiếng Anh các mô tả); kịch bản đổi she/her/herself thành token SHE, SHE_CAP, HER, HER_CAP, HER_OBJ, HERSELF (sinh trong tao_kich_ban.py), biến thể gốc điền sẵn đại từ nữ, biến thể nam điền he/his/him và các trường mô tả cũng đổi. "Ma'am" -> "Sir" cho nam; "I have/am 48" theo tuổi. Dự án mới `quet-an-ninh-day-chuyen-40-bien-the-93d3`, nhập bằng API timeout dài.
- Kết quả: `kiem-tra` 0 lỗi; Studio tải đủ 40 ảnh, 0 refs lỗi. Biến thể 16-20 và 31-35 có em bé địu (kịch bản gốc không em bé): CHỜ KIỂM CHỨNG khi gen. Gen thật: chưa.
- Áp dụng chung?: CÓ: kịch bản dùng chung cho cả hai giới thì đại từ hành khách phải là token; "her" đứng trước dấu câu là tân ngữ (him), còn lại là sở hữu (his).
- Đã chưng cất vào: chưa

### 2026-11-11 · split-screen-vertical-x0042 · 20 biến thể nhân vật từ CSV X0042 (chia đôi + gia sư AI) · loai: bien-the
- Hiện tượng: CSV 20 biến thể (mô tả người Mexico tiếng Việt, link Drive); BT 8-10 đổi "I am 28" thành 35, BT 16-20 thành 68 (phụ đề tự theo).
- Cách làm: dự án mới `SAMPLE/split-screen-vertical-x0042/`, tải 20 ảnh từ Drive bằng `uc?export=download&id=` (tải thẳng được, đều là webp) vào `anh/nhan-vat/`, refs trỏ tệp trong dự án. `cong-cu/tao_bien_the.py` có bảng BIEN_THE tiếng Anh (bỏ đồ nửa dưới), hàm `giong()` sinh giọng; lời thoại từ `luot(tuoi)`.
- Kết quả: JSON 20 biến thể hợp lệ, 15 lượt đúng thứ tự, đúng 1 wrong/1 right, token kịch bản đủ. Chưa nhập Studio, chưa gen.
- Áp dụng chung?: CÓ: CSV có link Drive thì tải về tệp cục bộ để dự án không phụ thuộc quyền chia sẻ.
- Đã chưng cất vào: chưa

### 2026-11-11 · split-screen-vertical-x0045-pt · 20 biến thể Brazil, lời thoại tiếng Bồ Đào Nha, chia đôi dọc · loai: bien-the
- Hiện tượng: CSV X0045 có kịch bản Bồ Đào Nha (chỉ "How old are you?", "I have/I am N" tiếng Anh), 20 biến thể (10 nữ, 10 nam) mỗi biến thể một tuổi N khác nhau; có link Drive.
- Cách làm: dự án `SAMPLE/split-screen-vertical-x0045-pt/`, tải 20 ảnh Drive vào `anh/nhan-vat/`. Loại mới `app/production/types/chia-doi-gia-su-ai-pt/` (bản sao hậu kỳ, whisper `small` vì `small.en` chỉ tiếng Anh). Kịch bản đổi VOICE/VIDEO SUFFIX sang tiếng Bồ Đào Nha, "Obrigada/Obrigado" theo giới, nền và đồ bàn đổi sang Brazil. Lượt 13 rút còn 20 từ.
- Kết quả: `kiem-tra` 0 lỗi 0 cảnh báo; nhập Studio (dự án `X0045-Split-screen-vertical-PT-20-bien-the-4715`), ảnh đã gắn. Gen thật: chưa, CHỜ KIỂM CHỨNG giọng Bồ Đào Nha và căn phụ đề.
- Áp dụng chung?: CÓ: thể loại nói ngôn ngữ khác tiếng Anh phải tạo loại hậu kỳ riêng có `"whisper": "small"`; câu giới tính ("Obrigada/o") sinh theo giới trong script biến thể, không để cố định.
- Đã chưng cất vào: chưa

### 2026-11-11 · split-screen-vertical-x0043-hi · 20 biến thể Ấn Độ, lời thoại tiếng Hindi, chia đôi dọc · loai: bien-the
- Hiện tượng: CSV X0043 có kịch bản Hindi (Devanagari; "How old are you?", "I have/I am N", Talka AI, AI Tutor tiếng Anh), 20 biến thể (10 nữ, 10 nam), mỗi biến thể một tuổi N; link Drive.
- Cách làm: dự án `SAMPLE/split-screen-vertical-x0043-hi/`, tải 20 ảnh Drive vào `anh/nhan-vat/`. Loại mới `app/production/types/chia-doi-gia-su-ai-hi/` (whisper `small`, font Nirmala UI cho Devanagari). Lượt 12 chia động từ theo giới (रही/रहे). Lượt 13 rút 25 -> 18 từ (giới hạn 20).
- Kết quả: `kiem-tra` 0 lỗi 0 cảnh báo; nhập Studio (`X0043-Split-screen-vertical-HI-20-bien-the-067c`), ảnh đã gắn. Gen thật: chưa, CHỜ KIỂM CHỨNG giọng Hindi và phụ đề Devanagari.
- Áp dụng chung?: CÓ: ngôn ngữ chia động từ theo giới (Hindi, Bồ Đào Nha) thì sinh câu theo giới trong script biến thể; câu gốc quá 20 từ phải rút trước khi nhập.
- Đã chưng cất vào: chưa

### 2026-11-11 · split-screen-vertical-x0039-baihoc · 20 biến thể Brazil, bài học "Where are you from?", tiếng Anh, chia đôi dọc · loai: bien-the
- Hiện tượng: CSV X0039 có kịch bản tiếng Anh mới (quê thay cho tuổi: "I am Mexico." sai, "I'm from Mexico." đúng), nhưng bảng 20 nhân vật và cột "đổi I am 28 thành I am N" y hệt X0045 (sót). Ảnh Drive giống hệt X0045.
- Cách làm: dự án `SAMPLE/split-screen-vertical-x0039-baihoc/`, kịch bản từ bản tiếng Anh X0042 (loại `chia-doi-gia-su-ai`, whisper small.en), giọng người học thêm giọng Brazil; biến thể từ script X0045 đổi `luot(PLACE, gioi)`. Quê giữ "Mexico" theo kịch bản dù nhân vật Brazil (biến `PLACE`).
- Kết quả: `kiem-tra` 0 lỗi 0 cảnh báo; nhập Studio (`X0039-Split-screen-vertical-BAI-HOC-20-bien-the-5d20`), ảnh đã gắn. Gen thật: chưa. CHỜ NGƯỜI DÙNG xác nhận quê Mexico hay Brazil.
- Áp dụng chung?: CÓ: CSV cùng bảng nhân vật dùng lại cho nhiều kịch bản thì cột "kiểu biến thể" có thể sót, đối chiếu với kịch bản trước khi áp.
- Đã chưng cất vào: chưa

### 2026-11-11 · split-screen-vertical-x0044-botskin · 20 biến thể Brazil + robot đổi trang phục theo biến thể, tiếng Bồ Đào Nha · loai: bien-the
- Hiện tượng: CSV X0044 y hệt X0045 (nhân vật, tuổi, lời thoại) nhưng thêm cột "Link ảnh AI": 20 ảnh robot, cùng một robot mặc trang phục khác nhau (khăn turban, mũ cao bồi, poncho...), nền xanh lá.
- Cách làm: dự án `SAMPLE/split-screen-vertical-x0044-botskin/`, tải 20 ảnh nhân vật + 20 ảnh robot (`anh/robot-skin/`); ghép ảnh robot thành bảng để xem rồi viết `TRANG_PHUC_ROBOT` (tiếng Anh) nối vào `NGUOI_DAY` từng biến thể; `refs.NGUOI_DAY` trỏ ảnh robot riêng. Kịch bản thêm câu "nền xanh lá của ảnh robot KHÔNG thuộc cảnh". Dùng lại loại `chia-doi-gia-su-ai-pt`.
- Kết quả: `kiem-tra` 0 lỗi 0 cảnh báo; nhập Studio (`X0044-Split-screen-vertical-BOT-skin-20-bien-the-976a`), ảnh đã gắn. Gen thật: chưa, CHỜ KIỂM CHỨNG robot mặc đúng trang phục và nền xanh không lọt vào cảnh.
- Áp dụng chung?: CÓ: ảnh tham chiếu robot đổi theo biến thể thì phải đổi cả mô tả `NGUOI_DAY` (mô tả trắng thuần mâu thuẫn với ảnh); xem ảnh bằng bảng ghép 10 ảnh/ lần thay vì từng ảnh.
- Đã chưng cất vào: chưa

### 2026-11-12 · split-screen (X0042/X0043/X0045) · lỗi chồng nền ở nửa AI + người/AI quá cỡ · loai: ky-thuat
- Hiện tượng: cảnh ghép 2 lớp nối khung (`noi: lien`): (1) nửa robot hiện thêm một đầu robot / vòng hào quang thứ hai phía trên, dải đen/vệt ở đáy (BT2 X0045 từ cảnh 3, BT19-20 X0042); (2) nhân vật to gấp 1,6-2 lần (X0045 BT13 nửa người dùng, X0043 BT6 cảnh 9-11) hoặc robot to/nhỏ x1,2-1,4 giữ nguyên tới hết video.
- Nguyên nhân: (1) `align_to_tail` căn khung đầu clip về khung nối bằng phép thu nhỏ/dời rồi lấp phần mép hụt bằng chính khung nối (cỡ khác) -> lộ đầu cũ chồng lên; clip Muse gốc (`sceneN_spk.mp4`) vẫn sạch, chỉ bản `_khop` hỏng. (2) Mọi kiểm tra cỡ cũ (`_start_mismatch`, `face_under_panels`) dùng Mediapipe nên KHÔNG đo được robot, và chỉ so với khung nối nên lệch cộng dồn không bị thấy.
- Cách sửa (`app/luo-studio/split.py`): `_cover_fix` luôn phóng thêm cho phủ kín khung (không lấp mép bằng khung nối); bỏ phép căn khung nối nếu lệch tới mức hụt mép (>6%) và không hoà khung nối khi khác cỡ; `size_dev` đo cỡ cả khung so với ẢNH GỐC bằng ORB (không cần dò mặt), lệch > `SIZE_MAX` (1,10) thì gen lại cảnh từ ảnh gốc 1 lần, giữ bản ít lệch hơn (cả clip nói và clip nghe). Tắt được bằng opts `check_size`.
- Cách kiểm cảnh đã gen: ORB đo cỡ nửa khung so với ảnh gốc (1,00 = đúng cỡ; <0,9 hoặc >1,1 là lỗi) cộng ảnh ghép `sceneN_last.png`.
- Kết quả: sửa xong code; gen lại các cảnh lỗi: xem dòng cập nhật bên dưới. CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ: mọi thể loại ghép 2 lớp nối khung.
- Đã chưng cất vào: chưa
- Cập nhật 2026-11-12: đã khởi động lại Studio bằng code mới và xếp gen lại 15 video từ cảnh lỗi đầu tiên (X0042 BT13/15/18/19/20; X0043 BT1/3/6; X0045 BT2/3/6/7/9/13/15). X0045 BT17 chưa có trong hàng đợi. CHỜ KIỂM CHỨNG kết quả gen lại.
### 2026-11-11 · tiem-thit-tieng-anh · tạo thể loại · loai: phan-tich / kich-ban / cong-cu
- Hiện tượng: (1) video 177 s song ngữ: `--lang es` dịch câu tiếng Anh sang tiếng Tây Ban Nha ("That's a beautiful cut" → "Eso es un bonito cut", "my meat delivery didn't come" → "mi teléfono no salió"), không bỏ đoạn như du-lich-chia-doi; (2) `danh-gia` báo 13 "đổi cơ chế" giả: chỉ là cắt giữa cận một người và trung cảnh hai người (không có PiP); (3) `video-moi.py kiem-tra` báo "cảnh: 0" khi tiêu đề cảnh là `CẢNH n: Lượt n` (thiếu mốc thời gian); (4) dòng `===== PHAN 1 =====` duy nhất làm kịch bản thành "nhiều phần" (đòi gen.py + "phan").
- Nguyên nhân: (1) Whisper ép ngôn ngữ thì dịch thay vì bỏ khi câu ngắn xen kẽ; (2) gợi ý khuôn dựa trên số mặt theo giây; (3) parser cần `CẢNH n (m:ss–m:ss): Lượt n`; (4) có dòng chia phần là chế độ nhiều phần.
- Cách làm / sửa: chạy thêm `phan-tich-video.py --lang en` trên bản sao video, phân người nói theo phụ đề (dòng trắng EN + dòng vàng ES = câu tiếng Anh). Bỏ dòng chia phần, ghi chú đặt trong khối [HAU KY]. `tao_kich_ban.py` sinh mốc thời gian giả 5 s/cảnh. Khuôn: cảnh thường nhiều góc, một phần; giọng AI do robot trên màn hình điện thoại nói (góc P không thấy mặt người) thay vì giọng ngoài khung ở cảnh cận Tavo.
- Kết quả: `kiem-tra` 0 lỗi, 0 cảnh báo. Chưa gen: CHỜ ảnh tham chiếu TAVO/TIO/KHACH/CHU + Studio chưa mở (chưa nhập). Rủi ro chờ kiểm chứng: robot nhép trên màn hình điện thoại (cảnh 22/24/26), cân màu kéo sáng cảnh đêm, ông chú + Tavo cùng khung.
- Áp dụng chung?: CÓ cho (1) (video song ngữ: luôn chạy cả hai ngôn ngữ, Whisper có thể DỊCH chứ không chỉ bỏ) và (3)(4) (định dạng kịch bản một phần); KHÔNG cho phần khuôn.
- Đã chưng cất vào: chưa

### 2026-11-11 · tiem-thit-tieng-anh · ảnh tham chiếu Muse + chạy thử cảnh 1–2 · loai: anh-tham-chieu / muse / cong-cu
- Hiện tượng: (1) `gen_anh_tham_chieu.py` (chép từ canh-sat) lỗi HTTP 401 "缺少 Authorization": `G.read_key()` không thấy khoá vì bản cài này để khoá ở `userdata/api/.env`; (2) "LUO Studio.bat" chạy qua `Start-Process cmd /c` ẩn cửa sổ không lên, chạy thẳng `.venv\Scripts\pythonw.exe app\launcher.py` thì lên (~1 phút mới có running.json); (3) 4 ảnh nhân vật gen chỉ từ chữ (mô tả NGUOI_ của biến thể + nền xám, Pixar), đúng ngoại hình, không chữ; (4) chạy thử: `scene1_start.png` (góc K) và `scene2_start.png` (góc A) bám rất sát bố cục video mẫu, đúng mặt theo ảnh tham chiếu; clip 1 (3,6 s) và 2 (4,5 s) nói đúng lời, ông chú vỗ ngực đúng hành động, Tavo cúi nhìn thớt, khách ở góc A chỉ thấy vai + gáy.
- Cách làm / sửa: script đặt `MUSE2API_ENV_FILE=userdata/api/.env` nếu có; mỗi nhân vật một phiên Muse riêng.
- Kết quả: ĐẠT (ảnh tham chiếu, cảnh 1–2). Còn nhỏ: cuối cảnh 1 khách xoay mặt gần về ống kính (EYE LINE ghi nhìn sang trái). Cảnh 3–37 CHỜ KIỂM CHỨNG (đặc biệt 6 B, 10 C, 21 N, 22 robot trên điện thoại).
- Áp dụng chung?: CÓ cho (1)(2) (script gọi LUO-API ngoài Studio phải tìm khoá ở `userdata/api/.env`; mở Studio bằng pythonw launcher) và (3) (gen ảnh tham chiếu từ chính mô tả NGUOI_ của biến thể để prompt và ảnh khớp).
- Đã chưng cất vào: chưa

### 2026-11-11 · tiem-thit-tieng-anh · Studio tắt giữa chừng · loai: studio
- Hiện tượng: chạy thử dừng sau cảnh 13/37 (scene13_last.png 11:21:39); Studio (pid 9704) và LUO-API (pid 4968) cùng mất, không có log lỗi (studio-loi.log không đổi, api.log dừng 11:21:18), không có sự kiện crash trong Windows; `userdata/running.json` còn sót.
- Nguyên nhân (đã đối chiếu giờ): Studio do agent mở từ shell của Claude → là tiến trình con của app Claude; app Claude khởi động lại (mọi tiến trình `claude` mới bắt đầu 11:23:13) → kill cả cây tiến trình, Studio chết theo. Không phải lỗi Studio.
- Cách sửa: mở Studio tách khỏi Claude (người dùng tự mở "LUO Studio.bat", hoặc `explorer.exe "...\LUO Studio.bat"`), rồi chạy tiếp biến thể (Studio dùng lại scene1..13 đã có).
- Kết quả: CHỜ KIỂM CHỨNG (sau khi mở lại).
- Áp dụng chung?: CÓ (mọi lần agent tự mở Studio)
- Đã chưng cất vào: chưa

### 2026-11-11 · tiem-thit-tieng-anh · chạy tiếp sau khi Studio tắt + duyệt cảnh 3–13 · loai: studio / muse
- Hiện tượng: người dùng tự mở lại Studio; hàng đợi trống (không lưu qua lần tắt). `POST /api/queue/add` + `/api/queue/start` lại cùng biến thể → engine dùng lại scene1..13 có sẵn, gen tiếp từ cảnh 14 (log "Cảnh 14: gen ảnh khung đầu"). Cảnh 3–13: Whisper khớp đủ 11 câu (EN và ES); góc B ra rộng hơn mô tả "close two-shot" (thấy cả quầy) nhưng đúng vị trí; đồng xu ở cảnh 7 nhỏ, khó thấy; cảnh 13 Tavo (người nghe) xoè tay đầu clip.
- Kết quả: ĐẠT (chạy tiếp; lời cảnh 1–13). Các cảnh sau CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ (Studio tắt giữa chừng: mở lại rồi thêm lại đúng biến thể vào hàng đợi, không cần xoá gì)
- Đã chưng cất vào: chưa

### 2026-11-11 · phong-van-pho-malayalam · tạo thể loại · loai: phan-tich / kich-ban / code-chung
- Hiện tượng: (1) video tên "interview street hindi" nhưng lời và phụ đề là MALAYALAM; `danh-gia --lang hi` cho 2 "câu" chữ Devanagari vô nghĩa (cả phần 2 dồn vào một câu 29 s), số từ/giây và cụm giọng vô dụng; (2) đếm mặt báo "đổi cơ chế" ở 4,83 s và 14,13 s: thật ra là cảnh chèn cận/đổi cỡ trong cùng góc qua vai, cơ chế chỉ đổi ở 25,7 s (vạch cam chia trên/dưới); (3) đo chuyển động miệng ô trên vô dụng (robot mẫu cử động liên tục), ô dưới thì phân biệt rõ lúc người bán nói; (4) engine chưa biết chữ Malayalam → câu Malayalam bị coi là 'en' và kiểm lời từng chữ bằng small.en.
- Cách làm / sửa: chép lời bằng cách cắt dải phụ đề (y 590–720) mỗi 0,25 s, chỉ giữ khung đổi chữ, xếp 14 khung/ảnh rồi đọc; ai nói ở phần 2 theo chuyển động miệng ô dưới. Engine: `_INDIC` thêm `ml` (U+0D00–0D7F), `voice_span` lấy mốc theo năng lượng như Bengali, `speech_issues` bỏ kiểm từng chữ. Kiểm thử ffmpeg `ass:shaping=complex` + Nirmala UI: chữ Malayalam ghép đúng.
- Kết quả: `kiem-tra --tai-anh` 0 lỗi 0 cảnh báo. Chưa gen: CHỜ ảnh tham chiếu phóng viên + người bán.
- Áp dụng chung?: CÓ cho (1)(3) (video ngôn ngữ Ấn Độ: xem chữ phụ đề trước khi chọn --lang; cắt dải phụ đề để chép lời; dùng ô của người thật để đo ai nói) và (4) (thêm chữ viết mới vào `_INDIC`).
- Đã chưng cất vào: chưa

### 2026-11-11 · tiem-thit-tieng-anh · chạy thử xong biến thể đầu (37 cảnh) · loai: muse / hau-ky / studio
- Hiện tượng: final.mp4 143 s 1080x1920 (gen 10:52–12:39, trừ ~7 phút Studio tắt). Whisper khớp lời mọi cảnh đã kiểm (1–26) cả EN lẫn ES; mặt 4 nhân vật + robot giữ ổn qua 15 góc. Cảnh đêm (21–26) giữ tối, cân màu không kéo sáng. Robot nói trên màn hình điện thoại (22/24/26): nhép miệng, không giao diện. Hậu kỳ: 44 dòng dịch, phụ đề trắng viền đen đúng vị trí.
- Còn lỗi nhỏ: dòng dịch đỏ nhỏ khó đọc (kiểu cố định của `_chung/phu_de.py`); nền sau điện thoại ở góc P là quầy thịt đèn vàng chứ không phải kho tối; cảnh 36/37 màn hình điện thoại có nhãn chữ nhỏ dưới robot; cảnh 29 Studio báo "vẫn lỗi lời nói sau 2 lần gen lại" (thiếu "ni") nhưng giữ bản tốt nhất; 2 lần WinError 32 (cảnh 32, 34) ở `engine.crun` → `subprocess.Popen` khi gọi ffmpeg cân màu (khởi chạy exe bị chặn, nghi phần mềm diệt virus quét ffmpeg.exe), Studio tự chạy lại được.
- Kết quả: ĐẠT (biến thể đầu chạy trọn). Chưa gắn Thương hiệu/Outro.
- Áp dụng chung?: CÓ: (a) giọng AI do robot trên màn hình điện thoại nói, không thấy mặt người → không bị người nhép giọng AI; (b) WinError 32 là lỗi khởi chạy tiến trình, không phải file cảnh bị giữ.
- Đã chưng cất vào: chưa

### 2026-11-11 · phong-van-pho-malayalam · ảnh tham chiếu + nhập Studio · loai: anh-tham-chieu / studio
- Hiện tượng: người dùng yêu cầu Muse gen ảnh phóng viên + người bán, robot dùng ảnh robot Talka (`xe-tai-canh-sat-gia-su-ai/anh/ai-robot-talka.png`). `gen_anh_tham_chieu.py` (chép từ tiem-thit, đổi sang ảnh thật) ra 2 ảnh 9:16 đầu gối trở lên, nền xám: đúng áo caro hồng + ba lô + kính + râu; đúng áo cánh hồng + sari caro nâu + bindi. Người bán ra già hơn mô tả (~55 thay vì 48) → sửa mô tả theo ảnh để prompt Muse và ảnh không mâu thuẫn.
- Kết quả: ĐẠT (ảnh tham chiếu). Nhập Studio: `Phong-van-pho-Malayalam-9ba6` / `Interview-street-Malayalam---Talka-d5f1`, refs tải đủ 3 ảnh, `QUAY_LUNG_PV` có trong biến thể. Chạy thử biến thể 01: CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ (ảnh tham chiếu gen từ chữ lệch tuổi → sửa mô tả theo ảnh, không gen lại nếu ảnh khác vẫn đạt)
- Đã chưng cất vào: chưa

### 2026-11-11 · phong-van-pho-malayalam · chạy thử phần 1 (11 cảnh) · loai: muse / studio / code-chung
- Hiện tượng: (1) khung đầu cảnh 1 rất sát video mẫu (góc qua vai phải, PV chỉ lộ viền má + gọng kính, người bán ba phần tư, xe đẩy inox), 11 cảnh PV luôn quay lưng, người bán giữ mặt; biển hiệu nền mờ không đọc được. (2) Cảnh tiếng Anh cắt sát đúng (1,1–6,8 s). Cảnh Malayalam (1,3,5,7,9,11) dài đúng 5,0 s, log "không nhận ra đủ lời để cắt sát": còn 2–3 s im lặng đuôi (cảnh 3: một từ "ഉടനെ" trong 5 s). (3) Cảnh 11 (14 từ Malayalam) nói tới giây cuối clip 5 s → có thể cụt câu. (4) Cao độ: cảnh PV 143–174 Hz (nam), người bán 197–333 Hz: không nhầm giọng.
- Nguyên nhân: (2) Studio mở TRƯỚC khi sửa engine.py → vẫn chạy code cũ (speech_lang 'en', Whisper small.en). Chạy `_energy_span` mới trên chính các clip: ra mốc đúng (cảnh 1: 0–2,57 s). (3) `gen_video.spoken_syllables` chỉ đếm chữ Latin → câu Malayalam = 0 âm tiết → `auto_duration` không dùng, clip 5 s.
- Cách sửa: `spoken_syllables` cộng thêm âm tiết chữ Malayalam (nguyên âm độc lập + phụ âm không có virama); thử: câu 3 âm tiết → 5 s, 43 âm tiết → 10 s, tiếng Anh không đổi. Cần khởi động lại Studio để nạp engine.py + gen_video.py, rồi cắt lại cảnh 1,3,5,7,9 (xoá scene*_cut/_last, giữ scene*_clip) và gen lại cảnh 11.
- Kết quả: CHƯA ĐẠT (cắt sát + độ dài clip Malayalam) → CHỜ KIỂM CHỨNG sau khi khởi động lại. Hình phần 1: ĐẠT.
- Áp dụng chung?: CÓ: sửa code dùng chung thì phải khởi động lại Studio trước lượt gen; ngôn ngữ chữ viết mới phải kiểm cả `speech_lang` (engine) lẫn `spoken_syllables` (gen_video).
- Đã chưng cất vào: chưa

### 2026-11-11 · tiem-thit-tieng-anh · sửa theo góp ý người dùng (bản 46 cảnh, cảnh không lời) · loai: kich-ban / code-chung / hau-ky
- Hiện tượng: người dùng xem bản 37 cảnh, chê 10 điểm: (1) cảnh 2 "Twenty years, my friend!" còn ~1,5 s im sau lời; thiếu các nhịp KHÔNG LỜI của video mẫu: Tavo ngơ ngác ấp úng ~3 s, bà chủ vào chợ tìm quầy, chặt thịt dài + nhanh và gói thịt nhanh (trước "Oh my God, ten minutes"), hôn trán (trước "You saved me today"), montage học nhiều ngày (sau "Again tomorrow"); "I'm sorry" phải là "I'm sorry, I don't speak Spanish"; cảnh "Aquí, siéntese" phải vội vã; app đổi Talka AI; "Me salvaste hoy" phải ngỡ ngàng.
- Nguyên nhân: (1) `engine.voice_span`: Whisper nghe đủ câu, hết lời 2,76 s, nhưng quy tắc "tiếng còn tiếp sau từ khớp cuối thì nới tới hết tiếng theo năng lượng" (thêm cho câu Tây Ban Nha bị Whisper bỏ sót từ cuối) nới tới 4,2 s vì tiếng cười/thở. Các điểm còn lại: bản 37 cảnh bỏ/gộp cảnh không lời vì Studio chưa có đường chạy thật cho cảnh không lời (lượt rỗng vẫn bị SPEAKER MAP bảo "có người nói", `turn_text` trả câu nói rỗng).
- Cách sửa: (a) `voice_span`: không nới khi từ khớp cuối chính là từ cuối của câu (đo lại cảnh 2: 0–2,76 s; câu Tây Ban Nha vẫn nới như cũ). (b) Cảnh không lời: `variant_values` cho lượt "text" rỗng → token rỗng; vòng gen: lượt rỗng + Voice trống → `mute_prompt` (bỏ câu có say/speak/talk/voice/lời/nói/giọng, thêm lệnh SILENT CLIP lên đầu), negative bỏ mục speech/voice + thêm "speech; talking...", không SPEAKER MAP, clip không track tiếng thì thêm tiếng lặng; trường mới `Cắt còn: N` / `Tua: K` (`gen_video.FIELDS`, `engine.mute_trim`, thử trên clip thật: 5 s → 3,5 s; tua 1,3 → 3,9 s). (c) `video-moi.py kiem-tra` đếm lượt rỗng là cảnh không lời. (d) `types/tiem-thit-tieng-anh/post.py`: hau_ky dùng chung đánh số lượt có lời liên tục (lượt có lời i = cảnh i) → map lại về đúng cảnh (kiểm: "You see? Nothing." → cảnh 7, "Talka AI." → cảnh 22). (e) Kịch bản 46 cảnh: 9 cảnh không lời (T, X, D2, Y, E hôn trán, Q1–Q4 chớp trắng), mô tả không dùng từ bị lọc (lần đầu "as if to say", "KHÔNG LỜI", "định nói" làm mất cả câu ACTION/diễn biến → đổi từ).
- Kết quả: kiem-tra 0 lỗi 0 cảnh báo ("37 lượt có lời + 9 cảnh không lời = 46 cảnh"); dựng prompt khô cả 9 cảnh không lời đủ ACTION + diễn biến, Voice rỗng, 0 âm tiết. CHƯA gen thật bản 46 cảnh → CHỜ KIỂM CHỨNG (cần khởi động lại Studio để nạp engine.py + gen_video.py).
- Áp dụng chung?: CÓ: (a) cảnh không lời dùng lượt rỗng + `Cắt còn`/`Tua` cho mọi thể loại cảnh thường; (b) hành động TRƯỚC câu nói → cảnh không lời riêng + cảnh có lời nối khung; (c) mô tả cảnh không lời tránh từ về nói/giọng; (d) hậu kỳ dùng chung chưa biết lượt rỗng → thể loại có cảnh không lời phải map lại (hoặc sửa `hau_ky.py` khi có thể loại thứ hai cần).
- Đã chưng cất vào: SO-TAY-KY-THUAT.md §3.5 (dòng cảnh không lời + hành động trước câu nói); PROMPT-CHO-AGENT.txt (lỗi hay gặp)

### 2026-11-11 · phong-van-pho-malayalam · hậu kỳ treo ở Whisper căn phụ đề · loai: hau-ky / code-chung
- Hiện tượng: gen xong 26 cảnh lúc 15:18, hậu kỳ (`types/phong-van-pho-malayalam/post.py` → `postprocess.align_by_scene` → `--_whisper_windows`, mô hình "small") chạy 25 phút chưa xong, tiến trình Whisper ăn ~1000 giây CPU. Ngoài ra cảnh 11 (clip 5 s) còn tiếng nói tới khung cuối → cụt câu (xác nhận).
- Nguyên nhân: `align_by_scene` chỉ bỏ qua Whisper cho câu chữ Bengali; câu Malayalam vẫn được đưa vào Whisper "small" kèm prompt Malayalam dài → giải mã lặp rất chậm, mà kết quả cũng không dùng được (align() chỉ đọc chữ Latin).
- Cách sửa: `app/production/postprocess.py` hai chỗ regex Bengali thêm dải Malayalam U+0D00–0D7F: đoạn Whisper rỗng, phụ đề rải theo độ dài chữ trong khoảng lời đã cắt sát. Chỉ ảnh hưởng câu có chữ Malayalam. Dừng hậu kỳ treo; xoá scene{1,3,5,7,9}_cut/_last, toàn bộ scene11_*, raw.mp4 → Studio tự xếp lại, chạy lại với code mới (đã khởi động lại 14:57).
- Kết quả: CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ: ngôn ngữ chữ viết mới phải kiểm 3 chỗ: `engine.speech_lang`/`voice_span`, `gen_video.spoken_syllables`, `postprocess.align_by_scene` (bỏ Whisper nếu Whisper không nghe được).
- Đã chưng cất vào: chưa

### 2026-11-11 · phong-van-pho-malayalam · xoá nhầm làm gen lại clip phần 1 · loai: studio / quy-trinh
- Hiện tượng: muốn "cắt lại" cảnh 1,3,5,7,9 (giữ scene*_clip) nhưng Studio gen lại cả khung đầu cảnh 1 và clip các cảnh đó; khung đầu cảnh 1 mới khác bố cục cũ (gần hơn, xe đẩy khác) → có thể giật hình ở chỗ cắt cảnh 1→2.
- Nguyên nhân: tôi xoá cả `scene{n}_cut.mp4` ở THƯ MỤC CHẠY (cấp trên). `types/_chung/nhieu_phan.py` thấy file cắt cấp trên mất thì xoá MỌI `phan{k}/scene{l}_*` của cảnh đó (cả clip, cả start) để gen lại. Thêm: xoá file cắt của cảnh ĐÃ được duyệt qua trong lượt đang chạy làm thiếu file khi ghép (cảnh 2: phải cắt lại tay bằng `engine.voice_span` + `smart_cut` từ clip còn giữ).
- Cách đúng: video nhiều phần muốn CẮT LẠI (không gen) → chỉ xoá `phan{k}/scene{l}_cut.mp4` + `_last.png`, GIỮ file cấp trên (engine cắt lại từ clip rồi `_link` ghi đè file cấp trên). Muốn GEN LẠI cảnh → xoá file cấp trên. Không xoá file của cảnh khi Studio đang chạy qua nó.
- Kết quả: ĐẠT (đã hiểu cơ chế); lượt này mất 6 lần gen thừa (cảnh 1,3,5,7,9 + khung đầu cảnh 1).
- Áp dụng chung?: CÓ (mọi thể loại nhiều phần).
- Đã chưng cất vào: chưa

### 2026-11-11 · phong-van-pho-malayalam · góp ý người dùng sau bản 130 s · loai: hau-ky / studio / code-chung
- Hiện tượng: người dùng chê (1) phần 1 còn nhiều khoảng trống; (2) phụ đề 0–40 s phải xuống thấp, gần đáy; (3) cảnh không liền mạch, giật nhiều; (4) phần 2 hiện quá nhiều chữ một lúc. Đo: giật khung cuối→khung đầu cảnh sau (trung bình |Δ| ảnh 90x160) 54/28/28/33/21 ở 1→2, 3→4, 5→6, 7→8, 9→10, các chỗ khác 4–16.
- Nguyên nhân: (3) cảnh lẻ bị gen lại (mục "xoá nhầm") còn cảnh chẵn vẫn nối từ khung cuối bản cũ của cảnh lẻ → chuỗi nối khung đứt. (1) cut_margin mặc định 0,5 s. (4) phụ đề theo câu.
- Cách sửa: (3) gen lại tuần tự cảnh 2–11 (xoá file cắt cấp trên cảnh 2–11; cảnh 1 chỉ xoá phan1/scene1_cut+last để cắt lại). (1) `types/phong-van-pho-malayalam/gen.py`: cut_margin ≤ 0,2. (2) config `y_theo_phan` "1": 1560. (4) `types/_chung/hau_ky.py` thêm tuỳ chọn `cum_tu_theo_phan` (`chia_cum`: chia dòng đã căn giờ thành cụm ≤ N từ, chia đều, giờ theo số ký tự; dòng có dịch/tô từ/fx giữ nguyên); config "2": 3. Phần 2 cảnh 15, 22 (cắt bằng code cũ, dư 7 s / 3 s): chỉ xoá phan2/scene{4,11}_cut+last để cắt lại từ clip nói có sẵn.
- Kết quả: CHỜ KIỂM CHỨNG (hàng đợi 4794b117).
- Áp dụng chung?: CÓ: (a) sửa lại MỘT cảnh giữa chuỗi nối khung thì mọi cảnh sau trong chuỗi phải gen lại, không thì giật; (b) `cum_tu_theo_phan` dùng được cho thể loại nào có phụ đề 1–3 từ như video mẫu.
- Đã chưng cất vào: chưa

### 2026-11-11 · phong-van-pho-malayalam · kết quả sửa theo góp ý (bản 105 s) · loai: studio / hau-ky
- Hiện tượng: sau khi gen lại cảnh 2–11 tuần tự: giật giữa cảnh còn 3–14 (trước 21–54): ĐẠT. Phụ đề phần 1 ở đáy, phần 2 cụm ≤ 3 từ: ĐẠT. Nhưng cảnh 3, 5, 6, 8 vẫn 4–5 s (lời ~0,5–1,4 s), cảnh 15 vẫn 10 s, tổng 138 s.
- Nguyên nhân: (a) cut_margin 0,2 tôi đặt → engine hi = max(0,3, margin+0,05) = 0,3, lo = 0,18 → cửa sổ tìm điểm cắt đúng 0,12 s, phép so `>= 0.12` trượt vì làm tròn số → `smart_cut` giữ cả clip (thử lại trên cảnh 5 với mốc lời đúng 0,42–1,78: ra 4,7 s). (b) `engine._energy_span` lấy mức tiếng nói theo phân vị 90: câu Malayalam rất ngắn ("ഉടനെ", 0,3 s trong clip 5 s) thì phân vị 90 vẫn là nền → None; thêm điều kiện câu ml phải > 0,5 s.
- Cách sửa: không cắt lại đuôi (đứt nối khung) mà TUA NHANH khoảng lặng đầu/giữa/cuối, giữ khung đầu + khung cuối: `SAMPLE/phong-van-pho-malayalam/cong-cu/nen_khoang_lang.py` (mức tiếng nói theo phân vị 99,5; bỏ tiếng động lẻ < 0,3 s; giữ 0,2 / 0,35 / 0,3 s; bản gốc lưu `*_cut.truoc-nen.mp4`), rồi xoá raw/final và cho Studio ghép + hậu kỳ lại (3 phút). gen.py: cut_margin ≤ 0,3 (không thấp hơn).
- Kết quả: ĐẠT về số đo: 137,6 s → 105 s, phần 1 53 s → ~33 s. Chưa có ý kiến người dùng.
- Áp dụng chung?: CÓ: (a) cut_margin < 0,3 làm hỏng cắt sát ở mọi thể loại (lỗi biên trong smart_cut, chưa sửa engine); (b) muốn bớt khoảng trống ở clip đã nối khung thì tua nhanh, không cắt đuôi; (c) `_energy_span` hụt câu rất ngắn trong clip dài (chưa sửa engine).
- Đã chưng cất vào: chưa

### 2026-11-11 · tiem-thit-tieng-anh · chạy thử bản 46 cảnh (cảnh không lời) · loai: muse / studio / code-chung
- Hiện tượng: final.mp4 172 s 1080x1920 (dự án Tiem-thit---Tavo-46-canh-f51c, gen 15:08–17:01, song song với một video Malayalam của phiên khác); log không có cảnh báo/lỗi mức warn ngoài cảnh 6 gen lại 1 lần (Muse tự cắt sang góc khác, Studio phát hiện "máy trôi") và cảnh 5 cắt lại rộng hơn (Whisper nghe tên "Tavo" sai). 9 cảnh không lời đều ĐẠT: 6 Tavo ấp úng (3,5 s, không tiếng, chỉ một tiếng "uhh" rất nhỏ), 11 bà chủ tìm quầy trong chợ (máy đứng yên), 17 chặt thịt nhanh (7,8 s sau tua x1,3), 18 gói thịt (3,9 s), 24 hôn trán, 32–35 montage. Phụ đề đúng cảnh nhờ post.py map lại; "Talka AI", "I'm sorry, I don't speak Spanish", cảnh 28 ngỡ ngàng đúng.
- Còn lỗi nhỏ: cảnh 18 thấy đỉnh đầu Tavo (dặn chỉ có tay) và chồng gói thịt có sẵn 4 gói từ đầu; cảnh 11 bà chỉ đi ngang chứ không bước về phía máy; cảnh 32 màn hình điện thoại có robot; cảnh 35 đèn sáng hơn "sáng sớm"; dòng dịch vẫn đỏ nhỏ; chưa gắn Thương hiệu/Outro.
- Kết quả: ĐẠT (đường cảnh không lời chạy thật lần đầu). Cắt đuôi sau "Twenty years, my friend!" đã sửa (xem mục trước).
- Áp dụng chung?: CÓ: cảnh không lời (lượt rỗng + Cắt còn/Tua) dùng được cho mọi thể loại cảnh thường; Studio chạy hai mục hàng đợi cùng lúc được; mở lại Studio sau khi sửa engine mới nạp code.
- Đã chưng cất vào: SO-TAY-KY-THUAT.md §3.5 (đã bỏ chữ "chưa gen thật" ở bước sau)

### 2026-11-11 · phong-van-pho-malayalam · bỏ tua nhanh, cắt sát theo lời (gen lại 4–11, rồi 9–11) · loai: studio / code-the-loai
- Hiện tượng: người dùng chê bản tua nhanh khoảng lặng "không tự nhiên, không được tua nhanh". Trả lại 19 bản cắt gốc, xoá `nen_khoang_lang.py`. Studio mặc định cũng tua quãng ngắt >= 0,55 s (speedfix, tối đa x2).
- Cách sửa: `types/phong-van-pho-malayalam/gen.py`: speedfix=False, cut_margin 0,3, và trong lúc chạy thể loại thay `E.voice_span` bằng `_span_ml` (năng lượng; mức lời theo phân vị 99,5; gộp nghỉ < 0,25 s; bỏ tiếng lẻ < 0,3 s cách > 0,8 s; sau quãng lặng >= 1 s bỏ phần còn lại nếu < 0,8 s hoặc nhỏ hơn lời chính >= 8 dB) cho MỌI câu (Whisper báo từ cuối "Otherwise." trễ 2 s). Thử trên clip: ഉടനെ 5 → 0,75 s, Otherwise 4,1 → 1,0, Therefore 5 → 1,0.
- Gen lại 4–11 (cắt lại 3): 120 s, giật giữa cảnh 3–17. Cảnh 8 còn 5 s (ồn nền -30..-36 dB sau lời bị tính là lời) → thêm điều kiện "nhỏ hơn 8 dB", cắt lại 8, gen lại 9–11.
- Kết quả: ĐẠT về số đo (hàng đợi 5c539137): 116 s, phần 1 35 s, cảnh 8 còn 1,0 s; không tua nhanh. Chỗ 10→11 đổi cỡ cảnh (Muse zoom dần trong cảnh 10, cảnh 11 về cỡ rộng). Chờ người dùng duyệt.
- Áp dụng chung?: CÓ: (a) không tua nhanh (bộ nhớ khong-tua-nhanh-video); (b) cắt sát đầu clip nối khung ("head" của smart_cut) cũng làm lệch khung nối nhẹ (2→3: 17); (c) mốc Whisper từ cuối không đủ tin để cắt sát câu một từ.
- Đã chưng cất vào: chưa

### 2026-11-11 · taxi-gia-su-ai · phân tích + kịch bản (thể loại mới) · loai: phan-tich / kich-ban / code-the-loai
- Hiện tượng: video mẫu 95 s song ngữ (taxi + gara tiếng Anh, phòng khách + phần AI tiếng Tây Ban Nha). `danh-gia` (Whisper en) dịch luôn câu Tây Ban Nha sang tiếng Anh ("Papá, ¿qué pasó?" → "Papa, what happened?") thay vì bỏ đoạn; phải chạy thêm `phan-tich-video.py --lang es` vào thư mục khác và đối chiếu phụ đề trên hình. Robot AI giọng 160–200 Hz bị gom chung cụm "A" với các giọng nam.
- Video gốc có 5 cảnh không lời trong phần cảnh thường của dự án NHIỀU phần; `nhieu_phan.plan` lọc `text.strip()` nên lượt rỗng biến mất → số cảnh phần 1 lệch.
- Cách làm: biến thể đặt `"text": "[KHONG LOI]"` (MARKER); `types/taxi-gia-su-ai/gen.py` bọc `engine.run_variant` đổi đúng MARKER thành "" trước khi engine chạy (clip câm như tiem-thit); `post.py` bỏ lượt MARKER khỏi phụ đề. Không sửa code dùng chung. Thử bằng code thật (giả run_variant): phần 1 25 lượt, rỗng ở 7/10/11/13/21; phụ đề 47 dòng, không dòng MARKER, cảnh câm không có phụ đề.
- Kết quả: CHỜ KIỂM CHỨNG (lượt gen thử đầu tiên). `kiem-tra`: 0 lỗi, 0 cảnh báo (đã đổi emo impatient/frustrated/annoyed/sad → từ trong EMO_CUES).
- Áp dụng chung?: CÓ (nếu gen thật đạt): (a) Whisper ép "en" trên đoạn Tây Ban Nha có thể DỊCH chứ không bỏ → luôn chạy ngôn ngữ thứ hai khi phụ đề trên hình là ngôn ngữ khác; (b) cảnh không lời trong dự án nhiều phần: dùng MARKER + gen.py, hoặc sửa `nhieu_phan.plan` giữ lượt rỗng (code chung, chưa làm).
- Đã chưng cất vào: chưa
### 2026-11-11 · taxi-gia-su-ai · chạy thử lần 1, cảnh 1 · loai: muse / kich-ban
- Hiện tượng: `scene1_start.png` sát video mẫu (góc qua kính chắn gió: tài xế to bên phải, khách nhỏ ở ghế sau trái). Nhưng `phan1/scene1_clip.mp4`: Muse giữ khung đầu ~1,5 s (tài xế chớp mắt, không nói) rồi TỰ CẮT sang bố cục khác: khách ở giữa ghế sau, tài xế quay lưng mép trái; khách nói đúng lời. Studio (`start_jump`/`hold_after_jump`) giữ đoạn sau cú cắt → `scene1_cut.mp4` 5,1 s bố cục mới, chuỗi nối khung cảnh 2–6 sẽ lệch khung đầu góc A.
- Nguyên nhân (giả thuyết mạnh): người nói (khách) quá nhỏ, ở hậu cảnh, trong khi người to tiền cảnh im → Muse "đạo diễn lại" cho người nói làm chủ thể. Cùng nhóm hiện tượng với "Muse gán giọng cho mặt nhìn thấy".
- Cách sửa: dừng riêng mục hàng đợi (`POST /api/stop {"id"}`); thêm góc A2 = đúng bố cục Muse tự chọn (khách giữa ghế sau, chỉ thấy gáy/vai tài xế) cho mọi câu của khách (cảnh 1 ảnh mới, cảnh 3 `Khung đầu từ cảnh: 1`, 4–6 nối khung); câu tài xế (cảnh 2) giữ góc A với `Prompt ảnh` riêng; negative thêm "a cut to another camera angle". Chép kịch bản đè `userdata/studio/types/Taxi-gia-su-AI-a6ce.txt`, đổi tên thư mục chạy cũ thành `-lan1-loi-cat-goc`, chạy lại mục 83bafa6f.
- Kết quả: CHỜ KIỂM CHỨNG (lần chạy 2).
- Áp dụng chung?: CÓ (nếu lần 2 đạt): người nói nhỏ ở hậu cảnh trong khi người im to ở tiền cảnh → Muse tự cắt góc giữa clip; cho người nói làm chủ thể khung (người im chỉ thấy gáy/vai).
- Đã chưng cất vào: chưa
### 2026-11-11 · taxi-gia-su-ai · người dùng bác góc A2 / góc J qua vai · loai: kich-ban / phan-hoi
- Hiện tượng: lần chạy 2 dùng góc A2 (khách giữa ghế sau, tài xế quay lưng) để né lỗi Muse tự cắt góc ở lần 1. Người dùng: "tại sao cảnh 1 lại ngồi như vậy? hãy bám sát cảnh, bố cục, vị trí nhân vật trong video gốc".
- Nguyên nhân: mình tự đổi bố cục để giảm rủi ro Muse mà không hỏi; người dùng ưu tiên bám video gốc hơn né rủi ro.
- Cách sửa: bỏ góc A2; mọi cảnh taxi dùng góc A như gốc; cảnh 2–6 dùng `Khung đầu từ cảnh: 1` (mỗi clip bắt đầu lại từ đúng bố cục gốc, clip nào Muse cắt góc thì không lan sang cảnh sau, và gen lại riêng clip đó); góc A khoá "ONE continuous shot… never cuts, never moves closer to the back seat"; negative "a cut to another camera angle". Góc J cũng bỏ "qua vai", về đúng gốc: hai người đối mặt cùng lộ mặt. Dùng lại `scene1_start.png` của lần 1 (đúng bố cục gốc).
- Kết quả: CHỜ KIỂM CHỨNG (lần chạy 3).
- Áp dụng chung?: CÓ: KHÔNG tự đổi bố cục/vị trí nhân vật so với video gốc để né rủi ro Muse; nếu cần thì hỏi người dùng trước. Né bằng cách khác (khung đầu từ cảnh, khoá máy, gen lại clip lỗi).
- Đã chưng cất vào: chưa
### 2026-11-11 · taxi-gia-su-ai · lần chạy 3: cảnh câm 7 bị điền câu của quản lý · loai: code-the-loai
- Hiện tượng: cảnh 1–6 ĐẠT (bố cục gốc giữ suốt clip nhờ `Khung đầu từ cảnh: 1` + khoá "ONE continuous shot", lời đúng, Whisper khớp). Cảnh 7 (góc P, câm) có `{{LUOT_7}}` = câu "Arjun, your ratings…" của lượt 8; `phan.json` phần 1 chỉ 20 cảnh (đáng ra 25).
- Nguyên nhân (đã chứng minh): `gen.py` thay `engine.run_variant` cho CẢ tiến trình Studio. Lần chạy đầu sau khi mở Studio thì đúng, nhưng từ lần thứ hai trong cùng tiến trình, lệnh gọi gốc của Studio (`server.gen_item` → `E.run_variant`) cũng đi qua hàm bọc → MARKER thành "" TRƯỚC `custom_gen` → `nhieu_phan.plan` bỏ lượt rỗng → lượt sau dồn lên.
- Cách sửa: hàm bọc chỉ đổi MARKER khi `opts["_part"]` (nhieu_phan gọi cho một phần). Thử: nạp gen.py 2 lần, gọi gốc giữ 5 MARKER, gọi phần đổi 5. Khởi động lại Studio (bỏ bản bọc cũ trong bộ nhớ), giữ cảnh 1–6, chuyển cảnh 7+ sang `taxi-mexico-goc-lan3-cam-lech`, chạy tiếp.
- Kết quả: CHỜ KIỂM CHỨNG (lần chạy 4).
- Áp dụng chung?: CÓ: thể loại monkeypatch hàm engine phải gắn điều kiện (chỉ khi `_part` / chỉ thư mục thể loại mình), vì Studio chạy mọi dự án trong cùng một tiến trình và hàm đã thay tồn tại tới khi tắt Studio.
- Đã chưng cất vào: chưa
### 2026-11-11 · taxi-gia-su-ai · lần chạy 4: phần 1 xong 25 cảnh · loai: muse / studio
- Hiện tượng: 25/25 cảnh phần 1 xong (18:41–19:27). Lời 20 cảnh có lời đều đúng (Whisper; câu ngắn "Papá, ¿qué pasó?", "Nada, hija." phải ép `es`). 5 cảnh câm đúng chỗ (7, 10, 11, 13, 21), độ dài theo `Cắt còn` (3 / 2,5 / 2 / 3 / 2 s), tiếng nền -15..-17 dB; riêng cảnh 13 có tiếng đỉnh -1,7 dB (cần nghe). Bố cục khớp gốc: taxi qua kính chắn gió giữ suốt 6 cảnh; gara 3 người, trao khoá, taxi mới; cảnh 12 hai người đối mặt (không thấy tài xế nhép theo trên ảnh ghép); phòng khách L/L2/L3; cận điện thoại robot (robot hoạt hình đơn giản, không chữ).
- Lệch nhỏ: cảnh 22–25 điện thoại sang tay bố và màn hình tối (gốc con gái cầm, màn hình robot). Phần 2: `base_HOC` bị ô che lần đầu → Studio gen lại rồi dịch xuống (`.che1.png`, `.truoc-dich.png`), kết quả đạt.
- Kết quả: ĐẠT (phần 1). Xác nhận: MARKER + điều kiện `_part` chạy thật; `Khung đầu từ cảnh: 1` giữ được bố cục khi người nói nhỏ ở hậu cảnh.
- Áp dụng chung?: CÓ: (a) cảnh không lời trong dự án nhiều phần bằng MARKER chạy được; (b) người nói nhỏ ở hậu cảnh: dùng lại nguyên khung đầu cho mọi cảnh cùng góc + khoá "one continuous shot, never reframes on whoever speaks" thay vì đổi bố cục.
- Đã chưng cất vào: chưa### 2026-11-11 · taxi-gia-su-ai · lần chạy 4: phần 2 + video hoàn chỉnh · loai: muse / studio
- Hiện tượng: phần 2 xong 18 cảnh, `final.mp4` 152,9 s (gốc 95 s, phần 1 ~83 s vì mỗi cảnh dài hơn gốc ~1–1,5 s, phần 2 ~69 s; khoảng lặng > 0,7 s chỉ 5 chỗ ≤ 1,1 s → không tua). Ghép 2 lớp đạt: robot trắng trong ô bo góc, tài xế hai tay vô lăng nhìn ống kính, viền đỏ + ❌ ở "I am Mexico", ✅ xanh ở "I am from Mexico", 💲 ở "no tengo dinero", phụ đề vàng; phần 1 ô trắng + dòng dịch, cảnh câm không phụ đề. Whisper: 17/18 câu phần 2 đúng; cảnh 28 (phần 2 cảnh 3) robot lặp "Where are you? Are you from? Where are you from?" (clip 6,8 s). Cảnh 13 câm: đỉnh -9,7 dB trong video cuối (không phải tiếng nổ).
- Nguyên nhân: Muse tự lặp/ấp úng câu tiếng Anh ngắn sau câu Tây Ban Nha trong cùng lượt (giả thuyết).
- Cách sửa: xoá `scene28_cut.mp4` + `_last.png` cấp trên (nhieu_phan xoá `phan2/scene3_*`), cất `final.mp4` cũ vào `_cu-canh28/final-lan4.mp4`, chạy lại mục 83bafa6f để gen lại riêng cảnh đó.
- Kết quả: ĐẠT. Clip mới 3,8 s, Whisper ép `en` nghe "¿De dónde eres? Where are you from?" (ép `es` thì phiên âm câu Anh thành "¿Dónde eres?", đừng tin), phụ đề hai dòng đúng; `final.mp4` 149,9 s. Các cảnh khác dùng lại, không gen lại.
- Mẹo kiểm: câu song ngữ trong một lượt phải chạy Whisper cả `es` và `en`.
- Áp dụng chung?: CHƯA RÕ (cần thêm lần lặp mới kết luận câu song ngữ trong một lượt hay bị lặp).
- Đã chưng cất vào: chưa

### 2026-11-12 · tiem-thit-tieng-anh · bản 50 cảnh (sửa theo góp ý lần 2) · loai: muse / kich-ban / studio
- Hiện tượng (góp ý người dùng sau bản 46 cảnh): (1) "Tío, dijo que hoy me pagaba la semana" phải do Tavo nói; (2) chặt + gói thịt phải nhanh, chuyên nghiệp hơn; (3) cảnh bà chủ cảm ơn / hôn trán: trên nóc tủ phải là các gói thịt Tavo vừa gói; (4) sau "Again tomorrow" là nhiều cảnh nhanh Tavo vừa làm việc vừa học bằng app; (5) thêm cảnh bà chủ "No, the young guy." trước "Tú, cállate"; (6) bà chủ vui mừng, nhẹ nhàng ở mọi cảnh nói với Tavo về sau.
- Nguyên nhân (1): Muse gán giọng cho MẶT NHÌN THẤY: cảnh 9 Tavo quay nghiêng miệng gần khép (emo "hesitant" có chữ "lips press"), ông chú nhìn thẳng Tavo → môi ông chú mấp máy theo lời Tavo (đã thấy trong clip bản 46 cảnh). Thể loại không đo được vì hai người cùng nhãn vị trí "behind-counter".
- Cách sửa: (1) Tavo mặt 3/4 hướng máy, miệng cử động rõ, emo "hopeful, worried"; ông chú "nhìn xuống đồng xu, môi mím". Kết quả: Tavo mở miệng theo lời, môi ông chú khép (ông vẫn nhìn Tavo, không nhìn đồng xu). (2) chặt: lời dặn "extreme speed ... blur", Tua 1,3→1,5; gói: đầu clip chỉ 1 gói, cuối 4 gói, góc Y "đầu nằm dưới mép dưới khung" (Muse vẫn để lộ đỉnh đầu nhỏ ở mép dưới). (3) góc E: 4 gói giấy hồng ({{DAO_GOI}}) trên nóc tủ kính; cả cảnh 20 và hôn trán (24, khung đầu từ 20) đều đúng. (4) montage 4→7 cảnh x 2,5 s, chớp trắng 0,2; mỗi cảnh có điện thoại hiện app (góc mới Q5, Q6, Q7). (5) cảnh M "No, the young guy." dùng `Khung đầu từ cảnh` của cảnh M "Hi. A month ago..."; "Tú, cállate" dùng khung đầu cảnh M2 "Yes, yes, me" (công cụ: `id="m"` / `start="@m"` trong tao_kich_ban.py). (6) emo "delighted, warm" + eye/act bà chủ mỉm cười vui mừng cả lúc nghe.
- Kết quả: ĐẠT các cảnh đã duyệt (9, 17, 18 một phần, 20, 24, 32–38, 41). final 178,7 s 1080x1920, 50 cảnh (38 có lời + 12 không lời), log không cảnh báo mức warn ngoài 1 lần WinError 32 tự chạy lại. Chưa duyệt kỹ từng cảnh 25–31, 39–50 (chỉ xem khung giữa).
- Áp dụng chung?: CÓ: (a) hai người cùng khung, người nghe nhìn thẳng người nói → Muse gán giọng cho người nghe: cho người nghe nhìn đi chỗ khác / người nói quay mặt 3/4 về máy, tránh emo có "lips press" cho người cần mở miệng; (b) góc cận từ trên xuống: không giữ được "đầu ngoài khung"; (c) đạo cụ đã làm ở cảnh trước phải nêu rõ trong CAMERA ANGLE của các cảnh sau (gói thịt trên nóc tủ).
- Đã chưng cất vào: SO-TAY-KY-THUAT.md (dòng cảnh không lời), README thể loại

### 2026-11-12 · phong-van-pho-malayalam · 40 biến thể từ bảng người dùng · loai: bien-the / kich-ban / anh-tham-chieu
- Hiện tượng: bảng csv 40 dòng: người bán đổi giới/tuổi/nghề + ảnh Drive (nhân vật phông xanh toàn thân 1152x2048, bối cảnh không người). Kịch bản cũ ghi cứng "the woman / gloved hands / pots / cart / saree" ở ANGLE, ACTION, NEGATIVE.
- Cách sửa: kịch bản chuyển sang token (TEN_HOC, SHE_/HER_/HERO_/SELF_HOC, TAY_HOC, VIEC_HOC, VIEC2_HOC, DAO_GANG thành câu đầy đủ); biến thể 01 điền như cũ (so chữ: chỉ đổi woman→vendor, cart→stall). `tao_40_bien_the.py` tải ảnh Drive (uc?export=download, ảnh webp → jpg), refs NGUOI_HOC + NEN_PHO + NEN_HOC. Biến thể nam: TEN_HOC "the vendor" (không "the man": "him/his" lẫn với phóng viên nam), giọng nam 100-135 Hz cho khác phóng viên.
- Kết quả: kiem-tra --tai-anh 0 lỗi 0 cảnh báo (324 mục). Đã nhập: loại `Phong-van-pho-Malayalam---40-nghe-5f1f`, dự án `Interview-street-Malayalam---40-bien-the-375b`, 40/40 biến thể đủ 5 ảnh refs. Chưa gen: CHỜ KIỂM CHỨNG (rủi ro cặp nam-nam cùng khung).
- Áp dụng chung?: CÓ: (a) kịch bản định làm nhiều biến thể nghề/giới thì viết token đại từ + đạo cụ ngay từ đầu; (b) kịch bản thêm token mới → loại dự án mới, không sửa loại đang có dự án.
- Đã chưng cất vào: chưa

### 12/11/2026 phong-van-pho-malayalam: người bán NAM đổi phóng viên sang NỮ (20 biến thể bt01-10, bt21-30)
- Hiện tượng/yêu cầu: người dùng yêu cầu người bán nam thì phóng viên phải là nữ để tránh lặp câu / người này nói câu của người kia (hai nam cùng khung, phóng viên quay lưng).
- Cách làm: `cong-cu/tao_40_bien_the.py` thêm `PV_NU` (ngoại hình, giọng 200-230 Hz, NHIN_PV/NGHE_PV đại từ "her", ảnh `anh/phong-vien-nu.png` gen bằng `gen_anh_tham_chieu.py PVN`); chỉ biến thể người bán nam dùng. Cặp nữ bán + nam PV giữ nguyên. Cập nhật dự án qua PUT, xoá thư mục chạy + bản xuất cũ của 20 biến thể, xếp lại hàng đợi 4 luồng.
- Kết quả: CHỜ KIỂM CHỨNG (xem lời có bị lặp/lẫn giọng không). Áp dụng riêng thể loại; quy tắc chung: cặp PV-người bán luôn khác giới. Chưa chưng cất.

### 2026-11-12 · tiem-thit-tieng-anh · thay robot AI bằng ảnh người dùng cung cấp · loai: muse / quy-trinh
- Yêu cầu: mọi cảnh có robot phải dùng đúng robot trong ảnh mới (anh/ROBOT.png).
- Cách làm: lưu ảnh làm ref `NGUOI_ROBOT`, viết lại mô tả `NGUOI_ROBOT` theo ảnh; cảnh 49 (Tavo giơ điện thoại) thêm ref ROBOT + tả robot trong prompt ảnh (trước đó chỉ "mặt robot trắng" nên màn hình không đúng robot). Chỉ gen lại 5 cảnh có robot (27, 29, 31, 49, 50; cảnh 50 nối từ khung cuối 49): tạo dự án mới, copy file scene{n}_* của các cảnh còn lại từ run cũ rồi xoá scene27/29/31/49/50_*, script.txt, variant.json, final/raw trước khi bắt đầu hàng đợi.
- Kết quả: ĐẠT. Robot ở cảnh 27 và điện thoại ở cảnh 49 giống ảnh (đầu trắng bóng có đường panel, giáp lục giác viền xanh, cổ cáp đen). final 177,8 s.
- Áp dụng chung?: CÓ: đổi nhân vật phụ chỉ cần gen lại các cảnh có nhân vật đó bằng cách dùng lại file cảnh cũ; cảnh chỉ nhắc nhân vật trên màn hình/đạo cụ cũng phải có ref ảnh và mô tả trong prompt ảnh.
### 2026-11-12 · taxi-gia-su-ai · xe taxi phải rõ là đang chạy · loai: muse / kich-ban
- Hiện tượng: người dùng: đoạn taxi (0–20 s) xe đang chạy mà cảnh vật ngoài kính đứng im, cần thấy phố hai bên cửa kính đổi.
- Nguyên nhân: prompt cũ ép nền đứng im ("Nothing moves in the background", NEN_PHO "all still", "LOCKED CAMERA on a tripod") nên Muse vẽ xe đỗ.
- Cách sửa: góc A có khối "MOVING TAXI, CAR-MOUNTED CAMERA" (máy gắn đầu xe: khung giữ y nguyên, nhưng phố trôi liên tục từ trước ra sau, rung nhẹ, vệt nắng/bóng), bỏ "all still", STYLE LOCK/SET LOCK/NEGATIVE ghi ngoại lệ cho góc A, negative thêm "a parked or stopped taxi; a frozen street". Giữ nguyên ảnh khung đầu; gen lại clip cảnh 1–6 (bản cũ ở `_cu-xe-dung/`).
- Kết quả: ĐẠT phần chuyển động: nhà, đèn giao thông, cột đèn trôi rõ ở cảnh 1–6, bố cục gốc giữ, lời 6 cảnh đúng (Whisper). Lệch: cảnh 3 tài xế quay đầu sang phải, giơ tay (bắt chước hành động khách) → thêm vào `act` cảnh 3 "the driver does NOT copy him…", gen lại riêng cảnh 3.
- Kết quả lần gen lại cảnh 3 (12/11 15:49): hết giơ tay, lời đúng, cảnh vật vẫn trôi; nhưng nửa sau clip tài xế vẫn quay đầu nghiêng sang phải (về phía cửa sổ). `final.mp4` ghép lại 15:58. CHỜ người dùng quyết có gen lại lần nữa không.
- Áp dụng chung?: CÓ, cho cảnh trong xe đang chạy: ghi rõ "camera fixed to the moving vehicle, outside streams past" thay vì khoá máy tripod + nền tĩnh; chạy xong phải soi người nghe có bắt chước cử chỉ người nói không.
- Đã chưng cất vào: chưa

### 2026-11-12 · tiem-thit-tieng-anh · nhạc nền, montage 1,3 s, cảnh 39–42 một góc · loai: studio / kich-ban / hau-ky
- Yêu cầu: (1) thêm nhạc nền; (2) 7 cảnh Tavo vừa học vừa làm cắt còn 1–1,5 s; (3) từ "Hi, a month ago…" đến "Tú, cállate" chỉ một nền, một góc.
- Cách làm: (1) Studio chưa có chức năng nhạc nền → công cụ riêng thể loại `cong-cu/them_nhac_nen.py` (nhạc guitar Latin tự tạo bằng numpy, không bản quyền; sidechain hạ nhạc khi có giọng; mặc định -15 dB), chạy trên final.mp4. (2) `keep=1.3` cho Q1–Q7; xoá scene{n}_cut/_last của 32–38 để cắt lại từ clip cũ, không gen lại. (3) cảnh 39–42 đều góc M (`start="noi"` nối khung cuối cảnh trước), bỏ M2; xoá scene39–42_* để gen lại.
- Kết quả: ĐẠT các cảnh 39–42 cùng nền, cùng góc (xem khung giữa). final 169,9 s. Nhạc chưa nghe thử, chỉ kiểm tra mức âm lượng.
- Áp dụng chung?: CÓ: đổi đoạn dài cần một góc → chọn góc có đủ cả hai người; cắt lại cảnh không lời chỉ cần xoá _cut và _last.
### 2026-11-12 · taxi-gia-su-ai · cảnh 1–6 không liền mạch, tay lỗi · loai: muse / kich-ban
- Hiện tượng: người dùng xem khung cuối 6 cảnh taxi: khách ngồi xa/gần khác nhau từng cảnh (cảnh 4 chồm sát tài xế), tư thế và hành động không nối nhau, mặt tài xế đổi giữa cảnh; cảnh 1 tay khách bị lỗi khi chỉ tay (một tay cầm điện thoại, tay kia chỉ).
- Nguyên nhân: cảnh 2–6 đều `Khung đầu từ cảnh: 1` → mỗi clip bắt đầu lại từ cùng khung đầu nên cuối clip mỗi cảnh một kiểu; hành động chỉ tay/giơ tay một tay trong khi tay kia giữ điện thoại → Muse vẽ tay hỏng.
- Cách sửa: cảnh 2–6 dùng `start="noi"` (khung đầu = khung cuối cảnh trước; máy gắn xe nên khung không đổi), mỗi cảnh kết thúc ở tư thế cố định (khách ngồi lùi, điện thoại áp tai, tay trống để trên đầu gối), bỏ chỉ tay: chỉ gật đầu/ngoái đầu/nâng bàn tay nhẹ; khi khách nói thêm "tài xế KHÔNG bắt chước, tay trên vô lăng, đầu/thân cố định"; khi tài xế nói thêm "khách ngồi lùi, không chồm tới gần". Cảnh nhìn ra cửa sổ: sửa "RIGHT" thành mép TRÁI khung (khách ngồi bên trái). Bản cũ cất ở `_cu-xe-dung/lan7/`.
- Kết quả: KHÔNG ĐẠT. Nối khung + máy gắn xe đang chạy: cảnh 1–2 thành cảnh rộng (xe nhỏ), từ cảnh 3 Muse tự đổi sang góc trong xe, khách ngồi cạnh tài xế ở hàng trên, có chữ "E 42 St" trên đèn mui; lỗi lan hết cảnh 4–6. Ngoài ra `scene1_start.png` bị gen lại (16:08) vì mình chuyển cả `scene1_cut.mp4` cấp trên → nhieu_phan xoá sạch `phan1/scene1_*`. Người dùng: "các cảnh sau tự dưng khách ngồi lên chỗ tài xế".
- Sửa lần 2: bỏ nối khung, cảnh 2–6 về lại `Khung đầu từ cảnh: 1`, giữ hành động đơn giản + tư thế cuối cố định; lấy lại ảnh khung đầu đã duyệt từ `taxi-mexico-goc-lan1-loi-cat-goc/phan1/scene1_start.png`; chỉ xoá file trong `phan1/` (giữ file cấp trên) để ảnh không bị gen lại. Bản lỗi cất ở `_cu-xe-dung/lan8-noi-khung/`.
- Kết quả lần 9 (17:04): bố cục ĐẠT cả 6 cảnh (tài xế to phải, khách nhỏ ghế sau trái), phố trôi, lời đúng 6/6, cảnh 1 hết lỗi tay. Còn lỗi: cảnh 3 tài xế quay hẳn đầu sang trái, mặt khác hẳn; cảnh 6 TÀI XẾ xoa trán (hành động viết cho khách), đèn mui có chữ "NEW YORK". Lưu ý: dừng mục giữa chừng thì Studio `_discard_inflight` xoá `scene{n}_cut` cấp trên → lần chạy sau nhieu_phan xoá cả ảnh khung đầu trong `phan1`; phải chép lại file cấp trên trước khi chạy tiếp.
- Sửa lần 10: bỏ mọi hành động của khách mà Muse dễ gán cho tài xế (ngoái đầu, xoa trán): khách chỉ cau mày, lắc đầu nhẹ, thở dài, tay để trên đầu gối; đèn mui "plain blank yellow, nothing written". Gen lại riêng cảnh 3 và 6 (bản cũ `_cu-xe-dung/lan9/`). Kết quả (17:21): cảnh 6 ĐẠT (tài xế buồn, tay trên vô lăng, không chữ trên đèn mui); cảnh 3 lời đúng, khung đúng, nhưng giữa clip tài xế vẫn ngoái đầu ra sau ~1 s rồi quay lại (lần thứ 3 ở câu "you missed the turn": Muse tự hiểu tài xế nhìn lại chỗ rẽ bị lỡ). Chờ người dùng quyết.
- Áp dụng chung (đã thấy 3 lần): người nói nhỏ ở hậu cảnh + người nghe to ở tiền cảnh → Muse gán HÀNH ĐỘNG của người nói (quay đầu, giơ tay, xoa trán) cho người nghe to. Chỉ viết cho người nói hành động nét mặt/đầu rất nhỏ.
- Áp dụng chung?: CÓ: (a) góc máy mà người nói nhỏ ở hậu cảnh thì KHÔNG nối khung chuỗi dài: Muse đổi góc và lỗi lan theo chuỗi; dùng lại một khung đầu đã duyệt. (b) Gen lại clip mà giữ ảnh khung đầu: chỉ xoá `phan{k}/scene{l}_clip/_cut/_last`, không đụng file cấp trên. (c) hành động phải có tay trống khi tay kia đã cầm vật.
- Đã chưng cất vào: chưa
- Sửa (12/11, người dùng báo "video chưa có nhạc"): bản trộn đầu để nhạc -15 dB + sidechain ngưỡng 0.02 → nhạc thấp hơn giọng ~12 dB và bị hạ liên tục (âm nền video luôn vượt ngưỡng), tăng âm lượng chỉ 0,1 dB nên không nghe ra. Đổi mặc định -8 dB, sidechain ngưỡng 0.1 tỉ lệ 2,5. Bài học: kiểm tra bằng so mean_volume trước/sau trộn (phải tăng ≥1 dB), đừng chỉ xem file đã ghi.

### 12/11/2026 phong-van-pho-tay-ban-nha: thể loại mới (20 biến thể ES Interview + robot Aiva), CHỜ KIỂM CHỨNG
- Yêu cầu: viết file kịch bản + 20 biến thể cho bảng "20 biến thể ES Interview" (lời Tây Ban Nha, người bán Mexico, PV khác giới, ảnh Drive) với robot Aiva (ảnh người dùng).
- Làm: thể loại mới (không đụng thể loại Malayalam): `SAMPLE/phong-van-pho-tay-ban-nha/` (tao_kich_ban.py, tao_20_bien_the.py, 60 ảnh bt20, robot-aiva.png) + `app/production/types/phong-van-pho-tay-ban-nha/` (gen.py cắt sát không tua nhanh, post.py, config.json).
  Token PV (HIS_PV/HIM_PV/TOC_PV) thay "his/beard/glasses/backpack" cứng vì PV khi nam khi nữ; assert PV khác giới người bán.
- Sửa so với bảng lời: gộp câu liền cùng người (15 → 12 lượt), "Kannur" → "Puebla", "nativa/nativo" theo giới.
- Kiểm tra: video-moi.py kiem-tra 0 lỗi / 0 cảnh báo. Chưa nhập Studio, chưa gen. Áp dụng riêng thể loại; quy tắc PV khác giới + token đại từ PV là chung (chưa chưng cất).
- PHÁT HIỆN: kịch bản phong-van-pho-malayalam còn ghi cứng "his / beard / glasses / backpack" cho PV, trong khi 20 biến thể người bán nam đã đổi PV sang nữ (12/11) => mô tả mâu thuẫn trong prompt. CHƯA SỬA (cần loại dự án mới + gen lại).

### 12/11/2026 san-khau-chia-doi-gia-su-ai: thẻ từ vựng bằng code
- Hiện tượng: video Lurnia có thẻ từ vựng (nhãn Bồ + câu Anh + phiên âm, từ đang đọc tô vàng) phía trên khung chia đôi.
- Cách làm: nền thẻ PNG (PIL) + chữ Anh và ô tô vàng bằng ASS theo mốc từ Whisper (pt); phụ đề chỉ phần 1. Whisper en nghe lời Bồ sai nên dùng pt+en.
- Kết quả: CHỜ KIỂM CHỨNG (post.py chưa chạy thử; Studio chưa mở, chưa gen). Áp dụng: riêng thể loại. Chưa chưng cất.

### 13/11/2026 san-khau-chia-doi-gia-su-ai: gen ảnh tham chiếu bằng Muse
- Ảnh diễn giả (không ref) và robot (ref = robot trắng người dùng + mũ xám, kính đen, áo bomber) gen bằng cong-cu/gen_anh.py (cần MUSE2API_ENV_FILE=userdata\api\.env vì settings.api_key trống). Kết quả: ĐẠT ngay lần đầu, mũ/kính/áo rõ, giữ mặt sứ trắng. Áp dụng: dùng lại gen_anh.py cho thể loại khác.

### 16/11/2026 san-khau-chia-doi-gia-su-ai: nhập Studio + chạy thử biến thể 01
- Dự án Lurnia---dien-gia-san-khau-8a5e, loại San-khau-the-tu-vung-chia-doi-gia-su-AI-986e. scene1_start.png: mặt/áo/nền sân khấu ĐẠT (khối đỏ không chữ, khán giả mờ), nhưng khung NHẬN TOÀN THÂN tới giày (prompt ghi 'từ đùi trở lên') nên mặt nhỏ hơn video mẫu. CHƯA ĐẠT khổ khung; chờ quyết định gen lại ảnh đầu.

### 16/11/2026 san-khau-chia-doi-gia-su-ai: phần 2 dùng `noi: cat` + ảnh gốc chuẩn
- Hiện tượng: base_HOC.png (Muse tự gen) lệch phải, mặt xoay, quá to (đầu ~12%); clip sau trôi: kẹp 2 clicker, vệt ghép (scene4_spklast.png) do `noi: lien`.
- Cách sửa: `noi: cat` (mọi clip xuất phát từ ảnh gốc cố định) + tự gen base_HOC/base_DAY chuẩn bằng cong-cu/gen_base.py (chính diện, giữa khung, đầu 22%, ref = ảnh AI người dùng) rồi đặt vào phan2/ trước khi chạy; câu NHAN VAT HOC thêm "STRAIGHT ON, nose on centre line". Bản lỗi cũ lưu ở phan2_truoc_khi_sua/.
- Kết quả: CHỜ KIỂM CHỨNG (đang gen lại phần 2). Áp dụng: thể loại này; muốn áp cho thể loại khác thì thêm `noi: cat` vào khối [GHEP HAI LOP] của kịch bản đó.

### 16/11/2026 san-khau-chia-doi-gia-su-ai: diễn giả nói "Sounds good" hai lần
- Hiện tượng: scene9_cut.mp4 (lượt diễn giả) Whisper nghe "Sounds good! Sounds good!" vì lời viết "{en}. {en}." (theo video mẫu lặp hai lần).
- Cách sửa: lượt diễn giả chỉ viết MỘT lần "{en}." (tao_bien_the.py), kịch bản dặn "repeats exactly ONCE, then stops"; Studio đọc lời từ biến thể nên 5 vòng đều đổi. Lời có hai lần thì Muse nói đủ hai lần: muốn lặp một lần thì chỉ ghi một lần.
- Kết quả: CHỜ KIỂM CHỨNG (đang gen lại từ cảnh 9). Áp dụng chung: mọi thể loại "học viên lặp lại câu".

### 16/11/2026 san-khau-chia-doi-gia-su-ai: đổi tên app + màn hình điện thoại cảnh 6
- Yêu cầu: cảnh 4 nói "Talka AI" thay YayTalk (APP trong tao_bien_the.py); cảnh 6 điện thoại hiện robot Talka AI (DAO_DIENTHOAI mô tả robot trắng mặt sứ mắt xanh, ảnh gốc anh/robot-talka-ai.webp chỉ để tham chiếu, không gửi Muse vì token ảnh trung tính sẽ lọt sang phần 2).
- Làm lại bằng "Chỉ làm lại cảnh này" (queue/redo only) cảnh 4 rồi 6. Kết quả: CHỜ KIỂM CHỨNG (Muse có thể vẽ robot trên màn hình chỉ gần giống; cảnh 5 nối từ khung cuối cảnh 4 nên không đổi).

### 16/11/2026 san-khau-chia-doi-gia-su-ai: thẻ từ vựng chuyển xuống dưới
- Hiện tượng: thẻ y 75–330 (đỉnh đầu ~20% = 384 px) che mặt trên ảnh split thực tế do khung cắt dải giữa.
- Cách sửa: config.json the.y = 1520 (thẻ dưới, 1520–1775); kịch bản đổi ràng buộc "17% trên trống" thành "mặt/tay trên 17% dưới". Hậu kỳ chạy lại là thấy ngay, không cần gen lại clip.
- Kết quả: CHỜ KIỂM CHỨNG (post.py chưa chạy thật lần nào; xem thẻ có che tay/clicker không). Áp dụng: riêng thể loại.

### 16/11/2026 san-khau-chia-doi-gia-su-ai: hậu kỳ thẻ dưới chạy thật
- post.py chạy trên bản gen đầy đủ (17 cảnh): thẻ ở dưới KHÔNG che mặt nào; ô tô vàng bám từ đang đọc (robot + diễn giả). Lỗi tìm thấy: khoảng cách từ/ô vàng rộng vì PP.text_width cộng ~14 px đệm và libass \fs = chiều cao dòng (~1,117 em). Sửa: đo bằng PIL arialbd ở cỡ fs/1,117. Kết quả: ĐẠT (xem 4 khung). Áp dụng: mọi nơi dùng ASS + đo chữ bằng PIL. Chưa chưng cất.

### 16/11/2026 san-khau-chia-doi-gia-su-ai: cảnh 2 = cảnh tiệc + gạch ngang/X/tiếng sai
- Video mẫu 5,8–8,8 s: diễn giả ở tiệc sang trọng (ly champagne, sảnh bokeh) nói "Me too / You're welcome / I'm fine, thank you", mỗi câu hiện chữ gạch ngang + X đỏ. Bản đầu của mình để cả cảnh ở sân khấu, thiếu hoàn cảnh.
- Sửa: cảnh 2 có Prompt ảnh riêng (tiệc, ngực trở lên); cảnh 3 `Khung đầu từ cảnh: 1` để quay lại sân khấu (không thì nối từ khung tiệc); lượt 2 đặt "gach": true → post.py vẽ từng câu (trắng, gạch đỏ, X) theo mốc Whisper + buzz.
- Kết quả: CHỜ KIỂM CHỨNG (đang gen lại cảnh 2; hậu kỳ gạch chưa chạy thật). Áp dụng: mọi cảnh "câu sai" đứng một mình ở phần thường.

### 16/11/2026 san-khau-chia-doi-gia-su-ai: cảnh tiệc bị kéo về sân khấu
- Hiện tượng: scene2_start.png đúng tiệc nhưng clip chuyển thành nền sân khấu (khối đỏ) cầm ly champagne. Nguyên nhân: gen_video.build_prompts LUÔN chèn SET LOCK + CHAR LOCK + STYLE LOCK vào Prompt video; khoá của phần 1 tả "sân khấu" (STYLE LOCK + SET LOCK + NEN_HOC) → ghi đè bối cảnh cảnh 2.
- Sửa: STYLE LOCK/SET LOCK phần 1 trung tính về địa điểm ("giữ đúng nơi/khung như khung đầu"); địa điểm chỉ ghi trong Prompt ảnh/Khung đầu từng cảnh. Gen lại cảnh 2.
- Kết quả: CHỜ KIỂM CHỨNG. Bài học chung: cảnh đổi bối cảnh giữa chừng thì khối khoá chung KHÔNG được nhắc địa điểm (khớp mục "Vật nền hiện dần" trong sổ tay).

### 16/11/2026 san-khau-chia-doi-gia-su-ai: cảnh tiệc phải là tình huống thật
- Yêu cầu người dùng: diễn giả nói chuyện với một người (không focus người đó), không nhìn ống kính. Sửa: Prompt ảnh/video cảnh 2 → mắt nhìn người ngoài khung bên trái, mép phải chỉ vai/gáy khách mờ nhoè; STYLE LOCK/CHAR LOCK EYE LINE đổi "nhìn ống kính" thành theo từng cảnh. Gen lại cảnh 2. Kết quả: CHỜ KIỂM CHỨNG.
- Còn phải làm: cắt khoảng không thoại thừa của cảnh 2 (xem khoảng lặng đầu/cuối clip mới).

### 16/11/2026 san-khau-chia-doi-gia-su-ai: cảnh tiệc ĐẠT + cắt khoảng lặng
- scene2_start.png + clip mới ĐẠT: diễn giả nghiêng mặt nhìn người ngoài khung, khách quay lưng mờ nhoè ở mép phải, ly champagne, sảnh sang trọng; gạch ngang + X khớp từng câu (±0,2 s).
- Cắt khoảng lặng: Whisper theo từ trên scene2_cut (4,58 s) cho lời 0–4,18 s, khoảng lặng giữa 1,70–2,62 s. Cắt bằng ffmpeg (bỏ 1,85–2,47 và đuôi sau 4,33, crossfade âm 50 ms) → 3,74 s; ghi đè phan1/scene2_cut.mp4 + scene2_cut.mp4 (bản gốc: phan1/scene2_cut_goc.mp4.bak) rồi POST /api/queue/start trên mục đã xong → Studio dựng lại raw từ các clip có sẵn (scenes.json cảnh 2 còn 3,74 s). Chạy tay, chưa thành tính năng: muốn cắt tự động thì giảm cut_margin ở Cài đặt.
- Áp dụng chung: cách "sửa clip rồi start lại mục done" dùng được để dựng lại mà không gen.

## 16/11/2026 — san-khau-chia-doi-gia-su-ai: cắt khoảng lặng cảnh 4, 7
- Cảnh 7 (clip 8,27 s): 0,5 s đầu còn cầm điện thoại giơ lên (đã hạ trong clip) + quãng lặng 1,18 s giữa câu + đuôi 0,86 s → cắt còn 6,5 s (giữ 0,5–5,65 và 6,35–7,7, nối âm acrossfade 50 ms). Cảnh 4: đuôi lặng 1,16 s → cắt còn 4,2 s.
- Quy trình: `silencedetect=n=-30dB:d=0.4` tìm lặng → sao lưu `sceneN_cut_goc.mp4.bak` → ffmpeg trim/concat → chép đè `phanX/sceneN_cut.mp4` và `sceneN_cut.mp4` → `POST /api/queue/start {"ids":[id]}` dựng lại raw + hậu kỳ (không gen lại). Phụ đề tự khớp lại theo Whisper.
- Gốc lỗi: kịch bản cảnh 7 bảo "hạ điện thoại ở đầu câu" nên đầu clip luôn còn điện thoại; nên bắt đầu cảnh 7 từ khung đã hạ tay.

## 16/11/2026 — san-khau-chia-doi-gia-su-ai: cắt khoảng lặng cảnh 8–17 (phần 2)
- Quy tắc cắt tự động: lặng đầu ≥0,4 s → giữ 0,12 s; lặng cuối ≥0,4 s → giữ 0,2 s; lặng giữa ≥0,4 s → giữ 0,3 s (0,15 mỗi bên); lặng <0,4 s giữ nguyên (nhịp thở). Nối bằng concat + fade 20 ms. Cảnh 10, 14 không có lặng dài nên giữ.
- Kết quả: video 79,7 → 72,4 s (-7,3 s). Thẻ từ vựng + tô vàng khớp lại theo Whisper, không phải sửa gì.
- Lưu ý: file `sceneN_cut.mp4` ở gốc và `phan2/scene(N-7)_cut.mp4` là hard-link, chép đè phải bắt SameFileError. Bản gốc: `sceneN_cut_goc.mp4.bak`.
- Chuyển động trong khoảng lặng chỉ là người nghe đứng im thở nhẹ (YAVG ~0,5–2), không có hành động; đoạn lặng ngắn thì giữ.

## 16/11/2026 — san-khau-chia-doi-gia-su-ai: sửa vào KỊCH BẢN để lần sau khỏi phải cắt tay
- Cảnh 7 thêm `Khung đầu từ cảnh: 5` (khung cuối cảnh 5: tay ngang bụng, không điện thoại) và bỏ ACTION "hạ điện thoại ở đầu clip" → không còn 0,5 s cầm điện thoại ở đầu cảnh 7 (hard cut từ cảnh 6). Đã chép sang `userdata/studio/types/`.
- Chưa tự động hoá: cắt lặng GIỮA câu (≥0,4 s) và đuôi lặng cảnh 4/8–17 mới chỉ làm tay trên bản chạy này; "Cắt sát lời nói" của Studio chỉ lo hai đầu clip.

## 16/11/2026 — san-khau-chia-doi-gia-su-ai: tiếng vỗ tay thừa + cắt lặng đầu/cuối mọi cảnh
- Cảnh 15 (lượt người học "I didn't catch that"): 1,4 s đầu clip là nền tiếng vỗ tay (RMS ~1000 đều, không phải lời; silencedetect -32 dB KHÔNG bắt vì nó ồn hơn ngưỡng) → cắt từ 1,4 s. Cảnh 12, 14 có tiếng lạ sau lời (RMS 770–850 ở cuối) → cắt đuôi theo thời điểm hết lời. Cách phát hiện: in RMS mỗi 0,25 s, nền đều ~1000 trước lời = vỗ tay/ồn khán giả.
- Cắt đầu/cuối cả 17 cảnh: giữ đầu 0,10 s, đuôi 0,15 s. Tổng 79,7 → 63,8 s. Thẻ từ vựng vẫn khớp.
- Lần sau: thêm vào Negative prompt/âm thanh "no applause, no crowd noise" để Muse khỏi sinh vỗ tay (chưa thêm vào kịch bản).
- Đã thêm 'applause, clapping, cheering, crowd noise, background music' vào mọi Negative prompt (phần 1 + khối [NEGATIVE] phần 2) và 'không vỗ tay, không tiếng khán giả' vào dòng Audio (16/11/2026).

### 2026-11-16 · san-khau-chia-doi-gia-su-ai · 4 CSV X0056–X0059 → 4 file biến thể (nam/nữ, Brazil/Hindi/Mexico, robot mặc đồ) · loai: studio
- CSV: Brazil 40, Hindi 20, Brazil+Robot 40 (thêm ảnh robot mặc theo từng người), Mexico 40; mọi ảnh Drive công khai tải được bằng `drive.google.com/uc?export=download&id=` (180 ảnh, 37 MB), phông xanh toàn thân.
- Kịch bản gốc viết cứng "he/his/man", "Brazilian Portuguese", "olha só", "cap", "belt" → đổi sang token {{HE}}/{{HE_C}}/{{HIS}}/{{HIM}}, {{NGON_NGU}}, {{TU_OLHA}}, "top of the head", "waist". CSV Hindi/Mexico không có cảnh 7 ("Como você diria?": robot hỏi câu đầu) → kịch bản bản 6 cảnh riêng (`-6CANH.txt`, cắt khối CẢNH 7 bằng code); lời phần 1 chia nhỏ từ CSV (câu "Yo también contestaba así" tách khỏi "Pero todo cambió..." giữ nhịp cảnh 3/4). Robot vòng học lấy đúng lời CSV ("¿Cómo dirías “X” en inglés? Y. Repite conmigo: Y.").
- Mô tả nhân vật chỉ gồm giới + quốc tịch + tuổi + "đúng như ảnh tham chiếu" (không dịch mô tả tiếng Việt: mặt/tóc/trang phục lấy từ ảnh). Giọng theo giới + tuổi. Robot CSV: "wearing exactly the outfit shown in the reference photo".
- Hindi: `post.py` đổi font Nirmala UI (nhãn thẻ PIL + phụ đề phần 1 + shaping complex); chữ nữ/nam trong lời Hindi ("देती थी/देता था", "लगी/लगा") chọn theo giới.
- Rủi ro chưa kiểm: Whisper `hi` có thể ghi từ tiếng Anh trong lượt Hindi thành chữ Devanagari → tô vàng từ có thể trượt; ảnh phông xanh toàn thân có thể làm Muse zoom ra toàn thân (đã có "thighs up" trong prompt); GIONG_DAY robot vẫn trầm nam cho mọi robot.
- Kết quả: kiểm tra 0 lỗi cả 5 cặp (brazil, brazil-robot, hindi, mexico, bản gốc). CHƯA gen thử.

### 2026-11-16 · san-khau-chia-doi-gia-su-ai · cảnh 3–6 chạy ra nền SẢNH TIỆC thay vì sân khấu (X0056, X0057) · loai: studio
- Hiện tượng: chỉ cảnh 2 được có nền tiệc, nhưng cảnh 3 (khung đầu lấy lại từ cảnh 1, đúng sân khấu) clip vẫn trôi sang sảnh tiệc (đèn chùm, ly champagne), cảnh 4–6 nối khung cuối nên kế thừa nền tiệc.
- Nguyên nhân: sau khi làm khoá STYLE/SET trung tính (không nêu địa điểm để cảnh 2 khác nền), prompt video các cảnh sân khấu không còn chỗ nào nói "sân khấu"; Muse giữ ngữ cảnh cảnh tiệc liền trước.
- Cách sửa: mỗi Prompt video cảnh 1,3,4,5,6,7 có câu `SETTING: ... stays on the conference stage exactly as in the start frame ({{NEN_HOC}}); never a ballroom, reception ...`; Negative prompt các cảnh đó thêm "ballroom, reception hall, chandeliers, champagne glasses, banquet tables, ... a change of location"; cảnh 3 ghi rõ khung đầu là khung sân khấu cảnh 1 (không phải "khung cuối cảnh trước"). Cảnh tiệc chỉ cảnh 2.
- Phải gen lại các dự án đã chạy: từ cảnh 3 trở đi (cảnh 4–6 đang bắt đầu từ khung cuối trôi nền).
- Áp dụng chung?: CÓ: khoá trung tính địa điểm thì từng cảnh phải tự nêu địa điểm; cảnh xen (tiệc) rồi quay lại phải có câu địa điểm + negative của nền xen.

### 2026-11-13 · taxi-gia-su-ai · bản Ấn Độ 20 biến thể (sheet X0061) · loai: kich-ban / code-the-loai
- Việc: người dùng đưa sheet 20 biến thể (lời tiếng Anh + Hindi khác bản Mexico; tài xế nam + khách NỮ có ảnh Drive). Người dùng chọn: bối cảnh thành phố Ấn Độ; Priya + sếp gen Muse; biến thể 2 (tài xế tên Arjun) đổi đồng nghiệp thành Rahul.
- Làm: kịch bản mới `KICH-BAN-TAXI-AN-DO.txt` (sinh bằng `cong-cu/tao_kich_ban_an_do.py`, dùng lại hàm dựng cảnh của bản Mexico, thay bảng góc Mumbai): P1 20 cảnh (5 câm; góc mới M: tài xế + sếp đối mặt cho câu Hindi xin xe + câu sếp mỉa), P2 ghép 2 lớp 9 lượt (Ava, "I am India" → "I am from India"), P3 2 cảnh kết (góc A + cận T3). Biến thể `BIEN-THE-TAXI-AN-DO-20.json` (`tao_bien_the_an_do.py`). Ảnh `anh/an-do/NGUOI-CON.png`, `QUANLY.png` (`gen_anh_an_do.py`), đã xem: đạt.
- Code thể loại: `post.py` biến thể có chữ Devanagari → font `font_devanagari` (Nirmala UI) thay Arial (Arial không có Devanagari; bản Mexico không đổi); `config.json` thêm kiểu/vị trí phụ đề phần 3.
- Kiểm tra: video-moi kiem-tra --tai-anh 0 lỗi, 40 link Drive tải được; nhieu_phan.plan 3 phần 20+9+2 cảnh. Nhập Studio: loại `Taxi-An-Do-gia-su-AI-07ef`, dự án `Taxi-An-Do---20-bien-the-05ff`, chạy cả 20 với 4 luồng (người dùng yêu cầu).
- Kết quả: ĐẠT (13/11, 2 video đầu taxi-in-01-raj, taxi-in-04-rohan, ~103 s). Whisper en: đủ và đúng mọi câu tiếng Anh; câu Hindi Whisper dịch ra đúng nghĩa (en) / chép đúng câu hết tiền (hi). Khách nữ - tài xế nam không nhép nhầm. Phụ đề Devanagari hiện đúng font Nirmala UI; ❌/✅ và icon tiền đúng chỗ; phần 3 đủ 2 cảnh. Lỗi nhỏ không hệ thống: BT4 cảnh 1 Muse zoom vào (mất nắp capô, khách to hơn) nhưng vẫn đúng chỗ ngồi sau-trái.
- Áp dụng chung?: CÓ cho khuôn 'khách khác giới với tài xế' (nhép không nhầm khi khác giới, khớp [[muse-gan-giong-cho-mat-nhin-thay]]) và font Devanagari tự chọn trong post.py.
- Đã chưng cất vào: chưa

### 2026-11-13 · lõi Studio (engine.py) · [WinError 32] khi chạy ffmpeg/ffprobe · loai: code-loi
- Việc: người dùng hỏi vì sao vài video Taxi Ấn Độ báo "[WinError 32] The process cannot access the file because it is being used by another process".
- Tìm ra: traceback trong `userdata/logs/studio-loi.log` (5 video taxi-in-02/03/05/07/09) đều hỏng ở `subprocess.Popen` → `CreateProcess` của ffprobe/ffmpeg (đo màu, cắt sát lời, lấy khung cuối, đo độ dài): file .exe bị giữ thoáng qua lúc khởi chạy (nghi trình diệt virus quét .exe khi 4 luồng gọi liên tục). Không riêng thể loại nào: 84 lần trong log từ 10/11 (~10 lần/ngày). Hậu quả cũ: video tự xếp lại sau 2 phút nhưng bỏ cảnh đang làm (mất clip Muse vừa gen).
- Làm: `engine.py` thêm `_popen_retry` (thử lại tối đa 8 lần, chờ 0.3 s, 0.6 s, ... khi PermissionError winerror 32), `crun` dùng nó. Thử giả lập 2 lần lỗi: lần 3 chạy được.
- Kết quả: CHỜ KIỂM CHỨNG (chỉ có hiệu lực sau khi Studio khởi động lại; xem log không còn dòng WinError 32 mới).
- Khởi động lại (người dùng yêu cầu, 13/11): taskkill cây tiến trình launcher (không gọi /api/stop để khỏi xoá cảnh dở + ảnh khung đầu), soát file ghi trong 3 phút cuối bằng ffprobe (chỉ phan2/raw.mp4 của BT11 hỏng → xoá), mở lại qua explorer, /api/queue/start 17 mục còn lại parallel 4 (4 mục đang chạy dở đứng đầu): các cảnh đã xong được dùng lại.
- Áp dụng chung?: CÓ (mọi thể loại, lõi Studio).
- Đã chưng cất vào: chưa

### 2026-11-16 · taxi-gia-su-ai · 40 biến thể bản Mexico (sheet X0060) vào dự án "Taxi - Miguel" · loai: bien-the / kich-ban
- Việc: người dùng đưa sheet X0060 (40 dòng: tài xế nam Mexico 23-65 tuổi + khách doanh nhân, 20 khách NỮ ở dòng 11-20, 31-40), yêu cầu tạo file biến thể cho dự án Taxi - Miguel, tải đủ ảnh link Drive về và gắn vào biến thể.
- Lời trong sheet là bản dịch tiếng Anh của đúng video gốc -> giữ nguyên LUOT của taxi-mexico-goc (tiếng Anh/Tây Ban Nha như gốc); chỉ đổi tài xế + khách.
- Làm: `cong-cu/tao_bien_the_x0060.py` -> `BIEN-THE-TAXI-X0060-40.json` (taxi-es-01-carlos ... taxi-es-40-adrian). Mô tả EN dịch từ sheet (bỏ giày/dáng đứng), sửa theo ảnh (BT7/22/30/35 là áo gilê chứ không phải blazer). Giọng tài xế theo tuổi (<30 / <46 / già), khách theo giới + tuổi, khách luôn cao giọng hơn tài xế. 80 ảnh tải về `anh/x0060/NN-HOC.png`, `NN-KHACH.png` (drive.usercontent ... confirm=t), đã xem: khớp mô tả.
- Kịch bản (dùng chung bản Mexico): đại từ của KHÁCH -> token `{{HIS_KHACH}}`/`{{HIM_KHACH}}` (bảng GIOI_KHACH trong tao_kich_ban.py, assert mỗi cụm phải có); bỏ chữ cứng theo ngoại hình Miguel ("his moustache trembles" -> "his lips tremble", "curly hair" -> "head") vì tài xế mới có người không ria/không tóc xoăn. Biến thể gốc thêm HIS_KHACH=his, HIM_KHACH=him. Bản Ấn Độ không đổi (gọi scene() riêng).
- Kiểm tra: video-moi kiem-tra --tai-anh 0 lỗi (364 mục); điền token cả 41 biến thể của dự án không còn {{.
- Studio: chép kịch bản mới vào loại Taxi-gia-su-AI-a6ce; PUT dự án Taxi---Miguel-9d63 = gốc + 40 biến thể, ảnh gắn đủ (không lỗi). Chưa chạy (người dùng chưa yêu cầu).
- Kết quả: ĐẠT (chạy thử taxi-es-11-andres, khách nữ Valentina, 16/11 12:59, 148s). Whisper en+es: đủ 43 lượt, đúng lời; khách nữ nhép đúng lượt của mình (cảnh 1-6), tài xế không nhép nhầm; khách ngồi ghế sau trái suốt, xe chạy rõ; bến xe 3 người, phòng khách với Lucía; phần 2 robot có ❌/✅ ở "I am Mexico"/"I am from Mexico" và icon đồng xu ở "no tengo dinero"; phụ đề EN+ES đủ. Token HIS_KHACH/HIM_KHACH hoạt động (her/her).
- Áp dụng chung?: CÓ cho cách làm "đại từ nhân vật đổi giới theo biến thể = token trong kịch bản" và "không viết cứng ngoại hình nhân vật có thể đổi trong lời tả cảnh".
- Đã chưng cất vào: chưa

### 2026-11-17 · taxi-gia-su-ai · video "435d2a85-0510_cartoon-turn-car_015_1" (chính là video mẫu của thể loại) → biến thể toàn tiếng Anh · loai: bien-the
- Việc: Studio gửi video tham chiếu chạy ngầm (không ảnh tham chiếu mới, ngôn ngữ lời English, 1 biến thể). `video-moi.py danh-gia`: 95,1 s, 42 câu, 4,12 từ/giây, 9 cảnh cắt, 2 cụm giọng (133 Hz / 225 Hz), 4 đoạn bố cục (taxi, gara, phòng khách, ô robot trên) + end card. Xem 4 ảnh tổng quan: trùng khít thể loại `taxi-gia-su-ai` (bản mẫu 0510_cartoon turn car_015_1) → KHÔNG tạo thể loại mới, KHÔNG sửa kịch bản/code.
- Làm: thêm `SAMPLE/taxi-gia-su-ai/cong-cu/tao_bien_the_tieng_anh.py` (import bảng V + LUOT của tao_bien_the.py, thay lời sang tiếng Anh cho cả phần 1 gia đình và phần 2 robot, bỏ `dich` tiếng Tây Ban Nha, giọng thành tiếng Anh giọng Mexico nhẹ) → `BIEN-THE-TAXI-TIENG-ANH.json` (taxi-tieng-anh-01, 43 lượt, 5 không lời).
- Ảnh tham chiếu: người dùng không đưa ảnh → dùng lại ảnh có sẵn của thể loại (HOC, KHACH, QUANLY, ARJUN, CON, DAY; ảnh AI người dùng đã đồng ý 11/11). Không gen thêm ảnh, không chạy thử.
- Kiểm tra: `kiem-tra --tai-anh` 0 lỗi 0 cảnh báo; P1 25 cảnh + P2 18 cảnh. Nhập Studio: loại `Taxi-gia-su-AI-a6ce`, dự án `Taxi---English-435d2a85-1800`. CHƯA gen.
- Kết quả: CHỜ KIỂM CHỨNG (chưa gen). Rủi ro như bản gốc: hai nam chung khung ở góc A/G/J, đổi 3 góc phòng khách; lời Anh của gia đình có thể làm Whisper `small` vẫn ổn (đa ngôn ngữ).
- Áp dụng chung?: KHÔNG (riêng thể loại).
- Đã chưng cất vào: không cần

### 2026-11-17 · phong-van-pho-tieng-anh · thể loại mới từ video phỏng vấn đường phố, lời tiếng Anh, 1 biến thể, chưa có ảnh refs · loai: kich-ban / bien-the
- Việc: Studio nhận lại video `1510_interview street hindi_005 (11)` (bản tải lên `e2a15ce0-1510_interview-street-hindi_005-11-onlin.mp4`, chạy ngầm), yêu cầu lời tiếng Anh, 1 biến thể, người dùng không đưa ảnh nhân vật.
- Phân tích lại bằng `video-moi.py danh-gia`: 76,9 s, 9 cảnh cắt, giọng 211/254 Hz, máy đứng yên; xem 4 ảnh tong-quan: khớp phân tích malayalam (phần 1 phố qua vai tới ~26 s, phần 2 robot trên / người bán selfie dưới).
- Làm: thư mục thể loại riêng `phong-van-pho-tieng-anh` chép từ tay-ban-nha (kịch bản đổi Mexico/Spanish → Mỹ/English, bỏ câu "reference photo" vì không có ảnh; `tao_bien_the.py` 1 biến thể, `refs` trống; PV nam + người bán nữ). Lời: dịch mạch tay-ban-nha, "Soy de Puebla" → "I'm from Denver". Code loại (gen/post/config) chép nguyên, chỉ đổi tên.
- Kiểm tra: `kiem-tra` 0 lỗi, 0 cảnh báo, 7 mục đạt. Nhập Studio KHÔNG chạy thử (thiếu ảnh refs).
- Kết quả: CHỜ KIỂM CHỨNG (chưa gen). Rủi ro: không refs nên mặt người bán có thể lệch giữa phần 1 và phần 2.
- Áp dụng chung?: KHÔNG (riêng thể loại). Bài học quy trình: khi chạy ngầm gặp video đã có thể loại cùng khuôn khác ngôn ngữ, chép thể loại gần nhất thay vì phân tích lại từ đầu; mô tả nhân vật bằng chữ khi chưa có ảnh.
- Đã chưng cất vào: không cần

### 2026-11-17 · taxi-gia-su-ai · tự kiểm tra dự án "Taxi - English (435d2a85)" · loai: kiem-tra
- Hiện tượng: hàng đợi Studio không có mục nào của `Taxi---English-435d2a85-1800`, `userdata/studio/runs/` không có thư mục của dự án → chưa có scene*_start.png/clip để đối chiếu. Dự án chỉ có file `projects/Taxi---English-435d2a85-1800.json`.
- Nguyên nhân: bước 5 chạy ngầm không kèm `--chay-thu` (người dùng không đưa ảnh nhân vật mới).
- Cách sửa: không có gì để sửa tại chỗ (chưa có lỗi gen); không gen thêm.
- Kết quả: CHỜ KIỂM CHỨNG. Áp dụng chung: không.
- Đã chưng cất vào: không cần

### 2026-11-17 · taxi-gia-su-ai · video "f2be28b2-0510_cartoon-turn-car_015_1" (video mẫu) → 3 biến thể Ấn Độ, tự gen ảnh thất bại · loai: bien-the
- Việc: Studio chạy ngầm, ngôn ngữ india, 3 biến thể, không ảnh. Đo lại như lần trước (95,1 s, 4,12 từ/giây, 9 cảnh cắt, 133/225 Hz).
- Làm: `cong-cu/tao_bien_the_an_do_3.py` (import bảng từ tao_bien_the_an_do.py, 3 cặp tài xế + khách mới) + kịch bản `KICH-BAN-TAXI-AN-DO.txt`; `kiem-tra` 0 lỗi; nhập dự án `Taxi-An-Do---3-bien-the-f2be28b2-8b57`.
- Gen ảnh nhân vật: 2 lần đầu `gen-anh-nhan-vat.py` lỗi "没有可用账号" (Muse hết tài khoản); gen lại sau đó thì 6/6 ảnh đạt (một người, đúng giới/tuổi, nền xanh phẳng, không chữ) → `anh/an-do-3/HOC1-3, KHACH1-3.png`, tạo lại biến thể có refs (`kiem-tra --tai-anh` 0 lỗi, 31 mục). Dự án đầu (không refs) đã xoá, nhập lại `Taxi-An-Do---3-bien-the-f2be28b2-7236`.
- Chạy thử taxi-in-3-01-ravi: `scene1_start.png` đúng bố cục góc A (tài xế phải, khách nữ sari xanh ghế sau trái nói điện thoại, taxi đen-vàng Mumbai). Studio bị khởi động lại 3 lần giữa chừng (đổi cổng trong running.json) làm mục hàng đợi thành `stopped` → phải `POST /api/queue/add` + `/api/queue/start` lại; lần 4 gen xong cảnh 1 (4,9 s): bố cục giữ suốt clip, khách nói, tài xế nhìn sang nghe, miệng không nhép rõ. Lệch nhỏ: mặt tài xế sau khung đầu hơi thực hơn ảnh hoạt hình.
- Kết quả: ĐẠT cảnh 1; các cảnh sau CHỜ KIỂM CHỨNG. Áp dụng chung?: KHÔNG (bài học quy trình: đọc cổng mới trong `userdata/running.json` và kiểm trạng thái mục hàng đợi sau mỗi lần Studio khởi động lại). Đã chưng cất vào: không cần

### 2026-11-17 · phong-van-pho-hindi · thể loại mới từ video phỏng vấn đường phố, lời Hindi, 3 biến thể, Muse hết tài khoản nên chưa có ảnh refs · loai: kich-ban / bien-the
- Việc: Studio chạy ngầm với `23be8c7e-1510_interview-street-hindi_005-11-onlin.mp4` (cùng video mẫu `1510_interview street hindi_005 (11)` của phong-van-pho-malayalam), ngôn ngữ india, 3 biến thể, không ảnh nhân vật. Phân tích lại bằng `danh-gia` (76,9 s, 9 cảnh cắt, giọng 211/254 Hz) và xem tong-quan_1/3: khớp phân tích malayalam (phần 1 phố qua vai tới 25,7 s, phần 2 robot trên / người bán selfie dưới). Tên file "hindi" nhưng phụ đề là Malayalam.
- Làm: thư mục riêng `phong-van-pho-hindi` chép từ malayalam (kịch bản + `tao_kich_ban.py` đổi sang Hindi/miền bắc Ấn, thêm câu "ảnh tham chiếu chỉ là mặt/tóc/trang phục, nền không thuộc cảnh"; `tao_bien_the.py` viết lại lời Hindi chữ Devanagari xen từ Anh, 26 lượt, ≤ 20 từ). PV nam + người bán nữ (V1 ~50 tuổi bám sát video, V2 ~28 tuổi quầy puri, V3 ~62 tuổi quầy trái cây). `types/phong-van-pho-hindi/gen.py`: ngoài `_span_ml`, đếm âm tiết chữ Devanagari (gen_video chỉ đếm Latin + Malayalam → câu Hindi bị clip 5 s cụt) bằng cách bọc `E.G.spoken_syllables` trong lúc chạy thể loại này, và `voice_span` bỏ Whisper cho câu `hi`. `cong-cu/gen_anh.py` bọc `_chung/gen-anh-nhan-vat.py` đổi STYLE sang photoreal (script chung cố định phong cách hoạt hình Pixar, không hợp video người thật).
- Kiểm tra: `kiem-tra` 0 lỗi, 0 cảnh báo. Nhập Studio: loại `Phong-van-pho-Hindi-66b8`, dự án `Interview-street-Hindi---Talka-d288` (3 biến thể, chưa gen).
- Gen ảnh: `/api/health` báo `no_account` (0 tài khoản Muse); `gen_anh.py` lỗi "没有可用账号，请先在管理页面导入 cookie" cho cả PV, V1, V2, V3 → `refs` chỉ có robot Talka; không chạy thử.
- Kết quả: CHƯA ĐẠT / CHỜ KIỂM CHỨNG (chưa gen). Rủi ro: tiếng Hindi qua Muse chưa kiểm chứng (đã có Gujarati/Bengali/Malayalam), thiếu refs thì mặt người bán lệch giữa phần 1 và 2. Áp dụng chung?: KHÔNG (riêng thể loại). Đã chưng cất vào: không cần

### 2026-11-17 · tiem-thit-hindi · video "17790cf1-0610_Cut-meat-ES_015_02" (chính là video mẫu của tiem-thit-tieng-anh) → 3 biến thể Hindi · loai: bien-the
- Việc: Studio chạy ngầm, ngôn ngữ india, 3 biến thể. `danh-gia`: 177 s, 65 câu, 4,24 từ/giây, 28 cảnh cắt, giọng 152/239 Hz, khớp phân tích tiem-thit-tieng-anh.
- Làm: thể loại anh em `SAMPLE/tiem-thit-hindi/` (kịch bản sinh bằng cách import bảng của tiem-thit-tieng-anh và đổi Spanish -> Hindi; `tao_bien_the.py` 3 biến thể Raju/Kabir/Arjun, lời Devanagari, dich Hindi) + `types/tiem-thit-hindi/` (post.py chép, config font Nirmala UI + shaping complex). `kiem-tra` 0 lỗi 0 cảnh báo; nhập Studio dự án `Tiem-thit---Hindi-17790cf1-127c`, chưa gen.
- Gen ảnh TAVO/TIO: `gen-anh-nhan-vat.py` lỗi "没有可用账号" 2 lần (Muse hết tài khoản) -> refs chỉ có CHU/KHACH/ROBOT dùng lại từ tiem-thit-tieng-anh; không chạy thử.
- Kết quả: CHƯA ĐẠT / CHỜ KIỂM CHỨNG. Áp dụng chung?: KHÔNG. Đã chưng cất vào: không cần

### 2026-11-17 · tiem-thit-hindi · chạy thử biến thể raju-tiem-thit-goc · loai: gen
- Hiện tượng: Muse có lại tài khoản; gen đủ 6 ảnh TAVO/TIO (A/B/C) nền xanh, xem từng ảnh: một người, đúng tuổi/giới, không chữ. Cập nhật `refs` vào dự án cũ (tạo dự án tạm để Studio tải ảnh, PUT biến thể sang dự án cũ, xoá file dự án tạm) thay vì tạo dự án v2.
- Chạy thử: `scene1_start.png` đạt (khách polo trắng một mình, chợ Ấn), `scene1_last.png` khách cười nói, nghiêng về quầy; các cảnh sau đang gen.
- Lưu ý quy trình: Studio khởi động lại làm đổi cổng (50820 → 58360): luôn đọc `userdata/running.json` ngay trước mỗi lệnh API.
- Kết quả: ĐẠT cảnh 1; phần còn lại CHỜ KIỂM CHỨNG. Áp dụng chung?: KHÔNG. Đã chưng cất vào: không cần

26-11-17 · tiem-thit-hindi · phân tích lại video (lần 2) · loai: phan-tich
- Hiện tượng: đo lại video (cùng file với tiem-thit-tieng-anh: 38 lượt có lời, giọng A 121–176 Hz / B 229–286 Hz) khớp kịch bản 50 cảnh hiện có; `kiem-tra --tai-anh` vẫn 0 lỗi, 0 cảnh báo. Không có chỗ nào lệch cần sửa nên KHÔNG đổi kịch bản/biến thể và KHÔNG gen lại.
- Chạy thử: `scene2_start.png` (góc A) ĐẠT: Tavo trái cúi nhìn thớt, ông chú giữa nhìn sang phải, mép phải chỉ vai + gáy khách áo polo trắng, tủ kính thịt ở 1/3 dưới.
- Kết quả: ĐẠT cảnh 1–2; phần còn lại CHỜ KIỂM CHỨNG. Áp dụng chung?: KHÔNG. Đã chưng cất vào: không cần

### 17/11/2026 - phong-van-pho-hindi: phân tích lại + gen ảnh PV/V1-V3 + chạy thử 01
- Hiện tượng: lần trước chưa gen vì Muse hết tài khoản. Lần này gen ảnh nền xanh (gen_anh.py) đạt cả 4; robot gốc có tai nghe nhưng ảnh robot-talka.png không có.
- Cách sửa: thêm tai nghe + mic vào NGUOI_DAY; cập nhật dự án cũ qua PUT /api/projects/<id> (ảnh mới tải bằng POST .../asset, PUT không tự tải link refs).
- Kết quả: scene1_start.png đạt (PV quay lưng); cảnh 1-2 gen xong. Nghe Hindi và base_DAY: CHỜ KIỂM CHỨNG. Riêng thể loại, chưa chưng cất.

### 19/11/2026 - 2e3fa1bf-canh-sat-xe-tai: thể loại mới + gen ảnh nhân vật thật + chạy thử cảnh 1
- Hiện tượng: `_chung/gen-anh-nhan-vat.py` mặc định phong cách hoạt hình 3D ("never photorealistic"), không dùng được cho video người thật. Ảnh HOC (nữ ~57) và CANHSAT (nam ~32) gen bằng bản sao `SAMPLE/2e3fa1bf-canh-sat-xe-tai/cong-cu/gen-anh-nhan-vat-that.py` (STYLE ảnh thật) đạt lần đầu, nền xanh phẳng; tài xế trông hơi già hơn mô tả.
- Chạy thử bien-the-01-goc (dự án Canh-sat-xe-tai-noi-sai-tuoi-4d30): scene1_start.png đúng người/bối cảnh nhưng máy rộng hơn mẫu (thấy cả đường); scene1_cut.mp4 3,0 s: tài xế nói, cảnh sát ngẩng nhìn lên, không quay ống kính.
- Kết quả: cảnh 1 ĐẠT; cảnh 2-4 và kịch bản B (đổi hook) CHỜ KIỂM CHỨNG. Riêng thể loại; gợi ý (chưa chưng cất): thêm tuỳ chọn phong cách ảnh thật cho gen-anh-nhan-vat.py dùng chung.

### 19/11/2026 - 2e3fa1bf-canh-sat-xe-tai: nhóm biến thể tx4wnb (5 cặp, goc) và x2oly3 (5 hook, hook)
- Hiện tượng: gen 10 ảnh nền xanh bằng `gen-anh-nhan-vat-that.py`: 9 đạt lần đầu, TX_B lỗi Muse "fs.raw path not found" (gen lại một lần đạt). Cả 10 ảnh: một người, đúng giới/tuổi, không chữ.
- Cách làm: tuổi trong lời thoại, `to`, cách gọi (Sir/Ma'am) và HIM_CANHSAT (him/her) sinh theo bảng; cặp luôn khác giới. `kiem-tra` cả hai nhóm 0 lỗi, 0 cảnh báo. Chưa gen video: CHỜ KIỂM CHỨNG (xe buýt/xe van cần xem khung đầu vì kịch bản tả "cabin window"). Riêng thể loại.

### 19/11/2026 · san-khau-x0071-hindi · phân tích video + viết hồ sơ hai kịch bản (goc/hook) · loai: phan-tich
- Hiện tượng: video tham chiếu `324369fe-X0071-Split-screen-HINDI_003-5.mp4` (75 s, 1080×1920, Hindi xen Anh) hoá ra CHÍNH LÀ video đã dùng để tạo `SAMPLE/san-khau-chia-doi-gia-su-ai/BIEN-THE-X0057-X0071-HINDI-20.json` trước đó (README của thể loại đó đã ghi rõ "X0071"); `danh-gia` + xem `tong-quan_1..4.jpg` xác nhận khớp gần như tuyệt đối với CẤU TRÚC HOOK/TÌNH HUỐNG do người dùng cung cấp (hook "Nice to meet you"/"Me too", nỗi đau tiệc gạch đỏ 3 câu, giải pháp Talka AI 3 tuần miễn phí, demo 5 câu Sounds good/I'm on my way/Give me a second/I didn't catch that/Here you go kèm nghĩa Hindi+phiên âm, CTA Google Play) — 0 điểm lệch đáng kể.
- Cách làm: KHÔNG tạo thể loại mới / code mới (đúng quy tắc "thể loại đã có → chỉ viết biến thể mới"); đóng gói lại thành mã `san-khau-x0071-hindi` (PHAN-TICH-VIDEO-MAU.md + CAU-TRUC.json + 2 cặp kịch bản/biến thể "goc" và "hook") nhưng [HAU KY] loai vẫn trỏ về code CHUNG `san-khau-chia-doi-gia-su-ai` (post.py đã tự bật Nirmala UI + shaping complex khi `HAU_KY.ngon_ngu == "hi"`, không cần sửa code). refs tái dùng ảnh AI đã có sẵn của chính thể loại gốc (`anh/hindi/bien-the-01.webp`, `anh/ai-robot-mu-kinh.png`) thay vì chọn trong kho nhân vật chung, vì ảnh đã vetted riêng cho đúng video này (không cắt từ video mẫu, không gen mới).
- Sửa lỗi template khi sao chép: 4 mốc "Diễn biến" của kịch bản `-6CANH` gốc neo vào TỪ TIẾNG BỒ ("Nunca, jamais"/"assim"/"praticar"/"fluência e confiança") dù field này được gửi thẳng cho Muse làm "Timed action beats" (`gen_video.py` dòng ~97) — với câu Hindi các từ đó không tồn tại nên cử chỉ sẽ lia sai nhịp. Sửa thành mốc theo VỊ TRÍ CÂU (đầu câu/giữa câu/nửa sau câu), không phụ thuộc ngôn ngữ.
- Hook mới (kịch bản B) lấy đúng từ insight đã cho (tình huống 3 trong 10 tình huống: không nghe kịp tiếng Anh, chỉ gật "yes, yes"), không suy ra insight khác; cấu trúc câu/độ dài giữ như hook gốc; tình huống (nỗi đau tiệc + giải pháp + demo) giữ nguyên 100%.
- Kết quả: `kiem-tra --tai-anh` cả hai kịch bản: 0 lỗi, 0 cảnh báo (kể cả refs tải được). Nhập Studio: loại `San-khau-the-tu-vung-chia-doi-gia-su-AI-X0071-Hindi-9512` + dự án `X0071-Hindi-Nice-to-meet-you-9ea9` (goc, đã chạy thử `bien-the-01-goc-nam-29`); loại `...-X0071-Hindi-doi-hook-d0f8` + dự án `...-doi-hook-7ed7` (hook, chưa chạy).
  Chạy thử cảnh 1: `scene1_start.png`/`scene1_last.png` ĐẠT — đúng diễn giả Ấn Độ ~29 tuổi, vest navy/cà vạt đỏ mận, mic cài tai, clicker tay phải, sân khấu rèm navy + khối 3D đỏ khớp ảnh gốc; khung cuối đúng tư thế (ngón tay hạ, hai tay gần ngang bụng, miệng khép). Cảnh 2 trở đi và kịch bản B: CHỜ KIỂM CHỨNG (Studio tiếp tục gen nền).
- Áp dụng chung?: CÓ một phần — mốc "Diễn biến" neo theo từ của NGÔN NGỮ KHÁC khi sao chép kịch bản sang ngôn ngữ mới là lỗi lặp lại (đã thấy ở mục 6 sổ tay dạng khác); nên rà lại 4 câu tương tự còn sót trong `KICH-BAN-SAN-KHAU-CHIA-DOI-GIA-SU-AI-6CANH.txt` gốc (Mexico cũng dùng chung file đó nên cũng dính lỗi này).
- Đã chưng cất vào: chưa (đợi xem kết quả gen thật cảnh 1 trước khi đưa vào sổ tay mục 6).

### 20/11/2026 · 8eecbce1-dien-gia-hindi · phân tích + hai kịch bản (goc/hook) + chạy thử · loai: phan-tich
- Hiện tượng: video `8eecbce1-Speaker-HINDI-sample.mp4` 25,6 s CHỈ có phần sân khấu (hook, tiệc 3 câu gạch, thú nhận, giải pháp, giơ điện thoại); cấu trúc người dùng chỉ định thêm demo 5 câu + CTA không có trong video. `danh-gia` tách một giọng nam thành 2 cụm (150 Hz / 205 Hz) do lên giọng nhấn mạnh — không phải hai người (xem ảnh: một người suốt video). Video gốc có lỗi liên tục: ly champagne của cảnh tiệc còn trên tay ở sân khấu 10–14 s.
- Cách làm: dùng lại khuôn `san-khau-chia-doi-gia-su-ai` (bản 6 cảnh Hindi từ `san-khau-x0071-hindi`), giữ demo phần 2 theo người dùng; bỏ ly trên sân khấu; cảnh tiệc đổi sang khung trung từ đùi trở lên như video. Ảnh kho mặc đồ thường → STYLE LOCK/Prompt ảnh ghi "ảnh tham chiếu chỉ cho mặt, tóc, dáng; quần áo theo mô tả". Kịch bản B: mọi thứ của hook là token (`LUOT_1`, `HOOK_HANH_DONG`, `HOOK_DIEN_BIEN`, `HOOK_CAM_XUC`, `HOOK_KHUNG_CUOI`) thay vì chỉ đổi lời như bản x0071. Biến thể sinh bằng `cong-cu/tao_bien_the.py`, tự đổi đuôi động từ Hindi theo giới (देता था/देती थी).
- Kết quả: `kiem-tra --tai-anh` cả hai 0 lỗi 0 cảnh báo; refs mã kho `NAM-30-45-IND-04` + `BOT-TALKA-DEF-INDIA-01` tải được. Nhập Studio A (chạy thử) + B (chưa chạy). Chạy thử cảnh 1: CHỜ KIỂM CHỨNG (cập nhật bên dưới).
- Áp dụng chung?: CÓ — (1) ảnh kho nhân vật mặc đồ thường: kịch bản cần nói rõ ảnh chỉ cho mặt/tóc/dáng, trang phục theo vai; (2) kịch bản "đổi hook" nên token hoá cả cử chỉ/nét mặt/khung cuối của hook chứ không chỉ lời. Chưa chưng cất (chờ kết quả gen).
- Cập nhật 20/11/2026 (chạy thử A, cảnh 1): `phan1/scene1_start.png` ĐẠT — mặt theo ảnh kho NAM-30-45-IND-04 nhưng mặc ĐÚNG trang phục vai (sơ mi hồng, cà vạt, gi-lê + quần kẻ sọc xám, micro cài tai, bút bấm tay phải), sân khấu rèm navy + khối đỏ + đầu khán giả khớp video; không có nền xanh hay quần áo của ảnh kho → câu "ảnh tham chiếu chỉ cho mặt, tóc, dáng; quần áo theo mô tả" có tác dụng. `scene1_cut.mp4` 4,88 s (gốc 4,97 s): giơ ngón trỏ tay phải ở ~0,5 s, hạ trước từ cuối, đứng yên cuối clip, máy đứng yên. ĐẠT (hình). Cảnh 2–6 và phần 2: CHỜ KIỂM CHỨNG (Studio gen tiếp).

### 20/11/2026 · 8da55fc4-dien-gia-hindi · phân tích + hai kịch bản (goc/hook) + chạy thử cảnh 1 · loai: kich-ban
- Hiện tượng: video `8da55fc4-Speaker-HINDI-sample.mp4` trùng từng byte (md5 612b43fa…) với `8eecbce1-Speaker-HINDI-sample.mp4`; `danh-gia --lang hi` cho số đo khớp lần trước (3,42 từ/giây, cắt 4,97 s / 9,97 s). Lần này cấu trúc người dùng chỉ có Hook / Nỗi đau / Giải pháp (không demo, không CTA) → thể loại MỘT phần, 6 cảnh thường, một nhân vật. Xem lại `luot_04.jpg`: ở cảnh tiệc diễn giả nhìn sang PHẢI khung (vai khách mờ góc dưới phải) — hồ sơ `8eecbce1` ghi nhầm "trái".
- Cách làm: dùng lại hậu kỳ `types/san-khau-chia-doi-gia-su-ai` (chữ gạch đỏ + X ở lượt `gach`, phụ đề Hindi) với kịch bản chỉ một dòng `===== PHAN 1 =====` (nhieu_phan.plan chạy được 1 phần, `kiem-tra` 0 lỗi). Kịch bản B sinh từ A bằng `cong-cu/tao_kich_ban_hook.py` (thay nguyên văn từng câu của cảnh 1, assert thấy đúng 1 lần) để hai bản luôn khớp từ cảnh 2. Token hoá thêm `NEN_TIEC`, `DAO_LY` cho biến thể đổi nhân vật/bối cảnh tiệc. Ảnh kho `NAM-30-45-IND-10` (trông già nhất, tóc bạc) cho vai ~50 tuổi.
- Kết quả: `kiem-tra --tai-anh` A và B: 0 lỗi, 0 cảnh báo. Chạy thử A (dự án `8da55fc4-Speaker-Hindi-Me-too-c25b`): `scene1_start.png` ĐẠT (mặt kho + trang phục vai + sân khấu; khung rộng hơn "từ gối" một chút), `scene1_cut.mp4` 4,73 s ĐẠT (ngón trỏ tay phải giơ đúng nhịp rồi hạ, máy đứng yên, mặt giữ nguyên). Cảnh 2–6 + kịch bản B: CHỜ KIỂM CHỨNG.
- Áp dụng chung?: CÓ — (1) hậu kỳ nhiều phần dùng được cho kịch bản 1 phần (chỉ một dòng PHAN 1) khi cần hiệu ứng riêng của thể loại khác mà không viết code mới; (2) sinh kịch bản "đổi hook" từ kịch bản gốc bằng script thay nguyên văn thay vì chép tay hai file.
- Đã chưng cất vào: chưa (chờ kết quả cảnh 2 tiệc và cả video).

### 20/11/2026 · 8da55fc4-dien-gia-hindi · nhóm biến thể yfma9g (đổi bộ bài học) · loai: kich-ban
- Hiện tượng: nhóm đổi lời hook + 3 câu bị gạch, nhưng "Diễn biến" cảnh 2 của kịch bản vẫn ghi cứng 3 câu cũ "(Me too / You're welcome / I'm fine, thanks)" — trường này gửi cho Muse, sẽ lệch với lời mới.
- Cách sửa: bỏ câu cụ thể khỏi "Diễn biến" (chỉ tả "ba câu đáp ngắn, đúng lời của lượt"), sinh lại kịch bản B, PUT /api/types cho hai loại. Biến thể sinh bằng script, `kiem-tra` 0 lỗi.
- Kết quả: CHỜ KIỂM CHỨNG (chưa gen nhóm này).
- Áp dụng chung?: CÓ — khi viết kịch bản có lượt "đổi được" (câu sai, câu hook), mọi trường gửi Muse (Diễn biến, Prompt video, Khung cuối) không được chép nguyên văn lời thoại; chỉ dùng {{LUOT_n}} hoặc tả chung.
- Đã chưng cất vào: chưa.

## 20/11/2026 — Thay màn hình điện thoại cảnh 6 bằng robot AI của người dùng + 2 dự án X0104 (Ả Rập) / X0105 (Hindi)
- **Yêu cầu**: ở các cảnh nhân vật cầm điện thoại (cảnh 6), màn hình phải là robot AI của người dùng (ảnh chân dung nền xanh dương) + chữ "Talka AI". Gen AI không vẽ được đúng ảnh/chữ → làm bằng code ở hậu kỳ.
- **Cách làm** (`app/production/types/san-khau-chia-doi-gia-su-ai/man_hinh_dt.py`, bật bằng `HAU_KY.man_hinh_dt: true`, ảnh `assets/robot-man-hinh-dt.webp`): dò vùng màn hình từng khung (xanh sáng, b−r>22; nền sân khấu tối và áo trắng ngà không ngả xanh nên không nhầm), lấy khung 4 góc bằng thân lồi, chiếu ảnh thay thế có phối cảnh, chỉ vẽ lên vùng màn hình (ngón tay che vẫn giữ). Không đụng mặt. Prompt gen vẫn tả "màn hình = chân dung robot trên nền xanh dương, không chữ" (`DAO_DIENTHOAI`) để Muse tạo màn hình xanh cho bộ dò bám.
- **Bài học dò**: (1) màn hình nhạt (robot trắng giữa nền xanh nhạt) làm vùng xanh bị thủng → fill thấp; phải đo bằng THÂN LỒI, và lấp kín thân lồi khi vẽ (nếu không còn sót thân tối của robot cũ). (2) 4 khung đầu lúc điện thoại vung vào hình bị nhoè (~0,13 s) không dò được → còn hình cũ, chấp nhận. (3) 20 biến thể X0106: hai biến thể (03a, 08a) sót lần đầu vì lý do (1).
- **X0106** (dự án đã gen xong 20/20): thay `scene6_cut.mp4` (gốc lưu `scene6_cut_goc.mp4.bak`) rồi `queue/start` → Studio dựng lại từ clip có sẵn, KHÔNG gen lại. Studio hôm nay chạy cổng 61587 (đọc `userdata/running.json`, không phải 51545).
- **X0104/X0105**: 2 CSV (20 nhân vật Ấn Độ GIỐNG NHAU, X0105 đánh số 21–40; X0104 lời Ả Rập, X0105 lời Hindi) → `BIEN-THE-X0104-ARAB-20.json`, `BIEN-THE-X0105-HINDI-20.json` (tool `cong-cu/tao_bien_the_csv.py arab hindi2`, ảnh `anh/arab/`), kịch bản `KICH-BAN-X0104-ARAB.txt` (= kịch bản X0071 với "Hindi" trong prompt đổi thành {{NGON_NGU}}) và `KICH-BAN-X0105-HINDI.txt`. Dự án Studio: `X0104-Hindi-Arab-20-bien-the-f84d`, `X0105-Hindi-20-bien-the-a1ed`. kiem-tra 0 lỗi.
- **Hỗ trợ tiếng Ả Rập trong hậu kỳ** (`post.py`, `ngon_ngu: "ar"`): máy này Pillow KHÔNG có raqm (không nối chữ/đảo chiều được) và cài thư viện bị chặn → nhãn câu Ả Rập trên thẻ do libass vẽ (style `Lbl`, BorderStyle 3 = ô hồng vừa chữ + gạch chân); phụ đề phần 1 font Arial + shaping complex (libass có HarfBuzz + FriBidi); mốc neo tìm câu tiếng Anh = "الانجليزية"; `phu_de.py` thêm "؟" làm dấu kết câu. Đã thử trên khung đen: chữ nối đúng, phải→trái đúng.
- **Chưa kiểm chứng khi gen thật**: Whisper nghe tiếng Ả Rập (mốc từ để tô vàng và căn phụ đề), giọng Ả Rập của nhân vật Ấn Độ qua Muse, và bộ dò màn hình trên video gen mới của X0104/X0105. Người dùng cần chọn Thương hiệu cho 2 dự án rồi chạy thử MỘT biến thể.

## 20/11/2026 (sau) — Bỏ cách đè hình lên màn hình điện thoại; đưa robot vào kịch bản để Muse vẽ ngay lúc gen
- **Người dùng không chấp nhận cách đè hình ở hậu kỳ** ("không đè lên như thế, thay luôn vào trong kịch bản robot của tôi để làm ngay từ đầu"). Đã GỠ hẳn: bước `man_hinh_dt` trong `post.py`, file `man_hinh_dt.py` và thư mục `assets/` của thể loại; cờ `HAU_KY.man_hinh_dt` không còn. (Công cụ rời `SAMPLE/8da55fc4-dien-gia-hindi/thay_man_hinh_dt.py` + ảnh chỉ còn dùng cho 20 video X0106 đã đè; không dùng cho dự án mới.)
- **Cách mới** (X0104 + X0105, kịch bản `KICH-BAN-X0104-ARAB.txt` / `KICH-BAN-X0105-HINDI.txt`, tạo bằng `cong-cu/tao_bien_the_csv.py arab hindi2`): robot đi vào cảnh 6 như một "nhân vật" phụ DT — biến thể có `TEN_DT`, ảnh `refs.NGUOI_DT` = `SAMPLE/san-khau-chia-doi-gia-su-ai/anh/robot-talka-dien-thoai.webp`. Lý do: `engine.run_variant` chỉ gửi kèm lệnh gen VIDEO các ảnh có khoá `NGUOI_*` và chỉ của nhân vật có token `NGUOI_<c>`/`TEN_<c>` trong cảnh (`scene_ref_filter`) → khai `{{TEN_DT}}` trong CẢNH 6 thì ảnh robot chỉ đi cùng cảnh 6, không lẫn vào các cảnh khác/phần 2. `DAO_DIENTHOAI` chỉ còn tả chiếc điện thoại; màn hình do đoạn "PHONE SCREEN" trong Prompt video cảnh 6 tả (robot đầu+vai nền xanh dương + chữ "Talka AI" trắng, "chỉ là hình trên màn hình, không phải robot đứng trong phòng").
- **Chặn chữ cũ**: [NEGATIVE] chung của phần 1 từng cấm "text, letters, words, icons, inset window" → sẽ triệt luôn chữ Talka AI; đã đổi thành cấm chữ trên phông/phụ đề/đè lên video và cho phép đúng "Talka AI" trên màn hình điện thoại. Negative cảnh 6 thay "text on the phone screen" bằng "robot khác / robot đứng trong phòng / chữ sai chính tả trên màn hình".
- **Nhập lại Studio**: dự án chưa chạy nên xoá 2 dự án + 2 loại cũ rồi nhập lại → `X0104-Hindi-Arab-20-bien-the-4c1e`, `X0105-Hindi-20-bien-the-083b` (tên biến thể `X0104_Speaker Arabic Nam_01` … `Nữ_20`; X0105 cũng 01–20). kiem-tra 0 lỗi (20 cảnh báo tên biến thể không phải dạng slug — chủ ý theo yêu cầu).
- **Chưa kiểm chứng (rủi ro chính)**: Muse có vẽ đúng robot từ ảnh và chữ "Talka AI" đọc được trên màn hình nhỏ hay không (chữ AI thường méo); có sinh thêm robot đứng trong phòng không (chú thích ảnh nhân vật của engine nói "giữ mặt/áo, không phải nhân vật khác" — có thể làm Muse coi nó là người thứ hai). Phải xem `scene6_last.png` của biến thể chạy thử đầu tiên. Nếu chữ méo: chỉ còn cách bỏ chữ khỏi prompt (robot thì vẫn ra) — không quay lại đè hình.

## 20/11/2026 (cuối) — Thử ảnh robot phông xanh lá 9:16 cho màn hình điện thoại: người dùng báo "không work"
- Dự án phụ `X0104 TEST canh 6` (1 cảnh = khung đầu cảnh 1 + hành động cảnh 6) dùng để thử riêng cảnh giơ điện thoại. Bản nền xanh dương (ảnh vuông) và bản phông xanh lá (ảnh 9:16 lấp kín màn hình) đều gen được robot + chữ "Talka AI" trên màn hình, nhưng người dùng kết luận cách phông xanh lá KHÔNG đạt → đã xoá dự án phụ + loại + file thử; giữ nguyên cách ảnh robot nền xanh dương (refs.NGUOI_DT) cho X0104/X0105/X0106.
- Chốt: Muse luôn vẽ lại màn hình theo ảnh tham chiếu, không dán nguyên ảnh; muốn đúng từng pixel chỉ có đè hình (người dùng đã bác). Không thử lại hướng khung đầu ghép sẵn trừ khi người dùng đề nghị.
- X0104/X0105: sau video thử số 01 đã chạy 02–20 của cả hai dự án theo cách này.

## 20/11/2026 — Lỗi "dính người ở góc màn hình" ở cảnh sân khấu 3–6 (X0104, X0105 video 01)
- **Hiện tượng**: cảnh 2 là cảnh tiệc có một vị khách quay lưng mờ ở mép phải; từ cảnh 3 đến 6 (sân khấu) vẫn thấy đầu/vai người đó ở mép phải khung, X0104 còn cầm ly champagne và cảnh 3 bị zoom cận (khung đầu cảnh 3 là khung rộng của cảnh 1 nhưng clip trôi dần), lỗi lan sang cảnh 4–6 vì mỗi cảnh nối từ khung cuối cảnh trước.
- **Nguyên nhân**: [CHAR LOCK] và [STYLE LOCK] là khối dùng chung, được chèn vào Prompt video của MỌI cảnh, và chứa câu riêng cho cảnh tiệc: "in the reception clip he looks at the person he is chatting with, who stays just out of frame". Cảnh sân khấu vì thế được dặn có "người đang trò chuyện ngoài khung" → Muse vẽ thêm người ở mép khung. Thêm nữa câu SETTING liệt kê "banquet, chandelier hall, champagne glass or party" trong Prompt video (câu khẳng định, không phải Negative) mớm ly rượu.
- **Sửa** (cho cả họ san-khau, 19 file kịch bản/loại — script `fix_guest.py`): EYE LINE chỉ còn "nhìn ống kính, MỘT MÌNH trong khung, không vai/đầu/bóng mờ của ai ở mép khung, tay không cầm gì ngoài khung đầu"; STYLE LOCK bỏ vế cảnh tiệc; Prompt video cảnh tiệc thêm ngoại lệ "RECEPTION CLIP ONLY: nhìn người ngoài khung, giữ vai/gáy mờ ở mép phải"; Negative các cảnh sân khấu thêm "another person at any edge of the frame, a guest's shoulder or the back of a head, a champagne glass or any drink in the hand"; SETTING bỏ "banquet, chandelier hall, champagne glass".
- **Bài học chung**: lock dùng chung cho nhiều cảnh KHÔNG được chứa câu chỉ đúng cho MỘT cảnh (cảnh tiệc, cảnh đổi góc…) — Muse làm theo mọi câu nó thấy trong prompt. Câu loại trừ ("never a ballroom…") đặt trong lời khẳng định cũng mớm đúng thứ cần tránh: để trong Negative.
- **Video đã gen** (X0104/X0105 số 01): chuyển cảnh 3–6 cũ vào `_loi_canh3-6/`, chạy lại để gen cảnh 3–6 với kịch bản đã sửa (các cảnh khác giữ). Kết quả: CHỜ KIỂM CHỨNG.

## 20/11/2026 — Lệch màu giữa các cảnh sân khấu 1,3,4,5,6 (X0104, X0105)
- **Hiện tượng**: cảnh 3–6 mỗi cảnh một tông (da ngả cam ở cảnh 5–6 của X0104, nhạt ở cảnh 6 của X0105, áo xám/xanh lệch). Người dùng yêu cầu lấy cảnh 1 làm chuẩn, bỏ cảnh 2 (tiệc).
- **Nguyên nhân**: engine (`color_mode: anchor`) chỉ kéo màu mỗi cảnh về khung đầu CỦA CHÍNH cảnh đó (cảnh tiệc làm chuẩn cho 3–6 khi cảnh 3 thiếu "Prompt ảnh" — đã sửa riêng) và `_grade` giới hạn nhỏ (bão hoà 0,8–1,35, U/V ±8). Chế độ `first` ép cả cảnh tiệc về cảnh 1 nên không dùng. Phần 2 (ghép 2 lớp, `split.py`) không có bước cân màu nào.
- **Sửa** (hậu kỳ, không cần khởi động lại Studio): `app/production/types/san-khau-chia-doi-gia-su-ai/man_mau.py` + bước 0a trong `post.py` — đo MÀU DA diễn giả (Haar + vùng má/trán, trung vị U/V) của cảnh 1 làm chuẩn rồi kéo bão hoà + U/V của từng cảnh sân khấu phần 1 (trừ lượt có "gach") về chuẩn bằng `eq`/`lutyuv` có `enable=between(t,...)`. KHÔNG đụng độ sáng.
- **Bài học đo màu**: đo cả khung để so cảnh toàn thân (cảnh 1) với cảnh cận bị lệch theo BỐ CỤC (cảnh 4 bị 'thiếu bão hoà 30%' chỉ vì ít khối đỏ trong khung) → sẽ chỉnh quá tay; phải đo trên thứ có mặt ở mọi cảnh (da). Đã thử: da cảnh 6 X0104 bớt cam, các cảnh khác đổi nhẹ.
- **Chưa làm**: phần 2 (cảnh 7–16) vẫn lệch giữa các cảnh (độ sáng/tông diễn giả); chờ người dùng chọn chuẩn cho phần 2.
- `python -I` không thêm thư mục script vào sys.path → post.py phải tự thêm HERE trước khi `import man_mau`.

## 19/11/2026 · bb327bac-ref-noi-chuyen (video mới, chạy ngầm)
- Hiện tượng: video PiP robot trên + người học dưới, 1 phần, tiếng Tây Ban Nha → làm bản tiếng Anh. Khuôn ghép 2 lớp (mẫu ghep-hai-lop) + `post.py`/`config.json` riêng (không gen.py). Tạo 2 kịch bản (A giữ hook, B đổi hook với token `HOOK_TV`).
- Ảnh: robot dùng lại `robot-talka.png`; người học gen Muse nền xanh (đạt, 1 lần). `base_HOC`/`base_DAY`/clip cảnh 1 đạt.
- Kết quả: cảnh 1 ĐẠT; cả video CHỜ KIỂM CHỨNG. Áp dụng riêng thể loại; chưa chưng cất.

## 19/11/2026 · 6fbf4a4b-ref-noi-chuyen (video mới, chạy ngầm, bản NGƯỜI THẬT của bb327bac-ref-noi-chuyen)
- Hiện tượng: cùng video (md5 trùng bb327bac) nhưng người dùng đòi nhân vật + bối cảnh là người thật, không hoạt hình. Dùng lại phân tích; STYLE LOCK "photorealistic live-action", NEGATIVE thêm cartoon/3D render; ảnh người học gen bằng `cong-cu/gen_anh_that.py` (nạp `gen-anh-nhan-vat.py` rồi ghi đè STYLE/NEG, không sửa mã chung): đạt lần đầu, một người, nền xanh phẳng.
- Chạy thử goc-01: `base_HOC.png` là người thật trong bếp thật, `base_DAY.png` robot nền đen; Studio gen lại cảnh 1 một lần do Muse phóng hình (`.zoom.mp4`), clip cuối robot nói, đạt.
- Kết quả: cảnh 1 ĐẠT; cả video và kịch bản B CHỜ KIỂM CHỨNG. Riêng thể loại; gợi ý chưa chưng cất: thêm tuỳ chọn ảnh thật cho gen-anh-nhan-vat.py dùng chung.

## 19/11/2026 · 6fbf4a4b-ref-noi-chuyen: nhóm biến thể sa5mxj (6 người học Âu Mỹ, phòng khách, robot BOT-TALKA)
- Hiện tượng: kịch bản cứng "tay đặt ở bồn rửa" + "bếp" nên không đổi được hành động/bối cảnh. Sửa: thêm token `DONG_HOC` (tư thế/tay) và câu "chỉ lấy mặt, tóc, quần áo từ ảnh tham chiếu, bỏ nền xanh và tư thế đứng"; "kitchen" → "calm background"; NGHE_HOC bỏ "sink". Đã PUT vào loại dự án và thêm DONG_HOC cho biến thể mẫu (kịch bản B không đổi).
- Ảnh: 7 ảnh người dùng tải từ Drive bằng link `drive.usercontent.google.com/download?id=..&export=download&confirm=t` (đổi webp → png), robot BOT-TALKA tả lại trong NGUOI_DAY; phòng khách gen bằng `cong-cu/gen_anh_that.py --bc` (đạt lần đầu) gắn `refs.NEN_HOC`. `kiem-tra` 0 lỗi.
- Kết quả: CHỜ KIỂM CHỨNG (chưa gen video). Riêng thể loại.

## 19/11/2026 · 6fbf4a4b-ref-noi-chuyen: sửa theo góp ý sau chạy thử goc-01
- Hiện tượng (final.mp4): (1) robot đổi mắt/giọng giữa các clip; (2) mặt người học nằm ở 40-55% khung, ô robot (đáy 33%) + phụ đề ô trắng che nửa mặt; (3) mỗi chỗ đổi cảnh người học khựng: đo diff vùng dưới có 1-3 khung đứng yên tại 1.5, 3.2, 7.9, 9.9, 23.9, 32.3 s và nhảy mạnh tại 16.8, 25.8 s; (4) viền sai/đúng chỉ phủ nửa màn hình.
- Nguyên nhân: (1) khối robot không khoá mắt/giọng; (2) kịch bản đặt đầu ở 40%, cỡ chest-up; (3) clip nghe có "liếc lên + gật" khác tư thế clip nói; (4) `config.json` chép `vien {x 0.5, rong 0.5}` của thể loại chia đôi dọc.
- Sửa: (1) NHAN VAT DAY khoá mắt xanh nhạt + "exact same voice"; (2) NHAN VAT HOC: waist-up, lùi xa, tóc ở 55%, mắt 62%, nửa trên khung trống; phụ đề co_chu 50; (3) NGHE_HOC: mắt nhìn máy, đầu/người đứng yên đúng tư thế clip nói, thêm "trở về cùng tư thế nghỉ giữa các lượt"; (4) bỏ `vien` khỏi config.json (viền toàn màn hình). Áp cả hai kịch bản và PUT cả hai loại dự án.
- Kết quả: CHỜ KIỂM CHỨNG (đợi gen lại). Khựng 1-3 khung ở chỗ nối là cơ chế nối clip chung của engine; nếu vẫn còn, cần xem xét engine (ngoài phạm vi thể loại). Chưa chưng cất.

## 19/11/2026 · 6fbf4a4b-ref-noi-chuyen: lỗi "Script còn token chưa có giá trị: DONG_HOC"
- Hiện tượng: Studio báo thiếu giá trị DONG_HOC khi chạy biến thể test của dự án 6fbf4a4b-ref-noi-chuyen-b36a.
- Nguyên nhân: khi nhóm sa5mxj thêm token DONG_HOC vào kịch bản A và PUT loại dự án, tôi chỉ sửa file `BIEN-THE-*.json` mà quên cập nhật biến thể đã nằm trong dự án Studio (dự án giữ bản sao riêng).
- Sửa: PUT `/api/projects/<id>` thêm DONG_HOC cho biến thể 6fbf4a4b-goc-01 (đúng giá trị trong file mẫu). Kịch bản B không dùng token này.
- Bài học (chung): thêm token vào kịch bản của thể loại đã nhập thì phải cập nhật CẢ biến thể trong các dự án đang có, không chỉ file JSON. Kết quả: CHỜ KIỂM CHỨNG.

## 19/11/2026 · 6fbf4a4b-ref-noi-chuyen: tự kiểm tra lượt chạy sau sửa (Bước 5)
- Hiện tượng: lượt gen lại 18:43 của goc-01 báo lỗi "No such file ... scene1_spk.mp4(.zoom.mp4)" (18:47) và thư mục run không còn clip nào để xem (chỉ base_*.png, script.txt). Log có dòng "Ghép 2 lớp ..." in 2 lần cùng lúc và 2 lần "Cảnh 1: clip DAY lệch/tự phóng (1.41, 1.25), gen lại": hai worker cùng chạy một biến thể và đổi tên/xoá file của nhau (sau 2 lần tự xếp lại hàng vì lỗi DONG_HOC). Lỗi tương tự ở sa5mxj-nam1 (".dang-ghi" mất sau khi bấm dừng 18:29). Hàng đợi chung đang có 40 mục taxi chờ.
- Nguyên nhân: đua file do chạy trùng/dừng giữa chừng (Studio), không phải kịch bản. Robot clip bị Muse phóng 1.25-1.41 (engine gen lại).
- Sửa: kịch bản A và B thêm "đầu và vai robot giữ đúng cỡ/vị trí mọi clip, không đẩy máy/zoom" (PUT cả hai loại dự án); xếp lại ĐÚNG MỘT mục goc-01 (không có cảnh nào xong để "làm lại riêng cảnh").
- Kết quả: CHỜ KIỂM CHỨNG; chưa có scene*_start/clip để đối chiếu bảng hành động. Riêng thể loại; lỗi đua file là của engine, chưa sửa (ngoài phạm vi).

## 19/11/2026 · 6fbf4a4b-ref-noi-chuyen: nhóm biến thể 7jbjlc (cùng mô tả với sa5mxj)
- Mô tả người dùng trùng nhóm sa5mxj nên dùng lại 7 ảnh (đã tải, sao sang `anh/nhom-7jbjlc/`) và script `cong-cu/tao_bien_the_nhom_7jbjlc.py` (bản sao đổi tiền tố tên `7jbjlc-*`); kịch bản đã có token DONG_HOC. `kiem-tra` 0 lỗi. CHỜ KIỂM CHỨNG, chưa gen. Riêng thể loại.

## 20/11/2026 · 6fbf4a4b-ref-noi-chuyen: nhóm biến thể w8sqp4 (Hindi, 20 biến thể, mã kho nhân vật India)
- Cách làm: lời Hindi Devanagari của người dùng (lượt 3, 4-13) xen "I am India." (wrong) / "I am from India." (right, `to` = "I am from India"), tên app Talka AI. 20 biến thể = 5 NU 20-30 + 5 NU 30-45 (bot BOT-TALKA-DEF-INDIA-02, kịch bản "danh sách A") + 5 NAM 20-30 + 5 NAM 30-45 (bot BOT-TALKA-DEF-INDIA-01, "danh sách B"); `refs` ghi MÃ kho, ngoại hình tả theo ảnh đã xem. Giọng robot A nam/baritone, robot B nữ.
- `config.json` của thể loại: thêm font Nirmala UI, shaping complex, whisper "small" (phụ đề chữ Hindi, xem sổ tay mục 6); ảnh hưởng nhẹ các nhóm tiếng Anh (whisper đa ngôn ngữ).
- `kiem-tra`: 0 lỗi; cảnh báo lượt 7 (24 từ) và 11 (22 từ) > 20 vì giữ nguyên lời người dùng; câu Devanagari Muse nói chưa kiểm chứng. CHỜ KIỂM CHỨNG, chưa gen. Riêng thể loại.

## 20/11/2026 · 6fbf4a4b-ref-noi-chuyen: nhóm biến thể pq92tq (Hindi, 40 biến thể, đủ 40 mã kho India)
- Cùng lời Hindi và cấu trúc với w8sqp4 nhưng dùng ĐỦ 20 mã nữ (bot BOT-TALKA-DEF-INDIA-02) + 20 mã nam (bot BOT-TALKA-DEF-INDIA-01) theo thứ tự người dùng ghi (20-30t 01-10 rồi 30-45t 01-10); script `cong-cu/tao_bien_the_nhom_pq92tq.py`. Đã xem ảnh 20 mã mới (06-10 mỗi nhóm) để tả ngoại hình; tên biến thể `pq92tq-<mã rút gọn>` duy nhất, 40 mã `refs` khác nhau.
- `kiem-tra`: 0 lỗi, 80 cảnh báo (lượt 7 và 11 quá 20 từ vì giữ nguyên lời Hindi). CHỜ KIỂM CHỨNG, chưa gen. Riêng thể loại.
