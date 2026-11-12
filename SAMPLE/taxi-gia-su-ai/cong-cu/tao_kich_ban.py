"""Sinh KICH-BAN-TAXI-GIA-SU-AI.txt từ bảng góc máy + bảng cảnh (sửa một chỗ, chạy lại).
  runtime\\python.exe SAMPLE\\taxi-gia-su-ai\\cong-cu\\tao_kich_ban.py
Thể loại: phim hoạt hình 3D kể chuyện, HAI phần (video mẫu 0510_cartoon turn car_015_1, 95 giây):
  PHẦN 1 cảnh thường, 25 cảnh (20 có lời + 5 KHÔNG LỜI), 10 góc máy: taxi -> gara -> phòng khách. Nhân vật HOC (tài xế), KHACH, QUANLY, ARJUN, CON.
  PHẦN 2 ghép 2 lớp: tài xế (HOC) toàn khung trong taxi + robot gia sư AI (DAY) trong ô ngang bo góc phía trên.
Cảnh không lời của phần 1: lượt có "text" = MARKER "[KHONG LOI]" trong biến thể (nhieu_phan dùng chung bỏ lượt rỗng, nên gen.py của thể loại
đổi MARKER thành chuỗi rỗng ngay trước khi engine chạy -> engine tạo clip câm như tiem-thit-tieng-anh)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "KICH-BAN-TAXI-GIA-SU-AI.txt")

DAY = "bright sunny late-afternoon light in a busy New York avenue"
GARA = "cool white fluorescent light inside a taxi garage mixed with daylight from the open roll-up door"
NHA = "soft natural daylight through sheer white curtains in a cosy living room"

# góc: (mô tả tiếng Việt, ánh sáng, mô tả khung hình tiếng Anh, khoá nhân vật có mặt, cận?)
ANG = {
    "A": ("góc A: nhìn qua kính chắn gió từ trên nắp capô taxi vàng: tài xế bên PHẢI cầm vô lăng (ngực trở lên); khách ngồi ghế sau bên TRÁI, nhỏ hơn, áp điện thoại vào tai; phố đông, nhà chọc trời phía sau",
          DAY,
          "CAMERA ANGLE A, medium shot looking into a yellow taxi through its clean windscreen from just above the yellow bonnet (the glossy yellow bonnet fills the bottom fifth of the frame): "
          "{{TEN_HOC}} ({{NGUOI_HOC}}) sits behind the steering wheel on the RIGHT half, chest-up, both hands on the wheel; in the back seat on the LEFT, smaller and further away, "
          "{{TEN_KHACH}} ({{NGUOI_KHACH}}) sits upright holding {{DAO_DIEN_THOAI_KH}} to his right ear; above the taxi roof and through the rear window {{NEN_PHO}}. The taxi is DRIVING forward down the avenue: the street outside the side windows, the rear window and above the roof slides past from front to back with a soft motion blur. ONE continuous shot exactly like the start frame for the whole clip: the passenger stays small in the back seat at the LEFT and the driver stays big at the RIGHT; the camera never cuts, never moves closer to the back seat and never reframes on whoever speaks.",
          ["HOC", "KHACH"], False),
    "P": ("góc P: trong xe, từ ghế phụ nhìn sang: tài xế ngồi ghế lái giữa-trái, nghiêng 3/4 về camera, cầm điện thoại thấp trong hai tay gần vô lăng, nhìn màn hình; cửa sổ sau lưng là phố gạch yên tĩnh",
          DAY,
          "CAMERA ANGLE P: medium close shot from the front passenger seat inside the parked taxi: {{TEN_HOC}} ({{NGUOI_HOC}}) sits in the driver's seat at the LEFT-centre, turned three-quarters toward the camera, "
          "holding {{DAO_DIEN_THOAI_TX}} low in both hands near the steering wheel, its screen turned toward him (the camera sees only a soft glow, nothing readable); "
          "through the side window behind him a quiet street of brick buildings. He is the only person in the frame.",
          ["HOC"], True),
    "G": ("góc G: trong gara taxi, ba người đứng hàng ngang từ gối trở lên: tài xế TRÁI, quản lý GIỮA cầm bảng kẹp hồ sơ, Arjun PHẢI; vài tài xế khác đứng xa phía sau, mờ, đứng yên",
          GARA,
          "CAMERA ANGLE G, medium-wide shot inside {{NEN_GARA}}: three men stand in a row facing the camera, from the knees up: {{TEN_HOC}} ({{NGUOI_HOC}}) at the LEFT, "
          "{{TEN_QUANLY}} ({{NGUOI_QUANLY}}) in the CENTRE, {{TEN_ARJUN}} ({{NGUOI_ARJUN}}) at the RIGHT; a few other taxi drivers in work clothes stand far behind them, small, blurred and still.",
          ["HOC", "QUANLY", "ARJUN"], False),
    "K": ("góc K: cận chùm chìa khoá: tay áo vest xanh của quản lý từ TRÁI chìa chìa khoá, bàn tay Arjun đeo đồng hồ bạc từ PHẢI đưa vào nhận; phía sau đồng nghiệp mờ vỗ tay",
          GARA,
          "CAMERA ANGLE K: close-up at chest height in the garage: from the LEFT an older man's hand in a navy suit sleeve holds out {{DAO_CHIA_KHOA}} by the ring; "
          "from the RIGHT a younger man's open palm with a silver wristwatch on the wrist reaches in under it; behind them, softly out of focus, a few co-workers in work shirts. No face is in focus.",
          ["QUANLY", "ARJUN"], True),
    "X": ("góc X: toàn cảnh gara: chiếc taxi vàng mới tinh đỗ tiền cảnh bên PHẢI, đầu xe chếch về camera; phía sau quản lý và Arjun đứng cạnh nhau cười, một hàng đồng nghiệp vỗ tay",
          GARA,
          "CAMERA ANGLE X, wide shot of the garage: a shiny brand-new yellow taxi with a blank roof light stands in the foreground at the RIGHT, its front angled toward the camera; "
          "behind it {{TEN_QUANLY}} ({{NGUOI_QUANLY}}) and {{TEN_ARJUN}} ({{NGUOI_ARJUN}}) stand side by side, smiling, with a short row of co-workers in work shirts; the open roll-up door and the street behind.",
          ["QUANLY", "ARJUN"], False),
    "J": ("góc J (như video gốc): cận hai người đứng đối mặt trong gara: tài xế bên TRÁI tiền cảnh từ ngực trở lên, mặt nghiêng 3/4 quay sang PHẢI; Arjun bên PHẢI quay sang TRÁI, tay cầm chìa khoá ngang thắt lưng; taxi vàng mới mờ phía sau",
          GARA,
          "CAMERA ANGLE J, close two-shot in the garage, both men standing face to face: {{TEN_HOC}} ({{NGUOI_HOC}}) on the LEFT half in the foreground, from the chest up, his face in three-quarter view turned RIGHT toward the young man; "
          "{{TEN_ARJUN}} ({{NGUOI_ARJUN}}) on the RIGHT half, from the chest up, turned LEFT toward him, {{DAO_CHIA_KHOA}} dangling from one hand at his waist; "
          "behind them the new yellow taxi and the garage, softly out of focus. Only these two people are in the frame.",
          ["HOC", "ARJUN"], True),
    "T": ("góc T: cận tài xế một mình trong gara, đầu và vai, giữa-trái, mặt hơi quay sang PHẢI, mắt nhìn xuống; taxi vàng mờ phía sau",
          GARA,
          "CAMERA ANGLE T: close-up of {{TEN_HOC}} ({{NGUOI_HOC}}) in the garage, head and shoulders, centre-left, face turned slightly to the RIGHT of the lens, eyes down; "
          "behind him the yellow taxi and the garage, softly out of focus. He is the only person in the frame.",
          ["HOC"], True),
    "L": ("góc L: phòng khách rộng: tài xế ngồi khom trên sofa sáng màu tiền cảnh TRÁI, tay chống gối, cúi mặt; con gái đứng phía sau bên PHẢI gần cửa sổ, cầm cốc; bàn trà gỗ có sách mở + tách cà phê góc dưới phải",
          NHA,
          "CAMERA ANGLE L, medium-wide shot of {{NEN_NHA}}: {{TEN_HOC}} ({{NGUOI_HOC}}) sits hunched on a light-beige sofa in the LEFT foreground, from the thighs up, forearms on his knees, eyes down; "
          "in the back at the RIGHT, standing near the window, {{TEN_CON}} ({{NGUOI_CON}}) holds {{DAO_COC}} in both hands; on a low wooden coffee table at the bottom right an open book and a coffee cup on a saucer. "
          "Only these two people are in the frame.",
          ["HOC", "CON"], False),
    "L2": ("góc L2: cận hai bố con ngồi sofa: bố TRÁI (ngực trở lên) hơi quay sang PHẢI; con gái ngồi sát bên PHẢI quay sang TRÁI, hai tay cầm cốc trên đùi; mép dưới là bàn trà, sách mở, tách cà phê; sau lưng cửa sổ rèm trắng",
           NHA,
           "CAMERA ANGLE L2, close two-shot on the sofa: {{TEN_HOC}} ({{NGUOI_HOC}}) sits at the LEFT, from the chest up, turned slightly RIGHT toward her; {{TEN_CON}} ({{NGUOI_CON}}) sits close beside him at the RIGHT, "
           "turned LEFT toward him, holding {{DAO_COC}} in both hands on her lap; the open book and the coffee cup on the coffee table along the bottom edge; behind them the window with sheer white curtains. "
           "Only these two people are in the frame.",
           ["HOC", "CON"], True),
    "PH": ("góc PH: cận điện thoại trong tay con gái (tay áo pyjama xanh bạc hà chấm bi), màn hình hướng camera là robot trắng thân thiện trên nền xanh, không chữ; ngón trỏ tay kia chỉ vào màn hình; nền sàn phòng khách mờ",
           NHA,
           "CAMERA ANGLE PH: close-up of {{DAO_DIEN_THOAI}} held upright in a girl's right hand (a mint-green polka-dot pajama sleeve), the screen turned toward the camera; the index finger of her other hand points at the screen; "
           "behind, softly out of focus, the living-room rug and the coffee table. No face in the frame.",
           ["CON"], True),
    "L3": ("góc L3: như L2 nhưng cốc đã đặt lên bàn; con gái cầm điện thoại bằng tay phải, màn hình (robot, không chữ) xoay về phía bố; bố cúi nhìn màn hình",
           NHA,
           "CAMERA ANGLE L3, close two-shot on the sofa: {{TEN_HOC}} ({{NGUOI_HOC}}) sits at the LEFT, from the chest up, leaning slightly RIGHT toward the phone; {{TEN_CON}} ({{NGUOI_CON}}) sits close beside him at the RIGHT, "
           "holding {{DAO_DIEN_THOAI}} in her right hand at chest height with the screen turned toward him; {{DAO_COC}} stands on the coffee table along the bottom edge next to the open book; "
           "behind them the window with sheer white curtains. Only these two people are in the frame.",
           ["HOC", "CON"], True),
}

MK = None   # người nói None = cảnh KHÔNG LỜI

# cảnh phần 1: góc, người nói, ngôn ngữ, "moi" (Prompt ảnh) / "noi" (khung cuối cảnh trước) / số cảnh (Khung đầu từ cảnh), hướng nhìn EN,
#              diễn biến VN, khung cuối VN, hành động EN (trong lúc nói), [keep/tua/trans/len]
S = [
    dict(g="A", w="KHACH", lang="English", start="moi",
         eye="the passenger looks forward at the back of the driver's head, the phone at his ear; the driver looks ahead at the road, just past the lens",
         dien="Khách ngồi sau, điện thoại áp tai, chồm người tới trước nhờ tài xế rẽ trái; tài xế nhìn đường, nghe.",
         cuoi="Khách ngồi lại, điện thoại vẫn áp tai; tài xế hai tay trên vô lăng, ngơ ngác; miệng khép.",
         act="the passenger, phone held at his ear in one hand, leans forward a little toward the driver, gives one small nod toward the road ahead with his head only, then sits back; his free hand rests on his knee the whole time"),
    dict(g="A", w="HOC", lang="English (very broken, heavy Mexican accent)", start=1,
         eye="the driver glances up toward the rear-view mirror at the passenger, confused, then back at the road; the passenger frowns at him",
         dien="Tài xế ngập ngừng lặp lại 'Fifth', nhíu mày, xin lỗi vì không hiểu; hai tay vẫn trên vô lăng.",
         cuoi="Tài xế nhìn đường, lúng túng; khách cau mày; miệng khép.",
         act="the driver frowns, raises his eyebrows and gives a small apologetic shake of the head, both hands staying on the wheel"),
    dict(g="A", w="KHACH", lang="English", start=1,
         eye="the passenger looks forward at the driver, then over his own shoulder back through the rear window; the driver looks ahead at the road, sad",
         dien="Khách bắt đầu nói 'rẽ trái ở...' rồi ngoái lại nhìn qua cửa kính sau, bực: xe đã qua chỗ rẽ.",
         cuoi="Khách ngồi yên ghế sau, điện thoại áp tai, nhìn tài xế bực; tài xế nhìn đường, lo; miệng khép.",
         act="the passenger, phone still at his ear, turns his head to glance back through the rear window, then turns it back toward the driver with an annoyed frown; his free hand rests on his knee"),
    dict(g="A", w="KHACH", lang="English", start=1,
         eye="the passenger glares at the back of the driver's head; the driver keeps his eyes on the road, embarrassed",
         dien="Khách gắt, giơ tay lên trời.",
         cuoi="Khách ngồi tựa lưng ghế, điện thoại áp tai, tay trống trên đầu gối; tài xế cúi mặt nhìn đường; miệng khép.",
         act="the passenger lifts his free open hand a little toward the driver in annoyance, then lowers it to his knee and settles back against the seat; the phone stays at his ear"),
    dict(g="A", w="KHACH", lang="English", start=1,
         eye="the passenger looks out of the side window beside him at the LEFT edge of the frame, talking into the phone; the driver looks ahead at the road, sad",
         dien="Khách quay sang nói vào điện thoại với người bên kia, chê tài xế không biết tiếng Anh; tài xế nghe thấy, buồn.",
         cuoi="Khách nhìn ra cửa sổ, điện thoại áp tai; tài xế buồn; miệng khép.",
         act="the passenger turns his head toward the side window and speaks into the phone with a tired sigh"),
    dict(g="A", w="KHACH", lang="English", start=1,
         eye="the passenger looks out of the side window beside him at the LEFT edge of the frame, talking into the phone; the driver looks ahead at the road, sad",
         dien="Khách thở dài với người trong điện thoại; tài xế mím môi, cúi mắt.",
         cuoi="Khách nhìn ra cửa sổ; tài xế cúi mắt nhìn vô lăng, buồn; miệng khép.",
         act="the passenger rolls his eyes and rubs his forehead once with his free hand"),
    dict(g="P", w=None, start="moi", keep=3, trans="chớp đen 0.4",
         eye="the driver looks down at the phone screen in his hands, then lifts his eyes and stares out of the windscreen; never into the lens",
         dien="CẢNH CÂM (~3 s): xe đã dừng, tài xế ngồi một mình nhìn điện thoại (đánh giá tệ của khách), thở dài, mặt buồn rười rượi, nhìn ra kính trước.",
         cuoi="Tài xế buông điện thoại xuống đùi, mắt buồn nhìn ra trước; miệng khép.",
         act="the driver stares at the phone screen, his shoulders sink, he lets out a long sad breath, lowers the phone to his lap and gazes out of the windscreen"),
    dict(g="G", w="QUANLY", lang="English", start="moi", trans="chớp trắng 0.3",
         eye="the manager looks at the young driver on the right, beaming; the young driver smiles back at him; the driver on the left looks at the manager with a hopeful little smile",
         dien="Quản lý quay sang Arjun, khen rối rít, gõ bút lên bảng kẹp; Arjun cười tự mãn; tài xế đứng bên trái cười gượng hi vọng.",
         cuoi="Quản lý nhìn Arjun cười; Arjun cười tự mãn; tài xế nhìn quản lý; miệng khép.",
         act="the manager turns toward the young driver and taps his clipboard twice with his pen, proud"),
    dict(g="G", w="QUANLY", lang="English", start="noi",
         eye="the manager looks at the young driver on the right; the young driver grins at him; the driver on the left stares at the keys",
         dien="Quản lý rút chùm chìa khoá từ túi áo vest, giơ lên trước mặt Arjun ở chữ 'brand new car'; tài xế bên trái sững lại.",
         cuoi="Quản lý giơ chùm chìa khoá về phía Arjun; Arjun cười rạng rỡ; tài xế đứng sững; miệng khép.",
         act="the manager takes {{DAO_CHIA_KHOA}} out of his jacket pocket and holds them up toward the young driver on 'brand new car'"),
    dict(g="K", w=None, start="moi", keep=2.5,
         eye="no face in focus; the hands meet in the middle of the frame",
         dien="CẢNH CÂM (~2,5 s): cận tay quản lý thả chùm chìa khoá vào lòng bàn tay Arjun, các ngón tay khép lại nắm chặt; đồng nghiệp mờ phía sau vỗ tay.",
         cuoi="Bàn tay Arjun nắm chặt chùm chìa khoá; tay quản lý rút ra.",
         act="the older hand lowers the keys and lets them drop into the younger open palm; the fingers close firmly around them; the older hand pulls back; the blurred co-workers behind clap"),
    dict(g="X", w=None, start="moi", keep=2,
         eye="the manager and the young driver look at the new taxi, smiling; never into the lens",
         dien="CẢNH CÂM (~2 s): toàn cảnh chiếc taxi vàng mới bóng loáng trong gara; quản lý và Arjun đứng sau cười, đồng nghiệp vỗ tay.",
         cuoi="Chiếc taxi mới đứng yên; mọi người cười.",
         act="the co-workers clap, the manager and the young driver smile proudly at the new taxi; the taxi and the camera stay still"),
    dict(g="J", w="ARJUN", lang="English", start="moi",
         eye="the young driver looks LEFT at the driver, smirking; the driver looks back at him, hurt, mouth closed",
         dien="Arjun lắc lắc chùm chìa khoá trước mặt tài xế, nhếch mép chế giễu: 'muốn xe mới thì học nói chuyện với khách trước đi'; tài xế nhìn Arjun, buồn, miệng khép.",
         cuoi="Arjun nhếch mép cười, chìa khoá trong tay; tài xế nhìn Arjun buồn bã; miệng khép.",
         act="the young driver jingles {{DAO_CHIA_KHOA}} once at waist height and tilts his head with a mocking smirk"),
    dict(g="T", w=None, start="moi", keep=3,
         eye="the driver looks down at the floor, then lifts his eyes slightly to the right, hurt; never into the lens",
         dien="CẢNH CÂM (~3 s): cận tài xế đứng một mình, cúi mặt, buồn, nuốt khan, mắt hơi ngấn nước.",
         cuoi="Tài xế cúi mặt buồn; miệng khép.",
         act="the driver lowers his eyes, swallows hard, his moustache trembles slightly and his eyes glisten; he stays where he is"),
    dict(g="L", w="CON", lang="Spanish", start="moi", trans="chớp trắng 0.3",
         eye="the girl looks at her father on the left, worried; the father keeps looking down",
         dien="Tối ở nhà: con gái đứng phía sau, cầm cốc, thấy bố ngồi buồn, bước lên một bước hỏi han.",
         cuoi="Con gái nhìn bố lo lắng, cầm cốc; bố cúi mặt; miệng khép.",
         act="the girl takes one small step forward holding the mug and tilts her head, worried"),
    dict(g="L", w="HOC", lang="Spanish", start="noi",
         eye="the father keeps his eyes down at the floor; the girl looks at him",
         dien="Bố không ngẩng lên, đáp khẽ cho qua.",
         cuoi="Bố cúi mặt; con gái nhìn bố; miệng khép.",
         act="the father gives a tiny shake of the head without looking up"),
    dict(g="L", w="HOC", lang="Spanish", start="noi",
         eye="the father lifts his eyes a little toward the girl on the right, sad; the girl looks at him",
         dien="Bố thở dài, kể hôm nay lại không hiểu khách nói gì.",
         cuoi="Bố nhìn con gái, buồn; con gái nhìn bố thương cảm; miệng khép.",
         act="the father sighs and rubs his hands together slowly on his knees"),
    dict(g="L2", w="CON", lang="Spanish", start="moi",
         eye="the girl looks at her father on the left, encouraging; the father looks down at his hands",
         dien="Con gái đã ngồi xuống cạnh bố, mỉm cười động viên.",
         cuoi="Con gái mỉm cười nhìn bố; bố nhìn xuống tay; miệng khép.",
         act="the girl leans her shoulder gently toward her father with a warm smile"),
    dict(g="L2", w="CON", lang="Spanish", start="noi",
         eye="the girl looks at her father on the left; the father turns his head and looks at her",
         dien="Con gái nói tiếp, nghiêng đầu cười; bố quay sang nhìn con.",
         cuoi="Bố nhìn con gái; con gái mỉm cười; miệng khép.",
         act="the girl nods encouragingly as she speaks"),
    dict(g="L2", w="HOC", lang="Spanish", start="noi",
         eye="the father looks at the girl on the right, puzzled; the girl looks back at him",
         dien="Bố nhíu mày tò mò: con đang luyện nói với ai vậy?",
         cuoi="Bố nhìn con gái tò mò; miệng khép.",
         act="the father raises his eyebrows, curious"),
    dict(g="L2", w="CON", lang="Spanish", start="noi",
         eye="the girl looks at the phone, then at her father on the left; the father looks at the phone",
         dien="Con gái lấy điện thoại từ túi áo pyjama, giơ màn hình về phía bố; bố nhìn màn hình.",
         cuoi="Con gái giơ điện thoại về phía bố, tay kia cầm cốc; bố nhìn màn hình; miệng khép.",
         act="holding the mug in her left hand, the girl pulls {{DAO_DIEN_THOAI}} out of her pajama pocket with her right hand and turns the screen toward her father"),
    dict(g="PH", w=None, start="moi", keep=2,
         eye="no face in the shot; the finger points at the robot on the screen",
         dien="CẢNH CÂM (~2 s): cận điện thoại, màn hình là robot gia sư trắng thân thiện, ngón tay con gái chỉ vào màn hình.",
         cuoi="Ngón tay chạm gần màn hình; điện thoại đứng yên.",
         act="the index finger moves in and points at the friendly robot face on the screen, tapping the air near it once; the phone stays steady"),
    dict(g="L3", w="CON", lang="Spanish", start="moi",
         eye="the girl looks at her father on the left, excited; the father looks at the phone screen",
         dien="Con gái hào hứng: như nói chuyện với giáo viên thật; bố nhìn chăm chú màn hình.",
         cuoi="Con gái cười nhìn bố; bố nhìn màn hình; miệng khép.",
         act="the girl smiles brightly and tilts the phone a little more toward him"),
    dict(g="L3", w="CON", lang="Spanish", start="noi",
         eye="the girl looks at the phone, then at her father; the father looks at the screen, interested",
         dien="Con gái chỉ vào màn hình giải thích: sửa lỗi khi mình nói, luyện hội thoại đời thực.",
         cuoi="Con gái nhìn bố; bố nhìn màn hình, tò mò; miệng khép.",
         act="the girl taps the edge of the phone with her left index finger as she explains"),
    dict(g="L3", w="HOC", lang="Spanish", start="noi",
         eye="the father looks at the girl on the right, doubtful; the girl looks at him",
         dien="Bố ngập ngừng, lo: học tiếng Anh đắt lắm.",
         cuoi="Bố nhìn con gái, lo lắng; miệng khép.",
         act="the father leans back a little and shakes his head slowly"),
    dict(g="L3", w="CON", lang="Spanish", start="noi",
         eye="the girl looks at her father on the left, confident; the father looks at her",
         dien="Con gái cười, lắc đầu: không cần đi học lớp; đưa điện thoại hẳn cho bố.",
         cuoi="Con gái đặt điện thoại vào tay bố; bố cầm điện thoại nhìn con; miệng khép.",
         act="the girl smiles, shakes her head and places the phone into her father's hand"),
]

HEAD = """[HAU KY]:
loai: taxi-gia-su-ai

