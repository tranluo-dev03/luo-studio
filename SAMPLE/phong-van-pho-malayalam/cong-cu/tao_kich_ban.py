"""Sinh lại SAMPLE/phong-van-pho-malayalam/KICH-BAN-PHONG-VAN-PHO-MALAYALAM.txt (11 cảnh phần 1 + phần 2 ghép 2 lớp trên/dưới).
Video mẫu: "1510_interview street hindi_005 (11)" (76,9 giây, 720x1280, app Aiva AI). Tên file ghi "hindi" nhưng lời và phụ đề là tiếng MALAYALAM xen tiếng Anh.
Sửa bảng SC (từng cảnh) hoặc các khối chữ rồi chạy:  runtime\\python.exe SAMPLE\\phong-van-pho-malayalam\\cong-cu\\tao_kich_ban.py
Số đo (SAMPLE/_chung/video-moi.py danh-gia): phần 1 0-25,7 s, máy đứng yên (rung nhẹ 22,6-25,7 s), 8 cảnh cắt nhưng cùng một góc qua vai,
chỉ 2 cảnh chèn cận người bán hàng (3,97-4,83 s và 8,27-8,9 s) -> giữ MỘT góc. Phần 2 25,7-76,9 s: robot ô trên (y 0-622), vạch cam (622-654),
người bán hàng selfie ô dưới (654-1280). Cắt cứng vào phần 2."""
import os
import sys

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = _args[0] if _args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "KICH-BAN-PHONG-VAN-PHO-MALAYALAM.txt")

HEAD = """[HAU KY]:
loai: phong-van-pho-malayalam

[GHI CHU]:
Thể loại "phỏng vấn đường phố rồi chia trên/dưới + gia sư AI, tiếng Malayalam xen tiếng Anh" (video mẫu: 1510_interview street hindi_005, 76,9 giây, app Aiva AI).
MỘT dự án 2 phần, Studio chạy bằng code riêng app/production/types/phong-van-pho-malayalam/gen.py (logic chung ở types/_chung/nhieu_phan.py).
Kịch bản sinh bằng cong-cu/tao_kich_ban.py: sửa ở đó rồi chạy lại.
  PHẦN 1 (cảnh thường, 11 cảnh, MỘT góc qua vai đứng yên): phóng viên trẻ (PV, mép TRÁI tiền cảnh, quay lưng nửa người, cầm micro đen chĩa về người bán)
         hỏi đố từ tiếng Anh người phụ nữ bán hàng rong (HOC, giữa-phải, đeo găng nilon, đứng sau xe đẩy inox có nhiều nồi). PV khai QUAY_LUNG_PV.
         Chỉ cảnh 1 gen ảnh khung đầu; cảnh 2-11 nối từ khung cuối cảnh trước. Bỏ 2 cảnh chèn cận mặt người bán của video mẫu.
  PHẦN 2 (ghép 2 lớp, cắt cứng khi vào phần): robot gia sư AI (robot Talka) ô TRÊN (DAY, y 0 -> 0,5), người bán hàng quay selfie ô DƯỚI (HOC, y 0,5 -> 1).
         Video mẫu có vạch cam ngang giữa hai ô (y 622-654/1280): Studio chưa vẽ, ghi "còn khác video mẫu".
         nen: DAY là CỐ Ý (bài học chia-tren-duoi-marathi/bengali).
  Hậu kỳ riêng: phụ đề chữ đen ô trắng, font Nirmala UI + shaping complex (chữ Malayalam), tâm y 960 ở cả hai phần (giữa khung như video mẫu).
  Ảnh tham chiếu: anh/robot-talka.png = robot Talka của người dùng (theo yêu cầu, thay robot của video mẫu); PV và HOC: Muse gen theo mô tả (cong-cu/gen_anh_tham_chieu.py). KHÔNG cắt ảnh từ video mẫu.
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.

===== PHAN 1: PHONG VAN DUONG PHO (CANH THUONG) =====

[STYLE LOCK]:
Vertical 9:16 photorealistic street-interview video in a small town in Kerala, soft overcast daylight, natural colours, the look of a real handheld vox-pop moment filmed on a phone but held very steady. One single camera angle for the whole part, an over-the-shoulder two-shot that never moves, never cuts and never zooms. The same two characters, the same stall and the same props in every clip. No text, no letters, no logos, no captions, no signboards with readable writing, no lettering on the microphone, the clothes or the stall anywhere in the frame.

[CHAR LOCK]:
The {{VAI_PV}}, {{TEN_PV}} ({{POS_PV}}): {{NGUOI_PV}}, {{DAO_MIC}} in his hand, held out toward {{TEN_HOC}} at chest height. VOICE LOCK INTERVIEWER: one single voice, {{GIONG_PV}}, the same in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}. {{DAO_GANG}} {{DAO_GIU}} VOICE LOCK VENDOR: one single voice, {{GIONG_HOC}}, the same in every clip.
When silent, the interviewer {{NGHE_PV}}; when silent, {{TEN_HOC}} {{NGHE_HOC}}.
EYE LINE (every clip, whoever speaks): {{TEN_PV}} {{NHIN_PV}}; {{TEN_HOC}} {{NHIN_HOC}}. Nobody looks into the lens; the interviewer's face never turns toward the camera.
RULE: in each clip exactly ONE character speaks, one line, keeping the EYE LINE. The other character stays silent the whole clip, mouth closed, but stays alive and reacts with the eyes and face as the clip describes. Each voice stays the same in every clip.
ACTION CLIPS: the actions are done WHILE the line is spoken and are complete by the last word. Props, the same in every clip: {{DAO_XE}} across the bottom of the frame, right in front of {{TEN_HOC}}.

[SET LOCK]:
{{NEN_PHO}}. The street behind is calm; nobody walks through the frame. The stall, its goods and the microphone stay where they are in the start frame; only the two people move.

[VIDEO SUFFIX]:
LOCKED CAMERA in every clip: no pan, no tilt, no zoom, no push-in, never a cut; the framing of the start frame stays exactly the same to the last frame. The speaker starts talking right away at a natural, unscripted pace (about 2.5 words per second for the Malayalam sentences, the single English words said clearly and confidently) and finishes the line promptly. After the last word the speaker relaxes with the mouth closed while the other keeps listening naturally, until the end of the clip (the usual rest pose: {{DAO_NGHI}}). Both sound like real people caught on camera, not actors and not a voice-over: relaxed natural pitch movement, everyday volume, small natural breaths. Malayalam is spoken in natural native Kerala Malayalam; the English words are said the way Malayali speakers say them, without switching voice. Sound: two real voices close to the microphone, a faint quiet street ambience, no music, no traffic noise over the voices. No subtitles, no text. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, icons, emoji, readable signboards, lettering on the microphone, the clothes or the stall; split screen, overlay, inset window; anyone looking into the lens; the interviewer turning his face to the camera or showing his full face; a side profile of the interviewer with both eyes visible; camera move, zoom, push-in, a cut, shaky handheld camera; two voices in one clip; the silent character moving the mouth; extra people in the foreground; people or vehicles passing in the background; the microphone, the goods or the stall changing position on their own; goods flying or spilling; face, hair or clothes changing; hands going to the head, face or hair; one character copying the other's movements; background music; robotic, text-to-speech or announcer voice; silent clip with no speech; slow, dragged speech.
"""

