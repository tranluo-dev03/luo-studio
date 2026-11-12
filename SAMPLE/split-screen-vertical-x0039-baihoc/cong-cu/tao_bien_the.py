"""Sinh SAMPLE/split-screen-vertical-x0039-baihoc/BIEN-THE-X0039-BAI-HOC-20.json từ bảng X0039_20-bien-the-split-screen-BAI-HOC.csv (20 biến thể nhân vật Brazil, lời thoại tiếng Anh, bài học "Where are you from?").
Sửa bảng BIEN_THE (nhân vật, giọng), PLACE hoặc luot() rồi chạy:
    .venv/Scripts/python.exe SAMPLE/split-screen-vertical-x0039-baihoc/cong-cu/tao_bien_the.py
Ảnh nhân vật: anh/nhan-vat/bien-the-NN.webp (tải từ link Drive trong CSV); ảnh robot: anh/robot-ai.webp.
Tuổi trong tên/mô tả giữ theo bảng nhưng KHÔNG đưa vào lời thoại (kịch bản X0039 không có câu tuổi)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "BIEN-THE-X0039-BAI-HOC-20.json")
DU_AN = "SAMPLE/split-screen-vertical-x0039-baihoc"
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
    "NEN_HOC": "a cosy Brazilian café corner: a plain warm-cream wall with a colourful hand-painted Brazilian folk-art panel (yellow, green, blue and orange geometric "
               "pattern) hanging on a thin wooden rod above and behind the head, a strip of blue-and-white azulejo tiles at the far right edge, soft warm daylight",
    "DAO_BAN": "a small white porcelain cup of black cafezinho coffee just left of centre, and a golden round pão de queijo cheese bread on a small wooden plate just "
               "right of centre",
}


def giong(gioi, nhom_tuoi, am, tinh, vung):
    who = "woman" if gioi == "nu" else "man"
    pron = "actress" if gioi == "nu" else "actor"
    return (f"a real Brazilian {who} {nhom_tuoi}, speaking English as a second language with a natural light {vung} Brazilian accent: {am}, "
            f"{tinh}; a real person, not an {pron}")


# (tên, ngoại hình, giọng, tuổi nói, giới)  Ảnh: anh/nhan-vat/bien-the-NN.webp
BIEN_THE = [
    ("bien-the-01-nu-20-bahia",
     "a 20-year-old Brazilian woman from Bahia, petite with narrow shoulders, a round face with full cheeks, big brown eyes and full lips, deep brown glowing skin, "
     "short black afro-textured curly hair close to the head under a neatly tied white turban (torço); a white lace blouse with puffed sleeves, a multicoloured "
     "beaded necklace, gold earrings and a silver bracelet; bright, cheerful traditional baiana style",
     giong("nu", "in her early twenties", "bright mid-high pitch", "warm and playful, a smile in the voice", "Bahian"), 20, "nu"),
    ("bien-the-02-nu-23-rio",
     "a 23-year-old Brazilian woman from Rio de Janeiro, tall with clear curves and balanced shoulders, a heart-shaped face with high cheekbones, almond-shaped brown "
     "eyes and full lips, sun-tanned bronze-brown skin, dark brown hair down to the mid back in voluminous waves with a rhinestone headband; a fitted green sequin "
     "samba dress with a matching sheer chiffon shawl over the shoulders, long rhinestone drop earrings and a gold bracelet; dazzling, glamorous samba style",
     giong("nu", "in her early twenties", "bright, lively mid-high pitch", "flirty, energetic and fun", "Carioca"), 23, "nu"),
    ("bien-the-03-nu-26-pernambuco",
     "a 26-year-old Brazilian woman from Pernambuco, balanced build with sloping shoulders, an oval face with moderate cheekbones, big brown eyes and a wide smile, "
     "light honey-brown skin, dark brown hair past the shoulders in soft waves tied half-up with a multicoloured ribbon; a vivid yellow-orange-red layered ruffle "
     "dress with a square neckline and puffed sleeves, large gold hoop earrings and a wooden-bead necklace; bright, joyful, energetic frevo style",
     giong("nu", "in her mid twenties", "bright mid pitch", "cheerful and energetic", "Pernambuco"), 26, "nu"),
    ("bien-the-04-nu-31-minas",
     "a 31-year-old Brazilian woman from Minas Gerais, balanced build with sloping shoulders, an oval face with moderate cheekbones and big brown eyes, medium olive-brown "
     "skin, long brown hair down to the mid back in a thick braid over one shoulder, a wide-brimmed straw hat; a white floral short-sleeved maxi dress with a fabric "
     "belt, small gold earrings and a beaded necklace; gentle, feminine countryside (caipira) style",
     giong("nu", "around thirty", "soft mid pitch", "gentle and friendly", "Mineiro"), 31, "nu"),
    ("bien-the-05-nu-35-parana",
     "a 35-year-old Brazilian woman from Paraná of German descent, tall with balanced shoulders, an oval face with high cheekbones, green eyes and thin lips, fair "
     "bright skin, golden-brown hair down to the mid back in two thick braids; a blue floral dirndl dress with a white puffed-sleeve blouse and a white apron tied at "
     "the waist, silver earrings and a silver bracelet; elegant, gentle traditional German-Brazilian style",
     giong("nu", "in her mid thirties", "clear mid pitch", "calm, kind and polite", "Southern Brazilian"), 35, "nu"),
    ("bien-the-06-nu-40-ceara",
     "a 40-year-old Brazilian woman from Ceará, balanced build with sloping shoulders, a heart-shaped face with moderate cheekbones, big brown eyes and light wrinkles "
     "around the eyes, light bronze-brown skin, dark brown hair down to the mid back pinned in a neat low bun at the nape; a white lace dress with a white lace shawl, "
     "a pearl necklace, pearl earrings and a silver bracelet; elegant, gentle traditional Ceará style",
     giong("nu", "around forty", "steady mid pitch", "warm, calm and graceful", "Nordestino"), 40, "nu"),
    ("bien-the-07-nu-47-goias",
     "a 47-year-old Brazilian woman from Goiás, average build, a little full, a softly square face with high cheekbones, dark brown eyes and light wrinkles around the "
     "eyes and mouth, deep olive-brown skin, dark brown shoulder-length hair in gentle waves under a brown cowboy hat; a red-and-black checked long-sleeved shirt, "
     "gold earrings and a leather bracelet; strong, free-spirited country (sertaneja) style",
     giong("nu", "in her late forties", "confident mid-low pitch", "friendly and direct", "Goiano"), 47, "nu"),
    ("bien-the-08-nu-55-rs",
     "a 55-year-old Brazilian woman from Rio Grande do Sul, average build, a little full, an oval face with slightly sagging cheeks and light wrinkles around the eyes "
     "and mouth, light olive-white skin, brown hair with silver strands, shoulder-length and pinned in a low bun, a brown wide-brimmed hat; a white blouse with a "
     "turned-down collar and a red neckerchief (lenço) around the neck, gold earrings and a silver bracelet; formal, calm traditional gaúcha style",
     giong("nu", "in her mid fifties", "even mid-low pitch", "calm, composed and warm", "Gaúcho"), 55, "nu"),
    ("bien-the-09-nu-64-bahia",
     "a 64-year-old Brazilian woman from Bahia, short and a little plump with rounded shoulders, a broad face with a slight double chin and deep wrinkles around the "
     "eyes and mouth, warm deep brown skin, short grey-silver hair under a neatly tied white turban (torço); a white long-sleeved lace blouse with a white lace shawl, "
     "a multicoloured beaded necklace and large gold earrings, a silver bracelet; dignified, respectful traditional baiana style",
     giong("nu", "in her mid sixties", "a soft, slightly husky mid-pitch voice", "kind and gently amused, a little slower than a young speaker", "Bahian"), 64, "nu"),
    ("bien-the-10-nu-72-amazonas",
     "a 72-year-old Brazilian woman from Amazonas, short and slightly thin with narrow shoulders and a slight stoop, a long face with high cheekbones and deep "
     "wrinkles around the eyes and mouth, dark bronze-brown skin with small age spots, short white hair cut at ear level and neatly combed; a white dress with a green "
     "leaf print and a matching fabric shawl, a wooden-bead necklace, gold earrings and a wooden bracelet; rustic, dignified Amazon style",
     giong("nu", "in her seventies", "a thin, light and slightly husky older voice", "gentle and wise, noticeably slower than a young speaker", "Amazonian"), 72, "nu"),
    ("bien-the-11-nam-24-bahia",
     "a 24-year-old Brazilian man from Bahia, solid build with broad shoulders, a square face with a defined jawline, dark brown eyes and short stubble, deep brown "
     "glowing skin, short black afro-textured curly hair close to the head; a white tank top with a yellow-and-green rope (corda) belt knot just visible, a "
     "multicoloured fabric wristband; strong, energetic capoeira style",
     giong("nam", "in his mid twenties", "a warm low-mid baritone, clearly lower than the tutor's voice", "energetic and upbeat", "Bahian"), 24, "nam"),
    ("bien-the-12-nam-27-sp",
     "a 27-year-old Brazilian man from São Paulo, balanced build with moderately broad shoulders, an oval face with big brown eyes, a wide smile and a short neatly "
     "trimmed full beard, medium olive-brown skin, black hair in a low fade with the top swept back, a Panama straw hat; a white linen shirt with a turned-down collar, "
     "a thin gold chain and a brown leather-strap watch; smart, cheerful samba-man style",
     giong("nam", "in his late twenties", "a relaxed low-mid baritone, clearly lower than the tutor's voice", "cheerful and charming", "Paulista"), 27, "nam"),
    ("bien-the-13-nam-30-rs",
     "a 30-year-old Brazilian man from Rio Grande do Sul, solid build with broad shoulders, a square face with a sharp jawline, dark brown eyes and a short full beard, "
     "light olive skin slightly sun-tanned, thick dark-brown slightly wavy hair swept back under a brown wide-brimmed hat; a white shirt with a turned-down collar "
     "under a red-and-black striped wool poncho; strong, free-spirited gaúcho style",
     giong("nam", "around thirty", "a deep, steady low baritone, clearly lower than the tutor's voice", "calm and strong", "Gaúcho"), 30, "nam"),
    ("bien-the-14-nam-36-minas",
     "a 36-year-old Brazilian man from Minas Gerais, solid build with broad shoulders, a square face with a defined jawline, dark brown eyes and a short full beard, "
     "warm golden-brown skin, a brown cowboy hat; a red-and-black checked long-sleeved shirt under a brown leather vest; strong, free-spirited country (sertanejo) style",
     giong("nam", "in his mid thirties", "a deep low baritone, clearly lower than the tutor's voice", "steady and friendly", "Mineiro"), 36, "nam"),
    ("bien-the-15-nam-41-ceara",
     "a 41-year-old Brazilian man from Ceará, average build, a little full with a slightly round belly, a round face with full cheeks, small dark brown eyes and a "
     "short moustache, light bronze-brown skin, a wide-brimmed straw hat; a short-sleeved blue-and-white checked shirt with a red bandana knotted around the neck; "
     "cheerful, friendly forró style",
     giong("nam", "in his early forties", "a warm mid-low baritone, clearly lower than the tutor's voice", "jovial and friendly", "Nordestino"), 41, "nam"),
    ("bien-the-16-nam-48-amazonas",
     "a 48-year-old Brazilian man from Amazonas, thin with slightly sloping shoulders, a long slightly gaunt face with high cheekbones, deep-set brown eyes and a "
     "stubbly grey-flecked moustache, dark sun-weathered brown skin with many wrinkles and dark spots, short thinning black-and-grey hair under a wide-brimmed straw "
     "hat; a beige linen long-sleeved shirt with the sleeves rolled to the elbow, the strap of a canvas crossbody bag; rustic, experienced Amazon fisherman style",
     giong("nam", "in his late forties", "a dry, slightly husky low-mid voice, clearly lower than the tutor's voice", "plain, quiet and weathered", "Amazonian"), 48, "nam"),
    ("bien-the-17-nam-56-pernambuco",
     "a 56-year-old Brazilian man from Pernambuco, stocky build with a slightly big belly and broad shoulders, a round face with full cheeks, small dark brown eyes and "
     "a short salt-and-pepper full beard, warm deep brown skin with deep wrinkles around the eyes and mouth, short black-and-grey hair, a multicoloured embroidered "
     "maracatu hat; an embroidered multicoloured patterned robe over a white shirt; vibrant, majestic maracatu style",
     giong("nam", "in his mid fifties", "a rich, deep low baritone, clearly lower than the tutor's voice", "proud and warm", "Pernambuco"), 56, "nam"),
    ("bien-the-18-nam-62-parana",
     "a 62-year-old Brazilian man from Paraná of German descent, average build, a little full with a slightly round belly, a round face with full cheeks, small blue "
     "eyes and a short silver moustache, fair bright skin with small age spots, short white-silver hair, a green felt hat; a short-sleeved red-and-white checked "
     "shirt; cheerful, friendly traditional German-Brazilian style",
     giong("nam", "in his early sixties", "a warm mid-low baritone, clearly lower than the tutor's voice", "jolly and friendly", "Southern Brazilian"), 62, "nam"),
    ("bien-the-19-nam-69-goias",
     "a 69-year-old Brazilian man from Goiás, short and stocky with broad shoulders and a slightly round belly, a square face with high cheekbones, small dark brown "
     "eyes and a salt-and-pepper moustache, dark bronze-brown skin with many wrinkles, short black-and-grey hair under a brown leather cowboy hat; a long-sleeved "
     "blue-and-black checked shirt under a brown leather vest, a red bandana around the neck; rustic, sturdy vaqueiro country style",
     giong("nam", "in his late sixties", "a gravelly, low older voice, clearly lower than the tutor's voice", "plain, sturdy and a little slower than a young speaker", "Goiano"), 69, "nam"),
    ("bien-the-20-nam-77-rio",
     "a 77-year-old Brazilian man from Rio de Janeiro, short and slightly thin with narrow shoulders and a clear stoop, a long face with high cheekbones and slightly "
     "hollow cheeks, deep wrinkles around the eyes and mouth, light olive-brown skin with age spots, short thinning white hair under a white Panama hat; a white linen "
     "shirt with a turned-down collar, thin metal-framed glasses; elegant, dignified carioca style",
     giong("nam", "in his late seventies", "a thin, soft and slightly husky older male voice, still lower than the tutor's voice", "refined and gentle, noticeably slower than a young speaker", "Carioca"), 77, "nam"),
]


def luot(place, gioi):
    """15 lượt theo kịch bản CSV X0039 (tiếng Anh, bài học "Where are you from?"). Câu sai: chữ đỏ + viền đỏ; câu nói lại đúng: chữ xanh + viền xanh.
    Kịch bản CSV ghi quê "Mexico" cho mọi biến thể dù nhân vật gốc Brazil: đổi PLACE (và câu sai/đúng) ở đây nếu cần."""
    L = [
        ("day", "Hi! Are you ready to practice English?", "friendly"),
        ("hoc", "Yes, I'm ready!", "cheerful"),
        ("day", "Where are you from?", "curious"),
        ("hoc", f"I am {place}.", "unsure", {"c": "red", "fx": "wrong"}),
        ("day", f"You should say, I'm from {place}.", "patient, encouraging"),
        ("hoc", f"I'm from {place}.", "confident", {"c": "green", "fx": "right"}),
        ("day", "Good job!", "warm, encouraging"),
        ("hoc", "Thank you, but who are you?", "curious"),
        ("day", "Me? I'm Talka AI, an AI tutor. I'll help you improve your English skills.", "cheerful"),
        ("hoc", "Thank you, but I don't have money.", "worried"),
        ("day", "What money? You can study for free.", "playful"),
        ("hoc", "For free? You're joking, right?", "surprised, skeptical"),
        ("day", "Nope, I'm serious! You can practice unlimited English conversations with a real AI avatar, anytime, anywhere.", "confident, enthusiastic"),
        ("hoc", "Really?", "surprised, hopeful"),
        ("day", "Yes, really! You'll sound like a native in no time. Just download Talka AI!", "reassuring, upbeat"),
    ]
    out = []
    for who, text, emo, *extra in L:
        t = {"who": who, "text": text, "emo": emo, "fx": "none"}
        t.update(extra[0] if extra else {})
        out.append(t)
    return out


PLACE = "Mexico"


res = []
for i, (name, nguoi, giong_hoc, tuoi, gioi) in enumerate(BIEN_THE, 1):
    anh = f"{DU_AN}/anh/nhan-vat/bien-the-{i:02d}.webp"
    assert os.path.isfile(os.path.join(HERE, "..", "..", "..", anh)), anh
    assert (gioi == "nu") == (i <= 10)
    v = {"name": name, **CHUNG, "NGUOI_HOC": nguoi, "GIONG_HOC": giong_hoc, "LUOT": luot(PLACE, gioi),
         "refs": {"NGUOI_DAY": [ROBOT], "NGUOI_HOC": [anh]}}
    res.append(v)
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(res))
