"""Hậu kỳ riêng của thể loại "robot đứng phố dạy tiếng lóng" (robot-pho-tieng-long). Studio gọi:
    python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Video Muse chỉ có robot nói trước nền phố. Hậu kỳ vẽ bằng code (PIL + ffmpeg + ASS), như video mẫu:
  1. Tiêu đề: ô xanh bo góc 2 dòng phía trên đầu robot, suốt video (HAU_KY.tieu_de).
  2. Badge sự kiện: ô cam + ô trắng bên trái, suốt video (HAU_KY.badge; bỏ qua nếu thiếu).
  3. Thẻ từ lóng (HAU_KY.the): đầu xanh (nhãn nhỏ "TEXANS SAY", từ to, đếm n/N) + thân trắng ("IT MEANS" + nghĩa). Thẻ hiện khi robot nói
     từ đó (moc_tu), nghĩa hiện khi robot nói nghĩa (moc_nghia), trước đó thân thẻ hiện "..."; thẻ giữ tới khi thẻ sau hiện (thẻ cuối giữ tới hết).
  4. Phụ đề karaoke: cụm 2–4 từ trên ô xanh bo góc, từ đang nói đổi sang xanh nhạt. Mốc từng từ lấy từ Whisper theo từng cảnh
     (postprocess.transcribe với jobs), khớp mờ với lời của biến thể; từ không nghe thấy thì nội suy.
Không logo, không end card: Thương hiệu của dự án gắn sau. Tham số bố cục: config.json cùng thư mục."""
import argparse
import difflib
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.dirname(os.path.dirname(HERE))
if PROD not in sys.path:
    sys.path.insert(0, PROD)
import postprocess as PP  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

W, H = 1080, 1920


def norm(w):
    """Dạng so khớp: chữ thường, bỏ dấu, chỉ giữ chữ/số (Latin, Devanagari...). 11/11/2026: biến thể Hindi/Bồ Đào Nha (trước chỉ giữ a-z0-9 nên từ Hindi bị bỏ)."""
    s = "".join(c for c in unicodedata.normalize("NFD", str(w).lower()) if not unicodedata.combining(c))
    return re.sub(r"[\W_]", "", s)


def rgb(c):
    return tuple(int(x) for x in c)


def bgr_hex(c):
    r, g, b = rgb(c)
    return f"{b:02X}{g:02X}{r:02X}"


