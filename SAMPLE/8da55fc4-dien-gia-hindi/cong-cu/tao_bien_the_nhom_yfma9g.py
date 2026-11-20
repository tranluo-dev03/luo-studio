"""Nhóm yfma9g (kịch bản A, goc): đổi BỘ BÀI HỌC (lời hook + 3 câu sách vở bị gạch ở cảnh tiệc) và đổi nhân vật.
Người dùng: "1 bản = 2 video = 1 nam + 1 nữ", 11 bộ bài học, 20 mã nhân vật (10 nữ + 10 nam India); nhóm này đặt đúng 10 biến thể
→ 10 bộ bài học ĐẦU TIÊN, mỗi bộ một biến thể, giới xen kẽ nữ/nam (5 nữ + 5 nam), mã bốc ngẫu nhiên (seed cố định) trong danh sách người dùng gửi,
mỗi biến thể một mã khác nhau. Muốn đủ cặp nam+nữ cho mọi bộ: chạy với --day-du (ghi file -DAY-DU, 22 biến thể; cần thêm 2 mã ngoài danh sách nếu dùng mã không lặp).
Tên "Priya"/"Rahul" và tuổi trong câu sai đổi theo nhân vật. Mọi biến thể giữ đủ bộ token như biến thể mẫu.
Chạy: python SAMPLE/8da55fc4-dien-gia-hindi/cong-cu/tao_bien_the_nhom_yfma9g.py"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tao_bien_the as M  # noqa: E402  (DAI_TU, PHONE, NHAN_VAT mẫu)

NHOM = "yfma9g"
MAU = M.NHAN_VAT[0]

# ---- 11 bộ bài học (người dùng gửi). {ten} = tên nhân vật, {tuoi} = tuổi ----
BAI = [
    ("how-are-you", "जब कोई आपसे “How are you?” कहे, तो कभी भी “I’m fine, thank you, and you?” मत बोलिए।",
     ["I’m fine, thank you, and you?", "I am fine only.", "Fine."]),
    ("whats-your-name", "जब कोई आपसे “What’s your name?” कहे, तो कभी भी “Myself {ten}” मत बोलिए।",
     ["Myself {ten}.", "My good name is {ten}.", "{ten} is my name."]),
    ("where-from", "जब कोई आपसे “Where are you from?” कहे, तो कभी भी “I belong to Delhi” मत बोलिए।",
     ["I belong to Delhi.", "I am coming from Delhi.", "My native is Delhi."]),
    ("what-do-you-do", "जब कोई आपसे “What do you do?” कहे, तो कभी भी “I am doing job” मत बोलिए।",
     ["I am doing job.", "I am working in bank since 5 years.", "I am in service."]),
    ("any-questions", "जब कोई आपसे “Any questions?” कहे, तो कभी भी “I have a doubt” मत बोलिए।",
     ["I have a doubt.", "One doubt is there.", "I am having doubt."]),
    ("mind-if-i-sit", "जब कोई आपसे “Do you mind if I sit here?” कहे, तो कभी भी “Yes” मत बोलिए।",
     ["Yes.", "Yes, please sit.", "Yes, no problem."]),
    ("some-coffee", "जब कोई आपसे “Would you like some coffee?” कहे, तो कभी भी “No” मत बोलिए।",
     ["No.", "I don’t want.", "No need."]),
    ("how-old", "जब कोई आपसे “How old are you?” कहे, तो कभी भी “My age is {tuoi}” मत बोलिए।",
     ["My age is {tuoi}.", "I am {tuoi} years.", "I am having {tuoi} years."]),
    ("can-you-help", "जब कोई आपसे “Can you help me?” कहे, तो कभी भी “What you want?” मत बोलिए।",
     ["What you want?", "Yes, tell me.", "Tell."]),
    ("happy-birthday", "जब कोई आपसे “Happy birthday!” कहे, तो कभी भी “Thanks, you too” मत बोलिए।",
     ["Thanks, you too.", "Same to you.", "Wish you the same."]),
    ("eat-meat", "जब कोई आपसे “Do you eat meat?” कहे, तो कभी भी “I am pure veg” मत बोलिए।",
     ["I am pure veg.", "I don’t take non-veg.", "I am non-veg."]),
]

# ---- 20 mã người dùng gửi; mặt/tóc/dáng viết THEO ẢNH kho ----
NGUOI = {
    "NU-20-30-IND-01": "a slim Indian woman in her mid twenties with the face, hair and build exactly as in the reference photo: an oval face, large dark eyes, long wavy black hair tied back loosely in a low ponytail",
    "NU-20-30-IND-02": "a full-figured Indian woman in her late twenties with the face, hair and build exactly as in the reference photo: a round soft face, dark eyes, black hair pulled back into a neat low bun",
    "NU-20-30-IND-03": "a slim Indian woman in her early twenties with the face, hair and build exactly as in the reference photo: a narrow oval face, dark eyes, very long straight black hair in a single braid over one shoulder",
    "NU-20-30-IND-04": "an Indian woman in her late twenties of medium build with the face, hair and build exactly as in the reference photo: a round face, dark eyes, black hair pulled back into a low ponytail",
    "NU-20-30-IND-05": "a sturdy Indian woman in her late twenties with the face, hair and build exactly as in the reference photo: a round face, dark eyes, short curly black hair",
    "NU-30-45-IND-06": "a slim Indian woman in her late thirties with the face, hair and build exactly as in the reference photo: an oval face with a gentle expression, dark eyes, black hair pulled back into a low ponytail",
    "NU-30-45-IND-07": "a slim Indian woman in her mid forties with the face, hair and build exactly as in the reference photo: a long lined face, dark eyes, black hair pulled back into a low bun",
    "NU-30-45-IND-08": "a full-figured Indian woman in her early forties with the face, hair and build exactly as in the reference photo: a round face, dark eyes, wavy black hair tied back loosely at the nape",
    "NU-30-45-IND-09": "an Indian woman in her early forties of medium build with the face, hair and build exactly as in the reference photo: an angular face with high cheekbones, dark eyes, black hair tied back tightly",
    "NU-30-45-IND-10": "a sturdy Indian woman in her mid forties with the face, hair and build exactly as in the reference photo: a round mature face, dark eyes, long black hair in a thick braid over one shoulder",
    "NAM-20-30-IND-01": "a young Indian man in his early twenties of medium build with the face, hair and build exactly as in the reference photo: a round youthful clean-shaven face, dark eyes, short neat black hair",
    "NAM-20-30-IND-02": "a slim Indian man in his late twenties with the face, hair and build exactly as in the reference photo: a lean face, a thick black moustache, wavy black hair swept back",
    "NAM-20-30-IND-03": "a slim young Indian man in his early twenties with the face, hair and build exactly as in the reference photo: a narrow clean-shaven face, wide dark eyes, short curly black hair",
    "NAM-20-30-IND-04": "a heavy-set Indian man around thirty with the face, hair and build exactly as in the reference photo: a broad round face, a thick black moustache, short black hair parted to the side",
    "NAM-20-30-IND-05": "a tall, very slim Indian man in his mid twenties with the face, hair and build exactly as in the reference photo: a narrow clean-shaven face, wavy black hair",
    "NAM-30-45-IND-06": "a stocky Indian man in his mid thirties with the face, hair and build exactly as in the reference photo: a full trimmed black beard and moustache, short black hair",
    "NAM-30-45-IND-07": "a heavy-set Indian man in his mid forties with the face, hair and build exactly as in the reference photo: a broad lined face, a thick black moustache, short black hair greying at the temples",
    "NAM-30-45-IND-08": "an Indian man in his mid thirties of medium build with the face, hair and build exactly as in the reference photo: an oval face, a thin black moustache, short black hair parted to the side",
    "NAM-30-45-IND-09": "a slim Indian man in his late thirties with the face, hair and build exactly as in the reference photo: a lean clean-shaven face, short curly black hair",
    "NAM-30-45-IND-10": "a slim Indian man in his early fifties with the face, hair and build exactly as in the reference photo: a lean lined face, grey hair combed straight back, a thick grey-white moustache",
}

# ---- Trang phục vai (insight: chỉn chu, thành đạt) ----
DO_NU = [
    "for this role she wears an elegant ivory silk saree with a wide gold border, a matching gold blouse, a small red bindi and small gold earrings",
    "for this role she wears a tailored navy blazer over a white silk blouse with a knee-length navy pencil skirt, a small bindi and a thin gold chain",
    "for this role she wears an embroidered deep-teal anarkali kurta with fine gold threadwork and a sheer dupatta pinned on one shoulder, a small bindi and gold stud earrings",
    "for this role she wears a sharp white trouser suit with a soft cream blouse, a small bindi and small gold hoop earrings",
    "for this role she wears a fitted maroon trouser suit over a blush silk blouse, a small bindi and a slim gold watch",
    "for this role she wears a long straight beige silk kurta under a structured charcoal blazer with slim trousers, a small bindi and gold studs",
]
DO_NAM = [
    "for this role he wears a tailored navy two-piece suit, a crisp white shirt and a burgundy tie",
    "for this role he wears a charcoal three-piece suit, a pale-blue shirt and a dark silver tie",
    "for this role he wears a cream silk kurta with a fitted dark-maroon Nehru jacket and slim trousers",
    "for this role he wears a light-grey blazer over a white open-collar shirt and dark trousers",
    "for this role he wears a dark-green bandhgala jacket with brass buttons and matching trousers",
    "for this role he wears a midnight-blue suit, a white shirt and a slim black tie",
]

GIONG = {
    ("nu", "20-30"): "a real Indian woman in her twenties, bright clear voice around 200–250 Hz, confident and warm like a rising young conference speaker, native Hindi; speaks the English words clearly with a light Indian accent; a real person, not an actor",
    ("nu", "30-45"): "a real Indian woman around forty, warm mid voice around 180–230 Hz that lifts a little on emphasis, poised and charismatic like a seasoned conference speaker, native Hindi; speaks the English words clearly with a light Indian accent; a real person, not an actor",
    ("nam", "20-30"): "a real Indian man in his twenties, clear mid voice around 120–160 Hz that lifts on emphasis, energetic and confident like a young conference speaker, native Hindi; speaks the English words clearly with a light Indian accent; a real person, not an actor",
    ("nam", "30-45"): "a real Indian man around forty, warm mid-low voice around 110–150 Hz that lifts to about 190 Hz on emphasis, confident and charismatic like a seasoned conference speaker, native Hindi; speaks the English words clearly with a light Indian accent; a real person, not an actor",
}

# ---- Bối cảnh bữa tiệc + đồ cầm (đổi theo bài, vẫn là tiệc sang trọng buổi tối) ----
TIEC = [
    ("a grand ballroom with warm golden chandelier lights, tall white floral arrangements, candle-lit tables with glasses and elegant guests far in the background", "a champagne flute of sparkling wine"),
    ("an elegant rooftop terrace party at night with strings of warm fairy lights, a city skyline glowing far behind, lounge tables and well-dressed guests far in the background", "a tall glass of fresh lime soda"),
    ("a luxurious hotel banquet hall with crystal chandeliers, round tables dressed in white linen, tall vases of white roses and guests far in the background", "a stemmed glass of red wine"),
    ("an upscale corporate networking evening in a hotel lounge with warm amber lamps, marble bar counter, potted palms and guests in suits far in the background", "a champagne flute of sparkling wine"),
    ("a glamorous wedding reception lawn at dusk with marigold and white flower garlands, warm lanterns, a decorated stage and guests far in the background", "a tall glass of mango juice"),
]

TUOI = {"20-30": "27", "30-45": "38"}
TEN = {"nu": "Priya", "nam": "Rahul"}


def nhom_tuoi(ma):
    return "20-30" if "-20-30-" in ma else "30-45"


def luot(hook, dong, gioi):
    tha = "देता था" if gioi == "nam" else "देती थी"
    laga = "लगा" if gioi == "nam" else "लगी"
    return [
        {"who": "hoc", "text": hook, "emo": "decisive, persuasive", "fx": "none", "phan": 1},
        {"who": "hoc", "text": " ".join(dong), "emo": "doubtful", "fx": "none", "phan": 1, "gach": True},
        {"who": "hoc", "text": f"पहले मैं भी ऐसे ही जवाब {tha}।", "emo": "playful, warm", "fx": "none", "phan": 1},
        {"who": "hoc", "text": "लेकिन फिर मैंने Talka AI के साथ प्रैक्टिस करना शुरू किया।", "emo": "upbeat, proud", "fx": "none", "phan": 1},
        {"who": "hoc", "text": f"सिर्फ़ तीन हफ़्तों में मैं फ़्लुएंटली और कॉन्फ़िडेंस के साथ इंग्लिश बोलने {laga}।", "emo": "confident, proud", "fx": "none", "phan": 1},
        {"who": "hoc", "text": "और ये बिल्कुल फ़्री है। देखिए!", "emo": "excited", "fx": "none", "phan": 1},
    ]


def bien_the(k, bai, ma):
    gioi = "nu" if ma.startswith("NU-") else "nam"
    nt = nhom_tuoi(ma)
    dt = M.DAI_TU[gioi]
    slug, hook, dong = bai
    f = {"ten": TEN[gioi], "tuoi": TUOI[nt]}
    do = (DO_NU if gioi == "nu" else DO_NAM)[k % 6]
    nen_tiec, ly = TIEC[k % len(TIEC)]
    v = {"name": f"{NHOM}-{k + 1:02d}-{slug}-{gioi}{ma.split('-')[1]}-{ma.split('-')[-1]}"}
    v.update({
        "TEN_HOC": "the speaker",
        "VAI_HOC": "keynote speaker",
        "NGUOI_HOC": f"{NGUOI[ma]}; {do}, polished and successful",
        "GIONG_HOC": GIONG[(gioi, nt)],
        "DAO_LY": ly,
        "NEN_HOC": MAU["NEN_HOC"],
        "NEN_TIEC": nen_tiec,
        "DAO_HOC": MAU["DAO_HOC"].format(his=dt["HIS"]),
        "DAO_DIENTHOAI": M.PHONE,
        "NGON_NGU": "Hindi",
        "TU_OLHA": "देखिए",
    })
    v.update(dt)
    v["HAU_KY"] = {"ngon_ngu": "hi"}
    v["LUOT"] = luot(hook.format(**f), [d.format(**f) for d in dong], gioi)
    v["refs"] = {"NGUOI_HOC": ma}
    return v


def chon_ma(n_nu, n_nam, seed=NHOM):
    r = random.Random(seed)
    nu = [m for m in NGUOI if m.startswith("NU-")]
    nam = [m for m in NGUOI if m.startswith("NAM-")]
    return r.sample(nu, n_nu), r.sample(nam, n_nam)


def main():
    day_du = "--day-du" in sys.argv
    if day_du:   # 11 bài × (nữ + nam): 22 biến thể, mã quay vòng
        nu, nam = chon_ma(10, 10)
        out = []
        for k, bai in enumerate(BAI):
            out.append(bien_the(2 * k, bai, nu[k % 10]))
            out.append(bien_the(2 * k + 1, bai, nam[k % 10]))
        name = f"BIEN-THE-NHOM-{NHOM}-DAY-DU.json"
    else:        # 10 bài đầu, giới xen kẽ nữ/nam
        nu, nam = chon_ma(5, 5)
        out = []
        for k, bai in enumerate(BAI[:10]):
            ma = nu[k // 2] if k % 2 == 0 else nam[k // 2]
            out.append(bien_the(k, bai, ma))
        name = f"BIEN-THE-NHOM-{NHOM}.json"
    names = [v["name"] for v in out]
    assert len(set(names)) == len(names)
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("Đã ghi", name, len(out), "biến thể")
    for v in out:
        print(" ", v["name"], v["refs"]["NGUOI_HOC"], "|", v["LUOT"][1]["text"])


if __name__ == "__main__":
    main()
