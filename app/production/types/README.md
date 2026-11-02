# Hậu kỳ riêng theo thể loại video

Mỗi thư mục con là hậu kỳ của **một thể loại**, tên thư mục = mã thể loại (trùng `SAMPLE/<mã>/`, nơi chứa kịch bản/biến thể của thể loại đó).

```
app/production/types/<mã>/
  post.py        điểm vào (bắt buộc)
  README.md      làm gì, file nào
  config.json    tham số (tuỳ chọn)
  assets/        ảnh/video riêng của thể loại (tuỳ chọn)
```

## Studio gọi hậu kỳ riêng thế nào
`app/luo-studio/server.py` → `custom_post`: nếu file loại dự án (`userdata/studio/types/<id>.json`) có `"post": "<mã>"` thì khi bấm Hậu kỳ, Studio chạy

```
python post.py <thư mục chạy>/raw.mp4 --scenes <thư mục chạy>/scenes.json --out <thư mục chạy>/final.mp4
```

`scenes.json` = `[{turn, start, end}]`: mốc (giây) từng cảnh trong `raw.mp4` (turn đếm từ 0). Không có `"post"` thì dùng hậu kỳ chung `app/production/postprocess.py`.

`post.py` tự `import` được `app/production/postprocess.py` (Whisper, cắt, end card...) bằng cách thêm thư mục `app/production` vào `sys.path`; xem `talka-bang-tu-vung/post.py`.

## Thể loại có hậu kỳ riêng
- `talka-bang-tu-vung/`: bút đỏ chỉ chữ + chữ tiếng Anh hiện khi đọc, logo, bảng chữ quảng cáo, end card, không phụ đề.
