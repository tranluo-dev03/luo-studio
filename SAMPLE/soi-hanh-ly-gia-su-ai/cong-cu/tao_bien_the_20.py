"""Sinh 2 file biến thể cho bộ "20 biến thể Sân bay_Check luggage" (05/11/2026), cùng lời thoại và nhân viên/robot của biến thể mẫu,
chỉ đổi hành khách (HOC) + giọng:
  - BIEN-THE-SOI-HANH-LY-20-KHONG-BE.json (biến thể 1-15, hành khách không địu con) -> dùng với KICH-BAN-SOI-HANH-LY-GIA-SU-AI-KHONG-BE.txt
  - BIEN-THE-SOI-HANH-LY-20-DIU-CON.json  (biến thể 16-20, người mẹ địu con)        -> dùng với KICH-BAN-SOI-HANH-LY-GIA-SU-AI.txt
Ảnh tham chiếu: NGUOI_HOC = link ảnh của từng biến thể trong bảng (Studio tự tải trang prnt.sc), NGUOI_DAY = ROBOT-GIA-SU-AI.png.
Câu tuổi phần 2 ("I have N" / "I am N") theo tuổi hành khách; câu "visiting my ..." hợp tuổi.
Chạy: runtime\\python.exe SAMPLE\\soi-hanh-ly-gia-su-ai\\cong-cu\\tao_bien_the_20.py"""
import copy
import json
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MAU = json.load(open(os.path.join(D, "BIEN-THE-SOI-HANH-LY-GIA-SU-AI.json"), encoding="utf-8"))[0]
ROBOT = {"url": "file:///" + os.path.abspath(os.path.join(D, "ROBOT-GIA-SU-AI.png")).replace("\\", "/"), "name": "ROBOT-GIA-SU-AI.png"}
CHUNG = ["TEN_CANBO", "NGUOI_CANBO", "GIONG_CANBO", "VAI_CANBO", "POS_CANBO", "NGHE_CANBO", "DAO_VALI", "DAO_VALI_2", "DAO_DIEN_THOAI",
         "NEN_SOI", "NEN_HOC", "TEN_DAY", "NGUOI_DAY", "NEN_DAY", "NHIN_DAY"]
GIONG_DAY = ("a bright, light, friendly young woman's voice, clearly lighter than the traveller's, smooth and clear with only a faint synthetic polish, "
             "patient and encouraging like a kind language teacher on a video call, neutral American accent")
ACCENT = "a natural Mexican accent with Spanish vowels and a soft r, not exaggerated"
REAL = "a real person, not an actor"

