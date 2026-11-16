"""Sinh 4 file biến thể từ 2 bảng CSV (nguon-csv/), cùng khuôn với tao_bien_the_20.py:
  X0076 "40 biến thể Sân bay_Check luggage" (Mexico, lời thoại tiếng Anh như biến thể mẫu)
      -> BIEN-THE-SOI-HANH-LY-X0076-40-KHONG-BE.json  (biến thể 11-40, không địu con) dùng với KICH-BAN-SOI-HANH-LY-GIA-SU-AI-KHONG-BE.txt
      -> BIEN-THE-SOI-HANH-LY-X0076-40-DIU-CON.json   (biến thể 1-10, người mẹ địu con) dùng với KICH-BAN-SOI-HANH-LY-GIA-SU-AI.txt
  X0077 "20 biến thể Sân bay_Check luggage HINDI" (Ấn Độ, lời thoại Hindi xen tiếng Anh, chép từ ô kịch bản đầu file CSV)
      -> BIEN-THE-SOI-HANH-LY-X0077-HINDI-20-KHONG-BE.json (biến thể 6-20)
      -> BIEN-THE-SOI-HANH-LY-X0077-HINDI-20-DIU-CON.json  (biến thể 1-5)
Chia đôi theo có/không em bé vì hai kịch bản (.txt) khác nhau (token DAO_BE / HE_HOC...), giống bộ 20 biến thể trước.
Ảnh tham chiếu NGUOI_HOC = link Drive ở cột cuối CSV (Studio tự đổi sang link tải thẳng), NGUOI_DAY = ROBOT-GIA-SU-AI.png.
Mô tả ngoại hình tiếng Việt trong CSV được dịch sang tiếng Anh ở bảng dưới; hàm kiem_tra() đối chiếu tuổi với CSV.
Chạy: .venv\\Scripts\\python.exe SAMPLE\\soi-hanh-ly-gia-su-ai\\cong-cu\\tao_bien_the_x0076_x0077.py"""
import copy
import csv
import json
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CSV_MEXICO = os.path.join(D, "nguon-csv", "X0076-MEXICO-40.csv")
CSV_HINDI = os.path.join(D, "nguon-csv", "X0077-HINDI-20.csv")
MAU_ALL = json.load(open(os.path.join(D, "BIEN-THE-SOI-HANH-LY-GIA-SU-AI.json"), encoding="utf-8"))
MAU = MAU_ALL[0]
ROBOT = {"url": "SAMPLE/soi-hanh-ly-gia-su-ai/ROBOT-GIA-SU-AI.png", "name": "ROBOT-GIA-SU-AI.png"}   # đường dẫn tương đối từ thư mục gốc Studio: chạy được trên máy khác
CHUNG = ["TEN_CANBO", "NGUOI_CANBO", "GIONG_CANBO", "VAI_CANBO", "POS_CANBO", "NGHE_CANBO", "DAO_VALI", "DAO_VALI_2", "DAO_DIEN_THOAI",
         "NEN_SOI", "NEN_HOC", "TEN_DAY", "NGUOI_DAY", "NEN_DAY", "NHIN_DAY"]
GIONG_DAY_EN = ("a bright, light, friendly young woman's voice, clearly lighter than the traveller's, smooth and clear with only a faint synthetic polish, "
                "patient and encouraging like a kind language teacher on a video call, neutral American accent")
GIONG_DAY_HI = ("a bright, light, friendly young woman's voice, clearly lighter than the traveller's, smooth and clear with only a faint synthetic polish, "
                "patient and encouraging like a kind language teacher on a video call, natural Hindi for the Hindi sentences and clear neutral English for the English ones")
ACCENT_MX = "a natural Mexican accent with Spanish vowels and a soft r, not exaggerated"
ACCENT_IN = "a natural Indian accent with Hindi intonation and soft consonants, not exaggerated"
REAL = "a real person, not an actor"
TRAITS = ["soft and a little shy", "warm and easygoing", "clear and brisk", "calm and steady", "bright and chatty", "gentle and polite"]

# ---------------------------------------------------------------------------------------------------------------------------
# Bảng X0076 (Mexico): (số, tuổi, ngoại hình EN, túi, em bé EN hoặc None)
# ---------------------------------------------------------------------------------------------------------------------------
def baby(color):
    return (f"a sleeping baby snug on her chest in {color} fabric wrap carrier, the baby's head tucked against the mother's chest with the face turned fully inward "
            "and NOT visible, only the back of the head with dark hair and the nape seen, the baby's legs tucked inside the carrier")


