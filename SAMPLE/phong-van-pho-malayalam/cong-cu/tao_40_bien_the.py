"""Sinh SAMPLE/phong-van-pho-malayalam/BIEN-THE-40-PHONG-VAN-PHO-MALAYALAM.json: 40 biến thể theo bảng người dùng
"40 biến thể interview - Sheet1.csv" (12/11/2026): mỗi biến thể đổi NGƯỜI BÁN (nam/nữ, trẻ/già, nghề) và BỐI CẢNH (quầy hàng đúng nghề).
Giữ nguyên: lời thoại, phóng viên, robot, góc máy, bố cục 2 phần (dùng chung LUOT/CHUNG của tao_bien_the.py).
Ảnh: tải từ link Drive trong bảng về anh/bt40/nv<NN>.jpg (nhân vật, phông xanh, toàn thân) và anh/bt40/nen<NN>.jpg (bối cảnh không người),
đổi webp -> jpg. Gắn vào "refs": NGUOI_HOC = ảnh nhân vật, NEN_PHO (phần 1) + NEN_HOC (phần 2, nền selfie) = ảnh bối cảnh.
Chạy:  runtime\\python.exe SAMPLE\\phong-van-pho-malayalam\\cong-cu\\tao_40_bien_the.py [--tai-anh "<file csv>"]
  --tai-anh: tải lại ảnh từ link Drive trong csv (mặc định dùng ảnh đã có trong anh/bt40/)."""
import csv
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tao_bien_the as TB  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ANH = "SAMPLE/phong-van-pho-malayalam/anh/"
BT40 = ANH + "bt40/"
OUT = os.path.join(HERE, "..", "BIEN-THE-40-PHONG-VAN-PHO-MALAYALAM.json")

GIONG = {   # nam: trầm hơn hẳn giọng phóng viên (150-180 Hz) để Muse không lẫn hai giọng nam
    ("m", "tre"): "a real young Malayali man's voice, low and relaxed (around 110-135 Hz), clearly deeper and calmer than the interviewer's, friendly and confident, "
                  "native Kerala Malayalam, says the English words like a proud learner; a real person, not an actor",
    ("m", "gia"): "a real elderly Malayali man's voice, low, slow and a little gravelly (around 100-125 Hz), clearly deeper and older than the interviewer's, warm "
                  "and good-humoured, native Kerala Malayalam, says the English words carefully like a proud learner; a real person, not an actor",
    ("f", "tre"): "a real young Malayali woman's voice, bright and lively (around 220-260 Hz), warm and confident, native Kerala Malayalam, says the English words "
                  "like a proud learner; a real person, not an actress",
    ("f", "gia"): "a real elderly Malayali woman's voice, warm, a little husky and unhurried (around 190-220 Hz), native Kerala Malayalam, says the English words "
                  "carefully like a proud learner; a real person, not an actress",
}

# Người bán NAM: phóng viên đổi sang NỮ (người dùng yêu cầu 12/11/2026) để Muse không lẫn giọng / lặp câu giữa hai người nam.
PV_NU = {
    "NGUOI_PV": ("a young Malayali woman about twenty-six years old, long black hair in a neat low ponytail falling down her back, a pink-and-white "
                 "plaid cotton shirt with rolled sleeves, blue jeans, a black backpack on her back"),
    "GIONG_PV": ("a real young Malayali woman's voice, bright light mezzo (around 200-230 Hz), friendly and playful like a street-interview host, native Kerala "
                 "Malayalam; a real person, not an announcer"),
    "NHIN_PV": "keeps her face pointed at the vendor's face, to the right and slightly down, the camera seeing only the back and the right edge of her head; she never turns toward the camera",
    "NGHE_PV": "holds the microphone still toward the vendor and keeps her face pointed at {him}, her head still, the camera seeing only the back of her head",
    "ANH": "phong-vien-nu.png",
}

