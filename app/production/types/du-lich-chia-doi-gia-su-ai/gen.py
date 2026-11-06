"""Gen riêng của thể loại du-lich-chia-doi-gia-su-ai: MỘT dự án, hai phần trong cùng một kịch bản (cùng khuôn san-bay / soi-hanh-ly).
  Phần 1: Carla và robot ở Machu Picchu (cảnh thường, một khung, 3 cảnh).
  Phần 2: gọi video với gia sư AI, ghép 2 lớp chia đôi dọc (robot nửa trái, Carla nửa phải, như chia-doi-gia-su-ai).
  Vào phần 2: nhoè chuyển động như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: du-lich-chia-doi-gia-su-ai."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))


def run(vdata, template, out_dir, opts, emit, cancel):
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