[GHI CHU]:
Thể loại "tài xế taxi + gia sư AI" (hoạt hình 3D kể chuyện, video mẫu 0510_cartoon turn car_015_1, 95 giây): MỘT dự án HAI phần, Studio chạy bằng code riêng
app/production/types/taxi-gia-su-ai/gen.py (logic chung types/_chung/nhieu_phan.py).
  PHẦN 1 (cảnh thường, {N_CANH} cảnh, {N_CAM} cảnh KHÔNG LỜI): tài xế taxi Mexico (HOC) không hiểu khách (KHACH) -> đánh giá tệ; ở gara quản lý (QUANLY) trao xe mới cho Arjun (ARJUN),
         Arjun chế giễu; về nhà con gái (CON) chỉ app gia sư AI trên điện thoại. Mỗi cảnh có lời một người nói; cảnh đổi góc có "Prompt ảnh", cảnh cùng góc liền sau nối khung cuối.
         Cảnh KHÔNG LỜI: lượt của biến thể có "text": "[KHONG LOI]" (gen.py đổi thành rỗng -> engine gen clip câm; "Cắt còn: N" giữ N giây đầu).
         Góc: A (taxi qua kính chắn gió), P (tài xế nhìn điện thoại), G (gara 3 người), K (cận chìa khoá), X (taxi mới), J (hai người đối mặt, Arjun nói),
         T (cận tài xế buồn), L (phòng khách rộng), L2 (sofa hai bố con), PH (cận điện thoại có robot), L3 (sofa, con gái cầm điện thoại).
  PHẦN 2 (ghép 2 lớp, mỗi lượt một cảnh): tài xế (HOC) toàn khung trong taxi, nhìn ống kính (điện thoại trên taplo); robot gia sư AI (DAY) trong ô ngang bo góc viền trắng
         phía trên (x 0.135, y 0.03, rộng 0.73, cao 0.28 -> gen 16:9). Vào phần 2 bằng nhoè chuyển động 0,5 giây. Cặp sửa lỗi "I am Mexico" -> "I am from Mexico".
  BẮT BUỘC ảnh tham chiếu (refs) cho HOC, KHACH, QUANLY, ARJUN, CON, DAY: nhiều góc máy.
  Hậu kỳ riêng (post.py, config.json): phần 1 phụ đề ô trắng chữ đen + dòng dịch; phần 2 chữ vàng viền đen. End card app: Thương hiệu -> Outro, không gen.
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.

