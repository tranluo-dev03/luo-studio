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
import numpy as np

ALLOWED = [5, 6, 8, 10]
MAX_SPEED = 1.35
# Giải mã YUV -> RGB bằng swscale mặc định bị lệch làm tròn (mất ~1 mức sáng mỗi lần lấy khung). Chuỗi cảnh nối khung cuối qua nhiều lần
# nên video tối dần. accurate_rnd + full_chroma_int làm hết độ lệch (đã đo: 0.00 mỗi vòng thay vì -1.05).
DEC_VF = "scale=flags=accurate_rnd+full_chroma_int:out_range=pc,format=rgb24"


def grab_frame(src, out_png, sseof=None, ss=None):
    """Lấy một khung hình thành PNG không làm tối/lệch màu."""
    cmd = ["ffmpeg", "-y"]
    if sseof is not None:
        cmd += ["-sseof", str(sseof)]
    if ss is not None:
        cmd += ["-ss", str(ss)]
    sh(cmd + ["-i", src, "-vf", DEC_VF, "-frames:v", "1", "-update", "1", out_png])


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


def color_match(ref, start, end, dur):
    """Bộ lọc ffmpeg kéo màu clip về `ref` (cảnh đầu), chỉnh dần theo thời gian từ đầu tới cuối clip vì Muse hay tối/nhạt dần trong clip.
    Trả về (chuỗi lọc, mô tả) hoặc ("", "") nếu đã đủ gần."""
    if not ref or not start or not end:
        return "", ""
    g0, g1 = _grade(ref, start), _grade(ref, end)
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


class QuotaExceeded(Exception):
    """Muse báo hết hạn mức tạo video (giới hạn 24 giờ): thử lại hay gen lại đều vô ích và còn tốn thêm."""


_QUOTA_RE = re.compile(r"24-hour limit|budget is (?:still )?exhausted|video budget|quota (?:is )?exhausted|hết hạn mức", re.I)


_TL = threading.local()


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
    def generate(self, kind, prompt, refs, session, duration=None, timeout=900, on_status=None, cancel=None, audios=None):
        body = {"prompt": prompt, "model": "muse-video" if kind == "video" else "muse-image", "aspect_ratio": "9:16",
                "raw_prompt": True, "timeout": min(int(timeout), 600), "session": session}  # API nhận tối đa 600s; thời gian chờ phía app (deadline) vẫn theo `timeout`
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
            for _ in range(6):
                if cancel and cancel.is_set():
                    raise Cancelled()
                time.sleep(0.5)
            st = self.req(f"{path}/{tid}")
            s, pr = st.get("status"), st.get("progress")
            if on_status and (s, pr) != last:
                last = (s, pr)
                on_status(s, pr)
            if s == "completed":
                url = st.get("url") or (st.get("video") or {}).get("url") or (st.get("result") or {}).get("url") or ((st.get("data") or [{}])[0]).get("url")
                if not url:
                    raise RuntimeError("API không trả về file")
                return self.download(url)
            if s in ("failed", "error"):
                raise RuntimeError(str(st.get("error") or "API báo lỗi"))
            if time.time() > deadline:
                raise RuntimeError("Hết thời gian chờ")


# ------------------------------------------------------------------ tham chiếu đính kèm theo token
def attachments(vdata, opts):
    """(ảnh data-url, chú thích ảnh, [(nhóm, audio data-url)]) từ vdata["refs"] = {TOKEN: [{type,file,name}]}."""
    base = opts.get("assets_dir") or ""
    labels, groups = opts.get("field_labels", {}), opts.get("field_groups", {})
    imgs, notes, auds = [], [], []
    for key, items in (vdata.get("refs") or {}).items():
        for it in items or []:
            p = os.path.join(base, os.path.basename(it.get("file", "")))
            if not os.path.isfile(p):
                continue
            if it.get("type") == "audio":
                auds.append((groups.get(key, "other"), G.data_url(p)))
            else:
                imgs.append(G.data_url(p))
                notes.append(f"the attached reference image #{len(imgs)} shows: {labels.get(key, key)}")
    legend = "; ".join(notes)
    return imgs, ("(the first images are general references) " + legend if legend else ""), auds


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


