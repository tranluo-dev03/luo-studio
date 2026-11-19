"""Sinh SAMPLE/phong-van-pho-hindi/BIEN-THE-PHONG-VAN-PHO-HINDI.json từ bảng NHAN_VAT + lời thoại luot().
Chạy:  runtime\\python.exe SAMPLE\\phong-van-pho-hindi\\cong-cu\\tao_bien_the.py
Video mẫu "1510_interview street hindi_005 (11)" có phụ đề Malayalam; bản này viết lại lời bằng tiếng HINDI (chữ Devanagari) xen từ tiếng Anh, theo đúng mạch
và nhịp của video mẫu (26 lượt: 11 phần 1 + 15 phần 2). Từ tiếng Anh viết chữ Latin để Muse đọc đúng.
Phóng viên luôn là NAM, người bán luôn là NỮ (khác giới: người bán không nhép theo giọng phóng viên quay lưng; kịch bản tả phóng viên bằng "his").
3 biến thể: 01 bám sát video mẫu (người bán nữ ~50), 02 người bán nữ trẻ, 03 người bán nữ lớn tuổi, mỗi người một quầy và một thành phố.
Ảnh tham chiếu: robot = anh/robot-talka.png (Talka, như thể loại Malayalam); PV + người bán = Muse gen photoreal nền xanh (cong-cu/gen_anh.py)."""
import json
import os
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-PHONG-VAN-PHO-HINDI.json")


def luot(city):
    """city: thành phố trong câu 'I am <city>' -> 'I am from <city>'. Người bán nữ (động từ giống cái)."""
    return [
        # PHẦN 1: phỏng vấn đường phố (11 cảnh)
        ("pv", 1, "अचानक को अंग्रेज़ी में क्या कहते हैं?", "playful, curious"),
        ("hoc", 1, "Suddenly.", "confident"),
        ("pv", 1, "तुरंत?", "playful"),
        ("hoc", 1, "Immediately.", "confident"),
        ("pv", 1, "अच्छा, ये बताइए... वरना?", "playful"),
        ("hoc", 1, "Otherwise.", "confident"),
        ("pv", 1, "इसलिए?", "playful"),
        ("hoc", 1, "Therefore.", "proud"),
        ("pv", 1, "आपने तो कहा था कि एक महीने पहले आपको अंग्रेज़ी का एक शब्द भी नहीं आता था!", "impressed"),
        ("hoc", 1, "Yeah, one month ago the only English I heard was from TV. And now I am talking fluently.", "proud"),
        ("hoc", 1, "फ़र्राटेदार अंग्रेज़ी बोलने का राज़ जानना है? पहले दिन से बोलना शुरू करो। आओ, मैं दिखाती हूँ।", "cheerful"),
        # PHẦN 2: robot ô trên, người bán ô dưới (15 cảnh)
        ("day", 2, "सिर्फ़ एक महीने में आप native speakers की तरह अंग्रेज़ी बोल सकते हैं, पता है? ये कोई जादू नहीं है।", "enthusiastic"),
        ("day", 2, "ये ऐसा ऐप है जो बोलते-बोलते आपकी ग़लतियाँ सुधारता है, और आपको सीखने का पता भी नहीं चलता।", "warm"),
        ("day", 2, "चलिए, एक बार try करते हैं। क्या आपको अंग्रेज़ी बोलना आता है?", "friendly"),
        ("hoc", 2, "थोड़ा-थोड़ा।", "hesitant"),
        ("day", 2, "Where are you from?", "friendly, curious"),
        ("hoc", 2, f"I am {city}.", "unsure"),
        ("day", 2, f"लगभग सही है। लेकिन I am from {city} कहें तो और भी अच्छा रहेगा।", "encouraging"),
        ("hoc", 2, "अरे, मुझे हमेशा यहीं पर confusion होता है।", "embarrassed"),
        ("day", 2, "इसीलिए तो मैं यहाँ हूँ, आपको सही बोलना सिखाने के लिए।", "reassuring"),
        ("hoc", 2, "लेकिन ये तो बहुत expensive होगा ना?", "worried"),
        ("day", 2, "बिल्कुल नहीं! आम English क्लास से ये सात गुना सस्ता है।", "reassuring"),
        ("day", 2, "रोज़ सिर्फ़ पंद्रह से बीस मिनट practice करना काफ़ी है।", "warm"),
        ("day", 2, "हिंदी में practice करने से आप धीरे-धीरे बहुत confident हो जाएँगे। ये AI टीचर के साथ असली English practice है।", "enthusiastic"),
        ("hoc", 2, "मतलब, एक real टीचर जैसा?", "curious"),
        ("day", 2, "हाँ, ये आपके grammar और pronunciation को सही करेगा और confidence के साथ बोलने में मदद करेगा।", "confident, warm"),
    ]


