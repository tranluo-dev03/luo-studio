"""Nhờ Muse gen ảnh tham chiếu chàng trai (người dùng yêu cầu 10/11/2026), lưu anh/nguoi-hoc.png. Chỉ dùng lời tả, không gửi khung nào của video mẫu.
Chạy khi Studio đang mở:  runtime\\python.exe SAMPLE\\chia-tren-duoi-bengali\\cong-cu\\gen_anh_hoc.py"""
import base64
import json
import os
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
os.environ.setdefault("MUSE2API_HOME", os.path.join(ROOT, "userdata", "api"))   # thiếu thì script ngoài Studio bị HTTP 401
sys.path.insert(0, os.path.join(ROOT, "app", "luo-studio"))
sys.path.insert(0, os.path.join(ROOT, "app", "production"))
sys.stdout.reconfigure(encoding="utf-8")
import engine as E  # noqa: E402

G = E.G
run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
f = os.path.join(ROOT, "userdata", "studio", "settings.json")
st = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
api = E.Api(f"http://127.0.0.1:{run['api_port']}", (st.get("api_key") or "").strip() or G.read_key())

prompt = ("Generate exactly one still image now, vertical 9:16, photorealistic portrait photo of a young Bengali man about twenty-five years old: warm brown skin, an oval face, "
          "short neat black hair with faded sides and volume on top, a trimmed short beard and moustache, dark kind eyes. He wears a cream-white cotton kurta with a fine maroon and gold "
          "embroidered collar and placket. He stands facing the camera straight on, framed from the top of the head down to the waist, centred, arms relaxed at his sides, a soft friendly "
          "closed-mouth smile, eyes looking into the lens. Plain smooth light-grey seamless studio background, soft even front light. One complete clean image: the whole head and both "
          "shoulders fully inside the frame, nothing cut by the edges. No text, no letters, no logos, no subtitles, no watermark, no other people, no objects in the hands.")
neg = "text, subtitles, captions, logo, watermark, cropped head, extra people, objects in the hands"
b = api.generate("image", G.muse_image_prompt(prompt, neg, 0), [], f"studio-bengali-hoc-{uuid.uuid4().hex[:6]}", timeout=420, on_status=lambda s, p: print("trạng thái:", s, p, flush=True))
out = os.path.join(HERE, "..", "anh", "nguoi-hoc.png")
open(out, "wb").write(b if isinstance(b, (bytes, bytearray)) else base64.b64decode(b))
print("XONG", os.path.abspath(out))
