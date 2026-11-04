"""LUO Studio - chế độ GHÉP 2 LỚP: mỗi nhân vật được gen RIÊNG (một mình trong khung) rồi ghép lại bằng ffmpeg.

Dùng cho bố cục mà các nhân vật nằm ở vùng tách biệt (vd. gia sư AI trong khung bo góc phía trên, người học quay selfie phía dưới).
Gen chung cả hai trong một clip thì Muse hay để người nghe mấp máy / cả hai cùng nói; gen riêng thì mỗi clip chỉ có MỘT người nên không thể nói chồng.

Mỗi video:
  1. ảnh gốc cho từng nhân vật (một lần): tư thế trung tính, miệng ngậm. MỌI clip của nhân vật đó bắt đầu từ ảnh này nên mặt/màu không trôi qua nhiều cảnh;
  2. thư viện clip NGHE (chế độ "dùng lại"): vài clip im lặng ~10 giây cho mỗi nhân vật có lúc phải nghe; mỗi cảnh lấy một đoạn khác nhau
     (chế độ "mỗi cảnh": gen clip nghe riêng cho từng cảnh, tốn gấp đôi lượt);
  3. mỗi lượt thoại = một cảnh: gen clip người nói -> cắt sát lời như chế độ thường -> lấy đoạn clip nghe dài đúng bằng -> ghép theo bố cục,
     tiếng chỉ lấy từ người nói -> scene<N>_cut.mp4 (Hậu kỳ dùng như cũ).

Script (loại dự án) có khối [GHEP HAI LOP] thay cho các khối CẢNH; mẫu: SAMPLE/ghep-hai-lop/KICH-BAN-GHEP-HAI-LOP.txt.
"""
import os, re, shutil, time, unicodedata

import engine as E
import gen_video as G
import make_variants as MV

W, H = 720, 1280
HDR = "GHEP HAI LOP"
ASPECTS = {"9:16": "a vertical 9:16 portrait frame", "16:9": "a horizontal 16:9 widescreen frame", "1:1": "a square 1:1 frame"}
LISTEN_DUR = 10
MORPH_DUR = 0.24   # giây; mỗi cảnh ghép bắt đầu lại từ ảnh gốc nên tư thế nhảy ở chỗ nối -> chèn đoạn chuyển mượt ngắn (optical flow)


def is_split(text):
    return bool(re.search(r"^\[" + HDR + r"\]:\s*$", text or "", re.M))


def _plain(s):
    s = unicodedata.normalize("NFD", str(s)).replace("đ", "d").replace("Đ", "D")
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c))).strip().lower()


def parse(text):
    """(cấu hình bố cục, các khối [TÊN]: nội dung). Khoá trong khối [GHEP HAI LOP] viết có dấu hay không dấu đều được."""
    parts = re.split(r"^\[([A-Z0-9 ]+)\]:\s*$", text, flags=re.M)
    blocks = {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}
    cfg = {"bg": None, "panels": {}, "radius": 0.05, "border": ("#FFFFFF", 3), "listen": ("reuse", 3), "join": ("chain", 0), "refresh": 0, "lock": False}
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
            if nums[0] + nums[2] > 1.001 or nums[1] + nums[3] > 1.001:
                raise RuntimeError(f'Dòng "{ln.strip()}": khung vượt ra ngoài video (x+rộng = {nums[0] + nums[2]:.2f}, y+cao = {nums[1] + nums[3]:.2f}, phải <= 1). '
                                   'Định dạng là x, y, RỘNG, CAO (không phải toạ độ hai góc). Nếu bạn muốn khung từ góc '
                                   f'({nums[0]:g}, {nums[1]:g}) tới ({nums[2]:g}, {nums[3]:g}) thì viết: '
                                   f'{nums[0]:g}, {nums[1]:g}, {nums[2] - nums[0]:.2f}, {nums[3] - nums[1]:.2f}')
            cfg["panels"][MV.ck(k[6:])] = tuple(nums)
        elif k == "bo goc" and nums:
            cfg["radius"] = nums[0]
        elif k == "vien":   # "#FFFFFF, 3" (màu, độ dày px); "khong" / 0 = không viền
            col = re.search(r"#[0-9A-Fa-f]{6}", v)
            rest = re.findall(r"\d+", v.replace(col.group(0), "") if col else v)
            cfg["border"] = (col.group(0) if col else "#FFFFFF", 0 if "khong" in _plain(v) else int(rest[-1]) if rest else 3)
        elif k == "noi":   # chỗ nối giữa các cảnh: "lien" (mặc định) = clip sau của mỗi nhân vật bắt đầu từ khung cuối clip trước của chính nó;
            pv = _plain(v)     # "morph [giây]" = vẫn bắt đầu từ ảnh gốc, chèn hình chuyển mượt ở chỗ nối; "cat" = bắt đầu từ ảnh gốc, cắt thẳng
            cfg["join"] = ("cut", 0) if "cat" in pv else ("morph", min(0.5, max(0.1, nums[0])) if nums else MORPH_DUR) if "morph" in pv else ("chain", 0)
        elif k == "lam moi":   # nối khung: cứ N cảnh gen lại khung nối thành ảnh sạch (giữ tư thế, lấy mặt/da từ ảnh gốc); 0 = tắt
            cfg["refresh"] = int(nums[0]) if nums else 0
        elif k == "khoa mieng":   # clip nghe gen bằng Muse: dán vùng môi khép lên từng khung, mặc định TẮT (môi trông cứng; gốc lỗi đã sửa ở prompt nghe); "co" = bật
            cfg["lock"] = "khong" not in _plain(v) and ("co" in _plain(v).split() or "bat" in _plain(v))
        elif k == "nghe":
            pv = _plain(v)
            cfg["listen"] = ("still", 0) if ("tinh" in pv or "dung yen" in pv) else ("scene", 0) if "moi canh" in pv else ("reuse", max(1, min(int(nums[0]) if nums else 3, 6)))
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


