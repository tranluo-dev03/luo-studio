# Thể loại `quet-an-ninh-day-chuyen`: quét an ninh cơ thể (dây chuyền) + gia sư AI

Nhân bản từ `soi-hanh-ly-gia-su-ai` (bản KHÔNG-BÉ) ngày 10/11/2026 theo [CHECKLIST-YEU-CAU-CHUYEN-KICH-BAN.txt](CHECKLIST-YEU-CAU-CHUYEN-KICH-BAN.txt).
Code riêng: `app/production/types/quet-an-ninh-day-chuyen/` (`gen.py`, `post.py`, `config.json`, gọi `types/_chung/`).

## Dạng video: MỘT dự án, hai phần (13 + 15 = 28 lượt)

| Phần | Cảnh | Nội dung |
|---|---|---|
| 1. Quét an ninh | 1–13, cảnh thường, 3 góc A/B/C | Nhân viên (`CANBO`, TRÁI cạnh cổng) hỏi hành khách nữ (`HOC`, PHẢI, vừa qua cổng) vì cổng dò kim loại báo động: dây chuyền chưa tháo. Cảnh 1 mở đầu bằng beep + đèn đỏ rồi cú lia vụt sang hành khách |
| 2. Hành khách + gia sư AI | 14–28, ghép 2 lớp | Hành khách selfie (nền sảnh sân bay) + robot ô góc trên phải; "I have 48" ❌ → "I am 48" ✅; giới thiệu, giá, kêu gọi |

Lời thoại 1–5 mới, **6–28 giữ nguyên** nguồn: 1 `Ma'am, could you step back for a moment?` · 2 `Sure.` · 3 `The scanner detected something metallic. Are you wearing any jewelry?` · 4 `Oh, it might be my necklace. I forgot to take it off.` · 5 `Please take it off. Is this your first time in America?`

## Dòng thời gian dây chuyền (khoá cứng trong từng cảnh)

| Cảnh | Trạng thái | Động tác |
|---|---|---|
| mở đầu + 1–2 | ĐEO | đèn đỏ nháy + beep; nhân viên ra dấu dừng; hành khách gật, KHÔNG chạm dây |
| 3 | ĐEO | nhân viên ra dấu cổng rồi cử chỉ nhẹ về vùng cổ (không chạm); bà nhìn xuống dây, đưa tay về phía dây |
| 4 | ĐEO | ngón tay chạm mặt dây; ngước nhìn nhân viên, hơi ngượng |
| 5 | ĐEO → THÁO | nhân viên chỉ khay đồ; bà hai tay gỡ chốt sau gáy, kéo dây ra, cầm ở tay phải (có `Giữ sau lời: 1.0` để kịp xong động tác) |
| 6 | CẤT | bà thả dây vào túi khoác vai khi trả lời "visiting my daughter" |
| 7–13, phần 2 | KHÔNG CÓ | cổ trống; điện thoại ở cảnh 10 là vật duy nhất cầm trên tay |

Đèn: hai cột LED đỏ của cổng chỉ nháy ở đoạn mở đầu và đầu cảnh 1; từ cảnh 2 tắt, đèn nhỏ trên xà chuyển xanh.

## Bảng chuyển bối cảnh/đạo cụ (checklist mục C)

| Cũ | Mới |
|---|---|
| máy soi X-ray + băng chuyền | cổng dò kim loại bạc (ảnh nền `1-NEN-CONG-DO-KIM-LOAI.webp`), đứng yên giữa-sau |
| vali xanh + vali nâu | bỏ hẳn (token `DAO_VALI*`, `DAO_BE` không còn trong kịch bản) |
| đèn đỏ trên máy soi | hai cột LED đỏ + tiếng beep ngắn ở cổng (chỉ lúc phát hiện) |
| chỉ xuống nắp vali / mở khoá kéo | ra dấu dừng → cử chỉ nhẹ về vùng cổ → bàn tay mở về khay đồ |
| hành khách chạm khoá vali | hành khách chạm / gỡ dây chuyền |
| màn hình X-ray | màn hình nhỏ tối trên xà cổng, không chữ |
| người mẹ địu bé | hành khách nữ, KHÔNG em bé; túi khoác vai giữ, tay đặt lên quai túi |

## File

