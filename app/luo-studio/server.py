"""LUO Studio - máy chủ cục bộ (stdlib) + bộ chạy job. Không cần cài thêm gói nào ngoài numpy/faster-whisper đã có."""
import base64, json, mimetypes, os, re, shutil, subprocess, sys, threading, time, unicodedata, urllib.error, urllib.parse, urllib.request, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

if os.name == "nt":  # không bật cửa sổ console khi gọi ffmpeg/python con (chạy bằng pythonw)
    _popen_init = subprocess.Popen.__init__

    def _popen_nowin(self, *a, **k):
        k.setdefault("creationflags", 0x08000000)
        _popen_init(self, *a, **k)
    subprocess.Popen.__init__ = _popen_nowin

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("LUO_STUDIO_DATA") or os.path.join(HERE, "data")   # bản đóng gói đặt dữ liệu người dùng ngoài thư mục mã nguồn
PROJ = os.path.join(DATA, "projects")
TYPES = os.path.join(DATA, "types")
RUNS = os.path.join(DATA, "runs")
TPL = os.path.join(HERE, "templates")
UI = os.path.join(HERE, "ui")
PRODUCTION = os.path.abspath(os.path.join(HERE, "..", "production"))
for d in (PROJ, RUNS, TYPES):
    os.makedirs(d, exist_ok=True)

import engine as E  # noqa: E402
import face_mesh as FM  # noqa: E402

LOCK = threading.RLock()
DEFAULT_SETTINGS = {"api_url": os.environ.get("LUO_API_URL", "http://127.0.0.1:18610"), "api_key": "", "timeout": 900, "retries": 2, "cut": True, "speedfix": True, "normalize": True, "check_overlap": True, "mouth_note": "", "overlap_retries": 2, "mouth_sens": "normal", "precise_cut": True, "fx_hook": True, "cut_margin": 0.5, "voice_split": True, "export_dir": "", "speed_max": 1.25, "chat_every": 1, "parallel": 1, "fx_ding": False, "fx_pop": False,
                    "logo": "", "endcard": "", "topbar": "", "whisper": "auto"}

# ------------------------------------------------------------------ lưu trữ
def jread(path, default=None):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default


def jwrite(path, obj):
    tmp = path + ".tmp"
    json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def settings():
    s = dict(DEFAULT_SETTINGS)
    s.update(jread(os.path.join(DATA, "settings.json"), {}) or {})
    if os.environ.get("LUO_API_URL"):  # launcher đã bật LUO-API và chọn cổng thật (cổng 18610 có thể bị chiếm): cổng cũ lưu trong settings.json không được ghi đè
        s["api_url"] = os.environ["LUO_API_URL"]
    return s


def api_key():
    k = settings().get("api_key", "").strip()
    return k or E.G.read_key()


def slug(s):
    s = unicodedata.normalize("NFKD", str(s).strip().replace("đ", "d").replace("Đ", "D")).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w.-]+", "-", s).strip("-")
    return s[:60] or "item"


BUILTIN = {
    "talka-phone": {"name": "Điện thoại + người học", "file": "talka-phone.txt", "defaults": {"POS_DAY": "RIGHT", "POS_HOC": "LEFT"},
                    "turns": {"day_label": "Robot dạy (trong điện thoại)", "hoc_label": "Người học"},
                    "labels": {"NEN_TRAI": "Căn phòng, bàn", "NEN_PHAI": "Nền màn hình điện thoại"}},
    "split-doi-thoai": {"name": "Chia đôi 2 nhân vật", "file": "split-doi-thoai.txt", "defaults": {"POS_DAY": "LEFT", "POS_HOC": "RIGHT"},
                        "turns": {"day_label": "Người dạy (bên trái)", "hoc_label": "Người học (bên phải)"}, "labels": {}},
}


def type_path(tid):
    return os.path.join(TYPES, slug(tid) + ".json")


def list_types():
    out = []
    for f in sorted(os.listdir(TYPES)):
        if f.endswith(".json"):
            t = jread(os.path.join(TYPES, f))
            if t:
                out.append(t)
    return out


def get_type(tid):
    return jread(type_path(tid)) or {"id": tid, "name": tid, "scenes": 0, "fields": [], "series": {}, "turns": {}, "defaults": {}}


def type_text(tid):
    return open(os.path.join(TYPES, slug(tid) + ".txt"), encoding="utf-8").read()


template_text = type_text


def _finish_type(t, script):
    an = E.analyze_script(script)
    if not an["scenes"]:
        raise ValueError('Script không có cảnh nào (cần các dòng dạng "CẢNH 1 (0:00–0:05): Tiêu đề")')
    t["scenes"] = an["scenes"]
    t["series"] = an["series"]
    t["fields"] = E.suggest_fields(an["plain"], "LUOT" in an["series"], t.get("fields"))
    t.setdefault("turns", {})
    t["turns"].setdefault("day_label", "Người dạy")
    t["turns"].setdefault("hoc_label", "Người học")
    t.setdefault("defaults", {})
    if "LUOT" in an["series"]:
        t["defaults"].setdefault("POS_DAY", "LEFT")
        t["defaults"].setdefault("POS_HOC", "RIGHT")
    open(os.path.join(TYPES, slug(t["id"]) + ".txt"), "w", encoding="utf-8").write(script)
    t["updated"] = int(time.time())
    jwrite(type_path(t["id"]), t)
    return t


def create_type(b):
    script = b.get("script", "")
    name = (b.get("name") or "").strip() or "Loại mới"
    t = {"id": slug(name) + "-" + uuid.uuid4().hex[:4], "name": name, "builtin": False, "fields": b.get("fields") or [], "turns": b.get("turns") or {},
         "defaults": b.get("defaults") or {}, "created": int(time.time())}
    return _finish_type(t, script)


def update_type(tid, b):
    t = jread(type_path(tid))
    if not t:
        raise ValueError("Không tìm thấy loại dự án")
    for k in ("name", "fields", "turns", "defaults"):
        if k in b:
            t[k] = b[k]
    return _finish_type(t, b.get("script") or type_text(tid))


