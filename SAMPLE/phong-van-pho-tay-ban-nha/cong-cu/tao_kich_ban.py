"""Sinh KICH-BAN-PHONG-VAN-PHO-TAY-BAN-NHA.txt (6 cảnh phần 1 + phần 2 ghép 2 lớp trên/dưới, 6 cảnh): cùng khuôn video mẫu
"1510_interview street hindi_005" (xem ../phong-van-pho-malayalam/) nhưng lời TIẾNG TÂY BAN NHA (Mexico), người bán + phóng viên + nền theo bảng
"20 biến thể ES Interview", robot Aiva (anh/robot-aiva.png). Phóng viên có thể nam HOẶC nữ (luôn khác giới người bán) nên mọi đại từ/ngoại hình của
phóng viên đi qua token (HIS_PV, HIM_PV, TOC_PV...).
Sửa bảng SC hoặc các khối chữ rồi chạy:  runtime\\python.exe SAMPLE\\phong-van-pho-tay-ban-nha\\cong-cu\\tao_kich_ban.py"""
import os
import sys

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = _args[0] if _args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "KICH-BAN-PHONG-VAN-PHO-TAY-BAN-NHA.txt")

HEAD = """[HAU KY]:
loai: phong-van-pho-tay-ban-nha

[GHI CHU]:
Thể loại "phỏng vấn đường phố rồi chia trên/dưới + gia sư AI, tiếng Tây Ban Nha (Mexico)": cùng khuôn video mẫu 1510_interview street hindi_005 (app Aiva AI) như phong-van-pho-malayalam, đổi lời sang tiếng Tây Ban Nha.
MỘT dự án 2 phần, Studio chạy bằng code riêng app/production/types/phong-van-pho-tay-ban-nha/gen.py (logic chung ở types/_chung/nhieu_phan.py).
Kịch bản sinh bằng cong-cu/tao_kich_ban.py: sửa ở đó rồi chạy lại. Biến thể sinh bằng cong-cu/tao_20_bien_the.py.
  PHẦN 1 (cảnh thường, 6 cảnh, MỘT góc qua vai đứng yên): phóng viên (PV, mép TRÁI tiền cảnh, quay lưng nửa người, cầm micro đen chĩa về người bán) hỏi người bán hàng rong
         (HOC, giữa-phải, đứng sau quầy đúng nghề). PV LUÔN KHÁC GIỚI người bán. PV khai QUAY_LUNG_PV. Chỉ cảnh 1 gen ảnh khung đầu; cảnh 2-6 nối từ khung cuối cảnh trước.
  PHẦN 2 (ghép 2 lớp, cắt cứng khi vào phần): robot Aiva ô TRÊN (DAY, y 0 -> 0,5), người bán quay selfie ô DƯỚI (HOC, y 0,5 -> 1). nen: DAY là CỐ Ý.
  Hậu kỳ riêng: phụ đề chữ đen ô trắng, tâm y 1560 (phần 1) / 960 (phần 2, cụm <= 3 từ). Không tua nhanh khoảng lặng (cắt sát theo lời).
  Ảnh tham chiếu: robot = anh/robot-aiva.png (người dùng cấp); người bán, phóng viên, nền = ảnh Drive trong bảng của người dùng (anh/bt20/). KHÔNG cắt ảnh từ video mẫu.
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.

===== PHAN 1: PHONG VAN DUONG PHO (CANH THUONG) =====

[STYLE LOCK]:
Vertical 9:16 photorealistic street-interview video in a town in Mexico, soft overcast daylight, natural colours, the look of a real handheld vox-pop moment filmed on a phone but held very steady. One single camera angle for the whole part, an over-the-shoulder two-shot that never moves, never cuts and never zooms. The same two characters, the same stall and the same props in every clip. No text, no letters, no logos, no captions, no signboards with readable writing, no lettering on the microphone, the clothes or the stall anywhere in the frame.

[CHAR LOCK]:
The {{VAI_PV}}, {{TEN_PV}} ({{POS_PV}}): {{NGUOI_PV}}, {{DAO_MIC}} in {{HIS_PV}} hand, held out toward {{TEN_HOC}} at chest height. VOICE LOCK INTERVIEWER: one single voice, {{GIONG_PV}}, the same in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}. {{DAO_GANG}} {{DAO_GIU}} VOICE LOCK VENDOR: one single voice, {{GIONG_HOC}}, the same in every clip.
When silent, the interviewer {{NGHE_PV}}; when silent, {{TEN_HOC}} {{NGHE_HOC}}.
EYE LINE (every clip, whoever speaks): {{TEN_PV}} {{NHIN_PV}}; {{TEN_HOC}} {{NHIN_HOC}}. Nobody looks into the lens; the interviewer's face never turns toward the camera.
RULE: in each clip exactly ONE character speaks, one line, keeping the EYE LINE. The other character stays silent the whole clip, mouth closed, but stays alive and reacts with the eyes and face as the clip describes. Each voice stays the same in every clip.
ACTION CLIPS: the actions are done WHILE the line is spoken and are complete by the last word. Props, the same in every clip: {{DAO_XE}} across the bottom of the frame, right in front of {{TEN_HOC}}.

[SET LOCK]:
{{NEN_PHO}}. The street behind is calm; nobody walks through the frame. The stall, its goods and the microphone stay where they are in the start frame; only the two people move.

[VIDEO SUFFIX]:
LOCKED CAMERA in every clip: no pan, no tilt, no zoom, no push-in, never a cut; the framing of the start frame stays exactly the same to the last frame. The speaker starts talking right away at a natural, unscripted pace (about 2.5 words per second, natural conversational Spanish) and finishes the line promptly. After the last word the speaker relaxes with the mouth closed while the other keeps listening naturally, until the end of the clip (the usual rest pose: {{DAO_NGHI}}). Both sound like real people caught on camera, not actors and not a voice-over: relaxed natural pitch movement, everyday volume, small natural breaths. The Spanish is spoken in natural native Mexican Spanish, exactly as written, every word said once. Sound: two real voices close to the microphone, a faint quiet street ambience, no music, no traffic noise over the voices. No subtitles, no text. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, icons, emoji, readable signboards, lettering on the microphone, the clothes or the stall; split screen, overlay, inset window; anyone looking into the lens; the interviewer turning {{HIS_PV}} face to the camera or showing {{HIS_PV}} full face; a side profile of the interviewer with both eyes visible; camera move, zoom, push-in, a cut, shaky handheld camera; two voices in one clip; the silent character moving the mouth; extra people in the foreground; people or vehicles passing in the background; the microphone, the goods or the stall changing position on their own; goods flying or spilling; face, hair or clothes changing; hands going to the head, face or hair; one character copying the other's movements; background music; robotic, text-to-speech or announcer voice; silent clip with no speech; slow, dragged speech.
"""

