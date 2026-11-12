# Thể loại `phong-van-pho-malayalam`: phỏng vấn đường phố rồi chia trên/dưới + gia sư AI, tiếng Malayalam xen tiếng Anh

Video mẫu `1510_interview street hindi_005 (11).mp4` (76,9 giây, app Aiva AI; tên file ghi "hindi" nhưng lời là Malayalam). Phóng viên đố người bán hàng rong
từ tiếng Anh, cô trả lời trôi chảy và rủ "lại đây tôi chỉ cho", rồi cắt sang khung chia trên/dưới: robot gia sư AI (robot Talka) sửa "I am Kannur" → "I am from Kannur", trả lời
câu hỏi về giá, cách học. Phân tích: [PHAN-TICH-VIDEO-MAU.md](PHAN-TICH-VIDEO-MAU.md).

| Phần | Cảnh | Chế độ | Nội dung |
|---|---|---|---|
| 1. Phỏng vấn | 1–11 | cảnh thường, MỘT góc qua vai, camera đứng yên | Phóng viên (PV) quay lưng mép trái cầm micro; người bán (HOC) sau xe đẩy inox, đeo găng |
| 2. Chia trên/dưới | 12–26 | ghép 2 lớp, cắt cứng khi vào phần | Robot Talka ô trên, người bán selfie ô dưới, nhìn thẳng ống kính |

| File | Nội dung |
|---|---|
| `KICH-BAN-PHONG-VAN-PHO-MALAYALAM.txt` | Kịch bản 2 phần, sinh bằng `cong-cu/tao_kich_ban.py` |
| `BIEN-THE-PHONG-VAN-PHO-MALAYALAM.json` | Biến thể, sinh bằng `cong-cu/tao_bien_the.py` (không sửa tay JSON) |
| `PHAN-TICH-VIDEO-MAU.md` | Số đo, bảng hành động, bảng "video gốc → kịch bản" |
| `PROMPT-CHO-AGENT.txt` | Quy tắc viết thêm biến thể |
| `anh/robot-talka.png` | Robot Talka (ảnh người dùng, cùng robot `xe-tai-canh-sat-gia-su-ai`), theo yêu cầu thay robot của video mẫu |
| `anh/phong-vien.png`, `anh/nguoi-ban.png` | Muse gen theo mô tả (`cong-cu/gen_anh_tham_chieu.py`), theo yêu cầu người dùng |
| `anh/khung-phan1-mau.png`, `anh/khung-phan2-mau.png` | Khung video mẫu để so bố cục, KHÔNG gửi cho Muse |

Code riêng: `app/production/types/phong-van-pho-malayalam/` (`gen.py`, `post.py`, `config.json`), chép từ `chia-tren-duoi-bengali`.

## Quyết định đã chốt (11/11/2026)

- Khuôn: nhiều phần, đổi cơ chế ở 25,7 s (chung khung → hai ô). Mẫu dùng lại: `chia-tren-duoi-bengali` (phần 2, gen.py/post.py), `check-hanh-ly-hindi` (bảng cảnh phần 1 một góc).
- Phần 1 giữ MỘT góc, bỏ 2 cảnh chèn cận người bán. Phóng viên khai `QUAY_LUNG_PV` + tả góc bằng hình học + `NHIN_/NGHE_` (sổ tay 3.3).
- Cặp phần 1 khác giới (PV nam, người bán nữ): an toàn hơn cho Muse.
- `nen: DAY`, `khung DAY: 0, 0, 1, 0.5`, `khung HOC: 0, 0.5, 1, 0.5` (video mẫu: 0–622 / vạch cam 622–654 / 654–1280). Cả hai gen 1:1.
- Lời chép từ phụ đề trên hình. Tốc độ ghi "about 2.5 words per second". `fx: none` mọi lượt (video không có ❌/✅).
- Hậu kỳ: font Nirmala UI, `shaping: complex`, chữ đen ô trắng, tâm y 960 (giữa khung) ở cả hai phần, cỡ 52.
- "Kannur" viết chữ Latin trong câu tiếng Anh để Muse đọc đúng; phụ đề video mẫu viết chữ Malayalam.

