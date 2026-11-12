"""Sinh BIEN-THE-20-PHONG-VAN-PHO-TAY-BAN-NHA.json: 20 biến thể theo bảng người dùng "20 biến thể ES Interview - Sheet1.csv" (12/11/2026).
Mỗi biến thể đổi NGƯỜI BÁN (nam/nữ, tuổi, nghề), PHÓNG VIÊN (luôn KHÁC GIỚI người bán, ảnh riêng từng biến thể) và BỐI CẢNH (ảnh không người).
Giữ nguyên: lời thoại (tiếng Tây Ban Nha, Mexico), robot Aiva, góc máy, bố cục 2 phần.
Ảnh: anh/bt20/nv<NN>.jpg (người bán), pv<NN>.jpg (phóng viên), nen<NN>.jpg (bối cảnh), tải từ link Drive trong csv (nguon/20-bien-the-ES-Interview.csv).
  --tai-anh: tải lại ảnh từ link Drive (mặc định dùng ảnh đã có).
Chạy:  runtime\\python.exe SAMPLE\\phong-van-pho-tay-ban-nha\\cong-cu\\tao_20_bien_the.py [--tai-anh]"""
import csv
import io
import json
import os
import re
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ANH = "SAMPLE/phong-van-pho-tay-ban-nha/anh/"
BT = ANH + "bt20/"
CSV = os.path.join(HERE, "..", "nguon", "20-bien-the-ES-Interview.csv")
OUT = os.path.join(HERE, "..", "BIEN-THE-20-PHONG-VAN-PHO-TAY-BAN-NHA.json")

# Lời thoại: bảng của người dùng. Sửa so với bảng (ghi rõ trong README):
#  - hai câu liền của cùng một người gộp thành một lượt (<= 20 từ): bảng 2+3 (người bán), 8+9 và 14+15 (robot)
#  - "Soy de Kannur" (Ấn Độ) -> "Soy de Puebla" (hợp bối cảnh Mexico)
#  - "como nativa" -> theo giới người bán (nativa / nativo)
def luot(nat):
    return [
        ("pv", 1, "¿Cómo aprendiste a hablar inglés tan bien?", "friendly, curious"),
        ("hoc", 1, "Hace un mes solo escuchaba inglés en la tele. Ahora ya hablo con fluidez todos los días.", "proud"),
        ("pv", 1, "¿Y cuál es tu secreto, en serio?", "amazed, friendly"),
        ("hoc", 1, "Empecé a practicar inglés desde el primer día.", "confident"),
        ("pv", 1, "¿De dónde eres tú exactamente?", "curious, playful"),
        ("hoc", 1, "Soy de Puebla, ven y te muestro cómo.", "cheerful, inviting"),
        ("day", 2, f"En solo un mes hablarás como {nat}. ¿Puedes repetir esta frase en inglés?", "warm, encouraging"),
        ("hoc", 2, "Sí, claro, puedo intentarlo ahora mismo.", "hesitant, willing"),
        ("day", 2, "¡Perfecto! Tu pronunciación mejora cada día.", "delighted"),
        ("hoc", 2, "¿Y esto no es muy caro, verdad?", "worried"),
        ("day", 2, "No, practica inglés gratis, sin límites.", "reassuring"),
        ("day", 2, "Corrijo tu gramática y pronunciación al instante. Hablarás con confianza, como con un profesor real.", "warm, confident"),
    ]


