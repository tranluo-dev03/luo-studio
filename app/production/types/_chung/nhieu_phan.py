"""Gen một video NHIỀU PHẦN trong MỘT dự án: mỗi phần là một kịch bản con chạy bằng chế độ có sẵn của Studio
(phần thường: các khối CẢNH, engine.run_variant; phần ghép 2 lớp: khối [GHEP HAI LOP], split.run_split), rồi ghép tất cả thành raw.mp4.
Dùng chung cho mọi thể loại: gen.py của thể loại chỉ cần gọi run(...) (xem types/san-bay-gia-su-ai/gen.py).

Kịch bản:
    [HAU KY]:
    loai: <mã thể loại>

    ===== PHAN 1: tình huống =====
    <kịch bản con thường: [STYLE LOCK] ... CẢNH 1 ...>

    ===== PHAN 2: ghép 2 lớp | vào: nhoè 0.5 =====
    <kịch bản con ghép 2 lớp: [GHEP HAI LOP] ...>
- Dòng chia phần: "PHAN"/"PHẦN" + số, tên tuỳ ý, sau dấu "|" là tuỳ chọn "vào: nhoè [giây]" (nhoè chuyển động khi vào phần này)
  hoặc "vào: chớp trắng|vàng|đen|#RRGGBB [giây]".
- Biến thể: một mảng LUOT chung, mỗi lượt có "phan": <số phần>, xếp theo thứ tự phần. Mỗi phần chỉ thấy các nhân vật có token
  TEN_/NGUOI_<KHOÁ> trong kịch bản con của nó (token của nhân vật khác bị bỏ khỏi biến thể khi gen phần đó).
  Nhân vật có mặt ở nhiều phần mà cần giá trị khác nhau (vd. hướng nhìn khi nói NHIN_HOC: phần 1 nhìn người đối diện, phần 2 nhìn ống kính):
  ghi thêm khoá "NHIN_HOC@2" trong biến thể, khoá này thay NHIN_HOC khi gen phần 2.

Thư mục chạy: mỗi phần chạy trong thư mục con phan<N>/ với số cảnh riêng; clip xong được nối (hard link) ra thư mục chạy theo số cảnh CHUNG
(scene<cảnh chung>_cut.mp4 / _last.png) nên Hậu kỳ, "Làm lại từ cảnh", xem ảnh trong Studio dùng như dự án thường.
Cảnh nào bị xoá ở thư mục chạy (làm lại) thì file của cảnh đó trong phần cũng bị xoá trước khi chạy để gen lại.
Ghi phan.json: [{scene, phan, local, turn}] để hậu kỳ riêng biết cảnh nào thuộc phần nào.
"""
import json
import os
import re
import shutil
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "luo-studio"))
if STUDIO not in sys.path:
    sys.path.insert(0, STUDIO)
import engine as E  # noqa: E402
import split as SP  # noqa: E402
import make_variants as MV  # noqa: E402
G = E.G
_FLASH = {"trang": "FFFFFF", "white": "FFFFFF", "vang": "FFF1C9", "den": "000000", "black": "000000"}


def _plain(s):
    s = unicodedata.normalize("NFD", str(s)).replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def parse_parts(template):
    """[{n, name, enter, text, split}] theo thứ tự trong kịch bản. enter = None | ("blur", giây) | ("flash", màu, giây)."""
    parts, cur = [], None
    for ln in template.splitlines(keepends=True):
        m = re.match(r"^\s*=+\s*phan\s+(\d+)\s*:?\s*([^|=]*?)\s*(?:\|\s*([^=]*?))?\s*=+\s*$", _plain(ln.rstrip("\r\n")))
        if m:
            cur = {"n": int(m.group(1)), "name": ln.strip().strip("= ").split("|")[0].strip(), "enter": _enter(m.group(3) or ""), "text": ""}
            parts.append(cur)
        elif cur is not None:
            cur["text"] += ln
    if not parts:
        raise RuntimeError('Kịch bản nhiều phần cần các dòng chia phần dạng "===== PHAN 1: tên phần ====="')
    for p in parts:
        p["split"] = SP.is_split(p["text"])
    if [p["n"] for p in parts] != list(range(1, len(parts) + 1)):
        raise RuntimeError("Các phần phải đánh số liên tiếp từ 1: " + ", ".join(str(p["n"]) for p in parts))
    return parts


