"""Sinh BIEN-THE-TAXI-GIA-SU-AI.json (biến thể đầu bám sát video mẫu).
  runtime\\python.exe SAMPLE\\taxi-gia-su-ai\\cong-cu\\tao_bien_the.py
Lượt phần 1 thứ n = CẢNH n của phần 1 (thứ tự người nói khớp bảng S trong tao_kich_ban.py); lượt phần 2 = lần lượt từng cảnh ghép 2 lớp.
Cảnh KHÔNG LỜI: "text" = MARKER (gen.py của thể loại đổi thành rỗng trước khi gen; post.py bỏ khỏi phụ đề).
Phần 1: lượt tiếng Anh có "dich" tiếng Tây Ban Nha, lượt tiếng Tây Ban Nha có "dich" tiếng Anh (như phụ đề video mẫu). Phần 2: không dịch.
Ảnh tham chiếu: SAMPLE/taxi-gia-su-ai/anh/<KHOÁ>.png (gen bằng cong-cu/gen_anh_tham_chieu.py, người dùng đồng ý 11/11/2026);
robot DAY dùng ảnh có sẵn SAMPLE/canh-sat-gia-su-ai/anh/DAY.png. Ảnh nào chưa có thì bỏ khỏi refs."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "BIEN-THE-TAXI-GIA-SU-AI.json")
MARKER = "[KHONG LOI]"   # phải trùng MARKER trong app/production/types/taxi-gia-su-ai/gen.py và post.py
CAM = None

# (phần, người nói, lời, cảm xúc, dịch hoặc None, thêm)
LUOT = [
    # PHẦN 1 - taxi
    (1, "khach", "Can you take a left on Fifth, so we can avoid the traffic?", "decisive, skeptical", "¿Puedes dar vuelta a la izquierda en la Quinta, para evitar el tráfico?", {}),
    (1, "hoc", "Fifth... sorry. I don't understand.", "confused, embarrassed", "Eh, quinta... perdón. No entiendo.", {}),
    (1, "khach", "Take the left on... You missed the turn!", "decisive, surprised", "Da vuelta a la izquierda en... ¡Te pasaste la vuelta!", {}),
    (1, "khach", "I just told you to take the left!", "decisive", "¡Acabo de decirte que dieras vuelta a la izquierda!", {}),
    (1, "khach", "Yeah, I'm in a cab. The driver barely speaks English.", "skeptical", "Sí, voy en un taxi. El conductor apenas habla inglés.", {}),
    (1, "khach", "I have to repeat everything I say.", "skeptical, doubtful", "Tengo que repetir todo lo que digo.", {}),
    (1, "hoc", CAM, "", None, {}),        # P: tài xế nhìn điện thoại, đánh giá tệ
    # gara
    (1, "quanly", "Arjun, your ratings are the best we've got. Customers love your conversations as well.", "proud, cheerful",
     "Arjun, tus calificaciones son las mejores que tenemos. A los clientes también les encantan tus conversaciones.", {}),
    (1, "quanly", "You get our brand new car!", "excited", "¡Te toca nuestro carro nuevo!", {}),
    (1, "arjun", CAM, "", None, {}),      # K: trao chìa khoá
    (1, "arjun", CAM, "", None, {}),      # X: taxi mới, đồng nghiệp vỗ tay
    (1, "arjun", "You want the new car? Learn to talk to the customers first.", "playful, proud",
     "¿Quieres el carro nuevo? Primero aprende a hablar con los clientes.", {}),
    (1, "hoc", CAM, "", None, {}),        # T: tài xế buồn
    # phòng khách (tiếng Tây Ban Nha, dịch tiếng Anh)
    (1, "con", "Papá, ¿qué pasó?", "worried", "Dad, what happened?", {}),
    (1, "hoc", "Nada, hija.", "worried, calm", "Nothing, sweetheart.", {}),
    (1, "hoc", "Hoy otra vez no pude entender a un cliente.", "worried, embarrassed", "Today again I couldn't understand a customer.", {}),
    (1, "con", "Sabes más inglés del que puedes expresar.", "warm, encouraging", "You know more English than you can express.", {}),
    (1, "con", "Solo te falta practicarlo en voz alta.", "encouraging", "You're just missing practicing it out loud.", {}),
    (1, "hoc", "¿Con quién estás hablando tú?", "curious", "Who are you talking to?", {}),
    (1, "con", "Con mi tutor de inglés con inteligencia artificial.", "proud, cheerful", "With my English tutor with artificial intelligence.", {}),
    (1, "con", CAM, "", None, {}),        # PH: cận điện thoại có robot
    (1, "con", "Es como hablar con un maestro de verdad.", "excited", "It's like talking with a real teacher.", {}),
    (1, "con", "Te corrige mientras hablas y practicas conversaciones de la vida real.", "excited",
     "It corrects you while you speak and you practice real-life conversations.", {}),
    (1, "hoc", "Pero las clases de inglés son muy caras.", "worried", "But English classes are very expensive.", {}),
    (1, "con", "No necesitas tomar clases.", "reassuring, cheerful", "You don't need to take classes.", {}),
    # PHẦN 2 - tài xế + gia sư AI (ghép 2 lớp)
    (2, "day", "¡Hola! ¿Qué tal tu inglés?", "cheerful", None, {}),
    (2, "hoc", "Más o menos.", "hesitant", None, {}),
    (2, "day", "¿De dónde eres? Where are you from?", "curious", None, {}),
    (2, "hoc", "I am Mexico.", "hesitant", None, {"fx": "wrong", "icon": "x", "to": "I am Mexico", "c": "red"}),
    (2, "day", "Casi. Mejor di: I am from Mexico.", "warm, encouraging", None, {}),
    (2, "hoc", "I am from Mexico.", "proud", None, {"fx": "right", "icon": "check", "to": "from", "c": "green"}),
    (2, "hoc", "Siempre me confundo con eso.", "embarrassed", None, {}),
    (2, "day", "Para eso estoy yo. Para ayudarte a hablar bien.", "warm", None, {}),
    (2, "hoc", "Pero no tengo dinero.", "worried", None, {"icon": "dollar"}),
    (2, "day", "¿Qué? No necesitas dinero. Puedes practicar inglés gratis.", "reassuring", None, {}),
    (2, "day", "No es como las otras apps o cursos caros.", "warm", None, {}),
    (2, "hoc", "¿Es en serio?", "surprised", None, {}),
    (2, "day", "Claro, nada de trampas.", "cheerful", None, {}),
    (2, "day", "Solo práctica real de conversación en inglés con tu tutor de inteligencia artificial.", "warm", None, {}),
    (2, "hoc", "¿Como un tutor real?", "curious, hopeful", None, {}),
    (2, "day", "Sí. Corrijo tu gramática, tu pronunciación y te ayudo a hablar con confianza.", "warm, encouraging", None, {}),
    (2, "hoc", "Ok, vamos a intentarlo.", "hopeful, delighted", None, {}),
    (2, "day", "Muy buena decisión. Vamos a hablar inglés juntos.", "cheerful, upbeat", None, {}),
]

NHIN = "keeps the eyes where the clip's EYE LINE says while speaking, never into the lens"

V = {
    "name": "taxi-mexico-goc",
    "TEN_HOC": "Miguel",
    "NGUOI_HOC": "a stylized 3D-animated Mexican man in his mid-forties, thick curly black hair, a thick black moustache, warm brown skin, kind tired brown eyes, a slightly heavy build, a dark chocolate-brown polo shirt with a few thin cream and tan horizontal stripes across the chest and sleeves, dark brown trousers",
    "GIONG_HOC": "a warm, soft, slightly hoarse man's baritone around 105-130 Hz, Mexican Spanish; his English is slow and broken with a heavy Mexican accent",
    "VAI_HOC": "taxi driver",
    "POS_HOC": "driver-seat",
    "NGHE_HOC": "keeps the mouth closed and looks where the clip's EYE LINE says (at the road, at the floor or at whoever is speaking), small natural blinks, hands where the clip puts them",
    "NHIN_HOC": NHIN,
    "NHIN_HOC@2": "looks into the lens, as if talking to the AI tutor on the phone mounted on the dashboard",
    "TEN_KHACH": "the passenger",
    "NGUOI_KHACH": "a stylized 3D-animated American businessman in his thirties, neatly combed dark-brown hair, clean-shaven, a navy-blue suit with a white shirt and a dark-blue tie",
    "GIONG_KHACH": "a quick, clipped, impatient American man's voice, a clear tenor around 140-170 Hz, sharper and higher than the driver",
    "VAI_KHACH": "taxi passenger",
    "POS_KHACH": "back-seat",
    "NGHE_KHACH": "keeps the mouth closed, the phone at his ear, looking out of the side window",
    "NHIN_KHACH": NHIN,
    "TEN_QUANLY": "the manager",
    "NGUOI_QUANLY": "a stylized 3D-animated taxi-company manager in his early sixties, neatly combed silver-grey hair, a short grey beard, a navy-blue suit with a white shirt and a dark tie, a plain brown clipboard and a pen",
    "GIONG_QUANLY": "a warm, hearty, proud older American man's voice around 115-135 Hz, upbeat and generous",
    "VAI_QUANLY": "taxi company manager",
    "POS_QUANLY": "garage-centre",
    "NGHE_QUANLY": "keeps the mouth closed and smiles at whoever is speaking, holding his clipboard",
    "NHIN_QUANLY": NHIN,
    "TEN_ARJUN": "Arjun",
    "NGUOI_ARJUN": "a stylized 3D-animated young Indian man in his mid-twenties, slim, short neat black hair, a trimmed black beard, a light-grey button-up shirt with rolled sleeves, dark jeans, a silver wristwatch",
    "GIONG_ARJUN": "a smooth, light, smug young man's voice around 140-160 Hz, American English with a slight Indian lilt, a little mocking",
    "VAI_ARJUN": "young taxi driver",
    "POS_ARJUN": "garage-right",
    "NGHE_ARJUN": "keeps the mouth closed with a confident smile, looking at whoever is speaking",
    "NHIN_ARJUN": NHIN,
    "TEN_CON": "Lucía",
    "NGUOI_CON": "a stylized 3D-animated Mexican teenage girl about seventeen, long wavy chestnut-brown hair, big warm brown eyes, mint-green long-sleeved pajamas with small white polka dots, barefoot",
    "GIONG_CON": "a bright, gentle, clear teenage girl's voice around 230-260 Hz, Mexican Spanish, caring and upbeat",
    "VAI_CON": "daughter",
    "POS_CON": "living-room",
    "NGHE_CON": "keeps the mouth closed and looks at her father with a caring face",
    "NHIN_CON": NHIN,
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": "a sleek feminine humanoid robot with a smooth glossy pearl-white bald head and a softly human-like face, pale blue eyes, soft pale lips that open and move naturally with every word whenever it speaks, thin panel seams on the head, a black segmented mechanical neck, white armoured shoulders with thin glowing blue seams (copy the reference image); realistic 3D render",
    "GIONG_DAY": "a calm, clear, friendly young woman's voice around 180-210 Hz with a very slight synthetic digital sheen, neutral Latin American Spanish and clear American English",
    "VAI_DAY": "AI tutor",
    "NHIN_DAY": "looks straight into the lens, as if talking to the person on the call",
    "NEN_DAY": "a plain deep black background with one thin soft white glowing arc behind the head",
    "NEN_HOC": "the inside of a yellow New York taxi on a sunny afternoon: black seats, and through the rear window a busy avenue with yellow cabs and brick buildings, softly out of focus",
    "XE": "a classic yellow New York taxi with black seats and a blank roof light",
    "NEN_PHO": "a sunny New York-like avenue: tall brick buildings and skyscrapers, trees, other yellow cabs far behind",
    "NEN_GARA": "a big taxi garage: grey concrete floor, a high ceiling with long fluorescent lights, metal lockers and a cork board on the wall, an open roll-up door with yellow taxis and a street outside",
    "NEN_NHA": "a cosy living room: a light-beige sofa, a low wooden coffee table with an open book and a coffee cup on a saucer, tall windows with sheer white curtains, a potted plant",
    "DAO_DIEN_THOAI_KH": "a black smartphone",
    "DAO_DIEN_THOAI_TX": "an old black smartphone with a glowing screen",
    "DAO_CHIA_KHOA": "a set of two new silver car keys on a ring with a black key fob",
    "DAO_COC": "a plain white ceramic mug",
    "DAO_DIEN_THOAI": "a blue smartphone whose screen shows only a friendly white humanoid robot face on a plain blue background, with no text, no buttons and no icons",
    "nguoi_theo_canh": True,
}

ANH = {"HOC": "SAMPLE/taxi-gia-su-ai/anh/HOC.png", "KHACH": "SAMPLE/taxi-gia-su-ai/anh/KHACH.png", "QUANLY": "SAMPLE/taxi-gia-su-ai/anh/QUANLY.png",
       "ARJUN": "SAMPLE/taxi-gia-su-ai/anh/ARJUN.png", "CON": "SAMPLE/taxi-gia-su-ai/anh/CON.png", "DAY": "SAMPLE/canh-sat-gia-su-ai/anh/DAY.png"}


def main():
    v = dict(V)
    v["LUOT"] = []
    for phan, who, text, emo, dich, extra in LUOT:
        if text is None:
            t = {"who": who, "text": MARKER, "emo": "", "fx": "none", "phan": phan}
        else:
            t = {"who": who, "text": text, "emo": emo, "fx": "none", "phan": phan}
            t.update(extra)
            if dich:
                t["dich"] = dich
        v["LUOT"].append(t)
    v["refs"] = {f"NGUOI_{k}": [p] for k, p in ANH.items() if os.path.exists(os.path.join(ROOT, p))}
    json.dump([v], open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n_cam = sum(1 for t in v["LUOT"] if t["text"] == MARKER)
    print(f"Đã ghi {os.path.normpath(OUT)}: {len(v['LUOT'])} lượt ({n_cam} không lời); ảnh tham chiếu: {', '.join(sorted(v['refs']))}")
    print("Người nói phần 1:", " ".join("-" if t["text"] == MARKER else t["who"] for t in v["LUOT"] if t["phan"] == 1))


if __name__ == "__main__":
    main()
