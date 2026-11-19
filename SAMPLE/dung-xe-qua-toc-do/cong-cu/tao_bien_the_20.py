"""Sinh SAMPLE/dung-xe-qua-toc-do/BIEN-THE-DUNG-XE-QUA-TOC-DO-20.json: 20 biến thể theo bảng
anh/20-bien-the/20-bien-the-dung-xe.csv (STT 1–20).
Ảnh đã tải về anh/20-bien-the/ (tai-xe-NN, canh-sat-NN, be-trai); refs trỏ tới các file đó.
Chạy: python SAMPLE/dung-xe-qua-toc-do/cong-cu/tao_bien_the_20.py
Lời thoại (LUOT) lấy từ phần kịch bản trong CSV, chỉ bỏ phần chữ Devanagari trong ngoặc.
Lưu ý: kịch bản viết cho "Bố" (nam). Với 15 biến thể tài xế nữ, lời thoại giữ nguyên như CSV."""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DIR_ANH = os.path.join("SAMPLE", "dung-xe-qua-toc-do", "anh", "20-bien-the")
OUT = os.path.join(HERE, "..", "BIEN-THE-DUNG-XE-QUA-TOC-DO-20.json")

# (STT, giới tài xế, tuổi, mô tả tài xế EN, mô tả cảnh sát EN, số ảnh cảnh sát [STT dùng ảnh])
BANG = [
    (1, "nam", 27, "an Indian man about 27 years old, brown skin, long black hair in a low ponytail, a short beard, a shy face with head bowed; a clean light-blue shirt, black jeans, white sneakers", "a woman about 28, brown skin, black hair in a low bun at the nape, a serious but gentle face; khaki Indian police uniform, police cap, black shoes", 1),
    (2, "nam", 30, "an Indian man about 30, brown skin, black hair neatly gelled back, thick moustache, a tense face biting the lip; a clean white polo shirt, grey trousers, brown leather shoes", "a woman about 32, brown skin, short black hair to the shoulders, a stern face and a decisive gaze; khaki Indian police uniform, police cap, black shoes", 2),
    (3, "nam", 26, "an Indian man about 26, brown skin, short curly black hair, light stubble, a bewildered face looking straight at the camera; a clean beige crew-neck T-shirt, blue jeans, sneakers", "a woman about 26, brown skin, black hair in a long braid down the back, a calm face and a firm tone; khaki Indian police uniform, police cap, black shoes", 3),
    (4, "nam", 29, "an Indian man about 29, brown skin, short black hair, thin moustache, a tired face, sighing; a clean blue-and-white striped shirt, black trousers, black leather shoes", "a woman about 35, brown skin, black hair in a high neat bun, a calm serious face; khaki Indian police uniform, police cap, black shoes", 1),
    (5, "nam", 24, "an Indian man about 24, brown skin, short messy black hair, no beard, a worried face with knitted brows and lips slightly parted; a light-grey jacket over a white T-shirt, black trousers, sneakers", "a woman about 29, brown skin, long black hair tied low, a serious face, holding a notebook; khaki Indian police uniform, police cap, black shoes", 1),
    (6, "nu", 22, "an Indian woman about 22, brown skin, long black hair loose over the shoulders, a shy face looking down; a clean blue kurta, white trousers, sandals", "a man about 30, brown skin, short black hair, a short moustache, a serious but gentle face; khaki Indian police uniform, police cap, black shoes", 6),
    (7, "nu", 24, "an Indian woman about 24, brown skin, short black hair to the shoulders, a self-conscious face with head bowed; a blue sari with a light pattern and a matching short-sleeved blouse, sandals", "a man about 28, brown skin, neatly slicked-back black hair, a stern face, standing straight; khaki Indian police uniform, police cap, black shoes", 6),
    (8, "nu", 26, "an Indian woman about 26, brown skin, black hair in a high neat bun, an anxious face biting the lip; a pale-yellow salwar kameez with a matching dupatta, sandals", "a man about 34, brown skin, short black hair, a thick moustache, a calm face; khaki Indian police uniform, police cap, black shoes", 6),
    (9, "nu", 48, "an Indian woman about 48, brown skin, black hair with some silver strands in a low bun, a slightly worried face looking down; a blue kurta, white trousers, sandals", "a man about 40, brown skin, black hair with some silver, a moustache, a serious face and a deep voice; khaki Indian police uniform, police cap, black shoes", 6),
    (10, "nu", 28, "an Indian woman about 28, brown skin, long black curled hair, a melancholic face looking to the side; a light-purple kurta, white trousers, sandals", "a man about 33, brown skin, short hair, a serious face, one hand on the hip; khaki Indian police uniform, police cap, black shoes", 6),
    (11, "nam", 48, "an Indian man about 48, brown skin, black hair turning silver on top, neatly combed, short silver beard, a worried face looking down; a clean white shirt, grey trousers, black leather shoes", "a woman about 38, brown skin, black hair in a neat bun, a calm serious face; khaki Indian police uniform, police cap, black shoes", 11),
    (12, "nam", 52, "an Indian man about 52, dark-brown skin, black hair with silver strands, silver moustache, light wrinkles, a tired, resigned face looking at the camera; a brown-and-green checked shirt, dark trousers, leather shoes", "a woman about 30, brown skin, long black hair tied low, a serious and firm face; khaki Indian police uniform, police cap, black shoes", 1),
    (13, "nam", 46, "an Indian man about 46, brown skin, thinning black hair neatly combed, black moustache, a worried furrowed brow; a clean blue shirt, black trousers, leather shoes", "a woman about 27, brown skin, short black hair, a strict but polite face; khaki Indian police uniform, police cap, black shoes", 1),
    (14, "nam", 55, "an Indian man about 55, brown skin, short silver hair, short silver beard, a sad face, simple glasses; a brown wool sweater over a white shirt, grey trousers, leather shoes", "a woman about 36, brown skin, black hair in a high bun, a calm and serious face; khaki Indian police uniform, police cap, black shoes", 1),
    (15, "nam", 50, "an Indian man about 50, brown skin, slightly receding black hair at the temples, short black beard, a tense face looking at the camera; a grey T-shirt, a light jacket, black jeans, sneakers", "a woman about 31, brown skin, curly black hair tied low, a serious face, holding papers; khaki Indian police uniform, police cap, black shoes", 1),
    (16, "nu", 45, "an Indian woman about 45, brown skin, black hair in a low bun, a tired, sad face, closed lips; a long-sleeved beige cotton kurta, white trousers, sandals", "a man about 38, brown skin, short black hair, a moustache, a serious and gentle face; khaki Indian police uniform, police cap, black shoes", 16),
    (17, "nu", 50, "an Indian woman about 50, brown skin, black hair with silver strands in a neat bun, a worried face, simple glasses; a light-pink sari with a faint pattern and a matching short-sleeved blouse, sandals", "a man about 32, brown skin, neatly slicked-back hair, a stern face, standing straight; khaki Indian police uniform, police cap, black shoes", 6),
    (18, "nu", 48, "an Indian woman about 48, brown skin, short black hair with a light wave, a serious, slightly tense face; a dark-green salwar kameez with a matching dupatta, sandals", "a young man about 29, brown skin, short black hair, a serious face; khaki Indian police uniform, police cap, black shoes", 6),
    (19, "nu", 54, "an Indian woman about 54, brown skin, silver hair in a neat high bun, a resigned face with some wrinkles; a light-orange kurta, white trousers, sandals", "a man about 45, brown skin, black hair with some grey, thick moustache, a calm face; khaki Indian police uniform, police cap, black shoes", 6),
    (20, "nu", 42, "an Indian woman about 42, brown skin, long black hair tied low, big eyes, lips slightly parted, a surprised look into the camera; a blue churidar with a matching long-sleeved top, a thin light shawl, sandals", "a man about 36, brown skin, short black hair, a short moustache, a serious face; khaki Indian police uniform, police cap, black shoes", 6),
]