# n, giới, tuổi, nghề (VAI), trang phục, quầy trước mặt (DAO_XE), việc tay cảnh 1, việc tay cảnh 5, tay lúc nghỉ, găng, nơi (NEN_PHO), nền selfie (NEN_HOC)
# Câu tiếng Anh gọn, tả theo bảng người dùng (cột trang phục + cột bối cảnh); chi tiết còn lại để ảnh tham chiếu lo.
NV = [
    (1, "m", 26, "street tea seller", "a short-sleeved small navy-and-white checked shirt buttoned up, sleeves rolled once, beige chinos, a thin brown belt, a black-strap watch on the left wrist and a thin red thread on the right wrist",
     "his small waist-high stainless-steel tea counter with a big brass tea kettle letting off thin steam, a tray of small glasses of milky tea, an aluminium milk can and a glass jar of round biscuits",
     "keeps slowly lining up the small tea glasses on the tray", "sets one glass of tea back on the tray", "his hands resting on the edge of the tea counter", False,
     "a quiet South Indian street on a soft sunny morning, slightly out of focus: old two-storey pale-yellow shophouses with rolling shutters, green trees, a grey asphalt road",
     "his tea stall on a sunny street, out of focus: the brass kettle and tea glasses at the lower right, old shophouses behind"),
    (2, "m", 28, "dosa cook at a street eatery", "a dark red polo shirt, a clean charcoal-grey canvas apron tied at the waist, dark blue jeans and a plain silver bracelet",
     "his flat round black iron dosa griddle on a steel gas stove, steel trays of batter and yellow potato filling, a basket of chopped onion and green chillies and a stack of shiny steel plates",
     "keeps slowly spreading a little batter in a circle on the griddle with a ladle", "lays the ladle down beside the griddle", "his hands resting on the edge of the steel counter", False,
     "a busy daytime street eatery under a blue-and-white striped awning, slightly out of focus: a worn cream wall, a wall fan, people far behind",
     "his dosa stall, out of focus: the griddle and steel plates at the lower right, the striped awning behind"),
    (3, "m", 25, "auto-rickshaw driver", "a mustard-yellow long-sleeved shirt with the sleeves rolled to the elbows and the top button open, straight black trousers, a silver metal watch and a pen in the chest pocket",
     "the front of his yellow-and-black auto-rickshaw parked beside him, its windscreen and handlebar visible",
     "keeps one hand on the rickshaw's handlebar, tapping it lightly", "lifts his hand off the handlebar and lets it rest on the frame", "one hand resting on the frame of his auto-rickshaw", False,
     "an auto-rickshaw stand at a South Indian street corner, slightly out of focus: two more yellow-and-black rickshaws parked behind, old shopfronts, trees",
     "the auto-rickshaw stand, out of focus: yellow-and-black rickshaws behind him, a street corner with trees"),
    (4, "m", 30, "vegetable seller at a traditional market", "a light green long-sleeved linen shirt rolled to mid-forearm, ash-grey chinos, a thin silver bracelet and a plain silver ring",
     "his long wooden vegetable stall with a pyramid of red tomatoes, bundles of green beans, carrots, pale cabbages and a bamboo basket of shallots",
     "keeps straightening a pile of tomatoes with his fingertips", "puts a tomato back on the pile", "his hands resting on the edge of the vegetable stall", False,
     "a traditional South Indian market on an early morning, slightly out of focus: other stalls, tarpaulin roofs, shoppers far behind",
     "his vegetable stall at a busy market, out of focus: colourful heaps of vegetables at the lower right, shoppers far behind"),
    (5, "m", 27, "barber at a small salon", "a fitted black crew-neck T-shirt, a plain black barber's apron with brown leather straps across the chest, dark grey skinny jeans and a black smartwatch",
     "the back of a black leather barber's chair and a small tray of combs, scissors and clippers on the counter beside it",
     "keeps slowly running a comb through his fingers", "puts the comb back in the tray", "one hand resting on the back of the barber's chair", False,
     "inside a small, clean, simple Indian barber salon, slightly out of focus: a long wall mirror, shelves with spray bottles and jars, warm lights",
     "his barber salon, out of focus: the mirror and barber chairs behind him"),
    (6, "m", 24, "fruit seller with a push cart", "a bright orange crew-neck T-shirt, knee-length moss-green cargo shorts, a blue cap worn backwards, a colourful fabric bracelet and a black sports watch",
     "his four-wheeled wooden fruit push cart with a pyramid of yellow mangoes, bananas hanging from a pole, whole pineapples, oranges and red apples",
     "keeps turning a mango in his hand, checking it", "puts the mango back on the pyramid", "his hands resting on the edge of the fruit cart", False,
     "a sunny South Indian pavement, slightly out of focus: old shophouses, trees, a few people far behind",
     "his fruit cart on a sunny street, out of focus: piles of mangoes and bananas at the lower right"),
    (7, "m", 29, "motorbike mechanic at a roadside workshop", "a slightly worn dark blue short-sleeved work shirt, dark grey work trousers, black safety boots, a large steel watch and a red-handled screwdriver in the chest pocket",
     "an open metal toolbox with spanners and screwdrivers on a workbench beside him",
     "keeps turning a spanner over in his hand", "lays the spanner back in the toolbox", "his hands resting on the edge of the workbench", False,
     "a roadside motorbike repair workshop, slightly out of focus: a silver scooter on its stand, tyres hanging on a wooden rack, a grey concrete floor",
     "his roadside workshop, out of focus: a scooter and hanging tyres behind him"),
    (8, "m", 31, "flower stall owner at a flower market", "an off-white long-sleeved linen shirt rolled to the elbows, olive chinos, a small wooden-bead necklace and a wooden-bead bracelet",
     "his low bamboo flower stall with buckets of orange marigolds, red roses wrapped in paper and strings of white jasmine",
     "keeps arranging a string of jasmine on the stall", "lays the jasmine string down on the stall", "his hands resting on the edge of the flower stall", False,
     "an early-morning flower market in South India, slightly out of focus: other flower stalls, jasmine garlands hanging on poles, shoppers far behind",
     "his flower stall, out of focus: buckets of marigolds and roses at the lower right"),
    (9, "m", 33, "young fisherman selling fish at a seaside market", "a dark sea-blue crew-neck T-shirt, a blue-and-white checked cotton towel over one shoulder, knee-length black shorts and a thin rope bracelet",
     "his long steel table of fresh fish on crushed ice, silvery mackerel in a row, small fish in blue plastic trays and a basket of prawns",
     "keeps lining up the mackerel on the ice", "puts a fish back on the ice", "his hands resting on the edge of the fish table", False,
     "a seaside fish market in South India in the morning, slightly out of focus: fishing boats at the shore, other fish stalls, buyers far behind",
     "his fish stall at the seaside market, out of focus: fish on ice at the lower right, boats far behind"),
    (10, "m", 23, "owner of a small fruit-juice counter", "a white short-sleeved polo shirt with a navy collar, a plain light green apron tied at the waist, light blue jeans and a blue smartwatch",
     "his white-and-mint wooden juice counter with a silver juicer, a blender, tall glasses upside down on a tray and a small glass shelf of oranges and pineapples",
     "keeps wiping a tall glass with a small cloth", "sets the glass down upside down on the tray", "his hands resting on the edge of the juice counter", False,
     "a food street in a South Indian town, slightly out of focus: other food stalls, shop fronts, people far behind",
     "his juice counter, out of focus: the juicer and fruit at the lower right"),
    (11, "f", 26, "street snack-cart owner", "a fitted fuchsia-pink short-sleeved blouse and a brown-and-black checked cotton saree on a light beige ground with a wine-red border, red and green glass bangles",
     "her stainless-steel snack push cart with big trays of golden round fried snacks, aluminium pots of chutney and a stack of steel plates",
     "keeps arranging the fried snacks in the tray with her gloved fingers", "puts a fried snack back in the tray", "her gloved hands resting above the trays", True,
     "a quiet old South Indian street in daytime, slightly out of focus: old shophouses with rolling shutters, coconut palms, a grey asphalt road",
     "her snack cart on a busy street, out of focus: trays of fried snacks at the lower right, shophouses behind"),
    (12, "f", 28, "sari and fabric stall owner at a market", "a turquoise silk saree with a golden border draped over the left shoulder, a bronze-gold elbow-length blouse, silver and turquoise bangles",
     "the front of her fabric stall with neatly folded saris laid out on a cloth-covered counter",
     "keeps smoothing a folded sari on the counter with her palm", "lays the folded sari back on the pile", "her hands resting on the folded saris", False,
     "a South Indian fabric market, slightly out of focus: tall wooden shelves stacked with rolls of cloth in rainbow colours",
     "her fabric stall, out of focus: shelves of colourful cloth rolls behind her"),
    (13, "f", 25, "tailor at a small shop", "a turmeric-yellow elbow-sleeve cotton kurti with small white flowers, black leggings, a thin cream dupatta over the right shoulder and a yellow measuring tape round the right wrist",
     "her old black iron treadle sewing machine with a wooden top, a half-sewn floral cloth and a small box of thread",
     "keeps smoothing the half-sewn cloth under the needle", "lays the cloth back on the machine", "her hands resting on the sewing-machine table", False,
     "a small tailor's shop in a South Indian market lane, slightly out of focus: shelves of pastel cloth rolls, a rack of finished clothes",
     "her tailor's shop, out of focus: cloth rolls and a clothes rack behind her"),
    (14, "f", 24, "flower-garland seller at a flower-market gate", "a dark green short-sleeved blouse and a lemon-yellow cotton saree with a green border, many green and yellow bangles",
     "her low bamboo table with round trays of loose jasmine, orange marigolds and red roses",
     "keeps threading a few jasmine buds onto a string", "lays the half-made garland on the tray", "her hands resting on the edge of the flower table", False,
     "the entrance of an early-morning flower market in South India, slightly out of focus: garlands hanging from bamboo poles, shoppers far behind",
     "her garland stall, out of focus: trays of flowers at the lower right, hanging garlands behind"),
    (15, "f", 29, "owner of a small bakery counter", "a cream-white short-sleeved buttoned shirt, a plain pastel-pink apron, light brown straight trousers, a small gold watch and a thin gold bracelet",
     "her two-tier glass display case with cream cakes topped with strawberries, golden croissants and a big glass jar of butter biscuits",
     "keeps straightening a tray of croissants on top of the glass case", "sets the tray back on the glass case", "her hands resting on top of the glass display case", False,
     "a small South Indian bakery, slightly out of focus: shelves of bread loaves in baskets, warm lights",
     "her bakery counter, out of focus: the glass case of cakes at the lower right"),
    (16, "f", 27, "herb and leaf seller at a market", "a lilac elbow-sleeve kurti with small white embroidery on the chest, wide off-white cotton palazzo trousers, a light lilac dupatta over the left shoulder and thin silver bangles",
     "her low wooden stall with bamboo trays heaped with bunches of coriander, mint, curry leaves wrapped in banana leaf and red amaranth",
     "keeps tying a small bunch of coriander", "lays the bunch back on the tray", "her hands resting on the edge of the herb stall", False,
     "a South Indian morning market, slightly out of focus: other green-vegetable stalls, shoppers far behind",
     "her herb stall, out of focus: heaps of green herbs at the lower right"),
    (17, "f", 23, "tea and breakfast seller near a bus stop", "a peach-orange short-sleeved blouse and a light blue cotton saree with small flowers, orange and white plastic bangles",
     "her small wood-and-tin counter with a big steel tea kettle on a mini gas stove, glasses and paper cups, a pot of boiled eggs and a tray of idlis",
     "keeps pouring a little tea from the kettle into a glass", "sets the kettle back on the stove", "her hands resting on the edge of the counter", False,
     "a bus stop in a small South Indian town, slightly out of focus: a bus shelter, a parked bus far behind, trees",
     "her tea counter by the bus stop, out of focus: the steel kettle at the lower right"),
    (18, "f", 30, "sales assistant at a small silver-jewellery shop", "a wine-red silk elbow-sleeve kurti with light gold embroidery at the neck, bronze churidar trousers, a red dupatta with a gold border, silver and red bangles",
     "her long glass jewellery case with silver bangles, necklaces, earrings and rings laid on red and navy velvet",
     "keeps arranging a silver bangle on the velvet tray", "lays the bangle back on the velvet", "her hands resting on top of the glass case", False,
     "inside a small silver-jewellery shop in a South Indian market street, slightly out of focus: glass shelves, warm display lights",
     "her jewellery shop, out of focus: glass shelves and warm lights behind her"),
    (19, "f", 26, "coconut seller with a push cart", "a sky-blue crew-neck T-shirt, a white cotton towel over the shoulder, dark grey cotton trousers rolled once at the ankle, a black waterproof watch and a colourful thread bracelet",
     "her old green-painted iron push cart with a neat pyramid of green coconuts and a few peeled white coconuts",
     "keeps turning a green coconut on the pile with both hands", "sets the coconut back on the pile", "her hands resting on the edge of the coconut cart", False,
     "a leafy South Indian street corner, slightly out of focus: big shady trees, old houses, a few people far behind",
     "her coconut cart, out of focus: green coconuts at the lower right, shady trees behind"),
    (20, "f", 28, "cosmetics stall owner at a market", "a powder-pink elbow-sleeve kurti with a few sequins on the chest, white straight jeans, a light pink dupatta, nude-pink nails, a small gold watch",
     "the front of her stall with trays of lipsticks, small cream jars, powder compacts and wrapped soaps",
     "keeps lining up a few lipsticks in the tray", "puts a lipstick back in the tray", "her hands resting on the edge of the cosmetics stall", False,
     "an indoor market in South India, slightly out of focus: wood-and-glass shelves of colourful bottles and jars, bright lights",
     "her cosmetics stall, out of focus: shelves of colourful products behind her"),
    (21, "m", 65, "old tea-shop owner at a street corner", "an off-white long-sleeved cotton shirt faded with age, rolled to the elbows and buttoned up, a checked cotton towel over the shoulder, grey cotton trousers, an old silver watch",
     "his old wooden tea counter painted green, a smoky grey brass tea kettle, a small charcoal stove and a metal tray of old glasses",
     "keeps slowly lining up the old tea glasses on the tray", "sets one glass back on the tray", "his hands resting on the edge of the tea counter", False,
     "an old street corner in a small South Indian town, slightly out of focus: old houses with tiled roofs, big trees, a quiet road",
     "his old tea shop at the corner, out of focus: the brass kettle at the lower right, old houses behind"),
    (22, "m", 68, "veteran fisherman selling fish", "a sun-faded red-and-black checked short-sleeved shirt with the top two buttons open over a white vest, a blue-and-white striped lungi to the calves, a black cord necklace with an old coin",
     "his low wood-and-steel table of fresh fish on melting crushed ice, fish on banana leaves and a bamboo basket of prawns and crabs",
     "keeps lining up the fish on the banana leaf", "puts a fish back on the ice", "his hands resting on the edge of the fish table", False,
     "a seaside fish market in South India at sunrise, slightly out of focus: fishing boats on the beach, other fish stalls",
     "his fish stall at sunrise, out of focus: fish on ice at the lower right, boats far behind"),
    (23, "m", 62, "pavement shoe repairer", "a pale blue short-sleeved shirt with a worn collar, grey-brown trousers, a cheap black plastic watch and a pen and a few coloured threads in the chest pocket",
     "his wooden box of awls, needles, glue and coloured thread on a green tarp, a few old shoes waiting for repair beside it",
     "keeps turning an old sandal in his hands, checking the stitching", "lays the sandal down beside the wooden box", "his hands holding an old sandal at waist height", False,
     "a familiar pavement corner in a South Indian street, slightly out of focus: an old yellow wall, a big tree, a big umbrella over his spot",
     "his shoe-repair corner on the pavement, out of focus: the old wall and umbrella behind him"),
    (24, "m", 60, "veteran vegetable seller at a traditional market", "a thin blue-and-white striped short-sleeved shirt, dark beige cotton trousers, an old black leather belt, a square brown-strap watch and an old gold ring",
     "his big two-tier wooden stall with cut orange pumpkin, potatoes and onions in bamboo baskets, a tall pile of tomatoes and big bunches of green bananas",
     "keeps straightening a pile of tomatoes with his fingertips", "puts a tomato back on the pile", "his hands resting on the edge of the vegetable stall", False,
     "a traditional South Indian market on a busy morning, slightly out of focus: other stalls under tarpaulin roofs, shoppers far behind",
     "his vegetable stall, out of focus: heaps of vegetables at the lower right"),
    (25, "m", 66, "old barber at a classic barber shop", "a white long-sleeved buttoned shirt rolled neatly to the elbows, a worn plain navy barber's apron, pressed grey trousers, an old wind-up watch with a black strap and a small black comb in the pocket",
     "the back of an old iron-and-leather barber's chair with wooden armrests and a metal tray of scissors and razors beside it",
     "keeps slowly running a comb through his fingers", "puts the comb back in the tray", "one hand resting on the back of the old barber's chair", False,
     "inside a classic Indian barber shop decades old, slightly out of focus: a big dark-wood-framed mirror, old glass bottles of hair oil on the shelf",
     "his classic barber shop, out of focus: the old mirror and chair behind him"),
    (26, "m", 70, "newspaper and lottery-ticket seller at a street corner", "a faded brown-and-cream checked long-sleeved shirt over a grey T-shirt, a brown striped cotton lungi to the ankles, a cheap black watch and a small moss-green cloth money bag across the chest",
     "his small wooden table with stacks of folded newspapers (no readable print) and a bundle of lottery tickets under a paperweight",
     "keeps straightening a stack of newspapers with both hands", "lays the newspapers back on the table", "his hands resting on the stack of newspapers", False,
     "a familiar South Indian street corner in the morning, slightly out of focus: old shops, a big tree, a quiet road",
     "his newspaper corner, out of focus: the newspaper table at the lower right"),
    (27, "m", 64, "owner of a small neighbourhood grocery shop", "a light pink thinly striped short-sleeved shirt buttoned up with a pen in the pocket, navy trousers, a black belt, an old gold watch, a gold ring and a thin gold chain",
     "his front counter with big glass jars of sweets and biscuits",
     "keeps tapping the lid of a glass sweet jar", "lets go of the jar and rests his hand on the counter", "his hands resting on the counter beside the glass jars", False,
     "a small grocery shop in a South Indian residential street, slightly out of focus: shelves packed with packets, bottles and sacks of rice",
     "his grocery shop, out of focus: shelves of goods behind him"),
    (28, "m", 69, "old watch repairer at a glass counter in a market", "a long-sleeved white shirt faded to cream, rolled to the elbows, a grey vest with many small pockets, black trousers and a classic leather-strap mechanical watch",
     "his low glass counter with old wall clocks inside and a small tray of wristwatches being repaired on top",
     "keeps turning a small wristwatch in his fingers, looking at it", "lays the wristwatch back in the tray", "his hands resting on top of the glass counter", False,
     "an indoor market in South India, slightly out of focus: other small stalls, warm lights",
     "his watch-repair counter, out of focus: old clocks behind him"),
    (29, "m", 58, "fruit seller at a small wholesale market", "a moss-green crew-neck T-shirt, a white cotton towel over the shoulder, dark brown cotton trousers, a big black sports watch, an old silver bracelet",
     "his wide wooden stall heaped with yellow mangoes in big baskets, standing pineapples, hanging bunches of bananas and papayas",
     "keeps turning a mango in his hand, checking it", "puts the mango back in the basket", "his hands resting on the edge of the fruit stall", False,
     "a small wholesale fruit market in South India in the early morning, slightly out of focus: crates of fruit, porters and buyers far behind",
     "his fruit stall, out of focus: heaps of mangoes at the lower right"),
    (30, "m", 67, "potter selling clay pots at a craft market", "an earth-brown long-sleeved cotton kurta rolled to the elbows, loose beige cotton trousers, a brown wooden-bead necklace and a colourful fabric bracelet",
     "his bamboo-and-wood shelves of red-brown clay pots, vases, small planters and a tray of little clay oil lamps",
     "keeps turning a small clay pot in his hands", "sets the clay pot back on the shelf", "his hands resting on the edge of the pottery shelf", False,
     "a craft market in South India, slightly out of focus: other craft stalls, shade cloths, people far behind",
     "his pottery stall, out of focus: clay pots at the lower right"),
    (31, "f", 62, "sweet fried-snack seller with a push cart", "a lilac short-sleeved blouse and a light green cotton saree with small flowers and a purple border, purple and green glass bangles",
     "her stainless-steel push cart under a purple-and-white striped canopy, with a heap of golden banana fritters, round fried sweets and a pot of syrup",
     "keeps arranging the banana fritters in the tray with her gloved fingers", "puts a fritter back on the heap", "her gloved hands resting above the trays", True,
     "a South Indian street in the soft afternoon, slightly out of focus: old pastel shophouses, coconut palms",
     "her snack cart, out of focus: golden fritters at the lower right, the striped canopy behind"),
    (32, "f", 65, "veteran fish seller at a fish market", "a brick-red short-sleeved blouse and a deep sea-blue cotton saree with a pale yellow border, red plastic and old silver bangles",
     "her low wooden fish table covered with banana leaves, rows of fish in red plastic trays and a bamboo basket of prawns and crabs",
     "keeps lining up the fish on the banana leaf", "puts a fish back in the tray", "her hands resting on the edge of the fish table", False,
     "a busy seaside fish market in South India in the early morning, slightly out of focus: boats, other fish sellers, buyers far behind",
     "her fish stall, out of focus: fish on banana leaves at the lower right"),
    (33, "f", 68, "flower seller near a temple gate", "a cream short-sleeved blouse and a lotus-pink cotton saree with a pale gold border, thin gold bangles and a red thread bracelet",
     "her low wooden table of heaped white jasmine, orange marigolds, pink lotus flowers in a basin of water and a stack of betel leaves",
     "keeps threading a few jasmine buds onto a string", "lays the jasmine string on the table", "her hands resting on the edge of the flower table", False,
     "a street corner near a temple gate in South India in the early morning, slightly out of focus: the temple gateway far behind, garlands on poles",
     "her flower stall near the temple, out of focus: heaps of jasmine and marigolds at the lower right"),
    (34, "f", 60, "vegetable and herb seller at a village market", "a moss-green short-sleeved blouse and a mustard-yellow cotton saree with a moss-green border, silver and wooden bangles",
     "her low tarpaulin stall with bamboo trays of green and red amaranth, bunches of herbs, a heap of turmeric roots, ginger and long lemongrass",
     "keeps tying a small bunch of herbs", "lays the bunch back on the tray", "her hands resting on the edge of the herb trays", False,
     "a village market in South India in the morning, slightly out of focus: other ground stalls, palm trees, villagers far behind",
     "her herb stall, out of focus: green bunches at the lower right"),
    (35, "f", 63, "owner of a small grocery shop in a lane", "a dark blue short-sleeved blouse and a maroon cotton-silk saree with a gold border, gold and red bangles and an old gold watch",
     "her wood-and-glass front counter with glass sweet jars, a tray of biscuits and boxes of matches and candles",
     "keeps tapping the lid of a glass sweet jar", "lets go of the jar and rests her hand on the counter", "her hands resting on the counter beside the glass jars", False,
     "a small grocery shop in a South Indian residential lane, slightly out of focus: iron shelves packed with small sacks of rice, spice packets hanging in strings",
     "her grocery shop, out of focus: shelves of goods behind her"),
    (36, "f", 66, "mending tailor at a market corner", "a blue-grey short-sleeved blouse and a beige-brown dotted cotton saree, tarnished silver bangles and a colourful thread bracelet",
     "her old black iron treadle sewing machine under a small tarp roof, a wooden box of coloured thread and a floral cloth being mended",
     "keeps smoothing the floral cloth under the needle", "lays the cloth back on the machine", "her hands resting on the sewing-machine table", False,
     "the edge of a South Indian market, slightly out of focus: a small tarp roof, a low plastic stool, market stalls far behind",
     "her mending corner, out of focus: the sewing machine and tarp roof behind her"),
    (37, "f", 70, "itinerant fruit seller with a shoulder pole", "a faded earth-orange short-sleeved blouse and a faded blue cotton saree with an orange border tucked up to the calves, faded old plastic bangles",
     "her two big bamboo baskets, one full of ripe yellow mangoes and one of bananas and oranges, partly covered with banana leaves",
     "keeps turning a mango in her hand", "puts the mango back in the basket", "her hands resting on the rim of the fruit basket", False,
     "the entrance of a market lane in South India, slightly out of focus: a low wall, her bamboo shoulder pole leaning on it, people far behind",
     "her fruit baskets at the market lane, out of focus: mangoes at the lower right"),
    (38, "f", 59, "seller of pottery and potted plants", "an earth-brown short-sleeved blouse and a brick-orange cotton saree with a brown border, wooden and silver bangles",
     "her low wooden shelf of small terracotta pots with green plants and red-brown clay pots and vases",
     "keeps turning a small potted plant to show its best side", "sets the pot back on the shelf", "her hands resting on the edge of the pottery shelf", False,
     "an open-air market in South India, slightly out of focus: other stalls, trees, shoppers far behind",
     "her pottery and plant stall, out of focus: green plants in clay pots at the lower right"),
    (39, "f", 67, "roadside tea seller under a big tree", "a dark red short-sleeved blouse and a dark green cotton saree with a gold border, green and red glass bangles",
     "her small wooden table with an old aluminium tea kettle, a tray of glasses, a cloth-wrapped flask of hot water and a jar of sweets",
     "keeps slowly lining up the tea glasses on the tray", "sets one glass back on the tray", "her hands resting on the edge of the tea table", False,
     "a roadside spot under a huge old tree at the head of a lane in South India, slightly out of focus: low plastic stools and a wooden bench around the trunk",
     "her roadside tea spot, out of focus: the tea kettle at the lower right, the big tree behind"),
    (40, "f", 71, "veteran cloth and shawl seller at a market", "an ivory short-sleeved blouse and an old soft navy-violet silk saree with a silver border, one tarnished silver bangle on each wrist",
     "her small old wooden stall with folded cloths in dark purple, brown, navy and maroon stacked in neat piles",
     "keeps smoothing a folded shawl on the pile with her palm", "lays the shawl back on the pile", "her hands resting on the folded cloths", False,
     "an old South Indian fabric market, slightly out of focus: other cloth stalls, shawls and saris hanging on display",
     "her cloth stall, out of focus: hanging shawls behind her"),
]

