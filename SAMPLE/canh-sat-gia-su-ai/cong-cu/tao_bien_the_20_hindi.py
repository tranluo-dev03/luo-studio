"""Sinh SAMPLE/canh-sat-gia-su-ai/BIEN-THE-20-AN-DO-HINDI.json: 20 biến thể gia đình Ấn Độ, lời thoại tiếng Hindi (chữ Devanagari, xen English), 12/11/2026.
    .venv\\Scripts\\python.exe -X utf8 SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\tai_anh_20_hindi.py       (tải ảnh, chỉ chạy một lần)
    .venv\\Scripts\\python.exe -X utf8 SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\tao_bien_the_20_hindi.py
Nguồn: CSV "20 biến thể IN dừng xe quá tốc độ" (anh/20-an-do-hindi/bang-goc.csv) + ảnh tải về anh/20-an-do-hindi/ (tai-xe-XX, canh-sat-nu-N / canh-sat-nam-N, be-trai).
Ảnh đính kèm bằng đường dẫn tương đối từ thư mục gốc kho mã ("refs": {"NGUOI_HOC": ["SAMPLE/canh-sat-gia-su-ai/anh/20-an-do-hindi/tai-xe-01.png"]}):
Studio tự chép vào dự án khi nhập biến thể, nên máy khác chỉ cần có kho mã, không cần link Drive.
Quy tắc (theo CSV): 10 tài xế nam (1-5, 11-15) đi với nữ cảnh sát, 10 tài xế nữ (6-10, 16-20) đi với nam cảnh sát; bé trai Ấn Độ ngồi cạnh, cùng một ảnh cho cả 20.
Cảnh sát đồng phục kaki Ấn Độ có mũ (MAU_DONGPHUC = khaki). Nền: đường dừa/ruộng lúa (duong-dua) cho cả 20 (cảnh sát kaki không hợp sa mạc kiểu Mỹ), màu xe xoay vòng 5 màu.
Lời thoại: 25 lượt như BIEN-THE-CANH-SAT-GIA-SU-AI.json, thay chữ bằng lời CSV. Chỗ CSV chỉ có chữ La-tinh (Hinglish) thì viết lại bằng Devanagari.
Tài xế nữ: động từ Hindi đổi giống cái (रही थीं, पाती, करूँगी, गई हैं), English "he/his" -> "she/her".
Tên app: CSV ghi "Ava AI" nhưng cả dự án và end card là "Aiva AI" -> giữ "Aiva AI" (nghe giống nhau).
Cũng thêm các token mới (giới tính đứa trẻ, đồng phục: boi_canh.MAC_DINH) vào 3 file biến thể cũ để chúng vẫn ra y như trước."""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boi_canh  # noqa: E402
import tai_anh_20_hindi as T  # noqa: E402
import tao_bien_the_20_nen as N  # noqa: E402   dùng lại nền duong-dua và bảng màu xe

DIR = T.DIR
REL = "SAMPLE/canh-sat-gia-su-ai/anh/20-an-do-hindi"
GOC = os.path.join(DIR, "BIEN-THE-CANH-SAT-GIA-SU-AI.json")
OUT = os.path.join(DIR, "BIEN-THE-20-AN-DO-HINDI.json")
CU = ["BIEN-THE-CANH-SAT-GIA-SU-AI.json", "BIEN-THE-20-TAI-XE.json", "BIEN-THE-20-NEN.json"]

NAM = {"CHA": "father", "CHA_ANH": "he", "CHA_CUA": "his", "CHA_O": "him", "CHA_VN": "bố"}
NU = {"CHA": "mother", "CHA_ANH": "she", "CHA_CUA": "her", "CHA_O": "her", "CHA_VN": "mẹ"}
CS_NU = {"CS_ANH": "she", "CS_CUA": "her", "CS_O": "her"}
CS_NAM = {"CS_ANH": "he", "CS_CUA": "his", "CS_O": "him"}
BE_TRAI = {"BE_LOAI": "boy", "BE_ANH": "he", "BE_CUA": "his", "BE_O": "him", "BE_CON": "son", "BE_VN": "trai", "GHE_BE": "blue"}
TAI_XE_TAIL = ", the seat belt across the chest"

