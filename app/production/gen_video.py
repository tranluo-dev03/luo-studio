#!/usr/bin/env python
"""Gen video nhiều cảnh bằng LUO-API, KHÔNG cần giao diện luo-flow (bản 2: nói nhanh, biểu cảm, nói xong đứng im).

Hai chế độ:

A) SCRIPT NODE + BIẾN THỂ (khuyên dùng, giống hệt chế độ 2b của luo-flow):
   python gen_video.py --nodes split-turns-nodes.txt --variants variants/langlearn-turns.json --out out/run1 \
       [--variant ten|all] [--ref1 refs/a.png --ref2 refs/b.png] [--only 2] [--dry-run]
   Token {{...}} trong script được thay bằng giá trị của biến thể (LUOT_n do make_variants.turn_text sinh).
   Cảnh có "Prompt ảnh" -> tạo ảnh khung đầu (kèm --ref1/--ref2 nếu có) rồi video; cảnh không có ảnh -> video
   lấy khung cuối clip trước làm tham chiếu (như dây endFrame -> reference trên canvas).

B) MASTER TEMPLATE + KỊCH BẢN NỘI DUNG (giống Batch mục 1 của luo-flow):
   python gen_video.py --master ../luo-flow/templates/master-split-dialogue.txt \
       --content ../luo-flow/templates/scripts/dialogue-langlearn.txt \
       --ref1 refs/ref1_tutor_robot.png --ref2 refs/ref2_learner_girl.png --out out/run1 [--dry-run] [--only 1]
   Mỗi cảnh: ảnh khung đầu (ref1, ref2, + khung cuối cảnh trước) rồi video (ảnh khung đầu làm tham chiếu).

Mỗi clip xong được cắt phần im lặng đầu và đuôi đứng im ngay (giữ --lead giây trước khi nói, --settle giây sau khi
hết lời; tắt bằng --no-trim) rồi ghép thành raw.mp4. Khung cuối nối sang cảnh sau lấy từ clip gốc (khung đứng im).
API key đọc từ ../luo-muse-api/.env (MUSE2API_KEY) hoặc biến môi trường MUSE2API_KEY; không in ra.
Chạy lại cùng --out thì bỏ qua các bước đã xong (resume).
"""
import argparse, base64, json, mimetypes, os, re, shutil, subprocess, sys, time, urllib.request, urllib.error

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED_DURATIONS = [5, 6, 8, 10]


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode:
        raise RuntimeError(f"{cmd[0]} lỗi: {r.stderr[-800:]}")
    return r


# ---------------------------------------------------------------- script parsing (cổng của parseSceneScript)
LOCKS = ["STYLE LOCK", "CHAR LOCK", "SET LOCK", "VIDEO SUFFIX", "NEGATIVE"]
FIELDS = ["Bối cảnh", "Voice", "Khung đầu", "Khung cuối", "Diễn biến", "Prompt ảnh", "Prompt video", "Audio", "Negative prompt"]


def parse_script(text):
    head = re.compile(r"^CẢNH (\d+) \(([^)]*)\): (.*)$", re.M)
    ms = list(head.finditer(text))
    pre = text[: ms[0].start()]
    locks = {}
    parts = re.split(r"^\[([A-Z ]+)\]:\s*$", pre, flags=re.M)
    for i in range(1, len(parts), 2):
        locks[parts[i].strip()] = parts[i + 1].strip()
    scenes = []
    for i, m in enumerate(ms):
        body = text[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(text)]
        f = {}
        pat = re.compile(r"^(" + "|".join(re.escape(x) for x in FIELDS) + r")(?:\s*\([^)]*\))?\s*:\s*", re.M)
        fm = list(pat.finditer(body))
        for j, x in enumerate(fm):
            f[x.group(1)] = body[x.end(): fm[j + 1].start() if j + 1 < len(fm) else len(body)].strip()
        rng = re.search(r"(\d+):(\d{2})\s*[–—-]\s*(\d+):(\d{2})", m.group(2))
        secs = (int(rng.group(3)) * 60 + int(rng.group(4))) - (int(rng.group(1)) * 60 + int(rng.group(2))) if rng else 6
        scenes.append({"n": int(m.group(1)), "title": m.group(3).strip(), "f": f, "seconds": secs if secs > 0 else 6})
    return locks, scenes


