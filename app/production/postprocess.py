#!/usr/bin/env python
"""Hậu kỳ video "split dialogue": cắt khoảng lặng dài, sinh phụ đề .ass theo audio thật (Whisper),
đóng thanh logo góc trên trái, thêm icon, nối end card.

  python postprocess.py RAW.mp4 --subs subs/langlearn.json [--out final.mp4] [--no-tighten] [--no-endcard] [--subs-only]

Cần: ffmpeg trong PATH, `pip install faster-whisper` (model small.en tải lần đầu).
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys, tempfile, time

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
COLORS = {"white": "FFFFFF", "red": "2A2AFF", "green": "5ACB3C", "yellow": "00D8FF"}  # ASS dùng BGR


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode:
        sys.exit("LỖI: " + " ".join(cmd[:3]) + "...\n" + r.stderr[-1500:])
    return r


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout)


def silences(path, noise="-35dB", dmin=0.8):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={noise}:d={dmin}", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    total = duration(path)
    return [(s, ends[i] if i < len(ends) else total) for i, s in enumerate(starts)]


def tighten(src, dst, settle=0.5, lead=0.12):
    """Cắt đoạn lặng dài (đuôi đứng im của mỗi clip + phần đầu clip sau trước khi nói).
    Giữ `settle` giây sau khi hết lời (để nhân vật về tư thế nghỉ) và `lead` giây trước câu kế tiếp.
    Vì prompt bắt nhân vật nói xong thì ĐỨNG IM như ảnh tĩnh, điểm cắt rơi vào đoạn tĩnh nên nối liền mạch."""
    total = duration(src)
    cuts = [(s + settle, e - lead) for s, e in silences(src) if e - s > settle + lead + 0.1]
    if not cuts:
        shutil.copy(src, dst)
        return total
    segs, t = [], 0.0
    for a, b in cuts:
        segs.append((t, a))
        t = b
    segs.append((t, total))
    parts, labels = [], ""
    for i, (a, b) in enumerate(segs):
        parts.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]")
        labels += f"[v{i}][a{i}]"
    fc = ";".join(parts) + f";{labels}concat=n={len(segs)}:v=1:a=1[v][a]"
    run(["ffmpeg", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17",
         "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", dst])
    return duration(dst)


def _whisper_child(wav, model_name, prompt_file, vad, compute, out_json):
    """Chạy trong tiến trình con: nhận dạng giọng rồi ghi các từ (từ, bắt đầu, kết thúc) ra file JSON."""
    from faster_whisper import WhisperModel
    prompt = open(prompt_file, encoding="utf-8").read() or None
    model = WhisperModel(model_name, device="cpu", compute_type=compute)
    segs, _ = model.transcribe(wav, word_timestamps=True, language="en" if model_name.endswith(".en") else None, initial_prompt=prompt,
                               condition_on_previous_text=False, vad_filter=vad)
    json.dump([(w.word, w.start, w.end) for s in segs for w in s.words], open(out_json, "w", encoding="utf-8"))


def _whisper_cmd(wav, model_name, prompt_file, vad, compute, out_json):
    # -I: tách khỏi môi trường người dùng; -W: bỏ cảnh báo pkg_resources của ctranslate2 (vô hại nhưng làm nhật ký rối)
    return [sys.executable, "-I", "-W", "ignore:pkg_resources:UserWarning", os.path.abspath(__file__), "--_whisper",
            wav, model_name, prompt_file, "1" if vad else "0", compute, out_json]


def _transcribe_isolated(wav, model_name, prompt, vad, compute):
    """Whisper trong tiến trình riêng: nếu thư viện native (ctranslate2, onnxruntime) hỏng cứng (segfault, mã 0xC0000005) thì chỉ tiến trình con chết,
    Hậu kỳ vẫn chạy tiếp. Trả về (danh sách từ hoặc None, có phải hỏng cứng không)."""
    prompt_file, out_json = wav + ".prompt.txt", wav + ".words.json"
    open(prompt_file, "w", encoding="utf-8").write(prompt or "")
    crashed = False
    try:
        r = subprocess.run(_whisper_cmd(wav, model_name, prompt_file, vad, compute, out_json), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=3600)
        if r.returncode == 0 and os.path.exists(out_json):
            return [tuple(w) for w in json.load(open(out_json, encoding="utf-8"))], False
        code = r.returncode & 0xFFFFFFFF
        crashed = r.returncode < 0 or code >= 0xC0000000   # Windows: 0xC0000005 (access violation)...; POSIX: tín hiệu (mã âm)
        tail = [l for l in (r.stderr or "").splitlines() if l.strip() and "pkg_resources" not in l][-3:]
        print(f"  Nhận dạng giọng lỗi (compute={compute}, VAD={'bật' if vad else 'tắt'}, mã thoát 0x{code:08X})" + ("; " + " | ".join(tail) if tail else ""))
    except subprocess.TimeoutExpired:
        print(f"  Nhận dạng giọng quá thời gian (compute={compute}); bỏ qua.")
    finally:
        for f in (prompt_file, out_json):
            try:
                os.remove(f)
            except OSError:
                pass
    return None, crashed


_VAD_MARK = os.path.join(tempfile.gettempdir(), "luo-studio-vad-crashed")   # đánh dấu "máy này VAD hỏng cứng" để các lần sau khỏi thử lại (hết hạn sau 30 ngày)


def _vad_known_bad():
    try:
        return time.time() - os.path.getmtime(_VAD_MARK) < 30 * 86400
    except OSError:
        return False


def transcribe(path, model_name="small.en", prompt=None, vad=True):
    """Danh sách từ (từ, bắt đầu, kết thúc) của audio trong `path`, hoặc None nếu máy này không chạy được Whisper.
    vad=True: thử có lọc VAD trước (căn phụ đề dòng đầu chuẩn hơn); VAD dùng onnxruntime, một engine riêng, và đã gây crash cứng trên một số máy,
    nên chỉ chạy trong tiến trình con và nếu hỏng thì tự chuyển sang không VAD (rồi nhớ lại để lần sau bỏ qua VAD)."""
    wav = path + ".wav"
    run(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
    try:
        attempts = ([(True, "int8")] if vad and not _vad_known_bad() else []) + [(False, "int8"), (False, "float32")]   # float32: phòng khi CPU không hỗ trợ int8 đúng
        for use_vad, compute in attempts:
            words, crashed = _transcribe_isolated(wav, model_name, prompt, use_vad, compute)
            if words is not None:
                return words
            if use_vad and crashed:
                try:
                    open(_VAD_MARK, "w").write(time.strftime("%Y-%m-%d %H:%M:%S"))
                except OSError:
                    pass
                print("  VAD hỏng trên máy này; chuyển sang nhận dạng không VAD (các lần Hậu kỳ sau sẽ bỏ qua VAD).")
        return None
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass


def estimate_words(path, units):
    """Phương án cuối khi không nhận dạng được giọng: rải đều các từ của phụ đề theo độ dài chữ trên toàn video, để Hậu kỳ vẫn ra video (thời điểm phụ đề chỉ là ước lượng)."""
    total = max(1.0, duration(path))
    toks = [(t, len(t) + 1) for u in units for t in u["t"].split()]
    wsum = sum(w for _, w in toks) or 1
    out, t0 = [], 0.2
    span = max(0.5, total - 0.6)
    for t, w in toks:
        d = span * w / wsum
        out.append((t, t0, t0 + d * 0.9))
        t0 += d
    return out


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def align(units, words, window=7):
    """Gán (start, end) cho từng đơn vị phụ đề bằng cách khớp mờ tuần tự với các từ Whisper."""
    toks = [(norm(w), s, e) for w, s, e in words if norm(w)]
    p = 0
    for u in units:
        first = last = None
        for tk in [norm(x) for x in u["t"].split() if norm(x)]:
            best = None
            for j in range(p, min(p + window, len(toks))):
                r = difflib.SequenceMatcher(None, tk, toks[j][0]).ratio()
                if r >= 0.6 and (best is None or r > best[0] + 0.15):
                    best = (r, j)
                    if r > 0.9:
                        break
            if best:
                j = best[1]
                first = toks[j][1] if first is None else first
                last = toks[j][2]
                p = j + 1
        u["s"], u["e"] = first, last
        u["ok"] = first is not None
    # đơn vị không khớp: chia đều khoảng trống giữa hai đơn vị khớp lân cận
    n = len(units)
    i = 0
    while i < n:
        if units[i]["s"] is None:
            j = i
            while j < n and units[j]["s"] is None:
                j += 1
            lo = units[i - 1]["e"] if i > 0 else 0.0
            hi = units[j]["s"] if j < n else (toks[-1][2] if toks else lo + 1)
            step = max(0.2, (hi - lo) / (j - i + 1))
            for k in range(i, j):
                units[k]["s"] = lo + step * (k - i) + 0.05
                units[k]["e"] = lo + step * (k - i + 1)
            i = j
        else:
            i += 1
    # kéo dài mỗi phụ đề tới ngay trước phụ đề kế (tối đa +0.35s)
    for i, u in enumerate(units):
        nxt = units[i + 1]["s"] if i + 1 < n else u["e"] + 0.5
        u["e"] = max(u["e"], min(nxt - 0.02, u["e"] + 0.35))
    return units


_FONTS = {}


def text_width(s, size, font="Arial"):
    """Độ rộng (px) của chuỗi ở cỡ chữ `size`, in đậm. Dùng Pillow nếu có, không thì ước lượng."""
    try:
        from PIL import ImageFont
        key = (font, size)
        if key not in _FONTS:
            cand = [r"C:\Windows\Fonts\arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
            _FONTS[key] = ImageFont.truetype(next(p for p in cand if os.path.exists(p)), size)
        return _FONTS[key].getlength(s) + 7 * 2 * 1.0  # + viền
    except Exception:
        return len(s) * size * 0.60


def fit_caption(text, size=84, min_size=44, max_w=930, max_lines=4, font="Arial"):
    """Chia dòng cân bằng (tối đa max_lines) và co cỡ chữ để không dòng nào vượt max_w. Trả (text có \\N, cỡ chữ)."""
    words = text.split()
    if not words:
        return text, size
    best = None
    for k in range(1, min(max_lines, len(words)) + 1):
        # quy hoạch động: chia k dòng sao cho dòng rộng nhất nhỏ nhất
        n = len(words)
        w = lambda i, j: text_width(" ".join(words[i:j]), 100, font)
        INF = 1e18
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        cut = [[0] * (n + 1) for _ in range(k + 1)]
        dp[0][0] = 0
        for r in range(1, k + 1):
            for j in range(r, n + 1):
                for i in range(r - 1, j):
                    c = max(dp[r - 1][i], w(i, j))
                    if c < dp[r][j]:
                        dp[r][j], cut[r][j] = c, i
        widest = dp[k][n]
        # cỡ chữ tối đa cho k dòng này, phạt nhẹ khi nhiều dòng (ưu tiên ít dòng nếu vẫn đọc được)
        fs = min(size, int(100 * max_w / widest)) if widest else size
        score = fs - (k - 1) * 6
        if best is None or score > best[0]:
            parts, j = [], n
            for r in range(k, 0, -1):
                i = cut[r][j]
                parts.append(" ".join(words[i:j]))
                j = i
            best = (score, "\\N".join(reversed(parts)), fs)
    return best[1], max(min_size, best[2])


def ts(t):
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def write_ass(units, path, font="Arial", size=84, y=1345):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,5,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines = []
    for u in units:
        col = COLORS.get(u.get("c", "white"), "FFFFFF")
        txt, fs = fit_caption(u["t"].replace("{", "").replace("}", ""), size=size, font=font)
        lines.append(f"Dialogue: 1,{ts(u['s'])},{ts(u['e'])},Cap,,0,0,0,,{{\\an5\\pos(540,{y})\\fs{fs}\\1c&H{col}&}}{txt}")
        ic = u.get("icon")
        if ic == "x":  # dấu X đỏ vẽ bằng vector
            lines.append(f"Dialogue: 2,{ts(u['s'])},{ts(u['e'])},Cap,,0,0,0,,{{\\an7\\pos(500,1110)\\1c&H2A2AFF&\\3c&HFFFFFF&\\bord4\\p1}}m 0 6 l 6 0 l 30 24 l 54 0 l 60 6 l 36 30 l 60 54 l 54 60 l 30 36 l 6 60 l 0 54 l 24 30{{\\p0}}")
        elif ic == "dollar":
            lines.append(f"Dialogue: 2,{ts(u['s'])},{ts(u['e'])},Cap,,0,0,0,,{{\\an5\\pos(540,1150)\\fs96\\1c&H00D8FF&\\3c&H000000&}}$")
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(head + "\n".join(lines) + "\n")


# ------------------------------------------------------------------ hiệu ứng viền nháy + âm thanh
PRAISE = re.compile(r"^\W*(great|perfect|exactly|good|well done|absolutely|awesome|nice|excellent|correct|that's right|yes|bravo|perfecto|exacto|muy bien|excelente|genial|ok, esto)", re.I)
GLOW = "00E5FF"  # xanh cyan (RGB)


def make_sfx(kind, path, sr=44100):
    """Sinh âm thanh: ding = tiếng 'tinh tinh' 2 nốt; pop = tiếng 'tách' nhẹ khi hiện phụ đề."""
    import math, struct, wave
    if kind == "buzz":   # "tè tè": hai tiếng còi buzzer ngắn, trầm, gắt (báo sai)
        n = int(sr * 0.62)
        buf = [0.0] * n
        for t0 in (0.0, 0.27):
            for i in range(int(t0 * sr), min(n, int((t0 + 0.2) * sr))):
                t = (i / sr) - t0
                env = min(1.0, t * 120) * min(1.0, (0.2 - t) * 120)
                buf[i] += env * sum(math.sin(2 * math.pi * 150 * k * t) / k for k in (1, 3, 5, 7)) * 0.42
        with wave.open(path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(b"".join(struct.pack("<h", max(-32767, min(32767, int(x * 32767)))) for x in buf))
        return
    if kind == "ding":
        notes, n = [(0.0, 1318.5), (0.14, 1975.5), (0.28, 2637.0)], int(sr * 1.1)
    else:
        notes, n = [(0.0, 880.0)], int(sr * 0.12)
    buf = [0.0] * n
    for t0, f in notes:
        i0 = int(t0 * sr)
        for i in range(i0, n):
            t = (i - i0) / sr
            env = math.exp(-t * (5.5 if kind == "ding" else 40)) * min(1.0, t * 800)
            buf[i] += env * (math.sin(2 * math.pi * f * t) + 0.35 * math.sin(2 * math.pi * 2 * f * t)) * (0.32 if kind == "ding" else 0.5)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", max(-32767, min(32767, int(x * 32767)))) for x in buf))


def glow_filters(times, dur=1.0, color=GLOW):
    """Chuỗi drawbox: viền phát sáng nhiều lớp, nháy 3 nhịp trong `dur` giây tại mỗi mốc."""
    fl = []
    for t in times:
        en = f"between(t,{t:.2f},{t + dur:.2f})*lt(mod(t-{t:.2f},0.34),0.2)"
        for th, al in ((46, 0.14), (26, 0.28), (12, 0.55), (5, 0.95)):
            fl.append(f"drawbox=x=0:y=0:w=iw:h=ih:color=0x{color}@{al}:t={th}:enable='{en}'")
    return ",".join(fl)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--subs", required=True, help="file JSON danh sách phụ đề [{t,c,icon}]")
    ap.add_argument("--out")
    ap.add_argument("--no-tighten", action="store_true")
    ap.add_argument("--settle", type=float, default=0.5, help="giây giữ lại sau khi hết lời (nhân vật về tư thế nghỉ), mặc định 0.5")
    ap.add_argument("--lead", type=float, default=0.12, help="giây giữ lại trước câu kế tiếp, mặc định 0.12")
    ap.add_argument("--no-endcard", action="store_true")
    ap.add_argument("--no-topbar", action="store_true")
    ap.add_argument("--logo-mov", help="logo động nền trong suốt 1080x1920 (mov/webm có alpha): chạy một lần rồi giữ khung cuối đến hết video; thay cho --topbar")
    ap.add_argument("--logo-hold", type=float, default=0, help="với --logo-mov: sau mỗi lần chạy logo đứng yên N giây rồi chạy lại (lặp đến hết video); 0 = chạy một lần rồi giữ khung cuối")
    ap.add_argument("--topbar", default=os.path.join(ASSETS, "topbar.png"))
    ap.add_argument("--endcard", default=os.path.join(ASSETS, "endcard.mp4"))
    ap.add_argument("--subs-only", action="store_true", help="chỉ in thời điểm phụ đề rồi thoát")
    ap.add_argument("--model", default="small.en", help="Whisper: small.en cho lời toàn tiếng Anh; medium (đa ngôn ngữ) khi có câu tiếng Tây Ban Nha")
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--ding", action="store_true", help="viền xanh nháy + tiếng tinh tinh ở câu khen (Great, Perfect, Exactly...) hoặc câu có \"fx\":\"ding\" trong file phụ đề")
    ap.add_argument("--pop", action="store_true", help="tiếng tách nhẹ mỗi khi hiện phụ đề mới")
    ap.add_argument("--hook-fx", action="store_true", help="câu có \"fx\":\"wrong\" -> viền đỏ nháy + tiếng tè tè; \"fx\":\"right\" -> viền xanh lá nháy + tiếng tinh tinh")
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.raw)[0] + "_final.mp4"
    units = json.load(open(a.subs, encoding="utf-8"))
    work = tempfile.mkdtemp(prefix="pp_")
    try:
        src = os.path.join(work, "tight.mp4")
        if a.no_tighten or a.subs_only:
            shutil.copy(a.raw, src)
        else:
            print(f"Cắt khoảng lặng: {duration(a.raw):.1f}s -> ", end="", flush=True)
            print(f"{tighten(a.raw, src, a.settle, a.lead):.1f}s")
        print("Transcribe + căn phụ đề...")
        prompt = " ".join(u["t"] for u in units)
        raw_units = json.loads(json.dumps(units))
        words = transcribe(src, a.model, prompt)
        if words is None:
            print("CẢNH BÁO: máy này không chạy được nhận dạng giọng; phụ đề dùng thời điểm ước lượng nên có thể lệch so với tiếng nói.")
            units = align(units, estimate_words(src, units))
        else:
            units = align(units, words)
            bad = sum(1 for u in units if not u["ok"])
            if bad >= 3:  # nhiều phụ đề không khớp: thử lại không lọc VAD, giữ kết quả khớp tốt hơn
                print("Nhiều phụ đề không khớp, thử lại không bật VAD...")
                w2 = transcribe(src, a.model, prompt, vad=False)
                if w2:
                    u2 = align(raw_units, w2)
                    if sum(1 for u in u2 if not u["ok"]) <= bad:
                        units = u2
        for u in units:
            print(f"  {u['s']:6.2f}-{u['e']:6.2f}  {u['c']:6}  {u['t']}")
        if a.subs_only:
            return
        write_ass(units, os.path.join(work, "subs.ass"), font=a.font)
        main_mp4 = os.path.join(work, "main.mp4")
        wrongs = [u["s"] for u in units if a.hook_fx and u.get("fx") == "wrong"]
        rights = [u["s"] for u in units if a.hook_fx and u.get("fx") == "right"]
        dings = [u["s"] for u in units if u.get("fx") != "right" and ((u.get("fx") == "ding") or (a.ding and u.get("fx") != "none" and PRAISE.match(u["t"])))]
        pops = [u["s"] for u in units] if a.pop else []
        glows = [g for g in (glow_filters(dings) if dings else "", glow_filters(wrongs, 1.1, "FF2A2A") if wrongs else "", glow_filters(rights, 1.1, "2EE86A") if rights else "") if g]
        vf = "scale=1080:1920:flags=lanczos,fps=30,subtitles=subs.ass" + ("," + ",".join(glows) if glows else "") + "[v0]"
        if wrongs or rights:
            print(f"Hiệu ứng mở đầu: {len(wrongs)} câu sai (viền đỏ + tè tè), {len(rights)} câu đúng (viền xanh lá + tinh tinh)")
        cmd = ["ffmpeg", "-y", "-i", "tight.mp4"]
        sfx_in = []  # (mốc giây, file wav, âm lượng)
        for kind, times, vol in (("ding", dings + rights, 0.9), ("buzz", wrongs, 0.85), ("pop", pops, 0.6)):
            if times:
                make_sfx(kind, os.path.join(work, kind + ".wav"))
                sfx_in += [(t, kind + ".wav", vol) for t in times]
        if a.logo_mov:
            lg = "logo" + os.path.splitext(a.logo_mov)[1]
            if a.logo_hold > 0:  # một chu kỳ = logo chạy + đứng yên N giây (giữ khung cuối), lặp vô hạn
                run(["ffmpeg", "-y", "-i", a.logo_mov, "-an", "-vf", f"tpad=stop_mode=clone:stop_duration={a.logo_hold}", "-c:v", "qtrle", "-pix_fmt", "argb", "logo_cycle.mov"], cwd=work)
                cmd += ["-stream_loop", "-1", "-i", "logo_cycle.mov"]
            else:
                shutil.copy(a.logo_mov, os.path.join(work, lg))
                cmd += ["-i", lg]
            # logo lặp vô hạn thì phải dừng theo video chính (shortest=1); logo chạy một lần thì giữ khung cuối đến hết video chính
            shortest = ":shortest=1" if a.logo_hold > 0 else ""
            fc = f"[0:v]{vf};[1:v]scale=1080:1920,format=rgba[lg];[v0][lg]overlay=0:0:eof_action=repeat:format=auto{shortest}[v]"
        elif a.no_topbar:
            fc = f"[0:v]{vf};[v0]null[v]"
        else:
            shutil.copy(a.topbar, os.path.join(work, "topbar.png"))
            cmd += ["-i", "topbar.png"]
            fc = f"[0:v]{vf};[v0][1:v]overlay=37:42:eof_action=repeat[v]"
        amap = "0:a"
        if sfx_in:
            base = sum(1 for x in cmd if x == "-i")
            names = sorted({f for _, f, _ in sfx_in})
            for f in names:
                cmd += ["-i", f]
            parts = []
            for k, (t, f, vol) in enumerate(sfx_in):
                idx = base + names.index(f)
                ms = int(t * 1000)
                parts.append(f"[{idx}:a]asplit=1[sx{k}in];[sx{k}in]adelay={ms}|{ms},volume={vol}[sx{k}]")
            fc += ";" + ";".join(parts) + ";[0:a]" + "".join(f"[sx{k}]" for k in range(len(sfx_in))) + f"amix=inputs={len(sfx_in) + 1}:normalize=0:duration=first[aout]"
            amap = "[aout]"
        cmd += ["-filter_complex", fc, "-map", "[v]", "-map", amap, "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "main.mp4"]
        run(cmd, cwd=work)
        if a.no_endcard:
            shutil.copy(main_mp4, out)
        else:
            run(["ffmpeg", "-y", "-i", main_mp4, "-i", a.endcard, "-filter_complex",
                 "[0:v]setsar=1,fps=30,format=yuv420p[a];[1:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[b];[0:a]aresample=44100[x];[1:a]aresample=44100[y];[a][x][b][y]concat=n=2:v=1:a=1[v][au]",
                 "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out])
        print("XONG ->", out, f"({duration(out):.1f}s)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--_whisper":   # tiến trình con của transcribe(): đối số do _whisper_cmd tạo
        _whisper_child(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] == "1", sys.argv[6], sys.argv[7])
        sys.exit(0)
    main()
