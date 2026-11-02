"""Hậu kỳ riêng cho thể loại "AI tutor ngồi đọc" (SAMPLE/ai-tutor-ngoi-doc).
Video Muse chỉ có robot ngồi đọc (phần trên khung để trống). Hậu kỳ:
  1. khung bảng: gen bằng AI (Muse) theo ô CO của biến thể (cờ, linh vật), trên phông xanh rồi cắt phông; lưu board.png trong thư mục chạy để dùng lại;
  2. chữ trong bảng do code điền theo ô BANG_TU ("tiếng mẹ đẻ | tiếng học | phiên âm"), đổi đúng lúc robot đọc từng cặp (Whisper theo từng cảnh);
  3. nhãn góc dưới (ô NHAN, vd. "AI Learning"). Không phụ đề, không end card.
Dùng: python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json [--model medium] [--board board.png]"""
import argparse, glob, json, os, re, shutil, subprocess, sys, tempfile, time, unicodedata

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(PROD))
sys.path[:0] = [PROD]
import postprocess as P  # noqa: E402

W, H = 1080, 1920
FONT_B = r"C:\Windows\Fonts\arialbd.ttf" if os.name == "nt" else "DejaVuSans-Bold.ttf"
LANG = {"portuguese": "pt", "english": "en", "spanish": "es", "french": "fr", "german": "de", "italian": "it", "vietnamese": "vi",
        "japanese": "ja", "korean": "ko", "chinese": "zh", "russian": "ru", "turkish": "tr", "arabic": "ar", "hindi": "hi", "indonesian": "id"}


def fold(s):
    return re.sub(r"[^a-z0-9 ]", " ", unicodedata.normalize("NFKD", str(s).lower()).encode("ascii", "ignore").decode()).split()


def lang_code(name):
    n = str(name).lower()
    return next((c for k, c in LANG.items() if k in n), None)


# ---------------------------------------------------------------- bảng từ trong biến thể
def parse_bang(text):
    rows = [[c.strip() for c in l.split("|")] for l in str(text).strip().splitlines() if l.strip()]
    pairs = [(r[0], r[1], r[2] if len(r) > 2 else "") for r in rows if len(r) >= 2]
    closing = next((r[0] for r in rows if len(r) == 1), "")
    return pairs, closing


# ---------------------------------------------------------------- khung bảng gen bằng AI
def _api():
    import gen_video as G
    studio = os.environ.get("LUO_STUDIO_DATA") or os.path.join(ROOT, "userdata", "studio")
    try:
        st = json.load(open(os.path.join(studio, "settings.json"), encoding="utf-8"))
    except (OSError, ValueError):
        st = {}
    os.environ.setdefault("MUSE2API_HOME", os.path.join(os.path.dirname(studio), "api"))
    return G, G.Api(os.environ.get("LUO_API_URL") or st.get("api_url") or "http://127.0.0.1:18610", st.get("api_key") or G.read_key())


def board_prompt(deco):
    return ("Generate exactly one still image (the image itself, not a description of it). A cheerful classroom-style wall board seen straight on, "
            "a WIDE HORIZONTAL LANDSCAPE rectangle about twice as wide as it is tall (aspect ratio 2:1, like a whiteboard or TV screen, NOT portrait, NOT square), "
            "centered and filling most of the frame width: a thick rounded wooden frame with a bright painted stripe pattern on its inner border, "
            "and a large, completely blank, plain white rectangular panel inside it (absolutely no text, letters or marks on the panel). "
            f"Decoration on top of the frame: {deco}. "
            "The whole board is isolated on a perfectly flat, evenly lit, pure chroma-key green (#00B140) background, with no shadow on the background "
            "and no other objects. No text, letters, numbers or logos anywhere in the image. Output only the generated image, with no written reply.")


def _key(raw_png):
    a = np.asarray(Image.open(raw_png).convert("RGB")).astype(np.float32)
    r, g, bl = a[..., 0], a[..., 1], a[..., 2]
    spill = g - np.maximum(r, bl)
    alpha = np.clip((60 - spill) / 35, 0, 1)
    g2 = np.minimum(g, np.maximum(r, bl) + 8)
    im = Image.fromarray(np.dstack([r, g2, bl, alpha * 255]).clip(0, 255).astype(np.uint8), "RGBA")
    return im.crop(im.getbbox())