def with_ctx(prompt, ctx):
    parts = [c for c in ctx if c and c not in prompt]
    return "\n\n".join(parts + [prompt]).strip()


def build_prompts(locks, sc):
    f = sc["f"]
    ctx = [locks.get("SET LOCK", ""), locks.get("CHAR LOCK", ""), locks.get("STYLE LOCK", "")]
    img = with_ctx(f.get("Prompt ảnh", ""), ctx)
    opening = f.get("Khung đầu", "")
    if opening and opening.lower() not in img.lower():
        img += f"\n\nOpening frame composition: {opening}"
    vid = with_ctx(f.get("Prompt video", ""), ctx)
    voice = f.get("Voice", "")
    audio = f.get("Audio", "")
    details = [
        f"Timed action beats:\n{f['Diễn biến']}" if f.get("Diễn biến") else "",
        f"Final frame to reach: {f['Khung cuối']}" if f.get("Khung cuối") else "",
        f"Spoken dialogue (required; the character says this on camera with accurate lip-sync): {voice}" if voice else "",
        f"Audio direction: {audio}{'' if voice else '. No speech.'}" if audio else "",
    ]
    vid = "\n\n".join([vid] + [d for d in details if d])
    suffix = locks.get("VIDEO SUFFIX", "")
    if suffix and suffix not in vid:
        vid += "\n\n" + suffix
    neg = "; ".join(x for x in [locks.get("NEGATIVE", ""), f.get("Negative prompt", "")] if x)
    return img, vid, neg


SIZE = "9:16"
SIZE_NOTE = f"Output aspect ratio: {SIZE}. Match this frame shape exactly. Use a tall portrait composition."


def muse_image_prompt(prompt, neg, n_refs):
    ref = ("\n\nUse the attached reference image" + ("" if n_refs == 1 else "s") + " as visual guidance; follow the prompt while preserving relevant subject details. "
           "THE REFERENCE IMAGES ARE AUTHORITATIVE FOR APPEARANCE: each person in the picture must have the face, hair, skin tone, age and clothing of THEIR OWN reference image "
           "(see the reference image notes); if the written description conflicts with a reference image, the reference image wins. Never blend two people's references into one face.") if n_refs else ""
    return ("Create exactly one still image. This is an image-generation request, not a video request. Do not create a video, animation, or sequence of frames. "
            "The text below may mention voice, dialogue, motion, clips or timing — those are notes for a later video step: IGNORE them and only render the single opening frame as a still picture.\n\n"
            f"{prompt}{ref}\n\n{SIZE_NOTE}" + (f"\n\nAvoid the following (negative prompt): {neg}" if neg else "")
            + "\n\nFINAL REMINDER: output exactly ONE STILL IMAGE (not a video, not an animation).")


def muse_video_prompt(prompt, neg, dur, n_refs):
    # chỉ coi là clip câm khi prompt nói rõ CẢ CLIP không có âm thanh ("the silent character", "makes no sound" KHÔNG tính)
    silent = re.search(r"(?:\bSILENT CLIP\b|\bsilent (?:video|clip)\b|\bno audio at all\b|\bwithout any (?:audio|sound)\b|\bmuted (?:video|clip)\b)", prompt, re.I)
    audio = ("SILENT CLIP: Return a video with no audio at all: no speech, no music, no sound effects." if silent else
             "AUDIO IS REQUIRED: Return a video with audible, synchronized sound; do not make a silent clip. Follow the requested audio direction exactly and make every requested sound clearly audible; if it says no music or speech only, add no music. Do not add spoken dialogue unless the prompt asks for it.")
    ref = ("\n\nUse the attached reference image" + ("" if n_refs == 1 else "s") + " as visual guidance.") if n_refs else ""
    single = (f"Make ONE NEW, SEPARATE clip of exactly {dur} seconds. Starting from the given start frame is fine, but do NOT extend, combine, merge or stitch any earlier video from this chat: "
              "the output must contain only this new clip, never the previous clips joined together.")
    return (f"Create a {SIZE} aspect ratio video clip, {dur} seconds long. {SIZE_NOTE} {single}\n\n{audio}{ref}\n\nPrompt: {prompt}"
            + (f"\n\nAvoid: {neg}" if neg else ""))


