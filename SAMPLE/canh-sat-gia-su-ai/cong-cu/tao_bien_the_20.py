"""Sinh SAMPLE/canh-sat-gia-su-ai/BIEN-THE-20-TAI-XE.json: 20 biến thể chỉ đổi người lái xe (10 nam, 10 nữ; Mexico / Ấn Độ / Mỹ), 10/11/2026.
    .venv\\Scripts\\python.exe -X utf8 SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\tao_bien_the_20.py
Nguồn: anh/20-tai-xe/danh-sach.csv + ảnh tai-xe-XX.png (gen bằng gen_20_tai_xe.py, người dùng đã duyệt).
Quyết định của người dùng (10/11/2026):
  - Tài xế Mỹ: giữ y kịch bản gốc (vẫn "tiếng Anh kém", bé dịch sang tiếng Tây Ban Nha).
  - Bé giống bố/mẹ: Mexico = anh/BE.png; Ấn Độ = be-an.png (câu cảnh 7 bằng tiếng Hindi); Mỹ da trắng = be-trang.png; Mỹ gốc Phi = be-phi.png.
  - Tài xế nữ đi với NAM cảnh sát (canh-sat-nam.png) để cặp nói chuyện khác giới (sổ tay 3.2); tài xế nam giữ nữ cảnh sát gốc.
Mọi thứ khác (xe, đường, robot Aiva, lời thoại phần 2) lấy từ biến thể gốc trong BIEN-THE-CANH-SAT-GIA-SU-AI.json.
Cũng thêm các token giới tính (gioi_tinh.py) còn thiếu vào biến thể gốc."""
import copy
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boi_canh  # noqa: E402   token bối cảnh: biến thể gốc giữ nền sa mạc, xe đỏ

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.normpath(os.path.join(HERE, ".."))
REL = "SAMPLE/canh-sat-gia-su-ai/anh"
GOC = os.path.join(DIR, "BIEN-THE-CANH-SAT-GIA-SU-AI.json")
OUT = os.path.join(DIR, "BIEN-THE-20-TAI-XE.json")

NAM = {"CHA": "father", "CHA_ANH": "he", "CHA_CUA": "his", "CHA_O": "him", "CHA_VN": "bố"}
NU = {"CHA": "mother", "CHA_ANH": "she", "CHA_CUA": "her", "CHA_O": "her", "CHA_VN": "mẹ"}
CS_NU = {"CS_ANH": "she", "CS_CUA": "her", "CS_O": "her"}
CS_NAM = {"CS_ANH": "he", "CS_CUA": "his", "CS_O": "him"}

# nét nhận diện ngắn (chèn vào góc A: mặt nghiêng tài xế ở mép khung)
NET = {
    "01": "slicked-back black hair, thick black moustache", "02": "short curly hair, trimmed full beard",
    "03": "grey-flecked buzz cut, short greying goatee", "04": "black undercut hair, sunglasses pushed up on the head",
    "05": "neat side-parted black hair, thick moustache", "06": "navy-blue turban, long black beard",
    "07": "thick black hair styled up, light stubble", "08": "sandy-blond hair, short sandy beard",
    "09": "short fade haircut, trimmed beard", "10": "receding brown hair, black-framed glasses",
    "11": "long wavy black hair, gold hoop earrings", "12": "brown high ponytail",
    "13": "short black bob, red lipstick", "14": "long black side braid, small red bindi",
    "15": "black low bun, large gold jhumka earrings", "16": "shoulder-length curled black hair, thin round glasses",
    "17": "long straight black hair, tiny nose stud", "18": "shoulder-length blonde hair",
    "19": "natural curly hair in a high puff, silver hoop earrings", "20": "auburn hair in a loose messy bun",
}
DA_DEN = {"09", "19"}   # Mỹ gốc Phi -> bé gốc Phi

GIONG = {
    ("Nam", "Mexico"): "a warm, slightly husky man's voice with a light Mexican accent, hesitant and nervous in English",
    ("Nam", "India"): "a warm man's voice with a clear Indian accent, hesitant and nervous in English",
    ("Nam", "US"): "a warm, slightly husky man's voice, American accent, hesitant and nervous",
    ("Nữ", "Mexico"): "a warm woman's voice with a light Mexican accent, hesitant and nervous in English",
    ("Nữ", "India"): "a warm woman's voice with a clear Indian accent, hesitant and nervous in English",
    ("Nữ", "US"): "a warm woman's voice, American accent, hesitant and nervous",
}

