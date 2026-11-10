# Thể loại `chia-tren-duoi-bengali`: đối mặt rồi chia trên/dưới + gia sư AI, tiếng Bengali xen tiếng Anh

Video mẫu `oder 5.mp4` (58,8 giây, quảng cáo app Supernova AI). Chàng trai hỏi Nova quy tắc học tiếng Anh, rồi cắt sang khung chia trên/dưới: Nova sửa "I have twenty five" và "I am Kolkata", giới thiệu app, kêu gọi cài. Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Đối mặt | 1–4 | cảnh thường, một khung, camera đứng yên | Nova mép trái, chàng trai mép phải, nhìn nghiêng hẳn, nền xám |
| 2. Chia trên/dưới | 5–20 | ghép 2 lớp, cắt cứng khi vào phần | Nova ngồi sofa ô trên, chàng trai ô dưới, nhìn thẳng ống kính |

| File | Nội dung |
|---|---|
| `KICH-BAN-CHIA-TREN-DUOI-BENGALI.txt` | Kịch bản 2 phần |
| `BIEN-THE-CHIA-TREN-DUOI-BENGALI.json` | 1 biến thể bám sát video, sinh bằng script |
| `cong-cu/tao_bien_the.py` | Sửa lời thoại, tên app (`APP`), nhân vật, `refs` ở đây rồi chạy, không sửa tay JSON |
| `PHAN-TICH-VIDEO-MAU.md` | Số đo, bảng hành động, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc viết thêm biến thể |
| `anh/khung-phan1-mau.png`, `anh/khung-phan2-mau.png` | Khung video mẫu để so bố cục, KHÔNG gửi cho Muse |

Code riêng: `app/production/types/chia-tren-duoi-bengali/` (`gen.py`, `post.py`, `config.json`).

## Quyết định đã chốt

- Khuôn: nhiều phần, vì video đổi cơ chế ở 12,79 s (chung khung → hai ô tách biệt).
- `nen: DAY`, `khung DAY: 0, 0, 1, 0.541`, `khung HOC: 0, 0.541, 1, 0.459` (đo trên video). Cả hai gen 1:1.
- Lời lấy từ phụ đề trên hình. Tốc độ ghi "about 3.3 words per second" theo lời thật.
- `fx: none` mọi lượt (video không có ❌/✅).
- Hậu kỳ: font Nirmala UI, `shaping: complex`, chữ đen ô trắng, tâm y 1699, cỡ 54.
- Nova hai khoá (`NOVA` phần 1, `DAY` phần 2), cùng mô tả và giọng.

## Chạy trong Studio

Đã nhập ngày 10/11/2026: loại dự án "Chia trên dưới Bengali" (`Chia-tren-duoi-Bengali-4a9d`), dự án "oder 5 - Supernova Bengali" (`oder-5---Supernova-Bengali-08be`), chưa gen. Nhập lại khi cần:

```
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\chia-tren-duoi-bengali\KICH-BAN-CHIA-TREN-DUOI-BENGALI.txt SAMPLE\chia-tren-duoi-bengali\BIEN-THE-CHIA-TREN-DUOI-BENGALI.json --ten-loai "Chia trên dưới Bengali" --ten-du-an "oder 5 - Supernova Bengali"
```

Trước khi chạy thử:
1. Đổi ảnh hoặc lời: chạy `cong-cu/tao_bien_the.py` rồi `cong-cu/cap_nhat_studio.py` (đẩy vào đúng dự án cũ).
2. Chạy MỘT biến thể; xem `phan1/scene1_start.png` (hai người nhìn nghiêng), `phan2/base_DAY.png`, `phan2/base_HOC.png`, nghe cảnh 1–3 xem Muse nói Bengali có đúng không, rồi mới chạy cả nhóm.

## Code chung đã sửa (10/11/2026)

- `app/luo-studio/engine.py`: `speech_lang` trả `bn` khi câu có chữ Bengali; `speech_issues` bỏ kiểm từng chữ cho câu đó. Chỉ ảnh hưởng câu có chữ Bengali.
- `app/production/types/_chung/phu_de.py`, `hau_ky.py`: tuỳ chọn `phu_de.shaping` trong `config.json`, mặc định tắt nên thể loại khác không đổi.

## Đã kiểm tra / chưa kiểm tra

- `video-moi.py kiem-tra`: 0 lỗi, 0 cảnh báo.
- Đốt thử phụ đề Bengali trên chính video mẫu: chữ ghép đúng sau khi bật `shaping: complex`. Câu dài nhất chiếm 4 dòng, không che mặt.
- Chạy thật trên Muse: xem nhật ký chạy ở cuối file.

## Rủi ro

- **Muse nói Bengali: chưa kiểm chứng.** Nếu đọc sai, cân nhắc phiên âm Latin trong `text` và cần trường riêng cho chữ phụ đề.
- Câu Bengali không được kiểm lời từng chữ: câu nói lặp/thiếu không tự gen lại, phải nghe tay.
- Phần 1 hai người nhìn nghiêng: Muse hay xoay mặt người nói ra ống kính. Kịch bản đã khoá bằng EYE LINE và `NHIN_`/`NGHE_`; xem kỹ cảnh 1–2.
- Lời viết cho người học nam và gia sư nữ; đổi giới phải kiểm lại câu.

## Ảnh tham chiếu (10/11/2026)

- Gia sư: `anh/nova.png`, người dùng gửi, robot trắng đầu không tóc (khác nhân vật tóc nâu áo cam của video mẫu). Tên khoá vẫn là `NOVA`.
- Chàng trai: `anh/nguoi-hoc.png`, Muse gen từ lời tả theo yêu cầu người dùng (`cong-cu/gen_anh_hoc.py`), không dùng khung nào của video mẫu.

## Còn khác video mẫu

- Gia sư là robot trắng theo ảnh người dùng, không phải nhân vật hoạt hình tóc nâu áo cam.
- Nền xám phần 1 đứng yên, video mẫu gợn sóng chuyển động.
- Bỏ chớp trắng 21 s và việc gia sư đổi áo giữa phần 2.
- Tay Nova giữ trên gối, không mở ra khi giảng.
- Phụ đề theo câu, không theo cụm 2–4 từ, không tô đậm dần.

## Nhật ký chạy

- 10/11/2026: chạy thử biến thể 01 (hàng đợi `580f3a96`). Phần 1 xong, khung đầu đạt. Dừng ở cảnh 12/20 theo yêu cầu người dùng để quét mã độc trên máy. Bấm chạy lại biến thể trong Studio để tiếp tục, cảnh đã xong được giữ.
- 10/11/2026: biến thể 01 xong, final 79,4 s, xuất ở `userdata/studio/exports/oder 5 - Supernova Bengali/`. Chờ người dùng duyệt.

## Bộ 20 biến thể theo CSV (10/11/2026)

- Kịch bản: `KICH-BAN-CHIA-TREN-DUOI-BENGALI-ROBOT-MO-DAU.txt`. Biến thể: `BIEN-THE-CHIA-TREN-DUOI-BENGALI-20-BIEN-THE.json`. Sinh lại bằng `cong-cu/tao_bo_csv.py`.
- Ảnh người học: điền cột link trong `cong-cu/20-bien-the.csv` hoặc đặt tệp `anh/bien-the/01.png` đến `20.png`, rồi sinh lại.
- Nhập trên máy khác: `.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap <kịch bản> <biến thể> --ten-loai "Bengali robot mo dau" --ten-du-an "Aiva Bengali 20 bien the"`.
- Chạy thử trước bt-01 và bt-06 (nam, nữ), xem người học có nhép theo robot ở phần 1 không.
