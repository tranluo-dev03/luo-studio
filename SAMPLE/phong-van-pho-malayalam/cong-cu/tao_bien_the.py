"""Sinh SAMPLE/phong-van-pho-malayalam/BIEN-THE-PHONG-VAN-PHO-MALAYALAM.json từ bảng NHAN_VAT + lời thoại LUOT.
Chạy:  runtime\\python.exe SAMPLE\\phong-van-pho-malayalam\\cong-cu\\tao_bien_the.py
Lời thoại đọc từ phụ đề trên hình của video mẫu (Malayalam + tiếng Anh, đọc từng khung 0,25 s). Whisper KHÔNG dùng được: nó nghe tiếng Malayalam
thành chữ Devanagari vô nghĩa (--lang hi) nên chỉ lấy mốc cảnh cắt và số mặt. Ai nói ở phần 2 xác định bằng chuyển động miệng ô dưới.
Gộp câu liền của cùng một người khi <= 20 từ. Sửa trong video mẫu: phóng viên nói "một tháng trước", người bán trả lời "ba tháng trước"
-> biến thể 01 thống nhất "một tháng" (khớp lời robot "trong một tháng").
Ảnh tham chiếu ở "refs": robot = ảnh robot Talka của người dùng (anh/robot-talka.png); phóng viên, người bán = Muse gen theo mô tả
(cong-cu/gen_anh_tham_chieu.py, theo yêu cầu người dùng 11/11/2026). Không cắt từ video mẫu."""
import json
import os
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-PHONG-VAN-PHO-MALAYALAM.json")

# who, phần, text, emo
LUOT = [
    # PHẦN 1: phỏng vấn đường phố (11 cảnh)
    ("pv", 1, "അപ്രതീക്ഷിതമായി എന്നതിന് ഇംഗ്ലീഷിൽ എന്താ പറയുക?", "playful, curious"),
    ("hoc", 1, "Suddenly.", "confident"),
    ("pv", 1, "ഉടനെ.", "playful"),
    ("hoc", 1, "Immediately.", "confident"),
    ("pv", 1, "ഇതും കൂടി നോക്കട്ടെ, അല്ലെങ്കിൽ...", "playful"),
    ("hoc", 1, "Otherwise.", "confident"),
    ("pv", 1, "അതുകൊണ്ട്?", "playful"),
    ("hoc", 1, "Therefore.", "proud"),
    ("pv", 1, "ഒരു മാസം മുൻപ് വരെ നിങ്ങൾക്ക് ഇംഗ്ലീഷിന്റെ ഒരു വാക്ക് പോലും അറിയില്ലായിരുന്നു എന്ന് പറഞ്ഞിരുന്നല്ലോ.", "impressed"),
    ("hoc", 1, "Yeah, one month ago the only English I heard was from TV. And now I am talking fluently.", "proud"),   # video: 2 câu liền -> gộp (18 từ)
    ("hoc", 1, "ശരിക്കും ഇംഗ്ലീഷ് ഫ്ലുവന്റ് ആയി സംസാരിക്കാനുള്ള സീക്രട്ട് എന്താണെന്നോ? ആദ്യദിവസം മുതൽക്കേ സംസാരിച്ച് തുടങ്ങണം. വാ, ഞാൻ കാണിച്ചുതരാം.", "cheerful"),
    # PHẦN 2: robot ô trên, người bán hàng ô dưới (15 cảnh)
    ("day", 2, "വെറും ഒരു മാസത്തിനുള്ളിൽ നിങ്ങൾക്ക് നേറ്റീവ് സ്പീക്കേഴ്സിനെ പോലെ ഇംഗ്ലീഷ് സംസാരിക്കാൻ തുടങ്ങാം എന്നറിയാമോ? ഇതൊരു മാജിക് ഒന്നുമല്ല.", "enthusiastic"),
    ("day", 2, "നിങ്ങൾ സംസാരിക്കുമ്പോൾ തന്നെ തെറ്റുകൾ തിരുത്തി തരുന്ന, നിങ്ങൾക്ക് പോലും അറിയാത്ത രീതിയിൽ കാര്യങ്ങൾ പഠിപ്പിച്ചു തരുന്ന ആപ്പ് ആണിത്.", "warm"),
    ("day", 2, "നമുക്കൊന്ന് ട്രൈ ചെയ്യാം. നിങ്ങൾക്ക് ഇംഗ്ലീഷ് സംസാരിക്കാൻ അറിയാമോ?", "friendly"),
    ("hoc", 2, "കുറച്ച്... കുറച്ച്.", "hesitant"),
    ("day", 2, "Where are you from?", "friendly, curious"),
    ("hoc", 2, "I am Kannur.", "unsure"),
    ("day", 2, "ഏകദേശം ശരിയാണ്. പക്ഷേ I am from Kannur എന്ന് പറയുന്നതായിരിക്കും കുറച്ചുകൂടി നല്ലത്.", "encouraging"),
    ("hoc", 2, "അയ്യോ, എനിക്ക് എപ്പോഴും ഇവിടെയാണ് കൺഫ്യൂസ് ആകുന്നത്.", "embarrassed"),
    ("day", 2, "അതുകൊണ്ടാണല്ലോ ഞാൻ ഇവിടെ ഉള്ളത്. കറക്റ്റ് ആയി സംസാരിക്കാൻ നിങ്ങളെ സഹായിക്കാൻ.", "reassuring"),
    ("hoc", 2, "പക്ഷേ, ഇതിന് expensive ആയിരിക്കില്ലേ?", "worried"),
    ("day", 2, "നോർമൽ ഇംഗ്ലീഷ് ക്ലാസ്സിനേക്കാൾ ഏഴു മടങ്ങ് കുറഞ്ഞ ചെലവിൽ ഇത് ലഭിക്കും.", "reassuring"),
    ("day", 2, "ദിവസവും വെറും പതിനഞ്ച് മുതൽ ഇരുപത് മിനിറ്റ് വരെ practice ചെയ്താൽ മതി.", "warm"),
    ("day", 2, "മലയാളത്തിലൂടെ practice ചെയ്യുന്നത് കൊണ്ട് പതുക്കെ നല്ല confident ആകും. ഒരു AI ടീച്ചറുടെ കൂടെ അസ്സൽ ഇംഗ്ലീഷ് practice.", "enthusiastic"),  # video: 2 câu liền -> gộp
    ("hoc", 2, "അതായത്, ഒരു real ടീച്ചറിനെ പോലെയാണോ?", "curious"),
    ("day", 2, "അതെ, ഇത് നിങ്ങളുടെ grammar-ഉം pronunciation-ഉം ശരിയാക്കും. ഒപ്പം confidence-യോടെ സംസാരിക്കാനും സഹായിക്കും.", "confident, warm"),
]

