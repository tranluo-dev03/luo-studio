"""Thay hình trên màn hình điện thoại ở cảnh có người cầm điện thoại (cảnh 6) bằng robot của người dùng + chữ "Talka AI".

Cách làm: dò vùng màn hình (xanh sáng, nền sân khấu tối, áo trắng ngà không ngả xanh) từng khung hình,
lấy khung 4 góc, chiếu ảnh thay thế vào đúng khung đó (có phối cảnh), chỉ vẽ lên chính điểm ảnh màn hình
(ngón tay che màn hình vẫn giữ nguyên). KHÔNG đụng tới mặt/người.

    python thay_man_hinh_dt.py <scene_in.mp4> <scene_out.mp4> [--debug dir]
Âm thanh giữ nguyên.
"""
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
FFMPEG = os.path.join(ROOT, "bin", "ffmpeg.exe")
ROBOT = os.path.join(HERE, "anh", "robot-man-hinh-dien-thoai.webp")
FONT = r"C:\Windows\Fonts\segoeuib.ttf"
TW, TH = 360, 780  # kích thước ảnh màn hình thay thế (tỉ lệ ~ 9:19.5)


def build_screen():
    """Ảnh màn hình mới: robot của người dùng (cắt phần đầu+vai) + chữ Talka AI."""
    im = Image.open(ROBOT).convert("RGB")
    w, h = im.size
    # ảnh robot vuông nền xanh dương: đặt ở nửa trên, phần ngực mờ dần vào nền xanh, chữ trắng bên dưới
    sq = im.crop((0, 0, min(w, h), min(w, h))).resize((TW, TW), Image.LANCZOS)
    top = np.array(sq)[:6].reshape(-1, 3).mean(0)
    blue = tuple(int(x) for x in (top * 0.55 + np.array([0, 40, 150]) * 0.45))
    can = Image.new("RGB", (TW, TH), tuple(int(x) for x in top))
    arr = np.array(can).astype(np.float32)
    for y in range(TH):  # nền xanh đậm dần xuống dưới
        t = min(1.0, y / TH)
        arr[y, :] = top * (1 - t) + np.array(blue) * t
    can = Image.fromarray(arr.astype(np.uint8))
    y0 = 40
    can.paste(sq, (0, y0))
    a = np.array(can).astype(np.float32)
    for y in range(y0 + TW - 90, y0 + TW):  # mờ phần dưới ảnh vào nền
        t = (y - (y0 + TW - 90)) / 90.0
        a[y, :] = a[y, :] * (1 - t) + np.array(blue) * t
    can = Image.fromarray(a.astype(np.uint8))
    dr = ImageDraw.Draw(can)
    f = ImageFont.truetype(FONT, 62)
    txt = "Talka AI"
    tw = dr.textlength(txt, font=f)
    dr.text(((TW - tw) / 2, 470), txt, font=f, fill=(255, 255, 255))
    f2 = ImageFont.truetype(FONT, 22)
    sub = "Your AI English tutor"
    sw = dr.textlength(sub, font=f2)
    dr.text(((TW - sw) / 2, 552), sub, font=f2, fill=(210, 228, 255))
    return cv2.cvtColor(np.array(can), cv2.COLOR_RGB2BGR)


def screen_mask(fr):
    b, g, r = [fr[..., i].astype(np.int16) for i in range(3)]
    m = ((b - r) > 22) & (b > 120) & (g > 110)
    m = m.astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return m


def order_quad(pts):
    """Sắp 4 góc theo TL,TR,BR,BL cho màn hình dọc."""
    pts = np.array(pts, np.float32).reshape(4, 2)
    c = pts.mean(0)
    ang = np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0])
    pts = pts[np.argsort(ang)]  # theo chiều kim đồng hồ bắt đầu từ -pi (trái)
    # chọn TL = điểm có x+y nhỏ nhất rồi giữ thứ tự kim đồng hồ
    k = int(np.argmin(pts.sum(1)))
    pts = np.roll(pts, -k, axis=0)
    return pts  # TL, TR, BR, BL


def detect(fr, prev=None):
    m = screen_mask(fr)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = None
    H, W = m.shape
    for c in cs:
        a = cv2.contourArea(cv2.convexHull(c))  # dùng thân lồi: robot sáng ở giữa màn hình làm thủng vùng xanh
        if a < 250 or a > 0.25 * H * W:
            continue
        rect = cv2.minAreaRect(c)
        (rw, rh) = rect[1]
        if min(rw, rh) < 1:
            continue
        fill = a / (rw * rh)
        asp = max(rw, rh) / min(rw, rh)
        if fill < 0.5 or not (1.2 < asp < 3.8):
            continue
        sc = a * fill
        if best is None or sc > best[0]:
            best = (sc, c, rect)
    if best is None:
        return None, m
    _, c, rect = best
    filled = np.zeros_like(m)
    cv2.fillConvexPoly(filled, cv2.convexHull(c), 255)  # lấp cả phần tối của robot cũ nằm trong màn hình
    m = filled
    hull = cv2.convexHull(c)
    peri = cv2.arcLength(hull, True)
    quad = None
    for eps in (0.02, 0.03, 0.045, 0.06):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4:
            quad = ap.reshape(4, 2)
            break
    if quad is None:
        quad = cv2.boxPoints(rect)
    return order_quad(quad), m


def process(src, dst, debug=None):
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scr = build_screen()
    src_q = np.float32([[0, 0], [TW, 0], [TW, TH], [0, TH]])
    tmp = dst + ".noaudio.mp4"
    vw = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
    n = hit = 0
    last = None
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        q, m = detect(fr)
        if q is not None:
            hit += 1
            if last is not None:  # làm mượt nhẹ để khỏi rung
                q = 0.6 * q + 0.4 * last if np.abs(q - last).max() < 40 else q
            last = q.astype(np.float32)
            Hm = cv2.getPerspectiveTransform(src_q, last.astype(np.float32))
            warp = cv2.warpPerspective(scr, Hm, (W, H), flags=cv2.INTER_LINEAR)
            # chỉ vẽ lên chính điểm ảnh màn hình (giữ ngón tay che); nới 2px cho kín viền xanh
            mm = cv2.dilate(m, np.ones((5, 5), np.uint8))
            region = np.zeros((H, W), np.uint8)
            cv2.fillConvexPoly(region, last.astype(np.int32), 255)
            region = cv2.erode(region, np.ones((3, 3), np.uint8))
            alpha = cv2.bitwise_and(mm, region)
            alpha = cv2.GaussianBlur(alpha, (3, 3), 0).astype(np.float32)[..., None] / 255.0
            fr = (fr * (1 - alpha) + warp * alpha).astype(np.uint8)
            if debug:
                cv2.polylines(fr, [last.astype(np.int32)], True, (0, 255, 0), 1)
        vw.write(fr)
        if debug and n % 12 == 0:
            os.makedirs(debug, exist_ok=True)
            cv2.imwrite(os.path.join(debug, f"f{n:03d}.png"), fr)
        n += 1
    vw.release()
    cap.release()
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", tmp, "-i", src, "-map", "0:v", "-map", "1:a?",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", dst], check=True)
    os.remove(tmp)
    return n, hit


if __name__ == "__main__":
    a = sys.argv[1:]
    dbg = a[a.index("--debug") + 1] if "--debug" in a else None
    n, hit = process(a[0], a[1], dbg)
    print(f"{os.path.basename(a[0])}: {hit}/{n} khung có màn hình")
