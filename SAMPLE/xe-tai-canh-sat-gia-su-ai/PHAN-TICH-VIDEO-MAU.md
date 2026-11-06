# Phân tích video mẫu: cảnh sát chặn xe tải + gia sư AI

Video: `AQPPCRx43iasG5-…LQAw (2) (online-video-cutter.com).mp4` (bản cắt, không có end card). Công cụ: `video-moi.py danh-gia` (05/11/2026).

## Tổng quan

| Mục | Số đo |
|---|---|
| Độ dài, cỡ | 50,0 s, 360×640 (9:16) |
| Lời | 32 câu Whisper → 22 lượt; tốc độ nói trung vị **4,55 từ/giây** (cao nhất 6,8); lặng giữa lượt 0,4 s |
| Cảnh cắt | 1 cảnh cắt cứng 18,43 s (chuyển phần, nhoè ngang 18,0–18,9 s); 1 cắt ẩn ~9,6 s (cảnh sát lùi ra, khung rộng hơn) |
| Máy quay | Phần 1 (0–18,4 s): có chuyển động (cầm tay trôi nhẹ, dịch tổng 302 px); phần 2: đứng yên |
| Mặt | Phần 1: 2 người chung khung (tài xế trái-trên nhỏ, cảnh sát phải); phần 2: ô AI phía trên + tài xế toàn khung |
| Giọng | Tài xế nữ ~200–220 Hz (lên ~290 Hz khi hào hứng, lượt 9–11); cảnh sát nam (cụm A gom lẫn, nghe lại: baritone); AI nữ trẻ ~180–200 Hz, sáng |
| Ngôn ngữ, sản phẩm | Tiếng Anh; app LangLearn (nhắc trong lời). Không popup, không end card trong bản cắt này |

## Cấu trúc phần

| Phần | Giây | Cơ chế | Nội dung |
|---|---|---|---|
| 1 | 0–18,4 | Cảnh thường, 2 người chung khung, 1 góc máy | Cảnh sát (nam, kính râm, áo phản quang) đứng dưới đường hỏi nữ tài xế xe tải nhoài ra cửa sổ cabin xanh sơn cờ Mỹ; đưa giấy tờ; tài xế khoe học 10 phút/ngày với LangLearn, lấy điện thoại |
| 2 | 18,4–50 | Ghép 2 lớp: AI hoạt hình 3D trong ô ngang bo góc viền trắng phía trên (x 0,03, y 0,012, rộng 0,94, cao 0,32), tài xế selfie trong cabin toàn khung | 2 câu sai được sửa, hỏi "who are you", hỏi tiền, tải app |

## Phụ đề / hiệu ứng (hậu kỳ, không gen)

| Phần | Người | Kiểu | Vị trí |
|---|---|---|---|
| 1 | Cảnh sát | chữ trắng, ô đen | tâm y ≈ 0,656 (1260/1920) |
| 1 | Tài xế | chữ đen, ô vàng | như trên |
| 2 | AI | chữ xanh ngọc, ô đen | ngay dưới ô AI, y ≈ 650 |
| 2 | Tài xế | chữ đen, ô trắng | như trên |

Câu sai: từ sai đỏ ("go to", "am very"), ❌ trên ô phụ đề, viền đỏ nháy toàn khung. Câu đúng "I'm going home": "going" xanh, ✅, viền xanh. "moneys": 💲. Vòng sóng âm trắng sau đầu AI nhấp nháy theo tiếng (Studio: tĩnh).

## Bảng hành động

