# Hướng dẫn: làm video "Talka bảng từ vựng" và tạo biến thể mới

Video: robot AI dạy cách nói từ Tây Ban Nha bằng tiếng Anh trước một tờ giấy "¿CÓMO SE DICE?". Bút đỏ lướt qua đúng chữ robot đang đọc, chữ tiếng Anh hiện ra khi đọc. Phần cuối là quảng cáo app trên nền thành phố, có ô bảng hiện lời robot. Video khoảng 60–70 giây, 9 cảnh.

**Muse chỉ gen robot trên nền xanh lục phẳng ở mọi cảnh.** **Hậu kỳ** tự dựng tờ giấy (ảnh tĩnh, vẽ bằng code từ file biến thể), viết chữ tiếng Anh, vẽ bút chỉ đúng từ; ở phần quảng cáo tự gen video nền thành phố bằng AI (theo ô `NEN_PHO`) và đặt ô bảng lên; cuối cùng tách nền xanh, đặt robot lên trên cùng với cỡ và vị trí như video mẫu. Vì giấy do hậu kỳ dựng nên chữ luôn đúng chính tả và bút luôn chỉ đúng hàng.

---

## 1. Làm video lần đầu

1. **Nhập kịch bản** (chỉ làm một lần): tab **Loại dự án** → **Loại mới** → chọn `SAMPLE\talka-bang-tu-vung\KICH-BAN-TALKA-CO-CHU.txt`.
   Tên loại bắt đầu bằng `KICH-BAN-TALKA` thì Studio tự dùng hậu kỳ riêng của thể loại này.
2. **Tạo dự án**: **Dự án mới** → chọn loại vừa nhập → chọn file biến thể `SAMPLE\talka-bang-tu-vung\BIEN-THE-TALKA-CO-CHU.json` (hoặc file biến thể mới, xem phần 2).
3. **Gen**: bấm chạy. Mỗi cảnh mất vài phút. Xem nhanh từng cảnh:
   - cả 9 cảnh: phía sau robot chỉ là **một màu xanh lục phẳng** (không giấy, không thành phố, không chữ, không tay, không bút). Nền xanh không phẳng hoặc có vật lạ thì gen lại cảnh đó;
   - robot đọc **đúng lời**. Lỗi hay gặp: đọc lẫn từ tiếng Anh vào câu hỏi, ví dụ "¿Cómo se dice **please**?". Gặp thì bấm **gen lại cảnh đó**, và cả cảnh ngay sau nó để hai cảnh nối khớp.
4. **Hậu kỳ**: bấm Hậu kỳ. Studio tự thêm tờ giấy, bút đỏ, chữ tiếng Anh, video nền thành phố (lần đầu mất thêm vài phút để gen, lưu `nen_pho.mp4` trong thư mục chạy) và ô bảng quảng cáo. Không có phụ đề, logo hay end card.

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
3. "HAU_KY"."bang"."hang": danh sách ĐÚNG 8 từ trên tờ giấy (mỗi phần tử {"tu": từ, "icon": ký tự biểu tượng}; giữ nguyên "giay", "tieu_de", "dau_trai", "but"):
   5 từ đầu = đúng 5 từ Tây Ban Nha của lượt 1, 2, 3, 5, 6, ĐÚNG THỨ TỰ và đúng chính tả (có dấu, có ¡ ! nếu có);
   3 từ sau = 3 từ Tây Ban Nha cùng chủ đề (không dùng tới).
   Mỗi từ ngắn (tối đa khoảng 12 ký tự) để vừa nửa trái tờ giấy.
