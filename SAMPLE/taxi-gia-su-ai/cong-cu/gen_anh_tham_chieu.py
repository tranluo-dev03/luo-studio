"""Gen ảnh tham chiếu nhân vật cho thể loại taxi-gia-su-ai bằng Muse (qua LUO-API của Studio đang chạy). Chỉ từ chữ, không dùng ảnh cắt từ video mẫu
(người dùng đồng ý gen bằng Muse, 11/11/2026). Robot DAY dùng ảnh có sẵn SAMPLE/canh-sat-gia-su-ai/anh/DAY.png nên không gen ở đây.
Chạy:  runtime\\python.exe SAMPLE\\taxi-gia-su-ai\\cong-cu\\gen_anh_tham_chieu.py [HOC KHACH QUANLY ARJUN CON]
Ảnh ra: SAMPLE/taxi-gia-su-ai/anh/<KHOÁ>.png (ảnh cũ cùng tên đổi thành <KHOÁ>-cu-<giờ>.png). Duyệt xong chạy lại tao_bien_the.py để thêm vào refs.
Mô tả nhân vật lấy từ biến thể (tao_bien_the.V) để ảnh và prompt Muse khớp nhau."""
import json
import os
import sys
import threading
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path[:0] = [HERE, os.path.join(ROOT, "app", "luo-studio"), os.path.join(ROOT, "app", "production")]
import engine as E  # noqa: E402
import gen_video as G  # noqa: E402
from tao_bien_the import V  # noqa: E402

ANH = os.path.join(HERE, "..", "anh")
STYLE = ("Pixar-style 3D CARTOON animated feature-film look: cartoon proportions, big round expressive eyes, simplified smooth features, soft rounded shapes, "
         "warm glowing skin, soft warm studio light; never photorealistic or semi-realistic")
SHEET = ("Character reference picture: ONE person only, shown from the knees up, standing straight and facing the camera in a three-quarter front view, "
         "relaxed neutral friendly face, mouth closed, arms relaxed at the sides, empty hands, on a plain flat light-grey studio background. "
         "No text, no logo, no lettering anywhere, nothing written on the clothes. Vertical 9:16.")
KEYS = ["HOC", "KHACH", "QUANLY", "ARJUN", "CON"]


def prompt(k):
    who = V[f"NGUOI_{k}"].replace("a stylized 3D-animated ", "").replace(", a plain brown clipboard and a pen", "")
    return f"{SHEET} {STYLE}. The person: {who}."


def main():
    names = [a.upper() for a in sys.argv[1:]] or KEYS
    run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
    env = os.path.join(ROOT, "userdata", "api", ".env")
    if not os.environ.get("MUSE2API_ENV_FILE") and os.path.exists(env):
        os.environ["MUSE2API_ENV_FILE"] = env
    key = G.read_key() or json.load(open(os.path.join(ROOT, "userdata", "studio", "settings.json"), encoding="utf-8")).get("api_key", "")
    api = E.Api(f"http://127.0.0.1:{run['api_port']}", key)
    os.makedirs(ANH, exist_ok=True)
    for k in names:
        sess = f"refs-taxi-{k.lower()}-{int(time.time())}-{uuid.uuid4().hex[:5]}"   # mỗi nhân vật một phiên: không lẫn ảnh trước
        print(f"[{k}] gen...", flush=True)
        b = api.generate("image", G.muse_image_prompt(prompt(k), "text, letters, logo, watermark, extra people, distorted face, photorealistic", 0),
                         [], sess, timeout=600, cancel=threading.Event(), aspect="9:16")
        out = os.path.join(ANH, f"{k}.png")
        if os.path.exists(out):
            os.replace(out, os.path.join(ANH, f"{k}-cu-{time.strftime('%H%M%S')}.png"))
        open(out, "wb").write(b)
        print(f"[{k}] -> anh/{k}.png ({len(b) // 1024} KB)", flush=True)


if __name__ == "__main__":
    main()
