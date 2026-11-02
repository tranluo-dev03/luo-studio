# Hậu kỳ riêng: Talka bảng từ vựng (`talka-bang-tu-vung`)

Kịch bản, biến thể, phân tích của thể loại này: `SAMPLE/talka-bang-tu-vung/`.

Không phụ đề. Các bước (`post.py`):
1. **Giấy + robot + bút chỉ + chữ tiếng Anh** (`giay.py`, `pointer.py`): video Muse cảnh dạy từ chỉ có robot trên nền xanh lục; hậu kỳ dựng tờ giấy tĩnh (spec trong `HAU_KY.bang` của biến thể, biết chính xác toạ độ từng từ), tách nền xanh (ffmpeg `colorkey` + `despill`) và ghép robot lên giấy. Không có `HAU_KY.bang` (video cũ gen kèm tờ checklist trong Muse) thì dò vị trí trên khung hình như trước. Như video gốc:
   - bút đỏ luôn nằm trên giấy, lướt qua đúng chữ robot đang đọc (từ Tây Ban Nha → chữ tiếng Anh → lướt lại khi đọc lại), trượt êm sang chữ/hàng tiếp theo;
   - chữ tiếng Anh xanh nghiêng hiện ra nguyên chữ đúng lúc bút đặt vào đầu chữ, ngồi trên vạch xám, giữ đến hết phần bảng chữ.
   - Mốc thời gian: Whisper theo từng cảnh. Vị trí: lấy từ `giay.py` khi có giấy dựng sẵn; không thì đo trên khung hình (vòng tròn đỏ = hàng, chữ đen = từ bản ngữ, vạch xám = chỗ đặt chữ).
2. **Cảnh quảng cáo** (từ lượt `ad_from`; video Muse cũng nền xanh), xếp lớp như video gốc: **video nền thành phố** gen bằng AI theo ô `NEN_PHO` (lưu `nen_pho.mp4` cạnh `raw.mp4`, lần sau dùng lại; xoá file này để gen nền khác) → **ô bảng** kích thước cố định → **robot** đã tách nền trên cùng.
3. **Bố cục robot như video mẫu** (`config.json` → `bo_cuc`): hậu kỳ đo đỉnh đầu, tâm đầu, bề rộng đầu robot trong video rồi phóng/thu và dời robot cho khớp: cảnh dạy từ đỉnh đầu 47,5%, tâm đầu 70% bề ngang, đầu rộng 28,5%; cảnh quảng cáo đỉnh đầu 48,5%, tâm 47%, đầu rộng 29%, đầu chỉ chạm mép dưới bảng (`che_bang`), không che chữ. Thân robot luôn chạm đáy khung (không phóng nhỏ quá mức đó).
4. **Chữ trong ô bảng**: ô trắng viền xanh giữa phía trên, hiện **đúng lời robot đang nói** theo từng cụm (Whisper căn thời điểm), chữ đậm xanh đậm, từ khoá tô đỏ. Nội dung trong `config.json` mục `phrases` (`text`: `\n` xuống dòng, `*chữ*` = đỏ); kiểu ô trong mục `board`.
Không gắn logo và không thêm end card (đã bỏ; file `assets/endcard-talka.mp4` còn trong repo nhưng không dùng).

## File
| File | Nội dung |
|---|---|
| `post.py` | Điểm vào: `python post.py raw.mp4 --scenes scenes.json --out final.mp4 [--variant bien-the.json] [--model medium] [--no-pointer]` |
| `pointer.py` | Bút chỉ + chữ tiếng Anh |
| `bien_the.py` | Đọc biến thể (Studio truyền `--variant`): cặp từ cho bút từ các lượt "¿Cómo se dice X? Se dice, Y. Repite conmigo. Y.", lời cho ô bảng quảng cáo từ lượt `ad_from` |
| `config.json` | `bo_cuc`: vị trí, cỡ robot như video mẫu; `board`: ô bảng quảng cáo cố định (`x`, `w`, `y_top`, `h` theo khung 1080x1920); `nen_pho_giay`: độ dài video nền; `robot_top`: chỉ cho video cũ; `ad_from`, `red_words`; `pointer`/`phrases`: chỉ dùng khi chạy tay không có `--variant` |
| `assets/marker.png`, `marker.json` | Ảnh cây bút (Muse gen trên phông xanh, đã cắt phông), toạ độ ngòi bút; `marker_raw.png` là ảnh gốc |
| `assets/endcard-talka.mp4` | End card cũ, không còn dùng |

Studio dùng hậu kỳ này khi loại dự án có tên bắt đầu bằng `KICH-BAN-TALKA` hoặc file loại có `"post": "talka-bang-tu-vung"` (`app/luo-studio/server.py`, hàm `custom_post`).
