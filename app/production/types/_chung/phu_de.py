"""Phụ đề hậu kỳ dùng chung cho các thể loại có hậu kỳ riêng: căn lời theo từng cảnh (Whisper, postprocess.align_by_scene) rồi đốt phụ đề vào video.
So với hậu kỳ chung (postprocess.py) có thêm:
- dòng dịch dưới phụ đề chính: khoá "dich" của lượt thoại (chữ đỏ viền trắng, nhỏ hơn), chia theo CÂU và hiện cùng câu tiếng Anh tương ứng
  (số câu hai bên khác nhau thì chia đều theo thứ tự);
- icon cạnh cuối câu: "icon": "x" (ô đỏ ❌), "check" (ô xanh ✅), "dollar" (túi tiền $);
- cụm chữ nhấn trên ô màu: "nhan": "<cụm chữ trong câu>" (vd. tên app) hiện riêng trên ô vàng chữ đen;
- viền nháy + tiếng: "fx": "wrong" (đỏ, tè tè) / "right" (xanh lá, tinh tinh) / "ding" (cyan, tinh tinh).
- ô nền sau chữ: "o": <màu> (vd. ô vàng chữ đen, ô đen chữ xanh ngọc); không có "o" thì chữ có viền đen;
- tô màu đúng các từ sai/đúng: "to": "<cụm chữ>" (hoặc danh sách), màu theo "fx" (wrong = đỏ, right = xanh lá) hoặc "to_mau".
Màu chữ chính theo "c" (white/yellow/red/green/black/teal/blue). Lượt không ghi "c"/"o" thì lấy kiểu mặc định (apply_styles, theo phần và người nói).
Dùng: units_from_variant(...) -> apply_styles(...) -> align(...) -> burn(...). Điểm vào đầy đủ cho post.py của thể loại: hau_ky.py."""
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.normpath(os.path.join(HERE, "..", ".."))
if PROD not in sys.path:
    sys.path.insert(0, PROD)
import postprocess as PP  # noqa: E402

BGR = {"white": "FFFFFF", "yellow": "00D8FF", "red": "2A2AFF", "green": "5ACB3C", "black": "000000", "teal": "C8E03F", "blue": "FF7A3A"}   # ASS dùng BGR; "blue" thêm 05/11/2026 cho du-lich-chia-doi (chỉ bổ sung)
FX_COLOR = {"wrong": "red", "right": "green"}


def _sentences(text):
    """Các câu của một lượt (câu rất ngắn dưới 12 ký tự gộp với câu sau), như hậu kỳ chung."""
    out = []
    text = re.sub(r"\s+", " ", str(text or "").strip())
    for p in (p.strip() for p in re.findall(r"[^.!?…]+[.!?…]*", text) if p.strip()):
        if out and len(out[-1]) < 12:
            out[-1] = out[-1] + " " + p
        else:
            out.append(p)
    return out


def _parts(text, phrase):
    """Chia lượt thành các dòng phụ đề theo câu; nếu có cụm nhấn thì tách cụm đó thành dòng riêng. Trả về [(chữ, ô nhấn?, số thứ tự câu)]."""
    out = [(t, False, i) for i, t in enumerate(_sentences(text))]
    if phrase:
        res = []
        for t, _, si in out:
            i = t.lower().find(phrase.lower())
            if i < 0:
                res.append((t, False, si))
                continue
            for seg, box in ((t[:i], False), (t[i:i + len(phrase)], True), (t[i + len(phrase):], False)):
                seg = seg.strip(" ,")
                if seg.strip(" .!?"):
                    res.append((seg, box, si))
                elif res and seg:   # dấu câu sau cụm nhấn
                    res[-1] = (res[-1][0] + seg, res[-1][1], res[-1][2])
        out = res
    return out


def _dich_by_sentence(dich, en):
    """Chia lời dịch theo các câu tiếng Anh `en` (danh sách câu): mỗi câu dịch (không gộp câu ngắn) đi với câu tiếng Anh nằm ở cùng vị trí tương đối
    tính theo số ký tự; câu tiếng Anh không nhận được câu dịch nào thì hiện câu dịch ở vị trí của nó (một câu dịch có thể kéo qua vài câu tiếng Anh)."""
    d = [p.strip() for p in re.findall(r"[^.!?…]+[.!?…]*", re.sub(r"\s+", " ", str(dich or "").strip())) if p.strip()]
    n = len(en)
    if not d or not n:
        return [""] * n
    pos = lambda parts: [(sum(map(len, parts[:i])) + len(p) / 2) / max(1, sum(map(len, parts))) for i, p in enumerate(parts)]   # vị trí giữa mỗi câu, 0..1
    edges = [sum(map(len, en[:i + 1])) / sum(map(len, en)) for i in range(n)]   # mép phải của từng câu tiếng Anh
    which = lambda x: next(i for i, e in enumerate(edges) if x <= e + 1e-9)
    groups = [[] for _ in range(n)]
    for p, x in zip(d, pos(d)):
        groups[which(x)].append(p)
    dpos, epos = pos(d), pos(en)
    return [" ".join(g) if g else min(zip(d, dpos), key=lambda q: abs(q[1] - epos[i]))[0] for i, g in enumerate(groups)]