def _enter(opt):
    m = re.search(r"vao\s*:\s*(.+)", opt)
    if not m:
        return None
    v = m.group(1)
    d = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:s|giay)?\s*$", v)
    secs = float(d.group(1).replace(",", ".")) if d else None
    if re.search(r"\blia\b|\bpan\b", v):   # lia máy nhanh sang người/cảnh kế tiếp; "lia trai" = máy lia sang trái, mặc định lia sang phải
        return ("pan", min(0.8, max(0.2, secs or 0.36)), "left" if re.search(r"trai|left", v) else "right")
    if "nhoe" in v or "blur" in v:
        return ("blur", min(1.2, max(0.2, secs or 0.5)))
    col = re.search(r"#([0-9a-f]{6})", v)
    col = col.group(1).upper() if col else next((c for k, c in _FLASH.items() if k in v), None)
    return ("flash", col, min(1.2, max(0.1, secs or 0.4))) if col else None


def part_chars(text, turns):
    keys = set(re.findall(r"\{\{\s*(?:TEN|NGUOI)_([A-Z0-9]+)\s*\}\}", text))
    if SP.is_split(text):   # ghép 2 lớp: nhân vật = nền + các khung trong bố cục
        cfg = SP.parse(text)[0]
        keys |= {cfg["bg"], *cfg["panels"]}
    return keys | {MV.ck(t.get("who")) for t in turns}


def sub_variant(vdata, keep, turns, part=None):
    """Biến thể cho một phần: bỏ token của nhân vật không có mặt trong phần (vd. TEN_DAY của robot ở phần tình huống) và ảnh gắn cho các token đó.
    Khoá "<TOKEN>@<số phần>" (vd. "NHIN_HOC@2") ghi đè <TOKEN> riêng cho phần đó; khoá @ của phần khác bị bỏ."""
    drop = set(MV.chars_of({k: x for k, x in vdata.items() if "@" not in str(k)})) - set(keep)
    gone = lambda k: isinstance(k, str) and any(k.endswith("_" + c) and k.isupper() for c in drop)
    v = {k: x for k, x in vdata.items() if not gone(k) and "@" not in str(k)}
    for k, x in vdata.items():
        base, _, n = str(k).partition("@")
        if n and part is not None and n.strip() == str(part) and not gone(base):
            v[base] = x
    if isinstance(vdata.get("refs"), dict):
        v["refs"] = {k: x for k, x in vdata["refs"].items() if not gone(k)}
    v["LUOT"] = turns
    return v


def _link(src, dst):
    try:
        os.remove(dst)
    except OSError:
        pass
    try:
        os.link(src, dst)
    except OSError:
        shutil.copyfile(src, dst)


def plan(vdata, template):
    """(các phần, danh sách cảnh chung [{scene, phan, local, turn}]). Kiểm tra lượt thoại khớp các phần."""
    parts = parse_parts(template)
    luot = [t for t in vdata.get("LUOT", []) if str(t.get("text", "")).strip()]
    if luot and not all("phan" in t for t in luot):
        raise RuntimeError('Kịch bản nhiều phần: mỗi lượt thoại cần khoá "phan" (số phần), vd. {"who": "hoc", "text": "...", "phan": 2}')
    seq = [int(t["phan"]) for t in luot]
    if seq != sorted(seq):
        raise RuntimeError('Lượt thoại phải xếp theo thứ tự phần (mọi lượt "phan": 1 trước, rồi "phan": 2...)')
    scenes, off = [], 0
    for p in parts:
        idx = [i for i, t in enumerate(luot) if int(t["phan"]) == p["n"]]
        p["turns"] = [luot[i] for i in idx]
        if not p["turns"] and (p["split"] or "{{LUOT_" in p["text"]):
            raise RuntimeError(f'Phần {p["n"]} ({p["name"]}) chưa có lượt thoại nào ("phan": {p["n"]})')
        count = len(idx) if (p["split"] or "{{LUOT_" in p["text"]) else len(re.findall(r"^CẢNH \d+ \(", p["text"], re.M))
        p["off"], p["count"] = off, count
        for l in range(1, count + 1):
            scenes.append({"scene": off + l, "phan": p["n"], "local": l, "turn": idx[l - 1] if l - 1 < len(idx) else None})
        off += count
        bad = {MV.ck(t.get("who")) for t in p["turns"]} - part_chars(p["text"], [])
        if bad:
            raise RuntimeError(f'Phần {p["n"]}: lượt thoại của {", ".join(sorted(bad))} nhưng kịch bản con không có nhân vật này')
    return parts, scenes


