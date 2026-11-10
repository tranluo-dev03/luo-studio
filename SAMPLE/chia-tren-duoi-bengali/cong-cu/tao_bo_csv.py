"""Sinh bộ 20 biến thể theo CSV "Face to face HINDI" của người dùng (10/11/2026):
  KICH-BAN-CHIA-TREN-DUOI-BENGALI-ROBOT-MO-DAU.txt  (phần 1 mới: robot nói cả 4 cảnh; phần 2 lấy nguyên từ kịch bản gốc)
  BIEN-THE-CHIA-TREN-DUOI-BENGALI-20-BIEN-THE.json
Chạy:  .venv\\Scripts\\python.exe SAMPLE\\chia-tren-duoi-bengali\\cong-cu\\tao_bo_csv.py
Lời thoại ở LUOT (chép từ CSV, bỏ dấu ngoặc kép). Tên app ở APP. Ngoại hình ở NHAN_VAT (dịch từ cột "Mô tả biến thể_text").
Ảnh tham chiếu người học: cột "Link ảnh biến thể" của 20-bien-the.csv, hoặc tệp anh/bien-the/<STT>.png. Chưa có ảnh thì biến thể chưa có refs NGUOI_HOC và in cảnh báo.
TUOI_THEO_BIEN_THE = True: câu "I have / I am <tuổi>" đổi theo tuổi từng biến thể (CSV ghi cố định twenty five). Đặt False để ai cũng nói twenty five."""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOSO = os.path.join(HERE, "..")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
APP = "Aiva AI"
TUOI_THEO_BIEN_THE = True
ANH = "SAMPLE/chia-tren-duoi-bengali/anh/"
KB_GOC = os.path.join(HOSO, "KICH-BAN-CHIA-TREN-DUOI-BENGALI.txt")
KB_RA = os.path.join(HOSO, "KICH-BAN-CHIA-TREN-DUOI-BENGALI-ROBOT-MO-DAU.txt")
BT_RA = os.path.join(HOSO, "BIEN-THE-CHIA-TREN-DUOI-BENGALI-20-BIEN-THE.json")

CHUC = {20: "twenty", 30: "thirty", 60: "sixty", 70: "seventy"}
DV = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def so_tieng_anh(n):
    return (CHUC[n - n % 10] + (" " + DV[n % 10] if n % 10 else ""))


def luot(tuoi):
    t = so_tieng_anh(tuoi if TUOI_THEO_BIEN_THE else 25)
    L = [
        ("nova", 1, "ইংলিশ শেখার সবচেয়ে প্রথম rule কি?", "friendly, curious"),
        ("nova", 1, "এটাকে মুখস্থ করবেন না। এটাকে ব্যবহার করুন।", "warm"),
        ("nova", 1, "আপনাকে শুধু কারো সাথে regularly কথা বলতে হবে।", "encouraging"),
        ("nova", 1, "AI এর সাথে। চলুন try করি।", "enthusiastic"),
        ("day", 2, "How old are you?", "friendly, curious"),
        ("hoc", 2, f"উম, I have {t}.", "unsure"),
        ("day", 2, f"আপনি বলতে চান, I am {t}.", "encouraging"),
        ("hoc", 2, f"হ্যাঁ, একদম। I am {t}.", "confident"),
        ("day", 2, "Where are you from?", "friendly, curious"),
        ("hoc", 2, "আ, I am Kolkata.", "unsure"),
        ("day", 2, "ভালো চেষ্টা। কিন্তু আপনার বলা উচিত, I am from Kolkata.", "encouraging"),
        ("hoc", 2, "Sorry. আমি প্রায়ই এত ভুল করে ফেলি।", "embarrassed"),
        ("day", 2, "কোন ব্যাপার না। AI teacher try করেছেন কি?", "reassuring"),
        ("day", 2, "Classes থেকে সাত গুণ সস্তা।", "enthusiastic"),
        ("day", 2, "রোজ মাত্র পনেরো থেকে কুড়ি মিনিট বাংলার সাহায্যে শিখলে একদম perfect।", "warm"),
        ("day", 2, "এজন্যই এক কোটিরও বেশি মানুষ নিজেদের ইংলিশ উন্নত করছেন।", "enthusiastic"),
        ("hoc", 2, "Wow! আমি কিভাবে join করব?", "curious"),
        ("day", 2, "নিচে install-এর button চাপুন।", "enthusiastic"),
        ("day", 2, f"{APP} install করুন, sign up করুন আর শুরু করুন।", "enthusiastic"),
        ("day", 2, "দিনেই improvement দেখা যাবে।", "warm"),
    ]
    return [{"who": w, "text": x, "emo": e, "fx": "none", "phan": p} for w, p, x, e in L]


