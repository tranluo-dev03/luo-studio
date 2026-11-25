"""Nhóm eyb53o (kịch bản goc): như kb3lqv nhưng 15 mã NU 06-10 (5-10t, 20-30t, 30-45t) với bot BOT-TALKA-DEF-LATIN-03.
Chạy: python tao_bien_the_nhom_eyb53o.py (không sửa tay JSON)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "BIEN-THE-NHOM-eyb53o.json")
REAL = "a real, photorealistic live-action Latino"
ROBOT = "exposed black cables and white mechanical arms and hands"
BOTS = {
    "BOT-TALKA-AVA-LATIN-03": (f"a humanoid AI avatar with a human-looking young woman's face, fair skin and a very long auburn braid, {ROBOT}, wearing a rust-orange ruffled dress, calm friendly expression",
                               "a calm, clear, warm young woman's voice around 205-225 Hz, speaking Spanish with the English words kept in English, patient and encouraging"),
    "BOT-TALKA-DEF-LATIN-02": (f"a humanoid AI robot with a glossy white head with a smooth white face and softly glowing pale-blue eyes, {ROBOT}, wearing a coral ruffle-sleeved blouse and blue jeans, calm friendly expression",
                               "a calm, clear, warm female-leaning synthetic-but-natural voice around 195-215 Hz, speaking Spanish with the English words kept in English, patient and encouraging"),
    "BOT-TALKA-AVA-LATIN-02": (f"a humanoid AI avatar with a human-looking young Latino man's face and short black hair, {ROBOT}, wearing a grey suit waistcoat over a white shirt, calm friendly expression",
                               "a calm, clear, warm young man's voice, a baritone around 125-145 Hz, speaking Spanish with the English words kept in English, patient and encouraging"),
    "BOT-TALKA-DEF-LATIN-03": (f"a humanoid AI robot with a glossy white head with a smooth white face and softly glowing pale-blue eyes, {ROBOT}, wearing a black embroidered charro jacket over a white shirt and black trousers, calm friendly expression",
                               "a calm, clear, warm male-leaning synthetic-but-natural voice, a baritone around 130-150 Hz, speaking Spanish with the English words kept in English, patient and encouraging"),
}
# (mã kho, tả ngoại hình EN theo ảnh, cao độ giọng)
A = [
    ("NU-5-10-LAT-06", "Black girl about 7, hair in two afro puffs, an orange t-shirt and a white pleated skirt", "270-290 Hz"),
    ("NU-5-10-LAT-07", "girl about 8, dark hair in a half ponytail, a denim jacket over a white t-shirt and jeans", "265-285 Hz"),
    ("NU-5-10-LAT-08", "girl about 8, two long dark braids, a colourful striped serape-pattern t-shirt and jeans", "265-285 Hz"),
    ("NU-5-10-LAT-09", "girl about 8, light-brown hair in two braids, a white embroidered blouse and a denim skirt with brown sandals", "265-285 Hz"),
    ("NU-5-10-LAT-10", "Black girl about 7, curly hair in a top bun, a purple t-shirt and black cargo trousers", "270-290 Hz"),
    ("NU-20-30-LAT-06", "woman about 24, dark hair tied back, a pink floral blouse and black trousers", "210-230 Hz"),
    ("NU-20-30-LAT-07", "woman about 27, hair tied back, a denim jacket over a salmon top and black trousers", "200-220 Hz"),
    ("NU-20-30-LAT-08", "woman about 25, dark hair tied back, a lavender short-sleeved blouse and grey trousers", "205-225 Hz"),
    ("NU-20-30-LAT-09", "woman about 28, hair tied back, an orange high-visibility vest over a white t-shirt and jeans", "195-215 Hz"),
    ("NU-20-30-LAT-10", "woman about 30, hair in a bun, a yellow floral blouse and blue jeans", "200-215 Hz"),
    ("NU-30-45-LAT-06", "woman about 36, curly dark hair pinned up, a navy short-sleeved top and navy trousers", "190-205 Hz"),
    ("NU-30-45-LAT-07", "woman about 39, hair tied back, a dark grey polo shirt and black trousers", "190-205 Hz"),
    ("NU-30-45-LAT-08", "woman about 50, short grey curly hair, an orange high-visibility vest over a yellow top and navy trousers", "180-195 Hz"),
    ("NU-30-45-LAT-09", "woman about 38, hair tied back, a brown polo shirt and brown trousers", "190-205 Hz"),
    ("NU-30-45-LAT-10", "woman about 34, curly dark hair in a bun, a white paint-splattered shirt and white trousers", "195-210 Hz"),
]
GROUPS = [(A, "BOT-TALKA-DEF-LATIN-03")]

NEN = "a bright cream-coloured kitchen with wooden cabinets and a granite counter, a sink in front of the person"

L = lambda who, text, emo, **k: dict({"who": who, "text": text, "emo": emo, "fx": "none"}, **k)
LUOT = [
    L("day", "Where are you from?", "curious"),
    L("hoc", "I am Mexico.", "cheerful", fx="wrong", c="red", icon="x"),
    L("day", "¡Casi! Pero la forma correcta de decirlo es: \"I am from Mexico.\"", "warm", fx="right", c="green", icon="check", to="I am from Mexico"),
    L("hoc", "Ay, siempre cometo ese mismo error.", "embarrassed"),
    L("day", "¡Para eso estoy aquí! Para ayudarte a mejorar tu inglés.", "warm"),
    L("hoc", "Pero no tengo dinero.", "worried"),
    L("day", "¿Dinero? ¡No tienes que pagar nada! Olvídate de las apps y los cursos caros. Con Talka AI puedes practicar inglés totalmente gratis.", "reassuring"),
    L("hoc", "¿En serio?", "surprised"),
    L("day", "¡Claro! Sin condiciones ocultas. Solo conversaciones reales en inglés con tu tutor de inteligencia artificial.", "friendly"),
    L("hoc", "¿Como si fuera un tutor de verdad?", "curious"),
    L("day", "¡Exacto! Talka AI te ayuda a mejorar tu gramática, tu pronunciación y a hablar inglés con más confianza.", "encouraging"),
    L("hoc", "¡Perfecto! Entonces voy a descargar Talka AI ahora mismo.", "confident"),
    L("day", "¡Excelente decisión! ¡Vamos a practicar inglés juntos!", "upbeat"),
]

res = []
for lst, bot_code in GROUPS:
    bot, gd = BOTS[bot_code]
    for ma, mo_ta, hz in lst:
        kid = "-5-10-" in ma
        who = ("boy" if "boy" in mo_ta.split(",")[0] else "girl") if kid else ("man" if ma.startswith("NAM") else "woman")
        res.append({
            "name": "eyb53o-" + ma.lower().replace("-lat-", "").replace("-", ""),
            "TEN_DAY": "the AI tutor", "NGUOI_DAY": bot, "GIONG_DAY": gd, "NEN_DAY": "a plain pure black background",
            "TEN_HOC": f"the {who}",
            "NGUOI_HOC": f"{REAL} {mo_ta} (a real person filmed on camera, not animated, not a cartoon)",
            "GIONG_HOC": f"a real {'child' if kid else 'adult'} {who}'s voice, around {hz}, native Mexican Spanish with English words kept in English, a little hesitant at first, brighter and more confident later",
            "NEN_HOC": NEN,
            "DONG_HOC": ("Their hands rest on the edge of the kitchen counter, only a tiny natural movement." if kid else "Their hands rest at the sink on a plate, only a tiny natural movement."),
            "POS_DAY": "TOP", "POS_HOC": "BOTTOM",
            "LUOT": [dict(x) for x in LUOT],
            "refs": {"NGUOI_HOC": ma, "NGUOI_DAY": bot_code},
        })
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK", OUT, len(res))
