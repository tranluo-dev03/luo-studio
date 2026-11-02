"""Thêm vào BIEN-THE-AI-TUTOR-NGOI-DOC.json các biến thể "người nói tiếng Tây Ban Nha học tiếng Anh" (mỗi biến thể: một robot/bối cảnh + bộ 7 cặp từ).
Chạy: python cong-cu/them-bien-the.py  (chạy lại được: biến thể trùng tên thì ghi đè). Nếu chạy lại tao-kich-ban.py (ghi đè file JSON) thì chạy file này sau đó.

Mỗi biến thể: name, NGUOI_DAY (robot + trang phục), TU_THE (tư thế/đạo cụ), NEN (bối cảnh), BANG_TU (7 cặp "tiếng Tây Ban Nha | tiếng Anh | phiên âm", dòng cuối là câu kết).
Chia cảnh: 7 cặp + câu kết = 4 cảnh (2, 2, 2 cặp, cảnh cuối 1 cặp + câu kết), cùng số cảnh với các biến thể 10 cặp."""
import json, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "BIEN-THE-AI-TUTOR-NGOI-DOC.json")
CLOSING = "¡Practica todos los días!"
SIT_TABLE = "sits behind a small round table, both forearms resting on the table, the table edge near the bottom of the frame"

ROBOT = ("a glossy white humanoid robot tutor with a realistic young woman's face, glowing light blue eyes, a smooth bald white head with a small "
         "white headset with blue LED lights, a black mechanical neck and joints with glowing blue accents")
BARE = ROBOT + ", a white armor-like torso with a thin vertical blue light on the chest"

SOFA = ("a cozy living room: a framed family photo on a pale wall, a warm table lamp, a green plant and a woven cushion, softly out of focus")
RESTO = ("a warm restaurant interior with wooden tables and hanging pendant lamps, softly out of focus; on her table a plate of grilled chicken with salad "
         "and a glass of water with a lemon slice")

ANH = {"bt03-buoi-sang": "https://prnt.sc/8dqS7WF0j5la", "bt04-buoi-toi": "https://prnt.sc/dW0L6MWenN95", "bt05-menh-lenh": "https://prnt.sc/a9d04hgP01a3", "bt06-gia-dinh": "https://prnt.sc/n8Clzxwriw3R", "bt07-bua-sang": "https://prnt.sc/tSLRIybfZOBZ", "bt08-nha-hang": "https://prnt.sc/6KEloEHtBZaA", "bt09-sieu-thi": "https://prnt.sc/LOXfBxP-V4ck", "bt10-mua-ao": "https://prnt.sc/GCEJQhwXKk4G", "bt11-tra-tien": "https://prnt.sc/b6oUacpgy4Zb", "bt12-van-phong": "https://prnt.sc/YUHe6dGy475_", "bt13-thoi-tiet": "https://prnt.sc/9Yn34zAcArJR", "robot-hoodie": "https://prnt.sc/H01XLzdTzF0w"}
# Ảnh robot tham chiếu của từng biến thể (link ảnh hoặc trang prnt.sc). Studio tải về và gắn vào ô NGUOI_DAY khi tạo dự án.

