"""Tra kho nhân vật / kho bot: in gọn mỗi mã MỘT dòng (mã | giới · tuổi · thị trường | mô tả ngoại hình tiếng Anh).
Dùng thay cho việc mở danh-muc.json (63 KB, phần lớn là link Drive) hay mở từng ảnh.

  python SAMPLE/_chung/kho-nhan-vat/tra-ma.py NU-30-45-AUMY-05 BOT-TALKA-AVA-AUMY-01     tra đúng các mã này
  python SAMPLE/_chung/kho-nhan-vat/tra-ma.py NAM-30-45-LAT                               lọc theo đoạn mã (10 người)
  python SAMPLE/_chung/kho-nhan-vat/tra-ma.py NU-20-30 "hi-vis"                           đoạn mã + chữ trong mô tả
  python SAMPLE/_chung/kho-nhan-vat/tra-ma.py BOT-AIVA INDIA --gon                        chỉ in mã

Mỗi từ là một điều kiện, phải khớp hết (không phân biệt hoa thường): khớp một đoạn của mã, hoặc có trong mô tả.
Mã đầy đủ mà không có trong kho -> in "KHÔNG CÓ TRONG KHO" và thoát với mã lỗi 1.
Cột mô tả (`mo_ta`) chép thẳng vào token NGUOI_<KHOÁ> của biến thể; mã thì ghi vào `refs`."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MA_DAY_DU = re.compile(r"(?:NAM|NU)-\d+-\d+-[A-Z]+-\d+|BOT-[A-Z]+-[A-Z]+-[A-Z]+-\d+")


def danh_muc():
    d = json.load(open(os.path.join(HERE, "danh-muc.json"), encoding="utf-8"))
    return d["nguoi"] + d["bot"]


def dong(r, gon=False):
    """Một dòng gọn cho một mục của danh mục."""
    if gon:
        return r["ma"]
    loai = " · ".join(str(r[k]) for k in ("gioi", "tuoi", "bot", "loai_bot", "thi_truong") if r.get(k))
    return f"{r['ma']} | {loai} | {r.get('mo_ta') or '(chưa có mô tả: mở ảnh anh/' + r['ma'] + '.webp)'}"


def tra(tu):
    """Danh sách mục khớp mọi từ trong `tu`, và danh sách mã đầy đủ không có trong kho."""
    ds = danh_muc()
    co = {r["ma"] for r in ds}
    tu = [t.strip() for t in tu if t.strip()]
    ma = [t.upper() for t in tu if MA_DAY_DU.fullmatch(t.upper())]
    if ma and len(ma) == len(tu):   # chỉ gồm các mã đầy đủ: tra từng mã, giữ thứ tự người dùng ghi
        return [r for m in ma for r in ds if r["ma"] == m], [m for m in ma if m not in co]

    def khop(r, t):
        return t.upper() in r["ma"] or t.lower() in (r.get("mo_ta") or "").lower()
    return [r for r in ds if all(khop(r, t) for t in tu)], []


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    gon = "--gon" in sys.argv
    tu = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not tu:
        sys.exit(__doc__)
    kq, la = tra(tu)
    for r in kq:
        print(dong(r, gon))
    for m in la:
        print(f"{m} | KHÔNG CÓ TRONG KHO")
    if not kq and not la:
        print("Không có mã nào khớp.")
    sys.exit(1 if la else 0)


if __name__ == "__main__":
    main()
