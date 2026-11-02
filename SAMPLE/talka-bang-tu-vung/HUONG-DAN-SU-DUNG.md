# Hướng dẫn: làm video "Talka bảng từ vựng" và tạo biến thể mới

Video: robot AI dạy cách nói từ Tây Ban Nha bằng tiếng Anh trước một tờ giấy "¿CÓMO SE DICE?". Bút đỏ lướt qua đúng chữ robot đang đọc, chữ tiếng Anh hiện ra khi đọc. Phần cuối là quảng cáo app trên nền thành phố, có ô bảng hiện lời robot. Video khoảng 60–70 giây, 9 cảnh.

**Muse chỉ gen robot nói trước tờ giấy trống.** Bút đỏ, chữ tiếng Anh, ô bảng quảng cáo, logo và end card đều do **Hậu kỳ** làm tự động, lấy nội dung từ file biến thể.

---

## 1. Làm video lần đầu

1. **Nhập kịch bản** (chỉ làm một lần): tab **Loại dự án** → **Loại mới** → chọn `SAMPLE\talka-bang-tu-vung\KICH-BAN-TALKA-CO-CHU.txt`.
   Tên loại bắt đầu bằng `KICH-BAN-TALKA` thì Studio tự dùng hậu kỳ riêng của thể loại này.
2. **Tạo dự án**: **Dự án mới** → chọn loại vừa nhập → chọn file biến thể `SAMPLE\talka-bang-tu-vung\BIEN-THE-TALKA-CO-CHU.json` (hoặc file biến thể mới, xem phần 2).
3. **Gen**: bấm chạy. Mỗi cảnh mất vài phút. Xem nhanh từng cảnh:
   - tờ giấy phải **trống** ở các vạch xám (không có chữ tiếng Anh, không có tay, không có bút);
   - robot đọc **đúng lời**. Lỗi hay gặp: đọc lẫn từ tiếng Anh vào câu hỏi, ví dụ "¿Cómo se dice **please**?". Gặp thì bấm **gen lại cảnh đó**, và cả cảnh ngay sau nó để hai cảnh nối khớp.
4. **Hậu kỳ**: bấm Hậu kỳ. Studio tự thêm bút đỏ, chữ tiếng Anh, ô bảng quảng cáo, logo, end card. Không có phụ đề.

---

## 2. Tạo biến thể mới (nhờ AI viết)

Một biến thể là một video: bộ từ vựng, ngoại hình và giọng robot, nền, lời quảng cáo, tên app. **Không cần sửa kịch bản hay code.** Chỉ cần một file `.json` biến thể mới.

### Cách làm
1. Mở Claude (hoặc ChatGPT), **đính kèm** file `BIEN-THE-TALKA-CO-CHU.json`.
2. Dán prompt mẫu ở dưới, sửa phần **[YÊU CẦU]**.
3. Lưu kết quả AI trả về thành file `.json`, ví dụ `BIEN-THE-TALKA-MOI.json`.
4. Kiểm tra theo **mục 3**, rồi tạo dự án mới bằng file đó, hoặc trong dự án bấm **Từ file**.
5. Chạy thử **một** biến thể trước khi chạy nhiều.

### Prompt mẫu (copy nguyên văn, sửa phần [YÊU CẦU])