CHUNG_TEN_CS = {"TEN_CANHSAT": "the officer", "VAI_CANHSAT": "officer", "POS_CANHSAT": "window-side",
                "NGHE_CANHSAT": "stays leaning at the car window looking at whoever in the car is speaking, calm attentive face, mouth closed",
                "NHIN_CANHSAT": "keeps the eyes on the person she is talking to, in the direction the clip's EYE LINE gives, never into the lens"}

NGUOI_BE = ("an Indian boy about 4–5 years old, brown skin, short tidy black hair, a chubby face, a sweet obedient look with a slightly puzzled expression, "
            "a clean white shirt, navy-blue trousers, clean sneakers")

def luot(nam):
    """Lượt thoại theo giới tính tài xế (nam: Papa / करूँगा; nữ: Mummy / करूँगी). Gia sư AI là nữ.
    Phần 1: cảnh sát tiếng Anh; tài xế tiếng Anh ậm ừ; bé trai tiếng Anh với cảnh sát, tiếng Hindi với bố/mẹ.
    Hindi viết chữ Devanagari xen từ tiếng Anh chữ La-tinh (engine.speech_lang nhận ra chữ Devanagari)."""
    me = "पापा" if nam else "मम्मी"
    kr = "करूँगा" if nam else "करूँगी"
    L = [
        ("canhsat", "Do you know you were speeding?", "decisive, calm", "none", 1),
        ("hoc", "Uh... yes.", "worried", "none", 1),
        ("canhsat", "License and registration, please.", "decisive", "none", 1),
        ("hoc", "Uh... I... I... I... Officer,", "hesitant, worried", "none", 1),
        ("hoc", "sorry.", "embarrassed", "none", 1),
        ("be", "Sorry, officer. He's nervous." if nam else "Sorry, officer. She's nervous.", "helpful, embarrassed", "none", 1),
        ("be", "And his English isn't very good." if nam else "And her English isn't very good.", "helpful", "none", 1),
        ("canhsat", "Does he have his license and registration?" if nam else "Does she have her license and registration?", "calm, friendly", "none", 1),
        ("be", f"{me}, अपना license और गाड़ी के papers दिखाओ।", "helpful", "none", 1),
        ("canhsat", "All right. Slow down next time.", "calm, friendly", "none", 1),
        ("hoc", "Uh... I wish... I can speak English like you.", "relieved, hopeful", "none", 1),
        ("be", "सिर्फ़ तीन हफ़्तों में Aiva AI के साथ।", "proud, cheerful", "none", 1),
        ("be", "हर रोज़ real conversations।", "cheerful", "none", 1),
        ("hoc", "सच में?", "surprised", "none", 2),
        ("day", "हाँ।", "warm", "none", 2),
        ("day", "चलो दिखाती हूँ।", "calm", "none", 2),
        ("day", "Where are you going?", "curious", "none", 2),
        ("hoc", "I go to home.", "cheerful", "wrong", 2, "x", "go to"),
        ("day", "You mean, I'm going home? Yes,", "warm, encouraging", "none", 2),
        ("hoc", "I'm going home.", "cheerful", "right", 2, "check", "going"),
        ("hoc", "I am very hurry.", "cheerful", "wrong", 2, "x", "am very"),
        ("day", "\"I'm in a hurry\" कहना सही तरीका है।", "warm", "none", 2),
        ("hoc", "ओह, ठीक है।", "relieved", "none", 2),
        ("hoc", "Thank you.", "calm", "none", 2),
        ("hoc", "रुको, तुम कौन हो?", "surprised", "none", 2),
        ("day", "मैं एक AI tutor हूँ, यहाँ तुम्हारी English practice और बेहतर बोलने में मदद करने के लिए।", "warm", "none", 2),
        ("hoc", "But I don't have monies.", "worried", "none", 2, "dollar", None),
        ("day", "It's \"I have no money.\" लेकिन परेशान मत हो,", "reassuring", "none", 2),
        ("day", "Aiva AI एक completely free app है।", "reassuring", "none", 2),
        ("hoc", "सचमुच?", "surprised", "none", 2),
        ("day", "हम कभी भी English practice कर सकते हैं,", "upbeat", "none", 2),
        ("day", "कहीं भी।", "upbeat", "none", 2),
        ("day", "बस Aiva AI download करो।", "upbeat", "none", 2),
        ("hoc", f"मैं अभी download {kr}।", "delighted", "none", 2),
        ("hoc", "बहुत-बहुत thank you।", "calm", "none", 2),
    ]
    out = []
    for item in L:
        who, text, emo, fx, phan = item[:5]
        d = {"who": who, "text": text, "emo": emo, "fx": fx, "phan": phan}
        if len(item) > 5 and item[5]:
            d["icon"] = item[5]
        if len(item) > 6 and item[6]:
            d["to"] = item[6]
        out.append(d)
    return out


