"""Sinh SAMPLE/quet-an-ninh-day-chuyen/BIEN-THE-QUET-AN-NINH-DAY-CHUYEN-40-BIEN-THE.json từ CSV "40 biến thể Sân bay_Quét an ninh".
Chạy:  .venv\\Scripts\\python.exe SAMPLE\\quet-an-ninh-day-chuyen\\cong-cu\\tao_bien_the_40.py [đường dẫn CSV]
- Nền là biến thể gốc (BIEN-THE-QUET-AN-NINH-DAY-CHUYEN.json, hành khách nữ): giữ nhân viên, robot, nền, đạo cụ, refs nhân viên/robot/nền.
- Mỗi biến thể từ CSV: NGUOI_HOC (mô tả tiếng Anh, bảng ANH bên dưới là bản dịch CSV tiếng Việt), GIONG_HOC theo giới/tuổi, refs NGUOI_HOC = link ảnh trong CSV
  (prnt.sc hoặc Google Drive: Studio tự tải về khi tạo dự án), lời thoại đổi "visiting my <người thân>" (lấy từ cột "Kiểu biến thể"), "Ma'am" -> "Sir" với nam,
  "I have/I am <tuổi>" theo tuổi nhân vật.
- Biến thể nam: đại từ hành khách đổi sang he/his/him/himself (các trường SHE, HER, HER_OBJ, HERSELF... do kịch bản dùng token), các trường mô tả cũng đổi he/his.
- Biến thể 16-20 và 31-35: CSV có em bé địu trước ngực; mô tả có ghi (kịch bản gốc không em bé: cần xem Muse dựng thế nào)."""
import copy
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..")
CSV_DEFAULT = r"G:\.shortcut-targets-by-id\18RHYCy9H0VKucU3z-IsYEnXWIepl_N4K\NHIPTY\40 biến thể Sân bay_Quét an ninh - Sheet1.csv"
BASE = os.path.join(D, "BIEN-THE-QUET-AN-NINH-DAY-CHUYEN.json")
OUT = os.path.join(D, "BIEN-THE-QUET-AN-NINH-DAY-CHUYEN-40-BIEN-THE.json")