V = [
    ("bt03-buoi-sang", BARE, "sits on a brown sofa, hands lightly clasped in front of her chest", SOFA, """Buenos días | Good morning | gud mór-ning
¿Dormiste bien? | Did you sleep well? | did iú slíip uél
Tengo sueño | I'm sleepy | áim slíipi
Me levanté temprano | I woke up early | ái uóuk ap érli
Tengo hambre | I'm hungry | áim jángri
¿Hay café? | Is there coffee? | iz der cófi
Vamos a empezar | Let's get started | lets guet stártid"""),
    ("bt04-buoi-toi", BARE, "sits at a restaurant table, one hand holding a fork with a piece of broccoli, the other forearm resting on the table", RESTO, """Buenas noches | Good evening | gud ívning
Estoy en casa | I'm home | áim jóum
Estoy cansado | I'm tired | áim táierd
Tengo frío | I'm cold | áim cóuld
Apaga la luz | Turn off the light | tern óf de láit
Hasta mañana | See you tomorrow | sí iú tumórou
Que descanses | Sleep well | slíip uél"""),
    ("bt05-menh-lenh", BARE, "sits on a brown sofa, hands lightly clasped in front of her chest", SOFA, """Abre la puerta | Open the door | óupen de dór
Cierra la ventana | Close the window | clóuz de uíndou
Ven aquí | Come here | cam jíer
Siéntate | Sit down | sit dáun
Espera un momento | Wait a moment | uéit a móument
Estoy ocupado | I'm busy | áim bízi
Ya voy | I'm coming | áim cáming"""),
    ("bt06-gia-dinh", BARE, "sits on a brown sofa, hands lightly clasped in front of her chest", SOFA, """Mi mamá | My mom | mái mam
Mi papá | My dad | mái dad
Mi hermano | My brother | mái bróder
Mi hermana | My sister | mái síster
Mi hijo | My son | mái son
Mi hija | My daughter | mái dóter
Mi familia | My family | mái fámili"""),
    ("bt07-bua-sang", BARE, "sits at a breakfast table, one hand holding a white coffee mug, the other forearm resting on the table",
     "a bright kitchen next to a sunny window with a green plant; on the table a plate of scrambled eggs with toast and a bowl of berries", """Quiero café | I want coffee | ái uánt cófi
Un vaso de agua | A glass of water | a glas ov uóter
Un huevo | An egg | an eg
Un poco de pan | Some bread | sam bred
Tengo sed | I'm thirsty | áim zérsti
Está delicioso | It's delicious | its dilíshes
Ya terminé | I'm done | áim don"""),
    ("bt08-nha-hang", BARE, "sits at a restaurant table, one hand holding a fork with a piece of broccoli, the other forearm resting on the table", RESTO, """Una mesa, por favor | A table, please | a téibol plíiz
El menú, por favor | The menu, please | de méniu plíiz
Quiero pollo | I want chicken | ái uánt chíken
Sin cebolla | No onions | nóu ánians
Más agua, por favor | More water, please | mor uóter plíiz
La cuenta, por favor | The check, please | de chek plíiz
Está muy rico | It's very good | its véri gud"""),
    ("bt09-sieu-thi", BARE, "stands in a supermarket aisle behind a shopping cart, both hands on its red handle",
     "a supermarket aisle with shelves of colorful products, softly out of focus; in the cart a milk carton, lettuce, tomatoes and bananas", """Necesito leche | I need milk | ái níid milk
Busco arroz | I'm looking for rice | áim lúking for ráis
¿Cuánto cuesta? | How much is it? | jáu mach iz it
Está barato | It's cheap | its chíip
Está caro | It's expensive | its ekspénsiv
Solo uno | Just one | yast uan
Gracias por su ayuda | Thanks for your help | zanks for iór jelp"""),
    ("bt10-mua-ao", BARE, "stands in a clothing store, one hand holding a pink t-shirt on a hanger",
     "a bright clothing store with racks of shirts in soft colors, softly out of focus", """Me gusta | I like it | ái láik it
No me gusta | I don't like it | ái dóunt láik it
Es muy grande | It's too big | its tú big
Es muy pequeño | It's too small | its tú smól
¿Tienen otra talla? | Do you have another size? | du iú jav anóder sáiz
Quiero probarlo | I want to try it | ái uánt tu trái it
Me queda bien | It fits well | it fits uél"""),
    ("bt11-tra-tien", ROBOT + ", wearing a navy school blazer with a white shirt and a red bow tie and a backpack on her shoulders",
     "stands in a school courtyard, holding a stack of books against her chest",
     "a sunny school courtyard with a modern school building and trees, softly out of focus", """Necesito dinero | I need money | ái níid móni
No tengo efectivo | I have no cash | ái jav nóu cash
Pago con tarjeta | I'll pay by card | áil péi bai card
¿Cuánto debo? | How much do I owe? | jáu mach du ái óu
Aquí tiene | Here you go | jíer iú góu
Quédese con el cambio | Keep the change | kíip de chéinch
Necesito un recibo | I need a receipt | ái níid a risíit"""),
    ("bt12-van-phong", ROBOT + ", wearing a gray blazer over a plain white t-shirt",
     "sits at an office desk, both hands resting on a laptop keyboard",
     "a modern bright office with large windows and desks, softly out of focus", """Voy al trabajo | I'm going to work | áim góuing tu uérk
Estoy listo | I'm ready | áim rédi
Llegué temprano | I'm early | áim érli
Llegué tarde | I'm late | áim léit
Necesito ayuda | I need help | ái níid jelp
Ya terminé | I'm done | áim don
Hasta mañana | See you tomorrow | sí iú tumórou"""),
    ("bt13-thoi-tiet", ROBOT + ", wearing a royal blue blazer over a plain white t-shirt",
     "stands in front of a weather screen, one hand raised in an open presenting gesture",
     "a TV weather studio with a blue screen showing a world map and a cartoon sun-and-cloud icon (no text or numbers), softly out of focus", """Hace calor | It's hot | its jat
Hace frío | It's cold | its cóuld
Está lloviendo | It's raining | its réining
Hay viento | It's windy | its uíndi
Hace sol | It's sunny | its sáni
Necesito una chamarra | I need a jacket | ái níid a yáket
Qué bonito día | What a nice day | uat a náis déi"""),
]


def luot(bang):
    ps = [l.split(" | ") for l in bang.split("\n")]
    groups = [ps[0:2], ps[2:4], ps[4:6], ps[6:7]]
    out = []
    for i, g in enumerate(groups):
        t = " ".join(f"{a.rstrip('.!')}{'' if a.endswith(('?', '!')) else '.'} {b.rstrip('.!')}{'' if b.endswith(('?', '!')) else '.'}" for a, b, _ in g)
        out.append({"who": "day", "text": t + (" " + CLOSING if i == 3 else ""), "emo": "warm, encouraging", "fx": "none"})
    return out


data = json.load(open(P, encoding="utf-8"))
for v in data:
    v.pop("NHAN", None)
    v.setdefault("TU_THE", SIT_TABLE)
base = next(v for v in data if v["name"] == "ai-tutor-es-hoc-anh-robot-hoodie")
base["refs"] = {"NGUOI_DAY": [ANH["robot-hoodie"]]}
names = {"ai-tutor-es-hoc-anh-" + n for n, *_ in V}
data = [v for v in data if v["name"] not in names]
for n, robot, tu_the, nen, bang in V:
    lines = [l.strip() for l in bang.split("\n")]
    assert len(lines) == 7 and all(l.count(" | ") == 2 for l in lines), n
    v = dict(base, name="ai-tutor-es-hoc-anh-" + n, NGUOI_DAY=robot, TU_THE=tu_the, NEN=nen,
             BANG_TU="\n".join(f"{a} | {b} | /{c}/" for a, b, c in (l.split(" | ") for l in lines)) + "\n" + CLOSING)
    v["LUOT"] = luot("\n".join(lines))
    v["refs"] = {"NGUOI_DAY": [ANH[n]]}
    data.append(v)
json.dump(data, open(P, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
print("ok:", len(data), "biến thể")