def voice_contrast(v, day):
    """Hai giọng cùng giới (vd. robot nữ + người học nữ) rất dễ bị Muse lẫn: gắn cho mỗi bên một đặc trưng cao độ trái ngược, giữ nhất quán ở mọi clip,
    để giọng nghe được chỉ khớp với MỘT khuôn mặt. Khác giới thì giọng đã đủ khác, không cần thêm."""
    gd, gh = _gender(v.get("GIONG_DAY", "")), _gender(v.get("GIONG_HOC", ""))
    if not gd or gd != gh:
        return ""
    if day:   # người nói là bên 'dạy' (robot)
        return "Its voice is clearly the HIGHER-pitched, brighter, lighter and quicker of the two voices in this video, easy to tell apart from the other character's voice."
    return "Its voice is clearly the LOWER-pitched, deeper, warmer and slower of the two voices in this video, easy to tell apart from the other character's voice."


def speaker_lock(v, turn):
    """Khối đầu prompt video, viết theo mẫu video call (master-ugc-ai-call): MỘT câu khẳng định ai nói gì + người kia im và đang làm việc riêng.
    Không liệt kê hàng loạt điều cấm (khiến Muse hiểu người nghe cũng 'có phần' trong lời thoại)."""
    import make_variants as MV
    pd, ph = v.get("POS_DAY", "LEFT"), v.get("POS_HOC", "RIGHT")
    day = turn.get("who") == "day"
    spk, lis = (v.get("TEN_DAY"), v.get("TEN_HOC")) if day else (v.get("TEN_HOC"), v.get("TEN_DAY"))
    spos, lpos = (pd, ph) if day else (ph, pd)
    task = v.get("VIEC", "").strip() if day else ""
    strong = same_gender(v) and bool(task)   # cùng giới: giấu miệng người nghe ngay từ đầu
    base = (f"keeps quietly {task} at the same slow, steady pace the whole time, head bowed low over the work, face half hidden by the hat or hair and turned down and away, eyes on the work, lips closed and still" if strong else
            f"keeps quietly {task} at the same slow, steady pace the whole time, head lowered over the work, eyes on the work, face partly turned away from the phone and the camera" if task
            else "stays in the calm base pose, still, eyes on the camera, mouth a flat closed line")
    contrast = voice_contrast(v, day)
    vs, vl = ("A", "B") if day else ("B", "A")
    role_s, role_l = ("tutor", "learner") if day else ("learner", "tutor")
    pd, ph = v.get("POS_DAY", "LEFT"), v.get("POS_HOC", "RIGHT")
    return (f"SPEAKER MAP: VOICE A belongs to the {pd} character ({v.get('TEN_DAY')}); VOICE B belongs to the {ph} character ({v.get('TEN_HOC')}). "
            f"In this clip only VOICE {vs} is heard, coming from the mouth of the {spos} character ({spk}). "
            f"The {role_s} ({spos}) says the line once, "
            f"{MV.speaker_how(v, turn['who'], turn.get('text', ''), turn.get('emo', ''))}. "
            f"The {role_s}'s expression grows naturally out of a calm ongoing mood and eases back down gently after the line. "
            + (f"{contrast} " if contrast else "") +
            f"The {role_l} ({lpos}) is quiet for the whole clip: lips gently closed, a calm relaxed face with a faint steady quiet mood, and {base}, at the {role_l}'s own pace regardless of the dialogue. "
            f"VOICE {vl} is resting in this clip.")


def drop_listener_voice(text, v, turn):
    """Bỏ 'VOICE LOCK' (khoá giọng) của NGƯỜI NGHE khỏi prompt: không có giọng nào được mô tả cho người im lặng thì Muse không có gì để lồng tiếng cho họ."""
    day = turn.get("who") == "day"
    voice = (v.get("GIONG_HOC") if day else v.get("GIONG_DAY")) or ""
    voice = voice.strip()
    if len(voice) < 12:
        return text
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


