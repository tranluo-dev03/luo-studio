# Thể loại: Talka bảng từ vựng (`talka-bang-tu-vung`)

Video mẫu: robot AI dạy cách nói từ Tây Ban Nha bằng tiếng Anh trước một bảng chữ ("¿CÓMO SE DICE?"), một cây bút đỏ chỉ vào chữ robot đang đọc, chữ tiếng Anh hiện ra khi đọc; phần cuối quảng cáo app **Talka** (đọc "TAWK-ah"). Phân tích chi tiết: `PHAN-TICH-VIDEO-MAU.md`.

## File

**Người dùng bắt đầu ở `HUONG-DAN-SU-DUNG.md`** (làm video, nhờ AI viết biến thể mới).

| File | Dùng để |
|---|---|
| `HUONG-DAN-SU-DUNG.md` | Hướng dẫn sử dụng + prompt mẫu nhờ AI viết biến thể |
| `KICH-BAN-TALKA-CO-CHU.txt` | Kịch bản đang dùng: 9 cảnh (6 cảnh bảng chữ + 3 cảnh quảng cáo nền thành phố) |
| `BIEN-THE-TALKA-CO-CHU.json` | Biến thể: robot, giọng, phát âm "Talka", tờ giấy (`NEN_BANG`), nền thành phố, 9 lượt thoại |
| `cong-cu/tao-kich-ban.py` | Tạo lại 2 file trên. Muốn sửa prompt thì sửa file này rồi chạy `python cong-cu/tao-kich-ban.py` |
| `PHAN-TICH-VIDEO-MAU.md` | Phân tích video gốc: lời thoại, thời lượng, bố cục |
| `phien-ban-cu/` | Bản đầu (bảng không chữ), giữ tham khảo |
| Hậu kỳ | `app/production/types/talka-bang-tu-vung/` (xem README ở đó) |

## Quy trình đang dùng (đã chốt)

**Muse chỉ gen robot nói trước bảng chữ CỐ ĐỊNH** (vạch xám luôn trống, không có tay/bút/chữ tiếng Anh).
**Hậu kỳ** làm phần còn lại, khớp lời đọc (Whisper):
- bút đỏ (giống video gốc) luôn nằm trên giấy, lướt qua đúng chữ robot đang đọc: từ Tây Ban Nha → chữ tiếng Anh → lướt lại khi đọc lại; sang cảnh sau trượt xuống hàng kế tiếp;
- chữ tiếng Anh hiện ra **nguyên chữ** đúng lúc bút đặt vào đầu chữ, giữ đến hết phần bảng chữ;
- ô bảng quảng cáo ở 3 cảnh cuối hiện đúng lời robot (như video gốc), logo, end card Talka; **không phụ đề**.
- Từ vựng cho bút và lời cho ô bảng **lấy từ chính biến thể** (`bien_the.py` trong thư mục hậu kỳ): biến thể mới không cần sửa code.

Studio tự chọn hậu kỳ này cho loại dự án có tên bắt đầu bằng `KICH-BAN-TALKA` (hoặc file loại có `"post": "talka-bang-tu-vung"`).

### Bố cục
- Robot từ bụng lên, đỉnh đầu ~40% chiều cao khung, tâm đầu ~62% chiều ngang, đầu rộng ~24%.
- Tờ giấy kem lưới chấm; tiêu đề ~6%; 8 hàng cách đều ~5%, từ ~12% đến ~47% → 5 hàng có chữ (Para mí … ¡Gracias!) nằm trên đầu robot.

## Những gì đã thử và vì sao bỏ (đừng lặp lại)

| Cách | Kết quả | Lý do bỏ |
|---|---|---|
| Muse tự vẽ tay + bút viết chữ, chỉ chữ | Chữ viết đè hàng khác, sai hàng (nhất là "Thank you"); bút không chỉ vào từ Tây Ban Nha | Model video gộp "chỉ chữ" với "đặt bút viết"; không giữ được chữ viết tay qua nhiều clip nối nhau |
| Video nền tham chiếu (gen nền trước, đưa làm tham chiếu) | Vẫn viết đè hàng | Muse vẽ lại toàn khung, tham chiếu chỉ là gợi ý |
| Ghép 2 lớp (robot phông xanh + nền giấy/bút gen riêng) | Cắt phông tốt, nhưng Muse vẫn viết sai hàng ở lớp nền; robot tự zoom giữa clip | Phức tạp, không giải quyết được lỗi viết chữ |
| Bàn tay/bút vẽ bằng code | Hoạt động nhưng không tự nhiên | Người dùng không chọn |
| Muse cho chữ tiếng Anh tự hiện (viết dần / hiện nguyên chữ) | Chữ hiện quá sớm (ngay trong câu hỏi) | Muse không bám nhịp lời nói |
| Prompt rất dài (~14.000 ký tự/clip) | Robot đọc lẫn "for me" vào câu hỏi | Từ vựng lặp 18 lần; Muse tự tóm tắt prompt làm mất chi tiết → dùng bản gọn (~6.000 ký tự) |

## Lỗi còn có thể gặp (do Muse)
- Robot thỉnh thoảng đọc lẫn từ tiếng Anh vào câu hỏi ("¿Cómo se dice for you…?") → gen lại cảnh đó. Hậu kỳ vẫn hiện chữ đúng lúc "Se dice, …" (lấy lần nói ngay trước "Repite").
- Vài khung lẻ chữ đen trên giấy lốm đốm trắng (model video vẽ lại cả khung + nén mạnh). Thoáng 1–2 khung.
- Muse có lúc vẽ thiếu vòng tròn đỏ ở các hàng dưới → hậu kỳ tự suy ra vị trí hàng theo khoảng cách đều.
