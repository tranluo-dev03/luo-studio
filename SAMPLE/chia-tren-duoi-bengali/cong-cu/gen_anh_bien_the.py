"""Nhờ Muse gen ảnh tham chiếu người học cho bộ 20 biến thể (người dùng yêu cầu 10/11/2026), lưu anh/bien-the/<STT>.png. Chỉ dùng lời tả theo CSV, không gửi khung nào của video mẫu.
Ảnh đã có thì bỏ qua; muốn gen lại ảnh nào thì xoá tệp đó rồi chạy lại.
Chạy khi Studio đang mở:  .venv\\Scripts\\python.exe SAMPLE\\chia-tren-duoi-bengali\\cong-cu\\gen_anh_bien_the.py"""
import base64
import json
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "anh", "bien-the")
os.environ.setdefault("MUSE2API_HOME", os.path.join(ROOT, "userdata", "api"))   # thiếu thì script ngoài Studio bị HTTP 401
sys.path.insert(0, os.path.join(ROOT, "app", "luo-studio"))
sys.path.insert(0, os.path.join(ROOT, "app", "production"))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")
import engine as E  # noqa: E402
import tao_bo_csv as T  # noqa: E402

# Phần dưới của trang phục theo CSV (trong video chỉ thấy tới ngang eo nên bảng NHAN_VAT không ghi)
DUOI = {
    1: "grey dress trousers, a black leather belt and polished black leather shoes", 2: "beige dress trousers and polished brown leather shoes",
    3: "dark dress trousers, a black leather belt and polished black leather shoes", 4: "white trousers and polished loafers",
    5: "dark dress trousers, a black leather belt and polished black leather shoes", 6: "high-heeled sandals", 7: "churidar trousers and embroidered shoes", 8: "high-heeled sandals",
    9: "a long flared skirt and high-heeled sandals", 10: "high-heeled sandals", 11: "white trousers and polished leather shoes", 12: "white trousers and polished leather shoes",
    13: "white trousers and polished leather shoes", 14: "dark dress trousers and polished leather shoes", 15: "white trousers and polished leather shoes", 16: "high-heeled sandals",
    17: "high-heeled sandals", 18: "embroidered shoes", 19: "golden sandals", 20: "high-heeled sandals",
}
G = E.G
run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
f = os.path.join(ROOT, "userdata", "studio", "settings.json")
st = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
api = E.Api(f"http://127.0.0.1:{run['api_port']}", (st.get("api_key") or "").strip() or G.read_key())
os.makedirs(OUT, exist_ok=True)
NEG = "text, subtitles, captions, logo, watermark, cropped head, cropped feet, extra people, objects in the hands, sitting, shadows on the background, patterned background"


def gen(row):
    stt, slug, gioi, tuoi, mo_ta = row
    out = os.path.join(OUT, f"{stt:02d}.png")
    if os.path.exists(out):
        return f"{stt:02d} da co"
    prompt = (f"Generate exactly one still image now, vertical 9:16, photorealistic full-body photo of {T.nguoi(gioi, tuoi, mo_ta)}, with {DUOI[stt]}. "
              "The person stands upright facing the camera straight on, the whole body from the top of the head to the feet fully inside the frame and centred, arms hanging relaxed at the sides, "
              "both hands empty, eyes looking into the lens, the mouth closed in a smile. The face is sharp, clear and evenly lit. Plain flat pure chroma-key green background (#00FF00) with nothing else on it. "
              "Not sitting, holding nothing. One complete clean image. No text, no letters, no logos, no watermark, no other people.")
    for lan in range(3):
        try:
            b = api.generate("image", G.muse_image_prompt(prompt, NEG, 0), [], f"studio-bengali-bt{stt:02d}-{uuid.uuid4().hex[:6]}", timeout=420, on_status=lambda s, p: None)
            with open(out, "wb") as fh:
                fh.write(b if isinstance(b, (bytes, bytearray)) else base64.b64decode(b))
            print(f"{stt:02d} XONG {slug}", flush=True)
            return f"{stt:02d} xong"
        except Exception as ex:  # noqa: BLE001
            print(f"{stt:02d} loi lan {lan + 1}: {str(ex)[:200]}", flush=True)
    return f"{stt:02d} THAT BAI"


if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex:
        kq = list(ex.map(gen, T.NHAN_VAT))
    print("TONG KET:", [x for x in kq if "THAT BAI" in x] or "khong anh nao that bai", "| co", len([n for n in os.listdir(OUT) if n.endswith(".png")]), "anh", flush=True)
