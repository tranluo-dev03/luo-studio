"""Sinh SAMPLE/split-screen-vertical-x0043-hi/BIEN-THE-X0043-HI-20.json từ bảng X0043_20-bien-the-split-screen-HINDI.csv (20 biến thể Ấn Độ, lời thoại tiếng Hindi).
Sửa bảng BIEN_THE (nhân vật, giọng, tuổi, giới) hoặc luot() rồi chạy:
    .venv\\Scripts\\python.exe SAMPLE\\split-screen-vertical-x0043-hi\\cong-cu\\tao_bien_the.py
Ảnh nhân vật: anh/nhan-vat/bien-the-NN.webp (tải từ link Drive trong CSV); ảnh robot: anh/robot-ai.webp.
Lời thoại theo kịch bản trong CSV: "How old are you?", "I have N.", "I am N." và các từ AI / Talka AI / AI Tutor viết tiếng Anh; còn lại tiếng Hindi (chữ Devanagari).
Tuổi N khác nhau từng biến thể (cột "Kiểu biến thể": đổi "I am 28" thành "I am N"); phụ đề sinh từ cùng lời thoại nên tự theo.
Nữ (BT 1-10) nói "मज़ाक कर रही हो ना?", nam (BT 11-20) nói "मज़ाक कर रहे हो ना?"."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "BIEN-THE-X0043-HI-20.json")
DU_AN = "SAMPLE/split-screen-vertical-x0043-hi"
ROBOT = DU_AN + "/anh/robot-ai.webp"

CHUNG = {
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": "a sleek feminine humanoid robot: a white helmet-like head with a few dark panel lines, a smooth white porcelain face with soft light-blue eyes and "
                 "finely sculpted lips, a black mechanical neck of cables and pistons, glossy white hexagonal chest and shoulder plates outlined with thin glowing cyan seams "
                 "over black mechanical joints",
    "GIONG_DAY": "a bright, warm, friendly young woman's voice with a light smooth synthetic sheen, native-sounding Hindi, clear, quick and confident, "
                 "like a cheerful language teacher on a video call",
    "NEN_DAY": "a bright white and pale-blue futuristic studio backdrop with soft vertical light strips and a thin glowing white circular halo ring behind the head",
    "TEN_HOC": "the learner",
    "NEN_HOC": "a cosy Indian chai café corner: a plain warm-cream wall with a colourful hand-painted Madhubani-style folk-art panel (orange, red, green and blue "
               "patterns) hanging on a thin wooden rod above and behind the head, a strip of blue-and-white painted tiles at the far right edge, soft warm daylight",
    "DAO_BAN": "a small clay kulhad cup of hot masala chai just left of centre, and two golden samosas on a small steel plate just right of centre",
}


def giong(gioi, nhom_tuoi, am, tinh, vung):
    who = "woman" if gioi == "nu" else "man"
    pron = "actress" if gioi == "nu" else "actor"
    return (f"a real Indian {who} {nhom_tuoi}, a native speaker of Hindi with a light {vung} regional touch and a beginner's English: {am}, "
            f"{tinh}; a real person, not an {pron}")


# (tên, ngoại hình, giọng, tuổi nói, giới)  Ảnh: anh/nhan-vat/bien-the-NN.webp
BIEN_THE = [
    ("bien-the-01-nu-21-assam",
     "a 21-year-old Indian woman from Assam, petite with narrow shoulders, a round face with full cheeks, big brown eyes and full lips, bright golden-yellow skin, "
     "long black hair past the shoulders in gentle waves with a white flower pinned on one side; a white silk mekhela chador with a gold-and-red border over a "
     "matching short-sleeved blouse, small gold earrings, a gold bracelet and a small red bindi in the middle of the forehead; gentle, elegant traditional Assamese style",
     giong("nu", "in her early twenties", "bright mid-high pitch", "soft, sweet and a little shy", "Assamese"), 21, "nu"),
    ("bien-the-02-nu-24-goa",
     "a 24-year-old Indian woman from Goa, balanced build with sloping shoulders, an oval face with moderate cheekbones and almond-shaped brown eyes, light bronze-brown "
     "skin, dark brown hair down to the mid back in voluminous waves tied half-up; a red-and-white checked Kunbi cotton sari with a short-sleeved red blouse, red "
     "bangles, gold earrings and a red bindi; bright, cheerful traditional Goan style",
     giong("nu", "in her mid twenties", "bright mid pitch", "cheerful and playful", "Konkani"), 24, "nu"),
    ("bien-the-03-nu-27-kashmir",
     "a 27-year-old Indian woman from Kashmir, tall and slim with sloping shoulders, an oval face with high cheekbones, hazel-green eyes and thin lips, fair golden-white "
     "skin, dark brown hair down to the mid back worn loose under a brown woollen headscarf; a long dark-brown woollen pheran with flower embroidery at the neckline, "
     "silver earrings and a silver bracelet; warm, modest traditional Kashmiri style",
     giong("nu", "in her late twenties", "clear mid pitch", "calm and gentle", "Kashmiri"), 27, "nu"),
    ("bien-the-04-nu-30-haryana",
     "a 30-year-old Indian woman from Haryana, tall with clear curves, an oval face with high cheekbones, big brown eyes and full lips, warm golden-brown skin, black hair "
     "down to the mid back in a thick braid over one shoulder with a gold borla ornament on the forehead; a deep-red silk ghagra choli with gold thread embroidery and "
     "a sheer gold odhni draped over the head and shoulders, layered gold bangles, large gold earrings and a red bindi; dazzling, glamorous traditional Haryanvi style",
     giong("nu", "around thirty", "confident mid pitch", "direct and lively", "Haryanvi"), 30, "nu"),
    ("bien-the-05-nu-34-manipur",
     "a 34-year-old Indian woman from Manipur, average build, a little full, a round face with full cheeks and big brown eyes, bright golden-yellow skin, long black hair "
     "in a low bun at the nape with a small white flower; a deep-pink phanek wrap skirt with a white sheer embroidered innaphee shawl over a matching short-sleeved blouse, "
     "silver earrings, a silver bracelet and a red bindi; gentle, feminine traditional Manipuri style",
     giong("nu", "in her mid thirties", "soft mid pitch", "gentle and warm", "Manipuri"), 34, "nu"),
    ("bien-the-06-nu-39-chhattisgarh",
     "a 39-year-old Indian woman from Chhattisgarh, balanced build with sloping shoulders, a heart-shaped face with moderate cheekbones, big brown eyes and light wrinkles "
     "around the eyes, light bronze-brown skin, black hair down to the mid back pinned in a neat low bun at the nape; a turmeric-yellow Kosa silk sari with a matching "
     "short-sleeved blouse, a gold necklace, gold earrings, a gold bracelet and a red bindi; dignified, calm traditional Chhattisgarhi style",
     giong("nu", "in her late thirties", "steady mid pitch", "calm and composed", "Chhattisgarhi"), 39, "nu"),
    ("bien-the-07-nu-46-jharkhand",
     "a 46-year-old Indian woman from Jharkhand, average build, a little full, a softly square face with high cheekbones, dark brown eyes and light wrinkles around the "
     "eyes and mouth, warm deep brown skin, black hair with a few silver strands, shoulder-length and pinned in a low bun; a red cotton sari with a white border and a "
     "short-sleeved red blouse, a tribal beaded necklace and metal bangles, large silver earrings and a red bindi; rustic, dignified traditional Jharkhandi style",
     giong("nu", "in her mid forties", "even mid-low pitch", "plain, warm and straightforward", "Jharkhandi"), 46, "nu"),
    ("bien-the-08-nu-54-uttarakhand",
     "a 54-year-old Indian woman from Uttarakhand, average build, a little full, an oval face with slightly sagging cheeks and light wrinkles around the eyes and mouth, "
     "warm golden-brown skin, black hair with many silver strands, shoulder-length and pinned in a low bun; a dark-red woollen choli with a golden pichora odhni "
     "embroidered with flowers draped over the head and shoulders, a gold necklace, gold earrings and a red bindi; formal, calm traditional Uttarakhandi style",
     giong("nu", "in her mid fifties", "steady mid-low pitch", "calm, dignified and kind", "Garhwali"), 54, "nu"),
    ("bien-the-09-nu-63-himachal",
     "a 63-year-old Indian woman from Himachal Pradesh, thin with narrow shoulders and a slight stoop, a long face with high cheekbones and clear wrinkles around the eyes "
     "and mouth, warm golden-brown skin, silver-grey hair down to the shoulders pinned in a low bun; a deep-green woollen choli under a striped woollen shawl, a small "
     "gold nath nose ring, gold earrings and a silver bracelet; rustic, modest traditional Himachali style",
     giong("nu", "in her early sixties", "a soft, slightly thin and mildly husky mid-pitch voice", "kind and gently amused, a little slower than a young speaker", "Pahari"), 63, "nu"),
    ("bien-the-10-nu-71-telangana",
     "a 71-year-old Indian woman from Telangana, short and a little plump with rounded shoulders, a broad face with a slight double chin and deep wrinkles around the eyes "
     "and mouth, deep bronze-brown skin with small age spots, short white hair cut at ear level and neatly combed; a red-and-blue geometric Pochampally ikat sari with "
     "a matching short-sleeved blouse, a gold necklace, gold earrings, a gold bracelet and a red bindi; dignified, respectful traditional Telangana style",
     giong("nu", "in her seventies", "a soft, slightly husky older voice", "warm and grandmotherly, noticeably slower than a young speaker", "Telugu"), 71, "nu"),
    ("bien-the-11-nam-22-assam",
     "a 22-year-old Indian man from Assam, tall and slim with level shoulders, a long face with a defined jawline, big brown eyes and a clean-shaven face, bright "
     "golden-yellow skin, thick black slightly wavy hair in a neat side part; a long-sleeved white kurta with a red-and-white gamocha scarf draped over one shoulder, "
     "a brown leather-strap watch; neat, elegant traditional Assamese style",
     giong("nam", "in his early twenties", "a warm mid-low pitch, clearly lower than the tutor's voice", "polite and friendly", "Assamese"), 22, "nam"),
    ("bien-the-12-nam-26-goa",
     "a 26-year-old Indian man from Goa, balanced build with moderately broad shoulders, an oval face with almond-shaped brown eyes and short stubble, light bronze-brown "
     "skin, black hair in a low fade with the top swept back; a white linen kurta with a turned-down collar, a black sports watch and a thin silver bracelet; "
     "easygoing, masculine traditional Goan style",
     giong("nam", "in his mid twenties", "a relaxed low-mid baritone, clearly lower than the tutor's voice", "easygoing and cheerful", "Konkani"), 26, "nam"),
    ("bien-the-13-nam-29-kashmir",
     "a 29-year-old Indian man from Kashmir, tall with broad shoulders, a long face with a defined jawline, hazel-green eyes and a short neatly trimmed full beard, fair "
     "golden-white skin, thick dark slightly wavy hair swept back under a brown karakul cap; a long dark-grey woollen pheran, a black leather-strap watch; formal, "
     "refined traditional Kashmiri style",
     giong("nam", "in his late twenties", "a smooth low-mid baritone, clearly lower than the tutor's voice", "polished and polite", "Kashmiri"), 29, "nam"),
    ("bien-the-14-nam-33-haryana",
     "a 33-year-old Indian man from Haryana, solid build with broad shoulders, a square face with a sharp jawline, dark brown eyes and a short full beard, warm "
     "golden-brown skin, a neatly tied orange pagri turban; a long-sleeved white kurta, a steel kara bracelet and a brown leather-strap watch; commanding, masculine "
     "traditional Haryanvi style",
     giong("nam", "in his early thirties", "a deep low baritone, clearly lower than the tutor's voice", "steady and confident", "Haryanvi"), 33, "nam"),
    ("bien-the-15-nam-38-manipur",
     "a 38-year-old Indian man from Manipur, balanced build with moderately broad shoulders, an oval face with big brown eyes and a short moustache, bright golden-yellow "
     "skin, thick short black hair swept back; a long-sleeved white kurta with a white cotton shawl draped over one shoulder, a black leather-strap watch; formal, "
     "refined traditional Manipuri style",
     giong("nam", "in his late thirties", "a calm low-mid baritone, clearly lower than the tutor's voice", "gentle and measured", "Manipuri"), 38, "nam"),
    ("bien-the-16-nam-43-chhattisgarh",
     "a 43-year-old Indian man from Chhattisgarh, average build, a little full with a slightly round belly, a round face with full cheeks, small dark brown eyes and a "
     "salt-and-pepper moustache, deep bronze-brown skin, short black-and-grey hair; a long turmeric-yellow kurta with a red gamchha scarf draped over one shoulder, a "
     "brown leather-strap watch; rustic, calm traditional Chhattisgarhi style",
     giong("nam", "in his early forties", "a warm mid-low baritone, clearly lower than the tutor's voice", "calm and homely", "Chhattisgarhi"), 43, "nam"),
    ("bien-the-17-nam-50-jharkhand",
     "a 50-year-old Indian man from Jharkhand, stocky build with a slightly big belly and broad shoulders, a square face with clear cheekbones, small dark brown eyes and "
     "a short salt-and-pepper full beard, warm deep brown skin with deep wrinkles around the eyes and mouth, short black hair with many silver strands, slightly thin at "
     "the crown; a long deep-green kurta, thin metal-framed glasses and a black leather-strap watch; formal, calm traditional Jharkhandi style",
     giong("nam", "around fifty", "a rich low baritone, clearly lower than the tutor's voice", "plain, sturdy and calm", "Jharkhandi"), 50, "nam"),
    ("bien-the-18-nam-58-uttarakhand",
     "a 58-year-old Indian man from Uttarakhand, average build, slightly thin with slightly sloping shoulders and a slight stoop, a long face with high cheekbones and deep "
     "wrinkles around the eyes and mouth, warm golden-brown skin, short black-and-grey hair under a brown woollen topi cap; a long grey woollen coat over a white kurta, "
     "thin metal-framed glasses; rustic, experienced traditional Uttarakhandi style",
     giong("nam", "in his late fifties", "a dry, slightly husky low-mid voice, clearly lower than the tutor's voice", "plain and weathered", "Garhwali"), 58, "nam"),
    ("bien-the-19-nam-66-himachal",
     "a 66-year-old Indian man from Himachal Pradesh, thin with slightly sloping shoulders and a slight stoop, a long face with high cheekbones and deep wrinkles around "
     "the eyes and mouth, dark bronze-brown skin, short thinning white hair under a green woollen Himachali topi cap; a long brown woollen coat over a white kurta with a "
     "striped woollen shawl, thin metal-framed glasses; rustic, experienced traditional Himachali style",
     giong("nam", "in his mid sixties", "a gravelly, low older voice, clearly lower than the tutor's voice", "plain, kind and a little slower than a young speaker", "Pahari"), 66, "nam"),
    ("bien-the-20-nam-75-telangana",
     "a 75-year-old Indian man from Telangana, short and slightly thin with narrow shoulders and a clear stoop, a long face with high cheekbones and slightly hollow "
     "cheeks, deep wrinkles around the eyes and mouth, warm deep brown skin with age spots, short thinning white hair; a long-sleeved white kurta with a white "
     "shoulder cloth, thin metal-framed glasses; rustic, dignified traditional Telangana style",
     giong("nam", "in his mid seventies", "a thin, soft and slightly husky older male voice, still lower than the tutor's voice", "gentle and wise, noticeably slower than a young speaker", "Telugu"), 75, "nam"),
]


def luot(n, gioi):
    """15 lượt theo kịch bản CSV. Tiếng Anh: lượt 3, 4, 6, một phần lượt 5, 9. Câu sai: chữ đỏ + viền đỏ; câu nói lại đúng: chữ xanh + viền xanh."""
    brk = "मज़ाक कर रही हो ना?" if gioi == "nu" else "मज़ाक कर रहे हो ना?"
    L = [
        ("day", "क्या आप अंग्रेज़ी बोलते हैं?", "friendly"),
        ("hoc", "थोड़ी बहुत।", "hesitant"),
        ("day", "How old are you?", "curious"),
        ("hoc", f"I have {n}.", "unsure", {"c": "red", "fx": "wrong"}),
        ("day", f"आपको ऐसे कहना चाहिए, I am {n}.", "patient, encouraging"),
        ("hoc", f"I am {n}.", "confident", {"c": "green", "fx": "right"}),
        ("day", "बहुत बढ़िया!", "warm, encouraging"),
        ("hoc", "शुक्रिया, लेकिन आप कौन हैं?", "curious"),
        ("day", "मैं? मैं Talka AI हूँ, एक AI Tutor। मैं आपकी अंग्रेज़ी बेहतर बनाने में मदद करूँगी।", "cheerful"),
        ("hoc", "शुक्रिया, लेकिन मेरे पास पैसे नहीं हैं।", "worried"),
        ("day", "पैसे किस बात के? आप यहाँ बिल्कुल मुफ़्त में सीख सकते हैं।", "playful"),
        ("hoc", f"मुफ़्त में? {brk}", "surprised, skeptical"),
        ("day", "नहीं, बिल्कुल सच! असली AI अवतार के साथ कभी भी, कहीं भी जितनी चाहें अंग्रेज़ी बातचीत की प्रैक्टिस करें।", "confident, enthusiastic"),
        ("hoc", "सच में?", "surprised, hopeful"),
        ("day", "हाँ, बिल्कुल! बहुत जल्द आप भी एक नेटिव स्पीकर की तरह अंग्रेज़ी बोलने लगेंगे। बस Talka AI डाउनलोड करें!", "reassuring, upbeat"),
    ]
    out = []
    for who, text, emo, *extra in L:
        t = {"who": who, "text": text, "emo": emo, "fx": "none"}
        t.update(extra[0] if extra else {})
        out.append(t)
    return out


res = []
for i, (name, nguoi, giong_hoc, tuoi, gioi) in enumerate(BIEN_THE, 1):
    anh = f"{DU_AN}/anh/nhan-vat/bien-the-{i:02d}.webp"
    assert os.path.isfile(os.path.join(HERE, "..", "..", "..", anh)), anh
    assert (gioi == "nu") == (i <= 10)
    v = {"name": name, **CHUNG, "NGUOI_HOC": nguoi, "GIONG_HOC": giong_hoc, "LUOT": luot(tuoi, gioi),
         "refs": {"NGUOI_DAY": [ROBOT], "NGUOI_HOC": [anh]}}
    res.append(v)
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(res))
