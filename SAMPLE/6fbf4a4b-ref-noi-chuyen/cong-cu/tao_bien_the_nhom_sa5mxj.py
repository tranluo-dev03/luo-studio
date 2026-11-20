"""Nhóm sa5mxj (kịch bản goc): 6 người học Âu Mỹ (3 nam, 3 nữ, 20-30 tuổi) ngồi ghế sofa phòng khách, robot BOT-TALKA, hook "I am Portugal." -> "I am from Portugal.".
Toàn tiếng Anh, không câu nào bằng tiếng mẹ đẻ. Chạy: python tao_bien_the_nhom_sa5mxj.py (không sửa tay JSON)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "BIEN-THE-NHOM-sa5mxj.json")
A = "SAMPLE/6fbf4a4b-ref-noi-chuyen/anh/nhom-sa5mxj/"
APP = "LangLearn"
REAL = "a real, photorealistic live-action person (filmed on camera, not animated, not a cartoon)"

ROBOT = ("a humanoid AI robot with a glossy white armoured body and a smooth white female-looking face with softly glowing pale-blue eyes, "
         "a white baseball cap, a blue denim vest over a red plaid shirt, exposed black cables at the neck and joints, calm friendly expression")
NEN = ("a small apartment living room in the evening: an old grey fabric sofa, a plain white wall, a small TV and a blurred picture frame behind the sofa, "
       "warm yellow lamp light, nothing written anywhere")
NO_NATIVE = "speaking only English, no words in any other language"
SIT = ("{p} sits on the grey sofa facing the camera, relaxed, and uses natural hand gestures while talking like in everyday conversation "
       "(open palms, small pointing and counting movements), hands returning to the lap when still.")

# (tên, tả ngoại hình EN, giọng EN, đại từ chủ ngữ/sở hữu, ảnh, TEN_HOC)
NV = [
    ("nam1", f"{REAL}: a young white European man about 25, short blond hair, light stubble, pale skin, blue eyes, a grey hoodie under a yellow high-visibility vest",
     f"a young man's voice, a light baritone around 115-130 Hz, bright and slightly hesitant at first, {NO_NATIVE}, a faint Portuguese accent", "He", "NAM1", "the young man"),
    ("nam2", f"{REAL}: a young Latino man about 27, short black hair, light brown skin, dark eyes, a worn grey work jacket over a black t-shirt",
     f"a young man's voice, a warm medium baritone around 105-120 Hz, steady and friendly, {NO_NATIVE}, a faint Portuguese accent", "He", "NAM2", "the young man"),
    ("nam3", f"{REAL}: a young Black man about 24, very short black hair, dark brown skin, a grey short-sleeved work shirt with a chest pocket",
     f"a young man's voice, a deep smooth baritone around 95-110 Hz, calm and a little shy at first, {NO_NATIVE}, a faint Portuguese accent", "He", "NAM3", "the young man"),
    ("nu1", f"{REAL}: a young South-Asian-looking woman about 26, long dark wavy hair in a loose ponytail, brown skin, dark eyes, a white shirt under a black waistcoat",
     f"a young woman's voice, a clear light voice around 205-225 Hz, polite and a little nervous at first, {NO_NATIVE}, a faint Portuguese accent", "She", "NU1", "the young woman"),
    ("nu2", f"{REAL}: a young white woman about 22, short blond pixie haircut, fair skin, light blue eyes, a dark-green polo shirt",
     f"a young woman's voice, a bright voice around 215-235 Hz, quick and cheerful, {NO_NATIVE}, a faint Portuguese accent", "She", "NU2", "the young woman"),
    ("nu3", f"{REAL}: a young Black woman about 28, short curly black hair, dark brown skin, a light grey polo shirt",
     f"a young woman's voice, a warm low-mid voice around 190-205 Hz, confident and relaxed, {NO_NATIVE}, a faint Portuguese accent", "She", "NU3", "the young woman"),
]

L = lambda who, text, emo, **k: dict({"who": who, "text": text, "emo": emo, "fx": "none"}, **k)
LUOT = [
    L("day", "Where are you from?", "curious"),
    L("hoc", "I am Portugal.", "cheerful", fx="wrong", c="red", icon="x"),
    L("day", "Almost. Better say: I am from Portugal.", "warm", fx="right", c="green", icon="check", to="I am from Portugal"),
    L("hoc", "I always mix that up.", "embarrassed"),
    L("day", "That's what I'm here for, to help you speak well.", "warm"),
    L("hoc", "But I don't have money.", "worried"),
    L("day", f"What? You don't need money. {APP} lets you practice English for free, unlike expensive apps and courses.", "reassuring"),
    L("hoc", "Seriously?", "surprised"),
    L("day", "Of course, no tricks. Only real conversation practice with your AI tutor.", "friendly"),
    L("hoc", "Like a real tutor?", "curious"),
    L("day", "Yes. I correct your grammar and pronunciation, and I help you speak with confidence.", "encouraging"),
    L("hoc", f"Okay, so I'm going to download {APP} right now.", "confident"),
    L("day", "Good decision. Let's speak English together.", "upbeat"),
]

res = []
for ten, nguoi, giong, p, anh, ten_hoc in NV:
    res.append({
        "name": f"sa5mxj-{ten}",
        "TEN_DAY": "the AI tutor",
        "NGUOI_DAY": ROBOT,
        "GIONG_DAY": "a calm, clear, warm male-leaning synthetic-but-natural voice, a baritone around 130-150 Hz, American English, patient and encouraging, speaking only English",
        "NEN_DAY": "a plain pure black background",
        "TEN_HOC": ten_hoc,
        "NGUOI_HOC": nguoi,
        "GIONG_HOC": giong,
        "NEN_HOC": NEN,
        "DONG_HOC": SIT.format(p=p),
        "POS_DAY": "TOP",
        "POS_HOC": "BOTTOM",
        "LUOT": [dict(x) for x in LUOT],
        "refs": {"NGUOI_DAY": [A + "BOT.png"], "NGUOI_HOC": [A + anh + ".png"], "NEN_HOC": [A + "PHONGKHACH.png"]},
    })
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK", OUT, len(res))
