"""Sinh BIEN-THE-TAXI-X0060-40.json: 40 biến thể cho dự án "Taxi - Miguel" (bản Mexico/New York), từ sheet X0060 (16/11/2026).
  runtime\\python.exe SAMPLE\\taxi-gia-su-ai\\cong-cu\\tao_bien_the_x0060.py [--khong-tai]
Mỗi dòng sheet đổi TÀI XẾ (tên, mô tả, giọng theo tuổi, ảnh) và KHÁCH (mô tả, giọng theo giới/tuổi, ảnh); lời thoại, Lucía, sếp, Arjun, robot,
bối cảnh giữ nguyên như biến thể gốc taxi-mexico-goc (tao_bien_the.py). Lời trong sheet là bản dịch tiếng Anh của đúng video gốc.
Khách nữ (dòng 11-20, 31-40): HIS_KHACH/HIM_KHACH = "her" (kịch bản dùng token này cho đại từ của khách, xem GIOI_KHACH trong tao_kich_ban.py).
Ảnh: tải link Google Drive của sheet về SAMPLE/taxi-gia-su-ai/anh/x0060/NN-HOC.<đuôi> và NN-KHACH.<đuôi> (người dùng yêu cầu tải về), refs trỏ file đã tải."""
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import tao_bien_the as TB  # noqa: E402

OUT = os.path.join(HERE, "..", "BIEN-THE-TAXI-X0060-40.json")
ANH_DIR = os.path.join(HERE, "..", "anh", "x0060")
REL = "SAMPLE/taxi-gia-su-ai/anh/x0060"

TX_TRE = "a warm, friendly young Mexican man's voice around 120-145 Hz, Mexican Spanish; his English is slow and broken with a heavy Mexican accent"
TX_TRUNG = "a warm, soft, slightly hoarse man's baritone around 105-130 Hz, Mexican Spanish; his English is slow and broken with a heavy Mexican accent"
TX_GIA = "a gentle, slightly gravelly older man's voice around 95-120 Hz, Mexican Spanish; his English is slow and broken with a heavy Mexican accent"
KH_NAM = "a quick, clipped, impatient man's voice, a clear tenor around 145-175 Hz, fluent American English with a faint Mexican accent, sharper and higher than the driver"
KH_NAM_GIA = "a firm, clipped, impatient mature man's voice around 135-160 Hz, fluent American English with a faint Mexican accent, sharper and higher than the driver"
KH_NU = "a crisp, quick, impatient young woman's voice around 210-240 Hz, fluent American English with a faint Mexican accent, clearly higher than the driver"
KH_NU_GIA = "a crisp, haughty, impatient mature woman's voice around 190-220 Hz, fluent American English with a faint Mexican accent, clearly higher than the driver"


def giong_tx(tuoi):
    return TX_TRE if tuoi < 30 else (TX_TRUNG if tuoi < 46 else TX_GIA)


def giong_kh(nu, tuoi):
    if nu:
        return KH_NU if tuoi < 45 else KH_NU_GIA
    return KH_NAM if tuoi < 40 else KH_NAM_GIA


def tx(tuoi, mo_ta):
    return f"a stylized 3D-animated Mexican man of {tuoi}, warm brown skin, {mo_ta}"


def kh(nu, tuoi, mo_ta):
    return f"a stylized 3D-animated Mexican business{'woman' if nu else 'man'} of {tuoi}, light-brown skin, {mo_ta}"