# (tuổi, mô tả tài xế tiếng Anh, nét nhận diện ngắn cho góc A)
TX = {
    1: ("Indian man about 27, brown skin, long black hair tied in a low ponytail, a short full beard, a clean blue button-up shirt",
        "low black ponytail, short full beard"),
    2: ("Indian man about 30, brown skin, neat gelled-back black hair, a thick moustache, a clean white polo shirt",
        "gelled-back black hair, thick moustache"),
    3: ("Indian man about 26, brown skin, short curly black hair, light stubble, a clean beige crew-neck T-shirt",
        "short curly black hair, light stubble"),
    4: ("Indian man about 29, brown skin, short neat black hair, a thin moustache, a clean blue-and-white striped shirt",
        "short black hair, thin moustache"),
    5: ("Indian man about 24, brown skin, short messy black hair, clean-shaven, a light grey jacket over a white T-shirt",
        "messy short black hair, clean-shaven, grey jacket"),
    6: ("Indian woman about 22, brown skin, long black hair worn loose over the shoulders, a clean blue kurta",
        "long loose black hair, blue kurta"),
    7: ("Indian woman about 24, brown skin, shoulder-length black hair, a blue sari with a light pattern and a matching short-sleeved blouse",
        "shoulder-length black hair, blue sari"),
    8: ("Indian woman about 26, brown skin, black hair in a neat high bun, a pale-yellow salwar kameez with a matching dupatta",
        "high black bun, pale-yellow dupatta"),
    9: ("Indian woman about 48, brown skin, black hair with grey strands in a low bun at the nape, a clean blue kurta",
        "grey-streaked low bun, blue kurta"),
    10: ("Indian woman about 28, brown skin, long black hair curled at the ends, a light-purple kurta",
         "long curled black hair, lilac kurta"),
    11: ("Indian man about 48, brown skin, half-grey hair combed neatly, a short grey beard, a clean white shirt",
         "half-grey combed hair, short grey beard"),
    12: ("Indian man about 52, dark-brown weathered skin with light wrinkles, black hair flecked with grey, a grey moustache, a blue-and-brown checked shirt",
         "grey-flecked black hair, grey moustache"),
    13: ("Indian man about 46, brown skin, thinning black hair combed neatly, a black moustache, a clean blue shirt",
         "thinning combed black hair, black moustache"),
    14: ("Indian man about 55, brown skin, short grey hair, a short grey beard, simple glasses, a brown sweater over a white shirt",
         "short grey hair and beard, glasses, brown sweater"),
    15: ("Indian man about 50, brown skin, black hair receding at the temples, a short black beard, a grey T-shirt under a light jacket",
         "receding black hair, short black beard, light jacket"),
    16: ("Indian woman about 45, brown skin, black hair in a low bun at the nape, a beige long-sleeved cotton kurta",
         "low black bun, beige kurta"),
    17: ("Indian woman about 50, brown skin, black hair with grey strands in a neat bun, simple glasses, a light-pink sari with a faint pattern",
         "grey-streaked bun, glasses, light-pink sari"),
    18: ("Indian woman about 48, brown skin, short softly wavy black hair, a green salwar kameez with a matching dupatta",
         "short wavy black hair, green dupatta"),
    19: ("Indian woman about 54, brown skin, grey hair in a neat high bun, a light-orange kurta",
         "grey high bun, light-orange kurta"),
    20: ("Indian woman about 42, brown skin, long black hair tied low, big eyes, a blue churidar set with a long matching top and a thin shawl",
         "long low-tied black hair, blue churidar"),
}

# cảnh sát (giới tính ngược tài xế): mô tả tiếng Anh theo CSV
KAKI = ("a clean pressed khaki Indian police uniform with a peaked police cap, a plain badge and shoulder patches without readable lettering, "
        "a black belt and black shoes")
