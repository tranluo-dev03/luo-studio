"""Chuyển file txt (mỗi dòng: gmail|pass|tokena|tokenb) thành file CSV
để import lên Google Sheet.

Hai chế độ:
  - Mặc định: tách mỗi dòng thành 4 cột gmail | pass | tokena | tokenb.
  - --mot-cot: giữ nguyên cả dòng, mỗi dòng txt là 1 hàng, chỉ 1 cột.

Cách dùng:
    python txt-sang-csv.py tai-khoan.txt
    python txt-sang-csv.py tai-khoan.txt --mot-cot
    python txt-sang-csv.py tai-khoan.txt -o ket-qua.csv
    python txt-sang-csv.py tai-khoan.txt --khong-tieu-de

Mặc định file CSV ra cùng tên, cùng thư mục với file txt (đuôi .csv;
chế độ --mot-cot thì thêm hậu tố -1cot.csv để không ghi đè lên bản 4 cột).
"""
import argparse
import csv
import sys
from pathlib import Path

TIEU_DE_4_COT = ["gmail", "pass", "tokena", "tokenb"]
TIEU_DE_1_COT = ["tai_khoan"]
SO_COT = len(TIEU_DE_4_COT)


def doc_dong(duong_dan: Path):
    # utf-8-sig để tự bỏ BOM nếu file txt được lưu từ Notepad
    with duong_dan.open("r", encoding="utf-8-sig", errors="replace") as f:
        for so_dong, dong in enumerate(f, start=1):
            dong = dong.strip()
            if dong:
                yield so_dong, dong


def main():
    # Console Windows mặc định cp1252 không in được tiếng Việt
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Chuyển txt gmail|pass|tokena|tokenb thành CSV")
    ap.add_argument("txt", type=Path, help="file txt đầu vào")
    ap.add_argument("-o", "--out", type=Path, help="file csv đầu ra")
    ap.add_argument("--mot-cot", action="store_true",
                    help="không tách: mỗi dòng txt thành 1 hàng, chỉ 1 cột")
    ap.add_argument("--khong-tieu-de", action="store_true", help="không ghi dòng tiêu đề")
    args = ap.parse_args()

    if not args.txt.is_file():
        sys.exit(f"Không thấy file: {args.txt}")

    if args.out:
        out = args.out
    elif args.mot_cot:
        out = args.txt.with_name(args.txt.stem + "-1cot.csv")
    else:
        out = args.txt.with_suffix(".csv")

    so_ok, dong_loi = 0, []

    # utf-8-sig: Google Sheet và Excel đều đọc đúng tiếng Việt / ký tự đặc biệt
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        if not args.khong_tieu_de:
            w.writerow(TIEU_DE_1_COT if args.mot_cot else TIEU_DE_4_COT)
        for so_dong, dong in doc_dong(args.txt):
            if args.mot_cot:
                w.writerow([dong])
            else:
                # maxsplit=3: nếu tokenb có chứa "|" thì vẫn giữ nguyên trong cột 4
                cot = [x.strip() for x in dong.split("|", SO_COT - 1)]
                if len(cot) < SO_COT:
                    dong_loi.append(so_dong)
                    cot += [""] * (SO_COT - len(cot))  # vẫn ghi, để trống cột thiếu
                w.writerow(cot)
            so_ok += 1

    kieu = "1 cột" if args.mot_cot else "4 cột"
    print(f"Đã ghi {so_ok} dòng ({kieu}) -> {out}")
    if dong_loi:
        print(f"Cảnh báo: {len(dong_loi)} dòng thiếu cột (đã để trống): dòng {', '.join(map(str, dong_loi[:20]))}"
              + (" ..." if len(dong_loi) > 20 else ""))


if __name__ == "__main__":
    main()
