"""Gen ảnh tham chiếu bằng Muse qua API của Studio đang chạy: python gen_anh.py dien-gia | robot  (ảnh ra SAMPLE/san-khau-chia-doi-gia-su-ai/anh/)."""
import json, os, sys, uuid, base64
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "app", "luo-studio")); sys.path.insert(0, os.path.join(ROOT, "app", "production"))
import engine as E
G = E.G
ANH = os.path.join(ROOT, "SAMPLE", "san-khau-chia-doi-gia-su-ai", "anh")
run = json.load(open(os.path.join(ROOT, "userdata", "running.json")))
sp = os.path.join(ROOT, "userdata", "studio", "settings.json")
st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
api = E.Api(os.environ.get("LUO_API_URL") or f"http://127.0.0.1:{run['api_port']}", (st.get("api_key") or "").strip() or G.read_key())
which = sys.argv[1]
COMMON = ("vertical 9:16, plain smooth light-grey seamless studio background, soft even front light, standing facing the camera straight on, framed from the top of the head "
          "down to the knees, centred, one complete clean image with nothing cut by the edges. No text, no letters, no logos, no subtitles, no watermark, no other people. ")
if which == "dien-gia":
    prompt = ("Generate exactly one still image now, photorealistic studio portrait photo. " + COMMON +
              "A charismatic Brazilian man in his late fifties, a tanned face with warm laugh lines, swept-back silver-grey hair, a neat short grey beard, warm brown eyes and a "
              "confident closed-mouth smile; a cream linen blazer over a white open-collar shirt, beige chinos and a brown leather belt, a thin black headset microphone along the "
              "left cheek, a small black presentation clicker in the right hand held low, the left arm relaxed. Eyes looking into the lens.")
    refs, out, neg = [], "ai-dien-gia.png", "text, subtitles, logo, watermark, cropped head, extra people, hat"
else:
    prompt = ("Generate exactly one still image now, photorealistic glossy CGI render. " + COMMON +
              "The SAME robot as in the reference image (keep its exact smooth white porcelain face, light-blue eyes, white hexagonal armour plates with thin glowing cyan seams, black cable neck and joints), "
              "now dressed as a street-style tutor: a grey baseball cap on its bald head, black wraparound sunglasses over the eyes, and a dark-grey and black zip-up bomber jacket with a raised collar "
              "worn open over the white chest armour. Both arms relaxed at the sides, mouth closed. Do not copy the reference's halo ring or its bright backdrop.")
    refs, out, neg = [G.data_url(os.path.join(ANH, "robot-goc-nguoi-dung.webp"))], "ai-robot-mu-kinh.png", "text, subtitles, logo, watermark, cropped head, extra people, halo ring"
b = api.generate("image", G.muse_image_prompt(prompt, neg, len(refs)), refs, f"studio-{which}-{uuid.uuid4().hex[:6]}", timeout=900,
                 on_status=lambda s, p: print(which, "trạng thái:", s, p, flush=True))
o = os.path.join(ANH, out)
open(o, "wb").write(b if isinstance(b, (bytes, bytearray)) else base64.b64decode(b))
print("XONG", o)