MX = [
    (1, 25, "a Mexican woman of about 25, about 155 cm, petite and slightly chubby, a round face with full cheeks and a short chin, a small slightly upturned nose, big round brown eyes, thick straight eyebrows, light brown olive skin with a few small natural blemishes, jet-black shoulder-length hair cut straight with thick bangs, a cream cotton round-neck T-shirt, light-blue wide-leg jeans and white sneakers",
     "a large beige canvas tote bag", baby("a plain beige")),
    (2, 26, "a Mexican woman of about 26, about 168 cm, tall and slim with level shoulders, a long oval face with slightly hollow cheeks, a wide forehead and a long, slightly pointed chin, a high straight nose, slightly slanted almond-shaped brown eyes, thin arched eyebrows, deep bronze skin with light freckles on both cheeks, chestnut-brown hair down to the middle of the back in big loose waves with a deep side parting, a loose ivory linen shirt, wide earth-brown linen trousers and brown leather sandals",
     "a brown linen tote bag", baby("an ash-grey")),
    (3, 27, "a Mexican woman of about 27, about 162 cm, a full figure with wide hips and a medium waist, a diamond-shaped face with high cheekbones, a clear jawline and a slightly pointed chin, full lips, slightly deep-set dark brown eyes, honey-brown skin with a few small pigment spots, thick naturally curly black hair to the shoulders dyed copper-brown ombre at the ends with the black roots clearly visible, a black tank top under an open dark-blue denim jacket, straight black jeans and short black leather boots",
     "a black canvas tote bag", baby("a navy-blue")),
    (4, 28, "a Mexican woman of about 28, about 160 cm, sturdy with full upper arms and sloping shoulders, a square face with a wide jaw, a narrow forehead, slightly asymmetric cheeks and a round chin, a wide nose, an upper lip thinner than the lower lip, dark brown skin with visible pores, a short black chin-length bob with a centre parting, neatly combed, a thin knitted sweater in dusty pink, straight dark-blue jeans, minimal white sneakers and small gold earrings",
     "a tan leather tote bag", baby("a burgundy-red")),
    (5, 29, "a Mexican woman of about 29, about 172 cm, tall with long legs and narrow hips, a rectangular face with a high forehead, a square jaw and a wide chin, a long slightly bumpy nose, small deep-set brown eyes, thick straight eyebrows, medium olive-brown skin with light acne marks, a short layered black wolf cut with a longer nape and messy natural bangs, an oversized plain white T-shirt, loose khaki cargo trousers with many pockets, chunky grey-white sneakers and a thin silver chain",
     "a black canvas tote bag", baby("a mustard-yellow")),
    (6, 30, "a Mexican woman of about 30, about 158 cm, short and stocky with a gently rounded belly, a pear-shaped face with a wide lower jaw, a narrow forehead, chubby cheeks and a round chin, round brown eyes, a short nose, light yellowish-brown skin with faint wrinkles around the eyes, chocolate-brown hair past the shoulders in soft waves with a centre parting, a mint-green cotton blouse with three-quarter sleeves, straight white trousers and cream loafers",
     "a cream leather tote bag", baby("a chocolate-brown")),
    (7, 31, "a Mexican woman of about 31, about 165 cm, an average, slightly full build with medium-wide shoulders, an oval face with moderate cheekbones and an oval chin, natural grooves on the lips, big brown eyes with clear eyelids, unevenly sun-tanned brown skin with visible pores and a few dark marks, thick black hair past the shoulders in a low ponytail with a few loose strands, a plain olive-green polo shirt, straight beige khaki trousers and simple sports shoes",
     "a dark-green canvas tote bag", baby("a terracotta-orange")),
    (8, 25, "a Mexican woman of about 25, about 170 cm, slim with a long neck and small shoulders, a heart-shaped face with a wide forehead, a small pointed chin and high cheekbones, a small straight nose, big brown eyes with long curled lashes, light brown skin with a pink glow, smooth, glossy straight black hair down to the middle of the back with a centre parting, a light-yellow cotton midi dress with a small flower print under a thin cream cardigan, white low sandals",
     "a pale-pink canvas tote bag", baby("a dusty-pink")),
    (9, 27, "a Mexican woman of about 27, about 163 cm, a strong, athletic build with medium-wide shoulders, a long round face with moderately full cheeks and a slight double chin, a medium-wide nose, dark brown eyes, thick straight eyebrows, deep bronze skin with small age spots, very short tight black curls ending at the ears with curly bangs over the forehead, a cream-white sports T-shirt, slim black joggers and black-and-white sports sneakers",
     "a black sports tote bag", baby("a plain black")),
    (10, 30, "a Mexican woman of about 30, about 157 cm, small and thin with narrow shoulders and slender arms, a small narrow oval face with slightly hollow cheeks and a small pointed chin, small brown eyes with slightly drooping lids, thin lips, deep olive-brown skin with fine wrinkles around the eyes, black hair in a high, slightly messy bun with a few strands falling on both sides of the face, a long-sleeved red-and-white checked shirt with the sleeves slightly rolled, faded wide-leg blue jeans and white sneakers",
     "a faded red-and-white cloth tote bag", baby("a brown-and-white striped")),
    (11, 26, "a Mexican woman of about 26, about 165 cm, a sturdy build with broad shoulders and strong arms, a square face with a clear jawline and high cheekbones, deep sun-tanned brown skin with a light smudge of dust on one cheek, long black hair tied in a neat high ponytail under a white safety helmet, a grey T-shirt, an orange high-visibility reflective vest, dark-blue multi-pocket work jeans, brown safety boots and a work glove on one hand",
     "a worn dark-grey canvas shoulder bag", None),
    (12, 28, "a Mexican woman of about 28, about 160 cm, small but wiry, a round face with sunburnt red cheeks, a slightly flat nose, round brown eyes and thick eyebrows, sunburnt copper-brown skin, brown-black hair in a long braid over one shoulder under a straw wide-brimmed hat, a long-sleeved blue-and-white checked shirt, faded jeans, brown rubber boots and an earth-brown coarse-cloth apron with a pair of gardening gloves tucked into its pocket",
     "a small brown canvas shoulder bag", None),
    (13, 32, "a Mexican woman of about 32, about 158 cm, a slightly plump build with a round belly, a chubby face with a double chin and slightly sagging cheeks, small slightly deep-set brown eyes with clear eye bags, olive-brown skin with forehead wrinkles, black hair with a few grey strands in a low bun under a dark-blue headscarf, a dark-grey polo shirt, wide black trousers, black sneakers, a black apron and a yellow rubber glove on one hand",
     "a black fabric shoulder bag", None),
    (14, 35, "a Mexican woman of about 35, about 163 cm, a solid build with broad shoulders, a wide face with full cheeks, a round chin, a wide nose, full lips and dark brown eyes, honey-brown skin with a small old burn scar on one forearm, short black hair ending at the ears under a low white chef's hat, a short-sleeved white chef's jacket, black small-check trousers, black non-slip shoes and a long white apron to the knees",
     "a black nylon shoulder bag", None),
    (15, 25, "a Mexican woman of about 25, about 155 cm, short and small, an oval face with big long-lashed brown eyes, a small nose, natural pink lips and a dimple on one cheek, light brown skin, long straight black hair tied in two low braids on both sides, a white blouse with traditional Mexican floral embroidery and puffed sleeves, a long bright-red pleated skirt and brown leather sandals",
     "a cream cloth crossbody bag", None),
    (16, 38, "a Mexican woman of about 38, about 170 cm, tall and large-framed with broad shoulders, a long face with high cheekbones and a long chin, small deep-set brown eyes, straight thick eyebrows, a small scar on the left eyebrow, dark brown skin with many fine wrinkles, short black pixie-cut hair slightly grey at the temples, a black T-shirt, loose olive-green cargo trousers, black work boots and a brown tool belt",
     "a black canvas shoulder bag", None),
    (17, 30, "a Mexican woman of about 30, about 162 cm, an average build, a diamond-shaped face with sharp high cheekbones and a pointed chin, thin lips, slightly slanted almond-shaped brown eyes, light olive-brown skin with light freckles, chestnut-brown hair to the shoulders in soft waves, half tied up, a white T-shirt under a see-through pale-blue plastic apron down to the knees, light-blue jeans, white sneakers and blue rubber gloves",
     "a grey canvas shoulder bag", None),
    (18, 27, "a Mexican woman of about 27, about 168 cm, slim, a long oval face with slightly hollow cheeks and a wide forehead, a high straight nose, big brown eyes, full lips, bronze-brown skin, long black hair tied in a neat low ponytail with a black hairband, a housekeeping uniform: a short-sleeved white shirt, a black knee-length skirt, a small white apron over the stomach, flat black shoes and a white glove on one hand",
     "a small black shoulder bag", None),
    (19, 40, "a Mexican woman of about 40, about 160 cm, a slightly thin build with sloping shoulders, a long narrow face with high cheekbones and hollow cheeks, a small chin, clear wrinkles around the eyes and mouth, sun-tanned dark brown skin with many age spots, salt-and-pepper hair in a low bun under a dark-green baseball cap (a cap worn on the head), an earth-brown long-sleeved T-shirt, olive-green khaki trousers, brown boots, an olive-green gardening apron with a front pocket and a pair of cloth gloves tucked into it",
     "a tan canvas shoulder bag", None),
    (20, 29, "a Mexican woman of about 29, about 157 cm, small, a small round face with big round brown eyes, a short nose, pursed lips and chubby cheeks, light olive-brown skin, softly curly black hair to the shoulders with a red hair clip, a turmeric-yellow short-sleeved blouse, straight black trousers, black loafers, a yellow tailor's measuring tape around the neck and a pair of scissors and thread in the shirt pocket",
     "a brown fabric shoulder bag", None),
    (21, 33, "a Mexican woman of about 33, about 164 cm, a slightly heavy build, a slightly square face with clear cheekbones and a slight double chin, deep-set brown eyes with eye bags, lips with natural grooves, unevenly sun-tanned brown skin, thick black hair in a low bun under a black hairnet, a grey T-shirt, a long black rubber apron, black jeans, black non-slip shoes and yellow rubber gloves",
     "a dark-grey nylon shoulder bag", None),
    (22, 25, "a Mexican woman of about 25, about 166 cm, tall and slim with long legs, a rectangular face with a high forehead, a square jaw and a wide chin, a long slightly bumpy nose, small deep-set brown eyes, medium olive-brown skin, a straight black bob ending at the chin with a centre parting, a bright-red windbreaker with reflective strips over a black T-shirt, black joggers and red-and-white sneakers",
     "a black delivery bag worn across the body", None),
    (23, 36, "a Mexican woman of about 36, about 159 cm, a heavy build with a big belly, a broad chubby face with slightly sagging cheeks, a clear double chin, a flat nose, small brown eyes, dark brown skin with many wrinkles, black hair with grey strands cut at the ears under a small red flower-print headscarf, a big purple flower-print blouse, loose black trousers, brown sandals and a blue floral cloth apron",
     "a faded brown cloth shoulder bag", None),
    (24, 31, "a Mexican woman of about 31, about 161 cm, a solid build, a pear-shaped face with a wide lower jaw, a narrow forehead, slightly asymmetric cheeks and a round chin, dark brown eyes with heavy lids, dark brown skin with visible pores, long black hair in a high ponytail under a white hair-net cap, a long-sleeved white T-shirt, navy trousers, white sneakers, white cloth gloves and a face mask pulled down to the chin",
     "a navy fabric shoulder bag", None),
    (25, 27, "a Mexican woman of about 27, about 163 cm, an average build, an oval face with moderate cheekbones and an oval chin, big gentle brown eyes, a faint smile, thin arched eyebrows, light yellowish-brown skin, long brown-black hair to the middle of the back in big loose waves with a side parting, light-blue medical scrubs, straight white trousers, white sneakers and a black wristwatch",
     "a black leather shoulder bag", None),
    (26, 39, "a Mexican woman of about 39, about 167 cm, tall with medium-wide shoulders, a long face with hollow cheeks and a long chin, a high slightly hooked nose, small brown eyes with drooping lids, a small white paint spot on the left cheek, dark bronze-brown skin, short brown-black hair at the nape under a white baseball cap with paint stains, an old white T-shirt with blue paint stains, faded white multi-pocket jeans, white boots and a cloth work glove on one hand",
     "a worn canvas shoulder bag with a few paint spots", None),
    (27, 28, "a Mexican woman of about 28, about 156 cm, short, a heart-shaped face with a wide forehead, a pointed chin and high cheekbones, big brown eyes, full pink lips, honey-brown skin, long black hair in two braids on both sides with a small white flower crown on the head, a short-sleeved white T-shirt, a long small-print blue skirt, a cream cloth apron and brown sandals",
     "a cloth tote bag holding a few fresh flowers", None),
    (28, 34, "a Mexican woman of about 34, about 162 cm, a slightly thin build, a long narrow face with high cheekbones, sunken brown eyes with clear eye bags and a tired look, thin lips, dark olive-brown skin, straight black hair to the shoulders in a low ponytail, a navy-blue polo shirt, black trousers, black sneakers and a black apron with a yellow cleaning cloth tucked into it",
     "a black fabric shoulder bag", None),
    (29, 25, "a Mexican woman of about 25, about 164 cm, a full figure with wide hips, a wide round face with chubby cheeks, a short chin, a small upturned nose, round brown eyes, light brown skin with a few small spots, jet-black shoulder-length hair cut straight with thick bangs under a white hair-net cap, a pastel-pink T-shirt, a white apron with flour stains, light-blue jeans, white sneakers and a light dusting of white flour on the hands",
     "a cream canvas shoulder bag", None),
    (30, 37, "a Mexican woman of about 37, about 169 cm, big and strong with very broad shoulders and thick arms, a broad square face with a clear jawline, a double chin, a wide nose, slightly deep-set dark brown eyes, a small scar on the chin, sun-tanned dark brown skin, short black hair ending at the ears tied back at the nape, a grey tank top under an open dark-blue denim jacket, dark-blue work jeans, brown boots and brown leather work gloves",
     "a dark canvas shoulder bag", None),
    (31, 70, "a Mexican woman of about 70, about 158 cm, slightly thin with narrow shoulders and a slight stoop, a long narrow face with high cheekbones, hollow cheeks and a small chin, deep wrinkles around the eyes and mouth, clear age spots, dark brown skin, almost completely white hair in a short chin-length bob with a side parting, neatly combed, a cream cotton T-shirt under a thin navy-blue cardigan, straight dark-blue jeans and minimal white sneakers",
     "a small brown leather shoulder bag", None),
    (32, 72, "a Mexican woman of about 72, about 155 cm, short and slightly plump with rounded shoulders, a wide face with a slight double chin and sagging cheeks, small wrinkles all over the face, clear eye bags, sun-tanned brown skin, thick salt-and-pepper hair cut at the nape, naturally a little wavy, a pale-pink small-flower shirt, loose beige khaki trousers and simple brown sandals",
     "a faded red cloth shoulder bag", None),
    (33, 74, "a Mexican woman of about 74, about 160 cm, thin with sloping shoulders and small arms, a long face with high cheekbones, thin lips, slightly sunken eyes with gently drooping lids, dark brown skin with many age spots, thin grey-and-black hair in a low bun at the nape with a few loose wisps, a pale-yellow cotton blouse, loose earth-brown trousers and old but clean black walking shoes",
     "a dark-green cloth shoulder bag", None),
    (34, 76, "a Mexican woman of about 76, about 152 cm, small with a slightly curved back, an oval face with sagging cheeks and a small chin, deep wrinkles and clear nasolabial folds, wrinkles on the neck, olive-brown skin, mostly grey hair cut short at the ears and a little thin on top, a thin ash-grey cardigan over a white T-shirt, dark trousers and low flat black shoes",
     "a small black leather shoulder bag", None),
    (35, 78, "a Mexican woman of about 78, about 163 cm, tall and thin, a long narrow face with a high forehead, a clear jawline, deeply hollow cheeks, sunken eyes, thin silver eyebrows and thin lips, dark brown skin with many brown spots, completely white hair to the shoulders in a low ponytail with a centre parting, a thin light-purple knitted sweater, wide black trousers, black loafers and a thin cream shawl over the shoulders",
     "a structured black leather shoulder bag", None),
    (36, 80, "a Mexican woman of about 80, about 150 cm, very short with a clearly bent back, a small round face with sagging cheeks and a double chin, deep wrinkles all over the face, hands with age spots and prominent veins, dark brown skin, short white slightly curly hair ending at the ears, a long-sleeved light-sky-blue blouse, a dark-brown ankle-length skirt, low black shoes and a thin white headscarf",
     "a small cream cloth shoulder bag", None),
    (37, 71, "a Mexican woman of about 71, about 166 cm, an average, slightly full build, a slightly square face with clear cheekbones and a wide chin, big brown eyes with drooping lids, lips with grooves, wrinkles around the eyes, unevenly sun-tanned brown skin, black hair with a lot of grey past the shoulders in a low ponytail, a plain burgundy polo shirt, faded blue jeans and simple white sports shoes",
     "a brown fabric shoulder bag", None),
    (38, 73, "a Mexican woman of about 73, about 157 cm, a slightly plump build, a diamond-shaped face with sharp high cheekbones and a small pointed chin, almond-shaped brown eyes, curved silver eyebrows, honey-brown skin with light age spots, a salt-and-pepper chin-length bob with a deep side parting and the ends curled under, a cream silk shirt with a straight cut, wide black dress trousers, brown loafers, small gold earrings and a fake pearl necklace",
     "a small brown leather handbag", None),
    (39, 75, "a Mexican woman of about 75, about 159 cm, an average build, an oval face with slightly hollow cheeks, a wide forehead and a long chin, a high nose, small brown eyes with drooping lids, light yellowish-brown skin with light wrinkles, brown-grey hair down to the middle of the back in a low braid over one shoulder, a moss-green knitted sweater, beige khaki trousers, white sneakers and a thin mustard-yellow scarf",
     "a tan canvas shoulder bag", None),
    (40, 79, "a Mexican woman of about 79, about 154 cm, short and thin with narrow shoulders, a long face with high cheekbones, hollow cheeks, a small pointed chin and thin lips, slightly sunken eyes, a calm composed look, dark brown skin with many deep wrinkles, white hair in a neat high bun at the back of the head with a small silver hairpin, a white cotton T-shirt under a thin earth-brown woollen jacket to the hips, wide black trousers and black walking shoes",
     "a small brown leather handbag", None),
]

