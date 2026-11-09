"""Sinh SAMPLE/robot-pho-tieng-long/BIEN-THE-ROBOT-PHO-TIENG-LONG.json từ bảng BIEN_THE bên dưới.
Sửa bảng rồi chạy:
    runtime\\python.exe SAMPLE\\robot-pho-tieng-long\\cong-cu\\tao_bien_the.py
Mỗi biến thể = một vùng/thành phố + 4 từ lóng. Lời thoại 6 lượt theo mạch video mẫu (mở đầu, 3 từ ngắn "X. That means Y.",
một từ dài hơn có giải thích, câu hỏi kêu gọi bình luận). Khoá HAU_KY chỉ dành cho hậu kỳ (tiêu đề, badge, thẻ từ lóng), Muse không thấy.
Mỗi thẻ: tu (chữ to trên thẻ), nghia (dòng IT MEANS), luot (chỉ số lượt 0-based mà robot nói từ đó), moc_tu / moc_nghia (từ trong lời
để căn thời điểm hiện thẻ / hiện nghĩa; mặc định = từ đầu của tu / nghia)."""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIEN-THE-ROBOT-PHO-TIENG-LONG.json")

ROBOT = ("a sleek white humanoid AI robot with a realistic young woman's face: smooth pale synthetic skin on the face, bright light-blue eyes, "
         "natural soft lips, a glossy white helmet-like skull with fine panel seams and no hair, round white ear discs, a black mechanical neck "
         "of cables and pistons, glossy white armor plates on the shoulders, chest and arms with black mechanical joints and a small round "
         "glowing light-blue disc in the middle of the chest.")
GIONG = ("a warm, bright, natural young woman's voice, native American English, like a friendly travel host recording a short tip video, "
         "lively varied intonation with a smile in the voice, clear crisp diction; completely human-sounding, not robotic")
NGHI = "lips closed in a soft smile, head upright, eyes on the lens, arms relaxed at the sides"

