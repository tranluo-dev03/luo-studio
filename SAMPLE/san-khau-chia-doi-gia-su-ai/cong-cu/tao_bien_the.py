"""Sinh SAMPLE/san-khau-chia-doi-gia-su-ai/BIEN-THE-SAN-KHAU-CHIA-DOI-GIA-SU-AI.json.
Sửa bảng BIEN_THE (tên, ngoại hình EN, giọng EN, ảnh) / VONG (5 cặp câu tiếng Bồ → tiếng Anh + phiên âm) / hàm luot() rồi chạy:
    .venv\\Scripts\\python.exe SAMPLE\\san-khau-chia-doi-gia-su-ai\\cong-cu\\tao_bien_the.py
Biến thể 01 bám sát video mẫu "Lurnia_ Learn Language with AI" (lời đã đối chiếu Whisper pt+en với phụ đề trên hình; app trong video là YayTalk).
Ảnh tham chiếu: CHỈ ảnh AI do người dùng cung cấp (link hoặc tệp trong anh/), KHÔNG cắt từ video mẫu. Ảnh chưa có thì bỏ khỏi refs và in cảnh báo."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "BIEN-THE-SAN-KHAU-CHIA-DOI-GIA-SU-AI.json")
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
ANH = "SAMPLE/san-khau-chia-doi-gia-su-ai/anh/"

APP = "Talka AI"   # tên ứng dụng nói trong lượt 4 (đổi ở đây nếu làm cho app khác)

# Robot gia sư AI trong video mẫu: robot trắng bạc mũ lưỡi trai xám, kính đen, áo khoác bomber đen-xám, tay cơ khí; đứng ngoài công viên.
ROBOT = ("a sleek humanoid robot with a smooth white porcelain face, black wraparound sunglasses, a grey baseball cap on its bald head, a black-and-dark-grey "
         "zip-up bomber jacket with ribbed collar and cuffs worn open over glossy white hexagonal chest armour with thin glowing cyan seams, a black mechanical neck of "
         "bundled cables, white and black segmented mechanical hands; its soft porcelain lips open and move naturally with every word whenever the robot itself speaks")
GIONG_DAY = ("a deep calm male synthetic voice around 95–120 Hz with a light robotic sheen, natural Brazilian Portuguese accent, patient and clear like a "
             "kind language tutor; speaks English words with a clean neutral American accent")
NEN_DAY = ("a sunny city park: green trees with soft sunlight filtering through, a dark wooden railing the robot rests one forearm on, a faint blurred path "
           "and lamp post, all softly out of focus")
NEN_HOC2 = "a deep navy-blue stage curtain with soft vertical folds, plain dark and softly lit, nothing else"
NEN_HOC1 = ("a dark conference stage: a deep navy-blue curtain backdrop, a round glossy red stage carpet at his feet, a few huge glowing red abstract 3D block "
            "shapes (no letters, no words) behind him on the left and right, and the dark out-of-focus silhouettes of an audience along the bottom edge")
DAO_HOC = ("a small black presentation clicker held loosely in the right hand low at the waist, and a thin black headset microphone along the left cheek")
DAO_DIENTHOAI = ("a modern smartphone whose screen shows only a portrait of a sleek white humanoid robot (smooth white porcelain face with light-blue eyes, bald white head, white armour plates with thin glowing cyan seams) on a soft light-white background, filling the screen, no text, no letters, no UI")

# (tên biến thể, TEN_HOC, ngoại hình EN, giọng EN, ảnh nhân vật hoặc None, ảnh robot hoặc None)
BIEN_THE = [
    ("bien-the-01-dien-gia-goc", "Rafael",
     "a charismatic Brazilian man in his late fifties, a tanned face with warm laugh lines, swept-back silver-grey hair, a neat short grey beard, warm "
     "brown eyes and a confident smile; a cream linen blazer over a white open-collar shirt, beige chinos and a brown leather belt",
     "a real Brazilian man in his late fifties, natural mid pitch around 140–160 Hz, warm, confident and charismatic like a conference speaker, native "
     "Brazilian Portuguese; speaks English clearly with a light Brazilian accent; a real person, not an actor",
     ANH + "ai-dien-gia.png", ANH + "ai-robot-mu-kinh.png"),
]

# 5 vòng thẻ từ vựng: (câu Bồ trên thẻ, câu Anh, phiên âm hiển thị trên thẻ)
VONG = [
    ("Soa bem", "Sounds good", "/saunz gud/"),
    ("Estou a caminho", "I'm on my way", "/aim on mai wei/"),
    ("Espera um segundo", "Give me a second", "/giv mi a sekənd/"),
    ("Não entendi", "I didn't catch that", "/ai didən kach dat/"),
    ("Aqui está", "Here you go", "/hir yu gou/"),
]


def luot(ten):
    """17 lượt: 7 phần 1 (diễn giả một mình), 10 phần 2 (5 vòng: robot đọc câu Bồ + 'Em inglês, X. Repita comigo.' → diễn giả lặp X MỘT lần)."""
    L = [
        ("hoc", 1, "Nunca, jamais responda “Me too” quando alguém disser “Nice to meet you”.", "decisive, persuasive"),
        ("hoc", 1, "Me too. You’re welcome. I’m fine, thank you.", "doubtful", {"gach": True}),   # cảnh TIỆC: hậu kỳ gạch ngang + dấu X + tiếng sai từng câu
        ("hoc", 1, "Eu também já respondia assim.", "playful, warm"),
        ("hoc", 1, f"Mas aí comecei a praticar com o {APP}.", "upbeat, proud"),
        ("hoc", 1, "Em apenas três semanas, eu já estava falando inglês com fluência e confiança.", "confident, proud"),
        ("hoc", 1, "E é de graça, olha só!", "excited"),
        ("hoc", 1, "Em apenas três semanas, você vai se surpreender com o quanto evoluiu. Como você diria?", "persuasive, curious"),
    ]
    for pt, en, _ in VONG:
        L.append(("day", 2, f"{pt}. Em inglês, {en}. Repita comigo.", "helpful, friendly"))
        L.append(("hoc", 2, f"{en}.", "cheerful, confident"))   # NÓI ĐÚNG MỘT LẦN: viết hai lần thì Muse nói hai lần ("Sounds good! Sounds good!", 16/11/2026)
    out = []
    for who, phan, text, emo, *ex in L:
        d = {"who": who, "text": text, "emo": emo, "fx": "none", "phan": phan}
        d.update(ex[0] if ex else {})
        out.append(d)
    return out


def hau_ky():
    """Thẻ từ vựng phần 2: lượt robot (luot) + lượt diễn giả lặp (luot_hoc), chỉ số 0-based trong LUOT (phần 1 có 7 lượt)."""
    the = []
    for k, (pt, en, ipa) in enumerate(VONG):
        the.append({"luot": 7 + 2 * k, "luot_hoc": 8 + 2 * k, "pt": pt, "en": en, "ipa": ipa})
    return {"ngon_ngu": "pt", "the": the}


def _refs(m, name):
    out = {}
    for k, x in m.items():
        if not x:
            continue
        if x.startswith("http") or os.path.isfile(os.path.join(ROOT, x)):
            out[k] = [x]
        else:
            print(f"CẢNH BÁO [{name}] {k}: chưa có ảnh {x} (chờ ảnh AI của người dùng), bỏ khỏi refs")
    return out


def main():
    res = []
    for name, ten, ngoai, giong, anh, anh_robot in BIEN_THE:
        v = {
            "name": name,
            "TEN_HOC": ten, "VAI_HOC": "keynote speaker", "NGUOI_HOC": ngoai, "GIONG_HOC": giong,
            "DAO_HOC": DAO_HOC, "DAO_DIENTHOAI": DAO_DIENTHOAI,
            "NEN_HOC": NEN_HOC1, "NEN_HOC2": NEN_HOC2,
            "TEN_DAY": "the AI tutor", "VAI_DAY": "AI robot tutor", "NGUOI_DAY": ROBOT, "GIONG_DAY": GIONG_DAY, "NEN_DAY": NEN_DAY,
            "HE": "he", "HE_C": "He", "HIS": "his", "HIM": "him", "NGON_NGU": "Brazilian Portuguese", "TU_OLHA": "olha só",   # đại từ + ngôn ngữ + từ "xem này": kịch bản dùng token
            "LUOT": luot(ten),
            "HAU_KY": hau_ky(),
        }
        refs = _refs({"NGUOI_HOC": anh, "NGUOI_DAY": anh_robot}, name)
        if refs:
            v["refs"] = refs
        res.append(v)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.normpath(OUT), f"({len(res)} biến thể)")


if __name__ == "__main__":
    main()
