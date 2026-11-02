"""Tạo lại kịch bản + biến thể Talka bảng từ vựng. Chạy: python cong-cu/tao-kich-ban.py -> ghi đè KICH-BAN-TALKA-CO-CHU.txt và BIEN-THE-TALKA-CO-CHU.json.
Muốn đổi câu chữ prompt thì sửa file này rồi chạy lại, không sửa tay file kịch bản.

Kịch bản Talka bảng từ vựng, bản GỌN: mỗi ý nói một lần, từ vựng nhắc ít lần (prompt dài ~14.000 ký tự làm Muse đọc lẫn từ tiếng Anh vào câu hỏi và làm bút chạy trước lời)."""
import copy, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # SAMPLE/talka-bang-tu-vung

HEAD = """[STYLE LOCK]:
Photorealistic cinematic CGI, vertical 9:16, sharp, soft even daylight. One locked-off tripod shot, no cuts, no zoom. The TEACHER stands in the lower part of the frame, seen from the belly up (a medium shot): head top at about 40 percent of the frame height, head center at about 62 percent of the frame width, head about 24 percent of the frame width, shoulders about 62 percent of the frame width, her body cut by the bottom edge at the belly; the area above her head shows the background. Same framing, lens and light in every clip. No captions, logos or subtitles.

[CHAR LOCK]:
TEACHER ({{TEN_DAY}}): {{NGUOI_DAY}}. Same face, head and armor in every frame; the only accent color is light blue. Voice: {{GIONG_DAY}}, the same voice in every clip; the English words said slowly and clearly in an American accent. {{PHAT_AM}}. A lively, expressive human face with accurate lip-sync; her own hands never appear.

[SET LOCK]:
The background stays exactly as in the start frame: it never moves or changes. The paper is pinned flat and never moves; words already on it never change. No hand, pen, marker or other object ever appears.

[VIDEO SUFFIX]:
Static camera. She speaks the line once at a natural, lively pace, with a short natural pause between sentences. After her last word she settles into the rest pose ({{DAO_NGHI}}) and holds still until the end of the clip (the tail is cut in editing; the next clip starts from that still frame). No music.

[NEGATIVE]:
captions, subtitles, logos, extra text; a second person or voice; the robot's hands in the frame; the robot larger or closer; camera movement or zoom; background or lighting change; face or armor change; misspelled or changing words on the paper; a word written over another word or on the wrong row; music, echo, robotic or text-to-speech voice; stiff face or wrong lip-sync.
"""

ROWS = ["Para mí", "Para ti", "Nunca", "Por favor", "¡Gracias!", "Lo siento", "Hasta luego", "Cuídate"]
ORD = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"]
# cảnh -> (thời lượng, nền, chữ đã có lúc bắt đầu, chữ mới, dòng)
SCENES = [
    ("0:00–0:06", "bang", [], "For me", 1),
    ("0:06–0:12", "bang", ["For me"], "For you", 2),
    ("0:12–0:18", "bang", ["For me", "For you"], "Never", 3),
    ("0:18–0:23", "bang", ["For me", "For you", "Never"], None, 0),
    ("0:23–0:29", "bang", ["For me", "For you", "Never"], "Please", 4),
    ("0:29–0:35", "bang", ["For me", "For you", "Never", "Please"], "Thank you", 5),
    ("0:35–0:40", "pho", [], None, 0),
    ("0:40–0:46", "pho", [], None, 0),
    ("0:46–0:53", "pho", [], None, 0),
]
AUDIO = "Only her voice, clean and dry; no music, no ambient sound."


def paper(done):
    """Bảng chữ CỐ ĐỊNH: các vạch xám luôn trống (chữ tiếng Anh và bút chỉ được ghép ở hậu kỳ)."""
    return "every gray line is empty, exactly as in the start frame"


def pen(new, row, done):
    """Không có chữ hay bút nào xuất hiện trong video: chữ tiếng Anh và cây bút chỉ chữ được ghép ở hậu kỳ, khớp lời đọc."""
    return "The paper behind her never changes: no word appears or is written on it, every gray line stays empty for the whole clip. No hand, pen or marker."


