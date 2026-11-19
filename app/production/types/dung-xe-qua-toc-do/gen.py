"""Gen riêng của thể loại dung-xe-qua-toc-do (Ấn Độ, người thật phông xanh): MỘT dự án, hai phần trong cùng một kịch bản.
  Phần 1: cảnh sát chặn xe quá tốc độ (cảnh thường: cảnh sát nói tiếng Anh, tài xế tiếng Anh ậm ừ, bé trai nói tiếng Anh với cảnh sát và tiếng Hindi với bố/mẹ).
  Phần 2: tài xế + gia sư AI Aiva AI, ghép 2 lớp. Vào phần 2: nhoè chuyển động.
Cùng cơ chế với canh-sat-gia-su-ai; logic nhiều phần dùng chung: ../_chung/nhieu_phan.py.

Khác canh-sat-gia-su-ai: lời Hindi viết chữ Devanagari (xen từ tiếng Anh chữ La-tinh). engine.voice_span với câu Devanagari hoặc không có từ La-tinh
để khớp (trả None -> cắt thường) hoặc chỉ khớp 1-2 từ Anh rồi lấy TOÀN BỘ đoạn có tiếng làm lời, kể cả tiếng cười / lẩm bẩm sau câu (video mẫu
16/11/2026: nhiều đoạn trống 3-5 s ở phần 2). Ở đây câu Devanagari lấy mốc lời theo các đoạn có tiếng liên tiếp tới khi đủ độ dài ước tính
và gặp khoảng nghỉ >= 0,7 s; mọi thứ sau đó bị cắt. Chỉ vá trong tiến trình của thể loại này; engine.py không bị sửa."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402
import engine as E  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))

_voice_span_goc = E.voice_span


def _doan_co_tieng(wav):
    """[(bắt đầu, kết thúc)] các đoạn có tiếng theo năng lượng (cùng ngưỡng E._energy_span), gộp khoảng nghỉ < 0,45 s, bỏ đoạn < 0,12 s."""
    import wave
    import numpy as np
    with wave.open(wav, "rb") as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
    win, hop = int(sr * 0.025), int(sr * 0.01)
    if len(a) < 2 * win:
        return []
    fr = np.lib.stride_tricks.sliding_window_view(a, win)[::hop]
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9)
    floor, level = np.percentile(db, 10), np.percentile(db, 90)
    if level - floor < 15:
        return []
    above = db > max(floor + 10, level - 15)
    segs, k, n = [], 0, len(above)
    while k < n:
        if above[k]:
            j = k
            while j < n and above[j:j + 45].any():   # khoảng nghỉ < 0,45 s vẫn tính cùng đoạn
                j += 1
            e = j
            while e > k and not above[e - 1]:
                e -= 1
            if (e - k) * hop / sr >= 0.12:
                segs.append((k * hop / sr, e * hop / sr + win / sr))
            k = j
        else:
            k += 1
    return segs


_HINDI_LATIN = set("kya aapko aap hai hain hoon kar karo karna rahe tum tumhari main mein ke ki ko ka nahi haan sach sachmuch chalo dikhata dikhao ruko kaun lekin bas hum kabhi kahin bhi abhi teen hafton sirf har roz theek kehna sahi tareeka madad yahaan aur liye apna zyada achhi inki bahut ye ho gaye pareshaan mat saath ek aakhir behtar bolne karne".split())


def _la_hindi(text):
    """Câu Hindi (chữ Devanagari hoặc Hindi viết chữ La-tinh): có từ Hindi phổ biến."""
    if E.speech_lang(text) in ("hi", "gu"):
        return True
    return any(w in _HINDI_LATIN for w in re.findall(r"[a-z]+", str(text).lower()))


def _voice_span_hindi(path, expected):
    """Câu thuần Devanagari: mốc lời = các đoạn có tiếng liên tiếp tới khi đã đủ độ dài ước tính của câu VÀ gặp khoảng nghỉ >= 0,7 s;
    tiếng cười / lẩm bẩm sau khoảng nghỉ đó bị cắt bỏ."""
    if not _la_hindi(expected):
        return _voice_span_goc(path, expected)
    wav = path + ".span.wav"
    E.sh(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
    try:
        segs = _doan_co_tieng(wav)
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass
    if not segs:
        return _voice_span_goc(path, expected)
    est = max(0.35, len(str(expected).split()) * 0.5)
    start, end = segs[0]
    for a, b in segs[1:]:
        if a - end >= 0.7 and end - start >= 0.8 * est:
            break
        end = b
    return (start, end) if end - start > 0.5 else _voice_span_goc(path, expected)


E.voice_span = _voice_span_hindi


def run(vdata, template, out_dir, opts, emit, cancel):
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