NOVA = ("a sleek feminine humanoid robot, exactly as in its reference photo: a smooth glossy white helmet-like head with no hair and a few thin dark panel lines, a smooth white "
        "porcelain face with soft light-blue eyes and soft neutral pale lips that open and move like a real person's whenever it speaks, small dark ear discs, a black mechanical neck of "
        "cables and pistons, glossy white hexagonal chest and shoulder plates outlined with thin glowing cyan seams over black mechanical joints")
GIONG_NOVA = "a bright, warm young woman's voice (around 220-330 Hz), clear and lively like a favourite teacher, native Kolkata Bengali, says the English words clearly with a light Indian English accent"
CHUNG = {
    "TEN_NOVA": "Nova", "VAI_NOVA": "AI English tutor", "POS_NOVA": "LEFT", "NGUOI_NOVA": NOVA, "GIONG_NOVA": GIONG_NOVA,
    "NHIN_NOVA": "looks only at the other person's face, straight across to the right in exact side profile",
    "NGHE_NOVA": "keeps a gentle closed-mouth smile, the eyes on the other person's face, in exact side profile",
    "NEN_NOVA": "a plain seamless studio backdrop of soft blurred grey tones with faint pale marbled ripple patterns, with no objects and no horizon",
    "POS_HOC": "RIGHT", "VAI_HOC": "learner",
    "NHIN_HOC": "looks only at the robot's face, straight across to the left in exact side profile, and never looks at the camera",
    "NGHE_HOC": "stays calm with the lips pressed together, the eyes open on the robot's face, in exact side profile, and never looks at the camera",
    "TEN_DAY": "Nova", "NGUOI_DAY": NOVA, "GIONG_DAY": GIONG_NOVA,
    "NEN_DAY": "a cosy living room in warm lamplight, slightly out of focus: a wide taupe sofa with a grey-green cushion and a striped rolled armrest on the right, a tall wooden bookcase with books "
               "behind on the left, a lit cream table lamp and a white mug on a side table at the left, long beige curtains and a bright window at the upper right",
    "NEN_HOC": "a bright, tidy Bengali home, slightly out of focus: a cream wall, a wooden shelf full of colourful books on the left with small plain framed family photos on top, a large leafy potted "
               "plant on a shelf on the right, a smaller potted plant low on the left, sheer white curtains and soft daylight at the right, the back of a beige sofa at the bottom of the view",
}

