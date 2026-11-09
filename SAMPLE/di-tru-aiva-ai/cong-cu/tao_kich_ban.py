"""Sinh SAMPLE/di-tru-aiva-ai/KICH-BAN-DI-TRU-AIVA-AI.txt từ các bảng cảnh dưới đây (sửa ở đây rồi chạy lại):
    .venv\\Scripts\\python.exe SAMPLE\\di-tru-aiva-ai\\cong-cu\\tao_kich_ban.py
Nhân bản từ di-tru-gia-su-ai (08/11/2026) theo kịch bản "oder 7" (file CSV người dùng đưa, app Aiva AI):
MỘT dự án, 3 phần: (1) bố/con trai gọi điện báo có agentes de inmigración (cắt xen 2 nơi), (2) cảnh sát hỏi (KHÔNG có robot nhỏ trên vai,
một góc máy), (3) ghép 2 lớp: hành khách + gia sư AI trong ô góc trên phải (gồm phần 3–5 của CSV: demo, pain point, CTA).
Hành khách (HOC) đổi giới/tuổi theo biến thể -> mọi đại từ của HOC dùng token {{HE_HOC}} / {{HIS_HOC}} / {{HIM_HOC}}, vai {{VAI_HOC}}."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "KICH-BAN-DI-TRU-AIVA-AI.txt")

HEAD = """[HAU KY]:
loai: di-tru-aiva-ai

[GHI CHU]:
Thể loại "di trú + Aiva AI" (kịch bản "oder 7", tiếng Tây Ban Nha xen tiếng Anh), nhân bản từ di-tru-gia-su-ai. MỘT dự án 3 phần, Studio chạy bằng
app/production/types/di-tru-aiva-ai/gen.py (logic chung types/_chung/nhieu_phan.py). Kịch bản sinh bằng cong-cu/tao_kich_ban.py.
  PHẦN 1 (cảnh thường, 5 cảnh): cuộc gọi cắt xen hai nơi: người gọi (BO: bố, hoặc con trai khi hành khách đã lớn tuổi) trong nhà / hành khách (HOC) trên vỉa hè.
         Mỗi cảnh MỘT người, mỗi cảnh một "Prompt ảnh" (khung đầu mới).
  PHẦN 2 (cảnh thường, 10 cảnh): cảnh sát (CANHSAT, phải) hỏi hành khách (HOC, trái) trên vỉa hè; MỘT góc máy rộng, cảnh 1 ảnh mới, cảnh sau nối khung.
  PHẦN 3 (ghép 2 lớp, 15 cảnh): hành khách đứng trên vỉa hè (nền 9:16), gia sư AI (DAY) trong ô dọc bo góc viền trắng góc trên PHẢI; vào bằng nhoè 0,5 s.
  Hậu kỳ (post.py + config.json): phần 1-2 chữ trắng, phần 3 chữ vàng; câu sai đỏ + viền đỏ, 💲 ở "no tengo dinero".
  Logo "Aiva AI": KHÔNG gen (Thương hiệu).
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.
"""

AUDIO = "Audio: Chỉ giọng nói của một nhân vật, rõ, gần; phần còn lại im lặng. Không hát, không ngân, không giai điệu, không nhạc, không tiếng xe."
NEG_ANH = "No text, no letters, no logos, no readable signs anywhere. Output only the image."

# ---------------- PHẦN 1: gọi điện ----------------
P1 = """===== PHAN 1: GOI DIEN (CAT XEN HAI NOI) =====

[STYLE LOCK]:
Vertical 9:16 photorealistic video, natural daylight, the look of a real phone moment caught on camera. Each clip shows ONE person ALONE in their own place, talking on a mobile phone held to the ear; the other person of the call is never in the frame. The camera stays still. No text, no letters, no logos, no captions, no phone screen visible.

[CHAR LOCK]:
{{TEN_BO}}, {{VAI_BO}}: {{NGUOI_BO}}. He is at home. VOICE LOCK CALLER: {{GIONG_BO}}, the same in every clip.
{{TEN_HOC}}, the {{VAI_HOC}}: {{NGUOI_HOC}}. {{TEN_HOC}} stands on the sidewalk outside a convenience store, holding {{DAO_CAFE}} in the left hand and the phone to the right ear. VOICE LOCK {{VAI_HOC}}: {{GIONG_HOC}}, the same in every clip.
RULE: the one person in the clip speaks one line with lip-sync, phone held to the ear, eyes slightly off to the side past the camera (never into the lens). When the line ends the mouth closes and the person stays still.

