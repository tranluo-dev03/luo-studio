"""Đặt góc máy từng cảnh phần 1 theo đúng shot của video gốc (bảng shot trong README.md).
Chạy lại được nhiều lần: thay Bối cảnh, Khung đầu, Hướng nhìn, Prompt ảnh, Ảnh tổng quan, Ảnh bố cục của mỗi CẢNH 1..12 trong kịch bản.
  .venv\\Scripts\\python.exe SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\goc_may.py"""
import os
import re

S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "KICH-BAN-CANH-SAT-GIA-SU-AI.txt")
PRE = "Generate exactly one still image now, vertical 9:16, stylized 3D animated feature-film look, warm golden-hour light. "
END = " Mouths closed, natural expressions. No text, no logos, no lettering anywhere. Output only the image."
NOCHILD = " There is NO child and no child seat anywhere in this frame."

# góc: (Bối cảnh VN, CAMERA ANGLE EN, hướng nhìn EN)
G = {
    "A": ("góc A (shot gốc 2.1-4.2s): trong xe, sát sau-phải tài xế: nghiêng mặt bố to ở mép trái, qua cửa sổ thấy cảnh sát cúi vào, tay đặt lên cửa",
          "CAMERA ANGLE A: the camera is INSIDE the car, in the middle of the front row, close behind and slightly to the right of {{TEN_HOC}} ({{NGUOI_HOC}}); the dark roof lining with a grab handle runs across the TOP of the frame, the dark window frame surrounds the view, the inside of the door and the steering wheel along the bottom; NO red car body is visible from outside. His face in PROFILE, large, at the LEFT edge of the frame "
          "(curly hair, beard, gold hoop earring), looking out of the open driver's window; through the window {{TEN_CANHSAT}} ({{NGUOI_CANHSAT}}) leans toward the window "
          "with one hand on the door frame, her face and upper body LARGE, filling the window, looking at him; behind her {{NEN_DUONG}}." + NOCHILD,
          "the officer looks at the driver (toward the left of the frame); the driver looks at the officer"),
    "A2": ("góc A2 (shot gốc 5.5-6.8s, 12.4-14.8s, 18.6-21.6s): góc nhìn của tài xế qua cửa sổ: cảnh sát cúi vào đầy khung, không thấy ai khác",
           "CAMERA ANGLE A2, the driver's point of view: the camera sits in the driver's seat and looks straight out through the open driver's window; the dark roof lining "
           "and window frame across the top, the top of the door along the bottom; {{TEN_CANHSAT}} ({{NGUOI_CANHSAT}}) leans toward the window and fills the frame from the "
           "waist up, centred, looking at the driver just beside the lens; behind her ONLY the empty desert road, golden grass and the sky, with the dark police SUV small and far away; no other cars. Nobody else is visible: no driver, no hands, no child.",
           "the officer looks at the driver, just beside the lens (not straight into it)"),
    "B": ("góc B (shot gốc 4.2-5.5s, 16.4-18.6s, 21.6-23.9s): ngoài cửa sổ tài xế nhìn vào: vô lăng góc dưới trái, bé ngồi ghế trẻ em ở ghế phụ phía xa bên trái bố, bố cầm lái bên phải",
          "CAMERA ANGLE B: the camera stands outside the open driver's window at chest height and looks into {{XE}}: the steering wheel at the lower left, {{TEN_HOC}} "
          "({{NGUOI_HOC}}) at the wheel on the RIGHT half, nearest to the camera; right beside him on the far side, on the LEFT half, {{TEN_BE}} ({{NGUOI_BE}}) sits upright "
          "in her pink booster child seat on the front passenger seat; both faces clear; red leather seats, the empty desert through the far windows; the glossy red door along the bottom. ONLY the father and the girl are in the frame: nobody outside the far windows, no other face anywhere.",
          "the driver looks up and just to the left of the lens, never into it; the girl looks the same way"),   # không nhắc cảnh sát: Muse vẽ cô ấy vào mép khung (06/11)
    "C": ("góc C (shot gốc 6.8-9.0s): cận cực sát mặt bố, mồ hôi lấm tấm",
          "CAMERA ANGLE C: EXTREME CLOSE-UP of {{TEN_HOC}} ({{NGUOI_HOC}}): his face fills the frame from the hairline to the chin, small beads of sweat on his forehead and "
          "cheeks, worried; the dark car interior behind him. Nobody else is visible." + NOCHILD,
          "the driver looks just past the right side of the lens, eyes darting nervously, never straight into the lens"),
    "C2": ("góc C2 (shot gốc 26.7-27.9s): cận bố từ phía ghế phụ, hai tay cầm điện thoại xanh trước ngực",
           "CAMERA ANGLE C2: close shot of {{TEN_HOC}} ({{NGUOI_HOC}}) from the front passenger side, head and chest, holding {{DAO_DIEN_THOAI}} in both hands at chest "
           "height with the back of the phone toward the camera, eyes on its screen; the red leather seat and the window behind him. Only a few beaded braids of the girl at the far left edge.",
           "the driver looks down at the phone screen in his hands"),
    "D": ("góc D (shot gốc 9.0-12.4s, 23.9-26.7s): cận bé từ phía ghế lái, chỉ có bé trong khung (bản đầu có cẳng tay bố ở mép dưới: người dùng thấy là tay lạ, bỏ)",
          "CAMERA ANGLE D: close shot of {{TEN_BE}} ({{NGUOI_BE}}) seen from the driver's seat: she sits upright in her pink booster child seat on the front passenger seat, "
          "framed TIGHT from the chest up, her face large in the upper half of the frame, the seat belt across her chest; only the red leather seat back behind her and a small piece of the passenger window at the top. "
          "ONLY the girl is in the frame: no other person, no uniform, no sleeve, no hands or arms of anyone else anywhere, and the left and right edges show only the car seat and door.",
          "the girl looks up and just past the right side of the lens, never straight into the lens"),
    "E": ("góc E (shot gốc 14.8-16.4s): cận bé quay sang bố, mặt bố ở mép phải",
          "CAMERA ANGLE E: close shot of {{TEN_BE}} ({{NGUOI_BE}}) in her pink booster child seat, filling the left two-thirds of the frame, turned toward her father and "
          "looking up at him; {{TEN_HOC}}'s face and shoulder ({{NGUOI_HOC}}) at the RIGHT edge of the frame, partly cut off, looking down at her; the passenger window and the desert behind her.",
          "the girl looks up at her father at the right of the frame; the father looks down at her"),
    "F": ("góc F (shot gốc 27.9-29.0s): cận hai bố con áp má, cùng nhìn điện thoại bố cầm",
          "CAMERA ANGLE F: close two-shot from the front, slightly low: {{TEN_HOC}} ({{NGUOI_HOC}}) and {{TEN_BE}} ({{NGUOI_BE}}) cheek to cheek, she leans from her booster "
          "seat at the LEFT against his shoulder, both looking down at {{DAO_DIEN_THOAI}} he holds at the lower right; warm sunset light from the windows behind them.",
          "both look down at the phone screen"),
}
ANG = {1: "A", 2: "B", 3: "A2", 4: "C", 5: "D", 6: "A2", 7: "B", 8: "A2", 9: "B", 10: "D", 11: "C2", 12: "F"}   # 7: người dùng muốn y hệt khung cảnh "Yes"
# Cảnh cùng góc với một cảnh trước: dùng NGUYÊN khung đầu của cảnh đó (engine: "Khung đầu từ cảnh"): nền, vị trí người, khung hình giống hệt, không vẽ lại
FROM = {6: 3, 8: 3, 7: 2, 9: 2, 10: 5}
EYE = {7: "the girl turns her head toward her father and talks to him; the father looks down at her and listens"}   # hướng nhìn riêng của cảnh, khác mặc định của góc
CLOSE_ANG = ("C", "C2", "D", "E", "F")
A2_LOCK = ("Only the officer is in this clip; no driver, no child ever appears. CAMERA LOCK: the camera is locked off for the whole clip: no pan, no zoom out, "
           "no reframing; only the officer and the empty road behind her are ever seen.")
