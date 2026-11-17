"""Cầu nối LUO Studio <-> Claude CLI: người dùng chỉ đưa video gốc, Studio tự chạy `claude -p` với prompt cố định
(quy trình skill luo-video-moi), cho phép nhiều video chạy song song, theo dõi nhật ký trực tiếp, gửi góp ý nối tiếp cùng phiên (--resume).

Mỗi "việc" (job) = một video: DATA/claude/<id>/job.json + log.jsonl. Tiến trình `claude` chạy với thư mục gốc dự án làm cwd để đọc
.claude/skills, SAMPLE/_chung/SO-TAY-KY-THUAT.md và bộ nhớ của dự án.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
VIDEO_EXT = (".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi")
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")

LOCK = threading.RLock()
_SEEN = {}         # id việc -> các id message đã cộng token tạm tính
JOBS = {}          # id -> job dict
PROCS = {}         # id -> Popen
CFG = {"dir": None, "settings": lambda: {}, "studio_url": lambda: ""}


def init(data_dir, get_settings, get_studio_url, on_done=None):
    CFG["on_done"] = on_done
    CFG["dir"] = os.path.join(data_dir, "claude")
    CFG["settings"] = get_settings
    CFG["studio_url"] = get_studio_url
    os.makedirs(CFG["dir"], exist_ok=True)
    for d in os.listdir(CFG["dir"]):
        try:
            j = json.load(open(os.path.join(CFG["dir"], d, "job.json"), encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if j.get("state") in ("running", "queued"):
            j["state"] = "stopped"
            j["note"] = "Studio đã tắt giữa chừng. Bấm 'Chạy lại' hoặc gửi góp ý để làm tiếp cùng phiên."
        JOBS[j["id"]] = j


def _jdir(jid):
    return os.path.join(CFG["dir"], jid)


def _save(j):
    d = _jdir(j["id"])
    os.makedirs(d, exist_ok=True)
    tmp = os.path.join(d, "job.json.tmp")
    json.dump(j, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(d, "job.json"))


def claude_exe():
    """Đường dẫn claude CLI: cài đặt > PATH > vị trí WinGet/npm quen thuộc."""
    p = (CFG["settings"]().get("claude_path") or "").strip()
    if p and os.path.exists(p):
        return p
    w = shutil.which("claude")
    if w:
        return w
    cands = []
    la = os.environ.get("LOCALAPPDATA", "")
    ap = os.environ.get("APPDATA", "")
    hm = os.path.expanduser("~")
    for base in (os.path.join(la, "Microsoft", "WinGet", "Packages"),):
        if os.path.isdir(base):
            for d in os.listdir(base):
                if d.startswith("Anthropic.ClaudeCode"):
                    cands.append(os.path.join(base, d, "claude.exe"))
    if os.name != "nt":
        cands += [os.path.join(hm, ".local", "bin", "claude"), os.path.join(hm, ".claude", "local", "claude"), os.path.join(hm, ".npm-global", "bin", "claude"),
                  "/usr/local/bin/claude", "/usr/bin/claude", "/opt/homebrew/bin/claude"]
    cands += [os.path.join(ap, "npm", "claude.cmd"), os.path.join(hm, ".local", "bin", "claude.exe"), os.path.join(hm, ".claude", "local", "claude.exe")]
    return next((c for c in cands if os.path.exists(c)), "")


def status():
    exe = claude_exe()
    if not exe:
        return {"ok": False, "error": "Không tìm thấy Claude CLI. Cài Claude Code rồi đăng nhập (chạy `claude` một lần), hoặc điền đường dẫn trong Cài đặt."}
    try:
        r = subprocess.run([exe, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
        return {"ok": r.returncode == 0, "version": r.stdout.strip(), "path": exe, "error": "" if r.returncode == 0 else (r.stderr.strip()[:200] or "lỗi")}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "path": exe, "error": str(e)[:200]}


# ------------------------------------------------------------------ prompt cố định
def python_cmd():
    p = os.path.join(ROOT, "runtime", "python.exe")
    return p if os.path.exists(p) else sys.executable


def prompt_new(j):
    opts = j["opts"]
    refs = j.get("images") or []
    lines = [
        "Bạn đang chạy NGẦM bên trong LUO Studio (không có người ngồi trả lời). Hãy làm đúng quy trình của skill `luo-video-moi`:",
        "đọc `.claude/skills/luo-video-moi/SKILL.md` và `SAMPLE/_chung/SO-TAY-KY-THUAT.md` rồi làm từ Bước 1 đến Bước 6.",
        "",
        f"VIDEO THAM CHIẾU: {j['video']}",
        f"Tên gợi ý cho thể loại/dự án: {j['name']}",
        f"Python của Studio: {python_cmd()} (đặt PYTHONIOENCODING=utf-8). Studio đang chạy tại {CFG['studio_url']()} (userdata/running.json).",
    ]
    if refs:
        lines.append("ẢNH THAM CHIẾU NHÂN VẬT do người dùng cung cấp (dùng làm `refs`, không cắt ảnh từ video mẫu):\n" + "\n".join("  - " + x for x in refs))
    else:
        lines.append("Người dùng KHÔNG cung cấp ảnh tham chiếu nhân vật: bạn phải tự gen (xem quy tắc ảnh `refs` bên dưới).")
    extra = j.get("extra") or []
    if extra:
        lines.append("ẢNH THAM CHIẾU THÊM do người dùng đính kèm (hãy Read từng ảnh; dùng để hiểu bối cảnh/phong cách/vật dụng/ý muốn theo phần 'Yêu cầu thêm'; "
                     "KHÔNG coi là ảnh nhân vật `refs` trừ khi phần yêu cầu thêm nói rõ):\n" + "\n".join("  - " + x for x in extra))
    if opts.get("lang"):
        lines.append(f"Ngôn ngữ lời thoại của video mới: {opts['lang']}.")
    if opts.get("note"):
        lines.append("Yêu cầu thêm của người dùng: " + opts["note"])
    lines += [
        "",
        "QUY TẮC KHI CHẠY NGẦM:",
        "- Không hỏi lại người dùng. Việc nào cần quyết thì chọn phương án an toàn nhất (khuôn ghép 2 lớp, không đổi bố cục video gốc) và ghi lý do vào README.",
        f"- Số biến thể viết: {opts.get('variants', 3)}.",
    ]
    lines += [
        "- ẢNH `refs` (mọi nhân vật + bối cảnh cần ảnh riêng): dùng ảnh người dùng cung cấp ở trên nếu có. Nhân vật/bối cảnh nào CHƯA có ảnh thì TỰ GEN bằng Muse, "
        "KHÔNG cắt từ video mẫu và KHÔNG chờ người dùng: chạy "
        f"`{python_cmd()} SAMPLE\\_chung\\gen-anh-nhan-vat.py --ra SAMPLE\\<mã>\\anh --nv <KHOÁ> \"<mô tả tiếng Anh: tuổi, giới, tóc, trang phục, thần thái>\" [--nv ...] [--bc <KHOÁ> \"<mô tả bối cảnh>\"]`. "
        "Nhân vật được gen trên NỀN XANH LỤC PHẲNG (kịch bản dặn bỏ nền khi dùng ảnh nền xanh), bối cảnh gen không có người. "
        "Mô tả phải khớp với `NGUOI_<KHOÁ>` trong biến thể. Gen xong Read từng ảnh kiểm tra (một người, đúng giới/tuổi, nền xanh phẳng, không chữ); hỏng thì gen lại (tối đa 2 lần). "
        "Rồi điền đường dẫn ảnh (tương đối từ thư mục gốc repo) vào `refs` của biến thể. Robot/nhân vật đã có ảnh trong SAMPLE của thể loại gần nhất thì dùng lại, không gen mới.",
    ]
    if opts.get("trial", True):
        lines.append("- Sau khi `kiem-tra` hết LỖI và đã có đủ ảnh `refs`, chạy `video-moi.py nhap ... --chay-thu` để chạy thử biến thể ĐẦU TIÊN trong Studio, "
                     "theo dõi tới khi xong cảnh đầu và tự xem khung đầu + clip cảnh 1 (Bước 5). Biến thể này là 'biến thể test' để người dùng xem và góp ý. "
                     "KHÔNG ngồi chờ cả video gen xong (mất nhiều phút, tốn lượt): sau khi cảnh 1 đạt thì báo cáo `[XONG]` ngay, Studio tự theo dõi tiến độ gen và báo hoàn tất khi video test xong.")
    else:
        lines.append("- Người dùng không muốn chạy thử: chỉ `nhap` (không `--chay-thu`).")
    lines += [
        "- Mỗi khi đổi sang bước mới, in MỘT dòng bắt đầu bằng `[BUOC n/6] ` mô tả đang làm gì (để giao diện hiện tiến độ). Bước: 1 Phân tích video, 2 Chọn khuôn, 3 Viết kịch bản + biến thể, 4 Kiểm tra + gen ảnh nhân vật, 5 Nhập Studio + chạy thử, 6 Báo cáo.",
        "- Chỉ sửa file của thể loại mới (SAMPLE/<mã>/, app/production/types/<mã>/); chỉ THÊM mục vào NHAT-KY-TRI-THUC.md. Không sửa mã dùng chung.",
        "- Chỉ dùng `[CAN-NGUOI]` khi thật sự bế tắc (Muse hết tài khoản, API Studio không chạy); thiếu ảnh thì tự gen chứ không dùng `[CAN-NGUOI]`.",
        "- Kết thúc bằng báo cáo ngắn theo Bước 6, dòng đầu là `[XONG] <mã thể loại> | <tên dự án trong Studio> | <id dự án> | <tên biến thể test hoặc 'chưa gen'>`.",
    ]
    return "\n".join(lines)


def prompt_check(j):
    return ("Hãy TỰ KIỂM TRA kết quả chạy thử của video này trong Studio (Bước 5 của skill `luo-video-moi`): "
            "xem trạng thái hàng đợi/dự án trong Studio, mở `userdata/studio/runs/<dự án>/<biến thể>/` xem scene*_start.png và clip các cảnh đã xong; "
            "đối chiếu với bảng hành động trong PHAN-TICH-VIDEO-MAU.md. Nêu lỗi cụ thể (nhân vật sai/lệch bố cục, hai người cùng nói, vật dụng sai, chữ lạ, nối khung khựng), "
            "rồi SỬA TẠI CHỖ kịch bản/biến thể của dự án cũ (không tạo dự án v2), cập nhật dự án trong Studio và chỉ làm lại đúng cảnh đổi (redo cảnh, không gen lại cả clip). "
            "Ghi mục vào NHAT-KY-TRI-THUC.md (Bước 5b). Không hỏi lại người dùng. Dòng đầu báo cáo: `[XONG] ...` hoặc `[CAN-NGUOI] <điều cần người dùng làm>`.")


def prompt_feedback(text, regen=False):
    s = ("GÓP Ý CỦA NGƯỜI DÙNG sau khi xem kết quả thử:\n" + text.strip() + "\n\n"
         "Làm theo quy tắc 'sửa tại chỗ': sửa kịch bản/biến thể của dự án cũ (kể cả loại dự án nếu kịch bản đổi) và cập nhật dự án trong Studio, "
         "không tạo dự án v2, không đổi bố cục video gốc nếu chưa hỏi. Ghi NHAT-KY-TRI-THUC.md. "
         "Nếu góp ý có ĐƯỜNG DẪN ẢNH: mở từng ảnh bằng Read, chép vào thư mục anh/ của dự án và gắn làm ảnh tham chiếu (refs) đúng cảnh/lượt được nêu (ảnh ở góp ý tổng thì gắn cho nhân vật/nền liên quan). ")
    if regen:
        s += ("KHÔNG tự thêm vào hàng đợi hay chạy gen: sau khi bạn báo xong, Studio sẽ tự GEN LẠI TOÀN BỘ biến thể test. "
              "Chỉ gen lại ảnh nhân vật (gen-anh-nhan-vat.py) nếu góp ý chê ảnh nhân vật. ")
    return s + "Dòng đầu báo cáo: `[XONG] <mã> | <tên dự án> | <id dự án> | <tên biến thể test>` hoặc `[CAN-NGUOI] ...`."


# ------------------------------------------------------------------ chạy tiến trình
def _log(j, kind, text):
    rec = {"t": round(time.time(), 1), "k": kind, "x": text}
    with LOCK:
        j["nlog"] = j.get("nlog", 0) + 1
        with open(os.path.join(_jdir(j["id"]), "log.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _short(v, n=160):
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n] + "…"


def _infer_step(text):
    """Đoán bước (1-5) từ lệnh/tệp Claude đang đụng tới, khi Claude quên in dòng [BUOC n/6]. Chỉ dùng để tăng, không bao giờ lùi."""
    s = text.lower()
    if "video-moi.py" in s and " nhap" in s or "chay-thu" in s or "/api/queue" in s or "studio/runs" in s or "studio\\runs" in s:
        return 5
    if "gen-anh-nhan-vat" in s or "kiem-tra" in s:
        return 4
    if "kich-ban" in s or "bien-the" in s or "tao_bien_the" in s or "tao_kich_ban" in s or "phan-tich-video-mau" in s:
        return 3
    if "danh-gia" in s or "phan-tich-video" in s or "luot_" in s or "tong-quan" in s or "chuyen-dong_" in s:
        return 1
    return 0


def _handle_event(j, ev):
    t = ev.get("type")
    if ev.get("session_id"):
        j["session"] = ev["session_id"]
    if t == "assistant":
        for b in (ev.get("message") or {}).get("content") or []:
            if b.get("type") == "text" and b.get("text", "").strip():
                txt = b["text"].strip()
                _log(j, "say", txt)
                for ln in txt.splitlines():
                    m = re.match(r"\[BUOC (\d+)/\d+\]\s*(.*)", ln)
                    if m:
                        j["step"] = ln[:140]
                        j["step_n"] = int(m.group(1))
                        j.setdefault("steps", {})[m.group(1)] = m.group(2)[:120]
            elif b.get("type") == "tool_use":
                inp = b.get("input") or {}
                what = _short(inp.get("command") or inp.get("file_path") or inp.get("pattern") or inp)
                _log(j, "tool", f"{b.get('name')}: " + what)
                j["activity"], j["act_t"] = f"{b.get('name')}: {what}"[:140], time.time()
                n = _infer_step(str(inp.get("command") or "") + " " + str(inp.get("file_path") or ""))
                if n > (j.get("step_n") or 0):
                    j["step_n"] = n
        # token tạm tính theo từng lượt (mỗi message một lần): cộng vào "live" của lần chạy hiện tại
        msg = ev.get("message") or {}
        u, mid = msg.get("usage") or {}, msg.get("id")
        seen = _SEEN.setdefault(j["id"], set())
        if u and mid and mid not in seen:
            seen.add(mid)
            lv = j.get("live") or {"in": 0, "out": 0, "cw": 0, "cr": 0}
            j["live"] = lv
            lv["in"] += u.get("input_tokens", 0) or 0
            lv["out"] += u.get("output_tokens", 0) or 0
            lv["cw"] += u.get("cache_creation_input_tokens", 0) or 0
            lv["cr"] += u.get("cache_read_input_tokens", 0) or 0
    elif t == "user":   # kết quả công cụ: lệnh `nhap` in "Đã tạo dự án <id> với N biến thể" -> gắn dự án ngay để thẻ hiện tiến độ gen khi Claude còn đang chạy
        for b in (ev.get("message") or {}).get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_result":
                c = b.get("content")
                txt = c if isinstance(c, str) else " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))
                m = re.search(r"Đã tạo dự án (\S+) với", txt or "")
                if m:
                    j["project_id"] = m.group(1)
    elif t == "result":
        j["result"] = ev.get("result") or ""
        j["is_error"] = bool(ev.get("is_error"))
        j["cost"] = round((j.get("cost") or 0) + (ev.get("total_cost_usd") or 0), 3)
        u = ev.get("usage") or {}
        j.setdefault("runs", []).append({"kind": j.get("cur_kind", "new"), "t": round(time.time()), "cost": round(ev.get("total_cost_usd") or 0, 4),
                                         "in": u.get("input_tokens", 0) or 0, "out": u.get("output_tokens", 0) or 0,
                                         "cw": u.get("cache_creation_input_tokens", 0) or 0, "cr": u.get("cache_read_input_tokens", 0) or 0,
                                         "turns": ev.get("num_turns", 0) or 0, "ms": ev.get("duration_ms", 0) or 0})
        j["live"] = None
        _SEEN.pop(j["id"], None)


def _run(j, prompt):
    exe = claude_exe()
    if not exe:
        j["state"], j["note"] = "error", status()["error"]
        _save(j)
        return
    cmd = [exe, "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "acceptEdits",
           "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep", "Bash", "--add-dir", ROOT]
    for d in {os.path.dirname(j["video"]), uploads_dir()} | {os.path.dirname(x) for x in j.get("images", []) + j.get("extra", [])}:
        if d and os.path.isdir(d):
            cmd += ["--add-dir", d]
    mdl = (CFG["settings"]().get("claude_model") or "").strip()
    if mdl:
        cmd += ["--model", mdl]
    if j.get("session"):
        cmd += ["--resume", j["session"]]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", NO_COLOR="1")
    j["state"], j["note"], j["started"] = "running", "", time.time()
    j["step"] = j.get("step") or "Đang khởi động Claude…"
    _save(j)
    _log(j, "sys", "Bắt đầu: " + ("tiếp tục phiên" if j.get("session") else "phiên mới"))
    try:
        p = subprocess.Popen(cmd, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        PROCS[j["id"]] = p
        p.stdin.write(prompt.encode("utf-8"))
        p.stdin.close()
        errbuf = []
        threading.Thread(target=lambda: [errbuf.append(l.decode("utf-8", "replace")) for l in p.stderr], daemon=True).start()
        for raw in p.stdout:
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            try:
                _handle_event(j, json.loads(line))
            except ValueError:
                _log(j, "sys", line[:300])
            if j["nlog"] % 5 == 0:
                _save(j)
        p.wait()
        if j.get("state") == "stopping":
            j["state"], j["note"] = "stopped", "Đã dừng."
        elif p.returncode != 0 and not j.get("result"):
            j["state"], j["note"] = "error", ("".join(errbuf)[-400:] or f"Claude thoát mã {p.returncode}")
        else:
            r = (j.get("result") or "").strip()
            j["state"] = "needs_user" if "[CAN-NGUOI]" in r else ("error" if j.get("is_error") else "done")
            j["note"] = next((l for l in r.splitlines() if l.startswith("[XONG]") or l.startswith("[CAN-NGUOI]")), r[:200])
            if j["note"].startswith("[XONG]"):   # [XONG] <mã> | <tên dự án> | <id dự án> | <biến thể test>
                f = [x.strip() for x in j["note"][6:].split("|")]
                j["type_id"], j["project_name"] = (f + ["", ""])[0], (f + ["", ""])[1]
                if len(f) > 2:
                    j["project_id"] = f[2]
                if len(f) > 3 and f[3] and f[3].lower() not in ("chưa gen", "chua gen"):
                    j["variant"] = re.split(r"\s*[\(\[]", f[3])[0].strip()   # bỏ chú thích kiểu "tên (đang chạy thử…)"
    except Exception as e:  # noqa: BLE001
        j["state"], j["note"] = "error", str(e)[:300]
    finally:
        PROCS.pop(j["id"], None)
        j["ended"] = time.time()
        j["step"] = ""
        try:
            if CFG.get("on_done"):
                CFG["on_done"](j)   # Studio liên kết dự án test, và tự gen lại toàn bộ nếu việc này là "gen lại toàn bộ"
        except Exception as e:  # noqa: BLE001
            _log(j, "sys", "Lỗi xử lý sau khi xong: " + str(e)[:200])
        _log(j, "sys", f"Kết thúc: {j['state']}")
        _save(j)
        _pump()


def _max_parallel():
    try:
        return max(1, int(CFG["settings"]().get("claude_parallel") or 2))
    except (TypeError, ValueError):
        return 2


def _pump():
    """Cho các việc đang xếp hàng chạy khi còn chỗ (tối đa claude_parallel tiến trình cùng lúc)."""
    with LOCK:
        busy = sum(1 for x in JOBS.values() if x["state"] in ("running", "stopping"))
        for j in sorted((x for x in JOBS.values() if x["state"] == "queued"), key=lambda x: x["created"]):
            if busy >= _max_parallel():
                break
            prompt = j.pop("_prompt", None)
            if not prompt:
                j["state"] = "error"
                j["note"] = "Thiếu prompt"
                continue
            j["state"] = "running"
            busy += 1
            threading.Thread(target=_run, args=(j, prompt), daemon=True).start()


def _enqueue(j, prompt):
    j["state"], j["note"] = "queued", ""
    j["_prompt"] = prompt
    _save({k: v for k, v in j.items() if k != "_prompt"})
    _pump()


# ------------------------------------------------------------------ API
def uploads_dir():
    d = os.path.join(CFG["dir"], "_uploads")
    os.makedirs(d, exist_ok=True)
    return d


def create(videos, images=None, opts=None, name=None, extra=None):
    """Mỗi video = một việc riêng, chạy song song theo giới hạn. videos: danh sách đường dẫn file."""
    opts = {"variants": 3, "trial": True, "lang": "", "note": "", **(opts or {})}
    out = []
    for v in videos:
        v = os.path.abspath(v)
        if not os.path.isfile(v) or not v.lower().endswith(VIDEO_EXT):
            raise ValueError(f"Không phải file video: {v}")
        base = os.path.splitext(os.path.basename(v))[0]
        j = {"id": uuid.uuid4().hex[:10], "video": v, "name": (name if name and len(videos) == 1 else base)[:60], "images": [os.path.abspath(i) for i in (images or []) if i], "extra": [os.path.abspath(i) for i in (extra or []) if i],
             "opts": opts, "created": time.time(), "state": "queued", "note": "", "session": "", "nlog": 0, "cost": 0, "cur_kind": "new", "runs": []}
        os.makedirs(_jdir(j["id"]), exist_ok=True)
        with LOCK:
            JOBS[j["id"]] = j
        _enqueue(j, prompt_new(j))
        out.append(j["id"])
    return out


def _pub(j):
    return {k: v for k, v in j.items() if not k.startswith("_")}


def list_jobs():
    with LOCK:
        return sorted((_pub(j) for j in JOBS.values()), key=lambda x: -x["created"])


def get(jid, since=0):
    j = JOBS.get(jid)
    if not j:
        return None
    lines = []
    try:
        with open(os.path.join(_jdir(jid), "log.jsonl"), encoding="utf-8") as f:
            for i, l in enumerate(f):
                if i >= since:
                    lines.append(json.loads(l))
    except OSError:
        pass
    return {**_pub(j), "log": lines, "since": since}


def _busy(j):
    return j["state"] in ("running", "stopping", "queued")


def send(jid, kind, text="", regen=False):
    j = JOBS.get(jid)
    if not j:
        raise ValueError("Không có việc này")
    if _busy(j):
        raise ValueError("Việc đang chạy, chờ xong hoặc bấm Dừng trước")
    if kind == "check":
        p = prompt_check(j)
    elif kind == "feedback":
        if not text.strip():
            raise ValueError("Góp ý trống")
        p = prompt_feedback(text, regen)
        _log(j, "user", text.strip())
        j["regen"] = bool(regen)
    elif kind == "retry":
        p = prompt_new(j) if not j.get("session") else "Tiếp tục công việc đang dở theo đúng quy trình, đến hết Bước 6."
    elif kind == "restart":   # phân tích LẠI từ đầu: phiên mới, bước về 0
        old = j.get("project_id") or ""
        j["session"], j["step_n"], j["steps"], j["step"] = "", 0, {}, ""
        p = prompt_new(j)
        if old:
            p += (f"\n\nĐÂY LÀ LẦN PHÂN TÍCH LẠI. Dự án `{old}` (thể loại `{j.get('type_id', '')}`) đã tạo từ lần trước: hãy phân tích kỹ hơn rồi CẬP NHẬT kịch bản/biến thể/dự án cũ này "
                  "(sửa tại chỗ, không tạo dự án trùng); chỉ làm lại phần gen nếu kịch bản đổi.")
        _log(j, "sys", "Phân tích lại từ đầu")
    else:
        raise ValueError("Loại yêu cầu không hợp lệ")
    j["result"] = ""
    j["cur_kind"] = "regen" if (kind == "feedback" and regen) else kind
    if kind in ("feedback", "check"):   # lần chạy mới: tiến trình các bước đếm lại từ đầu
        j["step_n"], j["steps"] = 0, {}
    _enqueue(j, p)


def stop(jid):
    j = JOBS.get(jid)
    if not j:
        return
    if j["state"] == "queued":
        j["state"], j["note"] = "stopped", "Đã bỏ khỏi hàng."
        j.pop("_prompt", None)
        _save(j)
        return
    p = PROCS.get(jid)
    if p and j["state"] == "running":
        j["state"] = "stopping"
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, creationflags=0x08000000)
            else:
                p.kill()
        except Exception:  # noqa: BLE001
            pass


def delete(jid):
    stop(jid)
    with LOCK:
        JOBS.pop(jid, None)
    shutil.rmtree(_jdir(jid), ignore_errors=True)
