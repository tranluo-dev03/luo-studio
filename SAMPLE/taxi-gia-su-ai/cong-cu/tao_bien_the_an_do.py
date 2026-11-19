"""Sinh BIEN-THE-TAXI-AN-DO-20.json: 20 biến thể bản Ấn Độ từ sheet "X0061_20 biến thể lái xe taxi IN" (13/11/2026).
  runtime\\python.exe SAMPLE\\taxi-gia-su-ai\\cong-cu\\tao_bien_the_an_do.py
Khớp KICH-BAN-TAXI-AN-DO.txt (tao_kich_ban_an_do.py): phần 1 20 lượt (lượt n = cảnh n, 5 MARKER), phần 2 9 lượt ghép 2 lớp, phần 3 2 lượt.
Mỗi biến thể đổi tài xế (HOC) + khách nữ (KHACH) theo sheet (ảnh = link Google Drive của sheet). Nhân vật dùng chung: sếp + Priya (Muse, anh/an-do/),
Arjun (anh/ARJUN.png), robot Ava (canh-sat-gia-su-ai/anh/DAY.png). Biến thể 2 tài xế tên Arjun -> đồng nghiệp đổi thành Rahul (người dùng chọn).
Lời giữ nguyên sheet; câu tiếng Anh có "dich" Hindi, câu Hindi có "dich" tiếng Anh (phần 1 + 3), phần 2 không dịch."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "BIEN-THE-TAXI-AN-DO-20.json")
MARKER = "[KHONG LOI]"   # trùng gen.py / post.py của thể loại
CAM = None
NHIN = "keeps the eyes where the clip's EYE LINE says while speaking, never into the lens"


def luot(dong_nghiep):
    dn_hi = {"Arjun": "अर्जुन", "Rahul": "राहुल"}[dong_nghiep]
    return [
        # PHẦN 1 - taxi (tiếng Anh, dịch Hindi)
        (1, "khach", "Can you take a left on Fifth, so we can avoid the traffic?", "decisive, skeptical", "क्या आप फिफ्थ पर लेफ्ट ले सकते हैं, ताकि ट्रैफिक से बच सकें?", {}),
        (1, "hoc", "Fifth? Sorry... I don't understand.", "confused, embarrassed", "फिफ्थ? सॉरी... मुझे समझ नहीं आया।", {}),
        (1, "khach", "Take the left! You missed the turn.", "decisive, surprised", "लेफ्ट लो! आपने मोड़ छोड़ दिया।", {}),
        (1, "khach", "I just told you to take the left.", "decisive", "मैंने अभी कहा था लेफ्ट लेने को।", {}),
        (1, "khach", "Yeah, I'm in a cab. The driver barely speaks English.", "skeptical", "हाँ, मैं टैक्सी में हूँ। ड्राइवर मुश्किल से इंग्लिश बोलता है।", {}),
        (1, "khach", "I have to repeat everything I say.", "skeptical, doubtful", "मुझे हर बात दोहरानी पड़ती है।", {}),
        (1, "hoc", CAM, "", None, {}),         # P: tài xế nhìn điện thoại
        # bến xe
        (1, "quanly", f"{dong_nghiep}, your ratings are the best we've got. Customers love your conversations.", "proud, cheerful",
         f"{dn_hi}, तुम्हारी रेटिंग सबसे अच्छी है। ग्राहकों को तुम्हारी बातें बहुत पसंद हैं।", {}),
        (1, "quanly", "You get our brand-new car!", "excited", "हमारी बिल्कुल नई कार तुम्हें मिलेगी!", {}),
        (1, "arjun", CAM, "", None, {}),       # K: trao chìa khoá
        (1, "arjun", CAM, "", None, {}),       # X: taxi mới
        (1, "hoc", "मुझे भी नई car चाहिए...", "hopeful, hesitant", "I want a new car too...", {}),
        (1, "quanly", "You want the new car? Learn to talk to the customers first.", "playful, proud", "नई कार चाहिए? पहले ग्राहकों से बात करना सीखो।", {}),
        (1, "hoc", CAM, "", None, {}),         # T: tài xế buồn
        # nhà (Hindi, dịch tiếng Anh)
        (1, "con", "पापा, क्या हुआ?", "worried", "Dad, what happened?", {}),
        (1, "hoc", "कुछ नहीं... मैं customers की बात समझ ही नहीं पाता।", "worried, embarrassed", "Nothing... I just can't understand the customers.", {}),
        (1, "con", "पापा, आपको English आती तो है, बस practice की ज़रूरत है।", "warm, encouraging", "Dad, you do know English, you just need practice.", {}),
        (1, "con", "ये देखो, Ava AI, आपकी English AI tutor.", "proud, cheerful", "Look, Ava AI, your English AI tutor.", {}),
        (1, "con", CAM, "", None, {}),         # PH: cận điện thoại
        (1, "con", "इससे ऐसे बात करो जैसे असली teacher से बात कर रहे हो।", "excited", "Talk to it like you're talking to a real teacher.", {}),
        # PHẦN 2 - tài xế + Ava (ghép 2 lớp)
        (2, "day", "Hi! Where are you from?", "cheerful, curious", None, {}),
        (2, "hoc", "I am India.", "hesitant", None, {"fx": "wrong", "icon": "x", "to": "I am India", "c": "red"}),
        (2, "day", "Almost! Say: I am FROM India.", "warm, encouraging", None, {}),
        (2, "hoc", "I am from India!", "proud", None, {"fx": "right", "icon": "check", "to": "from", "c": "green"}),
        (2, "hoc", "लेकिन English classes बहुत महंगी होती हैं... मेरे पास पैसे नहीं हैं।", "worried", None, {"icon": "dollar"}),
        (2, "day", "No problem! No tricks. Just real conversation in English with your AI.", "reassuring, cheerful", None, {}),
        (2, "day", "I correct your grammar and pronunciation while you speak.", "warm", None, {}),
        (2, "day", "Let's practice. A customer wants to go to the airport. What will you say?", "cheerful, upbeat", None, {}),
        (2, "hoc", "Hello sir, where would you like to go today?", "hopeful, delighted", None, {}),
        # PHẦN 3 - kết
        (3, "hoc", "Hello! Where would you like to go today?", "cheerful, confident", "नमस्ते! आज आप कहाँ जाना चाहेंगी?", {}),
        (3, "hoc", "अब मुझे English बोलने से डर नहीं लगता।", "proud, delighted", "Now I'm not afraid of speaking English.", {}),
    ]


TRE = "a warm, friendly young Indian man's voice around 120-145 Hz; his English is slow and broken with a heavy Indian accent, his Hindi natural and fluent"
TRUNG = "a warm, slightly hoarse mature Indian man's baritone around 105-125 Hz; his English is slow and broken with a heavy Indian accent, his Hindi natural and fluent"
GIA = "a gentle, slightly gravelly older Indian man's voice around 100-120 Hz; his English is slow and broken with a heavy Indian accent, his Hindi natural and fluent"
KH_TRE = "a crisp, quick, impatient young Indian woman's voice around 215-245 Hz, fluent English with a refined upper-class Indian accent, clearly higher than the driver"
KH_GIA = "a crisp, haughty, impatient mature Indian woman's voice around 190-220 Hz, fluent English with a refined upper-class Indian accent, clearly higher than the driver"

# (tên tài xế, mô tả EN, giọng, link ảnh | mô tả khách EN, giọng khách, link ảnh)
ROWS = [
    ("Raj", "a stylized 3D-animated young Indian taxi driver of 27, short neat black hair, a small black moustache, warm brown skin, a friendly face, a clean navy-blue polo shirt, khaki trousers", TRE,
     "https://drive.google.com/file/d/18xLq0Bl_hC_KCkSBJxGN-LoliYND6ypu/view?usp=drivesdk",
     "a stylized 3D-animated elegant wealthy Indian woman of 32, a red silk saree with gold embroidery, gold jewellery, a designer handbag, a haughty expression", KH_TRE,
     "https://drive.google.com/file/d/1RURI5zZV7hUBWt6eyUR40tgT4OqM5y0R/view?usp=drivesdk"),
    ("Arjun", "a stylized 3D-animated young Indian taxi driver of 24, neatly combed black hair, clean-shaven, warm brown skin, a bright smile, a clean white shirt, black trousers", TRE,
     "https://drive.google.com/file/d/1D-Aes3QYtUsEUsDfKbgz8bNYhYyWlpuW/view?usp=drivesdk",
     "a stylized 3D-animated wealthy young Indian woman of 28, an elegant navy-blue evening gown, a diamond necklace, her hair in a high bun", KH_TRE,
     "https://drive.google.com/file/d/17k6xvPuqNag-2aZbvff0E5HaS_9Cy5kw/view?usp=drivesdk"),
    ("Vikram", "a stylized 3D-animated young Indian Sikh taxi driver of 29, a neat full black beard, a blue turban, warm brown skin, a clean white kurta", TRE,
     "https://drive.google.com/file/d/1_GvxCHj9EO8n5J48IRY5Uhd6kYnfZXEe/view?usp=drivesdk",
     "a stylized 3D-animated wealthy Indian woman of 35, a pink silk saree, gold bangles, light make-up", KH_TRE,
     "https://drive.google.com/file/d/1g5NpAkN8KcUSQfRzp11F18sEWZ4_v3yx/view?usp=drivesdk"),
    ("Rohan", "a stylized 3D-animated young Indian taxi driver of 25, curly black hair, clean-shaven, warm brown skin, a clean checked shirt, blue jeans", TRE,
     "https://drive.google.com/file/d/1iBWRlTZocW4_nFa9w8wbwd_h-sSghBzP/view?usp=drivesdk",
     "a stylized 3D-animated wealthy young Indian woman of 29, an elegant yellow lehenga, big gold earrings", KH_TRE,
     "https://drive.google.com/file/d/1MO6ZgCVEnIORwC0sy9GPUmbOLzEPXlLw/view?usp=drivesdk"),
    ("Kabir", "a stylized 3D-animated young Indian taxi driver of 26, slicked-back black hair, clean-shaven, warm brown skin, a clean grey crew-neck T-shirt, brown khaki trousers", TRE,
     "https://drive.google.com/file/d/1iXaGiSKx-v42I_UN5c8NdxgqZ_1oqhhM/view?usp=drivesdk",
     "a stylized 3D-animated wealthy Indian woman of 31, an elegant purple silk dress, a gold watch, long wavy hair", KH_TRE,
     "https://drive.google.com/file/d/1F4oTugi8lzm_EqK6LHiRAA5ZH3S1vwQ6/view?usp=drivesdk"),
    ("Aarav", "a stylized 3D-animated young Indian taxi driver of 24, short neat black hair, clean-shaven, warm brown skin, a clean blue shirt, black trousers", TRE,
     "https://drive.google.com/file/d/13A-2HI8YQlluBo55RHcwaSaS66HJJ0gE/view?usp=drivesdk",
     "a stylized 3D-animated wealthy Indian woman of 30, a red silk saree with gold embroidery, gold jewellery, a designer handbag", KH_TRE,
     "https://drive.google.com/file/d/1kdDlquO9vxUBDCk6UQF_m6oxlgrV6iYp/view?usp=drivesdk"),
    ("Vihaan", "a stylized 3D-animated young Indian taxi driver of 26, neatly combed black hair, a small black moustache, warm brown skin, a clean white polo shirt, khaki trousers", TRE,
     "https://drive.google.com/file/d/1Z7PkaTQao0br9Jj6S-0MHfM5zFAhPhqw/view?usp=drivesdk",
     "a stylized 3D-animated wealthy young Indian woman of 27, an elegant wine-red evening gown, a diamond necklace, her hair in a high bun", KH_TRE,
     "https://drive.google.com/file/d/118L3lf9ThZrYniOHBeRZfTenTxAl96i0/view?usp=drivesdk"),
    ("Aditya", "a stylized 3D-animated young Indian taxi driver of 23, slightly wavy black hair, clean-shaven, warm brown skin, a clean checked shirt, blue jeans", TRE,
     "https://drive.google.com/file/d/1Ta4fhjzoEjhIp532S_DcuwPzTP79QKFL/view?usp=drivesdk",
     "a stylized 3D-animated wealthy young Indian woman of 24, an elegant yellow lehenga, big gold earrings", KH_TRE,
     "https://drive.google.com/file/d/1gKKjJ6Cb9_BGaQ511oCjwnTmnCYVGu8K/view?usp=drivesdk"),
    ("Reyansh", "a stylized 3D-animated young Indian taxi driver of 27, slicked-back black hair, a neat full black beard, warm brown skin, a clean grey crew-neck T-shirt, black trousers", TRE,
     "https://drive.google.com/file/d/1Pk70RsOBA933gYyKu9zv41G1dM3_W6jx/view?usp=drivesdk",
     "a stylized 3D-animated wealthy young Indian woman of 28, an elegant purple silk dress, a gold watch, long wavy hair", KH_TRE,
     "https://drive.google.com/file/d/1hyriOk8taKey9wM4oVRc_7jajwAhd7KW/view?usp=drivesdk"),
    ("Ayaan", "a stylized 3D-animated young Indian taxi driver of 25, shoulder-length black hair neatly tied back, clean-shaven, warm brown skin, a clean white kurta, white trousers", TRE,
     "https://drive.google.com/file/d/1PpdQ3IEWQU0cHfWo_Y0sfieO5NgJZBgp/view?usp=drivesdk",
     "a stylized 3D-animated wealthy young Indian woman of 26, a pink silk saree, gold bangles, light make-up", KH_TRE,
     "https://drive.google.com/file/d/1DA8BH829zf0qNTaelBDRLESZucdLcKhv/view?usp=drivesdk"),
    ("Ramesh", "a stylized 3D-animated middle-aged Indian taxi driver of 52, salt-and-pepper hair, a grey-black moustache, warm brown skin, a clean beige shirt, brown trousers", TRUNG,
     "https://drive.google.com/file/d/1W2kgPCRGUSXrnkowfbjtScVr5nz4lSeV/view?usp=drivesdk",
     "a stylized 3D-animated wealthy middle-aged Indian lady of 55, a purple silk saree with gold embroidery, pearl jewellery", KH_GIA,
     "https://drive.google.com/file/d/1IZrytGqqCby0cEslWiszcHvFQpeumqgc/view?usp=drivesdk"),
    ("Suresh", "a stylized 3D-animated middle-aged Indian taxi driver of 48, slightly balding, a thick black moustache, warm brown skin, a clean white kurta, white trousers", TRUNG,
     "https://drive.google.com/file/d/1Qr1As2mWNS6ATnY14Jgwqwh5357PV4wI/view?usp=drivesdk",
     "a stylized 3D-animated wealthy middle-aged Indian woman of 50, a blue silk saree, a gold necklace, her hair in a neat bun", KH_GIA,
     "https://drive.google.com/file/d/1XBPOZV26bPe1oPjfS5nCjSdeVNWk2Xa7/view?usp=drivesdk"),
    ("Mohan", "a stylized 3D-animated older Indian taxi driver of 58, grey hair, a short grey beard, warm brown skin, a clean light-blue shirt, grey trousers", GIA,
     "https://drive.google.com/file/d/1uFvxNa4sIfWLM0Ynat79pbGRkZuDGOir/view?usp=drivesdk",
     "a stylized 3D-animated wealthy older Indian woman of 60, a red silk saree, gold jewellery, grey hair in a high bun", KH_GIA,
     "https://drive.google.com/file/d/17aiVLaONI8qK_OF4WtdSbqqRT_9HEFCG/view?usp=drivesdk"),
    ("Devendra", "a stylized 3D-animated middle-aged Indian taxi driver of 45, black hair with grey streaks, clean-shaven, warm brown skin, a clean brown polo shirt, black trousers", TRUNG,
     "https://drive.google.com/file/d/1tEINjCsljmu0Nj7QPoqC2elluv7veSnr/view?usp=drivesdk",
     "a stylized 3D-animated wealthy middle-aged Indian woman of 48, an elegant orange silk saree, pearl earrings, light make-up", KH_GIA,
     "https://drive.google.com/file/d/1mttQ-ZAsAk9xhmVJa6jDvdbVaJXKa7gy/view?usp=drivesdk"),
    ("Prakash", "a stylized 3D-animated middle-aged Indian taxi driver of 55, salt-and-pepper hair, glasses, clean-shaven, warm brown skin, a clean white shirt, khaki trousers", TRUNG,
     "https://drive.google.com/file/d/1mIZtqsHmi_-kzeKAxn2Ldo83fboVXPu8/view?usp=drivesdk",
     "a stylized 3D-animated wealthy middle-aged Indian woman of 57, a deep-pink silk saree, a gold necklace, a calm expression", KH_GIA,
     "https://drive.google.com/file/d/1HY7Cm-8Mav6_0ihZqXx9AJ8sBt3d_Jcb/view?usp=drivesdk"),
    ("Rajesh", "a stylized 3D-animated middle-aged Indian taxi driver of 50, salt-and-pepper hair, a grey-black moustache, warm brown skin, a clean beige shirt, brown trousers", TRUNG,
     "https://drive.google.com/file/d/1mOaua-S_qCqdIT9_cJYWTiz8fyNsfjg-/view?usp=drivesdk",
     "a stylized 3D-animated wealthy older Indian woman of 58, a purple silk saree with gold embroidery, pearl jewellery, grey hair in a high bun", KH_GIA,
     "https://drive.google.com/file/d/1Df_AZpHXpyWUEInTRSzBxG7_HcttcEvT/view?usp=drivesdk"),
    ("Mahesh", "a stylized 3D-animated middle-aged Indian taxi driver of 54, long black hair in a low bun, a thick black moustache, warm brown skin, a clean white kurta, white trousers", TRUNG,
     "https://drive.google.com/file/d/1LTp_22019iz0_mBwvoL53brm67IqnDsL/view?usp=drivesdk",
     "a stylized 3D-animated wealthy middle-aged Indian woman of 52, an elegant orange silk saree, a gold necklace, her hair in a neat bun", KH_GIA,
     "https://drive.google.com/file/d/1W2EkuST4XYkcQyZrGuq47zM8A6ZVelBb/view?usp=drivesdk"),
    ("Anil", "a stylized 3D-animated middle-aged Indian taxi driver of 47, shoulder-length black hair, glasses, clean-shaven, warm brown skin, a clean light-purple shirt, black trousers", TRUNG,
     "https://drive.google.com/file/d/1PZxQ-6Y1u3Ul1p3952z21ffB2nPZUDA5/view?usp=drivesdk",
     "a stylized 3D-animated wealthy middle-aged Indian woman of 49, a deep-pink silk saree, pearl earrings, light make-up", KH_GIA,
     "https://drive.google.com/file/d/10JqyyteoMdZamvSLef2CJ6tTMrDjUuUt/view?usp=drivesdk"),
    ("Vijay", "a stylized 3D-animated older Indian taxi driver of 58, grey hair in a neat bun, a short grey beard, glasses, warm brown skin, a clean blue kurta", GIA,
     "https://drive.google.com/file/d/1Uskgx3RcMcRJanyU2nos2FjP7uLiv-7G/view?usp=drivesdk",
     "a stylized 3D-animated wealthy older Indian woman of 60, a red silk saree, gold jewellery, grey hair in a high bun", KH_GIA,
     "https://drive.google.com/file/d/1U3j-RI42k7o1SDdrej_atSc_mnnWDHlg/view?usp=drivesdk"),
    ("Sanjay", "a stylized 3D-animated middle-aged Indian taxi driver of 49, black hair tied in a high bun, a black moustache, warm brown skin, a clean orange shirt, khaki trousers", TRUNG,
     "https://drive.google.com/file/d/1-oDez-S0flYZO9EuV3KPcqEUSYGKPXBj/view?usp=drivesdk",
     "a stylized 3D-animated wealthy middle-aged Indian woman of 53, a purple silk saree, a gold necklace, a calm expression", KH_GIA,
     "https://drive.google.com/file/d/1KCIVEq6mM3045ZTmUXi2PnaMrsbqUPuW/view?usp=drivesdk"),
]

CHUNG = {
    "VAI_HOC": "taxi driver",
    "POS_HOC": "driver-seat",
    "NGHE_HOC": "keeps the mouth closed and looks where the clip's EYE LINE says (at the road, at the floor or at whoever is speaking), small natural blinks, hands where the clip puts them",
    "NHIN_HOC": NHIN,
    "NHIN_HOC@2": "looks into the lens, as if talking to the AI tutor on the phone mounted on the dashboard",
    "TEN_KHACH": "the passenger",
    "VAI_KHACH": "taxi passenger",
    "POS_KHACH": "back-seat",
    "NGHE_KHACH": "keeps the mouth closed, the phone at her ear, looking out of the side window",
    "NHIN_KHACH": NHIN,
    "TEN_QUANLY": "the manager",
    "NGUOI_QUANLY": "a stylized 3D-animated Indian taxi-company manager in his late fifties, neatly combed salt-and-pepper hair, a thick grey moustache, warm brown skin, a navy-blue Nehru jacket over a white shirt, dark trousers, a plain brown clipboard and a pen",
    "GIONG_QUANLY": "a hearty, confident older Indian man's voice around 110-130 Hz, fluent English with a warm Indian accent",
    "VAI_QUANLY": "taxi company manager",
    "POS_QUANLY": "depot-centre",
    "NGHE_QUANLY": "keeps the mouth closed and looks at whoever is speaking, holding his clipboard",
    "NHIN_QUANLY": NHIN,
    "NGUOI_ARJUN": "a stylized 3D-animated young Indian man in his mid-twenties, slim, short neat black hair, a trimmed black beard, a light-grey button-up shirt with rolled sleeves, dark jeans, a silver wristwatch",
    "GIONG_ARJUN": "a smooth, light, smug young man's voice around 140-160 Hz",
    "VAI_ARJUN": "young taxi driver",
    "POS_ARJUN": "depot-right",
    "NGHE_ARJUN": "keeps the mouth closed with a confident smile, looking at whoever is speaking",
    "NHIN_ARJUN": NHIN,
    "TEN_CON": "Priya",
    "NGUOI_CON": "a stylized 3D-animated Indian teenage girl about fifteen, long black hair in a single neat braid, big warm brown eyes, warm brown skin, a mustard-yellow cotton kurta with small white printed flowers and white leggings, barefoot",
    "GIONG_CON": "a bright, gentle, clear teenage girl's voice around 240-270 Hz, natural Hindi, caring and upbeat",
    "VAI_CON": "daughter",
    "POS_CON": "living-room",
    "NGHE_CON": "keeps the mouth closed and looks at her father with a caring face",
    "NHIN_CON": NHIN,
    "TEN_DAY": "Ava",
    "NGUOI_DAY": "a sleek feminine humanoid robot with a smooth glossy pearl-white bald head and a softly human-like face, pale blue eyes, soft pale lips that open and move naturally with every word whenever it speaks, thin panel seams on the head, a black segmented mechanical neck, white armoured shoulders with thin glowing blue seams (copy the reference image); realistic 3D render",
    "GIONG_DAY": "a calm, clear, friendly young woman's voice around 180-210 Hz with a very slight synthetic digital sheen, clear neutral English",
    "VAI_DAY": "AI tutor",
    "NHIN_DAY": "looks straight into the lens, as if talking to the person on the call",
    "NEN_DAY": "a plain deep black background with one thin soft white glowing arc behind the head",
    "NEN_HOC": "the inside of a black-and-yellow Mumbai taxi on a sunny afternoon: dark seats, and through the rear window a busy Mumbai street with black-and-yellow cabs and old apartment buildings, softly out of focus",
    "XE": "a classic black-and-yellow Mumbai taxi (black body, yellow roof) with dark seats and no roof sign",
    "NEN_PHO": "a sunny busy Mumbai street: colourful shop fronts, old apartment blocks with balconies, palm trees, other black-and-yellow cabs far behind",
    "NEN_GARA": "a big Mumbai taxi depot: grey concrete floor, a high tin roof with long tube lights, metal lockers and a notice board on the wall, a wide open rolling shutter with black-and-yellow taxis and a street outside",
    "NEN_NHA": "a cosy Indian apartment living room: a sofa with colourful cushions, a low wooden coffee table with an open book and a small glass of tea, a window with light cotton curtains, a potted plant",
    "DAO_DIEN_THOAI_KH": "a gold-coloured smartphone",
    "DAO_DIEN_THOAI_TX": "an old black smartphone with a glowing screen",
    "DAO_CHIA_KHOA": "a set of two new silver car keys on a ring with a black key fob",
    "DAO_COC": "a plain white ceramic cup",
    "DAO_DIEN_THOAI": "a blue smartphone whose screen shows only a friendly white humanoid robot face on a plain blue background, with no text, no buttons and no icons",
    "nguoi_theo_canh": True,
}

ANH_CHUNG = {"QUANLY": "SAMPLE/taxi-gia-su-ai/anh/an-do/QUANLY.png", "ARJUN": "SAMPLE/taxi-gia-su-ai/anh/ARJUN.png",
             "CON": "SAMPLE/taxi-gia-su-ai/anh/an-do/CON.png", "DAY": "SAMPLE/canh-sat-gia-su-ai/anh/DAY.png"}


def ten_slug(s):
    return s.lower().replace(" ", "-")


def main():
    out = []
    for i, (ten, hoc, giong, anh_hoc, khach, giong_kh, anh_kh) in enumerate(ROWS, 1):
        dn = "Rahul" if ten == "Arjun" else "Arjun"
        v = {"name": f"taxi-in-{i:02d}-{ten_slug(ten)}"}
        v.update(CHUNG)
        v.update({"TEN_HOC": ten, "NGUOI_HOC": hoc, "GIONG_HOC": giong, "NGUOI_KHACH": khach, "GIONG_KHACH": giong_kh, "TEN_ARJUN": dn})
        v["LUOT"] = []
        for phan, who, text, emo, dich, extra in luot(dn):
            if text is None:
                t = {"who": who, "text": MARKER, "emo": "", "fx": "none", "phan": phan}
            else:
                t = {"who": who, "text": text, "emo": emo, "fx": "none", "phan": phan}
                t.update(extra)
                if dich:
                    t["dich"] = dich
            v["LUOT"].append(t)
        refs = {"NGUOI_HOC": [anh_hoc], "NGUOI_KHACH": [anh_kh]}
        refs.update({f"NGUOI_{k}": [p] for k, p in ANH_CHUNG.items() if os.path.exists(os.path.join(ROOT, p))})
        v["refs"] = refs
        out.append(v)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = out[0]
    print(f"Đã ghi {os.path.normpath(OUT)}: {len(out)} biến thể, {len(v['LUOT'])} lượt/biến thể; ảnh chung: {', '.join(sorted(k for k in v['refs'] if k not in ('NGUOI_HOC', 'NGUOI_KHACH')))}")
    for p in (1, 2, 3):
        print(f"Người nói phần {p}:", " ".join("-" if t["text"] == MARKER else t["who"] for t in v["LUOT"] if t["phan"] == p))


if __name__ == "__main__":
    main()
