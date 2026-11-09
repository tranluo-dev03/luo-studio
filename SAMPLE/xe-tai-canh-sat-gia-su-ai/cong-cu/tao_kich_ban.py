"""Sinh SAMPLE/xe-tai-canh-sat-gia-su-ai/KICH-BAN-XE-TAI-CANH-SAT-GIA-SU-AI.txt từ bảng CANH (phần 1) và các khối phần 2.
Sửa bảng/khối ở đây rồi chạy:
    .venv\\Scripts\\python.exe SAMPLE\\xe-tai-canh-sat-gia-su-ai\\cong-cu\\tao_kich_ban.py
Video mẫu: AQPPCRx43ias...(online-video-cutter.com).mp4, 50 s. Phân tích: ../PHAN-TICH-VIDEO-MAU.md.
Không dùng đại từ he/she cho tài xế (biến thể có cả tài xế nam lẫn nữ): luôn gọi {{TEN_HOC}} / "the driver".
Đại từ cảnh sát: {{HE_CANHSAT}} / {{HIS_CANHSAT}} / {{HIM_CANHSAT}}; ánh sáng: {{SANG_P1}} (phần 1), {{SANG_P2}} (phần 2). Giá trị trong CHUNG của tao_bien_the.py."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "KICH-BAN-XE-TAI-CANH-SAT-GIA-SU-AI.txt")

TOC_DO = "a brisk natural pace, about 4 words per second, short lines faster"

HEAD = """[HAU KY]:
loai: xe-tai-canh-sat-gia-su-ai

[GHI CHU]:
Thể loại "cảnh sát chặn xe tải + gia sư AI" (người thật, ảnh chân thực): MỘT dự án 2 phần, Studio chạy bằng code riêng
app/production/types/xe-tai-canh-sat-gia-su-ai/gen.py (logic chung ở types/_chung/nhieu_phan.py). Kịch bản sinh bằng cong-cu/tao_kich_ban.py: sửa ở đó rồi chạy lại.
  PHẦN 1 (cảnh thường, 9 cảnh, MỘT góc máy đứng yên): cảnh sát giao thông (CANHSAT, đứng PHẢI dưới đường) hỏi tài xế xe tải (HOC, nhoài người
         ra cửa sổ cabin, TRÁI-TRÊN). Cảnh 1 có "Prompt ảnh" (khung đầu); các cảnh sau nối từ khung cuối cảnh trước. Đưa giấy tờ ở cảnh 5-6,
         tài xế lấy điện thoại ở cảnh 9. Gắn ảnh tham chiếu mặt cho CANHSAT và HOC (ảnh AI người dùng cung cấp).
  PHẦN 2 (ghép 2 lớp, mỗi lượt một cảnh): gen RIÊNG video tài xế quay selfie trong cabin (HOC, nền 9:16) và video gia sư AI hoạt hình 3D
         (DAY, ô bo góc viền trắng phía trên: x 0.03, y 0.012, rộng 0.94, cao 0.32 = 677x410 px -> gen 16:9), rồi ghép; nối khung ("noi: lien").
         Vào phần 2 bằng nhoè chuyển động 0,5 giây (như video mẫu).
  Lượt thoại: LUOT chung, mỗi lượt có "phan": 1 hoặc 2 (lượt phần 1 đứng trước). Phần 1 cần đúng 9 lượt (= 9 CẢNH).
  Hậu kỳ riêng (post.py, kiểu trong config.json): phần 1 cảnh sát chữ trắng ô đen, tài xế chữ đen ô vàng (y 1260);
         phần 2 AI chữ xanh ngọc ô đen, tài xế chữ đen ô trắng (y 650, ngay dưới ô AI); "to" tô màu từ sai/đúng, "icon" x/check/dollar, "fx" viền + tiếng.
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.

===== PHAN 1: CANH SAT CHAN XE TAI =====

