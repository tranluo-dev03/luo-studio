"""Sinh BIEN-THE-BB327BAC-REF-NOI-CHUYEN.json (kịch bản A, giữ hook) và ...-HOOK.json (kịch bản B, đổi hook).
Sửa lời / nhân vật / ảnh ở bảng dưới rồi chạy: python tao_bien_the.py  (không sửa tay JSON)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
APP = "LangLearn"

NHAN_VAT = {
    "TEN_DAY": "the AI tutor",
    "NGUOI_DAY": "a sleek humanoid AI robot with a glossy white armoured head and shoulders, a smooth white face, softly glowing pale-blue eyes, a slim neck of black cables and white shoulder plates with thin blue light lines, calm friendly expression",
    "GIONG_DAY": "a calm, clear, warm male-leaning synthetic-but-natural voice, a baritone around 130-150 Hz, American English, patient and encouraging",
    "NEN_DAY": "a plain pure black background",
    "TEN_HOC": "the housekeeper",
    "NGUOI_HOC": "a stylized 3D-animated Mexican woman in her early fifties, warm brown skin, kind tired brown eyes, dark hair pulled back in a neat bun with a dark-blue patterned headband, a navy-blue short-sleeved housekeeping uniform shirt with a small collar and a white half-apron",
    "GIONG_HOC": "a warm, friendly Mexican woman's voice, around 195-215 Hz, speaking English with a light Mexican accent, a little hesitant and halting at first, brighter and more confident later",
    "NEN_HOC": "a bright cream-coloured kitchen with wooden cabinets and a granite counter, a sink in front of her",
    "POS_DAY": "TOP",
    "POS_HOC": "BOTTOM",
    "refs": {
        "NGUOI_DAY": ["SAMPLE/bb327bac-ref-noi-chuyen/anh/DAY.png"],
        "NGUOI_HOC": ["SAMPLE/bb327bac-ref-noi-chuyen/anh/HOC.png"],
    },
}

L = lambda who, text, emo, **k: dict({"who": who, "text": text, "emo": emo, "fx": "none"}, **k)

# TÌNH HUỐNG (lượt 4-13), dùng chung cho cả hai kịch bản
TINH_HUONG = [
    L("hoc", "I always mix that up.", "embarrassed"),
    L("day", "That's what I'm here for, to help you speak well.", "warm"),
    L("hoc", "But I don't have money.", "worried"),
    L("day", f"What? You don't need money. {APP} lets you practice English for free, unlike expensive apps and courses.", "reassuring"),
    L("hoc", "Seriously?", "surprised"),
    L("day", "Of course, no tricks. Only real conversation practice with your AI tutor.", "friendly"),
    L("hoc", "Like a real tutor?", "curious"),
    L("day", "Yes. I correct your grammar and pronunciation, and I help you speak with confidence.", "encouraging"),
    L("hoc", f"Okay, so I'm going to download {APP} right now.", "confident"),
    L("day", "Good decision. Let's speak English together.", "upbeat"),
]

HOOK_GOC = [
    L("day", "Where are you from?", "curious"),
    L("hoc", "I am Mexico.", "cheerful", fx="wrong", c="red", icon="x"),
    L("day", "Almost. Better say: I am from Mexico.", "warm", fx="right", c="green", icon="check", to="I am from Mexico"),
]
HOOK_MOI = [
    L("day", "Where do you live?", "curious"),
    L("hoc", "I am live in Mexico.", "cheerful", fx="wrong", c="red", icon="x"),
    L("day", "Almost. Better say: I live in Mexico.", "warm", fx="right", c="green", icon="check", to="I live in Mexico"),
]


def ghi(ten, file, hook, them=None):
    v = dict({"name": ten}, **{k: x for k, x in NHAN_VAT.items() if k != "refs"})
    v.update(them or {})
    v["LUOT"] = hook + TINH_HUONG
    v["refs"] = NHAN_VAT["refs"]
    with open(os.path.join(OUT, file), "w", encoding="utf-8") as f:
        json.dump([v], f, ensure_ascii=False, indent=2)
    print("OK", file, len(v["LUOT"]), "luot")


ghi("bb327bac-goc-01", "BIEN-THE-BB327BAC-REF-NOI-CHUYEN.json", HOOK_GOC)
ghi("bb327bac-hook-01", "BIEN-THE-BB327BAC-REF-NOI-CHUYEN-HOOK.json", HOOK_MOI,
    {"HOOK_TV": "she says her first line brightly and over-confidently, chin slightly up, sure it is perfect, then her smile softens when the tutor answers"})
