"""Gen riêng của thể loại phong-van-pho-malayalam: MỘT dự án, hai phần (video mẫu "1510_interview street hindi_005", lời Malayalam).
  Phần 1: phóng viên (qua vai) hỏi đố người bán hàng rong (cảnh thường, một góc, 11 cảnh).
  Phần 2: robot Aiva ô trên, người bán hàng selfie ô dưới (ghép 2 lớp). Vào phần 2 cắt cứng như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: phong-van-pho-malayalam.

Riêng thể loại này (11/11/2026, góp ý người dùng "cắt cho vừa khớp lời, không tua nhanh"):
  - speedfix tắt: Studio mặc định tua nhanh quãng ngắt >= 0,55 s (tối đa x2) và tăng tốc giọng; người dùng thấy không tự nhiên.
  - cut_margin 0,3: cắt sát hơn mặc định 0,5 nhưng KHÔNG thấp hơn 0,3 (engine: hi = max(0,3; margin+0,05), lo = 0,18 -> cửa sổ 0,12 s, làm tròn số
    làm smart_cut bỏ qua và giữ nguyên cả clip).
  - mốc lời câu Malayalam: engine lấy theo năng lượng với mức tiếng nói = phân vị 90 và đòi lời > 0,5 s, nên câu rất ngắn ("ഉടനെ", 0,3 s trong clip 5 s)
    ra None -> không cắt. Trong lúc chạy thể loại này, mọi câu dùng _span_ml (mức theo đỉnh, bỏ tiếng động lẻ); xong trả lại hàm cũ."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

E = NP.E


def _span_ml(path):
    """(bắt đầu, kết thúc) lời nói theo năng lượng khung 25 ms: mức tiếng nói theo phân vị 99,5 (bắt được câu một từ trong clip dài),
    gộp quãng nghỉ < 0,25 s, bỏ tiếng động lẻ < 0,3 s cách đoạn khác > 0,8 s. None nếu không rõ."""
    import numpy as np
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(b, np.int16).astype(np.float32) / 32768.0
    win, hop = 400, 160
    if len(a) < 2 * win:
        return None
    fr = np.lib.stride_tricks.sliding_window_view(a, win)[::hop]
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9)
    floor, peak = np.percentile(db, 10), np.percentile(db, 99.5)
    if peak - floor < 15:
        return None
    on = db > max(floor + 12, peak - 22)
    segs, k = [], 0
    while k < len(on):
        if on[k]:
            j = k
            while j < len(on) and on[j]:
                j += 1
            if j - k >= 6:
                segs.append([k * hop / 16000, j * hop / 16000 + win / 16000])
            k = j
        else:
            k += 1
    gop = []
    for s in segs:
        if gop and s[0] - gop[-1][1] < 0.25:
            gop[-1][1] = s[1]
        else:
            gop.append(s)
    if len(gop) > 1:
        near = lambda i: min(abs(gop[i][0] - gop[j][1]) if j < i else abs(gop[j][0] - gop[i][1]) for j in range(len(gop)) if j != i)
        gop = [s for i, s in enumerate(gop) if not (s[1] - s[0] < 0.3 and near(i) > 0.8)] or gop
    lv = lambda x, y: float(db[int(x * 16000 / hop):max(int(x * 16000 / hop) + 1, int((y * 16000 - win) / hop))].max())
    for i in range(1, len(gop)):   # sau quãng lặng >= 1 s: phần còn lại < 0,8 s, hoặc nhỏ hơn lời chính >= 8 dB (ồn nền, lầm bầm; cảnh 8 "Therefore." 11/11/2026)
        rest_short = sum(y - x for x, y in gop[i:]) < 0.8
        rest_quiet = max(lv(x, y) for x, y in gop[i:]) < max(lv(x, y) for x, y in gop[:i]) - 8
        if gop[i][0] - gop[i - 1][1] >= 1.0 and (rest_short or rest_quiet):
            gop = gop[:i]
            break
    if not gop or gop[-1][1] - gop[0][0] < 0.15:
        return None
    return round(gop[0][0], 3), round(gop[-1][1], 3)


def run(vdata, template, out_dir, opts, emit, cancel):
    opts = dict(opts, cut_margin=min(float(opts.get("cut_margin", 0.5)), 0.3), speedfix=False)
    goc = E.voice_span

    def voice_span(path, expected):   # mọi câu (cả tiếng Anh): mốc Whisper của từ cuối hay trễ ~1-2 s ("Otherwise." hết lời 1,5 s, Whisper báo 3,48 s)
        return _span_ml(path) or (None if E.speech_lang(expected) == "ml" else goc(path, expected))
    E.voice_span = voice_span
    try:
        return NP.run(vdata, template, out_dir, opts, emit, cancel)
    finally:
        E.voice_span = goc
