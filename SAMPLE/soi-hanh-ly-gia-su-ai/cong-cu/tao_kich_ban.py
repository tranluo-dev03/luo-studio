"""Sinh lại SAMPLE/soi-hanh-ly-gia-su-ai/KICH-BAN-SOI-HANH-LY-GIA-SU-AI.txt (13 cảnh phần 1 + phần 2 ghép 2 lớp).
Sửa bảng SC (từng cảnh) hoặc các khối chữ rồi chạy: runtime\\python.exe SAMPLE\\soi-hanh-ly-gia-su-ai\\cong-cu\\tao_kich_ban.py
Camera đo trên video mẫu (OpenCV, điểm nền): chỉ đoạn mở đầu có chuyển động (cận nhân viên -> lia xuống theo tay tới vali -> lia nhanh sang người mẹ);
toàn cảnh đứng yên tuyệt đối, cận hai người chỉ rung vài px. Cú lia nhanh từ nhân viên sang người mẹ làm bằng "Chuyển cảnh: lia phải" ở cảnh 2
(ffmpeg, types/_chung/nhieu_phan.whip_pan; video mẫu cũng cắt ngay giữa cú lia), cảnh 1 camera đứng yên tuyệt đối (lần chạy thật: Muse biến "nghiêng theo tay" thành lia sang mẹ con, ngón tay trông như chỉ vào em bé)."""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "KICH-BAN-SOI-HANH-LY-GIA-SU-AI.txt")

HEAD = """[HAU KY]:
loai: soi-hanh-ly-gia-su-ai

[GHI CHU]:
Thể loại "soi hành lý + gia sư AI": MỘT dự án 2 phần, Studio chạy bằng code riêng app/production/types/soi-hanh-ly-gia-su-ai/gen.py
(cùng cơ chế với san-bay-gia-su-ai, logic chung ở types/_chung/nhieu_phan.py). Kịch bản sinh bằng cong-cu/tao_kich_ban.py: sửa ở đó rồi chạy lại.
  PHẦN 1 (cảnh thường, 13 cảnh): nhân viên soi chiếu (CANBO, đứng TRÁI sau băng chuyền) hỏi người mẹ địu con nhỏ (HOC, đứng PHẢI) về chiếc vali
         bị máy soi báo. Góc máy như video mẫu: cảnh 1 là CÚ LIA trong một clip: Studio gen trước một ảnh ngang 16:9 tổng quan
         ("Ảnh tổng quan": nhân viên trái, vali giữa, người mẹ phải), cắt phần trái làm khung đầu ("Khung đầu cắt: trái") và gửi kèm ảnh
         tổng quan khi gen video, để Muse lia theo tay nhân viên qua vali tới người mẹ đúng bố cục; cảnh 2 người mẹ trả lời, nối từ khung cuối
         cảnh 1; cảnh 3-7 toàn cảnh đứng yên; cảnh 8-13 cận hai người. Cảnh 3, 8 có "Prompt ảnh" riêng (Studio gửi kèm ảnh tổng quan để giữ
         cùng bối cảnh, đạo cụ); các cảnh còn lại nối từ khung cuối cảnh trước. Gắn ảnh tham chiếu mặt cho CANBO và HOC.
         Người nghe luôn nhìn theo tay người nói (vali, điện thoại): mỗi cảnh ghi hành động của CẢ HAI người theo từng nhịp.
  PHẦN 2 (ghép 2 lớp, mỗi lượt một cảnh): gen RIÊNG video người mẹ quay selfie (HOC, nền toàn khung 9:16) và video robot AI (DAY, ô bo góc
         góc trên phải: x 0.691, y 0.025, rộng 0.284, cao 0.258 = 306x495 px -> gen 9:16; đo bằng SAMPLE/_chung/do-vi-tri-dau.py --noi-ngang 0.15 trên người mẹ gen thật để không che mặt), rồi ghép; không viền;
         nối khung ("noi: lien"): clip sau của mỗi nhân vật bắt đầu từ khung cuối clip trước của chính nó. Vào phần 2 bằng nhoè chuyển động 0,5 giây.
  Lượt thoại: LUOT chung, mỗi lượt có "phan": 1 hoặc 2 (lượt phần 1 đứng trước). Phần 1 cần đúng 13 lượt (= 13 CẢNH).
  Hậu kỳ riêng (post.py, kiểu trong config.json): phần 1 chữ trắng viền đen; phần 2 AI chữ vàng, người mẹ chữ trắng;
         "fx" wrong/right viền đỏ/xanh + tiếng, "icon" x/check. Badge "Talka AI" góc trên trái: Thương hiệu -> logo cố định của dự án.
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.

===== PHAN 1: SOI CHIEU HANH LY =====

[STYLE LOCK]:
Vertical 9:16 photorealistic video at an airport security checkpoint, bright daylight from tall windows mixed with even fluorescent ceiling light, natural colours, the look of a real documentary moment. Each clip uses the camera angle described in its start frame. The camera stays still in every clip, except a clip that describes a CAMERA MOVE. The same two characters, the same place and the same props in every clip. No text, no letters, no logos, no captions, no icons, no lettering on the uniform, badge, scanner screen, signs or phone anywhere in the frame.

[CHAR LOCK]:
The {{VAI_CANBO}}, {{TEN_CANBO}} ({{POS_CANBO}}): {{NGUOI_CANBO}}. VOICE LOCK OFFICER: one single voice, {{GIONG_CANBO}}, the same in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}, carrying {{DAO_BE}} on her chest, {{DAO_TUI}} on her shoulder. {{DAO_GIU}} VOICE LOCK MOTHER: one single voice, {{GIONG_HOC}}, the same in every clip.
When silent, the officer {{NGHE_CANBO}}; when silent, the mother {{NGHE_HOC}}.
INTERACTION: the two react to each other like real people in one continuous moment. When one points at, touches or holds up something, the other's eyes follow it to that exact object, then come back to the speaker's face. Pointing is precise: the index finger aims straight at the named object.
EYE LINE (every clip, whoever speaks): the speaker looks at the other person or at the object named in the clip, as given in the clip's EYE LINE; the speaker's head never turns toward the camera, to the side or out of the frame while talking. Nobody looks into the lens.
RULE: in each clip exactly ONE character speaks, one line, with lip-sync, keeping the EYE LINE. The other character stays silent the whole clip, mouth closed, but stays alive and reacts with the eyes and face as the clip describes. A character who is not in the shot never appears. The baby sleeps the whole time and makes no sound. Each voice stays the same in every clip.
ACTION CLIPS: the actions are done WHILE the line is spoken, in the order given, and are complete by the last word. Props, the same in every clip: {{DAO_VALI}} lies flat on the roller conveyor directly between the two, in front of the mother and within easy reach of the officer's right hand, lid facing up; {{DAO_VALI_2}} lies behind it nearer the camera; {{DAO_DIEN_THOAI}} appears only when a clip's action says so, never duplicated.

[SET LOCK]:
{{NEN_SOI}}. The travellers in the far background are small, softly out of focus and stand still; nobody walks through the foreground. The X-ray conveyor is switched OFF and completely still: the rollers do not turn, and the suitcases, the phone, the bags and the baby stay exactly where they are in the start frame for the whole clip; nothing slides, drifts, rolls or shifts, only the people move.

[VIDEO SUFFIX]:
STATIC SET (every clip except the opening one): the conveyor is off, so the rollers never turn and every suitcase sits motionless on it exactly as in the start frame; the only things that move are the people, and the suitcases are only touched when the action says so.
Camera: still in every clip (no pan, no tilt, no zoom) unless the clip describes a CAMERA MOVE; never shaky, never a cut. The speaker starts talking right away at a quick, natural, unscripted conversational pace (about 4.5 to 5 words per second, short lines up to 6, no long pauses), like a real exchange at a busy checkpoint, and finishes the line promptly. After the last word (and the action, if the clip has one) the speaker relaxes with the mouth closed, while the other keeps listening naturally, until the end of the clip (the usual rest pose: {{DAO_NGHI}}). Both sound like real people caught on camera, not actors and not a voice-over: relaxed natural pitch movement, everyday volume, not over-enunciated, no theatrical emphasis, no radio-announcer polish; small natural breaths and tiny hesitations are fine. Sound: two real voices close to the camera in the natural acoustics of a large airport hall (a light natural room reverb), no music, no announcements, no crowd chatter over the voices, no baby sounds. No subtitles, no text. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, icons, emoji, lettering on the uniform, badge, scanner screen, signs or phone; split screen, overlay, inset window; anyone looking into the lens; the speaker turning the face to the camera, to the side or out of the frame; pointing at the wrong thing, sideways or vaguely into the air; pointing at the baby, the mother or any person; the listener staring blankly while the other points or shows something; shaky handheld camera, random zoom, a camera move the clip does not ask for, a cut; two voices in one clip; the silent character moving the mouth; the baby waking, crying, moving or disappearing; extra people in the foreground; people walking in the background; moving conveyor, turning rollers, suitcases sliding, drifting, rolling or changing position on their own; face, hair or outfit changing; hands going to the head, face or hair; one character copying the other's movements; background music, announcements; robotic, text-to-speech or announcer voice; silent clip with no speech; suitcases or phone multiplying, vanishing or moving by themselves; readable text or app interface on the phone; slow, dragged speech.
"""

