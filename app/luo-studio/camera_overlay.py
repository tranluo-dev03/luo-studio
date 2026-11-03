"""Lớp phủ "camera điện thoại" cho một clip cảnh (trường kịch bản "Lớp phủ: camera"): giao diện camera chung chung (lưới 3x3, 1x, hàng chế độ,
nút chụp) + đường viền trắng hình quả trứng ôm theo khuôn mặt từng khung hình (dựng từ viền mặt và độ nghiêng đầu theo điểm mốc mediapipe qua face_mesh.py).

Muse không vẽ được giao diện ổn định và vòng bám mặt đúng chỗ, nên phần này làm ở bước ghép. Khung ra 720x1280, cùng cách cắt với engine.concat_clips.
Giao diện mặc định vẽ bằng PIL, không logo, không sao chép giao diện của hãng nào; muốn dùng giao diện riêng thì đưa PNG trong suốt 9:16 (tự co về 720x1280).
"""
import os
import subprocess

import numpy as np

W, H = 720, 1280
FPS = 30
# viền mặt (FACEMESH_FACE_OVAL) và hai khoé mắt ngoài (33, 263) để lấy độ nghiêng đầu
OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132,
        93, 234, 127, 162, 21, 54, 103, 67, 109]
EYES = (33, 263)
GROW = 1.0       # bề rộng và nửa dưới so với viền mặt
GROW_TOP = 1.12  # nửa trên nới lên tới chân tóc (điểm mốc trán nằm dưới chân tóc), như video mẫu
TAPER = 0.22     # nửa dưới thon về cằm (0 = elip thường)
SMOOTH = 0.45   # làm mượt theo thời gian (0..1, càng nhỏ càng mượt nhưng càng trễ)
HOLD = 8        # mất dấu mặt tối đa N khung thì vẫn giữ vòng ở vị trí cũ, lâu hơn thì ẩn


