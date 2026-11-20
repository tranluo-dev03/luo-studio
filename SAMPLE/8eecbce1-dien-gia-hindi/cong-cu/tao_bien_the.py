"""Sinh BIEN-THE-8EECBCE1-DIEN-GIA-HINDI.json (kịch bản A, goc) và BIEN-THE-8EECBCE1-DIEN-GIA-HINDI-HOOK.json (kịch bản B, đổi hook).
Mỗi file 1 biến thể mẫu. Thêm biến thể: thêm dòng vào NHAN_VAT (A: đổi nhân vật) hoặc HOOKS (B: đổi hook), chạy lại.
Chạy: python SAMPLE/8eecbce1-dien-gia-hindi/cong-cu/tao_bien_the.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- Nhân vật (kịch bản A đổi các dòng này) ----
NHAN_VAT = [
    {
        "ten": "bien-the-01-goc-nam-50-gile-xam",
        "ma_hoc": "NAM-30-45-IND-04",
        "ma_day": "BOT-TALKA-DEF-INDIA-01",
        "gioi": "nam",
        "NGUOI_HOC": "an Indian man in his late forties with the face, hair and slim build exactly as in the reference photo: a lean face, short greying black hair, a neat salt-and-pepper beard and moustache; for this role he wears a crisp pale-pink dress shirt with buttoned cuffs, a dark charcoal tie, a buttoned grey pinstripe waistcoat and matching grey pinstripe trousers",
        "VAI_HOC": "keynote speaker",
        "GIONG_HOC": "a real Indian man in his late forties, warm mid-low voice around 130–170 Hz that lifts to about 200 Hz on emphasis, confident and charismatic like a seasoned conference speaker, native Hindi; speaks the English words clearly with a light Indian accent; a real person, not an actor",
        "DAO_HOC": "a small black presentation clicker held loosely in the right hand low at the waist, and a thin black headset microphone curving along the right cheek",
        "NEN_HOC": "a dark conference stage: a deep navy-blue curtain backdrop, a round glossy red stage platform with a red ring of light, huge glowing red abstract 3D block shapes (no letters, no words) behind him on the left and right, and the dark out-of-focus heads of an audience along the bottom edge",
        "NEN_HOC2": "a deep navy-blue stage curtain with soft vertical folds and a soft red glow at the sides, plain and dark, nothing else",
        "NGUOI_DAY": "a slim female humanoid robot exactly as in the reference photo: a smooth white porcelain face with calm dark eyes, a bald white head with black mechanical ear modules, a black mechanical neck of bundled cables, white segmented arms with black joints, wearing a bright pink silk saree with a gold border draped over one shoulder and a gold blouse; its soft porcelain lips open and move naturally with every word whenever the robot itself speaks",
        "GIONG_DAY": "a clear, calm female synthetic voice around 200–230 Hz with a light digital sheen, patient and kind like a language tutor; speaks Hindi naturally and the English phrases with a clean neutral American accent",
        "NEN_DAY": "a bright modern study room: soft daylight from a window, a plain light-beige wall and a blurred green plant, all softly out of focus",
    },
]

# ---- Hook (kịch bản B đổi các dòng này; kịch bản A dùng hook gốc) ----
HOOK_GOC = {
    "text": "जब कोई आपसे “Nice to meet you” कहे, तो कभी भी “Me too” मत बोलिए।",
    "emo": "decisive, persuasive",
}
HOOKS = [
    {
        "ten": "bien-the-01-hook-thank-you-for-coming",
        "text": "जब कोई कहे “Thank you for coming”, तो कभी भी “You’re welcome” मत बोलिए।",
        "emo": "decisive, knowing",
        "HOOK_CAM_XUC": "serious and knowing, with a faint amused smile at the corners of the mouth",
        "HOOK_HANH_DONG": "{he} gives one small slow head shake near the start of the line while raising the index finger of {his} right hand (the hand holding the clicker) to chest height, wags it gently once, then lowers the hand to the waist before the last word; the left hand stays low.",
        "HOOK_DIEN_BIEN": "Lắc đầu nhẹ một lần ở đầu câu, cùng lúc giơ ngón trỏ tay phải (tay cầm bút bấm) lên ngang ngực, lắc ngón tay nhẹ một lần, rồi hạ tay về ngang bụng trước từ cuối; tay trái buông.",
        "HOOK_KHUNG_CUOI": "{TEN} nhìn ống kính, nụ cười hiểu chuyện, tay phải đã hạ về ngang bụng cầm bút bấm, tay trái buông, miệng khép.",
    },
]

DAI_TU = {
    "nam": {"HE": "he", "HE_C": "He", "HIS": "his", "HIM": "him"},
    "nu": {"HE": "she", "HE_C": "She", "HIS": "her", "HIM": "her"},
}

PHONE = ("a modern smartphone whose screen shows only a portrait of a friendly white humanoid robot face on a soft light-blue background, "
         "filling the screen, no text, no letters, no UI")

THE = [
    ("ठीक है", "Sounds good", "/saunz gud/"),
    ("मैं रास्ते में हूं", "I'm on my way", "/aim on mai wei/"),
    ("एक सेकंड रुको", "Give me a second", "/giv mi a sekənd/"),
    ("मुझे समझ नहीं आया", "I didn't catch that", "/ai didən kach dat/"),
    ("ये लीजिए", "Here you go", "/hir yu gou/"),
]


def luot(hook, gioi):
    tha = "देता था" if gioi == "nam" else "देती थी"
    laga = "लगा" if gioi == "nam" else "लगी"
    out = [
        {"who": "hoc", "text": hook["text"], "emo": hook["emo"], "fx": "none", "phan": 1},
        {"who": "hoc", "text": "Me too. You’re welcome. I’m fine, thanks.", "emo": "doubtful", "fx": "none", "phan": 1, "gach": True},
        {"who": "hoc", "text": f"पहले मैं भी ऐसे ही जवाब {tha}।", "emo": "playful, warm", "fx": "none", "phan": 1},
        {"who": "hoc", "text": "लेकिन फिर मैंने Talka AI के साथ प्रैक्टिस करना शुरू किया।", "emo": "upbeat, proud", "fx": "none", "phan": 1},
        {"who": "hoc", "text": f"सिर्फ़ तीन हफ़्तों में मैं फ़्लुएंटली और कॉन्फ़िडेंस के साथ इंग्लिश बोलने {laga}।", "emo": "confident, proud", "fx": "none", "phan": 1},
        {"who": "hoc", "text": "और ये बिल्कुल फ़्री है। देखिए!", "emo": "excited", "fx": "none", "phan": 1},
    ]
    for hi, en, _ in THE:
        out.append({"who": "day", "text": f"“{hi}” को इंग्लिश में कैसे बोलेंगे? {en}. मेरे साथ बोलिए: {en}.", "emo": "helpful, friendly", "fx": "none", "phan": 2})
        out.append({"who": "hoc", "text": f"{en}.", "emo": "cheerful, confident", "fx": "none", "phan": 2})
    return out


def bien_the(nv, hook, ten, them=None):
    dt = DAI_TU[nv["gioi"]]
    v = {"name": ten, "TEN_HOC": "the speaker"}
    for k in ("VAI_HOC", "NGUOI_HOC", "GIONG_HOC", "DAO_HOC"):
        v[k] = nv[k]
    v["DAO_DIENTHOAI"] = PHONE
    v["NEN_HOC"] = nv["NEN_HOC"]
    v["NEN_HOC2"] = nv["NEN_HOC2"]
    v.update({"TEN_DAY": "the AI tutor", "VAI_DAY": "AI robot tutor", "NGUOI_DAY": nv["NGUOI_DAY"],
              "GIONG_DAY": nv["GIONG_DAY"], "NEN_DAY": nv["NEN_DAY"], "NGON_NGU": "Hindi"})
    v.update(dt)
    v["TU_OLHA"] = "देखिए"
    if them:
        v.update(them)
    v["HAU_KY"] = {"ngon_ngu": "hi", "the": [
        {"luot": 6 + 2 * i, "luot_hoc": 7 + 2 * i, "pt": hi, "en": en, "ipa": ipa} for i, (hi, en, ipa) in enumerate(THE)]}
    v["LUOT"] = luot(hook, nv["gioi"])
    v["refs"] = {"NGUOI_HOC": nv["ma_hoc"], "NGUOI_DAY": nv["ma_day"]}
    return v


def main():
    a = [bien_the(nv, HOOK_GOC, nv["ten"]) for nv in NHAN_VAT]
    nv = NHAN_VAT[0]
    dt = DAI_TU[nv["gioi"]]
    b = []
    for h in HOOKS:
        them = {
            "HOOK_CAM_XUC": h["HOOK_CAM_XUC"],
            "HOOK_HANH_DONG": h["HOOK_HANH_DONG"].format(he=dt["HE"].capitalize(), his=dt["HIS"]),
            "HOOK_DIEN_BIEN": h["HOOK_DIEN_BIEN"],
            "HOOK_KHUNG_CUOI": h["HOOK_KHUNG_CUOI"].format(TEN="Diễn giả"),
        }
        b.append(bien_the(nv, h, h["ten"], them))
    for name, data in (("BIEN-THE-8EECBCE1-DIEN-GIA-HINDI.json", a), ("BIEN-THE-8EECBCE1-DIEN-GIA-HINDI-HOOK.json", b)):
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Đã ghi", name, len(data), "biến thể")


if __name__ == "__main__":
    main()