# ---------------------------------------------------------------- mốc từng từ
def words_of_turns(raw, luot, scenes, model, lang="en"):
    """{chỉ số lượt: [(từ của biến thể, s, e)]}: Whisper theo từng cảnh, khớp mờ tuần tự với lời của biến thể, từ không nghe thấy nội suy."""
    by_turn = {s["turn"]: s for s in scenes}
    total = PP.duration(raw)
    idx = [i for i in range(len(luot)) if i in by_turn]
    jobs = []
    for i in idx:
        sc = by_turn[i]
        a, b = max(0.0, sc.get("speech", sc["start"]) - 0.2), min(total, sc["end"] + 0.2)
        jobs.append({"a": a, "b": b, "prompt": luot[i]["text"], "lang": lang})
    heard = PP.transcribe(raw, model, None, vad=True, jobs=jobs) if jobs else []
    if heard is None:
        print("CẢNH BÁO: máy này không chạy được nhận dạng giọng; mốc từ ước lượng đều trong từng cảnh.")
        heard = [[] for _ in jobs]
    out = {}
    for i, ws in zip(idx, heard):
        sc = by_turn[i]
        t0, t1 = sc.get("speech", sc["start"]), sc["end"]
        vw = [w for w in luot[i]["text"].split() if norm(w)]
        toks = [(norm(w), s, e) for w, s, e in ws if norm(w)]
        times, p = [], 0
        for w in vw:
            best = None
            for j in range(p, min(p + 6, len(toks))):
                r = difflib.SequenceMatcher(None, norm(w), toks[j][0]).ratio()
                if r >= 0.6 and (best is None or r > best[0] + 0.15):
                    best = (r, j)
                    if r > 0.9:
                        break
            if best:
                j = best[1]
                times.append([toks[j][1], toks[j][2]])
                p = j + 1
            else:
                times.append(None)
        # nội suy từ không khớp
        n = len(times)
        k = 0
        while k < n:
            if times[k] is None:
                j = k
                while j < n and times[j] is None:
                    j += 1
                lo = times[k - 1][1] if k > 0 else t0 + 0.1
                hi = times[j][0] if j < n else max(lo + 0.3 * (j - k), t1 - 0.3)
                step = max(0.12, (hi - lo) / (j - k))
                for m in range(k, j):
                    times[m] = [lo + step * (m - k), min(hi, lo + step * (m - k + 1))]
                k = j
            else:
                k += 1
        for k in range(n):   # mỗi từ kéo dài tới từ kế tiếp (không hở), nằm trong cảnh
            s = max(t0, times[k][0])
            e = times[k + 1][0] if k + 1 < n else min(t1, times[k][1] + 0.3)
            times[k] = [s, max(s + 0.08, min(e, t1))]
        out[i] = [(w, s, e) for w, (s, e) in zip(vw, times)]
        miss = sum(1 for t in heard[idx.index(i)]) == 0
        print(f"  lượt {i + 1}: {len(vw)} từ, {'KHÔNG nghe thấy (ước lượng)' if miss else f'{len(toks)} từ Whisper'}  {out[i][0][1]:.2f}-{out[i][-1][2]:.2f}s")
    return out


def find_word(words, key, start=0):
    """Chỉ số từ đầu tiên (từ `start`) mà dạng chuẩn bắt đầu bằng / chứa `key`."""
    k = norm(key)
    if not k:
        return None
    for i in range(start, len(words)):
        n = norm(words[i][0])
        if n == k or n.startswith(k) or (len(k) >= 4 and k in n):
            return i
    return None


# ---------------------------------------------------------------- vẽ lớp bằng PIL
def _font(path, size):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)


def _shadow(im, box, radius, alpha=90, blur=12, dy=10):
    from PIL import Image, ImageDraw, ImageFilter
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=radius, fill=(0, 0, 0, alpha))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))


