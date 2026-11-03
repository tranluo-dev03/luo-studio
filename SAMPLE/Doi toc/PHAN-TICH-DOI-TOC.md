# Thể loại "Đổi tóc + camera dò mặt": phân tích video gốc

Video gốc: `2810_Hair Boy ES_ (online-video-cutter.com).mp4`, dài 11,8 giây, không có cảnh cắt cứng (các lần chuyển cảnh là chớp sáng vàng/trắng).
Giọng đọc tiếng Tây Ban Nha, **lồng tiếng ngoài khung hình** (giọng nam, cao độ trung vị ~117 Hz). Người trong hình không nói câu nào.
Tốc độ nói: **3,0 từ/giây** (cao nhất 3,1). Khoảng lặng giữa các câu: 0,28 giây.
Chữ "DOWNLOAD" chạy khắp video là watermark của trang tải video, không thuộc nội dung.

## Bảng hành động

| Lượt | Giây | Ai nói | Từ/giây | Lời (phụ đề gốc) | Hành động trong hình | Vật dụng | Ánh mắt | Camera | Khung cuối |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,0–2,9 | Giọng đọc ngoài khung | 3,1 | ¿Cómo puedes encontrar el peinado perfecto para ti? | Thợ (tóc đen, râu, áo polo đen) đứng sau, tay phải cầm lược chải phần tóc trên, tay trái giữ đầu khách. Khách tóc đỏ, áo thun xanh navy, ngồi ghế cắt tóc, cười | Lược đen (tay thợ) | Khách nhìn chếch sang trái | Đứng yên, trung cảnh từ ngực lên | Thợ vẫn đang chải |
| (chuyển) | 2,5–3,6 | | | | Chớp sáng vàng, thợ biến mất | | | | |
| 2 | 3,2–6,9 | Giọng đọc ngoài khung | 3,0 | Solo abre la cámara y deja que la IA analice tu rostro. | Khách ngồi một mình nhìn thẳng. Tóc đổi 2 lần, lần nào cũng đổi lúc đầu đang quay sang bên: tóc đỏ gốc → quiff nâu dựng cao (cười) → pompadour nâu sẫm, sườn cạo (nâng cằm) | Không | Nhìn ống kính, quay đầu trái/phải | Đứng yên | Nhìn thẳng, tóc pompadour |
| (chuyển) | 6,8–7,9 | | | | Chớp sáng trắng, tóc về kiểu đỏ gốc, hiện giao diện camera | | | | |
| 3 | 7,2–11,8 | Giọng đọc ngoài khung | 2,6–3,0 | En segundos, te verás con diferentes peinados que realmente te favorecen. | Khách xoay đầu trái, phải, nghiêng nhẹ. Đè lên hình: giao diện camera điện thoại (đèn flash, HDR, lưới 3×3, "1x", hàng chế độ VIDEO/PHOTO/PORTRAIT, nút chụp) và **một hình bầu dục trắng bám theo khuôn mặt** | Không | Nhìn ống kính, xoay đầu | Đứng yên | Mặt hơi nghiêng, giao diện vẫn còn |

Hai khoảnh khắc chuyển động mạnh trong báo cáo (2,5–3,6 giây và 6,8–7,9 giây) đều là chớp sáng chuyển cảnh, không phải hành động.

## Từ video gốc sang kịch bản

| Video gốc | Kịch bản | Đơn giản hoá / ghi chú |
|---|---|---|
| Thợ chải tóc + câu mở đầu | CẢNH 1 (có Prompt ảnh), `LOI_MO` | Giữ nguyên. Thợ chỉ có ở cảnh 1 |
| Chớp sáng vàng | CẢNH 2 `Chuyển cảnh: chớp vàng 0.5` | Studio làm khi ghép clip |
| Tóc đổi lần 1 (quiff) trong lúc quay đầu | CẢNH 2 (Prompt ảnh tóc `TOC_MOI_A`), nửa đầu câu 2 `LOI_CAMERA` | Không bắt Muse biến hình tóc giữa clip (rất dễ hỏng mặt/tóc). Mỗi kiểu tóc là một ảnh khung đầu mới; mặt giữ nhờ ảnh cảnh trước được gửi kèm làm tham chiếu. Khách quay đầu từ bên về giữa, giống lúc "lộ" tóc mới ở video gốc |
| Tóc đổi lần 2 (pompadour) | CẢNH 3 (Prompt ảnh tóc `TOC_MOI_B`), nửa sau câu 2 `LOI_PHAN_TICH` | Câu 2 được tách làm hai để mỗi kiểu tóc có một clip có lời (Studio cắt clip ngay sau từ cuối, nên mỗi clip chỉ còn ~2 giây, đúng nhịp video gốc) |
| Chớp sáng trắng, tóc về kiểu gốc | CẢNH 4 (Prompt ảnh tóc `TOC_GOC`), `Chuyển cảnh: chớp trắng 0.5` | Giữa cảnh 2 và 3 thêm chớp trắng ngắn 0,3 giây để che chỗ đổi ảnh |
| Giao diện camera + hình bầu dục bám mặt | CẢNH 4 `Lớp phủ: camera`; Muse chỉ quay khách xoay đầu chậm | Studio đè giao diện camera chung chung và viền hình trứng bám mặt (mediapipe) khi ghép clip. Giao diện không sao chép giao diện của hãng nào; có thể thay bằng PNG riêng |
| Lồng tiếng ngoài khung | `Voice: (Lồng tiếng ngoài khung hình...)` + `GIONG_DOC`, Prompt video ghi "the off-screen narrator says ... The man never speaks" | Studio không còn tự thêm yêu cầu nhép miệng vào trường Voice |
| Phụ đề trắng giữa màn hình | Hậu kỳ lấy phụ đề từ lời trong ngoặc kép ở `Voice` từng cảnh (vì `LUOT` rỗng) | Lời tiếng Tây Ban Nha: Hậu kỳ tự chọn Whisper `medium` |

Biến thể: 4 bản tiếng Tây Ban Nha (giữ lời gốc, sửa chỗ nhận dạng sai) với 4 kiểu người và bộ tóc khác nhau, 1 bản tiếng Anh.
Mọi biến thể đã kiểm tra bằng code Studio: điền đủ token, 4 cảnh, độ dài clip 5/5/5/8 giây (bản tiếng Anh 5/5/5/6).