ANGLE = ("CAMERA ANGLE: LOCKED OVER-THE-SHOULDER TWO-SHOT at head height, the camera just behind the interviewer's right shoulder: {{TEN_PV}} fills the LEFT "
         "third of the frame in the foreground, seen from behind from the head down to the waist, the back of {{HIS_PV}} head ({{TOC_PV}}) and {{HIS_PV}} right ear at the upper left, "
         "only the edge of the cheek visible, {{HIS_PV}} eyes not visible; {{HIS_PV}} face points INTO the scene toward the vendor on the "
         "right and never turns to the camera; {{HIS_PV}} hand reaches forward holding {{DAO_MIC}} toward the "
         "vendor's chest. {{TEN_HOC}} stands in the CENTRE-RIGHT behind {{DAO_XE}}, seen from the waist up, turned three-quarters toward the left, facing the interviewer, "
         "{{HER_HOC}} face clearly visible in three-quarter view, {{HER_HOC}} head a little lower than the interviewer's, {{TAY_HOC}}. Across the bottom third "
         "of the frame: {{DAO_XE}}. Behind them {{NEN_PHO}}. FRAME ANCHORS: the interviewer stays in the left 35 percent, the vendor's face in the upper right "
         "half, the stall along the bottom; the frame edges never change.")
ANGLE_VN = ("một góc qua vai duy nhất, máy đứng yên: phóng viên quay lưng ở mép TRÁI tiền cảnh, máy sau vai phải phóng viên, tay chĩa micro đen về người bán; người bán "
            "giữa-phải sau quầy hàng đúng nghề, nhìn phóng viên")
BOTH = "In the shot: {{TEN_PV}} ({{NGUOI_PV}}), seen from behind. In the shot: {{TEN_HOC}} ({{NGUOI_HOC}}). {{DAO_GANG}}"
EYE = ("EYE LINE: the interviewer's face points at the vendor's face (to the right) with {{HIS_PV}} eyes not visible to the camera; "
       "the vendor looks at {{HIS_PV}} face (to the left) in three-quarter view; nobody looks into the lens")
ES = "Spanish"

