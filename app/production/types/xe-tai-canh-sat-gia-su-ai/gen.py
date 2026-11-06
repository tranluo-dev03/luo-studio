"""Gen riêng của thể loại xe-tai-canh-sat-gia-su-ai (người thật): MỘT dự án, hai phần trong cùng một kịch bản.
  Phần 1: cảnh sát chặn xe tải (cảnh thường, 2 nhân vật, một góc máy, 9 cảnh nối khung).
  Phần 2: tài xế + gia sư AI, ghép 2 lớp (gen RIÊNG video tài xế và video AI rồi ghép; AI trong ô bo góc viền trắng phía trên).
  Vào phần 2: nhoè chuyển động như video mẫu.
Giống canh-sat-gia-su-ai / san-bay-gia-su-ai; toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))


def run(vdata, template, out_dir, opts, emit, cancel):
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
