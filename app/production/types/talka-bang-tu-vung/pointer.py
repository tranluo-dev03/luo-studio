"""Chữ tiếng Anh + cây bút đỏ chỉ chữ, ghép ở hậu kỳ (như video gốc). Video Muse chỉ có robot nói trước bảng chữ cố định (vạch xám trống).
Như video gốc: bút luôn nằm trên giấy và lướt qua đúng chữ robot đang đọc (từ Tây Ban Nha, chữ tiếng Anh, chữ tiếng Anh lần đọc lại).
Mốc thời gian: Whisper theo từng cảnh. Toạ độ: đo trên khung hình (vòng tròn đỏ = hàng, chữ đen = từ Tây Ban Nha, chữ xanh = từ tiếng Anh)."""
import json, os, re, subprocess, unicodedata

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
NOWIN = 0x08000000 if os.name == "nt" else 0


def fold(s):
    return re.sub(r"[^a-z0-9 ]", "", unicodedata.normalize("NFKD", str(s).lower()).encode("ascii", "ignore").decode()).strip()


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", path],
                         capture_output=True, text=True).stdout
    st = json.loads(out)["streams"][0]
    n, d = st["r_frame_rate"].split("/")
    return int(st["width"]), int(st["height"]), float(n) / float(d)


def frames(path, w, h, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + ["-i", path] + (["-t", f"{t:.3f}"] if t else []) + \
          ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=NOWIN)   # dừng đọc sớm làm ffmpeg báo "Broken pipe": vô hại
    n = w * h * 3
    try:
        while True:
            buf = p.stdout.read(n)
            if len(buf) < n:
                break
            yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    finally:
        p.stdout.close()
        p.wait()


def frame_at(path, t, w, h):
    return next(frames(path, w, h, ss=t, t=0.2), None)


# ---------------------------------------------------------------- đo bố cục tờ giấy
def blue_mask(f):
    f = f.astype(np.int16)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    return (b > 110) & (b > r + 45) & (b > g + 20)


def rows_of(f):
    """[(y tâm hàng, x phải vòng tròn đỏ, chiều cao vòng tròn)] từ trên xuống, dò theo các vòng tròn đỏ có dấu tick ở mép trái tờ giấy."""
    h, w = f.shape[:2]
    a = f.astype(np.int16)
    red = (a[..., 0] > 160) & (a[..., 1] < 95) & (a[..., 2] < 95)
    red[:, int(w * 0.35):] = False
    ys = np.nonzero(red.sum(1) > 3)[0]
    groups = []
    for y in ys:
        if groups and y - groups[-1][-1] <= 3:
            groups[-1].append(y)
        else:
            groups.append([y])
    out = []
    for g in groups:
        if len(g) < h * 0.008:
            continue
        band = red[g[0]:g[-1] + 1]
        xs = np.nonzero(band.any(0))[0]
        out.append((int(np.mean(g)), int(xs.max()), len(g)))
    return out


def word_box(mask, y0, y1, x0, x1, gap=16):
    """Hộp của MỘT cụm chữ đầu tiên từ x0 sang phải: chỉ tính cột có nét đủ dày (bỏ chấm lưới giấy) và dừng ở khoảng trống > `gap` px sau chữ."""
    sub = mask[y0:y1, x0:x1]
    cols = sub.sum(0) >= 3
    xs = np.nonzero(cols)[0]
    if len(xs) < 5:
        return None
    start, end = xs[0], xs[0]
    for x in xs[1:]:
        if x - end > gap:
            break
        end = x
    ys = np.nonzero(sub[:, start:end + 1].any(1))[0]
    return (x0 + int(start), y0 + int(ys.min()), x0 + int(end), y0 + int(ys.max()))


