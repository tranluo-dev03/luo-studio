"""Tải ảnh biến thể từ 4 file CSV của người dùng (link Google Drive) về anh/<bo>/.
    python tai_anh_csv.py
Ảnh nhân vật: anh/<bo>/bien-the-NN.<đuôi>; ảnh robot: anh/<bo>/robot-NN.<đuôi>. Đã có thì bỏ qua."""
import csv, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
ANH = os.path.join(HERE, "..", "anh")
G = r"G:\.shortcut-targets-by-id\18RHYCy9H0VKucU3z-IsYEnXWIepl_N4K\NHIPTY\MC Nunca"
BO = {  # bộ: (tên file csv, thư mục anh)
    "brazil": ("X0056+X0070_MC Nunca_40 biến thể Nhân vật Brazil.xlsx - 40 biến thể.csv", "brazil"),
    "hindi": ("X0057+X0071_MC Nunca_20 biến thể Nhân vật HINDI.xlsx - 20 biến thể.csv", "hindi"),
    "brazil-robot": ("X0058+X0072_MC Nunca_40 biến thể Nhân vật Brazil + Robot.xlsx - 40 biến thể.csv", "brazil-robot"),
    "mexico": ("X0059+X0073_MC Nunca_40 biến thể Nhân vật Mexico.xlsx - 40 biến thể.csv", "mexico"),
    # X0104 (lời Ả Rập) và X0105 (lời Hindi) dùng CHUNG 20 nhân vật (cùng link Drive; X0105 đánh số 21–40) → cùng một thư mục ảnh "arab".
    # Hai file này nằm ngay trong NHIPTY (không trong "MC Nunca"); phần tử 3,4 = (thư mục gốc, số cần trừ khỏi STT).
    "arab": ("X0104_MC Nunca_10 biến thể nhân vật HINDI_Arab.xlsx - 20 biến thể.csv", "arab", os.path.dirname(G), 0),
    "hindi2": ("X0105_MC Nunca_20 biến thể nhân vật HINDI.xlsx - 20 biến thể.csv", "arab", os.path.dirname(G), 20),
}

def doc(bo):
    """Trả về danh sách dòng biến thể: (stt, mô tả, link nhân vật, mô tả robot|None, link robot|None)."""
    e = BO[bo]
    base, off = (e[2], e[3]) if len(e) > 2 else (G, 0)
    rows = list(csv.reader(open(os.path.join(base, e[0]), encoding="utf-8-sig")))
    out = []
    for r in rows:
        if r and re.match(r"Biến thể \d+$", r[0].strip()):
            out.append((int(r[0].split()[-1]) - off, r[2], r[3], r[4] if len(r) > 5 else None, r[5] if len(r) > 5 else None))
    return out

def id_of(link):
    return re.search(r"/d/([\w-]+)", link).group(1)

def tai(job):
    dest_base, link = job
    for e in (".webp", ".png", ".jpg"):
        if os.path.isfile(dest_base + e) and os.path.getsize(dest_base + e) > 1000:
            return dest_base + e, "co"
    data = urllib.request.urlopen(urllib.request.Request("https://drive.google.com/uc?export=download&id=" + id_of(link), headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
    e = ".webp" if data[:4] == b"RIFF" else ".png" if data[:4] == b"\x89PNG" else ".jpg" if data[:2] == b"\xff\xd8" else None
    if not e:
        raise RuntimeError(f"không phải ảnh: {link} ({data[:60]!r})")
    os.makedirs(os.path.dirname(dest_base), exist_ok=True)
    open(dest_base + e, "wb").write(data)
    return dest_base + e, "moi"

def main():
    jobs = []
    for bo, e in BO.items():
        d = e[1]
        for stt, _, link, _, rlink in doc(bo):
            jobs.append((os.path.join(ANH, d, f"bien-the-{stt:02d}"), link))
            if rlink:
                jobs.append((os.path.join(ANH, d, f"robot-{stt:02d}"), rlink))
    moi = 0; loi = []
    with ThreadPoolExecutor(6) as ex:
        for j, f in zip(jobs, ex.map(lambda j: _an(j), jobs)):
            if isinstance(f, Exception): loi.append((j[0], f))
            elif f[1] == "moi": moi += 1
    print(f"{len(jobs)} ảnh, tải mới {moi}, lỗi {len(loi)}")
    for x in loi: print("LỖI", x)

def _an(j):
    try: return tai(j)
    except Exception as e: return e

if __name__ == "__main__":
    main()
