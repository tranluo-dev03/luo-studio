"""Sinh SAMPLE/du-lich-chia-doi-gia-su-ai/BIEN-THE-DU-LICH-CHIA-DOI-GIA-SU-AI.json.
Sửa bảng BIEN_THE (nhân vật, giọng, ảnh, tên, tuổi, quê) hoặc hàm luot() rồi chạy:
    .venv\\Scripts\\python.exe SAMPLE\\du-lich-chia-doi-gia-su-ai\\cong-cu\\tao_bien_the.py
Biến thể 01 bám sát video mẫu (2310_face to face ES_005_2): lời giữ nguyên văn theo phụ đề trên hình (Whisper nghe nhầm "úselo", "una nativo",
"mejorarse/su inglés", "¿Ticiste a decir?"; phụ đề ghi "úsalo", "un nativo", "mejorar tu inglés", "¿Quisiste decir?").
Ảnh tham chiếu: CHỈ dùng ảnh AI do người dùng cung cấp (link hoặc tệp trong anh/), KHÔNG cắt ảnh từ video mẫu (người dùng chốt 05/11/2026).
Ảnh chưa có thì bỏ khỏi refs và in cảnh báo; đường dẫn tệp tính từ thư mục gốc."""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-DU-LICH-CHIA-DOI-GIA-SU-AI.json")
ANH = "SAMPLE/du-lich-chia-doi-gia-su-ai/anh/"
# Ảnh AI do người dùng cung cấp (thay bằng link Drive/prnt.sc hoặc tên tệp đặt trong anh/)
ANH_ROBOT = ANH + "ai-robot.png"   # MỘT robot cho cả hai phần (người dùng chốt 05/11/2026): robot trắng, không tai nghe
ANH_ROBOT_PHAN1 = ANH_ROBOT
ANH_ROBOT_PHAN2 = ANH_ROBOT

# Mô tả robot theo ảnh AI của người dùng; dùng chung NGUOI_ROBOT (phần 1) và NGUOI_DAY (phần 2)
ROBOT = ("a sleek feminine humanoid robot: a smooth matte-white porcelain face with calm light-blue eyes, soft flexible porcelain lips that "
         "open and move naturally with every word whenever the robot itself speaks, and a few thin "
         "panel lines, a bald white helmet-like head with small dark ear modules, a black mechanical neck of bundled cables, glossy white hexagonal "
         "armour plates on the chest, shoulders and arms with thin glowing cyan seams over black mechanical joints, slim black mechanical hands")

GIONG_AI = ("a warm, friendly young woman's voice with a light smooth synthetic sheen, around 170–210 Hz, natural Mexican Spanish accent, clear and "
            "patient, like a kind language tutor; speaks English words with a clean neutral American accent")

CHUNG = {
    # Phần 1: robot ở Machu Picchu
    "TEN_ROBOT": "the robot",
    "VAI_ROBOT": "AI robot guide",
    "POS_ROBOT": "LEFT",
    "NGUOI_ROBOT": ROBOT,
    "GIONG_ROBOT": GIONG_AI,
    # Phần 2: cùng robot, gọi video (nền tối như video mẫu)
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": ROBOT,
    "GIONG_DAY": GIONG_AI,
    "NEN_DAY": "a dark navy-to-deep-purple gradient backdrop with a faint glowing thin arc line and a few tiny soft light specks, like a calm digital space",
    "NEN_HOC": "a cosy living room in warm evening lamplight: a beige sofa with orange and grey cushions, a wooden bookshelf with books and a potted plant "
               "behind the left shoulder, a lit table lamp and a framed picture on a cream wall behind the right shoulder, softly out of focus",
    "DAO_COC": "The right hand holds a cream speckled ceramic coffee mug at chest height, just left of centre and inside the middle half of the "
               "width; the left hand rests on the knee; the mug stays in the same hand in every clip.",
}

# (tên, TEN_HOC, ngoại hình EN, giọng EN, ảnh, tuổi nói trong câu, quê)
BIEN_THE = [
    ("bien-the-01-carla-goc",
     "Carla",
     "a Mexican woman in her late thirties, an oval face with high cheekbones, warm brown eyes, natural full eyebrows and a friendly smile, medium tan skin, "
     "shoulder-length dark brown curly hair with a side part; a loose mustard-yellow long coat over a cream button-up blouse, brown trousers, a thin silver ring",
     "a real Mexican woman in her late thirties, natural mid-high pitch around 180–220 Hz, slightly husky and warm, native Mexican Spanish; speaks English "
     "as a beginner with a strong Mexican accent, Spanish vowels and a soft r; a real person, not an actress",
     ANH + "ai-carla.png", "22", "Mexico"),
]


