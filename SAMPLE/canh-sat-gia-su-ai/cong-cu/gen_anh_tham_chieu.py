"""Gen ảnh tham chiếu nhân vật + ảnh toàn cảnh cố định vị trí cho thể loại canh-sat-gia-su-ai (Muse, qua LUO-API của Studio đang chạy).
Chạy:  .venv\Scripts\python.exe SAMPLE\canh-sat-gia-su-ai\cong-cu\gen_anh_tham_chieu.py [CANHSAT HOC BE DAY TOANCANH]
Ảnh ra: SAMPLE/canh-sat-gia-su-ai/anh/<KHOÁ>.png (khoá cũ tên mặt cắt từ video được dùng làm ảnh tham chiếu đầu vào)."""
import json, os, sys, time, uuid, threading
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path[:0] = [os.path.join(ROOT, "app", "luo-studio"), os.path.join(ROOT, "app", "production")]
import engine as E, gen_video as G  # noqa: E402

ANH = os.path.join(ROOT, "SAMPLE", "canh-sat-gia-su-ai", "anh")
GOC = os.path.join(ANH, "goc-video")   # mặt cắt từ video gốc (làm ảnh mẫu đầu vào)
STYLE = "stylized 3D-animated feature-film look (Pixar-like), warm golden-hour light, clean smooth skin shading"
SHEET = ("Character reference picture: ONE person only, shown from the knees or waist up, standing straight and facing the camera in a three-quarter front view, relaxed neutral friendly face, mouth closed, "
         "arms relaxed at the sides, on a plain flat light-grey studio background. No text, no logo, no lettering anywhere. Vertical 9:16.")
JOBS = {
 "CANHSAT": (SHEET + f" {STYLE}. The person: a young Latina policewoman, dark brown hair pulled into a neat low bun, big brown eyes, a navy short-sleeved police uniform with a plain gold badge and plain shoulder patches without lettering, a black duty belt with a radio. "
            "Copy the face, hair and uniform of the reference image exactly.", "CANHSAT.png"),
 "HOC": (SHEET + f" {STYLE}. The person: a Latino man in his early thirties, short curly black hair, a short black beard, warm brown eyes, a small gold hoop earring, two thin gold chains, a sleeveless cream linen shirt with a faint leaf pattern, wooden bead bracelets on his wrist. "
         "Copy the face, hair and outfit of the reference image exactly.", "HOC.png"),
 "BE": (SHEET + f" {STYLE}. The person: a Latina girl about five years old, very big brown eyes, long thin braids threaded with colourful beads, a pink ruffled sleeveless dress, standing (no car seat shown). "
        "Copy the face, braids and dress of the reference image exactly.", "BE.png"),
 "DAY": (f"Character reference picture: ONE person only, head and shoulders, resting her chin on one hand, friendly confident expression, mouth closed, plain flat black background with soft concentric glowing white sound-wave rings behind her head. {STYLE}. "
         "The person: a young woman with long wavy golden-blonde hair, big warm brown eyes, a navy police-style uniform shirt with small plain patches without lettering. No text, no logo. Landscape 16:9. Copy the face and hair of the reference image exactly.", "DAY.png"),
 "TOANCANH": (f"Create ONE establishing picture, {STYLE}. THE SET (this picture fixes where everyone sits for the whole video): a glossy bright-red four-door sedan stopped on the shoulder of an empty two-lane desert highway at golden hour (dry golden grass, wooden power poles, a blue-and-orange sunset sky). "
              "The camera looks at the car from the FRONT, through the clean windscreen, at bonnet height. In the FRONT ROW, SIDE BY SIDE: the FATHER (Latino man, short curly black hair, short black beard, gold hoop earring, gold chains, sleeveless cream linen shirt, wooden bead bracelets) sits behind the steering wheel on the RIGHT half of the windscreen, hands on the wheel; "
              "the little GIRL (about five, long braids with colourful beads, pink ruffled dress) sits upright in a pink booster child seat on the front passenger seat on the LEFT half of the windscreen, right next to him. The rear seats are empty. "
              "OUTSIDE the car at the far RIGHT, next to the father's open driver's window: the POLICEWOMAN (dark hair in a low bun, navy short-sleeved police uniform with a plain gold badge, black duty belt), standing and leaning toward his window, looking in at him. "
              "Exactly ONE dark police SUV with flashing blue and red lights is parked on the road far behind the red car. Everyone has a closed mouth and a calm expression. Nobody looks into the lens. No text, no logos, no lettering anywhere, no licence plate text.", "TOANCANH.png"),
}
REFS = {"CANHSAT": ["CANHSAT"], "HOC": ["HOC"], "BE": ["BE"], "DAY": ["DAY"], "TOANCANH": ["CANHSAT", "HOC", "BE"]}


def main():
    names = [a for a in sys.argv[1:]] or list(JOBS)
    run = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))
    api = E.Api(f"http://127.0.0.1:{run['api_port']}", G.read_key() or json.load(open(os.path.join(ROOT, "userdata", "studio", "settings.json"), encoding="utf-8")).get("api_key", ""))
    sess = f"refs-{int(time.time())}-{uuid.uuid4().hex[:5]}"
    for k in names:
        prompt, out = JOBS[k]
        refs = []
        for r in REFS[k]:
            p = os.path.join(GOC, r + ".png")
            if os.path.exists(p):
                refs.append(G.data_url(p))
        print(f"[{k}] gen ({len(refs)} ảnh mẫu)...", flush=True)
        asp = "16:9" if k in ("DAY", "TOANCANH") else "9:16"
        b = api.generate("image", G.muse_image_prompt(prompt, "text, letters, logo, watermark, extra people, distorted face", len(refs)), refs, sess, timeout=600, cancel=threading.Event(), aspect=asp)
        open(os.path.join(ANH, out), "wb").write(b)
        print(f"[{k}] -> {out} ({len(b)//1024} KB)", flush=True)

if __name__ == "__main__":
    main()
