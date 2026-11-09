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
            keys_v = re.findall(r"\b[A-Z][A-Z0-9_]+\b", v)   # "HOC" / "HOC, KHACH" = chỉ khoá các nhân vật này (người thật nghe vẫn cười mím, môi động; robot thì yên)
            cfg["lock"] = {MV.ck(x) for x in keys_v} if keys_v else ("khong" not in _plain(v) and ("co" in _plain(v).split() or "bat" in _plain(v)))
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


def _style(blocks, key, v=None):
    """[STYLE LOCK] dùng chung cho mọi lớp, nhưng bỏ các mệnh đề (ngăn bởi . ; ) tả NHÂN VẬT KHÁC (nhắc tên ngắn TEN_<khoá khác>).
    07/11/2026 xe-tai 20 biến thể: STYLE LOCK phần 2 có "the AI tutor is a sleek photorealistic CGI humanoid robot…" -> prompt ảnh gốc/clip của
    tài xế (lớp nền) cũng tả robot, Muse vẽ robot ngồi ghế phụ cạnh tài xế ở 3/4 biến thể. Mỗi lớp chỉ được thấy mô tả của chính nó."""
    return _drop_others(blocks.get("STYLE LOCK", ""), blocks, key, v)


def _neg(blocks, key, v=None):
    """[NEGATIVE] dùng chung, bỏ các mục nhắc tên nhân vật khác (cùng lý do với _style)."""
    return _drop_others(blocks.get("NEGATIVE", ""), blocks, key, v)


def _drop_others(s, blocks, key, v=None):
    others = [c for c in (b[len("NHAN VAT "):] for b in blocks if b.startswith("NHAN VAT ")) if c != key]
    names = [n for n in ((v or {}).get(f"TEN_{c}", "").strip().lower() for c in others) if len(n) > 3]
    names = [re.sub(r"^(the|a|an)\s+", "", n) for n in names]
    if not s or not names:
        return s
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", s.strip()):
        keep = [x for x in re.split(r"(?<=;)\s+", sent) if not any(n in x.lower() for n in names)]
        t = " ".join(keep).strip().rstrip(";").strip()
        if t:
            out.append(t if t[-1] in ".!?" else t + ".")
    return " ".join(out)


def image_prompt(blocks, key, aspect, n_refs, legend, v=None, bg=None):
    body = "\n\n".join(x for x in [_style(blocks, key, v), _who(blocks, key)] if x)
    ref = (f"\n\nUse the attached reference image{'' if n_refs == 1 else 's'} as visual guidance for faces, outfits and props. THE REFERENCE IMAGES ARE AUTHORITATIVE FOR APPEARANCE: the person must look exactly like their own reference image (face, hair, skin tone, age, clothing); if the description conflicts with it, the reference wins." + (f" REFERENCE IMAGE NOTES: {legend}" if legend else "")) if n_refs else ""
    neg = _neg(blocks, key, v)
    return ("Create exactly one still image (not a video, not an animation).\n\n"
            f"{body}\n\nThis is the BASE FRAME of this character: exactly ONE person in the frame, nobody else visible. Neutral relaxed resting pose, mouth gently CLOSED, "
            f"calm attentive expression, looking toward the camera. Output {ASPECTS[aspect]} ({aspect}).{ref}"
            + (f"\n\nAvoid: {neg}" if neg else "") + "\n\nFINAL REMINDER: output exactly ONE STILL IMAGE.")


def speak_prompt(blocks, key, v, turn, aspect, dur, fix=""):
    who = MV.ck(turn.get("who"))
    name = v.get(f"TEN_{who}", "") or "the character"
    how = MV.speaker_how(v, turn["who"], turn.get("text", ""), turn.get("emo", ""))
    body = "\n\n".join(x for x in [_style(blocks, key, v), _who(blocks, key)] if x)
    suffix, neg = blocks.get("VIDEO SUFFIX", ""), _neg(blocks, key, v)
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


# Mệnh đề trong khối [NGHE <KHOÁ>] nhắc tới việc nói (dù là để CẤM: "no talking-like head bobbing, never mirrors the speaker"): Muse đọc thấy chữ
# "talking"/"speaker" là lồng tiếng nói vào clip nghe rồi cho mặt nhép theo. Đo 04/11/2026 trên 246 clip nghe: có câu đó 30/75 clip có tiếng (40%),
# không có 5/171 (3%). Khối NGHE chỉ nên tả điều NÊN làm (khép miệng, mỉm cười, gật nhẹ, chớp mắt); Studio tự bỏ các mệnh đề như vậy cho mọi thể loại.
_NGHE_SPEECH_RE = re.compile(r"\b(talk\w*|speak\w*|speech|mirror\w*|voice\w*|dialogue|words?|says?|said|mouthing|lip-?sync\w*|murmur\w*|whisper\w*)\b", re.I)


def _calm_listen(how):
    """Bỏ các mệnh đề (ngăn bởi . ; ,) của khối NGHE có nhắc tới lời nói / người nói, giữ phần tả dáng nghe."""
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", (how or "").strip()):
        s = " ".join(x for x in re.split(r"(?<=[;,])\s+", sent) if not _NGHE_SPEECH_RE.search(x)).strip().rstrip(",;")
        if s:
            out.append(s if s[-1] in ".!?" else s + ".")
    return " ".join(out)


