# Thể loại `phong-van-pho-tay-ban-nha`: phỏng vấn đường phố rồi chia trên/dưới + gia sư AI, tiếng Tây Ban Nha (Mexico)

Cùng khuôn video mẫu `1510_interview street hindi_005` (app Aiva AI) như [phong-van-pho-malayalam](../phong-van-pho-malayalam/README.md), đổi lời sang tiếng Tây Ban Nha.
Phân tích video mẫu, số đo, giọng: xem [PHAN-TICH-VIDEO-MAU.md](../phong-van-pho-malayalam/PHAN-TICH-VIDEO-MAU.md) (không lặp lại ở đây).

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Phỏng vấn | 1–6 | cảnh thường, MỘT góc qua vai, camera đứng yên | Phóng viên (PV) quay lưng mép trái cầm micro; người bán (HOC) sau quầy hàng đúng nghề |
| 2. Chia trên/dưới | 7–12 | ghép 2 lớp, cắt cứng khi vào phần | Robot Aiva ô trên, người bán selfie ô dưới, nhìn thẳng ống kính |

| File | Nội dung |
|---|---|
| `KICH-BAN-PHONG-VAN-PHO-TAY-BAN-NHA.txt` | Kịch bản 2 phần, sinh bằng `cong-cu/tao_kich_ban.py` (sửa ở đó, không sửa tay) |
| `BIEN-THE-20-PHONG-VAN-PHO-TAY-BAN-NHA.json` | 20 biến thể, sinh bằng `cong-cu/tao_20_bien_the.py` (bảng NV trong file) |
| `nguon/20-bien-the-ES-Interview.csv` | Bảng nguồn của người dùng (tên, mô tả, link Drive ảnh người bán / phóng viên / bối cảnh) + lời thoại |
| `anh/robot-aiva.png` | Robot Aiva (ảnh người dùng cấp 12/11/2026: robot trắng, tai nghe, chữ "AI" trên trán) |
| `anh/bt20/nv<NN>.jpg`, `pv<NN>.jpg`, `nen<NN>.jpg` | Người bán (phông xanh), phóng viên (phông xanh), bối cảnh không người; tải từ link Drive |

Code riêng: `app/production/types/phong-van-pho-tay-ban-nha/` (`gen.py` cắt sát theo lời + không tua nhanh, `post.py`, `config.json`).

## Quyết định đã chốt (12/11/2026)

- Phóng viên LUÔN KHÁC GIỚI người bán (bảng của người dùng đã đúng như vậy: 10 người bán nam + PV nữ, 10 người bán nữ + PV nam). Lý do: hai người cùng giới cùng khung, PV quay lưng,
  Muse hay cho người bán nhép theo giọng PV / lặp câu (bài học Malayalam, xem NHAT-KY-TRI-THUC.md). `tao_20_bien_the.py` có `assert` chặn cặp cùng giới.
- Mọi đại từ và ngoại hình của phóng viên đi qua token (`HIS_PV`, `HIM_PV`, `TOC_PV`...) vì PV khi nam khi nữ; kịch bản không còn ghi cứng "his / beard / glasses / backpack".
  (Kịch bản `phong-van-pho-malayalam` hiện vẫn ghi cứng "his" cho PV: xem README thể loại đó.)
- Lời thoại theo bảng, chỉ sửa 3 chỗ: (1) gộp 2 câu liền của cùng một người thành một lượt (bảng 2+3 người bán; 8+9 robot; 14+15 robot) → 12 lượt (6 + 6) thay vì 15;
  (2) "Soy de Kannur" (địa danh Ấn Độ, chắc sót từ mẫu cũ) → "Soy de Puebla"; (3) "como nativa" → "nativa" (người bán nữ) / "nativo" (nam).
- Hậu kỳ: chữ đen ô trắng, font Arial, phần 1 ở đáy (y 1560), phần 2 tâm y 960 và chia cụm ≤ 3 từ. Không tua nhanh khoảng lặng.
- Người bán không đeo găng (bảng không ghi); tạp dề ghi trong trang phục theo bảng.

## Chạy trong Studio

```
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\phong-van-pho-tay-ban-nha\KICH-BAN-PHONG-VAN-PHO-TAY-BAN-NHA.txt SAMPLE\phong-van-pho-tay-ban-nha\BIEN-THE-20-PHONG-VAN-PHO-TAY-BAN-NHA.json --ten-loai "Phong van pho Tay Ban Nha" --ten-du-an "Interview street ES - 20 bien the" --chay-thu
```
Chạy thử MỘT biến thể (mặc định là biến thể đầu = `es01-carlos-hernandez`), xem `scene1_start.png`, nghe cảnh 1–3, rồi `phan2/base_DAY.png`, `phan2/base_HOC.png` trước khi chạy cả nhóm.
Nhớ chọn Thương hiệu (logo Aiva AI) trong trang dự án.

## Đã kiểm tra / chưa kiểm tra

- `video-moi.py kiem-tra` (không tải ảnh): 0 lỗi, 0 cảnh báo, 65 mục đạt (12/11/2026). 60 ảnh Drive đã tải về `anh/bt20/` (20 người bán, 20 phóng viên, 20 bối cảnh).
- Chưa nhập Studio, chưa chạy trên Muse.

## Rủi ro

- Robot: ảnh tham chiếu có chữ "AI" sáng trên trán và biểu tượng sách trên ngực; prompt cho phép đúng chữ "AI" trên trán, còn lại cấm chữ. Muse có thể vẽ chữ khác / bỏ chữ "AI".
- Ảnh bối cảnh có biển hiệu tiếng Tây Ban Nha: prompt ghi làm mờ, Muse vẫn có thể vẽ lại chữ. Ảnh es06 / es09 / es15 là ảnh toàn cảnh rất dẹt (2736x912), Muse có thể cắt lệch.
- Tiếng Tây Ban Nha: mốc lời lấy theo năng lượng âm thanh (như Malayalam) rồi mới đến Whisper; câu một từ không có. Nghe tay vài cảnh đầu.
- Câu robot "¿Puedes repetir esta frase en inglés?" rồi người bán "Sí, claro, puedo intentarlo": bảng không có câu tiếng Anh nào để lặp (video mẫu có đoạn sửa "I am from..."); giữ nguyên theo bảng.
- Biến thể 15–20 (người bán lớn tuổi) bảng không ghi nghề: nghề suy từ tên bối cảnh (thủ công, đồ ăn, trái cây, hoa, quần áo, bánh).

## Còn khác video mẫu

- Không có đoạn robot sửa lỗi phát âm "I am Kannur" → "I am from Kannur" (bảng không có); không vạch cam giữa hai ô; phụ đề theo câu / cụm ≤ 3 từ ở phần 2.
