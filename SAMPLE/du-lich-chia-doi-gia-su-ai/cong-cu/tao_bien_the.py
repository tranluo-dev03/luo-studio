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
    "NHIN_ROBOT": "its head turned right toward her, eyes on her face",
    "NGHE_ROBOT": "keeps looking at the woman, its lips sealed in one still closed line from the first frame to the last, hands clasped, head and body perfectly still",
    "NEN_CANH": "the Machu Picchu citadel at golden hour: the steep green Huayna Picchu peak in the centre, grey stone terraces and Inca ruins below, "
                "soft white mist in the valley, distant mountain ridges, a dramatic orange-and-grey cloudy sky",
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


res = []
for name, ten, nguoi, giong, anh, tuoi, que in BIEN_THE:
    v = {"name": name, **CHUNG, "TEN_HOC": ten, "NGUOI_HOC": nguoi, "GIONG_HOC": giong,
         # riêng phần 1 (cảnh thường): vị trí, vai, hướng nhìn, tư thế nghe của Carla
         "POS_HOC@1": "RIGHT", "VAI_HOC@1": "traveller",
         "NHIN_HOC@1": "gazes up at the peak in the centre of the frame with a soft smile",
         "NGHE_HOC@1": "keeps gazing at the peak with the mouth closed, hands in the coat pockets, still",
         "LUOT": luot(ten, tuoi, que),
         "refs": _refs({"NGUOI_ROBOT": ANH_ROBOT_PHAN1, "NGUOI_DAY": ANH_ROBOT_PHAN2, "NGUOI_HOC": anh}, name)}
    res.append(v)
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(res))