ANGLE = {
    "A1": ("CAMERA ANGLE: MEDIUM SHOT OF THE OFFICER from slightly above chest height: {{TEN_CANBO}} stands left of centre at the grey X-ray conveyor, seen from the thighs up, body turned "
           "three-quarters to the right, head bowed, looking DOWN at the suitcase; {{DAO_VALI}} lies flat on the rollers in the lower centre of the frame, right in front of him and "
           "directly below his right hand; the right part of the frame shows only the empty conveyor and the hall behind: nobody else, no arm, no hand, no baby at the edge of the frame; "
           "behind him {{NEN_SOI}}. The officer is the only person in the shot."),
    "A": ("CAMERA ANGLE: WIDE SHOT of the security checkpoint from chest height, slightly from the side of the conveyor: {{TEN_CANBO}} stands at the LEFT behind the X-ray conveyor, "
          "seen from the knees up, face and body in three-quarter profile turned toward the right; {{TEN_HOC}} stands at the RIGHT edge of the frame, turned three-quarters toward the left, "
          "facing him, her face in clear three-quarter profile; between them, in the middle, the grey X-ray scanner tunnel with a small monitor on top (blurry grey image, no text); "
          "the roller conveyor runs diagonally through the lower half of the frame: {{DAO_VALI}} lies flat on it directly between them, in front of the mother and within easy reach "
          "of the officer's right hand, lid facing up; {{DAO_VALI_2}} in the foreground nearer the camera; behind them {{NEN_SOI}}."),
    "C": ("CAMERA ANGLE: CLOSE TWO-SHOT at head height: {{TEN_CANBO}} at the LEFT edge of the frame, cut off by the frame below the chest, his head and shoulder in three-quarter profile "
          "turned to the right toward the mother; {{TEN_HOC}} at centre-right, chest-up, turned three-quarters to the left toward him, her face large, clear and well lit; "
          "the dark edge of {{DAO_VALI}} along the bottom of the frame; behind them {{NEN_SOI}}, softly out of focus, with a long line of travellers standing still far away."),
}
ANGLE_VN = {
    "A1": "góc A1 cận trung nhân viên một mình (từ đùi trở lên) ở băng chuyền, vali xanh giữa-dưới khung ngay dưới tay ông; camera đứng yên",
    "B": "góc B cận người mẹ một mình (từ eo trở lên), quay 3/4 về mép trái nơi nhân viên đứng ngoài khung; vào cảnh bằng lia nhanh sang phải",
    "A": "góc A toàn cảnh: nhân viên đứng TRÁI sau băng chuyền, người mẹ đứng PHẢI (mép khung), máy soi ở giữa, vali xanh nằm giữa hai người trên băng chuyền",
    "C": "góc C cận hai người: nhân viên ở mép TRÁI (cắt ngang ngực, nghiêng 3/4), người mẹ giữa-phải, mặt to rõ",
}
ANGLE["B"] = ("CAMERA ANGLE: MEDIUM CLOSE-UP OF THE MOTHER ALONE: {{TEN_HOC}} from the waist up, slightly right of centre, turned three-quarters toward the left edge of the frame, "
              "where the officer stands just off-screen; the top of {{DAO_VALI}} at the bottom edge of the frame; behind her {{NEN_SOI}}, softly out of focus. "
              "The mother is the only person in the shot.")
