# Thể loại `2e3fa1bf-canh-sat-xe-tai`: cảnh sát chặn xe tải, tài xế nói sai tuổi (người thật)

Video mẫu 14,7 s (xem [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md)). Cấu trúc hook / tình huống: [CAU-TRUC.json](CAU-TRUC.json).
Khuôn: cảnh thường, 2 nhân vật chung khung, MỘT góc máy đứng yên (giống phần 1 của `xe-tai-canh-sat-gia-su-ai`, nhưng không có phần gia sư AI trong hình, chỉ 4 cảnh).
Code riêng: `app/production/types/2e3fa1bf-canh-sat-xe-tai/` (`post.py`, `config.json`: phụ đề trắng ô đen y 1320; câu sai đỏ + ❌, câu sửa xanh + ✅).

| Kịch bản | File | Nội dung |
|---|---|---|
| A (goc) | `KICH-BAN-2E3FA1BF-CANH-SAT-XE-TAI.txt` + `BIEN-THE-2E3FA1BF-CANH-SAT-XE-TAI.json` | giữ hook + tình huống như video gốc |
| B (hook) | `KICH-BAN-2E3FA1BF-CANH-SAT-XE-TAI-HOOK.txt` + `BIEN-THE-...-HOOK.json` | tình huống giữ nguyên, hook (lượt 1–2) mới: "Officer, my old is fifty!"; token `HOOK_TV` (cách tài xế nói câu sai), `HOOK_CS` (nét mặt cảnh sát khi hỏi lại) |

Sinh bằng `cong-cu/tao_kich_ban.py` và `cong-cu/tao_bien_the.py`. Đổi hook ở B: đổi lời lượt 1, `to` của lượt 1, lượt 2 (câu hỏi lại) và lượt 3 (câu sửa) cho khớp; lượt 4 giữ.

## Quyết định (chạy ngầm, không hỏi người dùng)
- Chọn khuôn an toàn: cảnh thường, nữ tài xế + nam cảnh sát (khác giới, tránh Muse gán nhầm giọng); không ghép 2 lớp vì không có ô PiP.
- Không có đạo cụ (video gốc không có giấy tờ/điện thoại), tay tài xế trên bậu cửa sổ.
- Ảnh refs tự gen bằng Muse (`cong-cu/gen-anh-nhan-vat-that.py`: bản sao của `_chung/gen-anh-nhan-vat.py` đổi sang phong cách ảnh thật vì video là người thật; bản chung mặc định phong cách hoạt hình 3D) trên nền xanh lục: `anh/HOC.png`, `anh/CANHSAT.png`. Cả hai đạt lần gen đầu. Tài xế trong ảnh trông hơi già hơn "cuối 50": theo dõi khi chạy thử.
- Câu cuối của cảnh sát ("Practice English every day with an AI tutor") nằm trong cảnh; logo/outro chọn ở Thương hiệu.
- Còn khác video mẫu: phụ đề ô đen thay vì chữ viền; máy tĩnh (video gốc cũng tĩnh).

## Nhật ký
- 19/11/2026: tạo thể loại; `kiem-tra` 0 lỗi (A và B).
