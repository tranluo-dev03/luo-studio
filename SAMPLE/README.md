# SAMPLE: kịch bản, biến thể và tài liệu theo thể loại video

Mỗi **thể loại video** có một **mã** (chữ thường, không dấu, nối bằng gạch ngang, ví dụ `talka-bang-tu-vung`). Mã này dùng chung cho hai chỗ:

| Chỗ | Chứa gì |
|---|---|
| `SAMPLE/<mã>/` | Nội dung: kịch bản (`KICH-BAN-*.txt`), biến thể (`BIEN-THE-*.json`), phân tích video mẫu, công cụ tạo kịch bản, ghi chú |
| `app/production/types/<mã>/` | Code hậu kỳ riêng của thể loại (nếu có): `post.py`, cấu hình, ảnh/video dùng khi hậu kỳ |

Thể loại không có hậu kỳ riêng thì dùng hậu kỳ chung (`app/production/postprocess.py`: phụ đề, logo, end card).

## Các thể loại hiện có

| Mã | Mô tả | Hậu kỳ riêng |
|---|---|---|
| `talka-bang-tu-vung` | Robot dạy từ vựng Tây Ban Nha → Anh trước bảng chữ; bút đỏ chỉ chữ, chữ tiếng Anh hiện khi đọc; phần cuối quảng cáo app Talka | Có (`app/production/types/talka-bang-tu-vung/`) |
| `canh-sat-nu` | Hội thoại cảnh sát nữ và tài xế | Không |
| `xe-tai` | Tài xế xe tải và gia sư AI | Không |
| `ghep-hai-lop` | Loại "Ghép 2 lớp": mỗi nhân vật gen riêng rồi ghép khung | Không (ghép trong `app/luo-studio/split.py`) |
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
