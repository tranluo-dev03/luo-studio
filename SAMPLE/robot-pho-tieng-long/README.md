# Thể loại: robot đứng phố dạy tiếng lóng (`robot-pho-tieng-long`)

Video mẫu: robot nữ đội mũ cao bồi, khoác sơ mi denim, đứng giữa phố cổ Texas, nhìn thẳng ống kính dạy 4 từ lóng Texas ("Howdy", "Y'all", "Fixin' to", "Bless your heart") nhân dịp F1 đến Texas, rồi hỏi người xem bình luận. Một khung máy đứng yên 25 s, mọi chữ là lớp hậu kỳ. Phân tích: `PHAN-TICH-VIDEO-MAU.md`.

## Khuôn đã chọn
**Một phần, cảnh thường, một nhân vật, 6 cảnh nối liên tục** (khung đầu từ `Prompt ảnh` cảnh 1, các cảnh sau nối từ khung cuối) + **hậu kỳ riêng vẽ chữ bằng code** (`app/production/types/robot-pho-tieng-long/post.py`). Gần nhất với `talka-bang-tu-vung` (robot nói + chữ do code dựng) nhưng nền phố thật do Muse gen, không cần phông xanh vì mọi lớp chữ là ô đặc đè lên.

| Cảnh | Lượt | Nội dung |
|---|---|---|
| 1 | 1 | Mở đầu (khung đầu mới) |
| 2–4 | 2–4 | "Từ. That means nghĩa." (thẻ hiện khi nói từ, nghĩa hiện khi nói nghĩa) |
| 5 | 5 | Từ dài có giải thích |
| 6 | 6 | Câu hỏi kêu gọi bình luận |

## File
| File | Dùng để |
|---|---|
| `KICH-BAN-ROBOT-PHO-TIENG-LONG.txt` | Kịch bản 6 cảnh, token `TEN/NGUOI/GIONG/POS/VAI/BOX_DAY`, `TRANG_PHUC`, `NEN_PHO`, `DAO_NGHI`; khối `[HAU KY] loai: robot-pho-tieng-long` |
| `BIEN-THE-ROBOT-PHO-TIENG-LONG.json` | 3 biến thể: `texan-f1-austin` (bám video mẫu), `aussie-sydney`, `brit-london`. Sinh bằng `cong-cu/tao_bien_the.py` (không sửa tay) |
| `cong-cu/tao_bien_the.py` | Bảng (vùng, trang phục, nền, tiêu đề, badge, nhãn thẻ, 6 lượt, 4 thẻ) → JSON |
| `BIEN-THE-30-GIAI-DO.json` | **30 biến thể "Giải đố"** từ CSV của người dùng (08/11/2026): 11 California, 8 Texas, 3 Arizona, 3 Illinois, 2 Florida, New Mexico, Colorado, Nevada; mỗi biến thể 4 từ lóng + ảnh robot (`refs.NGUOI_DAY`) + ảnh nền (`refs.NEN_PHO`) |
| `cong-cu/tao_30_bien_the.py` + `cong-cu/_csv30.json` | Sinh file 30 biến thể: bang + dân bang đọc từ cột "Kiểu biến thể", 4 từ lóng từ cột 3, trang phục/nền tả theo ảnh (bảng `TRANG_PHUC`, `NEN_PHO` trong script) |
| `anh/bt/btNN-nv.webp`, `btNN-bg.webp` | 60 ảnh tải từ link Google Drive trong CSV (robot nền xanh lá + nền địa danh), dùng làm `refs` |
| `anh/khung-mau*.png` | Khung video mẫu để so bố cục (KHÔNG gửi cho Muse) |
| `PROMPT-CHO-AGENT.txt` | Quy tắc khi viết biến thể mới |
| Hậu kỳ | `app/production/types/robot-pho-tieng-long/` (post.py, config.json, README.md) |