# ---------------------------------------------------------------------------------------------------------------------------
# Bảng X0077 (Ấn Độ): (số, tuổi, ngoại hình EN, túi, em bé EN hoặc None)
# ---------------------------------------------------------------------------------------------------------------------------
IN = [
    (1, 25, "an Indian woman of about 25, about 155 cm, petite and slightly chubby, a round face with full cheeks and a short chin, a small slightly upturned nose, big round dark-brown eyes, thick straight eyebrows, a small red bindi in the middle of the forehead, light wheat-brown smooth skin, jet-black shoulder-length hair cut straight with thick bangs, a short-sleeved turmeric-yellow cotton kurta, white salwar trousers, an earth-orange dupatta over one shoulder and brown sandals",
     "a large beige cloth tote bag", baby("a plain beige")),
    (2, 27, "an Indian woman of about 27, about 168 cm, tall and slim with level shoulders, a long oval face with slightly hollow cheeks, a wide forehead and a long, slightly pointed chin, a high straight nose, slightly slanted almond-shaped dark-brown eyes, thin curved eyebrows, no bindi, deep copper-brown skin, black hair down to the middle of the back in big loose waves with a deep side parting, tied in a low ponytail, a burgundy cotton saree with a gold border and a short-sleeved blouse of the same colour, gold-bronze sandals",
     "a brown cloth tote bag", baby("an ash-grey")),
    (3, 29, "an Indian woman of about 29, about 162 cm, a full figure with wide hips and a medium waist, a diamond-shaped face with high cheekbones, a clear jawline and a slightly pointed chin, full lips, slightly deep-set dark-brown eyes, a small black bindi in the middle of the forehead, honey-brown skin with a few small pigment spots, thick naturally curly black hair to the shoulders in one long braid over one shoulder, a long dusty-pink kurta with three-quarter sleeves, black churidar trousers and brown loafers",
     "a black cloth tote bag", baby("a navy-blue")),
    (4, 30, "an Indian woman of about 30, about 160 cm, sturdy with full upper arms and sloping shoulders, a square face with a wide jaw, a narrow forehead, slightly asymmetric cheeks and a round chin, a wide nose, an upper lip thinner than the lower lip, round dark-brown eyes, dark brown skin with visible pores, a short black chin-length bob with a centre parting, neatly combed, a short-sleeved cream-white cotton blouse, a long light-purple pleated skirt and low white sandals",
     "a tan leather tote bag", baby("a chocolate-brown")),
    (5, 31, "an Indian woman of about 31, about 165 cm, an average, slightly full build with medium-wide shoulders, an oval face with moderate cheekbones and an oval chin, natural grooves on the lips, big dark-brown eyes with clear eyelids, a small red bindi in the middle of the forehead, yellowish light-brown skin with light wrinkles around the eyes, black hair past the shoulders in a high, slightly messy bun with a few loose strands, a long-sleeved deep-blue salwar kameez, a mustard-yellow dupatta and white sneakers",
     "a mustard-yellow cloth tote bag", baby("a mustard-yellow")),
    (6, 26, "an Indian woman of about 26, about 163 cm, a sturdy build with broad shoulders and strong arms, a square face with a clear jawline and high cheekbones, deep sun-tanned brown skin with a light smudge of dust on one cheek, long black hair tied in a neat high ponytail under a yellow safety helmet, a grey T-shirt, an orange high-visibility reflective vest, wide black salwar trousers, brown safety boots and a work glove on one hand",
     "a worn dark-grey canvas shoulder bag", None),
    (7, 30, "an Indian woman of about 30, about 158 cm, small but wiry, a round face with sunburnt red cheeks, a slightly flat nose, round dark-brown eyes, thick eyebrows, a small red bindi in the middle of the forehead, black hair in a long braid over one shoulder under a red headscarf worn against the sun, a long-sleeved red-and-white checked kurta, faded navy-blue salwar trousers, brown rubber boots and an earth-brown coarse-cloth apron with a pair of gardening gloves tucked into its pocket",
     "a small brown cloth shoulder bag", None),
    (8, 34, "an Indian woman of about 34, about 160 cm, a slightly plump build with a round belly, a chubby face with a double chin and slightly sagging cheeks, small slightly deep-set dark-brown eyes with clear eye bags, black hair with a few grey strands in a low bun under a deep-purple headscarf, a deep-blue cotton saree wrapped in a neat working style with a matching short-sleeved blouse, black sneakers, a black apron and a yellow rubber glove on one hand",
     "a black fabric shoulder bag", None),
    (9, 38, "an Indian woman of about 38, about 156 cm, a solid build with broad shoulders, a wide face with full cheeks, a round chin, a wide nose, full lips and deep dark-brown eyes, a big red bindi in the middle of the forehead, black hair cut short at the ears under a small yellow flower-print headscarf, a long short-sleeved earth-orange kurta, black salwar trousers, brown sandals and a knee-length red flower-print cloth apron, a white wiping cloth over the shoulder",
     "a faded brown cloth shoulder bag", None),
    (10, 25, "an Indian woman of about 25, about 164 cm, slim with a long neck and small shoulders, a heart-shaped face with a wide forehead, a small pointed chin and high cheekbones, a small straight nose, big dark-brown eyes with long curled lashes, no bindi, long straight black hair down to the middle of the back with a centre parting, in a low ponytail, a short-sleeved white T-shirt, straight dark-blue jeans, white sneakers, a yellow tailor's measuring tape around the neck and scissors and thread in the shirt pocket",
     "a cream fabric shoulder bag", None),
    (11, 70, "an Indian woman of about 70, about 158 cm, slightly thin with narrow shoulders and a slight stoop, a long narrow face with high cheekbones and hollow cheeks, a small chin, deep wrinkles around the eyes and mouth, clear age spots, dark brown skin, almost completely white hair in a short chin-length bob with a side parting, neatly combed, a small red bindi in the middle of the forehead, a cream-white cotton saree with a red border, a short-sleeved white blouse and low brown sandals",
     "a small brown leather shoulder bag", None),
    (12, 71, "an Indian woman of about 71, about 155 cm, short and slightly plump with rounded shoulders, a wide face with a slight double chin and sagging cheeks, small wrinkles all over the face, clear eye bags, sun-tanned brown skin, thick salt-and-pepper hair cut at the nape, naturally a little wavy, no bindi, a long-sleeved light-pink kurta, white salwar trousers, a beige dupatta and simple brown sandals",
     "a faded red cloth shoulder bag", None),
    (13, 72, "an Indian woman of about 72, about 160 cm, thin with sloping shoulders and small arms, a long face with high cheekbones, thin lips, slightly sunken eyes with gently drooping lids, dark brown skin with many age spots, thin grey-and-black hair in a low bun at the nape with a few loose wisps, a small black bindi in the middle of the forehead, a turmeric-yellow silk saree with a long-sleeved blouse of the same colour and old but clean black walking shoes",
     "a dark-green cloth shoulder bag", None),
    (14, 73, "an Indian woman of about 73, about 152 cm, small with a slightly curved back, an oval face with sagging cheeks and a small chin, deep wrinkles and clear nasolabial folds, wrinkles on the neck, olive-brown skin, mostly grey hair cut short at the ears and a little thin on top, no bindi, a thin ash-grey cardigan over a white kurta, dark salwar trousers and low flat black shoes",
     "a small black leather shoulder bag", None),
    (15, 74, "an Indian woman of about 74, about 163 cm, tall and thin, a long narrow face with a high forehead, a clear jawline, deeply hollow cheeks, sunken eyes, thin silver eyebrows and thin lips, dark brown skin with many brown spots, completely white hair to the shoulders in a low ponytail with a centre parting, a small red bindi in the middle of the forehead, a light-purple cotton saree with a long-sleeved white blouse, a thin cream shawl over the shoulders and black loafers",
     "a structured black leather shoulder bag", None),
    (16, 75, "an Indian woman of about 75, about 150 cm, very short with a clearly bent back, a small round face with sagging cheeks and a double chin, deep wrinkles all over the face, hands with age spots and prominent veins, dark brown skin, short white slightly curly hair ending at the ears, a small black bindi in the middle of the forehead, a long-sleeved pale-sky-blue kurta, dark-brown salwar trousers, low black shoes and a thin white headscarf",
     "a small cream cloth shoulder bag", None),
    (17, 76, "an Indian woman of about 76, about 166 cm, an average, slightly full build, a slightly square face with clear cheekbones and a wide chin, big dark-brown eyes with drooping lids, lips with grooves, wrinkles around the eyes, unevenly sun-tanned brown skin, black hair with a lot of grey past the shoulders in a low ponytail, no bindi, a burgundy cotton saree with a gold border and a short-sleeved blouse of the same colour, plain white sports shoes",
     "a brown fabric shoulder bag", None),
    (18, 77, "an Indian woman of about 77, about 157 cm, a slightly plump build, a diamond-shaped face with sharp high cheekbones and a small pointed chin, almond-shaped dark-brown eyes, curved silver eyebrows, honey-brown skin with light age spots, a salt-and-pepper chin-length bob with a deep side parting and the ends curled under, a small red bindi in the middle of the forehead, a straight-cut long-sleeved cream silk kurta, wide black salwar trousers, brown loafers, small gold earrings and a fake pearl necklace",
     "a small brown leather handbag", None),
    (19, 78, "an Indian woman of about 78, about 159 cm, an average build, an oval face with slightly hollow cheeks, a wide forehead and a long chin, a high nose, small dark-brown eyes with drooping lids, yellowish light-brown skin with light wrinkles, brown-grey hair down to the middle of the back in a low braid over one shoulder, no bindi, an earth-brown knitted sweater, beige salwar trousers, white sneakers and a thin mustard-yellow scarf",
     "a tan canvas shoulder bag", None),
    (20, 80, "an Indian woman of about 80, about 154 cm, short and thin with narrow shoulders, a long face with high cheekbones, hollow cheeks, a small pointed chin and thin lips, slightly sunken eyes, a calm composed look, dark brown skin with many deep wrinkles, white hair in a neat high bun at the back of the head with a small silver hairpin, a small red bindi in the middle of the forehead, a white cotton saree with a gold border, a long-sleeved white blouse, a thin earth-brown woollen jacket to the hips and black walking shoes",
     "a small brown leather handbag", None),
]