| # | Giây | Ai nói | Từ/giây | Người nói làm gì | Người nghe | Vật dụng | Ánh mắt / camera | Khung cuối |
|---|---|---|---|---|---|---|---|---|
| 1 | 0,0–1,3 | Cảnh sát | 5,4 | Đứng dưới đường, ngẩng nhìn cabin, tay buông | Tài xế tì tay bậu cửa sổ, nhìn xuống | — | Cảnh sát mặt nghiêng trái ngẩng lên; máy trôi nhẹ | Như đầu |
| 2 | 1,7–3,7 | Tài xế | 3,9 | Nhìn xuống, ngập ngừng "uh" | Cảnh sát ngẩng nghe | — | Tài xế nhìn xuống cảnh sát | Tài xế tì tay |
| 3 | 4,2–5,3 | Cảnh sát | 6,0 | Hỏi, nghiêm | Tài xế nghe | — | — | — |
| 4 | 5,7–6,6 | Tài xế | 4,7 | Đáp ngắn | Cảnh sát nghe | — | — | — |
| 5 | 6,9–8,4 | Cảnh sát | 4,7 | Giơ tay phải lên phía cửa sổ (7,1 s, đỉnh chuyển động 7,1–7,25), lòng bàn tay ngửa | Tài xế quay vào lấy giấy (8,35 s thấy tờ giấy) | Giấy tờ xuất hiện trong tay tài xế | Máy trôi | Tay cảnh sát giơ, tài xế cầm giấy |
| 6 | 8,8–9,5 | Tài xế | 6,1 | Đưa giấy xuống cho cảnh sát | Cảnh sát nhận bằng tay phải | Giấy tờ đổi tay | Đỉnh chuyển động 9,4–10,1 s = cắt ẩn | Cảnh sát cầm giấy |
| 7 | 10,1–12,2 | Cảnh sát | 2,4–3,9 | ("Okay. Wow, your English is good.") Lùi ra, cười, quay lại nhìn tài xế | Tài xế cười | Giấy trong tay cảnh sát | Khung rộng hơn sau cắt ẩn | Cảnh sát ngẩng nhìn tài xế |
| 8 | 12,5–14,8 | Tài xế | 3,6 | Hào hứng, tự hào | Cảnh sát nghe | — | — | — |
| 9 | 15,0–18,2 | Tài xế | 2,8–6,4 | "Real conversations…" rồi "Here, let me show you": cầm điện thoại, nhìn màn hình | Cảnh sát cười, lùi nhẹ | Điện thoại xuất hiện | Nhoè ngang 18,0–18,9 s sang phần 2 | Tài xế cầm điện thoại |
| 10 | 18,5–19,2 | AI | 6,3 | Cằm tì tay, hỏi | Tài xế selfie cười | — | AI nhìn ống kính | — |
| 11 | 19,4–20,6 | Tài xế | 3,4 | "I go to home." (sai) | AI nghe | — | Viền đỏ, ❌ | — |
| 12 | 20,9–22,1 | AI | 4,3 | "You mean: I'm going home?" | — | — | — | — |
| 13 | 22,4–24,1 | Tài xế | 2,9 | "Ah, yes. I'm going home." (đúng) | — | — | Viền xanh, ✅ | — |
| 14 | 24,3–25,1 | Tài xế | 5,3 | "I am very hurry." (sai) | — | — | Viền đỏ, ❌ | — |
| 15 | 25,5–27,7 | AI | 6,1 | "I'm in a hurry, is the correct way to say that." | — | — | Không viền xanh | — |
| 16 | 28,0–30,9 | Tài xế | 2,8–5,6 | "Oh, okay. Thank you. Wait. Who are you?" | — | — | — | — |
| 17 | 31,5–36,5 | AI | 4,1–4,7 | "I'm an AI tutor, and I'm here to help you…" | — | — | — | — |
| 18 | 36,9–37,7 | Tài xế | 6,8 | "But I don't have moneys." | — | — | 💲 | — |
| 19 | 38,0–42,4 | AI | 3,2–5,6 | "It's I have no money. But don't worry, LangLearn is a completely free app." | — | — | — | — |
| 20 | 42,8–43,2 | Tài xế | 2,4 | "Seriously?" | — | — | — | — |
| 21 | 43,6–47,3 | AI | 2,7–3,0 | "We can practice English anytime, anywhere. Just download LangLearn." | — | — | — | — |
| 22 | 47,7–49,7 | Tài xế | 3,4–5,9 | "I will download now. Thank you so much." | — | — | — | Hết video |

