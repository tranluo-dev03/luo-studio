"""Hậu kỳ riêng cho thể loại "Talka bảng từ vựng": KHÔNG phụ đề; bút chỉ chữ + chữ tiếng Anh (pointer.py);
ô bảng ở các cảnh quảng cáo hiện đúng lời robot đang nói (như video gốc). Không gắn logo, không thêm end card.
Dùng: python post.py raw.mp4 --scenes scenes.json --out final.mp4 [--variant bien-the.json] [--config config.json] [--model medium]"""
import argparse, json, os, shutil, subprocess, sys, tempfile

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
    lh = int(cfg["size"] * 1.32)
    x0, w, pad, bw = cfg["x"], cfg["w"], cfg["pad"], cfg.get("border", 9)
    hgt = max(cfg.get("min_h", 0), pad * 2 + lh * len(lines))
    y0 = cfg["y_center"] - hgt // 2
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


def phrase_times(cfg, scenes, raw, model, work):
    """Mốc bắt đầu/kết thúc từng bảng và từng lần viết chữ: nhận dạng giọng theo cảnh; lỗi thì chia theo số ký tự trong cảnh."""
    ph = cfg["phrases"]
    units = [{"t": p["say"], "c": "white", "turn": p["turn"]} for p in ph]
    try:
        al = P.align_by_scene(raw, units, scenes, model)
        if al and all(u.get("ok", True) for u in al):
            return [(u["s"], u["e"]) for u in al]
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
    if a.variant and os.path.exists(a.variant):
        v = json.load(open(a.variant, encoding="utf-8"))
        v = v[0] if isinstance(v, list) else v
        luot = v.get("LUOT", [])
        cfg["pointer"] = bien_the.vocab_items(luot)
        hk = v.get("HAU_KY") or {}   # tuỳ chọn: {"giay": kiểu giấy (pointer.LAYOUTS), "but": kiểu bút (assets/marker-<kiểu>.png)}; bỏ trống = tờ checklist + bút đỏ mẫu
        for it in cfg["pointer"]:
            it["layout"], it["pen"] = hk.get("giay"), hk.get("but")
        cfg["phrases"] = bien_the.ad_phrases(luot, int(cfg.get("ad_from", 6)), cfg.get("red_words", []))
        print(f"Lấy nội dung từ biến thể \"{v.get('name', '')}\": {len(cfg['pointer'])} cặp từ, {len(cfg['phrases'])} ô bảng quảng cáo")
    have = {s["turn"] for s in scenes}
    cfg["phrases"] = [p for p in cfg.get("phrases", []) if p["turn"] in have]   # video chưa đủ cảnh (vd. chạy thử vài cảnh đầu): bỏ bảng chữ của cảnh không có
    work = tempfile.mkdtemp(prefix="talka_pp_")
    try:
        times = phrase_times(cfg, scenes, a.raw, a.model, work)
        src = a.raw
        if cfg.get("pointer") and not a.no_pointer:
            print("Bút chỉ chữ (đo mốc lời nói và vị trí chữ)...")
            try:
                src = pointer.add_pointer(a.raw, scenes, cfg["pointer"], os.path.join(work, "pointed.mp4"),
                                          lambda raw, model, jobs: P.transcribe(raw, model, None, vad=True, jobs=jobs), a.model)
            except Exception as ex:  # noqa: BLE001 - bút lỗi thì vẫn xuất video, chỉ thiếu bút
                print(f"  bút chỉ lỗi ({ex}); bỏ qua bước này")
                src = a.raw
        cmd = ["ffmpeg", "-y", "-i", src]
        fc = "[0:v]scale=1080:1920:flags=lanczos,fps=30[v1]"
        last = "v1"
        nph = len(cfg["phrases"])
        for i, ((s, e), p) in enumerate(zip(times[:nph], cfg["phrases"])):
            if i == 0 or cfg["phrases"][i - 1]["turn"] != p["turn"]:   # ô đầu của mỗi cảnh hiện ngay khi vào cảnh (như video gốc)
                s = min(s, next((x["start"] for x in scenes if x["turn"] == p["turn"]), s) + 0.05)
            if i + 1 < nph and times[i + 1][0] > e:
                e = times[i + 1][0] - 0.3   # như video gốc: ô bảng giữ nguyên đến khi ô kế tiếp hiện (cả khi sang cảnh mới), không có lúc trống
            elif i + 1 == nph:
                e = max(e, max(s["end"] for s in scenes) - 0.3)   # ô cuối giữ đến hết phần robot
            png = f"board{i}.png"
            render_board(p, os.path.join(work, png), cfg["board"])
            cmd += ["-i", png]
            fc += f";[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{s:.2f},{e + 0.3:.2f})'[v{i + 2}]"
            last = f"v{i + 2}"
            print(f"  bảng {i + 1}: {s:6.2f}-{e:6.2f}  " + " / ".join("".join(t for t, _ in segs) for segs in board_lines(p)))
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
