# Thể loại `di-tru-aiva-ai`: cuộc gọi báo động → cảnh sát hỏi → gia sư AI Aiva (tiếng Tây Ban Nha xen tiếng Anh)

Nhân bản từ `di-tru-gia-su-ai` (08/11/2026) theo file `oder 7 - Sheet1.csv` của người dùng: kịch bản 5 phần (gọi điện, cảnh sát, demo gia sư AI, pain point, CTA) + **20 biến thể nhân vật hành khách** (chỉ đổi hành khách; cảnh sát và gia sư AI giữ nguyên).
Code riêng: `app/production/types/di-tru-aiva-ai/` (`gen.py`, `post.py`, `config.json` giống `di-tru-gia-su-ai`), dùng chung `types/_chung/`.

## Dạng video: MỘT dự án, BA phần (30 cảnh)
| Phần | Cảnh | Chế độ | Nội dung (CSV) |
|---|---|---|---|
| 1. Gọi điện | 1–5 | cảnh thường, mỗi cảnh một người, `Prompt ảnh` mới | Người gọi (`BO`) báo hành khách (`HOC`) đừng về nhà: có agentes de inmigración |
| 2. Cảnh sát | 6–15 | cảnh thường, MỘT góc rộng (cảnh 1 ảnh mới, sau nối khung) | Cảnh sát hỏi; hành khách kể học bằng Aiva AI 10 phút/ngày |
| 3. Gia sư AI | 16–30 | ghép 2 lớp, ô AI dọc góc trên phải `0.615, 0.012, 0.37, 0.32`; vào bằng nhoè | CSV phần 3–5: sửa "I am Mexico", "no tengo dinero" 💲, giới thiệu, tải app |

## Đã đổi so với `di-tru-gia-su-ai`
| Mục | di-tru-gia-su-ai | di-tru-aiva-ai |
|---|---|---|
| Người gọi | bạn gái Valeria | bố ("Mija/Mijo"); hành khách ≥ 60 tuổi thì **con trai** ("Mamá/Papá") vì bố ~90 tuổi không hợp |
| Phần 2 | 3 khung + robot nhỏ trên vai sửa câu | 1 góc rộng, **không robot** (CSV không có) |
| Phần 3 | 13 lượt, kết ở "con confianza" | 15 lượt, thêm "gratis", CTA tải Aiva AI, "Vamos a hablar inglés juntos" |
| Hành khách | Diego, nam 20 | 20 biến thể: 10 trẻ / 10 già, 10 nữ / 10 nam; đại từ bằng token `HE_HOC` / `HIM_HOC`, vai `VAI_HOC` |
| Tên app | Talka (chỉ badge) | `APP = "Aiva AI"` trong `tao_bien_the.py` |

Gộp lượt so với CSV (cùng người nói liền nhau): "Aiva AI… a day." + "That's it." ; "¿De dónde eres?" + "Where are you from?" ; 3 câu "Que no necesitas dinero…/gratis/cursos caros" (20 từ) ; "Claro…" + "Solo práctica…" ; "Muy buena decisión." + "Vamos…". "¿Sí? Corrijo…" viết thành "Sí. Corrijo…".

## File
| File | Dùng làm gì |
|---|---|
| `KICH-BAN-DI-TRU-AIVA-AI.txt` | Kịch bản (sinh bằng `cong-cu/tao_kich_ban.py`) |
| `BIEN-THE-DI-TRU-AIVA-AI.json` | 20 biến thể `hk-01…hk-20` (sinh bằng `cong-cu/tao_bien_the.py`, bảng `HANH_KHACH` theo CSV) |
| `anh/hk-NN.png` | Ảnh hành khách người dùng đưa (Drive link trong CSV), phông xanh lá. `ai-canhsat.png`, `ai-day.png`: chép từ `di-tru-gia-su-ai` |

## Trạng thái (08/11/2026)
- `kiem-tra`: 0 lỗi; cảnh báo giữ: `fx 19:wrong` (CSV: AI sửa nhưng hành khách không nói lại câu đúng), "[NHAN VAT HOC] chưa nói đầu dưới ô" (đầu ở trái, ô AI chỉ ở 38% bên phải; như thể loại gốc).
- Ảnh hành khách: 18/20 tải được (Drive, WebP 1152×2048 → `anh/hk-NN.png`), đã xem: đúng thứ tự và mô tả CSV, phông xanh lá, đứng toàn thân.
  **hk-04 (nữ trẻ bảo mẫu) và hk-16 (nam già xây dựng) vẫn bị Drive chặn quyền** → `tao_bien_the.py` tự BỎ QUA biến thể thiếu ảnh hành khách. Có ảnh thì lưu `anh/hk-04.png`, `anh/hk-16.png`, chạy lại `tao_bien_the.py` và thêm vào dự án.
- Studio: loại `di-tru-aiva-ai-37c0`, dự án `di-tru-aiva-ai-c663` (18 biến thể), CHƯA gen.
- Người gọi (`BO`) không có ảnh tham chiếu → mặt có thể khác giữa cảnh 1, 3, 5.

## Chạy
```
.venv\Scripts\python.exe SAMPLE\di-tru-aiva-ai\cong-cu\tao_bien_the.py
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py kiem-tra SAMPLE\di-tru-aiva-ai\KICH-BAN-DI-TRU-AIVA-AI.txt SAMPLE\di-tru-aiva-ai\BIEN-THE-DI-TRU-AIVA-AI.json --tai-anh
.venv\Scripts\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\di-tru-aiva-ai\KICH-BAN-DI-TRU-AIVA-AI.txt SAMPLE\di-tru-aiva-ai\BIEN-THE-DI-TRU-AIVA-AI.json --ten-loai "di-tru-aiva-ai" --ten-du-an "di-tru-aiva-ai"
```

## Rủi ro
- Hành khách nam trẻ + cảnh sát nam cùng khung ở phần 2: Muse có thể gán nhầm giọng → nghe cảnh 6–15.
- Ảnh tham chiếu phông xanh lá: kịch bản đã dặn bỏ nền ảnh; nếu nền xanh lọt vào khung thì gen lại.
- Phần 3 thể loại gốc từng bị mặt người học trôi vào ô AI do bước khoá camera của `split.py` (chưa sửa code chung).