BE = {
    "mexico": (None, None),   # giữ NGUOI_BE + ảnh của biến thể gốc
    "india": ("a stylized 3D-animated Indian girl about five years old, very big dark-brown eyes, long black hair in two braids tied with small red ribbons, a tiny bindi, "
              "a pink ruffled sleeveless dress, sitting in a child car seat with the seat belt on", f"{REL}/20-tai-xe/be-an.png"),
    "trang": ("a stylized 3D-animated white American girl about five years old, very big blue eyes, light-brown hair in two pigtails with colourful clips, light freckles, "
              "a pink ruffled sleeveless dress, sitting in a child car seat with the seat belt on", f"{REL}/20-tai-xe/be-trang.png"),
    "phi": ("a stylized 3D-animated African-American girl about five years old, very big brown eyes, natural curly hair in two puffs with colourful bobbles, "
            "a pink ruffled sleeveless dress, sitting in a child car seat with the seat belt on", f"{REL}/20-tai-xe/be-phi.png"),
}
GIONG_BE_HINDI = "a bright, sweet, confident little girl's voice, clear English with a light Indian accent, also fluent Hindi"
CAU_HINDI = "आपका लाइसेंस और गाड़ी के कागज़।"

CS_NAM_NGUOI = ("a stylized 3D-animated American policeman in his early forties, short dark-brown hair, a clean-shaven square jaw, calm kind brown eyes, light-tan skin, "
                "a navy short-sleeved police uniform with a plain gold badge and shoulder patches without lettering, a black duty belt with a radio")
CS_NAM_GIONG = "a calm, clear, firm man's voice, American accent, polite and professional"
CS_NAM_ANH = f"{REL}/20-tai-xe/canh-sat-nam.png"


def nhin(ai):
    return f"keeps the eyes on the person {ai} is talking to, in the direction the clip's EYE LINE gives, never into the lens"


def main():
    goc_all = json.load(open(GOC, encoding="utf-8"))
    goc = goc_all[0]
    # biến thể gốc: thêm token giới tính (bố + nữ cảnh sát, như cũ)
    for k, v in {**NAM, **CS_NU, "NET_HOC": "curly hair, beard, gold hoop earring", "TIENG_BE": "tiếng Tây Ban Nha", **boi_canh.MAC_DINH}.items():
        goc.setdefault(k, v)
    json.dump(goc_all, open(GOC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    rows = list(csv.DictReader(open(os.path.join(DIR, "anh", "20-tai-xe", "danh-sach.csv"), encoding="utf-8-sig")))
    out = []
    for r in rows:
        m = r["Mã"]
        if not m.isdigit():
            continue
        gt, nc = r["Giới"], r["Nước"]
        nu = gt == "Nữ"
        v = copy.deepcopy(goc)
        v["name"] = f"tai-xe-{m}-{'nu' if nu else 'nam'}-{nc.lower()}"
        v.update(NU if nu else NAM)
        v.update(CS_NAM if nu else CS_NU)
        v["TEN_HOC"] = "the mother" if nu else "the father"
        v["NGUOI_HOC"] = "a stylized 3D-animated " + r["Prompt Muse (NGUOI_HOC)"].removeprefix("a ").removeprefix("an ") + ", the seat belt across the chest"
        v["GIONG_HOC"] = GIONG[(gt, nc)]
        v["NET_HOC"] = NET[m]
        v["NHIN_HOC"] = nhin("she" if nu else "he")
        v["refs"]["NGUOI_HOC"] = [f"{REL}/20-tai-xe/tai-xe-{m}.png"]
        if nu:   # nam cảnh sát
            v["NGUOI_CANHSAT"], v["GIONG_CANHSAT"], v["NHIN_CANHSAT"] = CS_NAM_NGUOI, CS_NAM_GIONG, nhin("he")
            v["refs"]["NGUOI_CANHSAT"] = [CS_NAM_ANH]
        be = "mexico" if nc == "Mexico" else "india" if nc == "India" else ("phi" if m in DA_DEN else "trang")
        if BE[be][0]:
            v["NGUOI_BE"], v["refs"]["NGUOI_BE"] = BE[be][0], [BE[be][1]]
        v["TIENG_BE"] = "tiếng Hindi" if nc == "India" else "tiếng Tây Ban Nha"
        if nc == "India":
            v["GIONG_BE"] = GIONG_BE_HINDI
        for l in v["LUOT"]:
            if nu and l["text"] == "Officer, sorry. He's nervous, and his English isn't very good.":
                l["text"] = "Officer, sorry. She's nervous, and her English isn't very good."
            elif nu and l["text"] == "Does he have his license and registration?":
                l["text"] = "Does she have her license and registration?"
            elif nc == "India" and l["text"] == "Tu licencia y los papeles del carro.":
                l["text"] = CAU_HINDI
        out.append(v)
    assert len(out) == 20, len(out)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for v in out:
        print(v["name"], "|", v["TEN_HOC"], "| CS:", v["CS_ANH"], "| bé:", v["refs"]["NGUOI_BE"][0].rsplit("/", 1)[1], "|", v["TIENG_BE"])


if __name__ == "__main__":
    main()
