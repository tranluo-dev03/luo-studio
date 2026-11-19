"""Sinh SAMPLE/chia-doi-gia-su-ai/BIEN-THE-CHIA-DOI-GIA-SU-AI.json.
Sửa bảng BIEN_THE (nhân vật, giọng, ảnh, tuổi trong câu sai/đúng) hoặc LUOT rồi chạy:
    runtime\\python.exe SAMPLE\\chia-doi-gia-su-ai\\cong-cu\\tao_bien_the.py
Lời thoại đúng như video mẫu (2110_langlearn vertical EN); câu "You're joking, right?" Whisper nghe nhầm thành "Huge jumping", phụ đề mẫu ghi đúng.
Ảnh tham chiếu: link Google Drive dạng chia sẻ dán thẳng được (Studio tự đổi sang link tải); ảnh robot là tệp trong thư mục anh/ (đường dẫn tính từ thư mục gốc)."""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-CHIA-DOI-GIA-SU-AI.json")
ROBOT = "SAMPLE/chia-doi-gia-su-ai/anh/robot-ai.webp"

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

# (tên, ngoại hình, giọng, link ảnh, tuổi nói trong câu sai/đúng)
BIEN_THE = [
    ("bien-the-01-co-gai-23",
     "a 23-year-old Mexican woman, softly curvy build, an oval face with slightly full cheeks, a small rounded nose and naturally full lips, light honey-brown skin "
     "with a few small freckles across the nose bridge, long chocolate-brown hair past the chest in loose waves with a centre part, the front strands framing the cheeks; "
     "a thin cream knit top with a square neckline and short sleeves, thin gold hoop earrings, the strap of a small brown leather shoulder bag on one shoulder; "
     "feminine, natural weekend-café style",
     "a real young Mexican woman in her early twenties speaking English as a second language: bright mid-high pitch, a natural Mexican accent with Spanish vowels "
     "and a soft r, warm and playful, a smile in the voice; a real person, not an actress",
     "https://drive.google.com/file/d/14qtDANFsKChhfxHc3YmQ1KGwiGWhjjgY/view?usp=sharing", "28"),
    ("bien-the-12-doanh-nhan-28",
     "a 28-year-old Mexican man, tall and lean with moderately broad shoulders, a long face with a slightly pointed chin, high cheekbones, deep-set eyes and a slim "
     "nose, light brown skin with a warm golden undertone, a short neatly trimmed full beard, thick dark-brown slightly curly hair brushed back loosely with a little "
     "volume; a tailored charcoal-grey two-button suit jacket over a black shirt with no tie and the top button open, a simple white pocket square; "
     "a stylish, masculine young businessman look",
     "a real young Mexican man in his late twenties speaking English as a second language: a warm low-mid baritone, clearly lower than the tutor's voice, a natural "
     "Mexican accent with Spanish vowels and a soft r, relaxed and a little charming; a real person, not an actor",
     "https://drive.google.com/file/d/1_4ch3_SFnA3RhfcClRpsKtq8Ul7gmiKO/view?usp=sharing", "28"),
    ("bien-the-19-ba-79",
     "a 79-year-old Mexican woman, small and slightly thin with sloping shoulders, an oval face with sagging cheeks, deep wrinkles at the corners of the mouth, on "
     "the forehead and neck, slightly deep-set eyes, medium olive-brown skin with natural age spots, short silver-white hair cut at ear level with soft volume and a "
     "side part, neatly combed; a thin dusty-pink crew-neck knit sweater with a white shirt collar showing, a small navy-and-cream geometric silk scarf loosely around "
     "the neck; neat, warm, modest grandmother style",
     "a real Mexican grandmother in her late seventies speaking English as a second language: a soft, slightly thin and husky older voice, a natural Mexican accent, "
     "kind and gently amused, a bit slower than a young speaker; a real person, not an actress",
     "https://drive.google.com/file/d/17M2lKhEW7L1NzJHqb3MOHEdT_VaiDt6X/view?usp=sharing", "68"),
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
for name, nguoi, giong, link, tuoi in BIEN_THE:
    v = {"name": name, **CHUNG, "NGUOI_HOC": nguoi, "GIONG_HOC": giong, "LUOT": luot(tuoi),
         "refs": {"NGUOI_DAY": [ROBOT], "NGUOI_HOC": [link]}}
    res.append(v)
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(res))
