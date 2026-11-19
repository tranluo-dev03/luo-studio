"""Hậu kỳ riêng của thể loại taxi-gia-su-ai (Studio gọi khi kịch bản có [HAU KY] loai: taxi-gia-su-ai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu: phần 1 phụ đề ô trắng chữ đen + dòng dịch (tiếng Tây Ban Nha cho câu tiếng Anh, tiếng Anh cho câu tiếng Tây Ban Nha);
phần 2 chữ vàng viền đen, không dịch; "fx"/"icon"/"to" cho cặp "I am Mexico" -> "I am from Mexico".
Cảnh KHÔNG LỜI của phần 1 có "text" = MARKER: vẫn có trong phan.json (đúng số cảnh) nhưng không có dòng phụ đề.
Toàn bộ logic còn lại dùng chung: ../_chung/hau_ky.py (kiểu trong config.json)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

MARKER = "[KHONG LOI]"
_units = hau_ky.PD.units_from_variant


def units_bo_khong_loi(v, scene_of_turn):
    co_chu = [t for t in v.get("LUOT", []) if str(t.get("text", "")).strip()]   # cùng cách đánh số lượt với nhieu_phan / phu_de
    cam = {i for i, t in enumerate(co_chu) if str(t.get("text", "")).strip() == MARKER}
    return [u for u in _units(v, scene_of_turn) if u.get("lid") not in cam]


def _co_devanagari(path):
    try:
        v = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return False
    chu = " ".join(str(t.get(k, "")) for t in v.get("LUOT", []) for k in ("text", "dich"))
    return any("ऀ" <= ch <= "ॿ" for ch in chu)


def _font_hindi():
    """Bản Ấn Độ (13/11/2026): lời/dịch có chữ Devanagari mà Arial không có -> dùng font_devanagari của config (Nirmala UI có cả Latin).
    Bản Mexico không có chữ Devanagari nên giữ Arial như cũ."""
    if "--variant" not in sys.argv or not _co_devanagari(sys.argv[sys.argv.index("--variant") + 1]):
        return
    cfg = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8")).get("phu_de", {})
    font, burn = cfg.get("font_devanagari", "Nirmala UI"), hau_ky.PD.burn

    def burn_hindi(*a, **kw):
        kw["font"] = font
        return burn(*a, **kw)
    hau_ky.PD.burn = burn_hindi


if __name__ == "__main__":
    hau_ky.PD.units_from_variant = units_bo_khong_loi
    _font_hindi()
    hau_ky.main(HERE)