_SPEAK_RE = re.compile(r"\b(speak\w*|talk\w*|voice\w*|says?|said|speech|sync\w*|accent|timbre|pitch|loudness|mouth\w*|monoton\w*|robotic|echo|reverb)\b", re.I)


def _no_speech(text, sep=None):
    """Bỏ mọi câu (hoặc mục cách nhau bằng `sep`) nói về lời nói / giọng / khẩu hình. Khối [NHAN VAT] viết cho lúc NÓI ("while speaking… VOICE: …",
    "moves its lips in clear sync with the words"); chèn nguyên vào prompt NGHE thì Muse làm theo và cho người nghe nhép miệng (03/11/2026)."""
    parts = [x.strip() for x in text.split(sep)] if sep else re.split(r"(?<=[.!?])\s+", text.strip())
    keep = [x for x in parts if x and not _SPEAK_RE.search(x)]
    return re.sub(r"\bexpressive lips\b", "lips", (sep + " ").join(keep) if sep else " ".join(keep))


def listen_prompt(blocks, key, v, aspect, dur, mood="", strict=False):
    name = v.get(f"TEN_{key}", "") or "the character"
    body = "\n\n".join(x for x in [_no_speech(blocks.get("STYLE LOCK", "")), _no_speech(_who(blocks, key))] if x)
    how = blocks.get(f"NGHE {key}", "") or "listening attentively to someone off-screen and visibly reacting: natural blinks, nods along, raised eyebrows, a soft smile, small head tilts"
    neg = _no_speech(blocks.get("NEGATIVE", ""), ";")
    return (f"Create {ASPECTS[aspect]} ({aspect}) video clip, {dur} seconds long. Make ONE NEW, SEPARATE clip.\n\n"
            "SILENT CLIP: Return a video with no audio at all: no speech, no music, no sound effects.\n\n"
            f"{body}\n\nThe clip starts exactly from the attached start frame. Exactly ONE person is in the frame: {name}. {name} is LISTENING, not speaking: "
            f"LIPS SEALED the whole clip, the mouth never opens and never moves as if talking; if the lips are slightly parted in the start frame they close in the first instant "
            f"and stay closed. {how}" + (f" Mood: {mood}." if mood else "")
            + (" RETRY: the previous attempt looked like talking. This time the head stays still, facing the same way as in the start frame, no glancing away, "
               "lips pressed gently together the whole time, only slow blinks and a faint smile." if strict else "")
            + " Calm, natural movements with the mouth closed; at the end back in the resting pose of the start frame."
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
    if layers[0][0] in cfg["panels"]:   # nền cũng có "khung <KHOÁ>" (vd. màn hình chia đôi): chỉ chiếm ô của nó, phần còn lại do các ô khác phủ
        bx, by, bw_, bh_ = cfg["panels"][layers[0][0]]
        x, y, w, h = _even(bx * W), _even(by * H), _even(bw_ * W), _even(bh_ * H)
        base = (f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30,setsar=1,trim=duration={dur:.3f},setpts=PTS-STARTPTS,"
                f"pad={W}:{H}:{x}:{y}:black[l0]")
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
    chain = cfg["join"][0] == "chain"
    if chain and mode == "reuse":
        mode = "scene"   # nối khung: clip nghe phải bắt đầu từ khung cuối của chính nhân vật đó nên không dùng thư viện clip nghe ("tinh" giữ nguyên)
    emit("log", msg=f"Ghép 2 lớp: nền {cfg['bg']}, khung {', '.join(f'{k} ({aspect_of(cfg, k)})' for k in cfg['panels'])}; clip nghe: "
                    + ("ảnh tĩnh (không thể nhép miệng)" if mode == "still" else "gen riêng mỗi cảnh" if mode == "scene" else f"dùng lại {n_lib} clip mỗi nhân vật")
                    + ("; nối khung: clip sau của mỗi nhân vật bắt đầu từ khung cuối clip trước của nó" if chain else ""))
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

    def gen(kind, prompt, start_png, path, aspect, dur=None, n=None, audios=None, state=None, ref_list=None, ident=None):
        vrefs = [G.data_url(start_png)] if start_png else list(ref_list if ref_list is not None else refs)
        if start_png and ident and os.path.exists(ident) and os.path.abspath(ident) != os.path.abspath(start_png):   # nối khung: neo mặt về ảnh gốc
            vrefs.append(G.data_url(ident))
            prompt += IDENT_NOTE

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
                    _gen_listen(gen, blocks, k, vdata, cfg, base[k], f, LISTEN_DUR, check and not cfg["lock"], emit)
                lib[k].append(_locked(f, emit, "", k) if cfg["lock"] else f)
    used = {k: 0 for k in keys}

    still_of = {}

    def listen_take(k, need, n):
        """(file, giây bắt đầu, có lặp) cho đoạn nghe dài `need` giây của nhân vật k ở cảnh n."""
        if mode == "still":   # người nghe = ảnh tĩnh nhúc nhích rất nhẹ: không thể mấp máy miệng (đo miệng không đủ tin cậy: môi hé nhẹ vẫn lọt ngưỡng)
            f = P(f"scene{n}_listen_{k}.mp4")
            src, frm = (seen[k] if chain else base[k]), None
            if chain and seen_clip.get(k) and _mouth_open(src, 0.06):   # vừa nói xong, miệng còn mở rõ: hoà 0,3s sang khung khép miệng gần nhất của CHÍNH clip đó
                closed = _closed_frame(seen_clip[k], P(f"scene{n}_khepmieng_{k}.png"), src)   # (cùng tư thế). Không bao giờ về ảnh gốc: tư thế khác, trông như chuyển cảnh
                if closed:
                    emit("log", msg=f"Cảnh {n}: {k} vừa nói xong còn mở miệng, người nghe khép miệng dần (khung cùng tư thế)")
                    src, frm = closed, src
            still_of[(n, k)] = src
            _still_clip(src, f, need, from_png=frm)
            return f, 0.0, False
        if mode == "scene":
            f = P(f"scene{n}_listen_{k}.mp4")
            if not os.path.exists(f):
                dur = next((d for d in E.ALLOWED if d >= need + 0.3), E.ALLOWED[-1])
                emit("scene", n=n, state="video", pct=0, note=f"clip nghe {k}")
                _gen_listen(gen, blocks, k, vdata, cfg, tail[k] if chain else base[k], f, dur, check and not cfg["lock"], emit, n=n, t_end=need + 0.3,
                            ident=base[k] if chain else None)   # có khoá miệng thì không cần đo miệng + gen lại (đỡ tốn lượt gen)
            if chain:   # khớp khung đầu clip nghe với khung người xem vừa thấy
                fa = P(f"scene{n}_listen_{k}_khop.mp4")
                if not os.path.exists(fa) or os.path.getmtime(fa) < os.path.getmtime(f):
                    emit("log", msg=f"Cảnh {n}: khớp clip nghe {k} với khung nối ({align_to_tail(f, seen[k], fa, base[k])})")
                f = fa
            if cfg["lock"]:
                f = _locked(f, emit, f"Cảnh {n}: ", k)
            elif check:   # gen lại rồi vẫn mấp máy (_gen_listen giữ bản ít nhất): khoá miệng RIÊNG clip này, để không thành hai người cùng nói (soi hành lý 03/11: 5/15 cảnh)
                s = _mouth_score(f, need + 0.3)
                if s is not None and s >= LISTEN_MAX:
                    emit("log", msg=f"Cảnh {n}: clip nghe {k} vẫn mấp máy miệng (mức {s:.3f}, ngưỡng {LISTEN_MAX}), khoá miệng riêng clip này", level="warn")
                    f = _locked(f, emit, f"Cảnh {n}: ", k)
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
    tail = dict(base)   # nối khung: ảnh gửi Muse làm khung đầu clip kế tiếp của từng nhân vật (khung cuối đã khử nhiễu, kéo màu về ảnh gốc)
    seen_clip = {}      # clip nói gần nhất làm ra `seen` của từng nhân vật (tìm khung khép miệng cùng tư thế)
    seen = dict(base)   # khung cuối người xem THẬT SỰ thấy của từng nhân vật: clip kế tiếp được căn khớp hình + màu về đúng khung này
    tail_f = lambda n, k: P(f"scene{n}_tail_{k}.png")
    seen_f = lambda n, k: P(f"scene{n}_seen_{k}.png")
    if chain and cfg["refresh"]:
        emit("log", msg='Bỏ qua "lam moi": ảnh làm mới vẽ lại tư thế/màu nên gây khựng ở chỗ nối (03/11/2026); chống sần mặt đã có ảnh gốc tham chiếu + khử nhiễu khung nối', level="warn")
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
                if chain and os.path.exists(tail_f(n, k)):
                    tail[k] = tail_f(n, k)
                    seen[k] = seen_f(n, k) if os.path.exists(seen_f(n, k)) else tail[k]
                    seen_clip[k] = P(f"scene{n}_spkcut.mp4") if k == spk else None
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

            speech_note = [""]   # ghi chú sửa lời nói (lặp từ, thừa từ) khi gen lại

            def gv():
                gen("video", speak_prompt(blocks, spk, vdata, turn, aspect_of(cfg, spk), dur, " ".join(x for x in (fix, speech_note[0]) if x)), tail[spk] if chain else base[spk], spk_f,
                    aspect_of(cfg, spk), dur=dur, n=n, audios=auds, ident=base[spk] if chain else None)
                if not E.has_audio(spk_f):
                    os.remove(spk_f)
                    raise RuntimeError("Muse trả về clip không có tiếng (mất lời thoại)")
            attempt("video", gv, n)
            if opts.get("check_speech", True):   # nói lặp từ / thừa từ / thiếu lời: gen lại ngay, giữ lần ít lỗi nhất

                def regen(note):
                    speech_note[0] = note
                    os.remove(spk_f)
                    attempt("video", gv, n)
                E.speech_retry(spk_f, turn["text"], regen, emit, n, int(opts.get("speech_retries", 1)))
        # cắt sát lời (như chế độ thường)
        emit("scene", n=n, state="cut", pct=100)
        vf_fix = ""
        src_f = spk_f
        if chain:   # Muse không giữ đúng khung đầu (tự thu khung, đổi màu): căn khớp hình + màu về khung người xem vừa thấy, hoà 0,2s đầu
            src_f = P(f"scene{n}_spk_khop.mp4")
            if not os.path.exists(src_f) or os.path.getmtime(src_f) < os.path.getmtime(spk_f):
                emit("log", msg=f"Cảnh {n}: khớp clip {spk} với khung nối ({align_to_tail(spk_f, seen[spk], src_f, base[spk])})")
        elif opts.get("normalize", True):   # cân màu từng nhân vật về clip đầu tiên của chính nhân vật đó
            c_start, c_end = E.color_stats(spk_f, [0.04, 0.2, 0.4]), E.color_stats(spk_f, [-0.6, -0.35, -0.1])
            ref_stats.setdefault(spk, c_start)
            vf_fix, note = E.color_match(ref_stats[spk], c_start, c_end, E.duration(spk_f))
            if vf_fix:
                emit("log", msg=f"Cảnh {n}: cân màu {spk} ({note})")
        span, margin = None, float(opts.get("cut_margin", 0.3))
        if opts.get("cut", True) and opts.get("precise_cut", True):
            try:
                span = E.interruptible(lambda: E.voice_span(src_f, turn["text"]), cancel)
            except E.Cancelled:
                raise
            except Exception as ex:  # noqa: BLE001
                emit("log", msg=f"Cảnh {n}: không xác định được mốc lời nói, cắt theo cách thường ({ex})", level="warn")
        info = E.smart_cut(src_f, spk_cut, spk_last, syll=syll, speedfix=opts.get("speedfix", True), vf_extra=vf_fix, max_speed=float(opts.get("speed_max", 1.25)),
                           span=span, lo=(0.18 if span else 0.15), hi=(max(0.3, margin + 0.05) if span else 0.8),
                           head_margin=99.0 if chain else margin * 0.7) if opts.get("cut", True) else None   # nối khung: không cắt đầu clip, khung đầu phải đúng là khung nối
        if info is None:
            shutil.copy(src_f, spk_cut)
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
        if chain:   # khung cuối từng nhân vật: `seen` = đúng khung người xem thấy (đích căn khớp), `tail` = bản đã làm sạch gửi Muse
            for k in keys:
                if k == spk:
                    shutil.copyfile(spk_last, seen_f(n, k))
                elif mode == "still":
                    shutil.copyfile(still_of[(n, k)], seen_f(n, k))
                else:
                    f, off, _ = layer[k][1:]
                    E.grab_frame(f, seen_f(n, k), ss=max(0.0, off + need - 1 / 30))
                shutil.copyfile(seen_f(n, k), tail_f(n, k))
                clean_tail(tail_f(n, k), base[k])
                seen[k], tail[k] = seen_f(n, k), tail_f(n, k)
                seen_clip[k] = spk_cut if k == spk else None
        clips.append(cut_f)
        emit("scene", n=n, state="done", pct=100, thumb=os.path.basename(last_f), clip=os.path.basename(cut_f), secs=round(E.duration(cut_f), 1))
    raw = E.concat_clips(clips, out_dir, emit)
    if cfg["join"][0] == "morph" and len(clips) > 1:
        marks = [sum(E.duration(c) for c in clips[:i]) for i in range(1, len(clips))]
        morph_cuts(raw, marks, cfg["join"][1])
        emit("log", msg=f"Làm mượt {len(marks)} chỗ nối giữa các cảnh ghép ({cfg['join'][1]:.2f}s mỗi chỗ)")
    return raw


def clean_tail(png, base_png, strength=0.6):
    """Khung nối (khung cuối clip trước -> khung đầu clip sau): khử nhiễu nhẹ (vệt nén) và kéo màu Lab về gần ảnh gốc của nhân vật.
    Không làm thì qua mỗi đời nối Muse vẽ vệt nén thành tàn nhang/vân da, mặt sần dần và nhạt màu dần (đo 03/11/2026: bão hoà 136 -> 108 sau 8 cảnh)."""
    import cv2
    import numpy as np
    im, ref = cv2.imread(png), cv2.imread(base_png)
    if im is None or ref is None:
        return
    im = cv2.fastNlMeansDenoisingColored(im, None, 3, 3, 5, 15)
    a = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32)
    b = cv2.cvtColor(cv2.resize(ref, (im.shape[1], im.shape[0])), cv2.COLOR_BGR2LAB).astype(np.float32)
    for c in range(3):
        m0, s0, m1, s1 = a[..., c].mean(), a[..., c].std() + 1e-6, b[..., c].mean(), b[..., c].std() + 1e-6
        t = (a[..., c] - m0) * (s1 / s0) + m1
        a[..., c] = a[..., c] * (1 - strength) + t * strength
    cv2.imwrite(png, cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR))


