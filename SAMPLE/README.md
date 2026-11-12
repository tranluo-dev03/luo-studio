# SAMPLE: kịch bản, biến thể và tài liệu theo thể loại video

Mỗi **thể loại video** có một **mã** (chữ thường, không dấu, nối bằng gạch ngang, ví dụ `talka-bang-tu-vung`). Mã này dùng chung cho hai chỗ:

| Chỗ | Chứa gì |
|---|---|
| `SAMPLE/<mã>/` | Nội dung: kịch bản (`KICH-BAN-*.txt`), biến thể (`BIEN-THE-*.json`), phân tích video mẫu, công cụ tạo kịch bản, ghi chú |
| `app/production/types/<mã>/` | Code riêng của thể loại (nếu có): `gen.py` (cách gen các cảnh, vd. trộn cảnh thường + ghép 2 lớp), `post.py` (hậu kỳ), cấu hình, ảnh/video. Code dùng lại được cho nhiều thể loại: `types/_chung/` |

Thể loại không có hậu kỳ riêng thì dùng hậu kỳ chung (`app/production/postprocess.py`: phụ đề, logo, end card).

## Các thể loại hiện có

| Mã | Mô tả | Hậu kỳ riêng |
|---|---|---|
| `talka-bang-tu-vung` | Robot dạy từ vựng Tây Ban Nha → Anh trước bảng chữ; bút đỏ chỉ chữ, chữ tiếng Anh hiện khi đọc; phần cuối quảng cáo app Talka | Có (`app/production/types/talka-bang-tu-vung/`) |
| `ai-tutor-ngoi-doc` | Robot ngồi đọc cặp câu (tiếng mẹ đẻ → tiếng học); bảng phía trên khung gen bằng AI, chữ + phiên âm do code điền | Có (`app/production/types/ai-tutor-ngoi-doc/`) |
| `canh-sat-nu` | Hội thoại cảnh sát nữ và tài xế | Không |
| `xe-tai` | Tài xế xe tải và gia sư AI | Không |
| `ghep-hai-lop` | Loại "Ghép 2 lớp": mỗi nhân vật gen riêng rồi ghép khung | Không (ghép trong `app/luo-studio/split.py`) |
| `san-bay-gia-su-ai` | Một dự án 2 phần: khách trả lời nhân viên hải quan (cảnh thường) → khách + robot gia sư AI gen riêng rồi ghép (ghép 2 lớp), sửa câu sai; phụ đề 2 màu + dòng dịch | Có: gen + hậu kỳ (`app/production/types/san-bay-gia-su-ai/`, dùng `types/_chung/`) |
| `canh-sat-gia-su-ai` | Hoạt hình 3D, một dự án 2 phần: cảnh sát chặn xe (3 nhân vật, 4 góc máy) → tài xế + gia sư AI ghép 2 lớp (bố cục `ghep-hai-lop`), sửa câu sai; cùng khuôn `san-bay-gia-su-ai` | Có: gen + hậu kỳ (`app/production/types/canh-sat-gia-su-ai/`, dùng `types/_chung/`) |
| `soi-hanh-ly-gia-su-ai` | Một dự án 2 phần: nhân viên an ninh hỏi người mẹ địu con ở máy soi hành lý (cảnh thường, đổi góc máy + một cú lia máy) → người mẹ quay selfie + robot gia sư AI ghép 2 lớp, sửa câu sai "I have 48"; cùng khuôn `san-bay-gia-su-ai` | Có: gen + hậu kỳ (`app/production/types/soi-hanh-ly-gia-su-ai/`, dùng `types/_chung/`) |
| `quet-an-ninh-day-chuyen` | Nhân bản từ `soi-hanh-ly-gia-su-ai` (10/11/2026): quét an ninh cơ thể, cổng dò kim loại báo động vì hành khách nữ CHƯA THÁO DÂY CHUYỀN (13 cảnh, 3 góc máy, cú lia vụt ở cảnh 1; dây chuyền đeo → tự tháo ở cảnh 5 → cất vào túi cảnh 6) → hành khách selfie + robot gia sư AI ghép 2 lớp, sửa "I have 48"; không vali, không em bé; kèm 4 ảnh tham chiếu (nền cổng, robot, hành khách, nhân viên) | Có: gen + hậu kỳ (`app/production/types/quet-an-ninh-day-chuyen/`, dùng `types/_chung/`) |
| `chia-doi-gia-su-ai` | Một phần ghép 2 lớp, màn hình chia đôi dọc: robot gia sư AI nửa trái, người dùng ngồi bàn cà phê nửa phải; sửa câu sai "I have 28"; phụ đề ô đen, viền sai/đúng chỉ ở nửa người dùng | Có: hậu kỳ (`app/production/types/chia-doi-gia-su-ai/`, dùng `types/_chung/`); gen dùng thẳng chế độ ghép 2 lớp |
| `chia-tren-duoi-marathi` | Một phần ghép 2 lớp theo video "oder 3", khung chia trên/dưới: robot gia sư AI ô trên, người học ô dưới; tiếng Marathi xen tiếng Anh, phụ đề chữ đen ô trắng font Nirmala UI; quảng cáo Supernova AI | Có: hậu kỳ (`app/production/types/chia-tren-duoi-marathi/`, dùng `types/_chung/`); gen dùng thẳng chế độ ghép 2 lớp |
| `chia-tren-duoi-bengali` | Một dự án 2 phần theo video "oder 5", tiếng Bengali xen tiếng Anh: Nova và chàng trai đứng đối mặt nhìn nghiêng (cảnh thường, 4 cảnh) → chia trên/dưới, Nova ô trên, người học ô dưới (ghép 2 lớp, 16 cảnh); phụ đề chữ đen ô trắng; quảng cáo Supernova AI | Có: gen + hậu kỳ (`app/production/types/chia-tren-duoi-bengali/`, dùng `types/_chung/`) |
| `du-lich-chia-doi-gia-su-ai` | Một dự án 2 phần, tiếng Tây Ban Nha xen tiếng Anh: Carla và robot ở Machu Picchu (cảnh thường, 3 cảnh) → gọi video chia đôi dọc với robot gia sư AI (ghép 2 lớp, khuôn `chia-doi-gia-su-ai`), sửa "I have 22" / "I'm Mexico" | Có: gen + hậu kỳ (`app/production/types/du-lich-chia-doi-gia-su-ai/`, dùng `types/_chung/`) |
| `xe-tai-canh-sat-gia-su-ai` | Người thật, một dự án 2 phần: cảnh sát chặn nữ tài xế xe tải (cảnh thường, 2 nhân vật, một góc máy, đưa giấy tờ) → tài xế selfie + gia sư AI hoạt hình 3D trong ô viền trắng phía trên (ghép 2 lớp), sửa câu sai; khuôn `canh-sat-gia-su-ai` | Có: gen + hậu kỳ (`app/production/types/xe-tai-canh-sat-gia-su-ai/`, dùng `types/_chung/`) |
| `di-tru-gia-su-ai` | Một dự án 3 phần, tiếng Tây Ban Nha xen tiếng Anh: cuộc gọi báo có agentes de inmigración (cắt xen 2 nơi, mỗi cảnh một người) → cảnh sát hỏi, robot nhỏ trên vai sửa "I am Mexico" (cảnh thường, 3 khung) → người học + gia sư AI ô dọc góc trên phải (ghép 2 lớp) | Có: gen + hậu kỳ (`app/production/types/di-tru-gia-su-ai/`, dùng `types/_chung/`) |
| `robot-pho-tieng-long` | Một phần, một nhân vật: robot đội mũ cao bồi đứng giữa phố Texas nói thẳng ống kính, dạy 4 từ lóng (nhân dịp F1); hậu kỳ vẽ tiêu đề, badge sự kiện, thẻ "TEXANS SAY / IT MEANS" hiện theo lời, phụ đề karaoke từ đang nói đổi màu; biến thể đổi vùng (Sydney, London) | Có: hậu kỳ (`app/production/types/robot-pho-tieng-long/`) |
| `check-hanh-ly-hindi` | Nhân bản từ `soi-hanh-ly-gia-su-ai` theo video "oder 6": nhân viên an ninh Ấn Độ + phụ nữ Gujarati mặc sari ở máy soi (MỘT góc máy khoá, 17 cảnh) → người phụ nữ + robot gia sư AI ghép 2 lớp, sửa "I have 62"; lời Gujarati xen tiếng Anh, phụ đề chữ đen ô trắng font Nirmala UI | Có: gen + hậu kỳ (`app/production/types/check-hanh-ly-hindi/`, dùng `types/_chung/`) |
| `di-tru-aiva-ai` | Nhân bản `di-tru-gia-su-ai` theo CSV "oder 7" (app Aiva AI): bố/con trai gọi báo agentes de inmigración → cảnh sát hỏi (một góc, không robot) → hành khách + gia sư AI ô góc phải (ghép 2 lớp); 20 biến thể hành khách nam/nữ, trẻ/già | Có: gen + hậu kỳ (`app/production/types/di-tru-aiva-ai/`, dùng `types/_chung/`) |
| `tiem-thit-tieng-anh` | Hoạt hình 3D kể chuyện theo video "0610_Cut meat ES" (177 s): cậu bé phụ việc tiệm thịt bị chê không biết tiếng Anh, giúp bà chủ nhà hàng, học mỗi đêm với robot gia sư AI trên điện thoại, một tháng sau được nhận việc; MỘT phần cảnh thường, 37 cảnh, 15 góc máy, 5 nhân vật; tiếng Tây Ban Nha xen tiếng Anh, dòng dịch dưới câu tiếng Anh | Có: hậu kỳ (`app/production/types/tiem-thit-tieng-anh/`, dùng `types/_chung/`); gen dùng chế độ cảnh thường |
| `phong-van-pho-malayalam` | Một dự án 2 phần theo video "1510_interview street hindi_005" (76,9 s, app Aiva AI), tiếng **Malayalam** xen tiếng Anh: phóng viên quay lưng (qua vai) đố từ tiếng Anh người phụ nữ bán hàng rong đeo găng sau xe đẩy inox (cảnh thường, MỘT góc, 11 cảnh) → robot gia sư AI (robot Talka) ô trên, người bán selfie ô dưới (ghép 2 lớp, 15 cảnh), sửa "I am Kannur"; phụ đề chữ đen ô trắng giữa khung, Nirmala UI | Có: gen + hậu kỳ (`app/production/types/phong-van-pho-malayalam/`, dùng `types/_chung/`) |
| `phong-van-pho-tay-ban-nha` | Cùng khuôn video "1510_interview street hindi_005" như phong-van-pho-malayalam nhưng lời **tiếng Tây Ban Nha (Mexico)**: phóng viên quay lưng (qua vai) hỏi người bán hàng rong (cảnh thường, MỘT góc, 6 cảnh) → robot Aiva ô trên, người bán selfie ô dưới (ghép 2 lớp, 6 cảnh); 20 biến thể (người bán + phóng viên KHÁC GIỚI + bối cảnh theo ảnh Drive); phụ đề chữ đen ô trắng, Arial | Có: gen + hậu kỳ (`app/production/types/phong-van-pho-tay-ban-nha/`, dùng `types/_chung/`) |
| `taxi-gia-su-ai` | Hoạt hình 3D kể chuyện theo video "0510_cartoon turn car_015_1" (95 s), tiếng Anh + Tây Ban Nha: tài xế taxi Mexico không hiểu khách, bị đánh giá tệ, mất xe mới vào tay Arjun, con gái chỉ app gia sư AI (cảnh thường, 25 cảnh gồm **5 cảnh không lời**, 11 góc máy, 5 nhân vật) → tài xế + robot gia sư AI ô ngang phía trên (ghép 2 lớp, 18 cảnh), sửa "I am Mexico"; cảnh không lời trong dự án nhiều phần bằng MARKER `[KHONG LOI]` (gen.py đổi thành rỗng) | Có: gen + hậu kỳ (`app/production/types/taxi-gia-su-ai/`, dùng `types/_chung/`) |
| `lam-vuon` | Biến thể mẫu chủ đề làm vườn (dùng kịch bản mẫu chung) | Không |

