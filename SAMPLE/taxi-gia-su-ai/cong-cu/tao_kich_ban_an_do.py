"""Sinh KICH-BAN-TAXI-AN-DO.txt: bản Ấn Độ (Mumbai, tiếng Anh + Hindi) theo lời của sheet "X0061_20 biến thể lái xe taxi IN" (13/11/2026).
  runtime\\python.exe SAMPLE\\taxi-gia-su-ai\\cong-cu\\tao_kich_ban_an_do.py
Dùng lại hàm dựng cảnh của tao_kich_ban.py (bản Mexico/New York đã kiểm chứng), chỉ thay bảng góc + bảng cảnh + khối khoá:
  PHẦN 1 cảnh thường 20 cảnh (5 KHÔNG LỜI): taxi (6) -> câm P -> bến xe: sếp khen Arjun, trao xe mới; tài xế xin xe (Hindi), sếp mỉa -> câm T
          -> nhà: Priya hỏi, bố kể (Hindi), Priya giới thiệu Ava AI -> câm PH.
  PHẦN 2 ghép 2 lớp: tài xế + robot Ava ở ô ngang trên (giống bản Mexico), cặp sửa lỗi "I am India" -> "I am from India".
  PHẦN 3 cảnh thường 2 cảnh (cảnh 5 kết của sheet): tài xế tự tin chào khách bằng tiếng Anh, rồi nói câu Hindi.
Bố cục góc A giữ như bản đã duyệt (tài xế to bên PHẢI, khách nhỏ ghế sau bên TRÁI, máy gắn đầu xe, phố trôi).
Bài học bản Mexico đưa vào đây: không nối khung chuỗi ở góc A (mọi cảnh A dùng Khung đầu từ cảnh 1); khách chỉ cử chỉ nhỏ, tay trống để trên đùi
(Muse gán hành động người nói nhỏ cho người nghe to); đèn mui không chữ."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tao_kich_ban as TK  # noqa: E402

OUT = os.path.join(HERE, "..", "KICH-BAN-TAXI-AN-DO.txt")

DAY = "bright warm late-afternoon sunlight on a busy Mumbai street"
GARA = "warm white tube lights inside an Indian taxi depot mixed with daylight from the wide open shutter"
NHA = "soft natural daylight through light cotton curtains in a cosy Indian apartment living room"

ANG = {
    "A": ("góc A: nhìn qua kính chắn gió từ trên nắp capô taxi đen-vàng: tài xế bên PHẢI cầm vô lăng (ngực trở lên); khách nữ ngồi ghế sau bên TRÁI, nhỏ hơn, áp điện thoại vào tai; phố Mumbai đông, xe chạy",
          DAY,
          "CAMERA ANGLE A, medium shot looking into a black-and-yellow Mumbai taxi through its clean windscreen from just above the glossy black bonnet (the black bonnet fills the bottom fifth of the frame, the yellow roof at the top): "
          "{{TEN_HOC}} ({{NGUOI_HOC}}) sits behind the steering wheel on the RIGHT half, chest-up, both hands on the wheel; in the back seat on the LEFT, smaller and further away, "
          "{{TEN_KHACH}} ({{NGUOI_KHACH}}) sits upright holding {{DAO_DIEN_THOAI_KH}} to her ear; above the taxi roof and through the rear window {{NEN_PHO}}; there is no roof sign and nothing written anywhere on the taxi. "
          "The taxi is DRIVING forward down the street: the street outside the side windows, the rear window and above the roof slides past from front to back with a soft motion blur. "
          "ONE continuous shot exactly like the start frame for the whole clip: the passenger stays small in the back seat at the LEFT and the driver stays big at the RIGHT; the camera never cuts, never moves closer to the back seat and never reframes on whoever speaks.",
          ["HOC", "KHACH"], False),
    "P": ("góc P: trong xe đỗ, từ ghế phụ nhìn sang: tài xế ngồi ghế lái giữa-trái, nghiêng 3/4 về camera, cầm điện thoại thấp trong hai tay gần vô lăng, nhìn màn hình; cửa sổ sau lưng là phố yên tĩnh",
          DAY,
          "CAMERA ANGLE P: medium close shot from the front passenger seat inside the parked taxi: {{TEN_HOC}} ({{NGUOI_HOC}}) sits in the driver's seat at the LEFT-centre, turned three-quarters toward the camera, "
          "holding {{DAO_DIEN_THOAI_TX}} low in both hands near the steering wheel, its screen turned toward him (the camera sees only a soft glow, nothing readable); "
          "through the side window behind him a quiet Mumbai side street with old apartment buildings. He is the only person in the frame.",
          ["HOC"], True),
    "G": ("góc G: trong bến taxi, ba người đứng hàng ngang từ gối trở lên: tài xế TRÁI, sếp GIỮA cầm bảng kẹp hồ sơ, Arjun PHẢI; vài tài xế khác đứng xa phía sau, mờ, đứng yên",
          GARA,
          "CAMERA ANGLE G, medium-wide shot inside {{NEN_GARA}}: three men stand in a row facing the camera, from the knees up: {{TEN_HOC}} ({{NGUOI_HOC}}) at the LEFT, "
          "{{TEN_QUANLY}} ({{NGUOI_QUANLY}}) in the CENTRE, {{TEN_ARJUN}} ({{NGUOI_ARJUN}}) at the RIGHT; a few other taxi drivers in work clothes stand far behind them, small, blurred and still.",
          ["HOC", "QUANLY", "ARJUN"], False),
    "K": ("góc K: cận chùm chìa khoá: tay áo jacket xanh navy của sếp từ TRÁI chìa chìa khoá, bàn tay Arjun đeo đồng hồ bạc từ PHẢI đưa vào nhận; phía sau đồng nghiệp mờ vỗ tay",
          GARA,
          "CAMERA ANGLE K: close-up at chest height in the depot: from the LEFT an older man's hand in a navy-blue jacket sleeve holds out {{DAO_CHIA_KHOA}} by the ring; "
          "from the RIGHT a younger man's open palm with a silver wristwatch on the wrist reaches in under it; behind them, softly out of focus, a few co-workers in work shirts. No face is in focus.",
          ["QUANLY", "ARJUN"], True),
    "X": ("góc X: toàn cảnh bến: chiếc taxi đen-vàng mới tinh đỗ tiền cảnh bên PHẢI, đầu xe chếch về camera; phía sau sếp và Arjun đứng cạnh nhau cười, một hàng đồng nghiệp vỗ tay",
          GARA,
          "CAMERA ANGLE X, wide shot of the depot: a shiny brand-new black-and-yellow taxi with no roof sign stands in the foreground at the RIGHT, its front angled toward the camera; "
          "behind it {{TEN_QUANLY}} ({{NGUOI_QUANLY}}) and {{TEN_ARJUN}} ({{NGUOI_ARJUN}}) stand side by side, smiling, with a short row of co-workers in work shirts; the open shutter and the street behind.",
          ["QUANLY", "ARJUN"], False),
    "M": ("góc M (như góc hai người đối mặt của video gốc): cận tài xế bên TRÁI tiền cảnh từ ngực trở lên, mặt nghiêng 3/4 quay sang PHẢI; sếp bên PHẢI quay sang TRÁI, tay cầm bảng kẹp; taxi mới mờ phía sau",
          GARA,
          "CAMERA ANGLE M, close two-shot in the depot, both men standing face to face: {{TEN_HOC}} ({{NGUOI_HOC}}) on the LEFT half in the foreground, from the chest up, his face in three-quarter view turned RIGHT toward the manager; "
          "{{TEN_QUANLY}} ({{NGUOI_QUANLY}}) on the RIGHT half, from the chest up, turned LEFT toward him, holding his clipboard against his chest; "
          "behind them the new black-and-yellow taxi and the depot, softly out of focus. Only these two people are in the frame.",
          ["HOC", "QUANLY"], True),
    "T": ("góc T: cận tài xế một mình trong bến, đầu và vai, giữa-trái, mặt hơi quay sang PHẢI, mắt nhìn xuống; taxi mờ phía sau",
          GARA,
          "CAMERA ANGLE T: close-up of {{TEN_HOC}} ({{NGUOI_HOC}}) in the depot, head and shoulders, centre-left, face turned slightly to the RIGHT of the lens, eyes down; "
          "behind him the black-and-yellow taxi and the depot, softly out of focus. He is the only person in the frame.",
          ["HOC"], True),
    "L": ("góc L: phòng khách rộng: tài xế ngồi khom trên sofa tiền cảnh TRÁI, tay chống gối, cúi mặt; con gái Priya đứng phía sau bên PHẢI gần cửa sổ, cầm cốc; bàn trà gỗ có sách mở + cốc trà góc dưới phải",
          NHA,
          "CAMERA ANGLE L, medium-wide shot of {{NEN_NHA}}: {{TEN_HOC}} ({{NGUOI_HOC}}) sits hunched on the sofa in the LEFT foreground, from the thighs up, forearms on his knees, eyes down; "
          "in the back at the RIGHT, standing near the window, {{TEN_CON}} ({{NGUOI_CON}}) holds {{DAO_COC}} in both hands; on a low wooden coffee table at the bottom right an open book and a small glass of tea. "
          "Only these two people are in the frame.",
          ["HOC", "CON"], False),
    "L2": ("góc L2: cận hai bố con ngồi sofa: bố TRÁI (ngực trở lên) hơi quay sang PHẢI; Priya ngồi sát bên PHẢI quay sang TRÁI, hai tay cầm cốc trên đùi; sau lưng cửa sổ rèm vải",
           NHA,
           "CAMERA ANGLE L2, close two-shot on the sofa: {{TEN_HOC}} ({{NGUOI_HOC}}) sits at the LEFT, from the chest up, turned slightly RIGHT toward her; {{TEN_CON}} ({{NGUOI_CON}}) sits close beside him at the RIGHT, "
           "turned LEFT toward him, holding {{DAO_COC}} in both hands on her lap; the open book and the glass of tea on the coffee table along the bottom edge; behind them the window with light cotton curtains. "
           "Only these two people are in the frame.",
           ["HOC", "CON"], True),
    "PH": ("góc PH: cận điện thoại trong tay Priya (tay áo kurta vàng mù tạt), màn hình hướng camera là robot trắng thân thiện, không chữ; ngón trỏ tay kia chỉ vào màn hình; nền phòng khách mờ",
           NHA,
           "CAMERA ANGLE PH: close-up of {{DAO_DIEN_THOAI}} held upright in a girl's right hand (a mustard-yellow kurta sleeve), the screen turned toward the camera; the index finger of her other hand points at the screen; "
           "behind, softly out of focus, the living-room rug and the coffee table. No face in the frame.",
           ["CON"], True),
    "L3": ("góc L3: như L2 nhưng cốc đã đặt lên bàn; Priya cầm điện thoại bằng tay phải, màn hình (robot, không chữ) xoay về phía bố; bố cúi nhìn màn hình",
           NHA,
           "CAMERA ANGLE L3, close two-shot on the sofa: {{TEN_HOC}} ({{NGUOI_HOC}}) sits at the LEFT, from the chest up, leaning slightly RIGHT toward the phone; {{TEN_CON}} ({{NGUOI_CON}}) sits close beside him at the RIGHT, "
           "holding {{DAO_DIEN_THOAI}} in her right hand at chest height with the screen turned toward him; {{DAO_COC}} stands on the coffee table along the bottom edge next to the open book; "
           "behind them the window with light cotton curtains. Only these two people are in the frame.",
           ["HOC", "CON"], True),
    # phần 3 (kết): cùng bố cục góc A, tài xế tự tin; cận tài xế trong xe
    "T3": ("góc T3: cận tài xế trong taxi đang chạy, từ ngực trở lên, giữa khung, hai tay trên vô lăng, mỉm cười tự tin nhìn đường (lệch khỏi ống kính); phố Mumbai trôi sau kính",
           DAY,
           "CAMERA ANGLE T3: medium close-up through the windscreen of the moving black-and-yellow taxi: {{TEN_HOC}} ({{NGUOI_HOC}}) alone in the front, from the chest up, centred, both hands on the steering wheel, "
           "looking ahead at the road just past the lens with a calm proud smile; the back seat behind him is empty; through the side and rear windows {{NEN_PHO}}. He is the only person in the frame.",
           ["HOC"], True),
}

MK = None
ANH_SANG = "the passenger, phone held at her ear in one hand, "

S = [
    dict(g="A", w="KHACH", lang="English (fluent, refined Indian accent)", start="moi",
         eye="the passenger looks forward at the back of the driver's head, the phone at her ear; the driver looks ahead at the road, just past the lens",
         dien="Khách ngồi sau, điện thoại áp tai, chồm nhẹ tới trước nhờ tài xế rẽ trái; tài xế nhìn đường, nghe.",
         cuoi="Khách ngồi lại, điện thoại vẫn áp tai, tay trống trên đùi; tài xế hai tay trên vô lăng, ngơ ngác; miệng khép.",
         act=ANH_SANG + "leans forward a little toward the driver, gives one small nod toward the road ahead with her head only, then sits back; her free hand rests on her lap the whole time"),
    dict(g="A", w="HOC", lang="English (very broken, heavy Indian accent)", start=1,
         eye="the driver glances up toward the rear-view mirror at the passenger, confused, then back at the road; the passenger frowns at him",
         dien="Tài xế ngập ngừng lặp lại 'Fifth?', nhíu mày, xin lỗi vì không hiểu; hai tay vẫn trên vô lăng.",
         cuoi="Tài xế nhìn đường, lúng túng; khách cau mày; miệng khép.",
         act="the driver frowns, raises his eyebrows and gives a small apologetic shake of the head, both hands staying on the wheel"),
    dict(g="A", w="KHACH", lang="English (fluent, refined Indian accent)", start=1,
         eye="the passenger looks forward at the driver, annoyed; the driver looks ahead at the road, worried",
         dien="Khách gắt: rẽ trái! Xe đã qua chỗ rẽ.",
         cuoi="Khách ngồi yên ghế sau, điện thoại áp tai, nhìn tài xế bực; tài xế nhìn đường, lo; miệng khép.",
         act=ANH_SANG + "frowns, raises her eyebrows in disbelief and gives one annoyed small shake of the head; her free hand rests on her lap; nobody turns around"),
    dict(g="A", w="KHACH", lang="English (fluent, refined Indian accent)", start=1,
         eye="the passenger glares at the back of the driver's head; the driver keeps his eyes on the road, embarrassed",
         dien="Khách bực, nâng nhẹ bàn tay rồi hạ xuống.",
         cuoi="Khách ngồi tựa lưng ghế, điện thoại áp tai, tay trống trên đùi; tài xế cúi mặt nhìn đường; miệng khép.",
         act=ANH_SANG + "lifts her free open hand a little toward the driver in annoyance, then lowers it to her lap and settles back against the seat"),
    dict(g="A", w="KHACH", lang="English (fluent, refined Indian accent)", start=1,
         eye="the passenger looks out of the side window beside her at the LEFT edge of the frame, talking into the phone; the driver looks ahead at the road, sad",
         dien="Khách quay sang nói vào điện thoại với người bên kia, chê tài xế không biết tiếng Anh; tài xế nghe thấy, buồn.",
         cuoi="Khách nhìn ra cửa sổ, điện thoại áp tai; tài xế buồn; miệng khép.",
         act=ANH_SANG + "turns her head toward the side window and speaks into the phone with a tired sigh"),
    dict(g="A", w="KHACH", lang="English (fluent, refined Indian accent)", start=1,
         eye="the passenger looks out of the side window beside her at the LEFT edge of the frame, talking into the phone; the driver looks ahead at the road, sad",
         dien="Khách thở dài với người trong điện thoại; tài xế mím môi, cúi mắt.",
         cuoi="Khách nhìn ra cửa sổ; tài xế cúi mắt nhìn vô lăng, buồn; miệng khép.",
         act=ANH_SANG + "rolls her eyes and lets out a tired sigh, her free hand resting on her lap; no hand touches any face"),
    dict(g="P", w=None, start="moi", keep=3, trans="chớp đen 0.4",
         eye="the driver looks down at the phone screen in his hands, then lifts his eyes and stares out of the windscreen; never into the lens",
         dien="CẢNH CÂM (~3 s): xe đã dừng, tài xế ngồi một mình nhìn điện thoại (đánh giá tệ của khách), thở dài, mặt buồn, nhìn ra kính trước.",
         cuoi="Tài xế buông điện thoại xuống đùi, mắt buồn nhìn ra trước; miệng khép.",
         act="the driver stares at the phone screen, his shoulders sink, he lets out a long sad breath, lowers the phone to his lap and gazes out of the windscreen"),
    dict(g="G", w="QUANLY", lang="English (warm Indian accent)", start="moi", trans="chớp trắng 0.3",
         eye="the manager looks at the young driver on the right, beaming; the young driver smiles back at him; the driver on the left looks at the manager with a hopeful little smile",
         dien="Sếp quay sang Arjun, khen, gõ bút lên bảng kẹp; Arjun cười tự mãn; tài xế đứng bên trái cười gượng hi vọng.",
         cuoi="Sếp nhìn Arjun cười; Arjun cười tự mãn; tài xế nhìn sếp; miệng khép.",
         act="the manager turns toward the young driver and taps his clipboard twice with his pen, proud"),
    dict(g="G", w="QUANLY", lang="English (warm Indian accent)", start="noi",
         eye="the manager looks at the young driver on the right; the young driver grins at him; the driver on the left stares at the keys",
         dien="Sếp rút chùm chìa khoá từ túi áo, giơ lên trước mặt Arjun ở chữ 'brand-new car'; tài xế bên trái sững lại.",
         cuoi="Sếp giơ chùm chìa khoá về phía Arjun; Arjun cười rạng rỡ; tài xế đứng sững; miệng khép.",
         act="the manager takes {{DAO_CHIA_KHOA}} out of his jacket pocket and holds them up toward the young driver on 'brand-new car'"),
    dict(g="K", w=None, start="moi", keep=2.5,
         eye="no face in focus; the hands meet in the middle of the frame",
         dien="CẢNH CÂM (~2,5 s): cận tay sếp thả chùm chìa khoá vào lòng bàn tay Arjun, các ngón tay khép lại nắm chặt; đồng nghiệp mờ phía sau vỗ tay.",
         cuoi="Bàn tay Arjun nắm chặt chùm chìa khoá; tay sếp rút ra.",
         act="the older hand lowers the keys and lets them drop into the younger open palm; the fingers close firmly around them; the older hand pulls back; the blurred co-workers behind clap"),
    dict(g="X", w=None, start="moi", keep=2,
         eye="the manager and the young driver look at the new taxi, smiling; never into the lens",
         dien="CẢNH CÂM (~2 s): toàn cảnh chiếc taxi đen-vàng mới bóng loáng trong bến; sếp và Arjun đứng sau cười, đồng nghiệp vỗ tay.",
         cuoi="Chiếc taxi mới đứng yên; mọi người cười.",
         act="the co-workers clap, the manager and the young driver smile proudly at the new taxi; the taxi and the camera stay still"),
    dict(g="M", w="HOC", lang="Hindi (natural Hinglish: the English word 'car' said the Indian way)", start="moi",
         eye="the driver looks RIGHT at the manager, hopeful and a little shy; the manager looks back at him, unimpressed",
         dien="Tài xế rụt rè xin sếp: tôi cũng muốn xe mới; sếp nhìn anh, không mấy thiện cảm.",
         cuoi="Tài xế nhìn sếp chờ đợi; sếp nhìn tài xế lạnh nhạt; miệng khép.",
         act="the driver clasps his hands together in front of his chest, a small hopeful gesture; the manager keeps his clipboard against his chest and does not move"),
    dict(g="M", w="QUANLY", lang="English (warm Indian accent, now cool and dismissive)", start="noi",
         eye="the manager looks LEFT at the driver with a cool, slightly mocking look; the driver looks back at him, hurt, mouth closed",
         dien="Sếp nhìn tài xế, mỉa: muốn xe mới thì học nói chuyện với khách trước đi; tài xế lặng người.",
         cuoi="Sếp quay đi nửa người, bảng kẹp trên ngực; tài xế nhìn sếp buồn bã; miệng khép.",
         act="the manager raises one eyebrow and tilts his head with a cool little smile; the driver does NOT copy him: his hands drop to his sides and he stays still"),
    dict(g="T", w=None, start="moi", keep=3,
         eye="the driver looks down at the floor, then lifts his eyes slightly to the right, hurt; never into the lens",
         dien="CẢNH CÂM (~3 s): cận tài xế đứng một mình, cúi mặt, buồn, nuốt khan, mắt hơi ngấn nước.",
         cuoi="Tài xế cúi mặt buồn; miệng khép.",
         act="the driver lowers his eyes, swallows hard and his eyes glisten; he stays where he is"),
    dict(g="L", w="CON", lang="Hindi", start="moi", trans="chớp trắng 0.3",
         eye="the girl looks at her father on the left, worried; the father keeps looking down",
         dien="Tối ở nhà: Priya đứng phía sau, cầm cốc, thấy bố ngồi buồn, bước lên một bước hỏi han.",
         cuoi="Priya nhìn bố lo lắng, cầm cốc; bố cúi mặt; miệng khép.",
         act="the girl takes one small step forward holding the cup and tilts her head, worried"),
    dict(g="L", w="HOC", lang="Hindi (natural Hinglish: the English word 'customers' said the Indian way)", start="noi",
         eye="the father lifts his eyes a little toward the girl on the right, sad; the girl looks at him",
         dien="Bố thở dài: không có gì... bố không hiểu khách nói gì cả.",
         cuoi="Bố nhìn con gái, buồn; Priya nhìn bố thương cảm; miệng khép.",
         act="the father sighs and rubs his hands together slowly on his knees"),
    dict(g="L2", w="CON", lang="Hindi (natural Hinglish: the English words 'English' and 'practice' said the Indian way)", start="moi",
         eye="the girl looks at her father on the left, encouraging; the father looks down at his hands",
         dien="Priya đã ngồi xuống cạnh bố, mỉm cười động viên: bố biết tiếng Anh mà, chỉ cần luyện.",
         cuoi="Priya mỉm cười nhìn bố; bố quay sang nhìn con; miệng khép.",
         act="the girl leans her shoulder gently toward her father with a warm smile and nods"),
    dict(g="L2", w="CON", lang="Hindi (natural Hinglish: 'Ava AI', 'English AI tutor' said the Indian way)", start="noi",
         eye="the girl looks at the phone, then at her father on the left; the father looks at the phone",
         dien="Priya lấy điện thoại, giơ màn hình về phía bố: đây là Ava AI, gia sư tiếng Anh AI của bố.",
         cuoi="Priya giơ điện thoại về phía bố, tay kia cầm cốc; bố nhìn màn hình; miệng khép.",
         act="holding the cup in her left hand, the girl takes {{DAO_DIEN_THOAI}} from her kurta pocket with her right hand and turns the screen toward her father"),
    dict(g="PH", w=None, start="moi", keep=2,
         eye="no face in the shot; the finger points at the robot on the screen",
         dien="CẢNH CÂM (~2 s): cận điện thoại, màn hình là robot gia sư trắng thân thiện, ngón tay Priya chỉ vào màn hình.",
         cuoi="Ngón tay chạm gần màn hình; điện thoại đứng yên.",
         act="the index finger moves in and points at the friendly robot face on the screen, tapping the air near it once; the phone stays steady"),
    dict(g="L3", w="CON", lang="Hindi (natural Hinglish: the English word 'teacher' said the Indian way)", start="moi",
         eye="the girl looks at her father on the left, excited; the father looks at the phone screen",
         dien="Priya hào hứng: nói chuyện với nó như với giáo viên thật; bố nhìn chăm chú màn hình.",
         cuoi="Priya đặt điện thoại vào tay bố, cười; bố cầm điện thoại nhìn màn hình; miệng khép.",
         act="the girl smiles brightly and places the phone into her father's hand"),
]

S3 = [
    dict(g="A", w="HOC", lang="English (clear and confident, light Indian accent)", start="moi",
         eye="the driver glances up at the rear-view mirror toward the passenger with a warm confident smile, then back at the road; the passenger smiles, pleasantly surprised",
         dien="Vài tuần sau: tài xế tự tin, mỉm cười chào khách qua gương bằng tiếng Anh trôi chảy; khách ngạc nhiên, mỉm cười.",
         cuoi="Tài xế nhìn đường, mỉm cười; khách mỉm cười; miệng khép.",
         act="the driver gives a small friendly nod toward the mirror, both hands on the wheel; the passenger smiles and nods once"),
    dict(g="T3", w="HOC", lang="Hindi (natural Hinglish: the English word 'English' said the Indian way)", start="moi",
         eye="the driver looks ahead at the road just past the lens, proud and happy",
         dien="Cận tài xế lái xe, tự hào: giờ tôi không còn sợ nói tiếng Anh nữa.",
         cuoi="Tài xế mỉm cười tự hào nhìn đường; miệng khép.",
         act="the driver smiles, lifts his chin a little with pride and gives a small satisfied nod, both hands on the wheel"),
]

KHOA = TK.HEAD.split("[STYLE LOCK]:", 1)[1].split("PHAN 2", 1)[0]   # các khối khoá của phần 1 bản gốc
KHOA = "[STYLE LOCK]:" + KHOA

GHI_CHU = """[HAU KY]:
loai: taxi-gia-su-ai