def refresh_builtin_scripts():
    """Script có sẵn trong templates\ được cập nhật (prompt mới) -> cập nhật loại dự án có sẵn tương ứng, giữ nguyên nhãn trường đã sửa."""
    for tid, c in BUILTIN.items():
        t = jread(type_path(tid))
        if not t:
            continue
        script = open(os.path.join(TPL, c["file"]), encoding="utf-8").read()
        try:
            same = type_text(tid) == script
        except OSError:
            same = False
        if not same:
            _finish_type(t, script)


def seed_types():
    if list_types():
        refresh_builtin_scripts()
        return
    for tid, c in BUILTIN.items():
        script = open(os.path.join(TPL, c["file"]), encoding="utf-8").read()
        an = E.analyze_script(script)
        fields = E.suggest_fields(an["plain"], "LUOT" in an["series"])
        for f in fields:
            if f["key"] in c["labels"]:
                f["label"] = c["labels"][f["key"]]
        _finish_type({"id": tid, "name": c["name"], "builtin": True, "fields": fields, "turns": c["turns"], "defaults": c["defaults"], "created": int(time.time())}, script)


def blank_variant(tid, name="Biến thể 1"):
    t = get_type(tid)
    v = {"name": name}
    for f in t["fields"]:
        v[f["key"]] = f.get("default", "")
    for pre, n in t.get("series", {}).items():
        v[pre] = [] if pre == "LUOT" else [""] * n
    v.update(t.get("defaults", {}))
    return v


def new_project(name, tid, variants=None):
    pid = slug(name) + "-" + uuid.uuid4().hex[:4]
    p = {"id": pid, "name": name, "template": tid, "variants": variants or [blank_variant(tid)], "refs": [], "created": int(time.time())}
    for v in p["variants"]:
        for k, val in get_type(tid).get("defaults", {}).items():
            v.setdefault(k, val)
    save_project(p)
    return p


def seed():
    seed_types()
    if any(f.endswith(".json") for f in os.listdir(PROJ)):
        return
    for fname, tid, name in (("talka-phone.json", "talka-phone", "Talka - nấu ăn"), ("langlearn-turns.json", "split-doi-thoai", "LangLearn - chia đôi")):
        src = jread(os.path.join(PRODUCTION, "variants", fname))
        if src:
            new_project(name, tid, src)


def project_path(pid):
    return os.path.join(PROJ, slug(pid) + ".json")


def load_project(pid):
    return jread(project_path(pid))


def save_project(p):
    p["updated"] = int(time.time())
    jwrite(project_path(p["id"]), p)


def project_summary(p):
    return {"id": p["id"], "name": p["name"], "template": p["template"], "variants": len(p["variants"]), "updated": p.get("updated", 0),
            "turns": max((len(v.get("LUOT", [])) for v in p["variants"]), default=0)}


# ------------------------------------------------------------------ hàng đợi
# Mỗi mục = một biến thể cần gen (kind "gen") hoặc một lần hậu kỳ (kind "post"). Người dùng thêm vào hàng đợi, sang tab Chạy tick và bấm Bắt đầu.
QUEUE = []
BATCH = {"state": "idle", "started": 0.0, "ended": 0.0, "ids": [], "parallel": 1}
QUOTA = {"hit": 0.0}   # lần cuối Muse báo hết hạn mức
ICANCEL = {}     # id mục đang chạy -> ItemCancel (dừng riêng một mục)
PENDING = []     # id mục đang chờ luồng trống (thứ tự bấm chạy)
ACTIVE = set()   # id mục đang chạy (gen chiếm luồng; hậu kỳ chạy riêng, không chiếm luồng)


class ItemCancel:
    def __init__(self):
        self.ev = threading.Event()

    def is_set(self):
        return self.ev.is_set()

QFILE = os.path.join(DATA, "queue.json")


def run_dir(pid, vname):
    return os.path.join(RUNS, slug(pid), slug(vname))


def busy():
    return bool(ACTIVE or PENDING)


def qsave():
    with LOCK:
        keep = [{k: v for k, v in it.items() if k != "log"} for it in QUEUE]
    try:
        jwrite(QFILE, {"items": keep})
    except OSError:
        pass


def qload():
    d = jread(QFILE, {}) or {}
    for it in d.get("items", []):
        if it.get("state") == "running":
            it["state"] = "stopped"
        elif it.get("state") == "waiting":
            it["state"] = "queued"
        it["log"] = []
        QUEUE.append(it)


def qfind(iid):
    return next((x for x in QUEUE if x["id"] == iid), None)


def qlog(it, msg, level="info"):
    with LOCK:
        it["log"].append({"t": time.strftime("%H:%M:%S"), "msg": msg, "level": level})
        del it["log"][:-120]


def queue_add(pid, names):
    p = load_project(pid)
    if not p:
        raise RuntimeError("Không tìm thấy dự án")
    T = get_type(p["template"])
    added = []
    with LOCK:
        for name in names:
            v = next((x for x in p["variants"] if x["name"] == name), None)
            if not v:
                continue
            old = next((x for x in QUEUE if x["kind"] == "gen" and x["project"] == pid and x["variant"] == name), None)
            if old and old["state"] == "running":
                continue
            if old:
                QUEUE.remove(old)
            total = len(v.get("LUOT", [])) or (T.get("series") or {}).get("LUOT") or T.get("scenes") or 0
            it = {"id": uuid.uuid4().hex[:8], "kind": "gen", "project": pid, "pname": p["name"], "variant": name, "state": "queued", "scenes": [], "total": total,
                  "raw": "", "final": "", "error": "", "added": time.time(), "started": 0.0, "ended": 0.0, "elapsed": 0.0, "log": []}
            QUEUE.append(it)
            added.append(it["id"])
    qsave()
    return added


def queue_remove(ids):
    with LOCK:
        for iid in ids:
            it = qfind(iid)
            if it and it["state"] != "running":
                if iid in PENDING:
                    PENDING.remove(iid)
                QUEUE.remove(it)
    qsave()


def queue_view():
    with LOCK:
        items = []
        for it in QUEUE:
            c = dict(it)
            c["log"] = it["log"][-40:]
            items.append(c)
        return {"items": items, "batch": dict(BATCH), "now": time.time(), "busy": busy()}


