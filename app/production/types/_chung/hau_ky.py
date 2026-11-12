"""Hậu kỳ phụ đề dùng chung cho thể loại nhiều phần: post.py của thể loại chỉ cần gọi main(<thư mục thể loại>).
Studio gọi: python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json

Đọc <thư mục thể loại>/config.json, mục "phu_de":
  co_chu, co_chu_dich      cỡ chữ phụ đề / dòng dịch (khung 1080x1920)
  y_theo_phan              {"<phần>": độ cao tâm phụ đề}
  kieu_theo_phan           {"<phần>": {"<người nói>" hoặc "*": {"c": màu chữ, "o": màu ô}}}  - lượt không ghi "c"/"o" thì lấy ở đây
  whisper                  model căn lời (mặc định small.en)
  cum_tu_theo_phan         (tuỳ chọn) {"<phần>": N}: chia phụ đề phần đó thành cụm <= N từ (không khai = giữ nguyên câu)
  vien                     (tuỳ chọn) {"x": 0.5, "rong": 0.5, "cuoi_cau": true}: viền sai/đúng chỉ nháy trong vùng dọc đó, ở cuối câu
Cảnh nào thuộc phần nào: phan.json do nhieu_phan.py ghi cạnh raw.mp4 (không có thì lượt thứ i = cảnh thứ i, coi như phần 1).
Không logo, không end card: phần Thương hiệu của dự án làm sau."""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import phu_de as PD  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def chia_cum(units, max_of):
    """Chia mỗi dòng phụ đề đã căn giờ thành cụm <= max_of(u) từ (0 = giữ nguyên); giờ chia theo số ký tự của cụm.
    Như video mẫu phụ đề hiện 1-3 từ một lần (phong-van-pho-malayalam, 11/11/2026). Dòng có dịch / tô từ / viền sai-đúng thì giữ nguyên."""
    out = []
    for u in units:
        n, ws = max_of(u), str(u.get("t", "")).split()
        if n <= 0 or len(ws) <= n or u.get("dich") or u.get("to") or u.get("fx") or "s" not in u or "e" not in u:
            out.append(u)
            continue
        k = -(-len(ws) // n)
        cuts = [round(i * len(ws) / k) for i in range(k + 1)]   # chia đều: 7 từ, tối đa 3 -> 2+3+2 thay vì 3+3+1
        chunks = [" ".join(ws[cuts[i]:cuts[i + 1]]) for i in range(k)]
        total, cur, s0, span = sum(len(c) + 1 for c in chunks), 0, u["s"], u["e"] - u["s"]
        for i, c in enumerate(chunks):
            v = dict(u, t=c)
            v["s"] = s0 + span * cur / total
            cur += len(c) + 1
            v["e"] = s0 + span * cur / total
            if i < len(chunks) - 1:
                v.pop("icon", None)
            out.append(v)
    return out


def main(type_dir, argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--scenes")
    ap.add_argument("--out", required=True)
    ap.add_argument("--variant", required=True)
    a = ap.parse_args(argv)
    cfg = json.load(open(os.path.join(type_dir, "config.json"), encoding="utf-8")).get("phu_de", {})
    v = json.load(open(a.variant, encoding="utf-8"))
    pj = os.path.join(os.path.dirname(os.path.abspath(a.raw)), "phan.json")
    plan = json.load(open(pj, encoding="utf-8")) if os.path.exists(pj) else []
    scene_of_turn = {s["turn"]: s["scene"] - 1 for s in plan if s.get("turn") is not None}
    phan_of_turn = {s["turn"]: str(s["phan"]) for s in plan if s.get("turn") is not None}
    if not plan:   # chạy tay trên video không có phan.json: lượt thứ i = cảnh thứ i
        n = len([t for t in v.get("LUOT", []) if str(t.get("text", "")).strip()])
        scene_of_turn, phan_of_turn = {i: i for i in range(n)}, {i: "1" for i in range(n)}
    units = PD.units_from_variant(v, scene_of_turn)
    kieu, ys = cfg.get("kieu_theo_phan", {}), cfg.get("y_theo_phan", {})

    def style_of(u):
        k = kieu.get(phan_of_turn.get(u["lid"], ""), {})
        return k.get(u["who"]) or k.get("*")
    PD.apply_styles(units, style_of)
    for u in units:
        y = ys.get(phan_of_turn.get(u["lid"], ""))
        if y:
            u["y"] = int(y)
    print(f"Căn {len(units)} dòng phụ đề theo {len(scene_of_turn)} cảnh...")
    units = PD.align(a.raw, units, a.scenes, cfg.get("whisper", "small.en"))
    cum = cfg.get("cum_tu_theo_phan") or {}
    if cum:
        units = chia_cum(units, lambda u: int(cum.get(phan_of_turn.get(u["lid"], ""), 0) or 0))
    vien = cfg.get("vien") or {}   # {"x": 0.5, "rong": 0.5, "cuoi_cau": true}: viền sai/đúng chỉ ở một vùng, nháy ở cuối câu (màn hình chia đôi)
    PD.burn(a.raw, units, a.out, font=cfg.get("font", "Arial"), shaping=cfg.get("shaping"), size=int(cfg.get("co_chu", 78)), dich_size=int(cfg.get("co_chu_dich", 46)),
            glow_box=(float(vien["x"]), float(vien["rong"])) if "x" in vien and "rong" in vien else None, glow_end=bool(vien.get("cuoi_cau")))
    print("XONG ->", a.out)