===== PHAN 1: TAXI, GARA, PHONG KHACH =====

[STYLE LOCK]:
Vertical 9:16 Pixar-style 3D CARTOON exactly like the character reference images: cartoon proportions, big round expressive eyes, simplified smooth features, soft rounded shapes, warm glowing skin, rich detail; never photorealistic or semi-realistic human faces. Every shot is one fixed camera that never pans, zooms or reframes inside a clip (in the taxi driving shots, CAMERA ANGLE A, the camera is fixed to the front of the moving taxi). Each clip uses the camera angle described in its start frame. The same characters (each only in the shots that name them) in every clip. No text, no letters, no numbers, no logos, no captions, no icons, no lettering on the taxi, roof light, clothes, signs, clipboard, paper or phone screens anywhere in the frame.

[CHAR LOCK]:
CHARACTERS: each person appears ONLY in the shots whose CAMERA ANGLE names them; a close-up shows only its one person, and nobody else is ever added behind or beside them.
The {{VAI_HOC}}, {{TEN_HOC}}: {{NGUOI_HOC}}. VOICE LOCK DRIVER: one single voice, {{GIONG_HOC}}, the same in every clip.
The {{VAI_KHACH}}, {{TEN_KHACH}}: {{NGUOI_KHACH}}. VOICE LOCK PASSENGER: one single voice, {{GIONG_KHACH}}, the same in every clip.
The {{VAI_QUANLY}}, {{TEN_QUANLY}}: {{NGUOI_QUANLY}}. VOICE LOCK MANAGER: one single voice, {{GIONG_QUANLY}}, the same in every clip.
The {{VAI_ARJUN}}, {{TEN_ARJUN}}: {{NGUOI_ARJUN}}. VOICE LOCK YOUNG DRIVER: one single voice, {{GIONG_ARJUN}}, the same in every clip.
The {{VAI_CON}}, {{TEN_CON}}: {{NGUOI_CON}}. VOICE LOCK GIRL: one single voice, {{GIONG_CON}}, the same in every clip.
When a character who is in the shot is silent: the driver {{NGHE_HOC}}; the passenger {{NGHE_KHACH}}; the manager {{NGHE_QUANLY}}; the young driver {{NGHE_ARJUN}}; the girl {{NGHE_CON}}.
RULE: in each clip with a line exactly ONE character speaks, one line, with lip-sync and an expressive face, keeping the EYE LINE. Anyone else in the frame stays silent with the mouth closed. Each voice stays the same in every clip.
EYE LINE (every clip): the speaker looks where the clip's EYE LINE says for the whole line; listeners look at the speaker unless the EYE LINE says otherwise. Nobody looks into the lens.
ACTION CLIPS: a physical action is done WHILE the line is spoken and is complete by the last word. Props, the same in every clip: {{DAO_DIEN_THOAI_KH}}, {{DAO_DIEN_THOAI_TX}}, {{DAO_CHIA_KHOA}}, {{DAO_COC}}, {{DAO_DIEN_THOAI}}; each appears only when a clip shows it, never duplicated, never with readable text.