NOBODY = ("CAMERA LOCK: the camera is locked off on this tight close-up for the whole clip: no pan, no zoom out, no reframing. Whoever the speaker talks to stays off-screen and is never shown. "
          "No one else ever appears in this clip: nobody at any window, nobody outside the car.")
LAY = {11: 4, 12: 2}   # cùng góc / cùng người: gửi kèm khung đầu cảnh đã có
WIDE = ("Wide landscape 16:9 overview of this shot, stylized 3D animated feature-film look, warm golden-hour light, the same people and car as the reference images. "
        "Everything important is in the CENTRE third of the picture; the outer thirds are only more of the same car interior or road. ")
OPEN8 = ("Mở đầu khung từ cảnh: 2\n"   # người dùng: đưa giấy tờ phải đúng vị trí cảnh "Yes" (bố sát cửa sổ phía cảnh sát, bé ở ghế phụ bên phải bố)
         "Mở đầu ảnh: " + PRE + "CAMERA ANGLE B (outside the open driver's window, looking in): {{TEN_HOC}} ({{NGUOI_HOC}}) at the wheel nearest to the window; "
         "{{TEN_BE}} ({{NGUOI_BE}}) sits upright in her pink booster child seat on the front passenger seat beside him, on his right; the steering wheel at the lower left." + END + "\n"
         # bản đầu: Muse để bố cầm lái 2 s rồi vụt máy vào trong xe, đưa giấy tờ ở góc khác (06/11) -> hành động ngay giây đầu + khoá máy, dài 3 s
         "Mở đầu video: Start exactly from the start-frame image. CAMERA LOCK: the camera is locked off exactly as in the start frame for the whole clip: no pan, no cut, "
         "no change of angle. THIS CLIP IS SILENT. RIGHT AWAY, in the first second, the father picks up {{DAO_GIAY_TO}} from his lap with his left hand and holds it out "
         "through the open window toward the camera; at about 1.5 seconds the officer's hand in a navy uniform sleeve comes in from the bottom edge of the frame, close to the "
         "camera, and takes it out of the frame; then the father puts his hand back on the wheel. The girl stays seated upright beside him and watches. Nobody changes "
         "seats. Nobody speaks; only soft rustling and quiet desert ambience. No text.\n"
         "Mở đầu dài: 3.0")
