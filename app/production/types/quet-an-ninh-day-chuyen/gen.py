"""Gen riêng của thể loại quet-an-ninh-day-chuyen (nhân bản từ soi-hanh-ly-gia-su-ai 10/11/2026): MỘT dự án, hai phần trong cùng một kịch bản.
  Phần 1: nhân viên an ninh hỏi hành khách nữ ở cổng dò kim loại vì bà chưa tháo dây chuyền (cảnh thường, 3 góc máy: toàn cảnh, cận hành khách, cận hai người).
  Phần 2: hội thoại hành khách (selfie) + gia sư AI, ghép 2 lớp (robot ở ô bo góc góc trên phải).
  Vào phần 2: nhoè chuyển động như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py (không có biến vali nào bắt buộc trong code: cổng/dây chuyền/khay chỉ là token trong kịch bản).
Studio gọi run(...) khi kịch bản có [HAU KY] loai: quet-an-ninh-day-chuyen."""
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
