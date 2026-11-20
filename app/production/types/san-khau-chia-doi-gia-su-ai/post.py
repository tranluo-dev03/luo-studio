"""Hậu kỳ riêng của thể loại san-khau-chia-doi-gia-su-ai (Studio gọi khi kịch bản có [HAU KY] loai: san-khau-chia-doi-gia-su-ai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Hai việc, đều bằng code (không giao Muse vẽ chữ):
  1. PHẦN 2 - thẻ từ vựng phía trên khung (như video mẫu "Lurnia"): ô trắng viền xanh + vàng, nhãn hồng câu tiếng Bồ, câu tiếng Anh chữ xanh,
     phiên âm đỏ; từ tiếng Anh đang được đọc tô vàng (cả lúc robot đọc lẫn hai lần diễn giả lặp). Nội dung: HAU_KY.the[] của biến thể
     {"luot": lượt robot, "luot_hoc": lượt diễn giả lặp, "pt", "en", "ipa"}. Mốc từng từ: Whisper theo từng cảnh (đa ngôn ngữ), khớp mờ với lời biến thể.
     Nền thẻ = PNG (PIL); chữ tiếng Anh + ô tô vàng = ASS (cùng phép đo PP.text_width nên khớp nhau).
  2. PHẦN 1 - phụ đề chữ trắng viền đen giữa khung, chia theo câu (dùng _chung/phu_de.py). Phần 2 không có phụ đề vì đã có thẻ.
Không logo, không end card: Thương hiệu của dự án (logo, Video giới thiệu, Outro) làm sau. Tham số: config.json cùng thư mục."""
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = os.path.dirname(HERE)
PROD = os.path.dirname(TYPES)
for _p in (os.path.join(TYPES, "_chung"), PROD, HERE):   # HERE: man_mau.py (python -I không tự thêm thư mục của script vào sys.path)
    if _p not in sys.path:
        sys.path.insert(0, _p)
import phu_de as PD  # noqa: E402
import postprocess as PP  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

W, H = 1080, 1920


def _load_robot_post():
    """Dùng lại words_of_turns / find_word / norm của robot-pho-tieng-long (chỉ đọc, không sửa file đó)."""
    path = os.path.join(TYPES, "robot-pho-tieng-long", "post.py")
    spec = importlib.util.spec_from_file_location("robot_pho_post", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rgb(c):
    return tuple(int(x) for x in c)


def bgr_hex(c):
    r, g, b = rgb(c)
    return f"{b:02X}{g:02X}{r:02X}"


def _font(path, size):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def render_card(cfg, pt, ipa, path, label=True):
    """Nền thẻ (không có chữ tiếng Anh): viền xanh + vàng, nhãn hồng câu tiếng Bồ gạch chân, phiên âm đỏ."""
    from PIL import Image, ImageDraw
    c = cfg["the"]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x, y, w, h = c["x"], c["y"], c["w"], c["h"]
    r = 34
    d.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=rgb(c["vien_ngoai"]) + (255,))
    d.rounded_rectangle((x + 8, y + 8, x + w - 8, y + h - 8), radius=r - 6, fill=rgb(c["vien_trong"]) + (255,))
    d.rounded_rectangle((x + 14, y + 14, x + w - 14, y + h - 14), radius=r - 10, fill=rgb(c["nen"]) + (255,))
    px, py = W / 2, y + c["y_nhan"]
    if label:   # tiếng Ả Rập: nhãn do libass vẽ (PIL ở máy này không có raqm nên không nối chữ / đảo chiều phải-trái được) → label=False
        f = _font(c.get("font_nhan", c["font"]), c["co_nhan"])   # tiếng Hindi: font_nhan = Nirmala UI Bold (Arial không có chữ Devanagari)
        tw = d.textlength(pt, font=f)
        d.rounded_rectangle((px - tw / 2 - 30, py - 30, px + tw / 2 + 30, py + 30), radius=16, fill=rgb(c["nhan_nen"]) + (255,))
        d.text((px, py - 2), pt, font=f, fill=rgb(c["nhan_chu"]) + (255,), anchor="mm")
        d.line((px - tw / 2, py + 22, px + tw / 2, py + 22), fill=rgb(c["nhan_chu"]) + (255,), width=3)
    f = _font(c["font"], c["co_ipa"])
    d.text((px, y + c["y_ipa"]), ipa, font=f, fill=rgb(c["chu_ipa"]) + (255,), anchor="mm")
    im.save(path)


