"""Gen riêng của thể loại chia-tren-duoi-bengali: MỘT dự án, hai phần trong cùng một kịch bản (video mẫu "oder 5").
  Phần 1: Nova và người học đứng đối mặt nhìn nghiêng trên nền xám (cảnh thường, một khung, 4 cảnh).
  Phần 2: Nova ô trên, người học ô dưới (ghép 2 lớp). Vào phần 2 cắt cứng như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: chia-tren-duoi-bengali."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402


def run(vdata, template, out_dir, opts, emit, cancel):
    return NP.run(vdata, template, out_dir, opts, emit, cancel)