# STT, tên ngắn, giới (nam/nu), tuổi, ngoại hình + phần áo thấy trong khung (dịch từ CSV; quần, giày, phông xanh, tư thế đứng không nằm trong khung nên bỏ)
NHAN_VAT = [
    (1, "nam-25-so-mi-trang", "nam", 25, "tall, an angular face, neatly combed black hair, clean-shaven, a confident smile; a crisp white dress shirt"),
    (2, "nam-28-blazer-navy", "nam", 28, "an oval face, a neatly trimmed beard, a warm smile; a navy blazer over a white dress shirt"),
    (3, "nam-22-so-mi-xanh", "nam", 22, "a youthful face, neatly combed black hair, a bright smile; a light-blue dress shirt"),
    (4, "nam-30-kurta-be", "nam", 30, "an athletic build with broad shoulders, short neat hair, a confident look; a beige kurta under a Nehru vest"),
    (5, "nam-26-kinh-caro", "nam", 26, "black-rimmed glasses, a bright face, side-parted black hair, a soft smile; a smart checked dress shirt"),
    (6, "nu-24-salwar-hong", "nu", 24, "long straight black hair, large eyes, fair skin, a gentle smile; a pink silk salwar kameez with a sheer dupatta and light gold jewellery"),
    (7, "nu-22-kurti-hoa", "nu", 22, "hair in a neat high bun, an oval face, a bright smile; a long elegant floral kurti"),
    (8, "nu-27-sari-do", "nu", 27, "long wavy curls, a confident smile; a luxurious red silk sari with a short blouse and light gold jewellery"),
    (9, "nu-20-kurta-trang", "nu", 20, "a shoulder-length bob, a youthful face, an innocent smile; an elegant white kurta"),
    (10, "nu-26-anarkali-ngoc", "nu", 26, "long straight black hair, a warm smile; a luxurious teal anarkali gown with a dupatta and light gold jewellery"),
    (11, "nam-70-kurta-trang", "nam", 70, "neatly combed silver hair, a kindly face, a neatly trimmed silver beard, a gentle smile; a pure white kurta under a beige Nehru vest"),
    (12, "nam-65-kurta-lua-be", "nam", 65, "silver hair, a gentle face, a warm smile; a beige silk kurta under a Nehru vest"),
    (13, "nam-72-rau-bac", "nam", 72, "a long neatly trimmed silver beard, a distinguished bearing, a kind confident smile; a grey silk kurta under a dark Nehru vest"),
    (14, "nam-60-blazer-navy", "nam", 60, "salt-and-pepper hair, a bright face, a warm smile; a light-blue dress shirt under a navy blazer"),
    (15, "nam-68-kurta-kem", "nam", 68, "neatly combed silver hair, a kindly face, a gentle smile; a cream kurta under a Nehru vest"),
    (16, "nu-65-sari-nau", "nu", 65, "silver hair in a neat low bun, a kind graceful face, a gentle smile; a warm brown silk sari with a blouse and light gold jewellery"),
    (17, "nu-70-sari-xam", "nu", 70, "neatly tied silver hair, a graceful face, a soft smile; a grey silk sari with a blouse and light gold jewellery"),
    (18, "nu-62-salwar-be", "nu", 62, "silver hair in a neat bun, a graceful face, a warm smile; a beige silk salwar kameez with a dupatta and light jewellery"),
    (19, "nu-75-sari-trang", "nu", 75, "white hair in a neat bun, a kindly face, a gentle smile; a pure white silk sari with a gold border, a blouse and light gold jewellery"),
    (20, "nu-68-sari-xanh", "nu", 68, "silver hair in a neat bun, a graceful face, a soft smile; a deep-blue silk sari with a gold border, a blouse and light gold jewellery"),
]


def giong(gioi, tuoi):
    if gioi == "nam":
        muc = "a real young Bengali man's voice, light baritone (around 130-170 Hz), plain and friendly" if tuoi < 40 else "a real elderly Bengali man's voice, warm low baritone (around 105-140 Hz), slightly gravelly and unhurried"
    else:
        muc = "a real young Bengali woman's voice, soft mid pitch (around 190-235 Hz), lower and plainer than the tutor's" if tuoi < 40 else "a real elderly Bengali woman's voice, mellow and slightly husky (around 160-200 Hz), unhurried"
    return muc + ", native Kolkata Bengali, says the English words like a beginner, a little slowly; a real person, not an actor"


def ten(gioi, tuoi):
    return "the " + ("young" if tuoi < 40 else "elderly") + " " + ("man" if gioi == "nam" else "woman")


def nguoi(gioi, tuoi, mo_ta):
    who = ("a young" if tuoi < 40 else "an elderly") + f" Bengali {'man' if gioi == 'nam' else 'woman'} about {tuoi} years old, warm brown skin"
    return f"{who}, {mo_ta}; realistic skin and fabric"


def link_csv():
    rows = list(csv.reader(open(os.path.join(HERE, "20-bien-the.csv"), encoding="utf-8-sig")))
    i = next(k for k, x in enumerate(rows) if x and x[0].startswith("STT"))
    return {int(x[0]): x[3].strip() for x in rows[i + 1:] if x and x[0].strip().isdigit()}


def bien_the():
    links, out, thieu = link_csv(), [], []
    assert set(links) == {n[0] for n in NHAN_VAT}, "CSV và bảng NHAN_VAT lệch STT"
    for stt, slug, gioi, tuoi, mo_ta in NHAN_VAT:
        v = {"name": f"bt-{stt:02d}-{slug}"}
        v.update(CHUNG)
        v.update({"TEN_HOC": ten(gioi, tuoi), "NGUOI_HOC": nguoi(gioi, tuoi, mo_ta), "GIONG_HOC": giong(gioi, tuoi)})
        v["LUOT"] = luot(tuoi)
        refs = {"NGUOI_NOVA": [ANH + "nova.png"], "NGUOI_DAY": [ANH + "nova.png"]}
        tep = f"{ANH}bien-the/{stt:02d}.png"
        if links[stt]:
            refs["NGUOI_HOC"] = [links[stt]]
        elif os.path.isfile(os.path.join(ROOT, tep)):
            refs["NGUOI_HOC"] = [tep]
        else:
            thieu.append(stt)
        v["refs"] = refs
        out.append(v)
    return out, thieu


