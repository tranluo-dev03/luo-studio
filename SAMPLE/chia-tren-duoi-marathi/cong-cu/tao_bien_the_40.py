"""Sinh SAMPLE/chia-tren-duoi-marathi/BIEN-THE-CHIA-TREN-DUOI-MARATHI-40-BIEN-THE.json từ CSV "40 biến thể_Horizontal HINDI - kịch bản".
Chạy:  .venv\\Scripts\\python.exe SAMPLE\\chia-tren-duoi-marathi\\cong-cu\\tao_bien_the_40.py [đường dẫn CSV]
- Lời thoại lấy từ phần "Kịch bản" của CSV (Robot / Nam), tên app đổi Aiva AI -> Talka AI (APP). Mỗi lượt <= 20 từ.
- Mỗi biến thể: mô tả người học + mô tả nền (CSV là tiếng Việt, bảng ANH dưới đây là bản tiếng Anh), link ảnh người học (refs NGUOI_HOC) và ảnh nền (refs NEN_HOC)
  lấy từ CSV (Studio tự tải link Drive khi tạo dự án).
- Kịch bản viết cho người học NAM. Biến thể NỮ: động từ nói VỀ người học được đổi giống (गेला होतास -> गेली होतीस, कसा -> कशी, म्हणालास -> म्हणालीस)."""
import csv
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_DEFAULT = r"G:\.shortcut-targets-by-id\18RHYCy9H0VKucU3z-IsYEnXWIepl_N4K\NHIPTY\40 biến thể_Horizontal HINDI - kịch bản .csv"
OUT = os.path.join(HERE, "..", "BIEN-THE-CHIA-TREN-DUOI-MARATHI-40-BIEN-THE.json")
APP = "Talka AI"

_spec = importlib.util.spec_from_file_location("tao_bien_the", os.path.join(HERE, "tao_bien_the.py"))
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)
CHUNG = {k: v for k, v in _m.CHUNG.items() if k != "NEN_HOC"}
ROBOT = "SAMPLE/chia-tren-duoi-marathi/anh/robot-ai.webp"


def luot(nu):
    gv = (lambda nam, nu_: nu_ if nu else nam)
    return [
        ("day", gv("काल कुठे गेला होतास?", "काल कुठे गेली होतीस?"), "friendly, curious"),
        ("hoc", "I go yesterday to the market.", "unsure"),
        ("day", 'कालची गोष्ट आहे, त्यामुळे "go" नाही, "went" बोल. "I went to the market yesterday."', "encouraging"),
        ("day", gv("Market मध्ये कसा गेला होतास?", "Market मध्ये कशी गेली होतीस?"), "friendly, curious"),
        ("hoc", "I go by bus.", "unsure"),
        ("day", gv('Almost बरोबर आहे. पण चांगलं होईल जर तू म्हणालास, "I went by bus."', 'Almost बरोबर आहे. पण चांगलं होईल जर तू म्हणालीस, "I went by bus."'), "encouraging"),
        ("hoc", "ओह! माझी इंग्लिश खरंच खूप weak आहे.", "embarrassed"),
        ("day", f"काही हरकत नाही. {APP} try केलंस का?", "reassuring"),
        ("hoc", f"{APP}, ते काय आहे?", "curious"),   # CSV: "<app> काय आहे?"; dấu phẩy để nói liền, không ngắt sau tên app
        ("day", "English बोलण्याची practice करण्यासाठी मी तुझी personal AI teacher आहे.", "enthusiastic"),
        ("day", "तू रोज फक्त पंधरा-वीस मिनिटं माझ्याशी बोल. तुझा confidence वाढेल.", "warm"),
        ("hoc", "पण माझं English तर खूप weak आहे.", "worried"),
        ("day", "काही हरकत नाही. तुझं English level कसंही असो, मी त्यानुसार तुझ्यासोबत practice करेन.", "reassuring"),
        ("day", "आणि सर्वात चांगली गोष्ट म्हणजे तुला सगळं समजून घेण्यासाठी फक्त English मध्ये बोलण्याची गरज नाही.", "enthusiastic"),
        ("day", "मी तुला मराठीच्या माध्यमातून English शिकवेन. तर काहीच tension नाही.", "warm"),
        ("day", "तू जितक्या वेळा चुकीचं बोलशील, मी तितक्या वेळा तुला योग्य पद्धतीने समजावेन आणि तुझं English correct करेन.", "reassuring"),
        ("day", "तुला कोणी judge करणार सुद्धा नाही.", "warm"),
        ("day", f"मग आता वेळ घालवू नकोस. खाली दिलेल्या download button वर click कर आणि आत्ताच {APP} डाउनलोड कर.", "enthusiastic"),
    ]


