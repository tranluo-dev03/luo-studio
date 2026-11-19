"""Gen ảnh gốc phần 2 (base_HOC / base_DAY) bằng Muse với bố cục chuẩn, ghi vào thư mục phan2 của lần chạy (Studio dùng lại file có sẵn).
python gen_base.py <thư mục phan2> HOC|DAY   (cần MUSE2API_ENV_FILE=userdata\api\.env nếu settings.api_key trống)"""
import json, os, sys, uuid, base64
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "app", "luo-studio")); sys.path.insert(0, os.path.join(ROOT, "app", "production"))
import engine as E
G = E.G
ANH = os.path.join(ROOT, "SAMPLE", "san-khau-chia-doi-gia-su-ai", "anh")
run = json.load(open(os.path.join(ROOT, "userdata", "running.json")))
sp = os.path.join(ROOT, "userdata", "studio", "settings.json")
st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
api = E.Api(f"http://127.0.0.1:{run['api_port']}", (st.get("api_key") or "").strip() or G.read_key())
out_dir, who = sys.argv[1], sys.argv[2]
COMMON = ("Generate exactly one still image now, vertical 9:16, photorealistic. Locked-off camera, the subject faces the lens STRAIGHT ON, perfectly centred left-right, "
          "the nose on the vertical centre line, shoulders square, mouth closed with a soft friendly expression. The top of the head is at 22% of the frame height and the upper 17% "
          "shows only background. No text, no letters, no logos, no other people. ")
if who == "HOC":
    prompt = (COMMON + "The SAME man as in the reference image (exact face, silver-grey swept-back hair, short grey beard, cream linen blazer over a white open-collar shirt, brown belt, headset microphone "
              "along the left cheek). Framed from above the head down to just below the belt, the body about two thirds of the frame width, arms relaxed, a small black presentation clicker in the right hand held low. "
              "Behind him: a plain deep navy-blue stage curtain with soft vertical folds, softly lit, nothing else.")
    ref, out = "ai-dien-gia.png", "base_HOC.png"
else:
    prompt = (COMMON + "The SAME robot as in the reference image (exact white porcelain face, grey baseball cap, black wraparound sunglasses, black zip-up bomber jacket worn open over white chest armour with cyan seams). "
              "Framed from above the cap down to the waist, shoulders about half of the frame width, both hands out of frame or relaxed low. Behind it: a sunny city park, green trees with soft sunlight, softly out of focus.")
    ref, out = "ai-robot-mu-kinh.png", "base_DAY.png"
refs = [G.data_url(os.path.join(ANH, ref))]
b = api.generate("image", G.muse_image_prompt(prompt, "text, subtitles, logo, watermark, cropped head, turned head, extra people", 1), refs, f"base-{who}-{uuid.uuid4().hex[:6]}", timeout=900)
o = os.path.join(out_dir, out)
open(o, "wb").write(b if isinstance(b, (bytes, bytearray)) else base64.b64decode(b))
print("XONG", o)