def luot(ten, tuoi, que):
    """12 lượt như video mẫu: 3 lượt phần 1 (Machu Picchu), 9 lượt phần 2 (gọi video).
    Câu sai: chữ đỏ + ❌ + viền đỏ ("fx": "wrong"); câu nói lại đúng: ✅ + viền xanh ("fx": "right"); cụm tiếng Anh đúng trong lời AI tô xanh ("to")."""
    ok1, ok2 = f"I'm {tuoi}", f"I'm from {que}"
    L = [
        ("hoc", 1, "¿Cuál es la primera regla para aprender inglés?", "curious, delighted"),
        ("robot", 1, "No lo estudies, úsalo. Solo necesitas hablar con un nativo.", "calm, warm"),
        ("hoc", 1, "¿Cómo?", "confused, surprised"),
        ("day", 2, "How old are you?", "friendly, curious"),
        ("hoc", 2, f"Eh, I have {tuoi}.", "unsure", {"c": "red", "fx": "wrong", "icon": "x"}),
        ("day", 2, f"¿Quisiste decir, {ok1}?", "patient, encouraging", {"to": ok1, "to_mau": "green"}),
        ("hoc", 2, f"Ah, sí, es verdad. {ok1}.", "relieved, confident", {"fx": "right", "icon": "check", "to": ok1, "to_mau": "green"}),
        ("day", 2, f"{ten}, where are you from?", "friendly, curious"),
        ("hoc", 2, f"I'm {que}.", "unsure", {"c": "red", "fx": "wrong", "icon": "x"}),
        ("day", 2, f"{ten}, buen intento, pero tienes que decir, {ok2}.", "patient, encouraging", {"to": ok2, "to_mau": "green"}),
        ("hoc", 2, f"Perdón, siempre me equivoco. {ok2}.", "embarrassed, confident", {"fx": "right", "icon": "check", "to": ok2, "to_mau": "green"}),
        ("day", 2, "No pasa nada, vamos a mejorar tu inglés hablando todos los días juntos.", "warm, reassuring"),
    ]
    out = []
    for who, phan, text, emo, *extra in L:
        t = {"who": who, "text": text, "emo": emo, "fx": "none", "phan": phan}
        t.update(extra[0] if extra else {})
        out.append(t)
    return out


ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))


def _refs(m, name):
    """Giữ link (http...) và tệp có thật; tệp chưa có thì bỏ và cảnh báo (chưa nhận ảnh AI của người dùng)."""
    out = {}
    for k, x in m.items():
        if not x:
            continue
        if x.startswith("http") or os.path.isfile(os.path.join(ROOT, x)):
            out[k] = [x]
        else:
            print(f"CẢNH BÁO [{name}] {k}: chưa có ảnh {x} (chờ ảnh AI của người dùng), bỏ khỏi refs")
    return out


# ---------------------------------------------------------------- điểm du lịch phần 1
# NEN_ROBOT = nền phần 1 (đuôi _ROBOT: Studio bỏ token + ảnh nền ở phần 2 vì phần 2 không có ROBOT; tên NEN_CANH sẽ bị gửi cả sang phòng khách).
# ANH_SANG = câu ánh sáng mở đầu STYLE LOCK; DIEM_NHIN = thứ người học ngắm ở giữa khung. "anh": ảnh nền (link Drive người dùng gửi) hoặc None.
NOI = {
    "machu": {"NEN_ROBOT": "the Machu Picchu citadel at golden hour: the steep green Huayna Picchu peak in the centre, grey stone terraces and Inca ruins "
                           "below, soft white mist in the valley, distant mountain ridges, a dramatic orange-and-grey cloudy sky",
              "ANH_SANG": "Golden-hour light at Machu Picchu: warm low sun from the right, dramatic orange-and-grey clouds in the sky",
              "DIEM_NHIN": "the peak", "anh": None},
    "chichen": {"NEN_ROBOT": "the great stepped pyramid of El Castillo at Chichén Itzá: a tall grey stone pyramid with a long central staircase and a "
                             "small square temple on top, an old stone-paved plaza in front, a dramatic sunset sky with dark clouds and golden sun rays "
                             "bursting from behind the temple",
                "ANH_SANG": "Sunset light at Chichén Itzá: the sun low behind the pyramid temple, golden rays through dark dramatic clouds, warm light on the faces",
                "DIEM_NHIN": "the pyramid",
                "anh": "https://drive.google.com/file/d/1TbAz2KaqGnJc7maH80XzXga2dhPalzg3/view?usp=drivesdk"},
    "tulum": {"NEN_ROBOT": "the Tulum ruins: a grey stone Mayan temple on a rocky green cliff above a calm turquoise Caribbean sea, a white sand beach "
                           "and tall palm trees below, a soft peach-and-gold sunset sky",
              "ANH_SANG": "Warm sunset light at Tulum: soft golden sun from the right, a peach-and-gold sky over the sea",
              "DIEM_NHIN": "the cliff-top temple",
              "anh": "https://drive.google.com/file/d/1RWlDF5JZeE8xVotxDI7nnMyg3akiNWEB/view?usp=drivesdk"},
}