# (tên tài xế, tuổi, mô tả tài xế, link ảnh | tên khách, nữ?, tuổi, mô tả khách, link ảnh)
D = "https://drive.google.com/file/d/{}/view?usp=drivesdk"
ROWS = [
    ("Carlos Mendoza", 24, "a round face, big round brown eyes, thick eyebrows, a gentle smile, short neat black hair, a thin moustache, a balanced build, a clean white long-sleeved shirt, dark trousers", "1bCyTjP8jRzUNKcfBc9CFcgxuC23L_s4i",
     "Andres Fuentes", False, 34, "a square face and square jaw, sharp brown eyes, short neatly combed black hair, a premium dark-grey suit, a white shirt, a navy-blue tie, a silver watch", "1mTb3D09qPho7bi4Iat_KVjQQBbuT7e_t"),
    ("Miguel Torres", 26, "a square face and square jaw, big brown eyes, thick eyebrows, short curly black hair, a short neat full beard along the jaw, a sturdy slightly heavy build, a clean blue polo shirt, dark trousers", "1ce7stigGvzjz9mX1NBKbIrbhSI4ht6NH",
     "Sebastian Molina", False, 28, "an oval face, big brown eyes, short slicked black hair, a premium navy-blue suit, a white shirt, a blue tie, a luxury watch", "15oJsSMYW4qCgyUXCMS2vupatssT8Te8n"),
    ("Diego Ramirez", 23, "an oval face, big round eyes, neat eyebrows, black hair swept neatly to one side, clean-shaven and youthful, a slim tall build, a clean blue-and-white striped shirt, dark trousers", "1iisthMpF6wSt77r3sAwK8FxljWy7rjl8",
     "Nicolas Ferrer", False, 32, "a long face, brown eyes behind black-framed glasses, short neatly combed black hair, a premium black suit, a white shirt, a luxury watch", "1gtoUidWaBaS0y7_IEp1fUW5lS45xxBtC"),
    ("Javier Morales", 28, "a long face, brown eyes behind black-framed glasses, thick eyebrows, short neat dark-brown hair, a thick moustache, a balanced build, a clean pale-pink shirt, dark trousers", "1e1kwiF1BO_EuryCKD1WLgIqy7k_lfIb4",
     "Santiago Vega", False, 29, "an oval face, big brown eyes, black hair neatly combed back, a premium brown suit, a cream shirt, a yellow tie, a luxury watch", "1eaG2EvpPXNxDcF2rfTHtZtArCtrHsVVS"),
    ("Alejandro Cruz", 25, "a square face and square jaw, big brown eyes, short black hair, a short neat chin beard, a fit balanced build, a clean red polo shirt, dark trousers", "1po-0qQCE2iVz0EtiuVsCiPxNkgwo8aEW",
     "Gael Romero", False, 27, "a square face, big brown eyes, short slicked black hair, a premium navy-blue suit, a white shirt, a silver tie, a luxury watch", "1aohCrfNpd135geLCjnh5R7_8nZurSodL"),
    ("Fernando Ortiz", 27, "a round face, big round eyes, a friendly smile, short curly black hair, a neat moustache, a balanced build, a clean pale-yellow shirt, dark trousers", "1njNgHc6VgMaRjuEvBZgGxBQe7HIib3kI",
     "Bruno Herrera", False, 31, "a long face, sharp brown eyes, short neatly combed black hair, a premium dark-grey suit, a light-blue shirt, a silver tie, a gold watch", "1CRbQyZ2mzU51qRsx9m3Ug4WHUujQHIZh"),
    ("Ricardo Vega", 29, "an oval face, big brown eyes, glossy black hair combed back, a neat full beard, a tall balanced build, a light-brown waistcoat over a white shirt, brown trousers", "1Oyuj478Bgv9upj8wLukyRvQfOMwHz5tf",
     "Axel Mendoza", False, 26, "an oval face, big brown eyes, slicked black hair, a premium black suit, a white shirt, a black bow tie, a luxury watch", "1_C5Uz--HUPV_itEJ7mO3pQHBpYconKdb"),
    ("Eduardo Silva", 24, "a round face, big round brown eyes, neat eyebrows, short neat brown hair, a thin moustache, a balanced build, a clean blue shirt, dark trousers", "1wGRSH8XeSOd4GRuGtNOm-w3_axjhUHqK",
     "Iker Salazar", False, 33, "a square face, brown eyes, short neatly combed black hair, a premium navy-blue suit, a white shirt, a red tie, a luxury watch", "1QfilYkhf3O9bbuIxRwpOjo9mv0wWgdf1"),
    ("Jorge Castillo", 26, "a square face, big brown eyes, short black hair, a short neat beard and moustache, a balanced build, a clean white polo shirt, dark trousers", "1pV6AEcAbpAqIr0IW1zJGHVGL8_fMdJxV",
     "Damian Ortiz", False, 30, "a long face, brown eyes, black hair neatly combed back, a premium dark-brown suit, a white shirt, a purple tie, a luxury watch", "1cldeV_rtbb2qWezfqZ1-RF-WWp9Fg7Bm"),
    ("Luis Herrera", 28, "a round face, brown eyes behind black-framed glasses, thick curly black hair, a thick moustache, a slightly heavy build, a clean white shirt, dark trousers", "1csUACLSpafmzN3J9bHOTPAWJWzNxtz7f",
     "Thiago Luna", False, 28, "an oval face, big brown eyes, short slicked brown hair, a premium light-grey suit, a white shirt, a black tie, a luxury watch", "1ACzbic2Ofi4o0xsqCj3U0UQE3tpLBy8w"),
    ("Andres Luna", 32, "an oval face, big brown eyes, short neat black hair, a neat moustache, a balanced build, a clean purple polo shirt, dark trousers", "1MwtQpru-VZAHXQbj8ulRhY90xBou67N2",
     "Valentina Rios", True, 27, "an oval face, big brown eyes, red lips, long wavy brown hair, a fitted premium red evening dress, luxurious gold jewellery", "1bkpGDjJkgxw1JibN-zghSt8f-AL11fk3"),
    ("Pablo Reyes", 35, "a square face and square jaw, big brown eyes, short dark-brown hair, a short neat full beard, a solid slightly heavy build, a clean white shirt, dark trousers", "1LwVRuBgfkpMjY_6ToE0vsLXQ4gOZ5Guz",
     "Camila Torres", True, 25, "a round face, big brown eyes, long straight glossy black hair, a premium pink silk dress, delicate light jewellery, an elegant white handbag", "1jDAjMHTV4tVmBFON4ubf75jKf9dCJjSN"),
    ("Sergio Navarro", 38, "a long face, deep brown eyes, thick eyebrows, black hair greying at the temples, a neat moustache, a balanced build, a clean navy-blue shirt, dark trousers", "1XBx15YF0qEPvUP44nkN9-VniWvMoZ503",
     "Sofia Herrera", True, 29, "an oval face, big brown eyes, golden-brown hair in a neat high bun, a premium white skirt suit, diamond earrings", "1m8UjLAwI2fH8uAfVFgewqd1KZhfodsnG"),
    ("Oscar Delgado", 33, "a round face, big round brown eyes, short curly black hair, a neat chin beard, a balanced build, a clean orange polo shirt, dark trousers", "1T7Hz-O91bZPIm37mhUCE9V0r3TM2EEKU",
     "Isabella Cruz", True, 26, "a round face, big brown eyes, long voluminous curly black hair, a premium navy-blue dress, delicate silver jewellery", "1UaLIaDVc3l5ZT8dkYLF4okadMOAbP-55"),
    ("Raul Medina", 36, "a square face, brown eyes behind black-framed glasses, short black hair, a thick moustache, a slightly heavy build, a clean grey shirt, dark trousers", "12evDcvMVx8psLlRydhEqiCRbnkhrpWYA",
     "Mariana Vega", True, 30, "an oval face, big brown eyes, long wavy brown hair, a premium purple dress with a silk shawl, luxurious gold jewellery", "1CrLsRvgRggCNqPe5E4Qd62ZOuRPM7nqM"),
    ("Gabriel Soto", 40, "an oval face, big brown eyes, black hair neatly combed back, a neat full beard, a tall balanced build, a clean wine-red shirt, dark trousers", "1soJft9tJELulo0AbOfiCSt56KvLKFNzI",
     "Daniela Morales", True, 28, "a round face, big brown eyes, shoulder-length wavy brown hair, a premium pale-pink pantsuit, a luxurious pink handbag", "1O9vE7829lciMn9wW5fq143MaZOzTYjYW"),
    ("Martin Aguilar", 42, "a square face, kind brown eyes, short neat brown hair, a neat moustache, a balanced build, a clean blue polo shirt, dark trousers", "1wluBdbuWZW9qKGvDJsT4b7Yf8-j4mMQx",
     "Fernanda Silva", True, 24, "an oval face, big brown eyes, long straight glossy black hair, a premium yellow dress, delicate gold jewellery", "1B046wLBoM83aeA_FjKwfyUeWw9fdu79t"),
    ("Felipe Cordero", 45, "a long face, brown eyes, slightly grey eyebrows, black hair with a lot of grey, a short neat beard, a balanced build, a clean white shirt, dark trousers", "1d6b6yfsx7l6LlF-jYK3NVZgiuqGbO9Cr",
     "Lucia Fernandez", True, 31, "a long face, brown eyes, brown hair in a neat low bun, an elegant black dress, a pearl necklace and pearl earrings", "1AznmQcAFPmAA1w8lVo2HOEbyrCG3Jad-"),
    ("Hugo Salazar", 48, "a round face, brown eyes behind brown-framed glasses, short salt-and-pepper grey hair, a neat moustache, a slightly heavy build, a clean blue shirt, dark trousers", "1aBtlhhYRAfAX6znGNpQe7F-LB_ZQMFHW",
     "Regina Castillo", True, 27, "an oval face, big brown eyes, long wavy blonde hair, a premium blue dress, luxurious gold earrings", "1oiHRfqFvQL24yfDYlAD1CX9Rhenq1aiu"),
    ("Ernesto Paredes", 44, "a square face, big brown eyes, short black hair, a neat full beard, a fit balanced build, a clean brown polo shirt, dark trousers", "18QMX29gRKMX7xaQyMyvEHJrMLp7V0XO7",
     "Paola Navarro", True, 29, "a round face, big brown eyes, long wavy brown hair, a premium white dress with a pink blazer, delicate light jewellery", "16pYiqQnWyziCk5VEujpnqmEhOYwUOqOY"),
    ("Arturo Fuentes", 50, "a long face, deep brown eyes, short neat salt-and-pepper hair, a thick moustache, a balanced build, a clean white shirt, dark trousers", "11vTILr_MGnHH80gJ0vWEhLTlsCJRe9pG",
     "Mauricio Leon", False, 45, "a square face, sharp brown eyes, short neatly combed salt-and-pepper hair, a premium black suit, a white shirt, a silver tie, a luxury watch", "1lebqGrS5u-GrmZp43jdynG-WlpqEj2-9"),
    ("Ignacio Ramos", 52, "a square face, brown eyes behind black-framed glasses, short grey hair, a short neat beard, a balanced build, a grey waistcoat over a white shirt, grey trousers", "1XJr_LMkTp7salOtTG2-5KyZZLd_hesvS",
     "Gustavo Paredes", False, 48, "a long face, brown eyes behind black-framed glasses, short black hair with grey streaks, a premium navy-blue suit, a white shirt, a wine-red tie, a gold watch", "1S3sRD3b0wXsoMF0E2TvthrL8W7TsPrZ9"),
    ("Roberto Guzman", 55, "a round kindly face, gentle brown eyes, short grey hair, a neat moustache, a slightly heavy build, a clean light-blue shirt, dark trousers", "1myK5-qW8GC_qAcfc6cKusD6FxGwlSDmi",
     "Federico Ramos", False, 42, "an oval face, brown eyes, short neatly combed black hair, a premium grey suit, a light-blue shirt, a navy-blue tie, a luxury watch", "1OrfjGXsj9SwCLnNBqGQJglrA9Il9CybH"),
    ("Manuel Ortega", 58, "a long face, brown eyes, short white hair, a neat grey full beard, a balanced build, a clean navy-blue polo shirt, dark trousers", "1WL1Fn7RjbH2Iu6H0F313bJ3SQyM9fyOu",
     "Hernan Soto", False, 50, "a square face, brown eyes, short black hair with grey streaks, a premium brown suit, a cream shirt, a yellow tie, a gold watch", "18kZBCFhs0nQgQOBf0mDDxH8PS3ISBSg1"),
    ("Jose Luis Vargas", 60, "a square face, brown eyes behind black-framed glasses, short grey hair, a white moustache, a slightly heavy build, a clean white shirt, dark trousers", "1H0hZTZpHBmy7Y4dAuW-4UGfUkFRsd0Jy",
     "Rafael Duarte", False, 44, "a long face, brown eyes, short black hair, a neat full beard, a premium black suit, a white shirt, a purple tie, a luxury watch", "1-Y0_3U5TAW7JjGK_np-_bSj5Kz_99xgE"),
    ("Francisco Leon", 54, "an oval face, brown eyes, short salt-and-pepper hair, a short neat beard, a balanced build, a clean pale-yellow shirt, dark trousers", "1Rsm7O9bHzf7EMOrCn66o3L0RZ5sh09VY",
     "Esteban Marin", False, 47, "an oval face, brown eyes, short salt-and-pepper hair, a thin moustache, a premium navy-blue suit, a white shirt, a black tie, a luxury watch", "1-6SgBak5ktkuU7cO9AWaIAszPMJffkPN"),
    ("Alberto Campos", 47, "a square face, big brown eyes, black hair with grey streaks, a neat moustache, a fit balanced build, a clean red polo shirt, dark trousers", "1ueWYLM2G9Bb-6ETKrcE2EI3cANU85kYw",
     "Octavio Reyes", False, 52, "a square face, brown eyes behind black-framed glasses, short black hair with grey streaks, a premium dark-grey suit, a white shirt, a red tie, a luxury watch", "15ei9Q7iCkevUawIqW6GsXX9TWGGBGFCv"),
    ("Enrique Mora", 51, "a long face, brown eyes, short greying brown hair, a neat full beard, a balanced build, a clean grey shirt, dark trousers", "1uZdt7tOysDIpFumqg271veICp7XiZLXj",
     "Alfonso Vega", False, 46, "a long face, brown eyes, short neatly combed black hair, a premium black suit, a white shirt, a blue tie, a luxury watch", "1_SmNx6lzkDhXzvdeKViT0Ml4yDUTp1ZX"),
    ("Cesar Dominguez", 57, "a round face, brown eyes, short grey hair, a thick moustache, a slightly heavy build, a clean blue shirt, dark trousers", "1nQQxgcMU4VhObayYBOVMlm_VQOtVD5yY",
     "Julian Campos", False, 43, "an oval face, brown eyes, short black hair, a premium dark-brown suit, a cream shirt, an orange tie, a luxury watch", "1K3Ks00XVBLTCQ5fXRJUtXPOMEcX2AT82"),
    ("Salvador Pena", 62, "a square face, brown eyes behind black-framed glasses, short white hair, a short neat grey beard, a balanced build, a brown waistcoat over a white shirt, brown trousers", "16TJ5mJ2HBPR3P2hB5TMKSwi9NiPSoBgz",
     "Bernardo Luna", False, 49, "a square face, brown eyes, neatly combed black hair with grey streaks, a premium navy-blue suit, a white shirt, a silver tie, a luxury watch", "1imY_lewRX9jva-bgLlqb6kUjzf2ejmRN"),
    ("Guillermo Rios", 65, "a round kindly face, gentle brown eyes, short white hair, a white moustache, a slightly heavy build, a clean white shirt, dark trousers", "1GRFqkajbLu83v1tkgFLYaD_9f5st-Mke",
     "Carmen Ortega", True, 55, "a round face, brown eyes, brown hair in a neat high bun, a premium purple silk dress, luxurious pearl jewellery", "1eNyuC4ziYa12OwmqYMBFBJ9FRk3et4Bn"),
    ("Alfredo Zuniga", 59, "an oval face, brown eyes, short salt-and-pepper hair, a short neat beard, a balanced build, a clean purple polo shirt, dark trousers", "1_oIu1ZQ2r1AeKk15PBAWzAhkwz10GSop",
     "Rosa Mendoza", True, 58, "an oval face, brown eyes, black hair in a neat high bun, a premium wine-red dress, luxurious gold earrings, a black handbag", "1iAz2WgFjcP3APQ8oceMZ_-P8P6r2tneo"),
    ("Tomas Ibarra", 63, "a long face, brown eyes behind black-framed glasses, short white hair, a grey full beard, a balanced build, a clean light-blue shirt, dark trousers", "1bmpONqiAe4K88n9KuZJAwrdto8PvzQRO",
     "Elena Vargas", True, 52, "a long face, brown eyes behind thin-framed glasses, short wavy golden-brown hair, a premium white pantsuit", "15NfoSE9iKzApp71dpA81TVKRnVg2uve4"),
    ("Vicente Solis", 56, "a square face, brown eyes, short salt-and-pepper hair, a neat moustache, a balanced build, a clean wine-red shirt, dark trousers", "1OHBJbNGZzGs0v_FikrLlOroi5vy7aP8i",
     "Margarita Leon", True, 60, "a round face, brown eyes, silver hair in a neat low bun, a premium navy-blue dress, a pearl necklace and pearl earrings", "1zM6l9SbnG5kSBa_yCDn1LbfCr-RN0ovX"),
    ("Rodolfo Marin", 61, "a long face, brown eyes, short grey hair, a short neat grey beard, a balanced build, a grey waistcoat over a white shirt, grey trousers", "1bTNCNLFCMc60Qf5aO09L6FWdmGUtAYpW",
     "Dolores Fuentes", True, 57, "an oval face, brown eyes, long wavy brown hair, a premium deep-pink dress, luxurious gold jewellery", "1TiBXbtBr-9Yej0nxKUoOwaxOnDBTPWI1"),
    ("Emilio Duarte", 54, "a square face, big brown eyes, black hair with grey streaks, a thick moustache, a balanced build, a clean white shirt, dark trousers", "1K7SchMAif67-RXzDVnRiVUuGmufsLi-n",
     "Josefina Ramos", True, 54, "a long face, brown eyes, short neatly curled black hair, a premium black dress with a white blazer, diamond earrings", "1dq0goiEUu6toVqnDKwxlSNlfzZNTo39i"),
    ("Leonardo Ponce", 57, "an oval face, brown eyes, short greying brown hair, a neat chin beard, a balanced build, a clean blue polo shirt, dark trousers", "1ydUjU1-5BOQvBzsFTyi9jSnj4iXi3BRm",
     "Teresa Salazar", True, 62, "a round face, brown eyes, silver hair in a neat high bun, a premium deep-purple dress with a silk shawl, a pearl necklace", "1Q9sPZ6f0yQr-NYFacS8ynyvQdaszwJl7"),
    ("Mateo Espinoza", 60, "a round face, brown eyes behind black-framed glasses, short grey hair, a neat moustache, a slightly heavy build, a clean white shirt, dark trousers", "1T9QGppnvQuDx_wwRlfVTt-cqRgaS-Xc4",
     "Adriana Ponce", True, 50, "an oval face, brown eyes, long wavy brown hair, a premium blue dress, delicate silver jewellery, an elegant white handbag", "1R11MluhoRCgjkYv98Iww5nigwCKeemJh"),
    ("Daniel Cabrera", 62, "a long face, brown eyes, short white hair, a short neat grey beard, a balanced build, a clean blue shirt, dark trousers", "1QnuXjn0uTbdTB-lr4pMYpQ8VOTcd2D4g",
     "Gloria Medina", True, 56, "a round face, brown eyes, voluminous wavy blonde hair, a sparkling premium gold dress, luxurious gold earrings", "17zDlw0msxYjBD7OKlRL20YZZRdaE9DmO"),
    ("Adrian Valdez", 64, "a round kindly face, gentle brown eyes, short white hair, a white moustache, a slightly heavy build, a clean grey polo shirt, dark trousers", "1U54g3zXyzs98dKKF41YqgOus2kRWIP2Z",
     "Patricia Ibarra", True, 59, "an oval face, brown eyes, brown hair in a neat high bun, a premium red dress with a black silk jacket, luxurious gold jewellery", "1dFzntMJfbHa0_1mnfiU7ZznN4Vk6o18J"),
]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def tai(file_id, ten):
    """Tải ảnh Google Drive về anh/x0060/<ten>.<đuôi>; có rồi thì dùng lại. Trả về đường dẫn tương đối từ gốc dự án."""
    for ext in ("png", "jpg", "webp"):
        if os.path.isfile(os.path.join(ANH_DIR, f"{ten}.{ext}")):
            return f"{REL}/{ten}.{ext}"
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as r:
        raw = r.read()
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        ext = "png"
    elif raw[:3] == b"\xff\xd8\xff":
        ext = "jpg"
    elif raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        ext = "webp"
    else:
        raise RuntimeError(f"{ten}: link {file_id} không trả về ảnh ({raw[:60]!r})")
    os.makedirs(ANH_DIR, exist_ok=True)
    open(os.path.join(ANH_DIR, f"{ten}.{ext}"), "wb").write(raw)
    print(f"  tải {ten}.{ext} ({len(raw) // 1024} KB)", flush=True)
    return f"{REL}/{ten}.{ext}"