## Cách chạy
```
runtime\python.exe SAMPLE\robot-pho-tieng-long\cong-cu\tao_bien_the.py
runtime\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\robot-pho-tieng-long\KICH-BAN-ROBOT-PHO-TIENG-LONG.txt SAMPLE\robot-pho-tieng-long\BIEN-THE-ROBOT-PHO-TIENG-LONG.json
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\robot-pho-tieng-long\KICH-BAN-ROBOT-PHO-TIENG-LONG.txt SAMPLE\robot-pho-tieng-long\BIEN-THE-ROBOT-PHO-TIENG-LONG.json --ten-loai "Robot phố tiếng lóng" --ten-du-an "Tiếng lóng Texas F1" --chay-thu
```
Trong trang dự án chọn Thương hiệu: logo cố định trên trái (badge "Talka AI" của video mẫu); không cần intro/outro.

## Quyết định đã chốt (08/11/2026)
- Gộp 12 câu thành 6 lượt (mỗi cảnh một lượt ~5 s): ít cảnh nối hơn, ít trôi mặt/trang phục; thẻ và nghĩa vẫn đúng lúc vì căn theo **từ** Whisper trong cảnh chứ không theo mốc cảnh.
- Không dùng `refs` ảnh nhân vật: chỉ một khung đầu mới (cảnh 1), các cảnh sau nối từ khung cuối. Người dùng muốn robot giống hệt một ảnh AI có sẵn thì thêm `"refs": {"NGUOI_DAY": ["<link>"]}` vào biến thể.
- Robot: môi tả "open and move naturally with every word" (không "sculpted/closed lips", xem sổ tay mục 6); tay buông dọc thân, cấm giơ tay (video mẫu tay gần như không cử động, và tay giơ lên sẽ bị thẻ che).
- `TRANG_PHUC` tách khỏi `NGUOI_DAY` để đổi mũ/áo theo vùng mà giữ nguyên robot.
- Phụ đề karaoke tự chia cụm (cắt ở dấu câu, tối đa 3 từ, không để cụm 1 từ lẻ); video mẫu chia tay từng cụm 2–4 từ. Chấp nhận khác nhẹ.
- Tốc độ nói ghi "about 4 words per second" theo số đo; Muse chậm hơn thì nâng "Tốc độ tăng tối đa".

## Dự án "Giải đố 30 biến thể" (Studio: `Giai-do-30-bien-the-4737`)
- Ảnh robot người dùng cung cấp đứng trên nền xanh lá, mặt sứ trắng (khác robot mặt người của biến thể Texas đầu): kịch bản dặn "copy that robot's face, head and outfit exactly; its plain green backdrop is NOT part of the scene".
- Ảnh nền có nhiều biển hiệu chữ (Hollywood, taquería, Pilsen...): kịch bản dặn nền mờ, chữ không đọc được; vẫn có rủi ro Muse vẽ chữ → xem `scene1_start.png` trước khi chạy cả nhóm.
- Giữ badge "OCT 23-25 / US GRAND PRIX" như video mẫu cho mọi bang (người dùng chỉ yêu cầu đổi câu thoại, nhân vật, nền, từ vựng). Dòng 12–19 (CSV không đổi lời) giữ Texas.
- Robot đeo kính râm (bt01, bt03, bt26): dò mặt để đặt tiêu đề có thể trượt → tiêu đề dùng toạ độ mặc định; kiểm tra khung.

## 60 biến thể mới (11/11/2026): đổi bài học / Ấn Độ / Brazil
Yêu cầu người dùng: 20 biến thể đổi bài học, 20 biến thể đổi nhân vật + bối cảnh tiếng Ấn Độ, 20 biến thể đổi nhân vật + bối cảnh tiếng Bồ Đào Nha; ảnh nhân vật và bối cảnh nhờ Muse gen trước, tổng hợp để duyệt.

