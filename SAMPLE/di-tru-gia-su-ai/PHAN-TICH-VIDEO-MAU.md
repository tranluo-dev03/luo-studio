# Phân tích video mẫu: `1410_immigration ES_003 (2) (online-video-cutter.com).mp4`

Công cụ: `video-moi.py danh-gia --lang es` (kết quả trong thư mục tạm `immigration-es-phan-tich/`), đã xem từng `tong-quan_N.jpg` và các `luot_NN.jpg` chính.

## Tổng quan
- 67,1 s, 720×1280, 40 câu, tốc độ nói trung vị **4,3 từ/giây** (câu ngắn tiếng Anh tới 7–10), 15 cảnh cắt cứng (1,9 … 31,9 s).
- Tiếng Tây Ban Nha xen câu tiếng Anh. Quảng cáo app "Talka AI": badge logo góc trên trái suốt video; dòng "POV: ¿Qué harías en una situación como esta?" ở đầu (0–15 s).
- Chuyển động máy: 4,3–8,0 s (máy trôi qua cửa kính căn hộ), 14,9–19,4 s (máy đẩy cận Diego khi robot nhỏ hiện ra). Còn lại đứng yên.
- Giọng (người nói lấy theo hình + phụ đề): Valeria ~230–240 Hz; Diego ~125–150 Hz; cảnh sát ~135–150 Hz (cùng giới với Diego); robot nhỏ ~310–320 Hz; gia sư AI phần 3 ~140–170 Hz (gom tự động lẫn với Diego, không tin cụm).

## Cấu trúc: 3 phần
| Phần | Giây | Hình | Cơ chế Studio |
|---|---|---|---|
| 1. Gọi điện | 0–12,5 | Cắt xen: Valeria trong căn hộ cao tầng (đứng / cận bên cửa sổ) ↔ Diego trước cửa hàng tiện lợi, cầm cà phê. Mỗi khung một người | Cảnh thường, 5 cảnh, mỗi cảnh `Prompt ảnh` mới, refs giữ mặt |
| 2. Cảnh sát | 12,5–31,9 | Cảnh sát nam ~45 tuổi hỏi Diego trên vỉa hè; robot chibi trắng–tím hiện trên vai Diego sửa câu "I am Mexico" | Cảnh thường, 10 cảnh, 3 khung (rộng / cận + robot / rộng + robot) |
| 3. Gia sư AI | 31,9–67,1 | Diego đứng vỉa hè nhìn ống kính; robot trắng hình người trong ô dọc bo góc viền trắng góc trên PHẢI (≈ x 0,615, y 0,012, rộng 0,37, cao 0,32) | Ghép 2 lớp, 13 cảnh, vào bằng nhoè 0,5 s |

## Phụ đề / hiệu ứng
- Phần 1–2: chữ trắng viền đen giữa-dưới (~0,67 chiều cao). Câu sai "I am Mexico." chữ đỏ; câu đúng "I am from Mexico." chữ xanh + ✅.
- Phần 3: chữ vàng viền đen (~0,63 chiều cao) cho cả hai người; câu sai đỏ + viền đỏ nháy quanh khung; 💰 ở "Pero... no tengo dinero".
- Studio: `config.json` → `kieu_theo_phan` (trắng / trắng / vàng), `y_theo_phan` 1300 / 1300 / 1210; `fx`, `icon`, `to`.

