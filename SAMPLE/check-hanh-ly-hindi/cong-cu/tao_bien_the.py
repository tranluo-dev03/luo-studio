"""Sinh SAMPLE/check-hanh-ly-hindi/BIEN-THE-CHECK-HANH-LY-HINDI.json từ bảng NHAN_VAT + lời thoại LUOT (theo video mẫu "oder 6.mp4").
Chạy:  .venv\\Scripts\\python.exe SAMPLE\\check-hanh-ly-hindi\\cong-cu\\tao_bien_the.py
Đổi tên app ở APP (một chỗ); đổi tuổi ở cột "tuoi" của từng biến thể (câu sai / câu sửa / câu đúng cùng đổi).
Lời thoại đọc từ phụ đề trên hình của video mẫu (Gujarati + tiếng Anh), Whisper chỉ dùng để lấy mốc giây (nó dịch sang tiếng Anh, không chép được chữ Gujarati).
Câu > 20 từ hoặc hai câu liền của cùng người nói được tách / gộp như ghi chú ở từng dòng."""
import json
import os

APP = "Supernova AI"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-CHECK-HANH-LY-HINDI.json")

# who, text, emo, phan, (fx, icon)
def luot(tuoi):
    p1 = [
        ("canbo", "Is this your bag?", "calm"),
        ("hoc", "Yes.", "calm"),
        ("canbo", "Can you speak English?", "curious"),
        ("hoc", "Yes, of course.", "confident"),
        ("canbo", "Can you prove it to me?", "playful"),
        ("hoc", "I have come to New York to visit my brother.", "calm"),          # video: một lượt 23 từ -> tách 2 lượt
        ("hoc", "I will be staying here for ten days, and then I will go back home.", "warm"),
        ("canbo", "Wow! તમારી English તો બહુ સરસ છે.", "impressed"),
        ("hoc", "Thank you.", "warm"),
        ("hoc", f"Honestly, હું બસ રોજ 15 to 20 minutes {APP} પર speaking practice કરું છું.", "proud"),
        ("hoc", "Daily conversationsથી લઈને real life situationsમાં કેવી રીતે વાત કરવી, એ બધું Miss Nova મને શીખવાડે છે.", "enthusiastic"),
        ("hoc", f"અને મારા level પ્રમાણે {APP} એક personalized course પણ બનાવે છે, જેનાથી મને English શીખવામાં ઘણી સરળતા રહે છે.", "proud"),
        ("canbo", f"{APP}?", "curious"),
        ("hoc", "હા, આ એક AI teacher છે, જેની સાથે તમે રોજ Englishમાં વાત કરીને practice કરી શકો છો.", "friendly"),
        ("hoc", "આ ક્યારેય તમને judge નહીં કરે કે તમારી Englishની મજાક નહીં ઉડાવે.", "reassuring"),
        ("hoc", "એક સારા friendની જેમ તમારી mistakes correct કરશે અને તમને confidently English બોલવામાં help કરશે.", "confident"),
        ("hoc", "ચાલો, હું તમને બતાવું.", "cheerful"),
    ]
    p2 = [
        ("day", "શું તમને English આવડે છે?", "friendly"),
        ("hoc", "હા, બસ થોડું ઘણું.", "hesitant"),
        ("day", "તમારી ઉંમર કેટલી છે?", "friendly"),
        ("hoc", f"I have {tuoi}.", "unsure", "wrong", "x"),
        ("day", f"તમારે કહેવું જોઈએ, I am {tuoi}.", "patient, encouraging"),
        ("hoc", f"I am {tuoi}.", "confident", "right", "check"),
        ("day", "Good job.", "encouraging"),
        ("hoc", "Thank you. પણ તમે કોણ છો?", "curious"),                          # video: hai câu liền của người phụ nữ -> gộp
        ("day", f"હું {APP}ની AI English teacher છું. હું તમારી English speaking improve કરવામાં તમારી મદદ કરીશ.", "warm, friendly"),
        ("day", "તમે ક્યારેય પણ મારી સાથે speaking practice કરી શકો છો.", "warm"),
        ("hoc", "Really?", "surprised"),
        ("day", "ચોક્કસ, તમે ક્યારેય પણ, ક્યાંય પણ મારી સાથે real life English conversationsની practice કરી શકો છો.", "cheerful"),
        ("hoc", "પણ આ તો બહુ મોંઘું હશે ને?", "doubtful"),
        ("day", "બિલકુલ પણ નહીં. આ normal coaching classes કરતાં seven times cheaper છે.", "reassuring"),
        ("day", f"અત્યાર સુધીમાં one crore plus લોકો {APP} પર મારી સાથે practice કરીને પોતાની English improve કરી રહ્યા છે.", "proud"),
        ("day", "તો પછી તમે શેની રાહ જોઈ રહ્યા છો? નીચે આપેલા Install Now પર click કરો,", "enthusiastic"),
        ("day", f"{APP} download કરો અને આજથી જ પોતાની English વધુ સારી બનાવવાનું શરૂ કરો.", "enthusiastic"),
    ]
    res = []
    for phan, rows in ((1, p1), (2, p2)):
        for r in rows:
            d = {"who": r[0], "text": r[1], "emo": r[2], "c": "black", "o": "white", "fx": r[3] if len(r) > 3 else "none", "phan": phan}
            if len(r) > 4:
                d["icon"] = r[4]
            res.append(d)
    return res


