# Phân tích video mẫu: `0510_cartoon turn car_015_1.mp4`

Công cụ: `video-moi.py danh-gia` (Whisper tiếng Anh) + `phan-tich-video.py --lang es` (Whisper tiếng Tây Ban Nha, vì video song ngữ), xem từng `luot_NN.jpg`, `chuyen-dong_NN.jpg`, `tong-quan_1..4.jpg`.
Kết quả gốc: `C:\Users\ADMIN\Downloads\0510_cartoon turn car_015_1-phan-tich\`.

## Tổng quan
- 95,1 s, 720×1280, hoạt hình 3D kiểu Pixar. Quảng cáo app học tiếng Anh có gia sư AI (end card "AI Learning English – Your AI Tutor", nút Google Play; app trên điện thoại ghi "LangLearn"). Badge app góc trên trái suốt video, sticker tím bay.
- 42–46 câu, tốc độ nói trung vị **4,1 từ/giây** (tối đa 6,7–7,1). Khoảng lặng giữa lượt 0,44 s.
- Cảnh cắt cứng: 16,17 / 21,2 / 22,03 / 23,13 / 27,13 / 39,9 / 49,93 / 89,0 s. Máy quay đứng yên mọi đoạn (rung nhẹ ≤ 5 px ở gara/phòng khách).
- Ngôn ngữ: taxi + gara tiếng Anh (phụ đề ô trắng chữ đen, dòng dịch tiếng Tây Ban Nha vàng nghiêng); phòng khách tiếng Tây Ban Nha (dòng dịch tiếng Anh); phần gia sư AI tiếng Tây Ban Nha xen câu tiếng Anh, phụ đề chữ vàng viền đen, không ô.
- Giọng: A (nam, 105–145 Hz: tài xế, khách, quản lý, Arjun đều nam), B (nữ 220–260 Hz: con gái). Robot AI 160–200 Hz (giọng nữ trầm, hơi máy).

## Cấu trúc
| Đoạn | Giây | Bối cảnh | Cơ chế Studio |
|---|---|---|---|
| 1 | 0–14 | Taxi vàng New York, nhìn qua kính chắn gió: tài xế phải, khách vest ngồi sau trái gọi điện | cảnh thường, góc A (6 cảnh) |
| — | 14–16 | Mờ đen → trong xe, tài xế nhìn điện thoại "NO ENGLISH $0 TIP" | cảnh KHÔNG LỜI (góc P) |
| 2 | 16–27 | Gara taxi: quản lý tóc bạc khen Arjun, trao chìa khoá; cận tay trao khoá; taxi mới; Arjun chế giễu tài xế; cận tài xế buồn | cảnh thường G, J + 3 cảnh KHÔNG LỜI (K, X, T) |
| 3 | 27–50 | Phòng khách: con gái pyjama xanh chấm bi hỏi bố; ngồi xuống cạnh bố; chỉ app trên điện thoại; cận điện thoại robot | cảnh thường L, L2, L3 + 1 cảnh KHÔNG LỜI (PH) |
| 4 | 50–89 | Tài xế toàn khung trong taxi nhìn ống kính, robot trắng trong ô ngang bo góc viền trắng phía trên (x 0,135 · y 0,03 · 0,73 × 0,28) | **PHẦN 2 ghép 2 lớp** |
| 5 | 89–95 | End card app | không gen (Thương hiệu → Outro) |

## Bảng hành động
| # | Giây | Ai nói | Lời (đã đối chiếu phụ đề) | Người nói làm gì | Người nghe | Vật dụng | Ánh mắt / camera | Khung cuối |
|---|---|---|---|---|---|---|---|---|
| 1 | 0–2,4 | khách | Can you take a left on 5th so we can avoid the traffic? | điện thoại áp tai, chồm tới | tài xế nhìn đường | điện thoại khách | khách nhìn gáy tài xế; máy đứng | khách ngồi lại |
| 2 | 3,7–5,4 | tài xế | 5th… sorry. I don't understand. | nhíu mày, lắc đầu | khách cau mày | — | tài xế liếc gương | tài xế lúng túng |
| 3 | 5,7–7,9 | khách | Take the left on… you missed the turn. | chỉ, ngoái nhìn sau (đỉnh chuyển động 6,4–7,4 s) | tài xế lo | — | — | khách bực |
| 4 | 8,2–9,3 | khách | I just told you to take the left. | xoè tay bực | tài xế cúi | — | — | tựa ghế |
| 5 | 10,2–12,3 | khách | Yeah, I'm in a cab. The driver barely speaks English. | quay ra cửa sổ nói điện thoại | tài xế buồn | — | — | — |
| 6 | 12,7–13,9 | khách | I have to repeat everything I say. | thở dài | tài xế mím môi | — | — | — |
| 7 | 13,9–16,1 | (không lời) | — | mờ đen, tài xế ngồi một mình nhìn điện thoại đánh giá tệ (đỉnh 13,6–16,5 s) | — | điện thoại tài xế | góc trong xe | buồn |
| 8 | 16,1–19,9 | quản lý | Arjun, your ratings are the best we've got. Customers love your conversations as well. | cầm bảng kẹp + bút, quay sang Arjun | Arjun cầm biển "4.9 STARS", tài xế cười gượng; đồng nghiệp đứng sau | bảng kẹp, biển | — | — |
| 9 | 20,3–21,2 | quản lý | You get our brand new car. | rút chìa khoá giơ lên | Arjun cười | chìa khoá | — | giơ khoá |
| 10 | 21,2–22,0 | (không lời) | — | cận tay thả khoá vào tay Arjun, đồng nghiệp vỗ tay | — | chìa khoá đổi tay | cận | tay nắm khoá |
| 11 | 22,0–23,1 | (không lời) | — | toàn cảnh taxi mới, mọi người vỗ tay | — | taxi mới | toàn | — |
| 12 | 23–25,3 | Arjun | You want the new car? Learn to talk to the customers first. | cầm khoá, nhếch mép, rồi bỏ đi | tài xế buồn (thấy mặt nghiêng) | chìa khoá | hai người đối mặt | Arjun đi khỏi |
| 13 | 25,4–27,1 | (không lời) | — | cận tài xế buồn, cúi mặt (đỉnh 25,4–27,4 s) | — | — | cận | cúi mặt |
| 14 | 27,5–28,5 | con gái | Papá, ¿qué pasó? | đứng sau cầm cốc, bước tới | bố cúi mặt trên sofa | cốc, sách mở, tách | — | — |
| 15 | 29–29,8 | bố | Nada, hija. | không ngẩng lên | con nhìn | — | — | — |
| 16 | 30,3–32,1 | bố | Hoy otra vez no pude entender a un cliente. | thở dài | con đi tới, ngồi xuống (đỉnh 32–32,8 s) | — | — | con ngồi cạnh |
| 17 | 32,2–33,9 | con gái | Sabes más inglés del que puedes expresar. | ngồi cạnh, cầm cốc, mỉm cười | bố nhìn xuống | cốc | — | — |
| 18 | 34,1–35,7 | con gái | Sólo te falta practicarlo en voz alta. | gật | bố quay sang | — | — | — |
| 19 | 36–36,8 | bố | ¿Con quién estás hablando? | nhíu mày | con nhìn | — | — | — |
| 20 | 37,4–39,4 | con gái | Con mi tutor de inglés con inteligencia artificial. | rút điện thoại, giơ màn hình (đỉnh 37,4–40,1 s) | bố nhìn màn hình | điện thoại xuất hiện | — | giơ điện thoại |
| 21 | 39,9–41 | (xen cận) | — | cận điện thoại app robot, ngón tay chỉ | — | điện thoại | cận | — |
| 22 | 39,9–41,5 | con gái | Es como hablar con un maestro de verdad. | cầm điện thoại | bố nhìn | — | — | — |
| 23 | 41,9–46,1 | con gái | Te corrige mientras hablas y puedes practicar conversaciones para situaciones de la vida real. | chỉ màn hình | bố chăm chú | — | — | — |
| 24 | 46,4–48,3 | bố | Pero las clases de inglés son muy caras. | ngập ngừng | con nhìn | — | — | — |
| 25 | 48,5–49,7 | con gái | No necesitas tomar clases. | cười | bố nhìn | — | — | → cắt sang phần AI |
| 26+ | 49,9–88,9 | tài xế ↔ robot | Más o menos / ¿De dónde eres? Where are you from? / I am Mexico ❌ / Casi. Mejor di: I am from Mexico / I am from Mexico ✅ (viền xanh lá nháy quanh khung) / Siempre me confundo con eso / Para eso estoy yo… / Pero no tengo dinero / ¿Qué? No necesitas dinero… gratis / No es como las otras apps… / ¿Es en serio? / Claro, nada de trampas. Solo práctica real… / ¿Como un tutor real? / Sí. Corrijo tu gramática… / Ok / Muy buena decisión. Vamos a hablar inglés juntos | tài xế hai tay vô lăng nhìn ống kính; robot nói trong ô | — | — | máy đứng | — |

Đỉnh chuyển động 88,75–89,25 s: chuyển sang end card.

## Video gốc → kịch bản
| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Taxi 6 lượt, một góc qua kính chắn gió | Phần 1 cảnh 1–6, góc A, cảnh 2–6 dùng nguyên khung đầu cảnh 1 | Giữ khách NAM (người dùng chốt); rủi ro tài xế nhép theo khách |
| Mờ đen + tài xế nhìn điện thoại "NO ENGLISH $0 TIP" | Cảnh 7 KHÔNG LỜI (P), `Chuyển cảnh: chớp đen 0.4`, `Cắt còn: 3` | Màn hình điện thoại không chữ (chỉ ánh sáng); nỗi buồn bằng nét mặt |
| Gara: quản lý khen + trao khoá | Cảnh 8–9 (G) | Bỏ biển "4.9 STARS · TOP DRIVER" (chữ trong hình) |
| Cận tay trao khoá; taxi mới | Cảnh 10 (K), 11 (X) KHÔNG LỜI | Taxi không chữ "TAXI"/"NYC" |
| Arjun chế giễu, tài xế thấy mặt nghiêng | Cảnh 12 (J): hai người đối mặt như gốc | Rủi ro hai nam cùng lộ mặt (người dùng chấp nhận); bỏ đoạn Arjun bỏ đi |
| Cận tài xế buồn | Cảnh 13 (T) KHÔNG LỜI | |
| Phòng khách rộng, con gái bước tới | Cảnh 14–16 (L) | |
| Con gái đi tới ngồi xuống (trong lượt bố) | Cảnh 17 đổi góc L2 (đã ngồi) | Không giao Muse "vừa đi vừa ngồi" trong một câu |
| Cận điện thoại xen giữa câu "inteligencia artificial" | Cảnh 21 (PH) KHÔNG LỜI sau câu | Màn hình robot, không chữ "LangLearn" |
| Con gái cầm điện thoại giải thích | Cảnh 22–25 (L3) | "Te corrige…" rút gọn 14 → 11 từ |
| Phần AI bắt đầu bằng "Más o menos" (thiếu câu hỏi) | Phần 2 thêm câu mở "¡Hola! ¿Qué tal tu inglés?" | Lời hợp mạch |
| "¿Qué?" | Gộp vào lượt robot "¿Qué? No necesitas dinero…" | |
| "Ok" một từ | "Ok, vamos a intentarlo." | Muse kém với câu 1 từ |
| Viền xanh lá nháy ở "I am from Mexico", ❌ ở "I am Mexico" | `fx: wrong/right`, `icon: x/check` | |
| Badge app, sticker tím bay, end card | Thương hiệu (logo cố định/bay, Outro) | không gen |

## Còn khác video mẫu / chưa làm được
- Dòng dịch kiểu chung (đỏ viền trắng), video mẫu vàng nghiêng.
- Phụ đề phần 1 ô chữ nhật; video mẫu ô bo tròn từng cụm 2–4 từ.
- Không có đồng nghiệp chuyển động/vỗ tay rõ ở cảnh có lời (nền đứng yên).
