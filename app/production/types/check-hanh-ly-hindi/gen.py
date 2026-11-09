"""Gen riêng của thể loại check-hanh-ly-hindi (nhân bản từ soi-hanh-ly-gia-su-ai 08/11/2026): MỘT dự án, hai phần.
  Phần 1: nhân viên an ninh nói chuyện với người phụ nữ Ấn Độ ở máy soi hành lý (cảnh thường, MỘT góc máy đứng yên, 17 cảnh).
  Phần 2: người phụ nữ nhìn ống kính + gia sư AI, ghép 2 lớp (robot ở ô bo góc viền trắng góc trên phải).
  Vào phần 2: nhoè chuyển động như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: check-hanh-ly-hindi."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))

def run(vdata, template, out_dir, opts, emit, cancel):
    # câu dẫn "gửi nguyên văn, không dùng bộ nhớ" cho Muse nay nằm chung ở engine (E.MEDIA_DIRECTIVE, cài đặt muse_directive), áp cho mọi thể loại
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