# (tên, TRANG_PHUC, NEN_PHO, tiêu đề 2 dòng, badge (trái, phải), nhãn thẻ (trên, dưới), các lượt, các thẻ)
BIEN_THE = [
    ("texan-f1-austin",
     "a light-brown felt cowboy hat with a curved brim sitting on the head, and an open faded light-blue denim shirt worn like a jacket over the white chest armor, sleeves rolled to the elbows",
     "a sunny historic main street in a Texas town at golden hour: two-storey red-brick buildings with wooden balconies and strings of warm bulb lights "
     "across the street, a leafy tree on the left, a cobblestone road leading away into a soft blur; the whole background softly out of focus.",
     ("F1 IS IN TEXAS", "TALK LIKE A TEXAN"), ("OCT 23-25", "US GRAND PRIX"), ("TEXANS SAY", "IT MEANS"),
     [("F1 is rolling into Texas, so let's talk like a Texan.", "excited, cheerful"),
      ("Howdy! That means hello.", "cheerful"),
      ("Y'all! That means you, all of you.", "playful, upbeat"),
      ("Fixin' to. That means about to.", "confident, cheerful"),
      ("And bless your heart. It sounds sweet, but it can mean you poor thing.", "warm, playful"),
      ("Would you say y'all? Tell me in the comments.", "curious, friendly")],
     [{"luot": 1, "tu": "HOWDY", "nghia": "hello"},
      {"luot": 2, "tu": "Y'ALL", "nghia": "you (all of you)", "moc_nghia": "you"},
      {"luot": 3, "tu": "FIXIN' TO", "nghia": "about to", "moc_tu": "fixin"},
      {"luot": 4, "tu": "BLESS YOUR HEART", "nghia": "sweet... or \"you poor thing\"", "moc_tu": "bless", "moc_nghia": "sweet"}]),
    ("aussie-sydney",
     "a wide-brimmed brown Akubra-style bush hat on the head, and an open red-and-black checked flannel shirt worn over the white chest armor, sleeves rolled up",
     "a bright Sydney harbourside promenade on a summer afternoon: a wide stone walkway, a white railing, sparkling blue water and distant sailboats, "
     "a few palm trees and a sandstone building on the right; the whole background softly out of focus.",
     ("SUMMER IN SYDNEY", "TALK LIKE AN AUSSIE"), ("SYDNEY", "TALK LIKE A LOCAL"), ("AUSSIES SAY", "IT MEANS"),
     [("Heading to Sydney? Then let's talk like an Aussie.", "excited, cheerful"),
      ("G'day! That means hello.", "cheerful"),
      ("Arvo. That means afternoon.", "playful, upbeat"),
      ("Reckon. That means I think.", "confident, cheerful"),
      ("And no worries. It sounds casual, and it means it's all fine.", "warm, playful"),
      ("Which one would you use? Tell me in the comments.", "curious, friendly")],
     [{"luot": 1, "tu": "G'DAY", "nghia": "hello", "moc_tu": "gday"},
      {"luot": 2, "tu": "ARVO", "nghia": "afternoon"},
      {"luot": 3, "tu": "RECKON", "nghia": "I think", "moc_nghia": "think"},
      {"luot": 4, "tu": "NO WORRIES", "nghia": "it's all fine", "moc_tu": "worries", "moc_nghia": "fine"}]),
    ("brit-london",
     "a grey tweed flat cap on the head, and an open beige trench coat with the collar turned up worn over the white chest armor",
     "a London street on a bright overcast day: a row of pale Georgian townhouses with black railings, a red telephone box on the left, "
     "a wet grey pavement, a black cab parked far behind; the whole background softly out of focus.",
     ("LONDON CALLING", "TALK LIKE A BRIT"), ("LONDON", "TALK LIKE A LOCAL"), ("BRITS SAY", "IT MEANS"),
     [("Off to London? Then let's talk like a Brit.", "excited, cheerful"),
      ("Cheers! That means thanks.", "cheerful"),
      ("Knackered. That means very tired.", "playful, upbeat"),
      ("Fancy a cuppa? That means want some tea.", "confident, cheerful"),
      ("And Bob's your uncle. It sounds odd, but it just means and there you go.", "warm, playful"),
      ("Would you say cheers? Tell me in the comments.", "curious, friendly")],
     [{"luot": 1, "tu": "CHEERS", "nghia": "thanks"},
      {"luot": 2, "tu": "KNACKERED", "nghia": "very tired", "moc_nghia": "very"},
      {"luot": 3, "tu": "FANCY A CUPPA?", "nghia": "want some tea?", "moc_tu": "fancy", "moc_nghia": "want"},
      {"luot": 4, "tu": "BOB'S YOUR UNCLE", "nghia": "and there you go", "moc_tu": "bob", "moc_nghia": "there"}]),
]


def build(name, trang_phuc, nen, tieu_de, badge, nhan, luot, the):
    return {
        "name": name,
        "TEN_DAY": "the robot host",
        "NGUOI_DAY": ROBOT,
        "TRANG_PHUC": trang_phuc,
        "GIONG_DAY": GIONG,
        "POS_DAY": "center",
        "BOX_DAY": "0.33,0.08,0.67,0.38",
        "VAI_DAY": "teacher",
        "DAO_NGHI": NGHI,
        "NEN_PHO": nen,
        "LUOT": [{"who": "day", "text": t, "emo": e, "fx": "none"} for t, e in luot],
        "HAU_KY": {
            "tieu_de": list(tieu_de),
            "badge": {"trai": badge[0], "phai": badge[1]},
            "nhan_tu": nhan[0],
            "nhan_nghia": nhan[1],
            "the": the,
        },
    }


if __name__ == "__main__":
    data = [build(*row) for row in BIEN_THE]
    for v in data:
        for t in v["LUOT"]:
            assert len(t["text"].split()) <= 20, (v["name"], t["text"])
        for c in v["HAU_KY"]["the"]:
            assert 0 <= c["luot"] < len(v["LUOT"]), (v["name"], c)
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Đã ghi {len(data)} biến thể -> {os.path.normpath(OUT)}")
