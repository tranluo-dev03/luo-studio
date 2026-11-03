"""Gen riêng của thể loại soi-hanh-ly-gia-su-ai: MỘT dự án, hai phần trong cùng một kịch bản (cùng khuôn san-bay-gia-su-ai).
  Phần 1: nhân viên soi chiếu hỏi người mẹ bế con ở máy soi hành lý (cảnh thường, 3 góc máy: toàn cảnh, cận người mẹ, cận hai người).
  Phần 2: hội thoại người mẹ (selfie) + gia sư AI, ghép 2 lớp (robot ở ô bo góc góc trên phải).
  Vào phần 2: nhoè chuyển động như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: soi-hanh-ly-gia-su-ai."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))


def run(vdata, template, out_dir, opts, emit, cancel):
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
