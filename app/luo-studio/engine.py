"""LUO Studio - engine: gen video nhiều cảnh qua LUO-API, nối khung cuối của clip ĐÃ CẮT.

Quy trình mỗi biến thể:
  script node (token) + biến thể -> các cảnh (mỗi cảnh một lượt nói)
  cảnh có "Prompt ảnh": ảnh khung đầu -> video; cảnh sau: video bắt đầu từ khung cuối của clip trước
  mỗi clip xong -> cắt đuôi ngay sau lời nói, chọn khung ÍT CHUYỂN ĐỘNG nhất làm điểm cắt
  -> khung cuối của clip đã cắt chính là khung đầu của clip kế => ghép liền mạch
  -> ghép các clip đã cắt thành raw.mp4
"""
import uuid
import base64, json, os, re, shutil, subprocess, sys, threading, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(HERE, "..", "production")
sys.path.insert(0, PROD)
import gen_video as G  # parse_script, build_prompts, muse_*_prompt, fill_tokens, variant_values, data_url, kind_of, read_key
import make_variants as MV  # ck/chars_of/cpos/crole: nhân vật tổng quát (khoá bất kỳ, không chỉ day/hoc)
import numpy as np

ALLOWED = [5, 6, 8, 10]
MAX_SPEED = 1.35
# Giải mã YUV -> RGB bằng swscale mặc định bị lệch làm tròn (mất ~1 mức sáng mỗi lần lấy khung). Chuỗi cảnh nối khung cuối qua nhiều lần
# nên video tối dần. accurate_rnd + full_chroma_int làm hết độ lệch (đã đo: 0.00 mỗi vòng thay vì -1.05).
DEC_VF = "scale=flags=accurate_rnd+full_chroma_int:out_range=pc,format=rgb24"


