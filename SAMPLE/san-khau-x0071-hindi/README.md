# X0071 Hindi — "Nice to meet you" / "Me too" (mã `san-khau-x0071-hindi`)

Video tham chiếu: `324369fe-X0071-Split-screen-HINDI_003-5.mp4` (75 s, 1080×1920, Hindi xen tiếng Anh, app **Talka AI**).
**Đây chính là video đã dùng để tạo `SAMPLE/san-khau-chia-doi-gia-su-ai/BIEN-THE-X0057-X0071-HINDI-20.json`** (20 biến thể Hindi) trước đây. Thư mục này KHÔNG tạo thể loại/code mới — chỉ đóng gói lại đúng MỘT biến thể mẫu theo yêu cầu "hai dạng kịch bản" (goc / đổi hook) + `CAU-TRUC.json`, dùng chung code `app/production/types/san-khau-chia-doi-gia-su-ai/`.

| Đoạn video gốc | Giây | Studio |
|---|---|---|
| Hook (sân khấu, "đừng đáp Me too") | 0:00–0:05 | Phần 1, cảnh 1 |
| Nỗi đau (tiệc, 3 câu gạch đỏ) + thú nhận | 0:05–0:11 | Phần 1, cảnh 2–3 |
| Giải pháp (Talka AI, 3 tuần, miễn phí, giơ điện thoại) | 0:11–0:23,6 | Phần 1, cảnh 4–6 |
| Demo 5 câu (chia đôi dọc, robot trái / diễn giả phải, thẻ nghĩa Hindi + phiên âm) | 0:23,6–0:59,7 | Phần 2, ghép 2 lớp, 10 lượt |
| Robot avatar + cài app + end card | 0:59,7–1:15 | **Không gen** → Thương hiệu dự án |

## File
| File | Nội dung |
|---|---|
| `PHAN-TICH-VIDEO-MAU.md` | Tổng quan, bảng hành động, bảng "video gốc → kịch bản", Insight người dùng (nguyên văn), đối chiếu cấu trúc hook/tình huống |
| `CAU-TRUC.json` | `hook` / `tinh_huong` / `quang_cao` / `hook_moi` theo mốc giây thật của video |
| `KICH-BAN-SAN-KHAU-X0071-HINDI.txt` + `BIEN-THE-SAN-KHAU-X0071-HINDI.json` | Kịch bản **A (goc)**: bám sát video gốc, 1 biến thể mẫu |
| `KICH-BAN-SAN-KHAU-X0071-HINDI-HOOK.txt` + `BIEN-THE-SAN-KHAU-X0071-HINDI-HOOK.json` | Kịch bản **B (đổi hook)**: giữ nguyên tình huống (nỗi đau tiệc + giải pháp + demo 5 câu), chỉ đổi lời cảnh 1 |

Code dùng chung: `app/production/types/san-khau-chia-doi-gia-su-ai/` (`gen.py`, `post.py`, `config.json`) — KHÔNG sửa, vì `post.py` đã tự chuyển font Nirmala UI + `shaping: complex` khi biến thể có `HAU_KY.ngon_ngu == "hi"`.