[SET LOCK]:
{{TEN_BO}}'s place: {{NEN_NHA}}. {{TEN_HOC}}'s place: {{NEN_PHO}}. Nothing in the background moves.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no cut. The speaker starts right away in natural Mexican Spanish at about 3.5 words per second (short lines faster), like a real phone call, not actors, and finishes the line. After the last word: calm closed-mouth face, still until the end. No music, no traffic noise. Speech only: nobody sings, hums or vocalises, no held notes, no melody; between sentences there is only silence or a short natural breath. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, readable signs, phone screen; a second person in the frame; looking into the lens; camera movement, zoom, cut; two voices; singing, humming, vocalising, a held musical note, a melody; face, hair or outfit changing; the phone vanishing or changing hands; background music; robotic voice; slow, dragged speech.
"""

ANH_BO_RONG = ("Generate exactly one still image now, vertical 9:16, photorealistic. {{TEN_BO}} ({{NGUOI_BO}}) stands alone in {{NEN_NHA}}, framed from the head "
               "down to the thighs, centred, the left hand on the hip, the right hand holding a black phone to the right ear, a worried frown, eyes looking "
               "slightly off to the side past the camera. Mouth closed. " + NEG_ANH)
ANH_BO_CAN = ("Generate exactly one still image now, vertical 9:16, photorealistic. Close-up of {{TEN_BO}} ({{NGUOI_BO}}) alone by the window of {{NEN_NHA}}: "
              "head and shoulders, the face large in the upper half of the frame, slightly turned to the left, the right hand holding a black phone to the right ear, "
              "a tense worried look, eyes looking off to the side past the camera. Mouth closed. " + NEG_ANH)
ANH_HOC_PHONE = ("Generate exactly one still image now, vertical 9:16, photorealistic, bright midday sun. {{TEN_HOC}} ({{NGUOI_HOC}}) stands alone on the sidewalk of "
                 "{{NEN_PHO}}. MEDIUM SHOT, not a full-body shot: the frame starts just above the hair and its bottom edge cuts across mid-thigh; the knees, lower legs and feet are outside the frame. Slightly left of centre, the right hand holding a black phone to the right ear, the left hand "
                 "holding {{DAO_CAFE}} at waist height, the store's glass doors on the left behind {{HIM_HOC}}, the street and traffic lights on the right. A tense, puzzled look, "
                 "eyes slightly off to the side past the camera. Mouth closed. " + NEG_ANH)

# (người nói, prompt ảnh, diễn biến VN, khung cuối VN, hành động EN)
CANH1 = [
    ("BO", ANH_BO_RONG, "Người gọi đứng trong phòng khách, tay trái chống hông, tay phải áp điện thoại, nói gấp và lo lắng.",
     "Người gọi áp điện thoại, mặt lo, miệng khép.", "he speaks urgently and quietly, frowning"),
    ("HOC", ANH_HOC_PHONE, "Hành khách đứng trước cửa hàng, áp điện thoại, ngạc nhiên hỏi lại, lông mày nhíu.",
     "Hành khách áp điện thoại, cầm cốc cà phê, miệng khép.", "{{HE_HOC}} frowns, puzzled, and asks back"),
    ("BO", ANH_BO_CAN, "Cận mặt người gọi bên cửa sổ, nói hạ giọng, mắt lo lắng liếc sang bên.",
     "Người gọi áp điện thoại, mặt căng, miệng khép.", "he lowers his voice, eyes darting to the side, worried"),
    ("HOC", ANH_HOC_PHONE, "Hành khách áp điện thoại, hoảng nhẹ, nói như thanh minh, lắc đầu một cái nhỏ.",
     "Hành khách áp điện thoại, cầm cốc, mặt lo, miệng khép.", "{{HE_HOC}} answers defensively, a small shake of the head"),
    ("BO", ANH_BO_CAN, "Cận mặt người gọi, dịu giọng trấn an, mắt vẫn lo.",
     "Người gọi áp điện thoại, mắt lo, miệng khép; hết phần 1.", "he softens his voice to calm {{HIM_HOC}}, still worried"),
]


def canh_p1(i, who, anh, dien, cuoi, act):
    n = i + 1
    ten = "{{TEN_%s}}" % who
    return "\n".join([
        f"CẢNH {n} (0:{(n - 1) * 3:02d}–0:{n * 3:02d}): Lượt {n}",
        f"Bối cảnh: chỉ một người trong khung ({ten}), đang nghe/nói điện thoại; không có người thứ hai, không chữ.",
        f"Voice: (Spanish, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}",
        "Khung đầu: ảnh mới theo Prompt ảnh.",
        "Khung cuối: " + cuoi,
        "Diễn biến: " + dien + " Nói xong đứng im đến hết clip.",
        "Prompt ảnh: " + anh,
        f"Prompt video: STYLE LOCK, SET LOCK. Start exactly from the start-frame image and keep its framing. CHAR LOCK. In this clip only {ten} is in the frame: "
        f"{{{{LUOT_{n}}}}} {ten} speaks with lip-sync into the phone; {act}. The phone stays at the ear. After the line, still until the end. VIDEO SUFFIX.",
        AUDIO,
        "Negative prompt: a second person; two voices; looking into the lens; text; camera movement.",
    ])


# ---------------- PHẦN 2: cảnh sát (một góc máy, không robot) ----------------
P2 = """===== PHAN 2: CANH SAT HOI =====