## Code chung đã sửa (11/11/2026)

- `app/luo-studio/engine.py`: `speech_lang` trả `ml` khi câu có chữ Malayalam; `voice_span` lấy mốc lời theo năng lượng âm thanh (như Bengali); `speech_issues`
  bỏ kiểm từng chữ cho câu Malayalam. Chỉ ảnh hưởng câu có chữ Malayalam.
- `app/production/gen_video.py`: `spoken_syllables` đếm âm tiết chữ Malayalam (trước đây = 0 → clip luôn 5 s, câu dài bị cụt).
- `app/production/postprocess.py`: `align_by_scene` bỏ Whisper cho câu Malayalam như Bengali (Whisper "small" treo >20 phút ở hậu kỳ), phụ đề rải theo độ dài chữ.

## Chạy trong Studio

```
runtime\python.exe SAMPLE\_chung\video-moi.py nhap SAMPLE\phong-van-pho-malayalam\KICH-BAN-PHONG-VAN-PHO-MALAYALAM.txt SAMPLE\phong-van-pho-malayalam\BIEN-THE-PHONG-VAN-PHO-MALAYALAM.json --ten-loai "Phong van pho Malayalam" --ten-du-an "Interview street Malayalam - Talka" --chay-thu
```

Đổi ảnh: chạy lại `cong-cu/gen_anh_tham_chieu.py [PV HOC]` rồi `cong-cu/tao_bien_the.py`.
Sau cảnh 1: xem `phan1/scene1_start.png` (phóng viên quay lưng, không lộ mặt; người bán ba phần tư), nghe cảnh 1–3 (Muse nói Malayalam đúng không,
người bán có nhép theo phóng viên không), rồi `phan2/base_DAY.png`, `phan2/base_HOC.png`.

## Đã kiểm tra / chưa kiểm tra

- `video-moi.py kiem-tra --tai-anh`: 0 lỗi, 0 cảnh báo (11/11/2026).
- Chưa chạy trên Muse.

## Rủi ro

- **Muse nói Malayalam: chưa kiểm chứng.** Câu Malayalam không được kiểm lời từng chữ (cắt sát theo năng lượng âm thanh): phải nghe tay.
- Phóng viên quay lưng là người nói: Muse có thể xoay mặt anh ra camera, hoặc người bán nhép theo giọng anh. Xem kỹ cảnh 1, 3, 5, 9.
- Câu một từ ("Suddenly.") rất ngắn: Muse có thể nói thêm chữ hoặc kéo dài.
- Robot có thêm tai nghe (video mẫu có) trong khi ảnh tham chiếu không có: Muse có thể bỏ tai nghe.
- Người bán trong ảnh tham chiếu trông ~55 tuổi (mô tả đã sửa theo ảnh).

## Còn khác video mẫu

- Bỏ 2 cảnh chèn cận mặt người bán và rung cầm tay cuối phần 1.
- Không có vạch cam giữa hai ô; không chữ "AI" trên trán robot.
- Phụ đề theo câu, không theo cụm 1–3 từ.
- "ba tháng" → "một tháng" ở lời người bán.
- Robot Talka (trắng, mặt người, viền xanh) thay robot Aiva đeo tai nghe chữ "AI" của video mẫu.

## Nhật ký chạy

- 11/11/2026: gen ảnh tham chiếu PV + người bán (Muse, từ chữ): đúng ngoại hình, không chữ. Nhập Studio: loại "Phong van pho Malayalam" (`Phong-van-pho-Malayalam-9ba6`), dự án "Interview street Malayalam - Talka" (`Interview-street-Malayalam---Talka-d5f1`), chạy thử biến thể 01 (hàng đợi `96c45565`).
- 11/11/2026: 26 cảnh gen xong 15:18. Phần 1: PV luôn quay lưng, mặt người bán giữ, giọng không nhầm. Lỗi: câu Malayalam không cắt sát (Studio chạy code cũ), cảnh 11 cụt câu,
  hậu kỳ treo ở Whisper 25 phút. Sửa 3 chỗ code chung (xem trên), cắt lại cảnh 1,3,5,7,9, gen lại cảnh 11, chạy lại hậu kỳ.
