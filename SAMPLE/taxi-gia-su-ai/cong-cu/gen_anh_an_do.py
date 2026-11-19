"""Gen ảnh tham chiếu nhân vật phụ cho bản Ấn Độ (20 biến thể X0061) bằng Muse qua LUO-API của Studio đang chạy.
Người dùng chọn "Gen bằng Muse" cho con gái Priya và sếp (13/11/2026). Tài xế + khách lấy ảnh Google Drive trong sheet; đồng nghiệp Arjun dùng anh/ARJUN.png;
robot Ava dùng SAMPLE/canh-sat-gia-su-ai/anh/DAY.png.
Chạy:  runtime\\python.exe SAMPLE\\taxi-gia-su-ai\\cong-cu\\gen_anh_an_do.py [CON QUANLY]
Ảnh ra: SAMPLE/taxi-gia-su-ai/anh/an-do/<KHOÁ>.png (ảnh cũ cùng tên đổi thành <KHOÁ>-cu-<giờ>.png).
Mô tả lấy từ tao_bien_the_an_do.CHUNG để ảnh và prompt Muse khớp nhau."""
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
from gen_anh_tham_chieu import SHEET, STYLE  # noqa: E402
from tao_bien_the_an_do import CHUNG  # noqa: E402

ANH = os.path.join(HERE, "..", "anh", "an-do")
KEYS = ["CON", "QUANLY"]
TEN_FILE = {"CON": "NGUOI-CON"}  # CON là tên thiết bị dành riêng trên Windows, không đặt được tên file


def prompt(k):
    who = CHUNG[f"NGUOI_{k}"].replace("a stylized 3D-animated ", "").replace(", a plain brown clipboard and a pen", "")
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
        sess = f"refs-taxi-in-{k.lower()}-{int(time.time())}-{uuid.uuid4().hex[:5]}"
        print(f"[{k}] gen...", flush=True)
        b = api.generate("image", G.muse_image_prompt(prompt(k), "text, letters, logo, watermark, extra people, distorted face, photorealistic", 0),
                         [], sess, timeout=600, cancel=threading.Event(), aspect="9:16")
        out = os.path.join(ANH, f"{TEN_FILE.get(k, k)}.png")
        if os.path.exists(out):
            os.replace(out, os.path.join(ANH, f"{TEN_FILE.get(k, k)}-cu-{time.strftime('%H%M%S')}.png"))
        open(out, "wb").write(b)
        print(f"[{k}] -> anh/an-do/{TEN_FILE.get(k, k)}.png ({len(b) // 1024} KB)", flush=True)


if __name__ == "__main__":
    main()