TAY_THUONG = "both arms hang relaxed at the sides, hands still."


def giong(gioi, tuoi):
    """Giọng người học theo giới + tuổi (người thật, tiếng Anh mới học, giọng Mexico)."""
    t = int(tuoi)
    if gioi == "woman":
        pitch = "natural mid-high pitch around 185–230 Hz, bright and warm" if t < 50 else "natural pitch around 165–200 Hz, warm, slightly thin and a little slower with age"
    else:
        pitch = "natural mid-low pitch around 100–135 Hz, warm and relaxed" if t < 50 else "low pitch around 95–125 Hz, slightly raspy, calm and a little slower with age"
    return (f"a real Mexican {gioi} of about {t}, {pitch}, native Mexican Spanish; speaks English as a beginner with a strong Mexican accent, "
            "Spanish vowels and a soft r; a real person, not an actor")


# CSV người dùng "20 biến thể Face to face - Sheet1.csv" (06/11/2026): đổi nhân vật + nền. Ảnh nhân vật toàn thân trên phông xanh.
# (tên biến thể, TEN_HOC, woman/man, tuổi, ngoại hình EN theo ảnh, link ảnh nhân vật, nơi)
D = "https://drive.google.com/file/d/{}/view?usp=drivesdk"
BIEN_THE_20 = [
    ("bien-the-01-lucia", "Lucía", "woman", "25", "a beautiful 25-year-old Mexican woman, a soft oval face, warm brown eyes, light freckles and a gentle smile, light-tan skin, long black hair in two thick braids woven with small red and pink flowers; a white huipil blouse with short puffed sleeves embroidered with red and pink roses and green leaves, a long full red skirt", "12-MINQXRAt7Qvb4YA_1I2Kgco7Ff3uJn", "chichen"),
    ("bien-the-02-valeria", "Valeria", "woman", "22", "a beautiful 22-year-old Mexican woman, a round face, dark brown eyes, warm tan skin, long wavy dark brown hair loose over the shoulders; a cobalt-blue huipil blouse embroidered with pink, yellow and white flowers, a pink fringed rebozo shawl over both shoulders, a long white skirt", "1g7xBU1nJXwQZOiDhoPredfdvyiBJrrFo", "chichen"),
    ("bien-the-03-ximena", "Ximena", "woman", "28", "a beautiful 28-year-old Mexican woman, an oval face, dark brown eyes, warm tan skin, dark hair in a bun under a crown of orange, yellow and purple flowers; a long-sleeved black Oaxaca-style dress densely embroidered with bright multicoloured flowers and butterflies", "1pfX540S8xU1-C-U3Jb3DQBZ4mlrIUaAG", "chichen"),
    ("bien-the-04-daniela", "Daniela", "woman", "24", "a beautiful 24-year-old Mexican woman, a slim oval face, dark eyes, warm tan skin, long straight black hair loose to the waist, small silver hoop earrings; a white short-sleeved blouse with colourful flower embroidery down the front, a long black skirt embroidered with big colourful flowers at the hem", "1-Q3zdz0rtOcWCozEtGA9DzZP_oI2_Hb2", "chichen"),
    ("bien-the-05-mariana", "Mariana", "woman", "27", "a beautiful 27-year-old Mexican woman, a round face with a warm smile, dark eyes, tan skin, black hair in two long braids; a green huipil blouse embroidered with white and gold flowers, a green-and-gold woven shawl over the shoulders, a long yellow pleated skirt", "1xa_j_Psh0LZAT01UTKbClPqZh6-puxaZ", "chichen"),
    ("bien-the-06-diego", "Diego", "man", "26", "a handsome 26-year-old Mexican man, short curly dark hair, light stubble, warm brown eyes, tan skin; a black charro suit embroidered with silver, a red silk neckerchief tied at the collar, a wide black sombrero with silver embroidery", "16I482kGmqS60tEtkkmhtwmG6IQol0m_r", "chichen"),
    ("bien-the-07-javier", "Javier", "man", "30", "a handsome 30-year-old Mexican man, short dark wavy hair, a neat short beard and a friendly smile, tan skin; a white short-sleeved guayabera shirt with pleats and four pockets, beige linen trousers, a straw Panama hat with a black band", "1aDHHZttajKpqvXG9Fv4SEzDJisCbgtWo", "chichen"),
    ("bien-the-08-mateo", "Mateo", "man", "24", "a handsome 24-year-old Mexican man, short dark hair, a young clean-shaven face, dark eyes, tan skin; a navy-blue mariachi suit with silver embroidery and silver buttons, a black bow tie, a wide navy sombrero with silver trim", "1DiNLtlRC4w-rBhYJdj4i4avoYbHUdtLV", "chichen"),
    ("bien-the-09-alejandro", "Alejandro", "man", "32", "a handsome 32-year-old Mexican man, short dark hair, a stubble beard and a strong jaw, tan skin; a white long-sleeved western shirt embroidered with green and black floral patterns, black trousers, a brown vaquero cowboy hat", "1HeZyLr99R3cHeUZnfowCDBUGpEpWUCFP", "chichen"),
    ("bien-the-10-santiago", "Santiago", "man", "28", "a handsome 28-year-old Mexican man, short dark hair, a neatly trimmed beard, tan skin; a white charro suit with silver embroidery, a green silk neckerchief, a wide black sombrero", "1Huoyq8DkkXlovQvWY4Kh2CFfygc8DoaS", "chichen"),
    ("bien-the-11-ernesto", "Ernesto", "man", "68", "a 68-year-old Mexican man, swept-back silver-white hair, a short white beard and moustache, kind dark eyes, tan wrinkled skin; a white long-sleeved linen shirt, beige khaki trousers, brown leather shoes", "1n21o_0whwQbntbGgq3FtQ-utkylRpkiw", "tulum"),
    ("bien-the-12-raul", "Raúl", "man", "72", "a 72-year-old Mexican man, short white hair, a white moustache, deep wrinkles, tan skin; a beige long-sleeved guayabera shirt, grey trousers, a cream Panama hat", "1wk9pXg9K3d4tTNwrQ47QoRuBDgqQgjaB", "tulum"),
    ("bien-the-13-arturo", "Arturo", "man", "65", "a 65-year-old Mexican man, salt-and-pepper hair combed back, clean-shaven, tan skin with light wrinkles; a navy-blue polo shirt, grey chinos with a brown leather belt", "1XKLwnxAiHpEQr2jfRrry3zZtcTEcHpM2", "tulum"),
    ("bien-the-14-rodolfo", "Rodolfo", "man", "75", "a 75-year-old Mexican man, short white hair, clean-shaven, a wrinkled kind face, tan skin; a white dress shirt with a thin grey sweater draped over the shoulders, black trousers", "1vaK7URCjPetXZEx8uT-HOM9ZwpzX4BGS", "tulum"),
    ("bien-the-15-ramon", "Ramón", "man", "70", "a 70-year-old Mexican man, short white hair, clean-shaven, a wrinkled face, tan skin; a light-blue long-sleeved guayabera shirt, white trousers, a wide woven straw hat", "1UrtHQGxc6-D4l8rkaCkde9fZx6WoTLB9", "tulum"),
    ("bien-the-16-rosa", "Rosa", "woman", "66", "a 66-year-old Mexican woman, silver hair in a low bun, a kind wrinkled face, tan skin; a white long-sleeved blouse, a beige shawl over the shoulders, a long navy-blue pleated skirt", "18PCCgoPejbCgnedTKnoYlQtm3otwJwtt", "tulum"),
    ("bien-the-17-carmen", "Carmen", "woman", "70", "a 70-year-old Mexican woman, short silver-white hair, a gentle smile, small earrings, tan skin; a navy-blue floral dress with small pink roses, a long beige cardigan", "14LRSV7b0PKAVTxGw4sfrns9iP12T5TLQ", "tulum"),
    ("bien-the-18-guadalupe", "Guadalupe", "woman", "74", "a 74-year-old Mexican woman, silver hair in a high bun, a wrinkled kind face, tan skin; a cream lightly embroidered short-sleeved blouse, a grey fringed rebozo shawl over the shoulders, a long black skirt", "1Oxjv-WL-NA0d6-mV0ajkl3iMRpfVN4Ih", "tulum"),
    ("bien-the-19-elena", "Elena", "woman", "62", "a 62-year-old Mexican woman, dark hair with grey strands in a neat bun, small gold earrings, tan skin; a white shirt, a light-blue linen blazer, white linen trousers", "11DumJKBriCwNy_oTURx5I5LS1ttnBZiK", "tulum"),
    ("bien-the-20-josefina", "Josefina", "woman", "78", "a 78-year-old Mexican woman, short silver hair, thin wire-rimmed glasses, a gentle smile, tan wrinkled skin; a long pale lavender dress with a thin lavender cardigan", "14diYqWpQC2ZFeHd47S1U7w7jcqQFVYes", "tulum"),
]


