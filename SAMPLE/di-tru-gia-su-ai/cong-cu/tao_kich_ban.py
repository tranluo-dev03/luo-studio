"""Sinh SAMPLE/di-tru-gia-su-ai/KICH-BAN-DI-TRU-GIA-SU-AI.txt từ các bảng cảnh dưới đây (sửa ở đây rồi chạy lại):
    .venv\\Scripts\\python.exe SAMPLE\\di-tru-gia-su-ai\\cong-cu\\tao_kich_ban.py
Video mẫu: 1410_immigration ES_003 (67 s). Phân tích: ../PHAN-TICH-VIDEO-MAU.md.
MỘT dự án, 3 phần: (1) gọi điện cắt xen 2 nơi, (2) cảnh sát hỏi + robot nhỏ trên vai sửa câu, (3) ghép 2 lớp: người học + gia sư AI trong ô góc trên phải."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "KICH-BAN-DI-TRU-GIA-SU-AI.txt")

HEAD = """[HAU KY]:
loai: di-tru-gia-su-ai

[GHI CHU]:
Thể loại "di trú + gia sư AI" (video mẫu 1410_immigration ES_003, 67 s, tiếng Tây Ban Nha xen tiếng Anh). MỘT dự án 3 phần, Studio chạy bằng
app/production/types/di-tru-gia-su-ai/gen.py (logic chung types/_chung/nhieu_phan.py). Kịch bản sinh bằng cong-cu/tao_kich_ban.py.
  PHẦN 1 (cảnh thường, 5 cảnh): cuộc gọi điện thoại cắt xen hai nơi: Valeria (AMIGA) trong căn hộ cao tầng / Diego (HOC) trước cửa hàng tiện lợi.
         Mỗi cảnh MỘT người, mỗi cảnh một "Prompt ảnh" (khung đầu mới), ảnh tham chiếu giữ mặt.
  PHẦN 2 (cảnh thường, 11 cảnh): cảnh sát (CANHSAT, phải) hỏi Diego (HOC, trái) trên vỉa hè; robot nhỏ (ROBO, robot của người dùng thu nhỏ) hiện trên vai Diego sửa câu sai.
         Ba khung: rộng hai người (cảnh 1-3), cận Diego + robot trên vai (cảnh 4-5), rộng hai người + robot trên vai (cảnh 6-11; cảnh 8 ảnh mới cùng góc để mặt không trôi).
         Hai người đứng yên cách nhau ~1 m suốt phần 2; cảnh sát luôn nhìn Diego, không bao giờ nhìn camera.
  PHẦN 3 (ghép 2 lớp, 13 cảnh): Diego đứng trên vỉa hè (nền 9:16), gia sư AI (DAY) trong ô dọc bo góc viền trắng góc trên PHẢI; vào bằng nhoè 0,5 s.
  Hậu kỳ (post.py + config.json): phần 1-2 chữ trắng viền đen, phần 3 chữ vàng; câu sai đỏ + viền đỏ, câu đúng xanh + ✅, 💲 ở "no tengo dinero".
  Logo/badge "Talka AI" và dòng "POV: ..." trên cùng: KHÔNG gen (Thương hiệu / chưa làm).
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.
"""

AUDIO = "Audio: Chỉ giọng của một nhân vật, rõ, gần; phần còn lại im lặng. Không nhạc, không tiếng xe."
NEG_ANH = "No text, no letters, no logos, no readable signs anywhere. Output only the image."

# ---------------- PHẦN 1: gọi điện ----------------
P1 = """===== PHAN 1: GOI DIEN (CAT XEN HAI NOI) =====

[STYLE LOCK]:
Vertical 9:16 photorealistic video, natural daylight, the look of a real phone moment caught on camera. Each clip shows ONE person ALONE in their own place, talking on a mobile phone held to the ear; the other person of the call is never in the frame. The camera stays still. No text, no letters, no logos, no captions, no phone screen visible.