KHONG_DAU = str.maketrans("àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ", "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd")


def tai_anh(csv_path):
    from PIL import Image
    import io
    rows = list(csv.reader(open(csv_path, encoding="utf-8")))[2:]
    os.makedirs(os.path.join(ROOT, BT40), exist_ok=True)
    for r in rows:
        n = int(r[0])
        for kind, url in (("nv", r[4]), ("nen", r[5])):
            fid = re.search(r"/d/([\w-]+)", url).group(1)
            req = urllib.request.Request(f"https://drive.google.com/uc?export=download&id={fid}", headers={"User-Agent": "Mozilla/5.0"})
            b = urllib.request.urlopen(req, timeout=120).read()
            Image.open(io.BytesIO(b)).convert("RGB").save(os.path.join(ROOT, BT40, f"{kind}{n:02d}.jpg"), quality=94)
        print("tải ảnh", n)


def ten(n, sex, age, vai):
    nhom = {"m": "nam", "f": "nu"}[sex] + ("-tre" if age < 50 else "-gia")
    slug = re.sub(r"[^a-z0-9]+", "-", vai.lower()).strip("-")
    slug = slug if len(slug) <= 32 else slug[:32].rsplit("-", 1)[0]
    return f"bt{n:02d}-{nhom}-{slug}"


