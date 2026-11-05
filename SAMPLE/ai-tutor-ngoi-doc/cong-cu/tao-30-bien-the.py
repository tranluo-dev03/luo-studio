"""Tạo BIEN-THE-AI-TUTOR-NGOI-DOC-30.json: 30 biến thể (đổi bộ từ vựng + đổi robot AI + đổi nền) từ cong-cu/30-bo-tu-vung.csv.
Mỗi biến thể gắn 2 ảnh tham chiếu bằng link Drive: refs.NGUOI_DAY (robot) và refs.NEN (nền). Bản đã tải sẵn nằm ở anh-mau/btNN-robot.* và btNN-nen.*.
Chạy: python -I cong-cu/tao-30-bien-the.py"""
import csv, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CLOSING = "¡Practica todos los días!"
ROBOT = ("a glossy white humanoid robot tutor with a realistic young woman's face, light blue eyes, a smooth white head, a black mechanical neck "
         "and joints, and a white armor-like torso with thin blue light lines")
LOOK = [  # đồ đội / trang phục theo ảnh robot của biến thể 1..30; không logo, không chữ
    "wearing black sunglasses and an olive green bomber jacket",
    "wearing a faded denim jacket with plain fabric patches",
    "wearing black sunglasses and a black Hawaiian shirt printed with pink hibiscus and green leaves",
    "wearing a plain navy baseball cap and a navy short-sleeved top over the white armor torso",
    "wearing a straw hat and an open red-and-black buffalo-plaid flannel shirt",
    "wearing a yellow hard hat and a navy work jacket with gray reflective stripes",
    "wearing a cream linen blazer over a white shirt",
    "wearing a crown of colorful flowers and a white Mexican blouse with colorful floral embroidery",
    "wearing a navy knit sweater with a black backpack on her shoulders",
    "wearing a black short-sleeved shirt with a beige apron",
    "wearing a navy captain's cap with gold trim and a navy blazer with gold buttons and shoulder epaulettes",
    "wearing a brown cowboy hat and a plain black t-shirt",
    "wearing an orange hard hat and an orange high-visibility jacket with gray reflective stripes",
    "wearing a black blazer",
    "wearing a white cowboy hat with a woven band and a white long-sleeved shirt",
    "wearing a plain white short-sleeved guayabera shirt",
    "wearing a wide-brimmed black charro sombrero and a black charro vest with silver embroidery",
    "wearing a red-and-black plaid flannel shirt, a black bandana around the neck and black gloves",
    "wearing a brown cowboy hat and a red-and-black plaid flannel shirt worn open like a short shrug",
    "wearing a wide-brimmed straw sun hat and an open beige linen shirt",
    "wearing a plain black baseball cap and a plain white t-shirt",
    "wearing a black mariachi jacket with gold embroidery and matching black trousers",
    "wearing an olive hooded jacket and a light gray scarf",
    "wearing a black leather jacket over a plain black t-shirt",
    "wearing a crown of orange marigold and pink flowers and a black lace dress with colorful floral embroidery",
    "wearing black sunglasses and a plain white short-sleeved guayabera shirt",
    "wearing a plain navy cap and a navy polo shirt",
    "wearing a sleeveless denim vest with a turquoise necklace and bracelet",
    "wearing a dark green knit beanie and an olive hooded puffer jacket",
    "wearing a black vest with a black bow tie over a white shirt",
]
SCENE = [  # nền theo ảnh nền của biến thể 1..30; bỏ hết chữ, biển hiệu, tên thương hiệu
    "a sunny boulevard with a pink star-patterned sidewalk, palm trees and vintage theaters along both sides",
    "a colorful street of small Latino shops covered in bright folk-art murals, with a quiet sidewalk",
    "a sunny beach boardwalk with palm trees, colorful surfboards leaning by a lifeguard tower and small beach shops",
    "an empty sandy beach at soft golden light with a long bridge crossing the calm bay in the distance",
    "green vineyard rows on rolling hills with a dirt path and mountains under a clear sky",
    "a large clean warehouse aisle with tall shelves stacked with cardboard boxes and a gray concrete floor",
    "a bright modern office with a large window overlooking a bay bridge, desks, a coffee machine and a green plant",
    "an open-air Mexican market alley with striped awnings, baskets of fruit and vegetables and blue-and-white talavera pottery",
    "a sunny school courtyard with an old stucco building behind iron gates and tall trees",
    "a small taqueria interior with a wooden counter, warm string lights, a tiled floor and a large window",
    "a busy container port dock with tall cranes, stacked colorful shipping containers and mountains across the water",
    "a lively music street with a guitar-shaped sign, string lights, small restaurants and a capitol dome far down the street",
    "an industrial harbor yard with containers and a city skyline of tall towers in the haze",
    "a quiet downtown street with a city skyline, a round observation tower and glass skyscrapers under a blue sky",
    "a road leading to an international border bridge with low shops on one side and dry mountains in the distance",
    "a green canal walkway with a stone bridge, cypress trees, umbrellas and small cafes along the water",
    "a dirt rodeo arena with wooden fences, bleachers and small flags, softly lit",
    "a ranch at sunset with a dirt path, wooden fences and dry grass under an orange sky",
    "an old western stockyards street with brick buildings, wooden fences and a dirt road",
    "a desert trail with cactus, rocky hills and a flat-topped mesa under a blue sky",
    "a quiet adobe old-town street with low earth-colored buildings and mountains behind",
    "an outdoor craft market with colorful pennants, blue canopies, woven blankets and mountains behind",
    "a city plaza with a giant mirror-like bean-shaped sculpture and tall skyscrapers behind it",
    "a city street with a huge colorful mural on a building wall and an arched gate far down the road",
    "a brick street decorated with colorful cut-paper banners and folk-art murals on the buildings",
    "a sunny plaza with a black-and-white tiled floor, a white arched gate, palm trees and Spanish colonial buildings",
    "a brick-paved main street lined with charming shops leading to a fairytale castle with blue spires",
    "a desert village of adobe houses with many colorful hot air balloons floating over the mountains",
    "a mountain meadow with dry grass, pine trees and a snow-capped peak under a blue sky",
    "a night street of a glowing neon city with bright casino lights, a tall tower replica and long light trails on the road",
]
SIT = "sits behind a small round table, both forearms resting on the table, the table edge near the bottom of the frame"
NO_TEXT = "; no readable text, signs or brand names anywhere, softly out of focus"


