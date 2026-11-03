"""Hậu kỳ riêng cho thể loại "Talka bảng từ vựng": KHÔNG phụ đề; bút chỉ chữ + chữ tiếng Anh (pointer.py);
ô bảng ở các cảnh quảng cáo hiện đúng lời robot đang nói (như video gốc). Không gắn logo, không thêm end card.
Video Muse toàn nền xanh (biến thể có HAU_KY.bang): xếp lớp từ dưới lên
  cảnh dạy từ:    tờ giấy + chữ tiếng Anh + bút  ->  robot (tách nền xanh)
  cảnh quảng cáo: video nền thành phố (gen bằng AI theo NEN_PHO, lưu nen_pho.mp4 cạnh raw.mp4)  ->  bảng chữ cố định  ->  robot
Robot được phóng/thu và dời cho khớp bố cục video mẫu (config.json "bo_cuc": đỉnh đầu, tâm đầu, bề rộng đầu theo tỉ lệ khung).
Dùng: python post.py raw.mp4 --scenes scenes.json --out final.mp4 [--variant bien-the.json] [--config config.json] [--model medium]"""
import argparse, json, os, shutil, subprocess, sys, tempfile, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [PROD, HERE]
import postprocess as P  # noqa: E402
import pointer  # noqa: E402
import bien_the  # noqa: E402

def board_lines(p):
    """Các dòng của một bảng: [[(chữ, đỏ?)]]. `text` dùng "\n" xuống dòng, *chữ* = tô đỏ (từ khoá); bản cũ `lines` = [[chữ, màu]]."""
    if "text" in p:
        return [[(seg, i % 2 == 1) for i, seg in enumerate(line.split("*")) if seg] for line in p["text"].split("\n")]
    return [[(t, c == "red")] for t, c in p.get("lines", [])]


