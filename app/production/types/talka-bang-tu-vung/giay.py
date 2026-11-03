"""Dựng tờ giấy bảng từ vựng bằng code (ảnh tĩnh) cho hậu kỳ: video Muse chỉ có robot trên nền xanh, hậu kỳ ghép robot lên tờ giấy này.
Vì giấy do code vẽ nên biết CHÍNH XÁC toạ độ từng từ: không phải dò từ ảnh, chữ luôn đúng chính tả, bút và chữ tiếng Anh luôn nằm đúng hàng.

spec (khai trong biến thể: "HAU_KY": {"bang": spec}):
  kieu      checklist | hai-cot | hai-cot-icon-trai | so-tay
  tieu_de   tiêu đề trên cùng
  dau_trai  tên cột trái (chỉ giấy hai cột), vd. "Español" / "Português"
  hang      [{"tu": từ bản ngữ, "icon": ký tự icon (Segoe UI Symbol), tuỳ chọn}] (đúng 8 hàng; 5 hàng đầu là 5 từ vựng)
render(spec, size, top) -> (ảnh RGB, [{"es_box", "slot", "base"} cho từng hàng], kiểu chữ tiếng Anh {"color", "fonts"})."""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

_F = r"C:\Windows\Fonts" if os.name == "nt" else "/usr/share/fonts/truetype/dejavu"


def _font(names, size):
    for n in names:
        p = os.path.join(_F, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, max(8, int(size)))
    return ImageFont.load_default()


HAND = ["Inkfree.ttf", "segoesc.ttf", "DejaVuSans.ttf"]
SERIF = ["georgia.ttf", "times.ttf", "DejaVuSerif.ttf"]
SERIF_B = ["georgiab.ttf", "timesbd.ttf", "DejaVuSerif-Bold.ttf"]
SANS_B = ["arialbd.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"]
SYMBOL = ["seguisym.ttf", "DejaVuSans.ttf"]

# Hàng 1 nằm ở Y1 (tỉ lệ chiều cao); bước hàng STEP được TÍNH để hàng 5 vừa kịp nằm trên đỉnh đầu robot (`top`, đo từ video), các hàng sau nối tiếp xuống hết tờ giấy
Y1S = {"checklist": 0.125, "hai-cot": 0.155, "hai-cot-icon-trai": 0.155, "so-tay": 0.195}
MARGIN, STEP_MIN, STEP_MAX = 0.04, 0.04, 0.095


def geometry(kieu, top):
    """(y hàng 1, bước hàng) theo đỉnh đầu robot `top` (0..1 chiều cao)."""
    y1 = Y1S[kieu]
    step = min(STEP_MAX, max(STEP_MIN, (top - MARGIN - y1) / 4))
    return y1, step
# chữ tiếng Anh: màu + bộ font (pointer.word_image)
EN_STYLE = {
    "checklist": {"color": (38, 66, 190), "fonts": ["segoeuii.ttf", "calibrii.ttf", "ariali.ttf"]},
    "hai-cot": {"color": (196, 52, 56), "fonts": HAND},
    "hai-cot-icon-trai": {"color": (196, 52, 56), "fonts": HAND},
    "so-tay": {"color": (146, 30, 42), "fonts": ["georgiai.ttf", "timesi.ttf"]},
}


def _shadow(im, box, blur, off, alpha):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((box[0] + off, box[1] + off * 1.4, box[2] + off, box[3] + off * 1.4), fill=(0, 0, 0, alpha))
    im.paste(Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(blur))).convert("RGB"))


def _fit(names, size, text, maxw):
    """Font cỡ `size`, thu nhỏ dần nếu `text` rộng hơn `maxw` (từ dài như "Prazer em conhecer você" không được lấn sang cột tiếng Anh)."""
    f = _font(names, size)
    while f.size > 24 and f.getlength(text) > maxw:
        f = _font(names, f.size * 0.94)
    return f


def _fit_all(names, size, items):
    """MỘT font chung cho mọi hàng: cỡ `size`, thu nhỏ dần cho tới khi từ nào cũng vừa bề rộng của nó. items = [(chữ, bề rộng tối đa)]."""
    f = _font(names, size)
    while f.size > 24 and any(f.getlength(t) > mw for t, mw in items):
        f = _font(names, f.size * 0.94)
    return f