def direct(link):
    return "https://drive.google.com/uc?export=download&id=" + re.search(r"/d/([^/?]+)", link).group(1)


def luot(ps):
    f = lambda s: s.rstrip(".!") + ("" if s.endswith(("?", "!")) else ".")
    groups = [ps[0:2], ps[2:4], ps[4:6], ps[6:7]]
    return [{"who": "day", "text": " ".join(f"{f(a)} {f(b)}" for a, b, _ in g) + (" " + CLOSING if i == 3 else ""), "emo": "warm, encouraging", "fx": "none"}
            for i, g in enumerate(groups)]


base = next(v for v in json.load(open(os.path.join(ROOT, "BIEN-THE-AI-TUTOR-NGOI-DOC.json"), encoding="utf-8")) if v["name"] == "ai-tutor-es-hoc-anh-robot-hoodie")
rows = list(csv.reader(open(os.path.join(HERE, "30-bo-tu-vung.csv"), encoding="utf-8-sig")))[1:]
assert len(rows) == len(LOOK) == len(SCENE) == 30
out = []
for n, r in enumerate(rows, 1):
    lines = [l.strip() for l in r[2].splitlines() if l.strip()]
    assert len(lines) == 21, (n, len(lines))
    ps = [tuple(lines[i:i + 3]) for i in range(0, 21, 3)]
    v = dict(base, name=f"ai-tutor-es-hoc-anh-bt{n:02d}", TU_THE=SIT, NGUOI_DAY=f"{ROBOT}, {LOOK[n - 1]}", NEN=SCENE[n - 1] + NO_TEXT,
             BANG_TU="\n".join(f"{a} | {b} | /{c}/" for a, b, c in ps) + "\n" + CLOSING, LUOT=luot(ps),
             refs={"NGUOI_DAY": [direct(r[3])], "NEN": [direct(r[4])]})
    out.append(v)
json.dump(out, open(os.path.join(ROOT, "BIEN-THE-AI-TUTOR-NGOI-DOC-30.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
print("ok:", len(out), "biến thể")