# STT: (giới, tuổi, mô tả ngoại hình EN)
ANH = {
    1: ("M", 52, "a Mexican man of about 52, medium build with a slight belly, a round face, uneven sun-tanned brown skin with visible pores and a few dark spots, short black hair mixed with grey and a slightly receding hairline, crow's feet and clear smile lines, a plain polo shirt and jeans, clean and tidy, an everyday look"),
    2: ("M", 58, "a Mexican man of about 58, sturdy build with slightly broad shoulders, a square face with clear cheekbones, deep dark-tan skin with natural signs of ageing, thin salt-and-pepper hair on top, a moustache and light stubble, slightly sunken eyes with eye bags and forehead wrinkles, a short-sleeved check shirt and old but clean khaki trousers, a working-class look"),
    3: ("M", 47, "a Mexican man of about 47, a heavy-set build with a gently round belly, a chubby face with a slight double chin, olive-brown skin with small dark marks and uneven texture, slightly curly black hair with a few grey strands, stubble not shaved too close, a natural slightly tired expression, a plain t-shirt and a thin jacket, simple clothes"),
    4: ("M", 55, "a Mexican man of about 55, a thin build with sloping shoulders, a long, slightly hollow face with high cheekbones, sun-tanned brown skin with many small wrinkles and dark under-eyes, short black-and-grey hair thinning at both temples, a neutral expression with the mouth naturally closed, a rolled-sleeve cotton shirt and faded jeans, tidy but plain"),
    5: ("M", 60, "a Mexican man of about 60, a stocky build with a larger belly and a short neck, a wide face with slightly sagging cheeks, dark brown skin with age spots and deep wrinkles around the mouth and eyes, mostly grey thinning hair, a salt-and-pepper moustache, a calm composed expression, a worn but clean polo shirt and dark trousers, an everyday look"),
    6: ("F", 73, "a Mexican woman of about 73, average height, a slim frame with narrow shoulders and thin arms, a naturally slightly stooped back, a long narrow face with high cheekbones, slightly hollow cheeks and a small chin, dark sun-tanned brown skin with age spots and clear wrinkles on the forehead, around the eyes, mouth and neck, slightly sunken eyes with relaxed eyelids and thin lips, almost completely white hair in a short chin-length bob with a side parting, neatly combed, no elaborate make-up, a calm friendly expression without forcing a smile, a cream-white cotton crew-neck t-shirt under a thin navy-blue cardigan worn open, loose dark-blue jeans, plain white sneakers, modern casual clothes, not traditional dress"),
    7: ("F", 62, "a Mexican woman of about 62, short and a little plump with rounded shoulders, a wide face with a slight double chin, sun-tanned brown skin with many small wrinkles on the forehead, around the eyes and on the neck, fairly thick salt-and-pepper hair cut at the nape and naturally wavy, slightly sunken eyes with dark under-eyes, a calm, slightly tired expression, a small-flower print blouse, loose khaki trousers and simple sandals, an ordinary older-woman look"),
    8: ("F", 68, "a Mexican woman of about 68, a thin frame with sloping shoulders and small arms, a long face with high cheekbones, dark brown skin with age spots and clear wrinkles on the forehead, eye corners and around the mouth, thin grey-and-black hair in a low bun at the nape with a few loose strands, thin lips, slightly sunken eyes, a calm, rarely smiling, life-worn expression, a light cotton blouse, loose fabric trousers and old but clean walking shoes"),
    9: ("F", 73, "a Mexican woman of about 73, a small slim frame with a slightly bent back, an oval face with sagging cheeks, olive-brown skin with many deep wrinkles, brown spots and uneven texture, almost entirely grey hair cut short at the ears and thin on top, eye bags, deep nasolabial folds and a clearly wrinkled neck, a natural kind but slightly tired look without a commercial smile, a thin cardigan over a t-shirt, dark long trousers and low-heeled shoes"),
    10: ("F", 50, "a Mexican woman of about 50, an average build, a little full-figured with moderately broad shoulders, a slightly square face with clear cheekbones, uneven sun-tanned brown skin with visible pores, a few dark marks and wrinkles around the eyes, thick black hair with a few grey strands, shoulder-length, tied in a low ponytail, no make-up or only very light make-up, natural lip lines, a friendly but not forced expression, a plain polo shirt, faded blue jeans and simple sports shoes, an everyday look"),
    11: ("F", 21, "a Latina girl of Mexican origin, about 21, about 155 cm tall, short and slightly chubby with rounded shoulders and a soft natural belly, a wide round face with plump cheeks, a short chin, a small slightly upturned nose, round brown eyes and thick straight eyebrows, light brown skin with an olive undertone, a few small pimples and natural pores, jet-black shoulder-length hair cut straight with thick straight bangs, a pastel-pink baby tee, light-blue wide-leg high-waist jeans, white sneakers and a small cream crossbody bag, a cute energetic Gen Z style, a cheerful expression with a wide natural smile showing the teeth"),
    12: ("F", 28, "a Latina woman of Mexican origin, about 28, about 168 cm tall, a full-figured body with wide hips, a moderate waist, balanced shoulders and natural curves, a diamond-shaped face with high cheekbones, a clear jawline and a slightly pointed chin, deep copper-brown skin with natural texture and a few small pigment spots, almond-shaped slightly upturned brown eyes, clearly arched eyebrows, a moderately wide nose and full lips, thick black hair to the waist in big voluminous waves with a deep side parting, a burgundy-red square-neck fitted top, black high-waist jeans of moderate fit, short black leather boots, a black leather belt and medium gold earrings, light make-up with brownish-pink lipstick, a modern glamorous Latina style, a confident expression with a faint smile"),
    13: ("F", 25, "a Latina girl of Mexican origin, about 25, about 172 cm tall, a tall slim build with fairly wide shoulders, a small chest, narrow hips and long arms and legs, a rectangular face with a high forehead, a square jaw and a wide chin, a long slightly humped nose, small deep-set brown eyes and thick straight eyebrows, medium olive-brown skin with light freckles, a few acne marks and natural pores, a short layered black wolf cut, longer at the nape, with messy natural bangs, an oversized plain white t-shirt, loose black multi-pocket cargo trousers, chunky grey-and-white sneakers, a thin silver chain and a black sports watch, no make-up, a tomboy streetwear style, a cold expression with closed lips, hands in the trouser pockets"),
    14: ("F", 35, "a Latina woman of Mexican origin, about 35, about 163 cm tall, a slender, slightly thin build with small shoulders and a long neck, a long oval face with slightly hollow cheeks, a wide forehead and a long chin, a high nose bridge with a slightly hooked tip, light yellowish-brown skin with a few pigment spots, light wrinkles around the eyes and natural smile lines, small brown eyes with slightly drooping lids and thin natural eyebrows, chestnut-brown hair in a straight chin-length bob parted in the middle and neatly combed, a cream silk loose-fitting shirt with one collar button open and sleeves lightly rolled, black high-waist wide-leg trousers, a thin leather belt, black loafers and small gold earrings, a minimalist chic grown-up style, a calm, slightly serious expression, one hand in a trouser pocket"),
    15: ("F", 30, "a Latina girl of Mexican origin, about 30, about 160 cm tall, a sturdy, somewhat heavy build with full upper arms, sloping shoulders and a not-too-small waist, a pear-shaped face with a wide lower jaw, a narrow forehead, slightly asymmetric cheeks and a round chin, dark brown skin with visible pores, a few dark marks and natural pigment spots, deep-set dark brown eyes with heavy lids, a wide nose and a thinner upper lip, very thick natural curly hair cut at the shoulders, dyed copper-brown with the black roots clearly showing, a black tank top under an oversized olive-green linen shirt worn open, charcoal-grey straight jeans, low black leather boots, large round-framed glasses, asymmetric silver earrings, a thin chain and a small tattoo on the forearm, an alternative artistic style, a relaxed, slightly curious expression with a gentle imperfect smile, hands in the trouser pockets"),
    16: ("F", 25, "a Mexican woman of 25, small and a little plump, a round face with full cheeks, olive-brown skin, dark curly hair in a slightly messy high bun, a fitted light-grey cotton t-shirt, dark-blue jeans and white sneakers, a newborn baby carried on her chest in a cream cloth sling with the baby's head and face clearly visible, a modern, simple, tidy look"),
    17: ("F", 32, "a Mexican woman of 32, tall with a strong athletic build and moderately broad shoulders, a square face with a clear jawline, copper-brown skin, long black hair in a high ponytail, a cream-white sports t-shirt, slim black joggers and sports sneakers, a baby of about 4 months carried on her chest in a beige cloth carrier with the baby's head and face clearly visible, a modern energetic sporty style, nothing too elaborate"),
    18: ("F", 28, "a Mexican woman of 28, a full-figured body with wide hips, an oval face with high cheekbones, medium olive-brown skin, natural wavy brown-black shoulder-length hair, a black round-neck t-shirt under an open light-blue denim shirt, wide dark-blue jeans and white sneakers, a newborn baby carried on her chest in a light-grey cloth wrap with the baby's head and face clearly visible, a young streetwear style, tidy"),
    19: ("F", 38, "a Mexican woman of 38, tall and thin with narrow shoulders, a long face with high cheekbones and slightly hollow cheeks, dark brown skin with natural texture, a short black bob cut at the chin with a side parting, a navy-blue cotton round-neck top, straight beige khaki trousers, black loafers, a baby of about 3 months carried on her chest in a white-cream cloth wrap with the baby's head and face clearly visible, a minimalist, elegant, modern style, not too formal"),
    20: ("F", 35, "a Mexican woman of 35, a slightly heavy build with a gently round belly, a wide face with a round chin, honey-brown skin with a few natural pigment spots, chocolate-brown shoulder-length hair with soft waves parted in the middle, a thin knitted dusty-pink sweater, straight black jeans, minimal white sneakers and small gold earrings, a newborn baby carried on her chest in a cream cloth wrap with the baby's head and face clearly visible, a feminine, modern, tidy, comfortable look"),
    21: ("M", 24, "a young Mexican man of about 24, about 170 cm tall, a tall thin build with narrow shoulders and long arms and legs, a long face with a pointed chin and slightly high cheekbones, light brown skin with a few small pimples and natural pores, thick black hair in a short undercut at the sides with the top swept back naturally without shiny gel, no beard, a fresh expression with a natural slight smile, a plain white t-shirt, light-blue straight jeans, white sneakers and a black sports watch, a casual young, tidy, modern style"),
    22: ("M", 28, "a young Mexican man of about 28, about 175 cm tall, a balanced build with moderately broad shoulders, firm arms and a fit look, a slightly square face with a clear jaw, a straight nose and deep brown eyes, copper-brown skin, a short trimmed full beard with a clear line, short black hair in a neat fade, a confident expression with a faint smile, an olive-green linen shirt, beige chinos, a brown leather belt and brown leather loafers, a smart-casual, polite, modern style"),
    23: ("M", 31, "a young Mexican man of about 31, about 168 cm tall, a heavy-set build with broad shoulders, a slightly round belly and a short neck, a round face with full cheeks, a slight double chin and unshaven stubble, dark brown skin with clear pores and a few dark marks, slightly curly short black hair with a few grey strands at the temples, a relaxed, slightly smiling expression with a friendly gaze, a dark-blue denim jacket over a black t-shirt, black jeans and short brown leather boots, a rugged but tidy streetwear style"),
    24: ("M", 22, "a young Mexican man of about 22, about 182 cm tall, a tall thin build with broad-ish shoulders, long arms and legs and a long neck, a long face with a high forehead, a long slightly humped nose, small brown eyes and thick eyebrows, olive-brown skin with light freckles and a few acne marks, a layered black wolf cut, longer at the nape, with messy natural bangs, no beard, a slightly cold expression with closed lips and a direct gaze, a grey hoodie, black joggers and chunky white-and-grey sneakers, a young, edgy streetwear style"),
    25: ("M", 35, "a Mexican man of about 35, about 172 cm tall, an average build with a slight belly and balanced shoulders, an oval face with moderate cheekbones and a round chin, a thin trimmed moustache, uneven sun-tanned brown skin with light wrinkles around the eyes and natural pores, black hair with a few grey strands, short and neat with a straight hairline, a calm expression with a faint smile, a navy-blue polo shirt, beige khaki trousers and minimal white sneakers, a tidy polite everyday style"),
    26: ("M", 68, "an elderly Mexican man of about 68, an average build with slightly sloping shoulders and an upright back, a long face with high cheekbones and a square chin, dark brown skin with many wrinkles on the forehead, around the eyes and at the corners of the mouth and age spots, almost entirely white hair cut short and slightly thin on top, a short trimmed white beard, slightly sunken eyes, a calm, composed expression, a long-sleeved white shirt, grey dress trousers, a black leather belt and black leather shoes, a classic elegant tidy style"),
    27: ("M", 73, "an elderly Mexican man of about 73, a small slightly thin frame with narrow shoulders, a slightly stooped back and thin arms, an oval face with slightly hollow cheeks, a small chin and thin lips, olive-brown skin with deep wrinkles on the forehead and around the mouth and clear brown spots, thin grey-and-black hair cut short at the ears and combed back neatly, no beard, slightly sunken eyes with slightly drooping eyelids, a kind, slightly tired expression without a commercial smile, a thin beige wool cardigan over a cream shirt, straight brown fabric trousers and black walking shoes, a warm, simple classic knit style"),
    28: ("M", 65, "an elderly Mexican man of about 65, a heavy-set build with a larger belly, broad shoulders and a short neck, a wide face with full cheeks, a slight double chin and a thick salt-and-pepper moustache, copper-brown skin with wrinkles around the eyes and clear pores, fairly thick salt-and-pepper hair cut short and slightly curly, a relaxed expression with a faint smile and a friendly gaze, a brown leather jacket over a white t-shirt, dark-blue jeans and brown leather boots, a casual, rugged but tidy style"),
    29: ("M", 78, "an elderly Mexican man of about 78, a short slightly thin frame with a slightly bent back and sloping shoulders, a slow walk, a long narrow face with high cheekbones, hollow cheeks and a pointed chin, dark brown skin with deep wrinkles, clear age spots and a wrinkled neck, thin white hair cut very short, light white stubble, sunken eyes with clear eye bags and a kind but tired gaze, a grey wool vest over a white shirt, loose dark fabric trousers and low black shoes, a simple, warm classic style"),
    30: ("M", 70, "an elderly Mexican man of about 70, medium-tall with a sturdy build, moderately broad shoulders and a slightly round belly, a square face with a clear jaw, high cheekbones and a wide chin, sun-tanned brown skin with light wrinkles around the eyes and on the forehead and small age spots, grey-and-black hair cut short and neat, a short trimmed grey beard, a calm expression with a faint smile, a white guayabera shirt, beige linen trousers and brown leather sandals, a breezy, polite style suited to a warm climate"),
    31: ("M", 30, "a Mexican man of about 30, an average build with balanced shoulders and a fit body, an oval face with moderate cheekbones and a round chin, a short trimmed full beard, copper-brown skin, short black hair in a neat fade with a tidy hairline, a cheerful expression with a faint smile, a fitted light-grey t-shirt, dark-blue jeans and white sneakers, a baby of about 5 months carried on his chest in a grey cloth carrier with the baby's head and face clearly visible, a modern, tidy, comfortable casual-dad style"),
    32: ("M", 35, "a Mexican man of about 35, a tall sturdy build with broad shoulders and full upper arms, a slightly square face with a clear jaw, a straight nose and deep brown eyes, dark brown skin with short light stubble, short neat black hair, a confident expression with a faint smile, a white linen shirt, navy-blue chinos and brown leather loafers, a baby of about 3 months carried on his chest in a beige cloth wrap with the baby's head and face clearly visible, a polite, modern smart-casual style"),
    33: ("M", 28, "a young Mexican man of about 28, a tall thin build with narrow shoulders and long arms and legs, a long face with a high forehead and a pointed chin, small brown eyes and thick eyebrows, olive-brown skin, a layered black wolf cut with messy natural bangs, no beard, a relaxed expression with a faint smile, a black hoodie, grey joggers and white sneakers, a newborn baby carried on his chest in a black cloth carrier with the baby's head and face clearly visible, a youthful, energetic, tidy sporty-dad style"),
    34: ("M", 38, "a Mexican man of about 38, an average build with a slight belly and balanced shoulders, a round face with full cheeks, a slight double chin and a thin moustache, uneven sun-tanned brown skin with light wrinkles around the eyes, black hair with a few grey strands, short and neat, a calm expression with a faint smile, a white polo shirt, brown khaki trousers and minimal white sneakers, a baby of about 6 months carried on his chest in a navy-blue cloth carrier with the baby's head and face clearly visible, a tidy polite everyday style"),
    35: ("M", 32, "a Mexican man of about 32, medium-tall with a firm, fit build and moderately broad shoulders, an oval face with high cheekbones and a slightly square chin, a short beard, copper-brown skin, thick black hair in a short undercut at the sides with the top swept back, a confident expression with a faint smile, a light-blue denim jacket over a white t-shirt, black jeans and short brown leather boots, a baby of about 4 months carried on his chest in a cream cloth wrap with the baby's head and face clearly visible, a streetwear-dad style with personality, tidy"),
    36: ("F", 45, "a Mexican woman of about 45, about 160 cm tall, an average, slightly full-figured build with balanced shoulders and a moderate waist, an oval face with clear cheekbones, a round chin and full lips, olive-brown skin with light wrinkles around the eyes, natural smile lines and a few small pigment spots, shoulder-length black hair with soft waves parted to the side and a few grey strands at the temples, a calm expression with a faint smile, a turquoise silk blouse, straight black trousers, low black heels and small gold earrings, an elegant modern office style"),
    37: ("F", 50, "a Mexican woman of about 50, about 165 cm tall, a tall, full-figured build with wide hips and balanced shoulders, a round face with full cheeks, a slight double chin and big brown eyes, honey-brown skin with light wrinkles on the forehead and around the eyes and small age spots, chocolate-brown shoulder-length hair in big waves parted in the middle, a warm expression with a faint smile, a burgundy-red small-flower midi dress, brown leather heels and a small matching handbag, a feminine, mature, elegant style"),
    38: ("F", 42, "a Mexican woman of about 42, about 158 cm tall, small and slightly plump with rounded shoulders and a soft natural belly, a wide round face with plump cheeks, a short chin and round brown eyes, light brown skin with an olive undertone, a few small pimples and natural pores, jet-black hair in a short chin-length bob with straight bangs, a cheerful expression with a wide natural smile, a thin knitted dusty-pink sweater, a long brown skirt, flat leather shoes and small gold earrings, a feminine, warm, tidy knit style"),
    39: ("F", 55, "a Mexican woman of about 55, about 163 cm tall, an average build with moderately broad shoulders and a slightly heavy figure, a slightly square face with a clear jaw, high cheekbones and a wide chin, dark brown skin with clear wrinkles on the forehead, around the eyes and at the corners of the mouth and age spots, thick salt-and-pepper hair in a neat low bun at the nape with a few loose strands, a calm, slightly stern expression without a commercial smile, a grey tailored suit (blazer and pencil skirt of the same set) over a white blouse, low black heels, a mature, elegant business style"),
    40: ("F", 48, "a Mexican woman of about 48, about 167 cm tall, a tall thin build with narrow shoulders and long arms and legs, a long oval face with slightly hollow cheeks, a long chin and a high nose bridge, light yellowish-brown skin with light wrinkles around the eyes and a few pigment spots, chestnut-brown hair to the waist, naturally straight, parted in the middle, a calm expression with a faint smile, a white shirt, straight dark-blue jeans, white sneakers and a cream canvas tote bag, an elegant modern casual-chic style"),
}


