# Phân tích video mẫu: `2310_face to face ES_005_2` (30,2 giây, 720×1280)

Công cụ: `video-moi.py danh-gia --lang es` (kết quả gốc: `Downloads/2310_face to face ES_005_2 (online-video-cutter.com)-phan-tich/`).
Whisper `--lang es` bỏ sót toàn bộ đoạn 7,6–22,9 s (người nói xen tiếng Anh); chạy lại `language=en` + đối chiếu phụ đề trên hình mới đủ lời.

## Tổng quan
- 12 lượt thoại, tốc độ trung vị **3,0 từ/giây** (cao nhất 3,85), khoảng lặng ~0,6 s.
- **1 cảnh cắt cứng ở 7,77 s** (có nhoè chuyển động 7,5–8,0 s) → chia **2 phần**. Camera đứng yên cả hai đoạn (đo OpenCV: tổng dịch 10–13 px trên 160×284).
- Ngôn ngữ: tiếng Tây Ban Nha (Mexico), câu tiếng Anh xen trong phần 2. Không nhạc.
- Logo "Aiva AI" (icon robot + chữ) góc trên trái suốt video → **bỏ** theo yêu cầu người dùng. Không có end card/popup.

## Cấu trúc phần
| Phần | Giây | Bố cục | Cơ chế Studio |
|---|---|---|---|
| 1 | 0–7,77 | Một khung, Machu Picchu hoàng hôn. Robot trắng mép trái (bị mép cắt vai trái), nhìn nghiêng sang phải về phía Carla; Carla nửa phải, eo trở lên, áo khoác vàng mù tạt, tay đút túi, nghiêng ba phần tư nhìn đỉnh Huayna Picchu ở giữa khung | Cảnh thường, 3 cảnh, cảnh 1 có `Prompt ảnh` |
| 2 | 7,77–30,2 | Chia đôi DỌC (vạch giữa, độ nổi 9,7): robot đeo tai nghe nửa trái nền xanh than–tím; Carla ngồi sofa phòng khách, tay phải cầm cốc, nửa phải. Mặt ở x 0,25 và 0,79, y 0,37 | Ghép 2 lớp, `khung HOC: 0.5,0,0.5,1` + `khung DAY: 0,0,0.5,1` (khuôn `chia-doi-gia-su-ai`) |

## Giọng (Hz trung vị, đo lại theo mốc thời gian đã sửa)
- Carla: 180–225 Hz (trung vị ~200), nữ, hơi khàn ấm, Mexico; nói tiếng Anh kiểu người mới học.
- Robot/AI: 147–216 Hz (trung vị ~185), nữ, ấm, hơi "máy". **Hai giọng nữ gần nhau** → rủi ro phần 1 (chung khung).

## Phụ đề và hiệu ứng
| Video gốc | Studio |
|---|---|
| P1: dải mờ xám ngang khung ở y ≈ 0,19; Carla chữ xanh dương, robot chữ vàng, chia cụm 2–4 từ | `y_theo_phan 1: 360`, ô đen theo dòng (không phải dải mờ cả bề ngang), chia theo câu; màu `blue` mới thêm vào `phu_de.py` |
| P2: phụ đề giữa khung y ≈ 0,555, AI vàng, Carla trắng, có viền đen | `y_theo_phan 2: 1065` |
| Câu sai "I have 22" / "I'm Mexico" chữ đỏ + ❌ | `"c": "red", "fx": "wrong", "icon": "x"`; viền đỏ nháy ở nửa phải (video gốc không có viền) |
| Cụm đúng trong lời AI ("I'm 22", "I'm from Mexico") chữ xanh lá trong ngoặc kép | `"to": ..., "to_mau": "green"` |
| Carla nói lại đúng + ✅ | `"fx": "right", "icon": "check"`; cụm tô xanh |
| Nhoè chuyển cảnh 7,5–8,0 s | `| vao: nhoe 0.5` |
| "AI" trên trán robot, icon quyển sách trên ngực | Bỏ (không chữ/icon trong prompt); ảnh tham chiếu đã xoá chữ "AI" |

