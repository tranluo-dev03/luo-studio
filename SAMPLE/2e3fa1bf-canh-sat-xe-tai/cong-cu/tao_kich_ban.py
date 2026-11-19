"""Sinh 2 kịch bản của thể loại 2e3fa1bf-canh-sat-xe-tai (sửa ở đây rồi chạy lại):
    runtime\\python.exe SAMPLE\\2e3fa1bf-canh-sat-xe-tai\\cong-cu\\tao_kich_ban.py
  A (goc)  : KICH-BAN-2E3FA1BF-CANH-SAT-XE-TAI.txt       giữ nguyên hook + tình huống như video gốc
  B (hook) : KICH-BAN-2E3FA1BF-CANH-SAT-XE-TAI-HOOK.txt  giữ tình huống, hook (cảnh 1-2) gắn token HOOK_* để đổi câu mà không đụng cảnh 3-4
Video gốc 14,7 s: nữ tài xế nhoài ra cửa sổ cabin nói sai tuổi ("I have fifty years"), cảnh sát hỏi lại, tài xế sửa, cảnh sát khen + gợi ý học tiếng Anh với gia sư AI.
Không dùng đại từ he/she cho tài xế (nhân vật sau này đổi giới): luôn gọi "the driver". Đại từ cảnh sát: {{HE_/HIS_/HIM_CANHSAT}}."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_A = os.path.join(HERE, "..", "KICH-BAN-2E3FA1BF-CANH-SAT-XE-TAI.txt")
OUT_B = os.path.join(HERE, "..", "KICH-BAN-2E3FA1BF-CANH-SAT-XE-TAI-HOOK.txt")

TOC_DO = "a brisk natural pace, about 3.5 words per second"

GHI_CHU = """[HAU KY]:
loai: 2e3fa1bf-canh-sat-xe-tai

[GHI CHU]:
Thể loại "cảnh sát chặn xe tải, tài xế nói sai tuổi" (người thật, ảnh chân thực, 14,7 s, 4 cảnh, MỘT góc máy đứng yên). Kịch bản sinh bằng cong-cu/tao_kich_ban.py.
  Cảnh 1 có "Prompt ảnh" (khung đầu); cảnh 2-4 nối từ khung cuối cảnh trước. Tài xế (HOC) nhoài ra cửa sổ cabin ở TRÁI-TRÊN, cảnh sát (CANHSAT) đứng PHẢI dưới đường.
  HOOK = cảnh 1-2 (câu sai của tài xế + cảnh sát hỏi lại). TÌNH HUỐNG = cảnh 3-4 (tài xế sửa + cảnh sát khen, gợi ý học với gia sư AI).
  Không có phần gia sư AI trong hình: câu cuối của cảnh sát là lời quảng cáo, nói trong cảnh; logo/end card do Thương hiệu của dự án.
"""

STYLE = """[STYLE LOCK]:
Vertical 9:16 photorealistic video on the shoulder of a wide highway {{SANG}}, natural colours, the look of a real documentary moment. One fixed camera at chest height on the road shoulder, the same framing in every clip; the camera stays still. The same two characters, the same truck and the same place in every clip. No text, no letters, no logos, no captions, no icons, no lettering on the uniform, vest, badge, truck or number plate anywhere in the frame.

[CHAR LOCK]:
The {{VAI_CANHSAT}}, {{TEN_CANHSAT}} ({{POS_CANHSAT}}): {{NGUOI_CANHSAT}}. VOICE LOCK OFFICER: one single voice, {{GIONG_CANHSAT}}, the same in every clip.
The {{VAI_HOC}}, {{TEN_HOC}} ({{POS_HOC}}): {{NGUOI_HOC}}. VOICE LOCK DRIVER: one single voice, {{GIONG_HOC}}, the same in every clip.
When silent, the officer {{NGHE_CANHSAT}}; when silent, the driver {{NGHE_HOC}}.
INTERACTION: the two react to each other like real people in one continuous moment, with the eyes and the face.
EYE LINE (every clip, whoever speaks): the officer looks up at the driver in the cab window; the driver looks down at the officer. The speaker's head never turns toward the camera, to the side or out of the frame while talking. Nobody looks into the lens.
RULE: in each clip exactly ONE character speaks, one line, with lip-sync, keeping the EYE LINE. The other character stays silent the whole clip, mouth closed, but stays alive and reacts with the eyes and face as the clip describes. Each voice stays the same in every clip. Nobody holds anything: hands stay on the window sill (driver) and relaxed by the belt (officer).