ANGLE = ("CAMERA ANGLE: LOCKED OVER-THE-SHOULDER TWO-SHOT at head height, the camera just behind the interviewer's right shoulder: {{TEN_PV}} fills the LEFT "
         "third of the frame in the foreground, seen from behind from the head down to the waist, the back of his head and his right ear at the upper left, "
         "only the right arm of his glasses and the edge of his beard and cheek visible, his eyes not visible; his face points INTO the scene toward the vendor on the "
         "right and never turns to the camera; a black backpack strap over his right shoulder; his hand reaches forward holding {{DAO_MIC}} toward the "
         "vendor's chest. {{TEN_HOC}} stands in the CENTRE-RIGHT behind {{DAO_XE}}, seen from the waist up, turned three-quarters toward the left, facing the interviewer, "
         "{{HER_HOC}} face clearly visible in three-quarter view, {{HER_HOC}} head a little lower than the interviewer's, {{TAY_HOC}}. Across the bottom third "
         "of the frame: {{DAO_XE}}. Behind them {{NEN_PHO}}. FRAME ANCHORS: the interviewer stays in the left 35 percent, the vendor's face in the upper right "
         "half, the stall along the bottom; the frame edges never change.")
ANGLE_VN = ("một góc qua vai duy nhất, máy đứng yên: phóng viên quay lưng ở mép TRÁI tiền cảnh, máy sau vai phải anh, tay chĩa micro đen về người bán; người bán "
            "giữa-phải sau quầy hàng đúng nghề, nhìn phóng viên")
BOTH = "In the shot: {{TEN_PV}} ({{NGUOI_PV}}), seen from behind. In the shot: {{TEN_HOC}} ({{NGUOI_HOC}}). {{DAO_GANG}}"
EYE = ("EYE LINE: the interviewer's face points at the vendor's face (to the right) with his eyes not visible to the camera; "
       "the vendor looks at his face (to the left) in three-quarter view; nobody looks into the lens")
