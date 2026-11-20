"""Nhóm w8sqp4 (kịch bản goc): lời Hindi (Devanagari) xen "I am India." / "I am from India." và tên app Talka AI.
20 biến thể = 10 nữ India (bot BOT-TALKA-DEF-INDIA-02) + 10 nam India (bot BOT-TALKA-DEF-INDIA-01); mỗi nhóm 5 người 20-30t + 5 người 30-45t (mã kho nhân vật).
Chạy: python tao_bien_the_nhom_w8sqp4.py (không sửa tay JSON)."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "BIEN-THE-NHOM-w8sqp4.json")
REAL = "a real, photorealistic live-action Indian"
BOT_A = ("a humanoid AI robot with a glossy white armoured head with a smooth white face, softly glowing pale-blue eyes and small white ear-pieces, "
         "exposed black cables and white mechanical arms, wearing a maroon waistcoat over a cream kurta and white trousers, calm friendly expression")
BOT_B = ("a humanoid AI robot with a glossy white armoured head with a smooth white face, softly glowing pale-blue eyes and small white ear-pieces, "
         "exposed black cables and white mechanical arms, wearing a pink silk saree with a gold border, calm friendly expression")
GD_A = "a calm, clear, warm male-leaning synthetic-but-natural voice, a baritone around 130-150 Hz, speaking Hindi with English words kept in English, patient and encouraging"
GD_B = "a calm, clear, warm female-leaning synthetic-but-natural voice, around 205-225 Hz, speaking Hindi with English words kept in English, patient and encouraging"
NEN = "a bright cream-coloured kitchen with wooden cabinets and a granite counter, a sink in front of the person"
DONG = "Their hands rest at the sink on a plate, only a tiny natural movement."

# (mã kho, ngoại hình EN theo ảnh, cao độ giọng)
NU = [
    ("NU-20-30-IND-01", "woman about 24, tan skin, dark hair in a long side braid, a dark teal-navy short-sleeved collared shirt and black trousers", "215-230 Hz"),
    ("NU-20-30-IND-02", "woman about 28, a fuller round face, dark hair tied back, a pink linen kurta over white salwar trousers", "200-215 Hz"),
    ("NU-20-30-IND-03", "woman about 23, slim, a very long dark braid, an orange kurta and blue jeans", "220-235 Hz"),
    ("NU-20-30-IND-04", "woman about 27, hair in a low braided ponytail, a purple kurta over dark grey trousers", "205-220 Hz"),
    ("NU-20-30-IND-05", "woman about 26, short curly dark hair, a yellow high-visibility vest over a navy t-shirt and black trousers", "195-210 Hz"),
    ("NU-30-45-IND-01", "woman about 38, hair neatly parted and pinned back, a long dark navy kurta over grey trousers", "190-205 Hz"),
    ("NU-30-45-IND-02", "woman about 42, a long dark braid, a yellow high-visibility vest over a teal t-shirt", "185-200 Hz"),
    ("NU-30-45-IND-03", "woman about 36, hair pulled back, a mustard-yellow kurta over blue jeans", "200-215 Hz"),
    ("NU-30-45-IND-04", "woman about 44, short dark hair, a sage-green short-sleeved shirt and black trousers", "180-195 Hz"),
    ("NU-30-45-IND-05", "woman about 40, a long dark braid, a magenta kurta over white salwar trousers", "195-210 Hz"),
]
NAM = [
    ("NAM-20-30-IND-01", "man about 22, neat short black hair, clean-shaven, a cream kurta and black trousers", "125-140 Hz"),
    ("NAM-20-30-IND-02", "man about 26, black hair, a thin moustache, a grey jacket over a yellow t-shirt and black jeans", "115-130 Hz"),
    ("NAM-20-30-IND-03", "man about 21, slim, short black hair, clean-shaven, a dark-green t-shirt and black cargo trousers", "130-145 Hz"),
    ("NAM-20-30-IND-04", "man about 29, heavy build, a thick black moustache, a red long-sleeved henley shirt and grey jeans", "100-115 Hz"),
    ("NAM-20-30-IND-05", "man about 27, slim, wavy black hair, a black chef's jacket and white trousers", "120-135 Hz"),
    ("NAM-30-45-IND-01", "man about 40, shaved head, a big handlebar moustache, a navy collared shirt and khaki trousers", "95-110 Hz"),
    ("NAM-30-45-IND-02", "man about 38, thin, short black hair, a yellow high-visibility vest over a dark-green t-shirt", "110-125 Hz"),
    ("NAM-30-45-IND-03", "man about 42, stout, a trimmed moustache, a long dark-green kurta and brown trousers", "100-115 Hz"),
    ("NAM-30-45-IND-04", "man about 44, grey-streaked short hair, a light-blue short-sleeved shirt and grey cargo trousers", "105-120 Hz"),
    ("NAM-30-45-IND-05", "man about 35, slim, tousled black hair, a black short-sleeved shirt and dark jeans", "115-130 Hz"),
]

L = lambda who, text, emo, **k: dict({"who": who, "text": text, "emo": emo, "fx": "none"}, **k)
LUOT = [
    L("day", "Where are you from?", "curious"),
    L("hoc", "I am India.", "cheerful", fx="wrong", c="red", icon="x"),
    L("day", "लगभग सही! लेकिन इसे कहने का सही तरीका है, \"I am from India.\"", "warm", fx="right", c="green", icon="check", to="I am from India"),
    L("hoc", "आह, मुझसे हमेशा यही गलती हो जाती है।", "embarrassed"),
    L("day", "इसीलिए तो मैं यहाँ हूँ, ताकि आपकी अंग्रेज़ी बेहतर हो सके।", "warm"),
    L("hoc", "लेकिन मेरे पास पैसे नहीं हैं।", "worried"),
    L("day", "क्या? आपको पैसे देने की ज़रूरत ही नहीं है। महंगे ऐप्स और कोर्सेज़ के बजाय, Talka AI पर अंग्रेज़ी की प्रैक्टिस बिल्कुल फ्री है।", "reassuring"),
    L("hoc", "सच में?", "surprised"),
    L("day", "बिल्कुल! कोई छिपी हुई शर्त नहीं है। बस अपने AI ट्यूटर के साथ असली अंग्रेज़ी बातचीत की प्रैक्टिस।", "friendly"),
    L("hoc", "एक असली ट्यूटर की तरह?", "curious"),
    L("day", "हाँ! Talka AI से आपकी ग्रामर और उच्चारण में सुधार होता है और आत्मविश्वास के साथ अंग्रेज़ी बोलने में मदद मिलती है।", "encouraging"),
    L("hoc", "ठीक है, तो अभी Talka AI डाउनलोड कर लेते हैं।", "confident"),
    L("day", "बहुत अच्छा फैसला! चलिए, साथ में अंग्रेज़ी बोलें।", "upbeat"),
]

res = []
for lst, bot, bot_code, gd, who, vo in ((NU, BOT_A, "BOT-TALKA-DEF-INDIA-02", GD_A, "woman", "woman's"), (NAM, BOT_B, "BOT-TALKA-DEF-INDIA-01", GD_B, "man", "man's")):
    for ma, mo_ta, hz in lst:
        short = ma.lower().replace("-ind-", "").replace("-", "")  # nu203001
        res.append({
            "name": f"w8sqp4-{short}",
            "TEN_DAY": "the AI tutor", "NGUOI_DAY": bot, "GIONG_DAY": gd, "NEN_DAY": "a plain pure black background",
            "TEN_HOC": f"the {who}",
            "NGUOI_HOC": f"{REAL} {mo_ta} (a real person filmed on camera, not animated, not a cartoon)",
            "GIONG_HOC": f"a real Indian {vo} voice, around {hz}, native Hindi with English words kept in English, a little hesitant at first, brighter and more confident later",
            "NEN_HOC": NEN, "DONG_HOC": DONG, "POS_DAY": "TOP", "POS_HOC": "BOTTOM",
            "LUOT": [dict(x) for x in LUOT],
            "refs": {"NGUOI_HOC": ma, "NGUOI_DAY": bot_code},
        })
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK", OUT, len(res))