AIVA = ("a sleek white humanoid AI robot teacher, exactly as in its reference photo: a smooth glossy white head with fine panel seams and no hair, a realistic "
        "young woman's face with pale light blue eyes, soft lips that open and move like a real person's whenever it speaks and a calm warm expression, a white over-ear headset with a thin microphone boom curving to "
        "its mouth, a black ribbed mechanical neck, white hexagon-plated armour on the shoulders and chest with black mechanical joints and thin glowing light blue accent lines")
GIONG_AIVA = ("a bright, warm young woman's voice (around 210-230 Hz) with a light synthetic sheen, clear and lively like a friendly teacher, native Hindi, "
              "says the English words clearly with a light Indian English accent")

# Ảnh gen từ chính các mô tả này (ANH_MO_TA) để ảnh và prompt khớp nhau.
PV_MO_TA = ("a young Indian man about twenty-eight years old, short neat black hair, thin black-framed glasses, a short trimmed beard, a pink-and-white "
            "plaid cotton shirt with rolled sleeves, a black backpack on his back")
BAN = {
    "V1": ("a north Indian woman about fifty years old, warm brown skin, black hair with a few grey strands parted in the middle and tied in a low bun, a small "
           "red bindi, a kind round face; a magenta-pink short-sleeved blouse and a brown-and-grey checked cotton saree with a thin red border draped over her "
           "left shoulder; photorealistic skin and fabric"),
    "V2": ("a north Indian woman about twenty-eight years old, medium brown skin, long black hair in a single braid over her right shoulder, a small black bindi, "
           "a lively oval face; a mustard-yellow cotton kurta with white block print and a light green cotton dupatta draped over both shoulders; photorealistic "
           "skin and fabric"),
    "V3": ("an elderly north Indian woman about sixty-two years old, wheat-brown skin with laugh lines, grey hair pulled back in a tight bun, a round "
           "gold nose stud, a gentle weathered face; a plain teal-blue cotton saree with a thin orange border, the end draped over her left shoulder; "
           "photorealistic skin and fabric"),
}
ANH_MO_TA = {"PV": PV_MO_TA, **BAN}

GIONG_BAN = {
    "V1": ("a real middle-aged north Indian woman's voice (around 200-230 Hz), warm, lively and a little husky, native Hindi, says the English words like a "
           "proud learner; a real person, not an actress"),
    "V2": ("a real young north Indian woman's voice (around 220-250 Hz), bright, quick and cheerful, native Hindi, says the English words like an eager "
           "learner; a real person, not an actress"),
    "V3": ("a real elderly north Indian woman's voice (around 190-215 Hz), warm, a little husky and unhurried, native Hindi, says the English words "
           "carefully like a proud learner; a real person, not an actress"),
}

CHUNG = {
    # phần 1
    "TEN_PV": "the interviewer", "VAI_PV": "street interviewer", "POS_PV": "LEFT foreground, seen from behind",
    "NGUOI_PV": PV_MO_TA,
    "GIONG_PV": ("a real young north Indian man's voice, light baritone (around 150-180 Hz), friendly and playful like a street-interview host, native Hindi; "
                 "a real person, not an announcer"),
    "QUAY_LUNG_PV": "1",
    "NHIN_PV": ("keeps his face pointed at the woman's face, to the right and slightly down, the camera seeing only the back and the right edge of his head; "
                "he never turns toward the camera"),
    "NGHE_PV": "holds the microphone still toward the woman and keeps his face pointed at her, his head still, the camera seeing only the back of his head",
    "DAO_MIC": "a plain black handheld microphone with no logo",
    "VAI_HOC": "street vendor",
    "POS_HOC": "CENTRE-RIGHT, behind the cart",
    "NHIN_HOC": "looks at the interviewer's face, to the left, in three-quarter view, and never looks at the camera",
    "SHE_HOC": "she", "HER_HOC": "her", "HERO_HOC": "her", "SELF_HOC": "herself",
    # phần 2
    "TEN_DAY": "the AI tutor", "NGUOI_DAY": AIVA, "GIONG_DAY": GIONG_AIVA,
    "NEN_DAY": ("a deep navy-to-violet gradient backdrop with one thin glowing purple circular ring behind the head and a few tiny glowing dots along the ring, "
                "nothing else"),
    "TEN_HOC": "the woman",
}

