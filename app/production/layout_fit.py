"""Giữ bố cục cố định cho thể loại có bảng chèn phía trên (AI tutor ngồi đọc): dò đỉnh đầu nhân vật, dựng khung để Muse mở rộng nền.
Muse hay gen nhân vật to/cận như ảnh tham chiếu; thay vì để robot bị bảng che hoặc làm mờ viền, thu nhân vật về đúng cỡ trong khung rồi nhờ Muse vẽ nối nền."""
import cv2
import numpy as np
from PIL import Image

HEAD_TARGET = 0.36   # đỉnh đầu ở ~36% chiều cao (đáy bảng ~33%)
HEAD_OK = 0.33       # đầu thấp hơn mức này (số lớn hơn) thì bảng không che
SCALE_MIN = 0.6
GREY = (128, 128, 128)


def head_top(path):
    """Đỉnh đầu (0..1 chiều cao khung) từ ảnh hoặc video: dò mặt Haar, đỉnh đầu ~ đỉnh khung mặt - 35% chiều cao mặt. None nếu không dò được."""
    try:
        cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        frames = []
        if str(path).lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            frames = [cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)]
        else:
            cap = cv2.VideoCapture(path)
            n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
            for k in range(1, 9):
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * k / 9))
                ok, fr = cap.read()
                if ok:
                    frames.append(fr)
            cap.release()
        tops = []
        for fr in frames:
            if fr is None:
                continue
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            f = cas.detectMultiScale(g, 1.1, 5, minSize=(g.shape[1] // 10, g.shape[1] // 10))
            if len(f):
                x, y, w, h = max(f, key=lambda r: r[2] * r[3])
                tops.append(max(0.0, (y - 0.35 * h) / g.shape[0]))
        return float(np.median(tops)) if tops else None
    except Exception:  # noqa: BLE001
        return None


def scale_for(top):
    """Tỉ lệ thu để đỉnh đầu về HEAD_TARGET khi neo đáy: top' = (1-s) + s*top."""
    return min(1.0, max(SCALE_MIN, (1 - HEAD_TARGET) / (1 - top)))


def make_canvas(src, dst, s):
    """Ảnh `src` thu còn s, neo đáy giữa khung cùng cỡ, chỗ trống (trên + hai bên) tô xám phẳng để Muse vẽ nối nền."""
    im = Image.open(src).convert("RGB")
    W, H = im.size
    fg = im.resize((max(1, int(W * s)), max(1, int(H * s))), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), GREY)
    canvas.paste(fg, ((W - fg.width) // 2, H - fg.height))
    canvas.save(dst)
    return dst


OUTPAINT_PROMPT = (
    "Edit the attached image. It is a photograph placed in the lower centre of a vertical 9:16 canvas, with flat plain grey (#808080) empty areas above it and on both sides. "
    "Fill ALL the grey areas by naturally extending the photograph's own scene: the same background, floor, walls, windows, props, lighting, perspective and colours, "
    "so the result is ONE seamless full-frame photograph with no visible borders, seams, bands or blur strips. "
    "Keep the existing photograph exactly as it is: the character's face, outfit, pose, size and position must not change, and the character must NOT be enlarged or moved. "
    "The extended area above the character's head must be only plain background (wall, sky or scenery) with no objects of interest, no text, no signs and no logos. "
    "Output exactly one still image, vertical 9:16.")
