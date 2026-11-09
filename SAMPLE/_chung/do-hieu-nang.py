#!/usr/bin/env python
"""Đo hiệu năng gen video của LUO Studio để tìm điểm nghẽn và số luồng tối ưu (xem DO-HIEU-NANG.md cùng thư mục).

Chạy bằng Python đi kèm Studio (chỉ dùng thư viện chuẩn, không cần cài thêm):

  runtime\\python.exe SAMPLE\\_chung\\do-hieu-nang.py theo-doi [--moi 5] [--nhan p2-a3]
      Lấy mẫu máy mỗi N giây trong lúc Studio đang gen: CPU%, RAM, số tab/RAM Chromium, ffmpeg, Python (Whisper/mediapipe), mạng,
      số việc LUO-API đang chạy/chờ, số video Studio đang chạy. Ghi userdata/logs/hieu-nang/<nhan>-<thời gian>.csv. Ctrl+C để dừng.
      --nhan: tên đợt đo, nên ghi cấu hình (vd. p2-a3 = parallel 2, 3 tài khoản) để sau so sánh.

  runtime\\python.exe SAMPLE\\_chung\\do-hieu-nang.py bao-cao [--tu "2026-11-07 14:00"] [--den "2026-11-07 16:00"] [--csv <file.csv>]
      Đọc userdata/api/data/tasks.json (mọi lệnh gen, có mốc thời gian từng bước) và file CSV của theo-doi (nếu có), in:
      thời gian từng bước, thời gian Muse vẽ theo số việc chạy cùng lúc, thông lượng (clip/giờ) theo số luồng, lỗi theo loại,
      CPU/RAM theo số việc đồng thời, và KẾT LUẬN điểm nghẽn. --tu/--den: chỉ tính lệnh gen trong khoảng (giờ máy).
"""
import argparse
import collections
import csv
import datetime as dt
import json
import os
import statistics
import subprocess
import sys
import time

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
USER = os.environ.get("LUO_USERDATA") or os.path.join(ROOT, "userdata")
TASKS = os.path.join(USER, "api", "data", "tasks.json")
QUEUE = os.path.join(USER, "studio", "queue.json")
OUT_DIR = os.path.join(USER, "logs", "hieu-nang")
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

# ------------------------------------------------------------------ theo dõi máy
PS_SAMPLE = r"""
$cpu = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
$os = Get-CimInstance Win32_OperatingSystem
$pr = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^(chrome|chromium|msedge|ffmpeg|ffprobe|python|pythonw)$' } |
      Group-Object Name | ForEach-Object { [pscustomobject]@{ n = $_.Name; c = $_.Count;
          ws = [long](($_.Group | Measure-Object WorkingSet64 -Sum).Sum); cpu = [double](($_.Group | Measure-Object CPU -Sum).Sum) } }
$st = Get-NetAdapterStatistics -ErrorAction SilentlyContinue
$rx = [long](($st | Measure-Object ReceivedBytes -Sum).Sum); $tx = [long](($st | Measure-Object SentBytes -Sum).Sum)
[pscustomobject]@{ cpu = $cpu; free_kb = $os.FreePhysicalMemory; total_kb = $os.TotalVisibleMemorySize; procs = @($pr); rx = $rx; tx = $tx } |
    ConvertTo-Json -Compress -Depth 4
"""

FIELDS = ["thoi_gian", "cpu_pct", "ram_dung_mb", "ram_trong_mb", "chromium_n", "chromium_mb", "chromium_cpu_pct", "ffmpeg_n", "ffmpeg_mb",
          "ffmpeg_cpu_pct", "python_n", "python_mb", "python_cpu_pct", "mang_nhan_kbps", "mang_gui_kbps",
          "api_dang_chay", "api_cho", "api_video_chay", "api_anh_chay", "studio_video_chay", "studio_video_cho"]


def _jload(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _tasks():
    t = _jload(TASKS, [])
    return t if isinstance(t, list) else list(t.values())


def _queue_items():
    q = _jload(QUEUE, [])
    return q if isinstance(q, list) else q.get("items", [])


def _sample_sys():
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", PS_SAMPLE], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", creationflags=CREATE_NO_WINDOW, timeout=60)
    return json.loads(r.stdout.strip() or "{}")


