"""Sinh SAMPLE/chia-tren-duoi-bengali/BIEN-THE-CHIA-TREN-DUOI-BENGALI.json từ bảng NHAN_VAT + lời thoại LUOT (theo video mẫu "oder 5.mp4").
Chạy:  runtime\\python.exe SAMPLE\\chia-tren-duoi-bengali\\cong-cu\\tao_bien_the.py
Đổi tên app ở APP (một chỗ). Ảnh tham chiếu ở cột "refs" của từng biến thể: CHỈ ảnh AI người dùng cung cấp (tệp trong anh/ hoặc link), không cắt từ video mẫu.
Lời thoại đọc từ phụ đề trên hình; Whisper chỉ dùng lấy mốc giây (nó dịch tiếng Bengali sang tiếng Anh, không chép được).
Câu liền nhau của cùng một người được gộp khi <= 20 từ. Câu kêu gọi cuối 22 từ nên tách hai lượt."""
import json
import os
import sys

APP = "Supernova AI"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-CHIA-TREN-DUOI-BENGALI.json")

# who, phần, text, emo
LUOT = [
    ("hoc", 1, "ইংলিশ শেখার সবচেয়ে প্রথম rule কি?", "friendly, curious"),
    ("nova", 1, "এটাকে মুখস্থ করবেন না। এটাকে ব্যবহার করুন। আপনাকে শুধু কারো সাথে কথা regularly বলতে হবে।", "warm"),
    ("hoc", 1, "কিন্তু কিভাবে?", "curious"),
    ("nova", 1, f"{APP} এর সাথে। চলুন try করি।", "enthusiastic"),
    ("day", 2, "How old are you?", "friendly, curious"),
    ("hoc", 2, "উম, I have twenty five.", "unsure"),
    ("day", 2, "আপনি বলতে চান, I am twenty five. তাই না?", "encouraging"),
    ("hoc", 2, "হ্যাঁ, একদম। I am twenty five.", "confident"),
    ("day", 2, "Where are you from?", "friendly, curious"),
    ("hoc", 2, "আ, I am Kolkata.", "unsure"),
    ("day", 2, "ভালো চেষ্টা। কিন্তু আপনার বলা উচিত, I am from Kolkata.", "encouraging"),
    ("hoc", 2, "Sorry. আমি প্রায়ই এতে ভুল করে ফেলি। I am from কলকাতা।", "embarrassed"),
    ("day", 2, "কোন ব্যাপার না। AI teacher try করেছেন কি?", "reassuring"),
    ("hoc", 2, "বেশ দামি হবে, তাই না?", "worried"),
    ("day", 2, "একদমই না। Normal English classes থেকে সাত গুণ সস্তা।", "enthusiastic"),
    ("day", 2, "রোজ মাত্র পনের থেকে কুড়ি মিনিট বাংলার সাহায্যে English শিখলে একদম perfect হয়ে যাবেন।", "warm"),
    ("day", 2, "এজন্যই এক কোটিরও বেশি মানুষ Supernova-তে practice করছেন এবং নিজেদের English উন্নত করছেন।", "enthusiastic"),
    ("hoc", 2, "Wow! আমি কিভাবে join করব?", "curious"),
    ("day", 2, f"নিচে install-এর button চাপুন। {APP} app install করুন।", "enthusiastic"),
    ("day", 2, "sign up করুন আর practice শুরু করুন। মাত্র ত্রিশ দিনেই improvement দেখা যাবে।", "warm"),
]

NOVA = ("a sleek feminine humanoid robot, exactly as in its reference photo: a smooth glossy white helmet-like head with no hair and a few thin dark panel lines, a smooth white "
        "porcelain face with soft light-blue eyes and soft lips that open and move like a real person's whenever it speaks, small dark ear discs, a black mechanical neck of cables and "
        "pistons, glossy white hexagonal chest and shoulder plates outlined with thin glowing cyan seams over black mechanical joints")
