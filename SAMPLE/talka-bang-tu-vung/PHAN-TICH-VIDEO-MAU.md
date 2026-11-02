# Phân tích "Video mẫu.mp4" → kịch bản Talka (robot dạy từ vựng, 1 nhân vật)

Nguồn: `D:\Tải về\Video mẫu.mp4`, 52,1 giây, 720x1280, 31 câu nói, **tốc độ nói trung vị 4,13 từ/giây** (cao nhất 5,13), khoảng lặng giữa các câu ~0,6 giây. Chạy bằng `SAMPLE\_chung\phan-tich-video.py`, đã xem ảnh tổng quan, từng lượt và các khoảnh khắc chuyển động.

File giao kèm:
- `KICH-BAN-TALKA.txt`: nhập ở tab "Loại dự án" → "Loại mới".
- `BIEN-THE-TALKA.json`: nhập ở tab biến thể (1 biến thể `talka-robot-trang`).

## 1. Video gốc có gì

Chỉ **một nhân vật nói**: robot trắng, nửa thân dưới khung, nhìn thẳng ống kính, camera cố định. Không có người học. Lời thoại xen tiếng Tây Ban Nha và tiếng Anh. Video gồm 3 đoạn:

| Giây | Đoạn | Nền | Việc xảy ra |
|---|---|---|---|
| 0–36,4 | Dạy từ | Tờ giấy checklist `¿CÓMO SE DICE?` trên tường be, 8 dòng từ tiếng Tây Ban Nha | Robot hỏi, đọc từ tiếng Anh, bảo lặp lại. Bút đỏ lướt qua giấy, chữ xanh tiếng Anh hiện cạnh mỗi từ |
| 36,4–49,2 | Quảng cáo | Thành phố lúc hoàng hôn | Robot mời tải ứng dụng; khung chữ trắng phía trên đổi theo từng cụm lời |
| 49,2–52,1 | End card | Nền trắng, logo và nút tải | Robot vẫn đọc "Best Language Learning App. Download now." |

## 2. Bảng hành động (mỗi lượt một dòng)

Ai nói: luôn là robot. Người nghe: không có. Ánh mắt: nhìn thẳng ống kính. Camera: đứng yên. Khung cuối: robot đứng im, miệng khép, tay không vào khung.

| Lượt | Giây (gốc) | Lời | Từ/giây | Hành động của robot | Vật/đồ họa trên màn hình |
|---|---|---|---|---|---|
| 1 | 0–6,4 | ¿Cómo se dice para mí en inglés? Se dice, for me. Repite conmigo. For me. | ~4,2 | Nói có biểu cảm, nhướng mày khi hỏi; từ tiếng Anh nói chậm, rõ | Bút đỏ lướt vào từ trên phải; chữ xanh `For me` hiện sau câu "Se dice" |
| 2 | 6,96–12,44 | ¿Cómo se dice para ti? Se dice, for you. Repite conmigo. For you. | ~4 | Như lượt 1 | Bút đỏ chỉ dòng 2; chữ xanh `For you` |
| 3 | 13,06–18,18 | ¿Cómo se dice nunca? Se dice, never. Repite conmigo. Never. | ~4 | Như lượt 1 | Chữ xanh `Never` |
| 4 | 18,98–23,58 | El inglés no es difícil y descubrirás que tengo razón si sigues esta página. | 3,0 | Nói chậm hơn, tự tin, mỉm cười | Bút đỏ lướt xuống dưới, không có từ mới |
| 5 | 24,24–29,7 | ¿Cómo se dice por favor? Se dice, please. Repite conmigo. Please. | ~3,5 | Như lượt 1 | Chữ xanh `Please` |
| 6 | 30,48–36,2 | ¿Cómo se dice gracias? Se dice, thank you. Repite conmigo. Thank you. | ~4 | Như lượt 1 | Chữ xanh `Thank you` (chỉ thấy một phần sau lưng robot) |
| 7 | 36,56–38,62 | ¿Quieres aprender inglés de una manera más fácil? | 3,9 | Nền đổi sang thành phố hoàng hôn; robot cười, nói thân thiện | Khung chữ trắng phía trên robot |
| 8 | 39,0–44,74 | Descarga Talka y en solo cuatro semanas podrás sonar como un hablante nativo. | 2,3 (có nhịp ngắt) | Nói thuyết phục | Khung chữ đổi theo cụm: "Descarga", "y en solo 4 semanas podrás sonar", "como un hablante nativo." |
| 9 | 45,08–51,56 | Un tutor con IA que te corrige en tiempo real y acelera tu progreso. Best Language Learning App. Download now. | ~3 | Giọng hào hứng, kêu gọi hành động | Khung chữ đổi cụm; từ 49,2s chuyển sang end card trắng |