def listen_prompt(blocks, key, v, aspect, dur, mood="", strict=False):
    name = v.get(f"TEN_{key}", "") or "the character"
    body = "\n\n".join(x for x in [_no_speech(_style(blocks, key, v)), _no_speech(_who(blocks, key))] if x)
    how = _calm_listen(blocks.get(f"NGHE {key}", "")) or "listening attentively to someone off-screen: natural blinks, raised eyebrows, a soft closed-mouth smile, small head tilts"
    neg = _no_speech(_neg(blocks, key, v), ";")
    return (f"Create {ASPECTS[aspect]} ({aspect}) video clip, {dur} seconds long. Make ONE NEW, SEPARATE clip.\n\n"
            "SILENT CLIP: Return a video with no audio at all: no speech, no music, no sound effects.\n\n"
            f"{body}\n\nThe clip starts exactly from the attached start frame. Exactly ONE person is in the frame: {name}, quietly listening. "
            f"LIPS SEALED: the lips are softly pressed together, still and relaxed from the first frame to the last, like a calm closed-mouth smile in a portrait; "
            f"if they are parted in the start frame they close at once and stay closed; the jaw stays still. {how}" + (f" Mood: {mood}." if mood else "")
            + (" RETRY: keep it calmer this time. The head stays still, facing the same way as in the start frame, no glancing away, "
               "lips pressed gently together the whole time, only slow blinks and a faint smile." if strict else "")
            + " Only the eyes, eyebrows and the head move a little; at the end back in the resting pose of the start frame."
            # Không liệt kê "talking; lip movement; mouthing words" trong Avoid: chữ cấm gợi đúng hành vi đó (xem _NGHE_SPEECH_RE). 05/11/2026 chia-doi
            # vẫn còn clip nghe hé môi / môi động nhẹ dù câm tiếng.
            + (f"\n\nAvoid: {neg}; parted lips; a moving jaw; a second person." if neg else "\n\nAvoid: parted lips; a moving jaw; a second person."))


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


# ---- ô của nhân vật khác che mặt nhân vật nền (06/11/2026, canh-sat-gia-su-ai phần 2: ô AI 1/3 trên + phụ đề che mắt tài xế)
SUB_BELOW = 0.07   # dải phụ đề thường đặt ngay dưới ô (tỉ lệ chiều cao khung): mặt cũng không được nằm trong dải này


