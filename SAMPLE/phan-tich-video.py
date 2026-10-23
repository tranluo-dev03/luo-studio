#!/usr/bin/env python
"""Phân tích video tham chiếu thành bộ dữ liệu để viết kịch bản KHÔNG bỏ sót hành động và tốc độ nói.

Chạy (dùng Python đi kèm Studio, đã có ffmpeg và faster-whisper):
    runtime\\python.exe SAMPLE\\phan-tich-video.py "duong\\dan\\video.mp4" [thu-muc-ra] [--lang en] [--model small]

Sinh ra trong thư mục ra (mặc định: <tên video>-phan-tich/):
    bao-cao.md        bảng các lượt nói (thời điểm, lời, số từ/giây, khoảng lặng), cảnh cắt, các khoảnh khắc chuyển động mạnh
    bao-cao.json      cùng dữ liệu ở dạng máy đọc
    tong-quan_N.jpg   ảnh ghép toàn video, 1 khung/giây (có số giây trên từng ô)
    luot_NN.jpg       ảnh ghép dày (4 khung/giây) cho TỪNG lượt nói + 0,3s trước và 0,5s sau
    chuyen-dong_NN.jpg  ảnh ghép dày quanh mỗi khoảnh khắc chuyển động mạnh (thường là lúc có hành động: đưa đồ, giơ tay, quay người)

Agent PHẢI xem từng ảnh luot_NN.jpg và chuyen-dong_NN.jpg rồi điền "bảng hành động" (xem HUONG-DAN-CHO-AGENT.md, mục 0).
"""
import argparse, json, os, re, subprocess, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(os.path.dirname(HERE), "bin")
FFMPEG = os.path.join(BIN, "ffmpeg.exe") if os.path.exists(os.path.join(BIN, "ffmpeg.exe")) else "ffmpeg"
FFPROBE = os.path.join(BIN, "ffprobe.exe") if os.path.exists(os.path.join(BIN, "ffprobe.exe")) else "ffprobe"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    if r.returncode:
        raise RuntimeError(f"{cmd[0]} lỗi: {r.stderr.decode('utf-8', 'replace')[-400:]}")
    return r


def duration(path):
    return float(run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout)


def sheet(video, out, t0, dur, fps, cols=6, w=240, stamp=True):
    """Ảnh ghép các khung hình trong [t0, t0+dur] với `fps` khung/giây; mỗi ô ghi số giây trong video gốc."""
    n = max(1, int(dur * fps + 0.5))
    rows = (n + cols - 1) // cols
    vf = f"fps={fps},scale={w}:-1"
    if stamp:
        vf += f",drawtext=text='%{{pts\\:hms\\:{t0:.2f}}}':x=4:y=4:fontsize=14:fontcolor=white:box=1:boxcolor=black@0.6"
    vf += f",tile={cols}x{rows}"
    try:
        run([FFMPEG, "-v", "error", "-y", "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", video, "-vf", vf, "-frames:v", "1", out])
    except RuntimeError:   # drawtext thiếu phông trên một số bản ffmpeg: bỏ nhãn thời gian
        run([FFMPEG, "-v", "error", "-y", "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", video, "-vf", f"fps={fps},scale={w}:-1,tile={cols}x{rows}", "-frames:v", "1", out])


def transcribe(video, tmp, lang, model):
    wav = os.path.join(tmp, "audio.wav")
    run([FFMPEG, "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav])
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language=lang or None, word_timestamps=True, vad_filter=False)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words if w.word.strip()]


def turns_from_words(words, gap=0.45, sentence_gap=0.08):
    """Gộp từ thành lượt nói. Ngắt khi (a) khoảng lặng giữa hai từ >= `gap`, hoặc (b) từ trước kết thúc câu (. ? !) và có khoảng hở >= `sentence_gap`.
    Video hội thoại thường gần như không có khoảng lặng giữa các người nói nên cần cả (b). Mỗi dòng là MỘT CÂU: agent ghép các câu liền nhau của cùng một người thành một lượt. Số từ/giây tính từ từ đầu đến từ cuối của câu."""
    turns, cur = [], []
    for w in words:
        if cur:
            g = w[1] - cur[-1][2]
            if g >= gap or (re.search(r"[.?!]$", cur[-1][0]) and g >= sentence_gap):
                turns.append(cur); cur = []
        cur.append(w)
    if cur:
        turns.append(cur)
    out = []
    for i, t in enumerate(turns):
        t0, t1 = t[0][1], t[-1][2]
        out.append({"n": i + 1, "start": round(t0, 2), "end": round(t1, 2), "text": " ".join(x[0] for x in t),
                    "words": len(t), "wps": round(len(t) / max(0.3, t1 - t0), 2),
                    "gap_before": round(t0 - (turns[i - 1][-1][2] if i else 0.0), 2)})
    return out