# (n, thời gian ước lượng, ngôn ngữ, ai nói, khung đầu VN (chỉ cảnh 1), diễn biến VN, khung cuối VN, ACTION EN, DELIVERY EN)
SC = [
    (1, "0:00–0:03", ES, "pv",
     "Góc qua vai: phóng viên quay lưng mép trái, tay chĩa micro đen về phía ngực người bán; người bán giữa-phải sau quầy hàng, "
     "nhìn phóng viên, mỉm cười. Miệng khép.",
     "Phóng viên hỏi, đầu hơi nghiêng về phía người bán, micro giữ yên. Người bán nhìn phóng viên, tay làm việc nhẹ trên quầy, nhướng mày thích thú.",
     "Micro vẫn chĩa về người bán; người bán nhìn phóng viên, tay trên quầy; miệng khép.",
     "the interviewer tilts {{HIS_PV}} head slightly toward the vendor while asking, the microphone held still toward {{HERO_HOC}}; {{TEN_HOC}} {{VIEC_HOC}} "
     "and raises {{HER_HOC}} eyebrows with a pleased look",
     "friendly, curious, a clear rise at the end of the question"),
    (2, "0:03–0:10", ES, "hoc",
     "", "Người bán trả lời tự hào, gật nhẹ ở 'en la tele', cười tươi ở 'con fluidez'; tay nghỉ trên quầy. Phóng viên gật đầu.",
     "Như khung đầu; miệng khép.",
     "{{TEN_HOC}} answers proudly with a small nod on 'en la tele' and a big smile on 'con fluidez', {{TAY_HOC}}; the interviewer nods",
     "proud and warm, natural, relaxed"),
    (3, "0:10–0:12", ES, "pv",
     "", "Phóng viên hỏi tiếp, thán phục, hơi nghiêng người. Người bán nhìn phóng viên, cười ngượng.",
     "Như khung đầu; miệng khép.",
     "the interviewer asks the next question with admiration, the microphone still toward {{HERO_HOC}}; {{TEN_HOC}} looks at {{HIM_PV}} and smiles a little shyly",
     "amazed, friendly, slightly teasing"),
    (4, "0:12–0:15", ES, "hoc",
     "", "Người bán trả lời tự tin, gật đầu một cái dứt khoát ở 'primer día', cười. Phóng viên gật đầu.",
     "Tay người bán trên quầy; miệng khép.",
     "{{TEN_HOC}} answers with confidence and one firm nod on 'primer día', then a grin; {{VIEC2_HOC}}; the interviewer nods",
     "confident, a little proud"),
    (5, "0:15–0:17", ES, "pv",
     "", "Phóng viên hỏi tiếp, nhướng mày tò mò, bàn tay không cầm micro mở ra một chút ngang hông rồi hạ xuống, micro vẫn chĩa về người bán. Người bán nhìn phóng viên, chờ.",
     "Phóng viên hạ tay; người bán mỉm cười nhìn phóng viên; miệng khép.",
     "the interviewer asks with curious raised eyebrows, {{HIS_PV}} free hand opening a little at {{HIS_PV}} hip in the middle of the line and then lowering, the microphone "
     "still toward {{HERO_HOC}}; {{TEN_HOC}} looks at {{HIM_PV}}, ready to answer",
     "curious, playful"),
    (6, "0:17–0:22", ES, "hoc",
     "", "Người bán hơi nghiêng người về phía phóng viên như kể bí mật, rồi ở 'ven' giơ tay phải vẫy nhẹ về phía mình như rủ 'lại đây', "
     "hạ tay về quầy trước 'cómo'. Phóng viên nghe chăm chú. Hết phần 1 (cắt cứng sang phần 2).",
     "Tay người bán về trên quầy; người bán mỉm cười nhìn phóng viên; miệng khép.",
     "{{TEN_HOC}} leans in a little as if sharing a secret; on 'ven' {{SHE_HOC}} lifts {{HER_HOC}} right hand and gives one small beckoning wave toward "
     "{{SELF_HOC}}, then lowers it back to rest before the last words; the interviewer listens closely",
     "confiding and cheerful, the last words warm and inviting"),
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
                   f"{ANGLE} {BOTH} Pose: the interviewer holds the microphone toward {{{{TEN_HOC}}}}, {{{{HIS_PV}}}} face pointing at {{{{HERO_HOC}}}}; {{{{TEN_HOC}}}} smiles at the interviewer, "
                   f"{{{{TAY_HOC}}}}. {EYE}. Mouths closed, natural expressions. Only these two people are visible in the foreground. "
                   "No text, no logos, no readable signs anywhere. Output only the image.")
    start = "Start exactly from the start-frame image." if first else "Start exactly from the provided start frame (the last frame of the previous clip) and continue from it with no cut or reset."
    lang_en = "in Mexican Spanish, exactly as written"
    if who == "pv":
        speak = (f"Only {{{{TEN_PV}}}} speaks, {lang_en}; the camera sees only the back and the right edge of {{{{HIS_PV}}}} head, {{{{HIS_PV}}}} face keeps pointing at the vendor. "
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
Photorealistic look, crisp focus on the face. Realistic skin, hair and fabric detail for the person in soft overcast daylight; glossy clean high-end CGI for the robot. The frame is square and is later trimmed slightly at the top and bottom, so the head always stays well inside the frame. No text, captions, logos, icons or watermarks anywhere in the frame (the robot's small glowing AI mark on its forehead is part of the robot and stays).

[NHAN VAT DAY]:
{{TEN_DAY}}: {{NGUOI_DAY}}, wearing white over-ear headphones with a small boom microphone at the left cheek. The reference image shows the robot's look, including the small glowing AI mark on its forehead; its dark app-icon backdrop, rounded corners, glowing ring, book icon on the chest and the pose are NOT part of the scene. Square frame on a fixed tripod, framed from the top of the head down to the upper chest, facing the camera straight on and perfectly centred left-right. The top of the head is about 8% down from the top edge, the centre of the face at about 45% of the frame height, the chin at about 68%, the head about 40% of the frame width; the shoulders reach the bottom corners. {{TEN_DAY}} keeps exactly this size in the frame in every clip. Behind: {{NEN_DAY}}. She looks straight into the lens, as if on a video call with the learner. While speaking her lips open and move naturally with every word, with small head tilts, lively eyebrows, a warm smile and natural blinks. VOICE: {{GIONG_DAY}}, the same timbre, pitch and loudness in every clip; speaks natural conversational Mexican Spanish, exactly as written.

[NGHE DAY]:
{{TEN_DAY}} waits calmly: looking into the lens, a gentle closed-mouth smile, slow blinks, a tiny head tilt now and then. The lips stay gently pressed together the whole clip; the head stays mostly still apart from that small tilt.

[NHAN VAT HOC]:
{{TEN_HOC}}: {{NGUOI_HOC}}. The reference photo shows only the face, hair and clothing: its background and pose are NOT part of the scene. Square selfie frame, as if {{SHE_HOC}} holds {{HER_HOC}} phone at arm's length in front of {{HER_HOC}} face: framed from the chest up, facing the camera straight on, perfectly centred left-right. The top of the hair is about 19% down from the top edge, the centre of the face at about 40% of the frame height, the shoulders span most of the frame width, the chest reaches the bottom edge. The phone and {{HER_HOC}} hands stay below and outside the frame. {{TEN_HOC}} keeps exactly this size in the frame in every clip. Behind: {{NEN_HOC}}. The camera stays steady. {{TEN_HOC}} looks straight into the lens, as if on a video call with the AI tutor. While speaking: natural expressions, brows knit a little when unsure, small head tilts, a blink on a hard word, then back to the lens. VOICE: {{GIONG_HOC}}, the same timbre, pitch and loudness in every clip; speaks natural everyday Mexican Spanish, exactly as written.

[NGHE HOC]:
{{TEN_HOC}} pays attention to the AI tutor: a relaxed friendly face with a faint smile, eyes on the lens, slow natural blinks, a small nod now and then. The lips stay gently pressed together the whole clip; the head stays mostly still apart from that small nod.

[VIDEO SUFFIX]:
Natural spontaneous conversational delivery, real people on a video call, not text-to-speech, not an announcer. Mexican Spanish sentences, exactly as written, every word said once. The tutor talks at about 2.5 words per second, warm and lively; the learner at about 2.5 words per second, plainer and a little unsure. The line starts right away, light natural breaths. Clean close voice, no music, no singing or humming, no background chatter, no sound effects, no strong echo.

[NEGATIVE]:
text, letters, captions, subtitles, logos, icons, watermark, readable signboards; any writing other than the single small glowing AI mark on the robot's forehead, writing on the headphones or the clothes; hair on the robot; phone or app interface in the frame; a hand or a phone in the frame; split screen or picture-in-picture inside the clip; a second person in the foreground; people walking close behind; hands touching the face or hair; camera cuts, zoom, push-in, pan, strong shake; the subject drifting off-centre; the head leaving the frame; face morphing, outfit change, hair change, age drift; distorted face; extra fingers; exaggerated gestures; repeated words; slow, dragged or stretched speech; flat monotone, robotic or announcer voice; singing, humming; background music; echo or reverb
""")
sys.stdout.reconfigure(encoding="utf-8")
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("ok", len(SC), os.path.abspath(OUT))
