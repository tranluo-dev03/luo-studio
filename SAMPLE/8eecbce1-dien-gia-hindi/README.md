# 8eecbce1 — Diễn giả sân khấu Hindi "Nice to meet you / Me too" (mã `8eecbce1-dien-gia-hindi`)

Video tham chiếu: `userdata/studio/claude/_uploads/8eecbce1-Speaker-HINDI-sample.mp4` (25,6 s, 1440×2560, Hindi xen Anh, app **Talka AI**).
Video chỉ có phần sân khấu (hook → tiệc → thú nhận → giải pháp → giơ điện thoại). Demo 5 câu và CTA do người dùng chỉ định trong cấu trúc hook/tình huống nhưng **không có trong video** → demo làm theo khuôn chia đôi đã kiểm chứng (phần 2), CTA = Thương hiệu.

| Phần | Cảnh/lượt | Chế độ | Video gốc |
|---|---|---|---|
| Phần 1 | cảnh 1 (HOOK) | cảnh thường, Prompt ảnh sân khấu | 0:00–0:05 |
| | cảnh 2 (tiệc, 3 câu gạch đỏ) | Prompt ảnh mới, khung trung | 0:05–0:10 |
| | cảnh 3–6 (thú nhận, giải pháp, giơ điện thoại) | cảnh 3 `Khung đầu từ cảnh: 1`, sau đó nối khung | 0:10–0:25,6 |
| Phần 2 | 10 lượt (5 vòng robot đọc mẫu → diễn giả lặp) | ghép 2 lớp chia đôi dọc, `noi: cat`, vào bằng nhoè 0,5 s | không có trong video |
| CTA | — | KHÔNG gen → Thương hiệu (logo "Talka AI" góc trên trái, Outro Google Play) | không có trong video |

## File
| File | Nội dung |
|---|---|
| `PHAN-TICH-VIDEO-MAU.md` | Tổng quan, lời đối chiếu phụ đề, bảng hành động, bảng "video gốc → kịch bản", Insight (nguyên văn), cấu trúc hook/tình huống |
| `CAU-TRUC.json` | hook / tinh_huong / quang_cao / hook_moi |
| `KICH-BAN-8EECBCE1-DIEN-GIA-HINDI.txt` + `BIEN-THE-8EECBCE1-DIEN-GIA-HINDI.json` | Kịch bản **A (goc)**: bám video gốc; biến thể sau ĐỔI NHÂN VẬT (mọi thứ của nhân vật/bối cảnh là token: NGUOI_, GIONG_, DAO_, NEN_, HE/HIS/HIM…) |
| `KICH-BAN-8EECBCE1-DIEN-GIA-HINDI-HOOK.txt` + `BIEN-THE-8EECBCE1-DIEN-GIA-HINDI-HOOK.json` | Kịch bản **B (đổi hook)**: cảnh 1 dùng token `LUOT_1`, `HOOK_HANH_DONG`, `HOOK_DIEN_BIEN`, `HOOK_CAM_XUC`, `HOOK_KHUNG_CUOI`; cảnh 2 trở đi y như A |
| `cong-cu/tao_bien_the.py` | Sinh cả hai file biến thể từ bảng `NHAN_VAT` (A) và `HOOKS` (B); tự đổi đại từ và đuôi động từ Hindi theo giới (देता था/देती थी, लगा/लगी) |

Code: dùng chung `app/production/types/san-khau-chia-doi-gia-su-ai/` (không sửa). Hindi: post.py tự dùng Nirmala UI + shaping complex.

