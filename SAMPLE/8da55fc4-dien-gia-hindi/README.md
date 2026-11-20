# 8da55fc4 — Diễn giả sân khấu Hindi "Nice to meet you / Me too" (mã `8da55fc4-dien-gia-hindi`)

Video tham chiếu: `userdata/studio/claude/_uploads/8da55fc4-Speaker-HINDI-sample.mp4` (25,6 s, 1440×2560, Hindi xen Anh, app **Talka AI**).
Một nhân vật (diễn giả) trên sân khấu kiểu TED: hook → tiệc (3 câu gạch đỏ) → thú nhận → giải pháp Talka AI → giơ điện thoại.
Video trùng từng byte với `8eecbce1-Speaker-HINDI-sample.mp4` (thể loại `8eecbce1-dien-gia-hindi`); lần này người dùng chỉ định cấu trúc CHỈ gồm Hook / Nỗi đau / Giải pháp (không demo, không CTA) nên đây là thể loại riêng, một phần.

| Phần | Cảnh/lượt | Chế độ | Video gốc |
|---|---|---|---|
| Hook | cảnh 1 | cảnh thường, Prompt ảnh sân khấu | 0:00–0:05 |
| Nỗi đau (tiệc) | cảnh 2 (3 câu gạch đỏ, `gach: true`) | Prompt ảnh mới, khung trung, khách mờ tiền cảnh phải | 0:05–0:10 |
| Nỗi đau (thú nhận) | cảnh 3 | `Khung đầu từ cảnh: 1` | 0:10–0:14 |
| Giải pháp | cảnh 4–6 (giơ điện thoại ở cảnh 6) | nối khung | 0:14–0:25,6 |
| Badge Talka AI | — | KHÔNG gen → Thương hiệu (logo cố định góc trên trái) | suốt video |

## File
| File | Nội dung |
|---|---|
| `PHAN-TICH-VIDEO-MAU.md` | Tổng quan, lời đối chiếu phụ đề, bảng hành động, bảng "video gốc → kịch bản", Insight (nguyên văn), cấu trúc hook/tình huống |
| `CAU-TRUC.json` | hook / tinh_huong / quang_cao (null) / hook_moi |
| `KICH-BAN-8DA55FC4-DIEN-GIA-HINDI.txt` + `BIEN-THE-8DA55FC4-DIEN-GIA-HINDI.json` | Kịch bản **A (goc)**: giữ hook + tình huống như video; biến thể sau ĐỔI NHÂN VẬT (TEN_/VAI_/NGUOI_/GIONG_HOC, DAO_HOC, DAO_LY, DAO_DIENTHOAI, NEN_HOC, NEN_TIEC, HE/HE_C/HIS/HIM là token) |
| `KICH-BAN-8DA55FC4-DIEN-GIA-HINDI-HOOK.txt` + `BIEN-THE-8DA55FC4-DIEN-GIA-HINDI-HOOK.json` | Kịch bản **B (đổi hook)**: cảnh 1 dùng token `LUOT_1`, `HOOK_HANH_DONG`, `HOOK_DIEN_BIEN`, `HOOK_CAM_XUC`, `HOOK_KHUNG_CUOI`; cảnh 2–6 y như A |
| `cong-cu/tao_kich_ban_hook.py` | Sinh kịch bản B từ A (thay đúng các câu của cảnh 1, assert mỗi câu thấy đúng 1 lần) |
| `cong-cu/tao_bien_the.py` | Sinh cả hai file biến thể từ bảng `NHAN_VAT` (A) và `HOOKS` (B); đại từ + đuôi động từ Hindi đổi theo giới (देता था/देती थी, लगा/लगी) |

Code: dùng chung `app/production/types/san-khau-chia-doi-gia-su-ai/` (không sửa): `gen.py` → `nhieu_phan` (1 phần, 6 cảnh thường), `post.py` vẽ chữ gạch đỏ + X + tiếng sai ở lượt `gach`, phụ đề Hindi Nirmala UI + shaping complex.