def robot_img(kind):
    bg = "{{NEN_BANG}}. No English words written yet" if kind == "bang" else "{{NEN_PHO}}. No text anywhere"
    return ("One still image (the image itself), vertical 9:16, photorealistic: the TEACHER, {{NGUOI_DAY}}, in the lower part of the frame, from the belly up (medium shot), head about 24 percent of the frame width, shoulders about 62 percent of the frame width, body cut by the bottom edge at the belly, "
            "head top at about 40 percent of the frame height, head center at about 62 percent of the frame width, looking into the lens, lips closed in a soft smile, hands out of the frame. "
            f"Behind her: {bg}. No hand, no marker, no logos.")


body = []
for i, (rng, kind, done, new, row) in enumerate(SCENES, 1):
    first = i == 1 or kind != SCENES[i - 2][1]
    board = kind == "bang"
    L = [f"CẢNH {i} ({rng}): Lượt {i}"]
    L.append("Bối cảnh: " + ("robot nhỏ nửa dưới khung, phía sau là tờ giấy checklist {{NEN_BANG}}." if board else "robot nhỏ nửa dưới khung, phía sau là {{NEN_PHO}}; không có chữ."))
    L.append(f"Voice: {{{{LUOT_{i}}}}}")
    if first:
        L.append("Khung đầu: New start frame: the teacher from the belly up in the lower part of the frame, head top at about 40 percent of the height, " + ("the paper checklist behind her with every gray line empty." if board else "the city skyline behind her, no text."))
    have = done + ([new] if new else [])
    L.append("Khung cuối: She holds the rest pose, still" + ("; no hand; the paper shows " + paper(have) + "." if board else "; no text in the frame.") + (" End of the video." if i == len(SCENES) else ""))
    if first:
        L.append("Prompt ảnh: " + robot_img(kind))
    start = "Start exactly from the start frame." if first else "Continue exactly from the previous clip's last frame (same teacher, pose, framing, background and paper)."
    state = f" Paper at the start: {paper(done)}." if board else ""
    act = (" " + pen(new, row, done)) if new else (" No hand or marker appears; the paper does not change." if board else "")
    L.append(f"Prompt video: {start}{state} {{{{LUOT_{i}}}}}{act} VIDEO SUFFIX.")
    L.append("Audio: " + AUDIO)
    L.append("Negative prompt: " + ("a hand, pen or marker in the frame; any word appearing or being written on the paper; text on the gray lines." if new else
                                   "a hand or marker in the frame." if board else "a hand or marker in the frame; any text in the frame."))
    body.append("\n".join(L))

open(os.path.join(OUT, "KICH-BAN-TALKA-CO-CHU.txt"), "w", encoding="utf-8").write(HEAD + "\n" + "\n\n".join(body) + "\n")

v = json.load(open(os.path.join(OUT, "BIEN-THE-TALKA-CO-CHU.json"), encoding="utf-8"))[0]
v["NEN_BANG"] = ("a big cream-colored paper checklist with a faint dotted grid, pinned flat on a light beige wall and filling almost the whole frame. "
                 "At about 6 percent from the top, the title \"¿CÓMO SE DICE?\" in thick black bold capitals. Below it eight medium-sized rows (not tiny), about 5 percent of the frame height apart, "
                 "from about 12 to 47 percent from the top, so the first five rows are clearly above her head. Each row: a dark bullet, a red circle with a white check mark, and a dark bold Spanish word, in order: "
                 "\"Para mí\", \"Para ti\", \"Nunca\", \"Por favor\", \"¡Gracias!\", \"Lo siento\", \"Hasta luego\", \"Cuídate\"; the Spanish words stay in the left half. "
                 "To the right of each word, a thin light-gray line from about 52 to 88 percent of the frame width, the empty slot for a blue handwritten-style English word. All words sharp and correctly spelled")