# Cảnh 1 = cú lia trong MỘT clip. Studio gen trước ảnh ngang tổng quan ("Ảnh tổng quan"), cắt phần trái làm khung đầu ("Khung đầu cắt: trái")
# và gửi kèm ảnh tổng quan cho bước gen video, để Muse biết người mẹ ở đâu khi lia.
# Lần chạy thật 15:08 (03/11): ảnh đúng, nhưng khi máy lia ông NHẤC tay chĩa theo hướng máy, cuối cú lia ngón tay dừng trước em bé; máy trôi đều ~2 s, không vụt.
# Nguyên nhân: "keeps pointing" + "camera follows his pointing arm" -> Muse cho tay đi theo camera. Sửa: vali nằm ngay dưới tay ông TRONG khung đầu, ông chỉ dốc xuống
# trong lúc nói, nói xong hạ tay về hông, RỒI máy mới vụt sang người mẹ (sau lời); "Lia nhanh: 3" để engine tua nhanh cú lia + nhoè ngang cho có lực.
# Lần 5 (user, sau lần chạy thứ hai): cú lia sang người mẹ đã ổn; muốn máy LIA THEO TAY như video mẫu (ông giơ tay chỉ là máy đi cùng), và trước câu hỏi có
# một đoạn hành lý trôi ra khỏi máy soi. Vali nằm phía trước-bên phải ông (giữa ông và người mẹ), không còn nằm ngay dưới tay ông trong khung đầu.
# Lần 7 (user so với video mẫu): bố cục + góc máy cảnh 1 sai, thiếu đèn báo đỏ nhấp nháy khi vali ra (phát hiện bất thường). Video mẫu: máy ở độ cao ngực, đứng
# chéo bên trái băng chuyền; băng chuyền chạy XIÊN từ góc dưới-trái (vali nâu rồi vali xanh) lên miệng máy soi ở giữa-phải; trên miệng hầm có đèn đỏ-cam; màn hình máy soi
# bên trái-trên; nhân viên đứng TRÁI, một tay đặt trên máy, cúi nhìn băng chuyền; người mẹ đứng PHẢI máy soi. Cận nhân viên: ông to ở nửa trái, máy soi có đèn đỏ ngay
# sau-bên phải ông, tay chỉ chéo xuống băng chuyền ở góc dưới-phải.
ANGLE["P"] = ("CAMERA ANGLE: MEDIUM SHOT OF THE OFFICER from chest height, from the front-left of the conveyor, the left part of the wide overview: {{TEN_CANBO}} fills the left half "
              "of the frame from the waist up, body turned three-quarters toward the right, head bowed, looking DOWN at the roller conveyor; his left hand rests on top of the grey X-ray "
              "scanner behind him; behind-right of him the grey scanner with a small monitor on top (blurry grey image) and a small red-orange ALARM LIGHT bar glowing on top of the "
              "tunnel entrance; the roller conveyor runs diagonally across the lower right of the frame, {{DAO_VALI}} lying on it low at the bottom right edge, mostly just below the "
              "bottom edge of the frame; his right arm relaxed at his side; behind everything {{NEN_SOI}}. The officer is the only person in the shot.")
ANGLE_VN["P"] = ("góc cận nhân viên từ độ cao ngực, đứng chéo bên trái băng chuyền: ông to ở nửa trái khung (từ eo lên), một tay đặt lên máy soi, cúi nhìn băng chuyền; sau-bên phải ông là máy soi "
                 "có ĐÈN BÁO ĐỎ nhấp nháy trên miệng hầm, băng chuyền chạy chéo xuống góc dưới-phải; ông giơ tay chỉ chéo xuống vali ở góc dưới-phải, máy đi theo tay; "
                 "nói xong ông hạ tay, máy vụt sang phải, dừng ở cận người mẹ")
ANGLE_VN["B"] = "góc B cận người mẹ (từ eo trở lên, quay 3/4 về mép trái nơi nhân viên đứng ngoài khung), chính là chỗ cú lia cảnh 1 dừng lại"
WIDE = {1: ("WIDE OVERVIEW of an airport security checkpoint, photorealistic, bright airport daylight, camera at chest height standing at the front-left of the roller conveyor "
            "and looking diagonally across it. The roller conveyor runs DIAGONALLY from the lower-left foreground (nearest the camera) up to the grey stainless X-ray scanner at the "
            "centre-right of the frame, so the conveyor and the scanner are seen at an angle, not head-on. On top of the scanner tunnel entrance: a small red-orange ALARM LIGHT bar, lit; "
            "a small monitor with a blurry grey X-ray image (no text) on the left top of the scanner. In the LEFT 30 percent of the width: {{TEN_CANBO}} ({{NGUOI_CANBO}}) stands behind "
            "the conveyor at the left of the scanner, seen from the knees up, body turned three-quarters toward the right, head bowed, looking DOWN at the conveyor, his left hand resting on "
            "top of the scanner. On the conveyor in the lower left, near the camera: {{DAO_VALI}} lies flat on the rollers, lid up; it is the only navy suitcase in the picture. In the RIGHT 30 "
            "percent of the width, standing right of the scanner: {{TEN_HOC}} ({{NGUOI_HOC}}), seen from the waist up, carrying {{DAO_BE}}, {{DAO_TUI}} on her shoulder, turned "
            "three-quarters to the left, looking down at the conveyor with a worried face, one hand on the baby's back. Behind everything {{NEN_SOI}}. Mouths closed, the baby asleep. "
            "Nobody else in the foreground. No text, no logos, no lettering anywhere.")}