def _emit_for(it):
    def emit(ev, **kw):
        with LOCK:
            if ev == "scene_init":
                it["scenes"] = kw["scenes"]
            elif ev == "scene":
                sc = next((x for x in it["scenes"] if x["n"] == kw["n"]), None)
                if sc:
                    st = kw.get("state")
                    if st in ("image", "video", "cut", "done") and not sc.get("t0"):
                        sc["t0"] = time.time()
                    if st == "done":
                        sc["t1"] = time.time()
                    sc.update({k: val for k, val in kw.items() if k != "n"})
            elif ev == "item":   # thông tin của cả video (vd. tài khoản Muse đã ghim)
                it.update(kw)
            elif ev == "log":
                qlog(it, kw["msg"], kw.get("level", "info"))
    return emit


def gen_item(it, cx):
    p = load_project(it["project"])
    if not p:
        raise RuntimeError("Dự án đã bị xoá")
    v = next((x for x in p["variants"] if x["name"] == it["variant"]), None)
    if not v:
        raise RuntimeError("Biến thể đã bị xoá hoặc đổi tên")
    for k, val in get_type(p["template"]).get("defaults", {}).items():
        v.setdefault(k, val)
    s = settings()
    opts = {"api_url": s["api_url"], "api_key": api_key(), "timeout": int(s["timeout"]), "retries": int(s["retries"]), "cut": bool(s["cut"]),
            "speedfix": bool(s.get("speedfix", True)), "speed_max": float(s.get("speed_max", 1.25)), "chat_every": int(s.get("chat_every", 1)), "normalize": bool(s.get("normalize", True)), "check_overlap": effective_check_overlap(it, s), "overlap_retries": int(s.get("overlap_retries", 5)), "mouth_sens": str(s.get("mouth_sens", "normal")), "precise_cut": bool(s.get("precise_cut", True)), "voice_split": bool(s.get("voice_split", True)), "cut_margin": float(s.get("cut_margin", 0.5)),
            "only": None, "scene_notes": dict(it.get("notes") or {}), "refs": p.get("refs", []), "field_labels": {f["key"]: f.get("label", f["key"]) for f in get_type(p["template"]).get("fields", [])}, "field_groups": {f["key"]: f.get("group", "other") for f in get_type(p["template"]).get("fields", [])}, "assets_dir": os.path.join(DATA, "assets", slug(it["project"]))}
    # Một video = một tài khoản Muse: mọi cảnh ghim vào cùng tài khoản; chạy tiếp thì ưu tiên tài khoản cũ
    opts["pin"], opts["pin_prefer"] = f"video-{it['id']}", it.get("account_id")
    try:
        E.run_variant(v, template_text(p["template"]), run_dir(it["project"], it["variant"]), opts, _emit_for(it), cx)
    finally:
        E.release_pin(opts, opts["pin"])
    it["raw"] = "raw.mp4"


def safe_name(name):
    """Tên file hợp lệ trên Windows, giữ nguyên tên biến thể (vd. nam-latin-30-40-mat3)."""
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "-", str(name)).strip(" .")
    return s or "video"