# Ngôn ngữ giọng nói nằm trong GIONG_DAY của từng biến thể (script không ghi cứng ngôn ngữ)
if "native Spanish" not in v["GIONG_DAY"]:
    v["GIONG_DAY"] = v["GIONG_DAY"].replace("young woman's voice,", "young woman's voice, speaking native Spanish,", 1)

# Biến thể tiếng Bồ Đào Nha (Brazil): cùng cấu trúc, đổi lời thoại, chữ trên giấy và ngôn ngữ giọng
PT_ROWS = [("Para mí", "Para mim"), ("Para ti", "Para você"), ("Nunca", "Nunca"), ("Por favor", "Por favor"), ("¡Gracias!", "Obrigado!"),
           ("Lo siento", "Sinto muito"), ("Hasta luego", "Até logo"), ("Cuídate", "Se cuida")]
PT_TEXTS = [
    "Como se diz para mim em inglês? Se diz, for me. Repita comigo. For me.",
    "Como se diz para você? Se diz, for you. Repita comigo. For you.",
    "Como se diz nunca? Se diz, never. Repita comigo. Never.",
    "O inglês não é difícil, e você vai descobrir que eu tenho razão se seguir esta página.",
    "Como se diz por favor? Se diz, please. Repita comigo. Please.",
    "Como se diz obrigado? Se diz, thank you. Repita comigo. Thank you.",
    "Quer aprender inglês de um jeito mais fácil?",
    "Baixe o Talka e em apenas quatro semanas você vai soar como um falante nativo.",
    "Um tutor com IA que corrige você em tempo real e acelera o seu progresso. Best Language Learning App. Download now.",
]
pt = copy.deepcopy(v)
pt["name"] = v["name"] + "-pt"
pt["GIONG_DAY"] = v["GIONG_DAY"].replace("speaking native Spanish", "speaking native Brazilian Portuguese (not Spanish)")
pt["PHAT_AM"] = v["PHAT_AM"].replace("two equal Spanish syllables", "two equal Portuguese syllables")
nb = v["NEN_BANG"].replace("¿CÓMO SE DICE?", "COMO SE DIZ?").replace("dark bold Spanish word", "dark bold Portuguese word").replace("the Spanish words stay", "the Portuguese words stay")
for es, p in PT_ROWS:
    assert f'"{es}"' in nb, es
    nb = nb.replace(f'"{es}"', f'"{p}"')
pt["NEN_BANG"] = nb
assert len(pt["LUOT"]) == len(PT_TEXTS) == 9
for turn, text in zip(pt["LUOT"], PT_TEXTS):
    turn["text"] = text

# ---- Các biến thể theo video tham chiếu. Chỉ khác nhau ở: tờ giấy (NEN_BANG), danh sách từ + lời đọc, ngôn ngữ, và khoá HAU_KY (kiểu giấy / kiểu bút cho hậu kỳ).
# HAU_KY = {"giay": pointer.LAYOUTS (hai-cot | hai-cot-icon-trai | so-tay), "but": assets/marker-<kiểu>.png (fountain | ballpoint)}; bỏ trống = tờ checklist + bút đỏ mẫu.
# Hình học giấy trong NEN_BANG (vạch kẻ hàng 1 ở 18,5% chiều cao, các vạch cách nhau 4,8%, cột phải bắt đầu ở ~57% bề rộng) phải khớp pointer.LAYOUTS.
VOCAB_TURNS = (0, 1, 2, 4, 5)   # lượt 1, 2, 3, 5, 6 là 5 từ vựng; lượt 4 (động viên) và 7-9 (quảng cáo) giữ nguyên theo biến thể gốc


def make(base, name, vocab_texts, nen_bang, hau_ky=None):
    x = copy.deepcopy(base)
    x["name"], x["NEN_BANG"] = name, nen_bang
    assert len(vocab_texts) == len(VOCAB_TURNS)
    for i, t in zip(VOCAB_TURNS, vocab_texts):
        x["LUOT"][i]["text"] = t
    if hau_ky:
        x["HAU_KY"] = hau_ky
    return x