[STYLE LOCK]:
Vertical 9:16 photorealistic video on the shoulder of a wide highway {{SANG_P1}}, natural colours, the look of a real documentary moment. One fixed camera at chest height on the road shoulder, the same framing in every clip; the camera stays still. The same two characters, the same truck and the same place in every clip. No text, no letters, no logos, no captions, no icons, no lettering on the uniform, vest, badge, truck, number plate or phone anywhere in the frame.

[CHAR LOCK]:
The {{VAI_CANHSAT}}, {{TEN_CANHSAT}} ({{POS_CANHSAT}}): {{NGUOI_CANHSAT}}. VOICE LOCK OFFICER: one single voice, {{GIONG_CANHSAT}}, the same in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}. VOICE LOCK DRIVER: one single voice, {{GIONG_HOC}}, the same in every clip.
When silent, the officer {{NGHE_CANHSAT}}; when silent, the driver {{NGHE_HOC}}.
INTERACTION: the two react to each other like real people in one continuous moment. When one holds out, hands over or holds up something, the other's eyes follow it to that exact object, then come back to the speaker's face.
EYE LINE (every clip, whoever speaks): the officer looks up at the driver in the cab window; the driver looks down at the officer. The speaker's head never turns toward the camera, to the side or out of the frame while talking. Nobody looks into the lens.
RULE: in each clip exactly ONE character speaks, one line, with lip-sync, keeping the EYE LINE. The other character stays silent the whole clip, mouth closed, but stays alive and reacts with the eyes and face as the clip describes. Each voice stays the same in every clip.
ACTION CLIPS: the actions are done WHILE the line is spoken, in the order given, and are complete by the last word. Props, the same in every clip: {{DAO_GIAY_TO}} and {{DAO_DIEN_THOAI}}; they appear only when a clip's action says so, never duplicated, never with readable text.

