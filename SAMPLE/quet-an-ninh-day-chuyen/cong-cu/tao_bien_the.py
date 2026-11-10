"""Sinh SAMPLE/quet-an-ninh-day-chuyen/BIEN-THE-QUET-AN-NINH-DAY-CHUYEN.json (1 biến thể, 28 lượt = 13 phần 1 + 15 phần 2).
Nhân bản từ soi-hanh-ly-gia-su-ai theo CHECKLIST-YEU-CAU-CHUYEN-KICH-BAN.txt (10/11/2026).
  - LUOT 1-5 mới theo kịch bản phần A của checklist; LUOT 6-13 và phần 2 (LUOT 14-28) GIỮ NGUYÊN nguồn (BIEN-THE-SOI-HANH-LY-GIA-SU-AI.json).
  - Ảnh tham chiếu đính kèm (đường dẫn tương đối từ thư mục gốc dự án, Studio tự đọc): anh-tham-chieu/*.webp
      NGUOI_HOC (hành khách), NGUOI_CANBO (nhân viên), NGUOI_DAY (robot), NEN_SOI + NEN_HOC (nền cổng dò kim loại).
Chạy: python SAMPLE\\quet-an-ninh-day-chuyen\\cong-cu\\tao_bien_the.py"""
import json
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(D, "..", "soi-hanh-ly-gia-su-ai", "BIEN-THE-SOI-HANH-LY-GIA-SU-AI.json")
OUT = os.path.join(D, "BIEN-THE-QUET-AN-NINH-DAY-CHUYEN.json")
IMG = "SAMPLE/quet-an-ninh-day-chuyen/anh-tham-chieu/"

nguon = json.load(open(SRC, encoding="utf-8"))[0]["LUOT"]
assert len(nguon) == 28

# Phần A của checklist: 5 lượt đầu mới. (who, text, emo) — emo thuộc EMO_CUES (app/production/prompt_parts.py)
MOI = [
    ("canbo", "Ma'am, could you step back for a moment?", "calm, polite"),
    ("hoc", "Sure.", "worried"),
    ("canbo", "The scanner detected something metallic. Are you wearing any jewelry?", "calm"),
    ("hoc", "Oh, it might be my necklace. I forgot to take it off.", "embarrassed"),
    ("canbo", "Please take it off. Is this your first time in America?", "interested"),
]
luot = []
for i, (who, text, emo) in enumerate(MOI):
    assert nguon[i]["who"] == who, (i, nguon[i]["who"], who)   # nhịp người nói giống bản gốc
    luot.append({"who": who, "text": text, "emo": emo, "c": "white", "fx": "none", "phan": 1})
luot += [dict(x) for x in nguon[5:]]   # lượt 6-28 giữ nguyên (visiting my daughter, 15 minutes a day, I have 48 -> I am 48...)