# ---------------------------------------------------------------------------------------------------------------------------
# Lời thoại
# ---------------------------------------------------------------------------------------------------------------------------
HINDI = [
    # (who, text, emo, phan, fx, icon)  -- chép từ ô kịch bản đầu file X0077; dấu ngoặc kép đổi thành “ ” cho an toàn khi đưa vào prompt
    ("canbo", "Is this your bag?", "routine, calm", 1),
    ("hoc", "Yes, it is.", "worried", 1),
    ("canbo", "First time in America?", "interested", 1),
    ("hoc", "Yes. We're, we're here to join my husband.", "warm", 1),
    ("canbo", "The scanner detected something unusual in your bag. I need you to open it.", "calm", 1),
    ("hoc", "Okay. It might be my power bank. Would you like me to take it out?", "helpful", 1),
    ("canbo", "Yes, please. You speak English really well, by the way.", "impressed", 1),
    ("hoc", "Thank you. I've been practicing with AI.", "proud, cheerful", 1),
    ("canbo", "With AI? How?", "curious", 1),
    ("hoc", "It's called Talka AI. I practice speaking with it for just 10 minutes a day, and it corrects me instantly.", "enthusiastic", 1),   # lượt 20 từ -> tách 2 lượt để đủ 13 lượt phần 1
    ("hoc", "After just three weeks, I started sounding way more natural.", "proud", 1),
    ("canbo", "Sounds useful.", "doubtful", 1),
    ("hoc", "And it's free. Here, let me show you.", "cheerful", 1),
    ("day", "Hey, how are you today?", "friendly", 2),
    ("hoc", "I'm fine, thank you. And you?", "hesitant", 2),
    ("day", "I'm good, thanks. वैसे, इसे कहने का एक बेहतर तरीका है, “I'm doing great.” ये ज़्यादा नेचुरल लगता है।", "patient, encouraging", 2),
    ("hoc", "Okay. I'm doing great.", "confident", 2),
    ("day", "Do you feel like watching a movie today?", "friendly", 2),
    ("hoc", "No. Today, I gonna see a friend.", "unsure", 2, "wrong", "x"),
    ("day", "ऐसे बोलकर देखिए: “Today, I'm going to see a friend.” फ्यूचर प्लान्स के बारे में बात करने के लिए हम “I'm going to” का इस्तेमाल करते हैं।", "patient, encouraging", 2),
    ("hoc", "समझ गई! “Today, I'm going to see a friend.” आप इंग्लिश सीखना इतना आसान बना देते हैं!", "delighted", 2, "right", "check"),
    ("day", "बिल्कुल! हर दिन मेरे साथ प्रैक्टिस कीजिए और आप कॉन्फिडेंस के साथ इंग्लिश बोल पाएँगी। बस Talka AI डाउनलोड कीजिए!", "encouraging", 2),
    ("hoc", "लैंग्वेज सीखने के लिए सबसे बेस्ट ऐप! मैं अभी डाउनलोड करती हूँ!", "enthusiastic", 2),
]