[SET LOCK]:
{{NEN_DUONG}}. The truck: {{XE}}, parked on the shoulder with the engine off. Nothing moves in the background: the far traffic stands still, the sky and the trees do not move.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no shake, no cut. The speaker starts right away at """ + TOC_DO + """, like real people caught on camera, not actors, and finishes the line. After the last word (and the action, if the clip has one) both keep a calm closed-mouth face and stay still until the end of the clip. No subtitles, no text, no music, no engine, traffic or wind noise. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, icons, emoji, lettering on uniform, vest, badge, truck or phone; the words LEFT, RIGHT or TOP or any label written in the frame; camera movement, zoom, shake, cut; two voices in one clip; the silent character moving the mouth; extra people in the foreground; passing cars, moving clouds; face, hair or outfit changing; one character copying the other's movements; the officer facing the camera; background music, engine noise; robotic or text-to-speech voice; silent clip with no speech; movement during the final still; documents or phone multiplying, vanishing or appearing in the wrong clip; readable text or app screen on the phone; slow, dragged speech.
"""

ANH_DAU = ("Generate exactly one still image now, vertical 9:16, photorealistic, {{SANG_P1}}. CAMERA ANGLE: a fixed camera at chest height "
           "on the road shoulder, a little behind and to the right of the officer, looking along the side of the truck. {{XE}} fills the left 60% of the frame, "
           "seen from its front-left corner at a slightly low angle: the windshield edge at the top-left, the open driver's window in the upper-left third and "
           "a big side mirror on a metal arm just right of that window. In the window: {{TEN_HOC}} ({{NGUOI_HOC}}), leaning out on folded forearms on the "
           "window sill, the head at about one third of the frame height, looking down at the officer. On the shoulder in the right third: {{TEN_CANHSAT}} "
           "({{NGUOI_CANHSAT}}), standing close to the truck, seen from slightly behind the left side, body from the knees up, head at about 40% of the "
           "frame height, the face in left profile turned up toward the driver's window. Behind them: {{NEN_DUONG}}. Mouths closed, natural expressions, "
           "nobody looks into the lens. Only these two people. No text, no logos, no lettering anywhere. Output only the image.")

# (người nói, lời trong ngoặc mô tả Diễn biến VN, Khung cuối VN, hướng nhìn EN, hành động EN hoặc None)
CANH = [
    ("canhsat", "Cảnh sát đứng dưới đường, ngẩng nhìn tài xế trong cửa sổ cabin, hỏi đều giọng, hai tay buông thả cạnh thắt lưng; tài xế tì tay lên bậu cửa sổ, nhìn xuống nghe.",
     "cảnh sát ngẩng nhìn tài xế, tay buông; tài xế tì tay bậu cửa sổ nhìn xuống; hai người miệng khép, đứng im.",
     "the officer looks up at the driver in the cab window the whole clip; the driver looks down at {{HIM_CANHSAT}}.", None),
    ("hoc", "Tài xế nhìn xuống cảnh sát, hơi mệt, ngập ngừng ở chữ \"uh\" rồi trả lời; cảnh sát ngẩng nhìn, mặt bình thản.",
     "tài xế tì tay bậu cửa sổ, cười nhẹ; cảnh sát ngẩng nhìn; hai người miệng khép, đứng im.",
     "the driver looks down at the officer the whole clip; the officer looks up at the driver.", None),
    ("canhsat", "Cảnh sát hỏi tiếp, nghiêm nhưng không gắt, mắt vẫn ngẩng nhìn tài xế; tài xế nghe, chớp mắt.",
     "cảnh sát ngẩng nhìn tài xế; tài xế nhìn xuống; hai người miệng khép, đứng im.",
     "the officer looks up at the driver in the cab window the whole clip; the driver looks down at {{HIM_CANHSAT}}.", None),
    ("hoc", "Tài xế đáp ngắn, gật nhẹ một cái; cảnh sát nghe.",
     "tài xế tì tay bậu cửa sổ nhìn xuống; cảnh sát ngẩng nhìn; hai người miệng khép, đứng im.",
     "the driver looks down at the officer the whole clip; the officer looks up at the driver.", None),
    ("canhsat", "Trong lúc nói, cảnh sát giơ tay phải lên phía cửa sổ, lòng bàn tay ngửa chờ giấy tờ; tài xế nhìn theo tay rồi quay vào trong, cầm {{DAO_GIAY_TO}} từ taplo lên, giữ trước ngực.",
     "tay phải cảnh sát giơ lên ngang cửa cabin, lòng bàn tay ngửa; tài xế cầm giấy tờ trước ngực trong cửa sổ; hai người miệng khép, đứng im.",
     "the officer looks up at the driver in the cab window the whole clip; the driver looks at {{HIS_CANHSAT}} raised hand, then turns briefly inside for the documents.",
     "the officer lifts {{HIS_CANHSAT}} right hand up toward the cab window, palm up, waiting for the documents; the driver turns slightly inside, picks up {{DAO_GIAY_TO}} from the dashboard and holds it at chest height in the window"),
    ("hoc", "Tài xế nhoài xuống, đưa {{DAO_GIAY_TO}} cho cảnh sát; cảnh sát nhận bằng tay phải, nhìn theo giấy tờ rồi ngẩng lên.",
     "cảnh sát cầm giấy tờ ngang ngực bằng tay phải; tài xế tì lại hai tay lên bậu cửa sổ; hai người miệng khép, đứng im.",
     "the driver looks down at the officer's hand and then at {{HIS_CANHSAT}} face; the officer looks at the documents, then up at the driver.",
     "the driver reaches down out of the window and hands {{DAO_GIAY_TO}} to the officer; {{HE_CANHSAT}} takes it in {{HIS_CANHSAT}} right hand and holds it at chest height; the driver rests both forearms back on the window sill"),
    ("canhsat", "Cảnh sát liếc giấy tờ trên tay, bật cười ngạc nhiên rồi ngẩng nhìn tài xế, nói với vẻ thán phục; tài xế cười tươi.",
     "cảnh sát cầm giấy tờ ngang ngực, cười, ngẩng nhìn tài xế; tài xế cười; hai người miệng khép, đứng im.",
     "the officer glances at the documents in {{HIS_CANHSAT}} hand, then looks up at the driver with a big surprised smile; the driver smiles down at {{HIM_CANHSAT}}.",
     "the officer glances down at the documents in {{HIS_CANHSAT}} right hand, gives a short surprised laugh, then looks back up at the driver"),
    ("hoc", "Tài xế hào hứng, hơi nhoài ra cửa sổ, nói với vẻ tự hào; cảnh sát cầm giấy tờ, ngẩng nghe, gật nhẹ.",
     "tài xế tì tay bậu cửa sổ, cười tự hào; cảnh sát cầm giấy tờ, ngẩng nhìn; hai người miệng khép, đứng im.",
     "the driver looks down at the officer the whole clip; the officer looks up at the driver, holding the documents.", None),
    ("hoc", "Tài xế nói tiếp; đến \"Here, let me show you\" thì cầm {{DAO_DIEN_THOAI}} lên trước ngực, nhìn xuống màn hình; cảnh sát mỉm cười nhìn theo điện thoại.",
     "tài xế cầm điện thoại trước ngực, nhìn màn hình (camera thấy mặt sau điện thoại); cảnh sát mỉm cười nhìn; hết phần 1; hai người miệng khép, đứng im.",
     "the driver looks down at the officer, then down at the phone screen; the officer smiles and looks at the phone.",
     "on the words \"let me show you\" the driver picks up {{DAO_DIEN_THOAI}} and holds it at chest height in the window, looking down at its screen (the camera sees only the back of the phone); the officer smiles and looks at the phone"),
]

AUDIO = "Audio: Chỉ giọng của một nhân vật, rõ, gần; phần còn lại im lặng. Không nhạc, không tiếng động cơ, không tiếng xe, không tiếng gió."
NEG = "Negative prompt: two voices; a silent character moving the mouth; text or captions; camera movement; the officer facing the camera; no speech."

PHAN2 = """===== PHAN 2: TAI XE + GIA SU AI (GHEP 2 LOP) | vao: nhoe 0.5 =====