def units_from_variant(v, scene_of_turn):
    """Các dòng phụ đề từ LUOT. scene_of_turn: {chỉ số lượt -> chỉ số cảnh (0-based) trong raw.mp4}; lượt không có cảnh thì bỏ."""
    units = []
    for ti, t in enumerate(x for x in v.get("LUOT", []) if str(x.get("text", "")).strip()):
        if ti not in scene_of_turn:
            continue
        dich = _dich_by_sentence(t.get("dich"), _sentences(t.get("text", ""))) if str(t.get("dich") or "").strip() else []
        parts = _parts(t.get("text", ""), t.get("nhan") or "")
        # viền + tiếng sai/đúng ("fx") rơi vào dòng chứa cụm sai/đúng ("to") nếu có, không phải luôn dòng đầu: "Ah, sí, es verdad. I'm 22." phải
        # ting ting ở "I'm 22", không ở "Ah, sí, es verdad." (05/11/2026, du-lich-chia-doi). Không có "to" thì như cũ (dòng đầu).
        tos = [x.lower() for x in ([t["to"]] if isinstance(t.get("to"), str) else list(t.get("to") or [])) if x]
        fx_i = next((i for i, (p, _, _) in enumerate(parts) if any(x in p.lower() for x in tos)), 0)
        for i, (p, box, si) in enumerate(parts):
            u = {"t": p, "c": t.get("c"), "o": t.get("o"), "who": str(t.get("who", "")).lower(), "turn": scene_of_turn[ti], "lid": ti, "box": box}
            if dich and dich[si]:
                u["dich"] = dich[si]
            if t.get("to"):
                u["to"] = [t["to"]] if isinstance(t["to"], str) else list(t["to"])
                u["to_mau"] = t.get("to_mau") or FX_COLOR.get(t.get("fx"), "yellow")
            if i == fx_i and t.get("fx") in ("wrong", "right", "ding"):
                u["fx"] = t["fx"]
            units.append(u)
        if units and units[-1]["lid"] == ti:
            if t.get("icon"):
                units[-1]["icon"] = t["icon"]
    return units


def apply_styles(units, style_of):
    """Điền màu chữ "c" / ô "o" cho dòng chưa ghi. style_of(unit) -> {"c": ..., "o": ...} (vd. theo phần và người nói, từ config.json của thể loại)."""
    for u in units:
        st = style_of(u) or {}
        if not u.get("c"):
            u["c"] = st.get("c") or "white"
        if not u.get("o") and st.get("o"):
            u["o"] = st["o"]
    return units


def _paint(txt, phrases, color, base):
    """Tô màu từng từ của các cụm `phrases` trong dòng phụ đề (không phân biệt hoa/thường), xong trả lại màu chính."""
    for w in (x.strip(".,!?\"'") for ph in phrases for x in ph.split()):
        if w:
            txt = re.sub(r"(?<![\w'])" + re.escape(w) + r"(?![\w'])", lambda m: "{\\1c&H" + color + "&}" + m.group(0) + "{\\1c&H" + base + "&}", txt, count=1, flags=re.I)
    return txt


def align(src, units, scenes_file, model="small.en"):
    scenes = json.load(open(scenes_file, encoding="utf-8")) if scenes_file and os.path.exists(scenes_file) else None
    res = PP.align_by_scene(src, units, scenes, model) if scenes else None
    if res is None:
        words = PP.transcribe(src, model, " ".join(u["t"] for u in units))
        res = PP.align(units, words or PP.estimate_words(src, units))
    for u in res:
        print(f"  {u['s']:6.2f}-{u['e']:6.2f}  {u.get('c') or 'white':6}  {u['t']}" + (f"  [{u['dich']}]" if u.get("dich") else ""))
    return res


