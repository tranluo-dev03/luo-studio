"""Sinh SAMPLE/xe-tai-canh-sat-gia-su-ai/BIEN-THE-XE-TAI-CANH-SAT-GIA-SU-AI.json.
Sửa bảng BIEN_THE (tài xế, cảnh sát, xe, đường, ảnh) hoặc hàm luot() rồi chạy:
    .venv\\Scripts\\python.exe SAMPLE\\xe-tai-canh-sat-gia-su-ai\\cong-cu\\tao_bien_the.py
Biến thể 01 bám sát video mẫu: lời giữ nguyên văn theo phụ đề trên hình (Whisper ghép "Okay. Wow, your English is good." thành hai câu;
phụ đề ghi "You mean: I'm going home?", "Ah, ... I'm going home.", "But I don't have moneys.").
Cặp nhân vật luôn KHÁC GIỚI (tài xế nữ, cảnh sát nam) để Muse không gán nhầm giọng khi hai người chung khung (sổ tay 3.2);
kịch bản dùng "his" cho cảnh sát, không dùng đại từ cho tài xế.
Ảnh tham chiếu: CHỈ dùng ảnh AI do người dùng cung cấp (link hoặc tệp trong anh/), KHÔNG cắt ảnh từ video mẫu (người dùng chốt 05/11/2026).
Ảnh chưa có thì để None: bỏ khỏi refs và in cảnh báo; đường dẫn tệp tính từ thư mục gốc repo."""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-XE-TAI-CANH-SAT-GIA-SU-AI.json")
ANH = "SAMPLE/xe-tai-canh-sat-gia-su-ai/anh/"
ANH_AI = ANH + "ai-robot-talka.png"   # robot Talka (ảnh AI người dùng gửi 05/11/2026, cùng robot của du-lich-chia-doi-gia-su-ai)

# Gia sư = robot app Talka (người dùng đổi 05/11/2026; trước là cô gái hoạt hình 3D tóc vàng như video mẫu). Mô tả theo ảnh ANH_AI.
AI = ("a sleek feminine humanoid robot: a smooth matte-white porcelain face with calm light-blue eyes, soft flexible porcelain lips that "
      "open and move naturally with every word whenever the robot itself speaks, a few thin panel lines, a bald white helmet-like head with small "
      "dark ear modules, a black mechanical neck of bundled cables, glossy white hexagonal armour plates on the chest, shoulders and arms with thin "
      "glowing cyan seams over black mechanical joints, slim black mechanical hands")

CHUNG = {
    "VAI_CANHSAT": "state trooper",
    "POS_CANHSAT": "RIGHT",
    "NGHE_CANHSAT": "stands still on the road looking up at the driver with a calm attentive face, mouth closed, hands relaxed unless the clip's action says otherwise",
    "NHIN_CANHSAT": "keeps looking up at the driver in the cab window, never into the lens",
    "VAI_HOC": "truck driver",
    "POS_HOC": "LEFT",
    "NGHE_HOC": "stays leaning on the window sill looking down at the officer with a friendly attentive face, mouth closed",
    "NHIN_HOC": "keeps looking down at the officer standing below the window, never into the lens",
    "NHIN_HOC@2": "looks into the lens, as if talking to the AI tutor on the phone held in the right hand",
    "DAO_GIAY_TO": "a small stack of papers: a plastic driver's licence card on top of a folded white registration sheet, no readable text",
    "DAO_DIEN_THOAI": "a black smartphone",
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": AI,
    "GIONG_DAY": "a bright, warm, friendly young woman's voice around 190–230 Hz with a light smooth synthetic sheen, clear American accent, upbeat and encouraging",
    "NEN_DAY": "a plain black background with soft concentric glowing white sound-wave rings behind her head",
    "NHIN_DAY": "looks straight into the lens, as if talking to the person on the call",
}