[GHEP HAI LOP]:
nen: HOC
khung DAY: 0.03, 0.012, 0.94, 0.32
bo goc: 0.05
vien: #FFFFFF, 3
noi: lien
nghe: moi canh

[STYLE LOCK]:
Vertical short-form social video look, {{SANG_P2}}, crisp focus on the face, realistic skin, hair and fabric detail. No text, captions, logos, icons or watermarks anywhere in the frame.

[NHAN VAT HOC]:
{{TEN_HOC}}: {{NGUOI_HOC}}. Sitting in the driver's seat of the parked truck, filming a selfie with the phone's front camera held at arm's length in the right hand: the extended right arm comes in from the lower-left corner of the frame (the phone itself is not visible). Slightly low angle, framed from the chest up, with plenty of empty headroom: the top of the head sits at about 38% of the frame height, the eyes at about 48%, the chin at about 60%, the head near the centre, a little left; the upper third of the frame shows only the calm, plain cab ceiling and the top of the window: nothing is drawn there, no window, no picture, no screen, no avatar, no face, no inset or overlay of any kind. Behind: {{NEN_CABIN}}. The camera stays steady (almost no shake). The driver is completely alone in the cab: the passenger seat beside the driver is empty. The driver looks into the lens while speaking, as if on a video call; when searching for an English word, a brief glance up to the side, then back to the lens. Small natural nods and facial expressions. VOICE: {{GIONG_HOC}}, the same timbre, pitch and loudness in every clip; a little slower here, like someone practising a foreign language, with small natural hesitations.

[NGHE HOC]:
{{TEN_HOC}} waits for the reply on the video call: friendly attentive expression and a soft smile, eyes on the lens, slow natural blinks, a small nod now and then. The lips stay gently pressed together the whole clip; the head stays mostly still.

