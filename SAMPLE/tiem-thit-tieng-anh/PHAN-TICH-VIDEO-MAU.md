# Phân tích video mẫu: `0610_Cut meat ES_015_02.mp4`

Công cụ: `video-moi.py danh-gia --lang es` + `phan-tich-video.py --lang en` (video song ngữ, ghép hai bản theo giây, đối chiếu phụ đề trên hình).

## Tổng quan
- 177 giây (≈171 s phim + 6 s end card), 9:16, hoạt hình 3D kiểu Pixar. 62 câu Whisper, **28 cảnh cắt cứng**, tốc độ nói trung vị 4,0 từ/giây (cao nhất 5,4); khoảng lặng trung vị 0,58 s, nhiều đoạn không lời dài (cắt thịt 8 s, học đêm, một tháng trôi qua 20 s).
- Mặt: trung vị 1 mặt/khung; chủ yếu cận một người hoặc hai người cùng khung; không có ô PiP/chia khung (những lần "đổi bố cục" công cụ báo là cảnh cắt giữa cận và trung cảnh).
- Chuyển động máy: 4/29 đoạn (đầu video cận dao cắt thịt, bà chủ đi qua chợ, montage học đêm, đoạn cuối) → bỏ, camera đứng yên.
- Giọng: cụm A ~140 Hz (ông chú, khách), cụm B ~229 Hz (bà chủ, Tavo, giọng AI).
- Ngôn ngữ: Tavo và ông chú nói **tiếng Tây Ban Nha** với nhau; khách, bà chủ, giọng AI nói **tiếng Anh**; ông chú nói tiếng Anh (giọng nặng) với khách/bà chủ; cuối phim Tavo nói tiếng Anh. Phụ đề: câu tiếng Anh = dòng trắng đậm + dòng dịch tiếng Tây Ban Nha vàng nghiêng; câu tiếng Tây Ban Nha = một dòng trắng.
- Quảng cáo: app học tiếng Anh có gia sư AI (logo góc trên phải, watermark "Learna AI", màn hình app: robot trắng + bong bóng chat + nút micro). End card 6 s: logo "AI Learning English / Your AI Tutor" + Google Play → **không gen** (Thương hiệu: logo, Outro).
- Dòng "Este anuncio incluye actores generados por IA" ở mép dưới: chữ hậu kỳ của video gốc, không gen.

## Cấu trúc truyện (một phần, nhiều bối cảnh)
| Đoạn | Giây | Bối cảnh | Nội dung |
|---|---|---|---|
| 1 | 0–30 | quầy thịt ban ngày | Tavo cắt thịt; khách khen; ông chú nhận công "20 năm", chê Tavo "không trường, không tiếng Anh", bắt chào, Tavo câm lặng; trả Tavo 2 đồng xu "tiền nước", "trả bằng chỗ ở và cơm" |
| 2 | 30–68 | chợ → phòng sau quầy → quầy cân | bà chủ nhà hàng mất hàng giao, cần gấp; Tavo cắt + gói 4 gói thịt trong 10 phút; bà hỏi tên, Tavo không hiểu; bà mở app trên điện thoại cho cậu, "một tháng nữa tôi quay lại" |
| 3 | 68–116 | đêm, kho tối | Tavo học với robot AI: "You saved me today" = "me salvaste hoy"; rưng rưng; nói được; "Perfect. Again tomorrow?"; montage một tháng (lịch, đánh dấu, cổng gắn, đứng dậy) |
| 4 | 116–171 | quầy thịt, một tháng sau | bà chủ hỏi người cắt thịt; ông chú nhận vơ, chê Tavo; Tavo nói tiếng Anh "It was me…"; bà nhận cậu về làm; "Ahora sí me llamo Tavo, tío"; Tavo nhìn ống kính kêu gọi tải app |
| 5 | 171–177 | — | end card (không gen) |

