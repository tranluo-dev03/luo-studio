"""Sinh SAMPLE/chia-tren-duoi-marathi/BIEN-THE-CHIA-TREN-DUOI-MARATHI.json từ bảng NHAN_VAT + lời thoại LUOT (theo video mẫu "oder 3.mp4").
Chạy:  .venv\\Scripts\\python.exe SAMPLE\\chia-tren-duoi-marathi\\cong-cu\\tao_bien_the.py
Đổi tên app ở APP (một chỗ). Thêm ảnh tham chiếu ở cột "refs" của từng biến thể (chỉ ảnh AI người dùng cung cấp).
Lời thoại đọc từ phụ đề trên hình của video mẫu; Whisper chỉ dùng lấy mốc giây (nó dịch Marathi sang tiếng Anh, không chép được).
"AI" trong "personal AI teacher" và câu cuối lấy theo lời nghe được: phụ đề cụm lúc đó không lọt vào khung đã xem.
Lời viết cho người học NAM (गेला, कसा, शकतोस, बोललो, करतो): đổi sang nữ phải sửa cả các động từ này (गेली, कशी, शकतेस, बोलले, करते)."""
import json
import os

APP = "Supernova AI"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-CHIA-TREN-DUOI-MARATHI.json")

# who, text, emo. Câu liền nhau của cùng một người được gộp (<= 20 từ).
LUOT = [
    ("day", "काल कुठे गेला होतास?", "friendly, curious"),
    ("hoc", "I go to the market.", "unsure"),
    ("day", "कालची गोष्ट आहे त्यामुळे go नाही went बोल. I went to the market yesterday.", "encouraging"),
    ("hoc", "I went to the market yesterday.", "confident"),
    ("day", "Yesterday तू market मध्ये कसा गेला होतास?", "friendly, curious"),
    ("hoc", "I go by bus.", "unsure"),
    ("day", "Almost बरोबर आहे. पण चांगलं होईल जर तू बोलशील, I went by bus.", "encouraging"),
    ("hoc", "ओह, माझी English खरंच खूप weak आहे.", "embarrassed"),
    ("day", f"काही हरकत नाही. {APP} try केलंस का?", "reassuring"),
    ("hoc", f"{APP}, ते काय आहे?", "curious"),                                                      # video: hai câu ngắn; dấu phẩy để nói liền, không ngắt sau tên app
    ("day", f"{APP} app वर माझ्यासोबत English बोलण्याची practice करु शकतोस. मी तुझी personal AI teacher आहे.", "enthusiastic"),
    ("day", "तू रोज फक्त पंधरा वीस मिनिटं माझ्याशी बोल आणि हळूहळू English बोलण्याचा confidence वाढव.", "warm"),
    ("hoc", "पण माझी English तर खूप weak आहे.", "worried"),
    ("day", "काही हरकत नाही. तुझी English level कशीही असो, मी त्यानुसार तुझ्यासोबत practice करेन.", "reassuring"),
    ("day", "आणि सर्वात चांगली गोष्ट म्हणजे तुला सगळं समजून घेण्यासाठी फक्त English मध्ये बोलण्याची गरज नाही.", "enthusiastic"),
    ("day", "मी तुला मराठीच्या माध्यमातून सुद्धा English समजावून सांगेन.", "warm"),
    ("hoc", "आणि मी चुकीची English बोललो तर?", "worried"),
    ("day", "तर काहीच tension नाही. तू जितक्या वेळा चुकीचं बोलशील, मी तितक्या वेळा तुला योग्य पद्धतीने समजावेन.", "reassuring"),
    ("day", "आणि तुझ्या mistakes correct करेन. तुला कोणी judge करणार सुद्धा नाहीये.", "warm"),
    ("hoc", "मग मी आत्ताच download करतो.", "decisive"),
    ("day", f"योग्य निर्णय. तू खाली दिलेल्या install now button वर click कर आणि {APP} download करून घे.", "enthusiastic"),
]

CHUNG = {
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": "a sleek feminine humanoid robot, exactly as in its reference photo: a smooth glossy white helmet-like head with no hair and a few thin dark panel lines, a smooth white "
                 "porcelain face with soft light-blue eyes and soft lips that open and move like a real person's, small dark ear discs, a black mechanical neck of cables and pistons, glossy "
                 "white hexagonal chest and shoulder plates outlined with thin glowing cyan seams over black mechanical joints",
    "GIONG_DAY": "a bright, warm young woman's voice (around 240-300 Hz) with a clean polished clarity, lively and kind like a favourite teacher, native Marathi",
    "NEN_DAY": "a modern, softly lit home study: tall wooden shelves with warm-lit niches holding books and small vases, vertical wooden slat panels, a tall window on the left "
               "with a soft pale city skyline, a small potted plant and a small glowing table lamp on a desk behind on each side, slightly out of focus",
    "TEN_HOC": "the learner",
    "NEN_HOC": "a modest old Indian room, slightly out of focus, warm dim light: a weathered beige plaster wall, a wooden shelf on the left with stacked steel kitchen tins, a small "
               "framed orange-toned picture with no writing high on the wall behind the head, a dark jacket hanging on a wall peg on the right, worn wooden posts at the far edges",
}

# Biến thể 1 bám sát video mẫu. Biến thể mới: thêm một dòng vào bảng, chỉ đổi đúng thứ được yêu cầu.
NHAN_VAT = [
    {
        "name": "bien-the-01-bam-sat-video",
        "NGUOI_HOC": "an elderly Indian man in his mid-sixties, lean build, weathered dark-brown skin with deep smile lines, short neat white hair, dark eyes, a white moustache and short "
                     "white beard; a worn, faintly stained cream-coloured cotton kurta with a small placket of cloth buttons at the neck; a warm village-elder look",
        "GIONG_HOC": "a real elderly Marathi man's voice in his sixties, warm baritone (around 120-160 Hz), slightly gravelly and unhurried, native Marathi, a beginner's Indian accent on "
                     "the English words; a real person, not an actor",
        "refs": {"NGUOI_DAY": ["SAMPLE/chia-tren-duoi-marathi/anh/robot-ai.webp"], "NGUOI_HOC": ["SAMPLE/chia-tren-duoi-marathi/anh/nguoi-hoc.png"]},
    },
]


def build():
    out = []
    for nv in NHAN_VAT:
        v = {"name": nv["name"]}
        v.update(CHUNG)
        v.update({k: x for k, x in nv.items() if k not in ("name", "refs")})
        v["LUOT"] = [{"who": w, "text": t, "emo": e, "fx": "none"} for w, t, e in LUOT]
        ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
        refs = {k: [p for p in ps if os.path.isfile(os.path.join(ROOT, p))] for k, ps in (nv.get("refs") or {}).items()}   # ảnh chưa gen xong thì chưa gắn
        refs = {k: ps for k, ps in refs.items() if ps}
        if refs:
            v["refs"] = refs
        out.append(v)
    return out


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.abspath(OUT), f"({len(NHAN_VAT)} biến thể, {len(LUOT)} lượt, dài nhất {max(len(t.split()) for _, t, _ in LUOT)} từ)")