def _icon(kind, x, y, s, t0, t1):
    """Dòng ASS vẽ icon vuông cạnh s tại (x, y) góc trên trái."""
    ts = lambda t: PP.ts(t)
    sq = f"m 0 0 l {s} 0 l {s} {s} l 0 {s}"
    if kind == "x":
        k = s / 60
        mark = " ".join(f"{c}" if c.isalpha() else f"{float(c) * k:.0f}" for c in "m 14 18 l 18 14 l 30 26 l 42 14 l 46 18 l 34 30 l 46 42 l 42 46 l 30 34 l 18 46 l 14 42 l 26 30".split())
        return [f"Dialogue: 3,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an7\\pos({x},{y})\\1c&H2A2AFF&\\bord0\\shad0\\p1}}{sq}{{\\p0}}",
                f"Dialogue: 4,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an7\\pos({x},{y})\\1c&HFFFFFF&\\bord0\\shad0\\p1}}{mark}{{\\p0}}"]
    if kind == "check":
        k = s / 60
        mark = " ".join(f"{c}" if c.isalpha() else f"{float(c) * k:.0f}" for c in "m 12 31 l 18 25 l 26 33 l 44 14 l 50 20 l 26 45".split())
        return [f"Dialogue: 3,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an7\\pos({x},{y})\\1c&H3CCB5A&\\bord0\\shad0\\p1}}{sq}{{\\p0}}",
                f"Dialogue: 4,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an7\\pos({x},{y})\\1c&HFFFFFF&\\bord0\\shad0\\p1}}{mark}{{\\p0}}"]
    if kind == "dollar":   # túi tiền: thân tròn vàng đậm + chữ $ nâu
        r, c = s / 2, s / 2 * 0.552
        circle = (f"m {r:.0f} 0 b {r + c:.0f} 0 {s} {r - c:.0f} {s} {r:.0f} b {s} {r + c:.0f} {r + c:.0f} {s} {r:.0f} {s} "
                  f"b {r - c:.0f} {s} 0 {r + c:.0f} 0 {r:.0f} b 0 {r - c:.0f} {r - c:.0f} 0 {r:.0f} 0")
        return [f"Dialogue: 3,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an7\\pos({x},{y})\\1c&H1F9FE0&\\3c&H0A4A7A&\\bord3\\shad0\\p1}}{circle}{{\\p0}}",
                f"Dialogue: 4,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an5\\pos({x + s // 2},{y + s // 2 + 2})\\fs{int(s * 0.8)}\\1c&H0A4A7A&\\bord0\\shad0}}$"]
    return []


def write_ass(units, path, font="Arial", size=78, y0=1345, dich_size=46):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,5,40,40,0,1
Style: Box,{font},{size},&H00000000,&H00000000,&H0000D8FF,&H0000D8FF,-1,0,0,0,100,100,0,0,3,14,0,5,40,40,0,1
Style: Dich,{font},{dich_size},&H002A2AFF,&H002A2AFF,&H00FFFFFF,&H00000000,-1,0,0,0,100,100,0,0,1,4,0,8,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ts, lines = PP.ts, []
    by_lid = {}
    for u in units:
        by_lid.setdefault(u["lid"], []).append(u)
    for lid, us in by_lid.items():
        y = us[0].get("y", y0)   # vị trí riêng theo lượt (vd. mỗi phần một độ cao)
        fitted = [PP.fit_caption(u["t"].replace("{", "").replace("}", ""), size=size, font=font) for u in us]
        for u, (txt, fs) in zip(us, fitted):
            base = BGR.get(u.get("c") or "white", "FFFFFF")
            body = _paint(txt, u["to"], BGR.get(u["to_mau"], "00D8FF"), base) if u.get("to") else txt
            if u.get("box"):   # cụm nhấn: ô vàng chữ đen
                lines.append(f"Dialogue: 1,{ts(u['s'])},{ts(u['e'])},Box,,0,0,0,,{{\\an5\\pos(540,{y})\\fs{fs}}}{txt}")
            elif u.get("o"):   # cả dòng trên ô màu
                oc = BGR.get(u["o"], "000000")
                lines.append(f"Dialogue: 1,{ts(u['s'])},{ts(u['e'])},Box,,0,0,0,,{{\\an5\\pos(540,{y})\\fs{fs}\\1c&H{base}&\\3c&H{oc}&\\4c&H{oc}&}}{body}")
            else:
                lines.append(f"Dialogue: 1,{ts(u['s'])},{ts(u['e'])},Cap,,0,0,0,,{{\\an5\\pos(540,{y})\\fs{fs}\\1c&H{base}&}}{body}")
            if u.get("icon"):
                rows = txt.split("\\N")
                w = max(PP.text_width(r, fs, font) for r in rows)
                s = int(fs * 0.9)
                ly = y + (len(rows) - 1) * fs * 0.55 - s / 2   # dòng cuối
                lines += _icon(u["icon"], int(540 + min(w, 960) / 2 + 6), int(ly), s, u["s"], u["e"])
        k = 0
        while k < len(us):   # dòng dịch theo từng câu: các dòng liền nhau cùng một câu dịch (cụm nhấn, câu dịch gộp) hiện liền một lần
            d, j = us[k].get("dich"), k
            while j + 1 < len(us) and us[j + 1].get("dich") == d:
                j += 1
            if d:
                dtxt, dfs = PP.fit_caption(d, size=dich_size, min_size=30, max_w=900, max_lines=2, font=font)
                rows = max(txt.count("\\N") + 1 for txt, _ in fitted[k:j + 1])
                dy = int(y + rows * size * 0.55 + 18)
                lines.append(f"Dialogue: 0,{ts(us[k]['s'])},{ts(us[j]['e'])},Dich,,0,0,0,,{{\\an8\\pos(540,{dy})\\fs{dfs}}}{dtxt}")
            k = j + 1
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(head + "\n".join(lines) + "\n")