Lưu ý nhận dạng giọng: công cụ nghe nhầm "IA" thành "línea" và "hija". Lời thật theo chữ trên màn hình và nghe lại bằng tiếng Tây Ban Nha: `Un tutor con IA`. Lượt 4 đã nghe lại bằng chế độ tiếng Tây Ban Nha, kết quả khớp.

Thay đổi so với video gốc: `LangLearn` → `Talka` (lượt 8). Mọi lời khác giữ nguyên.

## 3. Bảng "video gốc → kịch bản"

| Thành phần video gốc | Trong kịch bản | Ghi chú |
|---|---|---|
| Robot nửa thân dưới khung, nhìn ống kính | Có, cố định ở `[STYLE LOCK]`. Cảnh trung rộng, robot nhỏ: đỉnh đầu ~47% chiều cao khung, đầu rộng ~25% khung, vai ~60% khung; đoạn dạy từ lệch phải một chút (tâm đầu ~62% chiều rộng), đoạn thành phố ở giữa | Giữ nguyên bố cục |
| Robot màu trắng, chi tiết cam | Đổi theo ảnh của bạn: thân trắng viền đen, đường sáng **xanh dương nhạt**, mắt xanh nhạt, đầu trắng bóng không tóc | Token `NGUOI_DAY`; `[CHAR LOCK]` cấm màu cam/đỏ |
| Nền tờ giấy checklist có chữ | **Đơn giản hoá**: tờ giấy có thanh tiêu đề và 8 dòng với chấm tròn đỏ, nhưng các dòng chỉ là vạch xám, **không có chữ** | Token `NEN_BANG`. Muse hay vẽ sai chữ và làm chữ biến dạng giữa clip |
| Chữ xanh tiếng Anh hiện dần, bút đỏ và bàn tay lướt qua | **Bỏ khỏi prompt** (hình đồ họa chèn thêm, không phải cảnh quay) | Thêm lúc dựng, xem mục 4 |
| Cắt cứng sang nền thành phố (36,4s) | Cảnh 7 có `Prompt ảnh` riêng, nên Studio sinh khung đầu mới | Token `NEN_PHO` |
| Khung chữ trắng phía trên, chữ đổi theo cụm | **Bỏ khỏi prompt**; chừa nửa trên khung là nền trống | Phụ đề do hậu kỳ của Studio; khung chữ kiểu này phải dựng thêm |
| Logo LangLearn góc trên trái | Chừa trống góc trên trái và 12% phía trên | Logo ghép bằng hậu kỳ (Cài đặt → Logo) |
| End card trắng | Không có trong cảnh gen; nối bằng "End card" của hậu kỳ | `app\production\types\talka-bang-tu-vung\assets\endcard-talka.mp4` có sẵn trong repo, cần kiểm tra đúng mẫu |
| Lời thoại xen hai ngôn ngữ | Giữ nguyên trong `LUOT`; `[CHAR LOCK]` yêu cầu giọng Tây Ban Nha bản ngữ, từ tiếng Anh giọng Mỹ chuẩn | Xem rủi ro bên dưới |
| Giọng nói | `GIONG_DAY`: nữ trẻ, ấm, tươi, tự nhiên | Dùng lại một giọng cho mọi cảnh |

## 4. Việc phải làm thêm sau khi gen (hậu kỳ thủ công)

Prompt cố ý không chứa chữ, nên các thứ sau phải thêm bằng phần mềm dựng:
1. Chữ trên tờ giấy: tiêu đề `¿CÓMO SE DICE?` và 8 từ tiếng Tây Ban Nha (Para mí, Para ti, Nunca, Por favor, ¡Gracias!, Lo siento, Hasta luego, dòng cuối bị cắt nên không đọc được).
2. Chữ xanh tiếng Anh hiện ra đúng lúc robot nói từ đó: cảnh 1 `For me`, cảnh 2 `For you`, cảnh 3 `Never`, cảnh 5 `Please`, cảnh 6 `Thank you`.
3. Bút đỏ lướt qua (tuỳ chọn).
4. Khung chữ trắng ở cảnh 7–9 (tuỳ chọn, nếu muốn giống video gốc).

Vì Studio cắt sát lời nên thời lượng từng cảnh khác video gốc; hãy canh theo video đã gen, không dùng giây gốc.