M, F = "m", "f"
BAR = "{He} works with bare hands."
# n, nombre, sexo, edad, oficio, aspecto, ropa, puesto, tarea1, tarea2, manos en reposo, lugar | PV: sexo, edad, aspecto (pelo), ropa
NV = [
    (1, "Carlos Hernández", M, 24, "street taco seller", "short neat black hair, light stubble, a friendly smiling face, brown skin",
     "a clean white T-shirt, a clean black apron, blue jeans, clean sneakers",
     "a street taco cart with a steel griddle, a stack of corn tortillas, bowls of grilled meat, chopped onion and cilantro, and jars of salsa",
     "keeps turning pieces of meat on the griddle with a metal spatula", "sets the spatula back on the griddle", "his hands resting on the edge of the cart",
     "a sunny Mexican street in the daytime, houses painted yellow and orange, a few signboards that are blurred and unreadable",
     F, 28, "long brown hair tied in a low ponytail, a bright professional face", "a clean white shirt, black trousers, flat shoes"),
    (2, "Miguel Torres", M, 27, "street grilled-corn (elote) seller", "short curly black hair, a cheerful slightly puzzled face, brown skin",
     "a clean navy-blue polo shirt, a clean apron, black jeans, clean sneakers",
     "a street cart with a charcoal grill of corn cobs, a bowl of mayonnaise, grated white cheese, chili powder and lime wedges",
     "keeps turning a corn cob on the grill", "puts the corn cob back on the grill", "his hands resting on the edge of the cart",
     "a Mexican street in the daytime, houses painted blue and white, a small market far behind",
     F, 26, "long straight black hair, a friendly face", "a light-pink blouse, white trousers, flat shoes"),
    (3, "Diego Ramírez", M, 22, "street ice-cream seller", "short black hair lightly styled, a gentle innocent smile, light-brown skin",
     "a clean white shirt, a clean apron, beige khaki trousers, clean white sneakers",
     "a street ice-cream cart with a freezer with round lids, tubs of ice cream, a scoop and a stack of cones",
     "keeps scooping ice cream into a cone and smoothing it", "puts the scoop back in the tub", "his hands resting on the edge of the cart",
     "a Mexican street in the daytime, houses painted pink and yellow, green trees on both sides of the street",
     F, 30, "short brown hair at shoulder length, a confident face", "a light-blue shirt, black trousers, flat shoes"),
    (4, "Alejandro Morales", M, 26, "street soft-drink (agua fresca) seller", "short black hair, a serious, slightly tense face, brown skin",
     "a clean grey T-shirt, a clean apron, blue jeans, clean sneakers",
     "a street cart with large glass jars of colourful agua fresca, a stack of plastic cups, a long ladle and a bucket of ice",
     "keeps stirring a jar of agua fresca with the long ladle", "puts the ladle back in the jar", "his hands resting on the edge of the cart",
     "a Mexican street in the daytime, houses painted green and white, a few signboards that are blurred and unreadable",
     F, 27, "black hair in a low bun, a gentle face", "a white blouse, a long navy-blue skirt, flat shoes"),
    (5, "Jorge Castillo", M, 28, "street fruit seller", "short black hair, a short beard, a cheerful, smiling face, brown skin",
     "a clean white shirt, a clean apron, grey trousers, clean sneakers",
     "a street fruit stand with trays of cut mango, watermelon, pineapple and jicama, clear cups, lime and chili",
     "keeps arranging cut fruit in a clear cup", "puts a fruit cup back on the tray", "his hands resting on the edge of the stand",
     "a Mexican street fruit market in the daytime, colourful fruit stalls, houses painted orange and yellow",
     F, 29, "long brown hair, a smiling face", "a pale-yellow T-shirt, blue jeans, white sneakers"),
    (6, "María Fernanda López", F, 23, "street flower seller", "long black hair tied low, a pretty shy gentle smile, light-brown skin",
     "a clean white blouse, a clean apron, a long skirt with a light flower pattern, clean sandals",
     "a street flower stand with buckets of roses, sunflowers and carnations",
     "keeps arranging flowers into a bunch", "puts the bunch back in the bucket", "her hands resting on the edge of the flower stand",
     "a Mexican street flower market in the daytime, colourful flower stalls, houses painted pink and purple",
     M, 29, "short black hair, a friendly professional face", "a clean white shirt, grey trousers, leather shoes"),
    (7, "Lucía Herrera", F, 25, "street coffee seller", "long wavy brown hair, a fresh, confident face, brown skin",
     "a clean white shirt, a clean black apron, blue jeans, clean white sneakers",
     "a street coffee cart with a big steel coffee urn, rows of paper cups, a basket of sweet bread and a few jars of sugar",
     "keeps pouring coffee into a paper cup", "sets the coffee pot back on the cart", "her hands resting on the edge of the cart",
     "a Mexican street in the morning, houses painted brown and yellow, a few signboards that are blurred and unreadable",
     M, 27, "short black hair, a cheerful face", "a green polo shirt, beige khaki trousers, sneakers"),
    (8, "Valeria Sánchez", F, 21, "street churro seller", "long straight black hair, an innocent face with big eyes, light-brown skin",
     "a clean white T-shirt, a clean apron, light-blue jeans, white sneakers",
     "a street churro cart with a fryer, golden churros on a tray, sugar and small cups of chocolate",
     "keeps rolling a churro in cinnamon sugar", "puts the churro back on the tray", "her hands resting on the edge of the cart",
     "a Mexican street in the daytime, houses painted red and yellow, a small market far behind",
     M, 31, "short black hair, a short beard, a calm face", "a light-blue shirt, black trousers, leather shoes"),
    (9, "Camila Reyes", F, 27, "street snack seller", "black hair in a neat high bun, a cheerful, often smiling face, brown skin",
     "a pink blouse, a clean apron, black trousers, clean sandals",
     "a street snack cart with bags of chips, fried snacks, fruit cups and jars of sauce",
     "keeps filling a bag with snacks", "puts a bag of snacks back on the shelf", "her hands resting on the edge of the cart",
     "a Mexican street in the daytime, houses painted blue and orange, a few signboards that are blurred and unreadable",
     M, 28, "short black hair, a friendly face", "a clean white shirt, blue jeans, sneakers"),
    (10, "Sofía Mendoza", F, 24, "street sweet-bread (pan dulce) seller", "long brown hair, a gentle face with a soft smile, light-brown skin",
     "a pale-yellow shirt, a clean apron, white trousers, flat shoes",
     "a street bread cart with trays of pan dulce: conchas, cuernitos and orejas",
     "keeps arranging pieces of sweet bread on the tray", "puts a piece of bread back on the tray", "her hands resting on the edge of the cart",
     "a Mexican street in the morning, houses painted yellow and white",
     M, 30, "short black hair, a confident face", "a white polo shirt, grey trousers, leather shoes"),
    (11, "Ricardo Vega", M, 48, "street food seller", "black hair with grey strands, a short beard, a calm, slightly tired face, brown skin",
     "a clean white shirt, a clean apron, grey trousers, leather shoes",
     "a street-food stall with steel trays of food, a small gas burner with a pan and a stack of plates",
     "keeps stirring the pan on the burner", "puts the spoon back in the pan", "his hands resting on the edge of the stall",
     "a Mexican street in the daytime, houses painted brown and red, a small market far behind",
     F, 35, "long black hair, a professional, confident face", "a white blouse, black trousers, flat shoes"),
    (12, "Fernando Ortiz", M, 55, "street grilled-corn (elote) seller", "short black hair with grey, a gently lined, resigned face, dark-brown skin",
     "a grey T-shirt, a clean apron, blue jeans, clean sneakers",
     "a street cart with a charcoal grill of corn cobs, a bowl of mayonnaise, grated white cheese, chili powder and lime wedges",
     "keeps turning a corn cob on the grill", "puts the corn cob back on the grill", "his hands resting on the edge of the cart",
     "a Mexican street in the daytime, houses painted blue and yellow, green trees on both sides of the street",
     F, 32, "brown hair in a low bun, a gentle face", "a light-pink shirt, black trousers, flat shoes"),
    (13, "José Luis Navarro", M, 62, "street newspaper seller", "short grey hair, a short grey beard, a kindly gentle smile, simple glasses, brown skin",
     "a light-blue shirt, grey trousers, leather shoes",
     "a street newspaper stand with stacks of newspapers and magazines on a wooden counter",
     "keeps straightening a stack of newspapers", "puts a newspaper back on the stack", "his hands resting on the counter",
     "a Mexican street in the daytime, houses painted white and blue, a few signboards that are blurred and unreadable",
     F, 28, "long black hair, a fresh face", "a white blouse, a long navy-blue skirt, flat shoes"),
    (14, "Antonio Delgado", M, 50, "street taco seller", "black hair, slightly bald on top, a short black beard, a tense, direct look, brown skin",
     "a clean white shirt, a clean apron, black trousers, leather shoes",
     "a street taco cart with a steel griddle, a stack of corn tortillas, bowls of grilled meat, chopped onion and cilantro, and jars of salsa",
     "keeps turning pieces of meat on the griddle with a metal spatula", "sets the spatula back on the griddle", "his hands resting on the edge of the cart",
     "a Mexican street at midday, houses painted orange and red",
     F, 31, "long brown hair, a friendly face", "a light-blue shirt, grey trousers, flat shoes"),
    (15, "Manuel Aguilar", M, 68, "street handicraft seller", "short grey hair, a deeply lined kindly face, a clean cloth hat, brown skin",
     "a white shirt, beige trousers, leather shoes",
     "a street handicraft stall with colourful woven baskets, painted ceramic figures and embroidered cloths on a table",
     "keeps straightening a woven basket on the table", "puts the basket back on the table", "his hands resting on the table",
     "a Mexican street handicraft market in the daytime, colourful craft stalls, houses painted purple and yellow",
     F, 34, "black hair in a neat bun, a professional face", "a light-blue blouse, black trousers, flat shoes"),
    (16, "Carmen Salinas", F, 52, "street food seller", "black hair with grey strands in a neat bun, a kind face with a gentle smile, brown skin",
     "a pink blouse, a clean apron, a long skirt with a light pattern, clean sandals",
     "a street food stall with steel pots, trays of tamales and a stack of plates",
     "keeps arranging tamales on a tray", "puts a tamale back on the tray", "her hands resting on the edge of the stall",
     "a Mexican street in the daytime, houses painted pink and orange, a few signboards that are blurred and unreadable",
     M, 33, "short black hair, a friendly face", "a clean white shirt, grey trousers, leather shoes"),
    (17, "Rosa Jiménez", F, 47, "street fruit seller", "long black hair tied low, a slightly worried face, simple glasses, brown skin",
     "a green blouse, black trousers, clean sandals",
     "a street fruit stand with trays of cut mango, watermelon, pineapple and jicama, clear cups, lime and chili",
     "keeps arranging cut fruit on a tray", "puts a piece of fruit back on the tray", "her hands resting on the edge of the stand",
     "a Mexican street fruit market in the daytime, colourful fruit stalls, houses painted blue and white",
     M, 29, "short black hair, a cheerful face", "a white polo shirt, blue jeans, sneakers"),
    (18, "Guadalupe Flores", F, 60, "street flower seller", "grey hair in a neat high bun, a deeply lined, kind, resigned face, brown skin",
     "a white blouse, a long blue skirt, clean sandals",
     "a street flower stand with buckets of roses, sunflowers and carnations",
     "keeps arranging flowers into a bunch", "puts the bunch back in the bucket", "her hands resting on the edge of the flower stand",
     "a Mexican street flower market in the daytime, colourful flower stalls, houses painted yellow and pink",
     M, 32, "short black hair, a calm face", "a clean white shirt, black trousers, leather shoes"),
    (19, "Elena Cruz", F, 45, "street clothes seller", "short wavy black hair, a serious, slightly tense face, brown skin",
     "a light-yellow blouse, white trousers, clean sandals",
     "a street clothing stall with racks of colourful shirts, dresses and scarves",
     "keeps folding a shirt", "puts the folded shirt back on the pile", "her hands resting on the pile of clothes",
     "a Mexican street in the daytime, houses painted blue and red, a few signboards that are blurred and unreadable",
     M, 30, "short black hair, a friendly face", "a light-blue shirt, grey trousers, leather shoes"),
    (20, "Teresa Medina", F, 65, "street bread seller", "long grey hair in a low bun, a kind, gently lined, smiling face, brown skin",
     "a light-pink blouse, a long skirt with a light pattern, clean sandals",
     "a street cart with trays of bread and sweet pastries",
     "keeps arranging pieces of bread on the tray", "puts a piece of bread back on the tray", "her hands resting on the edge of the cart",
     "a Mexican street in the morning, houses painted white and yellow",
     M, 34, "short black hair, a confident face", "a navy-blue polo shirt, beige trousers, leather shoes"),
]

