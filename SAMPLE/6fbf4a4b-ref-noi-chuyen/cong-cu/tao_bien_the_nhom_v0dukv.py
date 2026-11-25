"""Nhóm v0dukv (kịch bản goc): lời tiếng Tây Ban Nha xen "I am Mexico." / "I am from Mexico." và Talka AI; 50 người Latinh (mã kho nhân vật) với 4 bot Talka.
Người dùng ghi 60 mã (4 bot x 15 mã) nhưng số lượng 50: lấy ĐỦ 40 người lớn (20-30t, 30-45t) + 10 trẻ 5-10t (nhóm A 01-03, B 06-07, C 01-03, D 06-07).
Chạy: python tao_bien_the_nhom_v0dukv.py (không sửa tay JSON)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "BIEN-THE-NHOM-v0dukv.json")
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
A = [  # NAM, bot AVA-LATIN-03
    ("NAM-20-30-LAT-01", "man about 24, short black hair, a yellow high-visibility vest over a navy t-shirt, black trousers", "120-135 Hz"),
    ("NAM-20-30-LAT-02", "man about 25, short black hair, a dark-brown polo shirt and grey cargo trousers", "115-130 Hz"),
    ("NAM-20-30-LAT-03", "man about 24, slim, black hair, a light-blue polo shirt and dark jeans", "125-140 Hz"),
    ("NAM-20-30-LAT-04", "man about 28, long black hair tied back, a brown plaid flannel shirt and blue jeans", "110-125 Hz"),
    ("NAM-20-30-LAT-05", "man about 22, wavy dark hair, a grey chef's jacket and black trousers", "125-140 Hz"),
    ("NAM-30-45-LAT-01", "man about 40, short black hair, a denim jacket over a white t-shirt and black jeans", "105-120 Hz"),
    ("NAM-30-45-LAT-02", "man about 34, wavy dark hair, a grey button shirt with rolled sleeves and black jeans", "110-125 Hz"),
    ("NAM-30-45-LAT-03", "Black man about 38, short curly hair, a black-and-grey striped long-sleeved top and jeans", "100-115 Hz"),
    ("NAM-30-45-LAT-04", "stocky Black man about 42, short hair, a black short-sleeved shirt and dark jeans", "95-110 Hz"),
    ("NAM-30-45-LAT-05", "light-skinned man about 44, light-brown hair, a blue denim shirt and white trousers", "105-120 Hz"),
    ("NAM-5-10-LAT-01", "boy about 7, curly black hair, a red t-shirt and jeans", "250-270 Hz"),
    ("NAM-5-10-LAT-02", "boy about 9, wavy dark hair, a blue hoodie and grey trousers", "240-260 Hz"),
    ("NAM-5-10-LAT-03", "boy about 8, curly dark hair, a white polo shirt and khaki trousers", "245-265 Hz"),
]
B = [  # NAM, bot DEF-LATIN-02
    ("NAM-20-30-LAT-06", "man about 26, short black hair, a light-blue short-sleeved work shirt and black trousers", "115-130 Hz"),
    ("NAM-20-30-LAT-07", "stocky man about 22, dark hair, an orange long-sleeved shirt and grey trousers", "110-125 Hz"),
    ("NAM-20-30-LAT-08", "slim man about 23, wavy brown hair, a yellow polo shirt and black trousers", "125-140 Hz"),
    ("NAM-20-30-LAT-09", "man about 29, dark hair tied back, a black overshirt and grey trousers", "105-120 Hz"),
    ("NAM-20-30-LAT-10", "man about 27, long dark hair, a beige short-sleeved shirt and olive trousers", "115-130 Hz"),
    ("NAM-30-45-LAT-06", "slim dark-skinned man about 33, short black hair, a teal polo shirt and grey cargo trousers", "110-125 Hz"),
    ("NAM-30-45-LAT-07", "man about 45, long black hair tied back, a white guayabera shirt and dark trousers", "95-110 Hz"),
    ("NAM-30-45-LAT-08", "man about 35, wavy brown hair, a red plaid shirt and blue jeans", "110-125 Hz"),
    ("NAM-30-45-LAT-09", "stout man about 42, black hair, a rust-orange short-sleeved shirt and dark grey trousers", "95-110 Hz"),
    ("NAM-30-45-LAT-10", "man about 40, black hair, a beige utility vest over a light-blue t-shirt and green trousers", "105-120 Hz"),
    ("NAM-5-10-LAT-06", "boy about 7, curly dark hair, an orange t-shirt and jeans", "250-270 Hz"),
    ("NAM-5-10-LAT-07", "boy about 8, curly dark hair, a navy sweater and jeans", "245-265 Hz"),
]
C = [  # NU, bot AVA-LATIN-02
    ("NU-20-30-LAT-01", "woman about 23, dark hair tied back, a white embroidered blouse and blue jeans", "205-225 Hz"),
    ("NU-20-30-LAT-02", "woman about 26, curly dark hair in an updo, a yellow floral blouse, jeans and white sneakers", "210-230 Hz"),
    ("NU-20-30-LAT-03", "woman about 25, a long black braid, a red short-sleeved shirt and dark jeans", "210-230 Hz"),
    ("NU-20-30-LAT-04", "woman about 29, a long braid, a worn denim shirt and brown trousers", "195-215 Hz"),
    ("NU-20-30-LAT-05", "woman about 28, short curly dark hair, a turquoise short-sleeved shirt and blue jeans", "200-220 Hz"),
    ("NU-30-45-LAT-01", "woman about 35, dark hair pulled back, a grey-and-black short-sleeved shirt and black trousers", "195-210 Hz"),
    ("NU-30-45-LAT-02", "Black woman about 38, small braided hair, a white chef's jacket and checkered trousers", "190-205 Hz"),
    ("NU-30-45-LAT-03", "woman about 42, wavy dark hair, a green jacket over a black top with a blue neckerchief, and jeans", "185-200 Hz"),
    ("NU-30-45-LAT-04", "woman about 40, a long dark braid, a white work coat and white trousers", "190-205 Hz"),
    ("NU-30-45-LAT-05", "woman about 33, long wavy dark hair, a yellow high-visibility vest over a navy shirt and khaki trousers", "200-215 Hz"),
    ("NU-5-10-LAT-01", "girl about 8, brown hair in a ponytail, a white t-shirt and jeans", "270-290 Hz"),
    ("NU-5-10-LAT-02", "girl about 9, two long dark braids, a yellow t-shirt and jeans", "260-280 Hz"),
    ("NU-5-10-LAT-03", "girl about 7, black curly hair in afro puffs, a red t-shirt and jeans", "275-295 Hz"),
]
D = [  # NU, bot DEF-LATIN-03
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
    ("NU-5-10-LAT-06", "Black girl about 7, hair in two afro puffs, an orange t-shirt and a white pleated skirt", "270-290 Hz"),
    ("NU-5-10-LAT-07", "girl about 8, dark hair in a half ponytail, a denim jacket over a white t-shirt and jeans", "265-285 Hz"),
]
GROUPS = [(A, "BOT-TALKA-AVA-LATIN-03"), (B, "BOT-TALKA-DEF-LATIN-02"), (C, "BOT-TALKA-AVA-LATIN-02"), (D, "BOT-TALKA-DEF-LATIN-03")]

# A, B, C, D mỗi nhóm giữ đủ người lớn; trẻ: A 01-03, B 06-07, C 01-03, D 06-07 (đã tách sẵn ở trên). Tổng = 13+12+13+12 = 50.
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
            "name": "v0dukv-" + ma.lower().replace("-lat-", "").replace("-", ""),
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
