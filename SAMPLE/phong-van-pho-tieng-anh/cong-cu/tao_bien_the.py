"""Sinh BIEN-THE-PHONG-VAN-PHO-TIENG-ANH.json: 1 biến thể tiếng Anh (Mỹ), bám video mẫu "1510_interview street hindi_005":
người bán nữ ~45 tuổi đeo găng nilon sau xe đẩy đồ ăn, phóng viên nam quay lưng (khác giới người bán), robot Aiva ô trên.
CHƯA có `refs` (người dùng không cấp ảnh AI): thêm ảnh vào dict REFS rồi chạy lại khi có.
Chạy:  runtime\python.exe SAMPLE\phong-van-pho-tieng-anh\cong-cu\tao_bien_the.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "BIEN-THE-PHONG-VAN-PHO-TIENG-ANH.json")

REFS = {}   # vd. {"NGUOI_DAY": ["SAMPLE/.../robot-aiva.png"], "NGUOI_PV": [...], "NGUOI_HOC": [...], "NEN_PHO": [...], "NEN_HOC": [...]}

# (who, phần, lời, cảm xúc); lời viết lại theo mạch video mẫu, <= 20 từ
LUOT = [
    ("pv", 1, "How did you learn to speak English so well?", "friendly, curious"),
    ("hoc", 1, "A month ago I only heard English on TV. Now I speak fluently every day.", "proud"),
    ("pv", 1, "So what's your secret, really?", "amazed, friendly"),
    ("hoc", 1, "I started practicing English from the very first day.", "confident"),
    ("pv", 1, "And where are you from, exactly?", "curious, playful"),
    ("hoc", 1, "I'm from Denver. Come, I'll show you how.", "cheerful, inviting"),
    ("day", 2, "In just one month you'll speak like a native. Can you say this sentence after me?", "warm, encouraging"),
    ("hoc", 2, "Yes, sure, I can try it right now.", "hesitant, willing"),
    ("day", 2, "Perfect! Your pronunciation gets better every day.", "delighted"),
    ("hoc", 2, "And this isn't very expensive, is it?", "worried"),
    ("day", 2, "No, you practice English for free, with no limits.", "reassuring"),
    ("day", 2, "I fix your grammar and pronunciation instantly. You'll speak with confidence, like with a real teacher.", "warm, confident"),
]

NOI = ("a quiet American small-town street in the daytime, two-storey brick buildings, a blue shop awning, a few trees, overcast sky; "
       "any signboards are blurred and unreadable")
TAY = "her gloved hands resting on the edge of the cart"


def build():
    v = {"name": "en01-street-food-vendor"}
    v.update({
        "TEN_PV": "the interviewer", "VAI_PV": "street interviewer", "POS_PV": "LEFT foreground, seen from behind",
        "NGUOI_PV": ("a young American man about 28 years old with short dark hair and thin glasses, a pink-and-white checked shirt, "
                     "a black backpack strap over the shoulder"),
        "GIONG_PV": "a real young American man's voice, light baritone (around 125-150 Hz), friendly and playful like a street-interview host, "
                    "native American English; a real person, not an announcer",
        "QUAY_LUNG_PV": "1",
        "HIS_PV": "his", "HIM_PV": "him", "TOC_PV": "short dark hair",
        "NHIN_PV": ("keeps his face pointed at the vendor's face, to the right and slightly down, the camera seeing only the back and the right edge of his head; "
                    "he never turns toward the camera"),
        "NGHE_PV": "holds the microphone still toward the vendor and keeps his face pointed at her, his head still, the camera seeing only the back of his head",
        "DAO_MIC": "a plain black handheld microphone with no logo",
        "TEN_HOC": "the vendor", "VAI_HOC": "street food seller", "POS_HOC": "CENTRE-RIGHT, behind the cart",
        "NGUOI_HOC": ("an American woman about 45 years old with black hair in a neat bun, a friendly open face, a magenta blouse "
                      "and a brown-grey shawl over the shoulder, a small red dot on the forehead; photorealistic skin and fabric"),
        "GIONG_HOC": "a real American woman's voice, warm, a little husky and unhurried (around 200-225 Hz), native American English; a real person, not an actress",
        "SHE_HOC": "she", "HER_HOC": "her", "HERO_HOC": "her", "SELF_HOC": "herself",
        "DAO_GANG": "She wears thin clear plastic food-service gloves.",
        "DAO_GIU": "Her gloved hands rest on the edge of the cart at the start of every clip.",
        "TAY_HOC": TAY, "VIEC_HOC": "keeps shaping a small dumpling with her gloved fingers", "VIEC2_HOC": "her gloved hands go back to the dough on the cart",
        "NHIN_HOC": "looks at the interviewer's face, to the left, in three-quarter view, and never looks at the camera",
        "NGHE_HOC": ("keeps the lips pressed together and looks at the interviewer's face with a friendly attentive face, " + TAY +
                     "; she never looks at the camera"),
        "DAO_NGHI": "the interviewer holding the microphone toward her, " + TAY,
        "DAO_XE": ("a stainless-steel street-food cart with several round steel pots of filling and sauce, a tray of fried snacks and small steel bowls"),
        "NEN_PHO": NOI + "; she stands behind her food cart",
        "TEN_DAY": "the AI tutor",
        "NGUOI_DAY": ("a glossy white humanoid AI robot with a smooth, calm, human-like face, glowing blue eyes, a small glowing AI mark on the forehead and "
                      "dark glossy neck joints"),
        "GIONG_DAY": "a bright, warm young woman's voice (around 210-230 Hz) with a light synthetic sheen, clear and lively like a friendly teacher, native American English",
        "NEN_DAY": ("a deep navy-to-violet gradient backdrop with one thin glowing purple circular ring behind the head and a few tiny glowing dots along the ring, "
                    "nothing else"),
        "NEN_HOC": "a busy outdoor food market with food trays and people walking, out of focus behind her; any signboards are blurred and unreadable",
    })
    v["LUOT"] = [{"who": w, "text": t, "emo": e, "c": "black", "o": "white", "fx": "none", "phan": p} for w, p, t, e in LUOT]
    if REFS:
        v["refs"] = REFS
    return [v]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.abspath(OUT), f"({len(data)} biến thể, {len(data[0]['LUOT'])} lượt, refs: {len(REFS)})")