GIONG_NOVA = "a bright, warm young woman's voice (around 220-330 Hz), clear and lively like a favourite teacher, native Kolkata Bengali, says the English words clearly with a light Indian English accent"

CHUNG = {
    "TEN_NOVA": "Nova", "VAI_NOVA": "AI English tutor", "POS_NOVA": "LEFT",
    "NGUOI_NOVA": NOVA, "GIONG_NOVA": GIONG_NOVA,
    "NHIN_NOVA": "looks only at the man's face, straight across to the right in exact side profile",
    "NGHE_NOVA": "keeps a gentle closed-mouth smile, the lips pressed together, the eyes on the man's face, in exact side profile",
    "NEN_NOVA": "a plain seamless studio backdrop of soft blurred grey tones with faint pale marbled ripple patterns, with no objects and no horizon",
    "VAI_HOC": "young man", "POS_HOC": "RIGHT",
    "NHIN_HOC": "looks only at Nova's face, straight across to the left in exact side profile, and never looks at the camera",
    "NGHE_HOC": "stays calm with the lips pressed together, the eyes on Nova's face, in exact side profile, and never looks at the camera",
    "TEN_DAY": "Nova", "NGUOI_DAY": NOVA, "GIONG_DAY": GIONG_NOVA,
    "NEN_DAY": "a cosy living room in warm lamplight, slightly out of focus: a wide taupe sofa with a grey-green cushion and a striped rolled armrest on the right, a tall wooden bookcase with books "
               "behind on the left, a lit cream table lamp and a white mug on a side table at the left, long beige curtains and a bright window at the upper right",
    "TEN_HOC": "the young man",
    "NEN_HOC": "a bright, tidy Bengali home, slightly out of focus: a cream wall, a wooden shelf full of colourful books on the left with small plain framed family photos on top, a large leafy potted "
               "plant on a shelf on the right, a smaller potted plant low on the left, sheer white curtains and soft daylight at the right, the back of a beige sofa behind him",
}

# Biến thể 1 bám sát video mẫu. Biến thể mới: thêm một dòng vào bảng, chỉ đổi đúng thứ được yêu cầu.
ANH = "SAMPLE/chia-tren-duoi-bengali/anh/"
NHAN_VAT = [
    {
        "name": "bien-the-01-bam-sat-video",
        "NGUOI_HOC": "a young Bengali man about twenty-five years old, warm brown skin, short neat black hair with faded sides and volume on top, a trimmed short beard and moustache, dark kind eyes; "
                     "a cream-white cotton kurta with a fine maroon and gold embroidered collar and placket; photorealistic skin and fabric",
        "GIONG_HOC": "a real young Bengali man's voice, light baritone (around 130-170 Hz), plain and friendly, native Kolkata Bengali, says the English words like a beginner, a little slowly; "
                     "a real person, not an actor",
        "refs": {"NGUOI_NOVA": [ANH + "nova.png"], "NGUOI_DAY": [ANH + "nova.png"], "NGUOI_HOC": [ANH + "nguoi-hoc.png"]},
    },
]

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")


def build():
    out = []
    for nv in NHAN_VAT:
        v = {"name": nv["name"]}
        v.update(CHUNG)
        v.update({k: x for k, x in nv.items() if k not in ("name", "refs")})
        v["LUOT"] = [{"who": w, "text": t, "emo": e, "fx": "none", "phan": p} for w, p, t, e in LUOT]
        refs = {}
        for k, ps in (nv.get("refs") or {}).items():
            ok = [p for p in ps if p.startswith("http") or os.path.isfile(os.path.join(ROOT, p))]
            if ok:
                refs[k] = ok
            else:
                print(f"CẢNH BÁO [{nv['name']}] {k}: chưa có ảnh {ps} (chờ ảnh AI của người dùng, chưa được gen)")
        if refs:
            v["refs"] = refs
        out.append(v)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.abspath(OUT), f"({len(NHAN_VAT)} biến thể, {len(LUOT)} lượt, dài nhất {max(len(t.split()) for _, _, t, _ in LUOT)} từ)")