def _ink(d, xy, text, font, fill, anchor="ls"):
    d.text(xy, text, font=font, fill=fill, anchor=anchor)
    return d.textbbox(xy, text, font=font, anchor=anchor)


def _word(d, x, base, text, font, fill):
    """Vẽ từ tại (x, đường chân chữ); trả về hộp chữ với đáy = đường chân chữ (bỏ nét thòng)."""
    l, t, r, _ = _ink(d, (x, base), text, font, fill)
    return (l, t, r, base)


def _icon(d, x, base, ch, size, fill):
    if ch:
        d.text((x, base), ch, font=_font(SYMBOL, size), fill=fill, anchor="ls")


def _checklist(w, h, spec, y1, step):
    im = Image.new("RGB", (w, h), (224, 222, 216))
    box = (int(w * 0.04), int(h * 0.02), int(w * 0.96), int(h * 0.975))
    _shadow(im, box, w * 0.012, w * 0.006, 110)
    d = ImageDraw.Draw(im)
    d.rectangle(box, fill=(248, 243, 228))
    r = max(1, int(w * 0.0016))
    for gy in range(box[1] + int(h * 0.012), box[3], int(w * 0.03)):
        for gx in range(box[0] + int(w * 0.012), box[2], int(w * 0.03)):
            d.ellipse((gx - r, gy - r, gx + r, gy + r), fill=(206, 199, 182))
    _ink(d, (w // 2, int(h * 0.075)), spec.get("tieu_de", ""), _font(SERIF_B, h * 0.05), (20, 20, 20), "ms")
    sc = min(1.12, max(1.0, step / 0.05))   # bước hàng lớn hơn thì chữ và vòng tròn to lên theo
    geo = []
    fw = _fit_all(SANS_B, h * 0.029 * sc, [(r["tu"], w * 0.39) for r in spec["hang"]])
    for k, row in enumerate(spec["hang"]):
        yc = (y1 + step * k) * h
        base = int(yc + h * 0.010 * sc)
        b, rc = int(w * 0.07), int(h * 0.0155 * sc)
        d.ellipse((b - w * 0.009, yc - w * 0.009, b + w * 0.009, yc + w * 0.009), fill=(40, 38, 36))
        cx = int(w * 0.135)
        d.ellipse((cx - rc, yc - rc, cx + rc, yc + rc), fill=(206, 36, 44))
        d.line((cx - rc * 0.5, yc, cx - rc * 0.1, yc + rc * 0.45, cx + rc * 0.55, yc - rc * 0.45), fill=(255, 255, 255), width=max(3, int(h * 0.0033)), joint="curve")
        box_es = _word(d, int(w * 0.19), base, row["tu"], fw, (28, 28, 30))
        sx0, sx1 = int(w * 0.60), int(w * 0.94)
        d.line((sx0, base + 5, sx1, base + 5), fill=(168, 168, 168), width=max(2, int(h * 0.0016)))
        geo.append({"es_box": box_es, "slot": sx0 + 6, "base": base + 3, "right": sx1})
    return im, geo


def _lined(w, h, spec, icon_left, y1, step):
    im = Image.new("RGB", (w, h), (252, 252, 250))
    d = ImageDraw.Draw(im)
    sc = min(1.25, max(1.0, step / 0.048))
    n = int((0.99 - y1) / step) + 3
    for j in range(-3, n):
        y = int((y1 + step * j) * h)
        if 0.06 * h < y < h * 0.99:
            d.line((0, y, w, y), fill=(178, 198, 228), width=max(2, int(h * 0.0016)))
    dv = int(w * 0.53)
    d.line((dv, int(h * 0.095), dv, h), fill=(54, 58, 72), width=max(3, int(w * 0.003)))
    _ink(d, (w // 2, int(max(0.05, y1 - step - 0.045) * h)), spec.get("tieu_de", ""), _font(HAND, h * 0.04), (36, 40, 54), "ms")
    hy = int((y1 - step) * h) - 6
    fh = _font(HAND, h * 0.031 * sc)
    lb = _ink(d, (int(w * 0.27), hy), spec.get("dau_trai", ""), fh, (36, 40, 54), "ms")
    d.line((lb[0], hy + 8, lb[2], hy + 8), fill=(54, 58, 72), width=max(3, int(h * 0.002)))
    rb = _ink(d, (int(w * 0.77), hy), spec.get("dau_phai", "English"), fh, (36, 40, 54), "ms")
    d.line((rb[0], hy + 8, rb[2], hy + 8), fill=(206, 56, 60), width=max(3, int(h * 0.002)))
    geo = []
    fw = _fit_all(HAND, h * 0.031 * sc, [(r["tu"], w * (0.31 if icon_left else 0.46) - (0 if icon_left or not r.get("icon") else h * 0.034 + 10)) for r in spec["hang"]])
    for k, row in enumerate(spec["hang"]):
        base = int((y1 + step * k) * h) - 6
        ic = row.get("icon", "")
        if icon_left:
            _icon(d, int(w * 0.045), base, ic, h * 0.034 * sc, (30, 34, 46))
            box_es = _word(d, int(w * 0.19), base, row["tu"], fw, (36, 40, 54))
        else:
            box_es = _word(d, int(w * 0.04), base, row["tu"], fw, (36, 40, 54))
            _icon(d, box_es[2] + int(w * 0.03), base, ic, h * 0.034 * sc, (30, 34, 46))
        geo.append({"es_box": box_es, "slot": int(w * 0.57) + 6, "base": base - 2, "right": int(w * 0.97)})
    return im, geo


def _notepad(w, h, spec, y1, step):
    im = Image.new("RGB", (w, h), (206, 205, 200))
    box = (int(w * 0.05), int(h * 0.045), int(w * 0.95), int(h * 0.975))
    _shadow(im, box, w * 0.014, w * 0.008, 120)
    d = ImageDraw.Draw(im)
    d.rectangle(box, fill=(251, 247, 236))
    for i in range(7):   # lò xo
        x = int(w * (0.14 + 0.12 * i))
        d.rounded_rectangle((x - w * 0.012, h * 0.022, x + w * 0.012, h * 0.075), radius=w * 0.012, fill=(24, 24, 28))
        d.rounded_rectangle((x - w * 0.004, h * 0.026, x - w * 0.001, h * 0.068), radius=2, fill=(110, 110, 118))
    _ink(d, (w // 2, int(h * 0.12)), spec.get("tieu_de", ""), _font(SERIF_B, h * 0.04), (22, 22, 24), "ms")
    d.line((int(w * 0.2), int(h * 0.128), int(w * 0.8), int(h * 0.128)), fill=(40, 40, 44), width=max(2, int(h * 0.0016)))
    sc = min(1.25, max(1.0, step / 0.048))
    for j in range(int((0.96 - y1) / step) + 1):   # vạch kẻ chạy hết tờ giấy
        y = int((y1 + step * j) * h)
        d.line((int(w * 0.1), y, int(w * 0.9), y), fill=(186, 184, 176), width=max(2, int(h * 0.0016)))
    geo = []
    fw = _fit_all(SERIF, h * 0.032 * sc, [(r["tu"], w * 0.45 - (h * 0.034 if r.get("icon") else 0)) for r in spec["hang"]])
    for k, row in enumerate(spec["hang"]):
        base = int((y1 + step * k) * h) - 6
        box_es = _word(d, int(w * 0.12), base, row["tu"], fw, (28, 28, 32))
        _icon(d, box_es[2] + int(w * 0.03), base, row.get("icon", ""), h * 0.034 * sc, (30, 30, 36))
        geo.append({"es_box": box_es, "slot": int(w * 0.60) + 6, "base": base - 2, "right": int(w * 0.9)})
    return im, geo


def render(spec, size, top=0.40):
    """top = đỉnh đầu robot (tỉ lệ chiều cao, đo từ video): 5 hàng đầu được dãn vừa kịp nằm trên đầu robot."""
    w, h = size
    kieu = spec.get("kieu") or "checklist"
    if kieu not in Y1S:
        raise ValueError(f"kiểu giấy lạ: {kieu}")
    y1, step = geometry(kieu, top)
    if kieu == "checklist":
        im, geo = _checklist(w, h, spec, y1, step)
    elif kieu in ("hai-cot", "hai-cot-icon-trai"):
        im, geo = _lined(w, h, spec, kieu == "hai-cot-icon-trai", y1, step)
    else:
        im, geo = _notepad(w, h, spec, y1, step)
    return im, geo, EN_STYLE[kieu]