PHAN1 = """[HAU KY]:
loai: chia-tren-duoi-bengali

[GHI CHU]:
Bản theo CSV "Face to face HINDI" (20 biến thể, lời Bengali, app Aiva AI). Khác KICH-BAN-CHIA-TREN-DUOI-BENGALI.txt ở PHẦN 1: robot nói cả 4 cảnh, người học im suốt phần 1. Phần 2 giữ nguyên.
  Sinh bằng cong-cu/tao_bo_csv.py, không sửa tay. Người học có thể nam hoặc nữ nên phần 1 không dùng đại từ của người học, chỉ dùng {{TEN_HOC}}.
  RỦI RO: phần 1 chỉ robot nói, người thật dễ bị Muse gán khẩu hình; biến thể nữ cùng giới với giọng robot rủi ro cao hơn.

===== PHAN 1: ROBOT MO DAU (CANH THUONG) =====

[STYLE LOCK]:
Vertical 9:16 photorealistic look with glossy clean high-end CGI for the robot, one fixed static camera at head height, a single frame with no split screen. Two figures stand face to face in exact side profile. {{TEN_NOVA}} is at the {{POS_NOVA}} edge of the frame, the face pointing right, the back of the head and the left shoulder touching the left frame edge. {{TEN_HOC}} is at the {{POS_HOC}} edge of the frame, the face pointing left, the back of the head and the right shoulder touching the right frame edge. Both heads are large and level: the tops of the heads at about 32% of the frame height, the chins at about 60%, the upper third of the frame shows only the backdrop. A small gap of backdrop separates the two faces in the middle of the frame. The bodies are seen from the head down to the waist. Same camera, framing and light in every clip. The reference photos show only the robot's design and the person's face, hair and clothing: their backdrops, any green screen, the glowing ring behind the robot and their poses are NOT part of the scene. No text, no letters, no logos anywhere in the frame.

[CHAR LOCK]:
The {{VAI_NOVA}}, {{TEN_NOVA}} ({{POS_NOVA}}): {{NGUOI_NOVA}}. The two robot hands are loosely clasped at the waist at the bottom edge of the frame. VOICE LOCK {{TEN_NOVA}}: one single voice, {{GIONG_NOVA}}, same timbre and pitch in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}. The arms hang at the sides, the hands below the frame.
EYE LINE: {{TEN_NOVA}} {{NHIN_NOVA}}; {{TEN_HOC}} {{NHIN_HOC}}. Each face stays in exact side profile the whole clip.
When silent, {{TEN_NOVA}} {{NGHE_NOVA}}; {{TEN_HOC}} {{NGHE_HOC}}.
RULE: in every clip of this part only the robot speaks; {{TEN_HOC}} is silent the whole clip with the mouth closed.

[SET LOCK]:
Behind them: {{NEN_NOVA}}. The backdrop stays still; nobody else is in the frame.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no shake, no cut. The robot starts talking right away in natural conversational Kolkata Bengali, keeping the English words in English, at about 3.3 words per second, and finishes the line promptly. After the last word both keep a calm closed-mouth face and stay still until the end of the clip. Natural voice, not an announcer. Quiet studio room, no music. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, icons, watermark, letters; writing on the robot or the clothes; hair on the robot; green screen; split screen, overlay, inset window; anyone looking into the lens; a face turning toward the camera; a front or three-quarter view of a face; camera movement, zoom, shake; two voices in one clip; the person moving the lips or mouthing the words; a third person; face, hair, clothes or robot design changing; furniture or objects in the backdrop; background music; robotic text-to-speech voice; slow, dragged speech

"""

CANH = [
    ("0:00-0:02", 1, "Robot hỏi, đầu hơi nghiêng về phía {{TEN_HOC}}.", "the head tilting very slightly toward {{TEN_HOC}} as it asks"),
    ("0:02-0:05", 2, "Robot nói, nhắm mắt một nhịp ở chữ đầu, tay giữ nguyên.", "with one slow blink"),
    ("0:05-0:09", 3, "Robot giảng, mắt nhìn mặt {{TEN_HOC}}, tay giữ nguyên.", "with lively eyebrows"),
    ("0:09-0:12", 4, "Robot nói, cười tươi ở chữ AI, tay giữ nguyên.", "smiling brightly on the word AI"),
]


