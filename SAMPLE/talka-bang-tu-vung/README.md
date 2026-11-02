# Thể loại: Talka bảng từ vựng (`talka-bang-tu-vung`)

Video mẫu: robot AI dạy cách nói từ Tây Ban Nha bằng tiếng Anh trước một bảng chữ ("¿CÓMO SE DICE?"), một cây bút đỏ chỉ vào chữ robot đang đọc, chữ tiếng Anh hiện ra khi đọc; phần cuối quảng cáo app **Talka** (đọc "TAWK-ah"). Phân tích chi tiết: `PHAN-TICH-VIDEO-MAU.md`.

## File

**Người dùng bắt đầu ở `HUONG-DAN-NHANH.md`** (từng bước, ngắn gọn); chi tiết hơn ở `HUONG-DAN-SU-DUNG.md` (làm video, nhờ AI viết biến thể mới).

| File | Dùng để |
|---|---|
| `HUONG-DAN-SU-DUNG.md` | Hướng dẫn sử dụng + prompt mẫu nhờ AI viết biến thể |
| `KICH-BAN-TALKA-CO-CHU.txt` | Kịch bản đang dùng: 9 cảnh (6 cảnh bảng chữ + 3 cảnh quảng cáo nền thành phố) |
| `BIEN-THE-TALKA-CO-CHU.json` | **20 biến thể** (1–10 tiếng Tây Ban Nha giấy checklist; 11–13 tiếng Bồ Đào Nha giấy kẻ hai cột + bút bi đỏ; 14–20 tiếng Bồ Đào Nha sổ lò xo + bút máy, có icon). Mỗi biến thể: robot, giọng, phát âm "Talka", nền xanh (`NEN_XANH`) và nền thành phố (`NEN_PHO`), tờ giấy cho hậu kỳ dựng (`HAU_KY.bang`), 9 lượt thoại |
| `anh-mau/` | 2 ảnh giấy mẫu của biến thể 11–20 (`giay-hai-cot.png`, `giay-so-tay.png`). Giấy do hậu kỳ vẽ bằng code theo `HAU_KY.giay` nên **không gửi cho Muse** (Muse chỉ gen robot nền xanh) |
| `cong-cu/tao-20-bien-the.py` | Tạo lại file 20 biến thể (danh sách từ, icon, giấy, bút); nền lấy từ `phien-ban-cu/BIEN-THE-TALKA-7-BIEN-THE.json`. Mỗi biến thể đọc 5 từ đầu, các từ còn lại có trên giấy nhưng không đọc |
| `cong-cu/tao-kich-ban.py` | Tạo lại 2 file trên. Muốn sửa prompt thì sửa file này rồi chạy `python cong-cu/tao-kich-ban.py` |
| `PHAN-TICH-VIDEO-MAU.md` | Phân tích video gốc: lời thoại, thời lượng, bố cục |
| `phien-ban-cu/` | Bản đầu (bảng không chữ), giữ tham khảo |
| Hậu kỳ | `app/production/types/talka-bang-tu-vung/` (xem README ở đó) |

## Quy trình đang dùng (đã chốt)

**Muse chỉ gen robot trên nền xanh lục phẳng ở MỌI cảnh** (dạy từ và quảng cáo), một khung hình liên tục, robot đứng giữa khung.
**Hậu kỳ** làm phần còn lại, khớp lời đọc (Whisper):
- **dựng tờ giấy bằng code** (`giay.py`, ảnh tĩnh: checklist, giấy kẻ dòng 2 cột, sổ lò xo; từ + icon lấy từ `HAU_KY.bang` của biến thể), tách nền xanh và ghép robot lên giấy. Giấy do code vẽ nên biết chính xác toạ độ từng từ: không dò, không sai chính tả, bút không lệch hàng;
- **cỡ và vị trí robot chỉnh ở hậu kỳ cho khớp video mẫu** (`config.json` → `bo_cuc`): hậu kỳ đo robot trong video rồi phóng/thu và dời. Cảnh dạy từ: đỉnh đầu 47,5% chiều cao, robot lệch phải (tâm đầu 70%); cảnh quảng cáo: đỉnh đầu 48,5%, robot giữa, đầu chỉ chạm mép dưới bảng;
- **cảnh quảng cáo xếp lớp**: video nền thành phố (hậu kỳ gen bằng AI theo `NEN_PHO`, lưu `nen_pho.mp4` trong thư mục chạy) → ô bảng cố định (như video mẫu: 9–90% bề ngang, 18–51% chiều cao) → robot;
- bút (đỏ mẫu / bút máy / bút bi) nằm **dưới robot** (không che robot), lướt qua đúng chữ robot đang đọc: từ bản ngữ → chữ tiếng Anh → lướt lại khi đọc lại; sang cảnh sau trượt xuống hàng kế tiếp;
- chữ tiếng Anh hiện ra **nguyên chữ** đúng lúc bút đặt vào đầu chữ, nằm trên giấy (sau lưng robot), giữ đến hết phần bảng chữ;
- ô bảng quảng cáo ở 3 cảnh cuối hiện đúng lời robot (như video gốc); **không phụ đề, không logo, không end card**.
- Từ vựng cho bút và lời cho ô bảng **lấy từ chính biến thể** (`bien_the.py` trong thư mục hậu kỳ): biến thể mới không cần sửa code.