PRE = {1: ("Generate exactly one still image now, vertical 9:16, photorealistic, bright airport daylight, camera at chest height standing at the front-left of the roller conveyor, "
           "looking diagonally across it. The roller conveyor runs DIAGONALLY from the lower-left foreground up to the grey stainless X-ray scanner at the centre-right of the frame. "
           "On top of the scanner tunnel entrance: a small red-orange ALARM LIGHT bar, lit, glowing red; a small monitor with a blurry grey X-ray image (no text) on the left top of the "
           "scanner. At the LEFT: {{TEN_CANBO}} ({{NGUOI_CANBO}}), seen from the knees up, body turned three-quarters toward the right, left hand resting on top of the scanner, looking DOWN at "
           "the conveyor. At the RIGHT, right of the scanner: {{TEN_HOC}} ({{NGUOI_HOC}}), carrying {{DAO_BE}}, {{DAO_TUI}} on her shoulder, looking down at the conveyor. "
           "{{DAO_VALI}} is just coming out of the dark tunnel opening onto the rollers. Mouths closed, the baby asleep. Nothing hangs from the ceiling or across the top of the "
           "frame: no curtain, no strips, no fabric. No text, no logos, no lettering anywhere. Output only the image.",
           "Start exactly from the start-frame image. THIS CLIP OVERRIDES the set lock about a still conveyor: here, and only here, the conveyor is switched ON and the rollers DO turn: {{DAO_VALI}} comes out of the scanner tunnel and rolls down the diagonal conveyor toward the "
           "camera SLOWLY, at a calm steady pace, taking about three full seconds to come out, and then rests still. The moment it comes out, the small red-orange ALARM LIGHT on top of the tunnel entrance starts flashing red, blinking on and off several times (the scanner has "
           "detected something abnormal). Both the officer and the mother watch the suitcase come out, their eyes following it down the conveyor; nobody points yet. The camera stays "
           "still. No curtain or strips anywhere. Nobody speaks; only the rumble of the rollers, a short electronic beeping alarm, and quiet airport ambience. No text.",
           "3.0")}
CROP = {1: "trái"}
# engine giữ yên phần dưới khung (băng chuyền, vali) như khung đầu, chỉ người cử động: Muse vẫn cho vali trượt dù đã dặn "conveyor off" (lần chạy 18:00 03/11:
# cảnh 2, 5, 6, 9, 12). Mốc = tỉ lệ chiều cao nơi vùng băng chuyền bắt đầu ở từng góc máy; cảnh có CAMERA MOVE không dùng.
FREEZE_Y = {"A": 0.55, "C": 0.8}   # góc B (cận mẹ sau cú lia): Muse hay trôi máy, phần dưới lấy từ khung đầu hiện bóng mờ
FOLLOW = {1: 1.0}   # engine: 1 giây máy đẩy vào + trôi xuống-phải theo tay tới vali ngay trước cú vụt (lần 15:43: Muse để máy đứng yên khi ông giơ tay chỉ)
FAST = {1: 3}   # engine tua nhanh cú lia sau lời 3 lần + nhoè ngang (Muse lia chậm ~2 s; video mẫu ~0,4 s)
CAM_PAN = ("CAMERA MOVES (the only clip with camera moves). First, WITH THE GESTURE, during the line: as the officer raises his right arm and points steeply DOWN and toward "
           "the camera at {{DAO_VALI}} lying low in front of him, the camera moves down along his arm to his fingertip and the suitcase lid just below it, with the red alarm light on the scanner still blinking behind him (reference image #2 shows "
           "where the suitcase and the mother are). His fingertip stays aimed down at the suitcase lid; the arm never swings sideways or toward the mother. Second, right after the last "
           "word he lowers his hand, and then the camera makes ONE fast whip pan to the RIGHT, sudden and hard like a handheld camera swinging, with strong horizontal motion blur, and "
           "stops abruptly on a medium shot of the mother on the other side of the conveyor, from the waist up, turned three-quarters toward the left, worried, one hand on the baby's "
           "back, looking toward the officer off-screen at the left, the navy suitcase at the lower left of her shot. The officer's hand never enters her shot. Nobody new appears; no "
           "cut. After the whip the camera holds still on the mother")
WHO = {"A1": "In the shot: {{TEN_CANBO}} ({{NGUOI_CANBO}}).", "P": "In the shot: {{TEN_CANBO}} ({{NGUOI_CANBO}}).",
       "B": "In the shot: {{TEN_HOC}} ({{NGUOI_HOC}}), carrying {{DAO_BE}}, {{DAO_TUI}} on her shoulder."}
