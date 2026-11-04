# Code riêng: chia đôi màn hình + gia sư AI (`chia-doi-gia-su-ai`)

Kịch bản, biến thể, phân tích: `SAMPLE/chia-doi-gia-su-ai/`. Studio dùng thư mục này khi kịch bản có khối `[HAU KY]` với dòng `loai: chia-doi-gia-su-ai`.
Thể loại chỉ có MỘT phần ghép 2 lớp nên không cần `gen.py`: Studio chạy thẳng chế độ ghép 2 lớp (`app/luo-studio/split.py`), nhân vật nền (`HOC`) cũng có `khung` riêng (nửa phải).

| File | Nội dung |
|---|---|
| `post.py` | Hậu kỳ: phụ đề theo người nói, viền + tiếng sai/đúng chỉ ở nửa phải. Logic: `../_chung/hau_ky.py` + `phu_de.py` |
| `config.json` | `phu_de`: cỡ chữ 56, tâm phụ đề ở y 1300 (khung 1080×1920), `kieu_theo_phan` (AI chữ trắng / người dùng chữ vàng, cả hai trên ô đen), `vien` (viền chỉ ở x 0,5–1, nháy ở cuối câu), Whisper `small.en` |

Chạy tay hậu kỳ: `runtime\python.exe app\production\types\chia-doi-gia-su-ai\post.py <run>\raw.mp4 --scenes <run>\scenes.json --out <run>\final.mp4 --variant <run>\variant.json`.
