# Đo hiệu năng gen video: tìm điểm nghẽn, số luồng tối ưu, cấu hình máy chủ

Công cụ: `SAMPLE/_chung/do-hieu-nang.py` (`theo-doi` lấy mẫu máy trong lúc gen, `bao-cao` tổng hợp). Dữ liệu gốc đã có sẵn,
không cần sửa code Studio: LUO-API ghi mốc thời gian từng bước của MỌI lệnh gen vào `userdata/api/data/tasks.json`.

## 1. Đường đi của một cảnh (để biết đo ở đâu)

```
Studio (parallel = số video chạy cùng lúc, tối đa 8)
  └─ mỗi video: các cảnh chạy TUẦN TỰ. Mỗi cảnh: gen ảnh khung đầu -> gen video -> cắt & kiểm tra
       ├─ gen ảnh / gen video  -> POST LUO-API (cùng máy) -> chờ 1 s/lần hỏi
       │     LUO-API: semaphore MUSE2API_CONCURRENCY (mặc định 8) -> chọn tài khoản (mỗi tài khoản tối đa
       │     MUSE2API_ACCOUNT_PARALLEL việc, mặc định 2) -> một tab Chromium / việc (~300 MB RAM) -> đính ảnh, gửi prompt
       │     -> MUSE VẼ TRÊN MÁY CỦA MUSE (một tài khoản = một VM riêng của Muse) -> tải file về data/media
       └─ cắt & kiểm tra (trong máy): ffmpeg (libx264 crf 17), Whisper small int8 CPU (1 tiến trình dùng chung, có khoá
             _WH_LOCK -> mọi video xếp hàng), mediapipe dò miệng (khoá _MP_LOCK, cũng xếp hàng)
```

Suy ra 4 nhóm yếu tố quyết định tốc độ:

| Nhóm | Gồm | Ai chịu | Cách đo |
| --- | --- | --- | --- |
| A. Muse vẽ | thời gian từ lúc Muse nhận prompt tới lúc có file | máy của Muse, tải trên VM của từng tài khoản | `timing.muse_render` trong tasks.json (mục 1, 2, 3 của `bao-cao`) |
| B. Trình duyệt + LUO-API | mở tab, đính ảnh, gửi, xác nhận, tải file | CPU/RAM máy mình, mạng | `checkout…confirmed`, `media_seen…downloaded` (mục 1) |
| C. Hậu kỳ trong máy | ffmpeg, Whisper, mediapipe cho từng cảnh | CPU máy mình, bị khoá tuần tự | bước "Cắt & kiểm tra" trong bảng Các bước của Studio; CPU% nhóm ffmpeg/python trong CSV |
| D. Chờ tài nguyên | chờ tài khoản rảnh, 429 hàng đợi đầy, Studio chờ luồng | số tài khoản, parallel | `queue_wait`, `n429` trong trace cảnh, `api_cho` / `studio_video_cho` trong CSV |

## 2. Điều đã đo được từ dữ liệu hiện có (600 lệnh gen, 28 giờ, máy Ryzen 5 5500 / 16 GB / không dùng GPU)

Chạy `runtime\python.exe SAMPLE\_chung\do-hieu-nang.py bao-cao` để xem bản mới nhất. Kết quả 07/11/2026:

| | ảnh | video |
| --- | --- | --- |
| Muse vẽ (trung vị / p90) | 34.5 s / 50 s | 47.9 s / 62.7 s |
| Mọi bước trong máy (mở chat + đính ảnh + gửi + xác nhận + tải về) | ~2.5 s | ~3.5 s |
| Tỉ lệ Muse vẽ trên tổng lệnh gen | 93 % | 93 % |

- **Máy mình chỉ chiếm ~7 % thời gian một lệnh gen.** CPU/RAM/ổ đĩa nhanh hơn không rút ngắn một cảnh được bao nhiêu.
- **Chạy 1, 2, 3 việc cùng lúc: Muse vẽ không chậm hơn** (46.8 / 46.6 / 49.7 s). Từ 4 việc trở lên p90 tăng vọt (87 s ở 4, 164 s ở 5):
  đó là lúc Muse bắt đầu nghẽn, không phải máy mình.
