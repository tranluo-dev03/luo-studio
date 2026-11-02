"""Tạo lại kịch bản + biến thể Talka bảng từ vựng. Chạy: python cong-cu/tao-kich-ban.py -> ghi đè KICH-BAN-TALKA-CO-CHU.txt và BIEN-THE-TALKA-CO-CHU.json.
Muốn đổi câu chữ prompt thì sửa file này rồi chạy lại, không sửa tay file kịch bản.

Cách làm: Muse chỉ gen ROBOT trên NỀN XANH LỤC phẳng (các cảnh dạy từ) và robot trên nền thành phố (cảnh quảng cáo, không có giấy).
Hậu kỳ (app/production/types/talka-bang-tu-vung) tự dựng tờ giấy (ảnh tĩnh, từ khai trong HAU_KY.bang của biến thể), tách nền xanh, ghép robot lên giấy,
viết chữ tiếng Anh và vẽ bút chỉ đúng chỗ; ô bảng quảng cáo cũng thêm ở hậu kỳ.
Kịch bản BẢN GỌN: mỗi ý nói một lần, từ vựng nhắc ít lần (prompt dài làm Muse đọc lẫn từ tiếng Anh vào câu hỏi)."""
import copy, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # SAMPLE/talka-bang-tu-vung

HEAD = """[STYLE LOCK]:
Photorealistic cinematic CGI, vertical 9:16, sharp, soft even daylight. One locked-off tripod shot, no cuts, no zoom. The TEACHER stands in the lower part of the frame, seen from the belly up (a medium shot): head top at about 40 percent of the frame height, head center at about 62 percent of the frame width, head about 24 percent of the frame width, shoulders about 62 percent of the frame width, her body cut by the bottom edge at the belly; the area above her head shows the background. Same framing, lens and light in every clip. No captions, logos or subtitles.

[CHAR LOCK]:
TEACHER ({{TEN_DAY}}): {{NGUOI_DAY}}. Same face, head and armor in every frame; the only accent color is light blue. Voice: {{GIONG_DAY}}, the same voice in every clip; the English words said slowly and clearly in an American accent. {{PHAT_AM}}. A lively, expressive human face with accurate lip-sync; her own hands never appear.

[SET LOCK]:
The background stays exactly as in the start frame: it never moves or changes. Lesson clips: the background is one perfectly flat, evenly lit green screen and nothing else (no paper, no wall, no writing, no object); her body has no green reflection or green rim light. Advert clips: the city skyline stays exactly as in the start frame, with no paper, board or note anywhere. No hand, pen, marker or other object ever appears.

[VIDEO SUFFIX]:
Static camera. She speaks the line once at a natural, lively pace, with a short natural pause between sentences. After her last word she settles into the rest pose ({{DAO_NGHI}}) and holds still until the end of the clip (the tail is cut in editing; the next clip starts from that still frame). No music.

[NEGATIVE]:
captions, subtitles, logos, extra text; a second person or voice; the robot's hands in the frame; the robot larger or closer; camera movement or zoom; background or lighting change; face or armor change; paper, notes, writing or any object behind her; music, echo, robotic or text-to-speech voice; stiff face or wrong lip-sync.
"""

# cảnh -> (thời lượng, nền: "xanh" = nền xanh lục (dạy từ), "pho" = nền thành phố (quảng cáo))
SCENES = [
    ("0:00–0:06", "xanh"),
    ("0:06–0:12", "xanh"),
    ("0:12–0:18", "xanh"),
    ("0:18–0:23", "xanh"),
    ("0:23–0:29", "xanh"),
    ("0:29–0:35", "xanh"),
    ("0:35–0:40", "pho"),
    ("0:40–0:46", "pho"),
    ("0:46–0:53", "pho"),
]
AUDIO = "Only her voice, clean and dry; no music, no ambient sound."
BG = {"xanh": "{{NEN_XANH}}", "pho": "{{NEN_PHO}}"}


# Cảnh giới thiệu app: ô bảng chữ (thêm ở hậu kỳ) nằm ở khoảng 18-38% chiều cao khung, nên robot phải NHỎ và THẤP (đầu từ ~50% trở xuống), nửa trên chỉ có trời và thành phố
AD_FRAME = ("She is small and LOW in the frame, seen from further away than a close-up portrait: head about 20 percent of the frame width, shoulders about 50 percent of the frame width, "
            "head top at about 50 percent of the frame height, head center at about 62 percent of the frame width, body cut by the bottom edge at the chest; "
            "the whole upper half of the frame (above 45 percent of the height) shows only sky and the distant skyline, completely empty on purpose because a text box is added there later")