## Bảng hành động (gộp theo cảnh Studio)
| Cảnh | Giây gốc | Ai nói | Lời (theo phụ đề) | Người nói làm gì | Người nghe / khác | Camera, khung cuối |
|---|---|---|---|---|---|---|
| P1-1 | 1,7–3,3 | Valeria | No regreses a casa todavía. | đứng phòng khách, khoanh tay trái, áp điện thoại phải, lo | — (Diego ở nơi khác; 0–1,9 s Diego cầm cà phê đi ra cửa hàng, không lời: BỎ) | đứng yên |
| P1-2 | 3,6–4,0 | Diego | ¿Por qué? | đứng trước cửa hàng, áp điện thoại, cầm cốc tay trái, nhíu mày | — | đứng yên |
| P1-3 | 4,9–6,8 | Valeria | Hay agentes de inmigración en la calle. | cận bên cửa sổ, hạ giọng | — | gốc: máy trôi sang cửa kính nhìn xuống phố (BỎ, đứng yên) |
| P1-4 | 8,7–9,9 | Diego | Pero yo no hice nada. | áp điện thoại, thanh minh | — | đứng yên |
| P1-5 | 10,5–12,1 | Valeria | Ya sé. / Tú tranquilo. | cận, trấn an | — | 2 câu → 1 lượt |
| P2-1 | 12,7–14,5 | Cảnh sát | Good morning, sir. Can I ask you a few questions? | bước tới cạnh Diego, lịch sự | Diego cầm cốc, nhìn cảnh sát | khung rộng hai người (gốc: 2 góc) |
| P2-2 | 14,9–15,3 | Cảnh sát | Where are you from? | hỏi | Diego nghe | |
| P2-3 | 15,8–16,3 | Diego | I am Mexico. (đỏ) | ngập ngừng | cảnh sát nghe | gốc: máy đẩy cận |
| P2-4 | 16,7–19,0 | Robot nhỏ | No, debes decir: I am from Mexico. (cụm xanh) | ngồi trên vai, nhìn ống kính, nói vui | Diego nhìn sang phải, im | cận Diego + robot (khung mới) |
| P2-5 | 19,9–21,1 | Diego | I am from Mexico. (xanh ✅) | nói lại tự tin | robot ngồi im | |
| P2-6 | 22,0–23,4 | Cảnh sát | How long have you been living here? | hỏi | | gốc: qua vai Diego → giữ khung rộng + robot |
| P2-7 | 23,8–25,3 | Diego | I've been living here for twelve years. | tự tin | | |
| P2-8 | 25,6–26,7 | Cảnh sát | Your English is really good. | khen, thán phục | Diego cười | |
| P2-9 | 27,3–29,8 | Diego | Thank you. / I used to struggle with English too. | cười tươi | | 2 câu → 1 lượt |
| P2-10 | 30,1–31,5 | Cảnh sát | How did you improve so much? | tò mò | | gốc: cận cảnh sát |
| P3-1…13 | 32,2–66,5 | AI / Diego xen kẽ | ¿Hablas inglés? … Sí. Corrijo tu gramática… | Diego đứng vỉa hè, cầm cốc, tay phải ra hiệu; AI trong ô nghiêng đầu, cười | người nghe miệng khép | máy cầm tay nhẹ; 💰 ở lượt 8; đỏ ở lượt 4 |

Whisper nghe nhầm (sửa theo phụ đề): "No, Devis, just here" → "No, debes decir:"; "no vengo dinero" → "no tengo dinero"; "¿Es un serio?" → "¿Es en serio?"; "Más o menos" ok.

## Video gốc → kịch bản
| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Diego đi ra cửa hàng, không lời (0–1,9 s) | BỎ | cảnh không lời ở đầu |
| Máy trôi qua cửa kính căn hộ (4,3–8 s) | camera đứng yên | 3.5 sổ tay |
| Cảnh sát: 4 góc máy (rộng, qua vai, cận Diego, cận cảnh sát) | 3 khung: rộng / cận + robot / rộng + robot | giảm trôi mặt; cùng giới (2 nam) trong một khung |
| Robot nhỏ ngồi trên vai từ 16 s tới hết phần 2 | có ở cảnh 4–10 phần 2 | rủi ro Muse cho robot nhép |
| Hai câu liền của một người | gộp một lượt (P1-5, P2-1, P2-9) | |
| Badge "Talka AI", dòng "POV…" | không gen | Thương hiệu / chưa làm dòng POV |
| Viền đỏ nháy phần 3, ✅, 💰 | `fx`, `icon` | |
| Phụ đề chia cụm 2–4 từ | phụ đề theo câu | còn khác |
