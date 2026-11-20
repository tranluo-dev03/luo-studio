# Thể loại `bb327bac-ref-noi-chuyen`: robot gia sư AI (ô ngang trên) + người học làm việc nhà (toàn khung)

Video mẫu `bb327bac-ref-noi-chuyen.mp4` (43,8 s, không cắt cảnh, camera đứng yên). Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md), cấu trúc hook/tình huống: [CAU-TRUC.json](CAU-TRUC.json).

| Kịch bản | File | Nội dung |
|---|---|---|
| A `goc` | `KICH-BAN-BB327BAC-REF-NOI-CHUYEN.txt` + `BIEN-THE-BB327BAC-REF-NOI-CHUYEN.json` | hook + tình huống như video gốc |
| B `hook` | `...-HOOK.txt` + `BIEN-THE-...-HOOK.json` | giữ tình huống, đổi hook (lượt 1-3); token `HOOK_TV` cho biểu cảm hook |

Khuôn: ghép 2 lớp, MỘT phần (không dùng khối CẢNH). Nền HOC, ô DAY `0.02, 0.01, 0.96, 0.32` (691x409 px → gen 16:9). Lý do chọn: ô robot là vùng tách biệt, không bao giờ hai người cùng nói.
Sinh biến thể: `cong-cu/tao_bien_the.py` (sửa lời/nhân vật ở đó). Ảnh: `anh/DAY.png` (robot dùng lại từ phong-van-pho-hindi), `anh/HOC.png` (gen bằng Muse, nền xanh, phong cách Pixar).
Code riêng: `app/production/types/bb327bac-ref-noi-chuyen/` (post.py, config.json: phụ đề ô trắng robot / ô vàng người học, sai đỏ ❌ → đúng xanh ✅).

## Quyết định (chạy ngầm)
- Toàn tiếng Anh; người học nói tiếng Anh vụng ("I am Mexico") nên hook giữ cấu trúc sửa lỗi.
- Người học là hoạt hình 3D (script gen ảnh chỉ có phong cách Pixar), robot ảnh thật có sẵn; video gốc là người thật.
- Bỏ vòng sóng âm quanh robot và dải sóng nháy (Studio chưa làm); bỏ câu "Más o menos" mở đầu.
- Hook B: "Where do you live?" / "I am live in Mexico." / "Almost. Better say: I live in Mexico."

## Chạy thử (kịch bản A, biến thể bb327bac-goc-01)
Cảnh 1 (robot hỏi) gen xong: `base_HOC.png` (bếp, mặt nửa dưới), `base_DAY.png` (robot nền đen 16:9) đạt; clip `scene1_spk.mp4` 10 s, robot nghiêng đầu nhẹ. Việc cần làm: chọn Thương hiệu (logo/outro) trong trang dự án.