def make_board(deco, cache_png, log=print):
    """Ảnh bảng RGBA (đã cắt phông xanh, cắt sát) + toạ độ lòng trắng (x0, y0, x1, y1). Dùng lại cache nếu có."""
    meta = cache_png + ".json"
    if os.path.exists(cache_png) and os.path.exists(meta):
        return Image.open(cache_png).convert("RGBA"), tuple(json.load(open(meta))["inner"])
    raw_png = cache_png.replace(".png", "_raw.png")
    best = None
    for attempt in range(3):
        if not os.path.exists(raw_png):
            log("Gen khung bảng bằng AI (Muse)...")
            G, api = _api()
            b = api.generate("image", G.muse_image_prompt(board_prompt(deco), "", 0), [], f"bang-{int(time.time())}", timeout=600, log=lambda m: None)
            if G.kind_of(b) == "video":
                open(raw_png + ".mp4", "wb").write(b)
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw_png + ".mp4", "-frames:v", "1", raw_png], check=True)
                os.remove(raw_png + ".mp4")
            else:
                open(raw_png, "wb").write(b)
        im = _key(raw_png)
        if best is None or im.width / im.height > best[0].width / best[0].height:
            best = (im, raw_png + f".{attempt}")
            shutil.copy(raw_png, best[1])
        if im.width / im.height >= 1.6:
            break
        log(f"Khung bảng chưa đủ ngang ({im.width}x{im.height}), gen lại...")
        os.remove(raw_png)
    im = best[0]
    shutil.copy(best[1], raw_png)
    for f in glob.glob(raw_png + ".[0-9]"):
        os.remove(f)
    if im.width / im.height < 1.6:
        im = im.resize((int(im.height * 1.8), im.height), Image.LANCZOS)
    inner = find_inner(im)
    im.save(cache_png)
    json.dump({"inner": inner}, open(meta, "w"))
    return im, inner


def find_inner(im):
    """Lòng trắng của bảng: vùng các hàng/cột phần lớn là điểm trắng."""
    a = np.asarray(im).astype(int)
    white = (a[..., :3].min(2) > 215) & (a[..., 3] > 200)
    h, w = white.shape
    cols = np.nonzero(white.mean(0) > 0.35)[0]
    rows = np.nonzero(white.mean(1) > 0.45)[0]
    if len(cols) < w * 0.3 or len(rows) < h * 0.2:
        return (int(w * 0.1), int(h * 0.25), int(w * 0.9), int(h * 0.9))
    return (int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1]))


def fallback_board():
    """Không gen được bảng (mất kết nối API): vẽ bảng đơn giản bằng code để vẫn ra video."""
    im = Image.new("RGBA", (1000, 500), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 20, 999, 499), 26, fill=(196, 128, 52, 255))
    d.rounded_rectangle((26, 46, 973, 473), 14, fill=(255, 255, 255, 255))
    return im, (36, 56, 964, 464)


# ---------------------------------------------------------------- vẽ chữ
def _font(px):
    return ImageFont.truetype(FONT_B, max(10, int(px)))


def _fit(d, text, px, maxw):
    while px > 14 and d.textlength(text, font=_font(px)) > maxw:
        px -= 2
    return _font(px)