AIVA = ("a sleek white humanoid AI robot teacher, exactly as in its reference photo: a smooth glossy white head with fine panel seams and no hair, a realistic "
        "young woman's face with pale light blue eyes, soft lips that open and move like a real person's whenever it speaks and a calm warm expression, a black "
        "ribbed mechanical neck, white hexagon-plated armour on the shoulders and chest with black mechanical joints and thin glowing light blue accent lines")
GIONG_AIVA = ("a bright, warm young woman's voice (around 210-230 Hz) with a light synthetic sheen, clear and lively like a friendly teacher, native Kerala "
              "Malayalam, says the English words clearly with a light Indian English accent")

NGUOI_HOC = ("a Malayali woman about fifty-five years old, warm brown skin, black hair with a few grey strands parted in the middle and tied in a low bun, "
             "a small red bindi, a kind round face; a magenta-pink short-sleeved blouse and a brown-and-grey checked cotton saree with a thin red border "
             "draped over her left shoulder; photorealistic skin and fabric")
GIONG_HOC = ("a real middle-aged Malayali woman's voice (around 200-230 Hz), warm, lively and a little husky, native Kerala Malayalam, says the English "
             "words like a proud learner; a real person, not an actress")

CHUNG = {
    # phần 1
    "TEN_PV": "the interviewer", "VAI_PV": "street interviewer", "POS_PV": "LEFT foreground, seen from behind",
    "NGUOI_PV": ("a young Malayali man about twenty-eight years old, short neat black hair, thin black-framed glasses, a short trimmed beard, a pink-and-white "
                 "plaid cotton shirt with rolled sleeves, a black backpack on his back"),
    "GIONG_PV": ("a real young Malayali man's voice, light baritone (around 150-180 Hz), friendly and playful like a street-interview host, native Kerala "
                 "Malayalam; a real person, not an announcer"),
    "QUAY_LUNG_PV": "1",
    "NHIN_PV": ("keeps his face pointed at the woman's face, to the right and slightly down, the camera seeing only the back and the right edge of his head; "
                "he never turns toward the camera"),
    "NGHE_PV": "holds the microphone still toward the woman and keeps his face pointed at her, his head still, the camera seeing only the back of his head",
    "DAO_MIC": "a plain black handheld microphone with no logo",
    "VAI_HOC": "street-food vendor",
    "POS_HOC": "CENTRE-RIGHT, behind the cart",
    "NHIN_HOC": "looks at the interviewer's face, to the left, in three-quarter view, and never looks at the camera",
    "NGHE_HOC": ("keeps the lips pressed together and looks at the interviewer's face with a friendly attentive face, her gloved hands resting above the pots; "
                 "she never looks at the camera"),
    "DAO_GANG": "She wears thin clear disposable plastic gloves on both hands.",
    # đại từ + động tác tay theo nghề (kịch bản dùng chung cho mọi nghề, xem tao_40_bien_the.py)
    "SHE_HOC": "she", "HER_HOC": "her", "HERO_HOC": "her", "SELF_HOC": "herself",
    "TAY_HOC": "her gloved hands resting above the pots",
    "VIEC_HOC": "keeps gently shaping a small ball of filling between her gloved fingers above the pots",
    "VIEC2_HOC": "puts the small ball of filling back into the pot",
    "DAO_GIU": "Her gloved hands stay above the steel pots on the cart.",
    "DAO_NGHI": "the interviewer holding the microphone toward her, the woman's gloved hands resting above the pots",
    "DAO_XE": ("a stainless-steel street-food push cart with several round steel pots and bowls of spiced fillings, chutneys and fried snacks, a few steel ladles "
               "in the pots, a stack of small steel plates"),
    "NEN_PHO": ("a quiet old street in a Kerala town on an overcast morning, slightly out of focus: weathered two-storey shophouses with balconies and closed "
                "rolling shutters, a faded blue awning, tall green trees, a grey asphalt road with no traffic; any signboards are blurred and unreadable"),
    # phần 2
    "TEN_DAY": "the AI tutor", "NGUOI_DAY": AIVA, "GIONG_DAY": GIONG_AIVA,
    "NEN_DAY": ("a deep navy-to-violet gradient backdrop with one thin glowing purple circular ring behind the head and a few tiny glowing dots along the ring, "
                "nothing else"),
    "TEN_HOC": "the woman",
    "NEN_HOC": ("her busy street-food stall at a crowded market street, out of focus: trays of colourful snacks and steel pots at the lower right, people walking "
                "far behind, shop fronts with blue awnings, overcast daylight"),
}