def head_span(png):
    """(đỉnh đầu, cằm, trái, phải) của khuôn mặt (tỉ lệ 0..1 của ảnh), đỉnh đầu ước lượng thêm phần tóc trên trán; None nếu không dò được mặt."""
    try:
        import cv2
        import face_mesh as FM
        im = cv2.imread(png)
        lm = FM.landmarker()
        try:
            pts = lm.find(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        finally:
            lm.close()
        if not pts:
            return None
        ys, xs = [p.y for p in pts], [p.x for p in pts]
        top, chin = min(ys), max(ys)
        return max(0.0, top - 0.35 * (chin - top)), chin, min(xs), max(xs)
    except Exception:  # noqa: BLE001 - máy không chạy được dò mặt: bỏ qua kiểm tra
        return None


def panel_clear_y(cfg, span):
    """Mép dưới thấp nhất của các ô (cộng dải phụ đề) đè lên mặt nhân vật nền; 0 nếu không ô nào che mặt."""
    if not span or cfg["bg"] in cfg["panels"]:
        # nền có "khung <KHOÁ>" riêng (màn hình chia đôi trái/phải): ảnh gốc của nó là khung 9:16 RIÊNG, toạ độ mặt trong ảnh đó không cùng hệ với ô của
        # nhân vật khác trên màn ghép, và không ô nào đè lên nó. Không bỏ qua thì ô DAY nửa trái bị tính là "che mặt" -> gen lại + dịch ảnh người xuống 35%
        # (du-lich-chia-doi 06/11/2026: AI cao, người thấp). Cùng điều kiện với face_under_panels.
        return 0.0
    top, chin, l, r = span
    need = 0.0
    for k, (x, y, w, h) in cfg["panels"].items():
        if k == cfg["bg"] or x > r or x + w < l:
            continue
        bottom = y + h + SUB_BELOW
        if top < bottom and chin > y:
            need = max(need, bottom)
    return need


def shift_down(png, dy_frac):
    """Dịch ảnh xuống dy_frac chiều cao (cắt phần đáy), lấp dải trên bằng hàng trên cùng kéo giãn + nhoè (dải đó nằm sau ô nên gần như không lộ)."""
    import cv2
    import numpy as np
    im = cv2.imread(png)
    h, w = im.shape[:2]
    dy = int(round(h * dy_frac))
    if dy <= 0:
        return
    out = np.empty_like(im)
    out[dy:] = im[: h - dy]
    band = cv2.resize(im[: max(4, h // 40)], (w, dy), interpolation=cv2.INTER_LINEAR)
    out[:dy] = cv2.GaussianBlur(band, (0, 0), 9)
    cv2.imwrite(png, out)


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
    E.set_prompt_prefix(opts)
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
            except (E.Cancelled, E.AccountError):
                raise   # lỗi tài khoản: để server đổi tài khoản
            except Exception as e:  # noqa: BLE001
                E.log_exc(f"split {label} cảnh {n}: {str(e)[:120]}")
                emit("log", msg=f"{'Cảnh ' + str(n) if n else 'Chuẩn bị'} {label}: {e}", level="warn")
                if E._QUOTA_RE.search(str(e)):
                    raise E.QuotaExceeded(f"Muse báo hết hạn mức tạo video (giới hạn 24 giờ): {str(e)[:160]}") from None
                if i > opts["retries"]:
                    raise
                if n:
                    emit("scene", n=n, state=label, pct=0, note=f"thử lại {i}/{opts['retries']}")
                time.sleep(4)

    def gen(kind, prompt, start_png, path, aspect, dur=None, n=None, audios=None, state=None, ref_list=None, ident=None, orig=None):
        vrefs = [G.data_url(start_png)] if start_png else list(ref_list if ref_list is not None else refs)
        if start_png and ident and os.path.exists(ident) and os.path.abspath(ident) != os.path.abspath(start_png):   # nối khung: neo mặt về ảnh gốc
            vrefs.append(G.data_url(ident))
            prompt += IDENT_NOTE
        # ảnh tham chiếu GỐC của chính nhân vật (gắn trong biến thể) gửi kèm MỌI clip, không chỉ lúc tạo ảnh gốc: chỉ có khung nối + ảnh gốc thì Muse
        # trôi dần sang một nhân vật khác qua các đời nối (05/11/2026, chia-doi BT12: robot đổi mặt/đầu từ cảnh 8 rồi giữ luôn bản sai tới hết video)
        extra = [u for u in (orig or []) if u][:2] if start_png else []
        if extra:
            k0 = len(vrefs)
            vrefs += extra
            prompt += ("\n\n" if k0 == 1 else "") + ORIG_NOTE.format(nums=" and ".join(f"#{k0 + i + 1}" for i in range(len(extra))), s="s" if len(extra) > 1 else "")

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
            gen("image", image_prompt(blocks, k, aspect_of(cfg, k), len(refs) + len(imgs_k), legend_k, vdata, cfg["bg"]), None, base[k], aspect_of(cfg, k), ref_list=list(refs) + list(imgs_k))
            if k == cfg["bg"]:   # ô của nhân vật khác (và dải phụ đề dưới ô) không được che mặt nhân vật nền
                for fix in range(2):   # 06/11: Muse bỏ qua yêu cầu "đầu ở N%" cả 2 lần gen lại -> chỉ gen lại 1 lần rồi dịch ảnh
                    span = head_span(base[k])
                    need = panel_clear_y(cfg, span)
                    if not need:
                        break
                    if fix < 1:
                        emit("log", msg=f"Ảnh gốc {k}: đỉnh đầu ở {span[0] * 100:.0f}% khung, bị ô che (cần thấp hơn {need * 100:.0f}%): gen lại", level="warn")
                        os.replace(base[k], base[k] + f".che{fix + 1}.png")
                        gen("image", image_prompt(blocks, k, aspect_of(cfg, k), len(refs) + len(imgs_k), legend_k, vdata, cfg["bg"])
                            + f"\n\nCOMPOSITION FIX: the top of the head (including hair) must be at least {need * 100 + 3:.0f}% down from the top edge of the frame "
                              f"and the whole face below that line; the upper {need * 100:.0f}% of the frame shows only background (it will be covered by another window).",
                            None, base[k], aspect_of(cfg, k), ref_list=list(refs) + list(imgs_k))
                    else:
                        dy = min(0.35, need + 0.03 - span[0])
                        shutil.copy(base[k], base[k] + ".truoc-dich.png")
                        shift_down(base[k], dy)
                        emit("log", msg=f"Ảnh gốc {k}: vẫn bị ô che sau 1 lần gen lại: dịch ảnh xuống {dy * 100:.0f}% để mặt nằm dưới ô", level="warn")

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
                    _gen_listen(gen, blocks, k, vdata, cfg, base[k], f, LISTEN_DUR, check and not _lock_on(cfg, k), emit, orig=att[k][0])
                lib[k].append(_locked(f, emit, "", k) if _lock_on(cfg, k) else f)
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
                spare = next((p for m in range(n - 1, 0, -1) if os.path.exists(p := P(f"scene{m}_listen_{k}.mp4"))   # clip nghe câm gần nhất của k (clip Muse:
                              and _audio_db(p) > float("-inf") and not _talky(p)), None)                                # có rãnh tiếng nhưng im; clip ảnh tĩnh không có rãnh tiếng)
                _gen_listen(gen, blocks, k, vdata, cfg, tail[k] if chain else base[k], f, dur, check and not _lock_on(cfg, k), emit, n=n, t_end=need + 0.3,
                            ident=base[k] if chain else None, spare=spare, orig=att[k][0])   # có khoá miệng thì không cần đo miệng + gen lại (đỡ tốn lượt gen)
            if chain:   # khớp khung đầu clip nghe với khung người xem vừa thấy
                fa = P(f"scene{n}_listen_{k}_khop.mp4")
                if not _fresh(fa, f):
                    emit("log", msg=f"Cảnh {n}: khớp clip nghe {k} với khung nối ({align_to_tail(f, seen[k], fa, base[k])})")
                f = fa
            if _lock_on(cfg, k):
                f = _locked(f, emit, f"Cảnh {n}: ", k)
            elif check:   # gen lại rồi vẫn mấp máy (_gen_listen giữ bản ít nhất): chỉ GHI CẢNH BÁO, giữ nguyên clip Muse. Người dùng bỏ "dán miệng" (06/11/2026,
                # du-lich-chia-doi biến thể 2 cảnh 4: môi cứng, lộ vết dán) và KHÔNG muốn thay bằng khung đứng yên: chỉ bỏ dán miệng, mọi thứ khác giữ như cũ
                s = _mouth_score(f, need + 0.3)
                talk = _talky(f)   # clip nghe vẫn có tiếng nói lọt vào = mặt đang nhép theo tiếng đó, dù mức miệng đo được dưới ngưỡng
                if (s is not None and s >= LISTEN_MAX) or talk:   # (05/11/2026 du-lich-chia-doi cảnh 4: -23 dB, mức 0,018 < 0,020 -> Carla nhép khi AI nói)
                    emit("log", msg=f"Cảnh {n}: clip nghe {k} vẫn " + ("có tiếng nói lọt vào" if talk else "mấp máy miệng") +
                                    (f" (mức {s:.3f}, ngưỡng {LISTEN_MAX})" if s is not None else "") + " sau khi gen lại; giữ nguyên clip (không dán miệng), xem lại cảnh này", level="warn")
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
        syll = G.spoken_syllables(f'"{turn["text"]}"')   # hàm chỉ đếm chữ trong ngoặc kép (dạng trường Voice): thiếu ngoặc thì ra 0 -> mọi clip 6 giây,
        dur = G.auto_duration(syll) if syll else 6      # câu 18 chữ bị cụt đuôi (04/11/2026, chia-doi cảnh 13: mất "avatar. Anytime, anywhere.")
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
                    aspect_of(cfg, spk), dur=dur, n=n, audios=auds, ident=base[spk] if chain else None, orig=att[spk][0])
                if not E.has_audio(spk_f):
                    os.remove(spk_f)
                    raise RuntimeError("Muse trả về clip không có tiếng (mất lời thoại)")
            attempt("video", gv, n)
            def frame_bad():   # > 1 = hỏng: Muse tự phóng / vẽ lại khác khung nối / mặt nhân vật nền lọt dưới ô khác
                v = max(_zoom_of(spk_f) / ZOOM_REGEN, _start_mismatch(spk_f, tail[spk]) / START_REGEN) if chain else 0.0
                try:
                    v = max(v, face_under_panels(spk_f, cfg, spk) / FACE_PANEL_MAX)
                except Exception:  # noqa: BLE001 - không có mediapipe: bỏ qua phần đo mặt
                    pass
                return v
            if (z0 := frame_bad()) > 1:   # Muse tự phóng khung / vẽ lại cảnh khác khung nối / mặt nền dưới ô khác: gen lại 1 lần, giữ bản lệch ít hơn
                emit("log", msg=f"Cảnh {n}: khung hình clip {spk} lệch khung nối hoặc tự phóng (mức {z0:.2f}), gen lại", level="warn")
                keep = spk_f + ".zoom.mp4"
                os.replace(spk_f, keep)
                try:
                    attempt("video", gv, n)
                    z1 = frame_bad()
                except Exception as ex:  # noqa: BLE001 - gen lại lỗi: dùng bản cũ
                    emit("log", msg=f"Cảnh {n}: gen lại lỗi ({ex}), giữ bản cũ", level="warn")
                    z1 = 99.0
                if z1 < z0:
                    os.remove(keep)
                else:
                    if os.path.exists(spk_f):
                        os.remove(spk_f)
                    os.replace(keep, spk_f)
            if opts.get("check_speech", True):   # nói lặp từ / thừa từ / thiếu lời: gen lại ngay, giữ lần ít lỗi nhất

                def regen(note):
                    nonlocal dur
                    if "missing" in note and dur < E.ALLOWED[-1] and E.duration(spk_f) - _speech_end(spk_f) < 0.35:   # nói tới sát cuối clip mà vẫn thiếu: clip quá ngắn
                        dur = next(d for d in E.ALLOWED if d > dur)
                        emit("log", msg=f"Cảnh {n}: lời nói kéo tới sát cuối clip mà vẫn thiếu chữ, gen lại clip dài {dur} giây", level="warn")
                    speech_note[0] = note
                    os.remove(spk_f)
                    attempt("video", gv, n)
                E.speech_retry(spk_f, turn["text"], regen, emit, n, int(opts.get("speech_retries", E.SPEECH_RETRIES)))
        # cắt sát lời (như chế độ thường)
        emit("scene", n=n, state="cut", pct=100)
        vf_fix = ""
        src_f = spk_f
        if chain:   # Muse không giữ đúng khung đầu (tự thu khung, đổi màu): căn khớp hình + màu về khung người xem vừa thấy, hoà 0,2s đầu
            src_f = P(f"scene{n}_spk_khop.mp4")
            if not _fresh(src_f, spk_f):
                emit("log", msg=f"Cảnh {n}: khớp clip {spk} với khung nối ({align_to_tail(spk_f, seen[spk], src_f, base[spk])})")
                try:
                    fp = face_under_panels(src_f, cfg, spk)
                    if fp > FACE_PANEL_MAX:
                        emit("log", msg=f"Cảnh {n}: CẢNH BÁO sau khi khớp, {fp:.0%} mặt {spk} nằm dưới ô khác", level="warn")
                except Exception:  # noqa: BLE001
                    pass
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
                           head_margin=99.0 if chain else margin * 0.7, close_mouth=0.7 if chain else 0.0) if opts.get("cut", True) else None   # nối khung: không cắt đầu clip, khung đầu phải đúng là khung nối
        if info is not None and span and opts.get("check_speech", True) and str(turn.get("text", "")).strip():   # cắt sát lời có thể xén mất chữ đầu/cuối
            try:
                lost = [v for v, _ in (E.speech_issues(turn["text"], spk_cut) or []) if v.startswith(("thiếu", "không nghe"))]
            except Exception:  # noqa: BLE001 - không có Whisper: bỏ qua
                lost = []
            if lost:
                emit("log", msg=f"Cảnh {n}: bản cắt sát lời bị mất chữ ({'; '.join(lost)}), cắt lại rộng hơn", level="warn")
                info = E.smart_cut(src_f, spk_cut, spk_last, syll=syll, speedfix=opts.get("speedfix", True), vf_extra=vf_fix, max_speed=float(opts.get("speed_max", 1.25)),
                                   span=None, lo=0.15, hi=0.8, head_margin=99.0 if chain else margin * 0.7, close_mouth=0.7 if chain else 0.0)
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


def _camera_lock(frames, min_zoom=0.03, min_shift=0.015, win=7):
    """Ma trận 3x3 cho từng khung đưa khung đó về khung hình của khung đầu (bù phóng + dời, bỏ xoay), hoặc (None, độ phóng) nếu camera
    gần như đứng yên. Ước lượng ORB + affine đồng dạng từ khung i tới khung 0 trên ảnh thu nhỏ, rồi khớp đường cong trơn (đa thức bậc 2) theo thời gian.
    Nền và thân người đứng yên chiếm đa số điểm khớp nên đầu gật/nghiêng vẫn giữ nguyên, chỉ phần camera tự phóng/dời bị triệt."""
    import cv2
    import numpy as np
    h, w = frames[0].shape[:2]
    k = 360 / w
    small = lambda f: cv2.cvtColor(cv2.resize(f, (360, int(h * k)), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(1500)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    k0, d0 = orb.detectAndCompute(small(frames[0]), None)
    if d0 is None or len(k0) < 30:
        return None, 1.0
    # Chỉ đo camera trên NỀN: dải mép trái/phải (25% mỗi bên) + dải trên (10%), nơi nhân vật đứng giữa khung không che tới.
    # Đo trên cả khung thì nhân vật gật/cúi đầu bị đọc thành camera dời (05/11/2026 xe-tai-canh-sat phần 2: AI nền đen, điểm khớp dồn trên người,
    # "khoá camera" kéo khung lên tới 97 px rồi lấy khung nối lấp mép hụt -> dải vỡ đáy ô AI, khung AI trôi lên xuống). Nền phẳng (ít điểm ở dải mép)
    # thì không đo được camera -> không khoá.
    sw = 360
    sh = int(h * k)
    band = np.array([p.pt[0] < 0.25 * sw or p.pt[0] > 0.75 * sw or p.pt[1] < 0.10 * sh for p in k0])
    if band.sum() < 60:
        return None, 1.0
    k0, d0 = [p for p, b in zip(k0, band) if b], d0[band]
    p0 = np.float32([p.pt for p in k0])
    par, last = [], (1.0, 0.0, 0.0)
    for f in frames:
        ki, di = orb.detectAndCompute(small(f), None)
        if di is not None and len(ki) >= 30:
            ms = bf.match(di, d0)
            if len(ms) >= 20:
                A, inl = cv2.estimateAffinePartial2D(np.float32([ki[m.queryIdx].pt for m in ms]), p0[[m.trainIdx for m in ms]],
                                                     method=cv2.RANSAC, ransacReprojThreshold=2.0)
                if A is not None and inl is not None and inl.sum() >= 15:
                    s = float(np.hypot(A[0, 0], A[1, 0]))
                    if 0.6 < s < 1.5:
                        last = (s, A[0, 2] / k, A[1, 2] / k)
        par.append(last)
    par = np.array(par)
    # Ước lượng từng khung bị nhiễu (người cử động, nền mờ): nắn theo từng khung làm clip RUNG gấp 2-3 lần clip gốc (đo 05/11/2026 du-lich-chia-doi:
    # nền 0,24 -> 0,73 px/khung, người dùng thấy nửa phải rung lắc). Muse tự phóng/dời khung từ từ, nên chỉ cần một đường cong TRƠN theo thời gian:
    # khớp đa thức bậc 2 cho từng tham số (phóng, dời x, dời y) -> bù được phóng/trôi chậm, không thêm rung (đo lại: 0,24 -> 0,24-0,30).
    # Đường cong NEO ở khung 0 = đứng yên (phóng 1, dời 0): khung đầu luôn đúng khung nối; đường cong tự do làm khung đầu dời sẵn hàng chục px
    # (đo 05/11/2026: -76 px ở ô AI, -15 px ở di-tru) -> giật ở chỗ nối và mép hụt ngay từ khung đầu.
    if len(par) >= 8:
        t = np.linspace(0.0, 1.0, len(par))
        B = np.stack([t, t * t], 1)
        ident = np.array([1.0, 0.0, 0.0])
        par = np.stack([ident[j] + B @ np.linalg.lstsq(B, par[:, j] - ident[j], rcond=None)[0] for j in range(3)], 1)
    elif len(par) >= win:
        ker = np.ones(win) / win
        par = np.stack([np.convolve(np.pad(par[:, j], win // 2, mode="edge"), ker, mode="valid") for j in range(3)], 1)
    zoom = float(max(1 / par[:, 0].min(), par[:, 0].max()))
    # dịch chuyển thật của tâm khung (bù cả phần sinh ra do phóng quanh góc trên-trái của hệ toạ độ)
    shift = np.hypot(par[:, 1] + (par[:, 0] - 1) * w / 2, par[:, 2] + (par[:, 0] - 1) * h / 2).max() / w
    if zoom - 1 < min_zoom and shift < min_shift:
        return None, zoom
    return [np.array([[s, 0, tx], [0, s, ty], [0, 0, 1]], np.float64) for s, tx, ty in par], zoom


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
                # nhận cả lệch lớn (05/11/2026: từ khi gửi Muse nguyên văn, Muse vẽ robot to hơn khung nối x1,4 ngay từ khung đầu): mép hụt lấy từ khung nối
                if 0.6 < s < 1.6 and abs(A[0, 2]) < 0.2 * w + abs(s - 1) * w and abs(A[1, 2]) < 0.2 * h + abs(s - 1) * h:
                    warped = cv2.warpAffine(frames[0], A, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                    err = lambda im: float(np.abs(cv2.resize(im, (180, 320)).astype(np.int16) - cv2.resize(tgt, (180, 320)).astype(np.int16)).mean())
                    if err(warped) < err(frames[0]) - 0.5:
                        M, note = A, f"phóng x{s:.3f}, dời {A[0, 2]:+.0f},{A[1, 2]:+.0f}px"
    # (1b) khoá camera: Muse hay tự phóng/dời khung giữa clip (đo 05/11/2026: tới x1.2-1.5, rồi nối khung giữ luôn cỡ đã phóng tới hết video)
    #      -> mỗi khung được đưa về đúng khung hình của khung đầu; phần mép bị hụt khi thu nhỏ lấy từ khung nối `tail_png` (camera và nền đứng yên;
    #      phần trái/phải còn bị cắt bỏ khi ghép vào khung hẹp)
    stab, zmax = _camera_lock(frames)
    if stab is not None:
        note += f", khoá camera (Muse phóng tới x{zmax:.2f})"
    M3 = np.vstack([M, [0, 0, 1]]) if M is not None else np.eye(3)
    ones = np.full((h, w), 255, np.uint8)
    # (1c) kéo bố cục về ảnh gốc: khớp khung đầu với khung nối làm lệch CỘNG DỒN qua các clip nối (06/11/2026 di-tru phần 3: mỗi cảnh Diego gần hơn
    #      và lệch phải thêm, tới cảnh 25 mặt nằm dưới ô AI; clip Muse gốc vẫn đúng khung, bản _khop mới lệch). Khung đầu vẫn khớp khung nối,
    #      rồi biến đổi đổi dần (ease) tới phép đưa khung cuối về đúng bố cục `base_png` -> khung cuối (= khung nối cảnh sau) luôn quay về ảnh gốc.
    E = np.eye(3)
    base_g = cv2.imread(base_png) if base_png else None
    if base_g is not None and (M is not None or stab is not None):
        T_last = M3 @ (stab[-1] if stab is not None else np.eye(3))
        wl = cv2.warpAffine(frames[-1], T_last[:2], (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        bg = cv2.resize(base_g, (w, h), interpolation=cv2.INTER_AREA)
        ks = 360 / w
        sm = lambda im: cv2.cvtColor(cv2.resize(im, (360, int(h * ks)), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        ob = cv2.ORB_create(2000)
        ka, da = ob.detectAndCompute(sm(wl), None)
        kb, db = ob.detectAndCompute(sm(bg), None)
        if da is not None and db is not None and len(ka) > 30 and len(kb) > 30:
            ms = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(da, db), key=lambda m: m.distance)[:500]
            if len(ms) >= 20:
                A2, inl = cv2.estimateAffinePartial2D(np.float32([ka[m.queryIdx].pt for m in ms]), np.float32([kb[m.trainIdx].pt for m in ms]),
                                                      method=cv2.RANSAC, ransacReprojThreshold=2.5)
                if A2 is not None and inl is not None and inl.sum() >= 15:
                    s2 = float(np.hypot(A2[0, 0], A2[1, 0]))
                    A2 = A2.copy()
                    A2[:, 2] /= ks
                    if 0.8 < s2 < 1.25 and abs(A2[0, 2]) < 0.15 * w + abs(s2 - 1) * w and abs(A2[1, 2]) < 0.15 * h + abs(s2 - 1) * h:
                        cand = cv2.warpAffine(wl, A2, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                        err2 = lambda im: float(np.abs(cv2.resize(im, (180, 320)).astype(np.int16) - cv2.resize(bg, (180, 320)).astype(np.int16)).mean())
                        if err2(cand) < err2(wl) - 0.5 and (abs(s2 - 1) > 0.02 or np.hypot(A2[0, 2], A2[1, 2]) > 0.01 * w):
                            fr_ = min(1.0, 0.1 / max(1e-6, abs(s2 - 1)), 0.06 * w / max(1e-6, float(np.hypot(A2[0, 2], A2[1, 2]))))   # mỗi clip kéo tối đa ~10% phóng / 6% dời: mép hụt nhỏ, vài cảnh là về hẳn
                            # chỉ kéo trong phần ảnh THẬT của clip (không để lộ mép hụt phải lấp bằng ảnh khác: lấp bằng khung nối/ảnh gốc
                            # đều lộ vệt, đo 06/11/2026): tìm tỉ lệ lớn nhất mà khung cuối vẫn phủ kín
                            full = np.vstack([A2, [0, 0, 1]]) - np.eye(3)
                            covered = lambda f: cv2.warpAffine(ones, ((np.eye(3) + f * full) @ T_last)[:2], (w, h), flags=cv2.INTER_NEAREST, borderValue=0).mean() >= 254.0
                            lo_, hi_ = 0.0, fr_
                            if not covered(hi_):
                                for _ in range(8):
                                    mid = (lo_ + hi_) / 2
                                    lo_, hi_ = (mid, hi_) if covered(mid) else (lo_, mid)
                                fr_ = lo_
                            if fr_ > 0.05:
                                E = np.eye(3) + fr_ * full
                                note += f", kéo về bố cục gốc ({fr_:.0%} của x{s2:.3f}, {A2[0, 2]:+.0f},{A2[1, 2]:+.0f}px)"

    def warp_i(i):
        """(khung đã căn, độ phủ 0-1 hoặc None nếu phủ kín)."""
        if stab is None and M is None:
            return frames[i], None
        T = (M3 @ stab[i])[:2] if stab is not None else M3[:2]
        if E is not None and not np.array_equal(E, np.eye(3)):
            u = i / max(1, len(frames) - 1)
            u = 0.5 - 0.5 * np.cos(np.pi * u)   # ease: đứng yên ở hai đầu, không giật
            T = ((np.eye(3) + u * (E - np.eye(3))) @ np.vstack([T, [0, 0, 1]]))[:2]
        im = cv2.warpAffine(frames[i], T, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        cov = cv2.warpAffine(ones, T, (w, h), flags=cv2.INTER_NEAREST, borderValue=0)
        if cov.min() == 255:
            return im, None
        return im, cv2.GaussianBlur(cv2.erode(cov, np.ones((9, 9), np.uint8)), (0, 0), 6).astype(np.float32)[..., None] / 255
    first, last = warp_i(0)[0], warp_i(len(frames) - 1)[0]
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
                             "-c:a", "copy", "-shortest", "-f", "mp4", out + ".dang-ghi"], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for i, f in enumerate(frames):
            u = i / max(1, n - 1)
            g, o = ga + (gb - ga) * u, oa + (ob - oa) * u
            wi, cov = warp_i(i)
            lab = cv2.cvtColor(wi, cv2.COLOR_BGR2LAB).astype(np.float32) * g + o
            im = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
            if cov is not None:   # mép hụt: lấy đúng khung nối (đã đúng màu người xem vừa thấy)
                im = (im * cov + tgt * (1 - cov)).astype(np.uint8)
            if i < nb:   # hoà từ đúng khung nối sang clip (cosine)
                a = 0.5 + 0.5 * np.cos(np.pi * i / nb)
                im = cv2.addWeighted(tgt, a, im, 1 - a, 0)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        err = proc.stderr.read().decode("utf-8", "replace")
        if proc.wait():
            raise RuntimeError(f"ffmpeg lỗi khi căn khớp clip: {err[-300:]}")
        os.replace(out + ".dang-ghi", out)
    finally:
        if proc.poll() is None:
            proc.kill()
        if os.path.exists(out + ".dang-ghi"):
            os.remove(out + ".dang-ghi")
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
              "(smooth, even, natural skin; freckles, spots and pores no more and no darker than in #2; no added grain or blotches); never show, cut or fade to #2. "
              "The camera stands still on a tripod for the whole clip: the person keeps exactly the size and the position in the frame they have in #1, "
              "from the first frame to the last. ")
ORIG_NOTE = ("Reference image{s} {nums}: the ORIGINAL reference of this same character, for APPEARANCE ONLY: the face, head shape and every detail of the "
             "hair or head, skin, outfit and body must match it exactly in every frame, from the first frame to the last; never morph into a different "
             "person or a different design. Ignore its background, pose and framing; never show, cut or fade to it.")
LISTEN_MAX = 0.020      # clip NGHE: chặt hơn ngưỡng "đang nói" (người im lặng thật đo được 0,008-0,019)
LISTEN_RETRIES = 2
LISTEN_RETRIES_NO_SPARE = 4   # clip nghe có tiếng và chưa có clip nghe câm nào của nhân vật đó để dùng lại
FACE_PANEL_MAX = 0.12   # phần mặt nhân vật nền nằm dưới ô của nhân vật khác vượt mức này (khung nào cũng tính): gen lại (06/11/2026 di-tru: ô AI che nửa mặt Diego)


def face_under_panels(path, cfg, k, n_frames=8):
    """Tỉ lệ lớn nhất (0..1) diện tích khung mặt của nhân vật nền `k` nằm dưới các ô khác, trên vài khung của clip `path` (toàn khung, đúng toạ độ video).
    0 nếu `k` không phải nền toàn khung hoặc không dò được mặt."""
    if k != cfg.get("bg") or k in cfg["panels"]:
        return 0.0
    rects = [v for kk, v in cfg["panels"].items() if kk != k]
    if not rects:
        return 0.0
    import face_mesh as FM
    import numpy as np
    W, H = 360, 640
    dur = max(0.5, E.duration(path))
    worst = 0.0
    with E._MP_LOCK:
        fm = FM.landmarker(min_conf=0.3)
        try:
            for i in range(n_frames):
                t = dur * (i + 0.5) / n_frames
                d = E.crun(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           capture_output=True).stdout
                if len(d) < W * H * 3:
                    continue
                lm = fm.find(np.frombuffer(d[: W * H * 3], np.uint8).reshape(H, W, 3))
                if not lm:
                    continue
                xs, ys = [p.x for p in lm], [p.y for p in lm]
                x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
                area = max(1e-6, (x1 - x0) * (y1 - y0))
                for rx, ry, rw, rh in rects:
                    ix = max(0.0, min(x1, rx + rw) - max(x0, rx))
                    iy = max(0.0, min(y1, ry + rh) - max(y0, ry))
                    worst = max(worst, ix * iy / area)
        finally:
            fm.close()
    return worst


START_REGEN = 1.2       # mặt ở khung đầu clip to/nhỏ hơn khung nối gửi đi quá mức này (Muse bỏ qua khung đầu, vẽ lại cảnh): gen lại
ZOOM_REGEN = 1.15       # Muse tự phóng khung quá mức này trong một clip: gen lại (khoá camera lấp mép bằng khung đầu, phóng mạnh thì lộ vết ghép)
# Clip NGHE phải câm, nhưng Muse vẫn hay tự lồng tiếng lẩm bẩm vào (04/11/2026, chia-doi-gia-su-ai: 3/5 clip nghe có tiếng -23..-36 dB, Whisper nghe ra
# "This is me.", "It is dead and failure...") rồi tạo mặt theo tiếng đó: người nghe hé môi, gật gù, lắc lư đúng nhịp nói. Môi hé ít nên _mouth_score không
# bắt được (0,004-0,012). Clip câm thật đo được -63 dB. Vì vậy đo TIẾNG của clip nghe: to hơn ngưỡng này là clip đang "nói" -> gen lại / thay bằng ảnh tĩnh.
LISTEN_AUDIO_MAX_DB = -45.0


def _audio_db(path):
    """Độ to trung bình (dB) của tiếng trong clip; không có tiếng thì -inf."""
    import subprocess
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", out)
    return float(m.group(1)) if m and m.group(1) != "-inf" else float("-inf")


def _speech_end(path):
    """Giây hết chữ cuối trong clip (mốc từ Whisper). Không dùng dò khoảng lặng: clip Muse có tiếng nền phòng nên không có đoạn im thật."""
    wav = path + ".end.wav"
    try:
        E.sh(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
        ws = E._transcribe(wav, True).get("words") or []
        return float(ws[-1][2]) if ws else 0.0
    except Exception:  # noqa: BLE001
        return 0.0
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass


def _talky(path):
    """Clip nghe có tiếng nói lọt vào (Muse tự lồng tiếng): mặt trong clip đang nhép theo tiếng đó."""
    try:
        return _audio_db(path) > LISTEN_AUDIO_MAX_DB
    except Exception:  # noqa: BLE001 - không đo được thì coi như câm, không chặn việc gen
        return False
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


def _fresh(out, src):
    """File dẫn xuất `out` dùng lại được: có, không cũ hơn `src`, và đọc được (file dở do tắt LUO giữa chừng: thiếu moov atom -> xoá để làm lại)."""
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        return False
    try:
        if E.duration(out) > 0:
            return True
    except Exception:  # noqa: BLE001 - ffprobe không đọc được
        pass
    os.remove(out)
    return False


def _lock_on(cfg, k):
    """Khoá miệng (dán môi khép lên clip nghe) đã BỎ theo yêu cầu người dùng 06/11/2026: luôn False, dòng "khoa mieng: ..." trong kịch bản không còn tác dụng."""
    return False


def _locked(f, emit, pre, k):
    """Bản đã khoá miệng của clip nghe `f` (tạo nếu chưa có / cũ hơn clip); lỗi thì dùng clip gốc."""
    fl = f[:-4] + "_khoa.mp4"
    if _fresh(fl, f):
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
                             "-c:a", "copy", "-shortest", "-f", "mp4", out + ".dang-ghi"], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
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
        os.replace(out + ".dang-ghi", out)
    finally:
        if proc.poll() is None:
            proc.kill()
        if os.path.exists(out + ".dang-ghi"):
            os.remove(out + ".dang-ghi")
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


def _zoom_of(path):
    """Mức Muse tự phóng/thu khung trong clip (1.0 = camera đứng yên), đo trên ảnh thu nhỏ. Lỗi thì 1.0."""
    try:
        import cv2
        cap, frames, i = cv2.VideoCapture(path), [], 0
        while True:
            ok, f = cap.read()
            if not ok:
                break
            if i % 2 == 0:
                frames.append(cv2.resize(f, (360, int(f.shape[0] * 360 / f.shape[1])), interpolation=cv2.INTER_AREA))
            i += 1
        cap.release()
        return _camera_lock(frames)[1] if len(frames) > 2 else 1.0
    except Exception:  # noqa: BLE001
        return 1.0


def _start_mismatch(path, start_png):
    """Tỉ lệ cỡ mặt (chiều cao) giữa khung đầu clip và khung nối đã gửi Muse, >= 1 (1.0 = khớp). Không dò được mặt thì 1.0.
    05/11/2026, chia-doi BT19 (từ khi gửi Muse nguyên văn): robot to x1,4 ngay khung đầu, có clip đổi hẳn nền."""
    try:
        import cv2
        import face_mesh as FM
        cap = cv2.VideoCapture(path)
        ok, f = cap.read()
        cap.release()
        im = cv2.imread(start_png)
        if not ok or im is None:
            return 1.0
        with E._MP_LOCK:
            fm = FM.landmarker(min_conf=0.3)
            try:
                hs = []
                for x in (f, im):
                    lm = fm.find(cv2.cvtColor(x, cv2.COLOR_BGR2RGB))
                    hs.append((max(p.y for p in lm) - min(p.y for p in lm)) if lm else None)
            finally:
                fm.close()
        if not all(hs):
            return 1.0
        r = hs[0] / hs[1]
        return max(r, 1 / r)
    except Exception:  # noqa: BLE001
        return 1.0


def _mouth_score(path, t_end=None):
    try:
        m = E.mouth_activity(path, "0,0,1,1", min(E.duration(path), t_end) if t_end else E.duration(path))
        return m[0] if m else None
    except Exception:  # noqa: BLE001 - máy không chạy được đo miệng (mediapipe lỗi): bỏ qua
        return None


def _loop_clip(src, out, dur):
    """Clip nghe dài `dur` giây từ một clip nghe có sẵn: đi xuôi rồi ngược (ping-pong) cho đủ độ dài, không tiếng."""
    E.sh(["ffmpeg", "-y", "-i", src, "-filter_complex",
          f"[0:v]fps=30,setsar=1,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,loop=loop=-1:size=32767,trim=duration={dur:.3f},setpts=PTS-STARTPTS,format=yuv420p[v]",
          "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "17", "-preset", "fast", out])


def _gen_listen(gen, blocks, k, vdata, cfg, base_png, f, dur, check, emit, n=None, t_end=None, ident=None, spare=None, orig=None):
    """Gen một clip nghe; nếu đo được miệng cử động (trong đoạn sẽ dùng, [0, t_end]) quá ngưỡng người nghe thì gen lại tối đa LISTEN_RETRIES lần
    kèm yêu cầu chặt hơn, giữ bản ít cử động nhất. Người nghe hé môi như đang nói khi người kia nói là lỗi dễ thấy nhất (03/11/2026: 0,025 vẫn lọt ngưỡng nói 0,029).
    Luôn đo TIẾNG của clip (kể cả khi tắt kiểm tra miệng): Muse hay tự lồng tiếng lẩm bẩm vào clip nghe và cho mặt nhép theo (xem LISTEN_AUDIO_MAX_DB).
    Clip có tiếng thì gen lại; sau LISTEN_RETRIES lần vẫn có tiếng thì dùng lại `spare` (clip nghe câm gần nhất của chính nhân vật này, còn chớp mắt, cử động
    tự nhiên; người gọi căn khớp nó về khung nối), chưa có thì giữ bản Muse ít tiếng nhất. Không dựng clip từ ảnh tĩnh: người dùng không muốn nhân vật đứng như ảnh (04/11/2026)."""
    aspect = aspect_of(cfg, k)
    who = f"{'Cảnh ' + str(n) + ': c' if n else 'C'}lip nghe của {k}"

    def bad(path):
        """(có tiếng nói, độ to nếu có tiếng, mức cử động miệng): so sánh được, nhỏ hơn = tốt hơn."""
        s = _mouth_score(path, t_end) if check else None
        t = _talky(path)
        z, m = _zoom_of(path), _start_mismatch(path, base_png)
        try:
            fp = face_under_panels(path, cfg, k)   # mặt nhân vật nền lọt dưới ô khác (06/11/2026 di-tru: ô AI che mặt Diego)
        except Exception:  # noqa: BLE001
            fp = 0.0
        return (t, round(_audio_db(path), 1) if t else -99.0, z > ZOOM_REGEN or m > START_REGEN or fp > FACE_PANEL_MAX, s if s is not None else 0.0, max(z, m))

    def ok(b):
        return not b[0] and not b[2] and b[3] < LISTEN_MAX

    gen("video", listen_prompt(blocks, k, vdata, aspect, dur), base_png, f, aspect, dur=dur, n=n, state="video", ident=ident, orig=orig)
    best = (bad(f), f)
    if ok(best[0]):
        return
    tries = []
    i = 0
    while i < (LISTEN_RETRIES if spare or not best[0][0] else LISTEN_RETRIES_NO_SPARE):   # còn tiếng mà chưa có clip câm dự phòng: thử thêm
        lim = LISTEN_RETRIES if spare or not best[0][0] else LISTEN_RETRIES_NO_SPARE
        why = (f"có tiếng nói lọt vào ({_audio_db(best[1]):.0f} dB): mặt đang nhép theo tiếng đó" if best[0][0]
               else f"khung hình lệch khung nối / tự phóng x{best[0][4]:.2f} / mặt lọt dưới ô khác" if best[0][2]
               else f"miệng cử động như đang nói (mức {best[0][3]:.3f}, ngưỡng {LISTEN_MAX})")
        emit("log", msg=f"{who}: {why}, gen lại {i + 1}/{lim}", level="warn")
        tmp = f"{f}.try{i}.mp4"
        tries.append(tmp)
        gen("video", listen_prompt(blocks, k, vdata, aspect, dur, strict=True), base_png, tmp, aspect, dur=dur, n=n, state="video", ident=ident, orig=orig)
        b1 = bad(tmp)
        if b1 < best[0]:
            best = (b1, tmp)
        if ok(best[0]):
            break
        i += 1
    if best[1] != f:
        os.replace(best[1], f)
    for t in tries:
        if os.path.exists(t):
            os.remove(t)
    if best[0][0]:   # gen lại vẫn có tiếng: không dùng clip Muse (người nghe sẽ nhép theo)
        if spare and os.path.exists(spare):
            _loop_clip(spare, f, dur)
            emit("log", msg=f"{who}: gen lại vẫn có tiếng nói, dùng lại clip nghe câm {os.path.basename(spare)} của {k} (căn khớp về khung nối)", level="warn")
        else:
            emit("log", msg=f"{who}: gen lại vẫn có tiếng nói và chưa có clip nghe câm nào của {k}, giữ bản ít tiếng nhất ({best[0][1]:.0f} dB). "
                            "Bấm gen lại cảnh này nếu thấy mấp máy", level="warn")
    elif best[0][3] >= LISTEN_MAX:
        emit("log", msg=f"Clip nghe của {k}: vẫn còn cử động miệng (mức {best[0][3]:.3f}), giữ bản ít nhất. Bấm gen lại cảnh này nếu thấy mấp máy", level="warn")