[SET LOCK]:
The taxi: {{XE}}. Outside: {{NEN_PHO}}. The garage: {{NEN_GARA}}. At home: {{NEN_NHA}}. A shot shows ONLY the people its CAMERA ANGLE names; people far in the background are small, blurred and stand still. Nothing moves in the background (no passing cars, no walking people) EXCEPT in the taxi driving shots (CAMERA ANGLE A): there the taxi is driving and the city outside streams continuously past its windows.

[VIDEO SUFFIX]:
Static camera, no zoom, no pan, no shake, no cut. Real people caught on camera, not actors. No subtitles, no text, no music. 9:16. In a clip with a line, the speaker starts right away at a natural, quick conversational pace (about 3.5 words per second, short lines up to 4.5, short pauses allowed), finishes the line and then, after the last word and the action, everyone keeps a calm closed-mouth face and stays still until the end of the clip, with no traffic noise over the voice.

[NEGATIVE]:
text, captions, subtitles, logos, icons, emoji, numbers, lettering on the taxi, roof light, clothes, clipboard, signs, paper or phone; app interface, buttons or chat bubbles on a phone screen; camera movement, zoom, shake, cut; two voices in one clip; a silent character moving the mouth; a character who is not in this shot appearing; extra people in the foreground; moving crowds in the garage or at home; face, hair or outfit changing; realistic live-action look; photorealistic or semi-realistic faces; one character copying another's movements; background music; robotic or text-to-speech voice for the humans; a clip with a line but no speech; movement during the final still after the speech; props multiplying, vanishing or appearing in the wrong clip; slow, dragged speech.
"""

PART2 = """
===== PHAN 2: TAI XE + GIA SU AI (GHEP 2 LOP) | vao: nhoe 0.5 =====