Studio tự chọn hậu kỳ này cho loại dự án có tên bắt đầu bằng `KICH-BAN-TALKA` (hoặc file loại có `"post": "talka-bang-tu-vung"`).

### Bố cục
- Robot từ bụng lên, đỉnh đầu ~40% chiều cao khung, tâm đầu ~62% chiều ngang, đầu rộng ~24%.
- Tờ giấy do hậu kỳ dựng (kiểu checklist: tiêu đề ~6%, 8 hàng cách đều ~5% từ ~12% đến ~47%; kiểu giấy kẻ dòng/sổ tay: vạch kẻ hàng 1 ở 18,5%, cách nhau 4,8%) → 5 hàng từ vựng luôn nằm trên đầu robot.

## Những gì đã thử và vì sao bỏ (đừng lặp lại)

| Cách | Kết quả | Lý do bỏ |
|---|---|---|
| Muse tự vẽ tay + bút viết chữ, chỉ chữ | Chữ viết đè hàng khác, sai hàng (nhất là "Thank you"); bút không chỉ vào từ Tây Ban Nha | Model video gộp "chỉ chữ" với "đặt bút viết"; không giữ được chữ viết tay qua nhiều clip nối nhau |
| Video nền tham chiếu (gen nền trước, đưa làm tham chiếu) | Vẫn viết đè hàng | Muse vẽ lại toàn khung, tham chiếu chỉ là gợi ý |
| Ghép 2 lớp (robot phông xanh + nền giấy/bút do **Muse gen riêng**) | Cắt phông tốt, nhưng Muse vẫn viết sai hàng ở lớp nền; robot tự zoom giữa clip | Lớp nền do AI gen nên vẫn sai chữ/hàng. Bản hiện tại khác: giấy do **code vẽ**, chỉ robot do Muse gen |
| Bàn tay/bút vẽ bằng code | Hoạt động nhưng không tự nhiên | Người dùng không chọn |
| Muse cho chữ tiếng Anh tự hiện (viết dần / hiện nguyên chữ) | Chữ hiện quá sớm (ngay trong câu hỏi) | Muse không bám nhịp lời nói |
| Prompt rất dài (~14.000 ký tự/clip) | Robot đọc lẫn "for me" vào câu hỏi | Từ vựng lặp 18 lần; Muse tự tóm tắt prompt làm mất chi tiết → dùng bản gọn (~6.000 ký tự) |

## Lỗi còn có thể gặp (do Muse)
- Robot thỉnh thoảng đọc lẫn từ tiếng Anh vào câu hỏi ("¿Cómo se dice for you…?") → gen lại cảnh đó. Hậu kỳ vẫn hiện chữ đúng lúc "Se dice, …" (lấy lần nói ngay trước "Repite").
- Vài khung lẻ chữ đen trên giấy lốm đốm trắng (model video vẽ lại cả khung + nén mạnh). Thoáng 1–2 khung.
- Nền xanh của Muse không phẳng (gradient, vệt sáng) làm viền robot khuyết hoặc lẫn xanh sau khi tách nền → gen lại cảnh đó. Hậu kỳ lấy màu nền thật từ góc trên và mép trái khung để tách, và bỏ viền xanh ngả vào robot.
- Hậu kỳ không còn đo vị trí chữ trên video (giấy do code dựng nên biết sẵn); chỉ video cũ gen kèm tờ giấy trong Muse mới còn dùng cách đo vòng tròn đỏ.