def words(ws):
    return ", ".join('"' + w + '"' for w in ws)


ROW_GEOMETRY = ("Below it there are eight rows, each sitting on its own thin ruled line: the first ruled line at about 18.5 percent from the top and the next lines every 4.8 percent, "
                "so the first five rows are clearly above her head. ")
EMPTY_RIGHT = "The whole right column stays completely empty (only the ruled lines, no words and no icons): it is the empty slot for a red handwritten-style English word. All words sharp and correctly spelled"
ICONS = "a speech bubble, a rising sun, two waving hands, a person outline, a gift box, a heart, praying hands and a sad face"


def paper_hai_cot(title, head_left, ws):
    """Giấy kẻ dòng hai cột (Español | English), icon nhỏ bên phải từ bản ngữ (ref 3, 4)."""
    return ("a big sheet of white lined notebook paper with thin pale blue ruled lines across the whole sheet and no dotted grid, pinned flat on a light gray wall and filling almost the whole frame. "
            f"At about 4 percent from the top, the title \"{title}\" in dark handwritten-style letters. At about 11 percent from the top, two column headers: \"{head_left}\" on the left with a dark underline and \"English\" on the right with a red underline. "
            "A thin dark vertical line divides the page into a left and a right column at about 53 percent of the frame width, from about 9 percent from the top down to the bottom of the page. "
            + ROW_GEOMETRY +
            f"In the left column each row has a dark handwritten word starting at about 4 percent of the frame width, followed right after by a small black line-art doodle icon, in order: {words(ws)}; the doodle icons in order are {ICONS}. "
            + EMPTY_RIGHT)


ES_ROWS_23 = ["Disculpa", "Buenos días", "Adiós", "¿Cómo estás?", "Gracias", "Te amo", "Por favor", "Lo siento"]
PT_ROWS_4 = ["Desculpa", "Bom dia", "Tchau", "Como vai?", "Obrigado", "Eu te amo", "Por favor", "Sinto muito"]
ES_TEXTS_23 = [
    "¿Cómo se dice disculpa en inglés? Se dice, excuse me. Repite conmigo. Excuse me.",
    "¿Cómo se dice buenos días? Se dice, good morning. Repite conmigo. Good morning.",
    "¿Cómo se dice adiós? Se dice, goodbye. Repite conmigo. Goodbye.",
    "¿Cómo se dice cómo estás? Se dice, how are you. Repite conmigo. How are you.",
    "¿Cómo se dice gracias? Se dice, thank you. Repite conmigo. Thank you.",
]
PT_TEXTS_4 = [
    "Como se diz desculpa em inglês? Se diz, excuse me. Repita comigo. Excuse me.",
    "Como se diz bom dia? Se diz, good morning. Repita comigo. Good morning.",
    "Como se diz tchau? Se diz, goodbye. Repita comigo. Goodbye.",
    "Como se diz como vai? Se diz, how are you. Repita comigo. How are you.",
    "Como se diz obrigado? Se diz, thank you. Repita comigo. Thank you.",
]

# Biến thể 2 (ref 2): giữ tờ checklist mẫu, đổi danh sách từ + lời đọc
nb_checklist = v["NEN_BANG"]
head, tail = nb_checklist.split("in order: ")[0], nb_checklist.split("; the Spanish words stay")[1]
v2 = make(v, v["name"].replace("-co-chu", "") + "-bt2", ES_TEXTS_23, head + "in order: " + words(ES_ROWS_23) + "; the Spanish words stay" + tail)

# Biến thể 3 (ref 3): giấy kẻ dòng hai cột, cùng danh sách từ
v3 = make(v, v["name"].replace("-co-chu", "") + "-bt3", ES_TEXTS_23, paper_hai_cot("¿Cómo se dice?", "Español", ES_ROWS_23), {"giay": "hai-cot"})

