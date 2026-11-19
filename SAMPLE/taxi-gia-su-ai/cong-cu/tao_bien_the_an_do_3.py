"""Sinh BIEN-THE-TAXI-AN-DO-3.json: 3 biến thể Ấn Độ (tiếng Anh + Hindi) từ video "0510_cartoon turn car_015_1" (17/11/2026, chạy ngầm từ Studio).
  runtime\python.exe SAMPLE\taxi-gia-su-ai\cong-cu\tao_bien_the_an_do_3.py
Khớp KICH-BAN-TAXI-AN-DO.txt (cùng khoá, 20+9+2 lượt). Lời và nhân vật chung (sếp, Priya, Arjun, robot Ava) lấy từ tao_bien_the_an_do.py;
chỉ đổi tài xế (HOC) + khách nữ (KHACH). Ảnh HOC/KHACH gen bằng Muse vào anh/an-do-3/ (HOC1, KHACH1 ...); chưa có ảnh thì biến thể không có refs HOC/KHACH.
Gen ảnh:  runtime\python.exe SAMPLE\_chung\gen-anh-nhan-vat.py --ra SAMPLE\taxi-gia-su-ai\anh\an-do-3 --nv HOC1 "<mô tả>" ... (mô tả = ROWS bên dưới, bỏ "a stylized 3D-animated")."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tao_bien_the_an_do import ANH_CHUNG, CHUNG, KH_GIA, KH_TRE, MARKER, ROOT, TRE, TRUNG, luot

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "BIEN-THE-TAXI-AN-DO-3.json")
ANH = "SAMPLE/taxi-gia-su-ai/anh/an-do-3"

ROWS = [
    ("Ravi", "a stylized 3D-animated young Indian taxi driver of 26, short neat black hair, clean-shaven, warm brown skin, a friendly face, a clean sky-blue polo shirt, khaki trousers", TRE,
     "a stylized 3D-animated elegant wealthy young Indian woman of 30, long straight black hair, a teal silk saree with a gold border, gold earrings, a haughty expression", KH_TRE),
    ("Gopal", "a stylized 3D-animated middle-aged Indian taxi driver of 51, salt-and-pepper hair, a thick grey-black moustache, warm brown skin, a clean beige shirt, brown trousers", TRUNG,
     "a stylized 3D-animated wealthy middle-aged Indian woman of 54, her hair in a neat bun, a maroon silk saree, a pearl necklace, a stern expression", KH_GIA),
    ("Sandeep", "a stylized 3D-animated Indian taxi driver of 36, black wavy hair, round glasses, a short trimmed beard, warm brown skin, a clean white kurta, black trousers", TRUNG,
     "a stylized 3D-animated stylish Indian businesswoman of 40, shoulder-length black hair, a navy-blue blazer and trousers, a laptop bag on her shoulder, an impatient expression", KH_TRE),
]


def main():
    out = []
    for i, (ten, hoc, giong, khach, giong_kh) in enumerate(ROWS, 1):
        v = {"name": f"taxi-in-3-{i:02d}-{ten.lower()}"}
        v.update(CHUNG)
        v.update({"TEN_HOC": ten, "NGUOI_HOC": hoc, "GIONG_HOC": giong, "NGUOI_KHACH": khach, "GIONG_KHACH": giong_kh, "TEN_ARJUN": "Arjun"})
        v["LUOT"] = []
        for phan, who, text, emo, dich, extra in luot("Arjun"):
            t = {"who": who, "text": MARKER if text is None else text, "emo": emo, "fx": "none", "phan": phan}
            if text is not None:
                t.update(extra)
                if dich:
                    t["dich"] = dich
            v["LUOT"].append(t)
        refs = {}
        for k, key in (("HOC", f"HOC{i}"), ("KHACH", f"KHACH{i}")):
            p = f"{ANH}/{key}.png"
            if os.path.exists(os.path.join(ROOT, p)):
                refs[f"NGUOI_{k}"] = [p]
        refs.update({f"NGUOI_{k}": [p] for k, p in ANH_CHUNG.items() if os.path.exists(os.path.join(ROOT, p))})
        v["refs"] = refs
        out.append(v)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Đã ghi {os.path.normpath(OUT)}: {len(out)} biến thể; refs HOC/KHACH: {[sum(k in v['refs'] for k in ('NGUOI_HOC', 'NGUOI_KHACH')) for v in out]}")


if __name__ == "__main__":
    main()
