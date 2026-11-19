"""Gen riêng của thể loại san-khau-chia-doi-gia-su-ai: MỘT dự án, hai phần trong cùng một kịch bản (cùng khuôn du-lich-chia-doi / san-bay).
  Phần 1: diễn giả một mình trên sân khấu (cảnh thường, một khung, 7 cảnh).
  Phần 2: chia đôi dọc, robot gia sư AI nửa trái + diễn giả nửa phải (ghép 2 lớp), 5 vòng đọc từ vựng; thẻ từ vựng do post.py vẽ.
  Vào phần 2: nhoè chuyển động.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: san-khau-chia-doi-gia-su-ai."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))


def run(vdata, template, out_dir, opts, emit, cancel):
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