| File | Dùng làm gì |
|---|---|
| `KICH-BAN-QUET-AN-NINH-DAY-CHUYEN.txt` | Kịch bản: `[HAU KY] loai: quet-an-ninh-day-chuyen` + PHAN 1 (13 CẢNH) + PHAN 2 (`[GHEP HAI LOP]`). Sinh bằng `cong-cu/tao_kich_ban.py`: sửa ở đó rồi chạy, không sửa tay `.txt` |
| `BIEN-THE-QUET-AN-NINH-DAY-CHUYEN.json` | 1 biến thể, 28 lượt, đã gắn `refs` 4 ảnh. Sinh bằng `cong-cu/tao_bien_the.py` |
| `anh-tham-chieu/` | 4 ảnh người dùng gửi: `1` nền cổng dò kim loại (gắn `NEN_SOI` và `NEN_HOC`), `2` robot gia sư AI (`NGUOI_DAY`), `3` hành khách (`NGUOI_HOC`), `4` nhân viên TSA (`NGUOI_CANBO`) |
| `CHECKLIST-YEU-CAU-CHUYEN-KICH-BAN.txt` | Yêu cầu gốc |
| `PHAN-TICH-VIDEO-MAU.md` | Phân tích video mẫu (bản sao từ `soi-hanh-ly-gia-su-ai`, chỉ dùng cho nhịp/phần 2) |
| `PROMPT-CHO-AGENT.txt` | Quy tắc để agent viết biến thể mới |

Đường dẫn ảnh trong `refs` là đường dẫn tương đối từ thư mục gốc dự án (`SAMPLE/quet-an-ninh-day-chuyen/anh-tham-chieu/...`), không phụ thuộc ổ đĩa.

## Chạy trong Studio

1. Kiểm tra: `.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\quet-an-ninh-day-chuyen\KICH-BAN-QUET-AN-NINH-DAY-CHUYEN.txt SAMPLE\quet-an-ninh-day-chuyen\BIEN-THE-QUET-AN-NINH-DAY-CHUYEN.json --tai-anh`
2. Nhập: `.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\quet-an-ninh-day-chuyen\KICH-BAN-QUET-AN-NINH-DAY-CHUYEN.txt SAMPLE\quet-an-ninh-day-chuyen\BIEN-THE-QUET-AN-NINH-DAY-CHUYEN.json --ten-loai "QUET AN NINH CO THE - DAY CHUYEN" --ten-du-an "quet-an-ninh-day-chuyen"` (thêm `--chay-thu` để chạy biến thể 1).
3. Chạy thử MỘT biến thể; xem trước `phan1/scene1_wide.png` (Officer trái, cổng giữa-sau, hành khách phải, đèn đỏ, không vali/băng chuyền), `scene1_start.png`, `scene3_start.png`, `scene8_start.png` (dây chuyền đeo ở 1–4, cổ trống ở 8), clip cảnh 5 (tháo dây liên tục, không nhân đôi), `phan2/base_HOC.png` (cổ trống), `phan2/base_DAY.png`.
4. Badge Talka AI: Thương hiệu → logo cố định của dự án (như bản gốc).

## Đã kiểm tra / chưa kiểm tra

- `video-moi.py kiem-tra --tai-anh`: 0 lỗi, 3 cảnh báo (kế thừa từ bản gốc, phần 2: `[NGHE HOC]`/`[NGHE DAY]` nhắc "nói", `[NHAN VAT HOC]` đầu nằm dưới ô); 5 ảnh refs đều đọc được; `nhieu_phan.plan`: 2 phần, 13 + 15 = 28 cảnh.
- `tao_kich_ban.py` tự kiểm: không còn suitcase/luggage/conveyor/zipper/batteries/water bottle/X-ray/baby/mother/vali/băng chuyền/em bé ngoài các câu CẤM (negative, "No suitcases...", ghi chú đầu file).
- **Chưa chạy thật trên Muse.** Phần dễ lỗi nhất: cảnh 5 (tháo dây trong ~3,5 s; nếu Muse không kịp, nâng `Giữ sau lời` ở cảnh 5 trong `tao_kich_ban.py` rồi chạy lại) và đoạn mở đầu + cú lia cảnh 1 (đèn đỏ, cổng đứng yên).

## Rủi ro / lưu ý

- Hành khách mặc theo ảnh tham chiếu (áo len be, áo hai dây trắng, jeans, giày trắng; dây chuyền vàng mảnh có mặt dây nhỏ), khác bản gốc (áo thun xám). Ảnh tham chiếu không có túi: túi khoác vai nâu được thêm bằng chữ theo checklist.
- Nhân viên theo ảnh tham chiếu (áo xanh hoàng gia, cà vạt đen, huy hiệu, bộ đàm vai); biển tên "TSA" trên ảnh bị cấm chữ trong prompt, Muse có thể vẽ lại chữ: gen lại cảnh 1 nếu thấy.
- Ảnh nền có băng chuyền/máy X-ray ở mép phải: `NEN_SOI` ghi rõ không có; nếu Muse vẽ lại, gen lại `scene1_wide.png`.
- Hai phần là hai ảnh gen khác nhau: ảnh tham chiếu mặt giữ khuôn mặt hành khách giữa hai phần.
