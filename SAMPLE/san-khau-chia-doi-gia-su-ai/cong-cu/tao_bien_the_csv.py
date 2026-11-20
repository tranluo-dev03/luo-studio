"""Sinh 4 file biến thể từ 4 CSV của người dùng (X0056–X0059) vào SAMPLE/san-khau-chia-doi-gia-su-ai/.
    python tai_anh_csv.py          # tải ảnh Drive về anh/<bo>/ (một lần)
    python tao_bien_the_csv.py     # ghi 4 file BIEN-THE-*.json
Bộ brazil / brazil-robot dùng kịch bản 7 cảnh (lời Bồ, như video mẫu); bộ hindi / mexico dùng kịch bản 6 cảnh (lời lấy từ CSV, bỏ cảnh 7).
Mô tả nhân vật = giới + quốc tịch + tuổi (từ CSV) + "đúng như ảnh tham chiếu" (ảnh phông xanh toàn thân; mặt/tóc/trang phục lấy từ ảnh)."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tao_bien_the as T  # noqa: E402
import tai_anh_csv as D  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, ".."))
REL = "SAMPLE/san-khau-chia-doi-gia-su-ai/anh/"

ROBOT_CSV = ("a sleek humanoid robot with a smooth white porcelain face with light-blue eyes, a bald white head, a black mechanical neck of bundled cables, "
             "glossy white hexagonal chest armour with thin glowing cyan seams and white and black segmented mechanical hands, wearing exactly the outfit shown in the reference photo; "
             "its soft porcelain lips open and move naturally with every word whenever the robot itself speaks")

BO = {
    "brazil": dict(file="BIEN-THE-X0056-X0070-BRAZIL-40.json", nat="Brazilian", lang="pt", ngon="Brazilian Portuguese", tu_olha="olha só"),
    "brazil-robot": dict(file="BIEN-THE-X0058-X0072-BRAZIL-ROBOT-40.json", nat="Brazilian", lang="pt", ngon="Brazilian Portuguese", tu_olha="olha só", robot=True),
    "hindi": dict(file="BIEN-THE-X0057-X0071-HINDI-20.json", nat="Indian", lang="hi", ngon="Hindi", tu_olha="देखिए"),
    "mexico": dict(file="BIEN-THE-X0059-X0073-MEXICO-40.json", nat="Mexican", lang="es", ngon="Mexican Spanish", tu_olha="Mira"),
    # X0104: nhân vật Ấn Độ nói tiếng Ả Rập; X0105: cùng 20 nhân vật, lời Hindi. Cả hai: điện thoại ở cảnh 6 hiện robot AI của người dùng (nhân vật phụ DT: ảnh tham chiếu NGUOI_DT, Muse vẽ ngay lúc gen, KHÔNG đè hình ở hậu kỳ).
    "arab": dict(file="BIEN-THE-X0104-ARAB-20.json", nat="Indian", lang="ar", ngon="Arabic", tu_olha="إليك الطريقة", dt=True, ma="X0104", ten="Arabic", stt0=0),
    "hindi2": dict(file="BIEN-THE-X0105-HINDI-20.json", nat="Indian", lang="hi", ngon="Hindi", tu_olha="देखिए", dt=True, ma="X0105", ten="Hindi", stt0=0),
}

# Điện thoại cầm trong cảnh 6: màn hình = robot AI của người dùng (ảnh nền xanh dương) + chữ "Talka AI". Robot đi vào cảnh như một "nhân vật" DT
# (TEN_DT / NGUOI_DT / refs.NGUOI_DT) để engine gửi ảnh kèm lệnh gen video cảnh 6 (video chỉ nhận ảnh của khoá NGUOI_*).
DAO_DT = "a modern smartphone in a slim dark case, its screen lit and facing the lens"
ROBOT_DT = ("a sleek humanoid AI robot shown only as a picture on the phone screen: smooth white porcelain face with calm grey-blue eyes, bald white domed head with "
            "white ear discs, bundled black cables at the neck, white armour shoulder plates, on a saturated royal-blue background")
ANH_ROBOT_DT = "SAMPLE/san-khau-chia-doi-gia-su-ai/anh/robot-talka-dien-thoai.webp"

VONG_AR = [("حسنًا", "Sounds good", "/saunz gud/"), ("أنا في الطريق", "I'm on my way", "/aim on mai wei/"),
           ("لحظة واحدة", "Give me a second", "/giv mi a sekənd/"),
           ("لم أفهم", "I didn't catch that", "/ai didən kach dat/"), ("تفضل", "Here you go", "/hir yu gou/")]

VONG_HI = [("ठीक है", "Sounds good", "/saunz gud/"), ("मैं रास्ते में हूँ", "I'm on my way", "/aim on mai wei/"),
           ("एक सेकंड रुको", "Give me a second", "/giv mi a sekənd/"),
           ("मुझे समझ नहीं आया", "I didn't catch that", "/ai didən kach dat/"), ("ये लीजिए", "Here you go", "/hir yu gou/")]
VONG_ES = [("Suena bien", "Sounds good", "/saunz gud/"), ("Voy en camino", "I'm on my way", "/aim on mai wei/"),
           ("Dame un segundo", "Give me a second", "/giv mi a sekənd/"),
           ("No entendí", "I didn't catch that", "/ai didən kach dat/"), ("Aquí tienes", "Here you go", "/hir yu gou/")]


def luot(lang, nu):
    """Danh sách lượt theo ngôn ngữ. Trả về (LUOT, VONG, số lượt phần 1)."""
    if lang == "pt":
        return T.luot("x"), T.VONG, 7
    if lang == "ar":
        phan1 = [
            ("hoc", 1, "عندما يقول لك أحدهم “Nice to meet you”، لا ترد أبدًا بعبارة “Me too”.", "decisive, persuasive"),
            ("hoc", 1, "Me too. You’re welcome. I’m fine, thanks.", "doubtful", {"gach": True}),
            ("hoc", 1, "في السابق، كانت هذه إجاباتي أيضًا.", "playful, warm"),
            ("hoc", 1, f"لكن بعد ذلك، بدأت أتدرب مع {T.APP}.", "upbeat, proud"),
            ("hoc", 1, "خلال ثلاثة أسابيع فقط، أصبحت أتحدث الإنجليزية بطلاقة وثقة.", "confident, proud"),
            ("hoc", 1, "وكل هذا مجانًا تمامًا. إليك الطريقة!", "excited"),
        ]
        vong = VONG_AR

        def rnd(pt, en):
            return f"كيف نقول «{pt}» باللغة الإنجليزية؟ {en}. لنرددها معًا: {en}."
    elif lang == "hi":
        phan1 = [
            ("hoc", 1, "जब कोई आपसे “Nice to meet you” कहे, तो कभी भी “Me too” मत बोलिए।", "decisive, persuasive"),
            ("hoc", 1, "Me too. You’re welcome. I’m fine, thanks.", "doubtful", {"gach": True}),
            ("hoc", 1, "पहले मैं भी ऐसे ही जवाब " + ("देती थी।" if nu else "देता था।"), "playful, warm"),
            ("hoc", 1, f"लेकिन फिर मैंने {T.APP} के साथ प्रैक्टिस करना शुरू किया।", "upbeat, proud"),
            ("hoc", 1, "सिर्फ़ तीन हफ़्तों में मैं फ्लुएंटली और कॉन्फिडेंस के साथ इंग्लिश बोलने " + ("लगी।" if nu else "लगा।"), "confident, proud"),
            ("hoc", 1, "और ये बिल्कुल फ्री है। देखिए!", "excited"),
        ]
        vong = VONG_HI

        def rnd(pt, en):
            return f"“{pt}” को इंग्लिश में कैसे बोलेंगे? {en}. मेरे साथ बोलिए: {en}."
    else:
        phan1 = [
            ("hoc", 1, "Nunca, pero nunca respondas “Me too” cuando alguien te diga “Nice to meet you”.", "decisive, persuasive"),
            ("hoc", 1, "Me too. You’re welcome. I’m fine, thanks.", "doubtful", {"gach": True}),
            ("hoc", 1, "Yo también contestaba así.", "playful, warm"),
            ("hoc", 1, f"Pero todo cambió cuando empecé a practicar con {T.APP}.", "upbeat, proud"),
            ("hoc", 1, "En tan solo tres semanas, ya hablaba inglés con fluidez y confianza.", "confident, proud"),
            ("hoc", 1, "¡Y es gratis! ¡Mira!", "excited"),
        ]
        vong = VONG_ES

        def rnd(pt, en):
            return f"¿Cómo dirías “{pt}” en inglés? {en}. Repite conmigo: {en}."
    L = list(phan1)
    for pt, en, _ in vong:
        L.append(("day", 2, rnd(pt, en), "helpful, friendly"))
        L.append(("hoc", 2, f"{en}.", "cheerful, confident"))
    out = []
    for who, phan, text, emo, *ex in L:
        d = {"who": who, "text": text, "emo": emo, "fx": "none", "phan": phan}
        d.update(ex[0] if ex else {})
        out.append(d)
    return out, vong, len(phan1)


def giong(nat, lang, nu, tuoi):
    do_tuoi = ("in their twenties" if tuoi < 30 else "in their thirties" if tuoi < 40 else "in their forties" if tuoi < 50
               else "in their fifties" if tuoi < 60 else "in their sixties")
    pitch = "natural mid-high pitch around 190–220 Hz, warm" if nu else "natural mid pitch around 120–150 Hz, warm"
    ngon = {"pt": "native Brazilian Portuguese; speaks English clearly with a light Brazilian accent",
            "hi": "native Hindi; speaks English clearly with a light Indian accent",
            "ar": "speaks fluent Modern Standard Arabic; speaks English clearly with a light Arabic accent",
            "es": "native Mexican Spanish; speaks English clearly with a light Mexican accent"}[lang]
    return (f"a real {nat} {'woman' if nu else 'man'} {do_tuoi}, {pitch}, confident and charismatic like a conference speaker, "
            f"{ngon}; a real person, not an actor")


def gioi(nu):
    return dict(HE="she", HE_C="She", HIS="her", HIM="her") if nu else dict(HE="he", HE_C="He", HIS="his", HIM="him")


def anh_path(bo, kind, stt):
    d = D.BO[bo][1]
    for e in (".webp", ".png", ".jpg"):
        if os.path.isfile(os.path.join(D.ANH, d, f"{kind}-{stt:02d}{e}")):
            return REL + f"{d}/{kind}-{stt:02d}{e}"
    raise FileNotFoundError(f"chưa có ảnh {kind}-{stt:02d} của bộ {bo} (chạy tai_anh_csv.py)")


def main():
    for bo, cfg in BO.items():
        if sys.argv[1:] and bo not in sys.argv[1:]:   # python tao_bien_the_csv.py arab hindi2 → chỉ dựng các bộ nêu tên
            continue
        res = []
        for stt, mo_ta, link, mo_ta_robot, link_robot in D.doc(bo):
            nu = mo_ta.lstrip().startswith("Người phụ nữ")
            tuoi = int(re.search(r"khoảng (\d+) tuổi", mo_ta).group(1))
            lt, vong, n1 = luot(cfg["lang"], nu)
            v = {
                # X0104/X0105: tên theo yêu cầu "<mã>_Speaker <Hindi|Arabic> <Nam|Nữ>_<STT>" (STT 01–20 cho cả hai dự án)
                "name": (f"{cfg['ma']}_Speaker {cfg['ten']} {'Nữ' if nu else 'Nam'}_{stt + cfg['stt0']:02d}" if cfg.get("ma")
                         else f"bien-the-{stt:02d}-{'nu' if nu else 'nam'}-{tuoi}"),
                "TEN_HOC": "the speaker", "VAI_HOC": "keynote speaker",
                "NGUOI_HOC": (f"a {cfg['nat']} {'woman' if nu else 'man'} of about {tuoi} years old, with the face, hair, build "
                              f"and complete outfit exactly as in the reference photo"),
                "GIONG_HOC": giong(cfg["nat"], cfg["lang"], nu, tuoi),
                "DAO_HOC": T.DAO_HOC, "DAO_DIENTHOAI": DAO_DT if cfg.get("dt") else T.DAO_DIENTHOAI,
                "NEN_HOC": T.NEN_HOC1, "NEN_HOC2": T.NEN_HOC2,
                "TEN_DAY": "the AI tutor", "VAI_DAY": "AI robot tutor",
                "NGUOI_DAY": ROBOT_CSV if cfg.get("robot") else T.ROBOT,
                "GIONG_DAY": T.GIONG_DAY.replace("natural Brazilian Portuguese accent", f"natural {cfg['ngon']} accent"),
                "NEN_DAY": T.NEN_DAY,
                "NGON_NGU": cfg["ngon"], "TU_OLHA": cfg["tu_olha"],
                "LUOT": lt,
                "HAU_KY": {"ngon_ngu": cfg["lang"], "the": [
                    {"luot": n1 + 2 * k, "luot_hoc": n1 + 1 + 2 * k, "pt": pt, "en": en, "ipa": ipa} for k, (pt, en, ipa) in enumerate(vong)]},
            }
            if cfg.get("dt"):
                v["TEN_DT"], v["NGUOI_DT"] = "the Talka AI robot", ROBOT_DT
            v.update(gioi(nu))
            v["refs"] = {"NGUOI_HOC": [anh_path(bo, "bien-the", stt)],
                         "NGUOI_DAY": [anh_path(bo, "robot", stt) if cfg.get("robot") else T.ANH + "ai-robot-mu-kinh.png"]}
            if cfg.get("dt"):
                v["refs"]["NGUOI_DT"] = [ANH_ROBOT_DT]
            res.append(v)
        with open(os.path.join(OUT, cfg["file"]), "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print(cfg["file"], len(res), "biến thể,", len(res[0]["LUOT"]), "lượt")


if __name__ == "__main__":
    main()
