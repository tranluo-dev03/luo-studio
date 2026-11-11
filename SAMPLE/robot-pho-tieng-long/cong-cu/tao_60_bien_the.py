"""Sinh 3 file biến thể (yêu cầu người dùng 11/11/2026, dự án "Giải đố"):
  BIEN-THE-20-BAI-HOC.json   20 biến thể ĐỔI BÀI HỌC: giữ robot Texas + phố Texas + badge F1, mỗi biến thể một chủ đề 4 cụm tiếng lóng Mỹ.
  BIEN-THE-20-AN-DO.json     20 biến thể ĐỔI NHÂN VẬT + BỐI CẢNH Ấn Độ: robot nói tiếng HINDI (chữ Devanagari) dạy 4 cụm tiếng lóng Mỹ.
  BIEN-THE-20-BRAZIL.json    20 biến thể ĐỔI NHÂN VẬT + BỐI CẢNH Brazil: robot nói tiếng BỒ ĐÀO NHA (Brazil) dạy 4 cụm tiếng lóng Mỹ.
Ba nhóm dùng chung 20 bộ bài học BAI (bộ k gắn cho biến thể k của mỗi nhóm); nghĩa viết sẵn tiếng Anh, Hindi (nói), Hinglish Latin (thẻ), Bồ Đào Nha.
Robot là Aiva AI (anh/aiva/aiva-robot.webp), chỉ đổi trang phục. Ảnh tham chiếu do Muse gen (lấy Aiva làm tham chiếu) theo đúng mô tả ở đây (cong-cu/gen_anh_60.py): anh/bh/ (1 robot + 1 nền cho cả nhóm bài học), anh/in/inNN-*.webp, anh/br/brNN-*.webp.
Chạy:  runtime\\python.exe SAMPLE\\robot-pho-tieng-long\\cong-cu\\tao_60_bien_the.py
Không sửa tay JSON: sửa bảng ở đây rồi chạy lại."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tao_bien_the as TB  # noqa: E402

ROOT_REL = "SAMPLE/robot-pho-tieng-long/anh"
OUT_DIR = os.path.join(HERE, "..")

# ------------------------------------------------------------------ 20 bộ bài học
# (cụm giới thiệu cho nhóm Texas, dòng 2 tiêu đề nhóm Texas, [(cụm, nghĩa EN, nghĩa Hindi nói, nghĩa Hinglish trên thẻ, nghĩa Bồ Đào Nha)] x4)
BAI = [
    ("four everyday slang words Americans use", "EVERYDAY SLANG", [
        ("What's up?", "how are you", "क्या चल रहा है", "kya chal raha hai", "e aí, tudo bem"),
        ("Bet", "okay, deal", "ठीक है, पक्का", "theek hai, pakka", "fechado"),
        ("No cap", "no lie, for real", "सच में, झूठ नहीं", "sach mein, jhooth nahi", "é sério, sem mentira"),
        ("Catch you later", "see you soon", "बाद में मिलते हैं", "baad mein milte hain", "até mais")]),
    ("four food phrases Americans love", "FOOD SLANG", [
        ("I'm starving", "I'm very hungry", "बहुत भूख लगी है", "bahut bhookh lagi hai", "morrendo de fome"),
        ("Grab a bite", "eat something quick", "जल्दी से कुछ खा लें", "jaldi se kuch kha lein", "comer alguma coisa rápida"),
        ("It hits the spot", "exactly what I needed", "एकदम मज़ा आ गया", "ekdum maza aa gaya", "caiu como uma luva"),
        ("Pig out", "eat way too much", "जी भर के खाना", "jee bhar ke khana", "comer até não aguentar")]),
    ("four ways Americans talk about money", "MONEY SLANG", [
        ("Broke", "no money at all", "जेब बिल्कुल खाली", "jeb bilkul khaali", "duro, sem grana"),
        ("Bucks", "dollars", "डॉलर", "dollars", "dólares"),
        ("Splurge", "spend a lot for fun", "दिल खोल के खर्चा", "dil khol ke kharcha", "gastar muito por prazer"),
        ("Costs an arm and a leg", "very expensive", "बहुत ही महँगा", "bahut hi mehenga", "custa os olhos da cara")]),
    ("four phrases Americans use at work", "WORK SLANG", [
        ("Swamped", "very busy", "काम में डूबा हुआ", "kaam mein dooba hua", "atolado de trabalho"),
        ("Call it a day", "stop working for today", "आज के लिए बस", "aaj ke liye bas", "encerrar o expediente"),
        ("Touch base", "talk for a moment", "थोड़ी बात कर लें", "thodi baat kar lein", "dar uma conversada rápida"),
        ("Pull an all-nighter", "work all night without sleep", "पूरी रात जागकर काम", "poori raat jaagkar kaam", "virar a noite trabalhando")]),
    ("four ways Americans say they're happy", "HAPPY SLANG", [
        ("Stoked", "super excited", "बहुत एक्साइटेड", "bahut excited", "super animado"),
        ("Over the moon", "very happy", "बहुत खुश", "bahut khush", "muito feliz"),
        ("On cloud nine", "extremely happy", "खुशी से झूम उठना", "khushi se jhoom uthna", "nas nuvens"),
        ("Pumped", "excited and ready", "जोश में तैयार", "josh mein taiyaar", "animado e pronto")]),
    ("four ways Americans say they're tired", "CHILL SLANG", [
        ("Beat", "very tired", "बहुत थका हुआ", "bahut thaka hua", "morto de cansaço"),
        ("Chill out", "relax", "आराम करो", "aaram karo", "relaxa"),
        ("Crash", "fall asleep fast", "तुरंत सो जाना", "turant so jaana", "apagar de sono"),
        ("Take it easy", "relax, don't worry", "टेंशन मत लो", "tension mat lo", "vai com calma")]),
    ("four ways Americans say yes", "SAYING YES", [
        ("Totally", "completely, yes", "बिल्कुल", "bilkul", "com certeza"),
        ("Sounds good", "I agree", "ठीक लगता है", "theek lagta hai", "parece ótimo"),
        ("You bet", "of course", "ज़रूर", "zaroor", "pode apostar"),
        ("I'm down", "count me in", "मैं तैयार हूँ", "main taiyaar hoon", "tô dentro")]),
    ("four ways Americans show surprise", "SURPRISE SLANG", [
        ("No way!", "I can't believe it", "यकीन नहीं होता", "yakeen nahi hota", "não acredito"),
        ("For real?", "really?", "सच में?", "sach mein?", "sério mesmo?"),
        ("Get out of here!", "you're kidding me", "मज़ाक मत करो", "mazaak mat karo", "para com isso"),
        ("Mind blown", "totally amazed", "दिमाग हिल गया", "dimaag hil gaya", "fiquei de queixo caído")]),
    ("four ways Americans say something is cool", "COOL SLANG", [
        ("Awesome", "really great", "ज़बरदस्त", "zabardast", "incrível"),
        ("Lit", "exciting and fun", "धमाकेदार", "dhamakedaar", "animado, top"),
        ("Fire", "amazing", "कमाल का", "kamaal ka", "sensacional"),
        ("Killing it", "doing really well", "छा गए", "chha gaye", "mandando muito bem")]),
    ("four ways Americans talk about the weather", "WEATHER SLANG", [
        ("It's pouring", "raining hard", "तेज़ बारिश हो रही है", "tez baarish ho rahi hai", "chovendo muito"),
        ("Freezing", "very cold", "बहुत ठंड", "bahut thand", "um gelo, muito frio"),
        ("Boiling", "very hot", "बहुत गर्मी", "bahut garmi", "um forno, muito calor"),
        ("Raining cats and dogs", "a really heavy rain", "मूसलाधार बारिश", "moosladhaar baarish", "chovendo canivete")]),
    ("four shopping phrases Americans use", "SHOPPING SLANG", [
        ("Window shopping", "looking without buying", "बस देखना, खरीदना नहीं", "bas dekhna, kharidna nahi", "só olhar, sem comprar"),
        ("A steal", "very cheap", "बहुत सस्ता", "bahut sasta", "uma pechincha"),
        ("A rip-off", "way too expensive", "लूट, बहुत महँगा", "loot, bahut mehenga", "um roubo, caro demais"),
        ("Shop till you drop", "shop until you're exhausted", "थकने तक शॉपिंग", "thakne tak shopping", "comprar até cansar")]),
    ("four dating phrases Americans use", "DATING SLANG", [
        ("Crush", "someone you secretly like", "जो दिल को पसंद हो", "jo dil ko pasand ho", "aquela paixonite"),
        ("Ghost", "stop replying suddenly", "अचानक जवाब देना बंद", "achanak jawab dena band", "sumir sem responder"),
        ("Hit it off", "like each other right away", "तुरंत जम जाना", "turant jam jaana", "se dar bem de cara"),
        ("Head over heels", "deeply in love", "पूरी तरह प्यार में", "poori tarah pyaar mein", "perdidamente apaixonado")]),
    ("four travel phrases Americans use", "TRAVEL SLANG", [
        ("Hit the road", "start a trip", "सफ़र शुरू करना", "safar shuru karna", "pegar a estrada"),
        ("Jet lag", "tired after a long flight", "लंबी फ़्लाइट के बाद थकान", "lambi flight ke baad thakaan", "cansaço depois de voo longo"),
        ("Bucket list", "dreams to do in life", "ज़िंदगी के सपनों की लिस्ट", "zindagi ke sapnon ki list", "lista de sonhos da vida"),
        ("Off the beaten path", "far from tourist spots", "भीड़ से दूर जगह", "bheed se door jagah", "longe dos lugares turísticos")]),
    ("four racing phrases for race day", "RACING SLANG", [
        ("Pole position", "starting in first place", "सबसे आगे से शुरुआत", "sabse aage se shuruaat", "largar em primeiro"),
        ("Full throttle", "as fast as possible", "पूरी रफ़्तार से", "poori raftaar se", "acelerar tudo"),
        ("Home stretch", "almost at the finish", "मंज़िल बस पास है", "manzil bas paas hai", "na reta final"),
        ("Neck and neck", "very close, side by side", "बराबर की टक्कर", "barabar ki takkar", "lado a lado")]),
    ("four school phrases Americans use", "SCHOOL SLANG", [
        ("Hit the books", "study hard", "मन लगाकर पढ़ना", "man lagakar padhna", "estudar pra valer"),
        ("Cram", "study a lot at the last minute", "आख़िरी वक्त की रटाई", "aakhri waqt ki rataai", "estudar tudo na última hora"),
        ("Ace it", "do it perfectly", "पूरे नंबर लाना", "poore number laana", "gabaritar"),
        ("Pass with flying colors", "pass really easily", "शानदार तरीके से पास", "shaandaar tarike se pass", "passar com louvor")]),
    ("four ways Americans admit a mistake", "OOPS SLANG", [
        ("My bad", "my mistake", "मेरी गलती", "meri galti", "foi mal"),
        ("Mess up", "make a mistake", "गड़बड़ कर देना", "gadbad kar dena", "fazer besteira"),
        ("Drop the ball", "fail to do your part", "ज़िम्मेदारी में चूक", "zimmedari mein chook", "pisar na bola"),
        ("Back to square one", "start all over again", "फिर से शुरुआत", "phir se shuruaat", "voltar à estaca zero")]),
    ("four internet slang words Americans use", "INTERNET SLANG", [
        ("Hit me up", "message me", "मुझे मैसेज करना", "mujhe message karna", "me chama"),
        ("Go viral", "spread fast online", "इंटरनेट पर छा जाना", "internet par chha jaana", "viralizar"),
        ("FOMO", "fear of missing out", "कुछ छूट जाने का डर", "kuch chhoot jaane ka darr", "medo de ficar de fora"),
        ("Low-key", "a little, quietly", "थोड़ा-सा, चुपके से", "thoda-sa, chupke se", "meio que, discretamente")]),
    ("four ways Americans say easy or hard", "EASY OR HARD?", [
        ("Piece of cake", "very easy", "बहुत आसान", "bahut aasaan", "moleza"),
        ("No-brainer", "an easy decision", "सोचने की ज़रूरत नहीं", "sochne ki zaroorat nahi", "decisão óbvia"),
        ("Not rocket science", "not difficult at all", "कोई मुश्किल काम नहीं", "koi mushkil kaam nahi", "não é nenhum bicho de sete cabeças"),
        ("Easier said than done", "harder than it sounds", "कहना आसान, करना मुश्किल", "kehna aasaan, karna mushkil", "falar é fácil, fazer é difícil")]),
    ("four ways Americans cheer you on", "PEP TALK SLANG", [
        ("You got this", "you can do it", "तुम कर सकते हो", "tum kar sakte ho", "você consegue"),
        ("Go for it", "try it now", "कर डालो", "kar daalo", "vai fundo"),
        ("Hang in there", "don't give up", "हिम्मत रखो", "himmat rakho", "aguenta firme"),
        ("Break a leg", "good luck", "गुड लक", "good luck", "boa sorte")]),
    ("four party phrases Americans use", "PARTY SLANG", [
        ("Hang out", "spend time together", "साथ में वक्त बिताना", "saath mein waqt bitaana", "sair junto"),
        ("Throw a party", "host a party", "पार्टी देना", "party dena", "dar uma festa"),
        ("Party animal", "someone who loves parties", "पार्टी का शौकीन", "party ka shaukeen", "festeiro"),
        ("Sleep in", "sleep late in the morning", "देर तक सोना", "der tak sona", "dormir até tarde")]),
]
assert len(BAI) == 20 and all(len(b[2]) == 4 for b in BAI)

EMO = ["cheerful", "playful, upbeat", "confident, cheerful", "warm, playful"]


AIVA = ("the Aiva AI robot: a glossy white-and-pale-lavender humanoid AI robot with a smooth sculpted feminine face with a calm friendly expression, "
        "glowing blue eyes and soft lips, a smooth glossy white skull with fine panel seams and no hair, a small glowing white \"AI\" mark on the forehead, "
        "a pair of white-and-black over-ear headphones worn over the ears with a thin microphone boom curving to the mouth, a black segmented mechanical neck, "
        "glossy white armor on the shoulders and chest with a small glowing white open-book icon at the centre of the chest.")


def robot(face=None):
    """Robot Aiva AI cố định (ảnh người dùng gửi 11/11/2026, anh/aiva/aiva-robot.webp): giống hệt ở mọi biến thể, chỉ đổi trang phục."""
    return AIVA


def giong(gender, lang):
    nguoi = "young woman's" if gender == "f" else "young man's"
    if lang == "hi":
        noi = ("a native Hindi speaker from India speaking natural, everyday Hindi, who says the English slang words in clear, fluent English; "
               "like a friendly Indian travel host recording a short tip video")
    else:
        noi = ("a native Brazilian Portuguese speaker speaking natural, everyday Brazilian Portuguese, who says the English slang words in clear, "
               "fluent American English; like a friendly Brazilian travel host recording a short tip video")
    return f"a warm, bright, natural {nguoi} voice, {noi}, lively varied intonation with a smile in the voice, clear crisp diction; completely human-sounding, not robotic"


def moc(text, toi_thieu=3):
    """Từ dùng để căn thời điểm (Latin hay Devanagari): từ đầu có >= `toi_thieu` ký tự chữ."""
    ws = text.split()
    for w in ws:
        if len(re.sub(r"[\W_]", "", w)) >= toi_thieu:
            return w.strip("'\"!?.,।")
    return ws[0].strip("'\"!?.,।")


def cum_noi(tu, cuoi):
    """Cụm tiếng lóng khi nói: giữ ?/! sẵn có, không thì thêm `cuoi`."""
    return tu if tu.endswith(("?", "!")) else tu + cuoi


def cum_hoi(tu):
    """Cụm tiếng lóng trong câu hỏi cuối: bỏ dấu, viết thường chữ đầu (trừ FOMO, I'm)."""
    w = tu.rstrip("?!.")
    return w if w.isupper() or w.startswith("I'm") else w[0].lower() + w[1:]


def the_cards(items, nghia_the, nghia_noi):
    return [{"luot": k + 1, "tu": it[0].upper(), "nghia": nghia_the(it), "moc_tu": moc(it[0], 2), "moc_nghia": moc(nghia_noi(it))}
            for k, it in enumerate(items)]


# ------------------------------------------------------------------ nhóm 1: đổi bài học (robot + phố Texas giữ nguyên)
TEXAS = list(TB.BIEN_THE[0])   # ("texan-f1-austin", TRANG_PHUC, NEN_PHO, ...)
TEXAS[1] = "a light-blue long-sleeve denim western shirt buttoned up, dark-blue jeans and a brown leather belt. The robot is fully dressed like a person: the clothes cover the whole torso, shoulders, arms and legs; only the robot head, neck and hands are visible"


def nhom_bai_hoc():
    out = []
    for k, (gioi_thieu, tieu_de2, items) in enumerate(BAI, 1):
        lines = [(f"F1 is rolling into Texas! Here are {gioi_thieu}.", "excited, cheerful")]
        for j, it in enumerate(items):
            lines.append(((f"{cum_noi(it[0], '!')} That means {it[1]}." if j < 3 else f"And {cum_noi(it[0], '.')} That means {it[1]}."), EMO[j]))
        lines.append((f"Would you say {cum_hoi(items[0][0])}? Tell me in the comments.", "curious, friendly"))
        the = the_cards(items, lambda it: it[1], lambda it: it[1])
        slug = re.sub(r"[^a-z0-9]+", "-", tieu_de2.lower()).strip("-")
        v = TB.build(f"bh{k:02d}-{slug}", TEXAS[1], TEXAS[2], ("F1 IS IN TEXAS", tieu_de2), TEXAS[4], ("AMERICANS SAY", "IT MEANS"), lines, the)
        v["NGUOI_DAY"] = AIVA
        v["refs"] = {"NGUOI_DAY": [f"{ROOT_REL}/bh/bh-nv.webp"], "NEN_PHO": [f"{ROOT_REL}/bh/bh-bg.webp"]}
        v["HAU_KY"]["ngon_ngu"] = "en"
        out.append(v)
    return out


# ------------------------------------------------------------------ nhóm 2: Ấn Độ, tiếng Hindi
# (slug, thành phố Latin cho tiêu đề, thành phố Devanagari, giới, khuôn mặt, trang phục, nền)
AN_DO = [
    ("mumbai-marine-drive", "MUMBAI", "मुंबई", "f", "a realistic young Indian woman's face: warm light-brown synthetic skin and dark brown eyes",
     "a coral-pink cotton saree with a thin gold border, draped over the left shoulder across the white chest armor",
     "Mumbai's Marine Drive at golden hour: a wide seaside promenade with a low concrete sea wall, the curving blue bay, a row of cream art-deco apartment buildings and tall palm trees, warm hazy sky"),
    ("delhi-india-gate", "DELHI", "दिल्ली", "m", "a realistic young Indian man's face, clean-shaven: medium-brown synthetic skin and dark brown eyes",
     "a white cotton kurta under a navy-blue sleeveless Nehru jacket with small round buttons",
     "the India Gate war memorial in New Delhi on a clear morning: the tall sandstone arch at the end of a wide green lawn and a straight red-gravel avenue, trees on both sides, pale blue sky"),
    ("jaipur-hawa-mahal", "JAIPUR", "जयपुर", "f", "a realistic young Indian woman's face: golden-brown synthetic skin and dark brown eyes",
     "a bright magenta-pink dupatta with tiny mirror-work embroidery draped over both shoulders above an orange embroidered blouse",
     "the Hawa Mahal palace in Jaipur in warm morning light: the tall pink sandstone facade with hundreds of small latticed windows and domes, an empty wide street in front"),
    ("agra-taj-mahal", "AGRA", "आगरा", "m", "a realistic Indian man's face in his thirties, clean-shaven: warm brown synthetic skin and dark eyes",
     "a cream-coloured cotton kurta with fine gold embroidery around the collar and down the front placket",
     "the gardens of the Taj Mahal in Agra at sunrise: the white marble mausoleum with its dome and four minarets at the end of a long reflecting pool lined with cypress trees, soft pink-gold sky"),
    ("varanasi-ghats", "VARANASI", "वाराणसी", "f", "a realistic Indian woman's face in her thirties: deep brown synthetic skin and dark brown eyes",
     "a saffron-yellow cotton saree draped over the left shoulder across the white chest armor",
     "the riverside ghats of Varanasi at early morning: wide stone steps going down to the calm Ganges river, old ochre and red temple-like buildings along the bank, wooden boats moored, soft misty light"),
    ("kolkata-howrah", "KOLKATA", "कोलकाता", "m", "a realistic young Indian man's face, clean-shaven: light-brown synthetic skin and dark brown eyes",
     "a white cotton kurta with a cream shawl with a thin red border folded over one shoulder",
     "a riverside promenade in Kolkata: the huge grey steel cantilever Howrah Bridge across the wide Hooghly river behind, a few old yellow Ambassador taxis parked along the road, warm afternoon haze"),
    ("bengaluru-tech", "BENGALURU", "बेंगलुरु", "f", "a realistic young Indian woman's face: medium-brown synthetic skin and dark brown eyes",
     "a slim navy-blue blazer worn open over a white cotton kurti with a round neck",
     "a modern tech-park plaza in Bengaluru: glass office towers, a wide paved walkway, tall rain trees with purple jacaranda flowers and neat green lawns, bright blue sky"),
    ("hyderabad-charminar", "HYDERABAD", "हैदराबाद", "m", "a realistic Indian man's face in his thirties, with a neatly trimmed short black beard: medium-brown synthetic skin and dark eyes",
     "a dark bottle-green sherwani-style long jacket with a stand-up collar and small gold buttons",
     "the Charminar monument in Hyderabad in warm late-afternoon light: the square granite and limestone arch building with four tall minarets, old shop buildings with closed shutters on both sides of an empty street"),
    ("goa-beach", "GOA", "गोवा", "f", "a realistic young Indian woman's face: tan golden-brown synthetic skin and dark brown eyes",
     "an open white linen shirt with rolled sleeves and a bright turquoise-and-orange tie-dye scarf loosely around the neck",
     "a quiet Goa beach at golden hour: soft pale sand, gentle turquoise waves, leaning coconut palm trees and a small bamboo beach shack with a palm-leaf roof, warm orange sky"),
    ("rishikesh-ganga", "RISHIKESH", "ऋषिकेश", "m", "a realistic young Indian man's face, clean-shaven: warm brown synthetic skin and dark brown eyes",
     "a loose off-white linen kurta and a light-grey cotton scarf around the neck",
     "Rishikesh by the Ganges: a long iron suspension footbridge over the clear turquoise river, green forested Himalayan foothills behind, old buildings on the far bank, soft morning light"),
    ("udaipur-lake", "UDAIPUR", "उदयपुर", "f", "a realistic Indian woman's face in her thirties: light-brown synthetic skin and dark brown eyes",
     "an emerald-green silk saree with a wide gold border, draped over the left shoulder across the white chest armor",
     "Lake Pichola in Udaipur at sunset: a white marble lakeside palace with domes and arches reflected in calm water, the Aravalli hills behind, a stone terrace in front, golden sky"),
    ("shimla-mall-road", "SHIMLA", "शिमला", "m", "a realistic Indian man's face in his forties, clean-shaven: fair light-brown synthetic skin and dark brown eyes",
     "a maroon wool V-neck sweater and a grey knitted muffler around the neck",
     "the Mall Road ridge in Shimla on a crisp clear day: a wide paved open square, a yellow neo-Gothic colonial church tower and old timber-framed buildings, pine-covered hills and distant snowy peaks"),
    ("kochi-fishing-nets", "KOCHI", "कोच्चि", "f", "a realistic young Indian woman's face: deep brown synthetic skin and dark brown eyes",
     "a cream Kerala kasavu saree with a wide gold border, draped over the left shoulder across the white chest armor",
     "the Fort Kochi waterfront in Kerala at sunset: giant wooden Chinese fishing nets on teak poles over the calm sea, coconut palms along the shore, orange sky"),
    ("darjeeling-tea", "DARJEELING", "दार्जिलिंग", "m", "a realistic young Indian man's face from the Himalayan hills, clean-shaven: light golden synthetic skin and dark brown eyes",
     "a dark-green padded jacket worn open over the white chest armor and a thick grey knitted scarf",
     "a Darjeeling tea garden: neat rows of bright green tea bushes on steep hills, a few tall shade trees, distant snow-capped Himalayan peaks under a clear blue sky"),
    ("lucknow-rumi-darwaza", "LUCKNOW", "लखनऊ", "f", "a realistic young Indian woman's face: fair light-brown synthetic skin and dark brown eyes",
     "a white chikankari kurta with fine white thread embroidery and a pale-pink dupatta over one shoulder",
     "the Rumi Darwaza gateway in Lucknow on a clear afternoon: the huge ornate Mughal arch gate in pale stone, an empty wide road passing under it, trees and blue sky"),
    ("ahmedabad-riverfront", "AHMEDABAD", "अहमदाबाद", "m", "a realistic Indian man's face in his thirties, with a neat short moustache: warm brown synthetic skin and dark eyes",
     "a short white kediyu-style pleated top with colourful red and green embroidery across the chest",
     "the Sabarmati Riverfront in Ahmedabad at golden hour: a wide paved promenade beside the calm river, a modern bridge with curved steel arches, green lawns and city buildings across the water"),
    ("mysuru-palace", "MYSURU", "मैसूर", "f", "a realistic Indian woman's face in her thirties: warm brown synthetic skin and dark brown eyes",
     "a mustard-yellow Mysore silk saree with a maroon border, draped over the left shoulder across the white chest armor",
     "the Mysore Palace in Karnataka in warm evening light: the grand palace with red domes, arches and a tall central tower behind wide manicured gardens, clear sky"),
    ("chandigarh-sukhna", "CHANDIGARH", "चंडीगढ़", "m", "a realistic young Indian man's face, clean-shaven: fair light-brown synthetic skin and dark brown eyes",
     "a plain light-blue sporty cricket-style jersey with a white collar and no letters, logos or numbers",
     "Sukhna Lake in Chandigarh at golden hour: a wide paved lakeside promenade with lamp posts, calm water, low green Shivalik hills on the far side, warm sky"),
    ("delhi-chandni-chowk", "DELHI", "दिल्ली", "f", "a realistic young Indian woman's face: medium-brown synthetic skin and dark brown eyes",
     "a red salwar kameez with fine gold embroidery and a light golden dupatta over both shoulders",
     "an old Delhi bazaar lane in Chandni Chowk early in the morning before opening: narrow old buildings with carved balconies, shop shutters closed, tangled overhead wires, warm soft light, completely empty"),
    ("mumbai-bandstand", "MUMBAI", "मुंबई", "m", "a realistic young Indian man's face, clean-shaven: medium-brown synthetic skin and dark brown eyes",
     "a black bomber jacket worn open over a plain white t-shirt",
     "the Bandstand seafront in Mumbai at sunset: a stone promenade with a railing above dark rocks and the sea, the long cable-stayed Bandra-Worli Sea Link bridge in the distance, orange sky"),
]
assert len(AN_DO) == 20

MO_DAU_HI = [
    "{c} वालो, आज सीखते हैं अमेरिकन इंग्लिश के चार मज़ेदार स्लैंग!",
    "{c} से नमस्ते! चलो, अमेरिकन लोगों की तरह इंग्लिश बोलना सीखें!",
    "{c} में हो? तो आज सीखो अमेरिकन इंग्लिश के चार स्लैंग!",
]


def nhom_an_do():
    out = []
    for k, (slug, city, city_hi, gender, face, outfit, nen) in enumerate(AN_DO, 1):
        items = BAI[k - 1][2]
        lines = [(MO_DAU_HI[(k - 1) % 3].format(c=city_hi), "excited, cheerful")]
        for j, it in enumerate(items):
            lines.append(((f"{cum_noi(it[0], '!')} इसका मतलब है, {it[2]}।" if j < 3 else f"और {cum_noi(it[0], '.')} इसका मतलब है, {it[2]}।"), EMO[j]))
        lines.append((f"आप {cum_hoi(items[0][0])} बोलोगे? कमेंट में बताओ!", "curious, friendly"))
        the = the_cards(items, lambda it: it[3], lambda it: it[2])
        v = TB.build(f"in{k:02d}-{slug}", outfit, nen + "; the whole background softly out of focus, any lettering on signs unreadable.",
                     (f"{city} WALON,", "SLANG SEEKHO!"), ("USA", "ENGLISH SLANG"), ("AMERICANS SAY", "MATLAB"), lines, the)
        v["NGUOI_DAY"] = robot(face)
        v["GIONG_DAY"] = giong(gender, "hi")
        v["refs"] = {"NGUOI_DAY": [f"{ROOT_REL}/in/in{k:02d}-nv.webp"], "NEN_PHO": [f"{ROOT_REL}/in/in{k:02d}-bg.webp"]}
        v["HAU_KY"].update({"ngon_ngu": "hi", "font_ass": "Nirmala UI", "shaping": "complex"})
        out.append(v)
    return out


# ------------------------------------------------------------------ nhóm 3: Brazil, tiếng Bồ Đào Nha
# (slug, tiêu đề dòng 1, "em ...", "de ...", giới, khuôn mặt, trang phục, nền)
BRAZIL = [
    ("rio-copacabana", "RIO DE JANEIRO", "no Rio", "do Rio", "f", "a realistic young Brazilian woman's face: light tan olive synthetic skin and warm hazel eyes",
     "an open lime-green linen shirt with rolled sleeves over the white chest armor",
     "the Copacabana promenade in Rio de Janeiro on a sunny afternoon: the famous black-and-white wavy mosaic sidewalk, tall palm trees, the wide golden beach and blue ocean, green hills in the distance"),
    ("rio-selaron", "RIO DE JANEIRO", "no Rio", "do Rio", "m", "a realistic young Brazilian man's face, clean-shaven: deep brown synthetic skin and dark brown eyes",
     "a mustard-yellow short-sleeve camp-collar shirt worn open over the white chest armor",
     "the Selarón Steps in Rio de Janeiro: a long staircase covered in bright red, yellow, blue and green ceramic tiles with plain patterns, colourful old houses on both sides, warm daylight"),
    ("rio-pao-de-acucar", "RIO DE JANEIRO", "no Rio", "do Rio", "f", "a realistic Brazilian woman's face in her thirties: warm brown synthetic skin and dark brown eyes",
     "a white crochet open-knit cardigan over the white chest armor",
     "the Urca seawall in Rio de Janeiro at golden hour: a low stone wall by calm blue water with small fishing boats, Sugarloaf Mountain rising behind, warm orange sky"),
    ("sao-paulo-paulista", "SÃO PAULO", "em São Paulo", "de São Paulo", "m", "a realistic Brazilian man's face in his thirties, clean-shaven: fair skin and dark brown eyes",
     "a slim charcoal-grey blazer worn open over a plain black t-shirt",
     "Avenida Paulista in São Paulo on a bright day: a wide modern avenue lined with tall glass skyscrapers and trees, a wide pedestrian sidewalk, modern architecture, light clouds"),
    ("sao-paulo-murais", "SÃO PAULO", "em São Paulo", "de São Paulo", "f", "a realistic young Brazilian woman's face: light-brown synthetic skin and dark brown eyes",
     "an oversized light-blue denim jacket worn open over the white chest armor",
     "a narrow alley in Vila Madalena, São Paulo, with every wall covered in huge colourful abstract street-art murals of faces, birds and flowers (pictures only, no letters), warm daylight"),
    ("interlagos-f1", "INTERLAGOS", "em Interlagos", "de Interlagos", "m", "a realistic young Brazilian man's face, clean-shaven: tan light-brown synthetic skin and dark brown eyes",
     "a red racing team jacket with white side stripes, no logos and no letters, worn open over the white chest armor",
     "the Interlagos race circuit in São Paulo on race weekend: an empty grey asphalt track with red-and-white kerbs, a tall covered grandstand, catch fences, green trees around, bright sky"),
    ("salvador-pelourinho", "SALVADOR", "em Salvador", "de Salvador", "f", "a realistic Brazilian woman's face in her thirties: deep dark-brown synthetic skin and dark brown eyes",
     "a white lace Baiana-style off-shoulder blouse with a long colourful beaded necklace",
     "the Pelourinho old town in Salvador: a sloping cobblestone square lined with pastel pink, blue, yellow and green colonial houses with tall windows, a baroque church far behind, bright sun"),
    ("florianopolis-praia", "FLORIANÓPOLIS", "em Floripa", "de Floripa", "m", "a realistic young Brazilian man's face, clean-shaven: sun-tanned light skin and light-brown eyes",
     "an open short-sleeve shirt with a blue ocean-wave print over the white chest armor",
     "a quiet beach in Florianópolis: soft white sand dunes with low green grass, clear turquoise water, a rocky green headland on the side, blue sky"),
    ("foz-do-iguacu", "FOZ DO IGUAÇU", "em Foz do Iguaçu", "de Foz do Iguaçu", "f", "a realistic young Brazilian woman's face: light olive synthetic skin and green eyes",
     "a khaki safari shirt with chest pockets and rolled sleeves, worn open over the white chest armor",
     "the Iguaçu Falls viewpoint: wide curtains of white waterfalls pouring over red cliffs into a misty gorge, lush green rainforest around, a faint rainbow in the mist"),
    ("manaus-teatro", "MANAUS", "em Manaus", "de Manaus", "m", "a realistic Brazilian man's face in his thirties, with a short neat beard: warm brown synthetic skin and dark eyes",
     "a light sage-green linen short-sleeve shirt worn open over the white chest armor",
     "the Amazon Theatre in Manaus: a pink Renaissance-style opera house with white columns and a dome of green, yellow and blue tiles, a wavy black-and-white mosaic square in front"),
    ("amazonia-rio", "AMAZÔNIA", "na Amazônia", "da Amazônia", "f", "a realistic Brazilian woman's face in her thirties: medium-brown synthetic skin and dark brown eyes",
     "a khaki utility vest with many pockets over the white chest armor",
     "a wooden dock on the Amazon river: a wide brown calm river, dense green rainforest on both banks, a small wooden riverboat moored, soft humid light"),
    ("olinda-ladeiras", "OLINDA", "em Olinda", "de Olinda", "m", "a realistic young Brazilian man's face, clean-shaven: deep brown synthetic skin and dark brown eyes",
     "a colourful short-sleeve shirt with a bold red, yellow, green and blue geometric frevo pattern",
     "a steep cobblestone street in historic Olinda: small colonial houses painted in bright orange, blue, green and yellow, palm trees, a view down to the sea, bright sun"),
    ("fortaleza-jangadas", "FORTALEZA", "em Fortaleza", "de Fortaleza", "f", "a realistic young Brazilian woman's face: light-brown synthetic skin and dark brown eyes",
     "a white cotton beach shirt with thin blue stripes worn open over the white chest armor",
     "a beach in Fortaleza at golden hour: golden sand, small wooden jangada sailboats with white triangular sails pulled up on the beach, palm trees, calm green sea"),
    ("brasilia-congresso", "BRASÍLIA", "em Brasília", "de Brasília", "m", "a realistic Brazilian man's face in his forties, clean-shaven: fair skin and blue-grey eyes",
     "a navy-blue suit jacket worn open over a light-blue shirt, no tie",
     "the National Congress in Brasília: two tall white twin towers between a white bowl-shaped dome and an upturned dome, a wide green lawn and a reflecting pool, huge blue sky"),
    ("ouro-preto", "OURO PRETO", "em Ouro Preto", "de Ouro Preto", "f", "a realistic Brazilian woman's face in her thirties: fair skin and dark brown eyes",
     "a mustard-yellow wool cardigan worn open over the white chest armor",
     "a steep cobblestone street in Ouro Preto: white colonial houses with colourful blue and green window frames, a baroque church with twin towers on the hill, green mountains, soft morning light"),
    ("gramado-flores", "GRAMADO", "em Gramado", "de Gramado", "m", "a realistic Brazilian man's face in his thirties, clean-shaven: fair skin and light-brown eyes",
     "a grey wool peacoat worn open over the white chest armor and a red wool scarf",
     "a street in Gramado: Bavarian-style half-timbered houses with steep roofs, beds of blue hydrangea flowers along the sidewalk, tall pine trees, cool soft light"),
    ("pantanal", "PANTANAL", "no Pantanal", "do Pantanal", "m", "a realistic Brazilian man's face in his fifties, with a short grey moustache: sun-tanned brown synthetic skin and dark eyes",
     "a red-and-brown plaid shirt with rolled sleeves and a brown leather vest",
     "the Pantanal wetlands at sunrise: a wooden ranch fence, flat green grassland with shallow water pools, scattered palm trees, a few white herons in the distance, golden mist"),
    ("lencois-maranhenses", "MARANHÃO", "no Maranhão", "do Maranhão", "f", "a realistic young Brazilian woman's face: tan golden-brown synthetic skin and dark brown eyes",
     "a flowing white linen shirt worn open over the white chest armor",
     "the Lençóis Maranhenses dunes: endless rolling white sand dunes with clear blue-green rainwater lagoons between them, bright blue sky with small clouds"),
    ("paraty", "PARATY", "em Paraty", "de Paraty", "m", "a realistic young Brazilian man's face, clean-shaven: light-brown synthetic skin and dark brown eyes",
     "a navy-and-white striped short-sleeve sailor t-shirt",
     "the historic centre of Paraty: a street of big irregular stones lined with white colonial houses with doors and window frames painted blue, yellow and green, colourful wooden boats in the bay at the end"),
    ("rio-arcos-da-lapa", "LAPA, RIO", "na Lapa", "da Lapa", "f", "a realistic young Brazilian woman's face: warm brown synthetic skin and dark brown eyes",
     "a shiny gold sleeveless party top",
     "the Lapa Arches in Rio de Janeiro at dusk: the long white double-tiered colonial aqueduct with many arches, warm street lamps, old buildings around, deep blue evening sky"),
]
assert len(BRAZIL) == 20

# ------------------------------------------------------------------ trang phục mặc đầy đủ như người (người dùng yêu cầu 11/11/2026)
# Áo kín thân, tay áo dài tới cổ tay, có quần / váy / sari quấn đủ: chỉ lộ đầu, cổ và bàn tay robot. Ghi đè cột trang phục của AN_DO / BRAZIL.
KIN = " The robot is fully dressed like a person: the clothes cover the whole torso, shoulders, arms and legs; only the robot head, neck and hands are visible."
FULL_IN = {
    "mumbai-marine-drive": "a coral-pink cotton saree with a thin gold border, wrapped and pleated the traditional way down to the feet, the pallu over the left shoulder, with a matching coral long-sleeve blouse",
    "delhi-india-gate": "a white long-sleeve cotton kurta reaching the knees, a navy-blue Nehru jacket buttoned up over it, and white churidar trousers",
    "jaipur-hawa-mahal": "an orange long-sleeve embroidered kurti reaching the knees, matching orange palazzo trousers, and a bright magenta-pink mirror-work dupatta over both shoulders",
    "agra-taj-mahal": "a knee-length cream long-sleeve kurta with fine gold embroidery around the collar and down the front, and cream pyjama trousers",
    "varanasi-ghats": "a saffron-yellow cotton saree wrapped and pleated the traditional way down to the feet, the pallu over the left shoulder, with a saffron long-sleeve blouse",
    "kolkata-howrah": "a white long-sleeve panjabi kurta reaching the knees, white dhoti-style trousers, and a cream shawl with a thin red border folded over one shoulder",
    "bengaluru-tech": "a navy-blue blazer buttoned over a white long-sleeve kurti, and slim navy-blue trousers",
    "hyderabad-charminar": "a dark bottle-green knee-length sherwani with long sleeves, buttoned up to the stand-up collar with small gold buttons, and cream churidar trousers",
    "goa-beach": "a white long-sleeve linen shirt buttoned up, light-beige linen trousers, and a turquoise-and-orange tie-dye scarf loosely around the neck",
    "rishikesh-ganga": "a long off-white linen kurta with long sleeves, loose white linen trousers, and a light-grey cotton scarf around the neck",
    "udaipur-lake": "an emerald-green silk saree with a wide gold border, wrapped and pleated the traditional way down to the feet, the pallu over the left shoulder, with an emerald long-sleeve blouse",
    "shimla-mall-road": "a maroon wool V-neck sweater over a white collared shirt, grey wool trousers, and a grey knitted muffler around the neck",
    "kochi-fishing-nets": "a cream Kerala kasavu saree with a wide gold border, wrapped and pleated the traditional way down to the feet, the pallu over the left shoulder, with a cream long-sleeve blouse",
    "darjeeling-tea": "a dark-green padded jacket zipped up, dark-grey trousers, and a thick grey knitted scarf around the neck",
    "lucknow-rumi-darwaza": "a white long-sleeve chikankari kurta with fine white thread embroidery reaching the knees, white straight trousers, and a pale-pink dupatta over one shoulder",
    "ahmedabad-riverfront": "a white long-sleeve kediyu-style pleated top with colourful red and green embroidery across the chest, and white churidar trousers",
    "mysuru-palace": "a mustard-yellow Mysore silk saree with a maroon border, wrapped and pleated the traditional way down to the feet, the pallu over the left shoulder, with a maroon long-sleeve blouse",
    "chandigarh-sukhna": "a light-blue long-sleeve cricket-style jersey with a white collar and no letters, logos or numbers, and white cricket trousers",
    "delhi-chandni-chowk": "a red long-sleeve salwar kameez with fine gold embroidery reaching the knees, red salwar trousers, and a light golden dupatta over both shoulders",
    "mumbai-bandstand": "a black bomber jacket half-zipped over a plain white t-shirt, and dark-blue jeans",
}
FULL_BR = {
    "rio-copacabana": "a lime-green long-sleeve linen shirt buttoned up, and white linen trousers",
    "rio-selaron": "a mustard-yellow long-sleeve camp-collar shirt buttoned up, and beige chino trousers",
    "rio-pao-de-acucar": "a white long-sleeve crochet cardigan buttoned over a white top, and light-blue jeans",
    "sao-paulo-paulista": "a charcoal-grey blazer buttoned over a black crew-neck sweater, and charcoal-grey trousers",
    "sao-paulo-murais": "an oversized light-blue denim jacket buttoned over a white t-shirt, and black jeans",
    "interlagos-f1": "a red racing team jacket with white side stripes, zipped up, with no logos and no letters, and black trousers",
    "salvador-pelourinho": "a white long-sleeve lace Baiana-style blouse, a long full white skirt down to the feet, and a long colourful beaded necklace",
    "florianopolis-praia": "a long-sleeve shirt with a blue ocean-wave print buttoned up, and light-khaki trousers",
    "foz-do-iguacu": "a khaki long-sleeve safari shirt with chest pockets buttoned up, and khaki cargo trousers",
    "manaus-teatro": "a sage-green long-sleeve linen shirt buttoned up, and cream linen trousers",
    "amazonia-rio": "an olive-green long-sleeve shirt with a khaki utility vest with many pockets over it, and olive cargo trousers",
    "olinda-ladeiras": "a long-sleeve shirt with a bold red, yellow, green and blue geometric frevo pattern buttoned up, and white trousers",
    "fortaleza-jangadas": "a white long-sleeve cotton shirt with thin blue stripes buttoned up, and white linen trousers",
    "brasilia-congresso": "a navy-blue suit jacket buttoned over a light-blue shirt, no tie, and navy-blue suit trousers",
    "ouro-preto": "a mustard-yellow wool cardigan buttoned over a cream blouse, and dark-brown corduroy trousers",
    "gramado-flores": "a grey wool peacoat buttoned up, a red wool scarf, and dark-grey trousers",
    "pantanal": "a red-and-brown plaid long-sleeve shirt buttoned up, a brown leather vest over it, and blue jeans",
    "lencois-maranhenses": "a flowing white long-sleeve linen shirt buttoned up, and wide white linen trousers",
    "paraty": "a navy-and-white striped long-sleeve sailor top, and navy-blue trousers",
    "rio-arcos-da-lapa": "a shiny gold long-sleeve party top, and black high-waisted trousers",
}
assert set(FULL_IN) == {r[0] for r in AN_DO} and set(FULL_BR) == {r[0] for r in BRAZIL}
AN_DO = [r[:5] + (FULL_IN[r[0]] + "." + KIN,) + r[6:] for r in AN_DO]
BRAZIL = [r[:6] + (FULL_BR[r[0]] + "." + KIN,) + r[7:] for r in BRAZIL]

MO_DAU_PT = [
    "Oi, gente! Direto {de}, bora aprender gírias do inglês americano!",
    "Tá {em}? Então aprende comigo quatro gírias do inglês americano!",
    "Hoje, {em}, vou te ensinar quatro gírias que os americanos usam!",
]


def nhom_brazil():
    out = []
    for k, (slug, title, em, de, gender, face, outfit, nen) in enumerate(BRAZIL, 1):
        items = BAI[k - 1][2]
        mo_dau = ("A Fórmula 1 chegou em Interlagos! Bora aprender gírias do inglês americano!" if slug == "interlagos-f1"
                  else MO_DAU_PT[(k - 1) % 3].format(em=em, de=de))
        lines = [(mo_dau, "excited, cheerful")]
        for j, it in enumerate(items):
            lines.append(((f"{cum_noi(it[0], '!')} Significa {it[4]}." if j < 3 else f"E {cum_noi(it[0], '.')} Significa {it[4]}."), EMO[j]))
        lines.append((f"Você usaria {cum_hoi(items[0][0])}? Conta aqui nos comentários!", "curious, friendly"))
        the = the_cards(items, lambda it: it[4], lambda it: it[4])
        v = TB.build(f"br{k:02d}-{slug}", outfit, nen + "; the whole background softly out of focus, any lettering on signs unreadable.",
                     (title, "GÍRIAS EM INGLÊS"), ("EUA", "INGLÊS AMERICANO"), ("AMERICANOS DIZEM", "SIGNIFICA"), lines, the)
        v["NGUOI_DAY"] = robot(face)
        v["GIONG_DAY"] = giong(gender, "pt")
        v["refs"] = {"NGUOI_DAY": [f"{ROOT_REL}/br/br{k:02d}-nv.webp"], "NEN_PHO": [f"{ROOT_REL}/br/br{k:02d}-bg.webp"]}
        v["HAU_KY"]["ngon_ngu"] = "pt"
        out.append(v)
    return out


def kiem(data):
    for v in data:
        for t in v["LUOT"]:
            assert len(t["text"].split()) <= 20, (v["name"], t["text"])
        for c in v["HAU_KY"]["the"]:
            txt = v["LUOT"][c["luot"]]["text"]
            for key in ("moc_tu", "moc_nghia"):
                assert c[key].lower() in txt.lower(), (v["name"], key, c[key], txt)
        assert all(len(x) <= 18 for x in v["HAU_KY"]["tieu_de"]), (v["name"], v["HAU_KY"]["tieu_de"])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for fn, data in (("BIEN-THE-20-BAI-HOC.json", nhom_bai_hoc()), ("BIEN-THE-20-AN-DO.json", nhom_an_do()), ("BIEN-THE-20-BRAZIL.json", nhom_brazil())):
        kiem(data)
        json.dump(data, open(os.path.join(OUT_DIR, fn), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"Đã ghi {len(data)} biến thể -> {fn}")
        for v in data[:2]:
            print("   ", v["name"], "|", " / ".join(t["text"] for t in v["LUOT"][:2]))


if __name__ == "__main__":
    main()