[GHEP HAI LOP]:
nen: HOC
khung DAY: 0.135, 0.03, 0.73, 0.28
bo goc: 0.05
vien: #FFFFFF, 3
nghe: moi canh

[STYLE LOCK]:
Vertical short-form video look, stylized Pixar-style 3D animated feature-film characters (soft rounded shapes, big expressive eyes, warm glowing skin), crisp focus on the face, warm sunny afternoon light. No text, captions, logos, icons or watermarks anywhere in the frame.

[NHAN VAT DAY]:
{{TEN_DAY}}: {{NGUOI_DAY}}. Framed for a wide call-window: head, neck and the top of the shoulders centred in the middle of the frame, facing the camera, clear space above the head, no arms or hands in the frame, a little empty space on both sides, in front of {{NEN_DAY}}. The camera is locked off and never moves. BODY LOCK: the shoulders and the chest stay fixed in exactly the same place in every frame; the body never slides sideways, sways, rises, sinks or turns, and the head stays upright and centred (at most a tiny nod); only the face moves: eyes, eyelids, eyebrows and lips. VOICE: {{GIONG_DAY}}, the same timbre, pitch and loudness in every clip.

[NGHE DAY]:
{{TEN_DAY}} listens to the person on the other end of the call: soft attentive smile, slow natural blinks, facing the camera; the head and body stay still and centred exactly as in the start frame, no head tilt, no sway, no sliding. Lips stay sealed.

