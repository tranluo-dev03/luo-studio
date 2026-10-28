"""LUO Studio - chế độ GHÉP 2 LỚP: mỗi nhân vật được gen RIÊNG (một mình trong khung) rồi ghép lại bằng ffmpeg.

Dùng cho bố cục mà các nhân vật nằm ở vùng tách biệt (vd. gia sư AI trong khung bo góc phía trên, người học quay selfie phía dưới).
Gen chung cả hai trong một clip thì Muse hay để người nghe mấp máy / cả hai cùng nói; gen riêng thì mỗi clip chỉ có MỘT người nên không thể nói chồng.

Mỗi video:
  1. ảnh gốc cho từng nhân vật (một lần): tư thế trung tính, miệng ngậm. MỌI clip của nhân vật đó bắt đầu từ ảnh này nên mặt/màu không trôi qua nhiều cảnh;
  2. thư viện clip NGHE (chế độ "dùng lại"): vài clip im lặng ~10 giây cho mỗi nhân vật có lúc phải nghe; mỗi cảnh lấy một đoạn khác nhau
     (chế độ "mỗi cảnh": gen clip nghe riêng cho từng cảnh, tốn gấp đôi lượt);
  3. mỗi lượt thoại = một cảnh: gen clip người nói -> cắt sát lời như chế độ thường -> lấy đoạn clip nghe dài đúng bằng -> ghép theo bố cục,
     tiếng chỉ lấy từ người nói -> scene<N>_cut.mp4 (Hậu kỳ dùng như cũ).

Script (loại dự án) có khối [GHEP HAI LOP] thay cho các khối CẢNH; mẫu: SAMPLE/Ghep hai lop/KICH-BAN-GHEP-HAI-LOP.txt.
"""
import os, re, shutil, time, unicodedata

import engine as E
import gen_video as G
import make_variants as MV

W, H = 720, 1280
HDR = "GHEP HAI LOP"
ASPECTS = {"9:16": "a vertical 9:16 portrait frame", "16:9": "a horizontal 16:9 widescreen frame", "1:1": "a square 1:1 frame"}
LISTEN_DUR = 10


def is_split(text):
    return bool(re.search(r"^\[" + HDR + r"\]:\s*$", text or "", re.M))


def _plain(s):
    s = unicodedata.normalize("NFD", str(s)).replace("đ", "d").replace("Đ", "D")
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c))).strip().lower()


def parse(text):
    """(cấu hình bố cục, các khối [TÊN]: nội dung). Khoá trong khối [GHEP HAI LOP] viết có dấu hay không dấu đều được."""
    parts = re.split(r"^\[([A-Z0-9 ]+)\]:\s*$", text, flags=re.M)
    blocks = {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}
    cfg = {"bg": None, "panels": {}, "radius": 0.05, "border": ("#FFFFFF", 3), "listen": ("reuse", 3)}
    for ln in blocks.get(HDR, "").splitlines():
        if ":" not in ln:
            continue
        k, v = (x.strip() for x in ln.split(":", 1))
        k = _plain(k)
        nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", v)]
        if k == "nen":
            cfg["bg"] = MV.ck(v)
        elif k.startswith("khung "):
            if len(nums) != 4 or not (0 <= nums[0] < 1 and 0 <= nums[1] < 1 and 0 < nums[2] <= 1 and 0 < nums[3] <= 1):
                raise RuntimeError(f'Dòng "{ln.strip()}": cần 4 số x, y, rộng, cao theo tỉ lệ khung hình (0..1)')
            cfg["panels"][MV.ck(k[6:])] = tuple(nums)
        elif k == "bo goc" and nums:
            cfg["radius"] = nums[0]
        elif k == "vien":   # "#FFFFFF, 3" (màu, độ dày px); "khong" / 0 = không viền
            col = re.search(r"#[0-9A-Fa-f]{6}", v)
            rest = re.findall(r"\d+", v.replace(col.group(0), "") if col else v)
            cfg["border"] = (col.group(0) if col else "#FFFFFF", 0 if "khong" in _plain(v) else int(rest[-1]) if rest else 3)
        elif k == "nghe":
            pv = _plain(v)
            cfg["listen"] = ("scene", 0) if "moi canh" in pv else ("reuse", max(1, min(int(nums[0]) if nums else 3, 6)))
    if not cfg["bg"]:
        raise RuntimeError("Khối [GHEP HAI LOP] thiếu dòng \"nen: <KHOÁ nhân vật làm nền toàn khung>\"")
    if not cfg["panels"]:
        raise RuntimeError("Khối [GHEP HAI LOP] thiếu dòng \"khung <KHOÁ>: x, y, rộng, cao\"")
    return cfg, blocks