[CHAR LOCK]:
{{TEN_AMIGA}}, {{VAI_AMIGA}}: {{NGUOI_AMIGA}}. She is at home in her apartment. VOICE LOCK WOMAN: {{GIONG_AMIGA}}, the same in every clip.
{{TEN_HOC}}, {{VAI_HOC}}: {{NGUOI_HOC}}. He stands on the sidewalk outside a convenience store, holding {{DAO_CAFE}} in the left hand and the phone to his right ear. VOICE LOCK MAN: {{GIONG_HOC}}, the same in every clip.
RULE: the one person in the clip speaks one line with lip-sync, phone held to the ear, eyes slightly off to the side past the camera (never into the lens). When the line ends the mouth closes and the person stays still.

[SET LOCK]:
{{TEN_AMIGA}}'s place: {{NEN_NHA}}. {{TEN_HOC}}'s place: {{NEN_PHO}}. Nothing in the background moves.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no cut. The head stays steady: no nodding. The speaker starts right away in natural Mexican Spanish at about 3.5 words per second (short lines faster), like a real phone call, not actors, and finishes the line. After the last word: calm closed-mouth face, still until the end. No music, no traffic noise. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, readable signs, phone screen; a second person in the frame; looking into the lens; camera movement, zoom, cut; repeated nodding or head bobbing; two voices; face, hair or outfit changing; the phone vanishing or changing hands; background music; robotic voice; slow, dragged speech.
"""

ANH_AMIGA_RONG = ("Generate exactly one still image now, vertical 9:16, photorealistic. {{TEN_AMIGA}} ({{NGUOI_AMIGA}}) stands alone in {{NEN_NHA}}, framed from the head "
                  "down to the thighs, centred, the left arm folded across the waist, the right hand holding a black phone to the right ear, a worried frown, eyes looking "
                  "slightly off to the side past the camera. Mouth closed. " + NEG_ANH)
ANH_AMIGA_CAN = ("Generate exactly one still image now, vertical 9:16, photorealistic. Close-up of {{TEN_AMIGA}} ({{NGUOI_AMIGA}}) alone by the window of {{NEN_NHA}}: "
                 "head and shoulders, the face large in the upper half of the frame, slightly turned to the left, the right hand holding a black phone to the right ear, "
                 "a tense worried look, eyes looking off to the side past the camera, the skyline behind her right shoulder. Mouth closed. " + NEG_ANH)
ANH_HOC_PHONE = ("Generate exactly one still image now, vertical 9:16, photorealistic, bright midday sun. {{TEN_HOC}} ({{NGUOI_HOC}}) stands alone on the sidewalk of "
                 "{{NEN_PHO}}, framed from the head down to the thighs, slightly left of centre, the right hand holding a black phone to the right ear, the left hand "
                 "holding {{DAO_CAFE}} at waist height, the store's glass doors on the left behind him, the street and traffic lights on the right. A tense, puzzled look, "
                 "eyes slightly off to the side past the camera. Mouth closed. " + NEG_ANH)

# (người nói, prompt ảnh, diễn biến VN, khung cuối VN, hành động EN)
CANH1 = [
    ("AMIGA", ANH_AMIGA_RONG, "Valeria đứng trong phòng khách, khoanh tay trái, tay phải áp điện thoại, nói gấp và lo lắng.",
     "Valeria áp điện thoại, mặt lo, miệng khép.", "she speaks urgently and quietly, frowning"),
    ("HOC", ANH_HOC_PHONE, "Diego đứng trước cửa hàng, áp điện thoại, ngạc nhiên hỏi lại, lông mày nhíu.",
     "Diego áp điện thoại, cầm cốc cà phê, miệng khép.", "he frowns, puzzled, and asks back"),
    ("AMIGA", ANH_AMIGA_CAN, "Cận mặt Valeria bên cửa sổ, nói hạ giọng, chậm và chắc để Diego bình tĩnh; mặt nghiêm, KHÔNG cười.",
     "Valeria áp điện thoại, mặt nghiêm, miệng khép.", "she keeps her voice low, slow and steady so he stays calm; a serious, calm, reassuring face with no smile at any moment, the lips never curl up",
     "smiling; a grin; the corners of the mouth turning up"),
    ("HOC", ANH_HOC_PHONE, "Diego áp điện thoại, hoảng nhẹ, nói như thanh minh, lắc đầu một cái nhỏ.",
     "Diego áp điện thoại, cầm cốc, mặt lo, miệng khép.", "he answers defensively, a small shake of the head"),
    ("AMIGA", ANH_AMIGA_CAN, "Cận mặt Valeria, dịu giọng trấn an, mắt vẫn lo.",
     "Valeria áp điện thoại, mắt lo, miệng khép; hết phần 1.", "she softens her voice to calm him, still worried"),
]


def canh_p1(i, who, anh, dien, cuoi, act, neg_them=""):
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
        "Negative prompt: a second person; two voices; looking into the lens; text; camera movement; nodding" + (f"; {neg_them}." if neg_them else "."),
    ])


# ---------------- PHẦN 2: cảnh sát + robot nhỏ ----------------
P2 = """===== PHAN 2: CANH SAT HOI + ROBOT NHO TREN VAI =====

