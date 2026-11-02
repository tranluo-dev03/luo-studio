"""Tạo file BIEN-THE-TALKA-CO-CHU.json gồm 20 biến thể (theo file "20 biến thể vocab.docx"). Chạy: python cong-cu/tao-20-bien-the.py

Biến thể 1-10: tiếng Tây Ban Nha, tờ checklist mẫu (như biến thể gốc), chỉ đổi danh sách từ + lời đọc.
Biến thể 11-13: tiếng Bồ Đào Nha, giấy kẻ dòng hai cột có bút bi đỏ, icon bên phải từ (ảnh anh-mau/giay-hai-cot.png).
Biến thể 14-20: tiếng Bồ Đào Nha, sổ lò xo, icon bên phải từ, bút máy (ảnh anh-mau/giay-so-tay.png).
Đọc thành tiếng 5 từ đầu của mỗi danh sách (lượt 1, 2, 3, 5, 6 của video); các từ còn lại có trên tờ giấy nhưng không đọc.
Biến thể gốc (tiếng Tây Ban Nha) và bản Bồ Đào Nha (lời quảng cáo) lấy từ phien-ban-cu/BIEN-THE-TALKA-7-BIEN-THE.json (bản 7 biến thể trước đây)."""
import copy, json, os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # SAMPLE/talka-bang-tu-vung
BASE = json.load(open(os.path.join(OUT, "phien-ban-cu", "BIEN-THE-TALKA-7-BIEN-THE.json"), encoding="utf-8"))
ES, PT = BASE[0], BASE[1]
for b in (ES, PT):
    b.pop("HAU_KY", None)
    b.pop("refs", None)
VOCAB_TURNS = (0, 1, 2, 4, 5)   # lượt từ vựng; lượt 4 (động viên) và 7-9 (quảng cáo) giữ nguyên theo biến thể gốc

# icon (Segoe UI Symbol, đơn sắc), cùng thứ tự với danh sách từ
I = dict(tay="✋", binhminh="\U0001F305", nang="☀", trang="\U0001F319", nguoi="\U0001F464", like="\U0001F44D", bat="\U0001F91D", vay="\U0001F44B",
         noi="\U0001F4AC", qua="\U0001F381", cuoi="☺", cua="\U0001F6AA", ok="\U0001F44C", tick="✔", buon="☹", tim="♡",
         co="\U0001F3C1", cuu="\U0001F198", cat="⏳", den="\U0001F4A1", chay="\U0001F3C3", cap="\U0001F4BC", sao="⭐",
         tien="\U0001F4B2", tang="\U0001F4C8", gio="\U0001F6D2", kinh="\U0001F50D", the="\U0001F4B3", mat="\U0001F4B5", tui="\U0001F6CD", vi="\U0001F4B0",
         canhbao="⚠", dung="\U0001F6D1", congan="\U0001F693", bs="\U0001F3E5", bando="\U0001F5FA", coi="\U0001F6A8", gio2="\U0001F4A8",
         hoi="❓", cham="❗", ghim="\U0001F4CD", banhrang="⚙", dongho="⏰", tai="\U0001F442",
         xucxac="\U0001F3B2", tram="\U0001F4AF", dh="⌚", ongtich="☑", het="\U0001F51A",
         dao="\U0001F37D", nuoc="\U0001F4A7", cam="\U0001F6AB", bia="\U0001F37B", nha="\U0001F3E0", sach="\U0001F4D6", noi2="\U0001F5E3", but="\U0001F4DD", lap="\U0001F501", tuc="\U0001F6B6")

