"""Thêm nhạc nền (tự tạo bằng code, không dính bản quyền) vào video đã gen xong.
  runtime\\python.exe SAMPLE\\tiem-thit-tieng-anh\\cong-cu\\them_nhac_nen.py <final.mp4> <ra.mp4> [--db -8] [--bpm 96]
Nhạc: guitar gảy kiểu Latin ấm (Am-F-C-G), bass nhẹ, shaker; nhạc tự hạ khi có người nói (sidechain), vào/ra mờ dần.
Không đụng video, chỉ trộn thêm âm thanh."""
import argparse
import subprocess
import sys
import wave

import numpy as np

SR = 44100


def karplus(freq, dur, vel=1.0, decay=0.996):
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = (np.random.default_rng(int(freq * 7)).random(period) * 2 - 1).astype(np.float64)
    out = np.empty(n)
    for i in range(n):
        j = i % period
        out[i] = buf[j]
        buf[j] = decay * 0.5 * (buf[j] + buf[(j + 1) % period])
    env = np.minimum(1, np.arange(n) / (SR * 0.003)) * np.exp(-np.arange(n) / (SR * dur * 0.55))
    return out * env * vel


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def make(total, bpm):
    beat = 60.0 / bpm
    out = np.zeros((int(SR * (total + 3)), 2))
    chords = [  # (bass, [arpeggio notes])
        (45, [57, 60, 64, 60, 69, 64, 60, 64]),   # Am
        (41, [57, 60, 65, 60, 69, 65, 60, 65]),   # F
        (48, [55, 60, 64, 60, 67, 64, 60, 64]),   # C
        (43, [55, 59, 62, 59, 67, 62, 59, 62]),   # G
    ]
    cache = {}

    def note(m, dur, vel):
        key = (m, round(dur, 2))
        if key not in cache:
            cache[key] = karplus(midi(m), dur)
        return cache[key] * vel

    def put(sig, t, pan=0.0):
        i = int(t * SR)
        if i >= len(out):
            return
        sig = sig[: len(out) - i]
        out[i:i + len(sig), 0] += sig * (1 - pan) * 0.5 + sig * 0.5 * 0
        out[i:i + len(sig), 1] += sig * (1 + pan) * 0.5

    bars = int(total / (4 * beat)) + 2
    rng = np.random.default_rng(3)
    for b in range(bars):
        bass, arp = chords[b % 4]
        t0 = b * 4 * beat
        lvl = 0.55 + 0.45 * min(1.0, t0 / 40.0)          # mở đầu nhẹ, rồi đầy dần
        put(note(bass - 12, beat * 1.6, 0.9 * lvl), t0, -0.1)
        put(note(bass - 12, beat * 1.2, 0.7 * lvl), t0 + 2 * beat, -0.1)
        for k, m in enumerate(arp):
            put(note(m, beat * 1.4, (0.55 + 0.15 * (k % 2 == 0)) * lvl), t0 + k * beat / 2, 0.15)
        if t0 > 20:  # shaker từ giây 20
            for k in range(16):
                t = t0 + k * beat / 4
                n = int(SR * 0.05)
                s = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * 0.012)) * (0.10 if k % 4 else 0.16)
                put(s, t, 0.25)
        if t0 > 20 and b % 2 == 0:  # tiếng gõ trầm nhẹ (tay trống)
            for off in (0, 2.5):
                n = int(SR * 0.18)
                tt = np.arange(n) / SR
                s = np.sin(2 * np.pi * (90 - 40 * tt * 5) * tt) * np.exp(-tt * 22) * 0.35
                put(s, t0 + off * beat, 0)
    out = out[: int(SR * total)]
    out /= max(1e-6, np.abs(out).max())
    fade = int(SR * 3)
    out[:fade] *= np.linspace(0, 1, fade)[:, None]
    out[-fade * 2:] *= np.linspace(1, 0, fade * 2)[:, None]
    return (out * 0.9 * 32767).astype(np.int16)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--db", type=float, default=-8.0, help="mức nhạc so với giọng (dB), mặc định -8")
    ap.add_argument("--bpm", type=float, default=96)
    a = ap.parse_args()
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.src]).decode().strip())
    pcm = make(dur, a.bpm)
    wav = a.dst + ".nhac.wav"  # xoá sau khi trộn
    with wave.open(wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    fc = (f"[1:a]volume={a.db}dB[m];[0:a]asplit=2[v][sc];"
          "[m][sc]sidechaincompress=threshold=0.1:ratio=2.5:attack=30:release=500[md];"
          "[v][md]amix=inputs=2:normalize=0:duration=first[a]")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", a.src, "-i", wav, "-filter_complex", fc,
                           "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", a.dst])
    import os
    os.remove(wav)
    print("Đã ghi", a.dst)


if __name__ == "__main__":
    sys.exit(main())
