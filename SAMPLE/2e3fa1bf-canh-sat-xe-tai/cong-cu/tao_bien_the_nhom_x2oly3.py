"""Nhóm x2oly3 (kịch bản B, hook): 5 biến thể giữ nhân vật + tình huống của biến thể mẫu, chỉ đổi câu sai ở hook
(kèm câu hỏi lại ở lượt 2, câu nói lại đúng ở lượt 3, HOOK_TV / HOOK_CS). Lượt 4 giữ nguyên.
    runtime\\python.exe SAMPLE\\2e3fa1bf-canh-sat-xe-tai\\cong-cu\\tao_bien_the_nhom_x2oly3.py
Ghi BIEN-THE-NHOM-x2oly3.json, dùng lại ảnh refs của biến thể mẫu."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tao_bien_the as MAU  # noqa: E402

# (tên, câu sai, cụm sai (to), câu hỏi lại, câu nói lại đúng, cụm đúng (to), HOOK_TV, HOOK_CS)
HOOKS = [
    ("hook-hunger", "Officer, I have hunger!", "have hunger", "Ma'am, you mean you are hungry?", "Oh no! Yes, I am hungry.", "I am hungry",
     "the driver says the line in a plain, hopeful way, chin slightly lifted, an eager half-smile, sure that the line is right",
     "eyebrows raised, a small polite puzzled frown, the head tilted slightly, as if checking whether the driver means food"),
    ("hook-cold", "Officer, I have cold!", "have cold", "Ma'am, you mean you are cold?", "Oh no! Yes, I am cold.", "I am cold",
     "the driver says the line in a cheerful, slightly shivery way, shoulders lifted a little, a wide confident smile",
     "eyebrows raised, the head tilted slightly, a small concerned frown, as if wondering about the weather"),
    ("hook-agree", "Officer, I am agree!", "am agree", "Ma'am, you mean you agree?", "Oh no! Yes, I agree.", "I agree",
     "the driver says the line in a friendly, nodding, over-confident way, a broad smile, sure that the line is perfect",
     "eyebrows raised and a small polite puzzled frown, the head tilted slightly, as if trying to understand what the driver agrees with"),
    ("hook-boring", "Officer, I am boring!", "am boring", "Ma'am, you mean you are bored?", "Oh no! Yes, I am bored.", "I am bored",
     "the driver says the line in a sighing, easy-going way, a tired half-smile, completely sure of the line",
     "eyebrows raised, the lips pressed in an amused effort not to smile, the head tilted slightly, as if trying to work out the meaning"),
    ("hook-thirty", "Officer, I have thirty years!", "have thirty years", "Ma'am, you mean you are thirty years old?", "Oh no! Yes, I am thirty years old.", "I am thirty years old",
     "the driver says the line in a bright, proud, confident way, a wide smile, completely sure of the line",
     "eyebrows raised and a small polite puzzled frown, the head tilted slightly, as if checking what was just said"),
]


def main():
    base = json.load(open(os.path.join(HERE, "..", "BIEN-THE-2E3FA1BF-CANH-SAT-XE-TAI-HOOK.json"), encoding="utf-8"))[0]
    out = []
    for (name, sai, to_sai, hoi, dung, to_dung, tv, cs) in HOOKS:
        v = {k: x for k, x in base.items() if k not in ("name", "LUOT", "HOOK_TV", "HOOK_CS")}
        v = {"name": name, **v, "HOOK_TV": tv, "HOOK_CS": cs}
        l = MAU.luot(sai, hoi, dung)
        l[0]["to"] = to_sai
        l[2]["to"] = to_dung
        v["LUOT"] = l
        out.append(v)
    p = os.path.join(HERE, "..", "BIEN-THE-NHOM-x2oly3.json")
    json.dump(out, open(p, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.normpath(p), len(out), "biến thể")


if __name__ == "__main__":
    main()
