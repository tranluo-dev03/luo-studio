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
- Kết quả: CHỜ KIỂM CHỨNG (cần khởi động lại Studio để nạp). Áp dụng chung?: CÓ. Đã chưng cất vào: chưa.

### 2026-11-05 · xe-tai-canh-sat-gia-su-ai · lượt gen 2 (robot Talka), video cuối · loai: studio
- Hiện tượng: `final.mp4` 82,6 s (18:42). Phần 1 giữ nguyên lượt 1. Phần 2: robot đúng ảnh mẫu suốt 13 cảnh, ô AI đứng yên, đáy sạch, mặt tài xế dưới ô;
  phụ đề y 1560 nằm ngang ngực ở cả hai phần, không che mặt; viền đỏ cảnh "I am very hurry", icon ✓ / ✗ / $ đúng chỗ.
- Kết quả: ĐẠT (sửa 1, 2, 3 xác nhận). Còn khác mẫu: dài ~1,6 lần mẫu; lời thoại vẫn gọi app "LangLearn".
- Áp dụng chung?: xem các mục sửa 1–3. Đã chưng cất vào: chưa.
