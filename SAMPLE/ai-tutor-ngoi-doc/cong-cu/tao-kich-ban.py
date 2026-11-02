"""Tạo kịch bản + biến thể cho thể loại "AI tutor ngồi đọc". Chạy: python cong-cu/tao-kich-ban.py
-> ghi KICH-BAN-AI-TUTOR-NGOI-DOC.txt và BIEN-THE-AI-TUTOR-NGOI-DOC.json (4 biến thể: gốc, đổi nền, đổi ngôn ngữ sang tiếng Bồ Đào Nha + cờ, đổi AI).

Muse chỉ gen robot ngồi đọc (phần trên khung để trống). Bảng phía trên do hậu kỳ ghép: khung bảng gen bằng AI theo ô CO, chữ trong bảng
do code điền theo ô BANG_TU (mỗi dòng "tiếng mẹ đẻ | tiếng học | phiên âm"; dòng cuối không có "|" là câu kết), khớp lúc robot đọc."""
import json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # SAMPLE/ai-tutor-ngoi-doc
PER_CLIP = 3          # số cặp câu mỗi cảnh (mỗi cảnh ~8–9 giây)

HEAD = """[STYLE LOCK]:
Photorealistic cinematic CGI, vertical 9:16, sharp, warm natural light. One locked-off tripod shot, no cuts, no zoom. The TUTOR sits behind a small round table in the lower part of the frame, seen from the waist up and centered: head top at about 36 percent of the frame height, head about 22 percent of the frame width, both forearms resting on the table; the table edge is near the bottom of the frame. The whole upper third of the frame shows only the background, with nothing important in it (a sign is added there in editing). Same framing, lens and light in every clip. No text, captions, logos or subtitles anywhere.

[CHAR LOCK]:
TUTOR ({{TEN_DAY}}): {{NGUOI_DAY}}. Same face, head, body and outfit in every frame. Voice: {{GIONG_DAY}}, the same voice in every clip. She is a native {{NGON_NGU_ME}} speaker teaching {{NGON_NGU_HOC}}: she says each {{NGON_NGU_ME}} phrase naturally, then its {{NGON_NGU_HOC}} translation slowly and clearly with a correct {{NGON_NGU_HOC}} accent. A friendly, expressive face with accurate lip-sync; small natural head movements; her hands stay relaxed on the table.

[SET LOCK]:
Background: {{NEN}}. It stays exactly as in the start frame for every clip: nothing in it moves or changes, no people walk through. No text, signs or writing anywhere.

[VIDEO SUFFIX]:
Static camera. She reads the phrase pairs in order at a calm teaching pace: each {{NGON_NGU_ME}} phrase, a tiny pause, its {{NGON_NGU_HOC}} translation, then a short pause before the next pair. After the last word she settles into the rest pose ({{DAO_NGHI}}) and holds still until the end of the clip (the tail is cut in editing; the next clip starts from that still frame). No music.

[NEGATIVE]:
captions, subtitles, logos, any text or letters in the frame; signs or boards in the background; a second person or voice; the tutor standing up, leaving or changing position; the tutor larger, closer or off-center; camera movement or zoom; background or lighting change; outfit or face change; music, echo, robotic or text-to-speech voice; wrong language or wrong accent; skipped, repeated or reordered phrases; stiff face or wrong lip-sync.

[HAU KY]:
loai: ai-tutor-ngoi-doc
Bảng từ (mỗi dòng: tiếng mẹ đẻ | tiếng học | phiên âm; dòng cuối = câu kết): {{BANG_TU}}
Trang trí bảng (cờ, linh vật): {{CO}}
"""


def pairs(bang):
    rows = [[c.strip() for c in l.split("|")] for l in bang.strip().splitlines() if l.strip()]
    return [r for r in rows if len(r) >= 2], next((r[0] for r in rows if len(r) == 1), "")


def turns(bang):
    """Lời đọc của từng cảnh, lấy đúng từ bảng từ: mỗi cảnh PER_CLIP cặp "mẹ đẻ. học."; câu kết đọc ở cảnh cuối."""
    ps, closing = pairs(bang)
    groups = [ps[i:i + PER_CLIP] for i in range(0, len(ps), PER_CLIP)]
    out = []
    for gi, g in enumerate(groups):
        said = " ".join(f"{a.rstrip('.!')}{'' if a.endswith(('?', '!')) else '.'} {b.rstrip('.!')}{'' if b.endswith(('?', '!')) else '.'}" for a, b, *_ in g)
        if gi == len(groups) - 1 and closing:
            said += " " + closing
        out.append({"who": "day", "text": said, "emo": "warm, encouraging", "fx": "none"})
    return out


def script(n):
    body = []
    for i in range(1, n + 1):
        L = [f"CẢNH {i} (0:{(i - 1) * 9:02d}–0:{i * 9:02d}): Lượt {i}"]
        L.append("Bối cảnh: robot tutor ngồi sau bàn nhỏ ở nửa dưới khung; phía sau là {{NEN}}; phần trên khung để trống (hậu kỳ ghép bảng).")
        L.append(f"Voice: {{{{LUOT_{i}}}}}")
        if i == 1:
            L.append("Khung đầu: New start frame: the tutor sitting behind the table, waist up, centered, head top at about 36 percent of the frame height, the upper third of the frame only background.")
        L.append("Khung cuối: She holds the rest pose, still, looking into the lens; same framing and background.")
        if i == 1:
            L.append("Prompt ảnh: One still image (the image itself), vertical 9:16, photorealistic: the TUTOR, {{NGUOI_DAY}}, sitting behind a small round table, "
                     "seen from the waist up, centered, head top at about 36 percent of the frame height, forearms resting on the table, looking into the lens, "
                     "lips closed in a soft smile. Behind her: {{NEN}}. The upper third of the frame shows only background. No text, no signs, no logos.")
        start = "Start exactly from the start frame." if i == 1 else "Continue exactly from the previous clip's last frame (same tutor, pose, framing and background)."
        L.append(f"Prompt video: {start} {{{{LUOT_{i}}}}} VIDEO SUFFIX.")
        L.append("Audio: Only her voice, clean and dry; no music, no ambient sound.")
        L.append("Negative prompt: any text or sign in the frame; a phrase read in the wrong language; skipped or repeated phrases.")
        body.append("\n".join(L))
    return HEAD + "\n" + "\n\n".join(body) + "\n"