## Bảng hành động
| # | Giây | Ai nói | Lời (đã sửa theo phụ đề) | Từ/s | Người nói làm gì | Người nghe | Camera / khung cuối |
|---|---|---|---|---|---|---|---|
| 1 | 0,0–2,1 | Carla | ¿Cuál es la primera regla para aprender inglés? | 3,85 | Nhìn đỉnh núi, cười hào hứng, hơi ngẩng | Robot nhìn Carla, im | Đứng yên; Carla vẫn nhìn núi |
| 2 | 2,6–6,4 | Robot | No lo estudies, úsalo. Solo necesitas hablar con un nativo. | 3,0 | Nói, đầu hơi nghiêng về Carla, tay đan trước bụng | Carla nhìn núi, nụ cười tắt thành suy nghĩ | Đứng yên |
| 3 | 7,0–7,3 | Carla | ¿Cómo? | 3,3 | Quay đầu sang trái nhìn robot, nhíu mày | Robot nhìn Carla | Khung cuối: Carla nhìn robot → cắt + nhoè |
| 4 | 7,7–9,0 | AI | How old are you? | — | Nhìn ống kính, cười | Carla nhìn ống kính, cầm cốc | Chia đôi, đứng yên |
| 5 | 9,0–10,4 | Carla | Eh, I have 22. ❌ | — | Ngập ngừng | AI im | |
| 6 | 10,4–12,9 | AI | ¿Quisiste decir, "I'm 22"? | — | Nghiêng đầu, kiên nhẫn | Carla nghe | |
| 7 | 13,0–15,1 | Carla | Ah, sí, es verdad. I'm 22. ✅ | — | Cười, gật | AI im | |
| 8 | 15,2–16,7 | AI | Carla, where are you from? | — | | Carla nghe | |
| 9 | 16,8–18,5 | Carla | I'm Mexico. ❌ | — | Ngập ngừng ("I am... Mexico") | AI im | |
| 10 | 18,6–22,9 | AI | Carla, buen intento, pero tienes que decir, "I'm from Mexico". | — | | Carla nghe | |
| 11 | 23,0–26,0 | Carla | Perdón, siempre me equivoco. I'm from Mexico. ✅ | — | Ngượng rồi tự tin | AI im | |
| 12 | 26,0–29,8 | AI | No pasa nada, vamos a mejorar tu inglés hablando todos los días juntos. | — | Cười ấm | Carla cười tươi cuối clip | Hết video |

Cốc: luôn trong tay phải Carla (bên trái khung của cô), không đổi tay. Không vật nào xuất hiện/biến mất.

## Video gốc → kịch bản
| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Phần 1, 3 lượt, một khung | PHAN 1, 3 CẢNH, cảnh 1 `Prompt ảnh`, cảnh 2–3 nối khung cuối | Giữ nguyên |
| Robot phần 1 (không tai nghe, có ống kính tai) khác robot phần 2 (tai nghe) | Hai khoá: `ROBOT` (phần 1) và `DAY` (phần 2), cùng giọng | `refs` riêng từng khoá |
| Phần 2 chia đôi | `[GHEP HAI LOP]` như `chia-doi-gia-su-ai` | Nhân vật gen 9:16 rồi cắt dải giữa |
| Lời giữ nguyên văn (người dùng yêu cầu "y hệt") | Biến thể 01 | Thêm "Eh," / "Ah," như tiếng ngập ngừng nghe được |
| Logo Aiva AI | Bỏ | Không cài Thương hiệu |
| Dải phụ đề mờ cả bề ngang ở P1, chia cụm từ | Ô đen theo dòng, chia theo câu | **Còn khác video mẫu** |
| "AI" trên trán + icon sách ngực robot | Bỏ | Tránh Muse vẽ chữ |