def bien_the(name, ten, gioi, nguoi, giong_hoc, anh, tuoi, que, noi, tay=TAY_THUONG):
    n = NOI[noi]
    refs = {"NGUOI_ROBOT": ANH_ROBOT_PHAN1, "NGUOI_DAY": ANH_ROBOT_PHAN2, "NGUOI_HOC": anh, "NEN_ROBOT": n["anh"]}
    nhin, nghe = f"gazes at {n['DIEM_NHIN']} in the centre of the frame with a soft smile", f"keeps gazing at {n['DIEM_NHIN']} with the mouth closed, arms and hands still"
    return {"name": name, **CHUNG,
            # Studio (nút "Thêm vào hàng đợi") chỉ kiểm KHOÁ GỐC, không tính "@1": thiếu là báo "chưa điền". Khoá gốc = giá trị phần 1 (phần 2 không dùng các token này).
            "NHIN_HOC": nhin, "NGHE_HOC": nghe, "VAI_HOC": "traveller",
            "TEN_HOC": ten, "NGUOI_HOC": nguoi, "GIONG_HOC": giong_hoc, "GIOI_HOC": gioi,
            "NEN_ROBOT": n["NEN_ROBOT"], "ANH_SANG": n["ANH_SANG"], "DIEM_NHIN": n["DIEM_NHIN"], "TAY_HOC": tay,
            "NHIN_ROBOT": f"its head turned right toward {ten}, eyes on {ten}'s face",
            "NGHE_ROBOT": f"keeps looking at {ten}, its lips sealed in one still closed line from the first frame to the last, hands clasped, head and body perfectly still",
            # riêng phần 1 (cảnh thường): vị trí, vai, hướng nhìn, tư thế nghe của người học
            "POS_HOC@1": "RIGHT", "VAI_HOC@1": "traveller",
            "NHIN_HOC@1": nhin,
            "NGHE_HOC@1": nghe,
            "LUOT": luot(ten, tuoi, que),
            "refs": _refs(refs, name)}


# File cũ: biến thể Carla (Machu Picchu, bám video mẫu)
res = [bien_the(name, ten, "woman", nguoi, gi, anh, tuoi, que, "machu", tay="both hands are in the pockets of the mustard coat.")
       for name, ten, nguoi, gi, anh, tuoi, que in BIEN_THE]
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(res), OUT)

# File mới: 20 biến thể theo CSV người dùng
OUT20 = os.path.join(os.path.dirname(os.path.abspath(OUT)), "BIEN-THE-DU-LICH-CHIA-DOI-20-BIEN-THE.json")
res20 = [bien_the(name, ten, gioi, nguoi, giong(gioi, tuoi), D.format(anh), tuoi, "Mexico", noi) for name, ten, gioi, tuoi, nguoi, anh, noi in BIEN_THE_20]
json.dump(res20, open(OUT20, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(res20), OUT20)
