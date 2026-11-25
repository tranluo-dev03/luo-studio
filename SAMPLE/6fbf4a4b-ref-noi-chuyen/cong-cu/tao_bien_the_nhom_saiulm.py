"""Nhóm saiulm (kịch bản goc): lời tiếng Ả Rập xen "I am United Arab Emirates." / "I am from the United Arab Emirates." và tên app Talka AI.
40 biến thể = 20 nữ India (bot BOT-TALKA-DEF-INDIA-02) + 20 nam India (bot BOT-TALKA-DEF-INDIA-03), đủ mã 20-30t và 30-45t số 01-10 (mã kho nhân vật).
Chạy: python tao_bien_the_nhom_saiulm.py (không sửa tay JSON)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "BIEN-THE-NHOM-saiulm.json")
REAL = "a real, photorealistic live-action Indian"
BOT_A = ("a humanoid AI robot with a glossy white armoured head with a smooth white face, softly glowing pale-blue eyes and small white ear-pieces, "
         "exposed black cables and white mechanical arms, wearing a maroon waistcoat over a cream kurta and white trousers, calm friendly expression")
BOT_B = ("a humanoid AI robot with a glossy white armoured head with a smooth white face, softly glowing pale-blue eyes and small white ear-pieces, "
         "exposed black cables and white mechanical arms and legs, wearing a long purple embroidered kurta coat with silver patterns, calm friendly expression")
GD_A = "a calm, clear, warm male-leaning synthetic-but-natural voice, a baritone around 130-150 Hz, speaking Arabic with English words kept in English, patient and encouraging"
GD_B = "a calm, clear, warm female-leaning synthetic-but-natural voice, around 205-225 Hz, speaking Arabic with English words kept in English, patient and encouraging"
NEN = "a bright cream-coloured kitchen with wooden cabinets and a granite counter, a sink in front of the person"
DONG = "Their hands rest at the sink on a plate, only a tiny natural movement."

# (mã kho, ngoại hình EN theo ảnh, cao độ giọng)
NU = [
    ("NU-20-30-IND-01", "woman about 24, tan skin, dark hair in a long side braid, a dark teal-navy short-sleeved collared shirt and black trousers", "215-230 Hz"),
    ("NU-20-30-IND-02", "woman about 28, a fuller round face, dark hair tied back, a pink linen kurta over white salwar trousers", "200-215 Hz"),
    ("NU-20-30-IND-03", "woman about 23, slim, a very long dark braid, an orange kurta and blue jeans", "220-235 Hz"),
    ("NU-20-30-IND-04", "woman about 27, hair in a low braided ponytail, a purple kurta over dark grey trousers", "205-220 Hz"),
    ("NU-20-30-IND-05", "woman about 26, short curly dark hair, a yellow high-visibility vest over a navy t-shirt and black trousers", "195-210 Hz"),
    ("NU-20-30-IND-06", "woman about 22, dark hair in a high ponytail, a royal-blue polo shirt, black trousers and white sneakers", "215-230 Hz"),
    ("NU-20-30-IND-07", "woman about 27, hair tied back, a white short-sleeved collared shirt and grey trousers", "205-220 Hz"),
    ("NU-20-30-IND-08", "woman about 29, a fuller figure, a long dark braid over one shoulder, a navy kurta over navy salwar trousers", "195-210 Hz"),
    ("NU-20-30-IND-09", "woman about 23, curly dark hair in a bun, a lavender long kurta over white leggings", "215-230 Hz"),
    ("NU-20-30-IND-10", "woman about 28, hair tied back, a maroon long-sleeved shirt and grey trousers", "200-215 Hz"),
    ("NU-30-45-IND-01", "woman about 38, hair neatly parted and pinned back, a long dark navy kurta over grey trousers", "190-205 Hz"),
    ("NU-30-45-IND-02", "woman about 42, a long dark braid, a yellow high-visibility vest over a teal t-shirt", "185-200 Hz"),
    ("NU-30-45-IND-03", "woman about 36, hair pulled back, a mustard-yellow kurta over blue jeans", "200-215 Hz"),
    ("NU-30-45-IND-04", "woman about 44, short dark hair, a sage-green short-sleeved shirt and black trousers", "180-195 Hz"),
    ("NU-30-45-IND-05", "woman about 40, a long dark braid, a magenta kurta over white salwar trousers", "195-210 Hz"),
    ("NU-30-45-IND-06", "woman about 34, hair in a low ponytail, an orange polo shirt and black trousers", "200-215 Hz"),
    ("NU-30-45-IND-07", "woman about 45, hair in a bun, a long beige kurta-coat over brown trousers", "180-195 Hz"),
    ("NU-30-45-IND-08", "woman about 37, dark hair pulled back, a white short-sleeved shirt and white trousers", "195-210 Hz"),
    ("NU-30-45-IND-09", "woman about 41, hair tied back, a black short-sleeved shirt and grey trousers", "185-200 Hz"),
    ("NU-30-45-IND-10", "woman about 45, a long dark braid, a maroon kurta over grey trousers", "180-195 Hz"),
]
NAM = [
    ("NAM-20-30-IND-01", "man about 22, neat short black hair, clean-shaven, a cream kurta and black trousers", "125-140 Hz"),
    ("NAM-20-30-IND-02", "man about 26, black hair, a thin moustache, a grey jacket over a yellow t-shirt and black jeans", "115-130 Hz"),
    ("NAM-20-30-IND-03", "man about 21, slim, short black hair, clean-shaven, a dark-green t-shirt and black cargo trousers", "130-145 Hz"),
    ("NAM-20-30-IND-04", "man about 29, heavy build, a thick black moustache, a red long-sleeved henley shirt and grey jeans", "100-115 Hz"),
    ("NAM-20-30-IND-05", "man about 27, slim, wavy black hair, a black chef's jacket and white trousers", "120-135 Hz"),
    ("NAM-20-30-IND-06", "man about 29, stout, a thick black moustache, a mint-green short-sleeved shirt and navy trousers", "105-120 Hz"),
    ("NAM-20-30-IND-07", "man about 23, slim, dark skin, short black hair, a mustard-yellow kurta and grey trousers", "125-140 Hz"),
    ("NAM-20-30-IND-08", "man about 24, curly dark hair, clean-shaven, a purple short-sleeved shirt and black trousers", "120-135 Hz"),
    ("NAM-20-30-IND-09", "man about 30, heavy build, a big moustache, hair slicked back, a navy waistcoat over a navy kurta and white trousers", "95-110 Hz"),
    ("NAM-20-30-IND-10", "man about 21, slim, straight black fringe, clean-shaven, a sage-green kurta and dark brown trousers", "125-140 Hz"),
    ("NAM-30-45-IND-01", "man about 40, shaved head, a big handlebar moustache, a navy collared shirt and khaki trousers", "95-110 Hz"),
    ("NAM-30-45-IND-02", "man about 38, thin, short black hair, a yellow high-visibility vest over a dark-green t-shirt", "110-125 Hz"),
    ("NAM-30-45-IND-03", "man about 42, stout, a trimmed moustache, a long dark-green kurta and brown trousers", "100-115 Hz"),
    ("NAM-30-45-IND-04", "man about 44, grey-streaked short hair, a light-blue short-sleeved shirt and grey cargo trousers", "105-120 Hz"),
    ("NAM-30-45-IND-05", "man about 35, slim, tousled black hair, a black short-sleeved shirt and dark jeans", "115-130 Hz"),
    ("NAM-30-45-IND-06", "man about 33, short black hair, a full black beard, a dark-brown shirt and black trousers", "105-120 Hz"),
    ("NAM-30-45-IND-07", "man about 44, stout, grey-streaked hair, a moustache, a teal kurta and grey trousers", "95-110 Hz"),
    ("NAM-30-45-IND-08", "man about 32, slim, short black hair, a moustache, a red-and-white striped shirt and blue jeans", "115-130 Hz"),
    ("NAM-30-45-IND-09", "man about 36, slim, curly black hair, a cream kurta and white trousers", "110-125 Hz"),
    ("NAM-30-45-IND-10", "man about 45, grey hair, a moustache, an olive-green kurta and khaki trousers", "100-115 Hz"),
]

L = lambda who, text, emo, **k: dict({"who": who, "text": text, "emo": emo, "fx": "none"}, **k)
LUOT = [
    L("day", "Where are you from?", "curious"),
    L("hoc", "I am United Arab Emirates.", "cheerful", fx="wrong", c="red", icon="x", to="I am United Arab Emirates"),
    L("day", "إجابة قريبة من الصواب! لكن الأفضل أن نقول: \"I am from the United Arab Emirates.\"", "warm", fx="right", c="green", icon="check", to="I am from the United Arab Emirates"),
    L("hoc", "آه، دائمًا ما أقع في هذا الخطأ.", "embarrassed"),
    L("day", "لهذا أنا هنا، للمساعدة على التحدث بالإنجليزية بشكل أفضل.", "warm"),
    L("hoc", "لكن ليس لدي مال.", "worried"),
    L("day", "ماذا؟ لا حاجة إلى دفع المال! مع Talka AI، يمكن ممارسة الإنجليزية مجانًا، بدلًا من التطبيقات والدورات المكلفة.", "reassuring"),
    L("hoc", "حقًا؟", "surprised"),
    L("day", "بالتأكيد! لا توجد شروط خفية. فقط محادثات حقيقية باللغة الإنجليزية مع مدرس بالذكاء الاصطناعي.", "friendly"),
    L("hoc", "مثل المدرس الحقيقي؟", "curious"),
    L("day", "نعم! مع Talka AI، يتم تصحيح أخطاء القواعد والنطق، مما يساعد على التحدث بالإنجليزية بثقة.", "encouraging"),
    L("hoc", "حسنًا، سأقوم بتنزيل Talka AI الآن.", "confident"),
    L("day", "قرار رائع! لنتحدث الإنجليزية معًا.", "upbeat"),
]

res = []
for lst, bot, bot_code, gd, who, vo in ((NU, BOT_A, "BOT-TALKA-DEF-INDIA-02", GD_A, "woman", "woman's"), (NAM, BOT_B, "BOT-TALKA-DEF-INDIA-03", GD_B, "man", "man's")):
    for ma, mo_ta, hz in lst:
        short = ma.lower().replace("-ind-", "").replace("-", "")  # nu203001
        res.append({
            "name": f"saiulm-{short}",
            "TEN_DAY": "the AI tutor", "NGUOI_DAY": bot, "GIONG_DAY": gd, "NEN_DAY": "a plain pure black background",
            "TEN_HOC": f"the {who}",
            "NGUOI_HOC": f"{REAL} {mo_ta} (a real person filmed on camera, not animated, not a cartoon)",
            "GIONG_HOC": f"a real {vo} voice, around {hz}, native Arabic (Gulf) with English words kept in English, a little hesitant at first, brighter and more confident later",
            "NEN_HOC": NEN, "DONG_HOC": DONG, "POS_DAY": "TOP", "POS_HOC": "BOTTOM",
            "LUOT": [dict(x) for x in LUOT],
            "refs": {"NGUOI_HOC": ma, "NGUOI_DAY": bot_code},
        })
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK", OUT, len(res))