# ---------------------------------------------------------------- API
class Api:
    def __init__(self, url, key):
        self.url, self.key = url.rstrip("/"), key

    def req(self, path, body=None, method=None):
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(self.url + path, data=data, method=method or ("POST" if body is not None else "GET"))
        if self.key:
            r.add_header("Authorization", f"Bearer {self.key}")
        if data:
            r.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                return json.loads(resp.read().decode() or "null")
        except urllib.error.HTTPError as e:
            raise ApiError(e.code, e.read().decode(errors="replace")[:300])
        except urllib.error.URLError as e:
            raise RuntimeError(f"Không kết nối được LUO-API {self.url}: {e}")

    def download(self, url):
        if url.startswith("/"):
            url = self.url + url
        r = urllib.request.Request(url)
        if self.key and url.startswith(self.url):
            r.add_header("Authorization", f"Bearer {self.key}")
        with urllib.request.urlopen(r, timeout=300) as resp:
            return resp.read()

    def generate(self, kind, prompt, refs, session, duration=None, timeout=600, log=print):
        body = {"prompt": prompt, "model": "muse-video" if kind == "video" else "muse-image", "aspect_ratio": SIZE,
                "raw_prompt": True, "timeout": min(int(timeout), 600), "session": session}  # API nhận tối đa 600s; thời gian chờ phía app (deadline) vẫn theo `timeout`
        if kind == "video":
            body["duration"] = duration
        if refs:
            body["reference_images"] = refs
        path = "/v1/videos" if kind == "video" else "/v1/images/tasks"
        deadline = time.time() + timeout
        while True:
            try:
                task = self.req(path, body)
                break
            except ApiError as e:
                if e.code == 429 and time.time() < deadline:
                    time.sleep(5)
                    continue
                raise
        tid = task.get("task_id") or task.get("id")
        log(f"    task {tid} đã nhận")
        last = ""
        while True:
            time.sleep(3)
            st = self.req(f"{path}/{tid}")
            s = st.get("status")
            if s != last:
                last = s
                log(f"    {kind}: {s}{'' if st.get('progress') is None else ' ' + str(st['progress']) + '%'}")
            if s == "completed":
                url = st.get("url") or (st.get("video") or {}).get("url") or (st.get("result") or {}).get("url") or ((st.get("data") or [{}])[0]).get("url")
                if not url:
                    raise RuntimeError("API không trả về địa chỉ file")
                return self.download(url)
            if s in ("failed", "error"):
                raise RuntimeError(str(st.get("error") or "API báo lỗi"))
            if time.time() > deadline:
                raise RuntimeError("Hết thời gian chờ")


class ApiError(Exception):
    def __init__(self, code, msg):
        super().__init__(f"HTTP {code}: {msg}")
        self.code = code


def read_key():
    k = os.environ.get("MUSE2API_KEY", "").strip()
    if k:
        return k
    # bản đóng gọn: .env của API nằm trong thư mục dữ liệu người dùng (MUSE2API_ENV_FILE hoặc MUSE2API_HOME/.env)
    cands = [os.environ.get("MUSE2API_ENV_FILE", ""), os.path.join(os.environ.get("MUSE2API_HOME", ""), ".env") if os.environ.get("MUSE2API_HOME") else "",
             os.path.join(HERE, "..", "luo-muse-api", ".env")]
    for env in cands:
        if env and os.path.exists(env):
            for line in open(env, encoding="utf-8", errors="replace"):
                m = re.match(r"\s*MUSE2API_KEY\s*=\s*(\S+)", line)
                if m:
                    return m.group(1).strip("'\"")
    return ""


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def kind_of(b):
    if b[4:8] == b"ftyp" or b[:4] == b"\x1aE\xdf\xa3":
        return "video"
    return "image"