[STYLE LOCK]:
Vertical 9:16 photorealistic video on a sunny city sidewalk, bright midday sun, natural colours, the look of a real moment caught on camera. The tiny robot, when present, is a glossy photorealistic CGI miniature humanoid robot sitting naturally on the young man's shoulder; the officer never notices it. The officer and the young man stand still about one metre apart (an arm's length, a clear gap of sidewalk between them) for the whole scene; nobody steps toward the other. The camera stays still. No text, no letters, no logos, no lettering on the uniform, badge, store or cup.

[CHAR LOCK]:
The {{VAI_CANHSAT}}, {{TEN_CANHSAT}} ({{POS_CANHSAT}}): {{NGUOI_CANHSAT}}. VOICE LOCK OFFICER: {{GIONG_CANHSAT}}, the same in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}, holding {{DAO_CAFE}} in the left hand the whole time. VOICE LOCK YOUNG MAN: {{GIONG_HOC}}, the same in every clip.
The {{VAI_ROBO}}, {{TEN_ROBO}} ({{POS_ROBO}}): {{NGUOI_ROBO}}; it only appears in clips that say so, always sitting on the young man's shoulder on the left side of the frame. VOICE LOCK TINY ROBOT: {{GIONG_ROBO}}.
EYE LINE: the officer {{NHIN_CANHSAT}}; the young man {{NHIN_HOC}}; the tiny robot {{NHIN_ROBO}} when it speaks. Only the tiny robot ever looks into the lens; the officer never does.
When silent: the officer {{NGHE_CANHSAT}}; the young man {{NGHE_HOC}}; the tiny robot {{NGHE_ROBO}}.
RULE: in each clip exactly ONE character speaks one line with lip-sync; the others stay silent with the mouth closed and react only with the eyes and face. The two men are clearly different: the officer is in his forties in a navy uniform, the young man is about 20 in a white T-shirt and a backwards black cap.