[GHI CHU]:
Bản ẤN ĐỘ của thể loại "tài xế taxi + gia sư AI" (Mumbai, tiếng Anh + Hindi; lời theo sheet X0061, 13/11/2026). MỘT dự án BA phần, code riêng
app/production/types/taxi-gia-su-ai/gen.py (logic chung types/_chung/nhieu_phan.py).
  PHẦN 1 (cảnh thường, {N_CANH} cảnh, {N_CAM} cảnh KHÔNG LỜI): tài xế Ấn Độ (HOC) không hiểu khách nữ (KHACH) -> đánh giá tệ; ở bến sếp (QUANLY) trao xe mới cho Arjun (ARJUN),
         tài xế xin xe (Hindi), sếp mỉa; về nhà con gái Priya (CON) giới thiệu gia sư AI Ava trên điện thoại.
         Cảnh KHÔNG LỜI: lượt của biến thể có "text": "[KHONG LOI]". Góc A: mọi cảnh dùng "Khung đầu từ cảnh: 1" (không nối khung, bài học bản đầu).
  PHẦN 2 (ghép 2 lớp): tài xế toàn khung trong taxi nhìn ống kính + robot Ava (DAY) trong ô ngang bo góc phía trên. Cặp sửa lỗi "I am India" -> "I am from India".
  PHẦN 3 (cảnh thường, 2 cảnh): tài xế tự tin chào khách bằng tiếng Anh; cận tài xế nói câu Hindi.
  Ảnh tham chiếu: tài xế + khách theo từng biến thể (link Drive của sheet); sếp + Priya gen Muse (anh/an-do/); Arjun anh/ARJUN.png; Ava canh-sat-gia-su-ai/anh/DAY.png.