# (từ tiếng Tây Ban Nha, từ tiếng Bồ Đào Nha, tiếng Anh, icon)
L = [
    [("Hola", "Olá", "Hello", "tay"), ("Buenos días", "Bom dia", "Good morning", "binhminh"), ("Buenas tardes", "Boa tarde", "Good afternoon", "nang"),
     ("Buenas noches", "Boa noite", "Good night", "trang"), ("¿Cómo estás?", "Como você está?", "How are you?", "nguoi"), ("Estoy bien", "Estou bem", "I'm fine", "like"),
     ("Mucho gusto", "Prazer em conhecer você", "Nice to meet you", "bat"), ("Adiós", "Tchau", "Goodbye", "vay")],
    [("Disculpa", "Com licença", "Excuse me", "noi"), ("Muchas gracias", "Muito obrigado", "Thank you very much", "qua"), ("De nada", "De nada", "You're welcome", "cuoi"),
     ("Con permiso", "Com licença", "Excuse me", "cua"), ("No hay problema", "Sem problema", "No problem", "ok"), ("Está bien", "Tudo bem", "It's okay", "tick"),
     ("Lo siento mucho", "Sinto muito", "I'm very sorry", "buon"), ("No te preocupes", "Não se preocupe", "Don't worry", "tim")],
    [("Estoy listo", "Estou pronto", "I'm ready", "tick"), ("Ya terminé", "Já terminei", "I'm done", "co"), ("Necesito ayuda", "Preciso de ajuda", "I need help", "cuu"),
     ("Un momento", "Um momento", "One moment", "cat"), ("Entendido", "Entendi", "Got it", "den"), ("Voy para allá", "Estou indo", "I'm coming", "chay"),
     ("Estoy ocupado", "Estou ocupado", "I'm busy", "cap"), ("Buen trabajo", "Bom trabalho", "Good job", "sao")],
    [("¿Cuánto cuesta?", "Quanto custa?", "How much is it?", "tien"), ("Está muy caro", "Está muito caro", "It's too expensive", "tang"), ("Lo quiero", "Eu quero", "I want it", "gio"),
     ("Solo estoy mirando", "Estou só olhando", "I'm just looking", "kinh"), ("¿Aceptan tarjeta?", "Aceitam cartão?", "Do you take cards?", "the"),
     ("En efectivo", "Em dinheiro", "In cash", "mat"), ("Necesito una bolsa", "Preciso de uma sacola", "I need a bag", "tui"), ("¿Dónde pago?", "Onde eu pago?", "Where do I pay?", "vi")],
    [("¡Ayuda!", "Socorro!", "Help!", "cuu"), ("¡Cuidado!", "Cuidado!", "Watch out!", "canhbao"), ("¡Detente!", "Pare!", "Stop!", "dung"),
     ("¡Llama a la policía!", "Chame a polícia!", "Call the police!", "congan"), ("Necesito un médico", "Preciso de um médico", "I need a doctor", "bs"),
     ("Estoy perdido", "Estou perdido", "I'm lost", "bando"), ("Es una emergencia", "É uma emergência", "It's an emergency", "coi"),
     ("¡No puedo respirar!", "Não consigo respirar!", "I can't breathe!", "gio2")],
    [("¿Qué pasó?", "O que aconteceu?", "What happened?", "cham"), ("¿Por qué?", "Por quê?", "Why?", "hoi"), ("¿Dónde estás?", "Onde você está?", "Where are you?", "ghim"),
     ("¿Qué haces?", "O que você está fazendo?", "What are you doing?", "banhrang"), ("¿Quién es?", "Quem é?", "Who is it?", "nguoi"),
     ("¿A qué hora?", "Que horas?", "What time?", "dongho"), ("¿Estás seguro?", "Você tem certeza?", "Are you sure?", "tick"), ("¿Me entiendes?", "Você me entende?", "Do you understand me?", "tai")],
    [("Claro", "Claro", "Of course", "tick"), ("Tal vez", "Talvez", "Maybe", "xucxac"), ("Por supuesto", "Com certeza", "Absolutely", "tram"),
     ("Ahora mismo", "Agora mesmo", "Right now", "dh"), ("Todavía no", "Ainda não", "Not yet", "cat"), ("Ya casi", "Quase pronto", "Almost done", "co"),
     ("Es verdad", "É verdade", "It's true", "ongtich")],
    [("Tengo hambre", "Estou com fome", "I'm hungry", "dao"), ("Tengo sed", "Estou com sede", "I'm thirsty", "nuoc"), ("Un vaso de agua", "Um copo de água", "A glass of water", "nuoc"),
     ("Sin hielo", "Sem gelo", "No ice", "cam"), ("Para llevar", "Para viagem", "To go", "tui"), ("Para comer aquí", "Para comer aqui", "For here", "dao"),
     ("La cuenta, por favor", "A conta, por favor", "The check, please", "mat"), ("Está delicioso", "Está delicioso", "It's delicious", "cuoi")],
    [("Ven aquí", "Venha aqui", "Come here", "tay"), ("Siéntate", "Sente-se", "Sit down", "nha"), ("Levántate", "Levante-se", "Get up", "tuc"),
     ("Espera un momento", "Espere um momento", "Wait a moment", "cat"), ("Ten cuidado", "Tome cuidado", "Be careful", "canhbao"), ("Vamos a comer", "Vamos comer", "Let's eat", "dao"),
     ("Ya voy", "Já vou", "I'm coming", "chay"), ("Te quiero", "Eu te amo", "I love you", "tim")],
    [("No sé", "Não sei", "I don't know", "hoi"), ("No entiendo", "Não entendo", "I don't understand", "den"), ("Habla despacio", "Fale devagar", "Speak slowly", "noi2"),
     ("Repite, por favor", "Repita, por favor", "Please repeat", "lap"), ("Estoy aprendiendo inglés", "Estou aprendendo inglês", "I'm learning English", "sach"),
     ("¿Qué significa?", "O que significa?", "What does it mean?", "but"), ("¿Cómo se dice?", "Como se diz?", "How do you say it?", "noi"),
     ("¿Puedes ayudarme?", "Você pode me ajudar?", "Can you help me?", "cuu")],
]


