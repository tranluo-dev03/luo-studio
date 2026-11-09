"""Sinh SAMPLE/di-tru-aiva-ai/BIEN-THE-DI-TRU-AIVA-AI.json từ bảng HANH_KHACH (không sửa tay JSON).
    .venv\\Scripts\\python.exe SAMPLE\\di-tru-aiva-ai\\cong-cu\\tao_bien_the.py
Nguồn: "oder 7 - Sheet1.csv" (người dùng, 08/11/2026): kịch bản Spanish + English (app Aiva AI) + 20 biến thể NHÂN VẬT HÀNH KHÁCH (HOC).
Cảnh sát, gia sư AI giữ nguyên ở mọi biến thể (ảnh tham chiếu ai-canhsat.png / ai-day.png của di-tru-gia-su-ai).
Ảnh hành khách: anh/hk-NN.png = ảnh AI người dùng đưa (link Drive trong CSV), phông xanh lá; chưa có file thì bỏ khỏi refs và in cảnh báo.
Người gọi phần 1 (BO): kịch bản CSV là "Bố" ("Mija..."). Hành khách >= 60 tuổi thì bố ~90 tuổi không hợp -> người gọi là CON TRAI ("Mamá/Papá...").
Đổi app: APP. Thêm hành khách: thêm một dòng vào HANH_KHACH."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "BIEN-THE-DI-TRU-AIVA-AI.json")
ANH = "SAMPLE/di-tru-aiva-ai/anh/"
APP = "Aiva AI"
QUE, NAM = "Mexico", "twelve"

CHUNG = {
    "DAO_CAFE": "a white takeaway coffee cup with a brown cardboard sleeve and a white lid, held in one hand at waist height",
    "NEN_NHA": ("a modest, tidy family living room in a small Los Angeles house: a window on the right with daylight and a palm tree outside, a brown sofa, "
                "framed family photos and a small wooden cross on a cream wall on the left, softly out of focus"),
    "NEN_PHO": ("a sunny Southern-California street corner: the sidewalk outside a small convenience store with red-and-white striped trim and glass doors covered "
                "in blurry colourful posters with no readable text, a crosswalk, traffic lights, power poles and palm trees, a few parked cars, bright midday sun, blue sky"),
    "TEN_CANHSAT": "the officer",
    "VAI_CANHSAT": "police officer",
    "NGUOI_CANHSAT": ("an American police officer in his mid-forties, white, short light-brown hair, clean-shaven, blue eyes, fit build; a dark-navy short-sleeve "
                      "police uniform shirt with a plain silver badge shape and a black shoulder radio, a black duty belt"),
    "GIONG_CANHSAT": "a confident American man in his forties, mid-low voice around 130–150 Hz, polite, calm and official, General American accent",
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": ("a sleek feminine humanoid robot: a smooth matte-white porcelain face with calm dark eyes and softly sculpted lips, a bald white helmet-like head, "
                  "a soft glowing white halo ring behind the head, white segmented armour panels over black mechanical joints on the neck, chest, shoulders and arms"),
    "GIONG_DAY": ("a calm, smooth, warm feminine voice with a light synthetic sheen, around 150–190 Hz, natural Mexican Spanish, clear and patient; "
                  "says English words with a neutral American accent"),
    "NEN_DAY": "a soft light-grey studio backdrop with a faint white glow behind the head",
}

GIONG = {
    ("f", "tre"): ("a real young Mexican woman's voice, around 200–240 Hz, warm and casual, native Mexican Spanish; speaks English as a learner "
                   "with a clear Mexican accent; a real person, not an actress"),
    ("f", "gia"): ("a real Mexican woman's voice in her sixties, around 180–210 Hz, warm and slightly husky, native Mexican Spanish; speaks English as a learner "
                   "with a clear Mexican accent; a real person, not an actress"),
    ("m", "tre"): ("a real young Mexican man's voice, around 125–150 Hz, slightly nasal and casual, native Mexican Spanish; speaks English as a learner "
                   "with a clear Mexican accent; a real person, not an actor"),
    ("m", "gia"): ("a real older Mexican man's voice, around 105–130 Hz, slightly gravelly and warm, native Mexican Spanish; speaks English as a learner "
                   "with a clear Mexican accent; a real person, not an actor"),
}
NGUOI_GOI = {
    "tre": ("TEN_BO", "his father", "father on the phone",
            "a Mexican man in his mid-fifties, short black hair greying at the temples, a thick moustache, tired kind eyes, tan skin; a light-blue button-up work shirt",
            "a Mexican man in his fifties, around 110–130 Hz, worried, urgent and hushed, native Mexican Spanish; a real person, not an actor"),
    "gia": ("TEN_BO", "the son", "adult son on the phone",
            "a Mexican man about forty, short black hair, a neatly trimmed short beard, brown eyes, tan skin; a plain grey polo shirt",
            "a Mexican man about forty, around 120–140 Hz, worried, urgent and hushed, native Mexican Spanish; a real person, not an actor"),
}

# (số, mã, tên, giới f/m, tuổi, ngoại hình EN)
HANH_KHACH = [
    (1, "nu-tre-giup-viec", "Daniela", "f", 26, "a Mexican woman about 26, long loose curly dark hair, a floral tattoo on the forearm, red lipstick, big gold hoop earrings; a fitted white blouse with red embroidery, a white apron, a fitted dark skirt and high-heeled boots"),
    (2, "nu-tre-phuc-vu", "Camila", "f", 24, "a Mexican woman about 24, long wavy black hair worn loose, a small tattoo on the shoulder, smoky eye makeup, gold hoop earrings; a fitted black off-the-shoulder top, a black waist apron, fitted black trousers and heels"),
    (3, "nu-tre-phu-bep", "Lupita", "f", 28, "a Mexican woman about 28, curly hair tied up under a colourful bandana, a tattoo on the arm, bold makeup, gold hoop earrings; a fitted white chef's jacket, an apron, fitted black trousers and kitchen shoes"),
    (4, "nu-tre-bao-mau", "Ximena", "f", 23, "a Mexican woman about 23, long loose curly hair, a butterfly tattoo on the arm, gold hoop earrings; a bright Mexican-embroidered fitted crop top, jeans and heeled sandals"),
    (5, "nam-tre-xay-dung", "Alejandro", "m", 27, "a muscular Mexican man about 27, Aztec-pattern tattoo sleeves on both arms, a moustache, a gold chain; a white hard hat, a fitted white T-shirt under an open orange high-visibility vest, fitted jeans and brown work boots"),
    (6, "nam-tre-lam-vuon", "Miguel", "m", 29, "a Mexican man about 29, tribal tattoos on the arms, a straw cowboy hat, a red bandana around the neck; a fitted plaid shirt with rolled sleeves, fitted jeans and leather boots"),
    (7, "nam-tre-dau-bep", "Javier", "m", 26, "a Mexican man about 26, a bandana on the head, an eagle tattoo on the chest and a swallow tattoo on the hand; a fitted white chef's jacket partly unbuttoned, a denim apron, fitted black trousers and kitchen shoes"),
    (8, "nam-tre-sua-xe", "Ricardo", "m", 30, "a Mexican man about 30, full tattoo sleeves on both arms (skulls, wrenches, roses), a moustache, a gold chain; a fitted blue work-uniform shirt with rolled sleeves and a red bandana in the pocket, fitted trousers and boots"),
    (9, "nam-tre-giao-hang", "Luis", "m", 24, "a Mexican man about 24, tribal tattoos on the arm, a backwards baseball cap, a gold chain; a fitted blue polo shirt under an open reflective jacket, fitted black trousers and sneakers"),
    (10, "nu-tre-tho-nail", "Andrea", "f", 25, "a Mexican woman about 25, long straight black hair worn loose, a rose tattoo on the shoulder, bold makeup, gold hoop earrings; a fitted colourful embroidered top, a black apron, fitted black trousers and heels"),
    (11, "nu-gia-giup-viec-khach-san", "Rosa", "f", 62, "a Mexican woman about 62, silver hair in a loose bun, a kind proud face, gold earrings; a colourful embroidered blouse, a white apron, a fitted dark skirt and heels"),
    (12, "nu-gia-dau-bep", "Carmen", "f", 65, "a Mexican woman about 65, silver hair tied with colourful ribbons, a gold necklace; a bright Mexican-embroidered blouse, a floral apron, a long full hot-pink skirt and heeled sandals"),
    (13, "nu-gia-tho-may", "Guadalupe", "f", 60, "a Mexican woman about 60, salt-and-pepper hair in a loose bun, big gold hoop earrings; a bright turquoise embroidered blouse, a long multicoloured skirt, an apron and heels"),
    (14, "nu-gia-cham-soc", "Teresa", "f", 68, "a Mexican woman about 68, silver hair tied with colourful ribbons, gold earrings and a gold pendant; a fitted polo shirt, trousers and flat shoes, a bright rebozo shawl over the shoulders"),
    (15, "nu-gia-ban-do-an", "Josefina", "f", 70, "a Mexican woman about 70, silver hair under a colourful head wrap, gold earrings; a bright Mexican-embroidered blouse, a long floral skirt, an apron and heeled sandals"),
    (16, "nam-gia-xay-dung", "Antonio", "m", 65, "a Mexican man about 65, grey hair and a grey beard, old-school tattoos (eagle, rose) on the arms, a gold chain; a white hard hat, a fitted T-shirt under an open high-visibility vest, fitted jeans and boots"),
    (17, "nam-gia-lam-vuon", "Manuel", "m", 68, "a Mexican man about 68, grey hair, a moustache, tattoos on the arms, a gold chain; a cowboy hat, a bandana around the neck, a fitted red plaid shirt with rolled sleeves, fitted jeans and leather boots"),
    (18, "nam-gia-nong-dan", "Ramón", "m", 62, "a Mexican man about 62, salt-and-pepper hair, tattoos on the arms; a straw hat, a bandana around the neck, a fitted work shirt with rolled sleeves, fitted jeans and boots"),
    (19, "nam-gia-tho-son", "Jesús", "m", 70, "a Mexican man about 70, white hair, a kind face, tattoos on the arms; a white cap, a fitted white painter's shirt and white trousers, work shoes"),
    (20, "nam-gia-lao-cong", "Francisco", "m", 66, "a Mexican man about 66, grey hair, a moustache, tattoos on the arms, a gold chain; a blue cap, a fitted blue janitor uniform with rolled sleeves, fitted trousers and boots"),
]


def luot(gioi, nhom):
    """30 lượt = 30 cảnh: phần 1 gọi điện (5), phần 2 cảnh sát (10), phần 3 gia sư AI trong ô (15). Lời theo kịch bản CSV."""
    goi = {("f", "tre"): "Mija", ("m", "tre"): "Mijo", ("f", "gia"): "Mamá", ("m", "gia"): "Papá"}[(gioi, nhom)]
    tranquilo = "tranquila" if gioi == "f" else "tranquilo"
    sai, dung = f"I am {QUE}.", f"I am from {QUE}."
    L = [
        # phần 1: gọi điện
        ("bo", 1, f"{goi}, no regreses a casa todavía.", "worried, urgent"),
        ("hoc", 1, "¿Qué? ¿Por qué?", "confused"),
        ("bo", 1, "Hay agentes de inmigración en la calle.", "worried, urgent"),
        ("hoc", 1, "Pero yo no hice nada.", "worried, hesitant"),
        ("bo", 1, f"Ya sé, tú {tranquilo}.", "calm, reassuring"),
        # phần 2: cảnh sát
        ("canhsat", 2, "Good morning. Can I ask you a few questions?", "calm, attentive"),
        ("hoc", 2, "Of course. What would you like to know?", "attentive, nervous"),
        ("canhsat", 2, "Where are you from?", "calm, attentive"),
        ("hoc", 2, f"{QUE}.", "calm"),
        ("canhsat", 2, "How long have you been living here?", "polite, curious"),
        ("hoc", 2, f"I've been living here for {NAM} years.", "confident"),
        ("canhsat", 2, "Your English is really good.", "impressed, friendly"),
        ("hoc", 2, "Thank you. I used to struggle with English too.", "happy, proud"),
        ("canhsat", 2, "Really? How did you improve so much?", "curious, friendly"),
        ("hoc", 2, f"{APP}, I just practice real conversations for about ten minutes a day. That's it.", "confident"),
        # phần 3–5 CSV: gia sư AI
        ("day", 3, "¿Hablas inglés?", "friendly, curious"),
        ("hoc", 3, "Más o menos.", "unsure"),
        ("day", 3, "¿De dónde eres? Where are you from?", "friendly, curious"),
        ("hoc", 3, sai, "unsure", {"c": "red", "fx": "wrong"}),
        ("day", 3, f"Casi. Mejor di: {dung}", "patient, encouraging", {"to": dung, "to_mau": "green"}),
        ("hoc", 3, "Siempre me confundo con eso.", "embarrassed"),
        ("day", 3, "Para eso estoy yo, para ayudarte a hablar bien.", "warm, reassuring"),
        ("hoc", 3, "Pero no tengo dinero.", "worried", {"icon": "dollar"}),
        ("day", 3, f"Que no necesitas dinero con {APP}. Puedes practicar inglés gratis. No es como las otras apps o cursos caros.", "cheerful, confident"),
        ("hoc", 3, "¿Es en serio?", "surprised"),
        ("day", 3, "Claro, nada de trampas. Solo práctica real de conversación en inglés con tu tutor de inteligencia artificial.", "cheerful, confident"),
        ("hoc", 3, "¿Como un tutorial?", "curious, surprised"),
        ("day", 3, "Sí. Corrijo tu gramática, pronunciación y te ayudo a hablar con confianza.", "warm, confident"),
        ("hoc", 3, f"Okey. Entonces, ¿voy a descargar {APP} ahorita mismo?", "happy, excited"),
        ("day", 3, "Muy buena decisión. Vamos a hablar inglés juntos.", "warm, cheerful"),
    ]
    out = []
    for who, phan, text, emo, *extra in L:
        t = {"who": who, "text": text, "emo": emo, "fx": "none", "phan": phan}
        t.update(extra[0] if extra else {})
        out.append(t)
    return out


def _refs(m, name):
    out = {}
    for k, x in m.items():
        if x and (x.startswith("http") or os.path.isfile(os.path.join(ROOT, x))):
            out[k] = [x]
        elif x:
            print(f"CẢNH BÁO [{name}] {k}: chưa có ảnh {x}, bỏ khỏi refs")
    return out


NHIN_HOC_GOC = "looks into the lens as if talking to a friend on a video call"
NGHE_HOC_GOC = "waits with an attentive soft smile, eyes on the lens, the lips gently pressed together, holding the coffee cup still"


def build():
    res = []
    for so, ma, ten, gioi, tuoi, nguoi in HANH_KHACH:
        nhom = "gia" if tuoi >= 50 else "tre"
        vai = ("young " if nhom == "tre" else "older ") + ("woman" if gioi == "f" else "man")
        he, his, him = ("she", "her", "her") if gioi == "f" else ("he", "his", "him")
        _, ten_bo, vai_bo, nguoi_bo, giong_bo = NGUOI_GOI[nhom]
        name = f"hk-{so:02d}-{ma}"
        v = {"name": name, **CHUNG,
             "TEN_HOC": ten, "VAI_HOC": vai, "NGUOI_HOC": nguoi, "GIONG_HOC": GIONG[(gioi, nhom)],
             "HE_HOC": he, "HIM_HOC": him,
             "TEN_BO": f"{ten}'s {ten_bo.split()[-1]}", "VAI_BO": vai_bo, "NGUOI_BO": nguoi_bo, "GIONG_BO": giong_bo,
             # hướng nhìn / tư thế nghe theo phần
             # khoá gốc (không @): Studio bắt buộc điền, dùng cho phần 3; phần 1-2 đã có khoá @ ghi đè
             "NHIN_HOC": NHIN_HOC_GOC, "NGHE_HOC": NGHE_HOC_GOC,
             "POS_BO": "alone-in-frame", "POS_HOC@1": "alone-in-frame",
             "NHIN_BO": "looks slightly off to the side, past the camera, as if listening to the phone",
             "NGHE_BO": "holds the phone to his ear with the mouth closed, worried eyes, still",
             "NHIN_HOC@1": "looks slightly off to the side, past the camera, as if listening to the phone",
             "NGHE_HOC@1": f"holds the phone to {his} ear with the mouth closed, still",
             "POS_HOC@2": "LEFT", "POS_CANHSAT": "RIGHT",
             "NHIN_HOC@2": "looks at the officer's face",
             "NGHE_HOC@2": "keeps looking at the officer with the mouth closed, holding the coffee cup still",
             "NHIN_CANHSAT": f"looks at the {vai}'s face",
             "NGHE_CANHSAT": f"keeps looking at the {vai} with the mouth closed, hands still, calm face",
             "LUOT": luot(gioi, nhom)}
        anh = {"NGUOI_HOC": ANH + f"hk-{so:02d}.png", "NGUOI_CANHSAT": ANH + "ai-canhsat.png", "NGUOI_DAY": ANH + "ai-day.png"}
        v["refs"] = _refs(anh, name)
        if "NGUOI_HOC" not in v["refs"]:   # thiếu ảnh hành khách: không đưa vào (gen không ảnh thì mặt lệch giữa các phần)
            print(f"BỎ QUA [{name}]: chưa có ảnh hành khách")
            continue
        res.append(v)
    return res


if __name__ == "__main__":
    res = build()
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("ok", len(res), "biến thể,", len(res[0]["LUOT"]), "lượt; lượt dài nhất",
          max(len(t["text"].split()) for v in res for t in v["LUOT"]), "từ")