def scrub_listener_text(text):
    """Bỏ các cụm làm người nghe 'phản ứng' (liếc điện thoại, gật nhẹ...) khỏi prompt video."""
    for pat, rp in _LISTENER_SCRUB:
        text = re.sub(pat, rp, text, flags=re.I | re.S)
    return naturalize(text)


_WM = None
_WM_LOCK = threading.Lock()


def _whisper():
    global _WM
    with _WM_LOCK:
        if _WM is None:
            from faster_whisper import WhisperModel
            _WM = WhisperModel("small.en", device="cpu", compute_type="int8")
    return _WM


_WH_LOCK = threading.Lock()


def voice_span(path, expected):
    """(bắt đầu, kết thúc) của phần LỜI THOẠI thật trong clip, theo mốc thời gian từng từ của Whisper. Chỉ tính các từ khớp lời thoại nên tiếng cười, thở, 'ha ha' không bị tính.
    None nếu không nhận ra đủ lời."""
    import difflib
    norm = lambda w: re.sub(r"[^a-z]", "", w.lower())
    exp = [norm(w) for w in re.findall(r"[A-Za-z']+", expected or "") if norm(w)]
    if not exp:
        return None
    wav = path + ".span.wav"
    sh(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
    try:
        with _WH_LOCK:
            segs, _ = _whisper().transcribe(wav, language="en", beam_size=1, vad_filter=False, condition_on_previous_text=False, word_timestamps=True)
            words = [(norm(w.word), w.start, w.end) for sg in segs for w in (sg.words or [])]
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass
    hit = [(a, b) for t, a, b in words if t and any(difflib.SequenceMatcher(None, t, e).ratio() >= 0.78 for e in exp)]
    if len(hit) < max(1, int(0.5 * len(exp))):
        return None
    return hit[0][0], hit[-1][1]


def heard_words(path):
    wav = path + ".chk.wav"
    sh(["ffmpeg", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav])
    try:
        segs, _ = _whisper().transcribe(wav, language="en", beam_size=1, vad_filter=False, condition_on_previous_text=False)
        return [w for sg in segs for w in re.findall(r"[a-z']+", sg.text.lower())]
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


ZONES = {"LEFT": (0.03, 0.12, 0.47, 0.52), "RIGHT": (0.53, 0.08, 0.97, 0.50)}   # vùng đầu/mặt mỗi bên (tỉ lệ khung hình)


def zone_motion(path, side, t_end, fps=15, W=180, H=320):
    """Mức chuyển động trung bình ở vùng mặt của một bên trong [0, t_end] (người nói thật ~8-12, người nghe đứng yên ~2-4)."""
    x0, y0, x1, y1 = ZONES.get(side, ZONES["LEFT"])
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
_FACE_BOX = {"LEFT": (0.0, 0.0, 0.62, 0.62), "RIGHT": (0.55, 0.12, 1.0, 0.62)}


def mouth_activity(path, side, t_end, fps=12):
    """(độ lệch chuẩn, cực đại) của độ mở miệng (khoảng hở môi / bề rộng miệng) ở khuôn mặt bên `side` trong [0, t_end]. None nếu không dò được mặt."""
    import cv2
    import mediapipe as mp
    W, H = 360, 640
    d = crun(["ffmpeg", "-v", "error", "-t", f"{max(0.5, t_end):.2f}", "-i", path, "-vf", f"fps={fps},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(d) // (W * H * 3)
    if n < 6:
        return None
    fr = np.frombuffer(d[: n * W * H * 3], np.uint8).reshape(n, H, W, 3)
    b = _FACE_BOX.get(side, _FACE_BOX["LEFT"])
    x0, y0, x1, y1 = int(b[0] * W), int(b[1] * H), int(b[2] * W), int(b[3] * H)
    vals = []
    with _MP_LOCK:
        fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.3)
        try:
            for f in fr:
                c = cv2.resize(f[y0:y1, x0:x1], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                r = fm.process(c)
                if r.multi_face_landmarks:
                    lm = r.multi_face_landmarks[0].landmark
                    vals.append(abs(lm[14].y - lm[13].y) / (abs(lm[291].x - lm[61].x) + 1e-6))
        finally:
            fm.close()
    if len(vals) < 6:
        return None
    a = np.array(vals)
    return float(a.std()), float(a.max())


def mouth_check(path, speaker_side, listener_side, sens="normal"):
    """Người NGHE mấp máy miệng như người nói? Đã đối chiếu trên clip thật: người im lặng thật std ≈ 0.008-0.019, người mấp máy ≥ 0.029."""
    t_end = speech_end_of(path)
    sp, li = mouth_activity(path, speaker_side, t_end), mouth_activity(path, listener_side, t_end)
    if not sp or not li:
        return None
    abs_t, rel_t = {"high": (0.017, 0.35), "low": (0.032, 0.6)}.get(sens, (0.024, 0.45))   # độ nhạy: cao bắt cả mấp máy nhẹ (dễ gen lại thừa), thấp chỉ bắt mấp máy rõ
    bad = li[0] >= abs_t and li[0] >= rel_t * sp[0]
    return {"bad": bad, "speaker": round(sp[0], 3), "listener": round(li[0], 3)}


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


def speed_factor(syll, spoken, max_speed=1.25, ok_rate=3.4, target_rate=4.0, soften=0.7, top_rate=4.8):
    """Hệ số tăng tốc cho lời bị Muse kéo chậm. Nhịp nói = âm tiết/giây (cả khoảng ngắt). Từ `ok_rate` trở lên: để nguyên.
    Chậm hơn: tăng một PHẦN (`soften`) khoảng cách tới nhịp mục tiêu, chặn ở `max_speed`, và không bao giờ đẩy nhịp sau chỉnh vượt `top_rate` (tránh nghe quá nhanh)."""
    rate = syll / spoken
    if rate >= ok_rate:
        return 1.0
    f = 1.0 + soften * (target_rate / rate - 1.0)
    f = min(f, max_speed, top_rate / rate)
    return round(f, 3) if f > 1.03 else 1.0


def smart_cut(src, cut_path, last_png, lo=0.15, hi=0.8, fps=24, syll=None, speedfix=True, vf_extra="", max_speed=1.25, span=None, head_margin=0.2):
    """Cắt đuôi sau lời nói. Điểm cắt = khung ít chuyển động nhất trong [hết lời+lo, hết lời+hi].
    Khung cuối của clip đã cắt (last_png) là khung đầu cho clip kế."""
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


# ------------------------------------------------------------------ chạy một biến thể
def run_variant(vdata, template, out_dir, opts, emit, cancel):
    """emit(event, **kw): scene_init / scene / log / done. Trả về đường dẫn raw.mp4."""
    os.makedirs(out_dir, exist_ok=True)
    n_real = len(vdata.get("LUOT", []))
    risky = same_gender(vdata)   # robot và người học cùng giới: nguy cơ nói chồng cao hơn nhiều
    if risky and opts.get("voice_split", True):
        vdata = voice_split(vdata)
        emit("log", msg="Robot và người học cùng giới: tách giọng (robot cao, sáng, trẻ; người học trầm, khàn, chậm) để Muse không lẫn giọng")
    template = expand_script(template, n_real)  # nhiều lượt hơn số cảnh: tự nhân bản cảnh cuối
    want0 = analyze_script(template)["series"].get("LUOT")
    if want0 and 0 < n_real < want0:  # ít lượt hơn script: bù lượt trống cho đủ token rồi chỉ chạy n_real cảnh đầu
        vdata = dict(vdata, LUOT=list(vdata["LUOT"]) + [{"who": "day", "text": "", "emo": ""}] * (want0 - n_real))
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
    luot = vdata.get("LUOT", [])
    att_imgs, att_legend, att_auds = attachments(vdata, opts)
    emit("scene_init", scenes=[{"n": s["n"], "who": (luot[s["n"] - 1]["who"] if s["n"] - 1 < len(luot) else ""),
                                "text": (luot[s["n"] - 1]["text"] if s["n"] - 1 < len(luot) else s["title"]),
                                "state": "wait"} for s in scenes])
    prev_last, clips, ref_stats = None, [], None
    for sc in scenes:
        n = sc["n"]
        if cancel.is_set():
            raise Cancelled()
        if chat_every > 0:  # chat mới: Muse không "nhớ" các clip trước (tránh bắt chước lỗi cũ, tránh trả về video ghép); nhân vật vẫn nhất quán nhờ khung đầu + khoá mô tả
            want = f"{base_session}-{(n - 1) // chat_every}"
            if want != session:
                if session != base_session or started_sessions:
                    end_session(session)
                session = want
            if session not in started_sessions:
                started_sessions.append(session)
        has_img = bool(sc["f"].get("Prompt ảnh"))
        img_p, vid_p, neg = G.build_prompts(locks, sc)
        turn = luot[n - 1] if n - 1 < len(luot) else None
        syll = G.spoken_syllables(sc["f"].get("Voice", ""))  # đếm âm tiết trước khi sửa prompt
        fix_note = str((opts.get("scene_notes") or {}).get(str(n), "")).strip()
        if turn and turn.get("who") in ("day", "hoc"):
            import make_variants as MV
            tt = MV.turn_text(vdata, turn["who"], turn.get("text", ""), turn.get("emo", ""))
            day = turn["who"] == "day"
            spos = vdata.get("POS_DAY", "LEFT") if day else vdata.get("POS_HOC", "RIGHT")
            sname = vdata.get("TEN_DAY") if day else vdata.get("TEN_HOC")
            said = re.sub(r"\s+", " ", str(turn.get("text", "")).strip().replace('"', "'"))
            if tt in vid_p:  # lượt thoại xuất hiện nhiều lần (CHAR LOCK + Spoken dialogue): giữ MỘT bản đầy đủ ở đầu, các chỗ khác chỉ còn lời nói
                first = vid_p.index(tt)
                vs = "A" if day else "B"
                vid_p = vid_p[:first] + f"(the line and its delivery are given at the top, voiced by VOICE {vs})" + vid_p[first + len(tt):]
                vid_p = vid_p.replace(tt, f'VOICE {vs} (the {"tutor" if day else "learner"}, {spos}) says: "{said}"')
            vid_p = speaker_lock(vdata, turn) + "\n\n" + scrub_listener_text(drop_listener_voice(vid_p, vdata, turn))
            neg = compact_negative(neg)
        dur = G.auto_duration(syll) if syll else next((d for d in ALLOWED if d >= sc["seconds"]), 10)
        if fix_note:  # người dùng yêu cầu sửa riêng cho cảnh này khi làm lại: đặt đầu prompt video, ưu tiên cao nhất
            vid_p = f"CORRECTION FOR THIS CLIP (highest priority, overrides anything below that conflicts with it): {fix_note}\n\n" + vid_p
            emit("log", msg=f"Cảnh {n}: gen lại kèm yêu cầu sửa: {fix_note[:120]}")
        P = lambda f: os.path.join(out_dir, f)
        img_f, vid_f, cut_f, last_f = P(f"scene{n}_start.png"), P(f"scene{n}_clip.mp4"), P(f"scene{n}_cut.mp4"), P(f"scene{n}_last.png")
        if ref_stats is None and opts.get("normalize", True) and os.path.exists(vid_f):  # chạy tiếp: lấy lại chuẩn màu từ cảnh đầu đã có
            ref_stats = color_stats(vid_f, [0.04, 0.2, 0.4])
        if os.path.exists(cut_f) and os.path.exists(last_f):
            emit("scene", n=n, state="done", pct=100, thumb=os.path.basename(last_f), clip=os.path.basename(cut_f), secs=round(duration(cut_f), 1))
            prev_last = last_f
            clips.append(cut_f)
            continue
        ref_imgs = list(refs) + list(att_imgs) + ([G.data_url(prev_last)] if (prev_last and has_img) else [])
        if att_legend and has_img:
            img_p = img_p + "\n\nREFERENCE IMAGE NOTES: " + att_legend
        spk_auds = [a for g, a in att_auds if g in ((turn or {}).get("who"), "other", "scene")]

        def attempt(label, fn):
            for i in range(1, opts["retries"] + 2):
                try:
                    return fn()
                except Cancelled:
                    raise
                except Exception as e:
                    emit("log", msg=f"Cảnh {n} {label}: {e}", level="warn")
                    if _QUOTA_RE.search(str(e)):
                        raise QuotaExceeded(f"Muse báo hết hạn mức tạo video (giới hạn 24 giờ): {str(e)[:160]}") from None
                    if i > opts["retries"]:
                        raise
                    emit("scene", n=n, state=label, pct=0, note=f"thử lại {i}/{opts['retries']}")
                    time.sleep(4)

        if has_img and not os.path.exists(img_f):
            emit("scene", n=n, state="image", pct=0)

            def gi():
                b = api.generate("image", G.muse_image_prompt(img_p, neg, len(ref_imgs)), ref_imgs, session, timeout=opts["timeout"],
                                 on_status=lambda s, p: emit("scene", n=n, state="image", pct=p or 0), cancel=cancel)
                if G.kind_of(b) == "video":
                    open(img_f + ".mp4", "wb").write(b)
                    grab_frame(img_f + ".mp4", img_f)
                    os.remove(img_f + ".mp4")
                else:
                    open(img_f, "wb").write(b)
            attempt("image", gi)
            emit("scene", n=n, state="image", pct=100, thumb=os.path.basename(img_f))
        if os.path.exists(vid_f) and not has_audio(vid_f):  # clip câm còn sót từ lần chạy trước: bỏ đi để gen lại
            emit("log", msg=f"Cảnh {n}: clip cũ không có tiếng, gen lại", level="warn")
            os.remove(vid_f)
        if not os.path.exists(vid_f):
            start = img_f if has_img else prev_last
            vrefs = [G.data_url(start)] if start and os.path.exists(start) else []
            emit("scene", n=n, state="video", pct=0, dur=dur)

            def gv():
                b = api.generate("video", G.muse_video_prompt(vid_p, neg, dur, len(vrefs)), vrefs, session, duration=dur, timeout=opts["timeout"],
                                 on_status=lambda s, p: emit("scene", n=n, state="video", pct=p or 0), cancel=cancel, audios=spk_auds or None)
                open(vid_f, "wb").write(b)
                got = duration(vid_f)
                if got > 2 * dur + 1:  # Muse đôi khi trả về cả chuỗi clip cũ ghép lại (rất dài): clip mới nằm ở cuối -> chỉ giữ `dur` giây cuối. Dài hơn vừa phải (vd. 10s thay vì 8s) thì giữ nguyên, tránh mất đầu câu
                    emit("log", msg=f"Cảnh {n}: Muse trả về video ghép {got:.0f}s, chỉ lấy {dur}s cuối", level="warn")
                    tmp = vid_f + ".tail.mp4"
                    sh(["ffmpeg", "-y", "-sseof", f"-{dur}", "-i", vid_f, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", tmp])
                    os.replace(tmp, vid_f)
                if not has_audio(vid_f):  # Muse đôi khi trả về clip câm (không có track tiếng): coi như lỗi để gen lại, nếu không bước ghép sẽ hỏng
                    os.remove(vid_f)
                    raise RuntimeError("Muse trả về clip không có tiếng (mất lời thoại)")
            tries = 0
            tried = []            # (điểm lỗi = mức mấp máy của người nghe, file) của các lần gen có lỗi, để cuối cùng giữ lần TỐT NHẤT
            base_vid_p = vid_p
            while True:
                attempt("video", gv)
                if not (opts.get("check_overlap", True) and turn and turn.get("who") in ("day", "hoc")):
                    break
                emit("scene", n=n, state="cut", pct=100, note="kiểm tra giọng")
                pd, ph = vdata.get("POS_DAY", "LEFT"), vdata.get("POS_HOC", "RIGHT")
                spk_side, lis_side = (pd, ph) if turn["who"] == "day" else (ph, pd)
                try:
                    chk = interruptible(lambda: mouth_check(vid_f, spk_side, lis_side, opts.get("mouth_sens", "normal")), cancel)
                except Cancelled:
                    raise
                except Exception as ex:  # noqa: BLE001
                    emit("log", msg=f"Cảnh {n}: bỏ qua kiểm tra miệng người nghe ({ex})", level="warn")
                    break
                if not chk:
                    emit("log", msg=f"Cảnh {n}: không dò được khuôn mặt hai bên nên bỏ qua kiểm tra miệng (không gen lại)", level="warn")
                    break
                if not chk["bad"]:
                    emit("log", msg=f"Cảnh {n}: đo miệng OK (người nói {chk['speaker']}, người nghe {chk['listener']})" + (f" sau {tries} lần gen lại" if tries else ""))
                    tried = []   # lần này đạt: dùng nó, bỏ các lần lỗi trước
                    break
                # lỗi: ghi nhận lần này rồi gen lại NGAY (không chờ làm xong cả video), kèm yêu cầu sửa đúng lỗi vừa gặp
                keep = f"{vid_f}.try{tries}"
                shutil.copyfile(vid_f, keep)
                tried.append((chk["listener"], keep))
                emit("log", msg=f"Cảnh {n}: lần {tries + 1} bị lỗi người nghe mấp máy miệng như người nói (người nói {chk['speaker']}, người nghe {chk['listener']})", level="warn")
                if tries < int(opts.get("overlap_retries", 0)):
                    day = turn["who"] == "day"
                    lpos = vdata.get("POS_HOC", "RIGHT") if day else vdata.get("POS_DAY", "LEFT")
                    lis_is_learner = day
                    steps = [
                        f"in the previous attempt the {lpos} character moved their mouth along with the speaker. This time the {lpos} character's mouth stays shut and perfectly still for the whole clip (lips pressed together); only the speaker's mouth ever moves.",
                        (f"the previous attempts still showed the {lpos} character mouthing along. Now the {lpos} character keeps their head bowed low over their hands and the work, face half hidden, eyes on their hands, lips pressed together, and never lifts their head."
                         if lis_is_learner else
                         f"the previous attempts still showed the {lpos} character mouthing along. Now the {lpos} character is a completely still, calm avatar: mouth a thin closed line, eyes on the camera, no lip movement at all, only slow blinking."),
                        (f"again the {lpos} character mouthed along. Now the {lpos} character turns their face away to the side, looking down at the work so that the mouth is not visible to the camera, and keeps it closed."
                         if lis_is_learner else
                         f"again the {lpos} character mouthed along. Now the {lpos} character looks calmly aside with a perfectly closed, motionless mouth and does not speak or smile."),
                        (f"the {lpos} character stays almost entirely turned away from the camera, working with the head down and the face in shadow, mouth completely closed and still for the entire clip."
                         if lis_is_learner else
                         f"the {lpos} character is shown as a frozen, silent video-call avatar: lips sealed, eyes softly lowered, no mouth movement whatsoever for the entire clip."),
                        (f"final attempt: the {lpos} character's lower face is not the focus at all: head lowered, chin tucked, attention fully on the work, lips sealed, absolutely no speaking or mouthing."
                         if lis_is_learner else
                         f"final attempt: the {lpos} character is a still image: eyes closed in a calm resting expression, lips sealed, absolutely no speaking or mouthing."),
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
        emit("scene", n=n, state="cut", pct=100)
        vf_fix, fix_note = "", ""
        if opts.get("normalize", True):
            c_start = color_stats(vid_f, [0.04, 0.2, 0.4])
            c_end = color_stats(vid_f, [-0.6, -0.35, -0.1])
            if ref_stats is None:
                ref_stats = c_start  # chuẩn màu = khung đầu cảnh 1 (đúng màu ảnh gốc)
            vf_fix, fix_note = color_match(ref_stats, c_start, c_end, duration(vid_f))
            if vf_fix:
                emit("log", msg=f"Cảnh {n}: cân màu về cảnh đầu ({fix_note})")
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
        info = smart_cut(vid_f, cut_f, last_f, syll=syll, speedfix=opts.get("speedfix", True), vf_extra=vf_fix, max_speed=float(opts.get("speed_max", 1.25)),
                         span=span, lo=(0.18 if span else 0.15), hi=(max(0.3, margin + 0.05) if span else 0.8), head_margin=margin * 0.7) if opts.get("cut", True) else None
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
        prev_last = last_f
        clips.append(cut_f)
        emit("scene", n=n, state="done", pct=100, thumb=os.path.basename(last_f), clip=os.path.basename(cut_f),
             secs=round(duration(cut_f), 1), raw=round(info["total"], 1) if info else None, note=(f"x{info['speed']}" if info and info["speed"] > 1 else ""))
        if info and info["speed"] > 1:
            emit("log", msg=f"Cảnh {n}: lời nói chậm, tăng tốc x{info['speed']}")
    end_session(session)
    raw = os.path.join(out_dir, "raw.mp4")
    ins, fl = [], ""
    for i, c in enumerate(clips):
        ins += ["-i", c]
        fl += f"[{i}:v]scale=720:1280:flags=accurate_rnd+full_chroma_int:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v{i}];"
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


def subs_from_variant(v, auto_hook=True):
    units = []
    turns = v.get("LUOT", [])
    explicit = any(t.get("fx") for t in turns)   # chỉnh tay ở bất kỳ lượt nào (kể cả "Không") thì tắt tự động
    marks = {} if explicit or not auto_hook else hook_marks(turns)
    for ti, t in enumerate(turns):
        text = re.sub(r"\s+", " ", str(t.get("text", "")).strip())
        parts = [p.strip() for p in re.findall(r"[^.!?…]+[.!?…]*", text) if p.strip()]
        merged = []
        for p in parts:
            if merged and len(merged[-1]) < 12:
                merged[-1] += " " + p
            else:
                merged.append(p)
        for i, p in enumerate(merged):
            u = {"t": p, "c": t.get("c") or "white"}
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
    return {"scenes": len(re.findall(r"^CẢNH \d+ \(", text, flags=re.M)), "plain": [t for t in tokens if t not in in_series], "series": series}


KNOWN_FIELDS = {
    "NGUOI_DAY": ("Ngoại hình", "day", "long", "a humanoid AI robot tutor with a smooth bald head…"), "TEN_DAY": ("Gọi ngắn", "day", "short", "the AI robot tutor"),
    "GIONG_DAY": ("Giọng", "day", "long", "a warm, lively female voice, American accent"),
    "NGUOI_HOC": ("Ngoại hình", "hoc", "long", "a young woman with long wavy brown hair, white t-shirt…"), "TEN_HOC": ("Gọi ngắn", "hoc", "short", "the young woman holding a spoon"),
    "GIONG_HOC": ("Giọng", "hoc", "long", "a natural, young, expressive voice"),
    "NEN_TRAI": ("Nền bên trái", "scene", "long", "a flat chroma-key green background"), "NEN_PHAI": ("Nền bên phải", "scene", "long", "an empty sunny garden, soft bokeh"),
    "VIEC": ("Đang làm gì", "scene", "long", "stirring a pot of pasta"), "DAO_CU": ("Đạo cụ", "scene", "long", "holding a wooden spoon"),
    "DAO_GIU": ("Cách cầm", "scene", "long", "she holds the spoon in her right hand"), "DAO_NGHI": ("Tay khi nghỉ", "scene", "long", "one hand resting on the pot handle"),
}


def suggest_fields(plain, has_luot, existing=None):
    """Gợi ý bảng trường từ các token. `existing` (danh sách trường đã có) được giữ nguyên nhãn/nhóm/loại theo key."""
    old = {f["key"]: f for f in (existing or [])}
    keys = list(plain)
    if has_luot:
        for k in ("TEN_DAY", "TEN_HOC"):
            if k not in keys:
                keys.append(k)
    out = []
    for k in keys:
        if k in old:
            out.append(old[k]); continue
        lab, grp, kind, ph = KNOWN_FIELDS.get(k, (k.replace("_", " ").capitalize(), "day" if k.endswith("_DAY") else "hoc" if k.endswith("_HOC") else "other", "long", ""))
        out.append({"key": k, "label": lab, "group": grp, "kind": kind, "ph": ph, "default": ""})
    order = {"day": 0, "hoc": 1, "scene": 2}
    prio = list(KNOWN_FIELDS)
    out.sort(key=lambda f: (order.get(f["group"], 3), prio.index(f["key"]) if f["key"] in prio else 100 + keys.index(f["key"])))
    return out