def doc_csv(path):
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    out = {}
    for r in rows:
        m = re.match(r"Biến thể\s+(\d+)\s*$", (r[0] if r else "").strip())
        if m and len(r) >= 4:
            out[int(m.group(1))] = r
    return out


def nguoi_than(kieu):
    """Lấy người thân mới từ cột 'Kiểu biến thể': thành "I'm visiting my X" (nháy thứ hai)."""
    m = re.search(r'thành\s+["“”]+I.m visiting my (\w+)', kieu)
    if not m:
        raise ValueError("không đọc được người thân: " + kieu[:80])
    return m.group(1).lower()


def giong(g, tuoi):
    if g == "F":
        if tuoi >= 60:
            return (f"a real elderly Mexican woman's voice in her {tuoi // 10 * 10}s speaking English as a second language: soft, slightly thin and husky, unhurried, a natural Mexican accent with Spanish vowels and soft r, "
                    "not exaggerated; warm, with a smile in the voice and quietly proud when she talks about her tutor; a real person, not an actress")
        dec = "early twenties" if tuoi < 25 else "late twenties" if tuoi < 30 else "thirties" if tuoi < 40 else "forties" if tuoi < 50 else "fifties"
        return (f"a real Mexican woman in her {dec} speaking English as a second language, mid-pitched (around 200-230 Hz), a natural Mexican accent with Spanish vowels and soft r, "
                "not exaggerated; quick and a little breathless when nervous, warm, with a smile in the voice and quietly proud when she talks about her tutor; a real person, not an actress")
    if tuoi >= 60:
        return (f"a real elderly Mexican man's voice in his {tuoi // 10 * 10}s speaking English as a second language: warm, slightly gravelly baritone (around 110-140 Hz), unhurried, a natural Mexican accent with Spanish vowels and soft r, "
                "not exaggerated; a smile in the voice and quietly proud when he talks about his tutor; a real person, not an actor")
    dec = "twenties" if tuoi < 30 else "thirties" if tuoi < 40 else "forties" if tuoi < 50 else "fifties"
    return (f"a real Mexican man in his {dec} speaking English as a second language, mid-low baritone (around 110-140 Hz), a natural Mexican accent with Spanish vowels and soft r, "
            "not exaggerated; a little quick and breathless when nervous, warm, with a smile in the voice and quietly proud when he talks about his tutor; a real person, not an actor")


