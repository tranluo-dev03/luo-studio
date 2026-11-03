"""Gen riêng của thể loại san-bay-gia-su-ai: MỘT dự án, hai phần trong cùng một kịch bản.
  Phần 1: tình huống ở quầy hải quan (cảnh thường, hai người chung khung, cảnh sau nối từ khung cuối cảnh trước).
  Phần 2: hội thoại người dùng + gia sư AI, ghép 2 lớp (gen RIÊNG video người dùng và video AI rồi ghép; AI ở ô góc trên phải).
  Vào phần 2: nhoè chuyển động như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: san-bay-gia-su-ai."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))


def run(vdata, template, out_dir, opts, emit, cancel):
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
