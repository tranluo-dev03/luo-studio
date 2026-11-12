"""Sinh KICH-BAN-TIEM-THIT-TIENG-ANH.txt từ bảng góc máy + bảng cảnh (sửa một chỗ, chạy lại).
  runtime\\python.exe SAMPLE\\tiem-thit-tieng-anh\\cong-cu\\tao_kich_ban.py
Thể loại: phim hoạt hình 3D kể chuyện, MỘT phần, cảnh thường, 5 nhân vật (TAVO, TIO, KHACH, CHU, ROBOT trên màn hình điện thoại),
mỗi cảnh một người nói; cảnh đổi góc máy có "Prompt ảnh", cảnh cùng góc liền nhau nối khung cuối, cảnh quay lại góc cũ dùng "Khung đầu từ cảnh"."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "KICH-BAN-TIEM-THIT-TIENG-ANH.txt")

DAY = "warm soft daylight from the high windows of a big indoor market hall and warm glowing bulbs over the stall"
NIGHT = "late at night, the only light is the cold bluish glow of a phone screen from below, deep soft shadows"
MORNING = "bright warm morning light streaming into the big indoor market hall"

# góc: (mô tả tiếng Việt, ánh sáng, mô tả khung hình tiếng Anh, khoá nhân vật có mặt, cận?)
ANG = {
    "A": ("góc A: nhìn từ phía khách vào quầy thịt: tủ kính thịt ở 1/3 dưới, Tavo bên TRÁI sau thớt, ông chú ở GIỮA; mép PHẢI chỉ có vai + gáy khách áo polo trắng (không thấy mặt)",
          DAY,
          "CAMERA ANGLE A, medium-wide shot from the customer side, facing the meat stall: across the bottom third a glass display case full of neatly stacked raw red steaks; "
          "behind the counter {{TEN_TAVO}} ({{NGUOI_TAVO}}) stands at the LEFT behind a worn wooden cutting board, and {{TEN_TIO}} ({{NGUOI_TIO}}) stands in the CENTRE, both chest-up above the display; "
          "at the far RIGHT edge only the out-of-focus shoulder and the back of the head of a customer in a white polo shirt, his face never visible; behind them {{NEN_SAP}}.",
          ["TAVO", "TIO"], False),
    "K": ("góc K: cận khách hàng từ ngực trở lên, đứng trước quầy, nền chợ mờ; chỉ một người",
          DAY,
          "CAMERA ANGLE K: medium close-up of {{TEN_KHACH}} ({{NGUOI_KHACH}}) from the chest up, standing in front of the meat stall, seen from just beside the counter, "
          "his body turned slightly to the LEFT toward the counter; behind him {{NEN_CHO}}, softly out of focus. He is the only person in the frame.",
          ["KHACH"], True),
    "B": ("góc B: cận hai người qua thớt gỗ: Tavo nửa TRÁI, ông chú nửa PHẢI, từ ngực trở lên, mép thớt + khăn trắng gấp ở dưới",
          DAY,
          "CAMERA ANGLE B, close two-shot across the wooden cutting board: {{TEN_TAVO}} ({{NGUOI_TAVO}}) on the LEFT half and {{TEN_TIO}} ({{NGUOI_TIO}}) on the RIGHT half, both from the chest up behind the counter, "
          "the worn edge of the wooden cutting board with a folded white towel along the bottom of the frame; behind them {{NEN_SAP}}. Only these two people are in the frame.",
          ["TAVO", "TIO"], True),
    "C": ("góc C: phòng sau quầy (tường gạch trắng, cuộn giấy hồng, móc xích, thớt lớn, ghế nhựa xanh): bà chủ nhà hàng bên TRÁI cầm sổ, Tavo mép PHẢI, hai người nhìn nhau",
          DAY,
          "CAMERA ANGLE C, medium shot in the back room of the stall: {{TEN_CHU}} ({{NGUOI_CHU}}) at the LEFT, holding {{DAO_SO}} at waist height, body turned RIGHT in three-quarter view; "
          "{{TEN_TAVO}} ({{NGUOI_TAVO}}) at the RIGHT edge, from the chest up, turned LEFT toward her; behind them {{NEN_PHONG}}. Only these two people are in the frame.",
          ["CHU", "TAVO"], False),
    "D": ("góc D: cận thớt lớn: Tavo bên TRÁI cúi trên thớt cầm dao phay trên tảng thịt bò; bà chủ đứng sau thớt bên PHẢI nhìn",
          DAY,
          "CAMERA ANGLE D: close shot over the big wooden chopping block in the back room: {{TEN_TAVO}} ({{NGUOI_TAVO}}) at the LEFT, leaning over the block, one hand resting on a large piece of raw red beef, {{DAO_DAO}} lying flat on the block beside it; "
          "{{TEN_CHU}} ({{NGUOI_CHU}}) stands behind the block at the RIGHT, from the waist up, watching him; behind them {{NEN_PHONG}}. Only these two people are in the frame.",
          ["TAVO", "CHU"], False),
    "W": ("góc W: sau quầy dài: Tavo TRÁI, bà chủ PHẢI, trước mặt 4 gói thịt bọc giấy hồng xếp hàng",
          DAY,
          "CAMERA ANGLE W, medium shot of the long wooden counter: {{TEN_TAVO}} ({{NGUOI_TAVO}}) at the LEFT and {{TEN_CHU}} ({{NGUOI_CHU}}) at the RIGHT stand behind it, from the waist up, turned toward each other; "
          "on the counter in front of them {{DAO_GOI}} lie in a neat row; behind them {{NEN_CHO}}, softly out of focus. Only these two people are in the frame.",
          ["TAVO", "CHU"], False),
    "E": ("góc E: quầy trước, cạnh cân đồng treo: bà chủ TRÁI tì tay lên tủ kính nhìn sang phải, Tavo mép PHẢI nhìn nghiêng sang trái; 4 gói thịt bọc giấy hồng (Tavo vừa gói) xếp hàng trên nóc tủ kính",
          DAY,
          "CAMERA ANGLE E, medium close shot at the front counter beside an old brass hanging scale on a chain: {{TEN_CHU}} ({{NGUOI_CHU}}) at the LEFT leans her forearms on the glass display, face in three-quarter view looking RIGHT; "
          "{{TEN_TAVO}} ({{NGUOI_TAVO}}) at the RIGHT edge, head and shoulders in profile, facing LEFT toward her; on top of the glass display between them lie the four packages of meat wrapped in plain pink butcher paper that the boy has just wrapped ({{DAO_GOI}}) in a neat row; raw steaks inside the glass display along the bottom; "
          "behind them {{NEN_SAP}}. Only these two people are in the frame.",
          ["CHU", "TAVO"], False),
    "E1": ("góc E1: cận mặt bà chủ, một ngón tay giơ lên, tay kia cầm bút; chỉ một người",
           DAY,
           "CAMERA ANGLE E1: close-up of {{TEN_CHU}} ({{NGUOI_CHU}}), head and shoulders, face turned slightly to the RIGHT of the lens, a pen held in one hand at the bottom of the frame; "
           "behind her the stall, softly out of focus. She is the only person in the frame.",
           ["CHU"], True),
    "N": ("góc N: đêm, cận Tavo ngồi khom trong kho tối, mặt sáng từ dưới lên bởi màn hình điện thoại (lưng điện thoại hướng camera ở mép dưới)",
          NIGHT,
          "CAMERA ANGLE N: close-up of {{TEN_TAVO}} ({{NGUOI_TAVO}}) at night, from the top of his hair to the chest, sitting hunched in {{NEN_DEM}}, holding {{DAO_DIEN_THOAI}} low in both hands at the bottom of the frame "
          "with the BACK of the phone toward the camera; his face is lit from below by the phone's cold glow, eyes on the screen. He is the only person in the frame.",
          ["TAVO"], True),
    "P": ("góc P: cận điện thoại trong hai bàn tay cậu bé (chỉ thấy tay), màn hình là robot gia sư AI gọi video trên nền xanh, không chữ, không nút",
          NIGHT,
          "CAMERA ANGLE P: close-up of {{DAO_DIEN_THOAI}} held upright in a boy's two hands at night (only the hands and thumbs at the sides, no face); the screen fills most of the frame and shows only "
          "{{TEN_ROBOT}} ({{NGUOI_ROBOT}}) in a video call, head and chest, centred, on a plain soft-blue background; no text, no buttons, no icons, no bars on the screen; the dark room around the phone.",
          ["ROBOT"], True),
    "M": ("góc M: một tháng sau, sáng: bà chủ bên TRÁI nhìn sang phải cầm sổ; ông chú sau tủ kính cong bên PHẢI nhìn bà; nền mái chợ cao",
          MORNING,
          "CAMERA ANGLE M, medium-wide shot along the front of the stall: {{TEN_CHU}} ({{NGUOI_CHU}}) at the LEFT, from the knees up, turned RIGHT in three-quarter view, holding {{DAO_SO}}; "
          "behind the curved glass display at the RIGHT stands {{TEN_TIO}} ({{NGUOI_TIO}}), chest-up, facing her; the high roof of the market hall in the background. Only these two people are in the frame; no boy.",
          ["CHU", "TIO"], False),
    "M2": ("góc M2: trung cảnh ông chú sau tủ kính, giữa-phải, nhìn sang trái về bà chủ (bà chỉ thấy vai, búi tóc, tay cầm sổ ở mép TRÁI, quay lưng 3/4)",
           MORNING,
           "CAMERA ANGLE M2: medium shot of {{TEN_TIO}} ({{NGUOI_TIO}}) behind the glass display, chest-up, centre-right, facing LEFT; {{TEN_CHU}} is only partly visible at the LEFT edge, seen from behind "
           "(her shoulder, the back of her hair bun and the hand holding {{DAO_SO}}), her face not visible; the market hall behind, softly out of focus. No boy in the frame.",
           ["TIO", "CHU"], False),
    "F": ("góc F: hai người đứng nghiêng đối mặt: bà chủ TRÁI nhìn phải, Tavo PHẢI nhìn trái; sau lưng tủ kính dài đầy thịt, cân treo",
          MORNING,
          "CAMERA ANGLE F, medium two-shot, both standing in profile facing each other: {{TEN_CHU}} ({{NGUOI_CHU}}) at the LEFT facing RIGHT, {{TEN_TAVO}} ({{NGUOI_TAVO}}) at the RIGHT facing LEFT, both from the thighs up; "
          "behind them the long glass display full of steaks and a brass hanging scale. Only these two people are in the frame.",
          ["CHU", "TAVO"], False),
    "G": ("góc G: cận Tavo giữa-phải, mặt hơi hướng sang trái (bà chủ ngoài khung); ông chú mờ ở mép TRÁI phía sau",
          MORNING,
          "CAMERA ANGLE G: close-up of {{TEN_TAVO}} ({{NGUOI_TAVO}}), head and shoulders, centre-right, face turned slightly to the LEFT of the lens; behind him at the LEFT edge {{TEN_TIO}} ({{NGUOI_TIO}}) "
          "stands soft and out of focus, looking at the boy; the market hall behind.",
          ["TAVO", "TIO"], True),
    "H": ("góc H: Tavo nhìn thẳng ống kính, ngực trở lên, giữa khung, nền chợ đông mờ",
          MORNING,
          "CAMERA ANGLE H: medium close shot of {{TEN_TAVO}} ({{NGUOI_TAVO}}) facing the camera, chest-up, centred, the busy market hall behind him softly out of focus. He holds {{DAO_DIEN_THOAI}} up beside his face, its screen toward the camera showing only {{TEN_ROBOT}} ({{NGUOI_ROBOT}}, copy the robot reference image), head and chest, no text. He is the only person in the frame.",
          ["TAVO", "ROBOT"], True),
    # --- góc của cảnh KHÔNG LỜI (lượt "text" rỗng) ---
    "T": ("góc T: cận Tavo một mình sau quầy, đầu và vai, mặt hơi quay sang PHẢI về phía ông chú (ngoài khung), nền sạp mờ",
          DAY,
          "CAMERA ANGLE T: close-up of {{TEN_TAVO}} ({{NGUOI_TAVO}}) behind the meat counter, head and shoulders, centre, face turned slightly to the RIGHT of the lens toward the butcher off-screen; "
          "behind him {{NEN_SAP}}, softly out of focus. He is the only person in the frame.",
          ["TAVO"], True),
    "X": ("góc X: lối đi trong chợ: bà chủ đi nhanh về phía máy giữa hai dãy sạp, cầm sổ, đảo mắt tìm quầy thịt",
          DAY,
          "CAMERA ANGLE X, medium-wide shot down an aisle of the big indoor market: {{TEN_CHU}} ({{NGUOI_CHU}}) walks toward the camera in the middle of the aisle, seen from the knees up, holding {{DAO_SO}}, "
          "between stalls of fruit, vegetables and spices on both sides; {{NEN_CHO}}; far shoppers are tiny, blurred and still. She is the only person clearly visible.",
          ["CHU"], False),
    "D2": ("góc D2: cận thớt lớn phòng sau: tay Tavo cầm dao phay ở nửa dưới, tảng thịt bò; mặt Tavo cúi tập trung ở nửa trên",
           DAY,
           "CAMERA ANGLE D2: close shot over the big wooden chopping block in the back room: {{TEN_TAVO}} ({{NGUOI_TAVO}}) leans over the block in the upper half of the frame, eyes down on the meat, concentrated, "
           "his hands holding {{DAO_DAO}} over a large slab of raw red beef in the lower half; a few thick steaks already cut at the side; behind him {{NEN_PHONG}}, softly out of focus. He is the only person in the frame.",
           ["TAVO"], True),
    "Y": ("góc Y: cận từ trên xuống quầy gỗ: chỉ hai bàn tay Tavo (tay áo xanh nhạt, tạp dề trắng) gói thịt bằng giấy hồng; chồng thịt bên trái, gói xong bên phải",
          DAY,
          "CAMERA ANGLE Y: tight top-down close-up of the long wooden counter, framed so that only {{TEN_TAVO}}'s two hands and forearms (light-blue T-shirt sleeves) enter from the bottom edge; "
          "his head, face and body are below the bottom edge and never in the frame; "
          "a roll of plain pink butcher paper, a pile of freshly cut raw steaks at the LEFT, ONE wrapped pink package at the RIGHT.",
          ["TAVO"], True),
    "Q1": ("góc Q1 (montage, ngày): Tavo chặt thịt sau quầy, điện thoại dựng cạnh cân đồng, một tai nghe trắng, liếc màn hình học",
           DAY,
           "CAMERA ANGLE Q1, medium shot behind the meat counter in daylight: {{TEN_TAVO}} ({{NGUOI_TAVO}}) cuts a steak on the wooden board, a small white earbud in one ear; "
           "{{DAO_DIEN_THOAI}} stands propped against the brass hanging scale beside him, its screen turned toward him (the camera sees only a soft glow, nothing readable); behind him {{NEN_SAP}}. He is the only person in the frame.",
           ["TAVO"], False),
    "Q2": ("góc Q2 (montage, tối): chợ vắng đèn vàng, Tavo quét sàn trước sạp, điện thoại trong túi tạp dề, tai nghe trắng",
           "late evening, the market hall empty and dim, only a few warm bulbs still glowing over the stall",
           "CAMERA ANGLE Q2, medium-wide shot of the closed meat stall in the late evening: {{TEN_TAVO}} ({{NGUOI_TAVO}}) sweeps the floor in front of the counter with a broom, seen from the knees up, "
           "{{DAO_DIEN_THOAI}} in the chest pocket of his apron, a small white earbud in one ear; behind him {{NEN_SAP}}, the shutters of other stalls half closed. He is the only person in the frame.",
           ["TAVO"], False),
    "Q3": ("góc Q3 (montage, đêm): kho tối, Tavo ngồi trên bao gấp, cầm điện thoại sáng, chăm chú luyện",
           NIGHT,
           "CAMERA ANGLE Q3, medium shot at night: {{TEN_TAVO}} ({{NGUOI_TAVO}}) sits on a pile of folded canvas sacks in {{NEN_DEM}}, seen from the knees up, holding {{DAO_DIEN_THOAI}} in both hands "
           "with its back to the camera, his face lit from below by its cold glow, eyes on the screen. He is the only person in the frame.",
           ["TAVO"], False),
    "Q5": ("góc Q5 (montage, ngày): phòng sau, Tavo cọ thớt gỗ lớn, điện thoại dựng trên kệ phát bài học, tai nghe một bên",
           DAY,
           "CAMERA ANGLE Q5, medium shot in the back room: {{TEN_TAVO}} ({{NGUOI_TAVO}}) scrubs the big wooden chopping block with a stiff brush, seen from the thighs up, a small white earbud in one ear; "
           "{{DAO_DIEN_THOAI}} stands propped on a shelf at the RIGHT with its screen glowing toward him (nothing readable); behind him {{NEN_PHONG}}. He is the only person in the frame.",
           ["TAVO"], False),
    "Q6": ("góc Q6 (montage, sáng): trước tủ kính, Tavo bưng khay thịt đầy, điện thoại kẹp trên mép khay, tai nghe một bên",
           MORNING,
           "CAMERA ANGLE Q6, medium shot from the customer side in the morning: {{TEN_TAVO}} ({{NGUOI_TAVO}}) carries a tray of raw red steaks toward the curved glass display, seen from the thighs up, a small white earbud in one ear, "
           "{{DAO_DIEN_THOAI}} wedged on the edge of the tray with its screen glowing; behind him {{NEN_SAP}}, the market hall still quiet. He is the only person in the frame.",
           ["TAVO"], False),
    "Q7": ("góc Q7 (montage, ngày): sau tủ kính, Tavo lau mặt kính, điện thoại tựa trên nóc tủ hiện app sáng",
           DAY,
           "CAMERA ANGLE Q7, medium close shot from the customer side: {{TEN_TAVO}} ({{NGUOI_TAVO}}) behind the glass display, chest-up, wiping the glass with a cloth, a small white earbud in one ear; "
           "{{DAO_DIEN_THOAI}} leans on top of the display with its screen glowing toward him (nothing readable); behind him {{NEN_SAP}}. He is the only person in the frame.",
           ["TAVO"], False),
    "Q4": ("góc Q4 (montage, sáng sớm): Tavo xếp thịt vào tủ kính, đứng thẳng, hít sâu, mỉm cười tự tin",
           MORNING,
           "CAMERA ANGLE Q4, medium shot from the customer side in the early morning: {{TEN_TAVO}} ({{NGUOI_TAVO}}) behind the curved glass display, chest-up, placing fresh raw steaks neatly in the display; "
           "behind him {{NEN_SAP}}, the market hall still quiet. He is the only person in the frame.",
           ["TAVO"], False),
}

# cảnh: góc, người nói, ngôn ngữ, "moi" (Prompt ảnh) / "noi" (khung cuối cảnh trước) / số cảnh (Khung đầu từ cảnh), hướng nhìn EN,
#       diễn biến VN, khung cuối VN, hành động EN (trong lúc nói), [tuỳ chọn]
S = [
    dict(g="K", w="KHACH", lang="English", start="moi",
         eye="the customer looks down-left at the meat on the counter, then at the butcher off-screen to the LEFT; never into the lens",
         dien="Khách cúi nhìn miếng thịt Tavo vừa cắt, trầm trồ, rồi ngẩng lên nhìn ông chủ (ngoài khung bên trái).",
         cuoi="Khách mỉm cười nhìn sang trái, miệng khép.",
         act="the customer leans in a little to admire the cut, then straightens up with an impressed smile"),
    dict(g="A", w="TIO", lang="English", start="moi",
         eye="the butcher looks at the customer at the right edge of the frame; the boy looks down at his cutting board",
         dien="Ông chú vỗ nhẹ tay lên ngực, khoe với khách, cười tự mãn; Tavo cúi nhìn thớt.",
         cuoi="Ông chú cười, tay buông xuống quầy; Tavo cúi nhìn thớt; miệng khép.",
         act="the butcher pats his own chest once with one hand, proudly, then rests the hand on the counter"),
    dict(g="K", w="KHACH", lang="English", start=1,
         eye="the customer looks toward the boy behind the counter, off-screen to the LEFT; never into the lens",
         dien="Khách hất cằm về phía Tavo (ngoài khung bên trái), tò mò.",
         cuoi="Khách nhìn sang trái, miệng khép.",
         act="the customer nods his chin once toward the left"),
    dict(g="A", w="TIO", lang="English", start=2,
         eye="the butcher glances at the boy on the left, then back at the customer at the right edge; the boy keeps looking down",
         dien="Ông chú liếc Tavo, phẩy tay coi thường, rồi quay lại nhìn khách; Tavo cúi đầu.",
         cuoi="Ông chú nhìn khách; Tavo cúi đầu; miệng khép.",
         act="the butcher gives a small dismissive wave of the hand toward the boy, then lowers the hand"),
    dict(g="A", w="TIO", lang="English", start="noi",
         eye="the butcher turns his head to the boy on the left and looks at him; the boy looks up at the butcher, startled",
         dien="Ông chú quay sang Tavo, ra lệnh như trêu; Tavo ngẩng lên, mắt mở to, miệng vẫn khép.",
         cuoi="Ông chú nhìn Tavo; Tavo nhìn ông chú, sợ sệt; miệng khép.",
         act="the butcher turns toward the boy and gestures at him with an open hand"),
    dict(g="T", w=None, start="moi", keep=3.5,
         eye="the boy looks at the butcher just to the right of the lens, then glances further right toward the customer, then down; never into the lens",
         dien="CẢNH CÂM (~3,5 s): Tavo đứng sững, mắt mở to, hé miệng định đáp nhưng không ra tiếng, khép lại, nuốt khan, lại hé miệng, rồi cúi mặt xấu hổ.",
         cuoi="Tavo cúi mặt, miệng khép, má đỏ lên.",
         act="the boy freezes with wide eyes, opens his mouth as if about to answer but no sound comes out, closes it, swallows nervously, "
             "opens it a little again without a sound, then lowers his eyes in shame; tiny nervous movements only"),
    dict(g="B", w="TIO", lang="English", start="moi",
         eye="the butcher looks off-screen to the RIGHT toward the customer; the boy looks down at the cutting board",
         dien="Ông chú quay sang khách (ngoài khung bên phải), xoè tay về phía Tavo, chê; Tavo cúi mặt xấu hổ.",
         cuoi="Ông chú cười khẩy nhìn sang phải; Tavo cúi mặt; miệng khép.",
         act="the butcher opens one palm toward the boy as he speaks, then lowers it"),
    dict(g="B", w="TIO", lang="Spanish", start="noi",
         eye="the butcher leans toward the boy and looks at him; the boy looks at the coins on the board",
         dien="Ông chú cúi sát Tavo, nói nhỏ nghiêm; đặt hai đồng xu lên thớt cạnh khăn ở chữ 'refresco'.",
         cuoi="Hai đồng xu nằm trên thớt; tay ông chú rút về; Tavo nhìn đồng xu; miệng khép.",
         act="the butcher leans toward the boy and, on the last words, puts {{DAO_TIEN}} down on the cutting board beside the towel, then pulls his hand back"),
    dict(g="B", w="TAVO", lang="Spanish", start="noi",
         eye="the boy lifts his head and looks at the butcher on his right, his face turned three-quarters toward the camera, speaking; the butcher looks down at the two coins and does not look at the boy",
         dien="Tavo ngẩng lên, mặt hơi hướng ra máy, nhìn ông chú và nói nhỏ, rụt rè nhưng rõ ràng đòi lương tuần; miệng Tavo cử động rõ theo từng chữ; ông chú nhìn xuống hai đồng xu, môi mím chặt, không nói.",
         cuoi="Tavo nhìn ông chú; ông chú nhìn xuống hai đồng xu; hai đồng xu vẫn trên thớt; miệng khép.",
         act="the boy lifts his eyes from the coins to the butcher and speaks, his mouth clearly forming every word with lip-sync and his face open to the camera; the butcher keeps his lips firmly sealed and stares down at the coins"),
    dict(g="B", w="TIO", lang="Spanish", start="noi",
         eye="the butcher looks at the boy, then turns his head away to the right; the boy looks down at the coins",
         dien="Ông chú cười nhạt, nói gọn rồi quay mặt đi; Tavo cúi nhìn hai đồng xu.",
         cuoi="Ông chú quay mặt sang phải; Tavo cúi nhìn đồng xu trên thớt; miệng khép.",
         act="the butcher shrugs slightly and turns his head away to the right as he finishes"),
    dict(g="X", w=None, start="moi", keep=4,
         eye="the woman looks left and right along the stalls, searching, then fixes her eyes on something off-screen to the right; never into the lens",
         dien="CẢNH CÂM (~4 s): bà chủ nhà hàng bước nhanh vào chợ, cầm sổ, ráo riết đảo mắt trái phải tìm hàng thịt, rồi thấy quầy (ngoài khung bên phải) và rẽ về phía đó.",
         cuoi="Bà chủ quay người sang phải, bước về phía quầy thịt; miệng khép.",
         act="the woman hurries forward with quick anxious steps, clutching the notepad, her head turning left and right as she scans the stalls, "
             "then she spots something off-screen to the right and turns toward it without slowing down"),
    dict(g="C", w="CHU", lang="English", start="moi",
         eye="the woman looks at the boy on the right, pleading; the boy looks at her",
         dien="Bà chủ nhà hàng vừa chạy tới, thở gấp, cầm sổ, nói với Tavo giọng lo lắng.",
         cuoi="Bà chủ nhìn Tavo, cầm sổ trước bụng; Tavo nhìn bà; miệng khép.",
         act="the woman lifts {{DAO_SO}} a little and gestures with her free hand, worried"),
    dict(g="C", w="CHU", lang="English", start="noi",
         eye="the woman looks around the room and back at the boy; the boy looks at her",
         dien="Bà chủ nhìn quanh tìm người giúp, hai tay nắm sổ.",
         cuoi="Bà chủ nhìn Tavo; miệng khép.",
         act="the woman glances around the room, then back at the boy, holding the notepad with both hands"),
    dict(g="C", w="TAVO", lang="Spanish", start="noi",
         eye="the boy looks at the woman on the left, calm; the woman looks at him",
         dien="Tavo giơ một bàn tay lên trấn an, bình tĩnh, nói nhẹ.",
         cuoi="Tavo hạ tay, nhìn bà chủ; bà nhìn cậu bối rối; miệng khép.",
         act="the boy raises one open palm calmly at chest height, then lowers it"),
    dict(g="C", w="CHU", lang="English", start="noi",
         eye="the woman looks at the boy, confused; the boy looks at her",
         dien="Bà chủ nghiêng đầu, lắc nhẹ, xin lỗi vì không nói được tiếng Tây Ban Nha.",
         cuoi="Bà chủ nhìn Tavo bối rối, sốt ruột; miệng khép.",
         act="the woman shakes her head slightly and opens one palm, apologetic and anxious"),
    dict(g="D", w="TAVO", lang="Spanish", start="moi",
         eye="the boy looks at the woman on the right while speaking, then down at the beef; the woman watches his hands",
         dien="Tavo nói nhanh, dứt khoát, chỉ vội chiếc ghế nhựa mời bà ngồi rồi chộp ngay con dao phay; mọi thứ gấp gáp.",
         cuoi="Tavo cầm dao phay giơ trên tảng thịt, sẵn sàng; bà chủ đứng nhìn, lo lắng; miệng khép.",
         act="in a hurry, the boy points quickly toward a stool off-screen with one hand and at once grabs {{DAO_DAO}} from the block, ready to cut; brisk, urgent movements"),
    dict(g="D2", w=None, start="moi", len=10, tua=1.5,
         eye="the boy looks down at the meat and the cleaver the whole time",
         dien="CẢNH CÂM (~8 s, tua x1,5): Tavo chặt thịt cực nhanh như thợ lành nghề: dao lên xuống liên tục, mỗi nhát một miếng dày đều, gạt sang bên và chặt tiếp ngay, tay gần như nhoè vì nhanh, không một nhịp nghỉ.",
         cuoi="Một chồng thịt cắt dày đều bên cạnh; Tavo vẫn cúi tập trung.",
         act="the boy chops at extreme speed like a master butcher: the cleaver rises and falls again and again in a rapid blur of motion, one stroke per second or faster, each stroke slicing a thick even steak, "
             "the flat of the blade sweeping each finished steak aside while the other hand feeds the beef forward, never a pause, never slowing down; sure, expert and efficient, urgent as if the customer is waiting; clean cuts, no blood splashes"),
    dict(g="Y", w=None, start="moi", tua=1.5,
         eye="no face in the shot; the hands work on the counter",
         dien="CẢNH CÂM (~4 s, tua x1,5): chỉ thấy hai bàn tay Tavo gói thịt giấy hồng cực nhanh, thành thạo: mỗi gói chỉ vài giây (đặt, gấp, lật, ép), xếp lên chồng rồi với gói tiếp ngay. Đầu clip bên phải chỉ có 1 gói, cuối clip có 4 gói.",
         cuoi="Bên phải có 4 gói thịt giấy hồng xếp ngay ngắn.",
         act="the boy's hands wrap the steaks in pink butcher paper at top speed with the folds of a professional: lay a steak on the paper, fold the sides, roll it over, press it flat, "
             "set the package on the stack at the right and snatch the next sheet and steak at once, hands almost a blur, never a pause. At the first frame only ONE wrapped package stands at the right; "
             "by the last frame there are exactly FOUR neatly stacked wrapped packages there"),
    dict(g="W", w="CHU", lang="English", start="moi",
         eye="the woman looks at the four packages, then at the boy on the left; the boy looks at her",
         dien="Bà chủ nhìn bốn gói thịt bọc giấy hồng đã xong, sững sờ, rồi nhìn Tavo.",
         cuoi="Bà chủ nhìn Tavo, mắt mở to; Tavo mỉm cười nhẹ; miệng khép.",
         act="the woman's eyes go from the row of packages to the boy, amazed"),
    dict(g="E", w="CHU", lang="English", start="moi",
         eye="the woman looks at the boy on the right, warmly; the boy looks at her",
         dien="Bà chủ cảm ơn rối rít, hỏi tên Tavo.",
         cuoi="Bà chủ mỉm cười nhìn Tavo; miệng khép.",
         act="the woman leans her forearms on the display and smiles at the boy"),
    dict(g="E", w="TAVO", lang="Spanish", start="noi",
         eye="the boy looks at the woman on the left, embarrassed; the woman looks at him",
         dien="Tavo ngượng, khẽ lắc đầu: không hiểu.",
         cuoi="Tavo nhìn bà chủ, ngượng; miệng khép.",
         act="the boy gives a small shake of the head"),
    dict(g="E", w="CHU", lang="English", start="noi",
         eye="the woman looks at her phone, then at the boy; the boy looks at the phone",
         dien="Bà chủ lấy điện thoại ra, giơ màn hình về phía Tavo, chỉ vào màn hình ở chữ 'this app'.",
         cuoi="Bà chủ cầm điện thoại giơ về phía Tavo; Tavo nhìn màn hình; miệng khép.",
         act="the woman lifts {{DAO_DIEN_THOAI}} with its screen turned toward the boy (the camera sees only a soft glow, no readable screen) and taps it once with her index finger"),
    dict(g="E1", w="CHU", lang="English", start="moi",
         eye="the woman looks at the boy just to the RIGHT of the lens, never into it",
         dien="Bà chủ giơ một ngón tay lên, nhấn mạnh 'một tháng', hào hứng.",
         cuoi="Bà chủ mỉm cười, ngón tay vẫn giơ; miệng khép.",
         act="the woman raises her index finger as she says 'one month'"),
    dict(g="E", w=None, start=20, keep=3.5,
         eye="the woman looks at the boy on the right, moved; the boy looks at her, surprised",
         dien="CẢNH CÂM (~3,5 s): bà chủ nghiêng người qua quầy, khẽ đỡ đầu Tavo, hôn nhẹ lên trán cậu như người mẹ rồi đứng thẳng lại; Tavo sững người, ngượng.",
         cuoi="Bà chủ đã đứng thẳng, mỉm cười nhìn Tavo; Tavo ngượng, má ửng đỏ; miệng khép.",
         act="the woman leans across the counter toward the boy, gently holds the side of his head with one hand and gives him a quick motherly kiss on the forehead, "
             "then straightens back up with a warm smile; the boy freezes in surprise and blushes"),
    dict(g="E", w="CHU", lang="English", start="noi",
         eye="the woman looks at the boy on the right, grateful; the boy looks at her",
         dien="Bà chủ ôm gói thịt vào lòng, cảm động, nói lời cảm ơn.",
         cuoi="Bà chủ ôm gói thịt, mỉm cười nhìn Tavo; miệng khép.",
         act="the woman picks up one of the pink-wrapped packages from the top of the display and hugs it to her chest"),
    dict(g="N", w="TAVO", lang="English (very broken, heavy Spanish accent)", start="moi",
         eye="the boy looks down at the phone screen in his hands",
         dien="Đêm, Tavo nhìn màn hình, cố đọc từng tiếng Anh, ngập ngừng.",
         cuoi="Tavo nhìn màn hình, môi khép, căng thẳng.",
         act="the boy frowns with concentration, trying each word slowly"),
    dict(g="P", w="ROBOT", lang="English, then a few words of Spanish", start="moi",
         eye="the robot on the screen looks straight out of the phone, at the boy holding it",
         dien="Robot trên màn hình nói chậm rõ, giải nghĩa sang tiếng Tây Ban Nha.",
         cuoi="Robot mỉm cười trên màn hình; tay cầm điện thoại yên.",
         act="only the robot on the screen moves its face; the hands holding the phone stay still"),
    dict(g="N", w="TAVO", lang="Spanish", start=26,
         eye="the boy looks at the phone screen, then lifts his eyes from it, staring into space as the meaning sinks in",
         dien="Tavo sững sờ, ngỡ ngàng khi hiểu ra ý nghĩa câu nói (bà chủ đã nói với cậu 'cậu đã cứu tôi'): mắt mở to, miệng hé, thì thầm lại nghĩa bằng tiếng Tây Ban Nha, mắt rưng rưng.",
         cuoi="Tavo mắt mở to, ngấn nước, một tay đặt lên ngực; miệng khép.",
         act="the boy's eyes widen in astonishment as he realises what the words mean, his eyebrows rise, his lips part, he whispers the words in disbelief, "
             "his eyes fill with tears and one hand rises slowly to his chest"),
    dict(g="P", w="ROBOT", lang="English", start=27,
         eye="the robot on the screen looks straight out of the phone, at the boy holding it",
         dien="Robot mời Tavo nói theo.",
         cuoi="Robot mỉm cười chờ; tay cầm điện thoại yên.",
         act="only the robot on the screen moves its face; the hands holding the phone stay still"),
    dict(g="N", w="TAVO", lang="English (slow, careful, light Spanish accent)", start=26,
         eye="the boy looks at the phone screen",
         dien="Tavo nói chậm từng chữ, lần đầu trọn câu; xong mỉm cười nhẹ, tự hào.",
         cuoi="Tavo mỉm cười nhìn màn hình; miệng khép.",
         act="the boy speaks slowly and carefully, then a small proud smile appears"),
    dict(g="P", w="ROBOT", lang="English", start=27,
         eye="the robot on the screen looks straight out of the phone, at the boy holding it",
         dien="Robot khen, hẹn mai học tiếp.",
         cuoi="Robot cười tươi trên màn hình; tay cầm điện thoại yên.",
         act="only the robot on the screen moves its face; the hands holding the phone stay still"),
    # montage nhiều ngày, không lời: Tavo vừa làm việc vừa học bằng app (7 cảnh ngắn ~2,5 s, chớp trắng nhanh giữa các ngày)
    dict(g="Q1", w=None, start="moi", keep=1.3, trans="chớp trắng 0.2",
         eye="the boy looks down at the meat, glances at the phone screen beside him, then back at the meat",
         dien="CẢNH CÂM (ngày 1, ~2,5 s): ban ngày, Tavo chặt thịt nhanh tay, vừa nghe bài qua tai nghe vừa liếc màn hình điện thoại dựng cạnh cân, gật đầu.",
         cuoi="Tavo cúi chặt thịt, khẽ mỉm cười; miệng khép.",
         act="the boy cuts the meat quickly while listening through the earbud, glances at the phone screen, nods to himself and goes on cutting"),
    dict(g="Q2", w=None, start="moi", keep=1.3, trans="chớp trắng 0.2",
         eye="the boy glances at the phone in his left hand, then down at the floor as he sweeps",
         dien="CẢNH CÂM (ngày 2, ~2,5 s): tối muộn, chợ vắng, Tavo một tay quét sàn, tay kia cầm điện thoại có app sáng, tai nghe một bên, gật gù.",
         cuoi="Tavo dừng chổi, mỉm cười nhìn điện thoại; miệng khép.",
         act="the boy sweeps with one hand and holds {{DAO_DIEN_THOAI}} in the other with its screen glowing toward him, glances at it, nods along to what he hears and smiles"),
    dict(g="Q5", w=None, start="moi", keep=1.3, trans="chớp trắng 0.2",
         eye="the boy looks at the board he scrubs, then up at the phone on the shelf, then back to the board",
         dien="CẢNH CÂM (ngày 3, ~2,5 s): phòng sau, Tavo cọ thớt gỗ thoăn thoắt, điện thoại dựng trên kệ phát bài học, ngước nhìn và gật.",
         cuoi="Tavo cọ thớt, gật đầu hài lòng; miệng khép.",
         act="the boy scrubs the chopping block with a brush in quick strokes, looks up at the phone propped on the shelf, nods and keeps scrubbing"),
    dict(g="Q3", w=None, start="moi", keep=1.3, trans="chớp trắng 0.2",
         eye="the boy looks at the phone screen in his hands",
         dien="CẢNH CÂM (ngày 4, ~2,5 s): đêm trong kho, Tavo ngồi trên đống bao nhìn màn hình app chăm chú, mặt sáng lên, nắm tay ăn mừng.",
         cuoi="Tavo nắm tay, cười tươi nhìn màn hình; miệng khép.",
         act="the boy studies the phone screen intently, his face lights up and he clenches one fist in a small silent celebration"),
    dict(g="Q6", w=None, start="moi", keep=1.3, trans="chớp trắng 0.2",
         eye="the boy looks ahead at the display he walks to, then at the phone propped in the tray",
         dien="CẢNH CÂM (ngày 5, ~2,5 s): sáng, Tavo bưng khay thịt đầy đi nhanh đến tủ kính, điện thoại kẹp trên khay phát bài, tai nghe một bên.",
         cuoi="Tavo đặt khay xuống, nhìn điện thoại, mỉm cười; miệng khép.",
         act="the boy walks briskly carrying a tray of raw steaks with {{DAO_DIEN_THOAI}} wedged on its edge, listening through the earbud, sets the tray down and glances at the phone with a smile"),
    dict(g="Q7", w=None, start="moi", keep=1.3, trans="chớp trắng 0.2",
         eye="the boy looks at the glass he wipes, then at the phone leaning on the display",
         dien="CẢNH CÂM (ngày 6, ~2,5 s): Tavo lau tủ kính nhanh tay, điện thoại tựa trên nóc tủ hiện app, vừa lau vừa nhìn màn hình và gật đầu.",
         cuoi="Tavo lau xong, nhìn điện thoại, gật đầu; miệng khép.",
         act="the boy wipes the glass display in fast circles with a cloth, {{DAO_DIEN_THOAI}} leaning on top of the display with its screen glowing, glances at it and nods"),
    dict(g="Q4", w=None, start="moi", keep=1.3, trans="chớp trắng 0.2",
         eye="the boy looks at the steaks in the display, then straight ahead, past the lens; never into the lens",
         dien="CẢNH CÂM (sáng sớm, ~2,5 s): Tavo xếp miếng thịt cuối vào tủ kính, đứng thẳng, hít sâu, mỉm cười tự tin: đã sẵn sàng.",
         cuoi="Tavo đứng thẳng, mỉm cười tự tin; miệng khép.",
         act="the boy places the last steak neatly in the display, stands up straight, takes a deep breath and smiles with quiet confidence"),
    dict(id="m", g="M", w="CHU", lang="English", start="moi",
         eye="the woman looks at the butcher on the right; the butcher looks at her",
         dien="Một tháng sau, bà chủ quay lại quầy, hỏi ông chú về cậu trai đã cắt thịt cho bà.",
         cuoi="Bà chủ nhìn ông chú, chờ; miệng khép.",
         act="the woman holds {{DAO_SO}} and gestures lightly with it toward the stall"),
    dict(id="m2", g="M", w="TIO", lang="English (heavy Spanish accent)", start="noi",
         eye="the butcher looks at the woman at the left, grinning proudly; the woman looks at him, her mouth closed",
         dien="Ông chú nhận vơ, vỗ ngực khoe 'tôi là thợ cả, hai mươi năm'.",
         cuoi="Ông chú cười toe, tay đặt trên ngực; miệng khép.",
         act="the butcher pats his chest twice with one hand, grinning"),
    dict(g="M", w="CHU", lang="English", start="noi",
         eye="the woman looks at the butcher on the right and shakes her head gently with a kind small smile; the butcher looks at her, taken aback, his mouth closed",
         dien="Bà chủ lắc đầu nhẹ, mỉm cười, đính chính với ông chú: người bà cần tìm không phải ông mà là cậu trai trẻ; ông chú khựng lại, miệng khép.",
         cuoi="Bà chủ nhìn ông chú, mỉm cười nhẹ; ông chú sững; miệng khép.",
         act="the woman shakes her head gently and, with a kind small smile, lifts one open hand a little as if pointing out someone else"),
    dict(g="M", w="TIO", lang="Spanish", start="noi",
         eye="the butcher turns his head sharply to the RIGHT, toward the boy off-screen, scolding; the woman at the left looks at the butcher, her mouth closed",
         dien="Ông chú quay sang phải (Tavo ngoài khung), quát khẽ, chê cậu.",
         cuoi="Ông chú nhìn sang phải, cau mày; miệng khép.",
         act="the butcher turns his head to the right and flicks one hand dismissively"),
    dict(g="F", w="TAVO", lang="English (clear, light Spanish accent)", start="moi",
         eye="the boy looks at the woman on the left, steady and calm; the woman looks at him, her eyes brightening with gentle joy",
         dien="Tavo bước ra, nói tiếng Anh rõ ràng, bình tĩnh: chính cậu đã cắt thịt.",
         cuoi="Tavo nhìn bà chủ; bà chủ sững lại rồi mắt sáng lên vui mừng; miệng khép.",
         act="the boy stands up straight and speaks calmly"),
    dict(g="F", w="CHU", lang="English", start="noi",
         eye="the woman looks at the boy on the right with a bright, gentle, delighted smile; the boy looks at her",
         dien="Bà chủ vui mừng, nhẹ nhàng, mắt sáng, mỉm cười hỏi Tavo.",
         cuoi="Bà chủ nhìn Tavo, mỉm cười vui mừng; miệng khép.",
         act="the woman's face lights up in a soft, happy, delighted smile, her eyebrows lifting gently"),
    dict(g="F", w="TAVO", lang="English (clear, light Spanish accent)", start="noi",
         eye="the boy looks at the woman on the left; the woman listens with a warm, quietly happy smile",
         dien="Tavo mỉm cười khiêm tốn.",
         cuoi="Tavo mỉm cười nhìn bà; miệng khép.",
         act="the boy smiles modestly"),
    dict(g="F", w="CHU", lang="English", start="noi",
         eye="the woman looks at the boy on the right with a warm, happy, gentle smile and bright eyes; the boy looks at her",
         dien="Bà chủ vui mừng, nhẹ nhàng, mời Tavo về làm cho nhà hàng của bà.",
         cuoi="Bà chủ mỉm cười vui mừng nhìn Tavo; Tavo sững người; miệng khép.",
         act="the woman, with a soft happy smile, holds out one open hand toward the boy on 'the job is yours', then lowers it"),
    dict(g="G", w="TAVO", lang="English (clear, light Spanish accent)", start="moi",
         eye="the boy looks at the woman off-screen to the LEFT, moved, eyes shining; the butcher behind him stares at the boy",
         dien="Tavo xúc động, nói với bà chủ (ngoài khung bên trái).",
         cuoi="Tavo mỉm cười, mắt sáng; ông chú phía sau nhìn cậu; miệng khép.",
         act="the boy smiles with shining eyes"),
    dict(g="G", w="TAVO", lang="Spanish", start="noi",
         eye="the boy turns his head over his shoulder to the LEFT and looks at the butcher behind him; the butcher looks back, stunned",
         dien="Tavo quay đầu qua vai trái nhìn ông chú, nói tự tin.",
         cuoi="Tavo nhìn ông chú; ông chú sững sờ; miệng khép.",
         act="the boy turns his head over his left shoulder toward the butcher as he speaks"),
    dict(g="H", w="TAVO", lang="Spanish", start="moi",
         eye="the boy looks straight into the lens, talking to the viewer",
         dien="Tavo nhìn thẳng ống kính, giơ điện thoại lên cạnh mặt (màn hình là ảnh robot, không chữ), kể lại hành trình.",
         cuoi="Tavo cầm điện thoại cạnh mặt, mỉm cười; miệng khép.",
         act="the boy lifts {{DAO_DIEN_THOAI}} beside his face with the screen toward the camera, the screen showing only the glossy white humanoid robot face from the start frame, no text"),
    dict(g="H", w="TAVO", lang="Spanish", start="noi",
         eye="the boy looks straight into the lens, talking to the viewer",
         dien="Tavo cười tươi, mời người xem tải app.",
         cuoi="Tavo cười tươi nhìn ống kính; miệng khép.",
         act="the boy breaks into a big confident smile"),
]

HEAD = """[HAU KY]:
loai: tiem-thit-tieng-anh
Thể loại "tiệm thịt học tiếng Anh" (hoạt hình 3D kể chuyện, video mẫu 0610_Cut meat ES, 177 giây): MỘT phần, cảnh thường, {N_CANH} cảnh ({N_CAM} cảnh không lời).
Tavo (cậu bé phụ việc tiệm thịt, không biết tiếng Anh) bị ông chú bóc lột và chê trước khách; một bà chủ nhà hàng cần gấp thịt, Tavo cắt giúp trong 10 phút,
bà chỉ cho cậu app học tiếng Anh AI; Tavo học mỗi ngày trong lúc làm việc; một tháng sau bà quay lại, Tavo nói tiếng Anh, được nhận việc.
Cảnh có lời: mỗi cảnh một người nói. Cảnh KHÔNG LỜI (lượt "text" rỗng trong biến thể, Voice trống): clip câm, engine bỏ SPEAKER MAP; "Cắt còn: N" giữ N giây đầu, "Tua: K" tua nhanh K lần.
Góc máy: A (quầy rộng), K (cận khách), T (cận Tavo ấp úng), B (cận hai chú cháu ở thớt), X (bà chủ tìm quầy trong chợ), C (phòng sau quầy), D (thớt lớn), D2 (chặt thịt nhanh),
Y (tay gói thịt), W (4 gói thịt), E (quầy cân treo), E1 (cận bà chủ), N (đêm, cận Tavo), P (điện thoại có robot AI), Q1–Q4 (montage học nhiều ngày),
M/M2 (một tháng sau), F (hai người đối mặt), G (cận Tavo, ông chú mờ sau), H (Tavo nhìn ống kính).
Cảnh có "Prompt ảnh" sinh khung đầu mới; "Khung đầu: Chính là khung cuối của cảnh trước" nối tiếp; "Khung đầu từ cảnh: N" dùng lại khung đầu cảnh N.
BẮT BUỘC gắn ảnh tham chiếu cho TAVO, TIO, KHACH, CHU, ROBOT (refs trong biến thể): nhiều góc máy, không có ảnh thì mặt/trang phục đổi giữa các cảnh.
Hậu kỳ riêng (post.py): phụ đề trắng viền đen; lượt tiếng Anh có dòng dịch tiếng Tây Ban Nha ("dich"). End card app: Thương hiệu -> Outro, không gen.
Khối [HAU KY] này không gửi cho Muse.

