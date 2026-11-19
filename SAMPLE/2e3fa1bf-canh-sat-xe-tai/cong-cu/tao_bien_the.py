"""Sinh BIEN-THE-2E3FA1BF-CANH-SAT-XE-TAI.json (kịch bản A, goc) và BIEN-THE-2E3FA1BF-CANH-SAT-XE-TAI-HOOK.json (kịch bản B, hook), mỗi file 1 biến thể mẫu.
    runtime\python.exe SAMPLE\2e3fa1bf-canh-sat-xe-tai\cong-cu\tao_bien_the.py
Biến thể mẫu bám sát video gốc: tài xế nữ ~57 tuổi, xe tải xanh, hoàng hôn, cảnh sát nam. Cặp luôn KHÁC GIỚI (sổ tay 3.2): biến thể sau chỉ đổi cả cặp
(tài xế nam + nữ cảnh sát) hoặc đổi tuổi/nghề/phong cách, giữ khác giới. Mọi thứ thuộc nhân vật/bối cảnh/phong cách là token.
Kịch bản B: hook = lượt 1-2. Đổi hook = đổi lời lượt 1 (câu sai) + HOOK_TV/HOOK_CS; lượt 2 (cảnh sát hỏi lại) và lượt 3 (câu sửa) phải khớp câu sai mới;
lượt 4 (khen + gợi ý gia sư AI) giữ nguyên.
Ảnh refs: SAMPLE/2e3fa1bf-canh-sat-xe-tai/anh/HOC.png, CANHSAT.png (gen bằng cong-cu/gen-anh-nhan-vat-that.py, nền xanh lục phẳng)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ANH = "SAMPLE/2e3fa1bf-canh-sat-xe-tai/anh/"

CHUNG = {
    "TEN_CANHSAT": "the officer",
    "NGUOI_CANHSAT": ("a Latino American man in his early thirties, short dark-brown hair with a neat side part, light stubble, warm brown eyes, a tan short-sleeved "
                      "state-trooper uniform shirt with plain shoulder patches and a gold star badge, a plain fluorescent yellow-green safety vest without lettering, "
                      "a black duty belt with holster and radio"),
    "GIONG_CANHSAT": "a relaxed, clear American man's baritone around 110–130 Hz, friendly and polite, warming up when he smiles",
    "VAI_CANHSAT": "state trooper",
    "POS_CANHSAT": "RIGHT",
    "NGHE_CANHSAT": "stands still on the road looking up at the driver with a calm attentive face, mouth closed, hands relaxed by the belt",
    "NHIN_CANHSAT": "keeps looking up at the driver in the cab window, never into the lens",
    "HIM_CANHSAT": "him",
    "TEN_HOC": "the truck driver",
    "NGUOI_HOC": ("a white American woman in her late fifties, a long oval face with fine wrinkles, hazel eyes, thin lips, chin-length light-brown hair with a few "
                  "gray strands and side-swept bangs; an olive-khaki canvas work jacket with yellow-green reflective stripes on the sleeves over a navy work shirt"),
    "GIONG_HOC": ("a warm, slightly husky American woman's voice in her late fifties, around 190–220 Hz, cheerful and a little loud when excited, "
                  "slower and embarrassed after a mistake; a real person, not an actress"),
    "VAI_HOC": "truck driver",
    "POS_HOC": "LEFT",
    "NGHE_HOC": "stays leaning on the window sill looking down at the officer with a friendly attentive face, mouth closed",
    "NHIN_HOC": "keeps looking down at the officer standing below the window, never into the lens",
    "XE": "a big glossy blue American semi-truck cab with chrome steps and tanks, a tall blue side mirror on a metal arm",
    "NEN_DUONG": ("the shoulder of a wide multi-lane highway at sunset: a flat dry field with a few tall palm trees along the road, far-away cars standing still, "
                  "a dramatic pink-and-orange sky with scattered clouds"),
    "SANG": "at sunset, warm golden-orange light",
}

REFS = {"NGUOI_HOC": [ANH + "HOC.png"], "NGUOI_CANHSAT": [ANH + "CANHSAT.png"]}


def luot(sai, hoi, dung):
    return [
        {"who": "hoc", "text": sai, "emo": "proud, cheerful", "fx": "wrong", "c": "red", "icon": "x", "to": "have fifty years"},
        {"who": "canhsat", "text": hoi, "emo": "confused, curious", "fx": "none"},
        {"who": "hoc", "text": dung, "emo": "embarrassed, amused", "fx": "right", "c": "green", "icon": "check", "to": "I am fifty years old"},
        {"who": "canhsat", "text": "Perfect! Practice English every day with an AI tutor.", "emo": "warm, encouraging", "fx": "none"},
    ]


def main():
    a = {"name": "bien-the-01-goc", **CHUNG, "refs": REFS,
         "LUOT": luot("Officer, I have fifty years!", "Ma'am, you mean you are fifty years old?", "Oh no! Yes, I am fifty years old.")}
    b = {"name": "bien-the-01-hook-moi", **CHUNG, "refs": REFS,
         "HOOK_TV": "the driver says the line in a cheerful, over-confident way, chin up, a wide smile, sure that the line is perfect",
         "HOOK_CS": "eyebrows raised and a small polite puzzled frown, the head tilted slightly, as if trying to work out what the driver means",
         "LUOT": luot("Officer, my old is fifty!", "Ma'am, you mean you are fifty years old?", "Oh no! Yes, I am fifty years old.")}
    b["LUOT"][0]["to"] = "my old"
    for fn, v in (("BIEN-THE-2E3FA1BF-CANH-SAT-XE-TAI.json", a), ("BIEN-THE-2E3FA1BF-CANH-SAT-XE-TAI-HOOK.json", b)):
        p = os.path.join(HERE, "..", fn)
        json.dump([v], open(p, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
        print("Đã ghi", os.path.normpath(p), f"({len(v['LUOT'])} lượt)")


if __name__ == "__main__":
    main()