- Tài khoản 142 chạy 1, 2, 3 việc cùng lúc đều ~48 s; tài khoản 397 chạy 2 việc đã 52 s, 3 việc lên 164 s (mẫu ít). **Mỗi tài khoản
  chịu tải khác nhau**, cần đo riêng từng tài khoản (mục 3 của báo cáo).
- Lỗi chủ yếu là **tài khoản không được gen video** ("not available for this account / in your country") và hết hạn mức 24 giờ, không
  phải lỗi máy. Tài khoản tốt quan trọng hơn máy tốt.
- Chưa có số đo CPU/RAM trong lúc gen (mục 5 báo cáo trống) vì chưa chạy `theo-doi`. Đây là việc cần làm ở bước 3.

Kết luận sơ bộ: **thông lượng = (số việc Muse chạy song song mà không chậm) / (thời gian một cảnh).** Số việc song song bị chặn bởi
số tài khoản × số việc mỗi tài khoản chịu được, không phải bởi CPU. Máy chủ chỉ cần đủ để nuôi số tab Chromium đó và hậu kỳ.

### 2b. Mô hình thật đang dùng: một tài khoản = một video, cảnh nối tiếp

Cách chạy hiện tại không có hai việc cùng lúc trên một tài khoản (trừ tài khoản 142 có 69 lệnh chồng nhau, vì `ACCOUNT_PARALLEL` mặc định 2
cho phép ghim 2 video lên một tài khoản khi parallel > số tài khoản; muốn ép đúng 1 video/tài khoản thì đặt `MUSE2API_ACCOUNT_PARALLEL=1`).
Khi đó mỗi tài khoản là **một dây chuyền nối tiếp**: gen → máy mình xử lý → gen → … và tốc độ = số tài khoản × tốc độ một dây chuyền.
Đo trên 5 tài khoản (mục 3b của `bao-cao`):

| Tài khoản | Lệnh gen | Tài khoản bận (Muse+API) | Trống giữa hai lệnh (trung vị / p90) |
| --- | --- | --- | --- |
| 396 | 161 | 73 % | 26.8 s / 44.8 s |
| 397 | 149 | 77 % | 17.9 s / 41.8 s |
| 259 | 43 | 63 % | 17.3 s / 30.7 s |
| 390 | 66 | 44 % (15 lệnh lỗi, gen lại) | 21.7 s / 50.5 s |

**Một phần tư thời gian tài khoản ngồi chờ máy mình.** Khoảng trống ~18-27 s mỗi lệnh gen là các bước trong máy cộng các độ trễ nối tiếp
(hỏi trạng thái mỗi 1 s, đọc file, ghi log). Đo trực tiếp ở trạng thái đã ấm trên clip cảnh 5.6 s, 720×1280 (Ryzen 5 5500, 07/11/2026):

| Bước trong máy | Thời gian (ấm) | Ghi chú |
| --- | --- | --- |
| Whisper `voice_span` (small.en int8) | 2.3-2.7 s | trước đây MỘT tiến trình + khoá chung `_WH_LOCK` |
| Whisper `speech_issues` (kiểm lời sau cắt) | 2.3-2.5 s | lần Whisper thứ hai mỗi cảnh |
| ffmpeg libx264 crf 17 mã hoá lại clip | 2.9 s (auto) / 5.9 s (1 luồng) | nhiều ffmpeg cùng lúc chia nhau nhân CPU |
| `smart_cut` (cắt + khung cuối) | 1.0-2.0 s | |
| mediapipe dò miệng `mouth_check` (người nói + người nghe) | 0.9-1.7 s | trước đây dưới khoá chung `_MP_LOCK` |
| `speech_end_of`, `color_stats`, `_first_closed_mouth` | < 1.2 s mỗi bước | |
| Lần đầu mỗi phiên Studio: import mediapipe 22 s, nạp Whisper 50-60 s | một lần | không tính vào từng cảnh |