`_chung/`: file dùng cho mọi thể loại (kịch bản/biến thể mẫu gia sư AI, prompt nhờ Claude viết kịch bản, hướng dẫn cho agent, công cụ `phan-tich-video.py`).

## Cấu trúc một thư mục thể loại

```
SAMPLE/<mã>/
  README.md                 tổng hợp: quy trình gen, cách dùng, các quyết định đã chốt và lý do
  KICH-BAN-*.txt            kịch bản đang dùng (nhập ở tab "Loại dự án" > "Loại mới")
  BIEN-THE-*.json           biến thể đang dùng (nhập khi tạo dự án / "Từ file")
  PHAN-TICH-VIDEO-MAU.md    phân tích video tham chiếu (nếu có)
  cong-cu/                  script tạo lại kịch bản/biến thể (nếu có)
  phien-ban-cu/             bản cũ, giữ để tham khảo
```

## Thêm thể loại mới (video tham chiếu mới)

Chỉ cần đưa video cho Claude trong thư mục dự án này: skill `luo-video-moi` (`.claude/skills/luo-video-moi/SKILL.md`) chạy trọn quy trình.
Tri thức nền và bảng chọn khuôn: **`_chung/SO-TAY-KY-THUAT.md`** (tổng hợp mọi kỹ thuật đã kiểm chứng qua các thể loại ở trên). Công cụ: `_chung/video-moi.py`.

1. `runtime\python.exe SAMPLE\_chung\video-moi.py danh-gia "<video>"`: bóc lời, nhịp, cảnh cắt, số mặt, chuyển động máy, cao độ giọng; gợi ý khuôn. Xem từng ảnh `luot_NN.jpg`, điền bảng hành động.
2. Chọn khuôn theo bảng mục 2 của sổ tay; sao mẫu gần nhất trong `SAMPLE/<mẫu>/`; viết `SAMPLE/<mã>/` (phân tích, kịch bản, biến thể, README, PROMPT-CHO-AGENT). Cần gen/hậu kỳ riêng: `app/production/types/<mã>/` (xem `app/production/types/README.md`), khai `[HAU KY] loai: <mã>` trong kịch bản.
3. `video-moi.py kiem-tra <kịch bản> <biến thể> --tai-anh`: kiểm bằng code Studio.
4. `video-moi.py nhap <kịch bản> <biến thể> --ten-loai ... --ten-du-an ... --chay-thu`: tạo loại dự án + dự án trong Studio đang chạy và chạy thử biến thể đầu.
5. Ghi lại trong `SAMPLE/<mã>/README.md` những gì đã thử và kết quả; kỹ thuật/lỗi mới thì bổ sung vào sổ tay.
