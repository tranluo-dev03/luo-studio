"""Gắn thương hiệu lên video đã hậu kỳ: logo bay (lặp đến hết video), logo cố định, rồi nối video giới thiệu app + video outro.
Thứ tự video cuối: [video gen từ tool (có logo bay + logo cố định)] + [video giới thiệu] + [video outro].
  python branding.py MAIN.mp4 --out OUT.mp4 [--fly logo_bay.mov] [--logo logo.png --logo-pos tl|tr|bl|br --logo-size 9 --logo-text "Talka AI"] [--intro gioi_thieu.mp4] [--outro outro.mp4]
- --fly: video logo bay nền trong suốt (mov/webm có alpha) cùng khung hình 9:16; lặp vô hạn, dừng theo video chính.
- --logo: ảnh logo đặt cố định ở góc; --logo-size = % bề ngang video (mặc định 9%), --logo-text = tên app viết cạnh logo; cụm logo + chữ nằm ở góc cách mép như video mẫu.
- Video giới thiệu / outro nối nguyên bản (không phủ logo), tự co về cùng khung hình, tần số 30fps, âm thanh 44.1kHz; clip không có tiếng được thêm tiếng lặng."""
import argparse
import json
import os
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

W, H, FPS = 1080, 1920, 30
MX, MY = 0.044, 0.039   # khoảng cách logo cố định tới mép: tỉ lệ bề ngang / chiều cao (như video mẫu Talka)
_FONTS = [r"C:\Windows\Fontsrialbd.ttf", r"C:\Windows\Fonts\segoeuib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type:format=duration", "-of", "json", path], capture_output=True, text=True, encoding="utf-8")
    j = json.loads(r.stdout or "{}")
    return float(j.get("format", {}).get("duration") or 0), any(s.get("codec_type") == "audio" for s in j.get("streams", []))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print((r.stderr or "")[-1500:])
        raise SystemExit(f"ffmpeg lỗi ({os.path.basename(cmd[0])})")


def make_badge(logo, text, size, pos, path):
    """Logo vuông + tên app bên cạnh (chữ trắng viền tối như video mẫu) -> PNG nền trong suốt. size = % bề ngang video cho cạnh logo."""
    from PIL import Image, ImageDraw, ImageFont
    L = max(16, int(W * size / 100))
    im = Image.open(logo).convert("RGBA")
    im = im.resize((L, max(1, round(L * im.height / im.width))), Image.LANCZOS)
    if not text:
        im.save(path)
        return
    fp = next((f for f in _FONTS if os.path.exists(f)), None)
    font = ImageFont.truetype(fp, int(L * 0.62)) if fp else ImageFont.load_default()
    sw = max(2, int(L * 0.05))
    box = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=font, stroke_width=sw)
    tw, th, gap = box[2] - box[0], box[3] - box[1], int(L * 0.22)
    out = Image.new("RGBA", (L + gap + tw + sw * 2, max(im.height, th + sw * 2)), (0, 0, 0, 0))
    right = pos in ("tr", "br")   # góc phải: chữ nằm bên trái logo để cả cụm sát mép
    ix = out.width - im.width if right else 0
    tx = -box[0] + sw if right else im.width + gap - box[0] + sw
    out.paste(im, (ix, (out.height - im.height) // 2))
    ImageDraw.Draw(out).text((tx, (out.height - th) // 2 - box[1] + sw // 2), text, font=font, fill=(255, 255, 255, 255), stroke_width=sw, stroke_fill=(38, 38, 40, 255))
    out.save(path)


def overlay(main, out, fly, logo, pos, size, text="", fly_opacity=100):
    """Phủ logo bay (lặp) và logo cố định lên video chính; âm thanh giữ nguyên."""
    cmd = ["ffmpeg", "-y", "-i", main]
    fc, last, n = [f"[0:v]scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},format=yuv420p[b0]"], "b0", 1
    if fly:
        cmd += ["-stream_loop", "-1", "-i", fly]
        fc.append(f"[{n}:v]scale={W}:{H},setsar=1,fps={FPS},format=rgba" + (f",colorchannelmixer=aa={fly_opacity / 100:.3f}" if fly_opacity < 100 else "") + "[fly]")
        fc.append(f"[{last}][fly]overlay=0:0:shortest=1:format=auto[b{n}]")
        last, n = f"b{n}", n + 1
    if logo:
        badge = out + ".badge.png"
        make_badge(logo, text, size, pos, badge)
        cmd += ["-loop", "1", "-i", badge]
        mx, my = int(W * MX), int(H * MY)
        x = mx if pos in ("tl", "bl") else f"W-w-{mx}"
        y = my if pos in ("tl", "tr") else f"H-h-{my}"
        fc.append(f"[{n}:v]format=rgba[lg]")
        fc.append(f"[{last}][lg]overlay={x}:{y}:shortest=1:format=auto[b{n}]")
        last, n = f"b{n}", n + 1
    cmd += ["-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "0:a?", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", out]
    try:
        run(cmd)
    finally:
        if logo and os.path.exists(out + ".badge.png"):
            os.remove(out + ".badge.png")


def concat(parts, out):
    """Nối nhiều video: cùng khung hình / fps / âm thanh; clip không có tiếng thì thêm tiếng lặng đúng độ dài."""
    cmd, fc, labels = ["ffmpeg", "-y"], [], ""
    n = 0
    for p in parts:
        dur, has_a = probe(p)
        cmd += ["-i", p]
        i = n
        n += 1
        fc.append(f"[{i}:v]scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS},format=yuv420p[v{i}]")
        if has_a:
            fc.append(f"[{i}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a{i}]")
        else:
            fc.append(f"anullsrc=r=44100:cl=stereo,atrim=duration={dur:.3f}[a{i}]")
        labels += f"[v{i}][a{i}]"
    fc.append(f"{labels}concat=n={len(parts)}:v=1:a=1[v][a]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out]
    run(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("main")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fly")
    ap.add_argument("--fly-opacity", type=float, default=100, help="độ đậm logo bay, %% (100 = đặc, 16 = mờ nhẹ)")
    ap.add_argument("--logo")
    ap.add_argument("--logo-pos", default="tl", choices=["tl", "tr", "bl", "br"])
    ap.add_argument("--logo-size", type=float, default=9, help="cạnh logo, %% bề ngang video")
    ap.add_argument("--logo-text", default="", help="tên app viết cạnh logo (vd. Talka AI)")
    ap.add_argument("--intro")
    ap.add_argument("--outro")
    a = ap.parse_args()
    work = tempfile.mkdtemp(prefix="brand_")
    try:
        cur = a.main
        if a.fly or a.logo:
            print("Phủ logo" + (" bay (lặp)" if a.fly else "") + (" + logo cố định" if a.logo else "") + "…", flush=True)
            cur = os.path.join(work, "over.mp4")
            overlay(a.main, cur, a.fly, a.logo, a.logo_pos, a.logo_size, a.logo_text, min(100, max(0, a.fly_opacity)))
        tail = [p for p in (a.intro, a.outro) if p]
        if tail:
            print("Nối " + " + ".join(n for n, p in (("video giới thiệu", a.intro), ("outro", a.outro)) if p) + "…", flush=True)
            concat([cur] + tail, a.out)
        else:
            os.replace(cur, a.out) if cur != a.main else run(["ffmpeg", "-y", "-i", a.main, "-c", "copy", a.out])
        print("XONG ->", a.out, f"({probe(a.out)[0]:.1f}s)")
    finally:
        for f in os.listdir(work):
            try:
                os.remove(os.path.join(work, f))
            except OSError:
                pass
        try:
            os.rmdir(work)
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