def robot_img(kind):
    bg = "{{NEN_XANH}}. Nothing else in the frame" if kind == "xanh" else "{{NEN_PHO}}. No text anywhere, no paper, no board, no note"
    if kind == "xanh":
        frame = ("in the lower part of the frame, from the belly up (medium shot), head about 24 percent of the frame width, shoulders about 62 percent of the frame width, body cut by the bottom edge at the belly, "
                 "head top at about 40 percent of the frame height, head center at about 62 percent of the frame width")
    else:
        frame = AD_FRAME
    return ("One still image (the image itself), vertical 9:16, photorealistic: the TEACHER, {{NGUOI_DAY}}, " + frame + ", looking into the lens, lips closed in a soft smile, hands out of the frame. "
            f"Behind her: {bg}. No hand, no marker, no logos.")


body = []
for i, (rng, kind) in enumerate(SCENES, 1):
    first = i == 1 or kind != SCENES[i - 2][1]
    lesson = kind == "xanh"
    L = [f"CẢNH {i} ({rng}): Lượt {i}"]
    L.append("Bối cảnh: " + (f"robot nhỏ nửa dưới khung, phía sau chỉ có nền xanh lục phẳng: {BG[kind]}. Không có giấy, không có chữ (hậu kỳ ghép tờ giấy sau)."
                            if lesson else f"robot NHỎ và THẤP (đỉnh đầu ~50% chiều cao, nửa trên khung chỉ có trời và thành phố, để trống cho ô chữ), phía sau là {BG[kind]}; không có chữ, không có tờ giấy (hậu kỳ thêm bảng sau)."))
    L.append(f"Voice: {{{{LUOT_{i}}}}}")
    if first:
        L.append("Khung đầu: New start frame: the teacher from the belly up in the lower part of the frame, head top at about 40 percent of the height, "
                 + ("against one perfectly flat green screen, nothing else." if lesson else "head top at about 50 percent of the height (small and low in the frame), the upper half only sky and distant skyline, no text, no paper."))
    L.append("Khung cuối: She holds the rest pose, still" + ("; no hand; the background is still one flat green." if lesson else "; no text in the frame, no paper.") + (" End of the video." if i == len(SCENES) else ""))
    if first:
        L.append("Prompt ảnh: " + robot_img(kind))
    start = "Start exactly from the start frame." if first else "Continue exactly from the previous clip's last frame (same teacher, pose, framing and the same background)."
    act = (" The green background stays one flat green: nothing appears on it. No hand, pen or marker." if lesson else
           " She stays small and low for the whole clip: her head never rises above 45 percent of the frame height and she never moves closer to the camera. No hand, pen or marker appears; the city background does not change.")
    L.append(f"Prompt video: {start} {{{{LUOT_{i}}}}}{act} VIDEO SUFFIX.")
    L.append("Audio: " + AUDIO)
    L.append("Negative prompt: " + ("paper, notes, writing, gradient, shadow or any object in the background; green on her body; a hand, pen or marker in the frame." if lesson
                                   else "a paper, note, notebook or board in the frame; a close-up or large robot, her head in the upper half of the frame, her moving closer to the camera; a hand or marker in the frame; any text in the frame."))
    body.append("\n".join(L))

open(os.path.join(OUT, "KICH-BAN-TALKA-CO-CHU.txt"), "w", encoding="utf-8").write(HEAD + "\n" + "\n\n".join(body) + "\n")

# ------------------------------------------------------------------ biến thể
v = json.load(open(os.path.join(OUT, "BIEN-THE-TALKA-CO-CHU.json"), encoding="utf-8"))[0]
v.pop("NEN_BANG", None)   # tờ giấy do hậu kỳ dựng (HAU_KY.bang), không còn gửi cho Muse
v.pop("HAU_KY", None)
v["NEN_XANH"] = "a perfectly flat, evenly lit, saturated chroma-key green screen (about #00B140) filling the whole frame: no texture, no gradient, no shadow, no object, no text"
# Ngôn ngữ giọng nói nằm trong GIONG_DAY của từng biến thể (script không ghi cứng ngôn ngữ)
if "native Spanish" not in v["GIONG_DAY"]:
    v["GIONG_DAY"] = v["GIONG_DAY"].replace("young woman's voice,", "young woman's voice, speaking native Spanish,", 1)

# Biểu tượng nhỏ bên cạnh từ (font Segoe UI Symbol, đơn sắc)
I = dict(noi="\U0001F4AC", nang="☀", vay="✋", nguoi="\U0001F464", qua="\U0001F381", tim="♡", cau="\U0001F64F", buon="☹", hoi="❓",
         kinh="\U0001F50D", binhminh="\U0001F305", cam="\U0001F6AB", cuoi="☺")


def hang(words, icons=None):
    return [{"tu": w, **({"icon": icons[k]} if icons else {})} for k, w in enumerate(words)]


def hau_ky(kieu, tieu_de, words, icons=None, dau_trai="", but=None):
    h = {"giay": kieu, "bang": {"tieu_de": tieu_de, "hang": hang(words, icons)}}
    if dau_trai:
        h["bang"]["dau_trai"] = dau_trai
    if but:
        h["but"] = but
    return h


