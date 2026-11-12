"""Sinh BIEN-THE-TIEM-THIT-TIENG-ANH.json (biến thể đầu bám sát video mẫu).
  runtime\\python.exe SAMPLE\\tiem-thit-tieng-anh\\cong-cu\\tao_bien_the.py
Lượt thứ n = CẢNH n của kịch bản (thứ tự người nói phải khớp bảng S trong tao_kich_ban.py).
Lượt tiếng Anh có "dich" (dòng dịch tiếng Tây Ban Nha); lượt tiếng Tây Ban Nha không có.
Ảnh tham chiếu: đặt ảnh AI người dùng cung cấp vào SAMPLE/tiem-thit-tieng-anh/anh/<KHOÁ>.png rồi chạy lại (ảnh nào chưa có thì bỏ khỏi refs)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "BIEN-THE-TIEM-THIT-TIENG-ANH.json")
APP = "Talka AI"
CAM = ""   # lượt rỗng = cảnh KHÔNG LỜI của kịch bản (who = người có mặt trong cảnh đó)

# (người nói, lời, cảm xúc, dịch tiếng Tây Ban Nha hoặc None)
LUOT = [
    ("khach", "Wow, that is a beautiful cut.", "impressed", "Vaya, qué corte tan bonito."),
    ("tio", "Twenty years, my friend!", "proud", "¡Veinte años, amigo mío!"),
    ("khach", "And the kid?", "curious", "¿Y el niño?"),
    ("tio", "Him? He is nobody. No school, no English.", "proud, playful", "¿Ese? Ese no es nadie. No fue a la escuela, no habla inglés."),
    ("tio", "Watch this. Tavo, say hello.", "playful", "Mira esto. Tavo, saluda."),
    ("tavo", CAM, "", None),   # T: Tavo ngơ ngác, ấp úng không ra tiếng
    ("tio", "You see? Nothing. Like talking to a wall.", "playful", "¿Ves? Nada. Como hablarle a una pared."),
    ("tio", "Y no le hables a los clientes. Para tu refresco.", "decisive", None),
    ("tavo", "Tío, dijo que hoy me pagaba la semana.", "hopeful, worried", None),
    ("tio", "Te pago con techo y comida.", "decisive", None),
    ("chu", CAM, "", None),    # X: bà chủ bước vào chợ ráo riết tìm quầy thịt
    ("chu", "Please, my meat delivery didn't come. My restaurant opens at seven.", "worried", "Por favor, no me llegó la carne. Mi restaurante abre a las siete."),
    ("chu", "Can somebody help me?", "worried", "¿Alguien me puede ayudar?"),
    ("tavo", "Tranquila. Yo le ayudo.", "reassuring", None),
    ("chu", "I'm sorry, I don't speak Spanish.", "confused, worried", "Lo siento, no hablo español."),
    ("tavo", "Aquí, siéntese, por favor.", "decisive", None),
    ("tavo", CAM, "", None),   # D2: chặt thịt rất nhanh
    ("tavo", CAM, "", None),   # Y: gói thịt rất nhanh
    ("chu", "Oh my God. Ten minutes?", "surprised", "Dios mío. ¿Diez minutos?"),
    ("chu", "Thank you. Really. What is your name?", "warm", "Gracias. De verdad. ¿Cómo te llamas?"),
    ("tavo", "Perdón, no entiendo.", "embarrassed", None),
    ("chu", f"Hey, take this app. {APP}.", "helpful", f"Oye, toma esta app. {APP}."),
    ("chu", "I come back in one month, okay? One month.", "excited", "Vuelvo en un mes, ¿sí? Un mes."),
    ("chu", CAM, "", None),    # E: bà chủ hôn lên trán Tavo
    ("chu", "You saved me today.", "warm", "Hoy me salvaste."),
    ("tavo", "You... saved... me... tudei?", "hesitant", "¿Me salvaste hoy?"),
    ("robot", "You saved me today. It means: me salvaste hoy.", "warm", "Me salvaste hoy. Significa: me salvaste hoy."),
    ("tavo", "Me salvaste hoy...", "surprised, expressive", None),   # ngỡ ngàng khi hiểu ra ý nghĩa
    ("robot", "Try it with me, Tavo. You saved me today.", "encouraging", "Dilo conmigo, Tavo. Me salvaste hoy."),
    ("tavo", "You... saved me... today.", "hopeful", "Me salvaste hoy."),
    ("robot", "Perfect! Again tomorrow?", "cheerful", "¡Perfecto! ¿Mañana otra vez?"),
    ("tavo", CAM, "", None),   # Q1, Q2, Q5, Q3, Q6, Q7, Q4: montage 7 ngày vừa làm việc vừa học bằng app, mỗi cảnh ~2,5 s
    ("tavo", CAM, "", None),
    ("tavo", CAM, "", None),
    ("tavo", CAM, "", None),
    ("tavo", CAM, "", None),
    ("tavo", CAM, "", None),
    ("tavo", CAM, "", None),
    ("chu", "Hi. A month ago someone here cut my order. A young guy. Is he still here?", "friendly",
     "Hola. Hace un mes alguien de aquí me preparó el pedido. Un chico joven. ¿Sigue aquí?"),
    ("tio", "Yes, yes, me! I am the master. Twenty years.", "proud", "¡Sí, sí, yo! Yo soy el maestro. ¡Veinte años!"),
    ("chu", "No, the young guy.", "friendly, warm", "No, el chico joven."),
    ("tio", "Tú, cállate. Este ni inglés sabe. De este no sale nada.", "decisive", None),
    ("tavo", "Hello. It was me. I cut your order. Ten minutes.", "confident", "Hola. Fui yo. Yo te preparé el pedido. Diez minutos."),
    ("chu", "You learned English?", "delighted, warm", "¿Aprendiste inglés?"),
    ("tavo", "One month. Every night.", "proud", "Un mes. Cada noche."),
    ("chu", "I own a restaurant. I need a butcher I can talk to. The job is yours.", "warm, delighted",
     "Tengo un restaurante. Necesito un carnicero con quien poder hablar. El trabajo es tuyo."),
    ("tavo", "You saved me too.", "warm", "Tú también me salvaste."),
    ("tavo", "Ahora sí me llamo Tavo, tío.", "confident", None),
    ("tavo", "Un mes. Eso es todo. Yo llegué sin nada y sin inglés.", "proud", None),
    ("tavo", f"Hoy tengo trabajo. {APP}. Bájala gratis.", "upbeat", None),
]

NHIN = "keeps the eyes where the clip's EYE LINE says while speaking"

V = {
    "name": "tavo-tiem-thit-goc",
    "TEN_TAVO": "Tavo",
    "NGUOI_TAVO": "a stylized 3D-animated Latino boy about fourteen, slim, warm brown skin, short dark curly hair with faded sides, big dark-brown eyes, a small mole on his left cheek, a light-blue crew-neck T-shirt under a long white canvas apron",
    "GIONG_TAVO": "a soft, slightly husky teenage boy's voice around 200-230 Hz, Mexican Spanish, shy and polite; when he speaks English, a light Mexican accent",
    "VAI_TAVO": "boy helper",
    "POS_TAVO": "behind-counter",
    "NGHE_TAVO": "keeps the mouth closed and looks at whoever is speaking (or down at his work when the clip says so), small natural blinks",
    "NHIN_TAVO": NHIN,
    "TEN_TIO": "the butcher",
    "NGUOI_TIO": "a stylized 3D-animated stocky Mexican man in his fifties, round face, a thick black moustache, bushy eyebrows, a white puffy cook's cap, a green plaid short-sleeved shirt, a long white butcher's apron with faint stains",
    "GIONG_TIO": "a loud, gravelly, boastful middle-aged man's voice around 120-140 Hz, Mexican Spanish; his English has a heavy Mexican accent",
    "VAI_TIO": "butcher (the boy's uncle)",
    "POS_TIO": "behind-counter",
    "NGHE_TIO": "keeps the mouth closed and looks at whoever is speaking, arms relaxed",
    "NHIN_TIO": NHIN,
    "TEN_KHACH": "the customer",
    "NGUOI_KHACH": "a stylized 3D-animated man in his late thirties, tall, slicked-back black hair, a long straight nose, clean-shaven, a crisp white polo shirt",
    "GIONG_KHACH": "a relaxed, friendly American man's voice, warm baritone around 130-150 Hz",
    "VAI_KHACH": "customer",
    "POS_KHACH": "customer-side",
    "NGHE_KHACH": "keeps the mouth closed and looks toward the counter",
    "NHIN_KHACH": NHIN,
    "TEN_CHU": "the restaurant owner",
    "NGUOI_CHU": "a stylized 3D-animated woman in her early forties, dark-brown hair in a low bun with a small silver hair clip, big hazel eyes, a dark plum button-up blouse with rolled sleeves, khaki trousers",
    "GIONG_CHU": "a warm, quick, expressive American woman's voice around 200-220 Hz",
    "VAI_CHU": "restaurant owner",
    "POS_CHU": "customer-side",
    "NGHE_CHU": "keeps the mouth closed and looks at whoever is speaking, attentive",
    "NHIN_CHU": NHIN,
    "TEN_ROBOT": "the AI tutor",
    "NGUOI_ROBOT": "a sleek female-looking humanoid AI robot exactly like the reference image: a smooth glossy pearl-white helmet-like head with a hexagonal panel line on the forehead, a smooth human-like white face with pale blue eyes and a calm closed-lip smile, a black cable-wrapped mechanical neck, glossy white hexagonal armour plates on the shoulders, chest and arms with thin glowing cyan seams and black joints",
    "GIONG_ROBOT": "a clear, warm, friendly young woman's voice with a very slight synthetic digital sheen, slow and very clear, American accent",
    "VAI_ROBOT": "AI tutor on the phone",
    "POS_ROBOT": "phone-screen",
    "NGHE_ROBOT": "keeps a soft closed-lip smile on the screen",
    "NHIN_ROBOT": "looks straight out of the phone screen at the person holding it",
    "NEN_SAP": "a traditional meat stall: white tiled back wall, steel hooks on chains, a roll of pink butcher paper on a wall holder, a brass hanging scale, warm glowing bulbs",
    "NEN_CHO": "a big busy indoor Latin American market hall with a high arched roof and rows of stalls far behind",
    "NEN_PHONG": "the back room of the stall: white tiled wall, a roll of pink butcher paper on a wall holder, steel hooks on chains, a big wooden chopping block, a small green plastic stool",
    "NEN_DEM": "a small dark storeroom behind the stall, rough plaster wall, stacks of folded canvas sacks",
    "DAO_TIEN": "two small plain silver coins",
    "DAO_SO": "a small blank white notepad",
    "DAO_DAO": "a heavy steel meat cleaver with a wooden handle",
    "DAO_GOI": "four packages of meat wrapped in plain pink butcher paper",
    "DAO_DIEN_THOAI": "a black smartphone",
    "nguoi_theo_canh": True,
}


def main():
    v = dict(V)
    v["LUOT"] = []
    for who, text, emo, dich in LUOT:
        t = {"who": who, "text": text, "emo": emo, "fx": "none"} if text else {"who": who, "text": "", "emo": ""}
        if dich:
            t["dich"] = dich
        v["LUOT"].append(t)
    refs = {}
    for k in ("TAVO", "TIO", "KHACH", "CHU", "ROBOT"):
        p = f"SAMPLE/tiem-thit-tieng-anh/anh/{k}.png"
        if os.path.exists(os.path.join(ROOT, p)):
            refs[f"NGUOI_{k}"] = [p]
    if "NGUOI_ROBOT" not in refs:   # dự phòng khi chưa có anh/ROBOT.png (robot người dùng cung cấp 12/11)
        refs["NGUOI_ROBOT"] = ["SAMPLE/soi-hanh-ly-gia-su-ai/ROBOT-GIA-SU-AI.png"]
    v["refs"] = refs
    json.dump([v], open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Đã ghi {os.path.normpath(OUT)}: {len(v['LUOT'])} lượt; ảnh tham chiếu: {', '.join(sorted(refs))}")


if __name__ == "__main__":
    main()