def anh(prefix, stt):
    """Đường dẫn ảnh đã tải (đuôi có thể .png/.jpg/.webp), tương đối từ thư mục gốc Studio."""
    tim = glob.glob(os.path.join(ROOT, DIR_ANH, f"{prefix}-{stt:02d}.*"))
    if not tim:
        raise SystemExit(f"thiếu ảnh {prefix}-{stt:02d}")
    return os.path.join(DIR_ANH, os.path.basename(tim[0])).replace("\\", "/")


def main():
    be = glob.glob(os.path.join(ROOT, DIR_ANH, "be-trai.*"))[0]
    be_path = os.path.join(DIR_ANH, os.path.basename(be)).replace("\\", "/")
    res = []
    for stt, gioi, tuoi, nguoi_hoc, nguoi_cs, so_cs in BANG:
        nam = gioi == "nam"          # tài xế nam -> cảnh sát nữ, và ngược lại
        cs_nu = nam
        cha = "father" if nam else "mother"
        cs_gioi = "woman" if cs_nu else "man"
        hz_hoc = ("110–140" if tuoi < 40 else "95–125") if nam else ("200–230" if tuoi < 40 else "185–215")
        hz_cs = "200–220" if cs_nu else "110–130"
        v = {
            "name": f"tai-xe-{stt:02d}-{'nam' if nam else 'nu'}-an-do",
            "TEN_CANHSAT": "the officer",
            "NGUOI_CANHSAT": nguoi_cs,
            "GIONG_CANHSAT": f"a clear, firm Indian {cs_gioi}'s voice around {hz_cs} Hz, calm and authoritative, speaking only English with a light Indian accent",
            "VAI_CANHSAT": "officer",
            "POS_CANHSAT": "window-side",
            "NGHE_CANHSAT": CHUNG_TEN_CS["NGHE_CANHSAT"],
            "TEN_HOC": f"the {cha}",
            "NGUOI_HOC": nguoi_hoc,
            "GIONG_HOC": f"a natural Indian {'man' if nam else 'woman'}'s voice in their {tuoi // 10 * 10 + 0}s, around {hz_hoc} Hz, hesitant, broken, mumbling English with many ums in Part 1; natural Hindi later; a real person, not an actress",
            "VAI_HOC": "driver",
            "POS_HOC": "driver-seat",
            "NGHE_HOC": "sits at the wheel looking at whoever is speaking, worried attentive face, mouth closed, hands on the steering wheel unless the clip's action says otherwise",
            "TEN_BE": "the little boy",
            "NGUOI_BE": NGUOI_BE,
            "GIONG_BE": "a bright, sweet little boy's voice around 300–340 Hz, fluent clear English when talking to the officer, natural Hindi when talking to his father or mother",
            "VAI_BE": "son",
            "POS_BE": "child-seat",
            "NGHE_BE": "sits in his child seat looking at whoever is speaking with big curious eyes, mouth closed",
            "XE": "a silver-grey Indian sedan with grey cloth seats",
            "NEN_DUONG": "a sunny Indian city road in daytime, a few tall trees, a rickshaw and small shops far away",
            "DAO_GIAY_TO": "a brown leather wallet with a driver's licence card and a folded white registration paper, no readable text",
            "DAO_DIEN_THOAI": "a blue smartphone",
            "TEN_DAY": "the AI tutor",
            "NGUOI_DAY": "a sleek feminine humanoid robot with a smooth glossy pearl-white bald head and face, softly sculpted human-like features, large glowing sapphire-blue eyes, a calm friendly closed-lip smile, white over-ear headphones, a segmented black-and-chrome neck with faint blue light, white armoured shoulders and chest; realistic 3D render",
            "GIONG_DAY": "a clear, warm, friendly young woman's voice with a very slightly synthetic digital sheen, bright and upbeat, natural Hindi with English words",
            "NEN_DAY": "a deep navy-to-violet gradient background with a thin glowing violet-blue orbit ring around her head",
            "NEN_HOC": "the inside of the grey car, grey cloth seats, daylight through the side windows",
            "NHIN_CANHSAT": CHUNG_TEN_CS["NHIN_CANHSAT"],
            "NHIN_HOC": "keeps the eyes on the person he is talking to, in the direction the clip's EYE LINE gives, never into the lens",
            "NHIN_BE": "keeps the eyes on the person he is talking to, in the direction the clip's EYE LINE gives, never into the lens",
            "NHIN_HOC@2": "looks into the lens, as if talking to the AI tutor on the phone mounted on the dashboard",
            "NHIN_DAY": "looks straight into the lens, as if talking to the person on the call",
            "LUOT": luot(nam),
            "refs": {
                "NGUOI_CANHSAT": [anh("canh-sat", so_cs)],
                "NGUOI_HOC": [anh("tai-xe", stt)],
                "NGUOI_BE": [be_path],
                "NGUOI_DAY": ["SAMPLE/canh-sat-gia-su-ai/anh/DAY-aiva.png"],
            },
            "nguoi_theo_canh": True,
            "CHA": cha,
            "CHA_ANH": "he" if nam else "she",
            "CHA_CUA": "his" if nam else "her",
            "CHA_O": "him" if nam else "her",
            "CHA_VN": "bố" if nam else "mẹ",
            "CS_ANH": "she" if cs_nu else "he",
            "CS_CUA": "her" if cs_nu else "his",
            "CS_O": "her" if cs_nu else "him",
            "NET_HOC": "an Indian driver of the given age",
            "TIENG_BE": "tiếng Hindi",
            "ANH_SANG": "bright daylight",
            "DUONG_SAU": "the Indian city road",
            "DUONG_TRONG": "the Indian city road",
            "NGOAI_XA": "the city street",
            "AM_NEN": "city street ambience",
            "MAU_XE": "silver-grey",
            "GHE_XE": "grey cloth",
        }
        res.append(v)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("OK", os.path.abspath(OUT), len(res), "biến thể")


if __name__ == "__main__":
    main()