- 11/11/2026 (góp ý người dùng): gen lại cảnh 2–11 nối khung tuần tự (hết giật); phụ đề phần 1 ở đáy (y 1560), phần 2 cụm ≤ 3 từ (`cum_tu_theo_phan`);
  nén khoảng lặng bằng `cong-cu/nen_khoang_lang.py` (tua nhanh, giữ khung nối). Bản xuất 105 s (trước 138 s).
- 11/11/2026: người dùng cấm tua nhanh → bỏ bản tua; gen.py cắt sát theo lời (mốc theo năng lượng mọi câu, speedfix tắt, cut_margin 0,3); gen lại 4–11 rồi 9–11.
  Bản xuất 116 s (phần 1 35 s), không tua nhanh. Còn: 10→11 đổi cỡ cảnh nhẹ; 2→3, 15→16, 22→23 lệch khung nhẹ do cắt lại.

## 40 biến thể theo bảng người dùng (12/11/2026)

- Nguồn: `40 biến thể interview - Sheet1.csv` (cột: kiểu, mô tả nhân vật, mô tả bối cảnh, link Drive ảnh nhân vật, link Drive ảnh bối cảnh).
  10 nam trẻ, 10 nữ trẻ, 10 nam già, 10 nữ già; mỗi người một nghề + quầy hàng đúng nghề.
- Ảnh tải về `anh/bt40/nv<NN>.jpg` (nhân vật phông xanh, toàn thân) và `anh/bt40/nen<NN>.jpg` (bối cảnh không người); webp → jpg.
- `cong-cu/tao_40_bien_the.py` → `BIEN-THE-40-PHONG-VAN-PHO-MALAYALAM.json`. Giữ lời thoại, phóng viên, robot, góc máy; đổi người bán (`NGUOI_HOC`,
  `GIONG_HOC` theo giới/tuổi, đại từ `SHE_/HER_/HERO_/SELF_HOC`), quầy (`DAO_XE`), động tác tay theo nghề (`VIEC_HOC`, `VIEC2_HOC`, `TAY_HOC`), găng (chỉ nghề đồ ăn chiên),
  nền (`NEN_PHO`, `NEN_HOC`). refs: `NGUOI_HOC` = ảnh nhân vật, `NEN_PHO` + `NEN_HOC` = ảnh bối cảnh.
- Kịch bản đổi sang token (không còn ghi cứng "woman / gloved / pots / cart"); biến thể 01 điền token như cũ. Vì kịch bản có token mới nên dùng
  LOẠI DỰ ÁN MỚI "Phong van pho Malayalam - 40 nghe" (loại cũ giữ cho dự án cũ).
- Rủi ro: 20 biến thể người bán NAM đứng cùng khung với phóng viên NAM (quay lưng): Muse có thể cho người bán nhép theo lời phóng viên.
  Đã làm giọng người bán nam trầm hẳn (100-135 Hz) so với phóng viên (150-180 Hz). Chạy thử một biến thể nam trước khi chạy cả nhóm.
- Ảnh bối cảnh có biển hiệu chữ Malayalam đọc được: prompt ghi làm mờ, Muse vẫn có thể vẽ lại chữ.
- Đã nhập Studio (12/11/2026): loại `Phong-van-pho-Malayalam---40-nghe-5f1f`, dự án "Interview street Malayalam - 40 bien the" (`Interview-street-Malayalam---40-bien-the-375b`), 40/40 biến thể đủ ảnh. Chưa gen.
- 12/11/2026: người bán nam (bt01-10, bt21-30) → phóng viên NỮ (`anh/phong-vien-nu.png`, `PV_NU` trong tao_40_bien_the.py), gen lại 20 biến thể. Người bán nữ giữ phóng viên nam. Quy tắc: PV và người bán luôn khác giới.