ROBOT = ("a sleek white humanoid robot tutor with a realistic young woman's face, glowing light blue eyes, a smooth white head with a red-and-black headset "
         "and a small microphone, black mechanical neck and joints, wearing a red and green Portugal football jersey with the number 7")
ROBOT_2 = ("a friendly chrome-silver robot tutor with a rounded helmet-like head, a smooth dark glass face screen showing two large glowing cyan oval eyes "
           "and a small smiling mouth light, slim silver arms with dark joints, wearing a yellow Brazil football jersey with green trim")
CAFE = ("a cozy sunny cafe interior: a large window onto a street with trees, warm wooden shelves with plants and hanging lamps, "
        "a latte with heart foam art and a glass of water on the table, softly out of focus")
LISBON = ("an outdoor cafe terrace on a sunny Lisbon street: colorful blue-and-white tiled building facades, a yellow vintage tram in the distance, "
          "a cobblestone sidewalk, a pastel de nata and an espresso on the table, softly out of focus")
US_FLAGS = ("two small United States flags on short wooden poles at the top left and top right corners, and a cheerful cartoon Uncle Sam mascot "
            "pointing forward from the top center")
PT_FLAGS = ("two small Portugal flags on short wooden poles at the top left and top right corners, and a cheerful cartoon Portuguese rooster "
            "(Galo de Barcelos) mascot from the top center")
VOICE_PT = ("a warm, bright young woman's voice, a native Brazilian Portuguese speaker, friendly and clear like a language teacher; completely human, "
            "not robotic")
VOICE_EN = ("a warm, bright young woman's voice, a native American English speaker, friendly and clear like a language teacher; completely human, "
            "not robotic")

BANG_PT_EN = """Com licença | Excuse me | /iks-kiúz mi/
Bom dia | Good morning | /gud mór-ning/
Tchau | Goodbye | /gud-bái/
Como você está? | How are you? | /hau ar iú/
Obrigado | Thank you | /ténk iú/
Eu te amo | I love you | /ái lóv iú/
Por favor | Please | /pliiz/
Desculpa | I'm sorry | /áim só-ri/
De nada | You're welcome | /iur uél-kam/
Sem problema | No problem | /nóu prób-lem/
Pratique todos os dias!"""

BANG_EN_PT = """Excuse me | Com licença | /kohn lee-SEN-sah/
Good morning | Bom dia | /bohn DEE-ah/
Goodbye | Adeus | /ah-DAY-oosh/
How are you? | Como está? | /KOH-moo shtah/
Thank you | Obrigado | /oh-bree-GAH-doo/
I love you | Amo-te | /AH-moo-tuh/
Please | Por favor | /poor fah-VOR/
I'm sorry | Desculpe | /dish-KOOL-puh/
You're welcome | De nada | /duh NAH-duh/
No problem | Sem problema | /sayn proo-BLAY-muh/
Practice every day!"""

BASE = {"TEN_DAY": "the robot tutor", "NGUOI_DAY": ROBOT, "GIONG_DAY": VOICE_PT, "DAO_NGHI": "lips closed in a soft smile, head upright, eyes on the lens",
        "NEN": CAFE, "NGON_NGU_ME": "Brazilian Portuguese", "NGON_NGU_HOC": "American English", "CO": US_FLAGS, "BANG_TU": BANG_PT_EN}
VARIANTS = [
    dict(BASE, name="ai-tutor-pt-hoc-anh"),
    dict(BASE, name="ai-tutor-pt-hoc-anh-nen-lisbon", NEN=LISBON),
    dict(BASE, name="ai-tutor-anh-hoc-bdn", GIONG_DAY=VOICE_EN, NGON_NGU_ME="American English", NGON_NGU_HOC="European Portuguese", CO=PT_FLAGS,
         BANG_TU=BANG_EN_PT, NGUOI_DAY=ROBOT.replace("a red and green Portugal football jersey with the number 7", "a simple white polo shirt with a small Portugal flag badge")),
    dict(BASE, name="ai-tutor-pt-hoc-anh-robot-moi", NGUOI_DAY=ROBOT_2),
]

for v in VARIANTS:
    v["LUOT"] = turns(v["BANG_TU"])
n = max(len(v["LUOT"]) for v in VARIANTS)
assert all(len(v["LUOT"]) == n for v in VARIANTS), "mọi biến thể phải có cùng số cảnh"
open(os.path.join(OUT, "KICH-BAN-AI-TUTOR-NGOI-DOC.txt"), "w", encoding="utf-8").write(script(n))
json.dump(VARIANTS, open(os.path.join(OUT, "BIEN-THE-AI-TUTOR-NGOI-DOC.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok:", n, "cảnh,", len(VARIANTS), "biến thể")