4. "PHAT_AM": nếu đổi tên app, viết lại hướng dẫn phát âm tên app theo cùng kiểu (ví dụ "TAWK-ah").
5. Giữ nguyên các khoá khác (POS_DAY, BOX_DAY, VAI_DAY, DAO_NGHI, NEN_XANH, NEN_PHO...) trừ khi tôi yêu cầu đổi.
6. Không thêm khoá mới, không bỏ khoá. Chỉ trả về JSON, không giải thích.
```

---

## 3. Kiểm tra file biến thể trước khi gen

- [ ] Có đúng **9** lượt trong `LUOT`.
- [ ] Lượt 1, 2, 3, 5, 6 đúng mẫu `¿Cómo se dice X? Se dice, Y. Repite conmigo. Y.` (Y giống nhau ở hai chỗ).
- [ ] 5 từ đầu trong `HAU_KY.bang.hang` **trùng y hệt và đúng thứ tự** với X của 5 lượt đó (và có đúng 8 từ). Từ trên giấy phải khớp lời đọc, vì bút tìm hàng theo thứ tự.
- [ ] Lượt 8 có "Descarga <Tên app>".
- [ ] Nếu đổi tên app: `PHAT_AM` đã sửa theo tên mới.

**Ngôn ngữ:** hậu kỳ đọc được mẫu câu tiếng Tây Ban Nha (`¿Cómo se dice X? Se dice, Y. Repite conmigo. Y.`, `Descarga <app>`) và tiếng Bồ Đào Nha (`Como se diz X? Se diz, Y. Repita comigo. Y.`, `Baixe o <app>`). Ngôn ngữ giọng nói khai trong `GIONG_DAY` của từng biến thể ("speaking native Spanish" / "speaking native Brazilian Portuguese"), script không ghi cứng. Mẫu tiếng Bồ: biến thể `talka-robot-trang-co-chu-pt`. **Tờ giấy và bút (khoá `HAU_KY`):** hậu kỳ dựng tờ giấy từ `"HAU_KY": {"giay": kiểu, "bang": {"tieu_de", "dau_trai", "hang": [{"tu", "icon"}]}, "but": kiểu}`. `giay`: `checklist` (giấy kem lưới chấm, vòng tròn đỏ), `hai-cot` (giấy kẻ dòng 2 cột Español | English, icon bên phải chữ), `hai-cot-icon-trai` (icon bên trái chữ), `so-tay` (sổ lò xo). `but`: bỏ trống = bút đỏ mẫu, hoặc `fountain` (bút máy), `ballpoint` (bút bi đỏ). `icon` là một ký tự biểu tượng (font Segoe UI Symbol), bỏ trống thì không có icon. Giấy vẽ trong `giay.py`, chữ tiếng Anh viết ở cột phải đúng hàng, nên đổi từ vựng không cần chỉnh gì thêm. Khoá `HAU_KY` chỉ được giữ khi tạo dự án từ file JSON biến thể (không giữ khi dùng "Điền từ file / bảng" vào biến thể đã có). Vẽ lại bút: `cong-cu/ve-but.py`.

File kịch bản và biến thể được sinh bởi `cong-cu/tao-kich-ban.py`, muốn đổi thì sửa script đó rồi chạy lại.

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
| Nền sau robot không phải xanh phẳng (có giấy, chữ, vệt sáng) hoặc robot bị khuyết mép sau hậu kỳ | Muse không giữ nền xanh | Gen lại cảnh đó; nếu hay bị, chỉnh `NEN_XANH` |
| Hậu kỳ báo "cảnh quảng cáo không phải nền xanh" | Video gen bằng kịch bản cũ (cảnh 7–9 nền thành phố) | Nhập lại kịch bản mới, gen lại cảnh 7–9 |
| Muốn đổi video nền thành phố | Nền đã lưu `nen_pho.mp4` | Xoá `nen_pho.mp4` trong thư mục chạy rồi Hậu kỳ lại |
| Bút chỉ sai hàng | 5 từ đầu trong `HAU_KY.bang.hang` không khớp thứ tự với lời đọc | Sửa biến thể, hậu kỳ lại |
| Chữ đen trên giấy chớp trắng 1–2 khung | Model video vẽ lại cả khung + nén | Thường bỏ qua được |
| Ô bảng quảng cáo thiếu chữ đỏ | Không có "Descarga <Tên app>" hoặc số + thời gian | Sửa câu trong lượt 7–9 |

---

## 5. Muốn chỉnh sâu hơn

- Kiểu ô bảng quảng cáo (vị trí, màu, cỡ chữ), lượt bắt đầu quảng cáo (`ad_from`), từ luôn tô đỏ (`red_words`): `app\production\types\talka-bang-tu-vung\config.json`.
- Câu chữ prompt của kịch bản: sửa `cong-cu\tao-kich-ban.py` rồi chạy lại để tạo `KICH-BAN-TALKA-CO-CHU.txt`, sau đó nhập lại kịch bản vào Studio.
- Lịch sử các cách đã thử và vì sao chọn cách hiện tại: `README.md` trong thư mục này.