| File | Nội dung |
|---|---|
| `BIEN-THE-20-BAI-HOC.json` | `bh01`–`bh20`: robot Aiva AI (trang phục sơ mi denim) + phố Texas + badge F1 giữ nguyên, mỗi biến thể một chủ đề 4 cụm tiếng lóng Mỹ (đồ ăn, tiền, công việc...). Chung 2 ảnh `anh/bh/` |
| `BIEN-THE-20-AN-DO.json` | `in01`–`in20`: 20 thành phố Ấn Độ, robot **Aiva AI** (ảnh người dùng gửi, `anh/aiva/aiva-robot.webp`) giữ nguyên, chỉ đổi trang phục, **mặc trọn bộ như người** (áo kín tay dài + quần/váy/sari quấn đủ, chỉ lộ đầu, cổ, bàn tay robot; không mũ vì tai nghe Aiva; giọng nữ/nam xen kẽ). Bảng `FULL_IN`, `FULL_BR` trong `tao_60_bien_the.py`; ảnh robot bản cũ ở `anh/_robot-cu/`, nói **Hindi chữ Devanagari**, cụm tiếng lóng giữ tiếng Anh. Thẻ: nghĩa Hinglish chữ Latin (PIL không có raqm, không vẽ được Devanagari); phụ đề Devanagari (ASS, Nirmala UI, shaping complex) |
| `BIEN-THE-20-BRAZIL.json` | `br01`–`br20`: 20 địa danh Brazil, robot **Aiva AI** giữ nguyên, chỉ đổi trang phục, nói **tiếng Bồ Đào Nha Brazil**; `br06` Interlagos mở đầu bằng F1 |
| `cong-cu/tao_60_bien_the.py` | Sinh 3 file trên. 20 bộ bài học `BAI` dùng chung cho cả 3 nhóm (bộ k cho biến thể k), nghĩa viết sẵn EN / Hindi / Hinglish / PT |
| `cong-cu/gen_anh_60.py` | Muse gen ảnh robot (nền xanh lá) + ảnh nền (cảnh trống) theo đúng mô tả trong biến thể → `anh/bh`, `anh/in`, `anh/br` (.webp). Bỏ qua ảnh đã có; `in03-nv --lai` để gen lại một ảnh |
| `cong-cu/tao_trang_duyet.py` | Trang duyệt `DUYET-60-BIEN-THE.html`: ảnh + 6 lời + 4 thẻ của từng biến thể; bấm ảnh đánh dấu gen lại, nút chép lệnh gen lại |

Hậu kỳ (`post.py`, chỉ thể loại này): `HAU_KY.ngon_ngu` (`en`/`hi`/`pt`) chọn Whisper (`small.en` hoặc `small` + mã ngôn ngữ), `HAU_KY.font_ass` + `shaping` cho phụ đề Devanagari, so khớp từ theo Unicode (trước chỉ a-z0-9), dấu `।` ngắt cụm phụ đề. Biến thể cũ (không có khoá) chạy như trước. Đã chạy thử offline trên video giả: chữ Devanagari và chữ có dấu hiện đúng.

Rủi ro chưa xử lý (code chung `engine.py`, chưa sửa):
- Câu Hindi kiểu "Chill out! इसका मतलब है, आराम करो।": `voice_span` chỉ khớp được từ tiếng Anh ở đầu câu và coi câu đã trọn → **có thể cắt mất phần nghĩa Hindi** khi cắt sát.
- Câu Bồ Đào Nha: `speech_lang` không có `pt` (câu có á/é/í/ó/ú bị coi là Tây Ban Nha, câu khác là tiếng Anh) → kiểm lời có thể báo thừa/thiếu sai và gen lại vô ích.
- Chưa chạy trên Muse cả 3 nhóm.

## Còn khác video mẫu
- Badge "Talka AI" phải chọn ở Thương hiệu.
- Ô tiêu đề là chuyển sắc xanh phẳng (mẫu có bóng nhẹ hơn); thẻ không có hoạt ảnh trượt vào.

## Lần thử
Xem `SAMPLE/_chung/NHAT-KY-TRI-THUC.md` (mục `robot-pho-tieng-long`).