def en_layout(cfg, en):
    """[(từ, x trái, rộng)] của câu tiếng Anh căn giữa khung, đo bằng PP.text_width (cùng thước với ASS)."""
    c = cfg["the"]
    # libass s = chiều cao dòng (ascent+descent ~ 1,117 em của Arial) nên chữ thật nhỏ hơn PIL cùng cỡ: đo bằng PIL ở cỡ fs/1,117 (đo thật 16/11/2026,
    # PP.text_width cộng thêm ~14 px đệm nên ô vàng và khoảng cách từ bị rộng)
    f = _font(c["font"], max(8, round(int(c["co_en"]) / 1.117)))
    words = en.split()
    total = f.getlength(en)
    x0 = W / 2 - total / 2
    out = []
    for i, wd in enumerate(words):
        ww = f.getlength(wd)
        pre = f.getlength(" ".join(words[:i + 1])) - ww
        out.append((wd, x0 + pre, ww))
    return out


def write_ass(cfg, rounds, path, extra=(), nhan_ass=False):
    """rounds: [{en, t0, t1, hl: [(chỉ số từ, s, e)]}] → ASS: chữ tiếng Anh xanh cả thời gian thẻ hiện + ô vàng + chữ đè lên khi từ đang đọc."""
    c = cfg["the"]
    size, font = int(c["co_en"]), c.get("font_ass", "Arial")
    blue, yel = bgr_hex(c["chu_en"]), bgr_hex(c["to_vang"])
    cy = c["y"] + c["y_en"]
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: En,{font},{size},&H00{blue},&H00{blue},&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: Lbl,Arial,{int(c['co_nhan'])},&H00{bgr_hex(c['nhan_chu'])},&H00{bgr_hex(c['nhan_chu'])},&H00{bgr_hex(c['nhan_nen'])},&H00{bgr_hex(c['nhan_nen'])},-1,0,1,0,100,100,0,0,3,22,0,5,0,0,0,1
Style: Cap,{font},64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,5,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ts, lines = PP.ts, []
    for r in rounds:
        if nhan_ass:   # nhãn câu tiếng Ả Rập: ô hồng (BorderStyle 3) + gạch chân, libass nối chữ và xử lý chiều phải-trái
            lines.append(f"Dialogue: 1,{ts(r['t0'])},{ts(r['t1'])},Lbl,,0,0,0,,{{\\an5\\pos({W // 2},{c['y'] + c['y_nhan']})}}{r['pt']}")
        lay = en_layout(cfg, r["en"])
        for wd, x, w in lay:   # chữ xanh thường
            lines.append(f"Dialogue: 2,{ts(r['t0'])},{ts(r['t1'])},En,,0,0,0,,{{\\an4\\pos({x:.0f},{cy})}}{wd}")
        for i, s, e in r["hl"]:   # ô vàng + chữ đè lên
            wd, x, w = lay[i]
            pad, hh = 12, int(size * 1.12)
            rect = f"m 0 0 l {w + 2 * pad:.0f} 0 l {w + 2 * pad:.0f} {hh} l 0 {hh}"
            lines.append(f"Dialogue: 3,{ts(s)},{ts(e)},En,,0,0,0,,{{\\an7\\pos({x - pad:.0f},{cy - hh / 2:.0f})\\1c&H{yel}&\\bord0\\shad0\\p1}}{rect}{{\\p0}}")
            lines.append(f"Dialogue: 4,{ts(s)},{ts(e)},En,,0,0,0,,{{\\an4\\pos({x:.0f},{cy})}}{wd}")
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(head + "\n".join(list(lines) + list(extra)) + "\n")


