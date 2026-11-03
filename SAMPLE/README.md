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

## Thêm thể loại mới

1. Tạo `SAMPLE/<mã>/`, phân tích video mẫu bằng `_chung/phan-tich-video.py`, viết kịch bản + biến thể (xem `_chung/HUONG-DAN-CHO-AGENT.md`).
2. Cần hậu kỳ riêng: tạo `app/production/types/<mã>/post.py` (xem `app/production/types/README.md`), rồi trong file loại dự án (`userdata/studio/types/<id>.json`) đặt `"post": "<mã>"`.
3. Ghi lại trong `SAMPLE/<mã>/README.md` những gì đã thử và kết quả, để lần sau không lặp lại.