## 5. Rủi ro và cách kiểm tra

- **Lời xen hai ngôn ngữ:** bộ cắt sát lời của Studio khớp từ theo chữ tiếng Anh không dấu, nên lời tiếng Tây Ban Nha có thể bị cắt kém chính xác. Khi đó Studio ghi "cắt theo cách thường" và vẫn ra video.
- **Số từ mỗi lượt:** lượt 9 dài 20 từ (đúng giới hạn tối đa 20). Nếu Muse nói không kịp, tách "Best Language Learning App. Download now." thành lượt riêng.
- **Một nhân vật:** kịch bản và `speaker_lock` đã kiểm tra chạy được với một nhân vật (không có người nghe, không đo miệng người nghe). Chưa gen thử trên Muse.
- **Đo miệng người nói:** dùng `BOX_DAY` = `0.35,0.43,0.85,0.7` (vùng mặt robot theo tỉ lệ khung). Nếu Muse đặt robot cao hoặc thấp hơn, chỉnh số này.
- **Cuối cùng, theo hướng dẫn:** chạy thử **một biến thể**, xem ảnh khung đầu cảnh 1 và cảnh 7 trước khi chạy cả nhóm.

## 6. Phương án 2: Muse tự vẽ chữ và bút (`*-CO-CHU`)

Hai file `KICH-BAN-TALKA-CO-CHU.txt` và `BIEN-THE-TALKA-CO-CHU.json` thay cho cặp file ở trên khi bạn muốn Muse vẽ luôn chữ trên giấy. Khác bản không chữ:
- Tờ giấy có tiêu đề `¿CÓMO SE DICE?` và 8 từ Tây Ban Nha theo thứ tự: Para mí, Para ti, Nunca, Por favor, ¡Gracias!, Lo siento, Hasta luego, **Cuídate** (dòng cuối trong video gốc bị cắt nên chỉ đọc được "Cuí"; "Cuídate" là phần tôi đoán, hãy sửa trong `NEN_BANG` nếu khác).
- Chữ xanh tiếng Anh hiện **dần theo từng cảnh**, mỗi cảnh ghi sẵn trạng thái tờ giấy lúc đầu và lúc cuối: cảnh 1 `For me`, cảnh 2 `For you`, cảnh 3 `Never`, cảnh 4 không viết thêm, cảnh 5 `Please`, cảnh 6 `Thank you`.
- Bàn tay cầm bút đỏ trượt vào từ góc trên bên phải, viết từ đó lúc robot nói, rồi ra khỏi khung trước từ cuối (khung cuối không còn tay, bút).
- `[STYLE LOCK]`, `[SET LOCK]`, `[NEGATIVE]` cho phép chữ **chỉ trên tờ giấy**; cảnh 7–9 (thành phố) vẫn cấm mọi chữ.

Rủi ro: chữ có dấu (¿ ¡ í é) dễ bị vẽ sai; chữ có thể nhoè hoặc đổi giữa clip; bàn tay và bút có thể méo hoặc không ra đúng lúc. Chữ sai ở cảnh nào sẽ lan sang các cảnh sau (cảnh sau nối từ khung cuối), nên khi thấy sai hãy gen lại **từ cảnh đầu tiên bị sai**. Studio dùng `raw_prompt` nên không tự xoá chữ khỏi ảnh.

### Sửa lần 2: neo vị trí viết bằng từ và vạch xám

Phiên gen thử báo cảnh 5 sai 10 lần liên tiếp: Muse viết `Please` đè lên `Never` (dòng 3) thay vì dòng 4. Bản `*-CO-CHU` đã đổi cách chỉ vị trí, chưa gen lại để kiểm chứng:
- Mỗi dòng có một **vạch xám mảnh** ở bên phải từ Tây Ban Nha (token `NEN_BANG`), là ô trống để viết.
- Prompt chỉ ô cần viết bằng **tên từ**, không chỉ bằng số dòng: "vạch xám ngay bên phải chữ `Por favor`", số dòng chỉ để phụ.
- Mỗi cảnh ghi rõ chữ xanh đã nằm ở vạch của từ nào, vạch nào còn trống, và cấm chạm hoặc viết đè các chữ đã có.
- `[NEGATIVE]` thêm: viết chữ mới đè lên chữ cũ, hoặc đặt cạnh sai từ Tây Ban Nha.

Nếu cảnh vẫn sai sau 2–3 lần thử, đừng thử tiếp bằng prompt: chuyển sang chèn chữ lúc dựng (bản không chữ).