def _font(size):
    from PIL import ImageFont
    for f in ("arial.ttf", "C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def default_ui():
    """Ảnh RGBA 720x1280 của giao diện camera mặc định."""
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = np.zeros((H, W, 4), np.uint8)   # dải tối mờ trên và dưới để chữ, nút dễ đọc
    top = np.clip((110 - np.arange(H)) / 110, 0, 1) * 90
    bot = np.clip((np.arange(H) - 980) / 300, 0, 1) * 120
    a[..., 3] = np.maximum(top, bot).astype(np.uint8)[:, None]
    img.alpha_composite(Image.fromarray(a, "RGBA"))
    d = ImageDraw.Draw(img)
    white, dim, yellow = (255, 255, 255, 255), (255, 255, 255, 90), (255, 214, 10, 255)
    for x in (W // 3, 2 * W // 3):                       # lưới 3x3 trong vùng xem trước
        d.line([(x, 100), (x, 1010)], fill=dim, width=1)
    for y in (100 + 910 // 3, 100 + 2 * 910 // 3):
        d.line([(0, y), (W, y)], fill=dim, width=1)
    d.polygon([(40, 28), (28, 52), (38, 52), (32, 72), (50, 44), (40, 44), (46, 28)], fill=white)   # tia chớp (đèn flash)
    d.text((210, 38), "HDR", font=_font(20), fill=white)
    d.ellipse([352, 34, 368, 50], outline=white, width=2)
    d.ellipse([670, 32, 694, 56], outline=white, width=2)
    d.ellipse([678, 40, 686, 48], fill=white)
    d.ellipse([338, 1012, 382, 1056], fill=(30, 30, 30, 160))   # nút thu phóng
    f = _font(17)
    d.text((360, 1034), "1x", font=f, fill=white, anchor="mm")
    modes, f = ["SLO-MO", "VIDEO", "PHOTO", "PORTRAIT", "PANO"], _font(19)
    widths = [d.textlength(m, font=f) for m in modes]
    x = 360 - widths[2] / 2 - sum(widths[:2]) - 2 * 34      # căn PHOTO vào giữa
    for m, w_ in zip(modes, widths):
        d.text((x, 1090), m, font=f, fill=yellow if m == "PHOTO" else white)
        x += w_ + 34
    d.ellipse([318, 1143, 402, 1227], outline=white, width=6)   # nút chụp
    d.ellipse([328, 1153, 392, 1217], fill=white)
    d.rounded_rectangle([96, 1159, 148, 1211], radius=8, fill=(60, 60, 60, 230), outline=white, width=2)   # ảnh vừa chụp
    d.ellipse([572, 1159, 624, 1211], fill=(60, 60, 60, 200))   # đổi camera
    d.arc([584, 1171, 612, 1199], 200, 340, fill=white, width=3)
    d.arc([584, 1171, 612, 1199], 20, 160, fill=white, width=3)
    return img


def load_ui(path=None):
    from PIL import Image
    if path and os.path.exists(path):
        return Image.open(path).convert("RGBA").resize((W, H))
    return default_ui()


def face_egg(lm):
    """Thông số hình trứng ôm mặt (cx, cy, nửa bề rộng, chiều cao nửa trên, chiều cao nửa dưới, góc nghiêng rad), pixel của khung W x H.
    Đo trong hệ toạ độ đã xoay thẳng theo độ nghiêng đầu (đường nối hai khoé mắt), nên hình trứng nghiêng theo đầu."""
    pts = np.array([(lm[i].x * W, lm[i].y * H) for i in OVAL])
    (ax, ay), (bx, by) = [(lm[i].x * W, lm[i].y * H) for i in EYES]
    roll = np.arctan2(by - ay, bx - ax)
    c, s = np.cos(roll), np.sin(roll)
    rot = np.array([[c, -s], [s, c]])
    eye_mid = np.array([(ax + bx) / 2, (ay + by) / 2])
    r = (pts - eye_mid) @ rot            # toạ độ theo trục của đầu, gốc ở giữa hai mắt
    lo, hi = r.min(0), r.max(0)
    cx, cy = eye_mid + np.array([(lo[0] + hi[0]) / 2, 0.0]) @ rot.T
    return np.array([cx, cy, (hi[0] - lo[0]) / 2 * GROW, -lo[1] * GROW_TOP, hi[1] * GROW, roll])


def egg_points(e, n=120):
    """Các điểm trên hình trứng: nửa trên là nửa elip, nửa dưới thon dần về cằm."""
    cx, cy, a, top, bot, roll = e
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    down = np.sin(t) > 0                 # trục y hướng xuống: sin > 0 là nửa dưới
    x = a * np.cos(t) * np.where(down, 1 - TAPER * np.sin(t), 1.0)
    y = np.where(down, bot, top) * np.sin(t)
    c, s = np.cos(roll), np.sin(roll)
    return np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)


def render(src, dst, ui_path=None):
    """Ghép lớp phủ camera vào clip `src`, ghi `dst` (giữ tiếng gốc). Trả về tỉ lệ khung hình dò được khuôn mặt (0..1)."""
    import cv2
    import face_mesh as FM
    ui = np.asarray(load_ui(ui_path), np.float32)
    ui_rgb, ui_a = ui[..., :3], ui[..., 3:] / 255.0
    flags = 0x08000000 if os.name == "nt" else 0
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf",
                            f"scale={W}:{H}:flags=accurate_rnd+full_chroma_int:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, creationflags=flags)
    tmp = dst + ".part.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", tmp],
                           stdin=subprocess.PIPE, creationflags=flags)
    fm = FM.landmarker(min_conf=0.3)
    state, lost, n, hit = None, HOLD + 1, 0, 0
    try:
        while True:
            buf = dec.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
            n += 1
            lm = fm.find(fr)
            if lm is not None:
                hit += 1
                lost = 0
                e = face_egg(lm)
                state = e if state is None else state + SMOOTH * (e - state)
            else:
                lost += 1
            if state is not None and lost <= HOLD:
                poly = np.round(egg_points(state) * 8).astype(np.int32)   # shift=3: toạ độ lẻ pixel cho nét mượt
                cv2.polylines(fr, [poly], True, (255, 255, 255), 3, cv2.LINE_AA, shift=3)
            out = fr.astype(np.float32) * (1 - ui_a) + ui_rgb * ui_a
            enc.stdin.write(out.astype(np.uint8).tobytes())
    finally:
        fm.close()
        try:
            enc.stdin.close()
        except OSError:
            pass
        enc.wait()
        dec.stdout.close()
        dec.wait()
    if enc.returncode or not n:
        raise RuntimeError("ffmpeg không ghi được clip có lớp phủ camera")
    os.replace(tmp, dst)
    return hit / n