[STYLE LOCK]:
Vertical 9:16 photorealistic video on a sunny city sidewalk, bright midday sun, natural colours, the look of a real moment caught on camera. One fixed camera angle for the whole part. No text, no letters, no logos, no lettering on the uniform, badge, store or cup.

[CHAR LOCK]:
The {{VAI_CANHSAT}}, {{TEN_CANHSAT}} ({{POS_CANHSAT}}): {{NGUOI_CANHSAT}}. VOICE LOCK OFFICER: {{GIONG_CANHSAT}}, the same in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}, holding {{DAO_CAFE}} in the left hand the whole time. VOICE LOCK {{VAI_HOC}}: {{GIONG_HOC}}, the same in every clip.
EYE LINE: the officer {{NHIN_CANHSAT}}; the {{VAI_HOC}} {{NHIN_HOC}}. Nobody looks into the lens.
When silent: the officer {{NGHE_CANHSAT}}; the {{VAI_HOC}} {{NGHE_HOC}}.
RULE: in each clip exactly ONE person speaks one line with lip-sync; the other stays silent with the mouth closed and reacts only with the eyes and face. The two look clearly different: the officer is a man in his forties in a navy uniform; the {{VAI_HOC}} wears the clothes described above.

[SET LOCK]:
{{NEN_PHO}}. Nothing in the background moves: parked cars, still palm trees, no passers-by.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no cut. The speaker starts right away at about 4 words per second (short questions up to 5), like real people caught on camera, not actors, and finishes the line. After the last word both keep a calm closed-mouth face and stay still until the end. No music, no traffic noise. Speech only: nobody sings, hums or vocalises, no held notes, no melody; between sentences there is only silence or a short natural breath. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, lettering on uniform, badge, store or cup; the words LEFT or RIGHT written in the frame; camera movement, zoom, cut; two voices in one clip; singing, humming, vocalising, a held musical note, a melody; a silent person moving the mouth; the two people looking alike; extra people; a robot or figurine; the coffee cup vanishing; background music; robotic voice; slow, dragged speech.
"""

ANH_RONG = ("Generate exactly one still image now, vertical 9:16, photorealistic, bright midday sun. A fixed camera at chest height on the sidewalk of {{NEN_PHO}}. "
            "Both people are in a MEDIUM SHOT, not a full-body shot: the frame starts just above their hair and its bottom edge cuts across their mid-thighs; the knees, lower legs and feet are outside the frame. On the left half: {{TEN_HOC}} ({{NGUOI_HOC}}), body turned three-quarters to the right toward the officer, holding "
            "{{DAO_CAFE}} in the left hand at waist height, the store's glass doors behind {{HIM_HOC}}. On the right half, close by: {{TEN_CANHSAT}} ({{NGUOI_CANHSAT}}), "
            "in a three-quarter left profile facing the {{VAI_HOC}}, hands relaxed at the belt. The two look at each other; "
            "mouths closed; nobody looks into the lens. Only these two people. " + NEG_ANH)

# (người nói, prompt ảnh mới?, diễn biến VN, khung cuối VN, hành động EN hoặc None)
CANH2 = [
    ("CANHSAT", ANH_RONG, "Cảnh sát đứng cạnh hành khách, lịch sự chào và hỏi; hành khách cầm cốc cà phê, nhìn cảnh sát, hơi căng.",
     "hai người nhìn nhau, miệng khép, đứng im.", "the officer gives a small polite nod as he starts"),
    ("HOC", None, "Hành khách trả lời lịch sự, cười gượng; cảnh sát nghe.",
     "hai người nhìn nhau, miệng khép.", "a polite, slightly tense smile"),
    ("CANHSAT", None, "Cảnh sát hỏi tiếp, nghiêm nhưng lịch sự; hành khách nghe, nuốt khan.",
     "hai người nhìn nhau, miệng khép.", None),
    ("HOC", None, "Hành khách trả lời ngắn, gật nhẹ.",
     "hai người nhìn nhau, miệng khép.", "a small nod"),
    ("CANHSAT", None, "Cảnh sát hỏi, mặt bình thản.",
     "hai người nhìn nhau, miệng khép.", None),
    ("HOC", None, "Hành khách trả lời tự tin, mỉm cười nhẹ; cảnh sát nghe, gật nhẹ.",
     "hai người nhìn nhau, miệng khép.", "a confident small smile"),
    ("CANHSAT", None, "Cảnh sát ngạc nhiên, khen với nụ cười thán phục.",
     "cảnh sát mỉm cười; hành khách cười; miệng khép.", "the officer raises his eyebrows with an impressed smile"),
    ("HOC", None, "Hành khách cười tươi, cảm ơn rồi kể thêm.",
     "hành khách cười; cảnh sát mỉm cười nhìn; miệng khép.", "a wide, happy smile"),
    ("CANHSAT", None, "Cảnh sát tò mò hỏi, hơi nghiêng đầu.",
     "hai người nhìn nhau, miệng khép.", "the officer tilts his head, curious"),
    ("HOC", None, "Hành khách tự hào kể về Aiva AI, nhún vai nhẹ ở chữ \"That's it\".",
     "hành khách mỉm cười tự hào; cảnh sát gật; miệng khép; hết phần 2.", "proud and relaxed, the whole line in one continuous spoken flow with no pause after the app name, a small shrug at the end"),
]


def canh_p2(i, who, anh, dien, cuoi, act):
    n = i + 1
    lines = [f"CẢNH {n} (0:{(n - 1) * 4:02d}–0:{n * 4:02d}): Lượt {n}",
             "Bối cảnh: khung rộng: hành khách trái, cảnh sát phải, vỉa hè trước cửa hàng; nắng trưa; không chữ.",
             f"Voice: (English, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}",
             "Khung đầu: ảnh mới theo Prompt ảnh." if anh else "Khung đầu: khung cuối của cảnh trước (cùng góc máy).",
             "Khung cuối: " + cuoi + " Khung này là khung đầu của cảnh sau.",
             "Diễn biến: " + dien + " Nói xong cả hai đứng im đến hết clip."]
    if anh:
        lines.append("Prompt ảnh: " + anh)
    who_en = {"CANHSAT": "the officer", "HOC": "the {{VAI_HOC}}"}[who]
    v = (f"Prompt video: STYLE LOCK, SET LOCK. Start exactly from the start-frame image and keep its framing. CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} "
         f"Only {who_en} speaks, with lip-sync; the other keeps the mouth closed. ")
    if act:
        v += f"While speaking: {act}. "
    v += "After the line both stay still until the end. VIDEO SUFFIX."
    return "\n".join(lines + [v, AUDIO, "Negative prompt: two voices; a silent person moving the mouth; text; camera movement."])


# ---------------- PHẦN 3: ghép 2 lớp ----------------
P3 = """===== PHAN 3: HANH KHACH + GIA SU AI (GHEP 2 LOP, O GOC PHAI) | vao: nhoe 0.5 =====