def _glow_box(times, dur, color, x0, w):
    """Như postprocess.glow_filters nhưng viền chỉ bao một vùng dọc [x0, x0 + w] (px, khung 1080x1920), vd. nửa khung của người dùng ở màn hình chia đôi."""
    fl = []
    for t in times:
        en = f"between(t,{t:.2f},{t + dur:.2f})*lt(mod(t-{t:.2f},0.34),0.2)"
        for th, al in ((46, 0.14), (26, 0.28), (12, 0.55), (5, 0.95)):
            fl.append(f"drawbox=x={x0}:y=0:w={w}:h=ih:color=0x{color}@{al}:t={th}:enable='{en}'")
    return ",".join(fl)


def burn(src, units, out, font="Arial", size=78, y=1345, dich_size=46, glow_box=None, glow_end=False):
    """Đốt phụ đề + viền nháy + tiếng hiệu ứng vào src (1080x1920 đầu ra), giữ tiếng gốc.
    glow_box = (x, rộng) theo tỉ lệ bề ngang: viền sai/đúng chỉ nháy trong vùng đó (mặc định cả khung).
    glow_end = True: viền + tiếng nháy ở cuối câu (0,6 giây trước khi hết lời) thay vì đầu câu, như video mẫu chia đôi."""
    work = tempfile.mkdtemp(prefix="pd_")
    try:
        write_ass(units, os.path.join(work, "subs.ass"), font=font, size=size, y0=y, dich_size=dich_size)
        shutil.copy(src, os.path.join(work, "in.mp4"))
        at = (lambda u: max(u["s"], u["e"] - 0.6)) if glow_end else (lambda u: u["s"])
        wrongs = [at(u) for u in units if u.get("fx") == "wrong"]
        rights = [at(u) for u in units if u.get("fx") == "right"]
        dings = [at(u) for u in units if u.get("fx") == "ding"]
        if glow_box:
            gx, gw = int(round(glow_box[0] * 1080)), int(round(glow_box[1] * 1080))
            glow = lambda ts, d=1.0, col=PP.GLOW: _glow_box(ts, d, col, gx, gw)
        else:
            glow = PP.glow_filters
        glows = [g for g in (glow(dings) if dings else "", glow(wrongs, 1.1, "FF2A2A") if wrongs else "",
                             glow(rights, 1.1, "2EE86A") if rights else "") if g]
        fc = "[0:v]scale=1080:1920:flags=lanczos,fps=30,subtitles=subs.ass" + ("," + ",".join(glows) if glows else "") + "[v]"
        cmd, sfx = ["ffmpeg", "-y", "-i", "in.mp4"], []
        for kind, times, vol in (("ding", dings + rights, 0.9), ("buzz", wrongs, 0.85)):
            if times:
                PP.make_sfx(kind, os.path.join(work, kind + ".wav"))
                sfx += [(t, kind + ".wav", vol) for t in times]
        amap = "0:a"
        if sfx:
            names = sorted({f for _, f, _ in sfx})
            for f in names:
                cmd += ["-i", f]
            parts = [f"[{1 + names.index(f)}:a]asplit=1[s{k}i];[s{k}i]adelay={int(t * 1000)}|{int(t * 1000)},volume={vol}[s{k}]" for k, (t, f, vol) in enumerate(sfx)]
            fc += ";" + ";".join(parts) + ";[0:a]" + "".join(f"[s{k}]" for k in range(len(sfx))) + f"amix=inputs={len(sfx) + 1}:normalize=0:duration=first[a]"
            amap = "[a]"
        print(f"Hiệu ứng: {len(wrongs)} câu sai, {len(rights)} câu đúng, {len(dings)} câu khen; {sum(1 for u in units if u.get('dich'))} dòng dịch")
        PP.run(cmd + ["-filter_complex", fc, "-map", "[v]", "-map", amap, "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "out.mp4"], cwd=work)
        shutil.move(os.path.join(work, "out.mp4"), out)
    finally:
        shutil.rmtree(work, ignore_errors=True)
