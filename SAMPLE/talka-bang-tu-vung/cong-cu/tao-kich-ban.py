"""Tạo lại kịch bản + biến thể Talka bảng từ vựng. Chạy: python cong-cu/tao-kich-ban.py -> ghi đè KICH-BAN-TALKA-CO-CHU.txt và BIEN-THE-TALKA-CO-CHU.json.
Muốn đổi câu chữ prompt thì sửa file này rồi chạy lại, không sửa tay file kịch bản.

Kịch bản Talka bảng từ vựng, bản GỌN: mỗi ý nói một lần, từ vựng nhắc ít lần (prompt dài ~14.000 ký tự làm Muse đọc lẫn từ tiếng Anh vào câu hỏi và làm bút chạy trước lời)."""
import json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # SAMPLE/talka-bang-tu-vung

HEAD = """[STYLE LOCK]:
Photorealistic cinematic CGI, vertical 9:16, sharp, soft even daylight. One locked-off tripod shot, no cuts, no zoom. The TEACHER stands in the lower part of the frame, seen from the belly up (a medium shot): head top at about 40 percent of the frame height, head center at about 62 percent of the frame width, head about 24 percent of the frame width, shoulders about 62 percent of the frame width, her body cut by the bottom edge at the belly; the area above her head shows the background. Same framing, lens and light in every clip. No captions, logos or subtitles.

[CHAR LOCK]:
TEACHER ({{TEN_DAY}}): {{NGUOI_DAY}}. Same face, head and armor in every frame; the only accent color is light blue. Voice: {{GIONG_DAY}}, the same voice in every clip; native Spanish, with the English words said slowly and clearly in an American accent. {{PHAT_AM}}. A lively, expressive human face with accurate lip-sync; her own hands never appear.

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
json.dump([v], open(os.path.join(OUT, "BIEN-THE-TALKA-CO-CHU.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