# (số, giới m/f, tuổi, tên ngắn, link ảnh, ngoại hình EN, túi, giọng EN, ai ở Mỹ, em bé EN hoặc None)
P = [
    (1, "m", 52, "polo", "https://prnt.sc/v9ZGXXiglwbd",
     "a Mexican man of about 52, medium build with a slight belly, a round face, unevenly sun-tanned brown skin, short black hair streaked with grey and a slightly receding hairline, crow's feet and clear smile lines, visible pores and a few dark spots, a plain polo shirt and jeans, clean, neat everyday style",
     "a dark-grey canvas shoulder bag",
     "a warm, steady Mexican man's voice in his early fifties, low-mid pitch (around 110-130 Hz), slightly husky, friendly and unhurried", "daughter", None),
    (2, "m", 58, "caro", "https://prnt.sc/OGLg28JuAOvD",
     "a Mexican man of about 58, a solid build with fairly broad shoulders, a square face with clear cheekbones, deep tan skin with natural signs of ageing, salt-and-pepper hair thinning slightly on top, a moustache and light stubble, slightly deep-set eyes with bags under them and forehead wrinkles, a short-sleeved checked shirt and old but clean khaki trousers, a modest everyday look",
     "a worn brown canvas shoulder bag",
     "a deep, slightly gravelly Mexican man's voice in his late fifties, low pitch (around 100-120 Hz), calm and plain-spoken", "daughter", None),
    (3, "m", 47, "ao-khoac", "https://prnt.sc/MUrHKt3FBhXA",
     "a Mexican man of about 47, a slightly heavy build with a round belly, a chubby face with a slight double chin, olive-brown skin with small dark marks and uneven texture, slightly curly black hair with a few grey strands, not too closely shaved stubble, a natural, slightly tired look, a plain T-shirt under a light jacket, simple casual clothes",
     "a black nylon shoulder bag",
     "a friendly, slightly nasal Mexican man's voice in his late forties, mid-low pitch (around 115-135 Hz), relaxed, a little tired", "daughter", None),
    (4, "m", 55, "so-mi", "https://prnt.sc/LD74D9P5fHeG",
     "a Mexican man of about 55, a thin build with slightly sloping shoulders, a long, slightly gaunt face with high cheekbones, sun-tanned brown skin with many fine wrinkles and darker skin under the eyes, short black-and-grey hair thinning a little at both temples, a cotton shirt with rolled-up sleeves and faded jeans, neat but plain",
     "a tan canvas shoulder bag",
     "a soft-spoken, slightly raspy Mexican man's voice in his mid fifties, mid-low pitch (around 110-130 Hz), modest and polite", "daughter", None),
    (5, "m", 60, "polo-cu", "https://prnt.sc/thpld3uXXFEg",
     "a Mexican man of about 60, a heavy build with a fairly big belly and a short neck, a wide face with slightly sagging cheeks, dark brown skin with age spots and deep wrinkles around the mouth and eyes, mostly grey hair thinning on top, a salt-and-pepper moustache, a calm composed face, a well-worn but clean polo shirt and dark trousers, everyday style",
     "a black leather shoulder bag",
     "a deep, calm, unhurried Mexican man's voice around sixty, low pitch (around 95-115 Hz), a little breathy, gentle", "daughter", None),
    (6, "f", 73, "cardigan-navy", "https://prnt.sc/h8gufAS-bDq2",
     "a Mexican woman of about 73, of average height and slightly thin, narrow shoulders, small arms and a slight natural stoop, a long narrow face with high cheekbones, slightly hollow cheeks and a small chin, dark sun-tanned brown skin with age spots and clear wrinkles on the forehead, around the eyes, mouth and neck, slightly deep-set eyes with drooping lids, thin lips, almost completely white hair in a short chin-length bob with a side parting, neatly combed, no heavy make-up, a cream-white round-neck cotton T-shirt under a slim navy-blue cardigan worn open, straight-cut dark-blue jeans and minimal white sneakers, modern, tidy and comfortable, not traditional and not formal",
     "a small brown leather shoulder bag",
     "a soft, slightly thin and wavering Mexican grandmother's voice in her seventies, mid pitch (around 180-210 Hz), gentle and kind", "daughter", None),
    (7, "f", 62, "so-mi-hoa", "https://prnt.sc/My4vuU4jNcaY",
     "a Mexican woman of about 62, short and slightly plump, rounded shoulders, a wide face with a slight double chin, sun-tanned brown skin with many fine wrinkles on the forehead, around the eyes and on the neck, fairly thick salt-and-pepper hair cut at the nape, naturally a little wavy and not styled, slightly deep-set eyes with darker skin under them, a calm, slightly tired face, a small-flower-print shirt, loose khaki trousers and simple sandals, a modest older woman's style",
     "a faded red cloth shoulder bag",
     "a warm, slightly husky Mexican woman's voice in her early sixties, mid-low pitch (around 170-200 Hz), motherly and easygoing", "daughter", None),
    (8, "f", 68, "bui-toc", "https://prnt.sc/chA176Je6xMF",
     "a Mexican woman of about 68, thin with slightly sloping shoulders and small arms, a long face with high cheekbones, dark brown skin with age spots and clear wrinkles on the forehead, at the corners of the eyes and around the mouth, thin grey-and-black hair in a low bun at the nape with a few loose wisps, thin lips, slightly deep-set eyes, a calm, experienced face, a light-coloured cotton blouse, loose cloth trousers and old but clean walking shoes",
     "a dark-green cloth shoulder bag",
     "a calm, low, slightly dry Mexican woman's voice in her late sixties, mid-low pitch (around 165-195 Hz), measured and composed", "daughter", None),
    (9, "f", 73, "toc-ngan", "https://prnt.sc/9tOFRf4zboZW",
     "a Mexican woman of about 73, small and slightly thin with a gentle stoop, an oval face with sagging cheeks, olive-brown skin with many deep wrinkles, brown spots and uneven texture, mostly grey hair cut short at the ears and a little thin on top, bags under the eyes, deep smile lines, clear wrinkles on the neck, a kind but slightly tired look, a thin cardigan over a T-shirt, dark trousers and low flat shoes",
     "a small black leather shoulder bag",
     "a gentle, slightly shaky Mexican grandmother's voice in her seventies, mid pitch (around 175-205 Hz), soft and sweet", "daughter", None),
    (10, "f", 50, "duoi-ngua", "https://prnt.sc/b1jhfypLu7fQ",
     "a Mexican woman of about 50, medium and slightly full build, moderately broad shoulders, a slightly square face with clear cheekbones, unevenly sun-tanned brown skin with visible pores, a few dark marks and wrinkles around the eyes, thick black hair with a few grey strands, past the shoulders, tied in a low ponytail, no or very light make-up, natural lines on the lips, a plain polo shirt, faded blue jeans and simple sneakers, everyday style",
     "a brown faux-leather shoulder bag",
     "a clear, friendly Mexican woman's voice around fifty, mid pitch (around 190-220 Hz), practical and warm", "daughter", None),
    (11, "f", 21, "gen-z", "https://prnt.sc/OeaMTbXOZbn1",
     "a young Mexican Latina woman of about 21, about 155 cm, short and slightly chubby, rounded shoulders, a round wide face with full cheeks, a short chin, a small slightly upturned nose, round brown eyes and thick straight eyebrows, light olive-brown skin with a few small spots and natural pores, jet-black shoulder-length hair cut straight with thick bangs, a fitted pastel-pink baby tee, light-blue high-waisted wide-leg jeans and white sneakers, a cute, lively Gen Z style",
     "a small cream crossbody bag",
     "a bright, bubbly young Mexican woman's voice of about 21, high pitch (around 220-260 Hz), quick and cheerful, a little giggly", "cousin", None),
    (12, "f", 28, "burgundy", "https://prnt.sc/nuRL7PGR89bQ",
     "a Mexican Latina woman of about 28, about 168 cm, a full curvy figure with wide hips, a diamond-shaped face with high cheekbones, a clear jawline and a slightly pointed chin, deep bronze-brown skin with natural texture and a few small pigment spots, almond-shaped brown eyes, clearly arched eyebrows, full lips, thick black hair down to the middle of the back in big loose waves with a deep side parting, a fitted square-neck burgundy top, black high-waisted jeans, short black leather boots, a black leather belt and medium gold earrings, light make-up with brown-pink lipstick, a modern, confident Latina style",
     "a black leather shoulder bag",
     "a smooth, warm, slightly low Mexican woman's voice of about 28, mid pitch (around 185-215 Hz), confident and easy", "sister", None),
    (13, "f", 25, "tomboy", "https://prnt.sc/WSc4cnNLpU77",
     "a Mexican Latina woman of about 25, about 172 cm, tall and lean, fairly broad straight shoulders, long arms and legs, a rectangular face with a high forehead, a square jaw and a wide chin, a long, slightly arched nose, small deep-set brown eyes and thick straight eyebrows, medium olive-brown skin with light freckles, a few acne marks and natural pores, a short layered black wolf cut, longer at the nape, with messy bangs, an oversized plain white T-shirt, loose black cargo trousers, chunky grey-white sneakers, a thin silver chain and a black sports watch, no make-up, a strong tomboy streetwear style",
     "a black canvas sling bag",
     "a low, cool, slightly husky young Mexican woman's voice of about 25, mid-low pitch (around 170-200 Hz), relaxed and laid-back", "brother", None),
    (14, "f", 35, "minimal", "https://prnt.sc/JBWy5J26DNyH",
     "a Mexican Latina woman of about 35, about 163 cm, slender and slightly thin, small shoulders and a long neck, a long oval face with slightly hollow cheeks, a wide forehead, a long chin and a high nose with a slightly hooked tip, light golden-brown skin with a few pigment spots, faint wrinkles around the eyes and natural smile lines, small brown eyes with slightly hooded lids and thin natural eyebrows, straight chestnut-brown hair in a chin-length bob with a centre parting, neatly combed, a loose cream silk shirt with the top button open and sleeves slightly rolled, black high-waisted wide-leg trousers, a thin leather belt, black loafers and small gold earrings, a minimalist, elegant style",
     "a structured black leather shoulder bag",
     "a calm, precise, mid-pitched Mexican woman's voice of about 35 (around 190-220 Hz), composed and a little serious", "sister", None),
    (15, "f", 30, "artistic", "https://prnt.sc/jrxSnyOoTSWB",
     "a Mexican Latina woman of about 30, about 160 cm, sturdy and slightly heavy-set, full arms, sloping shoulders and a not-too-small waist, a pear-shaped face with a wide lower jaw, a narrow forehead, slightly asymmetric cheeks and a round chin, dark brown skin with visible pores, a few dark marks and natural pigment spots, slightly deep-set dark-brown eyes with heavy lids, a wide nose, an upper lip thinner than the lower lip, very thick naturally curly shoulder-length hair dyed copper-brown with clearly visible black roots, a black tank top under an open oversized olive-green linen shirt, straight charcoal-grey jeans, low black leather boots, big round glasses, asymmetric silver earrings, a thin necklace and a small tattoo on the forearm, an artistic alternative style",
     "a mustard-yellow canvas tote bag",
     "a lively, slightly raspy Mexican woman's voice of about 30, mid pitch (around 185-215 Hz), curious and playful", "best friend", None),
    (16, "f", 25, "me-25", "https://prnt.sc/mjXN_l72nvrg",
     "a Mexican woman of 25, petite and slightly chubby, a round face with full cheeks, olive-brown skin, slightly curly black hair in a high, slightly messy bun, a fitted light-grey cotton T-shirt, dark-blue jeans and white sneakers, a modern, simple, tidy look",
     "a large beige canvas tote bag",
     "a sweet, slightly high young Mexican mother's voice of 25, mid-high pitch (around 210-240 Hz), soft and a little shy", "husband's family",
     "a sleeping newborn baby with a little dark hair, snug in a cream-coloured fabric wrap carrier tied over her chest, the baby's head and face clearly visible resting on her chest, eyes closed"),
    (17, "f", 32, "me-sporty", "https://prnt.sc/eyFM17SqwtO0",
     "a Mexican woman of 32, tall with a fit, athletic build and moderately broad shoulders, a square face with a clear jawline, bronze-brown skin, long black hair in a high ponytail, a cream-white sports T-shirt, slim black joggers and sporty sneakers, a modern, active sporty style",
     "a black sports backpack worn on one shoulder",
     "a clear, energetic Mexican woman's voice of 32, mid pitch (around 195-225 Hz), brisk and upbeat", "husband's family",
     "a sleeping baby of about four months with soft dark hair, snug in a beige fabric carrier on her chest, the baby's head and face clearly visible, eyes closed"),
    (18, "f", 28, "me-denim", "https://prnt.sc/USuKeyXx2L04",
     "a Mexican woman of 28, a full figure with wide hips, an oval face with high cheekbones, medium olive-brown skin, naturally curly dark-brown shoulder-length hair, a black round-neck T-shirt under an open light-blue denim shirt, dark-blue wide-leg jeans and white sneakers, a youthful streetwear style",
     "a large black canvas tote bag",
     "a warm, slightly husky young Mexican mother's voice of 28, mid pitch (around 190-220 Hz), relaxed and chatty", "husband's family",
     "a sleeping newborn baby with a little dark hair, snug in a light-grey fabric wrap carrier tied over her chest, the baby's head and face clearly visible, eyes closed"),
    (19, "f", 38, "me-bob", "https://prnt.sc/yufneN1ZjAFJ",
     "a Mexican woman of 38, tall and slim with narrow shoulders, a long face with high cheekbones and slightly hollow cheeks, dark brown skin with natural texture, a short black chin-length bob with a side parting, a navy-blue round-neck cotton top, straight beige khaki trousers and black loafers, a minimalist, elegant look",
     "a structured tan leather tote bag",
     "a calm, low, mature Mexican woman's voice of 38, mid-low pitch (around 175-205 Hz), steady and kind", "husband's family",
     "a sleeping baby of about three months with soft dark hair, snug in a creamy-white fabric wrap carrier on her chest, the baby's head and face clearly visible, eyes closed"),
    (20, "f", 35, "me-len-hong", "https://prnt.sc/JA0fVQ_QjSbo",
     "a Mexican woman of 35, slightly heavy with a gently rounded belly, a wide face and a round chin, honey-brown skin with a few natural pigment spots, chocolate-brown hair past the shoulders in soft waves with a centre parting, a thin knitted sweater in dusty pink, straight black jeans, minimal white sneakers and small gold earrings, a feminine, modern, tidy style",
     "a large camel-brown leather tote bag",
     "a gentle, melodic Mexican woman's voice of 35, mid pitch (around 195-225 Hz), warm and smiling", "husband's family",
     "a sleeping newborn baby with a little dark hair, snug in a cream-coloured fabric wrap carrier tied over her chest, the baby's head and face clearly visible, eyes closed"),
]