WHO_YOUNG = ["sister", "cousin", "brother", "best friend"]


def who_mx(age, has_baby, n):
    if has_baby:
        return "husband's family"
    if age >= 50:
        return "daughter"
    return WHO_YOUNG[n % len(WHO_YOUNG)]


def luot_mx(age, who):
    luot = copy.deepcopy(MAU["LUOT"])
    for t in luot:
        t["text"] = (t["text"].replace("visiting my daughter", f"visiting my {who}")
                     .replace("I have 48", f"I have {age}").replace("I am 48", f"I am {age}"))
    return luot


def luot_hi():
    res = []
    for r in HINDI:
        d = {"who": r[0], "text": r[1], "emo": r[2], "c": "yellow" if r[0] == "day" and r[3] == 2 else "white", "fx": r[4] if len(r) > 4 else "none", "phan": r[3]}
        if len(r) > 5:
            d["icon"] = r[5]
        res.append(d)
    return res


def voice(age, accent, hindi):
    lang = "speaking Hindi and English" if hindi else "speaking English as a second language"
    if age <= 30:
        v, hz = "a young {} woman's voice of about {}", "mid-high pitch (around 205-240 Hz)"
    elif age <= 45:
        v, hz = "a {} woman's voice of about {}", "mid pitch (around 190-225 Hz)"
    else:
        v, hz = "a soft, slightly thin and wavering {} grandmother's voice in her " + ("seventies" if age < 80 else "eighties") + ", about {}", "mid pitch (around 175-205 Hz)"
    return v, hz, lang