def with_retries(fn, tries, label):
    for i in range(1, tries + 1):
        try:
            return fn()
        except Exception as e:
            print(f"    ✗ {label} lần {i}/{tries}: {e}")
            if i == tries:
                raise
            time.sleep(5)


def silences(path, noise="-35dB", dmin=0.25):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={noise}:d={dmin}", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return st, en


def clip_duration(path):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout)


def trim_clip(src, dst, settle=0.5, lead=0.12):
    """Cắt phần im lặng đầu clip (giữ `lead` giây) và đuôi đứng im (giữ `settle` giây sau khi hết lời)."""
    total = clip_duration(src)
    st, en = silences(src)
    a, b = 0.0, total
    if st and st[0] <= 0.05 and en:                                  # im lặng ngay từ đầu clip
        a = max(0.0, en[0] - lead)
    if st and (len(en) < len(st) or en[-1] >= total - 0.05):         # im lặng kéo tới hết clip
        b = min(total, st[-1] + settle)
    if b - a < 0.8 or (a < 0.05 and b > total - 0.05):
        shutil.copy(src, dst)
        return total
    sh(["ffmpeg", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src, "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", dst])
    return b - a


TOKEN = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


def fill_tokens(text, values):
    # Thay nhiều lượt: giá trị của biến thể có thể nhắc tới token khác (vd. DAO_GIU = "... in {{TEN_LX}}'s hand ..."); giới hạn số lượt để token tự tham chiếu không lặp mãi
    out = text
    for _ in range(5):
        nxt = TOKEN.sub(lambda m: values.get(m.group(1).upper(), m.group(0)), out)
        if nxt == out:
            break
        out = nxt
    left = sorted(set(TOKEN.findall(out)))
    if left:
        sys.exit("Script còn token chưa có giá trị trong biến thể: " + ", ".join(left))
    return out


def variant_values(v):
    sys.path.insert(0, HERE)
    import make_variants as MV
    vals = {k: x for k, x in v.items() if isinstance(x, str) and k.isupper()}
    for i, item in enumerate(v.get("LUOT", []), 1):
        vals[f"LUOT_{i}"] = MV.turn_text(v, item["who"], item["text"], item.get("emo", ""))
    for i, item in enumerate(v.get("THOAI", []), 1):
        vals[f"THOAI_{i}"] = item
    return vals


def spoken_syllables(voice):
    """Đếm âm tiết của phần lời nói thật (trong ngoặc kép) của một lượt."""
    said = " ".join(re.findall(r'"([^"]+)"', voice or ""))
    n = 0
    for w in re.findall(r"[A-Za-z']+", said.lower()):
        w = w.replace("'", "")
        c = len(re.findall(r"[aeiouy]+", w))
        if w.endswith("e") and c > 1 and not re.search(r"(le|me|ne|re|de|te|se|ge|ve|ce)$", w):
            c -= 1
        n += max(1, c)
    return n


def auto_duration(syll):
    """Nhịp nhanh ~4 âm tiết/giây + 1–1,5s đứng im: ≤14 -> 5s, ≤20 -> 6s, ≤28 -> 8s, còn lại 10s."""
    return 5 if syll <= 14 else 6 if syll <= 20 else 8 if syll <= 28 else 10