def _lab_stats(img):
    import cv2
    import numpy as np
    a = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    return a.mean(0), a.std(0) + 1e-6


def align_to_tail(src, tail_png, out, base_png=None, blend=0.2, pull=0.35):
    """Nối khung khớp tuyệt đối: Muse KHÔNG giữ đúng khung đầu được gửi (đo 03/11/2026: tự thu khung ~5-8% và đổi màu, chỗ nối lệch 30-39/255).
    Clip `src` được: (1) căn hình học (phóng/dời/xoay nhỏ, ước lượng từ khung đầu clip -> `tail_png`) cho cả clip;
    (2) chỉnh màu Lab: khung đầu = đúng màu `tail_png`, đổi dần tới cuối clip kéo `pull` phần về ảnh gốc `base_png` (chống trôi màu qua nhiều cảnh);
    (3) hoà `blend` giây đầu từ đúng `tail_png` sang clip để mọi sai khác còn lại (nét mặt, tóc) chuyển êm.
    `tail_png` phải là khung người xem vừa thấy ở cuối cảnh trước. Giữ nguyên tiếng. Trả về mô tả ngắn."""
    import subprocess
    import cv2
    import numpy as np
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    cap.release()
    tgt = cv2.imread(tail_png)
    if not frames or tgt is None:
        shutil.copyfile(src, out)
        return "bỏ qua (không đọc được clip/khung nối)"
    h, w = frames[0].shape[:2]
    tgt = cv2.resize(tgt, (w, h), interpolation=cv2.INTER_AREA)
    # (1) hình học: ORB + affine đồng dạng, chỉ nhận khi thật sự làm khớp hơn
    M, note = None, "giữ khung"
    g0, gt = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY), cv2.cvtColor(tgt, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(3000)
    k0, d0 = orb.detectAndCompute(g0, None)
    kt, dt = orb.detectAndCompute(gt, None)
    if d0 is not None and dt is not None and len(k0) > 30 and len(kt) > 30:
        ms = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d0, dt), key=lambda m: m.distance)[:600]
        if len(ms) >= 20:
            A, inl = cv2.estimateAffinePartial2D(np.float32([k0[m.queryIdx].pt for m in ms]), np.float32([kt[m.trainIdx].pt for m in ms]),
                                                 method=cv2.RANSAC, ransacReprojThreshold=3.0)
            if A is not None and inl is not None and inl.sum() >= 15:
                s = float(np.hypot(A[0, 0], A[1, 0]))
                if 0.85 < s < 1.2 and abs(A[0, 2]) < 0.2 * w + (s - 1) * w and abs(A[1, 2]) < 0.2 * h + (s - 1) * h:
                    warped = cv2.warpAffine(frames[0], A, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                    err = lambda im: float(np.abs(cv2.resize(im, (180, 320)).astype(np.int16) - cv2.resize(tgt, (180, 320)).astype(np.int16)).mean())
                    if err(warped) < err(frames[0]) - 0.5:
                        M, note = A, f"phóng x{s:.3f}, dời {A[0, 2]:+.0f},{A[1, 2]:+.0f}px"
    warp = (lambda f: cv2.warpAffine(f, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)) if M is not None else (lambda f: f)
    first, last = warp(frames[0]), warp(frames[-1])
    # (2) màu: hệ số (gain, offset) Lab ở khung đầu (về tail) và khung cuối (về gần ảnh gốc), nội suy theo thời gian
    mt, st = _lab_stats(tgt)
    m0, s0 = _lab_stats(first)
    m1, s1 = _lab_stats(last)
    base = cv2.imread(base_png) if base_png else None
    if base is not None:
        mb, sb = _lab_stats(cv2.resize(base, (w, h), interpolation=cv2.INTER_AREA))
        me, se = m1 + pull * (mb - m1), s1 + pull * (sb - s1)
    else:
        me, se = m1, s1
    ga, gb = np.clip(st / s0, 0.8, 1.25), np.clip(se / s1, 0.8, 1.25)
    oa, ob = mt - ga * m0, me - gb * m1
    n, nb = len(frames), max(1, int(round(blend * fps)))
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps:.6f}", "-i", "-",
                             "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
                             "-c:a", "copy", "-shortest", out], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for i, f in enumerate(frames):
            u = i / max(1, n - 1)
            g, o = ga + (gb - ga) * u, oa + (ob - oa) * u
            lab = cv2.cvtColor(warp(f), cv2.COLOR_BGR2LAB).astype(np.float32) * g + o
            im = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
            if i < nb:   # hoà từ đúng khung nối sang clip (cosine)
                a = 0.5 + 0.5 * np.cos(np.pi * i / nb)
                im = cv2.addWeighted(tgt, a, im, 1 - a, 0)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        err = proc.stderr.read().decode("utf-8", "replace")
        if proc.wait():
            raise RuntimeError(f"ffmpeg lỗi khi căn khớp clip: {err[-300:]}")
    finally:
        if proc.poll() is None:
            proc.kill()
    return f"{note}, màu khớp khung nối, hoà {blend:.1f}s"