# (tên, tài xế: TEN, NGUOI, GIONG; cảnh sát: TEN, NGUOI, GIONG; XE, NEN_DUONG, NEN_CABIN, ảnh tài xế, ảnh cảnh sát)
BIEN_THE = [
    ("bien-the-01-goc",
     "the truck driver",
     "a white American woman in her late fifties, a long oval face with fine wrinkles, deep-set hazel eyes, thin lips, chin-length light-brown hair "
     "with a few gray strands and side-swept bangs; a tan canvas work jacket with yellow-green reflective stripes on the sleeves over a navy work shirt, "
     "a small blank white name patch on the chest",
     "a slightly husky, warm American woman's voice in her late fifties, around 200–230 Hz, Southern accent, rising brighter and faster when excited; "
     "a real person, not an actress",
     "the officer",
     "a white American man in his early thirties, short brown hair, light stubble, dark aviator sunglasses, a tan short-sleeved state-trooper uniform "
     "shirt with plain shoulder patches and a gold star badge, a plain fluorescent yellow-green safety vest without lettering, a black duty belt with "
     "holster and radio, a black wristwatch",
     "a relaxed, clear American man's baritone around 110–140 Hz, friendly but firm, slight Southern drawl",
     "a big glossy blue American semi-truck cab painted with a large waving stars-and-stripes flag design on the door and side, chrome steps and tanks, "
     "a tall blue side mirror on a metal arm",
     "the shoulder of a wide multi-lane highway at sunset: tall palm trees and green bushes along the road, far-away cars standing still in the distance, "
     "a dramatic pink-and-orange sky with scattered clouds",
     "the inside of the truck cab at sunset: dark gray seat and door panel, the side window on the right showing a still orange sunset over flat fields "
     "with a few trees, warm light on the face",
     None, None),
    ("bien-the-02-xe-do-sa-mac",
     "the truck driver",
     "a Mexican-American woman in her mid forties, a round face with full cheeks, warm dark-brown eyes, thick eyebrows, medium tan skin, long dark "
     "hair in a low ponytail with a few loose strands; a faded denim work shirt with rolled sleeves over a white T-shirt, a small silver cross necklace",
     "a warm, slightly raspy woman's voice in her mid forties, around 190–220 Hz, light Mexican accent in English, cheerful and quick when excited; "
     "a real person, not an actress",
     "the officer",
     "a Black American man in his early forties, a shaved head, a neat short beard, kind dark eyes, a dark-gray state-trooper uniform shirt with plain "
     "shoulder patches and a silver star badge, a plain fluorescent yellow-green safety vest without lettering, a black duty belt with holster and radio",
     "a deep, calm American man's voice around 95–125 Hz, warm and steady, polite",
     "a big glossy cherry-red American semi-truck cab with chrome trim, chrome steps and tanks, a tall chrome side mirror on a metal arm",
     "the shoulder of a straight two-lane desert highway at sunset: red rock mesas, dry desert brush, wooden power poles, a far-away car standing still, "
     "a glowing orange-and-violet sky",
     "the inside of the red truck cab at sunset: a tan leather seat and door panel, the side window on the right showing a still desert sunset with red "
     "rock mesas, warm light on the face",
     None, None),
    ("bien-the-03-xe-xanh-la-rung-thong",
     "the truck driver",
     "an Irish-American woman in her early sixties, a narrow face with freckles, pale blue eyes behind thin gold-rimmed glasses, short silver-white hair "
     "in a pixie cut; a red-and-black checked flannel shirt under a quilted dark-green vest",
     "a bright, slightly scratchy woman's voice in her early sixties, around 210–240 Hz, Midwestern accent, chatty and lively; a real person, not an actress",
     "the officer",
     "a Latino American man in his late twenties, short black hair with a neat fade, clean-shaven, dark brown eyes, dark aviator sunglasses, a navy "
     "state-trooper uniform shirt with plain shoulder patches and a gold star badge, a plain fluorescent yellow-green safety vest without lettering, "
     "a black duty belt with holster and radio",
     "a clear, energetic American man's voice around 115–145 Hz, friendly, slight Latino accent",
     "a big glossy forest-green American semi-truck cab with chrome trim, chrome steps and tanks, a tall chrome side mirror on a metal arm",
     "the shoulder of a quiet two-lane highway through a pine forest at sunset: tall dark pine trees on both sides, a far-away car standing still, "
     "a soft golden-pink sky",
     "the inside of the green truck cab at sunset: a dark gray seat and door panel, the side window on the right showing still pine trees against a "
     "golden sunset, warm light on the face",
     None, None),
]


