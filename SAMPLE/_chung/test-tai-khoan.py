#!/usr/bin/env python
"""Chạy một đợt test số luồng = số tài khoản trên Studio đang chạy (xem DO-HIEU-NANG.md, mục 3).

  runtime\\python.exe SAMPLE\\_chung\\test-tai-khoan.py tai-khoan
      Liệt kê tài khoản LUO-API (id, nhãn, bật/tắt, tình trạng) để chọn bộ cho từng đợt.

  runtime\\python.exe SAMPLE\\_chung\\test-tai-khoan.py khoi-dong-lai
      Tắt Studio + LUO-API đang chạy rồi mở lại (nạp code engine mới và userdata/api/.env). Chỉ làm khi không có video đang chạy.

  runtime\\python.exe SAMPLE\\_chung\\test-tai-khoan.py don-dep --du-an <id> --bien-the "a,b,c" [--nhan sau-test2]
      Dọn cảnh đã gen của các biến thể (lùi thư mục sang runs/<dự án>/_truoc-test/<nhãn>/) để lần chạy sau gen lại từ cảnh 1.
      Lệnh `chay` tự làm bước này nên thường không cần gọi riêng. Xoá hẳn thư mục _truoc-test khi không cần nữa để lấy lại ổ đĩa.

  runtime\\python.exe SAMPLE\\_chung\\test-tai-khoan.py chay --nhan test2 --du-an hanh-ly-khong-be-con-15bt-66af
        --bien-the "soi-hanh-ly-bien-the-13-nu-25-tomboy,soi-hanh-ly-bien-the-14-nu-35-minimal" --tai-khoan id1,id2 [--canh 10] [--phut 45]
      Một đợt: số luồng = số biến thể = số tài khoản (ghép theo thứ tự, video i dùng tài khoản i).
      1. Lùi thư mục kết quả cũ của các biến thể sang runs/<dự án>/_truoc-test/<nhãn>/ để chạy MỚI hoàn toàn (Studio dùng lại cảnh đã có nếu không lùi).
      2. Chỉ bật đúng bộ tài khoản của đợt (tắt các tài khoản khác, cuối đợt bật lại như cũ) và chọn tay tài khoản cho từng video.
      3. Thêm vào hàng đợi, chạy với parallel = N, đồng thời chạy do-hieu-nang.py theo-doi.
      4. Dừng khi MỌI video đã xong >= --canh cảnh (mặc định 10) hoặc hết --phut (mặc định 45), hoặc tất cả xong/lỗi.
      5. In báo cáo đợt (cảnh/giờ thực, thời gian mỗi cảnh, gen lại, Muse vẽ, trống giữa lệnh, CPU/RAM) và ghi userdata/logs/hieu-nang/<nhãn>-bao-cao.txt.
      Các video dừng giữa chừng có thể "chạy tiếp" trong Studio sau khi test xong.
"""
import argparse
import datetime as dt
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
USER = os.environ.get("LUO_USERDATA") or os.path.join(ROOT, "userdata")
RUNS = os.path.join(USER, "studio", "runs")
OUT_DIR = os.path.join(USER, "logs", "hieu-nang")
PY = sys.executable
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def _env():
    env = {}
    p = os.path.join(USER, "api", ".env")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines():
            if "=" in ln and not ln.startswith("#"):
                k, v = ln.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env


def _running():
    p = os.path.join(USER, "running.json")
    if not os.path.exists(p):
        raise SystemExit("Studio chưa chạy (không có userdata/running.json). Mở 'LUO Studio.bat' trước.")
    return json.load(open(p, encoding="utf-8"))