def face_top(raw, scenes):
    """Mép trên khuôn mặt (px, khung 1080x1920) đo ở vài khung rải trong video (Haar cascade), lấy trung vị; không thấy -> None."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None
    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    total = PP.duration(raw)
    tops = []
    for k in range(6):
        t = total * (k + 0.5) / 6
        png = raw + f".ft{k}.png"
        try:
            PP.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", raw, "-frames:v", "1", "-vf", f"scale={W}:{H}", png])
            im = cv2.imread(png)
            faces = det.detectMultiScale(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(int(W * 0.12), int(W * 0.12)))
            if len(faces):
                x, y, fw, fh = max(faces, key=lambda r: r[2] * r[3])
                tops.append(int(y))
        except Exception:  # noqa: BLE001
            pass
        finally:
            try:
                os.remove(png)
            except OSError:
                pass
    return int(np.median(tops)) if tops else None


def render_title(cfg, lines, path, face_y=None):
    from PIL import Image, ImageDraw
    c = dict(cfg["tieu_de"])
    if face_y is not None and c["y"] + c["h"] > face_y - 24:   # ô tiêu đề không được che mắt: đẩy lên trên khuôn mặt (robot gen đứng thấp hơn mẫu)
        c["y"] = max(int(cfg.get("tieu_de_y_min", 110)), face_y - 24 - c["h"])
        print(f"  tiêu đề dời lên y={c['y']} (mặt bắt đầu ở {face_y})")
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    box = (c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"])
    _shadow(im, box, c["bo"])
    d = ImageDraw.Draw(im)
    # nền chuyển sắc xanh nhạt -> xanh đậm (vẽ dải ngang rồi che bằng mặt nạ bo góc)
    grad = Image.new("RGBA", (c["w"], c["h"]), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    top, bot = rgb(cfg["xanh"]), rgb(cfg["xanh_dam"])
    for y in range(c["h"]):
        t = y / max(1, c["h"] - 1)
        gd.line([(0, y), (c["w"], y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))
    mask = Image.new("L", (c["w"], c["h"]), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, c["w"] - 1, c["h"] - 1), radius=c["bo"], fill=255)
    im.paste(grad, (c["x"], c["y"]), mask)
    f = _font(cfg["font"], c["co_chu"])
    n = len(lines)
    block = c["cach_dong"] * n
    y = c["y"] + (c["h"] - block) / 2 + (c["cach_dong"] - c["co_chu"]) / 2 - 2
    for i, line in enumerate(lines):
        col = (255, 255, 255, 255) if i == 0 else rgb(cfg["xanh_nhat"]) + (255,)
        tw = d.textlength(line, font=f)
        d.text((c["x"] + (c["w"] - tw) / 2, y + i * c["cach_dong"]), line, font=f, fill=col)
    im.save(path)


def render_badge(cfg, trai, phai, path):
    from PIL import Image, ImageDraw
    c = cfg["badge"]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = _font(cfg["font"], c["co_chu"])
    d = ImageDraw.Draw(im)
    w1 = d.textlength(trai, font=f) + c["pad"] * 2
    w2 = d.textlength(phai, font=f) + c["pad"] * 2
    x, y, h = c["x"], c["y"], c["h"]
    _shadow(im, (x, y, x + w1 + w2, y + h), c["bo"], alpha=70, blur=8, dy=6)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, y, x + w1 + w2, y + h), radius=c["bo"], fill=(255, 255, 255, 255))
    d.rounded_rectangle((x, y, x + w1, y + h), radius=c["bo"], fill=rgb(cfg["cam"]) + (255,))
    d.rectangle((x + w1 - c["bo"], y, x + w1, y + h), fill=rgb(cfg["cam"]) + (255,))   # góc trong vuông
    ty = y + (h - c["co_chu"]) / 2 - 3
    d.text((x + c["pad"], ty), trai, font=f, fill=(255, 255, 255, 255))
    d.text((x + w1 + c["pad"], ty), phai, font=f, fill=rgb(cfg["muc"]) + (255,))
    im.save(path)


def render_card(cfg, nhan_tu, tu, nhan_nghia, nghia, dem, path):
    """Thẻ từ lóng: đầu xanh (nhãn, từ to, đếm) + thân trắng (nhãn, nghĩa hoặc '...')."""
    from PIL import Image, ImageDraw
    c = cfg["the"]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x, y, w, hd, hb, bo = c["x"], c["y"], c["w"], c["h_dau"], c["h_than"], c["bo"]
    _shadow(im, (x, y, x + w, y + hd + hb), bo)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, y, x + w, y + hd + hb), radius=bo, fill=(255, 255, 255, 255))
    d.rounded_rectangle((x, y, x + w, y + hd), radius=bo, fill=rgb(cfg["xanh"]) + (255,))
    d.rectangle((x, y + hd - bo, x + w, y + hd), fill=rgb(cfg["xanh"]) + (255,))
    f_nhan, f_tu, f_nghia, f_dem = (_font(cfg["font"], c[k]) for k in ("co_nhan", "co_tu", "co_nghia", "co_dem"))
    pad = 28
    d.text((x + pad, y + 10), nhan_tu, font=f_nhan, fill=(215, 230, 255, 255))
    f = f_tu
    while d.textlength(tu, font=f) > w - pad * 2 - 90 and f.size > 30:
        f = _font(cfg["font"], f.size - 2)
    d.text((x + pad + 24, y + 10 + c["co_nhan"] + 4), tu, font=f, fill=(255, 255, 255, 255))
    dw = d.textlength(dem, font=f_dem)
    d.text((x + w - pad - dw, y + 10), dem, font=f_dem, fill=(215, 230, 255, 255))
    d.text((x + pad, y + hd + 8), nhan_nghia, font=f_nhan, fill=(120, 130, 150, 255))
    f = f_nghia
    while d.textlength(nghia, font=f) > w - pad * 2 - 20 and f.size > 24:
        f = _font(cfg["font"], f.size - 2)
    d.text((x + pad + 24, y + hd + 8 + c["co_nhan"]), nghia, font=f, fill=rgb(cfg["muc"]) + (255,))
    im.save(path)


# ---------------------------------------------------------------- phụ đề karaoke (ASS)
def chunks_of(words, max_words):
    """Chia các từ của một lượt thành cụm 2–max_words từ, cắt ở dấu câu; không để cụm 1 từ lẻ cuối câu."""
    out, cur = [], []
    for i, (w, s, e) in enumerate(words):
        cur.append(i)
        end_sent = bool(re.search(r"[.!?,…।]$", w))
        if end_sent or len(cur) >= max_words:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    merged = []
    for g in out:
        if merged and len(g) == 1 and len(merged[-1]) < max_words + 1 and not re.search(r"[.!?।]$", words[merged[-1][-1]][0]):
            merged[-1] = merged[-1] + g
        else:
            merged.append(g)
    return merged


def write_subs(cfg, turn_words, scenes, path, font=None):
    c = cfg["phu_de"]
    size, pad = c["co_chu"], c["pad_x"]
    blue, hi = bgr_hex(cfg["xanh"]), bgr_hex(cfg["xanh_nhat"])
    font = font or cfg.get("font_ass", "Arial")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Box,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00{blue},&H00{blue},-1,0,0,0,100,100,0,0,3,{pad},0,5,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ts, lines = PP.ts, []
    by_turn = {s["turn"]: s for s in scenes}
    for ti in sorted(turn_words):
        words = turn_words[ti]
        groups = chunks_of(words, int(c.get("toi_da_tu", 3)))
        t_end = by_turn[ti]["end"]
        for gi, g in enumerate(groups):
            g_start = words[g[0]][1]
            g_stop = words[groups[gi + 1][0]][1] - 0.02 if gi + 1 < len(groups) else min(t_end, words[g[-1]][2] + 0.25)
            for k, wi in enumerate(g):
                s = words[wi][1] if k else g_start
                e = words[g[k + 1]][1] if k + 1 < len(g) else g_stop
                if e <= s:
                    continue
                parts = []
                for m, wj in enumerate(g):
                    txt = words[wj][0].replace("{", "").replace("}", "")
                    parts.append(("{\\1c&H" + hi + "&}" + txt + "{\\1c&HFFFFFF&}") if m == k else txt)
                fs = size
                text = " ".join(words[wj][0] for wj in g)
                while PP.text_width(text, fs, font) > c.get("toi_da_rong", 900) and fs > 34:
                    fs -= 2
                lines.append(f"Dialogue: 1,{ts(s)},{ts(e)},Box,,0,0,0,,{{\\an5\\pos({W // 2},{c['y']})\\fs{fs}}}" + " ".join(parts))
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(head + "\n".join(lines) + "\n")
    return len(lines)


# ---------------------------------------------------------------- ghép
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--scenes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"))
    ap.add_argument("--model")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    scenes = json.load(open(a.scenes, encoding="utf-8"))
    v = json.load(open(a.variant, encoding="utf-8"))
    v = v[0] if isinstance(v, list) else v
    luot = [t for t in v.get("LUOT", []) if str(t.get("text", "")).strip()]
    hk = v.get("HAU_KY") or {}
    total = PP.duration(a.raw)
    lang = str(hk.get("ngon_ngu") or "en")   # "hi" / "pt": Whisper đa ngôn ngữ; phụ đề chữ Devanagari cần font Nirmala UI + shaping complex (HAU_KY.font_ass, HAU_KY.shaping)
    model = a.model or (cfg.get("whisper", "small.en") if lang == "en" else cfg.get("whisper_da_ngu", "small"))
    print(f"Biến thể \"{v.get('name', '')}\": {len(luot)} lượt, {len(scenes)} cảnh, {len(hk.get('the', []))} thẻ từ lóng; Whisper {model}")
    turn_words = words_of_turns(a.raw, luot, scenes, model, lang)
    work = tempfile.mkdtemp(prefix="pho_pp_")
    try:
        overlays = []   # (png, s, e)
        if hk.get("tieu_de"):
            p = os.path.join(work, "title.png")
            render_title(cfg, [str(x) for x in hk["tieu_de"]][:2], p, face_top(a.raw, scenes))
            overlays.append((p, 0.0, total))
        b = hk.get("badge") or {}
        if b.get("trai") or b.get("phai"):
            p = os.path.join(work, "badge.png")
            render_badge(cfg, str(b.get("trai", "")), str(b.get("phai", "")), p)
            overlays.append((p, 0.0, total))
        cards = [c for c in hk.get("the", []) if int(c.get("luot", -1)) in turn_words]
        pre = float(cfg.get("hien_truoc_tu", 0.05))
        starts = []
        for c in cards:
            ws = turn_words[int(c["luot"])]
            i_tu = find_word(ws, c.get("moc_tu") or str(c["tu"]).split()[0])
            if i_tu is None:
                i_tu = 0
            t_tu = ws[i_tu][1]
            i_ng = find_word(ws, c.get("moc_nghia") or str(c["nghia"]).split()[0], i_tu + 1)
            t_ng = ws[i_ng][1] if i_ng is not None else min(ws[-1][2], t_tu + 1.2)
            starts.append((max(0.0, t_tu - pre), max(t_tu, t_ng - pre), c))
        for n, (t_tu, t_ng, c) in enumerate(starts):
            t_next = starts[n + 1][0] if n + 1 < len(starts) else (total if cfg.get("giu_the_cuoi", True) else scenes[-1]["end"])
            dem = f"{n + 1}/{len(starts)}"
            p1, p2 = os.path.join(work, f"card{n}a.png"), os.path.join(work, f"card{n}b.png")
            render_card(cfg, hk.get("nhan_tu", "THEY SAY"), str(c["tu"]), hk.get("nhan_nghia", "IT MEANS"), "...", dem, p1)
            render_card(cfg, hk.get("nhan_tu", "THEY SAY"), str(c["tu"]), hk.get("nhan_nghia", "IT MEANS"), str(c["nghia"]), dem, p2)
            if t_ng > t_tu + 0.05:
                overlays.append((p1, t_tu, t_ng))
            overlays.append((p2, max(t_tu, t_ng), t_next))
            print(f"  thẻ {dem} {c['tu']!r}: {t_tu:.2f}s, nghĩa {t_ng:.2f}s, giữ tới {t_next:.2f}s")
        n_sub = write_subs(cfg, turn_words, scenes, os.path.join(work, "subs.ass"), hk.get("font_ass"))
        print(f"  phụ đề: {n_sub} mốc từ")
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", os.path.abspath(a.raw)]
        fc = f"[0:v]scale={W}:{H}:flags=lanczos,fps=30[v0]"
        last = "v0"
        for i, (png, s, e) in enumerate(overlays):
            cmd += ["-i", png]
            fc += f";[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'[v{i + 1}]"
            last = f"v{i + 1}"
        fc += f";[{last}]" + (f"ass=subs.ass:shaping={hk['shaping']}" if hk.get("shaping") else "subtitles=subs.ass") + "[v]"
        cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "out.mp4"]
        PP.run(cmd, cwd=work)
        shutil.move(os.path.join(work, "out.mp4"), a.out)
        print("XONG ->", a.out, f"({PP.duration(a.out):.1f}s)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