# Quầy + việc tay + nơi + nền selfie theo từng người bán
QUAY = {
    "V1": dict(
        DAO_GANG="She wears thin clear disposable plastic gloves on both hands.",
        TAY_HOC="her gloved hands resting above the pots",
        VIEC_HOC="keeps gently shaping a small ball of filling between her gloved fingers above the pots",
        VIEC2_HOC="puts the small ball of filling back into the pot",
        DAO_GIU="Her gloved hands stay above the steel pots on the cart.",
        DAO_XE=("a stainless-steel street-food push cart with several round steel pots and bowls of spiced fillings, chutneys and fried snacks, a few steel ladles "
                "in the pots, a stack of small steel plates"),
        NEN_PHO=("a quiet old street in a north Indian town on an overcast morning, slightly out of focus: weathered two-storey shophouses with balconies and closed "
                 "rolling shutters, a faded blue awning, tall green trees, a grey asphalt road with no traffic; any signboards are blurred and unreadable"),
        NEN_HOC=("her busy street-food stall at a crowded market street, out of focus: trays of colourful snacks and steel pots at the lower right, people walking "
                 "far behind, shop fronts with blue awnings, overcast daylight")),
    "V2": dict(
        DAO_GANG="She wears thin clear disposable plastic gloves on both hands.",
        TAY_HOC="her gloved hands resting on the rim of a steel bowl",
        VIEC_HOC="keeps gently tearing a small crisp puri into pieces over the steel bowl with her gloved fingers",
        VIEC2_HOC="lets the puri pieces drop back into the steel bowl",
        DAO_GIU="Her gloved hands stay on the rim of the steel bowl on the cart.",
        DAO_XE=("a bright street-snack cart with a large glass-fronted box of golden puris, a steel bowl of spiced potato filling, a big brass pot of tangy green "
                "water with a small steel ladle, and a stack of small leaf plates"),
        NEN_PHO=("a busy but calm market lane in a north Indian city in the morning light, slightly out of focus: old pastel-coloured buildings with carved "
                 "balconies, a few parked scooters far behind, a tall tree, no one close behind the stall; any signboards are blurred and unreadable"),
        NEN_HOC=("her bright snack stall in a crowded market lane, out of focus: the glass box of golden puris and brass pots at the lower right, shoppers walking "
                 "far behind, old pastel shop fronts, daylight")),
    "V3": dict(
        DAO_GANG="She works with bare hands.",
        TAY_HOC="her hands resting on the edge of a woven basket of fruit",
        VIEC_HOC="keeps gently turning a guava in her hands and polishing it with the end of her saree",
        VIEC2_HOC="puts the guava back on top of the pile in the basket",
        DAO_GIU="Her hands stay on the woven baskets of fruit on the cart.",
        DAO_XE=("a wooden fruit cart with woven baskets piled with guavas, bananas and pomegranates, a hanging brass weighing scale, and a folded cotton cloth "
                "on the edge"),
        NEN_PHO=("a quiet shaded road beside an old city market in north India in soft morning light, slightly out of focus: old stone arches, tall neem trees, "
                 "a grey road with no traffic; any signboards are blurred and unreadable"),
        NEN_HOC=("her fruit cart at a crowded market road, out of focus: baskets of colourful fruit at the lower right, people walking far behind, old stone "
                 "arches, daylight")),
}

ANH = "SAMPLE/phong-van-pho-hindi/anh/"
# Biến thể 01 bám sát video mẫu. Mỗi dòng: khoá người bán, tên biến thể, thành phố (câu 'I am <city>').
NHAN_VAT = [
    ("V1", "bien-the-01-bam-sat-video", "Lucknow"),
    ("V2", "bien-the-02-nguoi-ban-tre-puri", "Jaipur"),
    ("V3", "bien-the-03-nguoi-ban-lon-tuoi-trai-cay", "Patna"),
]

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")


def build():
    out = []
    for k, name, city in NHAN_VAT:
        v = {"name": name}
        v.update(CHUNG)
        q = QUAY[k]
        v.update(q)
        v["NGUOI_HOC"] = BAN[k]
        v["GIONG_HOC"] = GIONG_BAN[k]
        v["NGHE_HOC"] = ("keeps the lips pressed together and looks at the interviewer's face with a friendly attentive face, " + q["TAY_HOC"] +
                         "; she never looks at the camera")
        v["DAO_NGHI"] = "the interviewer holding the microphone toward her, " + q["TAY_HOC"]
        v["LUOT"] = [{"who": w, "text": t, "emo": e, "c": "black", "o": "white", "fx": "none", "phan": p} for w, p, t, e in luot(city)]
        refs = {}
        for key, p in (("NGUOI_DAY", "robot-talka.png"), ("NGUOI_PV", "PV.png"), ("NGUOI_HOC", k + ".png")):
            if os.path.isfile(os.path.join(ROOT, ANH + p)):
                refs[key] = [ANH + p]
            else:
                print(f"CẢNH BÁO [{name}] {key}: chưa có ảnh {ANH + p}")
        if refs:
            v["refs"] = refs
        out.append(v)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    L = luot("X")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    p1 = sum(1 for x in L if x[1] == 1)
    print("Đã ghi", os.path.abspath(OUT), f"({len(NHAN_VAT)} biến thể, {len(L)} lượt: {p1} phần 1 + {len(L) - p1} phần 2, "
          f"dài nhất {max(len(t.split()) for _, _, t, _ in L)} từ)")
