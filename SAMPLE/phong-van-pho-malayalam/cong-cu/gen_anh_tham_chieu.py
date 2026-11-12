"""Gen ảnh tham chiếu nhân vật cho thể loại phong-van-pho-malayalam bằng Muse (qua LUO-API của Studio đang chạy). Chỉ từ chữ, không dùng ảnh cắt từ video mẫu.
Người dùng yêu cầu (11/11/2026): Muse gen phóng viên + người bán theo mô tả; robot dùng ảnh robot Talka có sẵn (anh/robot-talka.png).
Chạy:  runtime\\python.exe SAMPLE\\phong-van-pho-malayalam\\cong-cu\\gen_anh_tham_chieu.py [PV HOC]
Ảnh ra: anh/phong-vien.png, anh/nguoi-ban.png (ảnh cũ cùng tên đổi thành <tên>-cu-<giờ>.png). Duyệt xong chạy lại tao_bien_the.py.
Mô tả lấy từ tao_bien_the.py để ảnh và prompt Muse khớp nhau."""
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
import tao_bien_the as TB  # noqa: E402

ANH = os.path.join(HERE, "..", "anh")
STYLE = "photorealistic photograph, natural soft overcast daylight, realistic skin texture and fabric detail, sharp focus on the face, a real ordinary person, not a model"
SHEET = ("Character reference photo: ONE person only, shown from the knees up, standing straight and facing the camera in a three-quarter front view, "
         "relaxed natural friendly face, mouth closed, arms relaxed at the sides, empty hands, on a plain flat light-grey studio background. "
         "No text, no logo, no lettering anywhere, nothing written on the clothes. Vertical 9:16.")
NHAN_VAT = {
    "PV": ("phong-vien", TB.CHUNG["NGUOI_PV"]),
    "HOC": ("nguoi-ban", TB.NGUOI_HOC),
    "PVN": ("phong-vien-nu", None),   # phóng viên nữ cho 20 biến thể người bán nam (tao_40_bien_the.PV_NU)
}


def main():
    names = [a.upper() for a in sys.argv[1:]] or list(NHAN_VAT)
    run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
    env = os.path.join(ROOT, "userdata", "api", ".env")   # bản cài này có thể để khoá API ở userdata/api/.env
    if not os.environ.get("MUSE2API_ENV_FILE") and os.path.exists(env):
        os.environ["MUSE2API_ENV_FILE"] = env
    key = G.read_key() or json.load(open(os.path.join(ROOT, "userdata", "studio", "settings.json"), encoding="utf-8")).get("api_key", "")
    api = E.Api(f"http://127.0.0.1:{run['api_port']}", key)
    os.makedirs(ANH, exist_ok=True)
    for k in names:
        ten, who = NHAN_VAT[k]
        if k == "PVN":
            import tao_40_bien_the as T40
            who = T40.PV_NU["NGUOI_PV"]
        sess = f"refs-pvmalayalam-{k.lower()}-{int(time.time())}-{uuid.uuid4().hex[:5]}"   # mỗi nhân vật một phiên: không lẫn ảnh trước
        print(f"[{k}] gen...", flush=True)
        b = api.generate("image", G.muse_image_prompt(f"{SHEET} {STYLE}. The person: {who}.",
                                                      "text, letters, logo, watermark, extra people, distorted face, cartoon, 3D render", 0),
                         [], sess, timeout=600, cancel=threading.Event(), aspect="9:16")
        out = os.path.join(ANH, f"{ten}.png")
        if os.path.exists(out):
            os.replace(out, os.path.join(ANH, f"{ten}-cu-{time.strftime('%H%M%S')}.png"))
        open(out, "wb").write(b)
        print(f"[{k}] -> anh/{ten}.png ({len(b) // 1024} KB)", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