## Nhân vật (để người dùng gen ảnh tham chiếu)
| Khoá | Nhân vật | Ngoại hình | Giọng |
|---|---|---|---|
| TAVO | cậu bé ~14 tuổi | da nâu, tóc xoăn ngắn, nốt ruồi má trái, áo thun xanh nhạt, tạp dề trắng | teen nam ~200–230 Hz, rụt rè |
| TIO | ông chú chủ quầy ~50 | ria mép rậm, mũ đầu bếp trắng, áo sơ mi caro xanh lá, tạp dề trắng bẩn | nam trầm khàn ~120–140 Hz, khoe khoang |
| KHACH | khách ~35 | tóc đen vuốt ngược, mũi dài, áo polo trắng | nam Mỹ ~130–150 Hz |
| CHU | bà chủ nhà hàng ~40 | tóc nâu búi thấp + kẹp bạc, mắt nâu lục, sơ mi tím mận xắn tay, quần kaki | nữ Mỹ ~200–220 Hz |
| ROBOT | gia sư AI trên màn hình | robot trắng ngọc, mắt xanh nhạt, cổ cơ khí đen, ngực có viền sáng xanh | nữ, hơi tổng hợp |

## Bảng hành động (theo lượt, đã gộp câu liền nhau)
| # | Giây | Ai nói | Lời (đã sửa theo phụ đề) | Hành động / người nghe / vật / ánh mắt / khung cuối |
|---|---|---|---|---|
| 0 | 0–2 | — | (không lời) | cận tay Tavo cắt miếng thịt dày trên thớt (máy hơi đẩy) |
| 1 | 2.3–4.4 | Khách (EN) | Wow. That's a beautiful cut. | khách ở mép phải cúi nhìn; ông chú gãi mũ cười; Tavo cúi thớt |
| 2 | 4.7–6.0 | Ông chú (EN) | Twenty years, my friend! | ông chú xoè tay khoe; khách cười |
| 3 | 6.5–6.9 | Khách (EN) | And the kid? | ông chú nhìn sang Tavo |
| 4 | 7.4–10.4 | Ông chú (EN) | Him? He is nobody. No school, no English. | nhún vai, ngón tay giơ lên; Tavo cúi mặt |
| 5 | 10.9–12.9 | Ông chú (EN) | Watch this. Tavo, say hello. | quay sang Tavo; Tavo ngẩng lên, miệng hé "ô" không ra tiếng (3,4 s im) |
| 6 | 17.0–19.6 | Ông chú (EN) | You see? Nothing. Like talking to a wall. | xoè tay về Tavo; Tavo nhìn thẳng, mắt buồn |
| 7 | 19.6–23 | — | (không lời) | khách quay đi về chợ (cắt sang cận khách đi) |
| 8 | 23.0–25.7 | Ông chú (ES) | Y no le hables a los clientes. Para tu refresco. | cận hai chú cháu; tay ông đặt 2 đồng xu bạc lên thớt cạnh khăn trắng |
| 9 | 26.2–27.9 | Tavo (ES) | Tío, dijo que hoy me pagaba la semana. | Tavo quay sang ông chú |
| 10 | 28.2–29.3 | Ông chú (ES) | Te pago con techo y comida. | ông quay lưng bỏ đi; Tavo nhìn đồng xu |
| 11 | 30–34 | — | (không lời) | bà chủ cầm sổ đi qua chợ, nhìn tủ kính (máy theo) |
| 12 | 34.2–38.0 | Bà chủ (EN) | Please, my meat delivery didn't come. My restaurant opens at seven. Can somebody help me? | phòng sau quầy, tay xoè, cầm sổ; Tavo nghe ở mép phải |
| 13 | 36.7–38.0 | Tavo (ES) | Tranquila. Yo le ayudo. | Tavo giơ tay trấn an |
| 14 | 38.0 | Bà chủ (EN) | I'm sorry. | không hiểu, xua tay |
| 15 | 38.6–40.1 | Tavo (ES) | Aquí. (siéntese, por favor) | chỉ ghế; rồi cầm dao phay chặt thịt |
| 16 | 40–48 | — | (không lời) | montage: chặt, bọc giấy hồng, 4 gói xếp hàng; bà chủ nhìn sững |
| 17 | 48.6–50.8 | Bà chủ (EN) | Oh my God. (Ten minutes?) | nhìn 4 gói thịt |
| 18 | 52.1–54.4 | Bà chủ (EN) | Thank you. Really. What is your name? | quầy cân treo, tì tay lên tủ kính; Tavo mép phải |
| 19 | 56.0–57.4 | Tavo (ES) | Perdón, no entiendo. | ngượng |
| 20 | 59.4–63.1 | Bà chủ (EN) | Here. This app. Learna AI. (bản Studio: "Hey, take this app. Talka AI.") | rút điện thoại, chỉ màn hình (màn hình app chèn 2 s); ghi tên app vào sổ |
| 21 | 64.0–67.7 | Bà chủ (EN) | I come back in one month. One month. | cận, giơ ngón tay, tay kia cầm bút; cận Tavo lo lắng |
| 22 | 69.7–70.4 | Bà chủ (EN) | You saved me today. | ôm gói thịt; quay đi |
| 23 | 72–84 | Tavo (EN) | Yu… tudei… | đêm, cận mặt sáng từ điện thoại; màn hình robot |
| 24 | 84–88 | AI (EN/ES) | You saved me today. It means: me salvaste hoy. | cận cực sát mắt Tavo |
| 25 | 88 | Tavo (ES) | Me salvaste hoy… | rưng rưng, nhìn sang chồng bao gấp |
| 26 | 88–89 | AI (EN) | Try it with me, Tavo. | |
| 27 | 89.8–93.7 | Tavo (EN) | You… saved me… today. | |
| 28 | 93.6–95.8 | AI (EN) | Perfect. Again tomorrow? | Tavo che miệng, mắt ướt |
| 29 | 96–116 | — | (không lời) | montage: cắt thịt đêm nhìn điện thoại, cận mặt ánh lò bánh, sổ lịch đánh dấu, Tavo đứng dậy trong phòng tối |
| 30 | 116–124 | Bà chủ (EN) | Hi. A month ago someone here cut my order. A young guy. Is he still here? | quay lại quầy, cầm sổ; Tavo thấp thoáng sau |
| 31 | 124–128.8 | Ông chú (EN) | Yes, yes, me. I am the master. Twenty years. | chỉ ngực, cười |
| 32 | 130–133.7 | Ông chú (ES) | Tú cállate. Este ni inglés sabe. De este no sale nada. | quay sang Tavo |
| 33 | 134.6–138.8 | Tavo (EN) | Hello. It was me. I cut your order. Ten minutes. | Tavo bước ra; cận ông chú sững sờ |
| 34 | 142–143 | Bà chủ (EN) | You learned English? | hai người đứng nghiêng đối mặt |
| 35 | 143.9–145.5 | Tavo (EN) | One month. Every night. | |
| 36 | 147–152 | Bà chủ (EN) | I own a restaurant. I need a butcher I can talk to. The job is yours. | |
| 37 | 154.5 | Tavo (EN) | You saved me too. | cận Tavo, ông chú mờ sau |
| 38 | 158.9 | Tavo (ES) | Ahora sí me llamo Tavo, tío. | quay đầu qua vai nhìn ông chú |
| 39 | 162.8–170.9 | Tavo (ES) | Un mes. Eso es todo. Yo llegué sin nada y sin inglés. Hoy tengo trabajo. Learna AI. Bájala gratis. | nhìn ống kính, cầm điện thoại có robot cạnh mặt |
| 40 | 171–177 | — | end card + "Thank you/¡Suscríbete!" | không gen |