def sang_nam(s):
    """Đổi đại từ nữ -> nam trong một chuỗi mô tả (đại từ tân ngữ khi 'her' đứng trước dấu câu)."""
    s = re.sub(r"\bherself\b", "himself", s)
    s = re.sub(r"\bShe\b", "He", s)
    s = re.sub(r"\bshe\b", "he", s)
    s = re.sub(r"\bHer\b", "His", s)
    s = re.sub(r"\bher\b(?=\s*[,;:.)]|\s*$)", "him", s)
    return re.sub(r"\bher\b", "his", s)


NAM = {"SHE": "he", "SHE_CAP": "He", "HER": "his", "HER_CAP": "His", "HER_OBJ": "him", "HERSELF": "himself"}
NU = {"SHE": "she", "SHE_CAP": "She", "HER": "her", "HER_CAP": "Her", "HER_OBJ": "her", "HERSELF": "herself"}


def build(csv_path):
    base = json.load(open(BASE, encoding="utf-8"))[0]
    data = doc_csv(csv_path)
    assert sorted(data) == list(range(1, 41)), sorted(data)
    out = []
    for stt in range(1, 41):
        g, tuoi, mo_ta = ANH[stt]
        r = data[stt]
        rel = nguoi_than(r[1])
        link = r[3].strip()
        v = copy.deepcopy(base)
        v["name"] = f"bien-the-{stt:02d}"
        if g == "M":   # đại từ nam trong mọi trường mô tả của biến thể gốc
            for k, val in list(v.items()):
                if isinstance(val, str) and k not in ("name", "NGUOI_HOC", "GIONG_HOC") and k not in NU:
                    v[k] = sang_nam(val)
        v.update(NAM if g == "M" else NU)
        v["VAI_HOC"] = "passenger"
        v["NGUOI_HOC"] = mo_ta
        v["GIONG_HOC"] = giong(g, tuoi)
        v["refs"] = dict(base["refs"])
        v["refs"]["NGUOI_HOC"] = [{"url": link, "name": f"nguoi-hoc-{stt:02d}"}]
        luot = copy.deepcopy(base["LUOT"])
        for i, l in enumerate(luot):
            t = l["text"]
            if i == 0 and g == "M":
                t = t.replace("Ma'am", "Sir")
            t = t.replace("visiting my daughter", f"visiting my {rel}").replace("I have 48", f"I have {tuoi}").replace("I am 48", f"I am {tuoi}")
            l["text"] = t
        v["LUOT"] = luot
        out.append(v)
    return out


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else CSV_DEFAULT
    res = build(p)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Da ghi", os.path.abspath(OUT), f"({len(res)} bien the, {len(res[0]['LUOT'])} luot)")