# ---------------------------------------------------------------- mốc lời nói
def find(words, phrase, after=-1.0, last=False):
    toks = fold(phrase).split()
    ws = [(fold(w), a, b) for w, a, b in words]
    hits = [(ws[i][1], ws[i + len(toks) - 1][2]) for i in range(len(ws) - len(toks) + 1)
            if ws[i][1] > after and all(ws[i + k][0] == toks[k] for k in range(len(toks)))]
    if not hits:
        hits = [(a, b) for w, a, b in ws if a > after and w == toks[0]]
    return (hits[-1] if last else hits[0]) if hits else None


def _all(words, phrase):
    """Mọi lần xuất hiện (bắt đầu, kết thúc) của cụm `phrase`."""
    toks = fold(phrase).split()
    ws = [(fold(w), a, b) for w, a, b in words]
    return [(ws[i][1], ws[i + len(toks) - 1][2]) for i in range(len(ws) - len(toks) + 1) if all(ws[i + k][0] == toks[k] for k in range(len(toks)))]


# ---------------------------------------------------------------- dựng đường đi của bút (theo video gốc)
# Video gốc: bút LUÔN nằm trên giấy, đi theo LỜI NÓI chứ không theo nét viết:
#   đầu cảnh bút nằm sẵn ở đầu từ Tây Ban Nha -> robot đọc từ đó: bút lướt từ đầu đến cuối từ -> trượt sang chỗ chữ tiếng Anh ->
#   robot nói từ tiếng Anh: bút lướt qua chữ tiếng Anh -> "Repite conmigo": lùi về đầu chữ -> robot đọc lại: lướt qua lần nữa ->
#   sang cảnh sau: trượt thẳng xuống đầu từ Tây Ban Nha của hàng kế tiếp. Không nhấc bút, không bay ra vào giữa các cảnh.
def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _smooth(v, sigma):
    """Làm mượt chuỗi số theo thời gian (lọc Gauss), giữ hai đầu."""
    if sigma <= 0 or len(v) < 3:
        return v
    r = int(sigma * 3)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    pad = np.concatenate([np.full(r, v[0]), v, np.full(r, v[-1])])
    return np.convolve(pad, k, mode="valid")


def _scene_layout(raw, sc, item, size, log):
    """Đo trên khung cuối cảnh: hộp từ Tây Ban Nha và vị trí đặt chữ tiếng Anh (đầu vạch xám, đường chân chữ). Video Muse không có chữ tiếng Anh."""
    w, h = size
    row = item["row"]
    end_f = frame_at(raw, max(sc["start"], sc["end"] - 0.25), w, h)
    if end_f is None:
        return None
    rows = rows_of(end_f)
    if len(rows) < row and len(rows) >= 2:   # Muse không vẽ đủ vòng tròn đỏ: các hàng cách đều nhau nên suy ra từ hàng 1 và 2
        step = rows[1][0] - rows[0][0]
        rows = rows + [(rows[0][0] + k * step, rows[0][1], rows[0][2]) for k in range(len(rows), row)]
    if len(rows) < row:
        log(f"  bút: cảnh lượt {sc['turn'] + 1}: chỉ thấy {len(rows)} hàng trên giấy, bỏ qua")
        return None
    cy, cx_red, ch = rows[row - 1]
    gap = (rows[1][0] - rows[0][0]) if len(rows) > 1 else int(h * 0.05)
    y0, y1 = int(cy - gap * 0.45), int(cy + gap * 0.45)
    dark = end_f.max(2) < 95
    es_box = word_box(dark, y0, y1, cx_red + 4, int(w * 0.52)) or (cx_red + 8, int(cy - ch * 0.5), int(w * 0.4), int(cy + ch * 0.5))
    base = es_box[3]                                    # chân chữ của hàng (từ Tây Ban Nha không có nét thòng)
    # đầu vạch xám bên phải từ Tây Ban Nha = chỗ đặt chữ tiếng Anh
    g = end_f[max(0, base - 4):base + 12, :, :].astype(int)
    lum, spread = g.mean(2), g.max(2) - g.min(2)
    paper = float(np.median(end_f[y0:y1, int(w * 0.6):int(w * 0.9)].mean(2)))
    line = ((lum < paper - 15) & (spread < 30)).any(0)
    slot = None
    x = es_box[2] + 8
    while x < int(w * 0.95):
        if line[x] and line[x:x + 40].mean() > 0.8:
            slot = x
            break
        x += 1
    slot = (slot or es_box[2] + int(w * 0.06)) + 6
    # độ cao của vạch xám: chữ tiếng Anh "ngồi" trên vạch, vạch không cắt ngang thân chữ
    yy0 = max(0, base - 16)
    gg = end_f[yy0:base + 16, slot:slot + 140, :].astype(int)
    on = ((gg.mean(2) < paper - 15) & ((gg.max(2) - gg.min(2)) < 30)).sum(1)
    line_y = yy0 + int(np.argmax(on)) if on.size and on.max() > 40 else base
    return es_box, slot, line_y - 2


