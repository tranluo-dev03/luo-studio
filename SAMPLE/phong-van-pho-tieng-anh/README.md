# Thể loại `phong-van-pho-tieng-anh`: phỏng vấn đường phố rồi chia trên/dưới + gia sư AI, lời tiếng Anh

Cùng khuôn video mẫu `1510_interview street hindi_005 (11)` (app Aiva AI) như [phong-van-pho-malayalam](../phong-van-pho-malayalam/README.md) và
[phong-van-pho-tay-ban-nha](../phong-van-pho-tay-ban-nha/README.md), lời **tiếng Anh**. Phân tích video mẫu, số đo, giọng: xem
[PHAN-TICH-VIDEO-MAU.md](../phong-van-pho-malayalam/PHAN-TICH-VIDEO-MAU.md). Lần phân tích 17/11/2026 (`video-moi.py danh-gia` trên bản tải lên, 76,9 s, 9 cảnh cắt,
2 cụm giọng 211 Hz / 254 Hz, 0 đoạn máy chuyển động) khớp phân tích cũ: không có gì mới.

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Phỏng vấn | 1–6 | cảnh thường, MỘT góc qua vai, camera đứng yên | Phóng viên (PV nam) quay lưng mép trái cầm micro; người bán nữ đeo găng sau xe đẩy đồ ăn |
| 2. Chia trên/dưới | 7–12 | ghép 2 lớp, cắt cứng khi vào phần | Robot Aiva ô trên, người bán selfie ô dưới, nhìn thẳng ống kính |

| File | Nội dung |
|---|---|
| `KICH-BAN-PHONG-VAN-PHO-TIENG-ANH.txt` | Kịch bản 2 phần, sinh bằng `cong-cu/tao_kich_ban.py` (sửa ở đó) |
| `BIEN-THE-PHONG-VAN-PHO-TIENG-ANH.json` | 1 biến thể `en01-street-food-vendor`, sinh bằng `cong-cu/tao_bien_the.py` |

Code riêng: `app/production/types/phong-van-pho-tieng-anh/` (`gen.py` cắt sát theo lời + không tua nhanh, `post.py`, `config.json`: chép từ tay-ban-nha, chỉ đổi tên loại).

## Quyết định đã chốt (17/11/2026, chạy ngầm, không hỏi người dùng)

- Là thể loại MỚI (thư mục riêng) dù khuôn giống tay-ban-nha: kịch bản tay-ban-nha ghi cứng "Mexico / Mexican Spanish" và nhắc "reference photo"; mỗi thể loại sửa file riêng (không can thiệp chéo).
- Khuôn an toàn nhất, không đổi bố cục video gốc: phần 1 một góc qua vai (bỏ 2 cảnh chèn cận + đổi cỡ nhẹ của gốc), phần 2 ghép 2 lớp trên/dưới.
- PV nam, người bán nữ (khác giới, như video gốc): hai người cùng giới cùng khung thì Muse cho người bán nhép theo giọng PV.
- Lời viết lại theo mạch tay-ban-nha (12 lượt = 6 + 6), dịch sang tiếng Anh; "Soy de Puebla" → "I'm from Denver". Không có đoạn sửa "I am Kannur → from" như gốc (giống tay-ban-nha).
- Không có ảnh tham chiếu nên `refs` trống, kịch bản bỏ câu "reference photo", nhân vật/nền chỉ tả bằng chữ. KHÔNG gen (quy tắc: ảnh refs chỉ từ ảnh AI người dùng đưa).
- Hậu kỳ: chữ đen ô trắng, Arial, phần 1 y 1560, phần 2 y 960 cụm ≤ 3 từ; Whisper `small` (đa ngôn ngữ). Không tua nhanh.

## Chạy trong Studio

```
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\phong-van-pho-tieng-anh\KICH-BAN-PHONG-VAN-PHO-TIENG-ANH.txt SAMPLE\phong-van-pho-tieng-anh\BIEN-THE-PHONG-VAN-PHO-TIENG-ANH.json --ten-loai "Phong van pho tieng Anh" --ten-du-an "Phong van pho tieng Anh" --chay-thu
```
Việc cần làm trước khi gen: bổ sung ảnh AI (xem dưới) vào `REFS` trong `cong-cu/tao_bien_the.py` hoặc gắn trong trang dự án; chọn Thương hiệu (logo Aiva AI).

## Ảnh tham chiếu cần người dùng cung cấp

1. Robot Aiva (trắng, tai nghe có mic, chữ "AI" trên trán): `NGUOI_DAY` (đã có `phong-van-pho-tay-ban-nha/anh/robot-aiva.png`, người dùng có thể dùng lại).
2. Người bán nữ ~45 tuổi (mặt, tóc, trang phục): `NGUOI_HOC`.
3. Phóng viên nam (nhìn từ phía sau: tóc, kính, áo, quai ba lô): `NGUOI_PV`.
4. Bối cảnh phố không người: `NEN_PHO` (phần 1) và chợ đông `NEN_HOC` (phần 2, ô dưới).

## Rủi ro

- Không có ảnh refs: mặt/trang phục có thể lệch giữa phần 1 và phần 2 (phần 2 người bán selfie tạo mới từ chữ).
- PV quay lưng + người bán nói: Muse có thể xoay mặt PV ra camera (đã khai `QUAY_LUNG_PV`, `NHIN_`, EYE LINE).
- Robot: chữ "AI" trên trán Muse có thể vẽ sai/bỏ.
- Câu robot "Can you say this sentence after me?" rồi người bán "Yes, sure...": không có câu mẫu để lặp (như tay-ban-nha).

## Chưa chạy trên Muse. Còn khác video mẫu

Không có đoạn đố từ "Suddenly/Immediately/Otherwise/Therefore" (phần 1 gốc 11 cảnh, đây 6 cảnh); không sửa "I am Kannur"; không vạch cam giữa hai ô; phụ đề cụm ≤ 3 từ ở phần 2.
