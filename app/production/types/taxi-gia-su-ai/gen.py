"""Gen riêng của thể loại taxi-gia-su-ai: MỘT dự án, HAI phần (phần 1 cảnh thường có cảnh KHÔNG LỜI -> phần 2 ghép 2 lớp ô robot phía trên).
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py.
Riêng thể loại này: nhieu_phan bỏ qua lượt "text" rỗng (coi là không có lượt), nên cảnh không lời của phần 1 được đánh dấu bằng MARKER trong biến thể.
Ngay trước khi engine chạy một phần, MARKER được đổi thành chuỗi rỗng -> engine tạo clip câm như chế độ cảnh thường (tiem-thit-tieng-anh).
Chỉ lượt có đúng MARKER bị đổi, nên thể loại khác chạy chung tiến trình không bị ảnh hưởng."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
MARKER = "[KHONG LOI]"


def _bo_marker(v):
    luot = v.get("LUOT")
    if not isinstance(luot, list) or not any(str(t.get("text", "")).strip() == MARKER for t in luot if isinstance(t, dict)):
        return v
    v = dict(v)
    v["LUOT"] = [dict(t, text="") if isinstance(t, dict) and str(t.get("text", "")).strip() == MARKER else t for t in luot]
    return v


def _gan_khong_loi():
    E = NP.E
    goc = getattr(E, "_run_variant_goc_taxi", None) or E.run_variant
    E._run_variant_goc_taxi = goc

    def run_variant(vdata, template, out_dir, opts, *a, **kw):
        # Chỉ đổi khi nhieu_phan gọi cho MỘT phần (opts["_part"]). Hàm này thay engine.run_variant cho cả tiến trình Studio,
        # nên lệnh gọi gốc của Studio (cả dự án) cũng đi qua đây: đổi ở đó thì nhieu_phan.plan mất lượt câm, lượt sau dồn lên
        # (11/11/2026, lần chạy 3: cảnh 7 câm bị điền câu của quản lý).
        if isinstance(opts, dict) and opts.get("_part"):
            vdata = _bo_marker(vdata)
        return goc(vdata, template, out_dir, opts, *a, **kw)
    E.run_variant = run_variant


def run(vdata, template, out_dir, opts, emit, cancel):
    _gan_khong_loi()
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