_FONTS = [r"C:\Windows\Fonts\segoeuii.ttf", r"C:\Windows\Fonts\calibrii.ttf", r"C:\Windows\Fonts\ariali.ttf"]


def word_image(text, cap_h, color=(38, 66, 190)):
    """Chữ tiếng Anh xanh nghiêng như video gốc (RGBA), cỡ theo chiều cao chữ Tây Ban Nha. Trả về (ảnh, độ lệch chân chữ tính từ đỉnh ảnh)."""
    from PIL import ImageDraw, ImageFilter, ImageFont
    path = next((f for f in _FONTS if os.path.exists(f)), None)
    font = ImageFont.truetype(path, max(12, int(cap_h * 1.32))) if path else ImageFont.load_default()
    asc, desc = font.getmetrics()
    tw = int(font.getlength(text)) + 8
    im = Image.new("RGBA", (tw, asc + desc + 6), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2, 2), text, font=font, fill=color + (255,), stroke_width=max(1, int(cap_h / 30)), stroke_fill=color + (255,))   # nét đậm vừa, gần độ dày chữ Tây Ban Nha
    a = im.getchannel("A").filter(ImageFilter.GaussianBlur(0.5)).point(lambda v: int(v * 0.93))   # ăn nhẹ vào giấy, không sắc lẹm
    im.putalpha(a)
    return im, asc + 2