Phần tính toán thật ~12-15 s mỗi cảnh; Whisper chiếm non nửa. Vì Whisper trước đây chỉ có **một tiến trình và một khoá chung**, khi N video chạy
song song mỗi lần nghe lời phải chờ tới N × 2.5 s, hai lần mỗi cảnh. Với 8 luồng, riêng chờ Whisper có thể thêm ~40 s cho một cảnh.
Đã sửa (07/11/2026): Whisper thành bể tối đa `LUO_WHISPER_WORKERS` tiến trình (mặc định 3, ~600 MB RAM mỗi tiến trình, mở thêm khi bận);
mediapipe bỏ khoá chung, chỉ chặn số lượt cùng lúc = số nhân CPU / 2.

Kiểm chứng (6 cảnh thật, mỗi cảnh = voice_span + speech_issues + mouth_check, Ryzen 5 5500 6 nhân):

| | Thời gian 6 cảnh | Mỗi cảnh |
| --- | --- | --- |
| Tuần tự (như khoá chung cũ) | 39.4 s | 6.6 s |
| 6 luồng song song, bể Whisper 3 tiến trình đã ấm | 28.2 s | 4.7 s |

Kết quả từng cảnh giống hệt nhau. Chỉ nhanh 1.4 lần vì 6 nhân CPU đã kín (Whisper và mediapipe đều đa luồng): **hậu kỳ song song tỉ lệ với số
nhân CPU**, đây là lý do duy nhất để máy chủ nhiều nhân hơn. Ước với 8 luồng video: máy 6 nhân xử lý ~4.7 s/cảnh, máy 12 nhân ~2.5-3 s/cảnh.

Ngoài ra, mỗi cảnh thường cần **nhiều hơn một lệnh gen video** vì các bước kiểm tra (lời thừa/thiếu, máy trôi, miệng người nghe) cho gen lại:
video 28 cảnh mất 75-109 phút, tức 160-230 s mỗi cảnh, trong khi một lệnh gen video chỉ ~51 s. Ước tính ~1.5-2 lệnh gen video mỗi cảnh.
Mỗi lần gen lại tốn thêm ~50 s Muse + ~30 s máy, nên **giảm số lần gen lại (prompt ổn hơn, nới ngưỡng kiểm tra) có tác dụng lớn hơn mọi nâng cấp máy.**

Công thức ước thông lượng theo mô hình này:

```
thời gian một cảnh  ≈  (số lệnh gen / cảnh) × (Muse vẽ ~48 s + API ~3.5 s)  +  máy mình ~30 s (+ chờ khoá khi nhiều luồng)
clip (cảnh) / giờ   ≈  số tài khoản × 3600 / thời gian một cảnh
```

Với 1.7 lệnh gen/cảnh: một cảnh ≈ 1.7 × 51.5 + 30 ≈ 118 s → **~30 cảnh/giờ/tài khoản**, 6 tài khoản → ~180 cảnh/giờ (~6 video 28 cảnh).
Bỏ được khoá mediapipe và rút bước dò miệng xuống ~5 s thì một cảnh còn ~100 s (+18 %); giảm gen lại từ 1.7 xuống 1.2 lệnh/cảnh thì còn ~92 s (+28 %).

## 3. Quy trình test (làm trên máy hiện tại trước, rồi lặp lại trên máy chủ thuê thử)

Chuẩn bị một bộ việc giống nhau cho mọi lần: một dự án có **12 biến thể cùng thể loại** (vd. soi-hanh-ly, 6-8 cảnh/biến thể). Mỗi lần
test chạy đúng bộ này để so sánh được.

Mỗi lần test:

1. Đặt cấu hình (xem mục 4), khởi động lại Studio bằng `LUO Studio.bat`.
2. Mở cửa sổ lệnh, chạy theo dõi với nhãn ghi rõ cấu hình:
   ```
   runtime\python.exe SAMPLE\_chung\do-hieu-nang.py theo-doi --moi 5 --nhan p4-a2-tk3
   ```
   (p4 = parallel 4, a2 = account_parallel 2, tk3 = 3 tài khoản). Ghi lại giờ bắt đầu.