def plain(s):
    return re.sub(r"[¿?¡!]", "", s).strip()


def lower1(s):
    return s if s.startswith("I") else s[:1].lower() + s[1:]


def spoken(lang, nat, en):
    nat, en = lower1(plain(nat)), lower1(plain(en))
    if lang == "es":
        return f"¿Cómo se dice {nat} en inglés? Se dice, {en}. Repite conmigo. {en}."
    return f"Como se diz {nat} em inglês? Se diz, {en}. Repita comigo. {en}."


def make(base, name, lang, words, hk):
    x = copy.deepcopy(base)
    x["name"], x["HAU_KY"] = name, hk
    for i, (nat, en) in zip(VOCAB_TURNS, words[:5]):
        x["LUOT"][i]["text"] = spoken(lang, nat, en)
    return x


def hau_ky(kieu, tieu_de, rows, dau_trai="", but=None, icons=False):
    h = {"giay": kieu, "bang": {"tieu_de": tieu_de, "hang": [{"tu": r[0], **({"icon": I[r[3]]} if icons else {})} for r in rows]}}
    if dau_trai:
        h["bang"]["dau_trai"] = dau_trai
    if but:
        h["but"] = but
    return h


out = []
for n, lst in enumerate(L, 1):
    if n <= 10:   # tiếng Tây Ban Nha, giấy checklist mẫu
        rows = [(es, es, en, ic) for es, _, en, ic in lst]
        out.append(make(ES, f"talka-bt{n:02d}-es", "es", [(r[0], r[2]) for r in rows], hau_ky("checklist", "¿CÓMO SE DICE?", rows)))
    else:
        pass
for n, lst in enumerate(L, 1):   # biến thể 11-20 = bản tiếng Bồ Đào Nha của danh sách 1-10
    rows = [(pt, pt, en, ic) for _, pt, en, ic in lst]
    words = [(r[0], r[2]) for r in rows]
    if n <= 3:   # biến thể 11-13: giấy kẻ dòng hai cột (ảnh giay-hai-cot.png)
        hk = hau_ky("hai-cot", "Como se diz?", rows, "Português", "ballpoint", icons=True)
    else:        # biến thể 14-20: sổ lò xo (ảnh giay-so-tay.png)
        hk = hau_ky("so-tay", "COMO SE DIZ?", rows, but="fountain", icons=True)
    out.append(make(PT, f"talka-bt{n + 10}-pt", "pt", words, hk))

names = [x["name"] for x in out]
assert len(out) == 20 and len(set(names)) == 20, names
json.dump(out, open(os.path.join(OUT, "BIEN-THE-TALKA-CO-CHU.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(out), "bien the")
