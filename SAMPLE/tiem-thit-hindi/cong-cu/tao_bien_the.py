"""Sinh BIEN-THE-TIEM-THIT-HINDI.json: 3 biến thể tiếng Hindi (mẹ đẻ) xen tiếng Anh, cùng 50 cảnh với tiem-thit-tieng-anh.
  runtime\\python.exe SAMPLE\\tiem-thit-hindi\\cong-cu\\tao_bien_the.py
Lượt n = CẢNH n (thứ tự người nói như bảng S của tao_kich_ban.py). Lượt tiếng Anh có "dich" (dòng dịch Hindi chữ Devanagari); lượt Hindi không có.
Ảnh tham chiếu: anh/<KHOÁ>_<A|B|C>.png của thư mục này (gen bằng SAMPLE/_chung/gen-anh-nhan-vat.py); KHACH, CHU, ROBOT dùng lại ảnh của tiem-thit-tieng-anh."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "BIEN-THE-TIEM-THIT-HINDI.json")
GOC = os.path.join(HERE, "..", "..", "tiem-thit-tieng-anh", "cong-cu", "tao_bien_the.py")

spec = importlib.util.spec_from_file_location("tbt_goc", GOC)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

APP = "Talka AI"
CAM = ""


def luot(b, bd, u):
    """b = tên cậu bé (Latin), bd = tên Devanagari, u = cách gọi ông chú (Devanagari)."""
    return [
        ("khach", "Wow, that is a beautiful cut.", "impressed", "वाह, क्या शानदार कटिंग है।"),
        ("tio", "Twenty years, my friend!", "proud", "बीस साल, मेरे दोस्त!"),
        ("khach", "And the kid?", "curious", "और लड़का?"),
        ("tio", "Him? He is nobody. No school, no English.", "proud, playful", "वो? वो कुछ नहीं। न स्कूल, न अंग्रेज़ी।"),
        ("tio", f"Watch this. {b}, say hello.", "playful", f"देखो ज़रा। {bd}, नमस्ते बोलो।"),
        ("tavo", CAM, "", None),
        ("tio", "You see? Nothing. Like talking to a wall.", "playful", "देखा? कुछ नहीं। जैसे दीवार से बात करना।"),
        ("tio", "और ग्राहकों से बात मत करना। ये रहे चाय के पैसे।", "decisive", None),
        ("tavo", f"{u}, आपने कहा था आज हफ़्ते की तनख़्वाह दोगे।", "hopeful, worried", None),
        ("tio", "तनख़्वाह नहीं, छत और खाना देता हूँ तुझे।", "decisive", None),
        ("chu", CAM, "", None),
        ("chu", "Please, my meat delivery didn't come. My restaurant opens at seven.", "worried",
         "प्लीज़, मेरा मीट नहीं आया। मेरा रेस्टोरेंट सात बजे खुलता है।"),
        ("chu", "Can somebody help me?", "worried", "क्या कोई मेरी मदद कर सकता है?"),
        ("tavo", "घबराइए मत, मैं आपकी मदद करता हूँ।", "reassuring", None),
        ("chu", "I'm sorry, I don't speak Hindi.", "confused, worried", "माफ़ कीजिए, मुझे हिंदी नहीं आती।"),
        ("tavo", "यहाँ बैठिए, कृपया।", "decisive", None),
        ("tavo", CAM, "", None),
        ("tavo", CAM, "", None),
        ("chu", "Oh my God. Ten minutes?", "surprised", "हे भगवान! दस मिनट?"),
        ("chu", "Thank you. Really. What is your name?", "warm", "शुक्रिया। सच में। तुम्हारा नाम क्या है?"),
        ("tavo", "माफ़ कीजिए, मुझे समझ नहीं आया।", "embarrassed", None),
        ("chu", f"Hey, take this app. {APP}.", "helpful", f"सुनो, ये ऐप लो। {APP}।"),
        ("chu", "I come back in one month, okay? One month.", "excited", "मैं एक महीने में लौटूँगी, ठीक है? एक महीना।"),
        ("chu", CAM, "", None),
        ("chu", "You saved me today.", "warm", "तुमने आज मुझे बचा लिया।"),
        ("tavo", "You... saved... me... tudei?", "hesitant", "तुमने... आज... मुझे बचाया?"),
        ("robot", "You saved me today. It means: तुमने आज मुझे बचा लिया।", "warm", None),
        ("tavo", "तुमने आज मुझे बचा लिया...", "surprised, expressive", None),
        ("robot", f"Try it with me, {b}. You saved me today.", "encouraging", f"मेरे साथ दोहराओ, {bd}। तुमने आज मुझे बचा लिया।"),
        ("tavo", "You... saved me... today.", "hopeful", "तुमने आज मुझे बचा लिया।"),
        ("robot", "Perfect! Again tomorrow?", "cheerful", "बिल्कुल सही! कल फिर से?"),
        ("tavo", CAM, "", None), ("tavo", CAM, "", None), ("tavo", CAM, "", None), ("tavo", CAM, "", None),
        ("tavo", CAM, "", None), ("tavo", CAM, "", None), ("tavo", CAM, "", None),
        ("chu", "Hi. A month ago someone here cut my order. A young guy. Is he still here?", "friendly",
         "नमस्ते। एक महीने पहले यहाँ किसी ने मेरा ऑर्डर काटा था। एक लड़के ने। क्या वो यहीं है?"),
        ("tio", "Yes, yes, me! I am the master. Twenty years.", "proud", "हाँ, हाँ, मैं! मैं उस्ताद हूँ। बीस साल!"),
        ("chu", "No, the young guy.", "friendly, warm", "नहीं, वो जवान लड़का।"),
        ("tio", "तू चुप रह। इसे अंग्रेज़ी तक नहीं आती। इससे कुछ नहीं होगा।", "decisive", None),
        ("tavo", "Hello. It was me. I cut your order. Ten minutes.", "confident", "नमस्ते। वो मैं था। मैंने आपका ऑर्डर काटा। दस मिनट।"),
        ("chu", "You learned English?", "delighted, warm", "तुमने अंग्रेज़ी सीख ली?"),
        ("tavo", "One month. Every night.", "proud", "एक महीना। हर रात।"),
        ("chu", "I own a restaurant. I need a butcher I can talk to. The job is yours.", "warm, delighted",
         "मेरा एक रेस्टोरेंट है। मुझे ऐसा कसाई चाहिए जिससे बात कर सकूँ। नौकरी तुम्हारी।"),
        ("tavo", "You saved me too.", "warm", "तुमने मुझे भी बचाया।"),
        ("tavo", f"अब मेरा नाम सच में {bd} है, {u}।", "confident", None),
        ("tavo", "बस एक महीना। मैं खाली हाथ आया था, अंग्रेज़ी भी नहीं आती थी।", "proud", None),
        ("tavo", f"आज मेरे पास काम है। {APP}, मुफ़्त डाउनलोड करो।", "upbeat", None),
    ]


# 3 biến thể: tên, cách gọi chú, ngoại hình cậu bé + ông chú, nền chợ. KHACH, CHU, ROBOT giữ như tiem-thit-tieng-anh.
BT = [
    dict(name="raju-tiem-thit-goc", ky="A", b="Raju", bd="राजू", u="चाचा",
         cho="a big busy indoor Indian covered bazaar with a high arched roof, rows of stalls with vegetables, spices and flowers far behind",
         boy="a stylized 3D-animated Indian boy about fourteen, slim, warm wheatish-brown skin, short black hair with a side parting, big dark-brown eyes, a small mole on his left cheek, a light-blue crew-neck T-shirt under a long white canvas apron",
         tio="a stylized 3D-animated stocky Indian man in his fifties, round face, a thick black moustache, bushy eyebrows, a white cotton cap, an orange-and-white checked short-sleeved shirt, a long white butcher's apron with faint stains"),
    dict(name="kabir-tiem-thit-lucknow", ky="B", b="Kabir", bd="कबीर", u="मामा",
         cho="a lively old covered meat-and-vegetable market of a North Indian city, arched brick ceiling, rows of stalls far behind",
         boy="a stylized 3D-animated Indian boy about fifteen, tall and lanky, medium-brown skin, thick curly black hair, bright dark eyes, a mustard-yellow crew-neck T-shirt under a long white canvas apron",
         tio="a stylized 3D-animated lean tall Indian man in his fifties, long face, a grey-streaked thin moustache, short grey stubble, a maroon checked short-sleeved shirt, a long white butcher's apron with faint stains"),
    dict(name="arjun-tiem-thit-delhi", ky="C", b="Arjun", bd="अर्जुन", u="ताऊजी",
         cho="a crowded Delhi-style indoor bazaar hall with a high ceiling, narrow aisles and stalls far behind",
         boy="a stylized 3D-animated Indian boy about thirteen, skinny, light-brown skin, a short buzz cut, large expressive dark eyes, a red crew-neck T-shirt under a long white canvas apron",
         tio="a stylized 3D-animated heavy-set Indian man in his late fifties, bald with a grey fringe, a big handlebar moustache, a navy short-sleeved shirt, a long white butcher's apron with faint stains"),
]


def bien_the(c):
    v = {k: x for k, x in G.V.items() if k != "LUOT"}
    v["name"] = c["name"]
    v["TEN_TAVO"] = c["b"]
    v["NGUOI_TAVO"] = c["boy"]
    v["GIONG_TAVO"] = "a soft, slightly husky teenage boy's voice around 200-230 Hz, Hindi, shy and polite; when he speaks English, a light Indian accent"
    v["NGUOI_TIO"] = c["tio"]
    v["GIONG_TIO"] = "a loud, gravelly, boastful middle-aged man's voice around 120-140 Hz, Hindi; his English has a heavy Indian accent"
    v["NEN_CHO"] = c["cho"]
    v["NEN_SAP"] = ("a traditional Indian meat stall: white tiled back wall, steel hooks on chains, a roll of pink butcher paper on a wall holder, "
                    "a brass hanging scale, warm glowing bulbs")
    v["LUOT"] = []
    for who, text, emo, dich in luot(c["b"], c["bd"], c["u"]):
        t = {"who": who, "text": text, "emo": emo, "fx": "none"} if text else {"who": who, "text": "", "emo": ""}
        if dich:
            t["dich"] = dich
        v["LUOT"].append(t)
    refs = {}
    for k, p in (("TAVO", f"SAMPLE/tiem-thit-hindi/anh/TAVO_{c['ky']}.png"), ("TIO", f"SAMPLE/tiem-thit-hindi/anh/TIO_{c['ky']}.png"),
                 ("KHACH", "SAMPLE/tiem-thit-tieng-anh/anh/KHACH.png"), ("CHU", "SAMPLE/tiem-thit-tieng-anh/anh/CHU.png"),
                 ("ROBOT", "SAMPLE/tiem-thit-tieng-anh/anh/ROBOT.png")):
        if os.path.exists(os.path.join(ROOT, p)):
            refs[f"NGUOI_{k}"] = [p]
    v["refs"] = refs
    return v


def main():
    out = [bien_the(c) for c in BT]
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for v in out:
        print(f"{v['name']}: {len(v['LUOT'])} lượt; refs: {', '.join(sorted(v['refs']))}")


if __name__ == "__main__":
    main()