def _call(url, body=None, method=None, headers=None, timeout=30):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data is not None else "GET"),
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method or 'POST'} {url} -> {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


class Studio:
    def __init__(self):
        r = _running()
        self.base = r["studio_url"].rstrip("/")
        env = _env()
        self.api = f"http://127.0.0.1:{r.get('api_port') or env.get('MUSE2API_PORT', '18610')}"
        self.hdr = {"Authorization": "Bearer " + env.get("MUSE2API_KEY", "")}

    def queue(self):
        q = _call(self.base + "/api/queue")
        return q if isinstance(q, list) else q.get("items", [])

    def accounts(self):
        d = _call(self.api + "/admin/accounts", headers=self.hdr)
        return d if isinstance(d, list) else d.get("accounts", [])

    def set_enabled(self, aid, on):
        _call(f"{self.api}/admin/accounts/{aid}", {"enabled": bool(on)}, method="PATCH", headers=self.hdr)


def cmd_tai_khoan(st):
    accs = st.accounts()
    print(f"{len(accs)} tài khoản:")
    for a in accs:
        print(f"  {a['id']}  {str(a.get('label') or ''):12} {'bật ' if a.get('enabled', True) else 'TẮT '} {str(a.get('note') or a.get('status') or '')[:60]}")


def cmd_khoi_dong_lai():
    r = _running()
    st = Studio()
    if any(it.get("state") in ("running", "waiting") for it in st.queue()):
        raise SystemExit("Đang có video chạy / chờ: dừng hết trong Studio trước rồi mới khởi động lại.")
    for pid in (r.get("pid"), r.get("api_pid")):
        if pid:
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, creationflags=CREATE_NO_WINDOW)
    time.sleep(3)
    bat = os.path.join(ROOT, "LUO Studio.bat")
    subprocess.Popen(["cmd", "/c", bat], cwd=ROOT, creationflags=CREATE_NO_WINDOW | 0x00000008)
    for _ in range(90):
        time.sleep(2)
        try:
            r2 = _running()
            if r2.get("pid") != r.get("pid"):
                _call(r2["studio_url"].rstrip("/") + "/api/health", timeout=5)
                print("Studio đã mở lại:", r2["studio_url"])
                return
        except Exception:  # noqa: BLE001
            pass
    raise SystemExit("Studio chưa lên sau 3 phút, mở 'LUO Studio (xem loi).bat' để xem lỗi.")


