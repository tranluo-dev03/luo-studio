"""Hậu kỳ riêng của thể loại di-tru-aiva-ai (Studio gọi khi kịch bản có [HAU KY] loai: di-tru-aiva-ai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Trước khi làm phụ đề: tắt tiếng hát/ngân nhỏ mà Muse đôi khi chèn vào khoảng lặng giữa hai câu (đoạn nhỏ hơn -22 dB, có cao độ đều từ 0,6 s trở lên).
Tiếng to bằng lời nói thì không phân biệt được với lời, không xử lý ở đây. Lỗi ở bước này thì dùng raw gốc, không làm hỏng video.
Logic còn lại dùng chung: ../_chung/hau_ky.py (kiểu phụ đề theo phần / người nói trong config.json của thư mục này)."""
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

SR, BUOC = 16000, 0.1
TRAN_DB, SAN_DB, IT_NHAT = -22, -45, 6   # đoạn nhỏ hơn TRAN_DB, trên SAN_DB, dài >= IT_NHAT bước (0,6 s)
LECH_HZ = 15   # cao độ lệch trung vị quá mức này thì là lời nói, không phải nốt ngân


def tim_doan_hat(a):
    n, doan, cur = int(BUOC * SR), [], []
    for i in range(0, len(a) - n, n):
        x = a[i:i + n] - a[i:i + n].mean()
        db = 20 * np.log10(float(np.sqrt((x ** 2).mean())) + 1e-6)
        ac = np.correlate(x, x, "full")[len(x) - 1:]
        lo, hi = int(SR / 500), int(SR / 80)
        k = lo + int(np.argmax(ac[lo:hi]))
        if SAN_DB < db < TRAN_DB and ac[k] / (ac[0] + 1e-9) > 0.5:
            cur.append((i / SR, SR / k))
            continue
        if cur:
            doan.append(cur)
        cur = []
    if cur:
        doan.append(cur)
    out = []
    for d in doan:
        giua = float(np.median([h for _, h in d]))   # bỏ các bước lẫn đuôi lời nói: chỉ giữ bước có cao độ sát trung vị
        deu = [t for t, h in d if abs(h - giua) <= LECH_HZ]
        if len(deu) >= IT_NHAT and len(deu) >= 0.75 * len(d):
            out.append((deu[0], deu[-1] + BUOC))
    return out


def khu_hat(raw):
    """Trả về file đã tắt các đoạn hát (cạnh raw, để hau_ky vẫn thấy phan.json), hoặc chính raw nếu không có gì để tắt."""
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", raw, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    doan = tim_doan_hat(np.frombuffer(pcm, dtype=np.float32))
    if not doan:
        return raw
    print("Tắt tiếng hát/ngân:", ", ".join(f"{a:.1f}-{b:.1f}s" for a, b in doan), flush=True)
    # chỉ mở rộng 0,05 s: lời nói có thể nằm sát ngay trước và sau nốt
    loc = ",".join(f"volume=enable='between(t,{max(0, a - 0.05):.2f},{b + 0.05:.2f})':volume=0" for a, b in doan)
    out = os.path.join(os.path.dirname(os.path.abspath(raw)), "raw_khu_hat.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", loc, "-c:a", "aac", "-b:a", "192k", out], check=True)
    return out


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        argv[0] = khu_hat(argv[0])
    except Exception as e:  # bước phụ: lỗi thì vẫn hậu kỳ bằng raw gốc
        print("Bỏ qua bước tắt tiếng hát:", e, flush=True)
    hau_ky.main(HERE, argv)