CS = {
    1: "Indian policewoman about 28, brown skin, black hair in a neat bun at the nape, a serious but gentle face",
    2: "Indian policewoman about 32, brown skin, short shoulder-length black hair, a stern face and decisive eyes",
    3: "Indian policewoman about 26, brown skin, black hair in a neat braid down the back, a calm face",
    4: "Indian policewoman about 35, brown skin, black hair in a neat high bun, a calm serious face",
    5: "Indian policewoman about 29, brown skin, long black hair tied low, a serious face",
    6: "Indian policeman about 30, brown skin, short neat black hair, a short moustache, a serious but gentle face",
    7: "Indian policeman about 28, brown skin, neatly combed black hair, a stern face, standing straight",
    8: "Indian policeman about 34, brown skin, short black hair, a thick moustache, a calm face",
    9: "Indian policeman about 40, brown skin, black hair flecked with grey, a moustache, a serious face",
    10: "Indian policeman about 33, brown skin, short cropped black hair, a serious face",
    11: "Indian policewoman about 38, brown skin, black hair in a neat bun, a calm serious face",
    12: "Indian policewoman about 30, brown skin, long black hair tied low, a serious decisive face",
    13: "Indian policewoman about 27, brown skin, short neat black hair, a stern but polite face",
    14: "Indian policewoman about 36, brown skin, black hair in a high bun, a serious calm face",
    15: "Indian policewoman about 31, brown skin, curly black hair tied low, a serious face",
    16: "Indian policeman about 38, brown skin, short neat black hair, a moustache, a serious gentle face",
    17: "Indian policeman about 32, brown skin, neatly combed black hair, a stern face, standing straight",
    18: "Indian policeman about 29, brown skin, short black hair, a young but serious face",
    19: "Indian policeman about 45, brown skin, black hair flecked with grey, a thick moustache, a calm face",
    20: "Indian policeman about 36, brown skin, short cropped black hair, a short moustache, a serious face",
}

BE_NGUOI = ("a stylized 3D-animated Indian boy about four or five years old, brown skin, short neat black hair, chubby cheeks, very big dark-brown eyes, a calm slightly puzzled face, "
            "a clean white short-sleeved shirt, sitting in a child car seat with the seat belt on")
GIONG_BE = "a bright, sweet, confident little boy's voice, clear English with a light Indian accent, also fluent Hindi"
GIONG_DAY = ("a clear, warm, friendly young woman's voice with a very slightly synthetic digital sheen, speaking natural Hindi mixed with clear English, "
             "a light Indian accent, bright and upbeat")
NGHE_BE = "sits in his child seat looking at whoever is speaking with big curious eyes, mouth closed"

# lời thoại 25 lượt: (nam/chung, nữ). Cùng thứ tự người nói và "phan" với biến thể gốc.
LOI = [
    ("क्या आपको पता है आप स्पीडिंग कर रहे थे?", "क्या आपको पता है आप स्पीडिंग कर रही थीं?"),
    ("हाँ।", None),
    ("लाइसेंस और रजिस्ट्रेशन, प्लीज़।", None),
    ("उह... मैं... मैं... मैं... Officer, sorry.", None),
    ("ये नर्वस हो गए हैं। और इनकी English भी ज़्यादा अच्छी नहीं है।", "ये नर्वस हो गई हैं। और इनकी English भी ज़्यादा अच्छी नहीं है।"),
    ("Does he have his license and registration?", "Does she have her license and registration?"),
    ("अपना लाइसेंस और गाड़ी के पेपर्स दिखाओ।", None),
    ("All right. Slow down next time.", None),
    ("काश मैं भी तुम्हारी तरह English बोल पाता।", "काश मैं भी तुम्हारी तरह English बोल पाती।"),
    ("सिर्फ़ तीन हफ़्तों में Aiva AI के साथ। हर रोज़ असली बातचीत।", None),
    ("सच में?", None),
    ("हाँ। चलो दिखाता हूँ।", None),
    ("Where are you going?", None),
    ("I go to home.", None),
    ("You mean, I'm going home? Yes,", None),
    ("I'm going home.", None),
    ("I am very hurry.", None),
    ("“I’m in a hurry” कहना सही तरीका है।", None),
    ("ओह, ठीक है। Thank you. रुको, तुम कौन हो?", None),
    ("मैं एक AI tutor हूँ, यहाँ तुम्हारी English practice में मदद करने के लिए, ताकि तुम बेहतर बोल सको।", None),
    ("But I don't have monies.", None),
    ("It's “I have no money.” लेकिन परेशान मत हो, Aiva AI एक completely free app है।", None),
    ("सचमुच?", None),
    ("हम कभी भी, कहीं भी English practice कर सकते हैं। बस Aiva AI download करो।", None),
    ("मैं अभी download करूँगा। बहुत-बहुत thank you.", "मैं अभी download करूँगी। बहुत-बहुत thank you."),
]
KIEU = {"Nam trẻ": "nam-tre", "Nữ trẻ": "nu-tre", "Nam trung niên": "nam-trung-nien", "Nữ trung niên": "nu-trung-nien"}


def nhin(ai):
    return f"keeps the eyes on the person {ai} is talking to, in the direction the clip's EYE LINE gives, never into the lens"