Whisper nghe nhầm đã sửa: "Eso es un bonito cut" → "That's a beautiful cut"; "Perdona, mi teléfono no salió" → "Please, my meat delivery didn't come"; "Aprenda A.I." → "Learna AI"; "Baja la grata" → "Bájala gratis"; "Tabo" → "Tavo".

## Video gốc → kịch bản (37 cảnh)
| Video gốc | Kịch bản | Ghi chú |
|---|---|---|
| Cận tay cắt thịt mở đầu (0–2 s) | bỏ | cảnh không lời |
| Lượt 1–6 | cảnh 1–5, 7 (góc K cận khách, A quầy rộng, B cận hai chú cháu) | khách chỉ nói ở góc K (một mình); ở góc A khách chỉ là vai + gáy mép phải → không có 2 người lớn nam cùng lộ mặt |
| Tavo hé miệng im lặng 3,4 s | cảnh 6 không lời (góc T, `Cắt còn: 3.5`) | bản 37 cảnh đã gộp, người dùng chê thiếu |
| Khách bỏ đi | bỏ | |
| Lượt 8–10 (2 đồng xu) | cảnh 8–10, nối khung liên tục để đồng xu ở lại trên thớt | |
| Bà chủ đi qua chợ | cảnh 11 không lời (góc X, máy đứng yên, bà đi về phía máy) | |
| Lượt 12–15 | cảnh 12–16 (góc C, D); câu dài tách 2 cảnh; "I'm sorry, I don't speak Spanish." | cảnh 16 vội vã, chộp dao |
| Montage chặt/bọc 8 s | cảnh 17 (D2 chặt nhanh, clip 10 s `Tua: 1.3`) + 18 (Y tay gói, `Tua: 1.3`), rồi W (4 gói xong) cảnh 19 | |
| Màn hình app (bong bóng chat, nút) | không gen giao diện; màn hình điện thoại chỉ là robot (góc P) hoặc ánh sáng | chữ trong hình bị cấm |
| Ghi tên app vào sổ | bỏ | chữ trong hình |
| Bà chủ hôn trán Tavo (trước "You saved me today") | cảnh 24 không lời, cảnh 25 nối khung | |
| Lượt 23–28 (học đêm) | cảnh 26–31: xen kẽ cận Tavo (N) và cận điện thoại robot nói (P) | robot nói trên màn hình để tránh Muse gán giọng AI cho mặt Tavo |
| Montage một tháng (20 s) | cảnh 32–35 không lời (Q1–Q4, chớp trắng, mỗi cảnh 3,5 s): vừa làm vừa học nhiều ngày | không gen chữ (lịch, sổ) |
| Lượt 30–39 | cảnh 36–46 (M, M2, F, G, H) | |
| End card | Thương hiệu → Outro | không gen |
| Phụ đề vàng nghiêng dòng dịch | dòng dịch kiểu chung (đỏ viền trắng) | `phu_de.py` cố định màu dòng dịch; muốn vàng nghiêng phải thêm tuỳ chọn vào code dùng chung |

## Rủi ro Muse
- **Ông chú + Tavo cùng khung (góc A, B, G)**: hai nam, khác hẳn tuổi (50 và 14) → ít rủi ro hơn cặp cùng tuổi nhưng vẫn cần nghe kỹ cảnh 2–9, 34–35 xem người nghe có nhép theo.
- 37 cảnh, 15 góc máy → **bắt buộc ảnh tham chiếu** cho TAVO, TIO, KHACH, CHU (ROBOT dùng `SAMPLE/soi-hanh-ly-gia-su-ai/ROBOT-GIA-SU-AI.png`).
- Robot nói trên màn hình điện thoại (góc P): Muse có thể vẽ giao diện/chữ lên màn hình hoặc không nhép miệng robot → xem `scene22_start.png` và clip cảnh 22 trước khi chạy hết.
- Cảnh 36 Tavo cầm điện thoại có ảnh robot: Muse có thể làm robot trên màn hình nhép miệng theo → nếu xảy ra, đổi thành điện thoại úp/màn hình sáng trơn.
- Ánh sáng đổi giữa ngày/đêm/sáng: Studio cân màu theo cảnh đầu (`color_mode anchor`); xem các cảnh đêm có bị kéo sáng lên không.
