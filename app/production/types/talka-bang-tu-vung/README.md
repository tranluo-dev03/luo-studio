# Hậu kỳ riêng: Talka bảng từ vựng (`talka-bang-tu-vung`)

Kịch bản, biến thể, phân tích của thể loại này: `SAMPLE/talka-bang-tu-vung/`.

Không phụ đề. Các bước (`post.py`):
1. **Bút chỉ + chữ tiếng Anh** (`pointer.py`): video Muse chỉ có robot nói trước bảng chữ cố định (vạch xám trống). Như video gốc:
   - bút đỏ luôn nằm trên giấy, lướt qua đúng chữ robot đang đọc (từ Tây Ban Nha → chữ tiếng Anh → lướt lại khi đọc lại), trượt êm sang chữ/hàng tiếp theo;
   - chữ tiếng Anh xanh nghiêng hiện ra nguyên chữ đúng lúc bút đặt vào đầu chữ, ngồi trên vạch xám, giữ đến hết phần bảng chữ.
   - Mốc thời gian: Whisper theo từng cảnh. Vị trí: đo trên khung hình (vòng tròn đỏ = hàng, chữ đen = từ Tây Ban Nha, vạch xám = chỗ đặt chữ).
2. **Logo** góc trái (`app/production/assets/topbar.png`).
3. **Ô bảng quảng cáo** ở các cảnh cuối, như video gốc: ô trắng viền xanh giữa phía trên, hiện **đúng lời robot đang nói** theo từng cụm (Whisper căn thời điểm), chữ đậm xanh đậm, từ khoá tô đỏ. Nội dung trong `config.json` mục `phrases` (`text`: `\n` xuống dòng, `*chữ*` = đỏ); kiểu ô trong mục `board`.
4. **End card** Talka (`assets/endcard-talka.mp4`).

## File
| File | Nội dung |
|---|---|
| `post.py` | Điểm vào: `python post.py raw.mp4 --scenes scenes.json --out final.mp4 [--variant bien-the.json] [--model medium] [--no-endcard] [--no-pointer]` |
| `pointer.py` | Bút chỉ + chữ tiếng Anh |
| `bien_the.py` | Đọc biến thể (Studio truyền `--variant`): cặp từ cho bút từ các lượt "¿Cómo se dice X? Se dice, Y. Repite conmigo. Y.", lời cho ô bảng quảng cáo từ lượt `ad_from` |
| `config.json` | `board`: kiểu ô bảng quảng cáo; `ad_from`, `red_words`; `pointer`/`phrases`: chỉ dùng khi chạy tay không có `--variant` |
| `assets/marker.png`, `marker.json` | Ảnh cây bút (Muse gen trên phông xanh, đã cắt phông), toạ độ ngòi bút; `marker_raw.png` là ảnh gốc |
| `assets/endcard-talka.mp4` | End card |

Studio dùng hậu kỳ này khi loại dự án có tên bắt đầu bằng `KICH-BAN-TALKA` hoặc file loại có `"post": "talka-bang-tu-vung"` (`app/luo-studio/server.py`, hàm `custom_post`).