[STYLE LOCK]:
Vertical 9:16 Pixar-style 3D CARTOON exactly like the character reference images: cartoon proportions, big round expressive eyes, simplified smooth features, soft rounded shapes, warm glowing skin, rich detail; never photorealistic or semi-realistic human faces. Every shot is one fixed static camera (no camera movement inside a clip). Each clip uses the camera angle described in its start frame. The same characters (each only in the shots that name them), the same market stall in every daytime clip. No text, no letters, no numbers, no logos, no captions, no icons, no price tags with writing, no lettering on clothes, signs, paper or phone screens anywhere in the frame.

[CHAR LOCK]:
CHARACTERS: each person appears ONLY in the shots whose CAMERA ANGLE names them; a close-up shows only its one person, and nobody else is ever added behind or beside them.
The {{VAI_TAVO}}, {{TEN_TAVO}}: {{NGUOI_TAVO}}. VOICE LOCK BOY: one single voice, {{GIONG_TAVO}}, the same in every clip.
The {{VAI_TIO}}, {{TEN_TIO}}: {{NGUOI_TIO}}. VOICE LOCK BUTCHER: one single voice, {{GIONG_TIO}}, the same in every clip.
The {{VAI_KHACH}}, {{TEN_KHACH}}: {{NGUOI_KHACH}}. VOICE LOCK CUSTOMER: one single voice, {{GIONG_KHACH}}, the same in every clip.
The {{VAI_CHU}}, {{TEN_CHU}}: {{NGUOI_CHU}}. VOICE LOCK WOMAN: one single voice, {{GIONG_CHU}}, the same in every clip.
The {{VAI_ROBOT}}, {{TEN_ROBOT}}: {{NGUOI_ROBOT}}, seen only on a phone screen. VOICE LOCK ROBOT: one single voice, {{GIONG_ROBOT}}, the same in every clip.
When a character who is in the shot is silent: the boy {{NGHE_TAVO}}; the butcher {{NGHE_TIO}}; the customer {{NGHE_KHACH}}; the woman {{NGHE_CHU}}; the robot {{NGHE_ROBOT}}.
RULE: in each clip with a line exactly ONE character speaks, one line, with lip-sync and an expressive face, keeping the EYE LINE. Anyone else in the frame stays silent with the mouth closed. Each voice stays the same in every clip.
EYE LINE (every clip): the speaker looks where the clip's EYE LINE says for the whole line; listeners look at the speaker. Nobody looks into the lens unless the clip's EYE LINE says so.
ACTION CLIPS: a physical action is done WHILE the line is spoken and is complete by the last word. Props, the same in every clip: {{DAO_TIEN}}, {{DAO_SO}}, {{DAO_DAO}}, {{DAO_GOI}}, {{DAO_DIEN_THOAI}}; each appears only when a clip shows it, never duplicated, never with readable text.

