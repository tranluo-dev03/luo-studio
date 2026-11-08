"""Sinh SAMPLE/robot-pho-tieng-long/BIEN-THE-30-GIAI-DO.json từ bảng CSV của người dùng
("0411_30 biến thể Giải đố.xlsx - 30 biến thể.csv", 08/11/2026): mỗi dòng = bang (trong cột "Kiểu biến thể"), 4 từ lóng + nghĩa (cột 3),
ảnh AI nhân vật (cột 4) và ảnh nền (cột 5). Ảnh đã tải về anh/bt/btNN-nv.webp (robot, nền xanh lá) và btNN-bg.webp (nền) và gắn vào
"refs" (NGUOI_DAY, NEN_PHO). Trang phục (TRANG_PHUC) và nền (NEN_PHO) tả bằng chữ theo ảnh đã xem, vì Muse làm theo chữ hơn ảnh.
Chạy:  runtime\\python.exe SAMPLE\\robot-pho-tieng-long\\cong-cu\\tao_30_bien_the.py
Lời thoại 6 lượt theo mạch video mẫu: 1 mở đầu "F1 is coming to <bang>, so let's talk like a <dân bang>."; 2-4 "<Từ>! That means <nghĩa>.";
5 "And <từ 4>. That means <nghĩa 4>."; 6 "Would you say <từ 1>? Tell me in the comments."  (dòng 11-19 không đổi lời: giữ Texas)."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tao_bien_the import build  # noqa: E402

OUT = os.path.join(HERE, "..", "BIEN-THE-30-GIAI-DO.json")
CSV_JSON = os.path.join(HERE, "_csv30.json")   # bản JSON của CSV (csv.DictReader), giữ lại để sinh lại không cần file gốc
ANH = "SAMPLE/robot-pho-tieng-long/anh/bt"
BADGE = ("OCT 23-25", "US GRAND PRIX")   # giữ như video mẫu (người dùng chỉ yêu cầu đổi câu thoại, nhân vật, nền, từ vựng)

# Trang phục của robot trong ảnh btNN-nv (robot: mặt sứ trắng, mắt xanh nhạt, giáp lục giác trắng viền xanh; chỉ khác đồ mặc ngoài)
TRANG_PHUC = {
    1: "black wayfarer sunglasses and an olive-green nylon bomber jacket worn open over the white chest armor",
    2: "an open blue denim trucker jacket with a few fabric patches on the chest (no readable letters) over the white chest armor",
    3: "black wayfarer sunglasses and an open dark-green Hawaiian shirt with pink and cream hibiscus print over the white chest armor",
    4: "a navy baseball cap and a navy short-sleeve polo shirt over the white chest armor",
    5: "a woven straw sun hat and an open red-and-black buffalo-plaid flannel shirt with rolled sleeves over the white chest armor",
    6: "a yellow construction hard hat and a navy work jacket with grey reflective stripes, worn open over the white chest armor",
    7: "a relaxed cream linen blazer worn open over the white chest armor",
    8: "a crown of pink, orange and white flowers on the head and a white Mexican blouse with bright embroidered flowers across the chest",
    9: "a navy crew-neck sweater with the straps of a black backpack on both shoulders",
    10: "a black short-sleeve shirt under a beige canvas kitchen apron tied at the neck",
    11: "a navy captain's peaked cap with a small gold anchor and a navy short-sleeve captain's jacket with gold buttons and shoulder boards",
    12: "a brown felt cowboy hat and a plain black t-shirt",
    13: "an orange construction hard hat and an open orange high-visibility jacket with grey reflective stripes over the white chest armor",
    14: "a slim black blazer worn open over the white chest armor",
    15: "a white felt cowboy hat with a braided band and a white long-sleeve western shirt",
    16: "a white short-sleeve guayabera shirt with pleated front panels",
    17: "a wide black charro sombrero with silver embroidery and a black charro vest with silver embroidery over the white chest armor",
    18: "an open red-and-black plaid flannel shirt, a black bandana tied around the neck and black leather gloves",
    19: "a brown felt cowboy hat and a red-and-black plaid flannel shirt with rolled sleeves",
    20: "a wide-brimmed natural straw sun hat and an open beige linen shirt over the white chest armor",
    21: "a black baseball cap and a plain white t-shirt",
    22: "a black mariachi charro jacket with gold embroidery and silver buttons",
    23: "an open olive-green windbreaker jacket and a grey knit scarf loosely around the neck",
    24: "an open black leather biker jacket over a black t-shirt",
    25: "a crown of orange marigolds and pink roses on the head and a black lace dress with colourful embroidered flowers on the shoulders",
    26: "black wayfarer sunglasses and a white short-sleeve guayabera shirt",
    27: "a navy baseball cap and a navy short-sleeve polo shirt",
    28: "a sleeveless blue denim vest and a chunky turquoise stone necklace",
    29: "a dark-green knit beanie and a dark-green puffer jacket worn open over the white chest armor",
    30: "a black casino-dealer waistcoat with a black bow tie over the white chest armor",
}

# Nền trong ảnh btNN-bg (mọi biển hiệu để mờ, không đọc được chữ)
NEN_PHO = {
    1: "the Hollywood Walk of Fame at midday: a pink terrazzo sidewalk with brass stars, tall palm trees, historic theatre marquees on both sides, blue sky",
    2: "a sunny East Los Angeles street corner: small shops covered in colourful murals, strings of papel picado flags, a lamp post, palm trees far away",
    3: "Venice Beach: pale sand in the foreground, colourful surfboards leaning on a stand, a painted surf shop and a lifeguard tower, tall palms and the ocean behind",
    4: "a San Diego bay shore at sunset: a long curved bridge on tall pillars over calm water, sandy shore with low dune plants, pastel sky",
    5: "a California vineyard at golden hour: long rows of green vines on a dirt track, rolling golden hills behind, blue sky",
    6: "inside a bright logistics warehouse: a long central aisle between tall steel shelves stacked with cardboard boxes, grey floor, skylights",
    7: "a Bay Area tech office: desks with laptops, a whiteboard, a coffee station and a floor-to-ceiling window showing the bay and a bridge",
    8: "an open-air Mexican market aisle: stalls with fresh produce, hanging dried chiles, woven baskets and painted pottery under striped awnings, palm trees behind",
    9: "the front of a Spanish-style Californian high school: cream stucco buildings with a tiled roof, an iron gate between stone pillars, tall trees, blue sky",
    10: "inside a small Orange County taqueria: a wooden counter, a menu board and a warm neon sign above, tiled floor, a window onto a sunny street",
    11: "the Port of Long Beach: a flat wooden dock in the foreground, stacks of coloured shipping containers, tall blue cranes and a container ship, hazy mountains",
    12: "an Austin music street: brick bars with guitar signs and string lights, a guitar shop window, the Texas Capitol dome and a big star sign in the distance",
    13: "a Houston port and refinery yard: a concrete road between shipping containers, cranes and industrial tanks, the downtown skyline behind",
    14: "an empty Dallas parking lot with the downtown skyline behind: the ball-topped Reunion Tower and glass skyscrapers, a few trees, clear sky",
    15: "an El Paso border street: a road leading to an international bridge with a blue overhead sign, old shopfronts on the left, desert mountains behind",
    16: "the San Antonio River Walk: a calm green canal lined with stone walkways, bald cypress trees, café umbrellas and a stone arched footbridge",
    17: "a San Antonio charreada arena: a sandy rodeo ring with wooden fences, covered wooden stands, Texas flags and faded sponsor boards behind",
    18: "a West Texas ranch at sunset: a dirt track, wooden rail fences, dry grass and scrub, a barn and a flat mesa under an orange sky",
    19: "the Fort Worth Stockyards: a wide dirt street between red-brick western buildings, cattle pens, a water tower, afternoon light",
    20: "the Arizona desert: a dirt trail between tall saguaro and cholla cacti, a rugged rocky peak behind, bright sky",
    21: "a street of old adobe buildings in Tucson's Old Pueblo: earth-coloured walls, wooden doors, cacti in pots, desert mountains behind",
    22: "a downtown Tucson street festival: market booths with pottery, rugs and jars under canopies, an old theatre marquee, mountains behind",
    23: "Chicago's Millennium Park: the mirrored bean sculpture on a stone plaza, glass skyscrapers behind, light clouds",
    24: "a Chicago Little Village street: a large colourful mural on a brick wall, a decorative arch over the street, shopfronts and a lamp post",
    25: "a Pilsen street dressed for Día de Muertos: strings of colourful papel picado across the street, red-brick buildings, murals and marigold decorations",
    26: "Little Havana in Miami: a park entrance with white pillars and an iron gate, palm trees, pastel buildings and small flags, a patterned tiled sidewalk",
    27: "a theme-park main street in Orlando: pastel Victorian shopfronts on both sides and a blue-and-white fairy-tale castle at the end, blue sky",
    28: "an Albuquerque adobe courtyard: earth-coloured adobe walls and wooden beams, dry ground, desert mountains and dozens of hot-air balloons in the sky",
    29: "the Colorado Rockies: a dry mountain meadow, pine forest on the slopes, snow-capped peaks and blue sky with soft clouds",
    30: "the Las Vegas Strip at night: a glowing Eiffel Tower replica, bright neon hotel signs, palm trees and a wet reflective road",
}


def demonym(kind):
    """("California", "a Californian") từ cột "Kiểu biến thể"; không đổi lời -> ("Texas", "a Texan")."""
    m = re.search(r'thành "F1 is coming to ([^"]+)"', kind)
    d = re.search(r'thành "Talk like (an? [\w ]+?)"', kind)
    return (m.group(1).strip(), d.group(1).strip()) if m and d else ("Texas", "a Texan")


def vocab(cell):
    """[(từ, nghĩa nói, nghĩa trên thẻ)] từ "Từ — nghĩa; Từ — nghĩa; ...". Bỏ phần trong ngoặc khi nói; thẻ giữ nghĩa gọn."""
    out = []
    for part in [p.strip() for p in cell.split(";") if p.strip()]:
        tu, nghia = [x.strip() for x in re.split(r"\s+[—–-]\s+", part, maxsplit=1)]
        noi = re.sub(r"\s*\([^)]*\)", "", nghia).strip().rstrip(".")
        noi = noi.split(" / ")[0].strip()   # "yeah, let's go / really?" -> nói vế đầu
        the = re.sub(r"\s*\([^)]*\)", "", nghia).strip()
        out.append((tu, noi, the))
    assert len(out) == 4, cell
    return out


def moc(text, toi_thieu=3):
    """Từ dùng để căn thời điểm: từ đầu tiên có >= `toi_thieu` ký tự chữ/số; không có thì từ đầu."""
    ws = text.split()
    for w in ws:
        if len(re.sub(r"[^A-Za-z0-9]", "", w)) >= toi_thieu:
            return w
    return ws[0]


def main():
    rows = json.load(open(CSV_JSON, encoding="utf-8"))
    data = []
    for i, r in enumerate(rows, 1):
        state, dan = demonym(r["Kiểu biến thể (so với bản gốc)"])
        words = vocab(r["Bộ từ vựng mới"])
        lines = [(f"F1 is coming to {state}, so let's talk like {dan}.", "excited, cheerful")]
        for k, (tu, noi, _) in enumerate(words):
            tu_noi = tu if tu.endswith(("?", "!")) else tu + ("!" if k < 3 else ".")
            lines.append(((f"{tu_noi} That means {noi}." if k < 3 else f"And {tu_noi} That means {noi}."),
                          ["cheerful", "playful, upbeat", "confident, cheerful", "warm, playful"][k]))
        w1 = words[0][0].rstrip("?!.")
        lines.append((f"Would you say {w1}? Tell me in the comments.", "curious, friendly"))
        the = [{"luot": k + 1, "tu": tu.upper(), "nghia": the_, "moc_tu": moc(tu, 2), "moc_nghia": moc(noi)} for k, (tu, noi, the_) in enumerate(words)]
        art = dan.split()[0]   # a / an
        name_dan = " ".join(dan.split()[1:])
        v = build(f"bt{i:02d}-{re.sub(r'[^a-z0-9]+', '-', state.lower()).strip('-')}", TRANG_PHUC[i], NEN_PHO[i] + "; the whole background softly out of focus, any lettering on signs unreadable.",
                  (f"F1 IS IN {state.upper()}", f"TALK LIKE {art.upper()} {name_dan.upper()}"), BADGE, (f"{name_dan.upper()}S SAY", "IT MEANS"), lines, the)
        v["refs"] = {"NGUOI_DAY": [f"{ANH}/bt{i:02d}-nv.webp"], "NEN_PHO": [f"{ANH}/bt{i:02d}-bg.webp"]}
        v["HAU_KY"]["nguon"] = {"dong_csv": r["Tên biến thể"], "anh_nhan_vat": r["Ảnh AI_biến thể"], "anh_nen": r["Ảnh background_biến thể"]}
        for t in v["LUOT"]:
            assert len(t["text"].split()) <= 20, (v["name"], t["text"])
        data.append(v)
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Đã ghi {len(data)} biến thể -> {os.path.normpath(OUT)}")
    for v in data:
        print(f"  {v['name']:28} {v['HAU_KY']['tieu_de'][1]:28} | " + " | ".join(c["tu"] for c in v["HAU_KY"]["the"]))


if __name__ == "__main__":
    main()