# Biến thể 4 (ref 4): như biến thể 3 nhưng tiếng Bồ Đào Nha (lời quảng cáo + động viên lấy từ biến thể Bồ gốc)
v4 = make(pt, v["name"].replace("-co-chu", "") + "-bt4-pt", PT_TEXTS_4, paper_hai_cot("Como se diz?", "Português", PT_ROWS_4), {"giay": "hai-cot"})

# Biến thể 5 (ref 5): sổ lò xo có vạch kẻ từng hàng + icon, bút máy; cùng danh sách từ với bản gốc
ES_ROWS_5 = ["Para mí", "Para ti", "Nunca", "Por favor", "¡Gracias!", "Lo siento", "Hasta luego", "Cuídate"]
nb5 = ("a tall cream-colored spiral-bound notepad filling almost the whole frame, pinned flat on a light gray wall: along its top edge a row of seven black metal spiral rings. "
       "At about 9 percent from the top, the title \"¿CÓMO SE DICE?\" in thick black bold serif capitals with a thin line under it. "
       + ROW_GEOMETRY +
       f"Each row has a dark serif Spanish word starting at about 12 percent of the frame width, followed right after by a small black line-art doodle icon, in order: {words(ES_ROWS_5)}; "
       "the doodle icons in order are a person with a hand on the chest, a person pointing, a crossed circle, praying hands, a heart, a sad face, a waving hand and a smiling face; "
       "the words and icons stay in the left half. Every ruled line continues to the right, and the right part of every line, from about 60 to 90 percent of the frame width, is an empty slot for a dark red serif English word: no words and no icons there. All words sharp and correctly spelled")
v5 = make(v, v["name"].replace("-co-chu", "") + "-bt5", [v["LUOT"][i]["text"] for i in VOCAB_TURNS], nb5, {"giay": "so-tay", "but": "fountain"})

# Biến thể 6 (ref 6): giấy kẻ dòng hai cột, icon bên trái từ, danh sách từ mới, bút bi đỏ
ES_ROWS_6 = ["Dios mío", "Gracias", "Por qué", "Cómo", "Mañana", "Para mí", "Para ti", "Nunca"]
ES_TEXTS_6 = [
    "¿Cómo se dice dios mío en inglés? Se dice, oh my god. Repite conmigo. Oh my god.",
    "¿Cómo se dice gracias? Se dice, thank you. Repite conmigo. Thank you.",
    "¿Cómo se dice por qué? Se dice, why. Repite conmigo. Why.",
    "¿Cómo se dice cómo? Se dice, how. Repite conmigo. How.",
    "¿Cómo se dice mañana? Se dice, tomorrow. Repite conmigo. Tomorrow.",
]
nb6 = ("a big sheet of white lined notebook paper with thin pale blue ruled lines across the whole sheet and no dotted grid, pinned flat on a light gray wall and filling almost the whole frame. "
       "At about 4 percent from the top, the title \"¿CÓMO SE DICE?\" in dark navy printed capitals with a thick dark underline. At about 11 percent from the top, two column headers: \"Español\" on the left with a dark underline and \"English\" on the right with a red underline. "
       "A thin dark vertical line divides the page into a left and a right column at about 53 percent of the frame width, from about 9 percent from the top down to the bottom of the page. "
       + ROW_GEOMETRY +
       f"In the left column each row starts with a small black line-art doodle icon at about 5 percent of the frame width, followed by a dark handwritten Spanish word starting at about 19 percent of the frame width, in order: {words(ES_ROWS_6)}; "
       "the doodle icons in order are praying hands with a halo, a gift box, a question mark, a magnifying glass, a sunrise, a heart, a person with an arrow and a prohibition sign. "
       + EMPTY_RIGHT)
v6 = make(v, v["name"].replace("-co-chu", "") + "-bt6", ES_TEXTS_6, nb6, {"giay": "hai-cot-icon-trai", "but": "ballpoint"})

names = [x["name"] for x in (v, pt, v2, v3, v4, v5, v6)]
assert len(set(names)) == len(names), names
json.dump([v, pt, v2, v3, v4, v5, v6], open(os.path.join(OUT, "BIEN-THE-TALKA-CO-CHU.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", names)
