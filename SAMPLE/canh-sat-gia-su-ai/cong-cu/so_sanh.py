"""So sánh một cảnh đã gen với đoạn tương ứng của video gốc: ảnh ghép 2 hàng (trên: video gốc, dưới: bản gen), cùng số khung.
  .venv\\Scripts\\python.exe SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\so_sanh.py <video gốc.mp4> <thư mục phan1 của lần chạy> <số cảnh> [ra.png]
Bảng ánh xạ cảnh -> giây trong video gốc lấy từ phân tích shot (README.md)."""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

# cảnh phần 1 -> (giây bắt đầu, giây kết thúc) trong video gốc (gồm cả đoạn không lời đầu cảnh nếu có)
SHOTS = {1: (0.0, 4.17), 2: (4.17, 5.47), 3: (5.47, 6.77), 4: (6.77, 8.97), 5: (8.97, 12.37), 6: (12.37, 14.77),
         7: (14.77, 16.43), 8: (16.43, 21.0), 9: (21.0, 23.9), 10: (23.9, 26.73), 11: (26.73, 27.4), 12: (27.4, 29.0)}
N = 8
W, H = 180, 320


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def frames(p, a, b, tmp, tag):
    out = []
    for i in range(N):
        t = a + (b - a) * (i + 0.5) / N
        f = os.path.join(tmp, f"{tag}_{i}.png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1", "-vf", f"scale={W}:{H}", f], check=True)
        out.append((t, f))
    return out


def main():
    goc, run, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    dst = sys.argv[4] if len(sys.argv) > 4 else os.path.join(run, f"so-sanh_canh{n}.png")
    clip = os.path.join(run, f"scene{n}_cut.mp4")
    a, b = SHOTS[n]
    with tempfile.TemporaryDirectory() as tmp:
        top = frames(goc, a, b, tmp, "g")
        bot = frames(clip, 0, dur(clip), tmp, "m")
        s = Image.new("RGB", (W * N, H * 2 + 40), "white")
        d = ImageDraw.Draw(s)
        d.text((4, 2), f"CANH {n}  tren: video goc {a:.2f}-{b:.2f}s   duoi: ban gen ({dur(clip):.1f}s)", fill="black")
        for i, ((tg, fg), (tm, fm)) in enumerate(zip(top, bot)):
            s.paste(Image.open(fg), (i * W, 20))
            s.paste(Image.open(fm), (i * W, 40 + H))
        s.save(dst)
    print(dst)


if __name__ == "__main__":
    main()