def video_duration(path):
    """Thời lượng của luồng HÌNH. Có thể ngắn hơn thời lượng cả file khi âm thanh dài hơn hình vài chục mili giây (clip đã cắt/tăng tốc thường như vậy)."""
    try:
        v = float(sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", path]).stdout.strip())
        if v > 0:
            return v
    except (RuntimeError, ValueError):
        pass
    return duration(path)


def grab_frame(src, out_png, sseof=None, ss=None):
    """Lấy một khung hình thành PNG không làm tối/lệch màu.
    `sseof` (số âm): lùi từ cuối LUỒNG HÌNH, không phải cuối file. `-sseof` của ffmpeg tính từ cuối file; khi âm thanh dài hơn hình thì mốc rơi sau khung hình cuối,
    ffmpeg bỏ khung đó và thoát mã 0 mà không ghi file nào ("No filtered frames"), làm bước sau văng [Errno 2] No such file. Vì vậy luôn kiểm tra file có thật sự được ghi,
    thử lùi dần, và cuối cùng giải mã hết clip rồi giữ khung cuối."""
    def attempt(pre):
        try:
            os.remove(out_png)   # tránh nhầm với file cũ còn sót
        except OSError:
            pass
        sh(["ffmpeg", "-y"] + pre + ["-i", src, "-vf", DEC_VF, "-frames:v", "1", "-update", "1", out_png])
        return os.path.exists(out_png) and os.path.getsize(out_png) > 0
    if sseof is None:
        tries = [["-ss", str(ss)] if ss is not None else []]
    else:
        vd = video_duration(src)
        tries, seen = [], set()
        for off in (sseof, -0.1, -0.2, -0.4, -0.8):
            t = round(max(0.0, vd + off), 3)
            if t not in seen:
                seen.add(t)
                tries.append(["-ss", f"{t:.3f}"])
    for pre in tries:
        if attempt(pre):
            return
    try:
        os.remove(out_png)
    except OSError:
        pass
    sh(["ffmpeg", "-y", "-i", src, "-vf", DEC_VF, "-update", "1", out_png])   # giải mã hết, ghi đè liên tục: file cuối cùng là khung cuối
    if not (os.path.exists(out_png) and os.path.getsize(out_png) > 0):
        raise RuntimeError(f"Không lấy được khung hình từ {os.path.basename(src)}")


def luma_stats(path, fps=2):
    """(trung bình, độ lệch chuẩn) của kênh Y (giá trị gốc 16-235, không đổi thang) trên các khung lấy mẫu."""
    d = crun(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale=90:160:flags=area,format=yuv420p,extractplanes=y",
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    n = len(d) // (90 * 160)
    if n < 1:
        return None
    a = np.frombuffer(d[: n * 90 * 160], np.uint8).reshape(n, 160, 90).astype(np.float32)
    return float(a.mean()), float(a.std(axis=(1, 2)).mean())


def exposure_fix(ref, cur, max_shift=0.12):
    """Bộ lọc eq đưa độ sáng/tương phản của clip `cur` về `ref`. Trả về (chuỗi lọc, mô tả) hoặc ("", "") nếu đã đủ gần."""
    if not ref or not cur:
        return "", ""
    mr, sr, mc, sc = ref[0], ref[1], cur[0], cur[1]
    if mc <= 0 or sc <= 1:
        return "", ""
    if abs(mc - mr) / mr < 0.02 and abs(sr / sc - 1) < 0.04:
        return "", ""
    a = min(1.15, max(0.85, sr / sc))
    b0 = (mr - a * mc) / 255.0
    b = max(-max_shift, min(max_shift, b0 - 0.5 * (1 - a)))
    return f"eq=contrast={a:.4f}:brightness={b:.4f}", f"sáng {100 * (mr - mc) / mr:+.1f}%"


# ------------------------------------------------------------------ giữ màu đồng nhất cả video
def color_stats(path, times):
    """Thống kê màu (trung bình các khung tại `times`): Y trung bình, Y độ lệch, độ bão hoà, U trung bình, V trung bình (thang 0-255 gốc của video)."""
    acc = []
    for t in times:
        cmd = ["ffmpeg", "-v", "error"] + (["-sseof", f"{t:.2f}"] if t < 0 else ["-ss", f"{t:.2f}"]) + \
              ["-i", path, "-frames:v", "1", "-vf", "scale=180:320:flags=area,format=yuv444p", "-f", "rawvideo", "-"]
        d = crun(cmd, capture_output=True).stdout
        if len(d) < 3 * 180 * 320:
            continue
        y, u, v = np.frombuffer(d[: 3 * 180 * 320], np.uint8).reshape(3, 320, 180).astype(np.float32)
        acc.append((y.mean(), y.std(), np.sqrt((u - 128) ** 2 + (v - 128) ** 2).mean(), u.mean(), v.mean()))
    return tuple(float(x) for x in np.mean(acc, axis=0)) if acc else None


def _grade(ref, cur):
    """(contrast, brightness, saturation, du, dv) đưa `cur` về `ref`, có giới hạn để không làm hỏng cảnh."""
    c = min(1.18, max(0.85, ref[1] / cur[1])) if cur[1] > 1 else 1.0
    b = max(-0.12, min(0.12, (ref[0] - (128 + (cur[0] - 128) * c)) / 255.0))
    sat = min(1.35, max(0.8, ref[2] / cur[2])) if cur[2] > 0.5 else 1.0
    du = max(-8.0, min(8.0, ref[3] - (128 + (cur[3] - 128) * sat)))
    dv = max(-8.0, min(8.0, ref[4] - (128 + (cur[4] - 128) * sat)))
    return c, b, sat, du, dv


def pull_palette(own, palette, w=0.7):
    """Chuẩn màu của cảnh mới = khung đầu của chính nó, nhưng sắc (bão hoà, U, V) kéo `w` về bảng màu chung của video: khung đầu do Muse vẽ hay ngả màu riêng,
    nếu lấy nguyên làm chuẩn thì mỗi cụm cảnh một tông. Độ sáng giữ của riêng cảnh (cận mặt và toàn cảnh có độ sáng trung bình khác nhau theo bố cục)."""
    if not palette:
        return own
    mix = lambda a, b: a + (b - a) * w
    return (own[0], own[1], mix(own[2], palette[2]), mix(own[3], palette[3]), mix(own[4], palette[4]))


def color_match(ref, start, end, dur, strength=1.0):
    """Bộ lọc ffmpeg kéo màu clip về `ref` (khung đầu chuẩn), chỉnh dần theo thời gian từ đầu tới cuối clip vì Muse hay tối/nhạt dần trong clip.
    strength 0..1: mức kéo về chuẩn (1 = kéo hết, 0.5 = một nửa) cho cảnh vốn khác ánh sáng không bị ép quá tay.
    Trả về (chuỗi lọc, mô tả) hoặc ("", "") nếu đã đủ gần."""
    if not ref or not start or not end:
        return "", ""
    s = max(0.0, min(1.0, float(strength)))
    soft = lambda g: (1 + (g[0] - 1) * s, g[1] * s, 1 + (g[2] - 1) * s, g[3] * s, g[4] * s)
    g0, g1 = soft(_grade(ref, start)), soft(_grade(ref, end))
    near = lambda g: abs(g[0] - 1) < 0.02 and abs(g[1]) < 0.006 and abs(g[2] - 1) < 0.03 and abs(g[3]) < 1 and abs(g[4]) < 1
    if near(g0) and near(g1):
        return "", ""
    D = max(0.5, dur)
    ramp = lambda a, b: f"{a:.4f}" if abs(a - b) < 1e-3 else f"'{a:.4f}+({b - a:.4f})*min(t/{D:.2f}\\,1)'"
    vf = f"eq=contrast={ramp(g0[0], g1[0])}:brightness={ramp(g0[1], g1[1])}:saturation={ramp(g0[2], g1[2])}:eval=frame"
    du, dv = (g0[3] + g1[3]) / 2, (g0[4] + g1[4]) / 2
    if abs(du) >= 1 or abs(dv) >= 1:
        vf += f",lutyuv=u='clip(val+({du:.1f})\\,16\\,240)':v='clip(val+({dv:.1f})\\,16\\,240)'"
    note = (f"sáng {100 * (ref[0] - end[0]) / ref[0]:+.0f}%, bão hoà {100 * (ref[2] - end[2]) / max(ref[2], 1):+.0f}% ở cuối clip")
    return vf, note


class Cancelled(Exception):
    pass


class AccountError(Exception):
    """Lỗi do TÀI KHOẢN Muse (phiên/cookie hỏng, tài khoản không được tạo video, hết hạn mức): thử lại trên cùng tài khoản vô ích.
    Studio dừng video, bỏ tài khoản này khỏi lựa chọn của video rồi chạy tiếp ngay bằng tài khoản khác đang bật (server._run_item)."""
    def __init__(self, msg, account=None, kind="account"):
        super().__init__(msg)
        self.account, self.kind = account, kind


class QuotaExceeded(AccountError):
    """Muse báo hết hạn mức tạo video (giới hạn 24 giờ): thử lại hay gen lại đều vô ích và còn tốn thêm."""
    def __init__(self, msg, account=None):
        super().__init__(msg, account, "quota")


# Tuỳ chọn tài khoản theo pin của video (server.gen_item đặt, Api.generate đọc): {"pin_account": id chọn tay, "pin_avoid": [id vừa lỗi]}.
# Theo pin (không theo luồng) để mọi đường gen của video đều nhận: run_variant, ghép 2 lớp, code gen riêng của thể loại.
PIN_EXTRA = {}
# LUO-API cũ chưa trả error_kind: nhận lỗi tài khoản theo nội dung (phiên bị đăng xuất, cookie hỏng, tài khoản không được tạo video).
_ACCOUNT_ERR_RE = re.compile(r"会话已被 muse\.ai 登出|会话认证失败|重新导入 cookie|指定账号 .* 不存在或已禁用|Tài khoản đã chọn .* không tồn tại", re.I)


_QUOTA_RE = re.compile(r"24-hour limit|budget is (?:still )?exhausted|video budget|quota (?:is )?exhausted|hết hạn mức|limit for the (?:last|past) 24 hours|(?:video|daily|generation) limit (?:is |has been )?reached", re.I)


_TL = threading.local()

# Muse (04/11/2026) là agent có bộ nhớ: nó tóm tắt prompt rồi mới gọi công cụ tạo media, trộn MEMORY.md / AGENTS.md / Goal của cả loạt video vào,
# nên mỗi lần gen Muse đọc một prompt khác nhau -> clip khác nhau, người nghe nhép miệng theo lời của cảnh. Câu dẫn này đặt trước MỌI prompt
# (mọi thể loại; tắt bằng cài đặt "muse_directive": false).
MEDIA_DIRECTIVE = (
    "[DIRECT MEDIA REQUEST] Call the media generation tool exactly once and give it the full request text below as its prompt, "
    "VERBATIM, word for word: do not summarize, shorten, paraphrase, translate or add anything. Do not read or use MEMORY.md, "
    "AGENTS.md, goals, notes, earlier chats, or earlier images and videos from the library; use only the files attached to this "
    "message, in the order given. Do not add any dialogue, speech, action or person that the request does not ask for. "
    "Do not launch subagents, do not draft follow-up clips, do not write memory or notes about this request. "
    "Reply only with the generated file.\n\n--- REQUEST ---\n")


def set_prompt_prefix(opts):
    """Đặt câu dẫn Muse cho luồng gen hiện tại theo cài đặt (gọi ở đầu run_variant / run_split)."""
    _TL.prompt_prefix = MEDIA_DIRECTIVE if (opts or {}).get("muse_directive", True) else ""


def crun(cmd, capture_output=False, text=False, encoding=None, errors=None, **kw):
    """subprocess.run có thể huỷ: nếu luồng hiện tại có cờ huỷ (set trong run_variant) thì kill tiến trình và ném Cancelled."""
    kw.pop("check", None)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text, encoding=encoding, errors=errors, **kw)
    cx = getattr(_TL, "cancel", None)
    while True:
        try:
            out, err = proc.communicate(timeout=0.3)
            return subprocess.CompletedProcess(cmd, proc.returncode, out, err)
        except subprocess.TimeoutExpired:
            if cx is not None and cx.is_set():
                proc.kill()
                proc.communicate()
                raise Cancelled()


def interruptible(fn, cancel):
    """Chạy fn ở luồng phụ (vd. Whisper không ngắt được); nếu bị huỷ thì bỏ qua kết quả và ném Cancelled ngay."""
    box = {}

    def w():
        try:
            box["v"] = fn()
        except BaseException as e:  # noqa: BLE001
            box["e"] = e
    th = threading.Thread(target=w, daemon=True)
    th.start()
    while th.is_alive():
        th.join(0.3)
        if cancel is not None and cancel.is_set():
            raise Cancelled()
    if "e" in box:
        raise box["e"]
    return box["v"]


def sh(cmd, **kw):
    r = crun(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode:
        err = r.stderr or ""
        # giữ cả dòng lỗi gốc (thường nằm đầu) lẫn phần đuôi; bỏ banner phiên bản
        lines = [l for l in err.splitlines() if l.strip() and not l.lstrip().startswith(("built with", "configuration:", "lib", "ffmpeg version"))]
        raise RuntimeError(f"{cmd[0]}: " + chr(10).join(lines[-12:])[-900:])
    return r


def sh_enc(cmd, vf_index=None, **kw):
    """Chạy ffmpeg mã hoá; nếu libx264 báo lỗi giữa chừng thì thử lại 1 luồng, rồi bỏ bộ lọc cân màu (-vf / eq) nếu có."""
    try:
        return sh(cmd, **kw)
    except RuntimeError:
        pass
    safe = list(cmd)
    i = safe.index("-c:v")
    safe[i:i] = ["-threads", "1"]
    try:
        return sh(safe, **kw)
    except RuntimeError:
        if vf_index is None:
            raise
    nofx = list(cmd)
    del nofx[vf_index:vf_index + 2]
    return sh(nofx, **kw)


def duration(path):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout)


def has_audio(path):
    return bool(sh(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", path]).stdout.strip())


# ------------------------------------------------------------------ API với huỷ + tiến độ
class Api(G.Api):
    def generate(self, kind, prompt, refs, session, duration=None, timeout=900, on_status=None, cancel=None, audios=None, on_account=None, pin=None, pin_prefer=None, aspect="9:16"):
        prompt = getattr(_TL, "prompt_prefix", "") + prompt   # câu dẫn riêng của một thể loại (gen.py của thể loại đặt, mặc định không có)
        body = {"prompt": prompt, "model": "muse-video" if kind == "video" else "muse-image", "aspect_ratio": aspect,
                "raw_prompt": True, "timeout": min(int(timeout), 600), "session": session}  # API nhận tối đa 600s; thời gian chờ phía app (deadline) vẫn theo `timeout`
        if pin:   # mọi cảnh của một video ghim vào MỘT tài khoản Muse (LUO-API không tự đổi tài khoản)
            body["pin"] = pin
            if pin_prefer:
                body["pin_prefer"] = pin_prefer
            ex = PIN_EXTRA.get(pin) or {}
            if ex.get("pin_account"):   # người dùng chọn tay tài khoản cho video
                body["pin_account"] = ex["pin_account"]
                body.pop("pin_prefer", None)
            if ex.get("pin_avoid"):     # tài khoản vừa lỗi với video: LUO-API chọn tài khoản khác
                body["pin_avoid"] = list(ex["pin_avoid"])
        if kind == "video":
            body["duration"] = duration
        if refs:
            body["reference_images"] = refs
        if audios and kind == "video":
            body["reference_audios"] = audios
        path = "/v1/videos" if kind == "video" else "/v1/images/tasks"
        deadline = time.time() + timeout
        while True:
            if cancel and cancel.is_set():
                raise Cancelled()
            try:
                task = self.req(path, body)
                break
            except G.ApiError as e:
                if e.code == 429 and time.time() < deadline:
                    time.sleep(5)
                    continue
                raise
        tid = task.get("task_id") or task.get("id")
        last = None
        while True:
            for _ in range(2):   # hỏi mỗi 1 s (trước 3 s): kết quả về sớm hơn trung bình ~1 s mỗi bước gen
                if cancel and cancel.is_set():
                    raise Cancelled()
                time.sleep(0.5)
            st = self.req(f"{path}/{tid}")
            s, pr = st.get("status"), st.get("progress")
            if on_account and st.get("account"):   # LUO-API báo tài khoản Muse đang gen task này (id + nhãn gợi nhớ, không có cookie)
                on_account(st["account"], st.get("account_label") or st["account"])
            if on_status and (s, pr) != last:
                last = (s, pr)
                on_status(s, pr)
            if s == "completed":
                local = G.local_result(self.url, st)   # LUO-API cùng máy: đọc thẳng file, không tải lại qua HTTP
                if local is not None:
                    return local
                url = st.get("url") or (st.get("video") or {}).get("url") or (st.get("result") or {}).get("url") or ((st.get("data") or [{}])[0]).get("url")
                if not url:
                    raise RuntimeError("API không trả về file")
                return self.download(url)
            if s in ("failed", "error"):
                msg, kind = str(st.get("error") or "API báo lỗi"), st.get("error_kind")
                if kind == "quota" or (kind is None and _QUOTA_RE.search(msg)):
                    raise QuotaExceeded(f"Muse báo hết hạn mức tạo video (giới hạn 24 giờ): {msg[:160]}", st.get("account"))
                if kind == "account" or (kind is None and _ACCOUNT_ERR_RE.search(msg)):
                    raise AccountError(f"Lỗi tài khoản Muse: {msg[:200]}", st.get("account"))
                raise RuntimeError(msg)
            if time.time() > deadline:
                raise RuntimeError("Hết thời gian chờ")


# ------------------------------------------------------------------ bố cục khung đầu cố định
def fit_start_frame(api, img_f, session, opts, emit, n, pin, pin_prefer, cancel, note_account):
    """Thể loại có bảng chèn phía trên: nếu nhân vật trong ảnh khung đầu quá to (đỉnh đầu cao hơn ~33% khung) thì thu về đúng cỡ, neo đáy, rồi nhờ Muse vẽ nối nền
    cho kín khung (không viền mờ, nền vẫn là nền gốc). Ảnh gốc giữ ở <ảnh>.orig.png. Muse vẽ lỗi / đổi cỡ thì thử lại, hết lượt thì giữ ảnh gốc và báo."""
    import layout_fit as LF
    top = LF.head_top(img_f)
    if top is None:
        emit("log", msg=f"Cảnh {n}: không dò được đầu nhân vật trong ảnh khung đầu, giữ nguyên", level="warn")
        return
    if top >= LF.HEAD_OK:
        emit("log", msg=f"Cảnh {n}: nhân vật đúng cỡ (đỉnh đầu ở {top * 100:.0f}% khung)")
        return
    s = LF.scale_for(top)
    emit("log", msg=f"Cảnh {n}: nhân vật quá to (đỉnh đầu ở {top * 100:.0f}% khung, bảng sẽ che mặt): thu {s:.2f} rồi nhờ Muse vẽ nối nền")
    orig = img_f + ".orig.png"
    shutil.copy(img_f, orig)
    canvas = img_f + ".canvas.png"
    LF.make_canvas(orig, canvas, s)
    for i in range(1, opts["retries"] + 2):
        try:
            b = api.generate("image", G.muse_image_prompt(LF.OUTPAINT_PROMPT, "", 1), [G.data_url(canvas)], session, timeout=opts["timeout"],
                             on_status=lambda st, p: emit("scene", n=n, state="image", pct=p or 0), cancel=cancel, on_account=note_account,
                             pin=pin, pin_prefer=pin_prefer)
            tmp = img_f + ".fit.png"
            if G.kind_of(b) == "video":
                open(tmp + ".mp4", "wb").write(b)
                grab_frame(tmp + ".mp4", tmp)
                os.remove(tmp + ".mp4")
            else:
                open(tmp, "wb").write(b)
            t2 = LF.head_top(tmp)
            if t2 is not None and t2 >= LF.HEAD_OK:
                os.replace(tmp, img_f)
                emit("log", msg=f"Cảnh {n}: đã mở rộng nền, đỉnh đầu ở {t2 * 100:.0f}% khung")
                break
            emit("log", msg=f"Cảnh {n}: Muse vẽ nối nền chưa đúng cỡ (đỉnh đầu {'?' if t2 is None else f'{t2 * 100:.0f}%'}), thử lại {i}/{opts['retries'] + 1}", level="warn")
        except (Cancelled, AccountError):
            raise
        except Exception as e:  # noqa: BLE001
            emit("log", msg=f"Cảnh {n}: vẽ nối nền lỗi: {e}", level="warn")
    else:
        emit("log", msg=f"Cảnh {n}: không mở rộng nền được, giữ ảnh gốc (nhân vật to, bảng có thể che mặt)", level="warn")
    for f in (canvas, img_f + ".fit.png"):
        if os.path.exists(f):
            os.remove(f)


# ------------------------------------------------------------------ tham chiếu đính kèm theo token
_REMBG = {}


def _cutout(im):
    """Tách phông (rembg, model u2net_human_seg chạy tại máy). Trả về ảnh RGBA hoặc None nếu chưa cài rembg / lỗi."""
    try:
        from rembg import new_session, remove
        if "s" not in _REMBG:
            _REMBG["s"] = new_session("u2net_human_seg")
        return remove(im, session=_REMBG["s"])
    except Exception:  # noqa: BLE001
        return None


def reframe_ref(path, out_dir, scale=0.85):
    """Ảnh nhân vật tham chiếu thường là cận cảnh, có sẵn nền riêng nên Muse chép luôn cỡ, khung và nền của ảnh. Tách phông nhân vật, thu còn `scale` chiều rộng,
    neo đáy giữa khung 9:16 trên nền trơn: Muse chỉ lấy mặt/trang phục, nền lấy từ lời dặn, nhân vật nhỏ và 1/3 trên trống (~đầu ở 34%).
    Chưa cài rembg thì dùng nền là chính ảnh phóng to và làm mờ (kém hơn)."""
    try:
        from PIL import Image, ImageFilter
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "reframed_" + os.path.splitext(os.path.basename(path))[0] + ".png")
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(path):
            return dst
        W, H = 720, 1280
        im = Image.open(path).convert("RGB")
        cut = _cutout(im)
        fw = int(W * scale)
        if cut is not None:
            canvas = Image.new("RGBA", (W, H), (226, 226, 226, 255))
            fg = cut.resize((fw, max(1, int(cut.height * fw / cut.width))), Image.LANCZOS)
            if fg.height > H:
                fg = fg.resize((max(1, int(fg.width * H / fg.height)), H), Image.LANCZOS)
            canvas.alpha_composite(fg, ((W - fg.width) // 2, H - fg.height))
            canvas.convert("RGB").save(dst)
            return dst
        k = max(W / im.width, H / im.height)
        bg = im.resize((int(im.width * k) + 1, int(im.height * k) + 1)).filter(ImageFilter.GaussianBlur(24))
        canvas = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
        fg = im.resize((fw, max(1, int(im.height * fw / im.width))))
        if fg.height > H:
            fg = fg.resize((max(1, int(fg.width * H / fg.height)), H))
        canvas.paste(fg, ((W - fg.width) // 2, H - fg.height))
        canvas.save(dst)
        return dst
    except Exception:  # noqa: BLE001 - không xử lý được thì dùng ảnh gốc
        return path


def attachments(vdata, opts, keep=None, offset=0, missing=None, lead=None):
    """(ảnh data-url, chú thích ảnh, [(nhóm, audio data-url)]) từ vdata["refs"] = {TOKEN: [{type,file,name}]}.
    keep(token, nhóm) -> bool: chỉ lấy tệp của các token thoả điều kiện (chế độ ghép 2 lớp: mỗi nhân vật chỉ nhận ảnh của chính nó).
    offset: số ảnh đã đứng TRƯỚC các ảnh này trong lệnh gửi (ảnh chung của dự án), để số thứ tự trong chú thích khớp thứ tự thật.
    missing: danh sách nhận tên các tệp được gắn nhưng không còn trên đĩa (trước đây bị bỏ qua âm thầm, video ra sai nhân vật mà không có cảnh báo).
    lead: câu đặt trước chú thích thay cho câu mặc định về ảnh chung (vd. nói ảnh #1 là khung đầu của clip)."""
    base = opts.get("assets_dir") or ""
    labels, groups = opts.get("field_labels", {}), opts.get("field_groups", {})
    imgs, notes, auds = [], [], []
    chars = MV.chars_of(vdata)

    def describe(key):
        """Câu tiếng Anh nói ảnh này là của AI. Tên trường (vd. "Ngoại hình") giống nhau ở mọi nhân vật nên Muse không biết ảnh nào của ai; phải nêu TÊN nhân vật (TEN_<khoá>)."""
        k = key.upper()
        c = next((c for c in chars if k.endswith("_" + c)), None)
        name = str(vdata.get("TEN_" + c) or "").strip()[:70] if c else ""
        if c and k.startswith("NGUOI"):
            who = f"{name} (character {c})" if name else f"character {c}"
            return f"the EXACT look of {who}: copy this person's face, hair, skin tone, age and clothing; it is NOT any other character"
        if c:
            return f"{labels.get(key, key)} for {name or 'character ' + c}"
        return str(labels.get(key, key))
    for key, items in (vdata.get("refs") or {}).items():
        if keep and not keep(key, groups.get(key, "other")):
            continue
        for it in items or []:
            p = os.path.join(base, os.path.basename(it.get("file", "")))
            if not os.path.isfile(p):
                if missing is not None:
                    missing.append(f"{labels.get(key, key)}: {it.get('name') or it.get('file')}")
                continue
            if it.get("type") == "audio":
                auds.append((groups.get(key, "other"), G.data_url(p)))
            else:
                framed = opts.get("layout_ref") and key.upper().startswith("NGUOI")   # thể loại có bố cục cố định: ảnh nhân vật chỉ để lấy mặt/trang phục
                imgs.append(G.data_url(reframe_ref(p, os.path.join(base, ".reframed")) if framed else p))
                notes.append(f"reference image #{offset + len(imgs)} is {describe(key)}"
                             + ("; take the character's identity and outfit ONLY, and leave out any logo, brand mark or text printed on it. Its plain background is NOT part of the scene (draw the background from the prompt), and the character must stay as small and as low in the frame as in this reference" if framed else ""))
    legend = "; ".join(notes)
    return imgs, ((("(the first images are general references) " if offset and lead is None else (lead or "")) + legend) if legend else ""), auds


# ---- ảnh ngang tổng quan (trường "Ảnh tổng quan" của một CẢNH): cho Muse thấy cả bố cục trước khi lia máy trong clip
WIDE_NOTE = ("Create exactly one still image, a HORIZONTAL 16:9 widescreen frame (landscape, much wider than tall). This is an image-generation request, not a video request: "
             "ignore any mention of voice, motion or timing. It is a WIDE OVERVIEW of the whole set: every person and object named below is fully inside the frame, at the position given. "
             "Ignore any mention of a vertical, portrait or 9:16 frame elsewhere in the text: this one picture is landscape 16:9.")
_CROP_X = {"trái": 0.0, "trai": 0.0, "giữa": 0.5, "giua": 0.5, "phải": 1.0, "phai": 1.0}


def crop_x(field):
    """Trường "Khung đầu cắt": trái / giữa / phải hoặc số 0..1 (vị trí khung dọc trong ảnh ngang). None nếu không khai."""
    m = re.search(r"trái|trai|giữa|giua|phải|phai|\d+(?:[.,]\d+)?", str(field or ""), re.I)
    if not m:
        return None
    w = m.group(0).lower()
    return _CROP_X[w] if w in _CROP_X else max(0.0, min(1.0, float(w.replace(",", "."))))


def wide_crop(src, out_png, x):
    """Cắt khung dọc 9:16 từ ảnh ngang tổng quan (x = 0 sát mép trái .. 1 sát mép phải), phóng lên 1080x1920. Trả về chiều rộng khung cắt (px của ảnh gốc)."""
    w, h = (int(v) for v in sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", src]).stdout.strip().split("x")[:2])
    cw = min(w, int(h * 9 / 16)) // 2 * 2
    ox = int((w - cw) * x)
    sh(["ffmpeg", "-y", "-i", src, "-vf", f"crop={cw}:{h}:{ox}:0,scale=1080:1920:flags=lanczos", "-frames:v", "1", "-update", "1", out_png])
    return cw


_TOK = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")


def scene_tokens(template):
    """{số cảnh: tập token {{...}} xuất hiện trong khối CẢNH đó của script (chưa điền)} - để biết cảnh nào có nhân vật / nền nào."""
    hs = list(re.finditer(r"^CẢNH (\d+) \(", template, re.M))
    return {int(h.group(1)): set(_TOK.findall(template[h.start(): hs[i + 1].start() if i + 1 < len(hs) else len(template)])) for i, h in enumerate(hs)}


def scene_ref_filter(toks, people, all_toks):
    """keep(token, nhóm) cho attachments(): chỉ gửi ảnh tham chiếu của nhân vật/nền có trong cảnh.
    Gửi cả ảnh người không có mặt làm Muse trộn mặt (vd. mặt cô gái lẫn vào cảnh sát). `people`: khoá nhân vật có mặt (NGUOI_<khoá>).
    Token không cảnh nào nhắc riêng (chỉ nằm trong các khối LOCK) thì không lọc được: vẫn gửi như cũ."""
    def keep(key, _grp):
        k = key.upper()
        if k.startswith("NGUOI_"):
            return k[6:] in people
        return k in toks or k not in all_toks
    return keep


# ------------------------------------------------------------------ chống 2 nhân vật cùng nói
OVERLAP_NEG = "both speaking at once; two voices in one clip"   # ngắn gọn, như mẫu video call: càng nhắc nhiều hiện tượng càng dễ gây ra


_FEM = re.compile(r"\b(woman|women|female|girl|lady|she|her)\b", re.I)
_MAS = re.compile(r"\b(man|men|male|boy|guy|he|his)\b", re.I)


def _gender(text):
    f, m = bool(_FEM.search(text or "")), bool(_MAS.search(text or ""))
    return "f" if f and not m else "m" if m and not f else ""


def same_gender(v):
    if v.get("_SG"):   # đã tách giọng: mô tả giọng mới không còn từ chỉ giới nên đánh dấu lại
        return True
    gd, gh = _gender(v.get("GIONG_DAY", "")), _gender(v.get("GIONG_HOC", ""))
    return bool(gd) and gd == gh


ROBOT_VOICE_SPLIT = ("VOICE A: a bright, youthful, high-pitched, quick and airy voice with a sing-song, strongly varying intonation and a smile in it, "
                     "like a cheerful studio-polished video-call assistant; natural and human-sounding, not robotic, clearly lighter, younger and faster than VOICE B")
LEARNER_VOICE_SPLIT = ("VOICE B: a low-pitched, deep, slow, husky and slightly gravelly voice with a grounded, earthy, plain intonation and warm hesitations; "
                       "clearly deeper, older and slower than VOICE A")


def voice_split(v):
    """Số đo trên clip thật: video có người học NAM chỉ lỗi 3% (1/36) còn người học NỮ lỗi 38% (9/24), tới 58% ở các lượt robot nói. Hai giọng nữ cùng nghe giống nhau nên Muse gán
    một giọng cho cả hai khuôn mặt. Khi cùng giới: tách hẳn âm sắc (robot cao, sáng, trẻ; người học trầm, khàn, chậm) ngay trong mô tả giọng, ở mọi clip."""
    if not same_gender(v):
        return v
    nv = dict(v)
    nv["_SG"] = True
    nv["GIONG_DAY"] = ROBOT_VOICE_SPLIT
    base = str(v.get("GIONG_HOC", "")).strip().rstrip(".")
    nv["GIONG_HOC"] = f"{base}; {LEARNER_VOICE_SPLIT}"
    return nv


_LOW_WORDS = re.compile(r"\b(low|deep|dry|firm|gravel\w*|husky|baritone|bass|rough|slow)\b", re.I)
_HIGH_CLEAN = re.compile(r"\b(?:slightly |a bit )?(?:husky|gravelly|deep|low|mid-low|unhurried|slow)\b,?\s*", re.I)
PAIR_LOW = "pitched clearly LOWER than the other character's voice: deeper, slower, huskier and more clipped, easy to tell apart from it"
PAIR_HIGH = "pitched clearly HIGHER than the other character's voice: lighter, brighter, quicker and more animated (a light tenor / alto), easy to tell apart from it"


def pair_voice_split(v):
    """Hai nhân vật bất kỳ (khoá tự đặt: khách / nhân viên, hai người đối diện...) CÙNG giới thì Muse dễ gán một giọng cho cả hai khuôn mặt (hộ chiếu 04/11: khách nam nhép lời nhân viên nam).
    Như voice_split nhưng cho mọi cặp khoá: bên có mô tả trầm / khô / cứng hơn thành giọng THẤP, bên kia thành giọng CAO, ghi vào GIONG_<khoá> và đánh dấu `_LOW` để speaker_lock nhắc lại. Khác giới thì để nguyên."""
    chars = MV.chars_of(v)
    if len(chars) != 2 or set(chars) == {"DAY", "HOC"} or v.get("_LOW"):
        return v
    voices = [str(v.get(f"GIONG_{c}") or "").strip().rstrip(".") for c in chars]
    g = [_gender(x) for x in voices]
    if not all(voices) or not g[0] or g[0] != g[1]:
        return v
    score = [len(_LOW_WORDS.findall(x)) for x in voices]
    lo = 0 if score[0] > score[1] else 1
    nv = dict(v, _LOW=chars[lo])
    nv[f"GIONG_{chars[lo]}"] = f"{voices[lo]}; {PAIR_LOW}"
    hi_base = re.sub(r"(?:,?\s+and)?[\s,]*$", "", _HIGH_CLEAN.sub("", voices[1 - lo]).strip())
    nv[f"GIONG_{chars[1 - lo]}"] = f"{hi_base}; {PAIR_HIGH}"
    return nv


def pair_contrast(v, k):
    low = v.get("_LOW")
    if not low:
        return ""
    return ("Its voice is clearly the LOWER-pitched, deeper and slower of the two voices in this video, easy to tell apart from the other character's voice." if k == low else
            "Its voice is clearly the HIGHER-pitched, lighter and quicker of the two voices in this video, easy to tell apart from the other character's voice.")


def voice_contrast(v, day):
    """Hai giọng cùng giới (vd. robot nữ + người học nữ) rất dễ bị Muse lẫn: gắn cho mỗi bên một đặc trưng cao độ trái ngược, giữ nhất quán ở mọi clip,
    để giọng nghe được chỉ khớp với MỘT khuôn mặt. Khác giới thì giọng đã đủ khác, không cần thêm."""
    gd, gh = _gender(v.get("GIONG_DAY", "")), _gender(v.get("GIONG_HOC", ""))
    if not gd or gd != gh:
        return ""
    if day:   # người nói là bên 'dạy' (robot)
        return "Its voice is clearly the HIGHER-pitched, brighter, lighter and quicker of the two voices in this video, easy to tell apart from the other character's voice."
    return "Its voice is clearly the LOWER-pitched, deeper, warmer and slower of the two voices in this video, easy to tell apart from the other character's voice."


def role_names(v, day):
    """(vai người nói, vai người nghe) của hai nhân vật day/hoc; giữ cho tương thích. Vai đặt bằng VAI_DAY / VAI_HOC, mặc định tutor / learner."""
    rd, rh = MV.crole(v, "DAY"), MV.crole(v, "HOC")
    return (rd, rh) if day else (rh, rd)


def speaker_lock(v, turn):
    """Khối đầu prompt video, viết theo mẫu video call (master-ugc-ai-call): MỘT câu khẳng định ai nói gì + người kia im và đang làm việc riêng.
    Không liệt kê hàng loạt điều cấm (khiến Muse hiểu người nghe cũng 'có phần' trong lời thoại).
    Số nhân vật bất kỳ: mỗi nhân vật có khoá (day, hoc hoặc khoá khác) và các token TEN_/POS_/GIONG_/VAI_/NGHE_<KHOÁ>; một người nói, tất cả còn lại im lặng."""
    k = MV.ck(turn.get("who"))
    chars = MV.chars_of(v)
    letter = {c: chr(65 + i) for i, c in enumerate(chars)}
    lis = [c for c in chars if c != k]
    spk, spos, role_s = v.get(f"TEN_{k}"), MV.cpos(v, k), MV.crole(v, k)
    contrast = voice_contrast(v, k == "DAY") if {k, *lis} == {"DAY", "HOC"} else pair_contrast(v, k)
    quiet = ""
    idle = v.get("listen") == "idle"   # người nghe "idle": môi khép nhưng vẫn sống (chớp mắt, thở, phản ứng nhẹ) thay vì đứng như ảnh tĩnh
    react = str(turn.get("emo2") or "").strip().replace('"', "'")
    for c in lis:
        task = v.get("VIEC", "").strip() if (k == "DAY" and c == "HOC") else ""
        strong = same_gender(v) and bool(task)   # cùng giới: giấu miệng người nghe ngay từ đầu
        pose = str(v.get(f"NGHE_{c}") or "").strip()   # tuỳ chọn: tư thế khi nghe do biến thể quy định (vd. hai người nhìn nhau, không nhìn ống kính)
        alive = ("listens in a natural, living idle: soft blinking, gentle breathing, small attentive head movements and a faint expression that follows the mood of the line"
                 + (f' (reacting "{react}")' if react else " (a slight smile, a small eyebrow lift or a tiny nod)") + ", mouth staying closed")
        base = (pose if pose else
                f"keeps quietly {task} at the same slow, steady pace the whole time, head bowed low over the work, face half hidden by the hat or hair and turned down and away, eyes on the work, lips closed and still" if strong else
                f"keeps quietly {task} at a slow, steady pace and {alive}" if task and idle else
                f"keeps quietly {task} at the same slow, steady pace the whole time, head lowered over the work, eyes on the work, face partly turned away from the phone and the camera" if task
                else f"{alive}, eyes resting on the speaker" if idle
                else "stays in the calm base pose, still, eyes on the camera, mouth a flat closed line")
        role_l = MV.crole(v, c)
        lb = MV.back_view(v, c)   # người nghe quay lưng về camera: không tả mặt / môi (kẻo Muse xoay mặt họ ra), chỉ tư thế
        mood = ("their back to the camera and face hidden, only the head and shoulders visible" if lb else
                "a living, attentive face" if idle else "a calm relaxed face with a faint steady quiet mood")
        quiet += (f"The {role_l} ({MV.cpos(v, c)}) is quiet for the whole clip: " + ("" if lb else "lips gently closed, ") + f"{mood}, and {base}, "
                  f"at the {role_l}'s own pace regardless of the dialogue. ")
    resting = " and ".join(f"VOICE {letter[c]}" for c in lis) + (" is" if len(lis) == 1 else " are") + " resting in this clip."
    back = MV.back_view(v, turn["who"])   # người nói quay lưng về camera (QUAY_LUNG_<khoá>): không nhắc miệng / nét mặt, kẻo Muse xoay mặt họ ra
    return ("SPEAKER MAP: " + "; ".join(f"VOICE {letter[c]} belongs to the {MV.cpos(v, c)} character ({v.get(f'TEN_{c}')})" for c in chars) + ". "
            f"In this clip only VOICE {letter[k]} is heard, " + (f"spoken by the {spos} character ({spk}), who has their back to the camera. " if back else f"coming from the mouth of the {spos} character ({spk}). ")
            + f"The {role_s} ({spos}) says the line once, "
            f"{MV.speaker_how(v, turn['who'], turn.get('text', ''), turn.get('emo', ''))}. "
            + (f"The {role_s}'s voice grows naturally out of a calm ongoing mood and eases back down gently after the line. " if back else
               f"The {role_s}'s expression grows naturally out of a calm ongoing mood and eases back down gently after the line. ")
            + (f"{contrast} " if contrast else "") + quiet + (resting if lis else ""))


_VOICE_RE = re.compile(r"\b(speak\w*|talk\w*|voice\w*|says?|said|speech|spoken|sync\w*|accent|timbre|pitch|loudness|monoton\w*|robotic|echo|reverb|heard|dialogue|pace|words per second"
                       r"|nói|giọng|lời|tiếng nói)\b", re.I)


def silent_prompt(text, v, who, said=""):
    """Prompt của clip IM LẶNG (chỉ lấy HÌNH) cho cảnh người nói quay lưng về camera: Muse tạo hình theo giọng, mà người quay lưng không có miệng nào hiện ra
    nên lời và cả động tác của họ bị gán cho khuôn mặt duy nhất nhìn thấy (người kia mấp máy, làm động tác của người nói). Clip này bỏ mọi câu/mệnh đề về nói, giọng, khẩu hình
    (giữ mô tả hình ảnh, mắt nhìn nhau, hành động), và là clip câm; tiếng lấy từ clip gen có giọng, hai clip ghép lại (voice_swap)."""
    act = re.search(r"ACTION, done WHILE the line is spoken[^:]*:\s*(.+?\.)(?=\s|$)", text)
    for part in re.split(r"(?<=[.!?])\s+", said.strip()):   # chính câu thoại không được lọt vào prompt câm (câu bị cắt ở dấu chấm trong ngoặc kép nên bộ lọc theo câu không bắt được)
        if part:
            text = text.replace(part, "")
    text = text.replace('"', "")
    keep = []
    for line in text.split("\n"):
        parts = re.split(r"(?<=[.!?;])\s+", line.strip())
        keep.append(" ".join(p for p in parts if p and not _VOICE_RE.search(p)))
    out = "\n".join(keep)
    k = MV.ck(who)
    role_s, spos = MV.crole(v, k), MV.cpos(v, k)
    out += (f"\n\nSILENT CLIP: nobody speaks in this clip, there is no dialogue and no voice-over; every character keeps the mouth gently closed for the whole clip and never mouths any words. "
            f"The {role_s} ({spos}) keeps their back to the camera with the face hidden and only moves the head and shoulders naturally"
            + (f"; during the clip, {act.group(1)} " if act else ". "))
    for c in MV.chars_of(v):
        if c != k:
            out += (f"The {MV.crole(v, c)} ({MV.cpos(v, c)}) listens in a natural, living idle (soft blinking, gentle breathing, small attentive head movements, a faint expression that follows the mood), "
                    f"eyes resting on the {role_s}, mouth closed, and does not copy the {role_s}'s movements or gestures. ")
    return out.strip()


def silent_negative(neg):
    return "; ".join(x.strip() for x in neg.split(";") if x.strip() and not re.search(r"speech|voice", x, re.I))


def drop_listener_voice(text, v, turn):
    """Bỏ 'VOICE LOCK' (khoá giọng) của NGƯỜI NGHE khỏi prompt: không có giọng nào được mô tả cho người im lặng thì Muse không có gì để lồng tiếng cho họ."""
    k = MV.ck(turn.get("who"))
    for c in MV.chars_of(v):
        if c == k:
            continue
        voice = str(v.get(f"GIONG_{c}") or "").strip()
        if len(voice) < 12:
            continue
        key = re.escape(voice[:40])
        text = re.sub(r"VOICE LOCK [A-Z ]*: one single voice, " + key + r"[^\n]*?(?:in every clip|every scene)\.\s*", "", text, flags=re.I)
        text = re.sub(r"VOICE LOCK [A-Z ]*: [^\n]{0,40}" + key + r"[^\n]*?(?:in every clip|every scene)\.\s*", "", text, flags=re.I)
    return text


_LISTENER_SCRUB = [
    (r"EVERY character, even a robot or an AI, has a fully human, expressive face and moves like a real person",
     "The speaking character, even a robot or an AI, has a fully human, expressive face and moves like a real person"),
    (r"both settle into the neutral rest pose and hold it completely frozen until the end of the clip",
     "the speaker settles into the neutral rest pose and holds it until the end of the clip, while the other character simply carries on with its own quiet activity"),
    (r"both characters settle into the neutral rest pose",
     "the speaker settles into the neutral rest pose"),
    (r"Nói xong thì cả hai về tư thế nghỉ và đứng im như ảnh tĩnh đến hết clip", "Nói xong người nói về tư thế nghỉ; người kia vẫn tiếp tục việc riêng của mình"),
    (r"Nói xong cả hai về tư thế nghỉ, miệng khép, rồi đứng im hoàn toàn như ảnh tĩnh đến hết clip", "Nói xong người nói về tư thế nghỉ, miệng khép"),
    (r"Accurate lip-sync only for the speaker, and only while speaking; the other character's lips stay closed for the whole clip\.", "Lip-sync only for the speaker."),
    (r"ONE SPEAKER PER CLIP \(strict\):.*?Never two voices in one clip\.",
     "ONE SPEAKER PER CLIP: one character speaks, once; the other is silent and keeps to its own base activity."),
    (r",?\s*(?:and\s+)?glanc(?:es|ing) at (?:it|the phone)(?: between lines)?", ""),
    (r"\s*and glances at the phone, listening", ""),
    (r"at most a tiny nod or a soft blink", "no nod, only natural blinking"),
    (r"\blistening calmly with a still, neutral face, ", ""),
]


_NEG_DROP = re.compile(r"silent character|two characters speaking|wrong character|lip movement while silent|overlapping speech|two voices|both characters|listener|speech until the very last|frozen hold", re.I)


def compact_negative(neg):
    """Như mẫu video call: negative có MỘT cụm ngắn về hai người nói cùng lúc; bỏ các mục nhắc đi nhắc lại người im lặng/nói chồng (dễ gợi ra chính hiện tượng đó)."""
    items = [x.strip() for x in re.split(r";|\.(?=\s)", neg) if x.strip()]
    keep = []
    for x in items:
        if not _NEG_DROP.search(x) and x not in keep:
            keep.append(x)
    return "; ".join(keep + [OVERLAP_NEG])


_NATURAL_RULES = [
    (r"As soon as the line is finished, the speaker settles into the neutral rest pose and holds it until the end of the clip, while the other character simply carries on with its own quiet activity \(a silent frozen tail that is cut in editing\)\.",
     "When the line is finished, the speaker's expression eases down gently and the speaker slips back into the calm ongoing activity; nobody freezes: both keep a natural, living, slightly moving state until the end of the clip (hands working slowly, relaxed face)."),
    (r"Nói xong người nói về tư thế nghỉ; người kia vẫn tiếp tục việc riêng của mình\.",
     "Nói xong biểu cảm của người nói dịu xuống tự nhiên; cả hai vẫn tiếp tục hoạt động nhẹ nhàng, không đóng băng."),
    (r"Final frame to reach: Nói xong người nói về tư thế nghỉ, miệng khép; khung cuối chính là khung tĩnh đó, để lượt sau nối tiếp từ đúng khung này\.",
     "Final frame to reach: người học vẫn đang làm việc đều tay, mắt nhìn công việc, mặt thư giãn (không cười lớn, không ngẩng nhìn); đây là khung đầu của lượt sau."),
    (r"TIMING \(speak first, then freeze\):", "TIMING (speak first, then carry on naturally):"),
    (r"Right after the last word, within half a second, the speaker settles into the neutral rest pose \(lips closed, soft smile, [^)]*\) and then HOLD IT COMPLETELY FROZEN.*?This silent frozen tail is cut in editing, and the next clip starts from this exact frozen frame\.",
     "Right after the last word the speaker's expression eases down gently and the speaker slips back into a calm, natural, living state (a relaxed face with a faint quiet mood, not a big smile, head at a natural height); "
     "the learner's hands keep working at their slow steady pace the whole time, with eyes on the work, and nothing freezes. The camera and lighting do not change. The next clip starts from this exact frame."),
]


def naturalize(text):
    """Bỏ lối kết thúc 'tư thế nghỉ + mỉm cười + đóng băng như ảnh tĩnh' (nguyên nhân khiến nhân vật cứ cuối clip lại ngẩng lên cười, bỏ việc đang làm, rồi clip sau phải đổi tư thế)."""
    for pat, rp in _NATURAL_RULES:
        text = re.sub(pat, rp, text, flags=re.S)
    return text


_UNFREEZE = [
    # "both characters rest ... and stay completely still, like a photo, until the end" / "everyone on screen ... HOLDS IT COMPLETELY FROZEN ..." / "both rest still until the end"
    (r"\b(?:both characters|both|everyone on screen|everyone|all characters)\b(?!\s+(?:hands|arms|feet|sides|eyes|of)\b)[^.]*?\b(?:rest|rests|stay|stays|hold|holds|remain|remains|settle|settles|freeze|freezes)\b"
     r"[^.]*?\b(?:completely still|still|frozen|like a (?:still )?photo(?:graph)?|paused image)\b[^.]*\.",
     "the speaker relaxes into a calm resting pose with the mouth closed, while the other character keeps a natural, living listening idle (soft blinking, gentle breathing, small facial reactions, mouth closed) until the end of the clip."),
    (r"(silent[^.]{0,40}?mouth closed), (?:a )?calm face", r"\1, a living, attentive listening face"),
    (r"cả hai\b[^.;]*?(?:đứng im|giữ im|đứng yên|như ảnh tĩnh)[^.;]*",
     "người nói về tư thế nghỉ, miệng khép; người kia vẫn lắng nghe tự nhiên (chớp mắt, thở, biểu cảm nhẹ, miệng khép) đến hết clip"),
]
_NEG_FREEZE = re.compile(r"final still|movement during|blinking|breathing motion|paused image", re.I)


def unfreeze_listener(text):
    """Chế độ người nghe "idle": gỡ các câu bắt CẢ HAI nhân vật đứng im như ảnh tĩnh trong kịch bản tự viết (câu chữ khác template mẫu nên naturalize() không khớp).
    Người nói vẫn về tư thế nghỉ sau lời thoại; chỉ người nghe được sống tự nhiên."""
    def fix(m, rp):
        out = m.expand(rp) if "\\1" in rp else rp
        return out[:1].upper() + out[1:] if m.group(0)[:1].isupper() else out
    for pat, rp in _UNFREEZE:
        text = re.sub(pat, lambda m, rp=rp: fix(m, rp), text, flags=re.I)
    return text


def unfreeze_negative(neg):
    return "; ".join(x.strip() for x in re.split(r";|\.(?=\s)", neg) if x.strip() and not _NEG_FREEZE.search(x))


def scrub_listener_text(text):
    """Bỏ các cụm làm người nghe 'phản ứng' (liếc điện thoại, gật nhẹ...) khỏi prompt video."""
    for pat, rp in _LISTENER_SCRUB:
        text = re.sub(pat, rp, text, flags=re.I | re.S)
    return naturalize(text)


# Whisper chạy trong MỘT tiến trình con sống suốt phiên (nạp mô hình một lần). Trước đây nạp ngay trong tiến trình Studio: trên máy có Visual C++ Redistributable cũ
# (< 14.40) ctranslate2/onnxruntime crash cứng trong MSVCP140.dll, kéo chết cả Studio và người dùng chỉ thấy "mất kết nối API" khi bấm Gen.
# Giờ nếu thư viện native hỏng thì chỉ tiến trình con chết, cảnh đó cắt theo cách thường, lần sau tự bật tiến trình mới.
# Đọc wav thành mảng float32 thay vì truyền đường dẫn: faster-whisper tự giải mã bằng PyAV và sẽ lỗi trên máy có bản PyAV cũ.
_WHISPER_WORKER = r"""
import json, sys, wave
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
print("ready", flush=True)
for line in sys.stdin:
    j = json.loads(line)
    with wave.open(j["wav"], "rb") as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
    segs, _ = m.transcribe(a, language="en", beam_size=1, vad_filter=False, condition_on_previous_text=False, word_timestamps=j["words"])
    segs = list(segs)
    print(json.dumps({"text": [s.text for s in segs], "words": [(w.word, w.start, w.end) for s in segs for w in (s.words or [])]}), flush=True)
"""
_WP = None
_WP_LINES = None
_WH_LOCK = threading.Lock()


def _wp_read(timeout):
    import queue
    try:
        line = _WP_LINES.get(timeout=timeout)
    except queue.Empty:
        line = None
    if line is None:
        rc = _WP.poll()
        _WP.kill()
        raise RuntimeError("nhận dạng giọng " + (f"bị tắt đột ngột (mã 0x{rc & 0xFFFFFFFF:08X}; chạy 'Chan doan.bat' để kiểm tra)" if rc is not None else "không phản hồi"))
    return line


def _transcribe(wav, words):
    """{'text': [...], 'words': [(từ, bắt đầu, kết thúc)]} của file wav 16 kHz mono, qua tiến trình Whisper riêng."""
    global _WP, _WP_LINES
    import queue
    with _WH_LOCK:
        if _WP is None or _WP.poll() is not None:
            _WP = subprocess.Popen([sys.executable, "-I", "-W", "ignore", "-c", _WHISPER_WORKER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace",
                                   creationflags=0x08000000 if os.name == "nt" else 0)
            _WP_LINES = queue.Queue()

            def pump(out, q):
                for ln in out:
                    q.put(ln)
                q.put(None)
            threading.Thread(target=pump, args=(_WP.stdout, _WP_LINES), daemon=True).start()
            while _wp_read(900).strip() != "ready":   # lần đầu có thể phải tải mô hình (~250 MB)
                pass
        _WP.stdin.write(json.dumps({"wav": os.path.abspath(wav), "words": words}) + "\n")
        _WP.stdin.flush()
        while True:
            ln = _wp_read(300).strip()
            if ln.startswith("{"):
                return json.loads(ln)


def voice_span(path, expected):
    """(bắt đầu, kết thúc) của phần LỜI THOẠI thật trong clip, theo mốc thời gian từng từ của Whisper. Chỉ tính các từ khớp lời thoại nên tiếng cười, thở, 'ha ha' không bị tính.
    None nếu không nhận ra đủ lời."""
    import difflib
    # tính cả SỐ: trước đây chỉ lấy chữ cái nên "I have 48." chỉ còn "i have", từ khớp cuối là "have" -> cắt mất "48" (soi hành lý 04/11).
    # Số viết bằng chữ ("forty-eight") hay chữ số ("48") đều quy về chữ số; mọi số Whisper nghe được đều khớp với số trong lời thoại.
    toks = lambda s: [t for t in (re.sub(r"[^a-z0-9]", "", _NUMW.get(x, x)) for x in re.findall(r"[a-z0-9']+", str(s).lower().replace("-", " "))) if t]
    exp = toks(expected or "")
    if not exp:
        return None
    has_num = any(e.isdigit() for e in exp)
    wav = path + ".span.wav"
    sh(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
    try:
        words = [(t, a, b) for w, a, b in _transcribe(wav, True)["words"] for t in toks(w)]
        onset, offset = _energy_span(wav)
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass
    same = lambda t, e: (has_num and t.isdigit() and e.isdigit()) or difflib.SequenceMatcher(None, t, e).ratio() >= 0.78
    hit = [(a, b) for t, a, b in words if any(same(t, e) for e in exp)]
    # Muse hay nói THÊM một từ của câu sau quãng nghỉ ("How old are you? ... How?", 05/11): từ đó cũng khớp lời thoại nên trước đây được giữ
    # lại thành "thừa thoại". Nay: khi đã nghe đủ (>= 90%) các từ của câu theo đúng thứ tự mà sau đó có quãng nghỉ >= 0,6 s rồi mới có tiếng
    # tiếp, thì câu kết thúc trước quãng nghỉ đó; mọi thứ sau bị cắt bỏ. Câu nói thật không có quãng nghỉ dài như vậy ở giữa.
    need, k, cut_after = max(1, int(round(0.9 * len(exp)))), 0, None
    for i, (t, a, b) in enumerate((x for x in words if any(same(x[0], e) for e in exp))):
        if cut_after is not None:
            break
        if k < len(exp) and same(t, exp[k]):
            k += 1
        elif k < len(exp) and k + 1 < len(exp) and same(t, exp[k + 1]):   # Whisper bỏ sót một từ
            k += 2
        if k >= need and i + 1 < len(hit) and hit[i + 1][0] - b >= 0.6:
            cut_after = i
    if cut_after is not None:
        hit = hit[:cut_after + 1]
    # Whisper ở đây là bản tiếng Anh (small.en). Với câu tiếng Tây Ban Nha nó chỉ khớp vài từ giữa câu: từ khớp đầu muộn hơn lời thật (mất đầu câu,
    # "El inglés", "Descarga Talka"), từ khớp cuối sớm hơn lời thật (mất đuôi câu, "fácil"), hoặc khớp quá ít -> trước đây trả None và cắt theo cách
    # thường, để lại đoạn nghỉ dài. Bổ sung lúc có tiếng nói thật theo năng lượng âm thanh (không phụ thuộc ngôn ngữ).
    if len(hit) < max(1, int(0.5 * len(exp))):
        return (onset, offset) if onset is not None and offset is not None and offset - onset > 0.5 else None
    start = onset if onset is not None and onset < hit[0][0] else hit[0][0]
    end = hit[-1][1]
    if cut_after is None and offset is not None and end < offset <= end + 1.5:   # tiếng nói còn tiếp sau từ khớp cuối (từ cuối Whisper không nhận ra)
        end = offset
    return start, end


def _energy_span(wav):
    """(giây bắt đầu, giây kết thúc) của tiếng nói trong file wav 16 kHz mono theo năng lượng âm thanh (vượt nền rõ rệt, liên tục ~60 ms); (None, None) nếu không rõ."""
    import wave
    import numpy as np
    try:
        with wave.open(wav, "rb") as w:
            sr = w.getframerate()
            a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
    except (OSError, wave.Error):
        return None, None
    win, hop = int(sr * 0.025), int(sr * 0.01)
    if len(a) < 2 * win:
        return None, None
    fr = np.lib.stride_tricks.sliding_window_view(a, win)[::hop]
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9)
    floor, level = np.percentile(db, 10), np.percentile(db, 90)
    if level - floor < 15:
        return None, None
    above = db > max(floor + 10, level - 15)
    starts = [k for k in range(len(above) - 5) if above[k:k + 6].all()]
    if not starts:
        return None, None
    return starts[0] * hop / sr, (starts[-1] + 6) * hop / sr + win / sr


def heard_words(path):
    wav = path + ".chk.wav"
    sh(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
    try:
        return [w for t in _transcribe(wav, False)["text"] for w in re.findall(r"[a-z']+", t.lower())]
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass


def word_check(expected, heard):
    """(tỉ lệ từ mong đợi nghe thấy, tỉ lệ từ thừa không thuộc lời) hoặc None nếu câu quá ngắn / không phải tiếng Anh."""
    import difflib
    norm = lambda w: re.sub(r"[^a-z]", "", w.lower())
    exp = [norm(w) for w in re.findall(r"[A-Za-z']+", expected) if norm(w)]
    hrd = [norm(w) for w in heard if norm(w)]
    if len(exp) < 4 or not hrd:
        return None
    ratio = lambda a, b: difflib.SequenceMatcher(None, a, b).ratio()
    matched = sum(1 for e in exp if any(ratio(e, h) >= 0.8 for h in hrd))
    extra = sum(1 for h in hrd if not any(ratio(h, e) >= 0.7 for e in exp))
    return matched / len(exp), extra / len(hrd)


def side_box(side, table):
    """Vùng khuôn mặt của một vị trí: tên có sẵn trong `table` (LEFT/RIGHT/TOP/BOTTOM) hoặc hộp "x0,y0,x1,y1" theo tỉ lệ khung hình (0..1), dùng cho bố cục bất kỳ."""
    side = str(side or "").strip()
    if side.upper() in table:
        return table[side.upper()]
    try:
        b = tuple(float(x) for x in side.split(","))
        if len(b) == 4 and 0 <= b[0] < b[2] <= 1 and 0 <= b[1] < b[3] <= 1:
            return b
    except ValueError:
        pass
    return None   # nhãn lạ và không có toạ độ: không biết khuôn mặt ở đâu nên không đo (đo nhầm mặt còn tệ hơn bỏ qua)


ZONES = {"LEFT": (0.03, 0.12, 0.47, 0.52), "RIGHT": (0.53, 0.08, 0.97, 0.50), "TOP": (0.2, 0.02, 0.8, 0.34), "BOTTOM": (0.1, 0.42, 0.8, 0.85)}   # vùng đầu/mặt mỗi bên (tỉ lệ khung hình)


def zone_motion(path, side, t_end, fps=15, W=180, H=320):
    """Mức chuyển động trung bình ở vùng mặt của một bên trong [0, t_end] (người nói thật ~8-12, người nghe đứng yên ~2-4)."""
    box = side_box(side, ZONES)
    if box is None:
        return 0.0
    x0, y0, x1, y1 = box
    d = crun(["ffmpeg", "-v", "error", "-t", f"{max(0.5, t_end):.2f}", "-i", path, "-vf", f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(d) // (W * H)
    if n < 3:
        return 0.0
    a = np.frombuffer(d[: n * W * H], np.uint8).reshape(n, H, W).astype(np.float32)[:, int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    return float(np.abs(np.diff(a, axis=0)).mean())


def speech_end_of(path):
    total = duration(path)
    st, en = _silences(path)
    return st[-1] if st and (len(en) < len(st) or en[-1] >= total - 0.06) else total


_MP_LOCK = threading.Lock()
_FACE_BOX = {"LEFT": (0.0, 0.0, 0.62, 0.62), "RIGHT": (0.55, 0.12, 1.0, 0.62),
             "TOP": (0.12, 0.0, 0.88, 0.38), "BOTTOM": (0.0, 0.40, 0.9, 0.92)}   # TOP/BOTTOM: bố cục khung gia sư ngang ở trên, người học ở dưới


OPEN_GAP = 0.15   # khoảng hở môi / bề rộng miệng từ mức này là há miệng thật; hé môi cười thường dưới mức này


def mouth_activity(path, side, t_end, fps=12):
    """(độ lệch chuẩn, cực đại, tỉ lệ khung hình há miệng rộng, tốc độ mở-khép) của độ mở miệng (khoảng hở môi / bề rộng miệng) ở khuôn mặt bên `side` trong [0, t_end]. None nếu không dò được mặt."""
    import cv2
    import face_mesh as FM
    W, H = 360, 640
    d = crun(["ffmpeg", "-v", "error", "-t", f"{max(0.5, t_end):.2f}", "-i", path, "-vf", f"fps={fps},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(d) // (W * H * 3)
    if n < 6:
        return None
    fr = np.frombuffer(d[: n * W * H * 3], np.uint8).reshape(n, H, W, 3)
    b = side_box(side, _FACE_BOX)
    if b is None:
        return None
    x0, y0, x1, y1 = int(b[0] * W), int(b[1] * H), int(b[2] * W), int(b[3] * H)
    vals = []
    with _MP_LOCK:
        fm = FM.landmarker(min_conf=0.3)
        try:
            for f in fr:
                c = cv2.resize(f[y0:y1, x0:x1], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                g = fm.mouth_gap(c)
                if g is not None:
                    vals.append(g)
        finally:
            fm.close()
    if len(vals) < 6:
        return None
    a = np.array(vals)
    return float(a.std()), float(a.max()), float((a > OPEN_GAP).mean()), float(np.abs(np.diff(a)).mean())


def mouth_unavailable_msg(ex, first=True):
    """Thông báo khi không chạy được kiểm tra miệng (thường là mediapipe lỗi DLL). Lần đầu trong một lần chạy kèm gợi ý nguyên nhân và cách chẩn đoán."""
    msg = str(ex)
    if first and ("DLL" in msg or "dynamic link library" in msg.lower()):
        return (f"{msg} | Thường do thiếu Microsoft Visual C++ Redistributable x64 (https://aka.ms/vs/17/release/vc_redist.x64.exe) hoặc CPU/máy ảo không hỗ trợ AVX; "
                "chạy 'Chan doan.bat' để kiểm tra. Gen video và Hậu kỳ vẫn bình thường, chỉ tắt tính năng chống người nghe mấp máy miệng.")
    return msg


def mouth_check(path, speaker_side, listener_side, sens="normal"):
    """Người NGHE mấp máy miệng như người nói? Đã đối chiếu trên clip thật: người im lặng thật std ≈ 0.008-0.019, người mấp máy ≥ 0.029.
    `listener_side` có thể là một vị trí hoặc danh sách (nhiều người nghe): trả về người nghe bị lỗi đầu tiên, nếu không thì người cử động miệng nhiều nhất (`idx` = chỉ số trong danh sách)."""
    t_end = speech_end_of(path)
    sp = mouth_activity(path, speaker_side, t_end)
    if not sp:
        return None
    abs_t, rel_t = {"high": (0.017, 0.35), "low": (0.032, 0.6)}.get(sens, (0.024, 0.45))   # độ nhạy: cao bắt cả mấp máy nhẹ (dễ gen lại thừa), thấp chỉ bắt mấp máy rõ
    open_t = {"high": 0.10, "low": 0.30}.get(sens, 0.18)   # tỉ lệ khung hình người nghe há miệng rộng: mấp máy thật ~0.2-0.35, chỉ cười ~0-0.13
    best = None
    for idx, side in enumerate(listener_side if isinstance(listener_side, (list, tuple)) else [listener_side]):
        li = mouth_activity(path, side, t_end)
        if not li:
            continue
        # Phải thoả TẤT CẢ: miệng cử động nhiều (std), há rộng thật sự đủ lâu, và mở-khép nhanh gần bằng người nói. Hé môi hoặc cười (kể cả lộ răng) làm tăng std nhưng ít há rộng / giữ yên nên không bị tính là mấp máy.
        bad = li[0] >= abs_t and li[0] >= rel_t * sp[0] and li[2] >= open_t and li[2] >= 0.4 * sp[2] and li[3] >= 0.55 * sp[3]
        # Người nghe cử động miệng gần bằng người nói (>= 70%) và có há miệng thật thì chắc chắn là nói theo, kể cả khi nhịp mở-khép chưa đủ nhanh
        bad = bad or (sens != "low" and li[0] >= 0.7 * sp[0] and li[2] >= 0.12 and li[0] >= abs_t)
        r = {"bad": bad, "speaker": round(sp[0], 3), "listener": round(li[0], 3), "open": round(li[2], 2), "idx": idx}
        if best is None or (r["bad"] and not best["bad"]) or (r["bad"] == best["bad"] and r["listener"] > best["listener"]):
            best = r
    return best


def overlap_check(path, speaker_side, listener_side, expected_text):
    """Phát hiện nghi vấn nói chồng/nhầm người: (1) mặt người NGHE cử động như người nói, (2) lời nghe được lệch lời mong đợi nhiều."""
    t_end = speech_end_of(path)
    sp, li = zone_motion(path, speaker_side, t_end), zone_motion(path, listener_side, t_end)
    bad_motion = False  # chuyển động mặt không đáng tin với bố cục điện thoại -> chỉ ghi số liệu, không dùng để quyết định
    wc = None
    try:
        wc = word_check(expected_text, heard_words(path))
    except Exception:  # noqa: BLE001 - thiếu mô hình/âm thanh: bỏ qua kiểm tra lời
        pass
    bad_words = bool(wc) and (wc[0] < 0.5 or wc[1] > 0.5)
    return {"bad": bad_motion or bad_words, "speaker": round(sp, 1), "listener": round(li, 1), "words": wc, "why": "lời nghe được lệch lời thoại" if bad_words else ""}


_NUMW = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
_NUMW.update({w: str(10 * i) for i, w in enumerate("x x twenty thirty forty fifty sixty seventy eighty ninety".split()) if i >= 2})


_CONTR = {"won't": "will not", "can't": "can not", "cannot": "can not", "shan't": "shall not", "let's": "let us", "gonna": "going to", "wanna": "want to"}
_FILLERS = {"um", "umm", "uh", "uhh", "ah", "oh", "hmm", "hm", "er", "erm", "mm", "mhm"}
SPEECH_RETRIES = 2   # gen lại tối đa khi lời nói sai (lặp / thừa / thiếu chữ); giữ lần ít lỗi nhất


def _speech_tokens(text):
    """Từ thường viết thường, bỏ tiếng ừm/à; viết tắt mở ra ("I'm" = "I am", "don't" = "do not") để chữ viết khác nhau không bị tính là sai;
    số (chữ hay chữ số) quy về chữ số, "sixty eight" gộp thành "68" để khớp "68"."""
    s = str(text).lower().replace("’", "'").replace("-", " ")
    s = re.sub(r"\b(" + "|".join(map(re.escape, _CONTR)) + r")\b", lambda m: _CONTR[m.group(1)], s)
    s = re.sub(r"n't\b", " not", s)
    s = re.sub(r"'(re|m|ll|ve|d|s)\b", lambda m: " " + {"re": "are", "m": "am", "ll": "will", "ve": "have", "d": "would", "s": "is"}[m.group(1)], s)
    out = []
    for w in re.findall(r"[a-z0-9']+", s):
        w = _NUMW.get(w.strip("'"), w.strip("'"))
        if not w or w in _FILLERS:
            continue
        if out and w.isdigit() and len(w) == 1 and w != "0" and out[-1].isdigit() and len(out[-1]) == 2 and out[-1].endswith("0") and out[-1] != "10":
            out[-1] = str(int(out[-1]) + int(w))   # "sixty" "eight" -> "68"
        else:
            out.append(w)
    return out


def speech_issues(expected, path):
    """Lỗi lời nói của clip so với câu mong đợi (Whisper): từ/cụm bị nói lặp (mà câu gốc không lặp), thừa dù chỉ 1 từ lạ, hoặc thiếu dù chỉ 1 từ
    (lời phải đúng từng chữ, 04/11/2026). Viết tắt, số, tiếng ừm/à đã chuẩn hoá trong _speech_tokens; chữ "nghe" được ở đoạn im cách xa câu thoại (> 1,2 giây,
    Whisper hay bịa "Thank you" ở đó) không tính là thừa.
    Trả về danh sách (mô tả tiếng Việt cho nhật ký, mô tả tiếng Anh cho ghi chú gen lại) (rỗng = đạt); None nếu không kiểm được (câu rỗng, không có Whisper)."""
    import difflib
    exp = _speech_tokens(expected)
    if not exp:
        return None
    wav = path + ".sp.wav"
    sh(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
    try:
        res = _transcribe(wav, True)
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass
    near = lambda a, b: a == b or (len(a) > 2 and len(b) > 2 and difflib.SequenceMatcher(None, a, b).ratio() >= 0.75)
    timed = [(t, float(w[1]), float(w[2])) for w in (res.get("words") or []) for t in _speech_tokens(w[0])]
    if not timed:   # bản Whisper không trả mốc thời gian: dùng chữ thường
        timed = [(t, 0.0, 0.0) for t in _speech_tokens(" ".join(res.get("text") or []))]
    hit_t = [(s, e) for t, s, e in timed if any(near(t, x) for x in exp)]
    if hit_t:   # bỏ chữ ở đoạn im xa câu thoại (Whisper bịa khi không có lời)
        lo, hi = min(s for s, _ in hit_t) - 1.2, max(e for _, e in hit_t) + 1.2
        timed = [x for x in timed if lo <= x[1] <= hi]
    hrd = [t for t, _, _ in timed]
    if not hrd:
        return [("không nghe thấy lời", "no speech was heard")]

    def join_compounds(a, other):   # từ ghép viết liền / rời khác nhau giữa kịch bản và Whisper ("anytime" / "any time")
        o, out = set(other), []
        for t in a:
            if out and out[-1] + t in o and out[-1] not in o:
                out[-1] += t
            else:
                out.append(t)
        return out
    hrd, exp = join_compounds(hrd, exp), join_compounds(exp, hrd)
    out, es = [], " " + " ".join(exp) + " "
    for n in (4, 3, 2, 1):   # cụm dài trước: "what I'm here for, what I'm here for"
        for i in range(len(hrd) - 2 * n + 1):
            if hrd[i:i + n] == hrd[i + n:i + 2 * n] and (" " + " ".join(hrd[i:i + 2 * n]) + " ") not in es:
                rep = " ".join(hrd[i:i + n])
                out.append((f'nói lặp "{rep}"', f'the words "{rep}" were said twice'))
                break
        if out:
            break
    extra = [h for h in hrd if not any(near(h, e) for e in exp)]
    if extra:
        out.append((f'thừa từ ngoài lời thoại ({" ".join(extra[:5])})', f'extra words not in the line were said ({" ".join(extra[:5])})'))
    # từ CỦA CÂU được nói nhiều lần hơn trong câu, dù không liền nhau ("How old are you? ... How?", 05/11): trước đây lọt vì vừa không lặp liền, vừa không lạ
    cnt = {}
    for h in hrd:   # mỗi từ nghe được chỉ tính cho MỘT từ của câu, từ giống nhất (near() cho "show" ~ "how": không được đếm "show" vào "how")
        best = max((e for e in dict.fromkeys(exp) if near(h, e)), key=lambda e: (h == e, difflib.SequenceMatcher(None, h, e).ratio()), default=None)
        if best is not None:
            cnt[best] = cnt.get(best, 0) + 1
    over = [e for e in dict.fromkeys(exp) if cnt.get(e, 0) > exp.count(e) and (len(e) > 1 or cnt[e] > exp.count(e) + 1)]   # từ 1 chữ ("a", "I") Whisper hay nghe thừa một lần: bỏ qua
    if over and not any("nói lặp" in v for v, _ in out):
        out.append((f'nói thừa từ của câu ({" ".join(over[:5])})', f'these words of the line were said more times than in the line ({" ".join(over[:5])})'))
    miss = [e for e in exp if not any(near(e, h) for h in hrd)]
    if miss:
        out.append((f'thiếu lời ({" ".join(miss[:5])})', f'these words of the line were missing: {" ".join(miss[:5])}'))
    return out


def speech_retry(path, expected, regen, emit, n, retries=1):
    """Kiểm tra lời nói của clip vừa gen; lỗi (lặp từ, thừa từ, thiếu lời) thì gọi regen(ghi chú sửa) tối đa `retries` lần, cuối cùng giữ lần ít lỗi nhất."""
    tried = []
    for k in range(retries + 1):
        try:
            iss = speech_issues(expected, path)
        except Exception as ex:  # noqa: BLE001 - thiếu Whisper / âm thanh hỏng: bỏ qua kiểm tra
            emit("log", msg=f"Cảnh {n}: bỏ qua kiểm tra lời nói ({ex})", level="warn")
            iss = None
        if not iss:
            if iss is not None and tried:
                emit("log", msg=f"Cảnh {n}: lời nói đạt sau {k} lần gen lại")
            break
        emit("log", msg=f"Cảnh {n}: lần {k + 1} lời nói lỗi: {'; '.join(v for v, _ in iss)}", level="warn")
        keep = f"{path}.sp{k}"
        shutil.copyfile(path, keep)
        tried.append((len(iss), k, keep))
        if k == retries:
            best = min(tried)
            shutil.copyfile(best[2], path)
            emit("log", msg=f"Cảnh {n}: vẫn lỗi lời nói sau {retries} lần gen lại, giữ lần ít lỗi nhất. Bấm gen lại cảnh này nếu muốn thử tiếp", level="warn")
            break
        emit("scene", n=n, state="video", pct=0, note=f"gen lại (lời nói) {k + 1}")
        regen(f'IMPORTANT RETRY NOTE: in the previous attempt the speech was wrong ({"; ".join(e for _, e in iss)}). Say the line exactly once, word for word: "{expected}". '
              "Do not repeat any word or phrase, do not add any word before or after it, do not stutter, then stop talking.")
    for _, _, f in tried:
        try:
            os.remove(f)
        except OSError:
            pass


# ------------------------------------------------------------------ cắt clip + chọn khung nối
def _silences(path, noise="-35dB", dmin=0.25):
    r = crun(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={noise}:d={dmin}", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return st, en


def _gray_frames(path, t0, t1, fps=24, w=90, h=160):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", path, "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"]
    d = crun(cmd, capture_output=True).stdout
    n = len(d) // (w * h)
    return np.frombuffer(d[: n * w * h], np.uint8).reshape(n, h, w).astype(np.float32)


def _mean_db(path, t0, t1):
    r = crun(["ffmpeg", "-hide_banner", "-ss", f"{t0:.2f}", "-t", f"{max(0.2, t1 - t0):.2f}", "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"],
             capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else None


def head_check(clip, cut, factor=1.0, span=1.2):
    """So độ to của `span` giây đầu clip gốc với clip đã cắt: lệch nhiều nghĩa là đầu câu có thể đã bị cắt/mất. Trả về (lệch dB, mô tả) hoặc None."""
    a, b = _mean_db(clip, 0.0, span * factor), _mean_db(cut, 0.0, span)
    if a is None or b is None:
        return None
    return round(b - a, 1), f"đầu clip gốc {a:.0f}dB, sau cắt {b:.0f}dB"


def camera_drift(path, fps=4, w=360, h=640):
    """Máy quay có trôi / lia / đẩy vào trong clip không, so với khung ĐẦU: (dịch ngang lớn nhất theo tỉ lệ bề ngang, dịch dọc theo tỉ lệ chiều cao, |log(tỉ lệ zoom)|
    lớn nhất, số điểm nền khớp ít nhất). Khớp điểm đặc trưng ORB giữa khung đầu và từng khung (4 khung/giây), ước lượng phép dời+xoay+phóng bằng RANSAC: điểm
    khớp chủ yếu nằm trên nền tĩnh (biển, cột, máy móc) nên người cử động không làm lệch. Dịch đo ở tâm khung (gồm cả phần do zoom). Đo thật (soi hành lý 05/11):
    máy đứng yên ≤ 1,2% / zoom ≤ 2%; máy lia (cảnh 1) 74%; máy đẩy vào (cảnh 13) 52%, zoom lớn, chỉ còn 5 điểm khớp. None nếu không đọc được clip."""
    import cv2
    fr = _gray_frames(path, 0.0, max(0.5, video_duration(path)), fps, w, h).astype(np.uint8)
    if len(fr) < 2:
        return None
    orb = cv2.ORB_create(1500)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    k0, d0 = orb.detectAndCompute(fr[0], None)
    if d0 is None or len(k0) < 20:
        return None
    dx = dy = dz = 0.0
    inl_min = 10 ** 6
    for f in fr[1:]:
        k1, d1 = orb.detectAndCompute(f, None)
        m = bf.match(d0, d1) if d1 is not None else []
        if len(m) < 20:
            inl_min = min(inl_min, len(m))
            continue
        p0 = np.float32([k0[x.queryIdx].pt for x in m])
        p1 = np.float32([k1[x.trainIdx].pt for x in m])
        M, inl = cv2.estimateAffinePartial2D(p0, p1, method=cv2.RANSAC, ransacReprojThreshold=3)
        if M is None:
            inl_min = 0
            continue
        s = float(np.hypot(M[0, 0], M[0, 1]))
        cx, cy = w / 2, h / 2
        nx, ny = M[0, 0] * cx + M[0, 1] * cy + M[0, 2], M[1, 0] * cx + M[1, 1] * cy + M[1, 2]
        dx, dy, dz = max(dx, abs(nx - cx) / w), max(dy, abs(ny - cy) / h), max(dz, abs(float(np.log(max(s, 1e-6)))))
        inl_min = min(inl_min, int(inl.sum()) if inl is not None else 0)
    return round(dx, 3), round(dy, 3), round(dz, 3), inl_min


CAM_MAX = (0.035, 0.035, 0.05, 15)   # ngưỡng máy trôi (dịch ngang, dịch dọc, zoom, số điểm nền khớp TỐI THIỂU) cho clip "máy đứng yên"; cầm tay rung nhẹ vẫn dưới mức này


def camera_retry(path, regen, emit, n, retries=1, limits=CAM_MAX):
    """Clip phải quay máy đứng yên: đo máy trôi; vượt ngưỡng thì gen lại kèm ghi chú (tối đa `retries` lần), giữ lần ít trôi nhất."""
    tried = []
    for k in range(retries + 1):
        try:
            d = camera_drift(path)
        except Exception as ex:  # noqa: BLE001 - không đo được: bỏ qua
            emit("log", msg=f"Cảnh {n}: không đo được máy trôi ({ex})", level="warn")
            return
        if d is None:
            return
        bad = [nm for nm, v, lim in zip(("ngang", "dọc", "zoom"), d, limits) if v > lim] + (["khung đổi hẳn"] if d[3] < limits[3] else [])
        desc = f"ngang {100 * d[0]:.1f}%, dọc {100 * d[1]:.1f}%, zoom {100 * d[2]:.1f}%, {d[3]} điểm nền khớp"
        if not bad:
            if k:
                emit("log", msg=f"Cảnh {n}: lần {k + 1} máy đứng yên ({desc})")
            break
        emit("log", msg=f"Cảnh {n}: lần {k + 1} máy trôi ({', '.join(bad)}: {desc})", level="warn")
        keep = f"{path}.cam{k}"
        shutil.copyfile(path, keep)
        tried.append((max([v / lim for v, lim in zip(d, limits)] + [limits[3] / max(d[3], 1)]), k, keep))
        if k == retries:
            best = min(tried)
            shutil.copyfile(best[2], path)
            emit("log", msg=f"Cảnh {n}: máy vẫn trôi sau {retries} lần gen lại, giữ lần ít trôi nhất. Bấm gen lại cảnh này nếu thấy khung hình đổi", level="warn")
            break
        emit("scene", n=n, state="video", pct=0, note=f"gen lại (máy trôi) {k + 1}")
        regen("IMPORTANT RETRY NOTE: in the previous attempt the camera moved (it drifted, panned or pushed in toward the people). The camera is LOCKED on a tripod: "
              "the framing of the start frame stays pixel-for-pixel the same for the whole clip; nothing at the edges of the frame enters or leaves; only the people move inside the frame.")
    for _, _, f in tried:
        try:
            os.remove(f)
        except OSError:
            pass


def speed_factor(syll, spoken, max_speed=1.25, ok_rate=3.4, target_rate=4.0, soften=0.7, top_rate=4.8):
    """Hệ số tăng tốc cho lời bị Muse kéo chậm. Nhịp nói = âm tiết/giây (cả khoảng ngắt). Từ `ok_rate` trở lên: để nguyên.
    Chậm hơn: tăng một PHẦN (`soften`) khoảng cách tới nhịp mục tiêu, chặn ở `max_speed`, và không bao giờ đẩy nhịp sau chỉnh vượt `top_rate` (tránh nghe quá nhanh)."""
    rate = syll / spoken
    if rate >= ok_rate:
        return 1.0
    f = 1.0 + soften * (target_rate / rate - 1.0)
    f = min(f, max_speed, top_rate / rate)
    return round(f, 3) if f > 1.03 else 1.0


def _first_closed_mouth(src, t0, t1, limit=0.04, fps=24):
    """Mốc (giây) của khung đầu tiên trong [t0, t1] mà người trong khung (một người, cả khung hình) khép miệng; t0 đã khép thì trả t0.
    None nếu không có khung khép miệng hoặc không dò được mặt / không chạy được mediapipe."""
    try:
        import cv2
        import face_mesh as FM
        W, H = 360, 640
        d = crun(["ffmpeg", "-v", "error", "-ss", f"{max(0.0, t0):.3f}", "-t", f"{max(0.1, t1 - t0):.3f}", "-i", src, "-vf", f"fps={fps},scale={W}:{H}",
                  "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        n = len(d) // (W * H * 3)
        if n == 0:
            return None
        fr = np.frombuffer(d[: n * W * H * 3], np.uint8).reshape(n, H, W, 3)
        with _MP_LOCK:
            fm = FM.landmarker(min_conf=0.3)
            try:
                for i, f in enumerate(fr):
                    g = fm.mouth_gap(cv2.resize(f, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))
                    if g is not None and g < limit:
                        return max(0.0, t0) + i / fps
            finally:
                fm.close()
    except Exception:  # noqa: BLE001
        return None
    return None


def smart_cut(src, cut_path, last_png, lo=0.15, hi=0.8, fps=24, syll=None, speedfix=True, vf_extra="", max_speed=1.25, span=None, head_margin=0.2, close_mouth=0.0):
    """Cắt đuôi sau lời nói. Điểm cắt = khung ít chuyển động nhất trong [hết lời+lo, hết lời+hi].
    Khung cuối của clip đã cắt (last_png) là khung đầu cho clip kế.
    close_mouth > 0 (clip MỘT người, chế độ ghép 2 lớp): khung cắt còn hé miệng thì cắt muộn thêm tối đa chừng ấy giây tới khung khép miệng đầu tiên.
    Không làm thì clip nghe cảnh sau của chính người này bắt đầu từ khung hé miệng và Muse giữ môi hé/mấp máy cả clip (05/11/2026, chia-doi BT12 cảnh 2)."""
    total = duration(src)
    st, en = _silences(src)
    speech_end = total
    if st and (len(en) < len(st) or en[-1] >= total - 0.06):
        speech_end = st[-1]
    speech_start = en[0] if (st and st[0] <= 0.05 and en) else 0.0
    head = 0.0
    if span:   # biết chính xác từ đầu/từ cuối của lời thoại: cắt sát, chỉ chừa một chút ở hai đầu
        speech_start, speech_end = max(0.0, span[0]), min(total, span[1])
        if speech_start - head_margin > 0.25:   # có đoạn im/ồn dài trước lời: bỏ bớt, chừa `head_margin`
            head = speech_start - head_margin
    t0, t1 = min(total - 0.1, speech_end + lo), min(total - 0.04, speech_end + hi)
    cut_t = max(0.5, total - 0.04)
    if t1 - t0 >= 0.12:
        w0 = max(0.0, t0 - 1 / fps)
        fr = _gray_frames(src, w0, t1 + 1 / fps, fps)
        if len(fr) >= 4:
            d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))          # d[i] = chuyển động giữa khung i và i+1
            score = d[:-1] + d[1:]                                      # chuyển động quanh khung i+1
            k = int(np.where(score <= score.min() * 1.2 + 0.05)[0][0]) + 1          # khung yên tĩnh SỚM nhất (cắt càng sớm càng gọn)
            cut_t = w0 + (k + 1) / fps                                  # cắt sau khung k (giữ khung k làm khung cuối)
    cut_t = max(0.6, min(total, cut_t))
    if close_mouth and cut_t < total - 0.05:   # khung cuối còn hé miệng: kéo điểm cắt tới khung khép miệng đầu tiên (tối đa close_mouth giây)
        t_closed = _first_closed_mouth(src, cut_t - 1 / fps, min(total - 0.04, cut_t + close_mouth))
        if t_closed is not None and t_closed > cut_t:
            cut_t = min(total, t_closed + 1 / fps)
    # Muse hay kéo giãn clip cho đủ độ dài: phần lớn là KHOẢNG NGẮT dài giữa các cụm từ chứ không phải giọng nói chậm. Nên:
    #  - khoảng ngắt dài (>=0.55s) được tua nhanh (tối đa x2, hình gần như đứng yên nên không lộ), giọng nói giữ nguyên tốc độ;
    #  - chỉ khi nhịp nói THẬT (tính riêng phần có tiếng) vẫn chậm mới tăng nhẹ tốc độ giọng, tối đa `max_speed`.
    # Khung cuối không đổi nên vẫn nối đúng với clip sau.
    inner = [(x, y) for x, y in zip(st, en) if x >= speech_start - 0.01 and y <= min(speech_end, cut_t) + 0.02 and y > x]
    voiced = max(0.3, (speech_end - speech_start) - sum(y - x for x, y in inner))
    sf = speed_factor(syll, voiced, max_speed, ok_rate=3.0, target_rate=3.6) if (speedfix and syll and syll >= 8) else 1.0  # câu rất ngắn (ừm, à, For real?) vốn nói chậm có chủ ý: không tăng tốc giọng
    longs = [(x, y) for x, y in inner if speedfix and y - x >= 0.55]
    if sf <= 1.02 and not longs:
        factor = 1.0
        cmd1 = ["ffmpeg", "-y"] + (["-ss", f"{head:.3f}"] if head else []) + ["-i", src, "-t", f"{cut_t - head:.3f}"] + (["-vf", vf_extra] if vf_extra else []) +                ["-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", cut_path]
        sh_enc(cmd1, vf_index=cmd1.index("-vf") if vf_extra else None)
    else:
        factor = sf if sf > 1.02 else 1.0
        sf = factor
        segs, pos = [], head
        for x, y in longs:
            if x < head:
                continue
            if x > pos + 0.05:
                segs.append((pos, x, sf))
            segs.append((x, y, max(sf, min(2.0, (y - x) / 0.4))))
            pos = y
        segs.append((pos, cut_t, sf))
        segs = [(u, v, f) for u, v, f in segs if v - u > 0.04]
        n = len(segs)
        atempo = lambda f: f"atempo={f:.4f}"
        fc = f"[0:v]{vf_extra or 'null'}[c];[c]split={n}" + "".join(f"[c{i}]" for i in range(n)) + f";[0:a]asplit={n}" + "".join(f"[a{i}]" for i in range(n)) + ";"
        for i, (u, v, f) in enumerate(segs):
            fc += f"[c{i}]trim={u:.3f}:{v:.3f},setpts=(PTS-STARTPTS)/{f:.4f}[v{i}];[a{i}]atrim={u:.3f}:{v:.3f},asetpts=PTS-STARTPTS,{atempo(f)}[x{i}];"
        fc += "".join(f"[v{i}][x{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
        try:
            sh_enc(["ffmpeg", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", cut_path])
        except RuntimeError:   # lọc phức tạp lỗi: cắt đơn giản không tăng tốc / không cân màu
            sh_enc(["ffmpeg", "-y"] + (["-ss", f"{head:.3f}"] if head else []) + ["-i", src, "-t", f"{cut_t - head:.3f}", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", cut_path])
            factor = 1.0; longs = []
    grab_frame(cut_path, last_png, sseof=-0.06)
    return {"total": total, "cut": duration(cut_path), "speech_end": speech_end, "speed": round(factor, 2), "pauses": round(sum(y - x for x, y in longs), 1)}


def prepend_preroll(pre_src, main, secs, vf_pre=""):
    """Ghép đoạn mở đầu không lời (clip Muse `pre_src`, tua cho vừa `secs` giây, tối đa nhanh 3 lần) vào ĐẦU clip cảnh `main` (cắt cứng), cùng cỡ khung / fps với `main`.
    Tiếng mở đầu: `secs` giây đầu của chính clip đó (tiếng sảnh, băng chuyền), mờ dần cuối; clip câm thì dùng im lặng."""
    w, h = (int(v) for v in sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", main]).stdout.strip().split("x")[:2])
    d = video_duration(pre_src)
    k = max(1.0, min(1.25, d / secs))   # gần đúng tốc độ thật: tua nhanh làm vali vút qua (user 03/11)
    secs = min(secs, d / k)
    a_pre = (f"[0:a]atrim=0:{secs:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(0.0, secs - 0.3):.3f}:d=0.3,aresample=48000,aformat=channel_layouts=stereo[pa];" if has_audio(pre_src)
             else f"anullsrc=r=48000:cl=stereo,atrim=0:{secs:.3f}[pa];")
    fc = (f"[0:v]setpts=(PTS-STARTPTS)/{k:.3f},trim=0:{secs:.3f},setpts=PTS-STARTPTS,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30,setsar=1" + (f",{vf_pre}" if vf_pre else "") + "[pv];"
          f"[1:v]fps=30,setsar=1[mv];{a_pre}[1:a]aresample=48000,aformat=channel_layouts=stereo[ma];[pv][pa][mv][ma]concat=n=2:v=1:a=1[v][a]")
    tmp = main + ".pre.mp4"
    sh_enc(["ffmpeg", "-y", "-i", pre_src, "-i", main, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", tmp])
    os.replace(tmp, main)
    return secs, k


def pan_span(path, min_t=0.0):
    """(bắt đầu, kết thúc) của đoạn camera lia mạnh nhất trong clip, từ `min_t` trở đi; None nếu không thấy. Đo dịch chuyển toàn khung giữa hai khung liền nhau (phase correlation)."""
    import cv2
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    prev, mv = None, []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(fr, (160, 284)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        mv.append(float(np.hypot(*cv2.phaseCorrelate(prev, g)[0])) if prev is not None else 0.0)
        prev = g
    cap.release()
    if len(mv) < 6:
        return None
    s = np.convolve(np.array(mv), np.ones(3) / 3, mode="same")
    i0 = int(min_t * fps)
    thr = max(0.8, 0.25 * float(s[i0:].max(initial=0)))
    best, run = None, None
    for i in range(i0, len(s)):
        if s[i] > thr:
            run = [i, i] if run is None else [run[0], i]
        if run and (s[i] <= thr or i == len(s) - 1):
            tot = float(s[run[0]:run[1] + 1].sum())
            if tot >= 8 and (best is None or tot > best[2]):   # tổng dịch >= 8 px trên khung rộng 160 (~5%): là cú lia thật, không phải rung tay
                best = (run[0], run[1], tot)
            run = None
    return (best[0] / fps, (best[1] + 1) / fps) if best else None


def whip_speedup(path, factor, min_t=0.0, blur=28, follow=0.0, follow_from=0.0):
    """Tua nhanh đoạn camera lia (sau `min_t`, thường là hết lời) `factor` lần và thêm nhoè ngang cho ra cú lia vụt có lực như quay thật;
    tiếng: bỏ bớt đoạn im lặng tương ứng ngay sau điểm bắt đầu lia. Khung cuối không đổi. Trả về (t0, t1, độ dài mới của đoạn lia) hoặc None.
    follow > 0: thêm `follow` giây máy đẩy vào và trôi theo tay ngay trước cú vụt (không sớm hơn `follow_from`, thường là đầu câu nói)."""
    sp = pan_span(path, min_t)
    if not sp or factor <= 1:
        return None
    t0, t1 = sp
    d = (t1 - t0) / factor
    fc = (f"[0:v]trim=0:{t0:.3f},setpts=PTS-STARTPTS[a];"
          f"[0:v]trim={t0:.3f}:{t1:.3f},setpts=(PTS-STARTPTS)/{factor:.3f},avgblur=sizeX={blur}:sizeY=1[b];"
          f"[0:v]trim=start={t1:.3f},setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0,fps=30[v];"
          f"[0:a]atrim=0:{t0 + d:.3f},asetpts=PTS-STARTPTS[x];[0:a]atrim=start={t1:.3f},asetpts=PTS-STARTPTS[y];[x][y]concat=n=2:v=0:a=1[au]")
    tmp = path + ".whip.mp4"
    sh_enc(["ffmpeg", "-y", "-i", path, "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", tmp])
    os.replace(tmp, path)
    if follow > 0:
        follow_push(path, max(follow_from, t0 - follow), t0, d)
    return t0, t1, d


def follow_push(path, a, b, d, zoom=1.35, fx=0.85, fy=0.7):
    """Máy "đi theo tay" trước cú vụt (như quay thật: máy đẩy vào và trôi theo cánh tay tới vật được chỉ): trong [a, b] phóng dần 1 -> `zoom` (chậm rồi nhanh)
    và lệch về phía phải-dưới (fx, fy: 0..1 vị trí khung trong ảnh), nối liền vào cú vụt [b, b+d] trong lúc đó trả dần về khung gốc. Không đổi độ dài."""
    w, h = (int(v) for v in sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", path]).stdout.strip().split("x")[:2])
    T = "(in/30)"
    z = (f"if(lt({T},{a:.3f}),1,if(lt({T},{b:.3f}),1+{zoom - 1:.3f}*pow(({T}-{a:.3f})/{max(0.05, b - a):.3f},2),"
         f"if(lt({T},{b + d:.3f}),{zoom:.3f}-{zoom - 1:.3f}*({T}-{b:.3f})/{max(0.05, d):.3f},1)))")
    vf = (f"fps=30,scale={w * 2}:{h * 2}:flags=lanczos,zoompan=z='{z}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d=1:s={w}x{h}:fps=30,setsar=1")
    tmp = path + ".follow.mp4"
    sh_enc(["ffmpeg", "-y", "-i", path, "-vf", vf, "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "copy", tmp])
    os.replace(tmp, path)


# ------------------------------------------------------------------ chạy một biến thể
def release_pin(opts, pin):
    """Bỏ ghim tài khoản của video trên LUO-API (video xong / dừng / lỗi) để video khác dùng được tài khoản đó."""
    try:
        Api(opts["api_url"], opts["api_key"]).req(f"/v1/pins/{pin}", method="DELETE")
    except Exception:  # noqa: BLE001 - API tự bỏ ghim sau vài giờ không dùng
        pass


def custom_gen(template):
    """Code gen riêng của thể loại: kịch bản có khối [HAU KY] với dòng "loai: <mã>" và có file app/production/types/<mã>/gen.py
    (hàm run(vdata, template, out_dir, opts, emit, cancel) -> raw.mp4). Không có thì None: chạy như thường. Cùng cách khai báo với post.py (server.custom_post)."""
    m = re.search(r"^\[HAU KY\]:[ \t]*\r?\n(?:(?!\[)[^\n]*\n)*?[ \t]*loai:[ \t]*([\w-]+)", (template or "") + "\n", re.M)
    path = os.path.join(PROD, "types", m.group(1), "gen.py") if m else ""
    if not (path and os.path.exists(path)):
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"gen_{m.group(1).replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_variant(vdata, template, out_dir, opts, emit, cancel):
    """emit(event, **kw): scene_init / scene / log / done. Trả về đường dẫn raw.mp4."""
    os.makedirs(out_dir, exist_ok=True)
    cg = custom_gen(template)
    if cg and not opts.get("_part"):   # thể loại có code gen riêng (vd. nhiều phần: tình huống + ghép 2 lớp); "_part" = đang chạy một phần của chính nó
        emit("log", msg=f"Gen theo code riêng của thể loại: {os.path.relpath(cg.__file__, PROD)}")
        return cg.run(vdata, template, out_dir, opts, emit, cancel)
    import split as SP
    if SP.is_split(template):   # loại dự án "ghép 2 lớp": mỗi nhân vật gen riêng rồi ghép (split.py)
        return SP.run_split(vdata, template, out_dir, opts, emit, cancel)
    n_real = len(vdata.get("LUOT", []))
    risky = same_gender(vdata)   # robot và người học cùng giới: nguy cơ nói chồng cao hơn nhiều
    vdata = dict(vdata, listen=str(opts.get("listen_mode") or "idle"))   # người nghe: "idle" (sống, phản ứng nhẹ, môi khép) hoặc "still" (đứng như ảnh tĩnh, cách cũ)
    if risky and opts.get("voice_split", True) and not (vdata.get("VAI_DAY") or vdata.get("VAI_HOC")):   # tách giọng kiểu "robot + người học" chỉ cho loại gia sư AI; thể loại khác tự khai vai nên giữ nguyên giọng đã mô tả
        vdata = voice_split(vdata)
        emit("log", msg="Robot và người học cùng giới: tách giọng (robot cao, sáng, trẻ; người học trầm, khàn, chậm) để Muse không lẫn giọng")
    elif opts.get("voice_split", True) and (nv := pair_voice_split(vdata)) is not vdata:
        vdata = nv
        emit("log", msg=f"Hai nhân vật cùng giới: tách giọng (giọng THẤP: {MV.crole(vdata, vdata['_LOW'])}; giọng CAO: bên còn lại) để Muse không lẫn giọng")
    template = expand_script(template, n_real)  # nhiều lượt hơn số cảnh: tự nhân bản cảnh cuối
    want0 = analyze_script(template)["series"].get("LUOT")
    if want0 and 0 < n_real < want0:  # ít lượt hơn script: bù lượt trống cho đủ token rồi chỉ chạy n_real cảnh đầu
        pad_who = (MV.chars_of(vdata) or ["DAY"])[0].lower()
        vdata = dict(vdata, LUOT=list(vdata["LUOT"]) + [{"who": pad_who, "text": "", "emo": ""}] * (want0 - n_real))
        opts = dict(opts, only=min(opts.get("only") or n_real, n_real))
    try:
        text = G.fill_tokens(template, variant_values(vdata))
    except SystemExit as e:
        raise RuntimeError(str(e)) from None
    locks, scenes = G.parse_script(text)
    for k in G.LOCKS:
        if k not in locks:
            raise RuntimeError(f"Thiếu khối [{k}] trong script")
    want = analyze_script(template)["series"].get("LUOT")
    n_luot = len(vdata.get("LUOT", []))
    if want and n_luot != want:
        raise RuntimeError(f"{n_luot} lượt thoại nhưng script cần {want}")
    only = opts.get("only")
    if only:
        scenes = [s for s in scenes if s["n"] <= only]
    open(os.path.join(out_dir, "script.txt"), "w", encoding="utf-8").write(text)
    _TL.cancel = cancel
    set_prompt_prefix(opts)
    api = Api(opts["api_url"], opts["api_key"])
    base_session = f"studio-{int(time.time())}-{uuid.uuid4().hex[:6]}"  # duy nhất để chạy song song không đụng phiên
    chat_every = int(opts.get("chat_every", 1))  # mở chat Muse mới sau mỗi N cảnh (0 = cả video dùng chung một chat)
    session = base_session
    started_sessions = []

    def end_session(sid):
        try:
            api.req(f"/v1/sessions/{sid}", method="DELETE")
        except Exception:  # noqa: BLE001
            pass
    refs = [G.data_url(p) for p in opts.get("refs", []) if p and os.path.exists(p)]
    layout = opts.get("layout_ref")   # wireframe bố cục của thể loại (vd. AI tutor ngồi đọc): ảnh #1, chỉ để khoá cỡ/vị trí nhân vật
    if layout and os.path.exists(layout):
        refs.insert(0, G.data_url(layout))
    else:
        layout = None
    luot = vdata.get("LUOT", [])
    att_missing = []
    att_imgs, att_legend, att_auds = attachments(vdata, opts, offset=len(refs), missing=att_missing)
    if att_missing:
        emit("log", msg="CẢNH BÁO: các ảnh/âm thanh tham chiếu sau được gắn vào biến thể nhưng KHÔNG tìm thấy file nên không được gửi: " + "; ".join(att_missing[:6]), level="warn")
    emit("log", msg=f"Tham chiếu: {len(refs) + len(att_imgs)} ảnh ({len(att_imgs)} gắn trong biến thể) sẽ gửi kèm lệnh gen ảnh khung đầu; {len(att_auds)} âm thanh mẫu giọng"
                    + ("" if att_imgs or refs else " - biến thể chưa gắn ảnh tham chiếu nào"))
    emit("scene_init", scenes=[{"n": s["n"], "who": (luot[s["n"] - 1]["who"] if s["n"] - 1 < len(luot) else ""),
                                "text": (luot[s["n"] - 1]["text"] if s["n"] - 1 < len(luot) else s["title"]),
                                "state": "wait"} for s in scenes])
    prev_last, clips, ref_stats = None, [], None
    last_wide = None           # ảnh ngang tổng quan gần nhất: gửi kèm các khung đầu sau để giữ cùng bối cảnh, đạo cụ, vị trí
    # cân màu: "anchor" = mỗi cảnh có khung đầu riêng (gen từ ảnh tham chiếu) là chuẩn màu cho chính nó và các cảnh nối tiếp sau nó;
    # "first" = mọi cảnh kéo về cảnh 1 (cách cũ: ép cảnh khác bối cảnh/ánh sáng về cảnh 1, các cảnh nối tiếp tối và đậm dần); "off" = không cân
    color_mode = str(opts.get("color_mode") or "anchor") if opts.get("normalize", True) else "off"
    color_strength = float(opts.get("color_strength", 1.0))
    ref_scene = None           # cảnh làm chuẩn màu hiện tại (để ghi nhật ký)
    palette = None             # bảng màu chung của cả video (ảnh tổng quan trung tính nếu có, không thì khung đầu cảnh đầu tiên): các khung đầu sau kéo sắc về đây
    s_toks = scene_tokens(template)
    all_toks = set().union(*s_toks.values()) if s_toks else set()
    prev_people = None         # nhân vật có mặt ở cảnh trước (cảnh nối tiếp không nhắc tên ai thì coi như giữ nguyên)
    prev_bg = None             # token nền (NEN_*) của cảnh trước
    acc_of = {}              # cảnh -> tên tài khoản Muse đang gen
    video_acc = {}             # tài khoản đã ghim cho cả video (id, tên)
    pin, pin_prefer = opts.get("pin"), opts.get("pin_prefer")
    mouth_hint_shown = False   # gợi ý nguyên nhân lỗi kiểm tra miệng chỉ hiện một lần mỗi lần chạy
    mouth_off = False          # kiểm tra miệng lỗi một lần thì bỏ qua cho các cảnh còn lại của video này
    for sc in scenes:
        n = sc["n"]
        if cancel.is_set():
            raise Cancelled()

        def note_account(acc_id, name, n=n):   # ghi tài khoản Muse đang gen cảnh này; chỉ ghi nhật ký khi đổi tài khoản
            if not video_acc:
                video_acc.update(id=acc_id, name=name)
                emit("item", account_id=acc_id, account=name)
                if pin_prefer and acc_id != pin_prefer:
                    emit("log", msg=f"Tài khoản cũ của video không dùng được (đang ghim cho video khác hoặc hết hạn mức): chạy tiếp bằng tài khoản {name}", level="warn")
                emit("log", msg=f"Video gen bằng tài khoản {name} (ghim cho mọi cảnh của video)")
            elif acc_id != video_acc["id"]:
                emit("log", msg=f"Cảnh {n}: CẢNH BÁO tài khoản đổi sang {name} (video đang ghim {video_acc['name']})", level="warn")
            if name != acc_of.get(n):
                acc_of[n] = name
                emit("scene", n=n, account=name)
        if chat_every > 0:  # chat mới: Muse không "nhớ" các clip trước (tránh bắt chước lỗi cũ, tránh trả về video ghép); nhân vật vẫn nhất quán nhờ khung đầu + khoá mô tả
            want = f"{base_session}-{(n - 1) // chat_every}"
            if want != session:
                if session != base_session or started_sessions:
                    end_session(session)
                session = want
            if session not in started_sessions:
                started_sessions.append(session)
        has_img = bool(sc["f"].get("Prompt ảnh"))
        wide_p = str(sc["f"].get("Ảnh tổng quan", "")).strip()   # ảnh ngang 16:9 cả bố cục: khung đầu cắt từ nó + gửi kèm bước gen video (cảnh có lia máy)
        cx = crop_x(sc["f"].get("Khung đầu cắt")) if wide_p else None
        has_img = has_img or cx is not None
        img_p, vid_p, neg = G.build_prompts(locks, sc)
        turn = luot[n - 1] if n - 1 < len(luot) else None
        syll = G.spoken_syllables(sc["f"].get("Voice", ""))  # đếm âm tiết trước khi sửa prompt
        fix_note = str((opts.get("scene_notes") or {}).get(str(n), "")).strip()
        spk_key = MV.ck(turn.get("who")) if turn else ""
        chars = MV.chars_of(vdata)
        spoken = bool(syll) or bool(turn and str(turn.get("text", "")).strip())   # cảnh không có lời thoại (hành động, chuyển cảnh): không đòi tiếng, không cắt theo lời, không đo miệng
        swap, vid_b, neg_b = False, "", ""   # swap: người nói quay lưng -> gen thêm clip câm lấy hình, clip có giọng chỉ lấy tiếng (xem silent_prompt)
        if turn and spk_key in chars:
            tt = MV.turn_text(vdata, turn["who"], turn.get("text", ""), turn.get("emo", ""))
            spos = MV.cpos(vdata, spk_key)
            said = re.sub(r"\s+", " ", str(turn.get("text", "")).strip().replace('"', "'"))
            if tt in vid_p:  # lượt thoại xuất hiện nhiều lần (CHAR LOCK + Spoken dialogue): giữ MỘT bản đầy đủ ở đầu, các chỗ khác chỉ còn lời nói
                first = vid_p.index(tt)
                vs = chr(65 + chars.index(spk_key))
                vid_p = vid_p[:first] + f"(the line and its delivery are given at the top, voiced by VOICE {vs})" + vid_p[first + len(tt):]
                vid_p = vid_p.replace(tt, f'VOICE {vs} (the {MV.crole(vdata, spk_key)}, {spos}) says: "{said}"')
            body = scrub_listener_text(drop_listener_voice(vid_p, vdata, turn))
            swap = bool(spoken and opts.get("voice_swap", False) and MV.back_view(vdata, spk_key) and len(chars) > 1)
            if swap:
                vid_b = silent_prompt(unfreeze_listener(body) if vdata.get("listen") == "idle" else body, vdata, turn["who"], said)
                neg_b = silent_negative(neg)
            vid_p = speaker_lock(vdata, turn) + "\n\n" + (unfreeze_listener(body) if vdata.get("listen") == "idle" else body)
            neg = compact_negative(unfreeze_negative(neg) if vdata.get("listen") == "idle" else neg)
        dur = G.auto_duration(syll) if syll else next((d for d in ALLOWED if d >= sc["seconds"]), 10)
        if fix_note:  # người dùng yêu cầu sửa riêng cho cảnh này khi làm lại: đặt đầu prompt video, ưu tiên cao nhất
            vid_p = f"CORRECTION FOR THIS CLIP (highest priority, overrides anything below that conflicts with it): {fix_note}\n\n" + vid_p
            if vid_b:
                vid_b = f"CORRECTION FOR THIS CLIP (highest priority, overrides anything below that conflicts with it): {fix_note}\n\n" + vid_b
            emit("log", msg=f"Cảnh {n}: gen lại kèm yêu cầu sửa: {fix_note[:120]}")
        P = lambda f: os.path.join(out_dir, f)
        img_f, vid_f, cut_f, last_f = P(f"scene{n}_start.png"), P(f"scene{n}_clip.mp4"), P(f"scene{n}_cut.mp4"), P(f"scene{n}_last.png")
        wide_f = P(f"scene{n}_wide.png")
        wide_ref = last_wide if (has_img and not wide_p) else None   # khung đầu mới ở cảnh sau: giữ cùng bối cảnh với ảnh tổng quan đã có
        if wide_p and os.path.exists(wide_f):
            last_wide = wide_f
        if color_mode == "anchor" and has_img:
            ref_stats = None   # khung đầu mới (đổi bối cảnh / góc máy): chuẩn màu mới là chính khung đầu này, không ép về cảnh khác
        if ref_stats is None and color_mode != "off" and os.path.exists(vid_f):  # chạy tiếp: lấy lại chuẩn màu từ clip làm chuẩn đã có
            ref_stats, ref_scene = color_stats(vid_f, [0.04, 0.2, 0.4]), n
        toks = s_toks.get(n, set())
        people = {c for c in chars if f"NGUOI_{c}" in toks or f"TEN_{c}" in toks}
        if not people:
            people = prev_people or set(chars)
        bg = {t for t in toks if t.startswith("NEN_")}
        bg_changed = bool(bg and prev_bg and bg != prev_bg)   # đổi nền (vd. nền xanh dạy từ -> nền thành phố quảng cáo): khung cuối cảnh trước còn nền/đồ vật cũ, Muse sẽ giữ lại
        prev_bg = bg or prev_bg
        same_setup = people == prev_people and not bg_changed
        prev_people = people
        if os.path.exists(cut_f) and os.path.exists(last_f):
            emit("scene", n=n, state="done", pct=100, thumb=os.path.basename(last_f), clip=os.path.basename(cut_f), secs=round(duration(cut_f), 1))
            prev_last = last_f
            clips.append(cut_f)
            continue
        ref_keep = scene_ref_filter(toks, people, all_toks) if toks else None
        sc_imgs, sc_legend, _ = attachments(vdata, opts, keep=ref_keep, offset=len(refs)) if ref_keep else (att_imgs, att_legend, [])
        use_prev = bool(prev_last and has_img and same_setup)   # khung cuối cảnh trước chỉ gửi khi cùng nhân vật; khác người thì nó làm lẫn mặt
        ref_imgs = list(refs) + list(sc_imgs) + ([G.data_url(prev_last)] if use_prev else [])
        if use_prev:
            sc_legend = (sc_legend + "; " if sc_legend else "") + f"reference image #{len(ref_imgs)} is the final frame of the previous clip: match its lighting and colour only"
        if sc_legend and has_img:
            img_p = img_p + "\n\nREFERENCE IMAGE NOTES: " + sc_legend
        if layout and has_img:
            img_p += ("\n\nLAYOUT GUIDE (highest priority, overrides the framing, crop and scale of every character reference): reference image #1 is a rough grey wireframe of the required framing, NOT an appearance reference. "
                      "Place the character so her head (including any headset) fills exactly the dark oval, her neck and shoulders fill the mid-grey shape, "
                      "and her body is no wider than it, with the table at the lower grey band; the pale top third (above the line) must be only plain background with nothing in it. "
                      "Never draw the grey shapes, the line or any of its colours, and never make the character larger or closer than the guide.")
        if wide_ref and os.path.exists(wide_ref):
            ref_imgs = ref_imgs + [G.data_url(wide_ref)]
            img_p += (f"\n\nreference image #{len(ref_imgs)} is a WIDE OVERVIEW of this same set from an earlier shot: keep the same place, the same props (colours, sizes, positions "
                      "and their order from front to back) and the same people and clothing as in it. It is for consistency only: use the framing written in this prompt and show only the people this prompt names.")
        # "Ảnh bố cục: <cảnh m>": khung đầu đã gen của cảnh m (cùng bối cảnh, góc khác) gửi kèm khi vẽ khung đầu mới -> giữ đúng thứ tự vali, vị trí người, máy móc
        # khi đổi góc máy (soi hành lý 05/11: cảnh 8 góc cận vẽ lại từ chữ, vali đổi thứ tự so với cảnh 3). Ảnh tổng quan 16:9 không đủ: Muse vẫn xếp lại đồ.
        lay = re.search(r"\d+", str(sc["f"].get("Ảnh bố cục", "")))
        if lay and has_img:
            lay_f = next((P(f"scene{int(lay.group(0))}_{k}.png") for k in ("start", "last") if os.path.exists(P(f"scene{int(lay.group(0))}_{k}.png"))), None)
            if lay_f:
                ref_imgs = ref_imgs + [G.data_url(lay_f)]
                img_p += (f"\n\nreference image #{len(ref_imgs)} is a FRAME OF THIS SAME SCENE already shot from another camera angle: it shows the true layout of the set, which objects "
                          "lie where (in which order, front to back and left to right), who stands where and what they wear. Keep every object and person at the same place in the room "
                          "as in it, seen from the angle written in this prompt; do not add, remove, swap or rearrange anything. Never show that frame itself.")
                emit("log", msg=f"Cảnh {n}: khung đầu vẽ kèm ảnh bố cục của cảnh {lay.group(0)}")
            else:
                emit("log", msg=f"Cảnh {n}: không có khung đầu của cảnh {lay.group(0)} để làm ảnh bố cục", level="warn")
        spk_auds = [a for g, a in att_auds if g in ((turn or {}).get("who"), "other", "scene")]

        def attempt(label, fn):
            for i in range(1, opts["retries"] + 2):
                try:
                    return fn()
                except (Cancelled, AccountError):
                    raise   # lỗi tài khoản: thử lại trên cùng tài khoản vô ích, để server đổi tài khoản
                except Exception as e:
                    emit("log", msg=f"Cảnh {n} {label}: {e}", level="warn")
                    if _QUOTA_RE.search(str(e)):
                        raise QuotaExceeded(f"Muse báo hết hạn mức tạo video (giới hạn 24 giờ): {str(e)[:160]}") from None
                    if i > opts["retries"]:
                        raise
                    emit("scene", n=n, state=label, pct=0, note=f"thử lại {i}/{opts['retries']}")
                    time.sleep(4)

        pre_v = str(sc["f"].get("Mở đầu video", "")).strip()   # đoạn không lời ghép trước clip của cảnh (gen TRƯỚC ảnh tổng quan: khung cuối của nó là nguồn bối cảnh để mọi khung sau cùng một máy soi / bố cục) (vd. hành lý trôi ra khỏi máy soi rồi mới tới câu hỏi)
        if pre_v:
            pre_img, pre_clip = P(f"scene{n}_pre_start.png"), P(f"scene{n}_pre_clip.mp4")
            pre_ip = str(sc["f"].get("Mở đầu ảnh", "")).strip()
            ctx = [locks.get("SET LOCK", ""), locks.get("STYLE LOCK", "")]
            if pre_ip and not os.path.exists(pre_img):
                p_refs = list(refs) + list(sc_imgs) + ([G.data_url(last_wide)] if last_wide and os.path.exists(last_wide) else [])
                p_prompt = G.with_ctx(pre_ip, ctx) + (f"\n\nreference image #{len(p_refs)} is a wide overview of this same set: keep the same place, props (colours, sizes) and lighting; "
                                                      "use the framing written above." if last_wide and os.path.exists(last_wide) else "")
                emit("scene", n=n, state="image", pct=0, note="mở đầu")
                emit("log", msg=f"Cảnh {n}: gen ảnh đoạn mở đầu không lời")

                def gpi():
                    b = api.generate("image", G.muse_image_prompt(p_prompt, neg, len(p_refs)), p_refs, session, timeout=opts["timeout"], cancel=cancel,
                                     on_status=lambda s, p: emit("scene", n=n, state="image", pct=p or 0), on_account=note_account, pin=pin, pin_prefer=pin_prefer)
                    if G.kind_of(b) == "video":
                        open(pre_img + ".mp4", "wb").write(b)
                        grab_frame(pre_img + ".mp4", pre_img)
                        os.remove(pre_img + ".mp4")
                    else:
                        open(pre_img, "wb").write(b)
                attempt("image", gpi)
            if not os.path.exists(pre_clip):
                p_start = pre_img if os.path.exists(pre_img) else img_f
                p_vrefs = [G.data_url(p_start)] if p_start and os.path.exists(p_start) else []
                p_vid = (G.with_ctx(pre_v, ctx) + "\n\nNO DIALOGUE: nobody speaks in this clip; only quiet natural ambience of the place."
                         + ("\n\nREFERENCE IMAGE NOTES: reference image #1 is the START FRAME (the clip begins exactly on it)." if p_vrefs else ""))
                emit("scene", n=n, state="video", pct=0, note="mở đầu")
                emit("log", msg=f"Cảnh {n}: gen video đoạn mở đầu không lời")

                def gpv():
                    b = api.generate("video", G.muse_video_prompt(p_vid, neg, 5, len(p_vrefs)), p_vrefs, session, duration=5, timeout=opts["timeout"], cancel=cancel,
                                     on_status=lambda s, p: emit("scene", n=n, state="video", pct=p or 0), on_account=note_account, pin=pin, pin_prefer=pin_prefer)
                    open(pre_clip, "wb").write(b)
                attempt("video", gpv)
        if wide_p and not os.path.exists(img_f):
            if not os.path.exists(wide_f):
                emit("scene", n=n, state="image", pct=0, note="ảnh tổng quan")
                w_imgs, w_legend, _ = attachments(vdata, opts, keep=ref_keep, offset=0)
                pre_last = P(f"scene{n}_pre_last.png")
                if pre_v and os.path.exists(pre_clip):   # khung cuối của đoạn mở đầu = bối cảnh chuẩn: cùng máy soi, băng chuyền, vali, vị trí người
                    grab_frame(pre_clip, pre_last, sseof=-0.06)
                    w_imgs = list(w_imgs) + [G.data_url(pre_last)]
                    w_legend = (w_legend + "; " if w_legend else "") + (f"reference image #{len(w_imgs)} is the LAST FRAME of the opening clip of this same set: draw the wide overview as the SAME moment of the SAME place "
                                                                      "(the same scanner, conveyor, suitcases, lighting and people in the same positions), only wider")
                w_prompt = (WIDE_NOTE + "\n\n" + G.with_ctx(wide_p, [locks.get("SET LOCK", ""), locks.get("CHAR LOCK", "")])
                            + (("\n\nREFERENCE IMAGE NOTES: " + w_legend + ". The reference images are authoritative for each person's face, hair, skin tone, age and clothing; "
                                "never blend two people's references into one face.") if w_legend else "")
                            + (f"\n\nAvoid: {neg}" if neg else "") + "\n\nFINAL REMINDER: output exactly ONE STILL IMAGE, landscape 16:9.")
                emit("log", msg=f"Cảnh {n}: gen ảnh ngang tổng quan 16:9 kèm {len(w_imgs)} ảnh tham chiếu")

                def gw():
                    b = api.generate("image", w_prompt, w_imgs, session, timeout=opts["timeout"], on_status=lambda s, p: emit("scene", n=n, state="image", pct=p or 0),
                                     cancel=cancel, on_account=note_account, pin=pin, pin_prefer=pin_prefer, aspect="16:9")
                    if G.kind_of(b) == "video":
                        open(wide_f + ".mp4", "wb").write(b)
                        grab_frame(wide_f + ".mp4", wide_f)
                        os.remove(wide_f + ".mp4")
                    else:
                        open(wide_f, "wb").write(b)
                attempt("image", gw)
            last_wide = wide_f
            if cx is not None:
                crop_f = P(f"scene{n}_crop.png")
                cw = wide_crop(wide_f, crop_f, cx)
                if cw >= 700 or not sc["f"].get("Prompt ảnh"):
                    os.replace(crop_f, img_f)
                    emit("log", msg=f"Cảnh {n}: khung đầu cắt từ ảnh tổng quan (vị trí {cx:.2f}, rộng {cw}px)")
                    emit("scene", n=n, state="image", pct=100, thumb=os.path.basename(img_f))
                else:   # ảnh tổng quan nhỏ: khung cắt mờ -> cho Muse vẽ lại sắc nét theo đúng bố cục khung cắt
                    ref_imgs = ref_imgs + [G.data_url(crop_f)]
                    img_p += (f"\n\nreference image #{len(ref_imgs)} is a rough low-resolution crop of EXACTLY the required framing, cut from the wide overview of this set: "
                              "redraw it sharp at full resolution with the same composition, positions, poses, props and people; it overrides any other framing description.")
                    emit("log", msg=f"Cảnh {n}: ảnh tổng quan nhỏ (khung cắt rộng {cw}px), gen lại khung đầu sắc nét theo khung cắt")
        if has_img and not os.path.exists(img_f):
            emit("scene", n=n, state="image", pct=0)
            emit("log", msg=f"Cảnh {n}: gen ảnh khung đầu kèm {len(ref_imgs)} ảnh tham chiếu" + (f" (trong đó {len(sc_imgs)} ảnh gắn trong biến thể)" if sc_imgs else ""))

            def gi():
                b = api.generate("image", G.muse_image_prompt(img_p, neg, len(ref_imgs)), ref_imgs, session, timeout=opts["timeout"],
                                 on_status=lambda s, p: emit("scene", n=n, state="image", pct=p or 0), cancel=cancel, on_account=note_account,
                                 pin=pin, pin_prefer=pin_prefer)
                if G.kind_of(b) == "video":
                    open(img_f + ".mp4", "wb").write(b)
                    grab_frame(img_f + ".mp4", img_f)
                    os.remove(img_f + ".mp4")
                else:
                    open(img_f, "wb").write(b)
            attempt("image", gi)
            if layout:
                fit_start_frame(api, img_f, session, opts, emit, n, pin, pin_prefer, cancel, note_account)
            emit("scene", n=n, state="image", pct=100, thumb=os.path.basename(img_f))
        if spoken and os.path.exists(vid_f) and not has_audio(vid_f):  # clip câm còn sót từ lần chạy trước: bỏ đi để gen lại
            emit("log", msg=f"Cảnh {n}: clip cũ không có tiếng, gen lại", level="warn")
            os.remove(vid_f)
        swap_todo = P(f"scene{n}_swap.todo")   # clip có giọng đã gen xong nhưng clip câm (hình) chưa ghép: lần chạy sau làm tiếp, không gen lại clip giọng
        a_ready = swap and os.path.exists(vid_f) and os.path.exists(swap_todo)
        if not os.path.exists(vid_f) or a_ready:
            start = img_f if has_img else prev_last
            vrefs = [G.data_url(start)] if start and os.path.exists(start) else []
            vid_legend = ""
            wide_lead = ""
            if wide_p and vrefs and os.path.exists(wide_f):   # cảnh lia máy: Muse thấy trước cả bố cục mà máy sẽ lia qua
                vrefs.append(G.data_url(wide_f))
                wide_lead = ("reference image #2 is a WIDE OVERVIEW (16:9) of the whole set, showing where every person and object stands; the start frame is one part of it. "
                             "Any camera move in this clip travels across exactly this layout and lands on the people and objects where this overview shows them; "
                             "never show the overview as a picture, never cut or fade to it; ")
                emit("log", msg=f"Cảnh {n}: gen video kèm ảnh tổng quan để máy lia đúng bố cục")
            if opts.get("video_char_refs", True):   # gửi kèm ảnh nhân vật có mặt cho cả bước gen video: chỉ có khung đầu thì qua nhiều cảnh nối tiếp mặt trôi dần
                pkeep = lambda key, grp: key.upper().startswith("NGUOI_") and (ref_keep is None or ref_keep(key, grp))
                lead = ("reference image #1 is the START FRAME (the clip begins exactly on it: same framing, people, background, lighting and colour); " if vrefs else "") + wide_lead
                c_imgs, c_legend, _ = attachments(vdata, opts, keep=pkeep, offset=len(vrefs), lead=lead)
                if c_imgs:
                    vrefs += c_imgs
                    vid_legend = ("\n\nREFERENCE IMAGE NOTES: " + c_legend + ". The character reference images are for IDENTITY ONLY: keep each person's face, hair, skin tone, age and clothing "
                                  "identical to their own reference for the whole clip; never show the reference images themselves, never cut, fade or switch to them, and "
                                  + ("keep the lighting and colours of the start frame; the framing changes only through the camera move this clip describes." if wide_lead else
                                     "never change the framing, background or colours of the start frame."))
                    emit("log", msg=f"Cảnh {n}: gen video kèm {len(c_imgs)} ảnh nhân vật để giữ mặt đồng nhất")
            if wide_lead and not vid_legend:
                vid_legend = "\n\nREFERENCE IMAGE NOTES: reference image #1 is the START FRAME (the clip begins exactly on it); " + wide_lead.rstrip("; ") + "."
            emit("scene", n=n, state="video", pct=0, dur=dur)

            speech_note = [""]   # ghi chú sửa lời nói (lặp từ, thừa từ) khi gen lại

            def gv():
                b = api.generate("video", G.muse_video_prompt(vid_p + speech_note[0] + vid_legend, neg, dur, len(vrefs)), vrefs, session, duration=dur, timeout=opts["timeout"],
                                 on_status=lambda s, p: emit("scene", n=n, state="video", pct=p or 0), cancel=cancel, audios=spk_auds or None, on_account=note_account,
                                 pin=pin, pin_prefer=pin_prefer)
                open(vid_f, "wb").write(b)
                got = duration(vid_f)
                if got > 2 * dur + 1:  # Muse đôi khi trả về cả chuỗi clip cũ ghép lại (rất dài): clip mới nằm ở cuối -> chỉ giữ `dur` giây cuối. Dài hơn vừa phải (vd. 10s thay vì 8s) thì giữ nguyên, tránh mất đầu câu
                    emit("log", msg=f"Cảnh {n}: Muse trả về video ghép {got:.0f}s, chỉ lấy {dur}s cuối", level="warn")
                    tmp = vid_f + ".tail.mp4"
                    sh(["ffmpeg", "-y", "-sseof", f"-{dur}", "-i", vid_f, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", tmp])
                    os.replace(tmp, vid_f)
                if spoken and not has_audio(vid_f):  # Muse đôi khi trả về clip câm (không có track tiếng): coi như lỗi để gen lại, nếu không bước ghép sẽ hỏng
                    os.remove(vid_f)
                    raise RuntimeError("Muse trả về clip không có tiếng (mất lời thoại)")
            tries = 0
            tried = []            # (điểm lỗi = mức mấp máy của người nghe, file) của các lần gen có lỗi, để cuối cùng giữ lần TỐT NHẤT
            base_vid_p = vid_p
            while not a_ready:
                attempt("video", gv)
                if spoken and turn and str(turn.get("text", "")).strip() and opts.get("check_speech", True):   # nói lặp từ / thừa từ / thiếu lời: gen lại ngay

                    def regen(note):
                        speech_note[0] = "\n\n" + note
                        os.remove(vid_f)
                        attempt("video", gv)
                    speech_retry(vid_f, turn["text"], regen, emit, n, int(opts.get("speech_retries", SPEECH_RETRIES)))
                    speech_note[0] = ""
                if opts.get("check_camera", True) and not wide_p and not sc["f"].get("Lia nhanh") and not re.search(r"CAMERA MOVE", base_vid_p):   # cảnh máy đứng yên: máy trôi / đẩy vào thì gen lại

                    def regen_cam(note):
                        speech_note[0] = "\n\n" + note
                        os.remove(vid_f)
                        attempt("video", gv)
                    camera_retry(vid_f, regen_cam, emit, n, int(opts.get("camera_retries", 1)))
                    speech_note[0] = ""
                if not (opts.get("check_overlap", True) and not mouth_off and turn and spoken and spk_key in chars) or wide_p or swap:   # swap: hình lấy từ clip câm nên không đo miệng clip giọng   # cảnh lia máy: mặt chạy khỏi vị trí cố định, không đo được
                    break
                spk_side = MV.cbox(vdata, spk_key)
                lis_keys = [c for c in chars if c != spk_key and MV.cbox(vdata, c)]
                if not spk_side or not lis_keys:
                    break   # chỉ một nhân vật trong khung (độc thoại) hoặc chưa khai vị trí: không có "người nghe" để đo
                emit("scene", n=n, state="cut", pct=100, note="kiểm tra giọng")
                try:
                    chk = interruptible(lambda: mouth_check(vid_f, spk_side, [MV.cbox(vdata, c) for c in lis_keys], opts.get("mouth_sens", "normal")), cancel)
                except Cancelled:
                    raise
                except Exception as ex:  # noqa: BLE001
                    emit("log", msg=f"Cảnh {n}: tắt kiểm tra miệng người nghe cho phần còn lại của video này ({mouth_unavailable_msg(ex, not mouth_hint_shown)})", level="warn")
                    mouth_hint_shown = True
                    mouth_off = True
                    break
                if not chk:
                    emit("log", msg=f"Cảnh {n}: không dò được khuôn mặt hai bên nên bỏ qua kiểm tra miệng (không gen lại)", level="warn")
                    break
                if not chk["bad"]:
                    emit("log", msg=f"Cảnh {n}: đo miệng OK (người nói {chk['speaker']}, người nghe {chk['listener']}, há miệng {chk['open']})" + (f" sau {tries} lần gen lại" if tries else ""))
                    tried = []   # lần này đạt: dùng nó, bỏ các lần lỗi trước
                    break
                # lỗi: ghi nhận lần này rồi gen lại NGAY (không chờ làm xong cả video), kèm yêu cầu sửa đúng lỗi vừa gặp
                keep = f"{vid_f}.try{tries}"
                shutil.copyfile(vid_f, keep)
                tried.append((chk["listener"], keep))
                emit("log", msg=f"Cảnh {n}: lần {tries + 1} bị lỗi người nghe mấp máy miệng như người nói (người nói {chk['speaker']}, người nghe {chk['listener']}, há miệng {chk['open']})", level="warn")
                if tries < int(opts.get("overlap_retries", 0)):
                    lkey = lis_keys[chk.get("idx", 0)]
                    lpos = MV.cpos(vdata, lkey)
                    legacy = {spk_key, lkey} == {"DAY", "HOC"}   # robot/gia sư + người học: các bước gen lại riêng cho hai vai này
                    lis_is_learner = spk_key == "DAY"
                    steps = [
                        f"in the previous attempt the {lpos} character moved their mouth along with the speaker. This time the {lpos} character's mouth stays shut and perfectly still for the whole clip (lips pressed together); only the speaker's mouth ever moves.",
                        (f"the previous attempts still showed the {lpos} character mouthing along. Now the {lpos} character keeps their head bowed low over their hands and the work, face half hidden, eyes on their hands, lips pressed together, and never lifts their head."
                         if legacy and lis_is_learner else
                         f"the previous attempts still showed the {lpos} character mouthing along. Now the {lpos} character is a completely still, calm avatar: mouth a thin closed line, eyes on the camera, no lip movement at all, only slow blinking."
                         if legacy else
                         f"the previous attempts still showed the {lpos} character mouthing along. Now the {lpos} character keeps their lips pressed together and their face calm and still, listening, and only blinks."),
                        (f"again the {lpos} character mouthed along. Now the {lpos} character turns their face away to the side, looking down at the work so that the mouth is not visible to the camera, and keeps it closed."
                         if legacy and lis_is_learner else
                         f"again the {lpos} character mouthed along. Now the {lpos} character looks calmly aside with a perfectly closed, motionless mouth and does not speak or smile."),
                        (f"the {lpos} character stays almost entirely turned away from the camera, working with the head down and the face in shadow, mouth completely closed and still for the entire clip."
                         if legacy and lis_is_learner else
                         f"the {lpos} character is shown as a frozen, silent video-call avatar: lips sealed, eyes softly lowered, no mouth movement whatsoever for the entire clip."
                         if legacy else
                         f"the {lpos} character stays almost completely still, like a held photograph: mouth closed, eyes calmly on the speaker, no change of expression for the entire clip."),
                        (f"final attempt: the {lpos} character's lower face is not the focus at all: head lowered, chin tucked, attention fully on the work, lips sealed, absolutely no speaking or mouthing."
                         if legacy and lis_is_learner else
                         f"final attempt: the {lpos} character is a still image: eyes closed in a calm resting expression, lips sealed, absolutely no speaking or mouthing."
                         if legacy else
                         f"final attempt: the {lpos} character's mouth is a thin closed line that does not move at all; they hold a neutral resting face for the whole clip, absolutely no speaking or mouthing."),
                    ]
                    note = steps[min(tries + (1 if same_gender(vdata) else 0), len(steps) - 1)]   # cùng giới: bỏ qua mức nhẹ nhất
                    tries += 1
                    vid_p = base_vid_p + f"\n\nIMPORTANT RETRY NOTE (attempt {tries + 1}): {note}"
                    os.remove(vid_f)
                    emit("scene", n=n, state="video", pct=0, note=f"gen lại {tries}")
                    emit("log", msg=f"Cảnh {n}: gen lại lần {tries} kèm yêu cầu sửa lỗi mấp máy")
                    continue
                # hết số lần gen lại mà vẫn lỗi: giữ lần ÍT LỖI nhất
                best = min(tried)
                shutil.copyfile(best[1], vid_f)
                emit("log", msg=f"Cảnh {n}: vẫn lỗi sau {tries} lần gen lại, giữ lần ít mấp máy nhất (người nghe {best[0]}). Bấm gen lại cảnh này kèm yêu cầu sửa nếu muốn thử tiếp", level="warn")
                emit("scene", n=n, state="video", pct=100, note="nghi nói chồng")
                break
            for _, f_try in tried:
                try:
                    os.remove(f_try)
                except OSError:
                    pass
            vid_p = base_vid_p
            if swap:   # hình lấy từ clip câm (gen từ cùng khung đầu), tiếng lấy từ clip giọng vừa gen
                open(swap_todo, "w").close()
                sil_f = P(f"scene{n}_silent.mp4")
                if not os.path.exists(sil_f):
                    emit("scene", n=n, state="video", pct=0, note="clip hình câm")
                    emit("log", msg=f"Cảnh {n}: người nói quay lưng: gen thêm clip câm lấy hình (người kia không thể nhép miệng / làm động tác thay), ghép tiếng từ clip giọng")

                    def gs():
                        b = api.generate("video", G.muse_video_prompt(vid_b + vid_legend, neg_b, dur, len(vrefs)), vrefs, session, duration=dur, timeout=opts["timeout"],
                                         on_status=lambda s, p: emit("scene", n=n, state="video", pct=p or 0), cancel=cancel, on_account=note_account,
                                         pin=pin, pin_prefer=pin_prefer)
                        open(sil_f, "wb").write(b)
                        if duration(sil_f) > 2 * dur + 1:
                            tmp = sil_f + ".tail.mp4"
                            sh(["ffmpeg", "-y", "-sseof", f"-{dur}", "-i", sil_f, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", tmp])
                            os.replace(tmp, sil_f)
                    attempt("video", gs)
                mix = vid_f + ".mix.mp4"
                sh(["ffmpeg", "-y", "-i", sil_f, "-i", vid_f, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", mix])
                voice_f = P(f"scene{n}_voice.mp4")
                shutil.copyfile(vid_f, voice_f)
                os.replace(mix, vid_f)
                os.remove(swap_todo)
        emit("scene", n=n, state="cut", pct=100)
        vf_fix, fix_note = "", ""
        if color_mode != "off":
            c_start = color_stats(vid_f, [0.04, 0.2, 0.4])
            c_end = color_stats(vid_f, [-0.6, -0.35, -0.1])
            if ref_stats is None:
                if palette is None:
                    palette = color_stats(last_wide, [0.0]) if last_wide and os.path.exists(last_wide) else c_start
                ref_stats, ref_scene = pull_palette(c_start, palette), n  # chuẩn màu = khung đầu của clip này, sắc kéo về bảng màu chung của video
            vf_fix, fix_note = color_match(ref_stats, c_start, c_end, duration(vid_f), color_strength)
            if vf_fix:
                emit("log", msg=f"Cảnh {n}: cân màu về khung đầu cảnh {ref_scene} ({fix_note})")
        span, margin = None, float(opts.get("cut_margin", 0.3))
        if opts.get("cut", True) and opts.get("precise_cut", True) and turn and str(turn.get("text", "")).strip():
            try:
                span = interruptible(lambda: voice_span(vid_f, turn["text"]), cancel)
            except Cancelled:
                raise
            except Exception as ex:  # noqa: BLE001
                emit("log", msg=f"Cảnh {n}: không xác định được mốc lời nói, cắt theo cách thường ({ex})", level="warn")
            if span:
                emit("log", msg=f"Cảnh {n}: lời nói từ {span[0]:.2f}s đến {span[1]:.2f}s trong clip {duration(vid_f):.1f}s; cắt sát, chừa ~{margin:.2f}s")
            else:
                emit("log", msg=f"Cảnh {n}: không nhận ra đủ lời để cắt sát, cắt theo cách thường", level="warn")
        lo, hi = (0.18 if span else 0.15), (max(0.3, margin + 0.05) if span else 0.8)
        keep = re.search(r"\d+(?:[.,]\d+)?", str(sc["f"].get("Giữ sau lời", "")))   # kịch bản: giữ thêm N giây sau từ cuối (vd. camera lia sang người kia sau câu nói)
        if keep:
            tail = min(4.0, float(keep.group(0).replace(",", ".")))
            lo, hi = max(lo, tail), max(hi, tail + 0.4)
            emit("log", msg=f"Cảnh {n}: giữ ~{tail:.1f}s sau lời nói (trường \"Giữ sau lời\")")
        info = smart_cut(vid_f, cut_f, last_f, syll=syll, speedfix=opts.get("speedfix", True), vf_extra=vf_fix, max_speed=float(opts.get("speed_max", 1.25)),
                         span=span, lo=lo, hi=hi, head_margin=margin * 0.7) if opts.get("cut", True) and spoken else None
        if info is not None and span and opts.get("check_speech", True):   # cắt sát lời có thể xén mất chữ đầu/cuối: kiểm lại bản đã cắt
            try:
                lost = [v for v, _ in (speech_issues(turn["text"], cut_f) or []) if v.startswith(("thiếu", "không nghe"))]
            except Exception:  # noqa: BLE001 - không có Whisper: bỏ qua
                lost = []
            if lost:
                emit("log", msg=f"Cảnh {n}: bản cắt sát lời bị mất chữ ({'; '.join(lost)}), cắt lại rộng hơn", level="warn")
                info = smart_cut(vid_f, cut_f, last_f, syll=syll, speedfix=opts.get("speedfix", True), vf_extra=vf_fix, max_speed=float(opts.get("speed_max", 1.25)),
                                 span=None, lo=max(lo, 0.15), hi=max(hi, 0.8), head_margin=margin * 0.7)
        if info is None:
            if vf_fix:
                sh_enc(["ffmpeg", "-y", "-i", vid_f, "-vf", vf_fix, "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "copy", cut_f])
            else:
                shutil.copy(vid_f, cut_f)
            grab_frame(cut_f, last_f, sseof=-0.06)
        try:
            if info:
                hc = head_check(vid_f, cut_f, info["speed"])
                emit("log", msg=f"Cảnh {n}: gốc {info['total']:.1f}s → sau cắt {info['cut']:.1f}s, hết lời lúc {info['speech_end']:.1f}s" + (f", tăng tốc giọng x{info['speed']}" if info["speed"] > 1 else "") + (f", rút {info['pauses']}s khoảng ngắt" if info.get("pauses") else ""))
                if hc and abs(hc[0]) > 6:
                    emit("log", msg=f"Cảnh {n}: CẢNH BÁO đầu câu có thể bị mất ({hc[1]}). Giữ file gốc scene{n}_clip.mp4 để kiểm tra", level="warn")
        except Exception:  # noqa: BLE001 - chỉ là chẩn đoán
            pass
        fast = re.search(r"\d+(?:[.,]\d+)?", str(sc["f"].get("Lia nhanh", "")))   # kịch bản: tua nhanh cú lia của Muse (thường lia chậm, không có lực) N lần + nhoè ngang
        if fast:
            try:
                vs_ = voice_span(cut_f, turn["text"]) if spoken and turn and str(turn.get("text", "")).strip() else None   # chỉ tua sau từ cuối (Whisper), không làm mất lời
                fol = re.search(r"\d+(?:[.,]\d+)?", str(sc["f"].get("Lia theo tay", "")))   # máy đẩy vào + trôi theo tay N giây trước cú vụt (Muse thường để máy đứng yên khi nhân vật chỉ tay)
                w = whip_speedup(cut_f, float(fast.group(0).replace(",", ".")), min_t=vs_[1] + 0.05 if vs_ else (speech_end_of(cut_f) if spoken else 0.0),
                                 follow=float(fol.group(0).replace(",", ".")) if fol else 0.0, follow_from=vs_[0] if vs_ else 0.0)
                emit("log", msg=(f"Cảnh {n}: cú lia {w[0]:.2f}–{w[1]:.2f}s tua nhanh còn {w[2]:.2f}s (trường \"Lia nhanh\")" if w else
                                 f"Cảnh {n}: không dò thấy cú lia sau lời nói, giữ nguyên clip (trường \"Lia nhanh\")"), **({} if w else {"level": "warn"}))
            except Exception as ex:  # noqa: BLE001
                emit("log", msg=f"Cảnh {n}: không tua nhanh được cú lia ({ex})", level="warn")
        if pre_v:
            try:
                ln = re.search(r"\d+(?:[.,]\d+)?", str(sc["f"].get("Mở đầu dài", "")))
                vf_pre = ""
                if color_mode != "off":   # đoạn mở đầu do Muse gen riêng: kéo màu về đầu clip chính để chỗ ghép không nhảy màu
                    c_main, c_pre = color_stats(cut_f, [0.05, 0.3]), color_stats(pre_clip, [0.05, 0.5])
                    vf_pre, _ = color_match(c_main, c_pre, c_pre, 1.0, 0.9) if c_main and c_pre else ("", "")
                secs, k = prepend_preroll(pre_clip, cut_f, float(ln.group(0).replace(",", ".")) if ln else 1.5, vf_pre)
                emit("log", msg=f"Cảnh {n}: ghép đoạn mở đầu {secs:.1f}s (tua x{k:.1f}) trước câu nói")
            except Exception as ex:  # noqa: BLE001
                emit("log", msg=f"Cảnh {n}: không ghép được đoạn mở đầu ({ex})", level="warn")
        prev_last = last_f
        clips.append(cut_f)
        emit("scene", n=n, state="done", pct=100, thumb=os.path.basename(last_f), clip=os.path.basename(cut_f),
             secs=round(duration(cut_f), 1), raw=round(info["total"], 1) if info else None, note=(f"x{info['speed']}" if info and info["speed"] > 1 else ""))
        if info and info["speed"] > 1:
            emit("log", msg=f"Cảnh {n}: lời nói chậm, tăng tốc x{info['speed']}")
    end_session(session)
    return concat_clips(clips, out_dir, emit, [scene_fx(sc["f"]) for sc in scenes])


_FLASH = {"trắng": "FFFFFF", "trang": "FFFFFF", "white": "FFFFFF", "vàng": "FFF1C9", "vang": "FFF1C9", "warm": "FFF1C9", "đen": "000000", "den": "000000", "black": "000000"}


def scene_fx(f):
    """Hiệu ứng khi ghép của một cảnh, từ trường "Chuyển cảnh" và "Lớp phủ" của kịch bản:
    - "Chuyển cảnh: chớp trắng [0.4]" / "chớp vàng" / "chớp #RRGGBB": cuối cảnh trước mờ dần sang màu đó rồi cảnh này hiện ra từ màu đó (tổng N giây, mặc định 0,4).
      Không chồng hai clip lên nhau nên độ dài video không đổi (mốc cảnh của Hậu kỳ vẫn đúng). "cắt thẳng" hoặc để trống = cắt thẳng.
    - "Lớp phủ: camera [đường-dẫn.png]": giao diện camera điện thoại + hình bầu dục bám theo khuôn mặt (camera_overlay.py)."""
    out = {}
    tr = str(f.get("Chuyển cảnh", "")).strip().lower()
    m = re.search(r"#?([0-9a-f]{6})\b", tr)
    color = m.group(1).upper() if m else next((c for k, c in _FLASH.items() if k in tr), None)
    if color and not re.search(r"cắt thẳng|cat thang", tr):
        d = re.search(r"(?<![0-9a-f#])(\d+(?:[.,]\d+)?)\s*(?:s|giây|giay)?\s*$", tr[m.end():] if m else tr)
        out["flash"] = (color, min(1.2, max(0.1, float(d.group(1).replace(",", ".")))) if d else 0.4)
    ov = str(f.get("Lớp phủ", "")).strip()
    if ov.lower().startswith("camera"):
        out["overlay"] = "camera"
        out["ui"] = ov[6:].strip().strip('"') or None
    return out


def concat_clips(clips, out_dir, emit, fx=None):
    """Ghép các clip cảnh (đã cắt) thành raw.mp4. fx: danh sách scene_fx() song song với clips (chớp sáng chuyển cảnh, lớp phủ camera)."""
    raw = os.path.join(out_dir, "raw.mp4")
    fx = list(fx or []) + [{}] * (len(clips) - len(fx or []))
    clips = list(clips)
    for i, c in enumerate(clips):
        if fx[i].get("overlay") == "camera":
            cam = os.path.splitext(c)[0] + "_cam.mp4"
            try:
                if not (os.path.exists(cam) and os.path.getmtime(cam) >= os.path.getmtime(c)):
                    import camera_overlay as CO
                    emit("log", msg=f"Cảnh {i + 1}: ghép giao diện camera + vòng bám mặt")
                    with _MP_LOCK:
                        found = CO.render(c, cam, fx[i].get("ui"))
                    if found < 0.5:
                        emit("log", msg=f"Cảnh {i + 1}: chỉ dò được khuôn mặt ở {found:.0%} số khung hình, vòng bám mặt có thể bị thiếu", level="warn")
                clips[i] = cam
            except Exception as ex:  # noqa: BLE001 - lớp phủ lỗi thì ghép clip gốc, không làm hỏng cả video
                emit("log", msg=f"Cảnh {i + 1}: không ghép được lớp phủ camera ({ex}); dùng clip gốc", level="warn")
    ins, fl = [], ""
    for i, c in enumerate(clips):
        ins += ["-i", c]
        fade = ""
        if fx[i].get("flash"):   # chớp sáng VÀO cảnh này: hiện ra từ màu chớp
            col, d = fx[i]["flash"]
            fade += f",fade=t=in:st=0:d={d / 2:.3f}:color=0x{col}"
        if i + 1 < len(clips) and fx[i + 1].get("flash"):   # cảnh sau có chớp sáng: cuối cảnh này mờ dần sang màu chớp
            col, d = fx[i + 1]["flash"]
            fade += f",fade=t=out:st={max(0.0, duration(c) - d / 2):.3f}:d={d / 2:.3f}:color=0x{col}"
        fl += f"[{i}:v]scale=720:1280:flags=accurate_rnd+full_chroma_int:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1{fade}[v{i}];"
        if has_audio(c):
            fl += f"[{i}:a]aresample=44100[a{i}];"
        else:  # không có track tiếng thì chèn im lặng đúng độ dài, để concat không báo "matches no streams"
            emit("log", msg=f"Cảnh {i + 1}: clip không có tiếng, chèn im lặng khi ghép", level="warn")
            fl += f"aevalsrc=0:c=stereo:s=44100:d={duration(c):.3f}[a{i}];"
    fl += "".join(f"[v{i}][a{i}]" for i in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=1[v][a]"
    emit("log", msg="Đang ghép clip…")
    sh_enc(["ffmpeg", "-y"] + ins + ["-filter_complex", fl, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", raw])
    return raw


# ------------------------------------------------------------------ phụ đề từ lời thoại
def hook_marks(turns):
    """Tự đánh dấu phần mở đầu của video gọi điện: câu ĐẦU TIÊN của người học = nói sai ("wrong"), câu kế tiếp của AI = sửa đúng ("right")."""
    marks = {}
    h = next((i for i, t in enumerate(turns) if t.get("who") == "hoc"), None)
    if h is not None:
        marks[h] = "wrong"
        d = next((i for i in range(h + 1, len(turns)) if turns[i].get("who") == "day"), None)
        if d is not None:
            marks[d] = "right"
    return marks


def _sub_parts(text):
    """Chia một lượt thành các dòng phụ đề theo câu; câu quá ngắn (< 12 ký tự) gộp vào câu sau."""
    text = re.sub(r"\s+", " ", str(text or "").strip())
    merged = []
    for p in (p.strip() for p in re.findall(r"[^.!?…]+[.!?…]*", text) if p.strip()):
        if merged and len(merged[-1]) < 12:
            merged[-1] += " " + p
        else:
            merged.append(p)
    return merged


def subs_from_script(text):
    """Phụ đề cho loại dự án không dùng LUOT (vd. lồng tiếng ngoài khung): lời trong ngoặc kép ở trường Voice của từng cảnh của script đã điền token (script.txt).
    "turn" = thứ tự cảnh, khớp mốc cảnh của Hậu kỳ."""
    try:
        _, scenes = G.parse_script(text)
    except (IndexError, AttributeError):
        return []
    units = []
    for ti, sc in enumerate(scenes):
        for p in _sub_parts(" ".join(re.findall(r'"([^"]+)"', sc["f"].get("Voice", "")))):
            units.append({"t": p, "c": "white", "turn": ti})
    return units


def subs_from_variant(v, auto_hook=True):
    units = []
    turns = v.get("LUOT", [])
    explicit = any(t.get("fx") for t in turns)   # chỉnh tay ở bất kỳ lượt nào (kể cả "Không") thì tắt tự động
    marks = {} if explicit or not auto_hook else hook_marks(turns)
    for ti, t in enumerate(turns):
        merged = _sub_parts(t.get("text", ""))
        for i, p in enumerate(merged):
            u = {"t": p, "c": t.get("c") or "white", "turn": ti}   # "turn": cảnh chứa phụ đề này (căn phụ đề theo từng cảnh)
            if i == 0 and t.get("icon"):
                u["icon"] = t["icon"]
            fx = t.get("fx") if explicit else marks.get(ti)
            if i == 0 and fx in ("wrong", "right"):
                u["fx"] = fx
            units.append(u)
    return units


def variant_values(v):
    """Giá trị token của một biến thể: trường CHỮ HOA dạng chuỗi; danh sách chuỗi -> KEY_1..KEY_n; LUOT -> câu lệnh lượt nói."""
    import make_variants as MV
    vals = {k: x for k, x in v.items() if isinstance(x, str) and k.isupper()}
    for k, x in v.items():
        if k.isupper() and isinstance(x, list) and k != "LUOT":
            for i, item in enumerate(x, 1):
                vals[f"{k}_{i}"] = str(item)
    for i, item in enumerate(v.get("LUOT", []), 1):
        vals[f"LUOT_{i}"] = MV.turn_text(v, item["who"], item["text"], item.get("emo", ""), item.get("emo2", ""))
    return vals


MAX_TURNS = 40
_HDR = re.compile(r"^CẢNH (\d+) \((\d+):(\d{2})–(\d+):(\d{2})\)", re.M)


def expand_script(text, n_turns):
    """Script linh hoạt theo số lượt: nếu lời thoại nhiều hơn số cảnh, nhân bản CẢNH cuối (đổi số cảnh, mốc thời gian, Lượt k, token LUOT_k)."""
    hs = list(_HDR.finditer(text))
    if not hs:
        return text
    last = hs[-1]
    k0 = int(last.group(1))
    if n_turns <= k0 or n_turns > MAX_TURNS:
        return text
    blk = text[last.start():].rstrip("\n")
    if "{{LUOT_%d}}" % k0 not in blk:
        return text
    a = int(last.group(2)) * 60 + int(last.group(3))
    b = int(last.group(4)) * 60 + int(last.group(5))
    ln, out = max(1, b - a), text.rstrip("\n")
    for k in range(k0 + 1, n_turns + 1):
        s0 = b + (k - k0 - 1) * ln
        t = lambda x: f"{x // 60}:{x % 60:02d}"
        nb = blk.replace(f"CẢNH {k0} ({last.group(2)}:{last.group(3)}–{last.group(4)}:{last.group(5)})", f"CẢNH {k} ({t(s0)}–{t(s0 + ln)})", 1)
        nb = nb.replace("Lượt %d" % k0, "Lượt %d" % k).replace("{{LUOT_%d}}" % k0, "{{LUOT_%d}}" % k)
        out += "\n\n" + nb
    return out + "\n"


def analyze_script(text):
    """Đọc script node: số cảnh, các token. Token dạng KEY_1..KEY_n liên tiếp = một 'chuỗi' (series)."""
    tokens = sorted(set(re.findall(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}", text)))
    groups = {}
    for t in tokens:
        m = re.match(r"^([A-Z][A-Z0-9_]*?)_(\d+)$", t)
        if m:
            groups.setdefault(m.group(1), []).append(int(m.group(2)))
    series, in_series = {}, set()
    for pre, ns in groups.items():
        ns = sorted(ns)
        if ns == list(range(1, len(ns) + 1)) and (len(ns) >= 2 or pre in ("LUOT", "THOAI")):
            series[pre] = len(ns)
            in_series.update(f"{pre}_{n}" for n in ns)
    if re.search(r"^\[GHEP HAI LOP\]:\s*$", text, flags=re.M):   # ghép 2 lớp: không có khối CẢNH, mỗi lượt thoại là một cảnh (số lượt tuỳ ý)
        return {"scenes": 0, "split": True, "plain": [t for t in tokens if t not in in_series], "series": {**series, "LUOT": 0}}
    return {"scenes": len(re.findall(r"^CẢNH \d+ \(", text, flags=re.M)), "plain": [t for t in tokens if t not in in_series], "series": series}


KNOWN_FIELDS = {
    "NGUOI_DAY": ("Ngoại hình", "day", "long", "a humanoid AI robot tutor with a smooth bald head…"), "TEN_DAY": ("Gọi ngắn", "day", "short", "the AI robot tutor"),
    "GIONG_DAY": ("Giọng", "day", "long", "a warm, lively female voice, American accent"),
    "NGUOI_HOC": ("Ngoại hình", "hoc", "long", "a young woman with long wavy brown hair, white t-shirt…"), "TEN_HOC": ("Gọi ngắn", "hoc", "short", "the young woman holding a spoon"),
    "GIONG_HOC": ("Giọng", "hoc", "long", "a natural, young, expressive voice"),
    "NEN_TRAI": ("Nền bên trái", "scene", "long", "a flat chroma-key green background"), "NEN_PHAI": ("Nền bên phải", "scene", "long", "an empty sunny garden, soft bokeh"),
    "VIEC": ("Đang làm gì", "scene", "long", "stirring a pot of pasta"), "DAO_CU": ("Đạo cụ", "scene", "long", "holding a wooden spoon"),
    "DAO_GIU": ("Cách cầm", "scene", "long", "she holds the spoon in her right hand"), "DAO_NGHI": ("Tay khi nghỉ", "scene", "long", "one hand resting on the pot handle"),
    "NEN_DAY": ("Nền", "day", "long", "a plain pure black background"), "NEN_HOC": ("Nền", "hoc", "long", "the inside of a truck cab at golden hour"),   # ghép 2 lớp: nền riêng của từng nhân vật
}


def suggest_fields(plain, has_luot, existing=None):
    """Gợi ý bảng trường từ các token. `existing` (danh sách trường đã có) được giữ nguyên nhãn/nhóm/loại theo key."""
    old = {f["key"]: f for f in (existing or [])}
    keys = list(plain)
    if has_luot and not any(re.fullmatch(r"TEN_[A-Z0-9]+", k) for k in keys):   # kịch bản đã khai nhân vật riêng (TEN_<khoá>) thì không thêm day/hoc
        for k in ("TEN_DAY", "TEN_HOC"):
            if k not in keys:
                keys.append(k)
    out = []
    for k in keys:
        if k in old:
            out.append(old[k]); continue
        pre = {"NHIN": "Hướng nhìn khi nói", "NGHE": "Tư thế khi nghe"}.get(k.split("_", 1)[0])   # trường nhân vật có nhãn chung, kèm tên khoá
        lab, grp, kind, ph = KNOWN_FIELDS.get(k, ((f"{pre} ({k.split('_', 1)[1]})" if pre and "_" in k else k.replace("_", " ").capitalize()),
                                                   "day" if k.endswith("_DAY") else "hoc" if k.endswith("_HOC") else "other", "long", ""))
        out.append({"key": k, "label": lab, "group": grp, "kind": kind, "ph": ph, "default": ""})
    order = {"day": 0, "hoc": 1, "scene": 2}
    prio = list(KNOWN_FIELDS)
    out.sort(key=lambda f: (order.get(f["group"], 3), prio.index(f["key"]) if f["key"] in prio else 100 + keys.index(f["key"])))
    return out