def run(vdata, template, out_dir, opts, emit, cancel, blur_strength=1.0):
    """Gen cả video nhiều phần; trả về raw.mp4 (đã có chuyển cảnh giữa các phần)."""
    parts, scenes = plan(vdata, template)
    json.dump(scenes, open(os.path.join(out_dir, "phan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    luot = [t for t in vdata.get("LUOT", []) if str(t.get("text", "")).strip()]
    emit("scene_init", scenes=[{"n": s["scene"], "who": luot[s["turn"]]["who"] if s["turn"] is not None else "",
                                "text": (f"[P{s['phan']}] " + luot[s["turn"]]["text"]) if s["turn"] is not None else f"[P{s['phan']}] cảnh {s['local']}",
                                "state": "wait"} for s in scenes])
    emit("log", msg="Video nhiều phần: " + "; ".join(f"phần {p['n']} {p['name']} ({'ghép 2 lớp' if p['split'] else 'cảnh thường'}, {p['count']} cảnh)" for p in parts))
    only = opts.get("only")
    notes = {int(k): v for k, v in (opts.get("scene_notes") or {}).items()}
    for p in parts:
        off, k = p["off"], p["n"]
        if only and off >= only:
            break
        pdir = os.path.join(out_dir, f"phan{k}")
        os.makedirs(pdir, exist_ok=True)
        for l in range(1, p["count"] + 1):   # cảnh bị xoá ở thư mục chạy (làm lại / dừng giữa chừng): xoá luôn file của cảnh đó trong phần để gen lại
            if not os.path.exists(os.path.join(out_dir, f"scene{off + l}_cut.mp4")):
                for f in os.listdir(pdir):
                    if re.match(rf"scene{l}_", f):
                        os.remove(os.path.join(pdir, f))

        def em(ev, off=off, k=k, pdir=pdir, **kw):
            if ev == "scene_init":
                return
            if ev == "scene" and "n" in kw:
                kw["n"] += off
                for key in ("thumb", "clip"):
                    name = kw.get(key)
                    if name and os.path.exists(os.path.join(pdir, name)):
                        m = re.match(r"scene(\d+)_(.+)$", name)
                        dst = f"scene{int(m.group(1)) + off}_{m.group(2)}" if m else f"phan{k}_{name}"
                        _link(os.path.join(pdir, name), os.path.join(out_dir, dst))
                        kw[key] = dst
            elif ev == "log":
                kw["msg"] = f"[Phần {k}] " + re.sub(r"Cảnh (\d+)", lambda m: f"Cảnh {int(m.group(1)) + off}", kw.get("msg", ""))
            emit(ev, **kw)
        popts = dict(opts, _part=True, scene_notes={str(g - off): v for g, v in notes.items() if off < g <= off + p["count"]},
                     only=(min(p["count"], only - off) if only else None))
        emit("log", msg=f"Phần {k}: {p['name']}")
        E.run_variant(sub_variant(vdata, part_chars(p["text"], p["turns"]), p["turns"], k), p["text"].strip() + "\n", pdir, popts, em, cancel)
        for l in range(1, (popts["only"] or p["count"]) + 1):   # chắc chắn clip từng cảnh đã có ở thư mục chạy (kể cả cảnh dùng lại từ lần trước)
            for suf in ("cut.mp4", "last.png"):
                src = os.path.join(pdir, f"scene{l}_{suf}")
                if os.path.exists(src):
                    _link(src, os.path.join(out_dir, f"scene{off + l}_{suf}"))
    n_all = min(len(scenes), only) if only else len(scenes)
    clips = [os.path.join(out_dir, f"scene{g}_cut.mp4") for g in range(1, n_all + 1)]
    fx = [{} for _ in clips]
    blurs, pans = [], []   # (chỉ số clip bắt đầu sau mốc, giây[, hướng])
    for p in parts:
        if p["off"] >= n_all:
            break
        sf = os.path.join(out_dir, f"phan{p['n']}", "script.txt")
        if not p["split"] and os.path.exists(sf):   # phần thường: giữ "Chuyển cảnh" / "Lớp phủ" của từng cảnh như chế độ thường
            _, scs = G.parse_script(open(sf, encoding="utf-8").read())
            for sc in scs:
                g = p["off"] + sc["n"] - 1
                if sc["n"] <= p["count"] and g < n_all:
                    fx[g] = E.scene_fx(sc["f"])
                    tr = _enter("vao: " + _plain(sc["f"].get("Chuyển cảnh", "")))   # "lia phải 0.3" / "nhoè": làm ở đây (engine chỉ có chớp màu)
                    if g and tr and tr[0] == "pan":
                        pans.append((g, tr[1], tr[2]))
                    elif g and tr and tr[0] == "blur":
                        blurs.append((g, tr[1]))
        if p["n"] > 1 and p["enter"]:
            if p["enter"][0] == "flash":
                fx[p["off"]]["flash"] = (p["enter"][1], p["enter"][2])
            elif p["enter"][0] == "pan":
                pans.append((p["off"], p["enter"][1], p["enter"][2]))
            else:
                blurs.append((p["off"], p["enter"][1]))
    raw = E.concat_clips(clips, out_dir, emit, fx)
    at = lambda i: sum(E.duration(c) for c in clips[:i])
    morphs = {}   # phần ghép 2 lớp: mỗi cảnh bắt đầu lại từ ảnh gốc nên tư thế nhảy ở chỗ nối -> chuyển mượt (split.morph_cuts); chỗ vào phần giữ hiệu ứng riêng
    for p in parts:
        if p["split"] and p["off"] < n_all:
            join = SP.parse(p["text"])[0]["join"]
            if join[0] == "morph":
                for i in range(p["off"] + 1, min(p["off"] + p["count"], n_all)):
                    morphs[at(i)] = join[1]
    for d in sorted(set(morphs.values())):
        SP.morph_cuts(raw, [t for t, x in morphs.items() if x == d], d)
    if morphs:
        emit("log", msg=f"Làm mượt {len(morphs)} chỗ nối trong phần ghép 2 lớp")
    if blurs:
        whip_blur(raw, [(at(i), d) for i, d in blurs], blur_strength)
        emit("log", msg="Chuyển cảnh nhoè: " + ", ".join(f"{at(i):.1f}s" for i, _ in blurs))
    if pans:
        whip_pan(raw, [(at(i), d, side) for i, d, side in pans], blur_strength)
        emit("log", msg="Chuyển cảnh lia máy: " + ", ".join(f"{at(i):.1f}s ({'trái' if side == 'left' else 'phải'})" for i, _, side in pans))
    return raw


def whip_pan(raw, marks, strength=1.0, zoom=1.4):
    """Lia máy nhanh qua mỗi mốc (giây, độ dài, "left"/"right"), như máy quay vụt từ người này sang người kia: nửa đầu khung cũ trượt ra, nửa sau khung mới trượt vào
    (phóng to `zoom` lần để có chỗ trượt) kèm nhoè ngang. Chỉ đè lên hình trong các khoảng đó, không đổi độ dài video và tiếng."""
    W, H = 720, 1280
    sw, sh = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    mid, top = (sw - W) / 2, (sh - H) / 2
    x = f"{mid:.1f}"
    for t, d, side in marks:
        h = d / 2
        a, b = t - h, t + h
        out_x = f"{mid:.1f}+{mid:.1f}*(t-{a:.3f})/{h:.3f}" if side == "right" else f"{mid:.1f}-{mid:.1f}*(t-{a:.3f})/{h:.3f}"   # khung cũ trượt ra
        in_x = f"{mid:.1f}*(t-{t:.3f})/{h:.3f}" if side == "right" else f"{2 * mid:.1f}-{mid:.1f}*(t-{t:.3f})/{h:.3f}"           # khung mới trượt vào
        x = f"if(between(t,{a:.3f},{t:.3f}),{out_x},if(between(t,{t:.3f},{b:.3f}),{in_x},{x}))"
    on = "+".join(f"between(t,{t - d / 2:.3f},{t + d / 2:.3f})" for t, d, _ in marks)
    fc = (f"[0:v]split=2[base][w];[w]scale={sw}:{sh},crop={W}:{H}:x='{x}':y={top:.1f},avgblur=sizeX={max(1, int(40 * strength))}:sizeY=1[pan];"
          f"[base][pan]overlay=0:0:enable='{on}'[v]")
    tmp = raw + ".pan.mp4"
    E.sh_enc(["ffmpeg", "-y", "-i", raw, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "copy", tmp])
    os.replace(tmp, raw)


def whip_blur(raw, marks, strength=1.0):
    """Nhoè chuyển động ngang quanh mỗi mốc (giây, độ dài): mờ tăng dần tới mốc rồi giảm dần, không đổi độ dài video."""
    fl = []
    for t, d in marks:
        h = d / 2
        for frac, size in ((1.0, 10), (0.66, 26), (0.33, 60)):
            a, b = t - h * frac, t + h * frac
            fl.append(f"avgblur=sizeX={max(1, int(size * strength))}:sizeY=1:enable='between(t,{a:.3f},{b:.3f})'")
    tmp = raw + ".blur.mp4"
    E.sh_enc(["ffmpeg", "-y", "-i", raw, "-vf", ",".join(fl), "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "copy", tmp])
    os.replace(tmp, raw)
