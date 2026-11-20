"""Nhóm jt9nb2 (kịch bản A, goc): 10 bộ bài học × (1 nữ + 1 nam) = 20 biến thể, đúng "1 bản = 2 video = 1 nam + 1 nữ".
Dùng ĐÚNG 20 mã người dùng gửi, mỗi mã một lần, ghép cặp ngẫu nhiên (seed "jt9nb2"). Bộ bài học, mô tả nhân vật, trang phục,
giọng, bối cảnh tiệc lấy chung từ tao_bien_the_nhom_yfma9g.py (sửa một chỗ). Bộ thứ 11 ("Do you eat meat?") không dùng vì người dùng ghi "10 bản".
Chạy: python SAMPLE/8da55fc4-dien-gia-hindi/cong-cu/tao_bien_the_nhom_jt9nb2.py"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tao_bien_the_nhom_yfma9g as Y  # noqa: E402

NHOM = "jt9nb2"


def main():
    r = random.Random(NHOM)
    nu = [m for m in Y.NGUOI if m.startswith("NU-")]
    nam = [m for m in Y.NGUOI if m.startswith("NAM-")]
    r.shuffle(nu)
    r.shuffle(nam)
    out = []
    for k, bai in enumerate(Y.BAI[:10]):
        for j, ma in enumerate((nu[k], nam[k])):
            i = 2 * k + j
            # chỉ số trang phục / bối cảnh: lệch so với nhóm yfma9g để không trùng tổ hợp
            v = Y.bien_the(i + 3, bai, ma)
            gioi = "nu" if ma.startswith("NU-") else "nam"
            v["name"] = f"{NHOM}-{k + 1:02d}{'a' if j == 0 else 'b'}-{bai[0]}-{gioi}{ma.split('-')[1]}-{ma.split('-')[-1]}"
            out.append(v)
    names = [v["name"] for v in out]
    mas = [v["refs"]["NGUOI_HOC"] for v in out]
    assert len(set(names)) == 20 and len(set(mas)) == 20
    with open(os.path.join(ROOT, f"BIEN-THE-NHOM-{NHOM}.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("Đã ghi", f"BIEN-THE-NHOM-{NHOM}.json", len(out), "biến thể")
    for v in out:
        print(" ", v["name"], v["refs"]["NGUOI_HOC"], "|", v["LUOT"][1]["text"])


if __name__ == "__main__":
    main()