# STT: (giới, tuổi, ngoại hình EN, nền EN)
ANH = {
    1: ("M", 25, "a young Indian man of about 25, brown skin, short messy black hair, light stubble, furrowed brows, mouth slightly open, a worried, confused look; a faded, wrinkled, stained old beige crew-neck t-shirt with a frayed collar",
        "a luxurious book café: wooden shelves full of books, brown leather chairs, warm yellow lamps, a large glass window onto the street, potted green plants"),
    2: ("F", 30, "an Indian woman of about 30, brown skin, long black hair tied low at the nape, a tired sad face with dark circles under the eyes, lips closed; a faded, wrinkled old beige long-sleeved cotton kurta of thin, worn fabric",
        "a luxurious Indian restaurant: polished wooden tables, yellow lanterns, Indian paintings on the wall, red velvet chairs, potted green plants"),
    3: ("M", 50, "an older Indian man of about 50, dark brown skin, black hair greying at the sides, a grey moustache, a deeply lined face, a tired, resigned look; an old faded wrinkled long-sleeved blue-and-brown check shirt with frayed buttons, thin worn cotton",
        "a luxurious chess club: wooden chessboards, brown leather chairs, warm yellow light, dark wooden bookshelves, a decorative fireplace"),
    4: ("F", 22, "a young Indian woman of about 22, brown skin, curly black hair tied high, big eyes, mouth slightly open, a surprised look turning to face the camera; an old faded pink sari with a worn pattern, thin wrinkled cotton, a matching short-sleeved blouse, the sari draped over one shoulder",
        "a luxurious Indian mansion courtyard: carved stone pillars, greenery, a small fountain, yellow lanterns, a clean stone floor"),
    5: ("M", 35, "an Indian man of about 35, brown skin, black hair greying a little, a short beard, a thoughtful face; an old grey-brown shirt with a frayed collar, old dark trousers, dusty shoes",
        "a luxurious architect's office: a large drafting table, house models, warm yellow desk lamps, wooden bookshelves, large windows"),
    6: ("F", 65, "an elderly Indian woman of about 65, wrinkled brown skin, grey hair in a low bun, a tired sad face; an old faded brown sari with a matching short-sleeved blouse, old sandals",
        "a luxurious traditional Indian veranda: carved wooden pillars, wicker chairs, greenery, yellow lanterns, a clean tiled floor"),
    7: ("M", 25, "a young Indian man of about 25, brown skin, short black hair, a thin moustache, a worried face; an old yellowed white shirt, faded torn blue jeans, old sandals",
        "a luxurious outdoor café: white parasols, wooden tables, greenery, a view onto the street, soft sunlight"),
    8: ("F", 60, "an Indian woman of about 60, brown skin, grey hair streaked with black tied low, a tired face; an old faded green salwar kameez with matching loose trousers, old sandals",
        "a luxurious Indian palace garden: red roses, a fountain, white stone benches, yellow lanterns, a stone path"),
    9: ("M", 45, "an Indian man of about 45, brown skin, short black hair, a thick black beard, a stern face; an old faded white kurta, old dark trousers, old sandals",
        "a luxurious Indian temple hall: white marble pillars, yellow oil lamps, fresh flowers, a clean polished stone floor"),
    10: ("F", 18, "a young Indian woman of about 18, brown skin, long black hair in a single braid over the shoulder, a gentle face; an old faded pink churidar set with a matching long-sleeved top, a thin shawl, dusty old sandals",
         "a luxurious traditional Indian dance studio: large mirrors, a polished wooden floor, warm yellow light, silk curtains, potted green plants"),
    11: ("M", 27, "a young Indian man of about 27, brown skin, long black hair in a low ponytail, a short full beard, an embarrassed face looking down; an old faded blue t-shirt with a frayed collar, faded black jeans torn at the knee, old flip-flops",
         "a luxurious indoor basketball court: a polished wooden floor, basketball hoops, bright white lights, spectator seats, glass walls"),
    12: ("M", 30, "a young Indian man of about 30, brown skin, black hair slicked neatly with gel, a thick moustache, a tense face biting his lip; an old yellowing white shirt with a stained collar, faded black trousers, old peeling leather shoes",
         "a luxurious modern company office: a tidy desk, a black leather swivel chair, large glass windows onto the city, potted green plants"),
    13: ("M", 26, "a young Indian man of about 26, brown skin, short curly black hair, light stubble, a blank, bewildered face looking into the camera; an old denim jacket torn at the shoulder, a yellowed white t-shirt under it, faded blue jeans, old flip-flops",
         "a luxurious rooftop bar: high stools, warm yellow lights, a wooden bar counter, a view of the city lit up at night"),
    14: ("M", 32, "a young Indian man of about 32, brown skin, black hair slightly receding at the temples, a long black beard, a sad face looking down; an old black t-shirt stained with oil, a frayed collar, faded dark trousers, oil-stained flip-flops",
         "a luxurious high-end car garage: gleaming luxury cars, tools hung neatly, a clean shiny floor, bright white lights"),
    15: ("M", 29, "a young Indian man of about 29, brown skin, shoulder-length black hair, a short beard, an anxious face looking down; an old brown sweater with worn sleeves, an old white shirt under it, faded grey trousers, old flip-flops",
         "a luxurious high-end apartment living room: a grey fabric sofa, wooden bookshelves, warm yellow lights, large glass doors, potted green plants"),
    16: ("M", 33, "a young Indian man of about 33, brown skin, short neat black hair, a thin moustache, a tired face, sighing; an old faded blue-and-white striped shirt with a frayed collar, old black trousers, old peeling leather shoes",
         "a luxurious garden café: wooden tables, white parasols, greenery, fresh flowers, soft sunlight"),
    17: ("M", 31, "a young Indian man of about 31, brown skin, messy black hair past the ears, scruffy stubble, a hopeless face looking into the camera; an old grey t-shirt torn at the shoulder, old faded cloth shorts, old flip-flops",
         "a luxurious high-end video-game lounge: big screens, gaming chairs, soft neon lights, a clean shiny floor"),
    18: ("M", 47, "an Indian man of about 47, brown skin, black hair half grey and combed neatly, a short grey beard, a stern face looking into the camera; an old yellowed white shirt, a frayed old tie, faded grey trousers, old leather shoes",
         "a luxurious law office: law bookcases up to the ceiling, a dark wooden desk, a green desk lamp, a brown leather chair"),
    19: ("M", 55, "an Indian man of about 55, brown skin, short neat white-grey hair, a short grey beard, a kind face with a slight smile; an old faded cream kurta, old white cloth trousers, old flip-flops",
         "a luxurious traditional Indian house garden: a large mango tree, stone benches, yellow lanterns, decorative terracotta walls"),
    20: ("M", 58, "an Indian man of about 58, brown skin, black hair heavily streaked with grey and combed neatly, a long greying beard, a pensive face looking into the distance; an old brown sweater worn at the elbows, an old white shirt under it, faded dark trousers, old flip-flops",
         "a luxurious home reading room: brown leather armchairs, warm yellow desk lamps, dark wooden bookshelves, a fireplace, a thick rug"),
    21: ("M", 46, "an Indian man of about 46, brown skin, thinning black hair combed neatly, a black moustache, a worried face with a wrinkled forehead; an old faded blue shirt, old black trousers, old peeling leather shoes",
         "a luxurious upscale grocery store: neat wooden shelves full of goods, warm yellow lights, a wooden checkout counter, a clean floor"),
    22: ("M", 52, "an Indian man of about 52, brown skin, grey hair combed back neatly, old-fashioned glasses, a focused face as if reading; an old grey blazer worn at the shoulders, an old white shirt, faded grey trousers, old leather shoes",
         "a prestigious university library: bookshelves up to the ceiling, a long wooden table, warm yellow desk lamps, large windows"),
    23: ("M", 60, "an Indian man of about 60, brown skin, short white-grey hair, a long grey beard, a calm face with closed eyes; an old faded white kurta, old white cloth trousers, bare feet",
         "a luxurious Indian temple courtyard: a large bodhi tree, yellow oil lamps, lotus flowers, a clean stone floor, a quiet atmosphere"),
    24: ("M", 48, "an Indian man of about 48, brown skin, black hair streaked with grey, a black moustache, an irritated frowning face; an old brown t-shirt dusted with sawdust, faded dark trousers, dusty old flip-flops",
         "a luxurious high-end woodworking workshop: a large wooden bench, tools hung neatly, a polished wooden floor, warm yellow lights, large windows"),
    25: ("M", 57, "an Indian man of about 57, brown skin, short neat grey hair, a tired face rubbing the forehead; an old yellowed white chef's jacket, faded dark trousers, old flip-flops",
         "a luxurious fine-dining restaurant kitchen: gleaming stainless-steel stoves, tidy utensils, bright white lights, neat spice shelves"),
    26: ("F", 19, "a young Indian woman of about 19, brown skin, long black hair loose over the shoulders, a shy face looking down; an old faded blue kurta, old white cloth trousers, old flip-flops",
         "a prestigious university campus: lush green lawns, an old tree, stone benches, a classic old building, soft sunlight"),
    27: ("F", 24, "a young Indian woman of about 24, brown skin, shoulder-length black hair, a self-conscious face with head lowered; an old faded blue sari with a worn pattern, a matching short-sleeved blouse, old flip-flops",
         "a luxurious handcraft embroidery workshop: wooden embroidery frames, bright coloured threads, warm yellow desk lamps, a large window onto a garden"),
    28: ("F", 26, "a young Indian woman of about 26, brown skin, black hair in a neat high bun, a worried face biting her lip; an old faded yellow salwar kameez with a matching dupatta, old flip-flops",
         "a luxurious Indian bridal dressing room: a large lighted mirror, fresh flowers, a velvet chair, warm yellow lights, silk curtains"),
    29: ("F", 21, "a young Indian woman of about 21, brown skin, black hair in two braids over the shoulders, an innocent face with a slight smile; an old faded white uniform blouse, an old blue skirt, old flip-flops",
         "a luxurious international school classroom: modern wooden desks and chairs, a whiteboard, bright lights, greenery, large windows"),
    30: ("F", 29, "a young Indian woman of about 29, brown skin, long black hair curled at the ends, a wistful sad face looking out of a window; an old faded purple kurta, old white cloth trousers, old flip-flops",
         "a luxurious Indian afternoon tea room: a wooden table, a silver teapot, velvet chairs, warm yellow lights, a window onto the garden"),
    31: ("F", 23, "a young Indian woman of about 23, brown skin, black hair half tied up, a tense face looking at a customer; an old faded orange sari, a matching short-sleeved blouse, old flip-flops",
         "a luxurious high-end flower market: colourful fresh flowers, wooden stalls, warm yellow lights, a glass dome roof, a clean floor"),
    32: ("F", 27, "a young Indian woman of about 27, brown skin, long curly black hair worn loose, a hesitant, shy face; an old faded green churidar set with a matching long-sleeved top, a thin shawl, old sandals",
         "a luxurious Indian silk showroom: colourful silks hung neatly, yellow spotlights, a polished wooden floor, a bench"),
    33: ("F", 72, "an elderly Indian woman of about 72, wrinkled brown skin, white hair in a neat high bun, old reading glasses, a kind face with a slight smile; an old faded white sari with a matching short-sleeved blouse, old flip-flops",
         "a luxurious meditation room in an Indian temple: a Buddha statue, scented candles, lotus flowers, a wooden floor, soft quiet light"),
    34: ("F", 80, "a very old Indian woman of about 80, deeply wrinkled brown skin, thin short white hair, a wrinkled face with a toothless smile; an old faded white kurta, old white cloth trousers, bare feet",
         "a luxurious veranda of a traditional garden house: a wooden rocking chair, greenery, yellow lanterns, a teapot on a small table"),
    35: ("F", 62, "an elderly Indian woman of about 62, wrinkled brown skin, grey hair streaked with black in a neat low bun, a stern face looking into the camera; an old faded red sari with a matching short-sleeved blouse, old flip-flops",
         "a luxurious traditional Indian kitchen: shiny copper pots, spices arranged neatly, a decorative wood stove, warm yellow lights, terracotta walls"),
    36: ("F", 68, "an elderly Indian woman of about 68, wrinkled brown skin, long grey hair worn loose over the shoulders, a pensive face looking into the distance; an old faded grey salwar kameez with a matching dupatta, old flip-flops",
         "a luxurious traditional sewing room: an antique sewing machine, neatly folded fabrics, warm yellow desk lamps, a large window onto a garden"),
    37: ("F", 75, "an elderly Indian woman of about 75, wrinkled brown skin, long white hair in a braid over the shoulder, a tired face with closed eyes; an old faded blue sari with a matching short-sleeved blouse, old flip-flops",
         "a luxurious riverside villa balcony: wicker chairs, greenery, a view of the river, yellow lanterns, warm evening light"),
    38: ("F", 85, "a very old Indian woman of about 85, deeply wrinkled brown skin, thin short white hair, a gentle, kindly smiling face; an old faded cream kurta, old white cloth trousers, old flip-flops",
         "a luxurious family prayer room: a carved wooden altar, yellow oil lamps, fresh flowers, religious paintings, warm yellow light"),
    39: ("F", 63, "an elderly Indian woman of about 63, wrinkled brown skin, grey hair in a neat low bun, old gold earrings, a worried face looking out at the yard; an old faded yellow sari with a matching short-sleeved blouse, old flip-flops",
         "a luxurious family vegetable garden: lush green vegetable beds, a flower trellis, stone benches, soft sunlight, a clean stone path"),
    40: ("F", 70, "an elderly Indian woman of about 70, wrinkled brown skin, short grey hair with a soft wave, a sad face looking down; an old faded purple sari with a matching short-sleeved blouse, old flip-flops",
         "a luxurious family antique showroom: glass cabinets of porcelain, yellow spotlights, an armchair, a thick rug, a window onto a garden"),
}