[SET LOCK]:
{{NEN_DUONG}}. The truck: {{XE}}, parked on the shoulder with the engine off. Nothing moves in the background: the far scenery stands still, the sky and the trees do not move.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no shake, no cut. The speaker starts right away at """ + TOC_DO + """, like real people caught on camera, not actors, and finishes the line. After the last word both keep a calm closed-mouth face and stay still until the end of the clip. No subtitles, no text, no music, no engine, traffic or wind noise. 9:16.

[NEGATIVE]:
text, captions, subtitles, logos, icons, emoji, lettering on uniform, vest, badge or truck; the words LEFT, RIGHT or TOP or any label written in the frame; camera movement, zoom, shake, cut; two voices in one clip; the silent character moving the mouth; extra people in the foreground; passing cars, moving clouds; face, hair or outfit changing; one character copying the other's movements; the officer facing the camera; background music, engine noise; robotic or text-to-speech voice; silent clip with no speech; movement during the final still; props or phones in the hands; slow, dragged speech.
"""

ANH_DAU = ("Generate exactly one still image now, vertical 9:16, photorealistic, {{SANG}}. CAMERA ANGLE: a fixed camera at chest height "
           "on the road shoulder, a little behind and to the right of the officer, looking along the side of the truck. {{XE}} fills the left 60% of the frame, "
           "seen from its front-left corner at a slightly low angle: the windshield edge at the top-left, the open driver's window in the upper-left third and "
           "a big side mirror on a metal arm just right of that window. In the window: {{TEN_HOC}} ({{NGUOI_HOC}}), leaning out on folded forearms on the "
           "window sill, the head at about one third of the frame height, looking down at the officer. On the shoulder in the right third: {{TEN_CANHSAT}} "
           "({{NGUOI_CANHSAT}}), standing close to the truck, seen from slightly behind the left side, body from the knees up, head at about 40% of the "
           "frame height, the face in left profile turned up toward the driver's window. Behind them: {{NEN_DUONG}}. Mouths closed, natural expressions, "
           "nobody looks into the lens. Only these two people. No text, no logos, no lettering anywhere. Output only the image.")

LOOK_UP = "the officer looks up at the driver in the cab window the whole clip; the driver looks down at {{HIM_CANHSAT}}."
LOOK_DOWN = "the driver looks down at the officer the whole clip; the officer looks up at the driver."

# (người nói, Diễn biến VN, Khung cuối VN, hướng nhìn EN, hành động EN hoặc None, hook?)
# Cảnh hook của kịch bản B dùng token HOOK_TV (cách tài xế nói câu sai) và HOOK_CS (phản ứng của cảnh sát khi hỏi lại).
CANH_A = [
    ("hoc", "Tài xế nhoài ra cửa sổ, tì hai tay lên bậu, nói to vui vẻ, tự tin, mặt rạng rỡ; cảnh sát đứng dưới ngẩng nhìn, mặt bình thản.",
     "tài xế tì tay bậu cửa sổ, cười; cảnh sát ngẩng nhìn lên; hai người miệng khép, đứng im.", LOOK_DOWN),
    ("canhsat", "Cảnh sát ngẩng nhìn tài xế, nhướn mày ngạc nhiên, hơi nghiêng đầu, hỏi lại với vẻ bối rối lịch sự; tài xế nghe, nụ cười nhạt dần.",
     "cảnh sát ngẩng nhìn tài xế, mày nhướn; tài xế nhìn xuống; hai người miệng khép, đứng im.", LOOK_UP),
    ("hoc", "Tài xế vừa nói \"Oh no!\" thì mắt mở to ngượng ngùng nhận ra lỗi, rồi bật cười, nói câu đúng chậm rãi rõ ràng; cảnh sát ngẩng nghe, gật nhẹ.",
     "tài xế tì tay bậu cửa sổ, cười ngượng; cảnh sát ngẩng nhìn; hai người miệng khép, đứng im.", LOOK_DOWN),
    ("canhsat", "Cảnh sát nở nụ cười rạng rỡ, gật đầu khen, nói tiếp với giọng vui, nhấn \"every day\"; tài xế cười lại.",
     "cảnh sát cười, ngẩng nhìn tài xế; tài xế cười nhìn xuống; hai người miệng khép, đứng im.", LOOK_UP),
]

HOOK_TV = ("the driver says the line in a bright, proud, confident way, a wide smile, completely sure of the line")
HOOK_CS = ("eyebrows raised and a small polite puzzled frown, the head tilted slightly, as if checking what was just said")


def canh(i, who, dien, cuoi, eye, hook_b):
    n = i + 1
    if hook_b and n == 1:
        dien = ("Tài xế nhoài ra cửa sổ, tì hai tay lên bậu; {{HOOK_TV}}; cảnh sát đứng dưới ngẩng nhìn, mặt bình thản.")
    if hook_b and n == 2:
        dien = ("Cảnh sát ngẩng nhìn tài xế, hỏi lại; nét mặt: {{HOOK_CS}}; tài xế nghe, nụ cười nhạt dần.")
    lines = [f"CẢNH {n} (0:{(n - 1) * 5:02d}–0:{n * 5:02d}): Lượt {n}" + (" (HOOK)" if hook_b and n <= 2 else ""),
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
    if hook_b and n == 1:
        extra = "DELIVERY: {{HOOK_TV}}. "
    elif hook_b and n == 2:
        extra = "The officer's face while asking: {{HOOK_CS}}. "
    elif n == 1:
        extra = "DELIVERY: " + HOOK_TV + ". "
    elif n == 2:
        extra = "The officer's face while asking: " + HOOK_CS + ". "
    elif n == 3:
        extra = "DELIVERY: on \"Oh no\" the driver's eyes widen with an embarrassed realisation, then a small laugh, and the rest is said slowly and clearly. "
    else:
        extra = "DELIVERY: a big warm smile, a approving nod on \"Perfect\", the emphasis on \"every day\". "
    extra = extra.replace("a approving", "an approving")
    v = (f"Prompt video: STYLE LOCK, SET LOCK. Start exactly from the start-frame image and keep its camera framing. CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} "
         f"Only that character speaks, with lip-sync, at {TOC_DO}. EYE LINE for the whole clip: {eye} The speaker never turns the head toward the camera while talking. "
         "The other person keeps the mouth closed and reacts only with the eyes and face. " + extra +
         "After the line both stay still until the end. Same voices as always, clean dry sound, no music. VIDEO SUFFIX.")
    lines += ["Audio: Chỉ giọng của một nhân vật, rõ, gần; phần còn lại im lặng. Không nhạc, không tiếng động cơ, không tiếng xe, không tiếng gió.", v.replace("Prompt video: ", "Prompt video: ", 1)]
    # giữ thứ tự trường như mẫu: Prompt video, Audio, Negative prompt
    lines = lines[:-2] + [v, lines[-2],
                          "Negative prompt: two voices; a silent character moving the mouth; text or captions; camera movement; the officer facing the camera; no speech."]
    return "\n".join(lines)


def build(hook_b):
    return GHI_CHU + "\n" + STYLE + "\n" + "\n\n".join(canh(i, c[0], c[1], c[2], c[3], hook_b) for i, c in enumerate(CANH_A)) + "\n"


def main():
    for path, hb in ((OUT_A, False), (OUT_B, True)):
        body = build(hb)
        open(path, "w", encoding="utf-8", newline="\n").write(body)
        print("Đã ghi", os.path.normpath(path), f"({len(CANH_A)} cảnh, {len(body)} ký tự)")


if __name__ == "__main__":
    main()
