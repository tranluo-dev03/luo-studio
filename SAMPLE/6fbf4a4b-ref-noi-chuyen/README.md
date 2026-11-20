# Thể loại `6fbf4a4b-ref-noi-chuyen`: robot gia sư AI (ô ngang trên) + người học làm việc nhà (toàn khung)

Video mẫu `6fbf4a4b-ref-noi-chuyen.mp4` (43,8 s, không cắt cảnh, camera đứng yên). Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md), cấu trúc hook/tình huống: [CAU-TRUC.json](CAU-TRUC.json).

| Kịch bản | File | Nội dung |
|---|---|---|
| A `goc` | `KICH-BAN-6FBF4A4B-REF-NOI-CHUYEN.txt` + `BIEN-THE-6FBF4A4B-REF-NOI-CHUYEN.json` | hook + tình huống như video gốc |
| B `hook` | `...-HOOK.txt` + `BIEN-THE-...-HOOK.json` | giữ tình huống, đổi hook (lượt 1-3); token `HOOK_TV` cho biểu cảm hook |

Khuôn: ghép 2 lớp, MỘT phần (không dùng khối CẢNH). Nền HOC, ô DAY `0.02, 0.01, 0.96, 0.32` (691x409 px → gen 16:9). Lý do chọn: ô robot là vùng tách biệt, không bao giờ hai người cùng nói.
Sinh biến thể: `cong-cu/tao_bien_the.py` (sửa lời/nhân vật ở đó). Ảnh: `anh/DAY.png` (robot dùng lại từ phong-van-pho-hindi), `anh/HOC.png` (gen bằng Muse, nền xanh, phong cách Pixar).
Code riêng: `app/production/types/6fbf4a4b-ref-noi-chuyen/` (post.py, config.json: phụ đề ô trắng robot / ô vàng người học, sai đỏ ❌ → đúng xanh ✅).

## Quyết định (chạy ngầm)
- Yêu cầu người dùng: nhân vật và bối cảnh phải là NGƯỜI THẬT (ảnh chụp), không hoạt hình, giống video gốc. STYLE LOCK ghi "photorealistic live-action", NEGATIVE cấm cartoon/3D render; ảnh `anh/HOC.png` gen bằng `cong-cu/gen_anh_that.py` (ghi đè STYLE Pixar, không sửa mã chung). Robot `anh/DAY.png` là ảnh robot thật dùng lại.
- Video trùng md5 với `bb327bac-ref-noi-chuyen` (phiên trước, người học hoạt hình) nên dùng lại phân tích; thể loại này là bản người thật.
- Toàn tiếng Anh; người học nói tiếng Anh vụng ("I am Mexico") nên hook giữ cấu trúc sửa lỗi.
- Bỏ vòng sóng âm quanh robot và dải sóng nháy (Studio chưa làm); bỏ câu "Más o menos" mở đầu.
- Hook B: "Where do you live?" / "I am live in Mexico." / "Almost. Better say: I live in Mexico."
- Khuôn ghép 2 lớp (an toàn, không đổi bố cục gốc).

## Chạy thử (kịch bản A, biến thể 6fbf4a4b-goc-01)
`base_HOC.png` người thật trong bếp thật, `base_DAY.png` robot nền đen 16:9 đạt; Studio gen lại cảnh 1 một lần (Muse phóng hình), clip cảnh 1 robot nói đạt. Cả video đang gen trong Studio. Kịch bản B chưa chạy (người dùng tự bấm). Việc cần làm: chọn Thương hiệu (logo/outro) trong trang dự án.