def ke_canh(i, gio, n, dien_bien, cu_chi):
    dau = ("Khung hoàn chỉnh: {{TEN_NOVA}} mép trái nhìn nghiêng hẳn sang phải, hai tay đan trước eo ở mép dưới khung; {{TEN_HOC}} mép phải nhìn nghiêng hẳn sang trái; nền {{NEN_NOVA}}. Hai người miệng khép."
           if i == 1 else "Chính là khung cuối của cảnh trước.")
    vao = "Start exactly from the start-frame image." if i == 1 else "Start exactly from the provided start frame (the last frame of the previous clip) and continue from it with no cut or reset."
    s = (f"CẢNH {i} ({gio}): Lượt {n}\n"
         "Bối cảnh: một khung duy nhất, nền xám, robot mép trái, người học mép phải, hai người nhìn nghiêng; không chữ.\n"
         f"Voice: (Bengali, chỉ robot nói trong clip này) {{{{LUOT_{n}}}}}\n"
         f"Khung đầu: {dau}\n"
         "Khung cuối: Robot mỉm cười miệng khép nhìn {{TEN_HOC}}; {{TEN_HOC}} vẫn nhìn robot, miệng khép; khung này là khung đầu của cảnh sau.\n"
         f"Diễn biến: {dien_bien} {{{{TEN_HOC}}}} im suốt clip: môi mím, mắt mở nhìn mặt robot, đầu không động. Nói xong cả hai đứng im đến hết clip.\n")
    if i == 1:
        s += ("Prompt ảnh: Generate exactly one still image now, vertical 9:16, a single frame with no split screen. Two figures stand face to face in exact side profile, both heads large and level, the tops of the heads at about 32% of the frame height "
              "and the chins at about 60%; the upper third of the frame shows only the backdrop. At the left edge: {{NGUOI_NOVA}}, the face pointing right, the back of the head and the left shoulder touching the left frame edge, the two hands loosely clasped at the waist "
              "at the bottom edge of the frame. At the right edge: {{NGUOI_HOC}}, the face pointing left, the back of the head and the right shoulder touching the right frame edge, seen from the head down to the waist. A small gap of backdrop separates the two faces in the middle. "
              "Backdrop: {{NEN_NOVA}}. Mouths closed. Each one looks only at the other's face. The reference photos give only the robot's design and the person's face, hair and clothing; their backdrops, any green screen and the glowing ring behind the robot are not part of the scene. No text, no logos, no letters anywhere. Output only the image.\n")
    s += (f"Prompt video: STYLE LOCK, SET LOCK. {vao} CHAR LOCK. {{{{TEN_HOC}}}} on the RIGHT is silent for this whole clip: the lips stay pressed together from the first frame to the last, the eyes stay open on the robot's face, the head does not move; {{{{TEN_HOC}}}} does not copy the robot's face or movements. "
          f"In this clip: {{{{LUOT_{n}}}}} The voice comes only from {{{{TEN_NOVA}}}} on the LEFT edge: the robot's lips open and move in clear sync with every word, {cu_chi}, always in exact side profile. After the line both stay still until the end. VIDEO SUFFIX.\n"
          "Audio: Chỉ giọng robot, rõ, nói xong sớm; phần còn lại im lặng. Không nhạc.\n"
          "Negative prompt: two voices; {{TEN_HOC}} moving the lips or mouthing the words; text or captions; split screen; looking into the lens; camera movement.\n\n")
    return s


def kich_ban():
    goc = open(KB_GOC, encoding="utf-8").read()
    i = goc.index("===== PHAN 2:")
    return PHAN1 + "".join(ke_canh(k + 1, c[0], c[1], c[2], c[3]) for k, c in enumerate(CANH)) + goc[i:]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    open(KB_RA, "w", encoding="utf-8", newline="\n").write(kich_ban())
    bt, thieu = bien_the()
    json.dump(bt, open(BT_RA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.abspath(KB_RA))
    print("Đã ghi", os.path.abspath(BT_RA), f"({len(bt)} biến thể, {len(bt[0]['LUOT'])} lượt)")
    if thieu:
        print("CHƯA CÓ ẢNH người học ở các biến thể:", thieu)