V = {
    "name": "quet-an-ninh-day-chuyen-01",
    "TEN_HOC": "the passenger",
    "VAI_HOC": "passenger",
    "NGUOI_HOC": ("a Latina woman in her late forties, warm light-tan skin, long wavy dark-brown hair with soft caramel highlights, parted in the middle, dark brown eyes, "
                  "a warm natural smile, a short beige knitted cardigan worn open with three wooden buttons over a plain white ribbed tank top, straight mid-blue jeans, white lace-up sneakers"),
    "GIONG_HOC": ("a real Mexican woman in her late forties speaking English as a second language, mid-pitched (around 200-230 Hz), a natural Mexican accent with Spanish vowels and soft r, "
                  "not exaggerated; quick and a little breathless when nervous, warm, with a smile in the voice and quietly proud when she talks about her tutor; a real person, not an actress"),
    "POS_HOC": "RIGHT",
    "NGHE_HOC": ("stands just past the metal detector gate with one hand resting on the strap of her shoulder bag, mouth closed; her eyes follow whatever the officer gestures at "
                 "(the gate, her necklace, the tray) and come back to his face, with a natural, slightly worried or smiling face that matches the moment"),
    "DAO_TUI": "a medium brown leather shoulder bag with a flap and a long strap",
    "DAO_DAY_CHUYEN": ("one thin, delicate gold-toned metal chain necklace with a single tiny pendant, hanging at her collarbone, easy to recognise "
                       "(the same necklace as in the passenger reference image)"),
    "DAO_KHAY": "a small light-grey plastic tray for personal items",
    "DAO_GIU": ("Her free hand rests on the strap of her shoulder bag or does the clip's action only: no hand ever goes to her head, face or hair; "
                "the only time her hands go to her neck is for the necklace actions the clip describes."),
    "DAO_NGHI": "the passenger standing with one hand resting on her bag strap, the officer standing still beside the gate",
    "DAO_DIEN_THOAI": ("a smartphone in a dark case; its screen shows a live video call with the AI tutor, the very same robot as everywhere else in this video: {{NGUOI_DAY}}, "
                       "seen from the waist up in front of {{NEN_DAY}}; it is only a picture on the phone screen, never a person in the scene; no text, no buttons"),
    "TEN_CANBO": "the security officer",
    "VAI_CANBO": "officer",
    "POS_CANBO": "LEFT",
    "NGUOI_CANBO": ("a man in his early forties, short side-swept brown hair, clean-shaven, a friendly firm face, a royal-blue airport security uniform shirt with dark epaulettes and a plain round shoulder patch, "
                    "a black tie with a silver tie clip, a plain gold-toned badge with no lettering, a black shoulder radio microphone with a coiled cord, a black belt, dark-navy cargo trousers, black boots; "
                    "no lettering on the nameplate"),
    "GIONG_CANBO": ("a real American airport security officer's voice, low baritone (around 130-150 Hz), a little tired from a long shift, even and unhurried, never theatrical: "
                    "statements fall in pitch at the end, yes/no questions lift slightly at the end; mostly flat and routine, warming up a little when he compliments her"),
    "NGHE_CANBO": ("stands beside the metal detector gate with both arms relaxed, head turned toward the passenger, mouth closed; his eyes follow whatever she touches or holds up "
                   "(her necklace, the phone) and come back to her face, with small natural reactions"),
    "NEN_SOI": ("a bright modern airport security area: a tall brushed-silver walk-through metal detector gate with two vertical LED bars and a small dark display on its top beam, "
                "tall glass windows and white columns, a glossy pale granite floor reflecting the light, blue retractable queue belts on chrome posts, a potted palm, "
                "and a few small travellers standing still far away; no baggage scanner, no conveyor, no suitcases"),
    "NEN_HOC": ("a bright, nearly empty modern airport hall just past the security checkpoint, softly out of focus: tall glass windows, white columns, "
                "a glossy pale granite floor reflecting the light, chrome posts with blue queue belts far behind her"),
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": ("a sleek feminine humanoid robot with glossy white armour panels with thin light-blue glowing seams, black cables and mechanical joints at the neck, shoulders and waist, "
                  "a smooth white porcelain face with soft light-blue eyes and finely sculpted lips, a calm friendly expression"),
    "GIONG_DAY": ("a bright, light, friendly young woman's voice, clearly higher and lighter than the passenger's, smooth and clear with only a faint synthetic polish, "
                  "patient and encouraging like a kind language teacher on a video call, neutral American accent"),
    "NEN_DAY": "a bright white-and-pale-blue studio backdrop with soft glowing light and a thin luminous white circular halo ring behind the head",
    "NHIN_CANBO": ("keeps his head turned toward the passenger in three-quarter profile, looking at her face (or at the gate, her neck area, the tray or the phone the clip names); "
                   "his face never turns to the camera or out of the frame"),
    "NHIN_HOC": ("looks at the officer's face, eyes level, never into the lens (except when the clip's action makes her look down at her necklace or the phone)"),
    "NHIN_HOC@2": "looks straight into the lens, as if talking to the AI tutor on the phone she is holding",
    "NHIN_DAY": "looks straight into the lens, as if talking to the person on the call",
    "refs": {
        "NGUOI_HOC": [{"url": IMG + "3-HANH-KHACH-PASSENGER.webp", "name": "3-HANH-KHACH-PASSENGER.webp"}],
        "NGUOI_CANBO": [{"url": IMG + "4-NHAN-VIEN-AN-NINH-OFFICER.webp", "name": "4-NHAN-VIEN-AN-NINH-OFFICER.webp"}],
        "NGUOI_DAY": [{"url": IMG + "2-ROBOT-GIA-SU-AI.webp", "name": "2-ROBOT-GIA-SU-AI.webp"}],
        "NEN_SOI": [{"url": IMG + "1-NEN-CONG-DO-KIM-LOAI.webp", "name": "1-NEN-CONG-DO-KIM-LOAI.webp"}],
        "NEN_HOC": [{"url": IMG + "1-NEN-CONG-DO-KIM-LOAI.webp", "name": "1-NEN-CONG-DO-KIM-LOAI.webp"}],
    },
    "LUOT": luot,
}
json.dump([V], open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(luot), "lượt ->", OUT)