ML = "Malayalam"
EN = "English"
MLEN = "Malayalam xen tiếng Anh"

# (n, thời gian mẫu, ngôn ngữ, ai nói, khung đầu VN (chỉ cảnh 1), diễn biến VN, khung cuối VN, ACTION EN, DELIVERY EN)
SC = [
    (1, "0:00–0:03", ML, "pv",
     "Góc qua vai như video mẫu: phóng viên quay lưng mép trái, tay chĩa micro đen về phía ngực người bán; người bán giữa-phải sau quầy hàng, "
     "hai tay đặt trên miệng nồi, nhìn phóng viên, mỉm cười. Miệng khép.",
     "Phóng viên hỏi đố, đầu hơi nghiêng về phía người bán, micro giữ yên. Người bán nhìn anh, tay vẫn làm việc nhẹ trên quầy, "
     "nhướng mày như đang nghĩ.",
     "Micro vẫn chĩa về người bán; người bán nhìn phóng viên, tay trên quầy; miệng khép.",
     "the interviewer tilts his head slightly toward the vendor as he asks, the microphone held still toward {{HERO_HOC}}; {{TEN_HOC}} {{VIEC_HOC}} "
     "and raises {{HER_HOC}} eyebrows, thinking",
     "light, playful quiz-show tone, a clear rise at the end of the question"),
    (2, "0:03–0:04", EN, "hoc",
     "", "Người bán trả lời ngay một từ, tự tin, gật nhẹ, mỉm cười. Phóng viên giữ micro, gật đầu.",
     "Như khung đầu; miệng khép.",
     "{{TEN_HOC}} answers at once with one small confident nod and a smile, {{TAY_HOC}}; the interviewer gives a small nod",
     "quick, confident, a smile in the voice"),
    (3, "0:04–0:04", ML, "pv",
     "", "Phóng viên đố tiếp một từ, giọng nhanh. Người bán nhìn anh, chờ.",
     "Như khung đầu; miệng khép.",
     "the interviewer fires the next word, keeping the microphone toward {{HERO_HOC}}; {{TEN_HOC}} looks at him, ready",
     "quick, playful"),
    (4, "0:04–0:05", EN, "hoc",
     "", "Người bán trả lời ngay, mỉm cười tự tin. Phóng viên gật đầu.",
     "Như khung đầu; miệng khép.",
     "{{TEN_HOC}} answers at once with a confident smile; the interviewer nods",
     "quick, clear, confident"),
    (5, "0:05–0:07", ML, "pv",
     "", "Phóng viên đố tiếp, kéo dài giọng ở chữ cuối như bỏ lửng. Người bán cười, tay đặt lại món đồ đang cầm.",
     "Tay người bán trên quầy; miệng khép.",
     "the interviewer asks, drawing out the last word as if leaving it hanging; {{TEN_HOC}} smiles and {{VIEC2_HOC}}",
     "teasing, the last word drawn out and left hanging"),
    (6, "0:07–0:08", EN, "hoc",
     "", "Người bán trả lời, gật đầu một cái dứt khoát, cười. Phóng viên gật đầu.",
     "Như khung đầu; miệng khép.",
     "{{TEN_HOC}} answers with one firm nod and a grin; the interviewer nods",
     "confident, a little proud"),
    (7, "0:08–0:08", ML, "pv",
     "", "Phóng viên đố từ cuối, nhanh. Người bán nhìn anh, mắt sáng lên.",
     "Như khung đầu; miệng khép.",
     "the interviewer asks the last word quickly; the vendor's eyes light up",
     "quick, playful"),
    (8, "0:08–0:09", EN, "hoc",
     "", "Người bán trả lời, cười tươi, hơi ngẩng cằm tự hào. Phóng viên lắc đầu nhẹ thán phục.",
     "Người bán cười tươi, miệng khép; phóng viên nhìn người bán.",
     "{{TEN_HOC}} answers with a bright smile, lifting {{HER_HOC}} chin a little with pride; the interviewer gives a small amazed shake of the head",
     "proud and bright"),
    (9, "0:09–0:14", ML, "pv",
     "", "Phóng viên nói, giọng ngạc nhiên thán phục, bàn tay không cầm micro mở ra một chút ngang hông ở giữa câu rồi hạ xuống, micro vẫn chĩa về cô. Người bán "
     "cười, hơi ngượng, gật nhẹ.",
     "Phóng viên hạ tay; người bán mỉm cười nhìn anh; miệng khép.",
     "the interviewer speaks with surprised admiration, his free hand opening a little at his hip in the middle of the line and then lowering, the microphone "
     "still toward {{HERO_HOC}}; {{TEN_HOC}} smiles, a little shy, and nods",
     "amazed, friendly, slightly teasing"),
    (10, "0:14–0:19", EN, "hoc",
     "", "Người bán trả lời bằng tiếng Anh, tự hào, gật nhẹ ở 'from TV', cười tươi ở 'fluently'; tay nghỉ trên quầy. Phóng viên gật đầu.",
     "Như khung đầu; miệng khép.",
     "{{TEN_HOC}} answers proudly in English with a small nod on 'from TV' and a big smile on 'fluently', {{TAY_HOC}}; "
     "the interviewer nods",
     "proud and warm, Indian English accent, fluent"),
    (11, "0:19–0:25", MLEN, "hoc",
     "", "Người bán hơi nghiêng người về phía phóng viên như kể bí mật, rồi ở câu cuối giơ tay phải vẫy nhẹ về phía mình như rủ 'lại đây, tôi chỉ cho', "
     "hạ tay về quầy trước chữ cuối. Phóng viên nghe chăm chú. Hết phần 1 (cắt cứng sang phần 2).",
     "Tay người bán về trên quầy; người bán mỉm cười nhìn phóng viên; miệng khép.",
     "{{TEN_HOC}} leans in a little as if sharing a secret; on the last sentence {{SHE_HOC}} lifts {{HER_HOC}} right hand and gives one small beckoning wave toward "
     "{{SELF_HOC}}, then lowers it back to rest as before the last word; the interviewer listens closely",
     "confiding and cheerful, the last sentence warm and inviting"),
]
AUDIO = "Audio: Chỉ giọng của một nhân vật, gần micro, rõ, tự nhiên như phỏng vấn đường phố thật, tiếng phố rất nhỏ. Không nhạc, không tiếng xe đè lên giọng."
NEG = "Negative prompt: two voices; the silent character moving the mouth; the interviewer turning to the camera; text or captions; split screen; anyone looking into the lens; camera move or zoom; people moving in the background; no speech."