Các dòng "===== PHAN n: ... =====" chia phần; mọi thứ phía trên dòng chia phần đầu tiên không gửi cho Muse.

===== PHAN 1: TAXI, BEN XE, NHA =====

"""

PART3_KHOA = """
===== PHAN 3: TAI XE TU TIN (KET) | vao: nhoe 0.5 =====

[STYLE LOCK]:
Vertical 9:16 Pixar-style 3D CARTOON exactly like the character reference images: cartoon proportions, big round expressive eyes, simplified smooth features, soft rounded shapes, warm glowing skin, rich detail; never photorealistic or semi-realistic human faces. Every shot is one fixed camera that never pans, zooms or reframes inside a clip (the camera is fixed to the front of the moving taxi). No text, no letters, no numbers, no logos, no captions, no icons, no lettering on the taxi, clothes or signs anywhere in the frame.

[CHAR LOCK]:
The {{VAI_HOC}}, {{TEN_HOC}}: {{NGUOI_HOC}}. VOICE LOCK DRIVER: one single voice, {{GIONG_HOC}}, the same in every clip.
The {{VAI_KHACH}}, {{TEN_KHACH}}: {{NGUOI_KHACH}}. VOICE LOCK PASSENGER: one single voice, {{GIONG_KHACH}}, the same in every clip.
When a character who is in the shot is silent: the driver {{NGHE_HOC}}; the passenger {{NGHE_KHACH}}.
RULE: in each clip exactly ONE character speaks, one line, with lip-sync and an expressive face, keeping the EYE LINE. Anyone else in the frame stays silent with the mouth closed. Nobody looks into the lens.

