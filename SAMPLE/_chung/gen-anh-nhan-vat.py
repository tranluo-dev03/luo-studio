"""Gen ảnh tham chiếu (nhân vật / bối cảnh) bằng Muse qua LUO-API của Studio đang chạy. Dùng khi người dùng không đưa sẵn ảnh (quy trình video mới tự động).

  runtime\\python.exe SAMPLE\\_chung\\gen-anh-nhan-vat.py --ra <thư mục> --nv KHOA "<mô tả tiếng Anh>" [--nv KHOA2 "<mô tả>" ...] [--bc KHOA "<mô tả bối cảnh>" ...]

  --nv  nhân vật: MỘT người/robot, đứng thẳng nhìn ống kính từ đầu gối trở lên, tay buông, miệng khép, trên NỀN XANH LỤC PHẲNG (chroma-key green).
  --bc  bối cảnh: cảnh trống, KHÔNG có người, không chữ.
Ảnh ra: <thư mục>/<KHOA>.png (ảnh cũ cùng tên đổi thành <KHOA>-cu-<giờ>.png). In ra mỗi dòng `OK <KHOA> <đường dẫn>`; lỗi in `LOI <KHOA> <lý do>` và thoát mã 1.
Các nhân vật gen SONG SONG (mỗi nhân vật một phiên Muse riêng để không lẫn mặt)."""
import argparse
import json
import os
import sys
import threading
import time
import uuid

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [os.path.join(ROOT, "app", "luo-studio"), os.path.join(ROOT, "app", "production")]
import engine as E  # noqa: E402
import gen_video as G  # noqa: E402

STYLE = ("Pixar-style 3D CARTOON animated feature-film look: cartoon proportions, big round expressive eyes, simplified smooth features, soft rounded shapes, "
         "warm glowing skin, soft warm studio light; never photorealistic or semi-realistic")
SHEET_NV = ("Character reference picture: ONE character only, shown from the knees up, standing straight and facing the camera in a three-quarter front view, "
            "relaxed neutral friendly face, mouth closed, arms relaxed at the sides, empty hands, on a plain FLAT SOLID PURE CHROMA-KEY GREEN background (#00B140), "
            "perfectly uniform green with no gradient, no shadow on the background, no floor line, no green on the character. "
            "No text, no logo, no lettering anywhere, nothing written on the clothes. Vertical 9:16.")
SHEET_BC = ("Environment reference picture: an EMPTY location with absolutely no people, no animals and no characters, natural lighting, clean composition, "
            "no text, no signs with lettering, no logo. Vertical 9:16.")
NEG = "text, letters, logo, watermark, extra people, distorted face, photorealistic"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ra", required=True)
    ap.add_argument("--nv", nargs=2, action="append", default=[], metavar=("KHOA", "MO_TA"))
    ap.add_argument("--bc", nargs=2, action="append", default=[], metavar=("KHOA", "MO_TA"))
    a = ap.parse_args()
    jobs = [(k, f"{SHEET_NV} {STYLE}. The character: {d}.") for k, d in a.nv] + [(k, f"{SHEET_BC} {STYLE}. The place: {d}.") for k, d in a.bc]
    if not jobs:
        sys.exit("Không có gì để gen")
    run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
    env = os.path.join(ROOT, "userdata", "api", ".env")
    if not os.environ.get("MUSE2API_ENV_FILE") and os.path.exists(env):
        os.environ["MUSE2API_ENV_FILE"] = env
    key = G.read_key() or json.load(open(os.path.join(ROOT, "userdata", "studio", "settings.json"), encoding="utf-8")).get("api_key", "")
    api = E.Api(f"http://127.0.0.1:{run['api_port']}", key)
    out_dir = os.path.abspath(a.ra)
    os.makedirs(out_dir, exist_ok=True)
    bad = []
    lock = threading.Lock()

    def one(k, prompt):
        try:
            sess = f"refs-auto-{k.lower()}-{int(time.time())}-{uuid.uuid4().hex[:5]}"
            b = api.generate("image", G.muse_image_prompt(prompt, NEG, 0), [], sess, timeout=600, cancel=threading.Event(), aspect="9:16")
            out = os.path.join(out_dir, f"{k}.png")
            if os.path.exists(out):
                os.replace(out, os.path.join(out_dir, f"{k}-cu-{time.strftime('%H%M%S')}.png"))
            open(out, "wb").write(b)
            with lock:
                print(f"OK {k} {out}", flush=True)
        except Exception as e:  # noqa: BLE001
            with lock:
                bad.append(k)
                print(f"LOI {k} {str(e)[:200]}", flush=True)

    ths = [threading.Thread(target=one, args=j) for j in jobs]
    [t.start() for t in ths]
    [t.join() for t in ths]
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
