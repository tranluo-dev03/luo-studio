# Kho nhân vật và kho bot

Nhân vật trong video lấy từ kho này, không gen bằng Muse nữa (chốt 19/11/2026).

- `danh-muc.json`: 180 người + 36 bot, mỗi mục có mã, phân loại, mô tả ngoại hình viết sẵn theo ảnh (`mo_ta`, tiếng Anh) và link Google Drive của ảnh gốc.
- `tra-ma.py`: tra kho, mỗi mã in một dòng `mã | phân loại | mô tả`. AI dùng file này thay cho việc mở danh mục hay mở ảnh (tiết kiệm token).
- `anh/<MÃ>.webp`: ảnh đã tải về (toàn thân, đứng, nền xanh lục).
- `tai-anh.py`: tải ảnh còn thiếu theo danh mục (`python SAMPLE/_chung/kho-nhan-vat/tai-anh.py`, thêm `--lai` để tải lại tất cả, hoặc ghi vài mã để tải riêng).

## Mã

| Kho | Dạng mã | Ý nghĩa |
|---|---|---|
| Người | `NAM-20-30-AUMY-03`, `NU-30-45-LAT-07`, `NAM-5-10-IND-01` | giới (NAM / NU) - nhóm tuổi (5-10, 20-30, 30-45) - thị trường (AUMY = Âu Mỹ, LAT = Latinh, IND = India) - số 01..10 |
| Bot | `BOT-AIVA-DEF-AUMY-01`, `BOT-TALKA-AVA-INDIA-03` | BOT - thương hiệu (AIVA / TALKA) - loại (DEF = người máy mặc định, AVA = AI avatar) - thị trường (AUMY / LATIN / INDIA) - số 01..03 |

## Gắn nhân vật vào biến thể

Chỉ cần ghi mã ở `refs` của biến thể, theo khoá nhân vật của kịch bản:

```json
{ "name": "bien-the-01",
  "refs": { "NGUOI_HOC": "NU-30-45-AUMY-05", "NGUOI_DAY": "BOT-TALKA-AVA-AUMY-01" } }
```

Khi nhập / lưu dự án, Studio chép ảnh của mã đó vào dự án và gắn làm ảnh tham chiếu (tên hiển thị = mã). Máy chưa có ảnh thì Studio tự tải theo danh mục.
Trong trình sửa biến thể, ô "mã kho nhân vật" dưới trường Ngoại hình cũng nhận mã (gõ hoặc chọn rồi Enter).
`video-moi.py kiem-tra` báo lỗi khi mã không có trong kho.

Mô tả `NGUOI_<KHOÁ>` của biến thể lấy từ `mo_ta` của mã: phần trước dấu `;` là tuổi, da, tóc, dáng (giữ nguyên); phần sau là trang phục trong ảnh (giữ nếu hợp vai, vai cần đồng phục thì thay bằng trang phục của vai).

## Tra mã

```
python SAMPLE/_chung/kho-nhan-vat/tra-ma.py NU-30-45-AUMY-05 BOT-TALKA-AVA-AUMY-01    tra đúng các mã này
python SAMPLE/_chung/kho-nhan-vat/tra-ma.py NAM-30-45-LAT                              lọc theo đoạn mã
python SAMPLE/_chung/kho-nhan-vat/tra-ma.py NU-20-30 hi-vis                            đoạn mã + chữ trong mô tả
python SAMPLE/_chung/kho-nhan-vat/tra-ma.py BOT-AIVA INDIA --gon                       chỉ in mã
```

Khi người dùng ghi mã vào ô mô tả nhóm biến thể (hoặc ô yêu cầu thêm / insight / cấu trúc lúc phân tích video), Studio tự tra và chèn sẵn dòng thông tin của từng mã vào lời giao việc cho Claude; mã không có trong kho thì Studio báo ngay khi bấm viết biến thể.

## Thêm nhân vật mới

Thêm một mục vào `danh-muc.json` (mã, phân loại, `link`, `drive_id`, `mo_ta`) rồi chạy `tai-anh.py <MÃ>`. Link Drive phải chia sẻ công khai. `mo_ta` viết tiếng Anh theo ảnh, dạng `<tuổi, da, tóc, dáng>; <trang phục>`.