def scene_cuts(video, thr=0.30):
    r = run([FFMPEG, "-hide_banner", "-i", video, "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"])
    return [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", r.stderr.decode("utf-8", "replace"))]


def motion_peaks(video, total, fps=8, w=90, h=160):
    """Các khoảnh khắc chuyển động mạnh (đưa đồ vật, giơ tay, quay người...): trả về [(giây bắt đầu, giây kết thúc, mức)]. Cảnh cắt cứng cũng tạo đỉnh nên đối chiếu với danh sách cảnh cắt."""
    d = run([FFMPEG, "-v", "error", "-i", video, "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"]).stdout
    n = len(d) // (w * h)
    if n < 4:
        return []
    a = np.frombuffer(d[: n * w * h], np.uint8).reshape(n, h, w).astype(np.float32)
    e = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    k = max(1, fps // 2)
    sm = np.convolve(e, np.ones(k) / k, mode="same")
    thr = float(np.median(sm) + 0.7 * sm.std())
    peaks, i = [], 0
    while i < len(sm):
        if sm[i] > thr:
            j = i
            while j + 1 < len(sm) and sm[j + 1] > thr:
                j += 1
            peaks.append((round(i / fps, 2), round((j + 1) / fps, 2), round(float(sm[i:j + 1].max()), 1)))
            i = j + 1
        else:
            i += 1
    return peaks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--model", default="small")
    ap.add_argument("--max-peaks", type=int, default=12)
    a = ap.parse_args()
    video = os.path.abspath(a.video)
    out = a.out or os.path.splitext(video)[0] + "-phan-tich"
    os.makedirs(out, exist_ok=True)
    total = duration(video)
    print(f"Video {total:.1f}s. Đang nhận dạng giọng (lần đầu có thể tải mô hình)...")
    words = transcribe(video, out, a.lang, a.model)
    turns = turns_from_words(words)
    cuts = scene_cuts(video)
    peaks = motion_peaks(video, total)
    peaks = sorted(peaks, key=lambda p: -p[2])[: a.max_peaks]
    peaks.sort()

    # ảnh ghép
    per = 24
    for i in range(0, int(total) + 1, per):
        sheet(video, os.path.join(out, f"tong-quan_{i // per + 1}.jpg"), i, min(per, total - i), 1, cols=6, w=200)
    for t in turns:
        t0 = max(0.0, t["start"] - 0.3)
        d = min(total - t0, t["end"] - t["start"] + 0.8)
        fps = 4 if d * 4 <= 12 else max(1.0, 12 / d)
        sheet(video, os.path.join(out, f"luot_{t['n']:02d}.jpg"), t0, d, fps, cols=6, w=240)
    for i, (p0, p1, lvl) in enumerate(peaks, 1):
        t0 = max(0.0, p0 - 0.4)
        d = min(total - t0, max(1.5, p1 - p0 + 0.8), 4.0)
        sheet(video, os.path.join(out, f"chuyen-dong_{i:02d}.jpg"), t0, d, 4, cols=6, w=240)

    wps = [t["wps"] for t in turns if t["words"] >= 4]
    stats = {"duration": round(total, 1), "turns": len(turns), "median_wps": round(float(np.median(wps)), 2) if wps else None,
             "max_wps": max(wps) if wps else None, "median_gap": round(float(np.median([t["gap_before"] for t in turns[1:]])), 2) if len(turns) > 1 else None}
    json.dump({"stats": stats, "turns": turns, "cuts": cuts, "motion": peaks}, open(os.path.join(out, "bao-cao.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    md = [f"# Báo cáo phân tích: {os.path.basename(video)}", "",
          f"- Độ dài {stats['duration']}s, {stats['turns']} câu nói (liền nhau cùng một người thì ghép thành một lượt). **Tốc độ nói trung vị: {stats['median_wps']} từ/giây** (cao nhất {stats['max_wps']}). Khoảng lặng giữa các lượt (trung vị): {stats['median_gap']}s.",
          f"- Cảnh cắt cứng (giây): {cuts or 'không có'}",
          "- Tốc độ này đưa vào kịch bản (ví dụ \"about N words per second\") và dùng để chọn độ dài clip; Muse thường nói chậm hơn video gốc.", "",
          "## Các lượt nói", "", "| # (câu) | Bắt đầu–kết thúc | Từ/giây | Lặng trước | Ai nói | Lời | Ảnh |", "|---|---|---|---|---|---|---|"]
    for t in turns:
        md.append(f"| {t['n']} | {t['start']}–{t['end']}s | {t['wps']} | {t['gap_before']}s | ? (điền) | {t['text']} | luot_{t['n']:02d}.jpg |")
    md += ["", "## Khoảnh khắc chuyển động mạnh (thường là lúc có hành động hoặc cảnh cắt)", "", "| Giây | Mức | Ảnh |", "|---|---|---|"]
    for i, (p0, p1, lvl) in enumerate(peaks, 1):
        md.append(f"| {p0}–{p1} | {lvl} | chuyen-dong_{i:02d}.jpg |")
    md += ["", "## Việc bắt buộc tiếp theo", "",
           "1. Xem TỪNG ảnh `luot_NN.jpg` và `chuyen-dong_NN.jpg` (và `tong-quan_N.jpg`).",
           "2. Điền **bảng hành động** theo từng lượt: ai nói; hành động của người nói; phản ứng/hành động của người nghe; vật dụng xuất hiện, đổi tay, biến mất; ánh mắt hướng đâu; cử động camera; trạng thái KHUNG CUỐI của lượt (tay ở đâu, ai cầm gì).",
           "3. Mọi hành động và vật dụng trong bảng phải có chỗ trong kịch bản (Diễn biến, Khung cuối, token đạo cụ). Hành động phải xảy ra TRONG lúc nói (Studio cắt clip ngay sau từ cuối).",
           "4. Mọi khoảnh khắc chuyển động mạnh trong bảng trên phải được giải thích (hành động nào, hay chỉ là cảnh cắt/chuyển cảnh)."]
    open(os.path.join(out, "bao-cao.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"Xong: {out}\n  {stats}")


if __name__ == "__main__":
    main()