# Giọng: người bán theo giới + tuổi; phóng viên khác giới (nữ tầm 200-230 Hz, nam tầm 125-150 Hz): cặp luôn tách giọng rõ
GIONG_BAN = {
    (M, "tre"): "a real young Mexican man's voice, low and relaxed (around 110-135 Hz), friendly, native Mexican Spanish; a real person, not an actor",
    (M, "gia"): "a real older Mexican man's voice, low, slow and a little gravelly (around 100-125 Hz), warm and good-humoured, native Mexican Spanish; a real person, not an actor",
    (F, "tre"): "a real young Mexican woman's voice, bright and lively (around 220-260 Hz), warm and confident, native Mexican Spanish; a real person, not an actress",
    (F, "gia"): "a real older Mexican woman's voice, warm, a little husky and unhurried (around 190-220 Hz), native Mexican Spanish; a real person, not an actress",
}
GIONG_PV = {
    F: "a real young Mexican woman's voice, bright light mezzo (around 200-230 Hz), friendly and playful like a street-interview host, native Mexican Spanish; a real person, not an announcer",
    M: "a real young Mexican man's voice, light baritone (around 125-150 Hz), friendly and playful like a street-interview host, native Mexican Spanish; a real person, not an announcer",
}
GIONG_AIVA = ("a bright, warm young woman's voice (around 210-230 Hz) with a light synthetic sheen, clear and lively like a friendly teacher, native Mexican "
              "Spanish")