def theo_doi(every, label):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{label}-{dt.datetime.now():%Y%m%d-%H%M%S}.csv")
    cores = os.cpu_count() or 1
    prev = None
    print(f"Ghi {path}  (mỗi {every}s, Ctrl+C để dừng)")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        while True:
            t0 = time.time()
            try:
                s = _sample_sys()
            except Exception as e:  # noqa: BLE001
                print("lấy mẫu lỗi:", e)
                time.sleep(every)
                continue
            groups = {"chromium": (0, 0, 0.0), "ffmpeg": (0, 0, 0.0), "python": (0, 0, 0.0)}
            for p in s.get("procs") or []:
                g = "chromium" if p["n"] in ("chrome", "chromium", "msedge") else ("ffmpeg" if p["n"].startswith("ff") else "python")
                c, ws, cpu = groups[g]
                groups[g] = (c + int(p["c"]), ws + int(p["ws"]), cpu + float(p["cpu"] or 0))
            row = {"thoi_gian": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "cpu_pct": round(float(s.get("cpu") or 0), 1),
                   "ram_dung_mb": round((int(s.get("total_kb") or 0) - int(s.get("free_kb") or 0)) / 1024),
                   "ram_trong_mb": round(int(s.get("free_kb") or 0) / 1024)}
            for g, (c, ws, cpu) in groups.items():
                row[f"{g}_n"], row[f"{g}_mb"] = c, round(ws / 2**20)
                pc = 0.0
                if prev is not None:
                    dtm = t0 - prev["t"]
                    pc = max(0.0, (cpu - prev["cpu"][g]) / dtm / cores * 100) if dtm > 0 else 0.0
                row[f"{g}_cpu_pct"] = round(pc, 1)
            rx, tx = int(s.get("rx") or 0), int(s.get("tx") or 0)
            if prev is not None and t0 > prev["t"]:
                row["mang_nhan_kbps"] = round(max(0, rx - prev["rx"]) / (t0 - prev["t"]) / 1024, 1)
                row["mang_gui_kbps"] = round(max(0, tx - prev["tx"]) / (t0 - prev["t"]) / 1024, 1)
            else:
                row["mang_nhan_kbps"] = row["mang_gui_kbps"] = 0
            prev = {"t": t0, "rx": rx, "tx": tx, "cpu": {g: v[2] for g, v in groups.items()}}
            ts = _tasks()
            run = [x for x in ts if x.get("status") == "processing"]
            row["api_dang_chay"] = len(run)
            row["api_cho"] = sum(1 for x in ts if x.get("status") == "queued")
            row["api_video_chay"] = sum(1 for x in run if x.get("kind") == "video")
            row["api_anh_chay"] = sum(1 for x in run if x.get("kind") == "image")
            qi = _queue_items()
            row["studio_video_chay"] = sum(1 for x in qi if x.get("state") == "running")
            row["studio_video_cho"] = sum(1 for x in qi if x.get("state") == "waiting")
            w.writerow(row)
            f.flush()
            print(f"{row['thoi_gian']}  CPU {row['cpu_pct']:>4}%  RAM dùng {row['ram_dung_mb']} MB  Chromium {row['chromium_n']} tiến trình/{row['chromium_mb']} MB"
                  f"  ffmpeg {row['ffmpeg_n']}  Python {row['python_mb']} MB  API chạy {row['api_dang_chay']} (chờ {row['api_cho']})  Studio chạy {row['studio_video_chay']}")
            time.sleep(max(0.5, every - (time.time() - t0)))


# ------------------------------------------------------------------ báo cáo
def _parse_t(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M").timestamp() if s else None


def _pct(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(len(v) * p))] if v else 0


def _med(v):
    return statistics.median(v) if v else 0