def giong(age, nat, accent, hindi, n):
    v, hz, lang = voice(age, accent, hindi)
    base = v.format(nat, age)
    return (f"{base}, {hz}, {TRAITS[n % len(TRAITS)]}; a real {nat} woman {lang}, {accent}; quick and a little nervous at the "
            f"checkpoint, warming up and quietly proud when talking about the tutor; {REAL}")


PRON_F = {"HE_HOC": "she", "HE_HOC_C": "She", "HIS_HOC": "her", "HIM_HOC": "her", "HIMSELF_HOC": "herself"}


def variant(p, nat, accent, hindi, link, tag):
    n, age, look, bag, baby_en = p
    v = {"name": f"soi-hanh-ly-{tag}-{n:02d}-nu-{age}"}
    if baby_en:
        v.update({"TEN_HOC": "the mother", "VAI_HOC": "mother"})
    else:
        v.update({"TEN_HOC": "the traveller", "VAI_HOC": "traveller"})
    v["NGUOI_HOC"] = look
    v["GIONG_HOC"] = giong(age, nat, accent, hindi, n)
    v["POS_HOC"] = "RIGHT"
    for k in CHUNG:
        v[k] = copy.deepcopy(MAU[k])
    v["POS_CANBO"] = MAU["POS_CANBO"]
    v["GIONG_DAY"] = GIONG_DAY_HI if hindi else (MAU["GIONG_DAY"] if baby_en else GIONG_DAY_EN)
    if baby_en:
        v["NGHE_HOC"] = MAU["NGHE_HOC"]
        v["DAO_BE"] = baby_en
        v["DAO_GIU"], v["DAO_NGHI"] = MAU["DAO_GIU"], MAU["DAO_NGHI"]
        v["NHIN_CANBO"], v["NHIN_HOC"], v["NHIN_HOC@2"] = MAU["NHIN_CANBO"], MAU["NHIN_HOC"], MAU["NHIN_HOC@2"]
    else:
        v["NGHE_HOC"] = ("stands with one hand resting on the strap of her bag, mouth closed; her eyes follow whatever the officer points at (the suitcase) and "
                         "come back to the officer's face, with a natural, slightly worried or smiling face that matches the moment")
        v["DAO_GIU"] = "Her free hand rests on the strap of her bag or does the clip's action only: no hand ever goes to the head, face or hair."
        v["DAO_NGHI"] = "the traveller standing with one hand resting on the bag strap, the officer standing still behind the conveyor"
        v["NHIN_CANBO"] = ("keeps his head turned toward the traveller in three-quarter profile, looking at the traveller's face (or at the suitcase or phone the clip "
                           "names); his face never turns to the camera or out of the frame")
        v["NHIN_HOC"] = "looks at the officer's face, eyes level, never into the lens (except when the clip's action is to look at the suitcase or the phone)"
        v["NHIN_HOC@2"] = "looks straight into the lens, as if talking to the AI tutor on the phone she is holding"
        v.update(PRON_F)
    v["DAO_TUI"] = bag
    v["LUOT"] = luot_hi() if hindi else luot_mx(age, who_mx(age, bool(baby_en), n))
    v["refs"] = {"NGUOI_HOC": [link], "NGUOI_DAY": [ROBOT]}
    return v


