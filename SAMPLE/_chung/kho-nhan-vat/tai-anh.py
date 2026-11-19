"""Tải ảnh của kho nhân vật / kho bot về máy theo danh-muc.json (link Google Drive) -> anh/<MÃ>.<png|jpg|webp>.
Dùng: python SAMPLE/_chung/kho-nhan-vat/tai-anh.py [MÃ ...] [--lai]     (không ghi mã = tải mọi ảnh còn thiếu; --lai = tải lại cả ảnh đã có)
Studio tự gọi phần này khi biến thể ghi một mã mà ảnh chưa có trên máy."""
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ANH = os.path.join(HERE, "anh")
EXTS = (".png", ".jpg", ".webp")


def danh_muc():
    d = json.load(open(os.path.join(HERE, "danh-muc.json"), encoding="utf-8"))
    return {r["ma"]: r for r in d["nguoi"] + d["bot"]}


def duong_dan(ma):
    """Đường dẫn ảnh đã tải của một mã, hoặc None."""
    for e in EXTS:
        p = os.path.join(ANH, ma + e)
        if os.path.isfile(p) and os.path.getsize(p) > 1000:
            return p
    return None


def tai(r, lai=False):
    """Tải ảnh của một mục danh mục; trả về đường dẫn. Lỗi thì ném ValueError."""
    p = duong_dan(r["ma"])
    if p and not lai:
        return p
    url = f"https://drive.google.com/uc?export=download&id={r['drive_id']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as f:
        raw = f.read(30 * 1024 * 1024)
    ext = ".png" if raw[:8] == b"\x89PNG\r\n\x1a\n" else ".jpg" if raw[:3] == b"\xff\xd8\xff" else ".webp" if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP" else ""
    if not ext:
        raise ValueError(f"{r['ma']}: link Drive không trả về ảnh (chưa chia sẻ công khai?)")
    os.makedirs(ANH, exist_ok=True)
    for e in EXTS:
        if e != ext and os.path.exists(os.path.join(ANH, r["ma"] + e)):
            os.remove(os.path.join(ANH, r["ma"] + e))
    p = os.path.join(ANH, r["ma"] + ext)
    with open(p + ".tmp", "wb") as f:
        f.write(raw)
    os.replace(p + ".tmp", p)
    return p


def main():
    dm = danh_muc()
    lai = "--lai" in sys.argv
    ds = [a for a in sys.argv[1:] if not a.startswith("--")] or list(dm)
    la = [m for m in ds if m not in dm]
    if la:
        sys.exit("Mã không có trong danh mục: " + ", ".join(la))

    def one(m):
        for i in range(3):
            try:
                return m, tai(dm[m], lai), ""
            except Exception as e:  # noqa: BLE001
                err = str(e)
        return m, None, err
    ok = loi = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        for m, p, err in ex.map(one, ds):
            if p:
                ok += 1
            else:
                loi += 1
                print("LỖI", m, err)
    print(f"Xong: {ok} ảnh có trên máy, {loi} lỗi. Thư mục: {ANH}")


if __name__ == "__main__":
    main()
