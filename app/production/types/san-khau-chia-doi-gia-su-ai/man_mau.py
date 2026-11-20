"""Cân sắc màu các cảnh SÂN KHẤU của phần 1 về cảnh 1 (bước hậu kỳ, chạy trong post.py).
Vì sao: engine chỉ kéo màu mỗi cảnh về khung đầu CỦA CHÍNH cảnh đó (chế độ "anchor") và chỉnh có giới hạn nhỏ, nên cảnh 3–6 mỗi cảnh một tông
(da ngả cam/vàng, áo xám / xanh). Ở đây kéo SẮC (độ đậm + hướng màu trong không gian Lab: a*, b*) về cảnh 1, KHÔNG đụng độ sáng/tương phản
(bố cục cảnh 1 là toàn thân, các cảnh sau là cận nên độ sáng trung bình khác nhau tự nhiên).
Đo trên MÀU DA diễn giả (vùng má/trán, Haar): cảnh toàn thân và cảnh cận có thống kê cả khung khác nhau theo bố cục chứ không theo tông màu
(đo thử 20/11/2026: bão hoà cảnh 4 'thiếu' 30% chỉ vì bố cục) → chỉnh theo cả khung sẽ quá tay. Chỉnh liên tục theo thời gian trong cảnh
(nửa đầu → nửa sau) vì Muse hay trôi màu dần. Bỏ qua cảnh tiệc (lượt có "gach") và phần 2.
Lần 1 làm bằng eq/lutyuv (YUV) bị chặn trần ±10 nên cảnh 6 của X0104 còn vàng (Lab b +3): đổi sang chỉnh trực tiếp a*/b* từng khung."""
import subprocess

import cv2
import numpy as np

_FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def _skin(fr):
    """(a*, b*, x, y, w) của vùng má/trán của khuôn mặt lớn nhất, hoặc None."""
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    fs = _FACE.detectMultiScale(g, 1.1, 5, minSize=(max(30, fr.shape[1] // 20),) * 2)
    if len(fs) == 0:
        return None
    x, y, w, h = max(fs, key=lambda f: f[2] * f[3])
    patch = fr[y + int(h * 0.35): y + int(h * 0.75), x + int(w * 0.2): x + int(w * 0.8)]
    if patch.size == 0:
        return None
    lab = cv2.cvtColor(patch, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    return float(lab[:, 1].mean()), float(lab[:, 2].mean()), float(x), float(y), float(w)


def _stats(cap, fps, times):
    """(a*, b*) màu da: lấy trung vị các lần dò; bỏ lần dò lệch vị trí/kích thước so với số đông (cảnh toàn thân có khuôn mặt nhỏ, máy dò mặt hay dò nhầm)."""
    det = [d for d in (_one(cap, fps, t) for t in times) if d]
    if len(det) < 2:
        return None
    mx, my, mw = (float(np.median([d[i] for d in det])) for i in (2, 3, 4))
    ok = [d for d in det if abs(d[4] - mw) <= 0.25 * mw and abs(d[2] - mx) <= 1.2 * mw and abs(d[3] - my) <= 1.2 * mw]
    if len(ok) < 2:
        return None
    return float(np.median([d[0] for d in ok])), float(np.median([d[1] for d in ok]))


def _one(cap, fps, t):
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(t * fps)))
    ok, fr = cap.read()
    return _skin(fr) if ok else None


def _grade(ref, cur):
    """(nhân độ đậm, da, db) đưa (a*,b*) của `cur` về `ref`, có giới hạn."""
    cr, cc = float(np.hypot(ref[0] - 128, ref[1] - 128)), float(np.hypot(cur[0] - 128, cur[1] - 128))
    k = min(1.35, max(0.7, cr / cc)) if cc > 1 else 1.0
    da = max(-14.0, min(14.0, ref[0] - (128 + (cur[0] - 128) * k)))
    db = max(-14.0, min(14.0, ref[1] - (128 + (cur[1] - 128) * k)))
    return k, da, db


def can_mau(src, dst, scenes, log=print):
    """scenes = [(số cảnh, bắt đầu, kết thúc)] đầu tiên là cảnh chuẩn (cảnh 1); các cảnh còn lại được kéo sắc về nó.
    Ghi dst và trả về True nếu có chỉnh; False (không ghi) nếu mọi cảnh đã đủ gần."""
    if len(scenes) < 2:
        return False
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n0, a0, b0 = scenes[0]
    span = lambda a, b, lo, hi, n=4: [a + (lo + (hi - lo) * i / (n - 1)) * (b - a) for i in range(n)]
    ref = _stats(cap, fps, span(a0, b0, 0.05, 0.95, 14))
    if not ref:
        cap.release()
        return False
    plan = []   # (bắt đầu, kết thúc, (k,da,db) đầu cảnh, (k,da,db) cuối cảnh)
    for n, a, b in scenes[1:]:
        c0 = _stats(cap, fps, span(a, b, 0.05, 0.4, 6)) or _stats(cap, fps, span(a, b, 0.05, 0.95, 10))
        c1 = _stats(cap, fps, span(a, b, 0.6, 0.95, 6)) or c0
        if not c0:
            log(f"  cảnh {n}: không thấy khuôn mặt để đo, giữ nguyên")
            continue
        g0, g1 = _grade(ref, c0), _grade(ref, c1)
        near = lambda g: abs(g[0] - 1) < 0.04 and abs(g[1]) < 1.2 and abs(g[2]) < 1.2
        log(f"  cảnh {n}: da (a*,b*) đầu {c0[0]:.0f},{c0[1]:.0f} cuối {c1[0]:.0f},{c1[1]:.0f} → chuẩn {ref[0]:.0f},{ref[1]:.0f}"
            + (" (đủ gần)" if near(g0) and near(g1) else f" → đầu ×{g0[0]:.2f} {g0[1]:+.1f} {g0[2]:+.1f}, cuối ×{g1[0]:.2f} {g1[1]:+.1f} {g1[2]:+.1f}"))
        if near(g0) and near(g1):
            continue
        plan.append((a, b, g0, g1))
    cap.release()
    if not plan:
        return False

    cap = cv2.VideoCapture(src)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps:.3f}", "-i", "-",
                          "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                          "-c:a", "copy", "-movflags", "+faststart", dst], stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        t = i / fps
        for a, b, g0, g1 in plan:
            if a <= t < b:
                f = (t - a) / max(0.1, b - a)
                k, da, db = (g0[j] + (g1[j] - g0[j]) * f for j in range(3))
                lab = cv2.cvtColor(fr, cv2.COLOR_BGR2LAB).astype(np.float32)
                lab[..., 1] = (128 + (lab[..., 1] - 128) * k + da).clip(0, 255)
                lab[..., 2] = (128 + (lab[..., 2] - 128) * k + db).clip(0, 255)
                fr = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
                break
        p.stdin.write(fr.tobytes())
        i += 1
    cap.release()
    p.stdin.close()
    if p.wait() != 0:
        log("  CẢNH BÁO: ffmpeg ghi video cân màu lỗi, bỏ qua")
        return False
    return True