[SET LOCK]:
Daytime: {{NEN_SAP}}, inside {{NEN_CHO}}. The back room: {{NEN_PHONG}}. Night: {{NEN_DEM}}. A shot shows ONLY the people its CAMERA ANGLE names; shoppers far in the background are tiny, blurred and stand still. Nothing moves in the background.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no shake, no cut. Real people caught on camera, not actors. No subtitles, no text, no music. 9:16. In a clip with a line, the speaker starts right away at a natural conversational pace (about 3 words per second, short lines up to 4, short pauses allowed), finishes the line and then, after the last word and the action, everyone keeps a calm closed-mouth face and stays still until the end of the clip, with no crowd noise over the voice.

[NEGATIVE]:
text, captions, subtitles, logos, icons, emoji, numbers, price tags with writing, lettering on clothes, signs, paper or phone; app interface, buttons or chat bubbles on a phone screen; camera movement, zoom, shake, cut; two voices in one clip; a silent character moving the mouth; a character who is not in this shot appearing; extra people in the foreground; moving crowd; face, hair or outfit changing; realistic live-action look; photorealistic or semi-realistic faces; one character copying another's movements; background music; robotic or text-to-speech voice for the humans; a clip with a line but no speech; movement during the final still after the speech; props multiplying, vanishing or appearing in the wrong clip; slow, dragged speech; blood.
"""

IMG = "Generate exactly one still image now, vertical 9:16, Pixar-style 3D animated feature-film look exactly like the character reference images, {light}. {body} EYE LINE: {eye}. Mouths closed, natural expressions. No text, no logos, no numbers, no lettering anywhere. Output only the image."


def names(keys):
    return " and ".join("{{TEN_%s}}" % k for k in keys)


def mute_scene(n, s, a, b):
    """Cảnh KHÔNG LỜI: lượt n của biến thể có "text" rỗng -> {{LUOT_n}} thành chuỗi rỗng (Voice trống); engine tạo clip câm (mute_prompt)
    và giữ nguyên độ dài clip, hoặc cắt / tua theo "Cắt còn" / "Tua". Không có câu nào nói về giọng, lời (engine cũng lọc bỏ)."""
    vn, light, body, people, close = ANG[s["g"]]
    noi = s["start"] == "noi"
    lines = [f"CẢNH {n} ({a // 60}:{a % 60:02d}–{b // 60}:{b % 60:02d}): Lượt {n} (không lời)"]
    lines.append(f"Bối cảnh: {vn}; không có chữ, không người lạ." + (" Nối từ khung cuối cảnh trước." if noi else ""))
    lines.append(f"Voice: {{{{LUOT_{n}}}}}")
    lines.append("Khung đầu: Chính là khung cuối của cảnh trước." if noi else f"Khung đầu: ảnh mới theo góc {s['g']}; miệng mọi người khép.")
    lines.append(f"Khung cuối: {s['cuoi']}")
    lines.append(f"Hướng nhìn: {s['eye']}.")
    lines.append(f"Diễn biến: {s['dien']}")
    if not noi:
        lines.append("Prompt ảnh: " + IMG.format(light=light, body=body, eye=s["eye"]))
    start = ("Start exactly from the provided start frame (the last frame of the previous clip) and continue from it with no cut or reset."
             if noi else "Start exactly from the start-frame image and keep its camera angle.")
    if s["g"] == "Y":
        only = "Only the boy's two hands and forearms are in this clip; no face, nobody else ever appears."
    else:
        only = f"Only {names(people)} {'is' if len(people) == 1 else 'are'} in this clip; nobody else ever appears."
    lock = ("CAMERA LOCK: the camera is locked off on this close shot for the whole clip: no pan, no zoom out, no reframing."
            if close else "LOCKED CAMERA on a tripod: no pan, no tilt, no zoom; the framing of the start frame stays the same to the last frame, even when a person walks.")
    vid = (f"STYLE LOCK, SET LOCK. {start} {only} {lock} CHAR LOCK. {{{{LUOT_{n}}}}} "
           f"EYE LINE for the whole clip: {s['eye'].replace('LEFT', 'left').replace('RIGHT', 'right')}. "
           f"ACTION, from the first frame to the last: {s['act']}. Mouths closed unless the ACTION describes otherwise. "
           f"Only the quiet natural sound of the place and of the action, no music. VIDEO SUFFIX.")
    lines.append("Prompt video: " + vid)
    lines.append("Audio: Không lời. Chỉ tiếng động tự nhiên của nơi đó và của hành động; không nhạc.")
    neg = "text or captions; camera movement; a character not in this shot appearing; anyone talking or mouthing words; music"
    if close:
        neg += "; anyone else added behind or beside the person"
    if s["g"] in ("D2", "Y"):
        neg += "; blood splashes; slow movements"
    lines.append("Negative prompt: " + neg + ".")
    if isinstance(s["start"], int):
        lines.append(f"Khung đầu từ cảnh: {s['start']}")
    if s.get("trans"):
        lines.append(f"Chuyển cảnh: {s['trans']}")
    if s.get("tua"):
        lines.append(f"Tua: {s['tua']}")
    if s.get("keep"):
        lines.append(f"Cắt còn: {s['keep']}")
    return "\n".join(lines)


def scene(i, s, a, b):
    n = i + 1
    if s["w"] is None:
        return mute_scene(n, s, a, b)
    vn, light, body, people, close = ANG[s["g"]]
    who = s["w"]
    s = dict(s, eye=s["eye"].replace("LEFT", "left").replace("RIGHT", "right"))   # từ vị trí viết hoa trong Prompt video từng bị Muse vẽ thành chữ
    lines = [f"CẢNH {n} ({a // 60}:{a % 60:02d}–{b // 60}:{b % 60:02d}): Lượt {n}"]
    noi = s["start"] == "noi"
    lines.append(f"Bối cảnh: {vn}; không có chữ, không người lạ." + (" Nối từ khung cuối cảnh trước." if noi else ""))
    lines.append(f"Voice: ({s['lang'].split(' (')[0].split(',')[0]}, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}")
    if noi:
        lines.append("Khung đầu: Chính là khung cuối của cảnh trước.")
    else:
        lines.append(f"Khung đầu: ảnh mới theo góc {s['g']}; miệng mọi người khép.")
    lines.append(f"Khung cuối: {s['cuoi']} Mọi người đứng im đến hết clip.")
    lines.append(f"Hướng nhìn: {s['eye']}.")
    lines.append(f"Diễn biến: {s['dien']} Nói xong mọi người đứng im đến hết clip.")
    if not noi:
        lines.append("Prompt ảnh: " + IMG.format(light=light, body=body, eye=s["eye"]))
    start = ("Start exactly from the provided start frame (the last frame of the previous clip) and continue from it with no cut or reset."
             if noi else "Start exactly from the start-frame image and keep its camera angle.")
    if who == "ROBOT":
        only = "Only {{TEN_ROBOT}} on the phone screen and the boy's hands holding the phone are in this clip; no face of the boy, nobody else ever appears."
        speak = "Only the robot on the phone screen speaks, with lip-sync and a friendly expressive face."
    else:
        only = f"Only {names(people)} {'is' if len(people) == 1 else 'are'} in this clip; nobody else ever appears."
        speak = "Only that character speaks, with lip-sync and an expressive face."
    lock = ("CAMERA LOCK: the camera is locked off on this close shot for the whole clip: no pan, no zoom out, no reframing."
            if close else "LOCKED CAMERA on a tripod: no pan, no tilt, no zoom; the framing of the start frame stays the same to the last frame.")
    hold = s.get("hold")
    after = ("The action continues for a few seconds after the line; then everyone stays still." if hold
             else "After the line and the action everyone stays still until the end.")
    vid = (f"STYLE LOCK, SET LOCK. {start} {only} {lock} CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} {speak} "
           f"LANGUAGE of this line: {s['lang']}. EYE LINE for the whole clip: {s['eye']}; the speaker never turns the head away from where the EYE LINE says while talking. "
           f"Anyone else in the shot keeps the mouth closed. Natural pace, about 3 words per second. "
           f"ACTION, done WHILE the line is spoken: {s['act']}. {after} Same voices as always, clean dry sound, no music. VIDEO SUFFIX.")
    lines.append("Prompt video: " + vid)
    lines.append("Audio: Chỉ giọng của một nhân vật, rõ, gần; phần còn lại im lặng. Không nhạc, không tiếng ồn chợ đè lên giọng.")
    neg = "two voices; a silent character moving the mouth; text or captions; camera movement; a character not in this shot appearing; no speech"
    if close:
        neg += "; anyone else added behind or beside the person"
    if who == "ROBOT":
        neg += "; the boy's face; app buttons, chat bubbles or text on the screen"
    lines.append("Negative prompt: " + neg + ".")
    if isinstance(s["start"], int):
        lines.append(f"Khung đầu từ cảnh: {s['start']}")
    if hold:
        lines.append(f"Giữ sau lời: {hold}")
    return "\n".join(lines)


def main():
    ids = {s["id"]: i + 1 for i, s in enumerate(S) if s.get("id")}
    for s in S:
        if isinstance(s["start"], str) and s["start"].startswith("@"):
            s["start"] = ids[s["start"][1:]]   # "@m" -> số cảnh có id "m" (dùng nguyên khung đầu của cảnh đó)
    n_cam = sum(1 for s in S if s["w"] is None)
    parts = [HEAD.replace("{N_CANH}", str(len(S))).replace("{N_CAM}", str(n_cam))]
    t = 0
    for i, s in enumerate(S):
        if isinstance(s["start"], int):
            src = S[s["start"] - 1]
            assert src["g"] == s["g"] and src["start"] == "moi", f"cảnh {i+1}: khung đầu từ cảnh {s['start']} phải cùng góc và có Prompt ảnh"
        if s["start"] == "noi":
            assert i > 0 and S[i - 1]["g"] == s["g"], f"cảnh {i+1}: nối khung cuối nhưng cảnh trước khác góc"
        ln = s.get("len", 5)   # mốc thời gian chỉ quyết định độ dài clip của cảnh KHÔNG LỜI (cảnh có lời: Studio tính theo số âm tiết)
        parts.append(scene(i, s, t, t + ln))
        t += ln
    open(OUT, "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
    print(f"Đã ghi {os.path.normpath(OUT)}: {len(S)} cảnh ({n_cam} không lời)")
    print("Người nói theo cảnh:", " ".join((s["w"] or "-").lower() for s in S))


if __name__ == "__main__":
    main()