Whisper đúng lời, chỉ cần ghép câu theo phụ đề: "Okay." + "Wow, your English is good." là một phụ đề; "I'm in a hurry." + "Is the correct way…" là lời AI (phụ đề xanh ngọc). Ngoài cửa sổ cabin phần 2 cây trôi qua (xe đang chạy).

## Video gốc → kịch bản

| Video gốc | Kịch bản Studio | Ghi chú |
|---|---|---|
| Phần 1 máy cầm tay trôi nhẹ + 1 cắt ẩn (khung rộng hơn) | MỘT góc máy đứng yên, 9 cảnh nối khung; cảnh 1 có `Prompt ảnh` | Đơn giản hoá (sổ tay 2.2); mặt giữ ổn định hơn |
| Cảnh sát lùi ra, quay gần như ra camera ở 9,7–10,5 s | Đứng tại chỗ, liếc giấy, cười, ngẩng nhìn tài xế | Đơn giản hoá; tránh người nói quay ra camera |
| "Okay." + "Wow, your English is good." | Một lượt | Cùng người liền nhau |
| "Real conversations…" + "Here, let me show you." | Một lượt, cầm điện thoại ở cụm sau | Cùng người liền nhau, hành động trong lúc nói |
| Xe cộ xa, mây, cây cọ | Đứng yên | Đơn giản hoá |
| Chữ "STATE TROOPER" trên áo, biển số, "WAB" trên cửa | Không chữ (áo phản quang trơn) | Mọi chữ do hậu kỳ |
| Nhoè ngang 0,5 s vào phần 2 | `| vao: nhoe 0.5` | Có sẵn |
| Ô AI bo góc viền trắng | `[GHEP HAI LOP] khung DAY: 0.03, 0.012, 0.94, 0.32`, viền #FFFFFF 3, bo 0.05 | 676×409 px → gen 16:9 |
| Xe đang chạy (cây trôi ngoài cửa) | Xe đỗ, cảnh ngoài đứng yên | Đơn giản hoá (`noi: lien` cần nền ổn định) |
| Selfie tay phải từ góc dưới-trái | `[NHAN VAT HOC]` tả đúng | Khớp |
| Phụ đề 2 kiểu × 2 phần, từ sai/đúng tô màu, ❌ ✅ 💲, viền đỏ/xanh | `config.json` + `to`/`icon`/`fx` | Có sẵn (`_chung/hau_ky.py`) |
| Vòng sóng âm nhấp nháy theo tiếng | Vòng sóng tĩnh trong nền AI (`NEN_DAY`) | Studio chưa làm |
| Phụ đề bo tròn | Ô chữ nhật | Studio chưa làm |
| End card | Không có trong bản cắt; nếu cần: Thương hiệu → Outro | Không gen |

## Rủi ro Muse

- Phần 1 hai người khác giới (an toàn hơn cùng giới). Cảnh sát nhìn nghiêng từ hơi sau lưng: miệng chỉ thấy một bên → có thể Muse cho tài xế nhép lời cảnh sát; nghe kỹ cảnh 1, 3, 5, 7.
- Tài xế nhỏ trong khung (đầu ~11% bề ngang): khẩu hình khó thấy; vị trí `LEFT`/`RIGHT` để Studio đo miệng người nghe theo nửa khung.
- Đưa giấy tờ qua cửa sổ cao (cảnh 5–6): tay có thể xuyên cửa / giấy nhân đôi → xem khung cuối cảnh 5, 6.
- Phần 2 tài xế phải khớp mặt phần 1: cần ảnh tham chiếu `NGUOI_HOC` (ảnh AI người dùng).