def render_board(p, path, cfg):
    """Ô bảng như video gốc: nền trắng, viền xanh, bóng đổ, chữ đậm xanh đậm căn giữa, từ khoá đỏ. Ảnh trong suốt 1080x1920."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf" if os.name == "nt" else "DejaVuSans-Bold.ttf", cfg["size"])
    lines = board_lines(p)
    lh = int(cfg["size"] * cfg.get("line", 1.32))
    x0, w, pad, bw = cfg["x"], cfg["w"], cfg["pad"], cfg.get("border", 9)
    if cfg.get("h"):   # ô kích thước cố định như video gốc: chữ nhiều dòng thì thu cỡ chữ cho vừa
        hgt = cfg["h"]
        while lh * len(lines) > hgt - pad * 2 and font.size > 30:
            font = ImageFont.truetype(font.path, font.size - 2)
            lh = int(font.size * cfg.get("line", 1.32))
    else:
        hgt = max(cfg.get("min_h", 0), pad * 2 + lh * len(lines))
    y0 = cfg["y_top"] if "y_top" in cfg else cfg["y_center"] - hgt // 2   # y_top: neo mép trên (bảng không đè lên mặt robot ở cảnh quảng cáo)
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((x0 + 8, y0 + 12, x0 + w + 8, y0 + hgt + 12), fill=(0, 0, 0, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im)
    d.rectangle((x0, y0, x0 + w, y0 + hgt), fill=tuple(cfg.get("border_color", [38, 84, 214])) + (255,))
    d.rectangle((x0 + bw, y0 + bw, x0 + w - bw, y0 + hgt - bw), fill=(255, 255, 255, 255))
    ink, red = tuple(cfg.get("ink", [24, 34, 92])), tuple(cfg.get("red", [222, 36, 40]))
    ty = y0 + (hgt - lh * len(lines)) // 2 + int(lh * 0.1)
    for i, segs in enumerate(lines):
        tw = sum(d.textlength(t, font=font) for t, _ in segs)
        x = x0 + (w - tw) / 2
        for t, is_red in segs:
            d.text((x, ty + i * lh), t, font=font, fill=(red if is_red else ink) + (255,))
            x += d.textlength(t, font=font)
    im.save(path)


def head_top_ratio(raw, t0, t1, size):
    """Đỉnh đầu robot (tỉ lệ chiều cao khung) trong [t0, t1] của video cũ (nền thành phố dính liền): dò khuôn mặt ở vài khung rải đều, lấy mức cao nhất. Không dò được -> None."""
    try:
        import cv2
    except ImportError:
        return None
    w, h = size
    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    tops = []
    for k in range(6):
        f = pointer.frame_at(raw, t0 + (t1 - t0) * (k + 0.5) / 6, w, h)
        if f is None:
            continue
        faces = det.detectMultiScale(cv2.cvtColor(np.ascontiguousarray(f), cv2.COLOR_RGB2GRAY), 1.1, 5, minSize=(int(w * 0.12), int(w * 0.12)))
        if len(faces):
            x, y, fw, fh = max(faces, key=lambda r: r[2] * r[3])
            tops.append((y - 0.25 * fh) / h)   # ô nhận dạng bắt đầu ở khoảng chân tóc/lông mày; đỉnh đầu cao hơn một chút
    return min(tops) if tops else None


def legacy_board_cfg(cfg, raw=None, t0=0.0, t1=0.0, size=None):
    """Ô bảng cho video cũ (robot dính liền nền thành phố, không tách được): mép dưới ô bảng chỉ chạm sát đỉnh đầu robot (đo theo khuôn mặt trong lúc ô hiện), không che mặt."""
    b = dict(cfg["board"], **cfg.get("board_cu", {}))
    top = head_top_ratio(raw, t0, t1, size) if raw and size else None
    if top is not None:
        bottom = int((top + float(cfg.get("bo_cuc", {}).get("che_bang", 0.025))) * 1920)
        b["h"] = max(260, min(int(b.get("h", 560)), bottom - 80))
        b["y_top"] = max(40, bottom - b["h"])
    return b


def phrase_times(cfg, scenes, raw, model, work):
    """Mốc bắt đầu/kết thúc từng bảng và từng lần viết chữ: nhận dạng giọng theo cảnh; lỗi thì chia theo số ký tự trong cảnh."""
    ph = cfg["phrases"]
    units = [{"t": p["say"], "c": "white", "turn": p["turn"]} for p in ph]
    try:
        al = P.align_by_scene(raw, units, scenes, model)
        if al and any(u.get("ok", True) for u in al):
            # câu robot KHÔNG nói (Muse bỏ câu, vd. "Best Language Learning App. Download now.") thì không hiện ô cho câu đó
            for u, p in zip(al, ph):
                if not u.get("ok", True):
                    print(f"  bỏ ô \"{p['say']}\": không nghe thấy robot nói câu này")
            return [(u["s"], u["e"]) if u.get("ok", True) else None for u in al]
    except Exception as ex:  # noqa: BLE001
        print(f"Căn giọng lỗi ({ex}); chia theo số ký tự.")
    out = []
    for turn in sorted({p["turn"] for p in ph}):
        sc = next(s for s in scenes if s["turn"] == turn)
        mine = [p for p in ph if p["turn"] == turn]
        tot = sum(len(p["say"]) for p in mine)
        t = sc["start"]
        for p in mine:
            dt = (sc["end"] - sc["start"]) * len(p["say"]) / tot
            out.append((t, t + dt))
            t += dt
    return out


# ---------------------------------------------------------------- video nền thành phố (cảnh quảng cáo)
def _api():
    import gen_video as G
    studio = os.environ.get("LUO_STUDIO_DATA") or os.path.join(os.path.dirname(PROD), os.pardir, "userdata", "studio")
    try:
        st = json.load(open(os.path.join(studio, "settings.json"), encoding="utf-8"))
    except (OSError, ValueError):
        st = {}
    os.environ.setdefault("MUSE2API_HOME", os.path.join(os.path.dirname(os.path.abspath(studio)), "api"))
    return G, G.Api(os.environ.get("LUO_API_URL") or st.get("api_url") or "http://127.0.0.1:18610", st.get("api_key") or G.read_key())


def city_video(desc, cache, dur=10):
    """Video nền cảnh quảng cáo: gen bằng Muse theo mô tả NEN_PHO, chỉ cảnh vật chuyển động nhẹ (không người, không chữ). Lưu `cache` để lần sau dùng lại."""
    if os.path.exists(cache):
        return cache
    print("Gen video nền cảnh quảng cáo bằng AI (Muse)...")
    G, api = _api()
    prompt = ("SILENT CLIP. A calm cinematic background plate for a vertical video: " + desc + ". "
              "Only very slow, smooth, continuous motion: a gentle slow camera drift, twinkling city lights, slowly drifting clouds. "
              "No person, no character, no robot, no text, no captions, no logos, no signs, no subtitles; one continuous shot with no cuts.")
    neg = "people, characters, text, captions, logos, watermark, cuts, fast camera moves, shaking"
    b = api.generate("video", G.muse_video_prompt(prompt, neg, dur, 0), [], f"nen-pho-{int(time.time())}", duration=dur, timeout=900, log=lambda m: None)
    if G.kind_of(b) != "video":
        raise RuntimeError("Muse không trả về video nền")
    open(cache, "wb").write(b)
    return cache


# ---------------------------------------------------------------- đo và đặt robot (video nền xanh)
def _green(f):
    a = f.astype(np.int16)
    return (a[..., 1] - np.maximum(a[..., 0], a[..., 2])) >= 45


def is_green_bg(raw, t, size):
    """Khung ở giây t có nền xanh không (dải trên cùng phần lớn là xanh lục)."""
    w, h = size
    f = pointer.frame_at(raw, t, w, h)
    return f is not None and _green(f[: int(h * 0.15)]).mean() > 0.8


def measure_robot(raw, t0, t1, size):
    """Đỉnh đầu, tâm đầu, bề rộng đầu (tỉ lệ khung) của robot trên nền xanh trong [t0, t1): trung vị của vài khung rải đều.
    Đầu = dải từ đỉnh đầu xuống thêm 3-13% chiều cao (gồm cả tai nghe), chưa tới vai."""
    w, h = size
    tops, cxs, hws = [], [], []
    for k in range(5):
        f = pointer.frame_at(raw, t0 + (t1 - t0) * (k + 0.5) / 5, w, h)
        if f is None:
            continue
        body = ~_green(f)
        e = max(1, int(w * 0.01))
        body[:, :e] = False
        body[:, -e:] = False
        rows = np.nonzero(body.sum(1) > 0.02 * w)[0]
        if not len(rows):
            continue
        top = rows[0]
        band = [r for r in range(top + int(h * 0.03), min(h, top + int(h * 0.13))) if body[r].any()]
        if not band:
            continue
        spans = [(np.nonzero(body[r])[0][0], np.nonzero(body[r])[0][-1]) for r in band]
        widths = sorted(b - a for a, b in spans)
        tops.append(top / h)
        hws.append(widths[int(len(widths) * 0.9)] / w)
        cxs.append(float(np.median([(a + b) / 2 for a, b in spans])) / w)
    if not tops:
        return None
    return float(np.median(tops)), float(np.median(cxs)), float(np.median(hws))


def place(m, target, top_min=0.0):
    """(tỉ lệ phóng, x, y theo tỉ lệ khung) để robot đo được `m` = (đỉnh, tâm, rộng đầu) khớp `target`.
    Phóng theo bề rộng đầu, nhưng không nhỏ hơn mức để thân robot vẫn chạm đáy khung (không hở đáy)."""
    top, cx, hw = m
    t_top = max(target["top"], top_min)
    s = max(target["head_w"] / max(hw, 1e-3), (1 - t_top) / max(1e-3, 1 - top))
    s = min(1.8, max(0.6, s))
    return s, target["cx"] - cx * s, t_top - top * s


def compose(raw, sections, out, color, dur):
    """Ghép robot (tách nền xanh) lên từng lớp nền. sections = [(video nền, giây bắt đầu, (s, x, y))]; tiếng giữ nguyên."""
    W, H = 1080, 1920
    n = len(sections)
    keyed = [i for i, sec in enumerate(sections) if sec[2] is not None]
    fc = [f"[0:v]scale={W}:{H}:flags=lanczos,fps=30,format=rgba,colorkey=color={color}:similarity=0.22:blend=0.08,despill=type=green:mix=0.5:expand=0,split={len(keyed)}"
          + "".join(f"[r{i}]" for i in keyed)]
    for i, (_, t0, xf) in enumerate(sections):
        fc.append(f"[{i + 1}:v]scale={W}:{H}:flags=lanczos,fps=30,format=rgba[b{i}]")
        if xf is None:   # video cũ: lớp này đã có sẵn robot, không ghép robot tách nền lên
            fc.append(f"[b{i}]copy[c{i}]")
            continue
        s, x, y = xf
        fc.append(f"[r{i}]scale={int(W * s) // 2 * 2}:{int(H * s) // 2 * 2}:flags=lanczos[rs{i}]")
        fc.append(f"[b{i}][rs{i}]overlay={int(x * W)}:{int(y * H)}:format=auto[c{i}]")
    last = "c0"
    for i in range(1, n):
        fc.append(f"[{last}][c{i}]overlay=0:0:enable='gte(t,{sections[i][1]:.3f})'[m{i}]")
        last = f"m{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", raw]
    for path, _, _ in sections:
        cmd += ["-i", path]
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{dur:.3f}", out]
    P.run(cmd)


def ad_raw_back(raw, boards, t0, dur, out):
    """Cảnh quảng cáo của video cũ (nền thành phố dính liền robot): giữ nguyên hình, chỉ đè các ô bảng chữ đúng mốc. Trước t0 để đen."""
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", raw]
    fc = "[0:v]scale=1080:1920:flags=lanczos,fps=30[v0]"
    last = "v0"
    for i, (png, s, e) in enumerate(boards):
        if e <= t0:
            continue
        cmd += ["-i", png]
        k = len(cmd) and (cmd.count("-i") - 1)
        fc += f";[{last}][{k}:v]overlay=0:0:enable='between(t,{max(s, t0):.2f},{e:.2f})'[v{k}]"
        last = f"v{k}"
    cmd += ["-filter_complex", fc, "-map", f"[{last}]", "-an", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p", out]
    P.run(cmd)


def ad_back(city, boards, t0, dur, out):
    """Lớp nền cảnh quảng cáo, dài bằng cả video (trước t0 để đen): video thành phố (chậm lại cho đủ dài) + các ô bảng chữ đúng mốc."""
    cd = P.duration(city) or 10
    slow = max(1.0, (dur - t0) / cd)
    cmd = ["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", city]
    fc = (f"[0:v]setpts={slow:.4f}*PTS,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,"
          f"tpad=start_duration={t0:.3f}:color=black[v0]")
    last = "v0"
    for i, (png, s, e) in enumerate(boards):
        cmd += ["-i", png]
        fc += f";[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[v{i + 1}]"
        last = f"v{i + 1}"
    cmd += ["-filter_complex", fc, "-map", f"[{last}]", "-an", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p", out]
    P.run(cmd)


def layered_main(a, cfg, scenes, paper, boards, v, work, out):
    """Video Muse nền xanh: dựng lớp nền từng phần rồi đặt robot (đã tách nền) lên trên với cỡ/vị trí như video mẫu."""
    w, h, _ = pointer.probe(a.raw)
    dur = P.duration(a.raw)
    lay = cfg["bo_cuc"]
    ad_from = int(cfg.get("ad_from", 6))
    key_until = min((s["start"] for s in scenes if s["turn"] >= ad_from), default=None)
    lesson_end = key_until or dur
    color = pointer.key_color(a.raw, (w, h))
    m = measure_robot(a.raw, 0.3, lesson_end, (w, h))
    if not m:
        raise RuntimeError("không thấy robot trên nền xanh ở cảnh dạy từ")
    xf = place(m, lay["bai"])
    print(f"Robot cảnh dạy từ: đỉnh đầu {m[0] * 100:.0f}%, tâm {m[1] * 100:.0f}%, đầu rộng {m[2] * 100:.0f}% -> phóng {xf[0] * 100:.0f}%, "
          f"đỉnh đầu {lay['bai']['top'] * 100:.1f}%, tâm {lay['bai']['cx'] * 100:.0f}%")
    back = os.path.join(work, "paper.mp4")
    if cfg.get("pointer") and not a.no_pointer:
        print("Bút chỉ chữ (đo mốc lời nói và vị trí chữ)...")
        pointer.add_pointer(a.raw, scenes, cfg["pointer"], back, lambda raw, model, jobs: P.transcribe(raw, model, None, vad=True, jobs=jobs), a.model,
                            paper=paper, key_until=key_until, robot_top_target=lay["bai"]["top"], back_only=True)
    if not os.path.exists(back):   # không có cặp từ nào: giấy trơn
        import giay
        giay.render(paper, (w, h), lay["bai"]["top"])[0].save(os.path.join(work, "paper.png"))
        P.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", "paper.png", "-t", f"{dur:.3f}", "-r", "30", "-pix_fmt", "yuv420p", "paper.mp4"], cwd=work)
    sections = [(back, 0.0, xf)]
    if key_until is not None and key_until < dur - 0.2:
        if not is_green_bg(a.raw, key_until + 0.5, (w, h)):   # video gen bằng kịch bản cũ: cảnh quảng cáo có sẵn nền thành phố dính liền robot -> giữ nguyên, chỉ thêm ô bảng
            print("  CẢNH BÁO: cảnh quảng cáo không phải nền xanh (video gen bằng kịch bản cũ): giữ nguyên robot và nền Muse gen, chỉ thêm ô bảng chữ. Muốn đủ bố cục mới thì nhập lại kịch bản và gen lại cảnh quảng cáo")
            back2 = os.path.join(work, "ad.mp4")
            for i, p in enumerate(cfg["phrases"]):   # vẽ lại ô bảng theo đỉnh đầu robot để không che mặt
                render_board(p, boards[i][0], legacy_board_cfg(cfg, a.raw, boards[i][1], boards[i][2], (w, h)))
            ad_raw_back(a.raw, boards, key_until, dur, back2)
            sections.append((back2, key_until, None))
            compose(a.raw, sections, out, color, dur)
            print("XONG ->", out, f"({P.duration(out):.1f}s)")
            return
        try:
            city = city_video(v.get("NEN_PHO") or "a dense big-city skyline at sunset, softly out of focus",
                              os.path.join(os.path.dirname(os.path.abspath(a.raw)), "nen_pho.mp4"), int(cfg.get("nen_pho_giay", 10)))
        except Exception as ex:  # noqa: BLE001 - không gen được nền: dùng nền chuyển màu tĩnh để vẫn ra video
            print(f"  CẢNH BÁO: không gen được video nền ({ex}); dùng nền chuyển màu")
            city = os.path.join(work, "nen.mp4")
            P.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "gradients=s=1080x1920:c0=0xF08A5D:c1=0x3A2E5C:x0=540:y0=0:x1=540:y1=1920:d=10",
                   "-t", "10", "-pix_fmt", "yuv420p", city])
        back2 = os.path.join(work, "ad.mp4")
        ad_back(city, boards, key_until, dur, back2)
        b = cfg["board"]
        m2 = measure_robot(a.raw, key_until, dur, (w, h)) or m
        # đầu robot chỉ chạm mép dưới bảng (như video mẫu), không che chữ trong bảng
        xf2 = place(m2, lay["qc"], top_min=(b["y_top"] + b["h"]) / 1920 - float(lay.get("che_bang", 0.025)))
        print(f"Robot cảnh quảng cáo: đỉnh đầu {m2[0] * 100:.0f}%, tâm {m2[1] * 100:.0f}%, đầu rộng {m2[2] * 100:.0f}% -> phóng {xf2[0] * 100:.0f}%")
        sections.append((back2, key_until, xf2))
    compose(a.raw, sections, out, color, dur)
    print("XONG ->", out, f"({P.duration(out):.1f}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--scenes", required=True)
    ap.add_argument("--out")
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"))
    ap.add_argument("--model", default="medium")
    ap.add_argument("--no-pointer", action="store_true", help="bỏ bước bút đỏ chỉ chữ")
    ap.add_argument("--variant", help="file JSON biến thể (Studio truyền vào): lấy từ vựng cho bút và lời cho ô bảng quảng cáo từ đây, thay cho mục pointer/phrases trong config")
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.raw)[0] + "_final.mp4"
    cfg = json.load(open(a.config, encoding="utf-8"))
    scenes = json.load(open(a.scenes, encoding="utf-8"))
    paper, v = None, {}
    if a.variant and os.path.exists(a.variant):
        v = json.load(open(a.variant, encoding="utf-8"))
        v = v[0] if isinstance(v, list) else v
        luot = v.get("LUOT", [])
        cfg["pointer"] = bien_the.vocab_items(luot)
        hk = v.get("HAU_KY") or {}   # {"giay": kiểu giấy, "bang": nội dung tờ giấy (xem giay.py), "but": kiểu bút (assets/marker-<kiểu>.png)}
        for it in cfg["pointer"]:
            it["pen"] = hk.get("but")
            if not hk.get("bang"):
                it["layout"] = hk.get("giay")   # video cũ gen kèm tờ giấy trong Muse: dò hàng theo kiểu giấy này
        if hk.get("bang"):   # giấy do hậu kỳ dựng: video Muse chỉ có robot trên nền xanh (cảnh dạy từ); cảnh quảng cáo (từ ad_from) giữ nền thành phố của Muse
            paper = dict(hk["bang"], kieu=hk.get("giay") or "checklist")
        cfg["phrases"] = bien_the.ad_phrases(luot, int(cfg.get("ad_from", 6)), cfg.get("red_words", []))
        print(f"Lấy nội dung từ biến thể \"{v.get('name', '')}\": {len(cfg['pointer'])} cặp từ, {len(cfg['phrases'])} ô bảng quảng cáo")
    have = {s["turn"] for s in scenes}
    cfg["phrases"] = [p for p in cfg.get("phrases", []) if p["turn"] in have]   # video chưa đủ cảnh (vd. chạy thử vài cảnh đầu): bỏ bảng chữ của cảnh không có
    work = tempfile.mkdtemp(prefix="talka_pp_")
    try:
        times = phrase_times(cfg, scenes, a.raw, a.model, work)
        keep = [i for i, t in enumerate(times) if t is not None]
        cfg["phrases"], times = [cfg["phrases"][i] for i in keep], [times[i] for i in keep]
        boards = []
        for i, ((s, e), p) in enumerate(zip(times[:len(cfg["phrases"])], cfg["phrases"])):
            if i == 0 or cfg["phrases"][i - 1]["turn"] != p["turn"]:   # ô đầu của mỗi cảnh hiện ngay khi vào cảnh (như video gốc)
                s = min(s, next((x["start"] for x in scenes if x["turn"] == p["turn"]), s) + 0.05)
            if i + 1 < len(cfg["phrases"]) and times[i + 1][0] > e:
                e = times[i + 1][0] - 0.3   # như video gốc: ô bảng giữ nguyên đến khi ô kế tiếp hiện (cả khi sang cảnh mới), không có lúc trống
            elif i + 1 == len(cfg["phrases"]):
                e = max(e, max(x["end"] for x in scenes) - 0.3)   # ô cuối giữ đến hết phần robot
            png = os.path.join(work, f"board{i}.png")
            render_board(p, png, cfg["board"] if paper else legacy_board_cfg(cfg, a.raw, s, e + 0.3, pointer.probe(a.raw)[:2]))
            boards.append((png, s, e + 0.3))
            print(f"  bảng {i + 1}: {s:6.2f}-{e:6.2f}  " + " / ".join("".join(t for t, _ in segs) for segs in board_lines(p)))
        if paper:   # giấy dựng ở hậu kỳ = video Muse nền xanh: ghép theo lớp (nền -> bảng -> robot)
            return layered_main(a, cfg, scenes, paper, boards, v, work, out)
        src = a.raw
        if cfg.get("pointer") and not a.no_pointer:
            print("Bút chỉ chữ (đo mốc lời nói và vị trí chữ)...")
            ad_from = int(cfg.get("ad_from", 6))
            key_until = min((s["start"] for s in scenes if s["turn"] >= ad_from), default=None)
            try:
                src = pointer.add_pointer(a.raw, scenes, cfg["pointer"], os.path.join(work, "pointed.mp4"),
                                          lambda raw, model, jobs: P.transcribe(raw, model, None, vad=True, jobs=jobs), a.model, paper=paper, key_until=key_until,
                                          robot_top_target=float(cfg.get("robot_top", 0.52)))
            except Exception as ex:  # noqa: BLE001 - bút lỗi thì vẫn xuất video, chỉ thiếu bút
                if paper:   # giấy dựng ở hậu kỳ: bỏ qua thì video ra nền xanh trơn, nên báo lỗi thay vì xuất video hỏng
                    raise
                print(f"  bút chỉ lỗi ({ex}); bỏ qua bước này")
                src = a.raw
        cmd = ["ffmpeg", "-y", "-i", src]
        fc = "[0:v]scale=1080:1920:flags=lanczos,fps=30[v1]"
        last = "v1"
        for i, (png, s, e) in enumerate(boards):   # video cũ (cảnh quảng cáo Muse gen kèm nền thành phố): ô bảng đè lên trên cùng
            cmd += ["-i", png]
            fc += f";[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[v{i + 2}]"
            last = f"v{i + 2}"
        main_mp4 = os.path.join(work, "main.mp4")
        cmd += ["-filter_complex", fc, "-map", f"[{last}]", "-map", "0:a", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "main.mp4"]
        P.run(cmd, cwd=work)
        shutil.copy(main_mp4, out)
        print("XONG ->", out, f"({P.duration(out):.1f}s)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