def doc_csv(path):
    """Trả {số: (tuổi trong mô tả VN, link)} từ file CSV."""
    res = {}
    for r in csv.reader(open(path, encoding="utf-8")):
        if r and re.match(r"^Biến thể \d+$", r[0].strip()) and len(r) >= 4:
            m = re.search(r"(\d+) tuổi", r[2])
            res[int(r[0].split()[-1])] = (int(m.group(1)) if m else None, r[3].strip(), "địu em bé" in r[1])
    return res


def kiem_tra(bang, csvd, ten):
    assert sorted(csvd) == [p[0] for p in bang], f"{ten}: số biến thể trong CSV khác bảng"
    for p in bang:
        age, link, has_baby = csvd[p[0]]
        assert age == p[1], f"{ten} biến thể {p[0]}: tuổi CSV {age} ≠ bảng {p[1]}"
        assert has_baby == bool(p[4]), f"{ten} biến thể {p[0]}: có/không em bé khác CSV"
        assert link.startswith("https://drive.google.com/"), f"{ten} biến thể {p[0]}: link lạ {link}"


def ghi(vs, name):
    f = os.path.join(D, name)
    json.dump(vs, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(name, len(vs))


if __name__ == "__main__":
    for bang, path, nat, accent, hindi, tag, out in (
            (MX, CSV_MEXICO, "Mexican", ACCENT_MX, False, "x0076", "BIEN-THE-SOI-HANH-LY-X0076-40"),
            (IN, CSV_HINDI, "Indian", ACCENT_IN, True, "x0077", "BIEN-THE-SOI-HANH-LY-X0077-HINDI-20")):
        csvd = doc_csv(path)
        kiem_tra(bang, csvd, tag)
        ra = {"KHONG-BE": [], "DIU-CON": []}
        for p in bang:
            ra["DIU-CON" if p[4] else "KHONG-BE"].append(variant(p, nat, accent, hindi, csvd[p[0]][1], tag))
        for k, vs in ra.items():
            ghi(vs, f"{out}-{k}.json")