BOTH = "In the shot: {{TEN_CANBO}} ({{NGUOI_CANBO}}). In the shot: {{TEN_HOC}} ({{NGUOI_HOC}}), carrying {{DAO_BE}}, {{DAO_TUI}} on her shoulder."
EYE_A = "EYE LINE: the officer looks at the mother's face (to the right), the mother looks at the officer's face (to the left), both in three-quarter profile; nobody looks into the lens"
EYE_C = "EYE LINE: the officer looks at the mother's face (to the right), the mother looks at the officer's face (to the left); nobody looks into the lens"
# Lần chạy thật đầu tiên (03/11): ông chỉ ngang sang phải về phía mẹ con thay vì chỉ xuống vali -> tay phải chĩa XUỐNG, mắt nhìn vali, cấm chỉ ngang / chỉ vào người
POINT = ("points DOWN at {{DAO_VALI}}: his right arm angles steeply down and forward over the conveyor, the hand below his waist, the index finger aimed straight down at the middle "
         "of the suitcase lid with the fingertip a few centimetres above it; the finger points down at that suitcase only, never sideways, never level with the chest, "
         "never toward the edge of the frame, the mother or the baby")

# (n, thời gian mẫu, góc, ảnh mới?, khung đầu VN, diễn biến VN, khung cuối VN, ACTION EN, EYE LINE EN, pose khung đầu EN, CAMERA MOVE EN, giữ sau lời (giây), chuyển cảnh)
SC = [
    (1, "0:00–0:01", "P", True,
     "Cắt từ phần trái ảnh tổng quan: cận nhân viên từ eo trở lên, tay phải buông, cúi nhìn chiếc vali xanh nằm thấp ngay trước mặt ông (ngay dưới mép khung). Miệng khép.",
     "Trước câu hỏi: đoạn mở đầu không lời ~1,2 s ở góc toàn cảnh A (như ảnh mẫu): vali xanh lăn ra khỏi hầm máy soi, cả nhân viên và người mẹ cùng nhìn theo, chưa ai chỉ (gen riêng, ghép trước). "
     "Rồi cắt sang cận nhân viên: ông vừa hỏi vừa giơ tay phải chỉ dốc XUỐNG chiếc vali nằm thấp trước mặt (về phía máy quay, không duỗi ngang), máy đi theo tay xuống tới đầu ngón tay và nắp vali. "
     "Ngón tay luôn chĩa xuống nắp vali, không chĩa về phía người mẹ hay em bé. Nói xong ông hạ tay, RỒI máy vụt sang phải (nhoè ngang mạnh), dừng gọn ở cận người mẹ "
     "bên kia băng chuyền, mặt lo, một tay trên lưng em bé, nhìn về phía nhân viên (ngoài khung bên trái), vali xanh ở góc dưới bên trái khung.",
     "Cận người mẹ một mình (từ eo trở lên), quay 3/4 về mép trái, mặt lo, một tay trên lưng em bé, nhìn về phía nhân viên ngoài khung bên trái; miệng khép.",
     "on 'Is this' the officer raises his right arm and points steeply DOWN and toward the camera at {{DAO_VALI}} lying low in front of him, the index finger aimed at the middle "
     "of the lid; on the word 'bag' he gives one small jab of the finger down toward the lid; his arm never swings sideways and never points toward the mother or the baby; right "
     "after the last word he lowers his hand to his side",
     "EYE LINE: the officer looks down at the suitcase he points at; the mother, once the camera reaches her, looks toward the officer off-screen at the left; nobody looks into the lens",
     "the officer standing with his right arm relaxed at his side, head bowed, looking down at the suitcase low in front of him",
     CAM_PAN, "2.5", None),
    (2, "0:01–0:02", "B", False, "",
     "Người mẹ trả lời ngay, gật nhẹ, mặt lo, mắt nhìn về phía nhân viên ở mép trái khung; tay phải rời lưng em bé, ngửa lòng bàn tay chỉ xuống chiếc vali ở góc dưới bên trái, rồi đặt lại lên lưng em bé.",
     "Người mẹ miệng khép, một tay trên lưng em bé; cảnh sau là góc toàn cảnh (có ảnh riêng).",
     "she gives a small worried nod and opens her free hand palm-up toward the suitcase at the lower left of the frame, then rests it on the baby's back again",
     "EYE LINE: the mother looks toward the officer just off-screen at the left edge of the frame, eyes level, not into the lens",
     "", None, None, None),
    (3, "0:02–0:04", "A", True,
     "Góc A: nhân viên đứng sau băng chuyền, tay phải đặt trên mép máy soi; người mẹ một tay trên lưng em bé; hai người nhìn nhau, miệng khép.",
     "Nhân viên nói 'The scanner detected something' và chỉ ngón trỏ thẳng vào nắp vali xanh; tới 'Please open your bag' ông ngửa bàn tay về phía khoá kéo của vali. "
     "Người mẹ nhìn theo tay ông xuống chiếc vali; ở chữ cuối cô đã rời tay khỏi lưng em bé, đưa tay về phía nắp vali. Tay trái nhân viên đặt trên nóc máy soi suốt câu.",
     "Nhân viên hạ tay phải; tay người mẹ vươn tới sát nắp vali; cả hai nhìn chiếc vali; miệng khép.",
     f"on the first sentence the officer {POINT}, his left hand resting on top of the scanner; on the second sentence he turns his right hand palm-up toward the suitcase zipper as if inviting her to open it, then lowers it; the mother's eyes follow his hand down to the suitcase, and on the last word she already reaches her free hand toward the suitcase lid",
     "EYE LINE: the officer looks at the suitcase as he points, then at the mother's face; the mother follows his hand to the suitcase, then looks up at him; nobody looks into the lens",
     "the officer standing behind the conveyor with his right hand resting on the edge of the scanner, the mother with one hand resting on the baby's back", None, None, None),
    (4, "0:04–0:07", "A", False, "",
     "Người mẹ bước sát lại, đặt cả hai bàn tay lên nắp vali xanh (tay trái gần quai, tay phải gần khoá kéo) khi nói 'Of course. It might be batteries'; "
     "tới câu hỏi 'Would you like me to take them out?' cô ngước lên nhìn nhân viên. Nhân viên nhìn theo tay cô xuống vali rồi nhìn lại mặt cô.",
     "Hai tay người mẹ đặt trên nắp vali, mắt nhìn nhân viên; nhân viên tay trên mép máy soi; miệng khép.",
     "the mother leans in and places both hands flat on the lid of {{DAO_VALI}} (left hand near the handle, right hand near the zipper), glancing down at it, then looks up at the officer on the question; the officer's eyes follow her hands to the suitcase, then return to her face",
     "EYE LINE: the mother looks at the suitcase under her hands, then at the officer's face on the question; the officer watches her hands, then her face; nobody looks into the lens",
     "", None, None, None),
    (5, "0:07–0:09", "A", False, "",
     "Nhân viên gật một cái ở chữ 'Yes', rồi ngửa tay trái về phía người mẹ khi hỏi. Trong lúc ông hỏi, người mẹ nhấc hai tay khỏi vali, đưa tay phải về lưng em bé.",
     "Người mẹ đứng thẳng, một tay trên lưng em bé; nhân viên hạ tay; miệng khép.",
     "the officer gives one short nod on 'Yes', then opens his left hand toward the mother as he asks; meanwhile the mother lifts her hands off the suitcase and brings one hand back to the baby's back",
     EYE_A, "", None, None, None),
    (6, "0:09–0:11", "A", False, "",
     "Người mẹ mỉm cười, gật nhẹ, tay rảnh đưa nhẹ trước ngực khi nói về con gái. Nhân viên nghe, gật nhẹ một cái.",
     "Người mẹ mỉm cười, một tay trên lưng em bé; nhân viên đứng im; miệng khép.",
     "the mother smiles and makes a small warm gesture at chest height with her free hand, then rests it on the baby again; the officer gives a small nod as he listens",
     EYE_A, "", None, None, None),
    (7, "0:11–0:12", "A", False, "",
     "Nhân viên nhướng mày, ngửa một bàn tay ra ngang hông về phía người mẹ như khen, mỉm cười nhẹ, rồi hạ tay. Người mẹ cười tươi hơn, gật nhẹ.",
     "Nhân viên đứng thẳng, tay hạ; người mẹ cười, một tay trên lưng em bé; miệng khép. Hết góc A.",
     "the officer raises his eyebrows and opens one hand palm-up at waist height toward the mother in an impressed, approving gesture, then lowers it; the mother's smile widens and she gives a small nod",
     EYE_A, "", None, None, None),
    (8, "0:12–0:15", "C", True,
     "Góc C: nhân viên mép trái nhìn sang phải, người mẹ giữa-phải nhìn nhân viên, một tay trên lưng em bé, mỉm cười, miệng khép.",
     "Người mẹ cười tươi ở 'Thank you', hai tay vẫn trên lưng em bé; tới 'I've been practicing' tay phải rời em bé, ngửa ra trước ngực như kể, mặt tự hào, rồi đặt lại lên lưng bé. Nhân viên nghe, mặt bình thản, nhìn cô.",
     "Người mẹ mỉm cười, một tay trên lưng em bé; nhân viên nhìn người mẹ; miệng khép.",
     "the mother beams on 'Thank you' with both hands still on the baby; on 'I've been practicing' she lifts her right hand off the baby and opens it palm-up in front of her chest as she explains, proud, then rests it on the baby again; the officer listens with a calm face, eyes on her",
     EYE_C,
     "the officer looking at the mother, the mother smiling with one hand resting on the baby's back", None, None, None),
    (9, "0:15–0:15", "C", False, "",
     "Nhân viên hỏi, hơi nghiêng đầu, nhướng mày tò mò, vẫn nhìn người mẹ (mặt nghiêng 3/4, không quay ra ống kính). Người mẹ mỉm cười.",
     "Như khung đầu; hai người miệng khép.",
     "the officer tilts his head slightly and raises his eyebrows with curiosity; the mother keeps smiling",
     EYE_C, "", None, None, None),
    (10, "0:15–0:19", "C", False, "",
     "Người mẹ vừa nói vừa đưa điện thoại từ bên hông phải lên, giơ ngang ngực giữa hai người, màn hình quay về phía nhân viên (camera thấy chân dung hoạt hình); tay kia ngửa ra giải thích. "
     "Mắt nhân viên nhìn xuống màn hình điện thoại và dừng ở đó.",
     "Người mẹ giơ điện thoại ngang ngực, màn hình quay ra; nhân viên nhìn điện thoại; miệng khép.",
     "the mother brings {{DAO_DIEN_THOAI}} up from her right side and holds it at chest height between them with the screen turned toward the officer, while her other hand makes a small open explaining gesture; the officer's eyes drop to the phone screen and stay on it",
     "EYE LINE: the mother looks at the officer's face while she talks; the officer looks down at the phone screen in her hand; nobody looks into the lens", "", None, None, None),
    (11, "0:19–0:22", "C", False, "",
     "Người mẹ tiếp tục nói, tự hào, vẫn giơ điện thoại, tay kia đặt lên lưng em bé. Cuối câu nhân viên ngước từ điện thoại lên nhìn cô, gật nhẹ như thấy ấn tượng.",
     "Người mẹ vẫn giơ điện thoại; nhân viên nhìn người mẹ; miệng khép.",
     "the mother keeps holding the phone up and rests her other hand on the baby; near the end of her line the officer raises his eyes from the phone to her face with a small impressed nod",
     "EYE LINE: the mother looks at the officer's face; the officer looks at the phone, then up at her face; nobody looks into the lens", "", None, None, None),
    (12, "0:22–0:23", "C", False, "",
     "Nhân viên hỏi, mặt hơi nghi ngờ, liếc xuống màn hình điện thoại, tay phải ngửa thấp ngang hông, rồi nhìn lại người mẹ. Người mẹ mỉm cười biết ý, vẫn giơ điện thoại.",
     "Như khung đầu; miệng khép.",
     "the officer glances down at the phone screen and opens his right hand palm-up low at hip height as he asks, then looks back at the mother with a slightly doubtful face; the mother keeps the phone up and smiles knowingly",
     EYE_C + " (the officer glances at the phone once)", "", None, None, None),
    (13, "0:23–0:26", "C", False, "",
     "Người mẹ cười, lắc đầu hai cái ở 'No, no'; ở 'it's free' cô xoay điện thoại về phía mình, cầm bằng hai tay trước ngực; tới 'Let me show you' cô chạm màn hình bằng ngón cái; nhân viên nghiêng người lại, cúi nhìn màn hình, cả hai cùng nhìn điện thoại. Nửa giây cuối máy đẩy nhẹ vào hai người. Hết phần 1 (sau đó nhoè chuyển sang phần 2).",
     "Người mẹ cầm điện thoại trước ngực, nhìn xuống màn hình; nhân viên cũng nhìn điện thoại; miệng khép.",
     "the mother shakes her head twice with a laugh on 'No, no'; on 'it's free' she turns {{DAO_DIEN_THOAI}} toward herself and holds it in both hands at chest height; on 'Let me show you' she taps the screen with her thumb; the officer leans in and looks down at the screen, so both look at the phone together; in the last half second the camera pushes in slightly toward the two of them (the only camera move of this clip, smooth, no shake)",
     "EYE LINE: the mother looks at the officer's face at the start of the line, then down at the phone as she taps it; the officer looks at the phone; nobody looks into the lens", "",
     "CAMERA MOVE: the camera stays still for most of the clip; only in the last half second it pushes in slightly and smoothly toward the two of them, no pan, no shake", None, None),
]

