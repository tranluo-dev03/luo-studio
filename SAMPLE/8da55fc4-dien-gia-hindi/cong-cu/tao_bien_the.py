"""Sinh BIEN-THE-8DA55FC4-DIEN-GIA-HINDI.json (kịch bản A, goc) và BIEN-THE-8DA55FC4-DIEN-GIA-HINDI-HOOK.json (kịch bản B, đổi hook).
Mỗi file 1 biến thể mẫu. Thêm biến thể: thêm dòng vào NHAN_VAT (A: đổi nhân vật) hoặc HOOKS (B: đổi hook), chạy lại. Không sửa tay JSON.
Chạy: python SAMPLE/8da55fc4-dien-gia-hindi/cong-cu/tao_bien_the.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- Nhân vật (kịch bản A đổi các dòng này: nghề, giới, tuổi, phong cách) ----
# ma_hoc: mã KHO NHÂN VẬT (SAMPLE/_chung/kho-nhan-vat). NGUOI_HOC: mặt/tóc/dáng THEO ẢNH kho + trang phục của vai.
NHAN_VAT = [
    {
        "ten": "bien-the-01-goc-nam-50-gile-xam",
        "ma_hoc": "NAM-30-45-IND-10",
        "gioi": "nam",
        "TEN_HOC": "the speaker",
        "VAI_HOC": "keynote speaker",
        "NGUOI_HOC": "an Indian man in his early fifties with the face, hair and slim build exactly as in the reference photo: a lean, lined face with deep-set dark eyes, grey hair combed straight back, a thick grey-white moustache and a clean-shaven chin; for this role he wears a crisp pale-pink dress shirt with buttoned cuffs, a dark charcoal tie, a buttoned grey pinstripe waistcoat and matching grey pinstripe trousers, polished and successful",
        "GIONG_HOC": "a real Indian man in his early fifties, warm mid-low voice around 130–170 Hz that lifts to about 200 Hz on emphasis, confident and charismatic like a seasoned conference speaker, native Hindi; speaks the English words clearly with a light Indian accent; a real person, not an actor",
        "DAO_HOC": "A thin skin-tone headset microphone curves along {his} right cheek, and a small black presentation clicker rests in {his} right hand.",
        "DAO_LY": "a champagne flute of sparkling wine",
        "NEN_HOC": "a dark TED-style conference stage: a deep navy-blue curtain backdrop, a round glossy red stage platform with a red ring of light, huge glowing red abstract 3D block shapes (no letters, no words) on the left and right, and the dark out-of-focus heads of an audience along the bottom edge",
        "NEN_TIEC": "a grand ballroom with warm golden chandelier lights, tall white floral arrangements, candle-lit tables with champagne glasses and elegant guests far in the background",
    },
]

# ---- Hook (kịch bản A dùng hook gốc; kịch bản B đổi các dòng HOOKS) ----
HOOK_GOC = {
    "text": "जब कोई आपसे “Nice to meet you” कहे, तो कभी भी “Me too” मत बोलिए।",
    "emo": "decisive, persuasive",
}
HOOKS = [
    {
        # Insight tình huống 2 (hành lang công ty): "How's it going?" → đáp như trả bài "I'm fine, thank you".
        "ten": "bien-the-01-hook-hows-it-going",
        "text": "जब कोई पूछे “How’s it going?”, तो कभी भी “I’m fine, thank you” मत बोलिए।",
        "emo": "decisive, knowing",
        "HOOK_CAM_XUC": "knowing and a little teasing, eyebrows raised, a faint amused smile at the corners of the mouth",
        "HOOK_HANH_DONG": "near the start of the line {he} tilts {his} head slightly and lifts {his} right hand (the hand holding the clicker) to chest height with the palm half open, as if asking a question; in the second half of the line {he} gives one small slow head shake and lowers the hand to the waist before the last word; the left hand stays low.",
        "HOOK_DIEN_BIEN": "Đầu câu nghiêng đầu nhẹ, nhướng mày, tay phải (cầm bút bấm) đưa lên ngang ngực, lòng bàn tay hé mở như đang hỏi; nửa sau câu lắc đầu chậm một lần và hạ tay về ngang bụng trước từ cuối; tay trái buông.",
        "HOOK_KHUNG_CUOI": "{TEN} nhìn ống kính, nụ cười hiểu chuyện, tay phải đã hạ về ngang bụng cầm bút bấm, tay trái buông, miệng khép.",
    },
]

DAI_TU = {
    "nam": {"HE": "he", "HE_C": "He", "HIS": "his", "HIM": "him"},
    "nu": {"HE": "she", "HE_C": "She", "HIS": "her", "HIM": "her"},
}

PHONE = ("a modern smartphone whose screen shows only a portrait of a friendly white humanoid robot face on a soft light-blue background, "
         "filling the screen, no text, no letters, no app interface")


def luot(hook, gioi):
    tha = "देता था" if gioi == "nam" else "देती थी"
    laga = "लगा" if gioi == "nam" else "लगी"
    return [
        {"who": "hoc", "text": hook["text"], "emo": hook["emo"], "fx": "none", "phan": 1},
        {"who": "hoc", "text": "Me too. You’re welcome. I’m fine, thanks.", "emo": "doubtful", "fx": "none", "phan": 1, "gach": True},
        {"who": "hoc", "text": f"पहले मैं भी ऐसे ही जवाब {tha}।", "emo": "playful, warm", "fx": "none", "phan": 1},
        {"who": "hoc", "text": "लेकिन फिर मैंने Talka AI के साथ प्रैक्टिस करना शुरू किया।", "emo": "upbeat, proud", "fx": "none", "phan": 1},
        {"who": "hoc", "text": f"सिर्फ़ तीन हफ़्तों में मैं फ़्लुएंटली और कॉन्फ़िडेंस के साथ इंग्लिश बोलने {laga}।", "emo": "confident, proud", "fx": "none", "phan": 1},
        {"who": "hoc", "text": "और ये बिल्कुल फ़्री है। देखिए!", "emo": "excited", "fx": "none", "phan": 1},
    ]


def bien_the(nv, hook, ten, them=None):
    dt = DAI_TU[nv["gioi"]]
    v = {"name": ten}
    for k in ("TEN_HOC", "VAI_HOC", "NGUOI_HOC", "GIONG_HOC", "DAO_LY", "NEN_HOC", "NEN_TIEC"):
        v[k] = nv[k]
    v["DAO_HOC"] = nv["DAO_HOC"].format(his=dt["HIS"])
    v["DAO_DIENTHOAI"] = PHONE
    v["NGON_NGU"] = "Hindi"
    v["TU_OLHA"] = "देखिए"
    v.update(dt)
    if them:
        v.update(them)
    v["HAU_KY"] = {"ngon_ngu": "hi"}
    v["LUOT"] = luot(hook, nv["gioi"])
    v["refs"] = {"NGUOI_HOC": nv["ma_hoc"]}
    return v


def main():
    a = [bien_the(nv, HOOK_GOC, nv["ten"]) for nv in NHAN_VAT]
    nv = NHAN_VAT[0]
    dt = DAI_TU[nv["gioi"]]
    b = []
    for h in HOOKS:
        them = {
            "HOOK_CAM_XUC": h["HOOK_CAM_XUC"],
            "HOOK_HANH_DONG": h["HOOK_HANH_DONG"].format(he=dt["HE"], his=dt["HIS"]),
            "HOOK_DIEN_BIEN": h["HOOK_DIEN_BIEN"],
            "HOOK_KHUNG_CUOI": h["HOOK_KHUNG_CUOI"].format(TEN="Diễn giả"),
        }
        b.append(bien_the(nv, h, h["ten"], them))
    for name, data in (("BIEN-THE-8DA55FC4-DIEN-GIA-HINDI.json", a), ("BIEN-THE-8DA55FC4-DIEN-GIA-HINDI-HOOK.json", b)):
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Đã ghi", name, len(data), "biến thể")


if __name__ == "__main__":
    main()
