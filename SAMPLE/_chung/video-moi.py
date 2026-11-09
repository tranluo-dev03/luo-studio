#!/usr/bin/env python
"""Công cụ cho quy trình "video mới -> kịch bản + biến thể -> Studio" (xem SO-TAY-KY-THUAT.md và skill `luo-video-moi`).

Chạy bằng Python đi kèm Studio (có ffmpeg, faster-whisper, cv2, numpy):

  runtime\\python.exe SAMPLE\\_chung\\video-moi.py danh-gia  <video.mp4 | thư-mục-phan-tich> [--lang en] [--model small]
      Chạy phan-tich-video.py (nếu chưa có bao-cao.json) rồi đo thêm: số khuôn mặt và vị trí theo giây, chuyển động máy quay theo từng đoạn
      giữa hai cảnh cắt, cao độ giọng từng lượt (gom thành 2 giọng), và GỢI Ý khuôn thể loại + kỹ thuật cần dùng. Ra: danh-gia.md, danh-gia.json.
      Gợi ý chỉ là điểm xuất phát: agent vẫn phải xem từng ảnh luot_NN.jpg và tự quyết định.

  runtime\\python.exe SAMPLE\\_chung\\video-moi.py kiem-tra  <KICH-BAN.txt> <BIEN-THE.json> [--tai-anh]
      Kiểm tra bằng chính code của Studio: token kịch bản = khoá biến thể, số cảnh/lượt, [GHEP HAI LOP] đọc được, nhiều phần hợp lệ,
      emo trong EMO_CUES, lời <= 20 từ, cặp wrong -> right, điền token không còn {{, độ dài prompt; --tai-anh: tải thử mọi link refs.
      Thoát mã 1 nếu có LỖI (cảnh báo không làm thoát lỗi).

  runtime\\python.exe SAMPLE\\_chung\\video-moi.py nhap <KICH-BAN.txt> <BIEN-THE.json> --ten-loai "Tên loại" --ten-du-an "Tên dự án" [--chay-thu] [--thu]
      Nhập vào Studio đang chạy (đọc userdata/running.json): tạo loại dự án (POST /api/types), tạo dự án với các biến thể (POST /api/projects,
      Studio tự tải ảnh refs), --chay-thu: thêm biến thể ĐẦU TIÊN vào hàng đợi và bắt đầu. --thu: chỉ in ra việc sẽ làm, không gọi API.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(ROOT, "bin")
FFMPEG = os.path.join(BIN, "ffmpeg.exe") if os.path.exists(os.path.join(BIN, "ffmpeg.exe")) else "ffmpeg"
STUDIO = os.path.join(ROOT, "app", "luo-studio")
PROD = os.path.join(ROOT, "app", "production")
CHUNG = os.path.join(PROD, "types", "_chung")
for p in (STUDIO, PROD, CHUNG):
    if p not in sys.path:
        sys.path.insert(0, p)


def _run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    if r.returncode:
        raise RuntimeError(f"{os.path.basename(str(cmd[0]))} lỗi: {r.stderr.decode('utf-8', 'replace')[-500:]}")
    return r


# ============================================================================ danh-gia

def _frames_gray(video, fps, w, h):
    """Khung xám (uint8) theo fps, cỡ w x h."""
    import numpy as np
    d = _run([FFMPEG, "-v", "error", "-i", video, "-vf", f"fps={fps},scale={w}:{h}", "-pix_fmt", "gray", "-f", "rawvideo", "-"]).stdout
    n = len(d) // (w * h)
    return np.frombuffer(d[: n * w * h], np.uint8).reshape(n, h, w)


def faces_timeline(video, fps=2, w=360):
    """[(giây, [(cx, cy, rộng, cao) theo tỉ lệ 0..1])] bằng Haar cascade (mặt thẳng + mặt nghiêng). Đủ để đếm người và biết họ ở phía nào."""
    import cv2
    import numpy as np
    cas = [cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, f)) for f in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml")]
    probe = _run([FFMPEG.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", video]).stdout.decode().strip().split(",")
    W0, H0 = int(probe[0]), int(probe[1])
    h = int(w * H0 / W0)
    fr = _frames_gray(video, fps, w, h)
    # vạch chia dọc (màn hình chia đôi): mép giữa khung có độ chênh cột lớn và bền qua mọi khung so với các cột khác
    import numpy as np
    col = np.abs(np.diff(fr.astype(np.float32), axis=2)).mean(axis=1)   # (khung, w-1): chênh giữa cột kề nhau, trung bình theo chiều dọc
    mid = col[:, w // 2 - 3: w // 2 + 2].max(axis=1)
    base = np.median(col, axis=1) + 1e-6
    seam = float(np.median(mid / base))
    faces_timeline.seam = seam   # >= 6: gần như chắc chắn có vạch chia giữa khung
    out = []
    for i, g in enumerate(fr):
        g = cv2.equalizeHist(g)
        boxes = []
        for c in cas:
            for (x, y, bw, bh) in c.detectMultiScale(g, 1.1, 5, minSize=(int(w * 0.07), int(w * 0.07))):
                boxes.append((x, y, bw, bh))
        # gộp hộp trùng nhau (frontal và profile cùng một mặt)
        keep = []
        for b in sorted(boxes, key=lambda b: -b[2] * b[3]):
            if not any(abs(b[0] + b[2] / 2 - k[0] - k[2] / 2) < max(b[2], k[2]) * 0.5 and abs(b[1] + b[3] / 2 - k[1] - k[3] / 2) < max(b[3], k[3]) * 0.5 for k in keep):
                keep.append(b)
        out.append((round(i / fps, 2), [(round((x + bw / 2) / w, 3), round((y + bh / 2) / h, 3), round(bw / w, 3), round(bh / h, 3)) for (x, y, bw, bh) in keep]))
    return out, (W0, H0)


def camera_motion(video, cuts, total, fps=8, w=160, h=284):
    """Dịch chuyển khung hình (px trên khung 160x284) giữa các khung liên tiếp bằng phase correlation, bỏ khung ngay tại cảnh cắt.
    Trả về theo từng đoạn giữa hai cảnh cắt: tổng dịch chuyển, dịch chuyển lớn nhất/giây, kết luận."""
    import cv2
    import numpy as np
    fr = _frames_gray(video, fps, w, h).astype(np.float32)
    if len(fr) < 3:
        return []
    shifts = []
    for i in range(1, len(fr)):
        (dx, dy), resp = cv2.phaseCorrelate(fr[i - 1], fr[i])
        shifts.append((i / fps, float(np.hypot(dx, dy)), float(resp)))
    bounds = [0.0] + sorted(c for c in cuts if 0 < c < total) + [total]
    segs = []
    for a, b in zip(bounds, bounds[1:]):
        if b - a < 0.3:
            continue
        s = [m for (t, m, r) in shifts if a + 0.2 <= t <= b - 0.05]
        if not s:
            continue
        per_sec = []
        for k in range(int(a), int(b) + 1):
            x = [m for (t, m, r) in shifts if max(a + 0.2, k) <= t < min(b - 0.05, k + 1)]
            if x:
                per_sec.append((k, round(float(np.sum(x)), 1)))
        tot = float(np.sum(s))
        mx = max(per_sec, key=lambda z: z[1]) if per_sec else (int(a), 0.0)
        verdict = ("đứng yên" if mx[1] < 4 else "rung nhẹ / cầm tay" if mx[1] < 10 else "có chuyển động máy (lia/đẩy/zoom)")
        segs.append({"tu": round(a, 2), "den": round(b, 2), "tong_px": round(tot, 1), "manh_nhat": {"giay": mx[0], "px": mx[1]}, "ket_luan": verdict,
                     "theo_giay": per_sec})
    return segs


def pitch_per_turn(wav, turns):
    """Cao độ trung vị (Hz) từng lượt: tự tương quan trên khung 40 ms, 16 kHz, 70–400 Hz, chỉ khung có năng lượng và tính tuần hoàn rõ."""
    import numpy as np
    import wave
    with wave.open(wav, "rb") as f:
        sr, n = f.getframerate(), f.getnframes()
        a = np.frombuffer(f.readframes(n), np.int16).astype(np.float32) / 32768.0
    win, hop = int(sr * 0.04), int(sr * 0.01)
    lo, hi = int(sr / 400), int(sr / 70)
    out = []
    for t in turns:
        s0, s1 = int(t["start"] * sr), int(t["end"] * sr)
        seg = a[s0:s1]
        f0s = []
        if len(seg) > win:
            thr = 0.25 * float(np.sqrt(np.mean(seg ** 2)) + 1e-6)
            for i in range(0, len(seg) - win, hop):
                x = seg[i:i + win]
                if np.sqrt(np.mean(x ** 2)) < thr:
                    continue
                x = x - x.mean()
                ac = np.correlate(x, x, "full")[win - 1:]
                if ac[0] <= 0:
                    continue
                ac = ac / ac[0]
                k = lo + int(np.argmax(ac[lo:hi]))
                if ac[k] > 0.5:
                    f0s.append(sr / k)
        out.append(round(float(np.median(f0s)), 0) if len(f0s) >= 5 else None)
    return out


def group_voices(hz):
    """Gom các lượt có Hz thành 2 giọng (k-means 1 chiều). Trả về (nhãn từng lượt 'A'/'B'/None, {A: (min, median, max), B: ...})."""
    import numpy as np
    v = [h for h in hz if h]
    if len(v) < 2:
        return [("A" if h else None) for h in hz], {"A": (min(v), v[0], max(v))} if v else {}
    c = [min(v), max(v)]
    for _ in range(20):
        lab = [0 if abs(x - c[0]) <= abs(x - c[1]) else 1 for x in v]
        nc = [float(np.mean([x for x, l in zip(v, lab) if l == i])) if any(l == i for l in lab) else c[i] for i in range(2)]
        if nc == c:
            break
        c = nc
    if abs(c[0] - c[1]) < 25:   # hai cụm quá gần: coi như một giọng (hoặc hai người cùng cao độ: cảnh báo riêng)
        return ["A" if h else None for h in hz], {"A": (min(v), float(np.median(v)), max(v))}
    names = {0: "A", 1: "B"}
    labels, groups = [], {}
    it = iter(v)
    for h in hz:
        if not h:
            labels.append(None); continue
        x = next(it)
        l = 0 if abs(x - c[0]) <= abs(x - c[1]) else 1
        labels.append(names[l]); groups.setdefault(names[l], []).append(x)
    return labels, {k: (min(g), float(np.median(g)), max(g)) for k, g in groups.items()}


def suggest(report, faces, cam, voices, labels):
    """Gợi ý khuôn + kỹ thuật từ số đo. Trả về danh sách dòng markdown."""
    import numpy as np
    turns, cuts, total = report["turns"], report["cuts"], report["stats"]["duration"]
    counts = [len(b) for _, b in faces]
    med_faces = float(np.median(counts)) if counts else 0
    share2 = sum(1 for c in counts if c >= 2) / max(1, len(counts))
    # ô nhỏ ở góc (PiP): một mặt nhỏ hơn hẳn mặt kia và nằm sát mép trên hoặc một nửa màn hình
    pip = 0
    for _, b in faces:
        if len(b) >= 2:
            big, small = sorted(b, key=lambda z: -z[2] * z[3])[:2]
            if small[2] * small[3] < 0.4 * big[2] * big[3] and (small[1] < 0.3 or abs(small[0] - big[0]) > 0.4):
                pip += 1
    pip_share = pip / max(1, sum(1 for c in counts if c >= 2))
    moves = [s for s in cam if "chuyển động" in s["ket_luan"]]
    lines = ["## Gợi ý khuôn (từ số đo, cần đối chiếu ảnh)", ""]
    lines.append(f"- Độ dài {total}s, {len(turns)} câu, {len(cuts)} cảnh cắt cứng, tốc độ nói trung vị {report['stats']['median_wps']} từ/giây.")
    lines.append(f"- Số mặt trung vị mỗi khung: {med_faces:g}; {share2:.0%} thời gian có ≥ 2 mặt; trong đó {pip_share:.0%} có dạng một mặt nhỏ tách riêng (ô PiP / chia khung).")
    mv_txt = ", ".join("%s–%ss" % (m["tu"], m["den"]) for m in moves[:6]) + ("…" if len(moves) > 6 else "")
    lines.append(f"- Đoạn có chuyển động máy: {len(moves)}/{len(cam)} ({mv_txt}).")
    lines.append(f"- Giọng: {len(voices)} cụm cao độ: " + "; ".join(f"{k}: {v[1]:.0f} Hz ({v[0]:.0f}–{v[2]:.0f})" for k, v in voices.items()) + " (gom tự động, một người nói lên xuống giọng có thể bị tách làm hai: nghe lại).")
    seam = getattr(faces_timeline, "seam", 0.0)
    split_screen = seam >= 6
    lines.append(f"- Vạch chia dọc giữa khung: {'CÓ' if split_screen else 'không'} (độ nổi {seam:.1f}; ≥ 6 là có).")
    lines.append("")
    rec = []
    if split_screen:
        rec.append("**Màn hình chia đôi dọc** → `[GHEP HAI LOP]` với nền có khung riêng (`khung HOC: 0.5, 0, 0.5, 1` + `khung DAY: 0, 0, 0.5, 1`), mẫu `chia-doi-gia-su-ai`: "
                   "gen riêng từng nhân vật 9:16 rồi cắt DẢI GIỮA, nhân vật đứng giữa, `noi: lien`, `nghe: moi canh`, refs cho cả hai; viền sai/đúng chỉ ở nửa người dùng (`config.json` → `vien`).")
    if med_faces < 1.5 and share2 < 0.2:
        rec.append("**Một nhân vật trong hình.** Nếu nhân vật nói → khuôn `talka-bang-tu-vung` (nền có chữ/bảng → nền xanh + hậu kỳ vẽ chữ) hoặc `ai-tutor-ngoi-doc` "
                   "(bảng gen AI + chữ do code). Nếu người trong hình KHÔNG nhép miệng (xem luot_NN.jpg) → lồng tiếng ngoài khung, khuôn `Doi toc` "
                   "(Voice trong ngoặc kép, LUOT: [], mỗi hình đổi là một Prompt ảnh).")
    if share2 >= 0.2 and pip_share >= 0.5:
        rec.append("**Hai vùng tách biệt (PiP / chia khung)** → `[GHEP HAI LOP]` (mẫu `ghep-hai-lop`, `chia-doi-gia-su-ai`, phần 2 `san-bay`/`soi-hanh-ly`): gen riêng từng nhân vật, "
                   "`noi: lien`, `nghe: moi canh`, đo ô bằng `do-vi-tri-dau.py`, refs cho mọi nhân vật.")
    if share2 >= 0.2 and pip_share < 0.5 and not split_screen:
        rec.append("**Hai người chung khung thật** → cảnh thường, khối CẢNH (mẫu `canh-sat-nu`, phần 1 `soi-hanh-ly-gia-su-ai`): một lượt một cảnh, hành động trong lúc nói, "
                   "`NGHE_/NHIN_` cho từng người, đạo cụ `DAO_*`. Kiểm tra giới tính hai người: cùng giới cùng khung dễ nhép nhầm (ưu tiên khác giới).")
    # chia phần: bố cục mặt đổi hẳn tại một cảnh cắt (vd. 2 mặt chung khung -> 1 mặt lớn + 1 mặt nhỏ)
    def layout(t0, t1):
        seg = [len(b) for s, b in faces if t0 <= s < t1]
        pp = sum(1 for s, b in faces if t0 <= s < t1 and len(b) >= 2 and (lambda bb: bb[1][2] * bb[1][3] < 0.4 * bb[0][2] * bb[0][3])(sorted(b, key=lambda z: -z[2] * z[3])))
        return (round(float(np.median(seg)), 0) if seg else 0, pp / max(1, len(seg)))
    bounds = [0.0] + [c for c in cuts if 0 < c < total] + [total]
    prev = None
    for a, b in zip(bounds, bounds[1:]):
        if b - a < 2:
            continue
        L = layout(a, b)
        if prev and (abs(L[0] - prev[0]) >= 1 or abs(L[1] - prev[1]) > 0.5):
            rec.append(f"**Có thể đổi cơ chế ở {a}s** (bố cục mặt đổi từ {prev} sang {L}: (số mặt, tỉ lệ PiP)). Nếu một bên là tình huống thật, bên kia là hội thoại với AI → "
                       "dự án NHIỀU PHẦN (`[HAU KY] loai: <mã>` + `===== PHAN n ... | vao: nhoe 0.5 =====`, gen.py/post.py 5 dòng gọi `_chung/`).")
        prev = L
    if len(cuts) >= 6:
        rec.append(f"**Nhiều góc máy ({len(cuts)} cảnh cắt).** Mỗi góc là một cảnh có `Prompt ảnh` + `CAMERA ANGLE` + EYE LINE riêng; BẮT BUỘC gắn ảnh tham chiếu mặt cho mọi nhân vật. "
                   "Cân nhắc giữ ít góc hơn (đổi cỡ cảnh làm mặt trôi) và ghi vào bảng \"video gốc → kịch bản\".")
    if moves:
        rec.append("**Có chuyển động máy.** Mặc định bỏ (camera đứng yên) hoặc làm bằng `Chuyển cảnh: lia phải/trái`; chỉ giao Muse lia khi có `Ảnh tổng quan` 16:9 + "
                   "`Khung đầu cắt` + khối CAMERA MOVE + `Giữ sau lời` (+ `Lia nhanh`, `Lia theo tay`). Xem SO-TAY-KY-THUAT.md mục 3.5.")
    if len(voices) == 1 and share2 >= 0.2:
        rec.append("**Cảnh báo: hai người nhưng chỉ một cụm cao độ** → có thể cùng giới, cùng tuổi: Muse hay gán giọng nhầm mặt. Mô tả giọng khác hẳn, hoặc đổi một người sang giới khác.")
    fast = [t for t in turns if t["words"] >= 4 and t["wps"] >= 5]
    if fast:
        rec.append(f"**Nói nhanh** ({len(fast)} câu ≥ 5 từ/giây): ghi \"about {report['stats']['median_wps']:.1f} words per second (short lines up to {report['stats']['max_wps']:.0f})\" vào [VIDEO SUFFIX]; Muse hay chậm hơn.")
    long_turns = [t for t in turns if t["words"] > 20]
    if long_turns:
        rec.append(f"**{len(long_turns)} câu dài > 20 từ** (câu {', '.join(str(t['n']) for t in long_turns[:8])}): tách thành hai lượt cùng người.")
    rec.append("Phần robot toàn khung kêu gọi tải app, popup cài app, end card, badge: KHÔNG gen → Thương hiệu của dự án (logo, Video giới thiệu, Outro).")
    lines += [f"{i}. {r}" for i, r in enumerate(rec, 1)]
    return lines


def cmd_danh_gia(a):
    src = os.path.abspath(a.src)
    if os.path.isdir(src):
        out, video = src, None
    else:
        video, out = src, os.path.splitext(src)[0] + "-phan-tich"
    rep = os.path.join(out, "bao-cao.json")
    if not os.path.exists(rep):
        if not video:
            sys.exit(f"Thư mục {out} chưa có bao-cao.json; đưa đường dẫn video để chạy phân tích.")
        print("Chưa có bao-cao.json: chạy phan-tich-video.py trước...")
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        subprocess.run([sys.executable, os.path.join(HERE, "phan-tich-video.py"), video, out, "--lang", a.lang, "--model", a.model], check=True, env=env)
    report = json.load(open(rep, encoding="utf-8"))
    if not video:
        cand = [os.path.join(os.path.dirname(out), f) for f in os.listdir(os.path.dirname(out)) if os.path.splitext(f)[0] + "-phan-tich" == os.path.basename(out)]
        video = cand[0] if cand else None
    if not video or not os.path.exists(video):
        sys.exit("Không tìm thấy file video cạnh thư mục phân tích; đưa đường dẫn video.")
    turns, cuts, total = report["turns"], report["cuts"], report["stats"]["duration"]
    print("Đếm khuôn mặt theo giây...")
    faces, (W0, H0) = faces_timeline(video)
    print("Đo chuyển động máy quay...")
    cam = camera_motion(video, cuts, total)
    print("Đo cao độ giọng từng lượt...")
    wav = os.path.join(out, "audio.wav")
    if not os.path.exists(wav):
        _run([FFMPEG, "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav])
    hz = pitch_per_turn(wav, turns)
    labels, voices = group_voices(hz)

    md = [f"# Đánh giá video: {os.path.basename(video)} ({W0}x{H0})", "",
          "Số đo bổ sung cho `bao-cao.md`. Gợi ý ở cuối chỉ là điểm xuất phát; vẫn phải xem từng ảnh `luot_NN.jpg` / `chuyen-dong_NN.jpg` và điền bảng hành động.", "",
          "## Lượt nói: cao độ, mặt trong khung", "", "| # | Giây | Từ/giây | Hz | Giọng | Số mặt (vị trí) | Lời |", "|---|---|---|---|---|---|---|"]
    def pos(b):
        return ("trái" if b[0] < 0.4 else "phải" if b[0] > 0.6 else "giữa") + ("-trên" if b[1] < 0.35 else "-dưới" if b[1] > 0.65 else "") + (" nhỏ" if b[2] < 0.18 else "")
    for t, h, l in zip(turns, hz, labels):
        fs = [b for s, b in faces if t["start"] <= s <= t["end"]]
        n = round(sum(len(b) for b in fs) / max(1, len(fs)), 1) if fs else 0
        sample = max(fs, key=len) if fs else []
        md.append(f"| {t['n']} | {t['start']}–{t['end']} | {t['wps']} | {h or '?'} | {l or '?'} | {n:g} ({', '.join(pos(b) for b in sample)}) | {t['text']} |")
    md += ["", "## Giọng (gom theo cao độ)", ""]
    for k, (lo, med, hi) in voices.items():
        kind = "nam trầm" if med < 140 else "nam / nữ trầm" if med < 175 else "nữ trung" if med < 230 else "nữ cao / trẻ em"
        md.append(f"- Giọng {k}: trung vị {med:.0f} Hz ({lo:.0f}–{hi:.0f}) → gợi ý `GIONG_`: \"{kind}, around {int(lo // 10 * 10)}–{int(hi // 10 * 10 + 10)} Hz\" (nghe lại để mô tả âm sắc, giọng vùng miền, nhịp).")
    md += ["", "## Chuyển động máy quay theo đoạn (giữa hai cảnh cắt)", "", "| Đoạn | Tổng dịch (px/160x284) | Mạnh nhất (giây: px) | Kết luận |", "|---|---|---|---|"]
    for s in cam:
        md.append(f"| {s['tu']}–{s['den']}s | {s['tong_px']} | {s['manh_nhat']['giay']}s: {s['manh_nhat']['px']} | {s['ket_luan']} |")
    md += ["", "## Số mặt theo giây", "", "| Giây | Số mặt | Vị trí (tâm x, y; rộng) |", "|---|---|---|"]
    for s, b in faces[::2]:
        md.append(f"| {s} | {len(b)} | {'; '.join(f'({x:.2f}, {y:.2f}; {w:.2f})' for x, y, w, h in b)} |")
    md += [""] + suggest(report, faces, cam, voices, labels)
    md += ["", "## Việc tiếp theo", "", "1. Xem từng ảnh `luot_NN.jpg`, `chuyen-dong_NN.jpg`, `tong-quan_N.jpg`; điền bảng hành động (ai nói, hành động, người nghe, vật dụng, ánh mắt, camera, khung cuối).",
           "2. Chọn khuôn theo bảng mục 2 của `SAMPLE/_chung/SO-TAY-KY-THUAT.md`; mở `SAMPLE/<mẫu>/` để dùng lại kịch bản, biến thể, cong-cu, PROMPT-CHO-AGENT.txt.",
           "3. Viết `SAMPLE/<mã mới>/PHAN-TICH-VIDEO-MAU.md` (bảng hành động + bảng video gốc → kịch bản), kịch bản, biến thể; rồi `video-moi.py kiem-tra`, `video-moi.py nhap`."]
    open(os.path.join(out, "danh-gia.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump({"video": video, "size": [W0, H0], "faces": faces, "camera": cam, "pitch": hz, "voice_label": labels, "voices": voices},
              open(os.path.join(out, "danh-gia.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Xong: {os.path.join(out, 'danh-gia.md')}")
    print("\n".join(suggest(report, faces, cam, voices, labels)))


# ============================================================================ kiem-tra

class Check:
    def __init__(self):
        self.err, self.warn, self.ok = [], [], []

    def e(self, m): self.err.append(m); print("  LỖI  ", m)
    def w(self, m): self.warn.append(m); print("  CẢNH BÁO", m)
    def o(self, m): self.ok.append(m); print("  ok   ", m)


def _tokens(text):
    return set(re.findall(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}", text))


def _emo_ok(emo, cues):
    words = [w.strip().lower() for w in re.split(r"[,\s]+", emo or "") if w.strip()]
    return (not words) or any(w in cues for w in words)


def _download_ok(url):
    m = re.search(r"drive\.google\.com/(?:file/d/|open\?id=|uc\?(?:[^#]*&)?id=)([\w-]{20,})", url)
    if m:
        url = f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    elif not re.match(r"^[a-z]+://", url, re.I):
        p = url if os.path.isabs(url) else os.path.join(ROOT, url)
        return os.path.isfile(p), f"tệp {'có' if os.path.isfile(p) else 'KHÔNG có'}: {p}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
            raw = r.read(2 * 1024 * 1024)
    except Exception as ex:  # noqa: BLE001
        return False, str(ex)[:100]
    if raw[:8] == b"\x89PNG\r\n\x1a\n" or raw[:3] == b"\xff\xd8\xff" or (raw[:4] == b"RIFF" and raw[8:12] == b"WEBP"):
        return True, f"ảnh {len(raw) // 1024} KB"
    if re.search(rb'(?:og|twitter):image"?\s+content="([^"]+)', raw) or re.search(rb'content="([^"]+)"\s+(?:property|name)="(?:og|twitter):image"', raw):
        return True, "trang có og:image (Studio tải được)"
    return False, "không phải ảnh / trang ảnh"


def _kiem_canh_thuong(c, text, v, label=""):
    import gen_video as G
    """Kiểm tra một phần CẢNH thường (rút từ lỗi người dùng phản ánh 06/11/2026, canh-sat-gia-su-ai):
    - "Khung đầu từ cảnh" / "Mở đầu khung từ cảnh" phải trỏ tới một cảnh ĐỨNG TRƯỚC trong cùng phần;
    - từ 3 nhân vật: biến thể phải bật "nguoi_theo_canh" (không thì engine tả mọi người là "đang im lặng trong khung" và Muse vẽ thêm họ: cảnh sát thừa ở cửa sổ);
    - cảnh cận một người mà Prompt video nhắc tên người khác: Muse hay vẽ thêm người đó vào khung."""
    try:
        locks, scenes = G.parse_script(re.sub(r"^\[HAU KY\]:.*?(?=^\[|^CẢNH)", "", text, flags=re.M | re.S))
    except Exception as ex:  # noqa: BLE001
        c.w(f"{label}parse_script: {ex}")
        return
    nums = {s["n"] for s in scenes}
    if "{{LUOT_" in text:   # cảnh có lượt thoại mà Prompt video mất {{LUOT_n}} (06/11: công cụ sửa kịch bản ăn lấn câu, Muse không còn nhận câu thoại / hướng nhìn)
        for s in scenes:
            if "Prompt video" in s["f"] and "{{LUOT_" not in s["f"]["Prompt video"] and "{{LUOT_" in s["f"].get("Voice", ""):
                c.e(f"{label}cảnh {s['n']}: Voice có {{{{LUOT_n}}}} nhưng Prompt video không có (mất câu thoại trong lời dặn Muse)")
    for s in scenes:
        for fld in ("Khung đầu từ cảnh", "Mở đầu khung từ cảnh"):
            if fld in s["f"]:
                m = re.search(r"\d+", s["f"][fld])
                if not m or int(m.group(0)) not in nums or int(m.group(0)) >= s["n"]:
                    c.e(f"{label}cảnh {s['n']}: \"{fld}: {s['f'][fld]}\" phải là số của một cảnh ĐỨNG TRƯỚC trong cùng phần")
    chars = sorted({t[4:] for t in re.findall(r"\{\{\s*(TEN_[A-Z0-9]+)\s*\}\}", text)})
    if len(chars) >= 3 and not v.get("nguoi_theo_canh"):
        c.e(f"{label}{len(chars)} nhân vật ({', '.join(chars)}) mà biến thể [{v.get('name')}] chưa có \"nguoi_theo_canh\": true "
            "(engine sẽ tả mọi người là đang có mặt trong khung, Muse vẽ thêm họ vào cảnh cận / cửa sổ)")
    for s in scenes:
        img = s["f"].get("Prompt ảnh", "")
        if not re.search(r"CLOSE-UP|close shot|close-up", img, re.I):
            continue
        here = set(re.findall(r"\{\{\s*TEN_([A-Z0-9]+)\s*\}\}", img))
        vid = s["f"].get("Prompt video", "")
        other = sorted({k for k in chars if k not in here and re.search(r"\{\{\s*(TEN|NGUOI)_%s\s*\}\}" % k, vid)})
        if len(here) == 1 and other:
            c.w(f"{label}cảnh {s['n']} là cảnh cận {', '.join(here)} nhưng Prompt video nhắc {', '.join(other)}: Muse hay vẽ thêm người đó vào khung")


def _kiem_ghep(c, cfg, blocks, label=""):
    """Ghép 2 lớp: khối [NHAN VAT <nền>] phải nói rõ đầu nằm thấp, dưới các ô (06/11/2026: ô AI + phụ đề che mắt tài xế). Studio còn tự dò mặt và gen lại / dịch ảnh."""
    b = blocks.get(f"NHAN VAT {cfg['bg']}", "")
    bx, _, bw, _ = cfg["panels"].get(cfg["bg"], (0, 0, 1, 1))
    # chỉ tính ô CHỒNG lên khung nền theo bề ngang (chia đôi trái/phải như du-lich-chia-doi: không ô nào che mặt người nền)
    low = max((y + h for k, (x, y, w, h) in cfg["panels"].items() if k != cfg["bg"] and y < 0.5 and x < bx + bw - 1e-6 and x + w > bx + 1e-6), default=0)
    if low and not re.search(r"\d+\s*%|lower (?:half|two-thirds|middle)|head (?:is )?low", b, re.I):
        c.w(f"{label}[NHAN VAT {cfg['bg']}] chưa nói rõ đầu nằm dưới ô (ô che tới {low * 100:.0f}% + phụ đề): ghi \"the top of the hair at about "
            f"{(low + 0.1) * 100:.0f}% down from the top edge\"")


def cmd_kiem_tra(a):
    import engine as E
    import gen_video as G
    import make_variants as MV
    import prompt_parts as PP
    import split as SP
    try:
        import nhieu_phan as NP
    except Exception:  # noqa: BLE001
        NP = None
    c = Check()
    text = open(a.kich_ban, encoding="utf-8").read()
    try:
        variants = json.load(open(a.bien_the, encoding="utf-8"))
    except json.JSONDecodeError as ex:
        c.e(f"JSON không đọc được: {ex}"); return c
    if not isinstance(variants, list) or not variants:
        c.e("File biến thể phải là một MẢNG có ít nhất một biến thể"); return c
    c.o(f"JSON hợp lệ, {len(variants)} biến thể")
    cues = set(PP.EMO_CUES)
    names = [v.get("name") for v in variants]
    if len(set(names)) != len(names) or not all(names):
        c.e("Tên biến thể (name) thiếu hoặc trùng")
    for n in names:
        if n and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n):
            c.w(f'name "{n}" nên là chữ thường không dấu nối bằng "-"')

    multi = bool(re.search(r"^\s*=+\s*PHAN\s+\d+", text, re.M | re.I)) or bool(re.search(r"^\s*=+\s*PH[ẦA]N\s+\d+", text, re.M | re.I))
    hau_ky = re.search(r"^\[HAU KY\]:\s*\n\s*loai:\s*([\w-]+)", text, re.M)
    if hau_ky:
        mã = hau_ky.group(1)
        d = os.path.join(PROD, "types", mã)
        has = [f for f in ("gen.py", "post.py", "config.json") if os.path.exists(os.path.join(d, f))]
        (c.o if has else c.w)(f"[HAU KY] loai: {mã} → app/production/types/{mã}/ có: {', '.join(has) or 'KHÔNG CÓ GÌ (dùng gen/hậu kỳ chung)'}")
        if multi and "gen.py" not in has:
            c.e(f"Kịch bản nhiều phần cần app/production/types/{mã}/gen.py (5 dòng gọi _chung/nhieu_phan.run)")
    elif multi:
        c.e("Kịch bản nhiều phần nhưng thiếu khối [HAU KY] loai: <mã> (Studio không biết chạy gen.py riêng)")

    an = E.analyze_script(text)
    split = bool(an.get("split")) and not multi
    voiceover = "LUOT" not in an["series"] and not multi and not split
    mode = "nhiều phần" if multi else "ghép 2 lớp" if split else "lồng tiếng / cảnh không LUOT" if voiceover else "cảnh thường"
    c.o(f"Chế độ: {mode}; cảnh: {an['scenes']}; chuỗi: {an['series']}")

    # token của kịch bản (bỏ LUOT_n), có cả token lồng trong giá trị biến thể
    toks = {t for t in _tokens(text) if not re.fullmatch(r"LUOT_\d+", t)}
    series_toks = {f"{k}_{i}" for k, n in an["series"].items() if k != "LUOT" for i in range(1, n + 1)}
    toks -= series_toks
    plain = set(an["plain"]) - {t for t in an["plain"] if t.startswith("LUOT_")}
    # khoá mà Studio hiểu dù kịch bản không có token tương ứng (chèn vào câu lệnh người nói / đo miệng / hậu kỳ)
    engine_keys = re.compile(r"^(TEN|NGUOI|GIONG|POS|BOX|VAI|NGHE|NHIN|QUAY_LUNG|EMO)_[A-Z0-9]+$|^HAU_KY$")
    for v in variants:
        vk = {k.split("@")[0] for k in v if isinstance(k, str) and k.isupper() and k not in ("LUOT",)}
        vk |= set(an["series"]) - {"LUOT"}
        nested = {t for x in v.values() if isinstance(x, str) for t in _tokens(x)}
        missing = plain - vk - nested
        extra = {k for k in vk - plain - set(an["series"]) if not engine_keys.match(k)}
        if missing:
            c.e(f'[{v.get("name")}] thiếu token của kịch bản: {", ".join(sorted(missing))}')
        # chỉ có khoá "<TOKEN>@<phần>" mà không có khoá gốc: nút "Thêm vào hàng đợi" của Studio chỉ kiểm khoá gốc → báo "chưa điền" (du-lich-chia-doi 06/11)
        only_at = {k for k in vk & plain if k not in v and k not in ("POS_DAY", "POS_HOC")}
        if only_at:
            c.e(f'[{v.get("name")}] chỉ có khoá "@phần", thiếu khoá gốc (Studio báo "chưa điền"): {", ".join(sorted(only_at))}')
        if extra:
            c.w(f'[{v.get("name")}] khoá không có trong kịch bản (Studio bỏ qua): {", ".join(sorted(extra))}')
        grp = {}
        for k in v:
            m = re.fullmatch(r"([A-Z][A-Z0-9_]*?)_(\d+)", k) if isinstance(k, str) else None
            if m and k not in series_toks:
                grp.setdefault(m.group(1), []).append(int(m.group(2)))
        for pre, ns in grp.items():
            if sorted(ns) == list(range(1, len(ns) + 1)) and len(ns) >= 2:
                c.w(f'[{v.get("name")}] các khoá {pre}_1..{pre}_{len(ns)} đánh số liên tiếp: Studio coi là chuỗi, không hiện thành trường riêng')
    if not any(e.startswith("[") and "thiếu token" in e for e in c.err):
        c.o("Mọi biến thể đủ token của kịch bản")

    # lượt thoại
    for v in variants:
        luot = [t for t in v.get("LUOT", []) if str(t.get("text", "")).strip()]
        nm = v.get("name")
        if voiceover:
            if luot:
                c.w(f"[{nm}] kịch bản không có {{{{LUOT_n}}}} nhưng biến thể có {len(luot)} lượt (Studio bỏ qua)")
            continue
        if not split and not multi and len(luot) != an["scenes"]:
            c.w(f"[{nm}] {len(luot)} lượt nhưng kịch bản có {an['scenes']} cảnh " + ("(Studio nhân bản cảnh cuối cho đủ)" if len(luot) > an["scenes"] else "(Studio chỉ chạy các cảnh có lượt, bỏ cảnh cuối)"))
        chars = set(MV.chars_of({k: x for k, x in v.items() if "@" not in str(k)}))
        for i, t in enumerate(luot, 1):
            who = MV.ck(t.get("who"))
            if who not in chars:
                c.e(f'[{nm}] lượt {i}: who "{t.get("who")}" không có nhân vật (TEN_{who}) trong biến thể; có: {", ".join(sorted(chars))}')
            n = len(str(t["text"]).split())
            if n > 20:
                c.w(f"[{nm}] lượt {i}: {n} từ (> 20): tách hai lượt cùng người")
            if not _emo_ok(t.get("emo", ""), cues):
                c.w(f'[{nm}] lượt {i}: emo "{t.get("emo")}" không có từ nào trong EMO_CUES ({", ".join(sorted(cues)[:8])}…)')
            if t.get("fx") not in (None, "none", "wrong", "right", "ding"):
                c.e(f'[{nm}] lượt {i}: fx "{t.get("fx")}" lạ')
        fx = [(i, t.get("fx")) for i, t in enumerate(luot, 1) if t.get("fx") in ("wrong", "right")]
        if fx:
            seq = [f for _, f in fx]
            if seq.count("wrong") != seq.count("right") or any(seq[i] == seq[i + 1] for i in range(len(seq) - 1)):
                c.w(f"[{nm}] fx: {', '.join(f'{i}:{f}' for i, f in fx)} (mong đợi từng cặp wrong → right)")
            else:
                c.o(f"[{nm}] {len(fx) // 2} cặp wrong → right ở lượt {', '.join(str(i) for i, _ in fx)}")
        elif not multi and not split and all(t.get("fx") is None for t in luot) and {"DAY", "HOC"} <= chars:
            c.w(f"[{nm}] không lượt nào có fx: Studio tự thêm viền đỏ/xanh theo day/hoc; nếu video không có nhịp sửa lỗi hãy đặt \"fx\": \"none\" ở mọi lượt")

    # chế độ riêng
    if split:
        try:
            cfg, blocks = SP.parse(text)
            for k, (x, y, w, h) in cfg["panels"].items():
                c.o(f"khung {k}: x {x}, y {y}, rộng {w}, cao {h} = {int(w * 720)}x{int(h * 1280)} px (720x1280) → gen {SP.aspect_of(cfg, k)}")
            for k in {cfg["bg"], *cfg["panels"]}:
                if f"NHAN VAT {k}" not in blocks:
                    c.e(f"thiếu khối [NHAN VAT {k}]")
            for k, b in blocks.items():
                if k.startswith("NGHE ") and re.search(r"\b(talk|speak|speaker|mirror|voice|word)", b, re.I):
                    hits = ", ".join(sorted(set(m.lower() for m in re.findall(r"\b(talk\w*|speak\w*|mirror\w*|voice|words?)", b, re.I))))
                    c.w(f"[{k}] nhắc tới nói/giọng/người nói ({hits}) → Muse hay lồng tiếng vào clip nghe; chỉ tả điều NÊN làm")
            c.o(f"[GHEP HAI LOP] đọc được: nền {cfg['bg']}, nối {cfg['join'][0]}, nghe {cfg['listen'][0]}")
            _kiem_ghep(c, cfg, blocks)
        except RuntimeError as ex:
            c.e(f"[GHEP HAI LOP]: {ex}")
    if multi:
        if NP is None:
            c.e("không import được nhieu_phan.py")
        else:
            for v in variants:
                try:
                    parts, scenes = NP.plan(v, text)
                    c.o(f"[{v.get('name')}] nhieu_phan.plan: {len(parts)} phần, {len(scenes)} cảnh chung (" + ", ".join(f"P{p['n']}: {p['count']} cảnh, {'ghép 2 lớp' if p['split'] else 'cảnh thường'}" for p in parts) + ")")
                    for p in parts:
                        sv = NP.sub_variant(v, NP.part_chars(p["text"], p["turns"]), p["turns"], p["n"])
                        filled = G.fill_tokens(p["text"], E.variant_values(sv))
                        left = sorted(set(_tokens(filled)) - {f"LUOT_{i}" for i in range(1, 60)})
                        if left:
                            c.e(f"[{v.get('name')}] phần {p['n']} sau khi điền còn token: {', '.join(left)}")
                        if p["split"]:
                            cfg, blocks = SP.parse(p["text"])
                            for k, (x, y, w, h) in cfg["panels"].items():
                                c.o(f"phần {p['n']} khung {k}: {int(w * 720)}x{int(h * 1280)} px → gen {SP.aspect_of(cfg, k)}")
                            for k, b in blocks.items():
                                if k.startswith("NGHE ") and re.search(r"\b(talk|speak|speaker|mirror|voice|word)", b, re.I):
                                    c.w(f"phần {p['n']} [{k}] nhắc tới nói/người nói → Muse hay lồng tiếng vào clip nghe")
                            if v is variants[0]:
                                _kiem_ghep(c, cfg, blocks, f"phần {p['n']} ")
                        else:
                            _kiem_canh_thuong(c, p["text"], v, f"phần {p['n']} ")
                except Exception as ex:  # noqa: BLE001
                    c.e(f"[{v.get('name')}] nhieu_phan.plan: {ex}")
    if not multi:
        for v in variants:
            try:
                tpl, n_real = E.expand_script(text, len(v.get("LUOT", []))), len(v.get("LUOT", []))
                want = E.analyze_script(tpl)["series"].get("LUOT")
                vv = v
                if want and 0 < n_real < want:   # Studio bù lượt trống cho đủ token rồi chỉ chạy n_real cảnh đầu
                    pad_who = (MV.chars_of(v) or ["DAY"])[0].lower()
                    vv = dict(v, LUOT=list(v["LUOT"]) + [{"who": pad_who, "text": "", "emo": ""}] * (want - n_real))
                filled = G.fill_tokens(tpl, E.variant_values(vv))
                left = sorted(set(_tokens(filled)) - {f"LUOT_{i}" for i in range(1, 60)})
                if left:
                    c.e(f"[{v.get('name')}] sau khi điền còn token: {', '.join(left)}")
            except SystemExit as ex:
                c.e(f"[{v.get('name')}] variant_values: {ex}")
            except Exception as ex:  # noqa: BLE001
                c.e(f"[{v.get('name')}] điền token lỗi: {ex}")
        if not split and an["scenes"]:
            try:
                locks, scenes = G.parse_script(re.sub(r"^\[HAU KY\]:.*?(?=^\[|^CẢNH)", "", text, flags=re.M | re.S))
                lock_words = sum(len(b.split()) for b in locks.values())
                (c.w if lock_words > 900 else c.o)(f"khối khoá {lock_words} từ (khuyên ≤ ~600; >1000 Muse quên ngữ cảnh)")
                no_img = [s["n"] for s in scenes if s["n"] == 1 and "Prompt ảnh" not in s["f"]]
                if no_img:
                    c.e("cảnh 1 không có Prompt ảnh")
                caps = [s["n"] for s in scenes if re.search(r"\b(TOP|BOTTOM|LEFT|RIGHT)\b", s["f"].get("Prompt video", "")) and not re.search(r"\b(TOP|BOTTOM|LEFT|RIGHT)\b", locks.get("NEGATIVE", ""))]
                if caps:
                    c.w(f"từ vị trí viết hoa trong Prompt video (cảnh {caps[:5]}) mà [NEGATIVE] không cấm chữ: Muse từng vẽ thành chữ")
                for s in scenes:
                    f = s["f"]
                    if "Ảnh tổng quan" in f and "Khung đầu cắt" not in f:
                        c.w(f"cảnh {s['n']} có Ảnh tổng quan nhưng thiếu Khung đầu cắt")
                    if "Lia nhanh" in f and "Giữ sau lời" not in f:
                        c.w(f"cảnh {s['n']} có Lia nhanh nhưng thiếu Giữ sau lời (cú lia sau lời sẽ bị cắt)")
                    if "CAMERA MOVE" in f.get("Prompt video", "") and "CAMERA MOVE" not in " ".join(locks.values()):
                        c.w(f"cảnh {s['n']} tả CAMERA MOVE nhưng khoá chung không cho phép (\"still unless the clip describes a CAMERA MOVE\")")
                for v in variants:
                    _kiem_canh_thuong(c, text, v)
            except Exception as ex:  # noqa: BLE001
                c.w(f"parse_script: {ex}")
    # refs
    for v in variants:
        refs = v.get("refs")
        if refs is None:
            continue
        if not isinstance(refs, dict):
            c.e(f"[{v.get('name')}] refs phải là object {{TOKEN: [link]}}"); continue
        for k, items in refs.items():
            if isinstance(items, (str, dict)):
                items = [items]
            for it in items or []:
                url = it if isinstance(it, str) else it.get("url", "")
                if a.tai_anh:
                    ok, msg = _download_ok(url)
                    (c.o if ok else c.e)(f"[{v.get('name')}] refs.{k}: {msg} ({url[:70]})")
                elif not url:
                    c.e(f"[{v.get('name')}] refs.{k} thiếu url")
    if any(isinstance(v.get("refs"), dict) for v in variants) and not a.tai_anh:
        c.o("có refs (chưa tải thử; thêm --tai-anh để kiểm tra link)")
    print(f"\nTổng: {len(c.err)} lỗi, {len(c.warn)} cảnh báo, {len(c.ok)} mục đạt.")
    print("Tiếp theo: chạy thử MỘT biến thể, xem scene1_start.png / scene<n>_start.png (cảnh đổi góc) / scene1_wide.png / base_<K>.png rồi mới chạy cả nhóm.")
    return c


# ============================================================================ nhap

def _studio_url():
    rj = os.path.join(ROOT, "userdata", "running.json")
    if not os.path.exists(rj):
        sys.exit("Studio chưa chạy (không có userdata/running.json). Mở LUO Studio.bat rồi chạy lại.")
    url = json.load(open(rj, encoding="utf-8")).get("studio_url", "").rstrip("/")
    try:
        with urllib.request.urlopen(url + "/api/health", timeout=5) as r:
            r.read()
    except Exception as ex:  # noqa: BLE001
        sys.exit(f"Không kết nối được Studio ở {url} ({ex}). Mở LUO Studio rồi chạy lại.")
    return url


def _api(url, method, path, body=None):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as ex:
        raise SystemExit(f"{method} {path} → {ex.code}: {ex.read().decode('utf-8', 'replace')[:400]}")


def cmd_nhap(a):
    text = open(a.kich_ban, encoding="utf-8").read()
    variants = json.load(open(a.bien_the, encoding="utf-8"))
    ten_loai = a.ten_loai or os.path.splitext(os.path.basename(a.kich_ban))[0]
    ten_du_an = a.ten_du_an or ten_loai
    print(f"Loại dự án: \"{ten_loai}\" ({len(text)} ký tự)  |  Dự án: \"{ten_du_an}\" ({len(variants)} biến thể: {', '.join(v.get('name', '?') for v in variants[:6])}{'…' if len(variants) > 6 else ''})")
    if a.thu:
        print("(--thu: không gọi API)"); return
    url = _studio_url()
    print(f"Studio: {url}")
    if a.loai:
        tid = a.loai
        print(f"Dùng loại dự án có sẵn: {tid}")
    else:
        t = _api(url, "POST", "/api/types", {"name": ten_loai, "script": text})
        if t.get("error"):
            sys.exit("Studio từ chối kịch bản: " + t["error"])
        tid = t["id"]
        print(f"Đã tạo loại dự án {tid}: {t.get('scenes')} cảnh, {len(t.get('fields', []))} trường" + (", ghép 2 lớp" if t.get("split") else ""))
        print("  Trường: " + ", ".join(f["key"] for f in t.get("fields", [])))
    p = _api(url, "POST", "/api/projects", {"name": ten_du_an, "template": tid, "variants": variants})
    pid = p["id"]
    print(f"Đã tạo dự án {pid} với {len(p.get('variants', []))} biến thể.")
    bad = [(v["name"], k, it.get("error")) for v in p.get("variants", []) for k, items in (v.get("refs") or {}).items() for it in (items if isinstance(items, list) else [items]) if isinstance(it, dict) and it.get("error")]
    for name, k, err in bad:
        print(f"  Ảnh refs lỗi [{name}] {k}: {err}")
    print(f"Mở: {url}/#project={pid}  (chọn Thương hiệu: logo / video giới thiệu / outro trong trang dự án)")
    if a.chay_thu:
        first = variants[0]["name"]
        q = _api(url, "POST", "/api/queue/add", {"project": pid, "variants": [first]})
        _api(url, "POST", "/api/queue/start", {"ids": q.get("ids", [])})
        print(f"Đã thêm và bắt đầu chạy thử biến thể \"{first}\" (hàng đợi {q.get('ids')}). Xem thẻ video trong Studio; kiểm tra scene1_start.png / base_<K>.png trước khi chạy cả nhóm.")
    else:
        print("Chưa gen. Trong Studio: tick MỘT biến thể → Thêm vào hàng đợi → Bắt đầu; hoặc chạy lại với --chay-thu.")


# ============================================================================ main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("danh-gia", help="đo mặt, máy quay, cao độ giọng và gợi ý khuôn")
    d.add_argument("src"); d.add_argument("--lang", default="en"); d.add_argument("--model", default="small")
    k = sub.add_parser("kiem-tra", help="kiểm tra kịch bản + biến thể bằng code Studio")
    k.add_argument("kich_ban"); k.add_argument("bien_the"); k.add_argument("--tai-anh", action="store_true")
    n = sub.add_parser("nhap", help="nhập loại dự án + dự án vào Studio đang chạy")
    n.add_argument("kich_ban"); n.add_argument("bien_the"); n.add_argument("--ten-loai"); n.add_argument("--ten-du-an")
    n.add_argument("--loai", help="id loại dự án có sẵn (không tạo loại mới)")
    n.add_argument("--chay-thu", action="store_true"); n.add_argument("--thu", action="store_true")
    a = ap.parse_args()
    if a.cmd == "danh-gia":
        cmd_danh_gia(a)
    elif a.cmd == "kiem-tra":
        c = cmd_kiem_tra(a)
        sys.exit(1 if c.err else 0)
    else:
        cmd_nhap(a)


if __name__ == "__main__":
    main()