out = [HEAD]
for n, t, lang, who, kd, db, kc, act, deliv in SC:
    first = n == 1
    out.append(f"\nCẢNH {n} ({t}): Lượt {n}")
    out.append(f"Bối cảnh: {ANGLE_VN}; không có chữ." + (" Khung đầu gen mới." if first else " Nối từ khung cuối cảnh trước."))
    out.append(f"Voice: ({lang}, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}")
    out.append(f"Khung đầu: {kd}" if first else "Khung đầu: Chính là khung cuối của cảnh trước.")
    out.append(f"Khung cuối: {kc} Khung này là khung đầu của cảnh sau.")
    out.append(f"Diễn biến: {db}")
    if first:
        out.append("Prompt ảnh: Generate exactly one still image now, vertical 9:16, photorealistic, a single frame with no split screen, soft overcast daylight. "
                   f"{ANGLE} {BOTH} Pose: the interviewer holds the microphone toward {{{{TEN_HOC}}}}, his face pointing at {{{{HERO_HOC}}}}; {{{{TEN_HOC}}}} smiles at the interviewer, "
                   f"{{{{TAY_HOC}}}}. {EYE}. Mouths closed, natural expressions. Only these two people are visible in the foreground. "
                   "No text, no logos, no readable signs anywhere. Output only the image.")
    start = "Start exactly from the start-frame image." if first else "Start exactly from the provided start frame (the last frame of the previous clip) and continue from it with no cut or reset."
    lang_en = {"Malayalam": "in Malayalam", "English": "in English", MLEN: "in Malayalam mixed with English words, exactly as written"}[lang]
    if who == "pv":
        speak = (f"Only {{{{TEN_PV}}}} speaks, {lang_en}; the camera sees only the back and the right edge of his head, his face keeps pointing at the vendor. "
                 "The vendor keeps the mouth closed and reacts as described.")
    else:
        speak = (f"Only {{{{TEN_HOC}}}} speaks, {lang_en}, with clear lip-sync, looking at the interviewer's face. "
                 "The interviewer is silent, holding the microphone still toward the vendor.")
    out.append(f"Prompt video: STYLE LOCK, SET LOCK. {start} CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} {speak} {EYE}. "
               f"ACTION, done WHILE the line is spoken, complete by the last word: {act}. LOCKED CAMERA: no pan, no tilt, no zoom. "
               f"After the line the speaker relaxes with the mouth closed and the other keeps listening naturally. DELIVERY of this line: {deliv}; a real person "
               "talking, not acting for the camera. Same voices as always, no music. VIDEO SUFFIX.")
    out.append(AUDIO)
    out.append(NEG)

