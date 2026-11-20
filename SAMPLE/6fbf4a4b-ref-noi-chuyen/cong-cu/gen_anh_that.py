"""Gen ảnh tham chiếu NGƯỜI THẬT (ảnh chụp thật, không hoạt hình) bằng cách chạy gen-anh-nhan-vat.py với STYLE/NEG ghi đè (không sửa mã dùng chung).
  python gen_anh_that.py --ra <thư mục> --nv KHOA "<mô tả>" [--bc KHOA "<mô tả>"]"""
import importlib.util
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
spec = importlib.util.spec_from_file_location("gan", os.path.join(ROOT, "SAMPLE", "_chung", "gen-anh-nhan-vat.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.STYLE = "PHOTOREALISTIC real photograph of a real person, shot on a DSLR camera, natural skin texture and pores, real fabric, natural light; absolutely NOT a cartoon, NOT animated, NOT 3D-render, NOT illustration"
m.NEG = "text, letters, logo, watermark, extra people, distorted face, cartoon, animation, 3D render, illustration, painting, plastic skin"
m.main()