[NHAN VAT DAY]:
{{TEN_DAY}}: {{NGUOI_DAY}}; a sleek photorealistic CGI render (glossy white porcelain armour, crisp clean studio quality), fully mechanical, never a cartoon. Framed for a wide call-window (landscape): head and shoulders centred in the middle of the frame, the chin resting lightly on the right hand, a little empty space on both sides, in front of {{NEN_DAY}}. The camera is locked off and never moves. While speaking the lips move in clear sync with the words, with small head tilts, raised eyebrows, a warm playful smile and slow blinks, like a friendly teacher. VOICE: {{GIONG_DAY}}, the same timbre, pitch and loudness in every clip.

[NGHE DAY]:
{{TEN_DAY}} waits calmly: a gentle closed-mouth smile, slow natural blinks, a tiny head tilt now and then, the chin resting lightly on the hand. The lips stay gently pressed together the whole clip; the head stays mostly still.

[VIDEO SUFFIX]:
Natural spontaneous conversational delivery, not text-to-speech, not an announcer: the driver about 3 words per second with small hesitations, the tutor about 4 words per second, bright and encouraging; the line starts right away, light natural breaths, a smile audible in the voice when the line is positive. Clean close voice, like a video call in a quiet truck cab, no music, no engine noise, no road noise, no echo.

[NEGATIVE]:
text, letters, captions, subtitles, logos, icons, watermark; phone screen or app interface in the frame; lettering on the name patch; toys, plush toys, figurines, dashboard ornaments; camera cuts, zoom, push-in, strong shake; a second person; face morphing, outfit change, hair change, age or style drift; a cartoon look; distorted face; extra or missing fingers or arms; jerky or exaggerated gestures; hands touching the face or hair; slow, dragged or stretched speech; flat monotone or robotic voice; background music; echo or reverb
"""


def canh(i, who, dien, cuoi, eye, act):
    n = i + 1
    lines = [f"CẢNH {n} (0:{(n - 1) * 5:02d}–0:{n * 5:02d}): Lượt {n}",
             "Bối cảnh: một góc máy cố định ven đường: xe tải chiếm 60% bên trái, tài xế nhoài ra cửa sổ cabin (trái-trên), cảnh sát đứng dưới đường bên phải, "
             "nhìn từ hơi sau lưng bên trái, mặt nghiêng ngẩng lên; không có chữ, không người lạ.",
             f"Voice: (English, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}"]
    if n == 1:
        lines.append("Khung đầu: ảnh mới theo Prompt ảnh (bố cục như trên); tài xế tì tay bậu cửa sổ nhìn xuống, cảnh sát ngẩng nhìn lên; miệng hai người khép.")
    else:
        lines.append("Khung đầu: khung cuối của cảnh trước (cùng góc máy).")
    lines.append("Khung cuối: " + cuoi + " Khung này là khung đầu của cảnh sau.")
    lines.append("Hướng nhìn: " + eye)
    lines.append("Diễn biến: " + dien + " Nói xong cả hai đứng im đến hết clip.")
    if n == 1:
        lines.append("Prompt ảnh: " + ANH_DAU)
    v = (f"Prompt video: STYLE LOCK, SET LOCK. Start exactly from the start-frame image and keep its camera framing. CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} "
         f"Only that character speaks, with lip-sync, at {TOC_DO}. EYE LINE for the whole clip: {eye} The speaker never turns the head toward the camera while talking. "
         "The other person keeps the mouth closed and reacts only with the eyes and face. ")
    if act:
        v += f"ACTION, done WHILE the line is spoken and complete by the last word: {act}. After the line and the action both stay still until the end. "
    else:
        v += "After the line both stay still until the end. "
    v += "Same voices as always, clean dry sound, no music. VIDEO SUFFIX."
    lines += [v, AUDIO, NEG]
    return "\n".join(lines)


def main():
    body = HEAD + "\n" + "\n\n".join(canh(i, *c) for i, c in enumerate(CANH)) + "\n\n" + PHAN2
    open(OUT, "w", encoding="utf-8", newline="\n").write(body)
    print("Đã ghi", os.path.normpath(OUT), f"({len(CANH)} cảnh phần 1, {len(body)} ký tự)")


if __name__ == "__main__":
    main()
