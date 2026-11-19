"""Sinh BIEN-THE-TAXI-TIENG-ANH.json: biến thể lời thoại TOÀN TIẾNG ANH (video tham chiếu 435d2a85-0510_cartoon-turn-car_015_1 = video mẫu của thể loại).
  runtime\python.exe SAMPLE\taxi-gia-su-ai\cong-cu\tao_bien_the_tieng_anh.py
Dùng lại bảng V (nhân vật, nền, đạo cụ) và cấu trúc lượt của tao_bien_the.py; chỉ thay LỜI sang tiếng Anh (gia đình cũng nói tiếng Anh, bỏ lời dịch Tây Ban Nha),
giọng đổi thành tiếng Anh giọng Mỹ-Mexico nhẹ. Kịch bản dùng lại KICH-BAN-TAXI-GIA-SU-AI.txt (25 cảnh phần 1 + ghép 2 lớp phần 2).
Ảnh tham chiếu: ảnh của thể loại (HOC, KHACH, QUANLY, ARJUN, CON, DAY); người dùng không đưa ảnh mới."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tao_bien_the as g

OUT = os.path.join(HERE, "..", "BIEN-THE-TAXI-TIENG-ANH.json")

# lượt n của phần 1 = cảnh n; text None = cảnh không lời (MARKER); phần 2 theo thứ tự cảnh ghép 2 lớp
EN = {
    1: "Can you take a left on Fifth, so we can avoid the traffic?",
    2: "Fifth... sorry. I don't understand.",
    3: "Take the left on... You missed the turn!",
    4: "I just told you to take the left!",
    5: "Yeah, I'm in a cab. The driver barely speaks English.",
    6: "I have to repeat everything I say.",
    8: "Arjun, your ratings are the best we've got. Customers love your conversations as well.",
    9: "You get our brand new car!",
    12: "You want the new car? Learn to talk to the customers first.",
    14: "Dad, what happened?",
    15: "Nothing, sweetheart.",
    16: "Today again I couldn't understand a customer.",
    17: "You know more English than you can express.",
    18: "You just need to practice it out loud.",
    19: "Who are you talking to?",
    20: "With my English tutor with artificial intelligence.",
    22: "It's like talking to a real teacher.",
    23: "It corrects you while you speak, and you practice real-life conversations.",
    24: "But English classes are very expensive.",
    25: "You don't need to take classes.",
}
P2 = [
    "Hi! How is your English?",
    "More or less.",
    "Where are you from?",
    "I am Mexico.",
    "Almost. The better way is to say, I am from Mexico.",
    "I am from Mexico.",
    "I always get confused with that.",
    "That's what I'm here for. To help you speak well.",
    "But I don't have money.",
    "What? You don't need money. You can practice English for free.",
    "It's not like the other apps or expensive courses.",
    "Are you serious?",
    "Of course, no cheating.",
    "Only real conversation practice in English with your AI tutor.",
    "Like a real tutor?",
    "Yes. I correct your grammar and pronunciation, and I help you speak with confidence.",
    "Okay, let's try it.",
    "Great decision. Let's speak English together.",
]


def main():
    v = dict(g.V)
    v["name"] = "taxi-tieng-anh-01"
    for k in ("GIONG_HOC", "GIONG_CON", "GIONG_DAY"):
        v[k] = v[k].replace("Mexican Spanish", "English with a light Mexican accent").replace("neutral Latin American Spanish and clear American English", "clear neutral American English")
    v["GIONG_HOC"] = v["GIONG_HOC"].replace("; his English is slow and broken with a heavy Mexican accent", "; his English is slow, halting and broken at first, with a heavy Mexican accent")
    luot, n1, n2 = [], 0, 0
    for phan, who, text, emo, dich, extra in g.LUOT:
        if text is None:
            n1 += 1
            t = {"who": who, "text": g.MARKER, "emo": "", "fx": "none", "phan": phan}
        else:
            if phan == 1:
                n1 += 1
                new = EN[n1]
            else:
                new = P2[n2]
                n2 += 1
            t = {"who": who, "text": new, "emo": emo, "fx": "none", "phan": phan}
            t.update(extra)
            if phan == 2 and extra.get("to") == "I am Mexico":
                t["to"] = "I am Mexico"
        luot.append(t)
    assert n2 == len(P2), (n2, len(P2))
    v["LUOT"] = luot
    v["refs"] = {f"NGUOI_{k}": [p] for k, p in g.ANH.items() if os.path.exists(os.path.join(g.ROOT, p))}
    json.dump([v], open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Đã ghi {os.path.normpath(OUT)}: {len(luot)} lượt; refs: {', '.join(sorted(v['refs']))}")


if __name__ == "__main__":
    main()
