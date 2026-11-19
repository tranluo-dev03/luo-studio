"""Gen ảnh tham chiếu PHOTOREAL (người thật, nền xanh lục phẳng) cho phong-van-pho-hindi bằng Muse.
Lý do có file riêng: SAMPLE/_chung/gen-anh-nhan-vat.py cố định phong cách hoạt hình Pixar, còn video mẫu là ảnh người thật; không sửa file dùng chung,
chỉ đổi hằng số STYLE trong bộ nhớ rồi gọi lại main() của nó.
Chạy:  runtime\python.exe SAMPLE\phong-van-pho-hindi\cong-cu\gen_anh.py [PV V1 V2 V3]  (mô tả lấy từ tao_bien_the.py)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path[:0] = [HERE, os.path.join(ROOT, "SAMPLE", "_chung")]
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("gen_anh_nv", os.path.join(ROOT, "SAMPLE", "_chung", "gen-anh-nhan-vat.py"))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
import tao_bien_the as TB  # noqa: E402

M.STYLE = ("photorealistic photograph, natural soft daylight on the person, realistic skin texture and fabric detail, sharp focus on the face, "
           "a real ordinary person, not a model, not cartoon, not a 3D render")
M.NEG = "text, letters, logo, watermark, extra people, distorted face, cartoon, 3D render, illustration"

if __name__ == "__main__":
    keys = [a.upper() for a in sys.argv[1:]] or list(TB.ANH_MO_TA)
    argv = ["gen_anh", "--ra", os.path.join(ROOT, "SAMPLE", "phong-van-pho-hindi", "anh")]
    for k in keys:
        argv += ["--nv", k, TB.ANH_MO_TA[k]]
    sys.argv = argv
    M.main()
