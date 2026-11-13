"""Tải ảnh của bộ 20 biến thể Ấn Độ (Hindi) từ link Google Drive trong CSV về anh/20-an-do-hindi/ (12/11/2026).
    .venv\\Scripts\\python.exe -X utf8 SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\tai_anh_20_hindi.py [đường-dẫn-CSV]
CSV nguồn: "20 biến thể IN dừng xe quá tốc độ - Sheet1.csv" (đã chép vào anh/20-an-do-hindi/bang-goc.csv; không cần chạy lại nếu ảnh đã có).
Ra: tai-xe-XX.png (20), canh-sat-nu-N.png / canh-sat-nam-N.png (mỗi ảnh khác nhau một tệp, nhiều biến thể dùng chung), be-trai.png (cả 20 dùng chung).
Ảnh Drive là webp -> đổi sang PNG như các ảnh khác trong thư mục anh/. Thêm vào lúc sinh biến thể: ảnh đi kèm kho mã nên máy khác không cần link Drive."""
import csv
import io
import json
import os
import re
import sys
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(DIR, "anh", "20-an-do-hindi")
CSV_GOC = os.path.join(OUT, "bang-goc.csv")
MAP = os.path.join(OUT, "anh-map.json")   # id Drive -> tên tệp (để lần sau không tải lại)


def doc_bang(path):
    """20 dòng biến thể: dict cột -> giá trị (bảng bắt đầu ở dòng có 'STT biến thể')."""
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    i = next(k for k, r in enumerate(rows) if r and r[0].strip() == "STT biến thể")
    out = []
    for r in rows[i + 1:]:
        if r and r[0].strip().isdigit():
            out.append({"stt": int(r[0]), "kieu": r[1], "tx": r[2], "tx_anh": r[3], "cs": r[4], "cs_anh": r[5], "be": r[6], "be_anh": r[7]})
    assert len(out) == 20, len(out)
    return out


def drive_id(url):
    m = re.search(r"/d/([\w-]{20,})", url)
    assert m, url
    return m.group(1)


def tai(fid):
    u = f"https://drive.usercontent.google.com/download?id={fid}&export=download"
    raw = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
    im = Image.open(io.BytesIO(raw))
    assert im.size[0] > 100, (fid, im.size)
    return im


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else CSV_GOC
    rows = doc_bang(src)
    os.makedirs(OUT, exist_ok=True)
    mp = json.load(open(MAP, encoding="utf-8")) if os.path.exists(MAP) else {}
    dem = {"nu": 0, "nam": 0}

    def luu(fid, ten):
        if fid in mp and os.path.exists(os.path.join(OUT, mp[fid])):
            return mp[fid]
        im = tai(fid)
        im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB").save(os.path.join(OUT, ten), "PNG")
        mp[fid] = ten
        print("tải", ten, im.size)
        return ten

    for r in rows:
        m = f"{r['stt']:02d}"
        luu(drive_id(r["tx_anh"]), f"tai-xe-{m}.png")
        fid = drive_id(r["cs_anh"])
        if fid not in mp:
            g = "nu" if r["cs"].startswith("Nữ") else "nam"
            dem[g] += 1
            luu(fid, f"canh-sat-{g}-{dem[g]}.png")
        if drive_id(r["be_anh"]) not in mp:
            luu(drive_id(r["be_anh"]), "be-trai.png")
    json.dump(mp, open(MAP, "w", encoding="utf-8"), indent=1)
    print("xong:", len(os.listdir(OUT)), "tệp trong", OUT)


if __name__ == "__main__":
    main()