def scene_keys(sc, item, words, es_box, en_box, base, log=print):
    """Các mốc (giây, x, y, kiểu) của bút trong một cảnh và lúc chữ tiếng Anh hiện ra. kiểu 'sweep' = lướt đều qua chữ, 'glide' = trượt êm sang chỗ khác."""
    es, en = item["es"], item["en"]
    y = base + 3
    ES_L, ES_R = (es_box[0] + 3, y), (es_box[2] - 2, y)
    EN_L, EN_R = (en_box[0] + 3, y), (en_box[2] - 2, y)
    t_es = find(words, es)
    # mốc "Repite conmigo" chia lời thành: lần nói chính (chữ tiếng Anh NGAY TRƯỚC "Repite") và lần đọc lại (sau "conmigo").
    # Muse đôi khi nói lẫn từ tiếng Anh vào câu hỏi ("¿Cómo se dice for you…?"), nên không lấy lần xuất hiện đầu tiên.
    rp = find(words, "repite", after=(t_es[1] if t_es else sc["start"]))
    cm = find(words, "conmigo", after=(rp[0] if rp else sc["start"])) or find(words, "migo", after=(rp[0] if rp else sc["start"]))
    if rp:
        before = [m for m in _all(words, en) if m[0] < rp[0] and (not t_es or m[0] > t_es[0])]
        t_en = before[-1] if before else None
    else:
        t_en = find(words, en, after=(t_es[1] if t_es else sc["start"]))
    t_rep = find(words, en, after=(cm[1] - 0.05 if cm else (t_en[1] + 0.3 if t_en else sc["start"])), last=True)
    if not t_rep and cm:   # Whisper không nghe ra lần đọc lại: robot đọc lại ngay sau "conmigo"
        t_rep = (cm[1] + 0.15, cm[1] + 0.8)
    s = sc["start"]
    e0, e1 = t_es if t_es else (s + 0.6, s + 1.1)
    e1 = max(e1, e0 + 0.45)                               # lướt từ Tây Ban Nha trong lúc đọc (tối thiểu 0,45 giây)
    n0, n1 = t_en if t_en else (e1 + 1.0, e1 + 1.6)
    n0 = max(n0, e1 + 0.35)
    n1 = max(n1, n0 + 0.6)
    r0, r1 = t_rep if t_rep else (n1 + 1.2, n1 + 1.8)
    r0 = max(r0, n1 + 0.45)
    r1 = min(max(r1, r0 + 0.5), sc["end"] - 0.05)
    keys = [(min(s + 0.35, e0), *ES_L, "glide"),                     # đầu cảnh: trượt về đầu từ Tây Ban Nha
            (e0, *ES_L, "hold"),
            (e1, *ES_R, "sweep"),                                    # đọc từ Tây Ban Nha: lướt qua từ
            (max(e1 + 0.05, n0 - 0.45), *ES_R, "hold"),
            (n0, *EN_L, "glide"),                                    # bút đặt vào đầu chữ tiếng Anh -> chữ hiện ra nguyên chữ
            (n1, *EN_R, "sweep"),                                    # nói từ tiếng Anh: lướt qua chữ
            (max(n1 + 0.05, r0 - 0.5), *EN_R, "hold"),
            (r0, *EN_L, "glide"),                                    # "Repite conmigo": lùi về đầu chữ
            (r1, *EN_R, "sweep")]                                    # đọc lại: lướt qua lần nữa
    keys = [k for i, k in enumerate(keys) if i == 0 or k[0] > keys[i - 1][0] + 1e-3]
    log(f"  bút cảnh lượt {sc['turn'] + 1}: lướt \"{es}\" {e0:.1f}-{e1:.1f}s, chữ \"{en}\" hiện + lướt {n0:.1f}-{n1:.1f}s"
        + (f", lướt lại {r0:.1f}-{r1:.1f}s" if t_rep else " (không nghe lần đọc lại: lướt lại sau khi đọc)"))
    return keys, n0


def path_frames(keys, n_frames, fps, off, t_in, t_out):
    """Vị trí ngòi bút cho mọi khung: vào khung trước mốc đầu, đi qua các mốc, ở yên giữa các cảnh, rút ra sau mốc cuối."""
    xs, ys = np.full(n_frames, off[0], float), np.full(n_frames, off[1], float)
    pts = [(t_in, off[0], off[1], "hold")] + keys + [(t_out, off[0], off[1], "glide")]
    j = 0
    for i in range(n_frames):
        t = i / fps
        if t < pts[0][0] or t >= pts[-1][0]:
            continue
        while j + 1 < len(pts) and pts[j + 1][0] <= t:
            j += 1
        a, b = pts[j], pts[min(j + 1, len(pts) - 1)]
        u = (t - a[0]) / max(1e-3, b[0] - a[0])
        u = u if b[3] == "sweep" else _ease(u) if b[3] == "glide" else 0.0
        if b[3] == "hold":
            xs[i], ys[i] = a[1], a[2]
        else:
            xs[i], ys[i] = a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
    sig = fps * 0.04
    return _smooth(xs, sig), _smooth(ys, sig)