def export_final(pid, vname, project_name, final):
    """Bản cuối mang TÊN BIẾN THỂ: file `<tên biến thể>.mp4` cạnh final.mp4 và một bản trong thư mục xuất (mặc định data/exports/<tên dự án>/). Dùng hard link để không tốn thêm dung lượng."""
    def put(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            os.remove(dst)
        except OSError:
            pass
        try:
            os.link(final, dst)
        except OSError:
            shutil.copy2(final, dst)
        return dst
    fn = safe_name(vname) + ".mp4"
    put(os.path.join(os.path.dirname(final), fn))
    base = settings().get("export_dir") or os.path.join(DATA, "exports")
    return put(os.path.join(base, safe_name(project_name), fn))


def _pcm(path, ss=0.0, t=None):
    """Âm thanh mono 16 kHz của file (float32 -1..1), tuỳ chọn một đoạn."""
    import numpy as np
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss else []) + ["-i", path] + (["-t", f"{t:.3f}"] if t else []) + ["-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"]
    d = E.crun(cmd, capture_output=True).stdout
    return np.frombuffer(d[: len(d) // 2 * 2], np.int16).astype(np.float32) / 32768.0


def _match_start(ref, sig, expect, span=1.0, sr=16000):
    """Vị trí (giây) trong `sig` nơi đoạn âm thanh `ref` (đầu một clip) xuất hiện, tìm quanh `expect` ± span bằng tương quan chéo chuẩn hoá. None nếu không khớp rõ."""
    import numpy as np
    lo = max(0, int((expect - span) * sr))
    hi = min(len(sig), int((expect + span) * sr) + len(ref))
    seg = sig[lo:hi]
    if len(ref) < sr // 2 or len(seg) < len(ref) or float(np.abs(ref).max()) < 0.01:
        return None
    n = 1 << (len(seg) + len(ref)).bit_length()
    corr = np.fft.irfft(np.fft.rfft(seg, n) * np.conj(np.fft.rfft(ref, n)), n)[: len(seg) - len(ref) + 1]
    cs = np.concatenate(([0.0], np.cumsum(seg.astype(np.float64) ** 2)))
    win = cs[len(ref):len(ref) + len(corr)] - cs[:len(corr)]
    ncc = corr / (np.sqrt(win * float((ref.astype(np.float64) ** 2).sum())) + 1e-9)
    i = int(np.argmax(ncc))
    return (lo + i) / sr if ncc[i] > 0.5 else None


def scene_marks(d, raw):
    """Ghi scenes.json = [{turn, start, end}] mốc (giây) của từng cảnh trong raw.mp4. Mốc dự kiến tính từ độ dài các clip scene<N>_cut.mp4 (hiệu chỉnh theo độ dài raw.mp4),
    rồi tinh chỉnh bằng cách khớp âm thanh đầu mỗi clip với raw.mp4 (độ dài clip chỉ cho mốc lệch tới ~0,7 giây ở vài cảnh, đã đo). Trả về đường dẫn file, hoặc None nếu thiếu clip."""
    try:
        clips, durs, n = [], [], 1
        while os.path.exists(os.path.join(d, f"scene{n}_cut.mp4")):
            clips.append(os.path.join(d, f"scene{n}_cut.mp4"))
            durs.append(E.video_duration(clips[-1]))
            n += 1
        total = sum(durs)
        if not durs or total <= 0 or not os.path.exists(raw):
            return None
        rawdur = E.duration(raw)
        k = rawdur / total
        if not 0.97 <= k <= 1.03:
            return None   # raw.mp4 không khớp các clip (đã sửa tay?): không dùng mốc theo cảnh
        starts, t = [], 0.0
        for du in durs:
            starts.append(t * k)
            t += du
        try:
            sig = _pcm(raw)
            for i in range(1, len(clips)):   # cảnh 1 luôn bắt đầu ở 0
                ref = _pcm(clips[i], t=2.0)
                m = _match_start(ref, sig, starts[i])
                if m is not None and abs(m - starts[i]) <= 1.0:
                    starts[i] = m
            starts = [starts[0]] + [max(starts[i], starts[i - 1] + 0.3) for i in range(1, len(starts))]   # luôn tăng dần
        except Exception:  # noqa: BLE001 - khớp âm thanh lỗi: dùng mốc tính từ độ dài clip
            pass
        marks = [{"turn": i, "start": round(starts[i], 3), "end": round(starts[i + 1] if i + 1 < len(starts) else rawdur, 3)} for i in range(len(starts))]
        path = os.path.join(d, "scenes.json")
        jwrite(path, marks)
        return path
    except (OSError, RuntimeError, ValueError):
        return None


def post_item(it, opts, cx):
    s = settings()
    p = load_project(it["project"])
    v = next(x for x in p["variants"] if x["name"] == it["variant"])
    d = run_dir(it["project"], it["variant"])
    raw, final = os.path.join(d, "raw.mp4"), os.path.join(d, "final.mp4")
    subs = E.subs_from_variant(v, auto_hook=bool(s.get("fx_hook", True)))
    jwrite(os.path.join(d, "subs.json"), subs)
    text = " ".join(u["t"] for u in subs)
    model = opts.get("whisper") or s.get("whisper", "auto")
    if model == "auto":
        model = "medium" if re.search(r"[¿¡áéíóúñüàèìòùâêôãõç]", text, re.I) else "small.en"
    cmd = [sys.executable, "-I", os.path.join(PRODUCTION, "postprocess.py"), raw, "--subs", os.path.join(d, "subs.json"), "--out", final, "--no-tighten", "--model", model]
    logo, endcard, topbar = opts.get("logo") or s["logo"], opts.get("endcard") or s["endcard"], opts.get("topbar") or s["topbar"]
    if logo and os.path.exists(logo):
        cmd += ["--logo-mov" if logo.lower().endswith((".mov", ".webm")) else "--topbar", logo]
    elif topbar and os.path.exists(topbar):
        cmd += ["--topbar", topbar]
    else:
        cmd += ["--no-topbar"]
    cmd += ["--endcard", endcard] if endcard and os.path.exists(endcard) else ["--no-endcard"]
    if opts.get("ding", s.get("fx_ding")):
        cmd.append("--ding")
    if opts.get("pop", s.get("fx_pop")):
        cmd.append("--pop")
    if s.get("fx_hook", True):
        cmd.append("--hook-fx")
    sc_file = scene_marks(d, raw)   # mốc từng cảnh trong raw.mp4: căn phụ đề theo từng cảnh (video trộn ngôn ngữ không bị lệch dây chuyền)
    if sc_file:
        cmd += ["--scenes", sc_file]
    qlog(it, "Hậu kỳ: " + os.path.basename(final))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    for line in proc.stdout:
        line = line.rstrip()
        if line and not cx.is_set():
            qlog(it, line)
        if cx.is_set():
            proc.kill()
            raise E.Cancelled()
    proc.wait()
    if proc.returncode != 0 or not os.path.exists(final):
        raise RuntimeError("Hậu kỳ lỗi, xem nhật ký")
    it["final"] = "final.mp4"
    try:
        out = export_final(it["project"], it["variant"], it.get("pname") or it["project"], final)
        it["export"] = out
        qlog(it, "Đã xuất: " + out)
    except OSError as e:
        qlog(it, f"Không xuất được bản mang tên biến thể: {e}", "warn")


def _discard_inflight(it):
    """Dừng giữa chừng: bỏ clip dở của cảnh đang gen để lần tiếp tục tạo lệnh gen mới cho đúng video đó (giữ các cảnh đã xong và ảnh khung đầu)."""
    if it.get("kind") != "gen":
        return
    cur = next((x for x in it.get("scenes", []) if x.get("state") != "done"), None)
    if not cur:
        return
    d = run_dir(it["project"], it["variant"])
    for suffix in ("clip.mp4", "cut.mp4", "last.png"):
        try:
            os.remove(os.path.join(d, f"scene{cur['n']}_{suffix}"))
        except OSError:
            pass
    qlog(it, f"Đã dừng ở cảnh {cur['n']}. Bấm Chạy tiếp để gen lại video cảnh này và đi tiếp.")


def _run_item(iid):
    it = qfind(iid)
    if not it or it["state"] == "running":
        return
    cx = ICANCEL[iid] = ItemCancel()
    with LOCK:
        it.update({"state": "running", "error": "", "started": time.time(), "ended": 0.0, "stopping": False})
        if it["kind"] == "gen":
            it["scenes"] = []
    qsave()
    try:
        if it["kind"] == "gen":
            gen_item(it, cx)
        else:
            post_item(it, it.get("opts") or {}, cx)
        it["state"] = "done"
        qlog(it, "Xong")
    except E.Cancelled:
        it["state"] = "stopped"
        _discard_inflight(it)
    except E.QuotaExceeded as e:
        # Mỗi video một tài khoản: chỉ dừng video này, các video khác đang dùng tài khoản khác chạy tiếp. Giữ các cảnh đã xong; Chạy tiếp thì LUO-API
        # chọn tài khoản khác (tài khoản vừa hết hạn mức bị tránh nếu còn tài khoản khác).
        it["state"] = "stopped"
        it["error"] = str(e)[:300]
        qlog(it, f"Dừng vì tài khoản {it.get('account') or '?'} hết hạn mức Muse: {e}", "error")
        _discard_inflight(it)
        QUOTA["hit"] = time.time()
    except Exception as e:  # noqa: BLE001
        it["state"] = "error"
        it["error"] = str(e)[:300]
        qlog(it, f"Lỗi - {e}", "error")
    finally:
        ICANCEL.pop(iid, None)
        it["stopping"] = False
        it["ended"] = time.time()
        it["elapsed"] = round(it["ended"] - it["started"], 1)
        qsave()


def _slots():
    return max(1, min(int(settings().get("parallel", 1) or 1), 8))


def _worker(iid):
    try:
        _run_item(iid)
    finally:
        with LOCK:
            ACTIVE.discard(iid)
        schedule()


def schedule():
    """Còn luồng trống thì lấy mục chờ kế tiếp ra chạy; hết việc thì đóng lượt chạy."""
    with LOCK:
        used = sum(1 for i in ACTIVE if (qfind(i) or {}).get("kind") == "gen")
        while PENDING and used < _slots():
            iid = PENDING.pop(0)
            it = qfind(iid)
            if not it or it["state"] != "waiting":
                continue
            ACTIVE.add(iid)
            used += 1
            threading.Thread(target=_worker, args=(iid,), daemon=True).start()
        if not ACTIVE and not PENDING and BATCH["state"] == "running":
            BATCH.update({"state": "done", "ended": time.time()})
        BATCH["parallel"] = _slots()


def queue_start(ids, parallel=None):
    """Thêm các mục vào lượt chạy bất cứ lúc nào: còn luồng thì chạy ngay, hết luồng thì chờ."""
    if parallel:
        st = settings()
        st["parallel"] = max(1, min(int(parallel), 8))
        jwrite(os.path.join(DATA, "settings.json"), st)
    ids = [i for i in ids if qfind(i) and qfind(i)["state"] not in ("running", "waiting")]
    if not ids:
        raise RuntimeError("Chưa chọn mục nào")
    with LOCK:
        if not busy():
            BATCH.update({"state": "running", "started": time.time(), "ended": 0.0, "ids": []})
        BATCH["state"] = "running"
        for iid in ids:
            qfind(iid)["state"] = "waiting"
            PENDING.append(iid)
            BATCH["ids"].append(iid)
    qsave()
    schedule()


def stop_items(ids=None):
    """Dừng một số mục (hoặc tất cả nếu ids=None): mục đang chờ thì rút khỏi hàng chờ, mục đang chạy thì báo dừng."""
    with LOCK:
        targets = set(ids) if ids else set(PENDING) | set(ACTIVE)
        for iid in list(PENDING):
            if iid in targets:
                PENDING.remove(iid)
                it = qfind(iid)
                if it and it["state"] == "waiting":
                    it["state"] = "queued"
        for iid in targets:
            cx, it = ICANCEL.get(iid), qfind(iid)
            if cx and it:
                cx.ev.set()
                it["stopping"] = True
                qlog(it, "Đang dừng…")
    qsave()
    schedule()


def start_post(pid, vname, opts):
    if any(x["kind"] == "gen" and x["project"] == pid and x["variant"] == vname and x["state"] == "running" for x in QUEUE):
        raise RuntimeError("Video này đang gen, đợi gen xong mới hậu kỳ được")
    if not os.path.exists(os.path.join(run_dir(pid, vname), "raw.mp4")):
        raise RuntimeError("Chưa có video thô")
    p = load_project(pid)
    it = {"id": uuid.uuid4().hex[:8], "kind": "post", "project": pid, "pname": (p or {}).get("name", pid), "variant": vname, "state": "queued", "scenes": [], "total": 0,
          "raw": "raw.mp4", "final": "", "error": "", "added": time.time(), "started": 0.0, "ended": 0.0, "elapsed": 0.0, "log": [], "opts": {k: opts.get(k, "") for k in ("logo", "endcard", "topbar", "whisper")}}
    with LOCK:
        QUEUE[:] = [x for x in QUEUE if not (x["kind"] == "post" and x["project"] == pid and x["variant"] == vname and x["state"] != "running")]
        QUEUE.append(it)
    with LOCK:  # hậu kỳ chạy ngay ở luồng riêng, không chờ luồng gen
        ACTIVE.add(it["id"])
        if BATCH["state"] != "running":
            BATCH.update({"state": "running", "started": time.time(), "ended": 0.0, "ids": []})
        BATCH["ids"].append(it["id"])
    threading.Thread(target=_worker, args=(it["id"],), daemon=True).start()
    return it["id"]


qload()


def results():
    out = []
    for pid in sorted(os.listdir(RUNS)) if os.path.isdir(RUNS) else []:
        p = load_project(pid)
        for vn in sorted(os.listdir(os.path.join(RUNS, pid))):
            d = os.path.join(RUNS, pid, vn)
            raw, fin = os.path.join(d, "raw.mp4"), os.path.join(d, "final.mp4")
            if not os.path.exists(raw) and not os.path.exists(fin):
                continue
            best = fin if os.path.exists(fin) else raw
            with LOCK:
                posts = [x for x in QUEUE if x["kind"] == "post" and x["project"] == pid and x["variant"] == vn]
            posting = any(x["id"] in ACTIVE for x in posts)
            last = posts[-1] if posts else None
            out.append({"posting": posting, "post_error": (last["error"] if last and last["state"] == "error" and not posting else ""), "project": pid, "project_name": (p or {}).get("name", pid), "variant": vn, "raw": os.path.exists(raw), "final": os.path.exists(fin),
                        "mtime": int(os.path.getmtime(best)), "secs": round(E.duration(best), 1), "size": os.path.getsize(best)})
    out.sort(key=lambda x: -x["mtime"])
    return out


def poster(pid, vn, which):
    d = os.path.join(RUNS, slug(pid), slug(vn))
    src = os.path.join(d, which + ".mp4")
    dst = os.path.join(d, which + ".jpg")
    if os.path.exists(src) and (not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", src, "-frames:v", "1", "-vf", "scale=360:-1", dst], capture_output=True)
    return dst if os.path.exists(dst) else None


def redo_from(pid, vname, n):
    d = run_dir(pid, vname)
    for f in os.listdir(d):
        m = re.match(r"scene(\d+)_", f)
        if m and int(m.group(1)) >= n or f in ("raw.mp4", "final.mp4", safe_name(vname) + ".mp4"):
            try:
                os.remove(os.path.join(d, f))
            except OSError:
                pass


def _pick_file_windows(kind):
    flt = "JSON (*.json)|*.json" if kind == "json" else "Tệp (*.mov;*.webm;*.png;*.jpg;*.mp4;*.json;*.txt)|*.mov;*.webm;*.png;*.jpg;*.mp4;*.json;*.txt|Tất cả|*.*"
    ps = ("Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.Form -Property @{TopMost=$true}; "
          f"$d = New-Object System.Windows.Forms.OpenFileDialog; $d.Filter = '{flt}'; "
          "if ($d.ShowDialog($f) -eq 'OK') { [Console]::OutputEncoding = [Text.Encoding]::UTF8; Write-Output $d.FileName }")
    r = subprocess.run(["powershell", "-NoProfile", "-STA", "-Command", ps], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip()


def pick_file(kind):
    if os.name == "nt":
        try:
            import tkinter  # noqa: F401
        except ImportError:
            return _pick_file_windows(kind)
    code = ("import tkinter as tk, tkinter.filedialog as fd, sys; r=tk.Tk(); r.withdraw(); r.attributes('-topmost',True); "
            "ft=[('Tệp','*.mov *.webm *.png *.jpg *.mp4 *.json *.txt')] if sys.argv[1]!='json' else [('JSON','*.json')]; "
            "print(fd.askopenfilename(filetypes=ft) or '')")
    r = subprocess.run([sys.executable, "-c", code, kind], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip().replace("/", os.sep)


MUSE_ALLOWED = re.compile(r"^(status|accounts|accounts/keepalive|accounts/[0-9a-f]{6,}|accounts/[0-9a-f]{6,}/(test|cookies|quota|keepalive)|tasks|tasks/clear|tasks/[A-Za-z0-9_]+|keepalive/status)$")


def muse_admin(method, sub, body=None, query=""):
    """Chuyển yêu cầu từ tab API của app tới /admin/<sub> của LUO-API (kèm khoá API). Chỉ cho các đường dẫn trong danh sách trắng."""
    if not MUSE_ALLOWED.match(sub):
        return 400, {"error": "Đường dẫn không hợp lệ"}
    url = settings()["api_url"].rstrip("/") + "/admin/" + sub + (("?" + query) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="PATCH" if method == "PUT" else method)
    k = api_key()
    if k:
        req.add_header("Authorization", f"Bearer {k}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            d = json.loads(raw)
            msg = d.get("detail") or d.get("error") or raw
        except ValueError:
            msg = raw
        return e.code, {"error": str(msg)[:300]}
    except Exception as e:  # noqa: BLE001
        return 502, {"error": f"Không kết nối được LUO-API: {e}"}


def app_version():
    """Số phiên bản (x.y.z) từ dòng đầu của version.txt ở thư mục gốc; rỗng nếu không đọc được."""
    try:
        first = open(os.path.join(HERE, "..", "..", "version.txt"), encoding="utf-8-sig").readline()
        m = re.search(r"\d+\.\d+\.\d+", first)
        return m.group(0) if m else ""
    except OSError:
        return ""


_MOUTH = {"t": 0.0, "res": None}
_MOUTH_PROBE = FM.probe_code()


def mouth_status(force=False, _code=None):
    """Tính năng đo miệng (mediapipe) có chạy được trên máy này không? Thử thật (nạp thư viện + chạy nhận diện mặt trên một ảnh trống) trong TIẾN TRÌNH RIÊNG,
    nên thư viện nhị phân hỏng cứng (DLL, crash) chỉ làm chết tiến trình thử. Kết quả được nhớ 15 phút (lỗi: 2 phút). Trả về {"ok": bool, "error": str}."""
    now = time.time()
    res = _MOUTH["res"]
    if not force and res is not None and now - _MOUTH["t"] < (900 if res["ok"] else 120):
        return res
    try:
        r = subprocess.run([sys.executable, "-I", "-W", "ignore", "-c", _code or _MOUTH_PROBE], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        if r.returncode == 0 and "ok" in r.stdout:
            res = {"ok": True, "error": ""}
        else:
            code = r.returncode & 0xFFFFFFFF
            lines = [l for l in (r.stderr or "").strip().splitlines() if l.strip()]
            detail = lines[-1] if lines else f"tiến trình thử bị lỗi hoặc crash (mã thoát 0x{code:08X})"
            res = {"ok": False, "error": E.mouth_unavailable_msg(RuntimeError(detail), True)}
    except subprocess.TimeoutExpired:
        res = {"ok": False, "error": "Kiểm tra quá thời gian (120 giây)."}
    except OSError as ex:
        res = {"ok": False, "error": f"Không chạy được tiến trình kiểm tra: {ex}"}
    _MOUTH["t"], _MOUTH["res"] = now, res
    return res


def disable_mouth_check(reason):
    """Tự tắt tính năng kiểm tra miệng + tự gen lại trong cài đặt và ghi lý do để giao diện hiển thị."""
    s = settings()
    s["check_overlap"] = False
    s["mouth_note"] = reason[:400]
    jwrite(os.path.join(DATA, "settings.json"), s)


def effective_check_overlap(it, s):
    """Giá trị `check_overlap` thực sự dùng cho lần chạy này: nếu cài đặt đang bật mà máy không chạy được đo miệng thì tự tắt (và lưu lại), không để mỗi cảnh báo lỗi."""
    if not bool(s.get("check_overlap", True)):
        return False
    st = mouth_status()
    if st["ok"]:
        return True
    disable_mouth_check(st["error"])
    qlog(it, "Tự tắt kiểm tra miệng người nghe và tự gen lại vì không khả dụng trên máy này: " + st["error"], "warn")
    return False


def health():
    s = settings()
    try:
        req = urllib.request.Request(s["api_url"].rstrip("/") + "/readyz")
        with urllib.request.urlopen(req, timeout=4) as r:
            d = json.loads(r.read().decode())
        ok = d.get("status") == "ready"
        return {"ok": ok, "accounts": d.get("accounts", 0), "status": d.get("status"), "key": bool(api_key()), "version": app_version()}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)[:120], "key": bool(api_key()), "version": app_version()}


# ------------------------------------------------------------------ HTTP
class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n).decode() or "{}") if n else {}

    def send_file(self, path, ctype=None):
        if not path or not os.path.isfile(path):
            return self.send_json({"error": "not found"}, 404)
        size = os.path.getsize(path)
        ctype = ctype or mimetypes.guess_type(path)[0] or "application/octet-stream"
        rng = self.headers.get("Range")
        start, end, code = 0, size - 1, 200
        if rng and (m := re.match(r"bytes=(\d*)-(\d*)", rng)):
            if m.group(1):
                start = int(m.group(1))
            if m.group(2):
                end = min(int(m.group(2)), size - 1)
            if not m.group(1) and m.group(2):
                start, end = max(0, size - int(m.group(2))), size - 1
            code = 206
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Cache-Control", "no-cache")
        if code == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        try:
            with open(path, "rb") as f:
                f.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        path, q = u.path, urllib.parse.parse_qs(u.query)
        try:
            if path.startswith("/api/"):
                return self.api("GET", path, q)
            if path.startswith("/asset/"):
                parts = [urllib.parse.unquote(x) for x in path[7:].split("/")]
                if len(parts) != 2 or any(".." in x for x in parts):
                    return self.send_json({"error": "bad path"}, 400)
                return self.send_file(os.path.join(DATA, "assets", slug(parts[0]), os.path.basename(parts[1])))
            if path.startswith("/media/"):
                parts = [urllib.parse.unquote(x) for x in path[7:].split("/")]
                if len(parts) != 3 or any(".." in x for x in parts):
                    return self.send_json({"error": "bad path"}, 400)
                if parts[2] == "poster-raw.jpg" or parts[2] == "poster-final.jpg":
                    return self.send_file(poster(parts[0], parts[1], parts[2][7:-4]))
                return self.send_file(os.path.join(RUNS, slug(parts[0]), slug(parts[1]), os.path.basename(parts[2])))
            f = "index.html" if path in ("/", "") else path.lstrip("/")
            full = os.path.normpath(os.path.join(UI, f))
            if not full.startswith(UI):
                return self.send_json({"error": "bad path"}, 400)
            return self.send_file(full)
        except Exception as e:  # noqa: BLE001
            return self.send_json({"error": str(e)}, 500)

    def do_POST(self):
        self.route_body("POST")

    def do_PUT(self):
        self.route_body("PUT")

    def do_DELETE(self):
        self.route_body("DELETE")

    def route_body(self, m):
        try:
            u = urllib.parse.urlparse(self.path)
            self.api(m, u.path, urllib.parse.parse_qs(u.query))
        except Exception as e:  # noqa: BLE001
            self.send_json({"error": str(e)}, 500)

    # ---- API
    def api(self, m, path, q):
        parts = path[5:].strip("/").split("/")
        a = parts[0]
        if m == "GET" and a == "boot":
            seed()
            return self.send_json({"settings": {**settings(), "api_key": "", "key_set": bool(settings().get("api_key"))},
                                   "projects": sorted((project_summary(p) for p in (jread(os.path.join(PROJ, f)) for f in os.listdir(PROJ) if f.endswith(".json")) if p),
                                                      key=lambda x: -x["updated"]),
                                   "types": list_types()})
        if a == "settings":
            if m == "GET":
                return self.send_json({**settings(), "api_key": "", "key_set": bool(settings().get("api_key"))})
            b = self.body()
            s = settings()
            for k in DEFAULT_SETTINGS:
                if k in b and not (k == "api_key" and b[k] == ""):
                    s[k] = b[k]
            if b.get("clear_key"):
                s["api_key"] = ""
            jwrite(os.path.join(DATA, "settings.json"), s)
            if "parallel" in b:
                schedule()  # tăng số luồng thì chạy ngay mục đang chờ
            return self.send_json({"ok": True})
        if a == "mouthcheck":
            return self.send_json(mouth_status(force=True))
        if a == "health":
            return self.send_json(health())
        if a == "muse":
            code, data = muse_admin(m, "/".join(parts[1:]), self.body() if m in ("POST", "PUT") else None, urllib.parse.urlencode({k: v[0] for k, v in q.items()}))
            return self.send_json(data, code)
        if a == "projects":
            if len(parts) == 1:
                if m == "POST":
                    b = self.body()
                    return self.send_json(new_project(b.get("name") or "Dự án mới", b.get("template") or "talka-phone", b.get("variants")))
                return self.send_json([])
            pid = parts[1]
            if m == "GET":
                p = load_project(pid)
                return self.send_json(p) if p else self.send_json({"error": "not found"}, 404)
            if len(parts) == 3 and parts[2] == "asset" and m == "POST":
                b = self.body()
                ext = os.path.splitext(b.get("name", ""))[1].lower()
                if ext not in (".png", ".jpg", ".jpeg", ".webp", ".mp3", ".wav", ".m4a", ".aac", ".ogg"):
                    return self.send_json({"error": "Chỉ nhận ảnh (png, jpg, webp) hoặc âm thanh (mp3, wav, m4a)"}, 400)
                raw = base64.b64decode(b.get("data", ""))
                if len(raw) > 15 * 1024 * 1024:
                    return self.send_json({"error": "File quá lớn (tối đa 15MB)"}, 400)
                d = os.path.join(DATA, "assets", slug(pid))
                os.makedirs(d, exist_ok=True)
                fn = uuid.uuid4().hex[:10] + ext
                open(os.path.join(d, fn), "wb").write(raw)
                return self.send_json({"file": fn, "type": "audio" if ext in (".mp3", ".wav", ".m4a", ".aac", ".ogg") else "image"})
            if m == "PUT":
                b = self.body()
                p = load_project(pid) or {}
                p.update({k: b[k] for k in ("name", "variants", "refs") if k in b})  # loại dự án (template) không đổi sau khi tạo
                p["id"] = pid
                save_project(p)
                return self.send_json({"ok": True})
            if m == "DELETE":
                try:
                    os.remove(project_path(pid))
                except OSError:
                    pass
                shutil.rmtree(os.path.join(RUNS, slug(pid)), ignore_errors=True)
                with LOCK:
                    QUEUE[:] = [x for x in QUEUE if x["project"] != pid or x["state"] == "running"]
                qsave()
                shutil.rmtree(os.path.join(DATA, "assets", slug(pid)), ignore_errors=True)
                return self.send_json({"ok": True})
        if a == "types":
            if len(parts) == 2 and parts[1] == "analyze" and m == "POST":
                b = self.body()
                an = E.analyze_script(b.get("script", ""))
                return self.send_json({**an, "fields": E.suggest_fields(an["plain"], "LUOT" in an["series"], b.get("fields"))})
            if m == "GET" and len(parts) == 1:
                return self.send_json(list_types())
            if m == "POST" and len(parts) == 1:
                try:
                    return self.send_json(create_type(self.body()))
                except ValueError as e:
                    return self.send_json({"error": str(e)}, 400)
            tid = parts[1] if len(parts) > 1 else ""
            if m == "GET" and tid:
                tp = jread(type_path(tid))
                return self.send_json({**tp, "script": type_text(tid)}) if tp else self.send_json({"error": "not found"}, 404)
            if m == "PUT":
                try:
                    return self.send_json(update_type(tid, self.body()))
                except ValueError as e:
                    return self.send_json({"error": str(e)}, 400)
            if m == "DELETE":
                used = [q["name"] for q in (jread(os.path.join(PROJ, f)) for f in os.listdir(PROJ) if f.endswith(".json")) if q and q.get("template") == tid]
                if used:
                    return self.send_json({"error": "Đang được dùng bởi: " + ", ".join(used[:3])}, 409)
                for ext in (".json", ".txt"):
                    try:
                        os.remove(os.path.join(TYPES, slug(tid) + ext))
                    except OSError:
                        pass
                return self.send_json({"ok": True})
        if a == "parse-xlsx" and m == "POST":
            import io
            import openpyxl
            b = self.body()
            wb = openpyxl.load_workbook(io.BytesIO(base64.b64decode(b.get("b64", ""))), data_only=True, read_only=True)
            ws = next((w for w in wb.worksheets if (w.max_row or 0) > 1), wb.worksheets[0])
            rows = [["" if c is None else str(c).strip() for c in r] for r in ws.iter_rows(values_only=True)]
            rows = [r for r in rows if any(r)]
            if len(rows) < 2:
                return self.send_json({"error": "Bảng cần ít nhất 2 dòng (dòng đầu là tên cột)"}, 400)
            w = len(rows[0])
            return self.send_json({"cols": rows[0], "rows": [(r + [""] * w)[:w] for r in rows[1:]]})
        if a == "queue":
            sub = parts[1] if len(parts) > 1 else ""
            if m == "GET" and not sub:
                return self.send_json(queue_view())
            b = self.body()
            try:
                if sub == "add":
                    return self.send_json({"ids": queue_add(b["project"], b["variants"])})
                if sub == "start":
                    queue_start(b.get("ids", []), b.get("parallel"))
                    return self.send_json({"ok": True})
                if sub == "remove":
                    queue_remove(b.get("ids", []))
                    return self.send_json({"ok": True})
                if sub == "redo":
                    it = qfind(b["id"])
                    if not it:
                        return self.send_json({"error": "Không làm lại được mục này"}, 409)
                    if it["state"] == "running":  # video đang chạy: dừng nó trước rồi làm lại từ cảnh được chọn
                        stop_items([it["id"]])
                        for _ in range(100):
                            if it["state"] != "running":
                                break
                            time.sleep(0.3)
                        if it["state"] == "running":
                            return self.send_json({"error": "Video đang bận, chưa dừng được. Thử lại sau vài giây."}, 409)
                    frm = int(b.get("from", 1))
                    redo_from(it["project"], it["variant"], frm)
                    with LOCK:
                        notes = {k: v for k, v in (it.get("notes") or {}).items() if int(k) < frm}  # ghi chú của các cảnh sẽ làm lại cũ đi; giữ ghi chú của cảnh trước đó
                        note = str(b.get("note", "")).strip()
                        if note:
                            notes[str(frm)] = note
                        it["notes"] = notes
                        it.update({"state": "queued", "scenes": [], "raw": "", "final": "", "error": ""})
                    qsave()
                    queue_start([it["id"]])
                    return self.send_json({"ok": True})
            except RuntimeError as e:
                return self.send_json({"error": str(e)}, 409)
        if a == "post" and m == "POST":
            b = self.body()
            try:
                return self.send_json({"id": start_post(b["project"], b["variant"], b)})
            except RuntimeError as e:
                return self.send_json({"error": str(e)}, 409)
        if a == "stop" and m == "POST":
            b = self.body()
            stop_items([b["id"]] if b.get("id") else (b.get("ids") or None))
            return self.send_json({"ok": True})
        if a == "results":
            return self.send_json(results())
        if a == "pick" and m == "POST":
            return self.send_json({"path": pick_file(self.body().get("kind", "file"))})
        if a == "open" and m == "POST":
            b = self.body()
            d = os.path.join(RUNS, slug(b["project"]), slug(b["variant"])) if b.get("variant") else RUNS
            named = os.path.join(d, safe_name(b["variant"]) + ".mp4") if b.get("variant") else ""
            if named and os.path.exists(named):
                subprocess.Popen(["explorer", "/select,", os.path.normpath(named)])  # mở thư mục và chọn sẵn video mang tên biến thể
            elif os.path.isdir(d):
                os.startfile(d)  # noqa: S606
            return self.send_json({"ok": True})
        if a == "delete-result" and m == "POST":
            b = self.body()
            shutil.rmtree(os.path.join(RUNS, slug(b["project"]), slug(b["variant"])), ignore_errors=True)
            return self.send_json({"ok": True})
        self.send_json({"error": "unknown endpoint"}, 404)


def make_server(port=0):
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    srv.daemon_threads = True
    return srv