def aspect_of(cfg, key):
    """Tỉ lệ gen của nhân vật: nền = 9:16; nhân vật trong khung = tỉ lệ (Muse hỗ trợ) gần nhất với khung."""
    if key not in cfg["panels"]:
        return "9:16"
    _, _, bw, bh = cfg["panels"][key]
    r = (bw * W) / (bh * H)
    return "16:9" if r >= 1.4 else "1:1" if r >= 0.75 else "9:16"


def _who(blocks, key):
    return blocks.get(f"NHAN VAT {key}", "")


def image_prompt(blocks, key, aspect, n_refs, legend):
    body = "\n\n".join(x for x in [blocks.get("STYLE LOCK", ""), _who(blocks, key)] if x)
    ref = (f"\n\nUse the attached reference image{'' if n_refs == 1 else 's'} as visual guidance for faces, outfits and props. THE REFERENCE IMAGES ARE AUTHORITATIVE FOR APPEARANCE: the person must look exactly like their own reference image (face, hair, skin tone, age, clothing); if the description conflicts with it, the reference wins." + (f" REFERENCE IMAGE NOTES: {legend}" if legend else "")) if n_refs else ""
    neg = blocks.get("NEGATIVE", "")
    return ("Create exactly one still image (not a video, not an animation).\n\n"
            f"{body}\n\nThis is the BASE FRAME of this character: exactly ONE person in the frame, nobody else visible. Neutral relaxed resting pose, mouth gently CLOSED, "
            f"calm attentive expression, looking toward the camera. Output {ASPECTS[aspect]} ({aspect}).{ref}"
            + (f"\n\nAvoid: {neg}" if neg else "") + "\n\nFINAL REMINDER: output exactly ONE STILL IMAGE.")


def speak_prompt(blocks, key, v, turn, aspect, dur, fix=""):
    who = MV.ck(turn.get("who"))
    name = v.get(f"TEN_{who}", "") or "the character"
    how = MV.speaker_how(v, turn["who"], turn.get("text", ""), turn.get("emo", ""))
    body = "\n\n".join(x for x in [blocks.get("STYLE LOCK", ""), _who(blocks, key)] if x)
    suffix, neg = blocks.get("VIDEO SUFFIX", ""), blocks.get("NEGATIVE", "")
    p = (f"Create {ASPECTS[aspect]} ({aspect}) video clip, {dur} seconds long. Make ONE NEW, SEPARATE clip: do not extend or stitch any earlier video.\n\n"
         "AUDIO IS REQUIRED: the character's voice, clearly audible, synchronized with the lips. No music, no other voices.\n\n"
         + (f"CORRECTION FOR THIS CLIP (highest priority): {fix}\n\n" if fix else "")
         + f"{body}\n\nThe clip starts exactly from the attached start frame. Exactly ONE person is in the frame: {name}. Nobody else appears or speaks. "
         f"In this clip {name} speaks {how} Accurate lip-sync on every syllable, lively natural facial expression and small head movements while speaking. "
         "As soon as the line is finished, they return to the same neutral resting pose as the start frame, mouth closed, and hold it completely still until the end of the clip."
         + (f"\n\n{suffix}" if suffix else "") + (f"\n\nAvoid: {neg}; a second person; anyone else talking." if neg else "\n\nAvoid: a second person; anyone else talking."))
    return p