[SET LOCK]:
{{NEN_PHO}}. Nothing in the background moves: parked cars, still palm trees, no passers-by.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no cut. Heads stay steady: no nodding. The two men keep the same distance, about one metre apart. The speaker starts right away at about 4 words per second (short questions up to 5), like real people caught on camera, not actors, and finishes the line. After the last word everyone keeps a calm closed-mouth face and stays still until the end. No music, no traffic noise. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, lettering on uniform, badge, store or cup; the words LEFT or RIGHT written in the frame; camera movement, zoom, cut; the officer looking into the lens or at the camera; the two men stepping closer, walking toward each other or standing shoulder to shoulder; repeated nodding or head bobbing; a beard, stubble or moustache on the young man; two voices in one clip; a silent character moving the mouth; the officer and the young man looking alike; extra people; the tiny robot in a clip that does not mention it; the tiny robot floating, flying or growing; a chibi or cartoon toy robot; the coffee cup vanishing; background music; robotic voice; slow, dragged speech.
"""

ANH_RONG = ("Generate exactly one still image now, vertical 9:16, photorealistic, bright midday sun. A fixed camera at chest height on the sidewalk of {{NEN_PHO}}. "
            "On the left half: {{TEN_HOC}} ({{NGUOI_HOC}}), framed from the head down to the thighs, body turned three-quarters to the right toward the officer, holding "
            "{{DAO_CAFE}} in the left hand at waist height, the store's glass doors behind him. On the right half, about one metre away from him with a clear gap of sidewalk between them: {{TEN_CANHSAT}} ({{NGUOI_CANHSAT}}), "
            "framed from the head down to the thighs, in a three-quarter left profile, his head and eyes turned to the young man's face, hands relaxed at the belt. The two look at each other; "
            "mouths closed; nobody looks into the lens. Only these two people. " + NEG_ANH)
ANH_CAN_ROBO = ("Generate exactly one still image now, vertical 9:16, photorealistic, bright midday sun, the store's shelves and glass doors softly blurred behind. "
                "A close shot of {{TEN_HOC}} ({{NGUOI_HOC}}) from the chest up, on the right half of the frame, in a right-side profile looking off to the right toward "
                "the officer just outside the right edge of the frame. On his shoulder on the left side of the frame sits {{TEN_ROBO}} ({{NGUOI_ROBO}}), a glossy photorealistic "
                "CGI miniature, its head at the height of his jaw, legs dangling over his shoulder, facing the camera with a bright friendly look, lips gently together. Nobody else in the frame. " + NEG_ANH)
ANH_RONG_ROBO = ANH_RONG.replace("Only these two people. ",
                                 "On the young man's shoulder on the left side of the frame sits {{TEN_ROBO}} ({{NGUOI_ROBO}}), small, about the size of his head, a glossy photorealistic "
                                 "CGI miniature, still, lips together. The officer does not notice it. Only these two people and the tiny robot. ")

# (người nói, khung: 'rong' | 'can' | 'rong_robo', prompt ảnh mới?, diễn biến VN, khung cuối VN, hành động EN hoặc None)
CANH2 = [
    ("CANHSAT", "rong", ANH_RONG, "Cảnh sát đứng cách Diego ~1 m, nhìn Diego, lịch sự chào và hỏi; Diego cầm cốc cà phê, nhìn cảnh sát, hơi căng. Không ai bước lại gần.",
     "hai người nhìn nhau, miệng khép, đứng im, vẫn cách ~1 m.", "the officer speaks politely and calmly, looking at the young man's face"),
    ("CANHSAT", "rong", None, "Cảnh sát hỏi tiếp, nghiêm nhưng lịch sự; Diego nghe, nuốt khan.",
     "hai người nhìn nhau, miệng khép.", None),
    ("HOC", "rong", None, "Diego trả lời ngập ngừng, không chắc chắn; cảnh sát nghe, mặt bình thản.",
     "hai người nhìn nhau, miệng khép.", "the young man hesitates, unsure"),
    ("ROBO", "can", ANH_CAN_ROBO, "Cận Diego nhìn sang phải về phía cảnh sát; robot nhỏ ngồi trên vai (bên trái khung) nhìn ống kính, nói vui vẻ, lắc đầu nhỏ ở chữ \"No\"; Diego im, miệng khép.",
     "robot ngồi trên vai mỉm cười, miệng khép; Diego nhìn sang phải, miệng khép.", "the tiny robot gives a small playful head shake on \"No\", then says the English phrase clearly"),
    ("HOC", "can", None, "Diego nói lại câu đúng với cảnh sát (ngoài khung bên phải), tự tin hơn; robot nhỏ ngồi im mỉm cười, miệng khép.",
     "Diego mỉm cười nhẹ nhìn sang phải; robot ngồi im; miệng khép.", "the young man says it clearly and more confidently; the tiny robot stays still"),
    ("CANHSAT", "rong_robo", ANH_RONG_ROBO, "Khung rộng hai người, robot nhỏ ngồi im trên vai Diego; cảnh sát hỏi tiếp.",
     "hai người nhìn nhau, robot ngồi im, miệng khép.", None),
    ("HOC", "rong_robo", None, "Diego trả lời tự tin, mỉm cười nhẹ; cảnh sát nghe, nhìn Diego, đầu yên.",
     "hai người nhìn nhau, miệng khép.", None),
    ("CANHSAT", "rong_robo", ANH_RONG_ROBO, "Cảnh sát ngạc nhiên, khen với nụ cười thán phục, vẫn nhìn Diego. (Ảnh mới cùng góc: mặt Diego lấy lại từ ảnh tham chiếu, không râu.)",
     "cảnh sát mỉm cười; Diego cười; miệng khép.", "the officer raises his eyebrows with an impressed smile"),
    ("HOC", "rong_robo", None, "Diego cười tươi, cảm ơn rồi kể thêm, hào hứng.",
     "Diego cười; cảnh sát mỉm cười nhìn; miệng khép.", "the young man smiles widely"),
    ("CANHSAT", "rong_robo", None, "Cảnh sát tò mò hỏi, hơi nghiêng đầu, nhìn Diego.",
     "hai người nhìn nhau, miệng khép.", "the officer tilts his head slightly, curious, still looking at the young man"),
    ("HOC", "rong_robo", None, "Giữ nguyên khung cuối cảnh trước: Diego trả lời tự tin, tự hào, mỉm cười; cảnh sát nghe, nhìn Diego; robot ngồi im trên vai.",
     "Diego mỉm cười; cảnh sát nhìn Diego; miệng khép; hết phần 2.", "the young man answers proudly with a confident smile; the officer listens, looking at him"),
]


def canh_p2(i, who, khung, anh, dien, cuoi, act):
    n = i + 1
    robo = khung != "rong"
    bc = {"rong": "khung rộng: Diego trái, cảnh sát phải, vỉa hè trước cửa hàng; không robot",
          "can": "cận Diego (phải khung, nhìn sang phải về phía cảnh sát ngoài khung), robot nhỏ ngồi trên vai bên trái khung",
          "rong_robo": "khung rộng: Diego trái, cảnh sát phải; robot nhỏ ngồi im trên vai Diego"}[khung]
    lines = [f"CẢNH {n} (0:{(n - 1) * 4:02d}–0:{n * 4:02d}): Lượt {n}",
             f"Bối cảnh: {bc}; nắng trưa; không chữ.",
             f"Voice: (English/Spanish, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}",
             "Khung đầu: ảnh mới theo Prompt ảnh." if anh else "Khung đầu: khung cuối của cảnh trước (cùng góc máy).",
             "Khung cuối: " + cuoi + " Khung này là khung đầu của cảnh sau.",
             "Diễn biến: " + dien + " Nói xong mọi người đứng im đến hết clip."]
    if anh:
        lines.append("Prompt ảnh: " + anh)
    who_en = {"CANHSAT": "the officer", "HOC": "the young man", "ROBO": "the tiny robot"}[who]
    v = (f"Prompt video: STYLE LOCK, SET LOCK. Start exactly from the start-frame image and keep its framing. CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} "
         f"Only {who_en} speaks, with lip-sync; everyone else keeps the mouth closed. ")
    v += ("The tiny robot is on the young man's shoulder" + (" and stays still unless it is the speaker. " if who != "ROBO" else ". ")) if robo else "The tiny robot is NOT in this clip. "
    if act:
        v += f"While speaking: {act}. "
    if khung != "can":
        v += "The officer keeps looking at the young man the whole clip, never at the camera; the two men stay about one metre apart. "
    v += "After the line everyone stays still until the end. VIDEO SUFFIX."
    neg = ("Negative prompt: two voices; a silent character moving the mouth; text; camera movement; the officer looking at the camera; the men moving closer; nodding; "
           "a beard or stubble on the young man" + ("; the tiny robot." if not robo else "."))
    return "\n".join(lines + [v, AUDIO, neg])


# ---------------- PHẦN 3: ghép 2 lớp ----------------
P3 = """===== PHAN 3: DIEGO + GIA SU AI (GHEP 2 LOP, O GOC PHAI) | vao: nhoe 0.5 =====

