# Hậu kỳ riêng: robot đứng phố dạy tiếng lóng (`robot-pho-tieng-long`)

Kịch bản, biến thể, phân tích: `SAMPLE/robot-pho-tieng-long/`. Không có `gen.py` (một phần, cảnh thường, Studio tự gen). Studio chạy hậu kỳ này khi kịch bản có `[HAU KY] loai: robot-pho-tieng-long`.

Video Muse chỉ có robot nói trước nền phố. `post.py` vẽ mọi chữ bằng code (PIL + ffmpeg + ASS), lấy nội dung từ khoá `HAU_KY` của biến thể:

| Lớp | Nội dung | Thời điểm |
|---|---|---|
| Tiêu đề | ô xanh bo góc 2 dòng phía trên đầu robot (dòng 1 trắng, dòng 2 xanh nhạt) – `HAU_KY.tieu_de` | suốt video |
| Badge | ô cam (`badge.trai`) + ô trắng (`badge.phai`) bên trái, ngay trên thẻ | suốt video (bỏ qua nếu thiếu) |
| Thẻ từ lóng | đầu xanh: nhãn `nhan_tu` + từ `tu` + đếm n/N; thân trắng: nhãn `nhan_nghia` + `nghia` (trước khi robot nói nghĩa: "...") – `HAU_KY.the[]` | thẻ hiện khi robot nói `moc_tu` (mặc định từ đầu của `tu`), nghĩa hiện khi robot nói `moc_nghia`; giữ tới thẻ sau; thẻ cuối giữ tới hết |
| Phụ đề karaoke | cụm 2–4 từ trên ô xanh bo góc, từ đang nói đổi sang xanh nhạt | mốc từng từ: Whisper theo từng cảnh (`postprocess.transcribe` với `jobs`), khớp mờ với lời biến thể; từ không nghe thấy nội suy |

Không logo, không end card (Thương hiệu của dự án gắn sau). Bố cục, màu, cỡ chữ: `config.json` (đo từ video mẫu 720×1280, nhân 1,5).

Chạy tay: `runtime\python.exe app\production\types\robot-pho-tieng-long\post.py <run>\raw.mp4 --scenes <run>\scenes.json --out <run>\final.mp4 --variant <run>\variant.json`