[GHEP HAI LOP]:
nen: HOC
khung DAY: 0.615, 0.012, 0.37, 0.32
bo goc: 0.08
vien: #FFFFFF, 3
noi: lien
nghe: moi canh

[STYLE LOCK]:
Vertical video filmed as one single continuous locked-off shot, bright midday sun, crisp focus on the face, realistic skin, hair and fabric detail. No text, captions, logos, icons or watermarks anywhere in the frame.

[NHAN VAT HOC]:
{{TEN_HOC}}, the {{VAI_HOC}}: {{NGUOI_HOC}}. The reference photo shows only the face, hair and clothing: its plain green background, standing pose and full-body framing are NOT part of the scene. {{TEN_HOC}} stands on the sidewalk of {{NEN_PHO}}, the store fronts along the left side, the street on the right. Filmed by a camera on a fixed tripod at chest height (nobody else visible, no arm, no phone in the frame). MEDIUM SHOT, not a full-body shot: the frame starts just above the hair and its bottom edge cuts across mid-thigh; the knees, lower legs and feet are outside the frame; {{TEN_HOC}} stands on the LEFT side of the frame: the head is in the upper third of the frame, the centre of the face about 30% of the frame width from the left edge, the whole head and hair to the left of the 55% vertical line; {{HE_HOC}} holds {{DAO_CAFE}} in the left hand (right side of the frame) at waist height. The right 45% of the upper third of the frame shows only empty blue sky, palm trees and the street, nothing important: no window, no screen, no inset. {{TEN_HOC}} is the only figure in the whole frame; the sky and the street hold no other figure or object in the air. {{HE_HOC}} looks into the lens as if talking to a friend on a video call; when searching for an English word, a brief glance up to the side, then back to the lens. Small natural nods and hand gestures with the free right hand at chest height. The camera never moves: no zoom in, no zoom out, no punch-in, no jump cut, no reframing. One single continuous shot with exactly the framing of the first frame from the first frame to the last; the head and hair stay to the left of the 55% vertical line the whole clip and never lean into the upper-right area. VOICE: {{GIONG_HOC}}, the same timbre, pitch and loudness in every clip.