out.append("""
===== PHAN 2: ROBOT O TREN, NGUOI BAN HANG O DUOI (GHEP 2 LOP) =====

[GHEP HAI LOP]:
nen: DAY
khung DAY: 0, 0, 1, 0.5
khung HOC: 0, 0.5, 1, 0.5
bo goc: 0
vien: khong
noi: lien
nghe: moi canh

[STYLE LOCK]:
Photorealistic look, crisp focus on the face. Realistic skin, hair and fabric detail for the person in soft overcast daylight; glossy clean high-end CGI for the robot. The frame is square and is later trimmed slightly at the top and bottom, so the head always stays well inside the frame. No text, captions, logos, icons or watermarks anywhere in the frame.

[NHAN VAT DAY]:
{{TEN_DAY}}: {{NGUOI_DAY}}, wearing white over-ear headphones with a small boom microphone at the left cheek. The reference photo shows only the robot's look: its pale backdrop, glowing ring and standing pose are NOT part of the scene. Square frame on a fixed tripod, framed from the top of the head down to the upper chest, facing the camera straight on and perfectly centred left-right. The top of the head is about 8% down from the top edge, the centre of the face at about 45% of the frame height, the chin at about 68%, the head about 40% of the frame width; the shoulders reach the bottom corners. {{TEN_DAY}} keeps exactly this size in the frame in every clip. Behind: {{NEN_DAY}}. She looks straight into the lens, as if on a video call with the learner. While speaking her lips open and move naturally with every word, with small head tilts, lively eyebrows, a warm smile and natural blinks. VOICE: {{GIONG_DAY}}, the same timbre, pitch and loudness in every clip; speaks natural conversational Malayalam and says the English words clearly.

[NGHE DAY]:
{{TEN_DAY}} waits calmly: looking into the lens, a gentle closed-mouth smile, slow blinks, a tiny head tilt now and then. The lips stay gently pressed together the whole clip; the head stays mostly still apart from that small tilt.

[NHAN VAT HOC]:
{{TEN_HOC}}: {{NGUOI_HOC}}. The reference photo shows only the face, hair and clothing: its background and pose are NOT part of the scene. Square selfie frame, as if {{SHE_HOC}} holds {{HER_HOC}} phone at arm's length in front of {{HER_HOC}} face: framed from the chest up, facing the camera straight on, perfectly centred left-right. The top of the hair is about 19% down from the top edge, the centre of the face at about 40% of the frame height, the shoulders span most of the frame width, the chest reaches the bottom edge. The phone and {{HER_HOC}} hands stay below and outside the frame. {{TEN_HOC}} keeps exactly this size in the frame in every clip. Behind: {{NEN_HOC}}. The camera stays steady. {{TEN_HOC}} looks straight into the lens, as if on a video call with the AI tutor. While speaking: natural expressions, brows knit a little when unsure, small head tilts, a blink on a hard word, then back to the lens. VOICE: {{GIONG_HOC}}, the same timbre, pitch and loudness in every clip; speaks natural everyday Malayalam and says the English words like a learner, a little slowly.

[NGHE HOC]:
{{TEN_HOC}} pays attention to the AI tutor: a relaxed friendly face with a faint smile, eyes on the lens, slow natural blinks, a small nod now and then. The lips stay gently pressed together the whole clip; the head stays mostly still apart from that small nod.

[VIDEO SUFFIX]:
Natural spontaneous conversational delivery, real people on a video call, not text-to-speech, not an announcer. Malayalam sentences with English words mixed in, exactly as written, every word said once. The tutor talks at about 2.5 words per second, warm and lively; the learner at about 2.5 words per second, plainer, unsure on the English words. The line starts right away, light natural breaths. Clean close voice, no music, no singing or humming, no background chatter, no sound effects, no strong echo.

[NEGATIVE]:
text, letters, captions, subtitles, logos, icons, watermark, readable signboards; writing on the robot, the headphones or the clothes; hair on the robot; phone or app interface in the frame; a hand or a phone in the frame; split screen or picture-in-picture inside the clip; a second person in the foreground; people walking close behind; hands touching the face or hair; camera cuts, zoom, push-in, pan, strong shake; the subject drifting off-centre; the head leaving the frame; face morphing, outfit change, hair change, age drift; distorted face; extra fingers; exaggerated gestures; repeated words; slow, dragged or stretched speech; flat monotone, robotic or announcer voice; singing, humming; background music; echo or reverb
""")
sys.stdout.reconfigure(encoding="utf-8")
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("ok", len(SC), os.path.abspath(OUT))
