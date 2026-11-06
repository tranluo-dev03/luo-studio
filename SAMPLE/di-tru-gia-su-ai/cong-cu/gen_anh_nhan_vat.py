"""Nhờ Muse gen ảnh tham chiếu nhân vật (ảnh AI hoàn chỉnh, CHỈ từ chữ, không dùng khung video mẫu) cho thể loại di-tru-gia-su-ai.
    set MUSE2API_HOME=userdata\\api
    .venv\\Scripts\\python.exe SAMPLE\\di-tru-gia-su-ai\\cong-cu\\gen_anh_nhan_vat.py [tên ...]
Không ghi tên thì gen mọi ảnh còn thiếu trong anh/. Ảnh ra: anh/ai-<tên>.png. Mô tả lấy từ tao_bien_the.py (biến thể 01) để ảnh và chữ khớp nhau."""
import base64
import json
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
ANH = os.path.join(HERE, "..", "anh")
sys.path.insert(0, os.path.join(ROOT, "app", "luo-studio"))
sys.path.insert(0, os.path.join(ROOT, "app", "production"))
os.environ.setdefault("MUSE2API_HOME", os.path.join(ROOT, "userdata", "api"))
import engine as E  # noqa: E402
sys.path.insert(0, HERE)
import tao_bien_the as TB  # noqa: E402

G = E.G
CHUNG = "Plain smooth light-grey seamless studio background, soft even front light. One complete clean image: the whole head, hair and both shoulders fully inside the frame, nothing cut by the edges. No text, no letters, no logos, no watermark, no other people."
NEG = "text, letters, logo, watermark, subtitles, cropped head, extra people, extra fingers"
V = TB.BIEN_THE[0]

ANH_CAN = {
    "amiga": ("photorealistic studio portrait photo", f"{V['NGUOI_AMIGA']}. She stands facing the camera straight on, framed from the top of the head down to the hips, centred, arms relaxed at her sides, empty hands, a calm closed-mouth expression, eyes looking into the lens."),
    "hoc": ("photorealistic studio portrait photo", f"{V['NGUOI_HOC']}. He stands facing the camera straight on, framed from the top of the head down to the knees, centred, arms relaxed at his sides, empty hands, a calm closed-mouth expression, eyes looking into the lens."),
    "canhsat": ("photorealistic studio portrait photo", f"{V['NGUOI_CANHSAT']}. He stands facing the camera straight on, framed from the top of the head down to the knees, centred, arms relaxed at his sides, empty hands, a calm closed-mouth expression, eyes looking into the lens. The badge and patches are plain shapes with no readable text."),
    "robo": ("high-end 3D render, cute stylized character design sheet look", f"{V['NGUOI_ROBO']}. Shown alone, full body from head to feet, sitting with legs dangling as if on a ledge, facing the camera, centred, a gentle closed-mouth smile."),
    "day": ("high-end photorealistic CGI render", f"{V['NGUOI_DAY']}. Shown alone, from just above the head down to the waist, facing the camera straight on, centred, arms relaxed, a calm closed-mouth expression, eyes looking into the lens."),
}


def gen(name):
    out = os.path.join(ANH, f"ai-{name}.png")
    if os.path.exists(out):
        print("đã có", out)
        return out
    run = json.load(open(os.path.join(ROOT, "userdata", "running.json")))
    sp = os.path.join(ROOT, "userdata", "studio", "settings.json")
    st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    api = E.Api(os.environ.get("LUO_API_URL") or f"http://127.0.0.1:{run['api_port']}", (st.get("api_key") or "").strip() or G.read_key())
    look, body = ANH_CAN[name]
    prompt = f"Generate exactly one still image now, vertical 9:16, {look}. {body} {CHUNG}"
    b = api.generate("image", G.muse_image_prompt(prompt, NEG, 0), [], f"ditru-{name}-{uuid.uuid4().hex[:6]}", timeout=900,
                     on_status=lambda s, p: print(name, "trạng thái:", s, p, flush=True))
    open(out, "wb").write(b if isinstance(b, (bytes, bytearray)) else base64.b64decode(b))
    print("XONG", out, flush=True)
    return out


if __name__ == "__main__":
    os.makedirs(ANH, exist_ok=True)
    names = sys.argv[1:] or list(ANH_CAN)
    with ThreadPoolExecutor(len(names)) as ex:
        list(ex.map(gen, names))