def main():
    khong_tai = "--khong-tai" in sys.argv
    goc = json.load(open(os.path.join(HERE, "..", "BIEN-THE-TAXI-GIA-SU-AI.json"), encoding="utf-8"))[0]
    out = []
    for i, (ten, tuoi, mo_ta, id_tx, ten_kh, nu, tuoi_kh, mo_ta_kh, id_kh) in enumerate(ROWS, 1):
        v = {k: x for k, x in goc.items() if k not in ("name", "refs")}
        his, him = ("her", "her") if nu else ("his", "him")
        v.update({
            "name": f"taxi-es-{i:02d}-{slug(ten.split()[0])}",
            "TEN_HOC": ten.split()[0],
            "NGUOI_HOC": tx(tuoi, mo_ta),
            "GIONG_HOC": giong_tx(tuoi),
            "NGUOI_KHACH": kh(nu, tuoi_kh, mo_ta_kh),
            "GIONG_KHACH": giong_kh(nu, tuoi_kh),
            "NGHE_KHACH": f"keeps the mouth closed, the phone at {his} ear, looking out of the side window",
            "HIS_KHACH": his,
            "HIM_KHACH": him,
        })
        refs = dict(goc["refs"])
        if khong_tai:
            refs["NGUOI_HOC"], refs["NGUOI_KHACH"] = [D.format(id_tx)], [D.format(id_kh)]
        else:
            refs["NGUOI_HOC"] = [tai(id_tx, f"{i:02d}-HOC")]
            refs["NGUOI_KHACH"] = [tai(id_kh, f"{i:02d}-KHACH")]
        v["refs"] = refs
        out.append(v)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Đã ghi {os.path.normpath(OUT)}: {len(out)} biến thể ({sum(1 for r in ROWS if r[5])} khách nữ), {len(out[0]['LUOT'])} lượt/biến thể")


if __name__ == "__main__":
    main()
