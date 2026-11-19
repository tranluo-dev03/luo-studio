"""Nhóm tx4wnb (kịch bản A, goc): 5 biến thể đổi cặp tài xế + cảnh sát (luôn khác giới), loại xe, bối cảnh/giờ; tuổi trong lời thoại theo tuổi tài xế.
    runtime\\python.exe SAMPLE\\2e3fa1bf-canh-sat-xe-tai\\cong-cu\\tao_bien_the_nhom_tx4wnb.py [--gen]   (--gen: gen ảnh refs còn thiếu, nền xanh, ảnh thật)
Ghi BIEN-THE-NHOM-tx4wnb.json cùng bộ token với BIEN-THE-2E3FA1BF-CANH-SAT-XE-TAI.json."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import tao_bien_the as MAU  # noqa: E402

ANH = "SAMPLE/2e3fa1bf-canh-sat-xe-tai/anh/nhom-tx4wnb/"
# (tên, tuổi bằng chữ, khoá ảnh tài xế, tả tài xế, giọng tài xế, khoá ảnh cảnh sát, tả cảnh sát, giọng cảnh sát, đại từ cảnh sát, xe, đường, ánh sáng)
CAST = [
    ("tx-nam-ban-tai-do", "forty-five", "TX_A",
     "a Mexican-American man in his mid forties, a broad face with a short dark beard, warm dark-brown eyes, short black hair with a little gray at the temples; a faded blue denim work shirt with rolled sleeves over a gray T-shirt, a plain brown baseball cap",
     "a deep, warm, slightly gravelly American man's voice in his mid forties, around 100–125 Hz, light Texan drawl, loud and cheerful when proud, slower and embarrassed after a mistake; a real person, not an actor",
     "CS_A",
     "a white American woman in her early thirties, light-brown hair in a tight bun, green eyes, light freckles, no sunglasses, a navy short-sleeved state-trooper uniform shirt with plain shoulder patches and a silver star badge, a plain fluorescent yellow-green safety vest without lettering, a black duty belt with holster and radio",
     "a clear, calm, friendly American woman's voice in her early thirties, around 190–220 Hz, warming up when she smiles", "her",
     "a glossy cherry-red American full-size pickup truck, tall cab, chrome grille and bumper, a big side mirror on a metal arm",
     "the shoulder of a straight two-lane desert highway at sunset: red rock mesas, dry desert brush, wooden power poles, a far-away car standing still, a glowing orange-and-violet sky",
     "at sunset, warm orange-violet light"),
    ("tx-nu-xe-giao-hang-dem", "twenty-five", "TX_B",
     "a Black American woman in her mid twenties, an oval face, bright dark eyes, short natural curly black hair, a gold stud earring; a bright orange hooded sweatshirt without any logo or lettering over a gray T-shirt",
     "a bright, quick, youthful American woman's voice in her mid twenties, around 210–240 Hz, lively and cheerful, shy and slower after a mistake; a real person, not an actress",
     "CS_B",
     "a white American man in his early forties, a square jaw, short graying brown hair, a neat mustache, tired kind eyes, no sunglasses, a dark-gray long-sleeved police uniform shirt with plain shoulder patches and a silver badge, a plain fluorescent yellow-green safety vest without lettering, a black duty belt with holster and radio",
     "a tired but kind American man's baritone in his early forties, around 105–130 Hz, calm and polite, warming up when he smiles", "him",
     "a white mid-size delivery van with a high roof and a sliding side door, a big side mirror on a metal arm, no markings or lettering",
     "a quiet city street at night: wet asphalt reflecting orange street lamps, closed shop fronts without readable signs, a far-away traffic light glowing, a deep blue night sky",
     "at night, warm orange street-lamp light with deep blue shadows"),
    ("tx-nam-xe-buyt-sang", "sixty", "TX_C",
     "an Indian-American man in his early sixties, a lined friendly face, thick gray mustache, kind brown eyes behind thin metal-rimmed glasses, short gray hair; a light-blue short-sleeved bus-driver shirt without lettering",
     "a gentle, slightly raspy American man's voice in his early sixties with a light Indian accent, around 110–135 Hz, cheerful and proud, slower and embarrassed after a mistake; a real person, not an actor",
     "CS_C",
     "a Black American woman in her mid forties, a calm oval face, black hair in a neat low bun, warm brown eyes, no sunglasses, a tan short-sleeved sheriff uniform shirt with plain shoulder patches and a gold star badge, a plain fluorescent yellow-green safety vest without lettering, a black duty belt with holster and radio",
     "a firm, warm American woman's voice in her mid forties, around 170–200 Hz, steady and polite, warming up when she smiles", "her",
     "a big white-and-yellow city bus with a tall front window and an open driver's side window, a large side mirror on a metal arm, no markings, route numbers or lettering",
     "a wide suburban avenue on a clear early morning: low golden sun, long soft shadows, green trees along the sidewalk, far-away parked cars standing still, a pale blue sky",
     "in the early morning, low soft golden sunlight"),
    ("tx-nu-xe-container-mua", "thirty-five", "TX_D",
     "a Vietnamese-American woman in her mid thirties, a round face, dark almond eyes, black hair in a high ponytail, light freckles; a yellow rain jacket with the hood down over a gray work shirt, no logos",
     "a calm, slightly low American woman's voice in her mid thirties, around 180–205 Hz, friendly and confident, slower and embarrassed after a mistake; a real person, not an actress",
     "CS_D",
     "a Black American man in his early fifties, a shaved head, a short gray-flecked beard, deep brown eyes, no sunglasses, a black short-sleeved police uniform shirt with plain shoulder patches and a silver badge, a plain fluorescent yellow-green safety vest without lettering, a black duty belt with holster and radio",
     "a deep, calm American man's voice in his early fifties, around 90–115 Hz, warm and steady, polite", "him",
     "a big forest-green long-haul semi-truck cab with chrome steps and tanks, a tall chrome side mirror on a metal arm, no markings",
     "the shoulder of a wet two-lane highway through a pine forest under an overcast sky after light rain: tall dark pine trees on both sides, shiny asphalt, a far-away car standing still, soft gray light",
     "under an overcast sky after light rain, soft gray diffuse light"),
    ("tx-nam-xe-van-vang-trua", "thirty", "TX_E",
     "an East Asian man in his late twenties, a young clean-shaven face, dark brown eyes, messy black hair, a gold-yellow polo-style delivery shirt without any logo or lettering and a plain black cap worn backwards",
     "an energetic, bright American man's voice in his late twenties, around 125–150 Hz, fast and cheerful, shy and slower after a mistake; a real person, not an actor",
     "CS_E",
     "a Latina American woman in her late twenties, long black hair in a low ponytail, brown eyes, no sunglasses, a tan short-sleeved state-trooper uniform shirt with plain shoulder patches and a gold star badge, a plain fluorescent yellow-green safety vest without lettering, a black duty belt with holster and radio",
     "a clear, upbeat American woman's voice in her late twenties, around 200–230 Hz, friendly and polite, warming up when she smiles", "her",
     "a big bright yellow delivery box van with a tall cab and a big side mirror on a metal arm, no markings, logos or lettering",
     "a sunny city boulevard at midday: clean white lane markings, palm trees, low modern buildings without readable signs, far-away cars standing still, a clear blue sky",
     "at midday under a clear sky, bright natural sunlight"),
]


def main():
    if "--gen" in sys.argv:
        args = []
        for c in CAST:
            for key, desc in ((c[2], c[3]), (c[5], c[6])):
                if not os.path.exists(os.path.join(ROOT, ANH, key + ".png")):
                    args += ["--nv", key, desc]
        if args:
            subprocess.run([os.path.join(ROOT, "runtime", "python.exe"), os.path.join(HERE, "gen-anh-nhan-vat-that.py"), "--ra", os.path.join(ROOT, ANH)] + args, check=False)
    out = []
    for (name, tuoi, kt, nt, gt, kc, nc, gc, him, xe, duong, sang) in CAST:
        v = {"name": name, **MAU.CHUNG}
        v.update({"NGUOI_HOC": nt, "GIONG_HOC": gt, "NGUOI_CANHSAT": nc, "GIONG_CANHSAT": gc, "HIM_CANHSAT": him, "XE": xe, "NEN_DUONG": duong, "SANG": sang})
        v["refs"] = {"NGUOI_HOC": [ANH + kt + ".png"], "NGUOI_CANHSAT": [ANH + kc + ".png"]}
        nam = name.startswith("tx-nam")
        goi = "Sir" if nam else "Ma'am"
        l = MAU.luot(f"Officer, I have {tuoi} years!", f"{goi}, you mean you are {tuoi} years old?", f"Oh no! Yes, I am {tuoi} years old.")
        l[0]["to"] = f"have {tuoi} years"
        l[2]["to"] = f"I am {tuoi} years old"
        v["LUOT"] = l
        out.append(v)
    p = os.path.join(HERE, "..", "BIEN-THE-NHOM-tx4wnb.json")
    json.dump(out, open(p, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("Đã ghi", os.path.normpath(p), len(out), "biến thể")


if __name__ == "__main__":
    main()
