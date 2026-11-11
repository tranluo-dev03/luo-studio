"""Sinh SAMPLE/canh-sat-gia-su-ai/BIEN-THE-20-NEN.json: 20 biến thể dùng lại 20 tài xế của BIEN-THE-20-TAI-XE.json, xáo thứ tự,
đổi nền (5 bối cảnh, mỗi bối cảnh 4 biến thể) và màu xe (5 màu, xoay vòng), 11/11/2026.
    .venv\\Scripts\\python.exe -X utf8 SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\tao_bien_the_20_nen.py
Chạy SAU tao_bien_the_20.py (lấy nhân vật, cảnh sát, bé, lời thoại từ BIEN-THE-20-TAI-XE.json).
Giữ quy tắc cũ: tài xế nữ đi với nam cảnh sát, tài xế nam với nữ cảnh sát; bé giống bố/mẹ; tài xế Ấn Độ có câu Hindi ở cảnh 7.
Nền chủ yếu khớp thị trường của tài xế (Mỹ: phố ngoại ô / đường quê cánh đồng ngô; Mexico: phố thị trấn sặc sỡ / cánh đồng agave;
Ấn Độ: đường dừa và ruộng lúa), vài biến thể cố ý chéo để xáo trộn.
Token nền: xem boi_canh.py."""
import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boi_canh  # noqa: E402

DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(DIR, "BIEN-THE-20-TAI-XE.json")
OUT = os.path.join(DIR, "BIEN-THE-20-NEN.json")

NEN = {
    "pho-my": {   # Mỹ: phố ngoại ô
        "ANH_SANG": "bright warm late-afternoon sunlight",
        "NEN_DUONG": "a quiet tree-lined American suburban street on a sunny late afternoon: neat two-storey houses with porches, green lawns, "
                     "white picket fences, tall maple trees, a clear blue sky, no signs or lettering",
        "DUONG_SAU": "the quiet suburban street, green lawns, maple trees and the blue sky",
        "DUONG_TRONG": "the quiet suburban street",
        "NGOAI_XA": "the quiet suburban street with houses and maple trees",
        "AM_NEN": "quiet suburban street ambience, distant birdsong",
    },
    "duong-ngo": {   # Mỹ: đường quê giữa cánh đồng ngô
        "ANH_SANG": "warm golden-hour light",
        "NEN_DUONG": "an empty two-lane country road through tall green cornfields at golden hour: a red wooden barn and a white farmhouse in "
                     "the distance, a tall metal farm windmill, a soft orange-and-blue sky",
        "DUONG_SAU": "the empty country road, tall green cornfields and the sky",
        "DUONG_TRONG": "the empty country road",
        "NGOAI_XA": "the green cornfields",
        "AM_NEN": "countryside ambience, rustling corn leaves and crickets",
    },
    "pho-mexico": {   # Mexico: phố thị trấn nhỏ nhiều màu
        "ANH_SANG": "bright warm afternoon sunlight",
        "NEN_DUONG": "a sunny cobblestone street in a colourful small Mexican town: pastel pink, yellow and turquoise one-storey houses with "
                     "wrought-iron windows, pink bougainvillea over the walls, a white church bell tower in the distance, a clear blue sky, no signs or lettering",
        "DUONG_SAU": "the colourful cobblestone street, pastel houses, bougainvillea and the blue sky",
        "DUONG_TRONG": "the colourful cobblestone street",
        "NGOAI_XA": "the colourful pastel houses of the town",
        "AM_NEN": "small-town street ambience, distant church bells",
    },
    "agave": {   # Mexico: đường qua cánh đồng agave xanh (Jalisco)
        "ANH_SANG": "warm orange sunset light",
        "NEN_DUONG": "an empty two-lane road through endless rows of blue agave fields at sunset: rolling hills and blue mountains on the "
                     "horizon, a few tall cacti, an orange-and-pink sky",
        "DUONG_SAU": "the empty road, blue agave fields, mountains and the sunset sky",
        "DUONG_TRONG": "the empty road through the agave fields",
        "NGOAI_XA": "the blue agave fields and mountains",
        "AM_NEN": "open countryside ambience, soft wind",
    },
    "duong-dua": {   # Ấn Độ: đường hai hàng dừa, ruộng lúa (kiểu Kerala)
        "ANH_SANG": "soft warm morning sunlight",
        "NEN_DUONG": "a quiet two-lane road through a lush green landscape on a sunny morning: tall coconut palms and banana trees along the "
                     "roadside, bright green rice paddies, misty green hills in the distance, a pale blue sky, no signs or lettering",
        "DUONG_SAU": "the quiet road, coconut palms, green rice paddies and the sky",
        "DUONG_TRONG": "the quiet palm-lined road",
        "NGOAI_XA": "the green rice paddies and coconut palms",
        "AM_NEN": "tropical countryside ambience, birdsong",
    },
}

XE = [   # (MAU_XE, GHE_XE): XE ghép từ hai giá trị này để khớp các câu tả cửa, ghế trong kịch bản
    ("pearl-white", "beige leather"),
    ("deep-blue", "light-grey fabric"),
    ("silver", "black leather"),
    ("emerald-green", "tan leather"),
    ("sunset-orange", "black leather"),
]

# (tài xế, nền) theo thứ tự biến thể mới; mỗi nền 4 lần, mỗi tài xế 1 lần
THU_TU = [
    ("01", "agave"), ("09", "pho-my"), ("05", "duong-dua"), ("13", "pho-mexico"), ("17", "duong-ngo"),
    ("18", "pho-my"), ("14", "duong-dua"), ("02", "pho-mexico"), ("08", "duong-ngo"), ("12", "agave"),
    ("16", "duong-dua"), ("11", "pho-mexico"), ("06", "duong-ngo"), ("19", "agave"), ("03", "pho-my"),
    ("10", "pho-mexico"), ("20", "duong-ngo"), ("04", "agave"), ("15", "pho-my"), ("07", "duong-dua"),
]


def main():
    src = {re.match(r"tai-xe-(\d+)", v["name"]).group(1): v for v in json.load(open(SRC, encoding="utf-8"))}
    assert len(THU_TU) == 20 and sorted(m for m, _ in THU_TU) == sorted(src), "mỗi tài xế đúng một lần"
    out = []
    for i, (m, nen) in enumerate(THU_TU, 1):
        v = copy.deepcopy(src[m])
        mau, ghe = XE[(i - 1) % len(XE)]
        n = NEN[nen]
        v.update(n)
        v["MAU_XE"], v["GHE_XE"] = mau, ghe
        v["XE"] = f"a glossy {mau} four-door sedan with {ghe} seats"
        v["NEN_HOC"] = f"the inside of the {mau} car in {n['ANH_SANG']}, {ghe} seats and {n['NGOAI_XA']} through the rear windows"
        v["name"] = f"nen-{i:02d}-{nen}-" + v["name"]
        thieu = [k for k in boi_canh.MAC_DINH if k not in v]
        assert not thieu, (v["name"], thieu)
        sot = [k for k in ("XE", "NEN_DUONG", "NEN_HOC", *boi_canh.MAC_DINH) if re.search(r"\b(desert|red leather|bright-red)\b", v[k])]
        assert not sot, (v["name"], sot)   # không còn sót nền sa mạc / xe đỏ của bản gốc
        out.append(v)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for v in out:
        print(v["name"], "|", v["MAU_XE"], "|", v["TEN_HOC"], "| CS:", v["CS_ANH"], "| bé:", v["refs"]["NGUOI_BE"][0].rsplit("/", 1)[1])


if __name__ == "__main__":
    main()
