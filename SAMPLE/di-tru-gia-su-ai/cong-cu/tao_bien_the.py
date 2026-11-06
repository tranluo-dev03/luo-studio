"""Sinh SAMPLE/di-tru-gia-su-ai/BIEN-THE-DI-TRU-GIA-SU-AI.json từ bảng BIEN_THE (không sửa tay JSON).
    .venv\\Scripts\\python.exe SAMPLE\\di-tru-gia-su-ai\\cong-cu\\tao_bien_the.py
Video mẫu: 1410_immigration ES_003 (67 s, tiếng Tây Ban Nha xen tiếng Anh). Biến thể 01 bám sát video mẫu: lời theo PHỤ ĐỀ trên hình
(Whisper nghe nhầm "No, Devis, just here" = "No, debes decir:", "¿Es un serio?" = "¿Es en serio?", "no vengo dinero" = "no tengo dinero").
Ảnh tham chiếu: ảnh AI gen bằng Muse từ CHỮ (cong-cu/gen_anh_nhan_vat.py, người dùng cho phép 05/11/2026), KHÔNG cắt từ video mẫu.
Biến thể mới: thêm một dict vào BIEN_THE (chỉ ghi khoá muốn đổi; còn lại lấy MAC_DINH), chạy lại."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "BIEN-THE-DI-TRU-GIA-SU-AI.json")
ANH = "SAMPLE/di-tru-gia-su-ai/anh/"

MAC_DINH = {
    # --- người học (cả 3 phần) ---
    "TEN_HOC": "Diego",
    "VAI_HOC": "young man",
    "NGUOI_HOC": ("a Mexican young man about 20 years old, slim build, light-tan skin, short dark-brown curly hair under a black baseball cap worn backwards, "
                  "thin dark eyebrows, brown eyes, clean-shaven, a small silver hoop earring, a small tattoo on the side of the neck and fine-line tattoos on the forearms; "
                  "a plain white crew-neck T-shirt and black trousers"),
    "GIONG_HOC": ("a real young Mexican man's voice, around 125–150 Hz, slightly nasal and casual, native Mexican Spanish; speaks English as a learner "
                  "with a clear Mexican accent; a real person, not an actor"),
    "DAO_CAFE": "a white takeaway coffee cup with a brown cardboard sleeve and a white lid, held in one hand at waist height",
    # --- bạn gái gọi điện (phần 1) ---
    "TEN_AMIGA": "Valeria",
    "VAI_AMIGA": "friend on the phone",
    "NGUOI_AMIGA": ("a Mexican-American young woman in her early twenties, long straight dark-brown hair past the shoulders with a middle part, thick dark eyebrows, "
                    "brown eyes, light-tan skin, long nude nails, fine-line floral tattoos on both forearms; a white ribbed cropped tank top and light-blue high-waisted jeans"),
    "GIONG_AMIGA": "a young Mexican woman's voice around 220–250 Hz, worried, urgent and hushed, native Mexican Spanish; a real person, not an actress",
    "NEN_NHA": ("a bright high-rise apartment living room: a floor-to-ceiling window on the right with a sunny downtown skyline of glass towers, a beige sofa, "
                "a framed picture and a lamp on a cream wall on the left, softly out of focus"),
    "NEN_PHO": ("a sunny Southern-California street corner: the sidewalk outside a small convenience store with red-and-white striped trim and glass doors covered "
                "in blurry colourful posters with no readable text, a crosswalk, traffic lights, power poles and palm trees, a few parked cars, bright midday sun, blue sky"),
    # --- cảnh sát (phần 2) ---
    "TEN_CANHSAT": "the officer",
    "VAI_CANHSAT": "police officer",
    "NGUOI_CANHSAT": ("an American police officer in his mid-forties, white, short light-brown hair, clean-shaven, blue eyes, fit build; a dark-navy short-sleeve "
                      "police uniform shirt with a plain silver badge shape and a black shoulder radio, a black duty belt"),
    "GIONG_CANHSAT": "a confident American man in his forties, mid-low voice around 130–150 Hz, polite, calm and official, General American accent",
    # --- robot nhỏ trên vai (phần 2) ---
    "TEN_ROBO": "the tiny robot",
    "VAI_ROBO": "tiny AI tutor robot",
    "NGUOI_ROBO": ("a tiny cute chibi robot about the size of a kitten, glossy white body panels with lavender-purple seams and joints, a big round head with soft "
                   "silver-white bob hair, big shiny blue cartoon eyes, round glowing purple headphone rings on both ears, short rounded arms and legs"),
    "GIONG_ROBO": ("a tiny bright cartoon girl's voice around 300–330 Hz, sweet and quick, Mexican Spanish; says English words with a clean American accent"),
    # --- gia sư AI trong ô góc phải (phần 3) ---
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": ("a sleek feminine humanoid robot: a smooth matte-white porcelain face with calm dark eyes and softly sculpted lips, a bald white helmet-like head, "
                  "a soft glowing white halo ring behind the head, white segmented armour panels over black mechanical joints on the neck, chest, shoulders and arms"),
    "GIONG_DAY": ("a calm, smooth, warm feminine voice with a light synthetic sheen, around 150–190 Hz, natural Mexican Spanish, clear and patient; "
                  "says English words with a neutral American accent"),
    "NEN_DAY": "a soft light-grey studio backdrop with a faint white glow behind the head",
}

ANH_MAC_DINH = {"NGUOI_HOC": ANH + "ai-hoc.png", "NGUOI_AMIGA": ANH + "ai-amiga.png", "NGUOI_CANHSAT": ANH + "ai-canhsat.png",
                "NGUOI_ROBO": ANH + "ai-robo.png", "NGUOI_DAY": ANH + "ai-day.png"}

BIEN_THE = [
    {"name": "bien-the-01-goc", "que": "Mexico", "nam": "twelve"},
]
BIEN_THE = [{**MAC_DINH, **b} for b in BIEN_THE]


def luot(que, nam):
    """28 lượt = 28 cảnh: phần 1 gọi điện (5), phần 2 cảnh sát + robot nhỏ (10), phần 3 robot gia sư trong ô (13)."""
    sai, dung = f"I am {que}.", f"I am from {que}."
    L = [
        # phần 1: gọi điện
        ("amiga", 1, "No regreses a casa todavía.", "worried, urgent"),
        ("hoc", 1, "¿Por qué?", "confused"),
        ("amiga", 1, "Hay agentes de inmigración en la calle.", "worried, urgent"),
        ("hoc", 1, "Pero yo no hice nada.", "worried, hesitant"),
        ("amiga", 1, "Ya sé. Tú tranquilo.", "calm, reassuring"),
        # phần 2: cảnh sát
        ("canhsat", 2, "Good morning, sir. Can I ask you a few questions?", "calm, attentive"),
        ("canhsat", 2, "Where are you from?", "calm, attentive"),
        ("hoc", 2, sai, "nervous, unsure", {"c": "red", "fx": "wrong"}),
        ("robo", 2, f"No, debes decir: {dung}", "cheerful, encouraging", {"to": dung, "to_mau": "green"}),
        ("hoc", 2, dung, "relieved, confident", {"c": "green", "fx": "right", "icon": "check"}),
        ("canhsat", 2, "How long have you been living here?", "polite, curious"),
        ("hoc", 2, f"I've been living here for {nam} years.", "confident"),
        ("canhsat", 2, "Your English is really good.", "impressed, friendly"),
        ("hoc", 2, "Thank you. I used to struggle with English too.", "happy, proud"),
        ("canhsat", 2, "How did you improve so much?", "curious, friendly"),
        # phần 3: gia sư AI
        ("day", 3, "¿Hablas inglés?", "friendly, curious"),
        ("hoc", 3, "Más o menos.", "unsure"),
        ("day", 3, "¿De dónde eres? Where are you from?", "friendly, curious"),
        ("hoc", 3, sai, "unsure", {"c": "red", "fx": "wrong"}),
        ("day", 3, f"¡Casi! Mejor di: {dung}", "patient, encouraging", {"to": dung, "to_mau": "green"}),
        ("hoc", 3, "Siempre me confundo con eso.", "embarrassed"),
        ("day", 3, "Para eso estoy yo, para ayudarte a hablar bien.", "warm, reassuring"),
        ("hoc", 3, "Pero... no tengo dinero.", "worried", {"icon": "dollar"}),
        ("day", 3, "¡No necesitas dinero! No es como las otras apps o cursos caros.", "cheerful, confident"),
        ("hoc", 3, "¿Es en serio?", "surprised"),
        ("day", 3, "¡Claro! Nada de trampas. Solo práctica real de conversación en inglés con tu tutor de inteligencia artificial.", "cheerful, confident"),
        ("hoc", 3, "¿Como... un tutor real?", "curious, surprised"),
        ("day", 3, "Sí. Corrijo tu gramática, pronunciación y te ayudo a hablar con confianza.", "warm, confident"),
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


def build():
    res = []
    for b in BIEN_THE:
        b = dict(b)
        que, nam, anh = b.pop("que"), b.pop("nam"), {**ANH_MAC_DINH, **b.pop("anh", {})}
        v = {k: x for k, x in b.items()}
        v.update({
            # hướng nhìn / tư thế nghe theo phần
            "POS_AMIGA": "alone-in-frame", "POS_HOC@1": "alone-in-frame",
            "NHIN_AMIGA": "looks slightly off to the side, past the camera, as if listening to the phone",
            "NGHE_AMIGA": "holds the phone to her ear with the mouth closed, worried eyes, still",
            "NHIN_HOC@1": "looks slightly off to the side, past the camera, as if listening to the phone",
            "NGHE_HOC@1": "holds the phone to his ear with the mouth closed, still",
            "POS_HOC@2": "LEFT", "POS_CANHSAT": "RIGHT", "POS_ROBO": "on-the-shoulder",
            "NHIN_HOC@2": "looks at the officer's face",
            "NGHE_HOC@2": "keeps looking at the officer with the mouth closed, holding the coffee cup still",
            "NHIN_CANHSAT": "looks at the young man's face",
            "NGHE_CANHSAT": "keeps looking at the young man with the mouth closed, hands still, calm face",
            "NHIN_ROBO": "looks straight into the lens with a bright smile",
            "NGHE_ROBO": "sits perfectly still on the shoulder like a small figurine, its tiny mouth closed, big eyes blinking slowly",
            "LUOT": luot(que, nam),
            "refs": _refs(anh, v["name"]),
        })
        res.append(v)
    return res


if __name__ == "__main__":
    res = build()
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("ok", len(res), "biến thể,", len(res[0]["LUOT"]), "lượt")
