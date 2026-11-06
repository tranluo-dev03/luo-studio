"""Gen riêng của thể loại di-tru-gia-su-ai: MỘT dự án, BA phần (gọi điện -> cảnh sát + robot nhỏ -> ghép 2 lớp ô góc phải) trong cùng một kịch bản.
  Phần 1: gọi điện cắt xen (cảnh thường, mỗi cảnh một người, Prompt ảnh mới).
  Phần 2: cảnh sát + Diego + robot nhỏ trên vai (cảnh thường, 3 khung).
  Phần 3: Diego + gia sư AI ghép 2 lớp (ô dọc góc trên phải), vào bằng nhoè.
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
