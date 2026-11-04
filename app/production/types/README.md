# Code riêng theo thể loại video (gen + hậu kỳ)

Mỗi thư mục con là code riêng của **một thể loại**, tên thư mục = mã thể loại (trùng `SAMPLE/<mã>/`, nơi chứa kịch bản/biến thể của thể loại đó).
Mỗi dự án thuộc một thể loại; thể loại nào cần cách gen hoặc hậu kỳ khác chế độ chung thì có code riêng ở đây.

```
app/production/types/<mã>/
  gen.py         gen riêng (tuỳ chọn): cảnh gen thế nào, trộn các chế độ, ghép ra raw.mp4
  post.py        hậu kỳ riêng (tuỳ chọn)
  README.md      làm gì, file nào
  config.json    tham số (tuỳ chọn)
  assets/        ảnh/video riêng của thể loại (tuỳ chọn)
app/production/types/_chung/    code dùng lại được cho nhiều thể loại (không phải một thể loại)
```

## Khai báo
Trong kịch bản có khối

```
[HAU KY]:
loai: <mã>
```

(các token chỉ dùng cho hậu kỳ cũng đặt trong khối này, không gửi cho Muse). Thể loại có file nào thì Studio dùng file đó; thiếu file nào thì dùng phần chung tương ứng.

## Gen riêng (`gen.py`)
`app/luo-studio/engine.py` → `custom_gen` / `run_variant`: có `types/<mã>/gen.py` thì Studio gọi

```python
run(vdata, template, out_dir, opts, emit, cancel)  # -> đường dẫn raw.mp4
```

với đúng tham số của `engine.run_variant` (biến thể, kịch bản, thư mục chạy, tuỳ chọn, hàm báo tiến độ `emit(scene_init / scene / log / item)`, cờ dừng).
Yêu cầu để Studio dùng như dự án thường: ghi `scene<N>_cut.mp4` và `scene<N>_last.png` cho từng cảnh ở thư mục chạy (Hậu kỳ tính mốc cảnh từ đó, "Làm lại từ cảnh N" xoá các file `scene<N>_*`),
và `emit("scene", n=..., thumb=..., clip=...)` với tên file trong thư mục chạy. `gen.py` có thể gọi lại `engine.run_variant(..., opts={..., "_part": True})` cho từng phần kịch bản.

## Hậu kỳ riêng (`post.py`)
`app/luo-studio/server.py` → `custom_post` (hoặc file loại dự án `userdata/studio/types/<id>.json` có `"post": "<mã>"`). Khi bấm Hậu kỳ, Studio chạy

```
python post.py <thư mục chạy>/raw.mp4 --scenes <thư mục chạy>/scenes.json --out <thư mục chạy>/final.mp4 --variant <thư mục chạy>/variant.json
```

`scenes.json` = `[{turn, start, end}]`: mốc (giây) từng cảnh trong `raw.mp4` (turn đếm từ 0). Không có `post.py` thì dùng hậu kỳ chung `app/production/postprocess.py`.
Sau hậu kỳ riêng, Studio vẫn gắn Thương hiệu của dự án (logo, video giới thiệu, outro).

`post.py` tự `import` được `app/production/postprocess.py` (Whisper, cắt, end card...) bằng cách thêm thư mục `app/production` vào `sys.path`; xem `talka-bang-tu-vung/post.py`.

## Code dùng chung (`_chung/`)
| File | Dùng khi |
|---|---|
| `nhieu_phan.py` | Một dự án nhiều phần (khoá biến thể `<TOKEN>@<phần>` ghi đè token riêng cho một phần, vd. `NHIN_HOC@2`), mỗi phần một chế độ (cảnh thường / ghép 2 lớp), chuyển cảnh giữa các phần (nhoè, chớp màu). Kịch bản chia phần bằng dòng `===== PHAN n: tên \| vao: nhoe 0.5 =====`; mỗi lượt thoại có `"phan"`. `gen.py` của thể loại chỉ cần gọi `nhieu_phan.run(...)` |
| `hau_ky.py` | Điểm vào hậu kỳ phụ đề cho thể loại nhiều phần: `post.py` chỉ cần `hau_ky.main(<thư mục thể loại>)`; kiểu phụ đề theo phần / người nói, độ cao, cỡ chữ đọc từ `config.json` → `phu_de` |
| `phu_de.py` | Phụ đề hậu kỳ có dòng dịch (`"dich"`), icon `x`/`check`/`dollar`, cụm nhấn trên ô vàng (`"nhan"`), ô nền sau chữ (`"o"`), tô màu từ sai/đúng (`"to"`), viền + tiếng `"fx"` wrong/right/ding, độ cao riêng từng lượt |

Thể loại mới cần trộn chế độ hoặc phụ đề kiểu này: tạo `types/<mã>/gen.py` / `post.py` vài dòng gọi `_chung` (xem `san-bay-gia-su-ai/`), chỉ viết code mới cho phần thật sự khác.

## Thể loại có code riêng
- `talka-bang-tu-vung/`: hậu kỳ: bút đỏ chỉ chữ + chữ tiếng Anh hiện khi đọc, logo, bảng chữ quảng cáo, end card, không phụ đề.
- `ai-tutor-ngoi-doc/`: hậu kỳ: khung bảng gen bằng AI + chữ/phiên âm điền theo lời đọc, nhãn góc dưới, không phụ đề.
- `san-bay-gia-su-ai/`: gen: phần 1 tình huống (cảnh thường) + phần 2 người dùng và AI gen riêng rồi ghép, nhoè chuyển cảnh; hậu kỳ: phụ đề 2 màu + dòng dịch + ❌/✅/$ + viền sai/đúng.
- `canh-sat-gia-su-ai/`: cùng khuôn `san-bay-gia-su-ai` (hoạt hình 3D): phần 1 cảnh sát chặn xe, 3 nhân vật, mỗi cảnh một góc máy; phần 2 tài xế + AI ghép 2 lớp; phụ đề ô vàng / ô đen chữ xanh ngọc / ô trắng, tô màu từ sai/đúng. Chỉ khác `config.json`.
- `soi-hanh-ly-gia-su-ai/`: cùng khuôn `san-bay-gia-su-ai`: phần 1 nhân viên soi chiếu + người mẹ địu con ở máy soi hành lý (cận nhân viên + lia máy theo tay tới vali sang người mẹ, toàn cảnh, cận hai người); phần 2 người mẹ quay selfie + robot AI ô bo góc góc trên phải; phụ đề trắng viền đen (phần 2 AI vàng), ❌/✅ + viền sai/đúng ở lượt người dùng. Chỉ khác `config.json`.
- `chia-doi-gia-su-ai/`: MỘT phần ghép 2 lớp, màn hình chia đôi dọc (robot AI nửa trái, người dùng bàn cà phê nửa phải; nhân vật nền `HOC` có `khung` riêng). Chỉ có hậu kỳ: phụ đề ô đen (AI trắng, người dùng vàng, câu sai đỏ, câu đúng xanh), viền sai/đúng chỉ ở nửa phải và nháy ở cuối câu (`phu_de.vien` trong `config.json`). Không có `gen.py`.