def listen_prompt(blocks, key, v, aspect, dur, mood=""):
    name = v.get(f"TEN_{key}", "") or "the character"
    body = "\n\n".join(x for x in [blocks.get("STYLE LOCK", ""), _who(blocks, key)] if x)
    how = blocks.get(f"NGHE {key}", "") or "listening attentively to someone off-screen: small natural blinks, a slight occasional nod, a soft friendly expression"
    neg = blocks.get("NEGATIVE", "")
    return (f"Create {ASPECTS[aspect]} ({aspect}) video clip, {dur} seconds long. Make ONE NEW, SEPARATE clip.\n\n"
            "SILENT CLIP: Return a video with no audio at all: no speech, no music, no sound effects.\n\n"
            f"{body}\n\nThe clip starts exactly from the attached start frame. Exactly ONE person is in the frame: {name}. {name} is LISTENING, not speaking: "
            f"LIPS SEALED the whole clip, the mouth never opens and never moves as if talking. {how}" + (f" Mood: {mood}." if mood else "")
            + " Movements stay small and slow; at the end they are back in the neutral resting pose of the start frame."
            + (f"\n\nAvoid: {neg}; talking; lip movement; mouthing words; a second person." if neg else "\n\nAvoid: talking; lip movement; mouthing words; a second person."))