def bao_cao(t_from, t_to, csv_path):
    tasks = [x for x in _tasks() if x.get("created_at") and (not t_from or x["created_at"] >= t_from) and (not t_to or x["created_at"] <= t_to)]
    done = [x for x in tasks if x.get("status") == "completed" and x.get("timing")]
    fails = [x for x in tasks if x.get("status") == "failed"]
    if not tasks:
        print("Không có lệnh gen nào trong khoảng thời gian này (tasks.json).")
        return
    span = (max(x["created_at"] for x in tasks) - min(x["created_at"] for x in tasks)) / 3600 or 1 / 3600
    print(f"== Lệnh gen: {len(tasks)} (xong {len(done)}, lỗi {len(fails)}), trải trong {span:.1f} giờ ==\n")

    # 1. thời gian từng bước (mốc của LUO-API, tính từ lúc bắt đầu cầm tab)
    print("1) Thời gian từng bước của một lệnh gen (giây, trung vị / p90). Bước trong máy = mọi bước trừ 'Muse vẽ'.")
    print(f"{'loại':6} {'N':>4} {'chờ tài khoản/tab':>18} {'mở chat':>8} {'đính ảnh+gửi':>13} {'Muse nhận':>10} {'Muse vẽ':>14} {'tải về':>8} {'tổng API':>9}")
    for kind in ("image", "video"):
        v = [x for x in done if x.get("kind") == kind]
        if not v:
            continue
        tm = [x["timing"] for x in v]
        def d(a, b):
            return [t.get(b, 0) - t.get(a, 0) for t in tm if t.get(a) is not None and t.get(b) is not None]
        qw = [float(x.get("queue_wait") or 0) for x in v]
        render = [t.get("muse_render") or (t.get("media_seen", 0) - t.get("confirmed", 0)) for t in tm]
        dl = d("media_seen", "downloaded")
        el = [float(x.get("elapsed") or 0) for x in v]
        print(f"{kind:6} {len(v):>4} {_med(qw):>8.1f}/{_pct(qw, .9):<9.1f} {_med(d('checkout', 'thread_ready')):>8.1f} {_med(d('thread_ready', 'sent')):>13.1f} "
              f"{_med(d('sent', 'confirmed')):>10.1f} {_med(render):>6.1f}/{_pct(render, .9):<7.1f} {_med(dl):>8.1f} {_med(el):>9.1f}")
    print("   -> Nếu 'Muse vẽ' chiếm > 85% tổng thì máy chủ không phải điểm nghẽn; tăng tốc chỉ bằng thêm việc song song (thêm tài khoản).\n")

    # 2. Muse vẽ theo số việc chạy CÙNG LÚC trên LUO-API
    iv = []
    for x in done:
        s = float(x["created_at"]) + float(x.get("queue_wait") or 0)
        iv.append((s, s + float(x.get("elapsed") or 0), x))
    by = collections.defaultdict(list)
    by_acc = collections.defaultdict(lambda: collections.defaultdict(list))
    for s, e, x in iv:
        n = sum(1 for s2, e2, _ in iv if s2 < e and e2 > s)
        same_acc = sum(1 for s2, e2, y in iv if s2 < e and e2 > s and y.get("account") == x.get("account"))
        r = x["timing"].get("muse_render") or (x["timing"].get("media_seen", 0) - x["timing"].get("confirmed", 0))
        by[(x.get("kind"), min(n, 8))].append((r, float(x.get("elapsed") or 0)))
        if x.get("kind") == "video":
            by_acc[x.get("account_label") or x.get("account")][min(same_acc, 4)].append(r)
    print("2) Thời gian Muse vẽ theo số việc đang chạy cùng lúc trên LUO-API (mọi tài khoản). Thông lượng = N / trung vị tổng -> clip/giờ nếu luôn đủ việc.")
    print(f"{'loại':6} {'cùng lúc':>8} {'N':>4} {'Muse vẽ tv':>10} {'p90':>7} {'tổng tv':>8} {'clip/giờ ước':>12}")
    best = {}
    for (kind, n), v in sorted(by.items()):
        r = [a for a, _ in v]
        el = [b for _, b in v]
        thr = n * 3600 / _med(el) if _med(el) else 0
        flag = ""
        if len(v) < 5:
            flag = "  (ít mẫu)"
        print(f"{kind:6} {n:>8} {len(v):>4} {_med(r):>10.1f} {_pct(r, .9):>7.1f} {_med(el):>8.1f} {thr:>12.0f}{flag}")
        if len(v) >= 5 and (kind not in best or thr > best[kind][1]):
            best[kind] = (n, thr)
    for kind, (n, thr) in best.items():
        print(f"   -> {kind}: thông lượng tốt nhất đo được ở {n} việc cùng lúc (~{thr:.0f}/giờ). Khi p90 tăng vọt so với mức trước đó là Muse bắt đầu nghẽn.")
    print()
    print("3) Muse vẽ video theo số việc chạy cùng lúc trên CÙNG MỘT tài khoản (một tài khoản = một VM Muse):")
    print(f"{'tài khoản':12} " + " ".join(f"{'%d việc' % k:>14}" for k in (1, 2, 3, 4)))
    for acc, m in by_acc.items():
        print(f"{str(acc):12} " + " ".join((f"{_med(m[k]):>6.1f}s n={len(m[k]):<4}" if m.get(k) else f"{'-':>14}") for k in (1, 2, 3, 4)))
    print("   -> Cột nào tăng rõ so với cột 1 việc là giới hạn MUSE2API_ACCOUNT_PARALLEL của tài khoản đó.\n")

    # 3b. mô hình thực tế: 1 tài khoản = 1 video, cảnh nối tiếp -> tài khoản bận bao nhiêu % thời gian, trống bao lâu giữa 2 lệnh
    print("3b) Một tài khoản = một video chạy nối tiếp: tài khoản 'bận' (Muse+API) bao nhiêu % và trống bao lâu giữa hai lệnh gen liên tiếp.")
    print("    Khoảng trống = phần máy mình làm giữa hai lệnh (cắt, Whisper, mediapipe, hỏi trạng thái) + Studio chờ luồng/khoá.")
    print(f"{'tài khoản':12} {'lệnh':>5} {'bận %':>6} {'trống tv':>9} {'p75':>6} {'p90':>6} {'chồng lệnh':>10} {'cảnh/giờ ước':>12}")
    seq = collections.defaultdict(list)
    for x in sorted(tasks, key=lambda x: x["created_at"]):
        s = x["created_at"] + float(x.get("queue_wait") or 0)
        seq[x.get("account_label") or x.get("account") or "?"].append((x["created_at"], s, s + float(x.get("elapsed") or 0), x))
    for acc, v in seq.items():
        gaps, overl = [], 0
        for i in range(1, len(v)):
            c0, s0, e0, x0 = v[i - 1]
            if x0.get("status") != "completed":
                continue
            g = v[i][0] - e0
            if g < 0:
                overl += 1
            elif g < 600:
                gaps.append(g)
        sessions, cur = [], []
        for item in v:   # phiên = chuỗi lệnh cách nhau < 10 phút
            if cur and item[0] - cur[-1][2] > 600:
                sessions.append(cur)
                cur = []
            cur.append(item)
        if cur:
            sessions.append(cur)
        span = sum(c[-1][2] - c[0][0] for c in sessions) or 1
        busy = sum(e - s for _, s, e, x in v if x.get("status") == "completed")
        gen_med = _med([e - s for _, s, e, x in v if x.get("status") == "completed"]) or 1
        per_scene = gen_med + _med(gaps)   # một lệnh gen + một khoảng trống (chưa tính gen lại)
        print(f"{str(acc):12} {len(v):>5} {busy / span * 100:>6.0f} {_med(gaps):>9.1f} {_pct(gaps, .75):>6.1f} {_pct(gaps, .9):>6.1f} {overl:>10} {3600 / per_scene:>12.0f}")
    print("   -> 'chồng lệnh' > 0: tài khoản đó đang chạy 2 video cùng lúc (MUSE2API_ACCOUNT_PARALLEL > 1), không đúng mô hình 1 tài khoản = 1 video.")
    print("   -> 'bận %' là trần của tài khoản: 75% nghĩa là 1/4 thời gian tài khoản ngồi chờ máy mình. Khoảng trống tăng theo parallel là máy nghẽn (khoá Whisper/mediapipe).\n")

    # 4. lỗi
    print("4) Lỗi theo loại:")
    cnt = collections.Counter((x.get("error_kind") or "?", (x.get("error") or "")[:70].replace("\n", " ")) for x in fails)
    for (k, msg), n in cnt.most_common(10):
        print(f"   {n:>3}  [{k}] {msg}")
    if not fails:
        print("   (không có)")
    print()

    # 5. CSV theo dõi máy
    rows = []
    if csv_path and os.path.exists(csv_path):
        with open(csv_path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    if rows:
        print(f"5) Máy ({len(rows)} mẫu, {os.path.basename(csv_path)}): theo số việc LUO-API đang chạy")
        g = collections.defaultdict(list)
        for r in rows:
            g[int(r["api_dang_chay"])].append(r)
        print(f"{'việc':>4} {'mẫu':>4} {'CPU tv':>7} {'CPU p90':>8} {'RAM dùng tv MB':>14} {'RAM trống min':>13} {'Chromium MB':>12} {'ffmpeg CPU%':>11} {'Python CPU%':>11} {'mạng nhận kbps':>14}")
        for n in sorted(g):
            v = g[n]
            fl = lambda k: [float(r[k] or 0) for r in v]  # noqa: E731
            print(f"{n:>4} {len(v):>4} {_med(fl('cpu_pct')):>7.0f} {_pct(fl('cpu_pct'), .9):>8.0f} {_med(fl('ram_dung_mb')):>14.0f} {min(fl('ram_trong_mb')):>13.0f} "
                  f"{_med(fl('chromium_mb')):>12.0f} {_med(fl('ffmpeg_cpu_pct')):>11.0f} {_med(fl('python_cpu_pct')):>11.0f} {_med(fl('mang_nhan_kbps')):>14.0f}")
        cpu90 = _pct([float(r["cpu_pct"] or 0) for r in rows], .9)
        ram_min = min(float(r["ram_trong_mb"] or 0) for r in rows)
        chrom = max(float(r["chromium_mb"] or 0) for r in rows)
        tabs = max(int(r["api_dang_chay"] or 0) for r in rows) or 1
        print(f"   RAM Chromium lớn nhất {chrom:.0f} MB ở tối đa {tabs} việc (~{chrom / tabs:.0f} MB/việc). CPU p90 toàn máy {cpu90:.0f}%. RAM trống thấp nhất {ram_min:.0f} MB.")
        print("   KẾT LUẬN máy: " + ("CPU là điểm nghẽn (p90 > 85%): thêm nhân CPU hoặc giảm parallel." if cpu90 > 85 else
                                   "RAM là điểm nghẽn (trống < 1.5 GB): thêm RAM hoặc giảm tab Chromium." if ram_min < 1500 else
                                   "CPU/RAM còn dư: điểm nghẽn nằm ở phía Muse (xem mục 2, 3) hoặc số tài khoản."))
    else:
        print("5) Không có CSV theo dõi máy (chạy 'theo-doi' trong lúc gen rồi truyền --csv) nên chưa kết luận được CPU/RAM.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("theo-doi")
    a.add_argument("--moi", type=float, default=5)
    a.add_argument("--nhan", default="do")
    b = sub.add_parser("bao-cao")
    b.add_argument("--tu")
    b.add_argument("--den")
    b.add_argument("--csv")
    args = ap.parse_args()
    if args.cmd == "theo-doi":
        try:
            theo_doi(args.moi, args.nhan)
        except KeyboardInterrupt:
            print("\nĐã dừng.")
    else:
        csv_path = args.csv
        if not csv_path and os.path.isdir(OUT_DIR):
            files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith(".csv"))
            csv_path = os.path.join(OUT_DIR, files[-1]) if files else None
        bao_cao(_parse_t(args.tu), _parse_t(args.den), csv_path)


if __name__ == "__main__":
    main()