# Ngữ điệu từng câu (nghe video mẫu + cao độ đo: nhân viên ~130-150 Hz, người mẹ ~200-230 Hz). Câu kể hạ giọng cuối câu, câu hỏi yes/no lên giọng cuối câu.
DELIV = {
    1: "routine, low and flat, a tired officer on a long shift, not accusing; a small natural rise on 'bag'",
    2: "quick and a little anxious, slightly breathy, a touch higher than her normal voice",
    3: "matter-of-fact and even, the pitch falling at the end of each sentence; 'Please open your bag' polite but routine",
    4: "eager to cooperate: 'Of course' quick; 'It might be batteries' a little apologetic with a light uncertain lift; the question helpful, rising at the end",
    5: "'Yes' short and flat; the question softer and more conversational, rising at the end, a hint of friendliness",
    6: "relaxed and warm, a smile audible in the voice, her own accent natural",
    7: "genuinely surprised and warmer, a small smile in the voice; 'by the way' tossed off lower and quicker",
    8: "'Thank you' with a small bashful laugh, then brighter and proud",
    9: "short, curious, a little skeptical, rising at the end",
    10: "animated and a bit faster, explaining with enthusiasm, natural accent, not rehearsed",
    11: "proud and smiling, slowing slightly on 'this confidently'",
    12: "lower and doubtful, half-joking, 'though' trailing off",
    13: "laughing lightly on 'No, no', reassuring; 'it's free' bright; 'Let me show you how it works' eager and a little faster",
}
AUDIO = "Audio: Chỉ giọng của một nhân vật, gần, rõ, tự nhiên như hội thoại thật, có độ vang nhẹ của sảnh lớn; nói nhanh và xong sớm. Không nhạc, không tiếng loa, không tiếng ồn đè lên giọng, không tiếng em bé."
NEG = "Negative prompt: two voices; the silent character moving the mouth; text or captions; split screen; anyone looking into the lens; pointing at the wrong object, sideways or at a person or the baby; people moving in the background; the baby waking or crying; no speech."
PACE = "Quick natural unscripted pace, about 4.5 to 5 words per second (short lines up to 6), no long pauses."