ANH = "SAMPLE/phong-van-pho-malayalam/anh/"
# Biến thể 01 bám sát video mẫu. Biến thể mới: thêm một dòng, chỉ đổi đúng thứ được yêu cầu.
NHAN_VAT = [
    {
        "name": "bien-the-01-bam-sat-video",
        "NGUOI_HOC": NGUOI_HOC, "GIONG_HOC": GIONG_HOC,
        "refs": {"NGUOI_DAY": [ANH + "robot-talka.png"], "NGUOI_PV": [ANH + "phong-vien.png"], "NGUOI_HOC": [ANH + "nguoi-ban.png"]},
    },
]

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")


def build():
    out = []
    for nv in NHAN_VAT:
        v = {"name": nv["name"]}
        v.update(CHUNG)
        v.update({k: x for k, x in nv.items() if k not in ("name", "refs")})
        v["LUOT"] = [{"who": w, "text": t, "emo": e, "c": "black", "o": "white", "fx": "none", "phan": p} for w, p, t, e in LUOT]
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
    p1 = sum(1 for x in LUOT if x[1] == 1)
    print("Đã ghi", os.path.abspath(OUT), f"({len(NHAN_VAT)} biến thể, {len(LUOT)} lượt: {p1} phần 1 + {len(LUOT) - p1} phần 2, "
          f"dài nhất {max(len(t.split()) for _, _, t, _ in LUOT)} từ)")
