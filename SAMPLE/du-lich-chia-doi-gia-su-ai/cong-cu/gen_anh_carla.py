import json, os, sys, time, uuid, base64
ROOT = r"D:\Work\Tools\luo-studio-main\luo-studio-main"
sys.path.insert(0, os.path.join(ROOT, "app", "luo-studio")); sys.path.insert(0, os.path.join(ROOT, "app", "production"))
import engine as E
G = E.G
S = sys.argv[1]
run = json.load(open(os.path.join(ROOT, "userdata", "running.json")))
st = json.load(open(os.path.join(ROOT, "userdata", "studio", "settings.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "userdata", "studio", "settings.json")) else {}
url = os.environ.get("LUO_API_URL") or f"http://127.0.0.1:{run['api_port']}"
key = (st.get("api_key") or "").strip() or G.read_key()
api = E.Api(url, key)
prompt = ("Generate exactly one still image now, vertical 9:16, photorealistic studio portrait photo. The SAME woman as in the reference images "
          "(keep her exact face, skin tone, eyes, eyebrows, smile, and shoulder-length dark brown curly hair with a side part): a Mexican woman in her late thirties. "
          "She wears exactly the outfit from the references: a loose mustard-yellow long coat over a cream button-up blouse, brown trousers. "
          "She stands facing the camera straight on, framed from the top of the head down to the knees, centred, arms relaxed at her sides, a soft friendly closed-mouth smile, "
          "eyes looking into the lens. Plain smooth light-grey seamless studio background, soft even front light. "
          "One complete clean image: the whole head, hair and both shoulders fully inside the frame, nothing cut by the edges. "
          "No text, no letters, no logos, no subtitles, no watermark, no other people, no objects in the hands.")
refs = [G.data_url(os.path.join(S, "in_mat.png")), G.data_url(os.path.join(S, "in_ao.png"))]
b = api.generate("image", G.muse_image_prompt(prompt, "text, subtitles, captions, logo, watermark, cropped head, extra people, mug, cup", len(refs)), refs,
                 f"studio-carla-{uuid.uuid4().hex[:6]}", timeout=900, on_status=lambda s, p: print("trạng thái:", s, p, flush=True))
out = os.path.join(S, "ai-carla.png")
open(out, "wb").write(b if isinstance(b, (bytes, bytearray)) else base64.b64decode(b))
print("XONG", out)