def morph_cuts(raw, marks, d=MORPH_DUR):
    """Chỗ nối giữa hai cảnh ghép: thay khoảng [t-d/2, t+d/2] bằng hình chuyển dần (minterpolate, optical flow) từ khung tại t-d/2 sang khung tại t+d/2,
    để tư thế không nhảy cóc. Không đổi độ dài video, tiếng giữ nguyên (lời nói luôn cách mép cảnh ~0,2s nên không mất khẩu hình)."""
    import tempfile
    total, h = E.duration(raw), d / 2
    marks = [t for t in marks if t - h > 0.05 and t + h < total - 0.05]
    if not marks:
        return
    work = tempfile.mkdtemp(prefix="morph_")
    try:
        ins, fl, cur = ["-i", raw], [], "0:v"
        for k, t in enumerate(marks):
            a, b = os.path.join(work, f"m{k}_000.png"), os.path.join(work, f"m{k}_001.png")
            E.sh(["ffmpeg", "-y", "-ss", f"{t - h:.3f}", "-i", raw, "-frames:v", "1", a])
            E.sh(["ffmpeg", "-y", "-ss", f"{t + h:.3f}", "-i", raw, "-frames:v", "1", b])
            shutil.copyfile(b, os.path.join(work, f"m{k}_002.png"))   # khung thứ ba để minterpolate có đủ đoạn A -> B
            mv = os.path.join(work, f"m{k}.mp4")
            E.sh(["ffmpeg", "-y", "-framerate", f"{1 / d:.4f}", "-i", os.path.join(work, f"m{k}_%03d.png"),
                  "-vf", f"minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,trim=duration={d:.3f}", "-pix_fmt", "yuv420p", mv])
            ins += ["-i", mv]
            fl.append(f"[{k + 1}:v]setpts=PTS-STARTPTS+{t - h:.3f}/TB[mv{k}]")
            fl.append(f"[{cur}][mv{k}]overlay=0:0:eof_action=pass:enable='between(t,{t - h:.3f},{t + h:.3f})'[o{k}]")
            cur = f"o{k}"
        tmp = raw + ".morph.mp4"
        E.sh_enc(["ffmpeg", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", f"[{cur}]", "-map", "0:a?", "-c:v", "libx264", "-crf", "17",
                  "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "copy", tmp])
        os.replace(tmp, raw)
    finally:
        shutil.rmtree(work, ignore_errors=True)


IDENT_NOTE = ("\n\nREFERENCE IMAGES: reference image #1 is the START FRAME (the clip begins exactly on it: same pose, framing, background and light). "
              "Reference image #2 is the SAME person in a clean, sharp base photo, for IDENTITY AND SKIN ONLY: keep the face, skin tone and skin texture exactly as in #2 "
              "(smooth, even, natural skin; freckles, spots and pores no more and no darker than in #2; no added grain or blotches); never show, cut or fade to #2.")
LISTEN_MAX = 0.020      # clip NGHE: chặt hơn ngưỡng "đang nói" (người im lặng thật đo được 0,008-0,019)
LISTEN_RETRIES = 2
MOUTH_TALKING = 0.029   # độ lệch chuẩn độ mở miệng: người im lặng thật ~0.008-0.019, mấp máy >= 0.029 (đã đo ở chế độ thường)


def _mouth_open(png, limit=0.04):
    """Ảnh tĩnh đang hé/mở miệng (khoảng hở môi / bề rộng miệng > limit)? Không dò được mặt thì coi như khép."""
    import cv2
    import face_mesh as FM
    im = cv2.imread(png)
    if im is None:
        return False
    try:
        fm = FM.landmarker(min_conf=0.3)
        try:
            g = fm.mouth_gap(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        finally:
            fm.close()
    except Exception:  # noqa: BLE001 - máy không chạy được dò mặt (mediapipe lỗi)
        return False
    return g is not None and g > limit


def _closed_frame(clip, out_png, ref_png, back=1.2, limit=0.05, max_diff=6.0):
    """Khung gần CUỐI clip nhất (trong `back` giây cuối) có miệng khép (khoảng hở môi / bề rộng miệng < limit) VÀ gần như cùng tư thế với `ref_png`
    (lệch trung bình < max_diff/255; lệch hơn thì hoà sẽ thấy bóng mờ tay/đầu), ghi ra `out_png`; None nếu không có."""
    import cv2
    import face_mesh as FM
    if not clip or not os.path.exists(clip):
        return None
    cap = cv2.VideoCapture(clip)
    fps, total = cap.get(cv2.CAP_PROP_FPS) or 24, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    start = max(0, total - int(back * fps))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    cap.release()
    try:
        fm = FM.landmarker(min_conf=0.3)
    except Exception:  # noqa: BLE001 - mediapipe lỗi
        return None
    ref = cv2.imread(ref_png)
    if ref is None or not frames:
        fm.close()
        return None
    small = lambda im: cv2.resize(im, (180, 320), interpolation=cv2.INTER_AREA).astype("int16")
    r = small(ref)
    try:
        for f in reversed(frames):
            if abs(small(f) - r).mean() >= max_diff:
                break   # lùi xa hơn chỉ càng khác tư thế
            g = fm.mouth_gap(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            if g is not None and g < limit:
                cv2.imwrite(out_png, f)
                return out_png
    finally:
        fm.close()
    return None


_LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]   # viền ngoài môi (mediapipe)
_ANCHOR = [1, 2, 4, 5, 6, 98, 327, 195, 168, 205, 425, 50, 280, 234, 454, 10, 33, 263, 133, 362]   # mũi, má, mắt, trán: bám theo đầu, không theo hàm/môi


def _locked(f, emit, pre, k):
    """Bản đã khoá miệng của clip nghe `f` (tạo nếu chưa có / cũ hơn clip); lỗi thì dùng clip gốc."""
    fl = f[:-4] + "_khoa.mp4"
    if os.path.exists(fl) and os.path.getmtime(fl) >= os.path.getmtime(f):
        return fl
    try:
        r = lock_mouth(f, fl)
    except Exception as ex:  # noqa: BLE001 - mediapipe lỗi / ffmpeg lỗi: vẫn chạy tiếp với clip gốc
        emit("log", msg=f"{pre}không khoá được miệng clip nghe {k} ({ex})", level="warn")
        return f
    if not r:
        emit("log", msg=f"{pre}không dò được mặt {k} trong clip nghe, giữ nguyên clip (có thể mấp máy miệng)", level="warn")
        return f
    emit("log", msg=f"{pre}khoá miệng {k} khi nghe ({r[0]}/{r[1]} khung)")
    return fl


def lock_mouth(src, out, grow=1.45, feather=0.35, ease=0.3):
    """Clip NGHE vẫn giữ nguyên chuyển động (gật đầu, chớp mắt, nghiêng người) nhưng MIỆNG đứng yên khép: mỗi khung, vùng môi được thay bằng
    vùng môi của khung khép miệng nhất trong clip, bám theo đầu (biến đổi đồng dạng ước lượng từ điểm mốc mũi/cằm/má), viền hoà mềm,
    màu khớp theo vùng da quanh miệng. Trả về (số khung đã khoá, tổng khung) hoặc None nếu không dò được mặt (giữ nguyên clip).
    Lý do: Muse vẫn cho người nghe hé môi như đang nói, đo miệng + gen lại không chặn được hết (03/11/2026); ảnh tĩnh thì đứng hình, mất tương tác."""
    import subprocess
    import cv2
    import numpy as np
    import face_mesh as FM
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    cap.release()
    if len(frames) < 2:
        return None
    h, w = frames[0].shape[:2]
    pts, gaps = [], []
    with E._MP_LOCK:
        fm = FM.landmarker(min_conf=0.3)
        try:
            for f in frames:
                lm = fm.find(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
                if lm is None:
                    pts.append(None)
                    gaps.append(None)
                    continue
                p = np.float32([[q.x * w, q.y * h] for q in lm])
                pts.append(p)
                gaps.append(abs(p[14, 1] - p[13, 1]) / (np.hypot(*(p[291] - p[61])) + 1e-6))
        finally:
            fm.close()
    ok_i = [i for i, g in enumerate(gaps) if g is not None]
    if len(ok_i) < len(frames) // 2:
        return None
    cand = [i for i in ok_i if i >= int(0.25 * fps)] or ok_i   # bỏ 0,25s đầu (đoạn hoà từ khung nối)
    r = min(cand, key=lambda i: gaps[i] + 0.002 * abs(i - cand[0]) / fps)   # khung khép miệng nhất (hơi ưu tiên khung sớm, gần khung nối)
    ref, rp = frames[r], pts[r]
    lips = rp[_LIPS]
    c = lips.mean(0)
    poly = ((lips - c) * grow + c).astype(np.int32)
    mw = float(np.hypot(*(rp[291] - rp[61])))
    mask = np.zeros((h, w), np.float32)
    cv2.fillPoly(mask, [poly], 1.0)
    k = max(3, int(mw * feather) | 1)
    mask = cv2.GaussianBlur(mask, (k, k), 0)
    ring = cv2.dilate((mask > 0.01).astype(np.uint8), np.ones((k, k), np.uint8)) - (mask > 0.01).astype(np.uint8)
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps:.6f}", "-i", "-",
                             "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
                             "-c:a", "copy", "-shortest", out], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    done, M = 0, None
    try:
        for i, f in enumerate(frames):
            if pts[i] is not None:
                A, _ = cv2.estimateAffinePartial2D(rp[_ANCHOR], pts[i][_ANCHOR], method=cv2.LMEDS)
                M = A if A is not None else M
            if M is not None:
                wr = cv2.warpAffine(ref, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                wm = cv2.warpAffine(mask, M, (w, h))[..., None] * min(1.0, i / max(1.0, ease * fps))   # khép miệng dần trong `ease` giây đầu
                wring = cv2.warpAffine(ring, M, (w, h)) > 0
                if wring.sum() > 20:   # ánh sáng trong clip đổi dần: kéo màu vùng dán theo da quanh miệng của khung hiện tại
                    wr = np.clip(wr.astype(np.float32) + (f[wring].mean(0) - wr[wring].mean(0)), 0, 255)
                f = (wr * wm + f.astype(np.float32) * (1 - wm)).astype(np.uint8)
                done += 1
            proc.stdin.write(np.ascontiguousarray(f).tobytes())
        proc.stdin.close()
        err = proc.stderr.read().decode("utf-8", "replace")
        if proc.wait():
            raise RuntimeError(f"ffmpeg lỗi khi khoá miệng: {err[-300:]}")
    finally:
        if proc.poll() is None:
            proc.kill()
    return done, len(frames)


def _still_clip(png, out, dur, from_png=None, fade=0.3):
    """Clip không tiếng từ một ảnh tĩnh: phóng nhẹ rồi trả về cỡ cũ (+-1,2%) kèm trôi ngang rất nhỏ cho đỡ 'chết'. Đầu và cuối clip đúng bằng ảnh.
    `from_png`: clip mở đầu bằng đúng ảnh này rồi hoà sang `png` trong `fade` giây (khung nối đang hé miệng -> ảnh gốc miệng khép)."""
    import cv2
    h, w = cv2.imread(png).shape[:2]
    w, h = w // 2 * 2, h // 2 * 2
    fr = max(2, int(round(dur * 30)))
    z = f"1+0.012*sin(PI*on/{fr})"
    zp = f"zoompan=z='{z}':x='iw/2-iw/zoom/2+4*sin(2*PI*on/{fr})':y='ih/2-ih/zoom/2':d=1:s={w}x{h}:fps=30,setsar=1,format=yuv444p"
    if from_png:
        ins = ["-framerate", "30", "-loop", "1", "-i", png, "-framerate", "30", "-loop", "1", "-i", from_png]
        fl = (f"[0:v]{zp}[m];[1:v]scale={w}:{h},fps=30,setsar=1,format=yuv444p[f];"
              f"[f][m]blend=all_expr='A*max(0\\,1-T/{fade})+B*min(1\\,T/{fade})',format=yuv420p[v]")
        cmd = ["ffmpeg", "-y"] + ins + ["-filter_complex", fl, "-map", "[v]"]
    else:
        cmd = ["ffmpeg", "-y", "-framerate", "30", "-loop", "1", "-i", png, "-vf", zp + ",format=yuv420p"]
    E.sh_enc(cmd + ["-frames:v", str(fr + 3), "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-an", out])


def _mouth_score(path, t_end=None):
    try:
        m = E.mouth_activity(path, "0,0,1,1", min(E.duration(path), t_end) if t_end else E.duration(path))
        return m[0] if m else None
    except Exception:  # noqa: BLE001 - máy không chạy được đo miệng (mediapipe lỗi): bỏ qua
        return None


def _gen_listen(gen, blocks, k, vdata, cfg, base_png, f, dur, check, emit, n=None, t_end=None, ident=None):
    """Gen một clip nghe; nếu đo được miệng cử động (trong đoạn sẽ dùng, [0, t_end]) quá ngưỡng người nghe thì gen lại tối đa LISTEN_RETRIES lần
    kèm yêu cầu chặt hơn, giữ bản ít cử động nhất. Người nghe hé môi như đang nói khi người kia nói là lỗi dễ thấy nhất (03/11/2026: 0,025 vẫn lọt ngưỡng nói 0,029)."""
    aspect = aspect_of(cfg, k)
    gen("video", listen_prompt(blocks, k, vdata, aspect, dur), base_png, f, aspect, dur=dur, n=n, state="video", ident=ident)
    s0 = _mouth_score(f, t_end) if check else None
    if s0 is None or s0 < LISTEN_MAX:
        return
    best, tries = (s0, f), []
    for i in range(LISTEN_RETRIES):
        emit("log", msg=f"{'Cảnh ' + str(n) + ': c' if n else 'C'}lip nghe của {k}: miệng cử động như đang nói (mức {best[0]:.3f}, ngưỡng {LISTEN_MAX}), gen lại {i + 1}/{LISTEN_RETRIES}", level="warn")
        tmp = f"{f}.try{i}.mp4"
        tries.append(tmp)
        gen("video", listen_prompt(blocks, k, vdata, aspect, dur, strict=True), base_png, tmp, aspect, dur=dur, n=n, state="video", ident=ident)
        s1 = _mouth_score(tmp, t_end)
        if s1 is not None and s1 < best[0]:
            best = (s1, tmp)
        if best[0] < LISTEN_MAX:
            break
    if best[1] != f:
        os.replace(best[1], f)
    for t in tries:
        if os.path.exists(t):
            os.remove(t)
    if best[0] >= LISTEN_MAX:
        emit("log", msg=f"Clip nghe của {k}: vẫn còn cử động miệng (mức {best[0]:.3f}), giữ bản ít nhất. Bấm gen lại cảnh này nếu thấy mấp máy", level="warn")