[GHEP HAI LOP]:
nen: HOC
khung DAY: 0.615, 0.012, 0.37, 0.32
bo goc: 0.08
vien: #FFFFFF, 3
noi: lien
nghe: moi canh

[STYLE LOCK]:
Vertical short-form social video look, bright midday sun, crisp focus on the face, realistic skin, hair and fabric detail. No text, captions, logos, icons or watermarks anywhere in the frame.

[NHAN VAT HOC]:
{{TEN_HOC}}: {{NGUOI_HOC}}. The reference photo shows only the face, hair and clothing: its grey background and pose are NOT part of the scene. He stands on the sidewalk of {{NEN_PHO}}, the store fronts along the left side, the street on the right. Filmed by a camera held in front of him at chest height (nobody else visible, no arm, no phone in the frame): framed from the top of the head down to the thighs, the top of the head at about 12% of the frame height, the face centred at about 38% of the frame width (left of centre); he holds {{DAO_CAFE}} in the left hand (right side of the frame) at waist height. The upper-right quarter of the frame shows only empty blue sky, palm trees and the street, nothing important: no window, no screen, no inset. He is the only figure in the whole frame; the sky and the street behind him hold no other figure or object in the air. He looks into the lens as if talking to a friend on a video call; when searching for an English word, a brief glance up to the side, then back to the lens. Small natural hand gestures with the free right hand at chest height; the head stays steady, no nodding. The camera is steady with a very light handheld feel and keeps the same distance the whole clip: it never moves closer, the framing stays head to thighs, his head stays in the left two thirds of the frame and never enters the upper-right quarter. VOICE: {{GIONG_HOC}}, the same timbre, pitch and loudness in every clip.