def render_card(board, inner, place, pair, closing=None):
    """Khung bảng + chữ của một cặp (hoặc câu kết), ảnh trong suốt W x H."""
    bx, by, scale = place
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = board.resize((int(board.width * scale), int(board.height * scale)), Image.LANCZOS)
    im.alpha_composite(bd, (bx, by))
    x0, y0, x1, y1 = [int(v * scale) for v in inner]
    x0, x1, y0, y1 = bx + x0, bx + x1, by + y0, by + y1
    iw, ih = x1 - x0, y1 - y0
    d = ImageDraw.Draw(im)
    cx = (x0 + x1) / 2
    if closing:
        f = _fit(d, closing, ih * 0.3, iw * 0.9)
        tw = d.textlength(closing, font=f)
        d.text((cx - tw / 2, y0 + ih / 2 - f.size * 0.6), closing, font=f, fill=(255, 210, 0, 255), stroke_width=max(2, f.size // 12), stroke_fill=(90, 40, 0, 255))
        return im
    native, target, pron = pair
    f1, f2, f3 = _fit(d, native, ih * 0.2, iw * 0.9), _fit(d, target, ih * 0.28, iw * 0.92), _fit(d, pron, ih * 0.17, iw * 0.9)
    gap = ih * 0.06
    total = f1.size + f2.size + (f3.size if pron else 0) + gap * (2 if pron else 1)
    y = y0 + (ih - total) / 2
    for text, f, col, under in ((native, f1, (20, 20, 20, 255), True), (target, f2, (226, 44, 36, 255), False), (pron, f3, (226, 44, 36, 255), False)):
        if not text:
            continue
        tw = d.textlength(text, font=f)
        d.text((cx - tw / 2, y), text, font=f, fill=col)
        if under:
            d.line((cx - tw / 2, y + f.size * 1.12, cx + tw / 2, y + f.size * 1.12), fill=col, width=max(2, f.size // 14))
        y += f.size + gap
    return im


def render_label(text, avatar):
    """Nhãn góc dưới: viên thuốc trắng, ảnh robot tròn, chữ xanh đậm."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    hgt, x, y = int(H * 0.058), int(W * 0.03), int(H * 0.885)
    f = _font(hgt * 0.5)
    tw = d.textlength(text, font=f)
    wid = int(hgt * 1.4 + tw + hgt * 0.9)
    d.rounded_rectangle((x + hgt // 2, y, x + wid, y + hgt), hgt // 2, fill=(255, 255, 255, 240))
    d.text((x + hgt * 1.35, y + hgt * 0.22), text, font=f, fill=(52, 52, 200, 255))
    if avatar is not None:
        s = int(hgt * 1.25)
        av = avatar.resize((s, s), Image.LANCZOS)
        mask = Image.new("L", (s, s), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), s // 5, fill=255)
        bg = Image.new("RGBA", (s, s), (40, 90, 220, 255))
        bg.alpha_composite(av.convert("RGBA"))
        im.paste(bg, (x, y + hgt // 2 - s // 2), mask)
    return im


# ---------------------------------------------------------------- mốc lời nói
def find_seq(words, phrase, after):
    toks = fold(phrase)
    if not toks:
        return None
    ws = [(t, a) for w, a, b in words for t in fold(w)]
    for i in range(len(ws)):
        if ws[i][1] <= after:
            continue
        if [t for t, _ in ws[i:i + len(toks)]] == toks:
            return ws[i][1]
    return next((a for t, a in ws if a > after and t == toks[0]), None)   # Whisper nghe khác: khớp từ đầu


def timeline(raw, scenes, turns, pairs, closing, model, lang):
    """Mốc bắt đầu của từng cặp (theo câu tiếng mẹ đẻ) và của câu kết, trong raw.mp4."""
    owner = []   # cảnh chứa từng cặp: cảnh mà lời đọc có câu tiếng mẹ đẻ của cặp đó
    ti = 0
    for a, b, _ in pairs:
        k = ti
        while k < len(turns) and " ".join(fold(a)) not in " ".join(fold(turns[k].get("text", ""))):
            k += 1
        ti = k if k < len(turns) else ti
        owner.append(ti)
    by = {s["turn"]: s for s in scenes}
    jobs = [{"a": max(0.0, by[t]["start"] - 0.1), "b": by[t]["end"] + 0.1, "prompt": turns[t]["text"], "lang": lang} for t in range(len(turns)) if t in by]
    res = P.transcribe(raw, model, None, vad=True, jobs=jobs) or [[] for _ in jobs]
    words = {t: r for t, r in zip([t for t in range(len(turns)) if t in by], res)}
    starts, last = [], -1.0
    for (a, b, _), t in zip(pairs, owner):
        if t not in by:
            starts.append(None)
            continue
        s = find_seq(words.get(t, []), a, max(last, by[t]["start"] - 0.2))
        starts.append(s)
        if s is not None:
            last = s
    # cặp không nghe ra: chia đều trong cảnh của nó
    for t in set(owner):
        idx = [i for i, o in enumerate(owner) if o == t]
        if t in by and any(starts[i] is None for i in idx):
            sc = by[t]
            for j, i in enumerate(idx):
                if starts[i] is None:
                    starts[i] = sc["start"] + (sc["end"] - sc["start"]) * j / len(idx)
    t_close = None
    if closing and turns:
        tc = len(turns) - 1
        if tc in by:
            t_close = find_seq(words.get(tc, []), closing, max([s for s in starts if s is not None] + [0.0]))
    return starts, t_close


# ---------------------------------------------------------------- chính
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--scenes", required=True)
    ap.add_argument("--out")
    ap.add_argument("--variant", required=True, help="file JSON biến thể (Studio truyền vào)")
    ap.add_argument("--model", default="medium")
    ap.add_argument("--board", help="ảnh bảng có sẵn (PNG nền trong suốt); không có thì gen bằng AI và lưu board.png cạnh raw.mp4")
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.raw)[0] + "_final.mp4"
    v = json.load(open(a.variant, encoding="utf-8"))
    v = v[0] if isinstance(v, list) else v
    scenes = json.load(open(a.scenes, encoding="utf-8"))
    pairs, closing = parse_bang(v.get("BANG_TU", ""))
    turns = v.get("LUOT", [])
    print(f"Biến thể \"{v.get('name', '')}\": {len(pairs)} cặp câu" + (f", câu kết \"{closing}\"" if closing else ""))
    run_dir = os.path.dirname(os.path.abspath(a.raw))
    try:
        if a.board:
            board, inner = Image.open(a.board).convert("RGBA"), find_inner(Image.open(a.board).convert("RGBA"))
        else:
            board, inner = make_board(v.get("CO", ""), os.path.join(run_dir, "board.png"))
    except Exception as ex:  # noqa: BLE001 - không gen được bảng vẫn ra video với bảng vẽ bằng code
        print(f"Không gen được khung bảng ({str(ex)[:120]}); dùng bảng vẽ bằng code")
        board, inner = fallback_board()
    # đặt bảng: rộng ~86% khung, đỉnh ~4.5%, đáy không quá ~35% (đầu robot ở ~36%)
    scale = min(W * 0.86 / board.width, H * 0.31 / board.height)
    place = (int((W - board.width * scale) / 2), int(H * 0.045), scale)
    starts, t_close = timeline(a.raw, scenes, turns, pairs, closing, a.model, lang_code(v.get("NGON_NGU_ME", "")))
    end = max(s["end"] for s in scenes)
    work = tempfile.mkdtemp(prefix="tutor_pp_")
    try:
        cards = []
        for i, pair in enumerate(pairs):
            s = 0.0 if i == 0 else max(0.0, starts[i] - 0.15)
            e = (starts[i + 1] - 0.15) if i + 1 < len(pairs) else ((t_close - 0.15) if t_close else end)
            cards.append((s, e, render_card(board, inner, place, pair)))
            print(f"  bảng {i + 1}: {s:6.2f}-{e:6.2f}  {pair[0]} / {pair[1]} / {pair[2]}")
        if closing and t_close:
            cards.append((t_close - 0.15, end, render_card(board, inner, place, None, closing)))
            print(f"  câu kết: {t_close - 0.15:6.2f}-{end:6.2f}  {closing}")
        fr = os.path.join(work, "f0.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.3", "-i", a.raw, "-vf", f"scale={W}:{H}", "-frames:v", "1", fr])
        avatar = None
        if os.path.exists(fr):   # ảnh robot cho nhãn: vùng mặt (giữa khung, ngay dưới bảng)
            f0 = Image.open(fr).convert("RGB")
            c = int(W * 0.13)
            avatar = f0.crop((W // 2 - c, int(H * 0.36), W // 2 + c, int(H * 0.36) + 2 * c))
        cmd = ["ffmpeg", "-y", "-i", a.raw]
        fc = f"[0:v]scale={W}:{H}:flags=lanczos,fps=30[v0]"
        last = "v0"
        for k, (s, e, im) in enumerate(cards):
            pth = os.path.join(work, f"card{k}.png")
            im.save(pth)
            cmd += ["-i", pth]
            fc += f";[{last}][{k + 1}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[c{k}]"
            last = f"c{k}"
        if v.get("NHAN"):
            pth = os.path.join(work, "label.png")
            render_label(v["NHAN"], avatar).save(pth)
            cmd += ["-i", pth]
            fc += f";[{last}][{len(cards) + 1}:v]overlay=0:0[lb]"
            last = "lb"
        cmd += ["-filter_complex", fc, "-map", f"[{last}]", "-map", "0:a", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", out]
        P.run(cmd)
        print("XONG ->", out, f"({P.duration(out):.1f}s)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