```
File đính kèm là file biến thể (JSON) cho video "Talka bảng từ vựng" của LUO Studio.
Hãy viết [SỐ LƯỢNG] biến thể MỚI, trả về MỘT mảng JSON hợp lệ, cùng cấu trúc, cùng tên khoá như file mẫu.

[YÊU CẦU]
- Từ vựng: 5 từ/cụm tiếng Tây Ban Nha mới và cách nói tiếng Anh, chủ đề: [ví dụ: chào hỏi / đồ ăn / du lịch]
- Tên app: [Talka]   (đọc là: [TAWK-ah])
- Ngoại hình robot / nhân vật: [giữ nguyên như mẫu | mô tả mới]
- Giọng: [giữ nguyên | mô tả mới]

QUY TẮC BẮT BUỘC (phần mềm tự đọc các câu này để làm bút chỉ và ô bảng, sai mẫu là hậu kỳ sai):
1. "name": tên ngắn, không dấu, không trùng (ví dụ "talka-chao-hoi-1").
2. "LUOT" có ĐÚNG 9 lượt, mỗi lượt {"who": "day", "text": ..., "emo": ..., "fx": "none"}:
   - Lượt 1, 2, 3, 5, 6 là 5 từ vựng, ĐÚNG mẫu câu:
     "¿Cómo se dice <từ Tây Ban Nha>? Se dice, <tiếng Anh>. Repite conmigo. <tiếng Anh>."
     (lượt 1 được thêm "en inglés" sau từ Tây Ban Nha, như file mẫu). Tiếng Anh ở hai chỗ phải giống hệt nhau.
   - Lượt 4: một câu động viên ngắn tiếng Tây Ban Nha (không theo mẫu trên).
   - Lượt 7, 8, 9: lời quảng cáo tiếng Tây Ban Nha. Lượt 8 phải có "Descarga <Tên app>".
     Số + thời gian viết bằng chữ, ví dụ "cuatro semanas" (phần mềm tự hiện thành "4 semanas" và tô đỏ).
     Có thể kết thúc lượt 9 bằng câu tiếng Anh ngắn như "Best Language Learning App. Download now."
   - Mỗi lượt đọc được trong khoảng 6–8 giây (khoảng 15–25 từ).
3. "NEN_BANG": giữ nguyên toàn bộ mô tả tờ giấy, CHỈ thay danh sách 8 từ trong ngoặc kép:
   5 từ đầu = đúng 5 từ Tây Ban Nha của lượt 1, 2, 3, 5, 6, ĐÚNG THỨ TỰ và đúng chính tả (có dấu, có ¡ ! nếu có);
   3 từ sau = 3 từ Tây Ban Nha cùng chủ đề (không dùng tới).
   Mỗi từ ngắn (tối đa khoảng 12 ký tự) để vừa nửa trái tờ giấy.
4. "PHAT_AM": nếu đổi tên app, viết lại hướng dẫn phát âm tên app theo cùng kiểu (ví dụ "TAWK-ah").
5. Giữ nguyên các khoá khác (POS_DAY, BOX_DAY, VAI_DAY, DAO_NGHI, NEN_PHO...) trừ khi tôi yêu cầu đổi.
6. Không thêm khoá mới, không bỏ khoá. Chỉ trả về JSON, không giải thích.
```

---

## 3. Kiểm tra file biến thể trước khi gen

- [ ] Có đúng **9** lượt trong `LUOT`.
- [ ] Lượt 1, 2, 3, 5, 6 đúng mẫu `¿Cómo se dice X? Se dice, Y. Repite conmigo. Y.` (Y giống nhau ở hai chỗ).
- [ ] 5 từ đầu trong `NEN_BANG` **trùng y hệt và đúng thứ tự** với X của 5 lượt đó. Từ trên giấy phải khớp lời đọc, vì bút tìm hàng theo thứ tự.
- [ ] Lượt 8 có "Descarga <Tên app>".
- [ ] Nếu đổi tên app: `PHAT_AM` đã sửa theo tên mới.

Kiểm tra nhanh bằng máy (từ thư mục gốc LUO Studio):

```
runtime\python.exe -c "import json,sys;sys.path.insert(0,r'app\production\types\talka-bang-tu-vung');import bien_the as B;v=json.load(open(r'DUONG-DAN\BIEN-THE-MOI.json',encoding='utf-8'));[print(x['name'],[(i['es'],i['en']) for i in B.vocab_items(x['LUOT'])],B.brand_of(x['LUOT'])) for x in v]"
```

Mỗi biến thể phải in ra **5 cặp từ** và **tên app**. Thiếu cặp nào thì câu ở lượt đó sai mẫu.

---

## 4. Lỗi thường gặp

| Hiện tượng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Robot đọc lẫn từ tiếng Anh vào câu hỏi | Lỗi ngẫu nhiên của Muse | Gen lại cảnh đó và cảnh ngay sau |
| Tờ giấy có chữ tiếng Anh / tay / bút | Muse làm sai kịch bản | Gen lại cảnh đó |
| Bút chỉ sai hàng | 5 từ đầu trong `NEN_BANG` không khớp thứ tự với lời đọc | Sửa biến thể, gen lại |
| Chữ đen trên giấy chớp trắng 1–2 khung | Model video vẽ lại cả khung + nén | Thường bỏ qua được |
| Ô bảng quảng cáo thiếu chữ đỏ | Không có "Descarga <Tên app>" hoặc số + thời gian | Sửa câu trong lượt 7–9 |

---

## 5. Muốn chỉnh sâu hơn

- Kiểu ô bảng quảng cáo (vị trí, màu, cỡ chữ), lượt bắt đầu quảng cáo (`ad_from`), từ luôn tô đỏ (`red_words`): `app\production\types\talka-bang-tu-vung\config.json`.
- Câu chữ prompt của kịch bản: sửa `cong-cu\tao-kich-ban.py` rồi chạy lại để tạo `KICH-BAN-TALKA-CO-CHU.txt`, sau đó nhập lại kịch bản vào Studio.
- Lịch sử các cách đã thử và vì sao chọn cách hiện tại: `README.md` trong thư mục này.