out = [HEAD]
for n, t, ang, img, kd, db, kc, act, eye, pose, cam, keep, trans in SC:
    out.append(f"\nCẢNH {n} ({t}): Lượt {n}")
    out.append(f"Bối cảnh: {ANGLE_VN[ang]}; không có chữ." + (" Đổi góc máy: khung đầu gen mới." if img else " Nối từ khung cuối cảnh trước."))
    out.append(f"Voice: (English, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}")
    out.append(f"Khung đầu: {kd}" if img else "Khung đầu: Chính là khung cuối của cảnh trước.")
    out.append(f"Khung cuối: {kc} Khung này là khung đầu của cảnh sau.")
    out.append(f"Diễn biến: {db}")
    if keep:
        out.append(f"Giữ sau lời: {keep}")
    if trans:
        out.append(f"Chuyển cảnh: {trans}")
    if n in WIDE:
        out.append(f"Ảnh tổng quan: {WIDE[n]}")
        out.append(f"Khung đầu cắt: {CROP[n]}")
    if n in FAST:
        out.append(f"Lia nhanh: {FAST[n]}")
    if n in FOLLOW:
        out.append(f"Lia theo tay: {FOLLOW[n]}")
    if ang in FREEZE_Y and not cam:
        out.append(f"Giữ yên dưới: {FREEZE_Y[ang]}")
    if n in PRE:
        out.append(f"Mở đầu ảnh: {PRE[n][0]}")
        out.append(f"Mở đầu video: {PRE[n][1]}")
        out.append(f"Mở đầu dài: {PRE[n][2]}")
    if img:
        out.append("Prompt ảnh: Generate exactly one still image now, vertical 9:16, photorealistic, a single frame with no split screen, bright airport daylight. "
                   f"{ANGLE[ang]} {WHO.get(ang, BOTH)} Pose: {pose}. {eye}. " + ("His mouth closed, a firm calm face. " if ang in ("A1", "P") else "Mouths closed, calm natural expressions, the baby asleep. ")
                   + "Only the characters named here are visible in the foreground. No text, no logos, no lettering anywhere. Output only the image.")
    start = "Start exactly from the start-frame image." if img else "Start exactly from the provided start frame (the last frame of the previous clip) and continue from it with no cut or reset."
    solo = ang in ("A1", "B")
    other = "the mother" if ang == "A1" else "the officer"
    camera = f" {cam}." if cam else (" LOCKED CAMERA: the camera does not move at all (no pan, no tilt, no zoom); the framing stays exactly as in the start frame, the suitcase stays right under his finger, "
                                      "and the mother and the baby never enter the frame." if ang == "A1" else " The camera stays still.")
    out.append(f"Prompt video: STYLE LOCK, SET LOCK. {start} CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} Only that character speaks, with lip-sync, "
               f"and keeps the EYE LINE while speaking ({eye.replace('EYE LINE: ', '')}); "
               + (f"{other} stays off-screen and is not heard. " if solo else "" if ang == "P" else "the other keeps the mouth closed and reacts as described. ")
               + f"{PACE} ACTION, done WHILE the line is spoken, in this order, complete by the last word: {act}.{camera} "
               + ("the mother, once the camera reaches her, keeps her mouth closed and reacts as described. " if ang == "P" else "")
               + ("After the line the camera holds on the mother, mouth closed, worried, looking toward the officer off-screen at the left" if ang == "P" else
                  ("After the line he holds the pointing pose with the mouth closed" if ang == "A1" else "After the line she relaxes with the mouth closed") if solo else "After the line the speaker relaxes with the mouth closed and the other keeps listening naturally")
               + ("" if ang == "A1" else "; the baby keeps sleeping") + f". DELIVERY of this line: {DELIV[n]}; a real person talking, not acting for the camera. Same voices as always, natural hall acoustics, no music. VIDEO SUFFIX.")
    out.append(AUDIO)
    out.append(NEG)