## Quyết định đã chốt (chạy ngầm, không hỏi lại)
- **Mã**: dùng mã riêng `san-khau-x0071-hindi` thay vì ghi đè vào thư mục `san-khau-chia-doi-gia-su-ai/` sẵn có, vì tên file bắt buộc của việc này (`KICH-BAN-<MÃ>.txt`, `BIEN-THE-<MÃ>.json`...) trùng tên với file GỐC (bản 7 cảnh tiếng Bồ dùng cho Brazil/Mexico) đang được các batch khác dùng — đổi mã để không đụng file đang dùng chung.
- **Ảnh `refs`**: KHÔNG chọn trong kho nhân vật chung và KHÔNG gen mới. Tái dùng ảnh AI đã có sẵn, đã vetted riêng cho đúng video X0071 này: `SAMPLE/san-khau-chia-doi-gia-su-ai/anh/hindi/bien-the-01.webp` (diễn giả nam ~29 tuổi) và `SAMPLE/san-khau-chia-doi-gia-su-ai/anh/ai-robot-mu-kinh.png` (robot Talka AI, mũ + kính đen). Lý do: ảnh này KHÔNG cắt từ video mẫu (là ảnh AI tải từ Drive theo CSV của một phiên trước), và đã từng được dùng cho đúng kịch bản 6 cảnh Hindi này — bám sát video gốc hơn là chọn ngẫu nhiên trong kho nhân vật chung.
- **Sửa lỗi template khi sao chép kịch bản**: 4 mốc "Diễn biến" của bản `-6CANH` gốc neo vào từ tiếng Bồ ("Nunca, jamais"/"assim"/"praticar"/"fluência e confiança") — trường này được gửi thẳng cho Muse (`gen_video.py`: "Timed action beats"), với câu Hindi các từ đó không tồn tại nên cử chỉ sẽ lệch nhịp. Đã sửa thành mốc theo vị trí câu (đầu câu/giữa câu/nửa sau câu), không phụ thuộc ngôn ngữ. **Chưa sửa vào file gốc** `san-khau-chia-doi-gia-su-ai/KICH-BAN-SAN-KHAU-CHIA-DOI-GIA-SU-AI-6CANH.txt` (ngoài phạm vi mã này; Mexico cũng dùng file đó nên cũng dính lỗi tương tự — nên sửa chung một lần sau).
- **Lượt "gạch" 3 câu sai** (Me too / You're welcome / I'm fine, thanks) không có cặp `fx: wrong → right` đi kèm ngay sau, vì video gốc không sửa ngay (đợi tới demo phần 2 mới dạy câu đúng, mà câu đúng không phải là bản dịch trực tiếp của 3 câu sai). Giữ đúng video: dùng `"gach": true` (cơ chế khác hẳn `fx`), không phải cảnh báo của `kiem-tra`.
- **Hook mới (kịch bản B)**: lấy tình huống 3 trong 10 tình huống của Insight (họp online, không nghe kịp, chỉ gật "yes, yes") — không bịa tình huống ngoài insight. Giữ cấu trúc câu và độ dài như hook gốc; tình huống (nỗi đau tiệc + giải pháp + demo 5 câu) giữ nguyên 100% giữa A và B.
- **Đơn giản hoá cho phép** (đã có sẵn ở kịch bản `-6CANH` gốc, giữ nguyên): phần demo giữ MỘT vẻ ngoài của diễn giả xuyên suốt (video gốc có đoạn xen thêm một vẻ ngoài kính râm/mũ ngoài trời ở vài khung demo, bỏ qua theo mục 2.2 sổ tay kỹ thuật).

## Rủi ro / cần xác nhận khi xem video gen thật
- `post.py` neo từ "ingles" (không dấu) để tìm chỗ robot bắt đầu nói tiếng Anh trong lượt; với câu Hindi (chữ "इंग्लिश") neo này không khớp, code tự rơi về tìm từ đầu lượt — cần xem `card*.png` khi gen thật để chắc chắn ô vàng tô đúng từ, đúng lần ("mời lặp" chứ không phải lần robot tự đọc trước).
- Whisper nghe phần demo (giây 25–45) rất lẫn (xem `bao-cao.md` gốc trong `_uploads/.../phan-tich/`); nội dung 5 câu/thẻ lấy nguyên từ bản đã nghe kỹ trước đó (`BIEN-THE-X0057-X0071-HINDI-20.json`), chưa nghe lại từ đầu trong lượt này.
- Robot/diễn giả hai nửa khác giới (nam/robot) nên không có rủi ro nhép sai theo mục 3.2 sổ tay.

## Nhật ký
- 19/11/2026: phân tích bằng công cụ (`video-moi.py danh-gia --lang hi`), xem `tong-quan_1..4.jpg`, xác nhận khớp đúng là video gốc của X0057/X0071. Viết `PHAN-TICH-VIDEO-MAU.md`, `CAU-TRUC.json`, 2 cặp kịch bản/biến thể. `kiem-tra --tai-anh` cả hai: **0 lỗi, 0 cảnh báo**.
- 19/11/2026: `nhap --chay-thu` kịch bản A → loại `San-khau-the-tu-vung-chia-doi-gia-su-AI-X0071-Hindi-9512`, dự án `X0071-Hindi-Nice-to-meet-you-9ea9`, biến thể `bien-the-01-goc-nam-29` đang chạy thử.
- 19/11/2026: `nhap` (không `--chay-thu`) kịch bản B → loại `San-khau-the-tu-vung-chia-doi-gia-su-AI-X0071-Hindi-doi-hook-d0f8`, dự án `X0071-Hindi-Nice-to-meet-you-doi-hook-7ed7`, biến thể `bien-the-01-hook-nam-29` (chưa chạy, người dùng tự bấm).