3. Trong Studio chọn cả 12 biến thể, bấm Chạy. Chờ xong hết (hoặc đủ ~60 phút). Ghi giờ kết thúc. Ctrl+C dừng theo dõi.
4. Báo cáo cho đúng khoảng giờ đó:
   ```
   runtime\python.exe SAMPLE\_chung\do-hieu-nang.py bao-cao --tu "2026-11-08 09:00" --den "2026-11-08 10:10"
   ```
   (`--csv` tự lấy file CSV mới nhất). Chép 3 con số vào bảng: **clip/giờ thực** (số cảnh xong ÷ giờ), **p90 Muse vẽ**, **CPU p90 / RAM trống min**.

Ma trận thử, mỗi ô một lần chạy (~1 giờ):

Theo mô hình một tài khoản = một video (mục 2b), đặt `MUSE2API_ACCOUNT_PARALLEL=1` cho mọi lần và chỉ thay đổi số tài khoản = parallel:

| Lần | Studio `parallel` = số tài khoản | Mục đích | Nhìn vào |
| --- | --- | --- | --- |
| 1 | 1 | mốc chuẩn: một dây chuyền không ai tranh | "trống tv" mục 3b (kỳ vọng ~20-27 s), CPU p90 |
| 2 | 3 | 3 dây chuyền: khoảng trống có dài ra không | "trống tv" so lần 1; Muse vẽ không đổi |
| 3 | 6 | 6 dây chuyền: khoá mediapipe bắt đầu lộ | "trống tv" p90; CPU p90; `python_cpu_pct` |
| 4 | 8 | trần của Studio | clip/giờ có còn tăng tuyến tính theo số tài khoản không |
| 5 (tuỳ chọn) | 3 tài khoản, `ACCOUNT_PARALLEL=2`, parallel 6 | so với lần 3: cùng 6 luồng nhưng ít tài khoản hơn, Muse có chậm không | Muse vẽ theo tài khoản, mục 3 |

Nếu clip/giờ ở lần 4 ≈ 8/3 × lần 2 thì máy không nghẽn tới 8 luồng, cứ thêm tài khoản. Nếu thấp hơn rõ và "trống tv" dài ra thì máy nghẽn ở hậu kỳ
(mediapipe/Whisper), xử lý bằng cách bỏ khoá chung (mục 4) trước khi mua máy to hơn, vì CPU to không giúp một bước đang bị xếp hàng tuần tự.

Đọc kết quả:

- clip/giờ tăng theo parallel mà p90 Muse vẽ không đổi: **chưa nghẽn**, tăng tiếp.
- p90 Muse vẽ tăng > 30 % so với lần trước, clip/giờ không tăng: **nghẽn phía Muse trên tài khoản** -> giảm `ACCOUNT_PARALLEL`, thêm tài khoản.
- `queue_wait` hoặc `api_cho` > 0 kéo dài, `studio_video_cho` > 0: **thiếu tài khoản so với parallel** (Studio chờ LUO-API). Parallel hữu ích
  tối đa = số tài khoản × ACCOUNT_PARALLEL; đặt cao hơn chỉ thêm lỗi "chờ tài khoản quá hạn".
- CPU p90 > 85 % hoặc RAM trống < 1.5 GB: **nghẽn máy** (xem mục 5). Dấu hiệu kèm theo: bước "Cắt & kiểm tra" trong trang chi tiết video dài hơn
  hẳn so với lần 1 (Whisper/mediapipe xếp hàng vì khoá chung).
- Mạng: `mang_nhan_kbps` bình thường chỉ vài trăm kbps (clip 5 s ~ 2-5 MB); `tải về` > 3 s hoặc `đính ảnh+gửi` > 3 s mới là mạng yếu.

Số luồng tối ưu = ô có clip/giờ cao nhất mà tỉ lệ lỗi không tăng và p90 chưa vỡ. Theo dữ liệu hiện có, dự đoán: **mỗi tài khoản 2 việc,
parallel = 2 × số tài khoản**, miễn là mỗi tài khoản được kiểm tra riêng (tài khoản 397 có dấu hiệu chỉ chịu 1).

## 4. Chỉnh ở đâu