def build():
    out = []
    for n, sex, age, vai, mac, quay, viec, viec2, tay, gang, noi, selfie in NV:
        he, his, him, self_ = ("he", "his", "him", "himself") if sex == "m" else ("she", "her", "her", "herself")
        nguoi = {"m": "man", "f": "woman"}[sex]
        v = {"name": ten(n, sex, age, vai)}
        v.update(TB.CHUNG)
        v.update({
            "TEN_HOC": "the vendor",   # không dùng "the man": cạnh phóng viên nam, "him/his" dễ lẫn hai người
            "VAI_HOC": vai,
            "NGUOI_HOC": (f"a Malayali {nguoi} about {age} years old, exactly as in {his} reference photo (same face, hair, build and clothes): {mac}; "
                          "photorealistic skin and fabric"),
            "GIONG_HOC": GIONG[(sex, "tre" if age < 50 else "gia")],
            "POS_HOC": "CENTRE-RIGHT, behind the stall",
            "SHE_HOC": he, "HER_HOC": his, "HERO_HOC": him, "SELF_HOC": self_,
            "DAO_GANG": f"{he.capitalize()} wears thin clear disposable plastic gloves on both hands." if gang else f"{he.capitalize()} works with bare hands.",
            "DAO_GIU": f"{tay[0].upper() + tay[1:]} at the start of every clip.",
            "TAY_HOC": tay,
            "VIEC_HOC": viec,
            "VIEC2_HOC": viec2,
            "NHIN_HOC": "looks at the interviewer's face, to the left, in three-quarter view, and never looks at the camera",
            "NGHE_HOC": (f"keeps the lips pressed together and looks at the interviewer's face with a friendly attentive face, {tay}; "
                         f"{he} never looks at the camera"),
            "DAO_NGHI": f"the interviewer holding the microphone toward {him}, {tay}",
            "DAO_XE": quay,
            "NEN_PHO": (f"{noi}; the place and the stall look exactly like the background reference photo (an empty view of this place), with {his} stall in front of {him}; "
                        "any signboards are blurred and unreadable"),
            "NEN_HOC": selfie + "; the place looks like the background reference photo; any signboards are blurred and unreadable",
        })
        nam = sex == "m"
        v["NGHE_PV"] = f"holds the microphone still toward {v['TEN_HOC']} and keeps his face pointed at {him}, his head still, the camera seeing only the back of his head"
        v["NHIN_PV"] = (f"keeps his face pointed at {v['TEN_HOC']}'s face, to the right and slightly down, the camera seeing only the back and the right edge of his head; "
                        "he never turns toward the camera")
        if nam:
            v.update({k: PV_NU[k].format(him=him) for k in ("NGUOI_PV", "GIONG_PV", "NHIN_PV", "NGHE_PV")})
        v["LUOT"] = [{"who": w, "text": t, "emo": e, "c": "black", "o": "white", "fx": "none", "phan": p} for w, p, t, e in TB.LUOT]
        refs = {"NGUOI_DAY": [ANH + "robot-talka.png"], "NGUOI_PV": [ANH + (PV_NU["ANH"] if nam else "phong-vien.png")], "NGUOI_HOC": [BT40 + f"nv{n:02d}.jpg"],
                "NEN_PHO": [BT40 + f"nen{n:02d}.jpg"], "NEN_HOC": [BT40 + f"nen{n:02d}.jpg"]}
        for k, ps in refs.items():
            for p in ps:
                if not os.path.isfile(os.path.join(ROOT, p)):
                    print(f"LỖI [{v['name']}] {k}: thiếu ảnh {p} (chạy với --tai-anh <csv>)")
        v["refs"] = refs
        out.append(v)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--tai-anh" in sys.argv:
        tai_anh(sys.argv[sys.argv.index("--tai-anh") + 1])
    data = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.abspath(OUT), f"({len(data)} biến thể; nam {sum(1 for x in NV if x[1] == 'm')}, nữ {sum(1 for x in NV if x[1] == 'f')})")