[NGHE HOC]:
{{TEN_HOC}} waits for the AI tutor: attentive expression and a soft smile, eyes on the lens, slow natural blinks, a small nod now and then, the coffee cup held still. The lips stay gently pressed together the whole clip; the head stays mostly still.

[NHAN VAT DAY]:
{{TEN_DAY}}: {{NGUOI_DAY}}; a clean, glossy, high-end photorealistic CGI robot. Portrait frame: the robot faces the camera, centred left-right, seen from a small gap above the halo ring down to the waist, the head in the upper third, the shoulders filling the middle of the width. Behind it: {{NEN_DAY}}. The camera is locked off and never moves. The robot looks straight into the lens. While speaking the lips move in clear sync with the words, with small head tilts, raised eyebrows and a warm smile, like a friendly teacher. VOICE: {{GIONG_DAY}}, the same timbre, pitch and loudness in every clip.

[NGHE DAY]:
{{TEN_DAY}} waits calmly: a gentle closed-mouth smile, slow natural blinks, a tiny head tilt now and then. The lips stay gently pressed together the whole clip; the head stays mostly still.

[VIDEO SUFFIX]:
One single continuous shot on a fixed tripod, exactly the framing of the first frame until the last frame; no zoom, no punch-in, no cut, even when the line is short. Natural spontaneous conversational delivery, not text-to-speech, not an announcer. Both speak natural Mexican Spanish and switch to English only for the English words in the line. The tutor talks clearly and warmly at about 3.5 words per second; the {{VAI_HOC}} a little slower, with small hesitations. The line starts right away, light natural breaths. Clean close voice, no music, no traffic noise, no echo. Speech only: nobody sings, hums or vocalises, no held notes, no melody; between sentences there is only silence or a short natural breath.

[NEGATIVE]:
text, letters, captions, subtitles, logos, icons, watermark; green screen or plain studio background; phone screen or app interface in the frame; picture-in-picture inside the clip; a second person; a toy robot or figurine; hands or a phone coming into the frame; camera cuts, jump cuts, zoom in, zoom out, push-in, punch-in, reframing, camera shake; a full-body wide shot, visible knees or feet; face morphing, outfit change, hair change; distorted face; extra fingers; jerky or exaggerated gestures; the coffee cup vanishing or changing hands; slow, dragged speech; robotic or announcer voice; singing, humming, vocalising, a held musical note, a melody; background music; echo
"""


def main():
    body = (HEAD + "\n" + P1 + "\n" + "\n\n".join(canh_p1(i, *c) for i, c in enumerate(CANH1)) + "\n\n"
            + P2 + "\n" + "\n\n".join(canh_p2(i, *c) for i, c in enumerate(CANH2)) + "\n\n" + P3)
    open(OUT, "w", encoding="utf-8", newline="\n").write(body)
    print("Đã ghi", os.path.normpath(OUT), f"({len(CANH1)} + {len(CANH2)} cảnh + phần ghép 2 lớp, {len(body)} ký tự)")


if __name__ == "__main__":
    main()