| Thứ | Chỗ chỉnh | Ghi chú |
| --- | --- | --- |
| Số video Studio chạy cùng lúc | Cài đặt Studio `parallel` (ô Song song khi bấm Chạy) | trần `LUO_MAX_PARALLEL` (biến môi trường, mặc định 32; trước 07/11/2026 chặn cứng 8). Ô Song song liệt kê tới trần này |
| Tổng việc LUO-API chạy cùng lúc | `MUSE2API_CONCURRENCY=` trong `userdata/api/.env` | đã đặt 24 (07/11/2026); phải ≥ số luồng Studio. Launcher giữ nguyên các dòng khác khi ghi lại file |
| ffmpeg mã hoá cảnh cùng lúc | `LUO_FFMPEG_SCENE` (mặc định = số nhân THẬT / 2: 6 nhân -> 3, 16 -> 8, 32 -> 16) | thêm 07/11/2026 (`crun` trong `app/luo-studio/engine.py`): mọi ffmpeg libx264 qua một cửa, chạy ở ưu tiên thấp hơn Chromium. Lý do: đợt 8 luồng CPU 100% làm khoảng trống giữa hai lệnh gen tăng 35 s -> 110 s |
| Video ráp cuối / hậu kỳ cùng lúc | `LUO_FFMPEG_ASM` (mặc định = (nhân + 2) / 4: 6 nhân -> 2, 16 -> 4, 32 -> 8) | `assembly_slot` quanh `concat_clips` và `post_item`; video phải chờ sẽ ghi "Chờ đến lượt ráp/hậu kỳ" vào log. `LUO_CPU_CORES` ép số nhân nếu máy đếm sai |
| Tab ấm Chromium | `MUSE2API_WARM_ALL` (mặc định 0), `MUSE2API_WARM_RECENT` (3600 s), `MUSE2API_TAB_IDLE` (1800 s) trong `.env` | từ 07/11/2026 chỉ mở sẵn tab cho tài khoản đang ghim video / đang gen / vừa dùng trong 1 giờ; tab rảnh quá 30 phút của tài khoản hết việc bị đóng (mỗi tab ~0.45 GB). Xem `/admin/status` mục `warm` |
| Việc song song trên một tài khoản | `MUSE2API_ACCOUNT_PARALLEL=` trong `userdata/api/.env` | mặc định 2; đo của tác giả gốc: 1 việc ~5 s phản hồi, 3 việc ~20 s, 10 việc 33-95 s |
| Số tài khoản | trang quản trị LUO-API (`/admin`) | yếu tố quyết định nhất; mỗi tài khoản có hạn mức video 24 giờ riêng |
| Số tiến trình Whisper | `LUO_WHISPER_WORKERS` (biến môi trường, mặc định 3) | đã sửa 07/11/2026: bể tiến trình thay một tiến trình + khoá chung; tăng lên 4 khi chạy 8 luồng trên máy ≥ 12 nhân / 32 GB |
| Số lượt mediapipe cùng lúc | `_MP_LOCK` trong `app/luo-studio/engine.py` = số nhân CPU / 2 | đã bỏ khoá chung 07/11/2026 |
| Số lần gen lại mỗi cảnh | cài đặt `check_speech`, `check_camera`, `check_overlap`, `overlap_retries`, `auto_retry` | mỗi lần gen lại ≈ +80 s cho cảnh đó; đếm bằng số lệnh video ÷ số cảnh trong một phiên (mục 3b) |

## 5. Chọn máy chủ (ước lượng, chốt lại bằng CSV của bước 3)

Máy chủ chỉ gen video **không cần GPU**: Whisper chạy CPU int8, ffmpeg libx264, Muse vẽ ở máy của Muse. Nhu cầu theo số việc song song N:

| Thành phần | Nhu cầu |
| --- | --- |
| RAM | Chromium ~300 MB/tab × N + nền Chromium ~1 GB + Studio/LUO-API ~1 GB + Whisper ~1 GB + Windows ~3 GB. N = 8 -> ~9 GB, lấy 16 GB; N = 16 -> 32 GB |
| CPU | Chromium mỗi tab ít CPU khi chờ; nặng là ffmpeg (mã hoá 1080×1920, đa luồng) và Whisper. Ước 1 nhân/2 việc song song + 2 nhân nền: N = 8 -> 6-8 vCPU; N = 16 -> 10-12 vCPU. Xung nhịp đơn nhân cao hơn tốt cho Whisper/mediapipe (bị khoá tuần tự) hơn là nhiều nhân |
| Ổ đĩa | SSD (Chromium profile, media tạm, ffmpeg ghi/đọc). Vài chục GB là đủ; media cũ nằm trong `userdata/api/data/media` cần dọn định kỳ |
| Mạng | vài Mbps là dư; quan trọng là ổn định (CDP + tải file), không cần băng thông lớn |
| Hệ điều hành | Windows (Studio đóng gói cho Windows); Linux chỉ cho LUO-API thì chạy được nhưng Studio chưa thử |

Thuê thử một máy 8 vCPU / 16 GB / SSD, chạy lại lần 3 và lần 6 của ma trận trên đó, so CSV: nếu CPU p90 < 60 % và RAM trống > 4 GB thì
máy dư, mua máy nhỏ hơn hoặc tăng N; ngược lại nâng cấp. Nếu tiền máy không đổi kết quả nhưng thêm tài khoản đổi kết quả thì tiền
nên dồn vào tài khoản.

## 6. Kết quả đo 07/11/2026: 2, 4, 8 tài khoản trên máy Ryzen 5 5500 (6 nhân) / 16 GB

Cách đo: dự án "hanh ly 15bt TEST 8 canh" (mỗi biến thể 4 cảnh phần 1 + 4 cảnh phần 2; đợt 2 đo trên kịch bản 28 cảnh, dừng ở 18 cảnh),
mỗi đợt một bộ tài khoản khác, một tài khoản một video (`MUSE2API_ACCOUNT_PARALLEL=1`), kết quả cũ dọn trước mỗi đợt. Báo cáo đầy đủ:
`userdata/logs/hieu-nang/test{2,4,8}-bao-cao.txt` + CSV máy.

| | 2 tài khoản | 4 tài khoản | 8 tài khoản |
| --- | --- | --- | --- |
| Cảnh / giờ (cả máy) | 39 | 60 | 88 |
| Cảnh / giờ / tài khoản | 19.5 | 15 | 11 |
| Cảnh phần 1 (gen ảnh + video), trung vị | 81-116 s | 118-132 s | 108-152 s |
| Cảnh phần 2 (hai lớp, có clip nghe), trung vị | 210-245 s | 190-298 s | 313-461 s |
| Muse vẽ video, trung vị | 56 s | 55 s | 52 s |
| Trống giữa hai lệnh gen trên một tài khoản, p90 | 31-43 s | 42-52 s | 83-137 s |
| CPU p90 toàn máy | 57 % | 91 % | 100 % |
| RAM trống thấp nhất | 2.3 GB | 0.99 GB | 0.46 GB |
| Chromium (tab nóng cho 14 tài khoản) | 5.4 GB | 6.9 GB | 6.3 GB |
| Lỗi | 1 (Muse không nhận lệnh, đã sửa) | 0 | 0 |

Kết luận:

- **Muse không chậm đi khi tăng tài khoản** (52-56 s mọi đợt). Mất mát khi tăng luồng nằm hoàn toàn ở máy: khoảng trống giữa hai lệnh gen
  tăng gấp 3 ở 8 luồng, CPU kín 100% mỗi khi từ 3 video trở lên cùng cắt / kiểm tra cảnh, RAM trống còn dưới 0.5 GB.
- **Máy 6 nhân / 16 GB chạy tốt 2 tài khoản, 4 là chấp nhận được (mất 23 %), 8 là quá tải (mất 45 %).** Công suất hậu kỳ của máy này
  ≈ 90 cảnh/giờ bất kể số tài khoản, tức ~15 cảnh/giờ cho mỗi nhân CPU.
- **Tài khoản đã dùng không nhanh hơn tài khoản mới**: trong đợt 8, 3 tài khoản mới (105, 106, 107) cho 108-149 s/cảnh phần 1, tài khoản dùng lại
  từ đợt 2 (ytb110) 110 s, nhóm chạm nhẹ 122-152 s; khác biệt nằm trong nhiễu.