def luot():
    P1 = [
        ("canhsat", "How long have you been driving today?", "calm, curious"),
        ("hoc", "I have been driving for, uh, six hours.", "hesitant, friendly"),
        ("canhsat", "When was the last time you slept?", "decisive, calm"),
        ("hoc", "I slept last night.", "confident, friendly"),
        ("canhsat", "Give me your driving license and registration.", "decisive"),
        ("hoc", "Here they are, sir.", "friendly, cheerful"),
        ("canhsat", "Okay. Wow, your English is good.", "impressed, amused"),
        ("hoc", "Honestly, just ten minutes a day with LangLearn.", "proud, enthusiastic"),
        ("hoc", "Real conversations exactly like this one. Here, let me show you.", "excited, playful"),
    ]
    out = [{"who": w, "text": t, "emo": e, "fx": "none", "phan": 1} for w, t, e in P1]
    P2 = [
        {"who": "day", "text": "Where are you going?", "emo": "curious, friendly"},
        {"who": "hoc", "text": "I go to home.", "emo": "cheerful, confident", "fx": "wrong", "icon": "x", "to": "go to"},
        {"who": "day", "text": "You mean, I'm going home?", "emo": "warm, encouraging"},
        {"who": "hoc", "text": "Ah, yes. I'm going home.", "emo": "cheerful", "fx": "right", "icon": "check", "to": "going"},
        {"who": "hoc", "text": "I am very hurry.", "emo": "cheerful, clumsy", "fx": "wrong", "icon": "x", "to": "am very"},
        {"who": "day", "text": "I'm in a hurry, is the correct way to say that.", "emo": "warm, patient"},
        {"who": "hoc", "text": "Oh, okay. Thank you. Wait, who are you?", "emo": "surprised, curious"},
        {"who": "day", "text": "I'm an AI tutor, and I'm here to help you practice your English and eventually get better at speaking.", "emo": "warm, friendly"},
        {"who": "hoc", "text": "But I don't have moneys.", "emo": "worried", "icon": "dollar"},
        {"who": "day", "text": "It's I have no money. But don't worry, LangLearn is a completely free app.", "emo": "reassuring, playful"},
        {"who": "hoc", "text": "Seriously?", "emo": "surprised"},
        {"who": "day", "text": "We can practice English anytime, anywhere. Just download LangLearn.", "emo": "upbeat, persuasive"},
        {"who": "hoc", "text": "I will download now. Thank you so much.", "emo": "delighted, excited"},
    ]
    for t in P2:
        out.append({"fx": "none", **t, "phan": 2})
    return out


def main():
    res = []
    for (name, ten_hoc, nguoi_hoc, giong_hoc, ten_cs, nguoi_cs, giong_cs, xe, duong, cabin, anh_hoc, anh_cs) in BIEN_THE:
        v = {"name": name,
             "TEN_CANHSAT": ten_cs, "NGUOI_CANHSAT": nguoi_cs, "GIONG_CANHSAT": giong_cs,
             "TEN_HOC": ten_hoc, "NGUOI_HOC": nguoi_hoc, "GIONG_HOC": giong_hoc,
             "XE": xe, "NEN_DUONG": duong, "NEN_CABIN": cabin, **CHUNG}
        refs = {k: [x] for k, x in (("NGUOI_HOC", anh_hoc), ("NGUOI_CANHSAT", anh_cs), ("NGUOI_DAY", ANH_AI)) if x}
        miss = [k for k, x in (("NGUOI_HOC", anh_hoc), ("NGUOI_CANHSAT", anh_cs), ("NGUOI_DAY", ANH_AI)) if not x]
        if miss:
            print(f"CẢNH BÁO {name}: chưa có ảnh tham chiếu cho {', '.join(miss)} (cần ảnh AI người dùng cung cấp)")
        if refs:
            v["refs"] = refs
        v["LUOT"] = luot()
        res.append(v)
    json.dump(res, open(OUT, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.normpath(OUT), f"({len(res)} biến thể, {len(res[0]['LUOT'])} lượt)")


if __name__ == "__main__":
    main()
