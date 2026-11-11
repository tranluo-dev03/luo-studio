"""Gen ảnh tham chiếu (robot + nền) cho 60 biến thể của tao_60_bien_the.py bằng Muse, qua LUO-API của Studio đang chạy. Chỉ từ chữ.
Chạy:  runtime\\python.exe SAMPLE\\robot-pho-tieng-long\\cong-cu\\gen_anh_60.py [bh|in|br|in03|br07-nv ...] [--lai] [--luong 3]
  không đối số: gen mọi ảnh còn thiếu (bỏ qua ảnh đã có, chạy lại được khi bị ngắt). --lai: gen lại cả ảnh đã có (ảnh cũ đổi tên <tên>-cu-<giờ>.webp).
Ảnh ra: anh/bh/bh-nv.webp, bh-bg.webp (cả nhóm đổi bài học dùng chung), anh/in/inNN-nv.webp, inNN-bg.webp, anh/br/brNN-nv.webp, brNN-bg.webp.
Robot đứng trên nền xanh lá trơn (kịch bản đã dặn bỏ nền xanh); ảnh nền là cảnh trống, không người."""
import argparse
import io
import json
import os
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path[:0] = [HERE, os.path.join(ROOT, "app", "luo-studio"), os.path.join(ROOT, "app", "production")]
import engine as E  # noqa: E402
import gen_video as G  # noqa: E402
import tao_60_bien_the as T  # noqa: E402

ANH = os.path.join(HERE, "..", "anh")
AIVA = os.path.join(ANH, "aiva", "aiva-robot.webp")
SHEET_NV = ("Character reference image: the attached reference image shows the Aiva AI robot: reproduce THIS EXACT robot (same face, eyes, forehead \"AI\" mark, headphones with microphone, neck, white armor and chest book icon, same proportions and colours) and change ONLY its clothing as described: dress it fully like a person in the described clothes (closed top with long sleeves, trousers, a skirt or a fully wrapped saree), covering the whole torso, shoulders, arms and legs, so only the robot head, neck and hands are visible. Extend the body down to the thighs. ONE robot only, a plain full-bleed photo with square corners (no rounded frame, no black border, no icon background), seen from the thighs up, standing straight in the middle of the frame and facing the camera, "
            "lively friendly face, lips closed in a soft smile, looking straight into the lens, arms relaxed at the sides with open hands near the hips, "
            "on a plain flat bright-green studio backdrop. No text, no logo, no lettering anywhere, nothing written on the clothes. Vertical 9:16. "
            "Photorealistic cinematic CGI, soft even studio light, sharp detail on the face, the white armor and the fabric.")
NEG_NV = "text, letters, logo, watermark, a different face, a hat over the headphones, bare robot torso, bare robot arms or legs, an open jacket showing the armor, a second robot or person, hands raised, pointing, cartoon, anime, distorted face, human hair on the head"
SHEET_BG = ("Background plate photograph, vertical 9:16, photorealistic, taken at chest height with a 35mm lens, sharp and detailed, natural light. "
            "The place is completely empty: no people, no animals, no moving vehicles, nothing in the foreground. Any signs carry no readable letters. "
            "No text, no logo, no watermark.")
NEG_BG = "people, person, crowd, robot, text, letters, readable signs, logo, watermark, cartoon"


def tasks():
    """[(mã, đường dẫn ra, prompt, negative)]"""
    out = []
    tx = T.TEXAS
    out.append(("bh-nv", os.path.join(ANH, "bh", "bh-nv.webp"), f"{SHEET_NV} Outfit: {tx[1]}.", NEG_NV))
    out.append(("bh-bg", os.path.join(ANH, "bh", "bh-bg.webp"), f"{SHEET_BG} The place: {tx[2].split('; the whole background')[0]}", NEG_BG))
    for k, (slug, city, city_hi, gender, face, outfit, nen) in enumerate(T.AN_DO, 1):
        out.append((f"in{k:02d}-nv", os.path.join(ANH, "in", f"in{k:02d}-nv.webp"), f"{SHEET_NV} Outfit: {outfit}.", NEG_NV))
        out.append((f"in{k:02d}-bg", os.path.join(ANH, "in", f"in{k:02d}-bg.webp"), f"{SHEET_BG} The place: {nen}.", NEG_BG))
    for k, (slug, title, em, de, gender, face, outfit, nen) in enumerate(T.BRAZIL, 1):
        out.append((f"br{k:02d}-nv", os.path.join(ANH, "br", f"br{k:02d}-nv.webp"), f"{SHEET_NV} Outfit: {outfit}.", NEG_NV))
        out.append((f"br{k:02d}-bg", os.path.join(ANH, "br", f"br{k:02d}-bg.webp"), f"{SHEET_BG} The place: {nen}.", NEG_BG))
    return out


def api():
    run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
    env = os.path.join(ROOT, "userdata", "api", ".env")
    if not os.environ.get("MUSE2API_ENV_FILE") and os.path.exists(env):
        os.environ["MUSE2API_ENV_FILE"] = env
    key = G.read_key() or json.load(open(os.path.join(ROOT, "userdata", "studio", "settings.json"), encoding="utf-8")).get("api_key", "")
    return E.Api(f"http://127.0.0.1:{run['api_port']}", key)


def save_webp(b, out):
    from PIL import Image
    im = Image.open(io.BytesIO(b)).convert("RGB")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        os.replace(out, out[:-5] + f"-cu-{time.strftime('%H%M%S')}.webp")
    im.save(out, "WEBP", quality=90)
    return im.size


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("chon", nargs="*")
    ap.add_argument("--lai", action="store_true")
    ap.add_argument("--luong", type=int, default=3)
    a = ap.parse_args()
    todo = [t for t in tasks() if (not a.chon or any(t[0].startswith(c) for c in a.chon)) and (a.lai or not os.path.exists(t[1]))]
    print(f"{len(todo)} ảnh cần gen, {a.luong} luồng", flush=True)
    A = api()
    cancel = threading.Event()

    def one(t):
        ma, out, prompt, neg = t
        sess = f"refs-pho60-{ma}-{int(time.time())}-{uuid.uuid4().hex[:5]}"
        for lan in range(2):
            try:
                refs = [G.data_url(AIVA)] if ma.endswith("-nv") else []
                b = A.generate("image", G.muse_image_prompt(prompt, neg, len(refs)), refs, sess + f"-{lan}", timeout=600, cancel=cancel, aspect="9:16")
                w, h = save_webp(b, out)
                return f"{ma}: OK {w}x{h}"
            except Exception as e:  # noqa: BLE001
                err = str(e)[:160]
        return f"{ma}: LỖI {err}"

    t0 = time.time()
    with ThreadPoolExecutor(max(1, a.luong)) as ex:
        futs = [ex.submit(one, t) for t in todo]
        for n, f in enumerate(as_completed(futs), 1):
            print(f"[{n}/{len(todo)} {time.time() - t0:.0f}s] {f.result()}", flush=True)


if __name__ == "__main__":
    main()
