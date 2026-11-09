"""Sinh SAMPLE/xe-tai-canh-sat-gia-su-ai/BIEN-THE-XE-TAI-20-BIEN-THE.json: 20 biến thể theo bảng người dùng gửi 06/11/2026
(anh/20-bien-the/20-bien-the-xe-tai.csv: "20 biến thể Xe tải_Check license - Sheet1.csv").
    .venv\\Scripts\\python.exe SAMPLE\\xe-tai-canh-sat-gia-su-ai\\cong-cu\\tao_bien_the_20.py
Ba kiểu biến thể (cột "Kiểu biến thể"):
  1–5   đổi tài xế (nữ Mexico 41–55) + cảnh BAN ĐÊM; cảnh sát giữ như video mẫu (nam, không ảnh).
  6–10  đổi tài xế (nam Mexico 42–54) + đổi cảnh sát thành NỮ cảnh sát Mỹ (ảnh chung cho 10 biến thể); cảnh hoàng hôn như mẫu.
  11–15 chỉ đổi tài xế (nữ Mexico 25–33); cảnh và cảnh sát như mẫu.
  16–20 đổi tài xế (nam Mexico 25–34) + nữ cảnh sát; cảnh hoàng hôn.
Cặp nhân vật phần 1 luôn khác giới (sổ tay 3.2): tài xế nữ đi với cảnh sát nam, tài xế nam đi với nữ cảnh sát. Lời thoại giữ như tao_bien_the.py
(chỉ "sir" thành "ma'am" khi cảnh sát nữ). Ảnh tham chiếu: link Google Drive trong CSV (Studio tự tải); bản tải về để xem ở anh/20-bien-the/.
Gia sư AI = robot Talka, giọng, nền, lời thoại: dùng chung với tao_bien_the.py."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tao_bien_the import ANH_AI, BIEN_THE, CHUNG, luot  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "BIEN-THE-XE-TAI-20-BIEN-THE.json")
G = "https://drive.google.com/file/d/{}/view?usp=drivesdk"

# cảnh sát nam + xe + đường + cabin của biến thể gốc (video mẫu)
_, _, _, _, _, CS_NAM, GIONG_CS_NAM, XE, DUONG, CABIN, _, _ = BIEN_THE[0]

CS_NU = ("a white American woman in her mid thirties, an oval face, light-blue eyes, a serious steady gaze, blond hair pulled back in a neat low bun at "
         "the nape; a full dark-navy police uniform: short-sleeved navy uniform shirt with plain shoulder patches without lettering and a silver star "
         "badge, a radio on the shoulder, navy trousers, a black duty belt with holster, cuffs and radio; standing straight, confident and authoritative")
GIONG_CS_NU = "a clear, firm American woman's voice around 180–210 Hz, calm and authoritative, polite, slight Southern drawl"
ANH_CS_NU = G.format("1zJ1nJ9T1n7PxUhzLomf8fOHiFBnKGiHs")
NU = {"HE_CANHSAT": "she", "HIS_CANHSAT": "her", "HIM_CANHSAT": "her", "VAI_CANHSAT": "police officer"}

DEM = {
    "SANG_P1": "at night, lit by tall orange sodium street lamps and the warm glow of the truck's cab lights, a deep-blue night sky, both faces clearly lit",
    "SANG_P2": "night inside the cab, a soft warm dome light and the gentle glow of the phone screen clearly lighting the face",
    "NEN_DUONG": ("the shoulder of a wide multi-lane highway at night: tall palm trees silhouetted against a deep-blue night sky, a row of tall orange "
                  "street lamps along the road, far-away car lights standing still in the distance"),
    "NEN_CABIN": ("the inside of the truck cab at night: dark gray seat and door panel lit by a soft warm dome light, the side window on the right "
                  "showing a dark highway with a few distant orange street lamps"),
}


def giong_nu(tuoi, net):
    hz = "200–230" if tuoi < 40 else "185–215"
    return (f"a natural Mexican woman's voice in her {tuoi_txt(tuoi)}, around {hz} Hz, {net}, a clear light Mexican accent in English; "
            "a real person, not an actress")


def giong_nam(tuoi, net):
    hz = "110–140" if tuoi < 40 else "95–125"
    return (f"a natural Mexican man's voice in his {tuoi_txt(tuoi)}, around {hz} Hz, {net}, a clear light Mexican accent in English; "
            "a real person, not an actress")


def tuoi_txt(t):
    d = t // 10 * 10
    k = "early" if t % 10 <= 3 else "mid" if t % 10 <= 6 else "late"
    return f"{k} {'twenties' if d == 20 else 'thirties' if d == 30 else 'forties' if d == 40 else 'fifties'}"


# (số, mã tên, kiểu: "dem" | "cs-nu" | "tai-xe", giới tài xế, tuổi, ngoại hình EN, nét giọng, id ảnh Drive tài xế)
BANG = [
    (1, "dem-ao-cam", "dem", "nu", 48,
     "a Mexican woman, 48 years old, a round face, short straight black hair to the shoulders, medium-dark tan skin, dark circles under tired eyes; "
     "a worn faded orange high-visibility work jacket with gray reflective stripes and small plain chest patches without lettering, faded blue jeans",
     "tired but warm", "1ot2Zf670axrDacs6Lc1HLJ0DkCjOtOyI"),
    (2, "dem-bui-toc", "dem", "nu", 52,
     "a Mexican woman, 52 years old, a long face, black hair with gray strands in a low bun, a small mole on the left cheek; an old gray T-shirt "
     "under a navy-blue work jacket, rough calloused hands",
     "slightly husky and steady", "1GbrFGDiKqLO7I4uxqq-6Gzmg6kkWoDrw"),
    (3, "dem-kinh-den", "dem", "nu", 44,
     "a Mexican woman, 44 years old, a square face with hollow cheeks, short curly brown hair, black-rimmed glasses; a fluorescent yellow "
     "reflective safety vest without lettering over a brown T-shirt, khaki-brown trousers",
     "brisk and practical", "1CKHvNhq0MMlr6UKGL1FJsdcLxTOc07-V"),
    (4, "dem-toc-tet", "dem", "nu", 55,
     "a Mexican woman, 55 years old, an oval sun-weathered face, long black hair in a single braid over one shoulder, a small scar on the chin; "
     "an old red plaid flannel shirt, jeans",
     "warm, slightly raspy", "15ifO-v-jJP0XYpfyEvrRXibn_ZULfWup"),
    (5, "dem-toc-pixie", "dem", "nu", 41,
     "a Mexican woman, 41 years old, a heart-shaped face with freckles on both cheeks, short black pixie-cut hair; a faded denim jacket over an "
     "old white T-shirt, a woven fabric bracelet on the wrist",
     "lively and bright", "1uGsOONBLIHaLgxhPhI_ZygcSu0qjKT9b"),
    (6, "nam-ao-cam", "cs-nu", "nam", 50,
     "a Mexican man, 50 years old, a square face with deep forehead wrinkles, short black buzz-cut hair, a sparse short beard; a fluorescent "
     "orange reflective safety vest without lettering over a dark-gray T-shirt, jeans",
     "deep and calm", "1gaYScHJRCluYMZfTuEQNOekWRo24vGtP"),
    (7, "nam-ria-mep", "cs-nu", "nam", 45,
     "a Mexican man, 45 years old, a long sun-tanned face, black hair combed back with gray strands at the temples, a thick moustache; a gray "
     "T-shirt under a blue work jacket",
     "warm and steady", "1HssqVwLPT81qMLLxW9ETQ4TKvszeqgMi"),
    (8, "nam-hoi-dau", "cs-nu", "nam", 54,
     "a Mexican man, 54 years old, a round face, a bald head with gray hair at the sides, tired deep-set eyes; an old red-and-navy checked "
     "short-sleeved shirt, khaki trousers",
     "slow, slightly gravelly", "1YEOuPFAfpmo0i3foWrAX1i-17cpL2YuD"),
    (9, "nam-toc-xoan", "cs-nu", "nam", 42,
     "a Mexican man, 42 years old, an oval face, ear-length curly brown hair, a short chin beard, a small tattoo on the neck; a denim jacket over "
     "an old black T-shirt",
     "relaxed and friendly", "1PUI1jqTBdWzbwLcHjdkhtcnBE0GavPEA"),
    (10, "nam-gang-tay", "cs-nu", "nam", 47,
     "a Mexican man, 47 years old, an angular face, short black hair, a small scar on the right eyebrow; a fluorescent yellow reflective safety "
     "vest without lettering over a navy work shirt, jeans with torn knees, a black work glove on one hand",
     "firm and plain-spoken", "1sPLjNbyA1OphM1VT9ME3JnbEhj1tQXK5"),
    (11, "nu-duoi-ngua", "tai-xe", "nu", 27,
     "a Mexican woman, 27 years old, a round face with freckles, long brown hair in a high ponytail, a fit sporty build; an olive-green T-shirt, jeans",
     "bright and energetic", "1OzlkwkaUdvC_YprMMfwPHRTdpUeCCc3d"),
    (12, "nu-mai-ngo", "tai-xe", "nu", 31,
     "a Mexican woman, 31 years old, a long face, chin-length straight black hair with blunt bangs, small earrings; a white tank top under an open "
     "blue plaid flannel shirt, cargo trousers",
     "cool and confident", "13yPvHbIE04WNwxslIfR_05q76_wNTFdK"),
    (13, "nu-bui-cao", "tai-xe", "nu", 25,
     "a Mexican woman, 25 years old, a square face, curly brown hair in a high bun with sunglasses pushed up on the head, a small flower tattoo on "
     "the arm; a yellow T-shirt, ripped jeans",
     "cheerful and quick", "1kkgTu02lSPRORasUI8VOeiOYZw28LRMu"),
    (14, "nu-toc-tet-hai-ben", "tai-xe", "nu", 33,
     "a Mexican woman, 33 years old, an oval face, long black hair in two braids, a red bandana around the neck; a red T-shirt, khaki trousers, "
     "a free-spirited look",
     "warm and easygoing", "1XpywTN7_pq9j9CAnDVj2xj8Lp1UpSw5e"),
    (15, "nu-toc-bob", "tai-xe", "nu", 29,
     "a Mexican woman, 29 years old, a heart-shaped face with a big bright smile, honey-blond-brown bob haircut; a denim shirt, long denim shorts, "
     "a big wristwatch",
     "sunny and upbeat", "1S0su94tIujqsM4jqedNfuEsjjY8T-qVE"),
    (16, "nam-mu-nguoc", "cs-nu", "nam", 26,
     "a Mexican man, 26 years old, a long face, black undercut hair under a black baseball cap worn backwards, a sparse chin beard; a white "
     "T-shirt, jeans",
     "casual and lively", "13irONSHa0hgzfZCi0vf3bfsW2e1TYR-_"),
    (17, "nam-xam-tay", "cs-nu", "nam", 30,
     "a Mexican man, 30 years old, a square face, short brown hair, a thin moustache, tattoos on the arms; a gray tank top, green cargo trousers",
     "easygoing, slightly low", "1rpGsZvPsLPXMkFMbLDUyDbchZm3nWuWP"),
    (18, "nam-kinh-tron", "cs-nu", "nam", 28,
     "a Mexican man, 28 years old, a round face with a wide toothy smile, short curly black hair, round thin-rimmed glasses; a red plaid flannel "
     "shirt, jeans",
     "friendly and cheerful", "1LGQuxNlGDkVQH8olbwoW40Xwx2mepf0I"),
    (19, "nam-duoi-ngua", "cs-nu", "nam", 34,
     "a Mexican man, 34 years old, an oval face, long brown hair in a low ponytail, a short full beard, a dark bandana around the neck; a black "
     "T-shirt under a denim jacket",
     "calm and mellow", "1NQWpZVH_vL00Gle1aCbu2xErtmHGsgdM"),
    (20, "nam-crew-cut", "cs-nu", "nam", 25,
     "a Mexican man, 25 years old, an angular face, honey-blond-brown crew-cut hair; a navy-blue T-shirt, khaki trousers, a pair of tan leather "
     "work gloves tucked into the belt",
     "young and earnest", "1sx_QqmAdxziLL_oF1D8vTaET3nqAKSTg"),
]


def main():
    res = []
    for so, ma, kieu, gioi, tuoi, nguoi, net, anh in BANG:
        v = {"name": f"bien-the-{so:02d}-{ma}", **CHUNG,
             "TEN_HOC": "the truck driver", "NGUOI_HOC": nguoi,
             "GIONG_HOC": (giong_nu if gioi == "nu" else giong_nam)(tuoi, net),
             "TEN_CANHSAT": "the officer", "NGUOI_CANHSAT": CS_NAM, "GIONG_CANHSAT": GIONG_CS_NAM,
             "XE": XE, "NEN_DUONG": DUONG, "NEN_CABIN": CABIN}
        refs = {"NGUOI_HOC": [G.format(anh)], "NGUOI_DAY": [ANH_AI]}
        if kieu == "dem":
            v.update(DEM)
        if kieu == "cs-nu":
            v.update(NU, NGUOI_CANHSAT=CS_NU, GIONG_CANHSAT=GIONG_CS_NU)
            refs["NGUOI_CANHSAT"] = [ANH_CS_NU]
        assert (gioi == "nu") == (kieu != "cs-nu"), f"{so}: cặp nhân vật phải khác giới"
        v["refs"] = refs
        v["LUOT"] = luot("ma'am" if kieu == "cs-nu" else "sir")
        res.append(v)
    json.dump(res, open(OUT, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.normpath(OUT), f"({len(res)} biến thể, {len(res[0]['LUOT'])} lượt)")


if __name__ == "__main__":
    main()