## Quyết định đã chốt (chạy ngầm, không hỏi lại)
- **Không tạo code thể loại mới**: video thuộc đúng khuôn `san-khau-chia-doi-gia-su-ai` (bản 6 cảnh Hindi). Kịch bản sao từ `SAMPLE/san-khau-x0071-hindi/` (đã gen thử cảnh 1 đạt 19/11) rồi sửa theo video này.
- **Giữ demo phần 2 dù video không có**: người dùng chỉ định demo 5 câu trong cấu trúc → theo người dùng (quy tắc: lệch thì vẫn theo người dùng, ghi lại). Phương án an toàn: ghép 2 lớp (hai nhân vật không bao giờ chung khung).
- **Ảnh refs từ kho nhân vật**: diễn giả `NAM-30-45-IND-04` (nam India mảnh, tóc đen điểm bạc, râu muối tiêu — gần nhất với diễn giả ~50 tuổi tóc muối tiêu của video; kho không có nhóm > 45). Robot `BOT-TALKA-DEF-INDIA-01` (người máy Talka India, nữ, saree hồng viền vàng) — khác giới với diễn giả nên giọng hai nửa tách hẳn. Ảnh kho mặc quần áo thường nên kịch bản chỉ lấy mặt/tóc/dáng, trang phục theo vai (sơ mi hồng, cà vạt, gi-lê + quần kẻ sọc xám như video).
- **Đơn giản hoá**: máy đứng yên (video đẩy/rung nhẹ từ giây 10); bỏ ly champagne lọt lên sân khấu ở 10–14 s (lỗi liên tục của video gốc); cảnh thú nhận dùng lại khung sân khấu cảnh 1 thay vì khung gần hơn; câu giải pháp 23 từ tách 2 lượt.
- **Hook mới (B)**: tình huống "quầy check-in hội nghị" trong insight: "Thank you for coming" → đừng đáp "You're welcome". Cùng cấu trúc + độ dài hook gốc; "You're welcome" là một trong 3 câu bị gạch ở cảnh tiệc nên nối mạch tự nhiên. Cử chỉ: lắc đầu nhẹ + lắc ngón trỏ một lần.
- Biến thể A đặt tên `bien-the-01-goc-nam-50-gile-xam` (bám video: nam). Insight nói trọng tâm là nữ 35–50: biến thể sau đổi nhân vật chỉ cần thêm dòng `NHAN_VAT` với `gioi: "nu"` (đại từ + động từ Hindi tự đổi).

## Rủi ro / cần xem khi gen
- Cảnh 2 (tiệc) là Prompt ảnh mới: xem `scene2_start.png` có đúng mặt/trang phục, không nhìn ống kính.
- Cảnh 6: điện thoại phải không chữ; Muse hay vẽ giao diện.
- Phần 2: thẻ từ vựng + ô tô vàng với câu Hindi (neo "इंग्लिश") cần xem `card*.png` khi gen thật (rủi ro đã ghi ở `san-khau-x0071-hindi`).
- Người dùng: chọn Thương hiệu (logo Talka AI, Outro Google Play) trong trang dự án.

## Nhật ký
- 20/11/2026: `danh-gia --lang hi`, xem luot_01..09 + ảnh ghép 1 khung/giây. Viết hồ sơ, 2 kịch bản, 2 biến thể (sinh bằng `cong-cu/tao_bien_the.py`). `kiem-tra --tai-anh` cả hai: 0 lỗi, 0 cảnh báo.
- 20/11/2026: `nhap --chay-thu` A → loại `8eecbce1-Dien-gia-san-khau-Hindi-Nice-to-meet-you-8207`, dự án `8eecbce1-Speaker-Hindi---Me-too-eebe`, biến thể `bien-the-01-goc-nam-50-gile-xam` đang chạy thử.
- 20/11/2026: `nhap` B (không chạy thử) → loại `8eecbce1-Dien-gia-san-khau-Hindi-Nice-to-meet-you-doi-hook-e908`, dự án `8eecbce1-Speaker-Hindi---Me-too-doi-hook-8480`, biến thể `bien-the-01-hook-thank-you-for-coming`.
- 20/11/2026: chạy thử cảnh 1 ĐẠT: `scene1_start.png` đúng mặt kho + trang phục vai + sân khấu; `scene1_cut.mp4` 4,88 s, ngón trỏ tay phải giơ/hạ đúng nhịp, máy đứng yên. Cảnh 2–6 + phần 2 Studio gen tiếp (chưa xem).