PRON = {"m": {"HE_HOC": "he", "HE_HOC_C": "He", "HIS_HOC": "his", "HIM_HOC": "him", "HIMSELF_HOC": "himself"},
        "f": {"HE_HOC": "she", "HE_HOC_C": "She", "HIS_HOC": "her", "HIM_HOC": "her", "HIMSELF_HOC": "herself"}}


def variant(n, g, age, short, link, look, bag, voice, who, baby):
    v = {"name": f"soi-hanh-ly-bien-the-{n:02d}-{'nam' if g == 'm' else 'nu'}-{age}-{short}"}
    his = "his" if g == "m" else "her"
    if baby:   # bản có em bé: giữ đúng cách viết của biến thể mẫu (người mẹ)
        v.update({"TEN_HOC": "the mother", "VAI_HOC": "mother"})
    else:
        v.update({"TEN_HOC": "the traveller", "VAI_HOC": "traveller"})
    v["NGUOI_HOC"] = look
    v["GIONG_HOC"] = (f"{voice}; a real Mexican {'man' if g == 'm' else 'woman'} speaking English as a second language, {ACCENT}; quick and a little nervous at the "
                      f"checkpoint, warming up and quietly proud when talking about the tutor; {REAL}")
    v["POS_HOC"] = "RIGHT"
    for k in CHUNG:
        v[k] = copy.deepcopy(MAU[k])
    v["POS_CANBO"], v["GIONG_DAY"] = MAU["POS_CANBO"], GIONG_DAY if not baby else MAU["GIONG_DAY"]
    if baby:
        v["NGHE_HOC"] = MAU["NGHE_HOC"]
        v["DAO_BE"] = baby
        v["DAO_GIU"], v["DAO_NGHI"] = MAU["DAO_GIU"], MAU["DAO_NGHI"]
        v["NHIN_CANBO"], v["NHIN_HOC"], v["NHIN_HOC@2"] = MAU["NHIN_CANBO"], MAU["NHIN_HOC"], MAU["NHIN_HOC@2"]
    else:
        v["NGHE_HOC"] = (f"stands with one hand resting on the strap of {his} bag, mouth closed; {his} eyes follow whatever the officer points at (the suitcase) and "
                         "come back to the officer's face, with a natural, slightly worried or smiling face that matches the moment")
        v["DAO_GIU"] = (f"{his.capitalize()} free hand rests on the strap of {his} bag or does the clip's action only: no hand ever goes to the head, face or hair.")
        v["DAO_NGHI"] = "the traveller standing with one hand resting on the bag strap, the officer standing still behind the conveyor"
        v["NHIN_CANBO"] = ("keeps his head turned toward the traveller in three-quarter profile, looking at the traveller's face (or at the suitcase or phone the clip "
                           "names); his face never turns to the camera or out of the frame")
        v["NHIN_HOC"] = "looks at the officer's face, eyes level, never into the lens (except when the clip's action is to look at the suitcase or the phone)"
        v["NHIN_HOC@2"] = f"looks straight into the lens, as if talking to the AI tutor on the phone {'he is' if g == 'm' else 'she is'} holding"
        v.update(PRON[g])
    v["DAO_TUI"] = bag
    luot = copy.deepcopy(MAU["LUOT"])
    for t in luot:
        t["text"] = (t["text"].replace("visiting my daughter", f"visiting my {who}")
                     .replace("I have 48", f"I have {age}").replace("I am 48", f"I am {age}"))
    v["LUOT"] = luot
    v["refs"] = {"NGUOI_HOC": [link], "NGUOI_DAY": [ROBOT]}
    return v


ra = {"KHONG-BE": [], "DIU-CON": []}
for p in P:
    ra["DIU-CON" if p[-1] else "KHONG-BE"].append(variant(*p))
for k, vs in ra.items():
    f = os.path.join(D, f"BIEN-THE-SOI-HANH-LY-20-{k}.json")
    json.dump(vs, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f, len(vs))