- Mỗi cảnh cần trung bình **2.9 lệnh gen** (đợt 8: 187 lệnh / 64 cảnh): phần 2 cần clip nói + clip nghe, cộng gen lại khi clip nghe lọt tiếng.
  Một video 28 cảnh ≈ 75 lệnh gen. Con số này quyết định hạn mức 24 giờ của tài khoản.
- Một tài khoản không bị tranh CPU làm được ~19.5 cảnh/giờ ≈ **0.7 video 28 cảnh mỗi giờ ≈ 85 phút một video** (khớp số đo thực tế 75-109 phút).

## 7. Đề xuất cấu hình cho 200 video 28 cảnh / ngày

Nhu cầu: 200 × 28 = 5 600 cảnh/ngày = 233 cảnh/giờ nếu chạy 24/24, 467 cảnh/giờ nếu chỉ chạy 12 giờ.

**Tài khoản (yếu tố quyết định, hai ràng buộc):**

1. Thời gian: 233 ÷ 19.5 ≈ 12 tài khoản chạy liên tục 24/24; thực tế cần dự phòng cho lỗi, gen lại và tài khoản bị từ chối → **16-20 tài khoản**
   (24/24) hoặc **30-40 tài khoản** (12 giờ/ngày).
2. Hạn mức 24 giờ của Muse: 200 video × 75 lệnh = **15 000 lệnh gen/ngày**. Nếu mỗi tài khoản chỉ được X lệnh/ngày thì cần ≥ 15 000 / X tài khoản
   (X = 150 → 100 tài khoản; X = 500 → 30). Đã thấy một tài khoản làm 180 lệnh trong một ngày không bị chặn; con số X thật cần hỏi gói Muse đang dùng.
   Ràng buộc này nhiều khả năng lớn hơn ràng buộc thời gian.

**Máy (tính theo công suất hậu kỳ ~15 cảnh/giờ/nhân, RAM ~0.5 GB mỗi tài khoản cho tab nóng + 0.6 GB mỗi tiến trình Whisper + 4 GB nền):**

| Cấu hình một máy | Tài khoản chạy song song | Cảnh / giờ | Ghi chú |
| --- | --- | --- | --- |
| 6 nhân / 16 GB (máy hiện tại) | 2-3 | 40-55 | 4 trở lên bắt đầu mất sản lượng |
| 8 vCPU / 32 GB | 4-5 | 80-100 | |
| 16 vCPU / 32-64 GB | 10-12 | 200-230 | một máy đủ 200 video/ngày nếu chạy 24/24 |
| 32 vCPU / 64 GB | 20-24 | 400-460 | một máy đủ 200 video/ngày trong 12 giờ |

Khuyến nghị: **2 máy 16 vCPU / 32 GB, SSD, Windows, không GPU**, mỗi máy 10-12 tài khoản, chạy 24/24 → ~430 cảnh/giờ, dư ~1.8 lần so với
233 cần thiết để chịu được gen lại, Muse treo và giờ cao điểm Muse chậm. Hai máy thay vì một máy to để một máy lỗi không mất cả ngày.
Chốt lại bằng cách thuê thử một máy 16 vCPU, chạy lại đợt 8 và đợt 12 với `test-tai-khoan.py`, xem CPU p90 có dưới 80 % và "trống p90" có
dưới 50 s không.

**Việc trong code để mỗi máy chạy được nhiều tài khoản hơn (theo thứ tự lợi ích):**

1. Giới hạn số ffmpeg mã hoá cùng lúc theo số nhân (nhân / 2) và ráp video cuối chạy tối đa nhân / 4 việc một lúc, ưu tiên thấp: san bằng cơn
   CPU 100 % để Chromium / LUO-API không bị đói CPU.
2. Giảm gen lại ở phần 2 (clip nghe lọt tiếng): mỗi lần gen lại ≈ +80 s và +1 lệnh vào hạn mức.
3. Tab nóng chỉ mở cho tài khoản đang bật (tiết kiệm ~0.45 GB RAM mỗi tài khoản rảnh).
