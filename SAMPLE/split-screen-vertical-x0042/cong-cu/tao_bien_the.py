"""Sinh SAMPLE/split-screen-vertical-x0042/BIEN-THE-X0042-20.json từ bảng X0042_20-bien-the-split-screen.csv (20 biến thể nhân vật).
Sửa bảng BIEN_THE (nhân vật, giọng, tuổi trong câu sai/đúng) hoặc LUOT rồi chạy:
    runtime\\python.exe SAMPLE\\split-screen-vertical-x0042\\cong-cu\\tao_bien_the.py
Ảnh nhân vật: SAMPLE/split-screen-vertical-x0042/anh/nhan-vat/bien-the-NN.webp (tải từ link Drive trong CSV); ảnh robot: anh/robot-ai.webp.
Tuổi trong câu: BT 1-7 và 11-15 giữ "I am 28"; BT 8-10 đổi thành "I am 35"; BT 16-20 đổi thành "I am 68" (phụ đề tự đổi theo vì sinh từ cùng lời thoại)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "BIEN-THE-X0042-20.json")
DU_AN = "SAMPLE/split-screen-vertical-x0042"
ROBOT = DU_AN + "/anh/robot-ai.webp"

CHUNG = {
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": "a sleek feminine humanoid robot: a white helmet-like head with a few dark panel lines, a smooth white porcelain face with soft light-blue eyes and "
                 "finely sculpted lips, a black mechanical neck of cables and pistons, glossy white hexagonal chest and shoulder plates outlined with thin glowing cyan seams "
                 "over black mechanical joints",
    "GIONG_DAY": "a bright, warm, friendly young woman's voice with a light smooth synthetic sheen, neutral American accent, clear, quick and confident, "
                 "like a cheerful language teacher on a video call",
    "NEN_DAY": "a bright white and pale-blue futuristic studio backdrop with soft vertical light strips and a thin glowing white circular halo ring behind the head",
    "TEN_HOC": "the learner",
    "NEN_HOC": "a cosy Mexican café corner: a plain warm-cream wall with a colourful hand-woven Mexican tapestry (orange, red, blue and yellow geometric pattern) hanging "
               "on a thin wooden rod above and behind the head, a strip of blue-and-white talavera tiles at the far right edge, soft warm daylight",
    "DAO_BAN": "a talavera-painted ceramic mug of hot chocolate (blue, orange and white flower pattern) just left of centre, and a round sweet concha bun with a white "
               "sugar-shell top on a small wooden plate just right of centre",
}


def giong(gioi, tuoi_text, am, tinh):
    who = "woman" if gioi == "nu" else "man"
    act = "actress" if gioi == "nu" else "actor"
    return (f"a real Mexican {who} {tuoi_text} speaking English as a second language: {am}, a natural Mexican accent with Spanish vowels and a soft r, "
            f"{tinh}; a real person, not an {act}")


# (tên, ngoại hình, giọng, tuổi nói trong câu sai/đúng). Ảnh: anh/nhan-vat/<STT>.webp
BIEN_THE = [
    ("bien-the-01-nu-22",
     "a 22-year-old Mexican woman, tall slim build with sloping shoulders, a heart-shaped face with a small neat chin, big brown eyes and softly arched eyebrows, "
     "light honey-brown skin with naturally rosy cheeks, long black hair in a neat high ponytail with thin wispy bangs falling on the forehead; a cream round-neck "
     "short-sleeved knit crop top, small round silver earrings, a brown leather strap watch, the strap of a beige canvas tote on one shoulder; youthful, energetic weekend style",
     giong("nu", "in her early twenties", "bright mid-high pitch", "warm and playful, a smile in the voice"), "28"),
    ("bien-the-02-nu-25",
     "a 25-year-old Mexican woman, petite with narrow shoulders and a slim waist, a round face with full cheeks, almond-shaped eyes and moderately thick eyebrows, "
     "warm golden-brown skin with a light flush on the cheeks, chestnut-brown shoulder-length hair with curled-under ends framing the face and thin straight bangs; "
     "a white puffed-sleeve blouse with a square neckline, a small pearl necklace, gold teardrop earrings; feminine, soft vintage style",
     giong("nu", "in her mid twenties", "light, soft mid-high pitch", "gentle and friendly"), "28"),
    ("bien-the-03-nu-28",
     "a 28-year-old Mexican woman, tall and strong build with moderately broad shoulders, an oval face with a defined jawline, high cheekbones and full lips, "
     "deep olive-brown skin with natural skin texture, short black afro-textured curly hair close to the head with natural volume around the face; a fitted black "
     "t-shirt under a short brown leather jacket, large gold hoop earrings, the thin strap of a black crossbody bag; edgy, urban, strong yet feminine style",
     giong("nu", "in her late twenties", "confident mid pitch, a little low and smooth", "direct and self-assured"), "28"),
    ("bien-the-04-nu-20",
     "a 20-year-old Mexican woman, slender with narrow shoulders, an oval face with slightly rounded cheeks, big round eyes with naturally long lashes, light "
     "honey-brown skin and natural pink lips, auburn-brown hair past the shoulders in big waves with a centre part, the front strands framing the cheeks; a "
     "jade-green silk camisole with a V-neckline, long gold drop earrings and a thin bracelet; elegant, gentle style",
     giong("nu", "in her early twenties", "bright, light and youthful pitch", "sweet, a little shy and smiling"), "28"),
    ("bien-the-05-nu-27",
     "a 27-year-old Mexican woman, balanced build with straight shoulders, a slightly square face with a soft jawline and clear cheekbones, dark brown eyes, "
     "medium bronze-brown skin with natural pigmentation, a short black pixie cut with the fringe swept to one side; a grey pinstripe straight-cut blazer over a "
     "white round-neck t-shirt, small silver earrings, a gold-strap watch; modern, edgy, tidy office style",
     giong("nu", "in her late twenties", "clear mid pitch", "brisk and professional, confident"), "28"),
    ("bien-the-06-nu-24",
     "a 24-year-old Mexican woman, moderately full figure with slightly wide hips, a plump round face with full cheeks, big brown eyes and naturally curved "
     "eyebrows, warm golden-brown skin with a light flush on the cheeks, long chocolate-brown hair down to the mid back in a braid over one shoulder with a few "
     "strands framing the face; a burnt-orange long-sleeved turtleneck sweater, a thin cream wool scarf loosely around the neck, small gold earrings; warm, friendly autumn style",
     giong("nu", "in her mid twenties", "warm mid pitch", "cosy and cheerful"), "28"),
    ("bien-the-07-nu-30",
     "a 30-year-old Mexican woman, slim and tall with sloping shoulders, a long face with a straight nose bridge, high cheekbones and moderately thin lips, "
     "medium olive-brown skin with natural texture, long straight black hair with a side part tied low at the nape, a small gold hair clip holding the front "
     "strands; a moss-green V-neck dress with three-quarter sleeves under a long beige trench coat, small gold earrings and a silver metal-strap watch; elegant, mature, professional style",
     giong("nu", "around thirty", "smooth mid pitch", "calm, polished and composed"), "28"),
    ("bien-the-08-nu-33",
     "a 33-year-old Mexican woman, small and softly full build with rounded shoulders, a round face with full cheeks and a rounded chin, dark brown eyes, medium "
     "honey-brown skin with a few tiny pigment spots and natural smile lines, a dark brown shoulder-length bob with curled-under ends framing the face and a side "
     "part; a dusty-pink silk round-neck blouse with elbow-length sleeves, thin black-framed glasses and gold oval earrings; neat, calm, practical office style",
     giong("nu", "in her early thirties", "steady mid pitch", "calm, practical and kind"), "35"),
    ("bien-the-09-nu-37",
     "a 37-year-old Mexican woman, tall with moderately broad shoulders, a long oval face with a defined jawline, prominent cheekbones and very faint expression "
     "lines around the eyes, medium bronze-brown skin with natural pigmentation, black hair with a few silver strands, shoulder-length with soft waves and a "
     "centre part; a charcoal-grey single-breasted suit blazer over a white shirt with a spread collar, a gold-strap watch and pearl earrings; professional manager look, quietly elegant",
     giong("nu", "in her late thirties", "composed mid-low pitch", "measured and self-possessed"), "35"),
    ("bien-the-10-nu-31",
     "a 31-year-old Mexican woman, balanced build with slightly wide hips, a heart-shaped face with a slightly pointed chin, almond eyes and a modest low nose "
     "bridge, light olive-brown skin with a light flush on the cheeks, caramel-brown hair past the chest in large curls with a centre part, the front strands "
     "framing both cheeks; a blue-and-white striped long-sleeved shirt with the sleeves rolled to the forearm, small pearl earrings and a white leather-strap watch; "
     "young, creative, feminine yet professional style",
     giong("nu", "in her early thirties", "bright mid pitch", "lively and creative"), "35"),
    ("bien-the-11-nam-26",
     "a 26-year-old Mexican man, athletic build with broad shoulders and a moderately full chest, a masculine square face with a sharp jawline and a straight "
     "nose bridge, medium olive-brown skin, a short neatly trimmed full beard, thick black hair in an undercut with the top swept neatly back; a white polo shirt "
     "with a folded collar, black-framed sunglasses hooked on the collar, a brown leather strap watch and a thin leather bracelet; sporty, smart, friendly style",
     giong("nam", "in his mid twenties", "a warm low-mid baritone, clearly lower than the tutor's voice", "relaxed and a little charming"), "28"),
    ("bien-the-12-nam-29",
     "a 29-year-old Mexican man, tall and lean with moderately broad shoulders, a long face with a slightly pointed chin, high cheekbones and deep-set eyes, "
     "light brown skin with a warm golden undertone, clean shaven, dark brown-black hair ear length swept to one side with slight volume; a grey turtleneck "
     "sweater under a long black wool coat, a grey wool scarf around the neck; elegant, mature, slightly quiet winter style",
     giong("nam", "in his late twenties", "a calm low-mid baritone, clearly lower than the tutor's voice", "quiet and thoughtful"), "28"),
    ("bien-the-13-nam-24",
     "a 24-year-old Mexican man, slim but wiry build, an oval face with a soft jawline, slightly full cheeks, big brown eyes and a natural smile, light "
     "honey-brown skin with a thin neatly trimmed moustache, short natural curly black hair cut short at the sides with the fringe falling lightly on the "
     "forehead; a mid-blue denim shirt with the sleeves rolled to the elbow, a thin silver bracelet; young, easygoing, creative style",
     giong("nam", "in his early twenties", "an easy mid-low pitch, lighter than an older man's", "friendly and easygoing"), "28"),
    ("bien-the-14-nam-32",
     "a 32-year-old Mexican man, solid build with big shoulders and a moderately thick neck, a rectangular face with a wide forehead, low cheekbones, a square "
     "jaw and a defined chin, slightly dark bronze-brown skin with short natural stubble, a black buzz cut close to the head; a fitted black t-shirt under a "
     "short black bomber jacket; masculine, strong, striking presence",
     giong("nam", "in his early thirties", "a deep low baritone, clearly lower than the tutor's voice", "steady and a little gruff"), "28"),
    ("bien-the-15-nam-28",
     "a 28-year-old Mexican man, tall and lean with level shoulders, an oval face with a moderately defined jawline, a slightly broad nose, full lips and dark "
     "brown eyes, warm caramel-brown skin with a few small moles and clean shaven, black hair past the nape tied in a neat low ponytail with a centre part; a "
     "teal two-piece suit blazer with a modern two-button cut over a white spread-collar shirt with no tie, a white pocket square, a minimal silver ring; "
     "stylish, artistic, creative look",
     giong("nam", "in his late twenties", "a warm mid-low baritone, clearly lower than the tutor's voice", "smooth and expressive"), "28"),
    ("bien-the-16-nu-64",
     "a 64-year-old Mexican woman, medium build, a little fuller around the middle with rounded shoulders, a round face with slightly sagging cheeks and light "
     "wrinkles around the eyes and mouth, light olive-brown skin with small age spots and natural uneven pigmentation, grey-and-dark-brown hair about half and "
     "half, short with light volume and a side part; a white round-neck blouse with a tiny floral print and three-quarter sleeves, a small pearl necklace and "
     "round gold earrings; clean, ironed, gentle traditional style",
     giong("nu", "in her mid sixties", "a soft, slightly thin and mildly husky mid-pitch voice", "kind and gently amused, a little slower than a young speaker"), "68"),
    ("bien-the-17-nu-70",
     "a 70-year-old Mexican woman, a full build with rounded shoulders, a softly square face with a rounded chin and full cheeks, small wrinkles around the eyes "
     "and the corners of the mouth, medium honey-brown skin with a few dark spots on the cheeks, white hair in a short chin-length bob with natural volume and a "
     "side part; a light-purple cardigan with small buttons over a white round-neck t-shirt, small gold earrings and a silver bracelet; simple, cheerful everyday style",
     giong("nu", "in her seventies", "a soft, slightly husky older voice", "cheerful and chatty, a bit slower than a young speaker"), "68"),
    ("bien-the-18-nu-75",
     "a 75-year-old Mexican woman, small and thin with narrow shoulders and a slightly natural stoop, a long face with high cheekbones, slightly hollow cheeks and "
     "thin lips, clear wrinkles on the forehead and around the mouth, medium bronze-brown skin with age spots and realistic skin texture, white-grey hair in a "
     "neat low bun at the nape with a few loose strands at the temples; a dark-green long-sleeved round-neck top with a thin cream wool shawl draped around the "
     "shoulders, thin gold-framed glasses and small round earrings; neat, classic, graceful style",
     giong("nu", "in her mid seventies", "a thin, light and slightly husky older voice", "refined and gentle, noticeably slower than a young speaker"), "68"),
    ("bien-the-19-nu-67",
     "a 67-year-old Mexican woman, tall with moderately broad shoulders, an oval face with a soft jawline, natural wrinkles on the cheeks and slight shadows "
     "under the eyes, warm golden-brown skin with small pigment spots, brown hair mixed with grey, shoulder-length in gentle natural waves tied in a neat low "
     "ponytail; a white shirt with a spread collar under an earth-orange knitted wool vest, thin brown-framed glasses and minimal gold earrings; intellectual, "
     "elegant everyday style",
     giong("nu", "in her late sixties", "a clear, slightly husky mid-low voice", "thoughtful and warm, a little slower than a young speaker"), "68"),
    ("bien-the-20-nu-72",
     "a 72-year-old Mexican woman, short and round with sloping shoulders, a plump round face with full cheeks, a slight double chin and small wrinkles around "
     "the eyes, light olive-brown skin with a few age spots on the cheeks, short white curly hair close to the head with natural volume and a side part, neatly "
     "combed; a navy long-sleeved dress with small white polka dots under a thin cream cardigan, a small pearl earring and a thin gold bracelet; warm, kindly, polite and tidy style",
     giong("nu", "in her early seventies", "a soft, warm and slightly thin older voice", "grandmotherly and kind, a bit slower than a young speaker"), "68"),
]


def luot(tuoi):
    """15 lượt như video mẫu (câu nối liền của cùng một người gộp thành một lượt). Câu sai: chữ đỏ + viền đỏ; câu nói lại đúng: chữ xanh + viền xanh."""
    L = [
        ("day", "Do you speak English?", "friendly"),
        ("hoc", "Um, more or less.", "hesitant"),
        ("day", "How old are you?", "curious"),
        ("hoc", f"I have {tuoi}.", "unsure", {"c": "red", "fx": "wrong"}),
        ("day", f"You have to say, I am {tuoi}.", "patient, encouraging"),
        ("hoc", f"I am {tuoi}.", "confident", {"c": "green", "fx": "right"}),
        ("day", "Good job.", "warm, encouraging"),
        ("hoc", "Thank you, but who are you?", "curious"),
        ("day", "Me? I'm an AI tutor. I'll help you improve your English skills.", "cheerful"),
        ("hoc", "Thank you, but I don't have money.", "worried"),
        ("day", "What money? You can study for free.", "playful"),
        ("hoc", "For free? You're joking, right?", "surprised, skeptical"),
        ("day", "Nope, I'm serious. You can practice unlimited English conversations with a real AI avatar. Anytime, anywhere.", "confident, enthusiastic"),
        ("hoc", "Really?", "surprised, hopeful"),
        ("day", "Yes, really. You'll sound like a native in no time.", "reassuring, upbeat"),
    ]
    out = []
    for who, text, emo, *extra in L:
        t = {"who": who, "text": text, "emo": emo, "fx": "none"}
        t.update(extra[0] if extra else {})
        out.append(t)
    return out


res = []
for i, (name, nguoi, giong_hoc, tuoi) in enumerate(BIEN_THE, 1):
    anh = f"{DU_AN}/anh/nhan-vat/bien-the-{i:02d}.webp"
    assert os.path.isfile(os.path.join(HERE, "..", "..", "..", anh)), anh
    v = {"name": name, **CHUNG, "NGUOI_HOC": nguoi, "GIONG_HOC": giong_hoc, "LUOT": luot(tuoi),
         "refs": {"NGUOI_DAY": [ROBOT], "NGUOI_HOC": [anh]}}
    res.append(v)
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(res))