def gach_lines(R, cfg, v, luot, by_turn, raw, model, work):
    """Cảnh tiệc: mỗi câu xã giao của lượt có "gach" hiện (chữ trắng viền đen) khi được nói, gạch ngang đỏ + dấu X đỏ bên phải, tiếng sai (buzz);
    giữ tới hết cảnh. Trả (dòng ASS, [mốc buzz], [wav])."""
    import re
    c = cfg.get("gach", {})
    idx = [i for i, t in enumerate(luot) if t.get("gach") and i in by_turn]
    if not idx:
        return [], [], []
    tw = R.words_of_turns(raw, luot, [by_turn[i] for i in idx], model, str(c.get("ngon_ngu", "en")))
    size, cx, x_x = int(c.get("co_chu", 62)), int(c.get("x", 450)), int(c.get("x_dau_x", 905))
    y0, dy = int(c.get("y", 1090)), int(c.get("cach_dong", 118))
    f = _font(cfg["the"]["font"], max(8, round(size / 1.117)))
    ts, lines, times = PP.ts, [], []
    for i in idx:
        ws = tw.get(i)
        if not ws:
            continue
        sents = [x.strip() for x in re.findall(r"[^.!?]+[.!?]?", luot[i]["text"]) if x.strip()]
        pos, end = 0, by_turn[i]["end"] + 0.3
        for k, snt in enumerate(sents):
            n = len(snt.split())
            s0 = ws[min(pos, len(ws) - 1)][1]
            pos += n
            y = y0 + k * dy
            txt = snt.rstrip(".!?")
            w = f.getlength(txt)
            lines.append(f"Dialogue: 1,{ts(s0)},{ts(end)},Cap,,0,0,0,,{{\\an5\\pos({cx},{y})\\fs{size}}}{txt}")
            lines.append(f"Dialogue: 2,{ts(s0)},{ts(end)},Cap,,0,0,0,,{{\\an7\\pos({cx - w / 2 - 6:.0f},{y - 4})\\1c&H2A2AFF&\\bord0\\shad0\\p1}}m 0 0 l {w + 12:.0f} 0 l {w + 12:.0f} 8 l 0 8{{\\p0}}")
            lines += PD._icon("x", x_x, y - 28, 56, s0, end)
            times.append(s0)
            print(f"  gạch lượt {i + 1} câu {k + 1}: {txt!r} {s0:.2f}-{end:.2f}s")
    wav = os.path.join(work, "buzz.wav")
    PP.make_sfx("buzz", wav)
    return lines, times, [wav]