CHUNG = {
    "VAI_CANBO": "officer", "POS_CANBO": "LEFT", "TEN_CANBO": "the security officer",
    "VAI_HOC": "woman", "POS_HOC": "RIGHT", "TEN_HOC": "the woman",
    "TEN_DAY": "the AI tutor",
    "NGHE_CANBO": "stands with his left elbow resting on top of the scanner and his right hand on the edge of the tray, head turned toward the woman, mouth closed, "
                  "listening with a friendly face, small nods, his eyes following any gesture she makes and coming back to her face",
    "NGHE_HOC": "stands with her right hand holding the strap of her shoulder bag, mouth closed, looking at the officer's face with a calm friendly smile; her eyes follow "
                "whatever he points at (the bag) and come back to his face",
    "DAO_GIU": "Her right hand holds the bag strap or does the clip's action only: no hand ever goes to her head, face or hair.",
    "DAO_KHAY": "a bright blue plastic airport security tray",
    "DAO_VALI": "a brown leather doctor-style handbag with two rolled handles",
    "DAO_NGHI": "the officer leaning with his left elbow on the scanner, right hand on the edge of the tray; the woman holding her bag strap, both looking at each other",
    "NEN_SOI": "a bright modern Indian airport terminal: a grey stainless X-ray baggage scanner, tall glass windows with daylight, white ceiling, a dark-blue hanging sign "
               "showing only a white airplane pictogram, a tall colourful folk-art wall panel in orange and yellow at the upper right, potted palms, and small travellers "
               "standing far away behind blue queue belts",
    "NEN_HOC": "a bright, modern airport departure hall, softly out of focus: long white ceiling light strips, glass walls, yellow flight-information boards without "
               "readable text, travellers far away",
    "NGUOI_DAY": "a cute friendly humanoid robot with a smooth glossy white head and face, big soft light-blue eyes, gentle soft lips, small black-and-silver ear "
                 "discs on both sides of the head like headphones, a white chest plate with a round glowing blue light in the middle, black mechanical neck joints",
    "NEN_DAY": "a plain deep-blue gradient studio backdrop, lighter blue behind the head",
    "GIONG_DAY": "a bright, light, friendly young woman's voice (around 230-260 Hz), smooth and clear with only a faint synthetic polish, patient and encouraging like a "
                 "kind teacher on a video call, natural Gujarati with Indian English for the English words",
    "NHIN_CANBO": "keeps his head turned toward the woman in three-quarter profile, looking at her face (or at the bag the clip names); his face never turns to the camera",
    "NHIN_HOC": "looks at the officer's face, eyes level, never into the lens",
    "NHIN_HOC@2": "looks straight into the lens, as if talking to the AI tutor on a video call",
    "NHIN_DAY": "looks straight into the lens, as if talking to the person on the call",
}

# Biến thể 1 bám sát video mẫu; biến thể 2 đổi nhân vật. tuoi: tuổi trong nhịp sửa lỗi "I have N" -> "I am N".
NHAN_VAT = [
    {
        "name": "check-hanh-ly-gujarati-sari-xanh",
        "tuoi": 62,
        "NGUOI_HOC": "an Indian woman around sixty, warm medium-brown skin, black hair with a few grey strands pulled back into a low bun, a small red bindi, dark brown "
                     "eyes, a thin gold chain necklace, gold bangles, a dark-green silk saree with a small red-and-gold motif and a wide red-and-gold border, a red "
                     "short-sleeved blouse with small white motifs",
        "DAO_TUI": "a large dark-brown leather shoulder bag",
        "GIONG_HOC": "a real Gujarati woman around sixty, mid-to-high pitch (around 210-240 Hz), warm and gentle, natural Gujarati, Indian English accent for the English "
                     "words, not exaggerated; a real person, not an actress",
        "NGUOI_CANBO": "a young Indian man in his late twenties, short thick wavy black hair, light stubble, a friendly face, a white short-sleeved shirt under a navy-blue "
                       "vest, a navy tie, a blue lanyard with a plain white ID card with no lettering",
        "GIONG_CANBO": "a young Indian man's voice, light baritone (around 140-170 Hz), friendly and relaxed, Indian English accent, natural Gujarati when he speaks "
                       "Gujarati; statements fall at the end, questions rise slightly",
    },
    {
        "name": "check-hanh-ly-gujarati-sari-tim",
        "tuoi": 58,
        "NGUOI_HOC": "an Indian woman in her late fifties, light-brown skin, a round friendly face, thin gold-rimmed glasses, black hair streaked with grey in a neat "
                     "bun, a small maroon bindi, small gold earrings, a purple cotton saree with a thin golden border and a matching purple blouse",
        "DAO_TUI": "a tan leather shoulder bag",
        "GIONG_HOC": "a real Gujarati woman in her late fifties, mid pitch (around 200-225 Hz), soft and cheerful, natural Gujarati, Indian English accent for the "
                     "English words; a real person, not an actress",
        "NGUOI_CANBO": "an Indian man in his early thirties, short neat black hair with a side parting, a trimmed black moustache, a calm face, a light-blue short-sleeved "
                       "uniform shirt, a dark-blue tie, a blue lanyard with a plain white ID card with no lettering",
        "GIONG_CANBO": "an Indian man's voice in his thirties, baritone (around 125-150 Hz), calm and friendly, Indian English accent, natural Gujarati when he speaks "
                       "Gujarati; statements fall at the end, questions rise slightly",
    },
]

out = []
for nv in NHAN_VAT:
    v = {"name": nv["name"]}
    v.update(CHUNG)
    v.update({k: x for k, x in nv.items() if k not in ("name", "tuoi")})
    v["LUOT"] = luot(nv["tuoi"])
    out.append(v)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for v in out:
    n = [len(t["text"].split()) for t in v["LUOT"]]
    print(v["name"], len(v["LUOT"]), "lượt; phần 1:", sum(t["phan"] == 1 for t in v["LUOT"]), "; số từ dài nhất:", max(n))