def giong(g, tuoi):
    if g == "F":
        if tuoi >= 60:
            return (f"a real elderly Marathi woman's voice in her {tuoi // 10 * 10}s: soft, slightly thin and husky, unhurried, native Marathi, a beginner's Indian accent on the English words; a real person, not an actress")
        return (f"a real young Marathi woman's voice in her {'late teens' if tuoi < 20 else 'twenties' if tuoi < 30 else 'thirties'}: natural mid pitch (around 190-230 Hz), plain and a little shy, "
                "native Marathi, a beginner's Indian accent on the English words; a real person, not an actress")
    if tuoi >= 55:
        return (f"a real elderly Marathi man's voice in his {tuoi // 10 * 10}s: warm baritone (around 110-150 Hz), slightly gravelly and unhurried, native Marathi, a beginner's Indian accent on the English words; a real person, not an actor")
    return (f"a real Marathi man's voice in his {'twenties' if tuoi < 30 else 'thirties' if tuoi < 40 else 'forties' if tuoi < 50 else 'fifties'}: mid-low baritone (around 110-140 Hz), plain and a little unsure on the English words, "
            "native Marathi, a beginner's Indian accent; a real person, not an actor")


def doc_csv(path):
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    i = next(k for k, r in enumerate(rows) if r and r[0].strip().startswith("STT"))
    return {int(r[0]): r for r in rows[i + 1:] if r and r[0].strip().isdigit()}


def build(csv_path):
    data = doc_csv(csv_path)
    out = []
    for stt in sorted(ANH):
        g, tuoi, nguoi, nen = ANH[stt]
        r = data[stt]
        link_nv, link_nen = r[4].strip(), r[5].strip()
        v = {"name": f"bien-the-{stt:02d}", **CHUNG, "NGUOI_HOC": nguoi, "GIONG_HOC": giong(g, tuoi), "NEN_HOC": nen}
        v["LUOT"] = [{"who": w, "text": t, "emo": e, "fx": "none"} for w, t, e in luot(g == "F")]
        v["refs"] = {"NGUOI_DAY": [ROBOT], "NGUOI_HOC": [link_nv], "NEN_HOC": [link_nen]}
        out.append(v)
    return out


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else CSV_DEFAULT
    res = build(p)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    n = max(len(l["text"].split()) for l in res[0]["LUOT"])
    print("Đã ghi", os.path.abspath(OUT), f"({len(res)} biến thể, {len(res[0]['LUOT'])} lượt, dài nhất {n} từ)")