out.append("""
===== PHAN 2: NGUOI ME + GIA SU AI (GHEP 2 LOP) | vao: nhoe 0.5 =====

[GHEP HAI LOP]:
nen: HOC
khung DAY: 0.691, 0.025, 0.284, 0.258
bo goc: 0.03
vien: khong
noi: lien
nghe: moi canh

[STYLE LOCK]:
Vertical short-form social video look, bright natural daylight, crisp focus on the face, realistic skin, hair and fabric detail for the real person, glossy clean high-end CGI for the robot. No text, captions, logos, icons or watermarks anywhere in the frame.

[NHAN VAT HOC]:
{{TEN_HOC}}: {{NGUOI_HOC}}, carrying {{DAO_BE}} on her chest, {{DAO_TUI}} on her left shoulder. She films herself selfie-style with the phone's front camera held at arm's length in her right hand: her extended right arm comes in from the lower-left corner of the frame (the phone itself is not visible), her left hand rests on the baby's back. Slightly high angle, framed from the waist up; her head is a little left of centre with the top of the head at about one fifth of the frame height; the top-right corner of the frame (right third, top quarter) shows only calm background, because it is covered later by a small tutor window; her head always stays clearly left of that corner and she never leans toward the right. Behind her: {{NEN_HOC}}. The camera stays steady (almost no shake). She looks into the lens while speaking, as if talking to the AI tutor on the phone; when she has to think of an English word she glances briefly up and to the side, then back to the lens. Small natural nods and facial expressions while speaking; her left hand may lift from the baby for a small gesture and always comes back to rest on the baby. The baby sleeps the whole time. VOICE: {{GIONG_HOC}}, the same timbre, pitch and loudness in every clip; she speaks a little slower here, like someone practising a foreign language, with small natural hesitations.

[NGHE HOC]:
{{TEN_HOC}} listens to the AI tutor: friendly attentive expression and a soft smile, eyes on the lens, slow natural blinks, a small nod now and then, left hand resting on the baby. Reacts visibly and naturally to what is being said: nods along, raises the eyebrows, smiles, tilts the head, small natural shifts of the shoulders. Mouth stays closed the whole time.

[NHAN VAT DAY]:
{{TEN_DAY}}: {{NGUOI_DAY}}. Portrait-oriented frame (taller than wide): the robot stands upright, head and upper body down to the waist, centred, head in the upper third, arms relaxed at the sides. Behind it: {{NEN_DAY}}. The camera is locked off and never moves. The robot looks straight into the lens. While speaking it moves its lips in clear sync with the words, with small head tilts, a warm smile and slow blinks, like a patient friendly teacher. VOICE: {{GIONG_DAY}}, the same timbre, pitch and loudness in every clip.

[NGHE DAY]:
{{TEN_DAY}} listens calmly: stands, looking into the lens, a gentle closed-mouth smile, slow blinks, a tiny head tilt now and then, arms at the sides. Reacts visibly and naturally to what is being said: nods along, raises the eyebrows, smiles, tilts the head, small natural shifts of the shoulders. Mouth stays closed the whole time.

[VIDEO SUFFIX]:
Natural spontaneous conversational delivery, not text-to-speech, not an announcer: the mother about 3 words per second with small hesitations, the tutor about 3.5 words per second, warm and encouraging; the line starts right away, light natural breaths, a smile audible in the voice when the line is positive. Clean close voice, like a video call in a quiet hall, no music, no background sound effects, no airport announcements, no baby sounds, no strong echo.

[NEGATIVE]:
text, letters, captions, subtitles, logos, icons, signs with readable words, watermark; phone or app interface in the frame; camera cuts, zoom, push-in, strong shake; a second person in the foreground; people walking in the background; the baby waking, crying or moving; face morphing, outfit change, hair change, age or style drift; distorted face; extra or missing fingers or arms; jerky or exaggerated gestures; hands touching the face or hair; slow, dragged or stretched speech; flat monotone, robotic or announcer voice; background music; echo or reverb
""")
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("ok", len(SC))
