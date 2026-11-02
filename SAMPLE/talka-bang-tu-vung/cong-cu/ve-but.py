"""Vẽ các cây bút cho hậu kỳ Talka (kiểu bút khai trong biến thể: "HAU_KY": {"but": "fountain" | "ballpoint"}).
Chạy bằng Python của dự án (cần Pillow, numpy): .venv\\Scripts\\python.exe SAMPLE\\talka-bang-tu-vung\\cong-cu\\ve-but.py
Ghi assets/marker-<kiểu>.png (RGBA, ngòi ở góc trái trên, thân chạy xuống phải như marker.png) và marker-<kiểu>.json (toạ độ ngòi)."""
import json
import math
import os

import numpy as np
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                   "app", "production", "types", "talka-bang-tu-vung", "assets")
ANGLE = 58          # độ nghiêng của trục bút so với phương ngang (marker.png ~ 61)
SS = 2              # vẽ gấp đôi rồi thu nhỏ cho mép mịn


def _seg(x0, x1, hw0, hw1, color, gloss=0.35, metal=False):
    return dict(x0=x0, x1=x1, hw0=hw0, hw1=hw1, color=np.array(color, float), gloss=gloss, metal=metal)


def render(segs, length, height):
    """Trục bút nằm ngang, ngòi ở x=0. Mỗi đoạn là hình trụ có bóng đổ + vệt sáng (hw = nửa bề rộng thay đổi dọc đoạn để tạo hình nón / phối cảnh)."""
    L, H = length * SS, height * SS
    yc = H / 2
    img = np.zeros((H, L, 4), float)
    ys = np.arange(H)[:, None]
    for s in segs:
        x0, x1 = int(s["x0"] * SS), int(s["x1"] * SS)
        xs = np.arange(x0, x1)[None, :]
        t = (xs - x0) / max(1, x1 - x0)
        hw = (s["hw0"] + (s["hw1"] - s["hw0"]) * t) * SS
        v = (ys - yc) / np.maximum(hw, 1e-3)
        inside = (np.abs(v) <= 1)
        edge = np.clip((1 - np.abs(v)) * hw / 1.5, 0, 1)   # mép mềm ~1,5 px
        shade = 0.55 + 0.45 * np.sqrt(np.clip(1 - v * v, 0, 1))
        spec = np.exp(-((v + 0.38) / 0.16) ** 2) * s["gloss"]
        if s["metal"]:
            spec = spec + 0.25 * np.exp(-((v - 0.45) / 0.12) ** 2)
        col = s["color"][None, None, :] * shade[..., None]
        col = col + (255 - col) * spec[..., None]
        a = np.where(inside, edge, 0.0)
        sl = np.s_[:, x0:x1]
        cur = img[sl]
        img[sl] = np.where(a[..., None] > 0, np.concatenate([np.clip(col, 0, 255), (a * 255)[..., None]], axis=2), cur)
    return Image.fromarray(img.astype(np.uint8), "RGBA")


def pens():
    steel = (150, 152, 160)
    return {
        # bút máy: ngòi kim loại sẫm, cổ bút xanh đen, vòng vàng, thân màu da bò (như ref)
        "fountain": render([
            _seg(0, 300, 2, 66, (58, 58, 70), gloss=0.5, metal=True),
            _seg(300, 330, 66, 76, (190, 160, 90), gloss=0.5, metal=True),
            _seg(330, 560, 76, 96, (34, 36, 66), gloss=0.45),
            _seg(560, 600, 98, 100, (214, 178, 96), gloss=0.55, metal=True),
            _seg(600, 1780, 104, 138, (224, 180, 112), gloss=0.35),
            _seg(1780, 1830, 138, 139, (214, 178, 96), gloss=0.5, metal=True),
        ], 1830, 300),
        # bút bi đỏ: đầu bạc, mũi đen, thân đỏ bóng có vòng bạc (như ref)
        "ballpoint": render([
            _seg(0, 70, 2, 20, steel, gloss=0.5, metal=True),
            _seg(70, 190, 20, 62, (30, 30, 34), gloss=0.3),
            _seg(190, 240, 64, 66, steel, gloss=0.5, metal=True),
            _seg(240, 1120, 70, 100, (206, 24, 36), gloss=0.5),
            _seg(1120, 1170, 102, 104, steel, gloss=0.55, metal=True),
            _seg(1170, 1800, 104, 124, (206, 24, 36), gloss=0.5),
            _seg(1800, 1850, 124, 120, (170, 18, 28), gloss=0.35),
        ], 1850, 260),
    }


def finish(im, name):
    rot = im.rotate(-ANGLE, expand=True, resample=Image.BICUBIC)
    a = np.array(rot.getchannel("A"))
    ys, xs = np.nonzero(a > 8)
    d = (math.cos(math.radians(ANGLE)), math.sin(math.radians(ANGLE)))   # hướng từ ngòi về đuôi
    k = int(np.argmin(xs * d[0] + ys * d[1]))
    tip = (int(xs[k]), int(ys[k]))
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    rot = rot.crop(box)
    tip = (tip[0] - box[0], tip[1] - box[1])
    w, h = rot.size
    rot = rot.resize((w // SS, h // SS), Image.LANCZOS)
    tip = (tip[0] // SS, tip[1] // SS)
    rot.save(os.path.join(OUT, f"marker-{name}.png"))
    json.dump({"tip": list(tip), "size": list(rot.size)}, open(os.path.join(OUT, f"marker-{name}.json"), "w"))
    print(name, rot.size, "tip", tip)


if __name__ == "__main__":
    for n, im in pens().items():
        finish(im, n)