[NGHE HOC]:
{{TEN_HOC}} waits for the AI tutor: attentive expression and a soft smile, eyes on the lens, slow natural blinks, the head steady, the coffee cup held still. The lips stay gently pressed together the whole clip; the head stays mostly still.

[NHAN VAT DAY]:
{{TEN_DAY}}: {{NGUOI_DAY}}; a clean, glossy, high-end photorealistic CGI robot. Portrait frame: the robot faces the camera, centred left-right, seen from a small gap above the halo ring down to the waist, the head in the upper third, the shoulders filling the middle of the width. Behind it: {{NEN_DAY}}. The camera is locked off and never moves. The robot looks straight into the lens. While speaking the lips move in clear sync with the words, with small head tilts, raised eyebrows and a warm smile, like a friendly teacher. VOICE: {{GIONG_DAY}}, the same timbre, pitch and loudness in every clip.

[NGHE DAY]:
{{TEN_DAY}} waits calmly: a gentle closed-mouth smile, slow natural blinks, a tiny head tilt now and then. The lips stay gently pressed together the whole clip; the head stays mostly still.

[VIDEO SUFFIX]:
Natural spontaneous conversational delivery, not text-to-speech, not an announcer. Both speak natural Mexican Spanish and switch to English only for the English words in the line. The tutor talks clearly and warmly at about 3.5 words per second; the young man a little slower, with small hesitations. The line starts right away, light natural breaths. Clean close voice, no music, no traffic noise, no echo.

[NEGATIVE]:
text, letters, captions, subtitles, logos, icons, watermark; phone screen or app interface in the frame; picture-in-picture inside the clip; a second person; a toy robot or figurine on the shoulder; hands or a phone coming into the frame; camera cuts, zoom, push-in, strong shake; repeated nodding or head bobbing; a beard, stubble or moustache on the young man; the face near the upper-right corner; face morphing, outfit change, hair change; distorted face; extra fingers; jerky or exaggerated gestures; the coffee cup vanishing or changing hands; slow, dragged speech; robotic or announcer voice; background music; echo
"""


def main():
    body = (HEAD + "\n" + P1 + "\n" + "\n\n".join(canh_p1(i, *c) for i, c in enumerate(CANH1)) + "\n\n"
            + P2 + "\n" + "\n\n".join(canh_p2(i, *c) for i, c in enumerate(CANH2)) + "\n\n" + P3)
    open(OUT, "w", encoding="utf-8", newline="\n").write(body)
    print("Đã ghi", os.path.normpath(OUT), f"({len(CANH1)} + {len(CANH2)} cảnh + phần ghép 2 lớp, {len(body)} ký tự)")


if __name__ == "__main__":
    main()
