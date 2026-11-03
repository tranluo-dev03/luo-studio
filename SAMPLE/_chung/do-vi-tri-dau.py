"""Đo vị trí ĐẦU của nhân vật nền (ghép 2 lớp) trên mọi khung hình, rồi đề xuất ô nhân vật trong khung (robot/AI) ở một góc mà không che đầu.

Chạy:  runtime\\python.exe SAMPLE\\_chung\\do-vi-tri-dau.py <thư mục phan2 của lần chạy | file video/ảnh ...> [--nen HOC] [--goc tren-phai]
       [--ti-le 0.62] [--rong-toi-da 0.30] [--le 0.025] [--noi-ngang 0.35] [--noi-tren 0.6]
  - Thư mục: lấy base_<NEN>.png, listen_<NEN>_*.mp4 và các sceneN_spk.mp4 mà người nói là <NEN> (đọc ../variant.json + ../phan.json nếu có).
  - --ti-le: rộng/cao (theo pixel) của ô; mặc định 0.62 (gen 9:16 rồi cắt vừa). --rong-toi-da: bề rộng tối đa của ô (tỉ lệ khung).
In ra: vùng đầu (gộp mọi khung, x0,y0,x1,y1 theo tỉ lệ 0..1) và dòng "khung DAY: x, y, rộng, cao" để dán vào khối [GHEP HAI LOP].
Vùng đầu = khung mặt (mediapipe) nới thêm cho tóc: lên trên --noi-tren x cao mặt (mặc định 0,6), hai bên --noi-ngang x rộng mặt (mặc định 0,35;
chỉ cần không che MẶT thì dùng nhỏ hơn, vd. 0,1, ô sẽ to hơn và có thể che một phần tóc hai bên)."""
import argparse
import glob
import json
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "app", "luo-studio"))
import face_mesh as FM  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def files_from_dir(d, nen):
    out = [p for p in [os.path.join(d, f"base_{nen}.png")] if os.path.exists(p)] + sorted(glob.glob(os.path.join(d, f"listen_{nen}_*.mp4")))
    run = os.path.dirname(os.path.abspath(d))
    vj, pj = os.path.join(run, "variant.json"), os.path.join(run, "phan.json")
    spk = sorted(glob.glob(os.path.join(d, "scene*_spk.mp4")), key=lambda p: int(os.path.basename(p)[5:].split("_")[0]))
    if os.path.exists(vj):
        luot = [t for t in json.load(open(vj, encoding="utf-8")).get("LUOT", []) if str(t.get("text", "")).strip()]
        part = os.path.basename(os.path.normpath(d)).replace("phan", "")
        if os.path.exists(pj) and part.isdigit():
            plan = {(s["phan"], s["local"]): s["turn"] for s in json.load(open(pj, encoding="utf-8"))}
            who = lambda n: str(luot[plan[(int(part), n)]].get("who", "")).upper() if (int(part), n) in plan else ""
        else:
            who = lambda n: str(luot[n - 1].get("who", "")).upper() if n - 1 < len(luot) else ""
        spk = [p for p in spk if who(int(os.path.basename(p)[5:].split("_")[0])) == nen]
    return out + spk


def frames(path, fps=3):
    if path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        im = cv2.imread(path)
        if im is not None:
            yield cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        return
    cap = cv2.VideoCapture(path)
    step = max(1, int(round((cap.get(cv2.CAP_PROP_FPS) or 24) / fps)))
    i = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if i % step == 0:
            yield cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        i += 1
    cap.release()


def head_boxes(paths, side=0.35, top=0.6):
    lm = FM.landmarker(0.4)
    boxes, seen = [], 0
    try:
        for p in paths:
            for rgb in frames(p):
                seen += 1
                pts = lm.find(rgb)
                if not pts:
                    continue
                xs, ys = [q.x for q in pts], [q.y for q in pts]
                fx0, fx1, fy0, fy1 = min(xs), max(xs), min(ys), max(ys)
                fw, fh = fx1 - fx0, fy1 - fy0
                boxes.append((fx0 - side * fw, fy0 - top * fh, fx1 + side * fw, fy1))
    finally:
        lm.close()
    return np.array(boxes), seen


def suggest(head, corner, ratio, wmax, margin, W=1080, H=1920):
    """Ô lớn nhất (rộng <= wmax) đặt sát góc, không chạm vùng đầu (cách `margin`). ratio = rộng/cao theo pixel."""
    hx0, hy0, hx1, hy1 = head
    right, top = "phai" in corner, "tren" in corner
    best = None
    for w in np.linspace(wmax, 0.12, 60):
        h = w * W / ratio / H
        x = 1 - w - margin if right else margin
        y = margin if top else 1 - h - margin
        clear = (x >= hx1 + margin) if right else (x + w <= hx0 - margin)   # nằm hẳn bên cạnh đầu
        clear = clear or ((y + h <= hy0 - margin) if top else (y >= hy1 + margin))   # hoặc hẳn phía trên / dưới đầu
        if clear and y >= 0 and y + h <= 1:
            best = (round(x, 3), round(y, 3), round(w, 3), round(h, 3))
            break
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="+")
    ap.add_argument("--nen", default="HOC")
    ap.add_argument("--goc", default="tren-phai")
    ap.add_argument("--ti-le", type=float, default=0.62)
    ap.add_argument("--rong-toi-da", type=float, default=0.30)
    ap.add_argument("--le", type=float, default=0.025)
    ap.add_argument("--noi-ngang", type=float, default=0.35)
    ap.add_argument("--noi-tren", type=float, default=0.6)
    a = ap.parse_args()
    paths = []
    for s in a.src:
        paths += files_from_dir(s, a.nen.upper()) if os.path.isdir(s) else [s]
    if not paths:
        sys.exit("Không có file nào để đo")
    b, seen = head_boxes(paths, a.noi_ngang, a.noi_tren)
    print(f"Đo {len(paths)} file, {seen} khung, thấy mặt ở {len(b)} khung")
    if not len(b):
        sys.exit("Không dò được khuôn mặt nào")
    # gộp: lấy biên ngoài ở phân vị 99 (bỏ vài khung dò sai), kẹp trong 0..1
    head = (max(0.0, float(np.percentile(b[:, 0], 1))), max(0.0, float(np.percentile(b[:, 1], 1))),
            min(1.0, float(np.percentile(b[:, 2], 99))), min(1.0, float(np.percentile(b[:, 3], 99))))
    print("Vùng đầu (gộp mọi khung): x %.3f–%.3f, y %.3f–%.3f" % (head[0], head[2], head[1], head[3]))
    box = suggest(head, a.goc, a.ti_le, a.rong_toi_da, a.le)
    if not box:
        print("Không đặt được ô ở góc này mà không che đầu: thử góc khác, giảm --rong-toi-da, hoặc sửa bố cục nhân vật nền (đầu lệch về phía kia).")
        return
    print(f"Đề xuất ô ({a.goc}, rộng/cao {a.ti_le}): x {box[0]}, y {box[1]}, rộng {box[2]}, cao {box[3]} "
          f"= {int(box[2] * 1080)}x{int(box[3] * 1920)} px trên khung 1080x1920")
    print(f"khung DAY: {box[0]}, {box[1]}, {box[2]}, {box[3]}")


if __name__ == "__main__":
    main()