def don_dep(pid, names, label, log=print):
    """Lùi thư mục kết quả của các biến thể sang runs/<pid>/_truoc-test/<label>/ để lần chạy sau không dùng lại cảnh cũ."""
    st = Studio()
    busy = [it["variant"] for it in st.queue() if it.get("project") == pid and it["variant"] in names and it.get("state") in ("running", "waiting")]
    if busy:
        raise SystemExit("Đang chạy / chờ, dừng trước khi dọn: " + ", ".join(busy))
    for name in names:
        d = os.path.join(RUNS, pid, name)
        if os.path.isdir(d) and os.listdir(d):
            dst = os.path.join(RUNS, pid, "_truoc-test", label, name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                dst += f"-{dt.datetime.now():%H%M%S}"
            shutil.move(d, dst)
            log(f"dọn {name}: lùi sang {os.path.relpath(dst, RUNS)}")
        else:
            log(f"dọn {name}: chưa có gì")


def _scenes_done(it):
    return sum(1 for sc in it.get("scenes") or [] if sc.get("state") == "done")


def cmd_chay(a):
    st = Studio()
    names = [x.strip() for x in a.bien_the.split(",") if x.strip()]
    acc_ids = [x.strip() for x in a.tai_khoan.split(",") if x.strip()]
    n = len(names)
    if n != len(acc_ids):
        raise SystemExit(f"Số biến thể ({n}) phải bằng số tài khoản ({len(acc_ids)})")
    if n > 8:
        raise SystemExit("Studio chạy tối đa 8 luồng")
    accs = {x["id"]: x for x in st.accounts()}
    for aid in acc_ids:
        if aid not in accs:
            raise SystemExit(f"Không có tài khoản {aid} (xem lệnh tai-khoan)")
    if any(it.get("state") in ("running", "waiting") for it in st.queue()):
        raise SystemExit("Đang có video chạy / chờ trong Studio: dừng hết trước khi test.")
    os.makedirs(OUT_DIR, exist_ok=True)
    log_f = open(os.path.join(OUT_DIR, f"{a.nhan}-nhat-ky.txt"), "a", encoding="utf-8")

    def log(*s):
        msg = f"{dt.datetime.now():%H:%M:%S} " + " ".join(str(x) for x in s)
        print(msg)
        log_f.write(msg + "\n")
        log_f.flush()

    # 1. lùi thư mục kết quả cũ
    don_dep(a.du_an, names, a.nhan, log)
    # 2. bật đúng bộ tài khoản
    prev = {aid: x.get("enabled", True) for aid, x in accs.items()}
    for aid, x in accs.items():
        want = aid in acc_ids
        if x.get("enabled", True) != want:
            st.set_enabled(aid, want)
    log(f"bật {n} tài khoản: " + ", ".join(accs[i].get("label") or i for i in acc_ids) + f"; tắt {sum(1 for i in accs if i not in acc_ids)} tài khoản khác")
    # 3. hàng đợi
    ids = _call(st.base + "/api/queue/add", {"project": a.du_an, "variants": names})["ids"]
    if len(ids) != n:
        raise SystemExit(f"Chỉ thêm được {len(ids)}/{n} biến thể vào hàng đợi (tên sai?)")
    for iid, aid in zip(ids, acc_ids):
        _call(st.base + "/api/queue/account", {"id": iid, "account_id": aid, "label": accs[aid].get("label") or aid})
    mon = subprocess.Popen([PY, "-X", "utf8", os.path.join(HERE, "do-hieu-nang.py"), "theo-doi", "--moi", "5", "--nhan", a.nhan],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)
    t_start = time.time()
    _call(st.base + "/api/queue/start", {"ids": ids, "parallel": n})
    log(f"BẮT ĐẦU {a.nhan}: {n} luồng, dừng khi mỗi video >= {a.canh} cảnh hoặc sau {a.phut} phút")
    _theo_doi_va_bao_cao(st, a, ids, acc_ids, accs, prev, t_start, mon, log)


def _theo_doi_va_bao_cao(st, a, ids, acc_ids, accs, prev, t_start, mon, log):
    n = len(ids)
    # 4. theo dõi
    try:
        last = ""
        while True:
            time.sleep(20)
            items = {it["id"]: it for it in st.queue() if it["id"] in ids}
            done = [_scenes_done(it) for it in items.values()]
            states = [it.get("state") for it in items.values()]
            el = (time.time() - t_start) / 60
            line = f"{el:5.1f} phút | cảnh xong: {done} | trạng thái: {states}"
            if line != last:
                log(line)
                last = line
            if all(s in ("done", "error", "stopped") for s in states):
                log("mọi video đã kết thúc")
                break
            if min(done) >= a.canh:
                log(f"mỗi video đã xong >= {a.canh} cảnh: dừng")
                break
            if el >= a.phut:
                log(f"hết {a.phut} phút: dừng")
                break
    except KeyboardInterrupt:
        log("Ctrl+C: dừng đợt")
    _call(st.base + "/api/stop", {"ids": ids})
    for _ in range(30):
        time.sleep(2)
        if not any(it.get("state") in ("running", "waiting") for it in st.queue() if it["id"] in ids):
            break
    t_end = time.time()
    if mon is not None:
        mon.terminate()
    else:   # theo-doi do lần chạy trước mở: tắt theo dòng lệnh
        subprocess.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*do-hieu-nang.py*theo-doi*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
                       capture_output=True, creationflags=CREATE_NO_WINDOW)
    for aid, on in prev.items():
        if (accs[aid].get("enabled", True) if aid in acc_ids else False) != on or aid not in acc_ids:
            try:
                st.set_enabled(aid, on)
            except Exception as e:  # noqa: BLE001
                log("không bật lại được tài khoản", aid, e)
    log("đã trả trạng thái bật/tắt tài khoản như trước")
    # 5. báo cáo
    items = [it for it in st.queue() if it["id"] in ids]
    hours = (t_end - t_start) / 3600
    rep = [f"=== Đợt {a.nhan}: {n} luồng / {n} tài khoản, {hours * 60:.0f} phút ==="]
    tot_done, per = 0, []
    for it, aid in zip(items, acc_ids):
        scs = [sc for sc in it.get("scenes") or [] if sc.get("state") == "done" and sc.get("t0") and sc.get("t1")]
        d = [sc["t1"] - sc["t0"] for sc in scs]
        per += d
        tot_done += len(scs)
        rep.append(f"  {it['variant'][:40]:40} tk {accs[aid].get('label') or aid:6} cảnh xong {len(scs):2}  mỗi cảnh tv {statistics.median(d) if d else 0:5.0f}s  "
                   f"trạng thái {it.get('state')} {('lỗi: ' + str(it.get('error'))[:80]) if it.get('error') else ''}")
    rep.append(f"  TỔNG: {tot_done} cảnh xong trong {hours * 60:.0f} phút = {tot_done / hours if hours else 0:.0f} cảnh/giờ; "
               f"mỗi cảnh trung vị {statistics.median(per) if per else 0:.0f}s, p90 {sorted(per)[int(len(per) * .9)] if per else 0:.0f}s")
    csvs = sorted(f for f in os.listdir(OUT_DIR) if f.startswith(a.nhan + "-") and f.endswith(".csv"))
    args = [PY, "-X", "utf8", os.path.join(HERE, "do-hieu-nang.py"), "bao-cao", "--tu", dt.datetime.fromtimestamp(t_start).strftime("%Y-%m-%d %H:%M"),
            "--den", dt.datetime.fromtimestamp(t_end + 60).strftime("%Y-%m-%d %H:%M")] + (["--csv", os.path.join(OUT_DIR, csvs[-1])] if csvs else [])
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = "\n".join(rep) + "\n\n" + r.stdout + (r.stderr or "")
    out = os.path.join(OUT_DIR, f"{a.nhan}-bao-cao.txt")
    open(out, "w", encoding="utf-8").write(text)
    print(text)
    print("Đã ghi", out)