OPEN9 = ("Mở đầu ảnh: " + PRE + "From INSIDE the car, the driver's point of view through the open driver's window: {{TEN_CANHSAT}} ({{NGUOI_CANHSAT}}) seen from BEHIND, "
         "walking away along the road toward the dark police SUV parked behind the car; plain navy uniform back with no lettering, black duty belt; the window frame and "
         "roof lining around the view; desert, power poles and sunset sky." + NOCHILD + END + "\n"
         "Mở đầu video: Start exactly from the start-frame image and keep its camera. THIS CLIP IS SILENT: the officer keeps walking away toward the police SUV, getting "
         "smaller. The camera stays still. Nobody speaks; only quiet footsteps and soft desert ambience. No text.\n"
         "Mở đầu dài: 1.5")


def rep(seg, f, val):
    return re.sub(r"^%s: [^\n]*" % re.escape(f), lambda _: f"{f}: {val}", seg, count=1, flags=re.M)


def main():
    t = open(S, encoding="utf-8").read()
    ms = list(re.finditer(r"^CẢNH (\d+) \(", t, re.M))
    end = t.find("\n=====", ms[-1].start()) + 1
    out = t[:ms[0].start()]
    for i, m in enumerate(ms):
        n = int(m.group(1))
        seg = t[m.start():(ms[i + 1].start() if i + 1 < len(ms) else end)]
        bc, cam, eye = G[ANG[n]]
        eye = EYE.get(n, eye)
        seg = rep(seg, "Bối cảnh", bc + "; không có chữ, không người lạ.")
        seg = rep(seg, "Khung đầu", f"ảnh mới theo {bc.split(' (')[0]}; miệng mọi người khép.")
        seg = rep(seg, "Hướng nhìn", eye + ".")
        seg = rep(seg, "Prompt ảnh", PRE + cam + " EYE LINE: " + eye + "." + END)
        # câu hướng nhìn có thể chứa ";" -> thay tới mốc cố định "; the speaker never turns" (bản cũ thay tới ";" đầu tiên: phần đuôi dồn lại mỗi lần chạy)
        seg = re.sub(r"EYE LINE for the whole clip: .*?; the speaker never turns", lambda _: f"EYE LINE for the whole clip: {eye}; the speaker never turns", seg, count=1)
        seg = re.sub(r" Only two people are in this clip: [^.]*\.[^.]*\.", "", seg)
        # xoá ĐÚNG NGUYÊN VĂN các câu do công cụ chèn (bản cũ dùng regex "[^.]*\." ăn lấn câu sau mỗi lần chạy: mất cả {{LUOT_n}} ở cảnh 3, 6, 8)
        for added in (" " + A2_LOCK, " Only the officer is in this clip; no driver, no child ever appears.", " No child ever appears in this clip."):
            seg = seg.replace(added, "")
        if ANG[n] == "A2":
            seg = seg.replace("keep its camera angle.", "keep its camera angle. " + A2_LOCK, 1)
        seg = seg.replace(" Only the father and the girl are in this clip: nobody ever appears at any window or outside the car; the far windows show only the empty desert.", "")
        if ANG[n] == "B":
            seg = seg.replace("keep its camera angle.", "keep its camera angle. Only the father and the girl are in this clip: nobody ever appears at any window or outside the car; the far windows show only the empty desert.", 1)
            seg = re.sub(r"^(Negative prompt: [^\n]*?)\.?$", lambda m: m.group(1) if "face at a window" in m.group(1) else m.group(1) + "; a face at a window or a person outside the car.", seg, count=1, flags=re.M)
        seg = seg.replace(" " + NOBODY, "")
        if ANG[n] in CLOSE_ANG:   # so sánh v7 cảnh 4: Muse thêm mặt cảnh sát sau cửa sổ ở cảnh cận
            seg = seg.replace("keep its camera angle.", "keep its camera angle. " + NOBODY, 1)
            seg = re.sub(r"^(Negative prompt: [^\n]*?)\.?$", lambda m: m.group(1) if "face at a window" in m.group(1) else m.group(1) + "; a face at a window or a person outside the car; camera pan or zoom out revealing other people.", seg, count=1, flags=re.M)
        if ANG[n] in ("A", "C"):
            seg = seg.replace("keep its camera angle.", "keep its camera angle. No child ever appears in this clip.", 1)
        for f in ("Ảnh tổng quan", "Khung đầu cắt", "Ảnh bố cục"):
            seg = re.sub(r"^%s: [^\n]*\n?" % re.escape(f), "", seg, flags=re.M)
        if n == 7:   # video gốc: bé nói, bố chỉ nhìn; việc đưa giấy tờ nằm ở shot không lời đầu cảnh 8
            seg = re.sub(r" ACTION, done WHILE the line is spoken[^.]*\.[^.]*\.", " ACTION: the father listens and nods once.", seg)
            seg = rep(seg, "Diễn biến", "Bé gái quay sang bố, nói tiếng Tây Ban Nha; bố nhìn xuống bé, gật đầu. Nói xong mọi người đứng im đến hết clip.")
            seg = rep(seg, "Khung cuối", "bé nhìn bố, bố nhìn bé; mọi người miệng khép, đứng im đến hết clip.")
        if n == 8:
            seg = re.sub(r"^Mở đầu (ảnh|video|dài|khung từ cảnh): [^\n]*\n?", "", seg, flags=re.M)
            seg = re.sub(r"ACTION, done WHILE the line is spoken and complete by the last word: [^.]*\.[^.]*\.",
                         "ACTION, done WHILE the line is spoken: she holds {{DAO_GIAY_TO}} she has just been given, glances at it, then looks up at the driver.", seg)
            seg = rep(seg, "Diễn biến", "Cảnh sát cầm giấy tờ vừa nhận (đoạn mở đầu: bố đưa giấy tờ qua cửa sổ), nhìn qua rồi ngẩng lên dặn. Nói xong mọi người đứng im đến hết clip.")
            seg = seg.rstrip("\n") + "\n" + OPEN8 + "\n"
        if n == 9:
            seg = re.sub(r"^Mở đầu (ảnh|video|dài|khung từ cảnh): [^\n]*\n?", "", seg, flags=re.M)
            seg = seg.rstrip("\n") + "\n" + OPEN9 + "\n"
        seg = seg.rstrip("\n") + "\n"
        seg = re.sub(r"^Khung đầu từ cảnh: [^\n]*\n?", "", seg, flags=re.M)
        if n in FROM:
            seg += f"Khung đầu từ cảnh: {FROM[n]}\n"
        elif ANG[n] not in CLOSE_ANG:   # góc cận cắt từ ảnh ngang bị lỏng khung (so sánh v7 cảnh 4): chỉ góc rộng có ảnh tổng quan
            seg += "Ảnh tổng quan: " + WIDE + cam + "\nKhung đầu cắt: giữa\n"
        if n in LAY:
            seg += f"Ảnh bố cục: {LAY[n]}\n"
        out += seg + "\n"
    out += t[end:]
    assert len(re.findall(r"^CẢNH \d+ \(", out, re.M)) == 12
    open(S, "w", encoding="utf-8").write(out)
    print("OK", ANG)


if __name__ == "__main__":
    main()