ES_ROWS = ["Para mí", "Para ti", "Nunca", "Por favor", "¡Gracias!", "Lo siento", "Hasta luego", "Cuídate"]
v["HAU_KY"] = hau_ky("checklist", "¿CÓMO SE DICE?", ES_ROWS)

# Biến thể 1 (ref 1): tờ checklist mẫu, tiếng Bồ Đào Nha (Brazil)
PT_ROWS = ["Para mim", "Para você", "Nunca", "Por favor", "Obrigado!", "Sinto muito", "Até logo", "Se cuida"]
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
pt["HAU_KY"] = hau_ky("checklist", "COMO SE DIZ?", PT_ROWS)
assert len(pt["LUOT"]) == len(PT_TEXTS) == 9
for turn, text in zip(pt["LUOT"], PT_TEXTS):
    turn["text"] = text

# ---- Các biến thể theo video tham chiếu: chỉ khác nhau ở tờ giấy + danh sách từ + lời đọc + ngôn ngữ + bút (khoá HAU_KY).
VOCAB_TURNS = (0, 1, 2, 4, 5)   # lượt 1, 2, 3, 5, 6 là 5 từ vựng; lượt 4 (động viên) và 7-9 (quảng cáo) giữ nguyên theo biến thể gốc


def make(base, name, vocab_texts, hk):
    x = copy.deepcopy(base)
    x["name"], x["HAU_KY"] = name, hk
    assert len(vocab_texts) == len(VOCAB_TURNS)
    for i, t in zip(VOCAB_TURNS, vocab_texts):
        x["LUOT"][i]["text"] = t
    return x


ES_ROWS_23 = ["Disculpa", "Buenos días", "Adiós", "¿Cómo estás?", "Gracias", "Te amo", "Por favor", "Lo siento"]
ICONS_23 = [I["noi"], I["nang"], I["vay"], I["nguoi"], I["qua"], I["tim"], I["cau"], I["buon"]]
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
ES_ROWS_5 = ES_ROWS
ICONS_5 = [I["nguoi"], I["vay"], I["cam"], I["cau"], I["tim"], I["buon"], I["vay"], I["cuoi"]]
ES_ROWS_6 = ["Dios mío", "Gracias", "Por qué", "Cómo", "Mañana", "Para mí", "Para ti", "Nunca"]
ICONS_6 = [I["cau"], I["qua"], I["hoi"], I["kinh"], I["binhminh"], I["tim"], I["nguoi"], I["cam"]]
ES_TEXTS_6 = [
    "¿Cómo se dice dios mío en inglés? Se dice, oh my god. Repite conmigo. Oh my god.",
    "¿Cómo se dice gracias? Se dice, thank you. Repite conmigo. Thank you.",
    "¿Cómo se dice por qué? Se dice, why. Repite conmigo. Why.",
    "¿Cómo se dice cómo? Se dice, how. Repite conmigo. How.",
    "¿Cómo se dice mañana? Se dice, tomorrow. Repite conmigo. Tomorrow.",
]
stem = v["name"].replace("-co-chu", "")

# Biến thể 2 (ref 2): tờ checklist mẫu, danh sách từ + lời đọc mới
v2 = make(v, stem + "-bt2", ES_TEXTS_23, hau_ky("checklist", "¿CÓMO SE DICE?", ES_ROWS_23))
# Biến thể 3 (ref 3): giấy kẻ dòng hai cột Español | English, icon bên phải từ
v3 = make(v, stem + "-bt3", ES_TEXTS_23, hau_ky("hai-cot", "¿Cómo se dice?", ES_ROWS_23, ICONS_23, "Español"))
# Biến thể 4 (ref 4): như biến thể 3 nhưng tiếng Bồ Đào Nha
v4 = make(pt, stem + "-bt4-pt", PT_TEXTS_4, hau_ky("hai-cot", "Como se diz?", PT_ROWS_4, ICONS_23, "Português"))
# Biến thể 5 (ref 5): sổ lò xo có vạch kẻ từng hàng + icon, bút máy; cùng danh sách từ với bản gốc
v5 = make(v, stem + "-bt5", [v["LUOT"][i]["text"] for i in VOCAB_TURNS], hau_ky("so-tay", "¿CÓMO SE DICE?", ES_ROWS_5, ICONS_5, but="fountain"))
# Biến thể 6 (ref 6): giấy kẻ dòng hai cột, icon bên trái từ, danh sách từ mới, bút bi đỏ
v6 = make(v, stem + "-bt6", ES_TEXTS_6, hau_ky("hai-cot-icon-trai", "¿CÓMO SE DICE?", ES_ROWS_6, ICONS_6, "Español", but="ballpoint"))

names = [x["name"] for x in (v, pt, v2, v3, v4, v5, v6)]
assert len(set(names)) == len(names), names
json.dump([v, pt, v2, v3, v4, v5, v6], open(os.path.join(OUT, "BIEN-THE-TALKA-CO-CHU.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", names)