def cmd_tiep(a):
    """Bám vào đợt đang chạy: tìm mục hàng đợi của các biến thể, lấy giờ BẮT ĐẦU từ nhật ký, rồi theo dõi / dừng / báo cáo như `chay`."""
    st = Studio()
    names = [x.strip() for x in a.bien_the.split(",") if x.strip()]
    acc_ids = [x.strip() for x in a.tai_khoan.split(",") if x.strip()]
    accs = {x["id"]: x for x in st.accounts()}
    items = {it["variant"]: it for it in st.queue() if it.get("project") == a.du_an and it["variant"] in names}
    if len(items) != len(names):
        raise SystemExit("Không thấy đủ biến thể trong hàng đợi: " + ", ".join(n for n in names if n not in items))
    ids = [items[n]["id"] for n in names]
    t_start = time.time()
    nk = os.path.join(OUT_DIR, f"{a.nhan}-nhat-ky.txt")
    if os.path.exists(nk):
        for ln in open(nk, encoding="utf-8"):
            if "BẮT ĐẦU" in ln:
                hh, mm, ss = ln[:8].split(":")
                t_start = time.mktime(dt.datetime.now().replace(hour=int(hh), minute=int(mm), second=int(ss)).timetuple())
    log_f = open(nk, "a", encoding="utf-8")

    def log(*s):
        msg = f"{dt.datetime.now():%H:%M:%S} " + " ".join(str(x) for x in s)
        print(msg)
        log_f.write(msg + "\n")
        log_f.flush()
    prev = {aid: True for aid in accs}   # cuối đợt bật lại mọi tài khoản
    log(f"TIẾP {a.nhan}: bám vào đợt đã bắt đầu lúc {dt.datetime.fromtimestamp(t_start):%H:%M:%S}, dừng khi mỗi video >= {a.canh} cảnh hoặc sau {a.phut} phút")
    _theo_doi_va_bao_cao(st, a, ids, acc_ids, accs, prev, t_start, None, log)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tai-khoan")
    sub.add_parser("khoi-dong-lai")
    d = sub.add_parser("don-dep")
    d.add_argument("--du-an", required=True)
    d.add_argument("--bien-the", required=True)
    d.add_argument("--nhan", default="don-dep")
    t = sub.add_parser("tiep", help="bám vào đợt đang chạy (do lệnh chay trước đó mở) với mốc dừng mới")
    t.add_argument("--nhan", required=True)
    t.add_argument("--du-an", required=True)
    t.add_argument("--bien-the", required=True)
    t.add_argument("--tai-khoan", required=True)
    t.add_argument("--canh", type=int, default=18)
    t.add_argument("--phut", type=float, default=60)
    c = sub.add_parser("chay")
    c.add_argument("--nhan", required=True)
    c.add_argument("--du-an", required=True)
    c.add_argument("--bien-the", required=True)
    c.add_argument("--tai-khoan", required=True)
    c.add_argument("--canh", type=int, default=10)
    c.add_argument("--phut", type=float, default=45)
    a = ap.parse_args()
    if a.cmd == "tai-khoan":
        cmd_tai_khoan(Studio())
    elif a.cmd == "khoi-dong-lai":
        cmd_khoi_dong_lai()
    elif a.cmd == "don-dep":
        don_dep(a.du_an, [x.strip() for x in a.bien_the.split(",") if x.strip()], a.nhan)
    elif a.cmd == "tiep":
        cmd_tiep(a)
    else:
        cmd_chay(a)


if __name__ == "__main__":
    main()