## Cách chạy
```
.venv\Scripts\python.exe SAMPLE\8da55fc4-dien-gia-hindi\cong-cu\tao_kich_ban_hook.py
.venv\Scripts\python.exe SAMPLE\8da55fc4-dien-gia-hindi\cong-cu\tao_bien_the.py
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\8da55fc4-dien-gia-hindi\KICH-BAN-8DA55FC4-DIEN-GIA-HINDI.txt SAMPLE\8da55fc4-dien-gia-hindi\BIEN-THE-8DA55FC4-DIEN-GIA-HINDI.json --tai-anh
```

## Quyết định đã chốt (chạy ngầm, không hỏi lại)
- **Khuôn**: cảnh thường MỘT nhân vật (không ai nói cùng khung → không cần ghép 2 lớp). Không đổi bố cục video gốc. Dùng lại hậu kỳ `san-khau-chia-doi-gia-su-ai` vì nó đã có hiệu ứng chữ gạch đỏ + X cho cảnh tiệc; không viết code mới.
- **Không có phần demo / CTA**: người dùng không chỉ định và video không có → không gen. Badge Talka AI = Thương hiệu.
- **Ảnh refs từ kho**: diễn giả `NAM-30-45-IND-10` (nam India mảnh, mặt gầy nhiều nếp, tóc bạc chải ngược, ria mép bạc dày) — trông già nhất, tóc bạc gần nhất với diễn giả ~50 tuổi tóc muối tiêu của video (kho không có nhóm > 45). Đã xem cả 10 ứng viên NAM-30-45-IND. Khác ứng viên đã dùng ở `8eecbce1` (IND-04) để hai dự án không trùng mặt. Video gốc là nam → biến thể mẫu nam; insight nói trọng tâm nữ 35–50 → biến thể sau chỉ cần thêm dòng NHAN_VAT `gioi: "nu"`.
- **Đơn giản hoá**: máy đứng yên (video đẩy/rung nhẹ từ 10 s); bỏ ly champagne lọt lên sân khấu ở 10–14 s (lỗi liên tục video gốc); cảnh thú nhận dùng lại khung sân khấu cảnh 1 thay vì khung gần hơn; câu giải pháp 23 từ tách 2 lượt (4 + 5).
- **Hướng nhìn cảnh tiệc**: video gốc nhìn sang PHẢI khung về vị khách có vai mờ ở góc dưới phải (bản `8eecbce1` ghi nhầm "trái") → kịch bản ghi phải. Thêm nét nhăn mặt ngượng sau câu cuối theo insight ("mặt nhăn lại vì ngượng").
- **Lệch giữa mô tả người dùng và video**: lời thú nhận "trước đây tôi cũng trả lời y như vậy" người dùng xếp trong "Nỗi đau" (cảnh tiệc), video nói câu này khi đã về SÂN KHẤU → giữ như video (cảnh 3 sân khấu), vẫn tính vào phần tình huống. Video có thêm "देखिए!" + giơ điện thoại ở cuối giải pháp → giữ.
- **Hook mới (B)**: tình huống "hành lang công ty" của insight: "How's it going?" → đừng đáp "I'm fine, thank you". Cùng cấu trúc + độ dài hook gốc; "I'm fine, thanks" là một trong 3 câu bị gạch nên nối mạch tự nhiên. Cử chỉ: nghiêng đầu, nhướng mày, tay phải hé mở như hỏi, rồi lắc đầu chậm một lần. (Không dùng "Thank you for coming" vì đã dùng ở `8eecbce1`.)

## Rủi ro / cần xem khi gen
- Cảnh 2 (tiệc) là Prompt ảnh mới: xem `scene2_start.png` đúng mặt/trang phục, nhìn sang phải, không nhìn ống kính; khách chỉ là vai mờ.
- Cảnh 3 `Khung đầu từ cảnh: 1`: không được cầm ly.
- Cảnh 6: điện thoại phải không chữ; Muse hay vẽ giao diện.
- Người dùng: chọn Thương hiệu (logo Talka AI góc trên trái) trong trang dự án.