# ------------------------------------------------------------------ ghép
def _masks(out_dir, w, h, radius, border):
    """PNG mặt nạ bo góc (w x h) và PNG viền (lớn hơn `bw` px mỗi phía). Trả về (mask, viền hoặc None, bw)."""
    from PIL import Image, ImageDraw
    r = max(0, int(radius * W))
    col, bw = border
    mask = os.path.join(out_dir, f"_mask_{w}x{h}_{r}.png")
    if not os.path.exists(mask):
        im = Image.new("L", (w, h), 0)
        ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
        im.save(mask)
    if bw <= 0:
        return mask, None, 0
    edge = os.path.join(out_dir, f"_border_{w}x{h}_{r}_{bw}_{col[1:]}.png")
    if not os.path.exists(edge):
        rgb = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))
        im = Image.new("RGBA", (w + 2 * bw, h + 2 * bw), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle([0, 0, w + 2 * bw - 1, h + 2 * bw - 1], radius=r + bw, fill=rgb + (255,))
        im.save(edge)
    return mask, edge, bw


def _even(x):
    return int(round(x / 2.0)) * 2


def compose(out, dur, layers, audio_src, cfg, out_dir):
    """Ghép một cảnh. layers = [(khoá, file, giây bắt đầu, có lặp không)], phần tử đầu là NỀN; các phần tử sau đặt vào khung của khoá đó. Tiếng lấy từ `audio_src` (index trong layers)."""
    ins, fl = [], []
    for i, (_, path, off, loop) in enumerate(layers):
        ins += (["-stream_loop", "-1"] if loop else []) + (["-ss", f"{off:.3f}"] if off > 0 else []) + ["-i", path]
    base = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1,trim=duration={dur:.3f},setpts=PTS-STARTPTS[l0]"
    fl.append(base)
    cur, img_idx = "l0", len(layers)
    for i, (key, _, _, _) in enumerate(layers[1:], 1):
        bx, by, bw_, bh_ = cfg["panels"][key]
        x, y, w, h = _even(bx * W), _even(by * H), _even(bw_ * W), _even(bh_ * H)
        mask, edge, bw = _masks(out_dir, w, h, cfg["radius"], cfg["border"])
        ins += ["-loop", "1", "-i", mask]
        mi = img_idx
        img_idx += 1
        fl.append(f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30,setsar=1,trim=duration={dur:.3f},setpts=PTS-STARTPTS,format=rgba[p{i}]")
        fl.append(f"[{mi}:v]format=gray,trim=duration={dur:.3f}[m{i}]")
        fl.append(f"[p{i}][m{i}]alphamerge[pm{i}]")
        if edge:
            ins += ["-loop", "1", "-i", edge]
            ei = img_idx
            img_idx += 1
            fl.append(f"[{cur}][{ei}:v]overlay={x - bw}:{y - bw}:shortest=1[e{i}]")
            cur = f"e{i}"
        fl.append(f"[{cur}][pm{i}]overlay={x}:{y}:shortest=1[o{i}]")
        cur = f"o{i}"
    fl.append(f"[{cur}]format=yuv420p[v]")
    fl.append(f"[{audio_src}:a]aresample=44100,atrim=duration={dur:.3f},asetpts=PTS-STARTPTS[a]")
    E.sh_enc(["ffmpeg", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}",
              "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", out])


# ------------------------------------------------------------------ chạy một biến thể
def run_split(vdata, template, out_dir, opts, emit, cancel):
    try:
        text = G.fill_tokens(template, E.variant_values(vdata))
    except SystemExit as e:
        raise RuntimeError(str(e)) from None
    cfg, blocks = parse(text)
    open(os.path.join(out_dir, "script.txt"), "w", encoding="utf-8").write(text)
    luot = [t for t in vdata.get("LUOT", []) if str(t.get("text", "")).strip()]
    if not luot:
        raise RuntimeError("Biến thể chưa có lượt thoại nào")
    keys = [cfg["bg"]] + [k for k in cfg["panels"] if k != cfg["bg"]]
    for t in luot:
        k = MV.ck(t.get("who"))
        if k not in keys:
            raise RuntimeError(f'Lượt thoại của "{t.get("who")}" nhưng bố cục chỉ có {", ".join(keys)} (thêm dòng "khung {k}: ..." vào khối [GHEP HAI LOP])')
    for k in keys:
        if not _who(blocks, k):
            raise RuntimeError(f"Script thiếu khối [NHAN VAT {k}] (mô tả nhân vật {k} khi đứng MỘT MÌNH trong khung)")
    only = opts.get("only")
    if only:
        luot = luot[:only]
    E._TL.cancel = cancel
    api = E.Api(opts["api_url"], opts["api_key"])
    pin, pin_prefer = opts.get("pin"), opts.get("pin_prefer")
    refs = [G.data_url(p) for p in opts.get("refs", []) if p and os.path.exists(p)]
    mode, n_lib = cfg["listen"]
    P = lambda f: os.path.join(out_dir, f)
    emit("scene_init", scenes=[{"n": i + 1, "who": t["who"], "text": t["text"], "state": "wait"} for i, t in enumerate(luot)])
    emit("log", msg=f"Ghép 2 lớp: nền {cfg['bg']}, khung {', '.join(f'{k} ({aspect_of(cfg, k)})' for k in cfg['panels'])}; clip nghe: "
                    + ("gen riêng mỗi cảnh" if mode == "scene" else f"dùng lại {n_lib} clip mỗi nhân vật"))
    acc = {}

    def note_account(acc_id, name, n=None):
        if not acc:
            acc.update(id=acc_id, name=name)
            emit("item", account_id=acc_id, account=name)
            if pin_prefer and acc_id != pin_prefer:
                emit("log", msg=f"Tài khoản cũ của video không dùng được (đang ghim cho video khác hoặc hết hạn mức): chạy tiếp bằng tài khoản {name}", level="warn")
            emit("log", msg=f"Video gen bằng tài khoản {name} (ghim cho mọi cảnh của video)")
        if n:
            emit("scene", n=n, account=name)

    def attempt(label, fn, n=None):
        for i in range(1, opts["retries"] + 2):
            try:
                return fn()
            except E.Cancelled:
                raise
            except Exception as e:  # noqa: BLE001
                emit("log", msg=f"{'Cảnh ' + str(n) if n else 'Chuẩn bị'} {label}: {e}", level="warn")
                if E._QUOTA_RE.search(str(e)):
                    raise E.QuotaExceeded(f"Muse báo hết hạn mức tạo video (giới hạn 24 giờ): {str(e)[:160]}") from None
                if i > opts["retries"]:
                    raise
                if n:
                    emit("scene", n=n, state=label, pct=0, note=f"thử lại {i}/{opts['retries']}")
                time.sleep(4)

    def gen(kind, prompt, start_png, path, aspect, dur=None, n=None, audios=None, state=None, ref_list=None):
        vrefs = [G.data_url(start_png)] if start_png else list(ref_list if ref_list is not None else refs)

        def go():
            b = api.generate(kind, prompt, vrefs, None, duration=dur, timeout=opts["timeout"], aspect=aspect, cancel=cancel, audios=audios,
                             on_status=(lambda s, p: emit("scene", n=n, state=state or kind, pct=p or 0)) if n else None,
                             on_account=lambda a, nm: note_account(a, nm, n), pin=pin, pin_prefer=pin_prefer)
            if kind == "image":
                if G.kind_of(b) == "video":
                    open(path + ".mp4", "wb").write(b)
                    E.grab_frame(path + ".mp4", path)
                    os.remove(path + ".mp4")
                else:
                    open(path, "wb").write(b)
                return
            open(path, "wb").write(b)
            got = E.duration(path)
            if got > 2 * dur + 1:   # Muse trả về chuỗi clip cũ ghép lại: clip mới nằm ở cuối
                tmp = path + ".tail.mp4"
                E.sh(["ffmpeg", "-y", "-sseof", f"-{dur}", "-i", path, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", tmp])
                os.replace(tmp, path)
        attempt(kind, go, n)

    # ảnh/âm thanh tham chiếu gắn trong biến thể: mỗi nhân vật chỉ nhận ảnh của CHÍNH nó (token kết thúc bằng _<KHOÁ>, vd. NGUOI_DAY; token không thuộc nhân vật nào
    # thì dùng chung). Trước đây mọi ảnh gửi cho cả hai nhân vật nên khuôn mặt bị trộn lẫn.
    def owner(token, group):
        t = token.upper()
        return next((c for c in keys if t.endswith("_" + c)), None) or (group.upper() if group.upper() in keys else None)

    att, att_missing = {}, []
    for k in keys:
        att[k] = E.attachments(vdata, opts, keep=lambda tok, grp, k=k: owner(tok, grp) in (None, k), offset=len(refs), missing=att_missing if k == keys[0] else [])
    if att_missing:
        emit("log", msg="CẢNH BÁO: các ảnh/âm thanh tham chiếu sau được gắn vào biến thể nhưng KHÔNG tìm thấy file nên không được gửi: " + "; ".join(att_missing[:6]), level="warn")
    att_auds = E.attachments(vdata, opts)[2]   # mẫu giọng: lọc theo người nói ở từng cảnh (nhóm trường), không cần tách theo nhân vật ở đây

    # 1. ảnh gốc từng nhân vật
    base = {}
    for k in keys:
        base[k] = P(f"base_{k}.png")
        imgs_k, legend_k, _ = att[k]
        emit("log", msg=f"Tham chiếu cho {k}: {len(refs) + len(imgs_k)} ảnh ({len(imgs_k)} gắn trong biến thể)" + ("" if imgs_k or refs else " - chưa gắn ảnh tham chiếu cho nhân vật này"))
        if not os.path.exists(base[k]):
            emit("log", msg=f"Chuẩn bị: gen ảnh gốc cho {k} ({vdata.get('TEN_' + k, k)}, tỉ lệ {aspect_of(cfg, k)})")
            emit("scene", n=1, state="image", pct=0, note=f"ảnh gốc {k}")
            gen("image", image_prompt(blocks, k, aspect_of(cfg, k), len(refs) + len(imgs_k), legend_k), None, base[k], aspect_of(cfg, k), ref_list=list(refs) + list(imgs_k))

    # 2. thư viện clip nghe (chế độ dùng lại): chỉ cho nhân vật có lúc phải nghe
    listeners = [k for k in keys if any(MV.ck(t["who"]) != k for t in luot)]
    lib = {k: [] for k in keys}
    check = bool(opts.get("check_overlap", True))
    if mode == "reuse":
        for k in listeners:
            for i in range(n_lib):
                f = P(f"listen_{k}_{i + 1}.mp4")
                if not os.path.exists(f):
                    emit("log", msg=f"Chuẩn bị: gen clip nghe {i + 1}/{n_lib} cho {k}")
                    emit("scene", n=1, state="video", pct=0, note=f"clip nghe {k} {i + 1}/{n_lib}")
                    _gen_listen(gen, blocks, k, vdata, cfg, base[k], f, LISTEN_DUR, check, emit)
                lib[k].append(f)
    used = {k: 0 for k in keys}

    def listen_take(k, need, n):
        """(file, giây bắt đầu, có lặp) cho đoạn nghe dài `need` giây của nhân vật k ở cảnh n."""
        if mode == "scene":
            f = P(f"scene{n}_listen_{k}.mp4")
            if not os.path.exists(f):
                dur = next((d for d in E.ALLOWED if d >= need + 0.3), E.ALLOWED[-1])
                emit("scene", n=n, state="video", pct=0, note=f"clip nghe {k}")
                _gen_listen(gen, blocks, k, vdata, cfg, base[k], f, dur, check, emit, n=n)
            return f, 0.0, E.duration(f) < need
        c = used[k]
        used[k] += 1
        f = lib[k][c % len(lib[k])]
        L = E.duration(f)
        room = L - need - 0.2
        off = ((c // len(lib[k])) * 2.7) % room if room > 0.1 else 0.0   # cùng clip dùng lại thì lấy đoạn khác
        return f, off, room <= 0

    # 3. từng cảnh
    clips, ref_stats = [], {}
    for i, turn in enumerate(luot):
        n = i + 1
        if cancel.is_set():
            raise E.Cancelled()
        spk = MV.ck(turn["who"])
        cut_f, last_f = P(f"scene{n}_cut.mp4"), P(f"scene{n}_last.png")
        if os.path.exists(cut_f) and os.path.exists(last_f):
            emit("scene", n=n, state="done", pct=100, thumb=os.path.basename(last_f), clip=os.path.basename(cut_f), secs=round(E.duration(cut_f), 1))
            clips.append(cut_f)
            for k in keys:   # giữ thứ tự lấy clip nghe như lần chạy trước
                if k != spk:
                    used[k] += 1
            continue
        syll = G.spoken_syllables(turn["text"])
        dur = G.auto_duration(syll) if syll else 6
        fix = str((opts.get("scene_notes") or {}).get(str(n), "")).strip()
        spk_f, spk_cut, spk_last = P(f"scene{n}_spk.mp4"), P(f"scene{n}_spkcut.mp4"), P(f"scene{n}_spklast.png")
        if os.path.exists(spk_f) and not E.has_audio(spk_f):
            os.remove(spk_f)
        if not os.path.exists(spk_f):
            emit("scene", n=n, state="video", pct=0, dur=dur)
            if fix:
                emit("log", msg=f"Cảnh {n}: gen lại kèm yêu cầu sửa: {fix[:120]}")
            auds = [a for g, a in att_auds if g in (turn.get("who"), "other", "scene")] or None

            def gv():
                gen("video", speak_prompt(blocks, spk, vdata, turn, aspect_of(cfg, spk), dur, fix), base[spk], spk_f, aspect_of(cfg, spk), dur=dur, n=n, audios=auds)
                if not E.has_audio(spk_f):
                    os.remove(spk_f)
                    raise RuntimeError("Muse trả về clip không có tiếng (mất lời thoại)")
            attempt("video", gv, n)
        # cắt sát lời (như chế độ thường)
        emit("scene", n=n, state="cut", pct=100)
        vf_fix = ""
        if opts.get("normalize", True):   # cân màu từng nhân vật về clip đầu tiên của chính nhân vật đó
            c_start, c_end = E.color_stats(spk_f, [0.04, 0.2, 0.4]), E.color_stats(spk_f, [-0.6, -0.35, -0.1])
            ref_stats.setdefault(spk, c_start)
            vf_fix, note = E.color_match(ref_stats[spk], c_start, c_end, E.duration(spk_f))
            if vf_fix:
                emit("log", msg=f"Cảnh {n}: cân màu {spk} ({note})")
        span, margin = None, float(opts.get("cut_margin", 0.3))
        if opts.get("cut", True) and opts.get("precise_cut", True):
            try:
                span = E.interruptible(lambda: E.voice_span(spk_f, turn["text"]), cancel)
            except E.Cancelled:
                raise
            except Exception as ex:  # noqa: BLE001
                emit("log", msg=f"Cảnh {n}: không xác định được mốc lời nói, cắt theo cách thường ({ex})", level="warn")
        info = E.smart_cut(spk_f, spk_cut, spk_last, syll=syll, speedfix=opts.get("speedfix", True), vf_extra=vf_fix, max_speed=float(opts.get("speed_max", 1.25)),
                           span=span, lo=(0.18 if span else 0.15), hi=(max(0.3, margin + 0.05) if span else 0.8), head_margin=margin * 0.7) if opts.get("cut", True) else None
        if info is None:
            shutil.copy(spk_f, spk_cut)
        need = E.duration(spk_cut)
        # lớp của từng nhân vật: người nói = clip vừa cắt, người khác = đoạn clip nghe
        layer = {}
        for k in keys:
            if k == spk:
                layer[k] = (k, spk_cut, 0.0, False)
            else:
                f, off, loop = listen_take(k, need, n)
                layer[k] = (k, f, off, loop)
        order = [cfg["bg"]] + [k for k in cfg["panels"] if k != cfg["bg"]]
        layers = [layer[k] for k in order]
        emit("log", msg=f"Cảnh {n}: {spk} nói {need:.1f}s" + (f" (tăng tốc x{info['speed']})" if info and info["speed"] > 1 else "") + ", ghép với " +
                        ", ".join(f"{k} nghe" for k in order if k != spk))
        compose(cut_f, need, layers, order.index(spk), cfg, out_dir)
        E.grab_frame(cut_f, last_f, sseof=-0.06)
        clips.append(cut_f)
        emit("scene", n=n, state="done", pct=100, thumb=os.path.basename(last_f), clip=os.path.basename(cut_f), secs=round(E.duration(cut_f), 1))
    return E.concat_clips(clips, out_dir, emit)


MOUTH_TALKING = 0.029   # độ lệch chuẩn độ mở miệng: người im lặng thật ~0.008-0.019, mấp máy >= 0.029 (đã đo ở chế độ thường)


def _mouth_score(path):
    try:
        m = E.mouth_activity(path, "0,0,1,1", E.duration(path))
        return m[0] if m else None
    except Exception:  # noqa: BLE001 - máy không chạy được đo miệng (mediapipe lỗi): bỏ qua
        return None


def _gen_listen(gen, blocks, k, vdata, cfg, base_png, f, dur, check, emit, n=None):
    """Gen một clip nghe; nếu đo được miệng cử động như đang nói thì gen lại một lần và giữ bản ít cử động hơn."""
    aspect = aspect_of(cfg, k)
    gen("video", listen_prompt(blocks, k, vdata, aspect, dur), base_png, f, aspect, dur=dur, n=n, state="video")
    s0 = _mouth_score(f) if check else None
    if s0 is None or s0 < MOUTH_TALKING:
        return
    emit("log", msg=f"Clip nghe của {k}: miệng cử động như đang nói (mức {s0:.3f}), gen lại", level="warn")
    tmp = f + ".try.mp4"
    gen("video", listen_prompt(blocks, k, vdata, aspect, dur), base_png, tmp, aspect, dur=dur, n=n, state="video")
    s1 = _mouth_score(tmp)
    if s1 is not None and s1 < s0:
        os.replace(tmp, f)
    else:
        os.remove(tmp)