def bo_sung_khoa_cu():
    """Thêm token mới (giá trị cũ) vào 3 file biến thể đã có: bé gái, ghế hồng, đồng phục navy."""
    moi = {k: v for k, v in boi_canh.MAC_DINH.items() if k in ("BE_LOAI", "BE_ANH", "BE_CUA", "BE_O", "BE_CON", "BE_VN", "GHE_BE", "MAU_DONGPHUC")}
    for fn in CU:
        p = os.path.join(DIR, fn)
        d = json.load(open(p, encoding="utf-8"))
        dem = 0
        for v in d:
            for k, g in moi.items():
                if k not in v:
                    v[k] = g
                    dem += 1
        if dem:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{fn}: thêm {dem} khoá")


def main():
    bo_sung_khoa_cu()
    goc = json.load(open(GOC, encoding="utf-8"))[0]
    rows = T.doc_bang(T.CSV_GOC)
    mp = json.load(open(T.MAP, encoding="utf-8"))
    assert len(LOI) == len(goc["LUOT"]) == 25
    nen = N.NEN["duong-dua"]
    out = []
    for r in rows:
        i = r["stt"]
        m = f"{i:02d}"
        nu = r["kieu"].startswith("Nữ")
        assert r["cs"].startswith("Nam" if nu else "Nữ"), (i, r["cs"])   # cảnh sát giới tính ngược lại
        v = copy.deepcopy(goc)
        v["name"] = f"hindi-{m}-{KIEU[r['kieu']]}"
        v.update(NU if nu else NAM)
        v.update(CS_NAM if nu else CS_NU)
        v.update(BE_TRAI)
        # tài xế
        mo_ta, net = TX[i]
        v["TEN_HOC"] = "the mother" if nu else "the father"
        v["NGUOI_HOC"] = "a stylized 3D-animated " + mo_ta + TAI_XE_TAIL
        v["GIONG_HOC"] = ("a warm woman's voice" if nu else "a warm man's voice") + " with a clear Indian accent, speaking Hindi and hesitant, nervous English"
        v["NET_HOC"] = net
        v["NHIN_HOC"] = nhin("she" if nu else "he")
        # cảnh sát
        v["NGUOI_CANHSAT"] = "a stylized 3D-animated " + CS[i] + ", " + KAKI
        v["GIONG_CANHSAT"] = ("a calm, clear, firm man's voice" if nu else "a calm, clear, firm woman's voice") + " with a light Indian accent, speaking Hindi and English, polite and professional"
        v["NHIN_CANHSAT"] = nhin("he" if nu else "she")
        v["MAU_DONGPHUC"] = "khaki"
        # bé trai
        v["NGUOI_BE"], v["GIONG_BE"], v["NGHE_BE"], v["NHIN_BE"] = BE_NGUOI, GIONG_BE, NGHE_BE, nhin("he")
        v["VAI_BE"], v["TEN_BE"] = "son", "the little boy"
        v["TIENG_BE"] = "tiếng Hindi"
        v["GIONG_DAY"] = GIONG_DAY
        # nền + xe
        mau, ghe = N.XE[(i - 1) % len(N.XE)]
        v.update(nen)
        v["MAU_XE"], v["GHE_XE"] = mau, ghe
        v["XE"] = f"a glossy {mau} four-door sedan with {ghe} seats"
        v["NEN_HOC"] = f"the inside of the {mau} car in {nen['ANH_SANG']}, {ghe} seats and {nen['NGOAI_XA']} through the rear windows"
        # ảnh đính kèm (đường dẫn trong kho mã)
        cs_file = mp[T.drive_id(r["cs_anh"])]
        v["refs"] = {
            "NGUOI_CANHSAT": [f"{REL}/{cs_file}"],
            "NGUOI_HOC": [f"{REL}/tai-xe-{m}.png"],
            "NGUOI_BE": [f"{REL}/be-trai.png"],
            "NGUOI_DAY": goc["refs"]["NGUOI_DAY"],
        }
        for k, files in v["refs"].items():
            for f in files:
                assert os.path.isfile(os.path.join(DIR, "..", "..", f)), f
        # lời thoại
        for l, (a, b) in zip(v["LUOT"], LOI):
            l["text"] = b if (nu and b) else a
        out.append(v)
    assert len(out) == 20
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for v in out:
        print(v["name"], "|", v["TEN_HOC"], "| CS:", v["CS_ANH"], "|", v["refs"]["NGUOI_CANHSAT"][0].rsplit("/", 1)[1], "|", v["MAU_XE"])


if __name__ == "__main__":
    main()