[SET LOCK]:
The taxi: {{XE}}. Outside: {{NEN_PHO}}. The taxi is driving and the city outside streams continuously past its windows.

[VIDEO SUFFIX]:
No zoom, no pan, no cut. No subtitles, no text, no music. 9:16. The speaker starts right away at a natural, quick conversational pace (about 3.5 words per second), finishes the line and then everyone keeps a calm closed-mouth face and stays still until the end of the clip, with no traffic noise over the voice.

[NEGATIVE]:
text, captions, subtitles, logos, numbers, lettering on the taxi, clothes or signs; camera zoom, shake, cut; two voices in one clip; a silent character moving the mouth; a character who is not in this shot appearing; face, hair or outfit changing; realistic live-action look; one character copying another's movements; background music; a clip with a line but no speech; slow, dragged speech.
"""

THAY = [   # chữ bản New York trong hàm dựng cảnh / khối khoá -> bản Mumbai
    ("brick buildings, shop fronts, trees, lamp posts and parked yellow cabs sliding by", "colourful shop fronts, old apartment blocks, palm trees, lamp posts and parked black-and-yellow cabs sliding by"),
    ("phone at his ear, and does not lean forward", "phone at her ear, and does not lean forward"),
    ("no lettering on the taxi, roof light, clothes, signs, clipboard, paper or phone screens", "no lettering on the taxi, clothes, signs, clipboard, paper or phone screens"),
    ("lettering on the taxi, roof light, clothes, clipboard, signs, paper or phone", "lettering on the taxi, clothes, clipboard, signs, paper or phone"),
    ("both men keep exactly the framing", "both people keep exactly the framing"),
    ("sweeping across the two men", "sweeping across the two people"),
    ("moving crowds in the garage or at home", "moving crowds in the depot or at home"),
]


def dung(ds, ang):
    TK.ANG = ang
    out, t = [], 0
    for i, s in enumerate(ds):
        if isinstance(s["start"], int):
            src = ds[s["start"] - 1]
            assert src["g"] == s["g"] and src["start"] == "moi", f"cảnh {i+1}: khung đầu từ cảnh {s['start']} phải cùng góc và có Prompt ảnh"
        if s["start"] == "noi":
            assert i > 0 and ds[i - 1]["g"] == s["g"], f"cảnh {i+1}: nối khung cuối nhưng cảnh trước khác góc"
        ln = s.get("len", 5)
        out.append(TK.scene(i, s, t, t + ln))
        t += ln
    return out


def main():
    n_cam = sum(1 for s in S if s["w"] is None)
    head = GHI_CHU.replace("{N_CANH}", str(len(S))).replace("{N_CAM}", str(n_cam))
    p1 = dung(S, ANG)
    p3 = dung(S3, ANG)
    txt = head + KHOA + "\n" + "\n\n".join(p1) + "\n" + TK.PART2 + PART3_KHOA + "\n" + "\n\n".join(p3) + "\n"
    for a, b in THAY:
        txt = txt.replace(a, b)
    txt = txt.replace("the top of his curly hair at about 38%", "the top of his head at about 38%")
    txt = txt.replace("the inside of a yellow New York taxi", "the inside of a black-and-yellow Mumbai taxi")
    assert "New York" not in txt and "Mexic" not in txt, "còn chữ của bản New York/Mexico"
    open(OUT, "w", encoding="utf-8").write(txt)
    print(f"Đã ghi {os.path.normpath(OUT)}: phần 1 {len(S)} cảnh ({n_cam} không lời) + phần 2 ghép 2 lớp + phần 3 {len(S3)} cảnh")
    print("Người nói phần 1:", " ".join((s["w"] or "-").lower() for s in S))
    print("Người nói phần 3:", " ".join(s["w"].lower() for s in S3))


if __name__ == "__main__":
    main()