[NHAN VAT HOC]:
{{TEN_HOC}}: {{NGUOI_HOC}}, alone in the driver's seat of the taxi, the seat belt across his chest. Seen from a phone mounted on the dashboard in front of him, chest-up, centred, both hands on the steering wheel at the bottom of the frame; his head is LOW in the frame: the top of his curly hair at about 38% down from the top edge, his face in the middle of the frame; the upper 35% of the frame shows only the taxi's roof lining and the rear window with no part of his head (it is covered later by a call window). Behind him: {{NEN_HOC}}. The seat beside him and the back seat are empty. He looks into the lens while speaking, as if talking to the phone. Small natural head movements only, no cuts, no zoom. VOICE: {{GIONG_HOC}}, the same timbre, pitch and loudness in every clip.

[NGHE HOC]:
{{TEN_HOC}} listens to the phone on the dashboard: eyes on the lens, friendly attentive expression, slow blinks, a small nod now and then, both hands on the steering wheel. Lips stay sealed.

[VIDEO SUFFIX]:
Natural spontaneous conversational delivery, not text-to-speech, clear (about 3.5 words per second, short lines faster), the line starts right away, light natural breaths, a smile audible in the voice when the line is positive. Clean voice only, no music, no traffic noise, no echo.

[NEGATIVE]:
text, letters, captions, subtitles, logos, icons, watermark; phone screen or app interface in the frame; camera cuts, zoom, push-in, shake; a second person; face morphing, outfit change, age or style drift; realistic live-action look; distorted face; extra or missing fingers; jerky or exaggerated gestures; slow, dragged or stretched speech; flat monotone or robotic voice for the driver; background music; echo or reverb
"""

IMG = "Generate exactly one still image now, vertical 9:16, Pixar-style 3D animated feature-film look exactly like the character reference images, {light}. {body} EYE LINE: {eye}. Mouths closed, natural expressions. No text, no logos, no numbers, no lettering anywhere. Output only the image."


def names(keys):
    return " and ".join("{{TEN_%s}}" % k for k in keys)


def only_line(g, people):
    if g == "K":
        return "Only two hands (an older man's hand in a navy suit sleeve and a younger man's hand with a silver wristwatch) are in focus in this clip; no face in focus."
    if g == "PH":
        return "Only the girl's hands and the phone are in this clip; no face, nobody else ever appears."


    return f"Only {names(people)} {'is' if len(people) == 1 else 'are'} in this clip" + ("; the co-workers far behind stay small, blurred and still." if g in ("G", "X") else "; nobody else ever appears.")


def mute_scene(n, s, a, b):
    """Cảnh KHÔNG LỜI: biến thể đặt "text": "[KHONG LOI]"; gen.py đổi thành rỗng -> {{LUOT_n}} rỗng, engine tạo clip câm (mute_prompt).
    Mô tả không dùng các từ say/speak/talk/voice/lời/nói/giọng (engine lọc bỏ cả câu chứa chúng)."""
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
    lock = ("CAMERA LOCK: the camera is locked off on this close shot for the whole clip: no pan, no zoom out, no reframing."
            if close else "LOCKED CAMERA on a tripod: no pan, no tilt, no zoom; the framing of the start frame stays the same to the last frame.")
    vid = (f"STYLE LOCK, SET LOCK. {start} {only_line(s['g'], people)} {lock} CHAR LOCK. {{{{LUOT_{n}}}}} "
           f"EYE LINE for the whole clip: {s['eye'].replace('LEFT', 'left').replace('RIGHT', 'right')}. "
           f"ACTION, from the first frame to the last: {s['act']}. Mouths closed. "
           f"Only the quiet natural sound of the place and of the action, no music. VIDEO SUFFIX.")
    lines.append("Prompt video: " + vid)
    lines.append("Audio: Không lời. Chỉ tiếng động tự nhiên của nơi đó và của hành động; không nhạc.")
    neg = "text or captions; camera movement; a character not in this shot appearing; anyone moving the lips as if forming words; music"
    if close:
        neg += "; anyone else added behind or beside the person"
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
    s = dict(s, eye=s["eye"].replace("LEFT", "left").replace("RIGHT", "right"))   # từ vị trí viết hoa trong Prompt video từng bị Muse vẽ thành chữ
    lines = [f"CẢNH {n} ({a // 60}:{a % 60:02d}–{b // 60}:{b % 60:02d}): Lượt {n}"]
    noi = s["start"] == "noi"
    lines.append(f"Bối cảnh: {vn}; không có chữ, không người lạ." + (" Nối từ khung cuối cảnh trước." if noi else ""))
    lines.append(f"Voice: ({s['lang'].split(' (')[0]}, chỉ một người nói trong clip này) {{{{LUOT_{n}}}}}")
    lines.append("Khung đầu: Chính là khung cuối của cảnh trước." if noi else f"Khung đầu: ảnh mới theo góc {s['g']}; miệng mọi người khép.")
    lines.append(f"Khung cuối: {s['cuoi']} Mọi người đứng im đến hết clip.")
    lines.append(f"Hướng nhìn: {s['eye']}.")
    lines.append(f"Diễn biến: {s['dien']} Nói xong mọi người đứng im đến hết clip.")
    if not noi:
        lines.append("Prompt ảnh: " + IMG.format(light=light, body=body, eye=s["eye"]))
    start = ("Start exactly from the provided start frame (the last frame of the previous clip) and continue from it with no cut or reset."
             if noi else "Start exactly from the start-frame image and keep its camera angle.")
    lock = ("CAMERA LOCK: the camera is locked off on this close shot for the whole clip: no pan, no zoom out, no reframing."
            if close else "LOCKED CAMERA on a tripod: no pan, no tilt, no zoom; the framing of the start frame stays the same to the last frame.")
    if s["g"] == "A" and s["w"] != "HOC":   # 12/11: tài xế nghe bắt chước cử chỉ khách (giơ tay, quay đầu): khoá thân/đầu
        s = dict(s, act=s["act"] + "; the driver does NOT copy the passenger: he keeps both hands on the wheel and his head and body fixed facing forward, only his eyes and eyebrows move")
    if s["g"] == "A" and s["w"] == "HOC":
        s = dict(s, act=s["act"] + "; the passenger stays seated far back in the back seat, phone at his ear, and does not lean forward or move closer to the camera")
    if s["g"] == "A":   # người dùng 12/11: xe phải rõ là đang chạy (cảnh vật ngoài kính trôi), máy gắn trên xe nên khung giữ nguyên
        lock = ("MOVING TAXI, CAR-MOUNTED CAMERA: the camera is rigidly fixed to the front of the taxi, so the cab and both men keep exactly the framing of the start frame "
                "to the last frame; but the taxi is DRIVING forward at steady city speed for the whole clip: through the side windows, the rear window and above the roof the city "
                "streams past continuously from front to back (brick buildings, shop fronts, trees, lamp posts and parked yellow cabs sliding by), with gentle road vibration "
                "and bands of sunlight and shadow sweeping across the two men.")
    vid = (f"STYLE LOCK, SET LOCK. {start} {only_line(s['g'], people)} {lock} CHAR LOCK. In this clip: {{{{LUOT_{n}}}}} Only that character speaks, with lip-sync and an expressive face. "
           f"LANGUAGE of this line: {s['lang']}. EYE LINE for the whole clip: {s['eye']}; the speaker never turns the head away from where the EYE LINE says while talking. "
           f"Anyone else in the shot keeps the mouth closed. Natural quick pace, about 3.5 words per second. "
           f"ACTION, done WHILE the line is spoken: {s['act']}. After the line and the action everyone stays still until the end. Same voices as always, clean dry sound, no music. VIDEO SUFFIX.")
    lines.append("Prompt video: " + vid)
    lines.append("Audio: Chỉ giọng của một nhân vật, rõ, gần; phần còn lại im lặng. Không nhạc, không tiếng xe cộ đè lên giọng.")
    neg = "two voices; a silent character moving the mouth; text or captions; camera movement; a character not in this shot appearing; no speech"
    if close:
        neg += "; anyone else added behind or beside the person"
    if s["g"] == "A":
        neg += "; a cut to another camera angle; the passenger moving to another seat; a parked or stopped taxi; a frozen street outside the windows"
    lines.append("Negative prompt: " + neg + ".")
    if isinstance(s["start"], int):
        lines.append(f"Khung đầu từ cảnh: {s['start']}")
    if s.get("trans"):
        lines.append(f"Chuyển cảnh: {s['trans']}")
    return "\n".join(lines)


def main():
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
    open(OUT, "w", encoding="utf-8").write("\n\n".join(parts) + "\n" + PART2)
    print(f"Đã ghi {os.path.normpath(OUT)}: phần 1 {len(S)} cảnh ({n_cam} không lời) + phần 2 ghép 2 lớp")
    print("Người nói phần 1:", " ".join((s["w"] or "-").lower() for s in S))


if __name__ == "__main__":
    main()