## Nhật ký
- 20/11/2026: `danh-gia --lang hi` (số đo khớp lần chạy 8eecbce1), xem ảnh tổng quan + luot_04, luot_09. Viết hồ sơ, 2 kịch bản (B sinh từ A), 2 biến thể. `kiem-tra --tai-anh` cả hai: 0 lỗi, 0 cảnh báo.
- 20/11/2026: `nhap --chay-thu` A → loại `8da55fc4-Dien-gia-san-khau-Hindi-Nice-to-meet-you-96b9`, dự án `8da55fc4-Speaker-Hindi-Me-too-c25b`, biến thể test `bien-the-01-goc-nam-50-gile-xam`.
- 20/11/2026: `nhap` B (không chạy thử) → loại `8da55fc4-Dien-gia-san-khau-Hindi-Nice-to-meet-you-doi-hook-ae12`, dự án `8da55fc4-Speaker-Hindi-Me-too-doi-hook-3cfa`, biến thể `bien-the-01-hook-hows-it-going`.
- 20/11/2026: `scene1_start.png` ĐẠT: đúng mặt kho (tóc bạc chải ngược, ria bạc), sơ mi hồng + cà vạt + gi-lê/quần kẻ sọc xám, micro cài tai, bút bấm tay phải, sân khấu rèm navy + khối đỏ + bục vòng đỏ + đầu khán giả mờ. Khung rộng hơn yêu cầu (thấy tới ống quyển thay vì từ gối).
- 20/11/2026: `scene1_cut.mp4` 4,73 s ĐẠT (gốc 4,97 s): ngón trỏ tay phải giơ lên ngang vai trong lúc nói, hạ trước từ cuối, máy đứng yên, mặt/trang phục giữ nguyên. Cảnh 2–6 Studio gen tiếp (chưa xem); kịch bản B chưa gen.
- 20/11/2026: nhóm `yfma9g` (kịch bản A) → `BIEN-THE-NHOM-yfma9g.json`, 10 biến thể sinh bằng `cong-cu/tao_bien_the_nhom_yfma9g.py`: đổi BỘ BÀI HỌC (lời hook + 3 câu sách vở bị gạch ở lượt 2) và nhân vật. Người dùng gửi 11 bộ + "1 bộ = 1 nam + 1 nữ" nhưng nhóm đặt 10 biến thể → lấy 10 bộ đầu, giới xen kẽ nữ/nam (5 + 5), mã bốc ngẫu nhiên (seed `yfma9g`) trong 20 mã người dùng gửi. Bộ 11 ("Do you eat meat?") và nửa còn lại của mỗi cặp: chạy script với `--day-du` (22 biến thể). Tên trong câu sai đổi theo giới (Priya/Rahul), tuổi theo nhóm tuổi (27/38). Trang phục theo insight (saree, anarkali, blazer + chân váy, suit trắng/đỏ mận, kurta + blazer; nam: suit, Nehru, bandhgala), bối cảnh tiệc + đồ cầm đổi theo bài (`NEN_TIEC`, `DAO_LY`). `kiem-tra --tai-anh`: 0 lỗi, 0 cảnh báo.
- 20/11/2026: sửa kịch bản A (B sinh lại): "Diễn biến" cảnh 2 bỏ 3 câu viết cứng "(Me too / You're welcome / I'm fine, thanks)" (trường này gửi cho Muse) → "ba câu đáp xã giao ngắn liên tiếp (đúng lời của lượt)". Đã PUT /api/types cho cả hai loại dự án (96b9, ae12). Không thêm token mới.
- 20/11/2026: nhóm `jt9nb2` (kịch bản A) → `BIEN-THE-NHOM-jt9nb2.json`, 20 biến thể = 10 bộ bài học đầu × (1 nữ + 1 nam), dùng đúng 20 mã người dùng gửi, mỗi mã một lần, ghép cặp ngẫu nhiên (seed `jt9nb2`); sinh bằng `cong-cu/tao_bien_the_nhom_jt9nb2.py` (dùng chung bảng của `tao_bien_the_nhom_yfma9g.py`). Bộ 11 "Do you eat meat?" không dùng (người dùng ghi "10 bản"). `kiem-tra --tai-anh`: 0 lỗi, 0 cảnh báo. Không sửa kịch bản.
