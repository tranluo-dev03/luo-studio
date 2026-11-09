"""Gen riêng của thể loại di-tru-aiva-ai: MỘT dự án, BA phần (gọi điện -> cảnh sát -> ghép 2 lớp ô góc phải) trong cùng một kịch bản.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py.
Riêng thể loại này: ảnh nền phần 3 (base_HOC.png) được căn để đầu nằm bên trái ô AI, kể cả khi Muse vẽ người lệch phải."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
MA = "di-tru-aiva-ai"
O_AI_X, O_AI_DAY = 0.615, 0.332   # mép trái, mép dưới ô AI (khớp "khung DAY" trong kịch bản)
CACH_O, TOC, CAT_MAX = 0.03, 0.35, 0.22   # khoảng trống tới ô; tóc rộng thêm so với mặt; cắt mép trái tối đa


def can_trai(png, span):
    """Đầu chạm ô AI thì cắt bớt mép trái ảnh rồi phóng lại đủ khung, đầu dịch sang trái mà không phải vẽ thêm hình. Trả về True nếu đã sửa ảnh."""
    import cv2
    top, chin, l, r = span
    phai = r + TOC * (r - l)
    dich = O_AI_X - CACH_O
    if phai <= dich or top >= O_AI_DAY:
        return False
    cat = min(CAT_MAX, (phai - dich) / (1 - dich))
    im = cv2.imread(png)
    h, w = im.shape[:2]
    cv2.imwrite(png + ".truoc-can.png", im)
    cv2.imwrite(png, cv2.resize(im[:int(round(h * (1 - cat))), int(round(w * cat)):], (w, h), interpolation=cv2.INTER_LANCZOS4))
    print(f"Ảnh gốc {os.path.basename(png)}: đầu chạm ô AI (tới {phai * 100:.0f}% chiều ngang), cắt mép trái {cat * 100:.0f}%", flush=True)
    return True


def _gan_can_trai():
    """split.py dò mặt ngay sau khi gen ảnh nền: chen bước căn vào đó. Chỉ tác động file của dự án thuộc thể loại này; thể loại khác đi thẳng hàm gốc."""
    SP = NP.SP
    goc = getattr(SP, "_head_span_goc", None) or SP.head_span
    SP._head_span_goc = goc

    def head_span(png):
        span = goc(png)
        try:
            if span and MA in str(png).replace("\\", "/") and os.path.basename(png) == "base_HOC.png" and can_trai(png, span):
                span = goc(png)
        except Exception as e:  # noqa: BLE001 - bước phụ: lỗi thì giữ ảnh như cũ
            print("Bỏ qua bước căn đầu:", e, flush=True)
        return span
    SP.head_span = head_span


def run(vdata, template, out_dir, opts, emit, cancel):
    _gan_can_trai()
    return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