def run_one(locks, scenes, out, api, a, refs):
    """Gen một video. scenes đã thay token; refs = data URL ảnh tham chiếu cho ảnh khung đầu (có thể rỗng)."""
    os.makedirs(out, exist_ok=True)
    session = f"gv-{os.path.basename(out)}-{int(time.time())}"[:120]
    prev_last = None
    clips = []
    for sc in scenes:
        n = sc["n"]
        has_img = bool(sc["f"].get("Prompt ảnh"))
        img_p, vid_p, neg = build_prompts(locks, sc)
        dur = next((d for d in ALLOWED_DURATIONS if d >= sc["seconds"]), 10)
        syll = spoken_syllables(sc["f"].get("Voice", ""))
        if syll and not a.keep_duration:
            dur = auto_duration(syll)
        refs_img = list(refs) + ([data_url(prev_last)] if prev_last else [])
        n_vref = 1 if (has_img or prev_last or (a.dry_run and n > 1)) else 0
        if has_img:
            open(os.path.join(out, f"scene{n}_image_prompt.txt"), "w", encoding="utf-8").write(muse_image_prompt(img_p, neg, len(refs_img)))
        open(os.path.join(out, f"scene{n}_video_prompt.txt"), "w", encoding="utf-8").write(muse_video_prompt(vid_p, neg, dur, n_vref))
        print(f"\n=== CẢNH {n}: {sc['title']} ({dur}s, {'ảnh khung đầu + video' if has_img else 'video nối khung cuối'}) ===")
        if a.dry_run:
            print("  (dry-run) prompt đã ghi vào", out)
            continue
        img_file = os.path.join(out, f"scene{n}_start.png")
        vid_file = os.path.join(out, f"scene{n}_clip.mp4")
        cut_file = os.path.join(out, f"scene{n}_cut.mp4")
        last_file = os.path.join(out, f"scene{n}_last.png")
        if has_img and not os.path.exists(img_file):
            print("  → ảnh khung đầu")

            def gen_img():
                b = api.generate("image", muse_image_prompt(img_p, neg, len(refs_img)), refs_img, session, timeout=a.timeout, log=print)
                if kind_of(b) == "video":  # Muse trả video cho node ảnh: lấy khung đầu
                    tmp = img_file + ".mp4"
                    open(tmp, "wb").write(b)
                    sh(["ffmpeg", "-y", "-i", tmp, "-vf", "scale=flags=accurate_rnd+full_chroma_int:out_range=pc,format=rgb24", "-frames:v", "1", img_file])
                    os.remove(tmp)
                else:
                    open(img_file, "wb").write(b)
            with_retries(gen_img, a.retries + 1, "ảnh")
        elif has_img:
            print("  ✓ ảnh khung đầu đã có")
        if not os.path.exists(vid_file):
            print("  → video")
            vrefs = [data_url(img_file)] if has_img else ([data_url(prev_last)] if prev_last else [])

            def gen_vid():
                b = api.generate("video", muse_video_prompt(vid_p, neg, dur, len(vrefs)), vrefs, session, duration=dur, timeout=a.timeout, log=print)
                open(vid_file, "wb").write(b)
            with_retries(gen_vid, a.retries + 1, "video")
        else:
            print("  ✓ video đã có")
        # khung cuối lấy từ clip GỐC: chính là khung đứng im mà clip sau bắt đầu từ đó
        sh(["ffmpeg", "-y", "-sseof", "-0.12", "-i", vid_file, "-vf", "scale=flags=accurate_rnd+full_chroma_int:out_range=pc,format=rgb24", "-frames:v", "1", "-update", "1", last_file])
        prev_last = last_file
        if a.no_trim:
            clips.append(vid_file)
        else:
            d = trim_clip(vid_file, cut_file, a.settle, a.lead)
            print(f"  ✂ cắt im lặng đầu/đuôi: {clip_duration(vid_file):.1f}s -> {d:.1f}s")
            clips.append(cut_file)
        print(f"  ✔ xong cảnh {n}")

    if a.dry_run or not clips:
        return
    try:
        api.req(f"/v1/sessions/{session}", method="DELETE")
    except Exception:
        pass
    final = os.path.join(out, "raw.mp4")
    ins, fl = [], ""
    for i, c in enumerate(clips):
        ins += ["-i", c]
        fl += f"[{i}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v{i}];[{i}:a]aresample=44100[a{i}];"
    fl += "".join(f"[v{i}][a{i}]" for i in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=1[v][a]"
    sh(["ffmpeg", "-y"] + ins + ["-filter_complex", fl, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", final])
    print(f"\nXONG -> {final} ({clip_duration(final):.1f}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nodes", help="chế độ A: script node có token (split-turns-nodes.txt, talka-phone-nodes.txt...)")
    ap.add_argument("--variants", help="chế độ A: file JSON biến thể (giống đầu vào của make_variants.py)")
    ap.add_argument("--variant", help="chế độ A: tên biến thể cần chạy, hoặc 'all' (mặc định: biến thể đầu tiên)")
    ap.add_argument("--master", help="chế độ B: master template")
    ap.add_argument("--content", help="chế độ B: kịch bản nội dung")
    ap.add_argument("--ref1", help="REFERENCE IMAGE 1 (người dạy): bắt buộc ở chế độ B, tuỳ chọn ở chế độ A")
    ap.add_argument("--ref2", help="REFERENCE IMAGE 2 (người học): bắt buộc ở chế độ B, tuỳ chọn ở chế độ A")
    ap.add_argument("--out", required=True)
    ap.add_argument("--api", default="http://127.0.0.1:18610")
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=900, help="giây chờ tối đa cho mỗi ảnh/video (Muse đôi khi kẹt ở 92%% rất lâu)")
    ap.add_argument("--only", type=int, help="chỉ chạy tới cảnh số N (ví dụ 2 để thử 2 cảnh đầu)")
    ap.add_argument("--dry-run", action="store_true", help="chỉ sinh prompt ra file, không gọi API")
    ap.add_argument("--no-trim", action="store_true", help="không cắt im lặng đầu/đuôi từng clip")
    ap.add_argument("--keep-duration", action="store_true", help="dùng đúng độ dài ghi trong tiêu đề cảnh thay vì tự tính theo số âm tiết lời nói")
    ap.add_argument("--settle", type=float, default=0.5, help="giây giữ lại sau khi hết lời (nhân vật về tư thế nghỉ), mặc định 0.5")
    ap.add_argument("--lead", type=float, default=0.12, help="giây giữ lại trước khi bắt đầu nói, mặc định 0.12")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    api = Api(a.api, read_key())

    if a.nodes:
        if not a.variants:
            sys.exit("Chế độ script node cần --variants")
        raw = open(a.nodes, encoding="utf-8").read()
        data = json.load(open(a.variants, encoding="utf-8"))
        if a.variant == "all":
            chosen = data
        else:
            chosen = [v for v in data if v["name"] == a.variant] if a.variant else data[:1]
            if not chosen:
                sys.exit(f"Không có biến thể '{a.variant}'. Có: {', '.join(v['name'] for v in data)}")
        refs = [data_url(x) for x in (a.ref1, a.ref2) if x]
        for v in chosen:
            text = fill_tokens(raw, variant_values(v))
            locks, scenes = parse_script(text)
            for k in LOCKS:
                if k not in locks:
                    sys.exit(f"Thiếu khối [{k}] trong script node")
            n_luot = len(v.get("LUOT", []))
            if n_luot and n_luot != len(scenes):
                sys.exit(f"{v['name']}: có {n_luot} lượt nhưng script có {len(scenes)} cảnh")
            if a.only:
                scenes = [s for s in scenes if s["n"] <= a.only]
            vout = os.path.join(out, v["name"]) if len(chosen) > 1 else out
            os.makedirs(vout, exist_ok=True)
            open(os.path.join(vout, "script.txt"), "w", encoding="utf-8").write(text)
            print(f"\n##### Biến thể {v['name']}: {len(scenes)} cảnh -> {vout}")
            run_one(locks, scenes, vout, api, a, refs)
        return

    if not (a.master and a.content and a.ref1 and a.ref2):
        sys.exit("Cần --nodes + --variants (chế độ A) hoặc --master + --content + --ref1 + --ref2 (chế độ B)")
    script_path = os.path.join(out, "script.txt")
    print(sh(["node", os.path.join(HERE, "compose_cli.js"), a.master, a.content, script_path]).stdout.strip())
    locks, scenes = parse_script(open(script_path, encoding="utf-8").read())
    for k in LOCKS:
        if k not in locks:
            sys.exit(f"Thiếu khối [{k}] trong kịch bản đã ghép")
    if a.only:
        scenes = [s for s in scenes if s["n"] <= a.only]
    run_one(locks, scenes, out, api, a, [data_url(a.ref1), data_url(a.ref2)])


if __name__ == "__main__":
    main()