def highlights(R, words, en, start_idx=0):
    """Chỉ số từ đọc câu tiếng Anh `en` liên tiếp trong lời `words` của một lượt, từ vị trí start_idx.
    Trả ([(chỉ số từ trong câu, s, e)], vị trí kết thúc) hoặc ([], start_idx) nếu không thấy."""
    ew = en.split()
    out, p = [], start_idx
    for k, wd in enumerate(ew):
        j = R.find_word(words, wd, p)
        if j is None:
            break
        out.append((k, j))
        p = j + 1
    if len(out) < max(1, len(ew) - 1):   # không đủ từ → bỏ
        return [], start_idx
    res = []
    for n, (k, j) in enumerate(out):
        s = words[j][1]
        e = words[out[n + 1][1]][1] if n + 1 < len(out) else words[j][2] + 0.1
        res.append((k, s, max(s + 0.12, e)))
    return res, out[-1][1] + 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--scenes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"))
    a = ap.parse_args(argv)
    cfg = json.load(open(a.config, encoding="utf-8"))
    scenes = json.load(open(a.scenes, encoding="utf-8"))
    v = json.load(open(a.variant, encoding="utf-8"))
    v = v[0] if isinstance(v, list) else v
    luot = [t for t in v.get("LUOT", []) if str(t.get("text", "")).strip()]
    hk = v.get("HAU_KY") or {}
    lang = str(hk.get("ngon_ngu") or "pt")
    model = cfg.get("phu_de", {}).get("whisper", "small")
    if lang == "ar":   # chữ Ả Rập: phụ đề + nhãn thẻ do libass vẽ (Arial có chữ Ả Rập; shaping complex = HarfBuzz + FriBidi)
        cfg.setdefault("phu_de", {})["font"] = "Arial"
        cfg["phu_de"]["shaping"] = "complex"
    if lang == "hi":   # chữ Devanagari: font Nirmala UI + shaping complex (như robot-pho-tieng-long, chia-doi-gia-su-ai-hi)
        cfg["the"]["font_nhan"] = "C:\\Windows\\Fonts\\NirmalaB.ttf"
        cfg.setdefault("phu_de", {})["font"] = "Nirmala UI"
        cfg["phu_de"]["shaping"] = "complex"
    total = PP.duration(a.raw)
    by_turn = {s["turn"]: s for s in scenes if s.get("turn") is not None}
    work = tempfile.mkdtemp(prefix="sk_pp_")
    try:
        cur = os.path.abspath(a.raw)
        # ---- 0a. cân sắc màu các cảnh sân khấu phần 1 (trừ cảnh tiệc) về cảnh 1: engine chỉ kéo mỗi cảnh về khung đầu của chính nó nên cảnh 3–6 mỗi cảnh một tông
        try:
            pj0 = os.path.join(os.path.dirname(os.path.abspath(a.raw)), "phan.json")
            plan0 = json.load(open(pj0, encoding="utf-8")) if os.path.exists(pj0) else []
            p1 = sorted((s for s in plan0 if str(s.get("phan")) == "1" and s.get("turn") in by_turn), key=lambda s: s["scene"])
            stage = [(s["scene"], by_turn[s["turn"]]["start"], by_turn[s["turn"]]["end"]) for s in p1
                     if not (s["turn"] < len(luot) and luot[s["turn"]].get("gach"))]
            if len(stage) >= 2:
                import man_mau as MM
                print(f"Cân màu về cảnh {stage[0][0]} (cảnh sân khấu phần 1, bỏ cảnh tiệc):")
                out_mau = os.path.join(work, "mau.mp4")
                if MM.can_mau(cur, out_mau, stage):
                    cur = out_mau
        except Exception as ex:  # noqa: BLE001
            print(f"CẢNH BÁO: không cân màu về cảnh 1 được ({type(ex).__name__}: {ex}); giữ nguyên màu")
        # ---- 0. cảnh tiệc: chữ gạch ngang + X + tiếng sai
        R = _load_robot_post()
        extra, buzz_t, buzz_w = gach_lines(R, cfg, v, luot, by_turn, a.raw, model, work)
        # ---- 1. thẻ từ vựng (phần 2)
        the = [t for t in hk.get("the", []) if int(t.get("luot", -1)) in by_turn]
        rounds, overlays = [], []
        if the:
            need = sorted({i for t in the for i in (int(t["luot"]), int(t.get("luot_hoc", -1))) if i in by_turn})
            tw = R.words_of_turns(a.raw, luot, [by_turn[i] for i in need], model, lang) if need else {}
            # words_of_turns đánh chỉ số theo vị trí trong `scenes` truyền vào: truyền đủ scenes theo thứ tự lượt để giữ chỉ số lượt
            pre = float(cfg["the"].get("hien_truoc", 0.05))
            for n, t in enumerate(the):
                ti, th = int(t["luot"]), int(t.get("luot_hoc", -1))
                ws = tw.get(ti)
                if not ws:
                    print(f"  CẢNH BÁO: thẻ {n + 1} không có mốc từ của lượt {ti + 1}; bỏ thẻ")
                    continue
                en = str(t["en"])
                after = R.find_word(ws, "الانجليزية" if lang == "ar" else "ingles")   # robot đọc "Em inglês, <en>.": tìm câu tiếng Anh sau chữ "inglês"
                hl, _ = highlights(R, ws, en, (after + 1) if after is not None else 0)
                if th in tw:
                    pos = 0
                    for _rep in range(2):   # diễn giả lặp hai lần
                        h2, pos = highlights(R, tw[th], en, pos)
                        hl += h2
                t0 = max(0.0, ws[0][1] - pre)
                rounds.append({"en": en, "pt": str(t["pt"]), "ipa": str(t.get("ipa", "")), "t0": t0, "t1": 0.0, "hl": hl, "last": by_turn.get(th, by_turn[ti])["end"]})
            for k, r in enumerate(rounds):
                r["t1"] = rounds[k + 1]["t0"] if k + 1 < len(rounds) else min(total, r["last"] + 0.3)
                p = os.path.join(work, f"card{k}.png")
                render_card(cfg, r["pt"], r["ipa"], p, label=(lang != "ar"))
                overlays.append((p, r["t0"], r["t1"]))
                print(f"  thẻ {k + 1} {r['en']!r}: {r['t0']:.2f}-{r['t1']:.2f}s, {len(r['hl'])} lần tô từ")
        if rounds or extra:
            if True:
                write_ass(cfg, rounds, os.path.join(work, "card.ass"), extra, nhan_ass=(lang == "ar"))
                cmd = ["ffmpeg", "-y", "-v", "error", "-i", cur]
                fc = f"[0:v]scale={W}:{H}:flags=lanczos,fps=30[v0]"
                last = "v0"
                for i, (png, s, e) in enumerate(overlays):
                    cmd += ["-i", png]
                    fc += f";[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'[v{i + 1}]"
                    last = f"v{i + 1}"
                fc += f";[{last}]subtitles=card.ass[v]"
                amap = "0:a?"
                if buzz_t:   # tiếng sai (buzz) tại mỗi câu bị gạch
                    n0 = len(overlays) + 1
                    cmd += ["-i", buzz_w[0]]
                    parts = [f"[{n0}:a]asplit={len(buzz_t)}" + "".join(f"[b{k}]" for k in range(len(buzz_t)))]
                    parts += [f"[b{k}]adelay={int(t * 1000)}|{int(t * 1000)},volume=0.85[d{k}]" for k, t in enumerate(buzz_t)]
                    fc += ";" + ";".join(parts) + ";[0:a]" + "".join(f"[d{k}]" for k in range(len(buzz_t))) + f"amix=inputs={len(buzz_t) + 1}:normalize=0:duration=first[a]"
                    amap = "[a]"
                cmd += ["-filter_complex", fc, "-map", "[v]", "-map", amap, "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "cards.mp4"]
                PP.run(cmd, cwd=work)
                cur = os.path.join(work, "cards.mp4")
        # ---- 2. phụ đề phần 1
        pj = os.path.join(os.path.dirname(os.path.abspath(a.raw)), "phan.json")
        plan = json.load(open(pj, encoding="utf-8")) if os.path.exists(pj) else []
        phan_of_turn = {s["turn"]: str(s["phan"]) for s in plan if s.get("turn") is not None}
        gach_i = {i for i, t in enumerate(luot) if t.get("gach")}   # lượt đã có chữ gạch ngang: không phụ đề thường
        scene_of_turn = {s["turn"]: s["scene"] - 1 for s in plan if s.get("turn") is not None and str(s["phan"]) == "1" and s["turn"] not in gach_i}
        if not plan:
            scene_of_turn = {i: i for i in range(len(luot)) if i < len(luot) and not hk.get("the")}
        pdc = cfg.get("phu_de", {})
        if scene_of_turn:
            units = PD.units_from_variant(v, scene_of_turn)
            kieu = pdc.get("kieu_theo_phan", {}).get("1", {})
            PD.apply_styles(units, lambda u: kieu.get(u["who"]) or kieu.get("*"))
            y = pdc.get("y_theo_phan", {}).get("1")
            for u in units:
                if y:
                    u["y"] = int(y)
            print(f"Phụ đề phần 1: {len(units)} dòng, {len(scene_of_turn)} cảnh")
            units = PD.align(a.raw, units, a.scenes, model)
            PD.burn(cur, units, a.out, font=pdc.get("font", "Arial"), size=int(pdc.get("co_chu", 64)), shaping=pdc.get("shaping"))
        else:
            shutil.copy(cur, a.out)
        print("XONG ->", a.out)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