def render(raw, out, xs, ys, labels, size, fps, scale=0.28):
    """Ghép chữ tiếng Anh (labels = [(giây hiện, giây tắt, ảnh, (x, y))]) và bút đỏ (vị trí ngòi xs, ys) lên raw. Tiếng giữ nguyên."""
    w, h = size
    base = Image.open(os.path.join(HERE, "assets", "marker.png")).convert("RGBA")
    meta = json.load(open(os.path.join(HERE, "assets", "marker.json"), encoding="utf-8"))
    s = scale * h / 1280
    mk = base.resize((int(base.width * s), int(base.height * s)), Image.LANCZOS)
    sh = Image.new("RGBA", mk.size, (0, 0, 0, 0))
    sh.putalpha(mk.getchannel("A").point(lambda v: int(v * 0.3)))
    tip = (meta["tip"][0] * s, meta["tip"][1] * s)
    tmp = out + ".v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", f"{fps:.3f}", "-i", "-",
                            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE, creationflags=NOWIN)
    for i, f in enumerate(frames(raw, w, h)):
        t = i / fps
        show = [lb for lb in labels if lb[0] <= t < lb[1]]
        pen = i < len(xs) and xs[i] < w + 20
        if show or pen:
            im = Image.fromarray(f).convert("RGBA")
            for _, _, img, pos in show:
                im.alpha_composite(img, pos)
            if pen:
                x, y = int(round(xs[i] - tip[0])), int(round(ys[i] - tip[1]))
                im.paste(sh, (x + 10, y + 16), sh)
                im.paste(mk, (x, y), mk)
            f = np.asarray(im.convert("RGB"))
        enc.stdin.write(np.ascontiguousarray(f).tobytes())
    enc.stdin.close()
    enc.wait()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", raw, "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "copy", "-shortest", out], check=True)
    os.remove(tmp)


def add_pointer(raw, scenes, items, out, transcribe, model="medium", log=print):
    """items = [{turn, es, en, row}]; transcribe(raw, model, jobs) -> list từ theo từng đoạn (giờ tuyệt đối). Trả về đường dẫn video đã ghép, hoặc raw nếu không làm được.
    Video Muse chỉ có robot nói trước bảng chữ cố định (vạch xám trống). Hậu kỳ ghép: chữ tiếng Anh hiện ra nguyên chữ khi bút đặt vào đầu chữ và giữ đến hết
    phần bảng chữ; bút đỏ nằm trên giấy, lướt qua đúng chữ robot đang đọc, trượt sang chữ/hàng tiếp theo."""
    w, h, fps = probe(raw)
    by_turn = {s["turn"]: s for s in scenes}
    todo = sorted([(it, by_turn[it["turn"]]) for it in items if it["turn"] in by_turn], key=lambda x: x[1]["start"])
    if not todo:
        return raw
    jobs = [{"a": max(0.0, sc["start"] - 0.1), "b": sc["end"] + 0.1, "prompt": f'{it["es"]} {it["en"]} repite conmigo', "lang": "es"} for it, sc in todo]
    res = transcribe(raw, model, jobs) or [[] for _ in todo]
    board_end = todo[-1][1]["end"]                      # chữ đã hiện giữ đến hết cảnh bảng chữ cuối
    keys, labels = [], []
    lays = [_scene_layout(raw, sc, it, (w, h), log) for it, sc in todo]
    caps = sorted(l[0][3] - l[0][1] for l in lays if l)
    cap = caps[len(caps) // 2] if caps else 30          # một cỡ chữ chung cho mọi hàng ("¡Gracias!" có dấu ¡ ! nên cao hơn, không lấy riêng)
    for (it, sc), words, lay in zip(todo, res, lays):
        if not lay:
            continue
        es_box, slot, base = lay
        text = it.get("text") or it["en"][:1].upper() + it["en"][1:]
        img, asc = word_image(text, cap)
        pos = (int(slot), int(base - asc))
        en_box = (pos[0], pos[1], pos[0] + img.width - 6, base)
        k, t_on = scene_keys(sc, it, words, es_box, en_box, base, log)
        keys += k
        labels.append((t_on, board_end, img, pos))
    if not keys:
        return raw
    total = int(round(max(s["end"] for s in scenes) * fps)) + 2
    off = (w + 80, h * 0.95)
    xs, ys = path_frames(keys, total, fps, off, max(0.0, todo[0][1]["start"] - 0.01), min(board_end, keys[-1][0] + 0.7))
    render(raw, out, xs, ys, labels, (w, h), fps)
    return out