NGUOI_AIVA = ("a glossy white humanoid AI robot with a smooth, calm, human-like face, glowing blue eyes, a small glowing AI mark on the forehead and "
              "dark glossy neck joints")


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def tai_anh():
    from PIL import Image
    rows = [r for r in csv.reader(open(CSV, encoding="utf-8")) if r and r[0].strip().isdigit()]
    os.makedirs(os.path.join(ROOT, BT), exist_ok=True)
    for r in rows:
        n = int(r[0])
        for kind, url in (("nv", r[3]), ("pv", r[5]), ("nen", r[7])):
            fid = re.search(r"/d/([\w-]+)", url).group(1)
            req = urllib.request.Request(f"https://drive.google.com/uc?export=download&id={fid}", headers={"User-Agent": "Mozilla/5.0"})
            b = urllib.request.urlopen(req, timeout=120).read()
            Image.open(io.BytesIO(b)).convert("RGB").save(os.path.join(ROOT, BT, f"{kind}{n:02d}.jpg"), quality=94)
        print("tải ảnh", n, flush=True)


def build():
    out = []
    for n, ten, sex, age, vai, look, mac, quay, viec, viec2, tay, noi, psex, page, plook, pmac in NV:
        he, his, him, self_ = ("he", "his", "him", "himself") if sex == M else ("she", "her", "her", "herself")
        phe, phis, phim = ("he", "his", "him") if psex == M else ("she", "her", "her")
        assert psex != sex, f"biến thể {n}: phóng viên phải khác giới người bán"
        nguoi = "man" if sex == M else "woman"
        pnguoi = "man" if psex == M else "woman"
        tuoi = "tre" if age < 40 else "gia"
        v = {"name": f"es{n:02d}-{slug(ten)}"}
        v.update({
            # phần 1
            "TEN_PV": "the interviewer", "VAI_PV": "street interviewer", "POS_PV": "LEFT foreground, seen from behind",
            "NGUOI_PV": (f"a young Mexican {pnguoi} about {page} years old, exactly as in {phis} reference photo (same face, hair and build): {plook}; "
                         f"{pmac}"),
            "GIONG_PV": GIONG_PV[psex],
            "QUAY_LUNG_PV": "1",
            "HIS_PV": phis, "HIM_PV": phim, "TOC_PV": plook.split(",")[0],
            "NHIN_PV": (f"keeps {phis} face pointed at the vendor's face, to the right and slightly down, the camera seeing only the back and the right edge of {phis} head; "
                        f"{phe} never turns toward the camera"),
            "NGHE_PV": f"holds the microphone still toward the vendor and keeps {phis} face pointed at {him}, {phis} head still, the camera seeing only the back of {phis} head",
            "DAO_MIC": "a plain black handheld microphone with no logo",
            "TEN_HOC": "the vendor", "VAI_HOC": vai, "POS_HOC": "CENTRE-RIGHT, behind the stall",
            "NGUOI_HOC": (f"a Mexican {nguoi} about {age} years old, exactly as in {his} reference photo (same face, hair, build and clothes): {look}; {mac}; "
                          "photorealistic skin and fabric"),
            "GIONG_HOC": GIONG_BAN[(sex, tuoi)],
            "SHE_HOC": he, "HER_HOC": his, "HERO_HOC": him, "SELF_HOC": self_,
            "DAO_GANG": BAR.format(He=he.capitalize()),
            "DAO_GIU": f"{tay[0].upper() + tay[1:]} at the start of every clip.",
            "TAY_HOC": tay, "VIEC_HOC": viec, "VIEC2_HOC": viec2,
            "NHIN_HOC": "looks at the interviewer's face, to the left, in three-quarter view, and never looks at the camera",
            "NGHE_HOC": (f"keeps the lips pressed together and looks at the interviewer's face with a friendly attentive face, {tay}; "
                         f"{he} never looks at the camera"),
            "DAO_NGHI": f"the interviewer holding the microphone toward {him}, {tay}",
            "DAO_XE": quay,
            "NEN_PHO": (f"{noi}; the place and the stall look exactly like the background reference photo (an empty view of this place), with {his} stall in front of {him}; "
                        "any signboards are blurred and unreadable"),
            # phần 2
            "TEN_DAY": "the AI tutor", "NGUOI_DAY": NGUOI_AIVA, "GIONG_DAY": GIONG_AIVA,
            "NEN_DAY": ("a deep navy-to-violet gradient backdrop with one thin glowing purple circular ring behind the head and a few tiny glowing dots along the ring, "
                        "nothing else"),
            "NEN_HOC": f"{noi}, out of focus behind {him}; the place looks like the background reference photo; any signboards are blurred and unreadable",
        })
        v["LUOT"] = [{"who": w, "text": t, "emo": e, "c": "black", "o": "white", "fx": "none", "phan": p}
                     for w, p, t, e in luot("nativa" if sex == F else "nativo")]
        refs = {"NGUOI_DAY": [ANH + "robot-aiva.png"], "NGUOI_PV": [BT + f"pv{n:02d}.jpg"], "NGUOI_HOC": [BT + f"nv{n:02d}.jpg"],
                "NEN_PHO": [BT + f"nen{n:02d}.jpg"], "NEN_HOC": [BT + f"nen{n:02d}.jpg"]}
        for k, ps in refs.items():
            for p in ps:
                if not os.path.isfile(os.path.join(ROOT, p)):
                    print(f"LỖI [{v['name']}] {k}: thiếu ảnh {p} (chạy với --tai-anh)")
        v["refs"] = refs
        out.append(v)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--tai-anh" in sys.argv:
        tai_anh()
    data = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.abspath(OUT), f"({len(data)} biến thể; người bán nam {sum(1 for x in NV if x[2] == M)}, nữ {sum(1 for x in NV if x[2] == F)}; "
          f"{len(data[0]['LUOT'])} lượt)")
