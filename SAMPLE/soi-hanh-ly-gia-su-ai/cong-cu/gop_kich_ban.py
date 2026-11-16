"""Gộp kịch bản "địu con" + "không bé" thành MỘT kịch bản dùng token, và gộp 2 file biến thể thành một.
Mỗi cặp thay thế trong KHONG_BE (tao_kich_ban.py) thành token BE_nn: biến thể địu con nhận cụm gốc, biến thể không bé nhận cụm thay.
Chạy:  python gop_kich_ban.py <ma: x0076|x0077>"""
import ast, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.dirname(HERE)
ma = sys.argv[1]
CFG = {
    "x0076": ("KICH-BAN-SOI-HANH-LY-GIA-SU-AI", "BIEN-THE-SOI-HANH-LY-X0076-40", "KICH-BAN-SOI-HANH-LY-X0076.txt", "BIEN-THE-SOI-HANH-LY-X0076-40.json"),
    "x0077": ("KICH-BAN-SOI-HANH-LY-GIA-SU-AI-HINDI", "BIEN-THE-SOI-HANH-LY-X0077-HINDI-20", "KICH-BAN-SOI-HANH-LY-X0077-HINDI.txt", "BIEN-THE-SOI-HANH-LY-X0077-HINDI-20.json"),
}[ma]
src_kb, src_bt, out_kb, out_bt = CFG
dst = os.path.join(os.path.dirname(SAMPLE), "soi-hanh-ly-" + ma)

tree = ast.parse(open(os.path.join(HERE, "tao_kich_ban.py"), encoding="utf-8").read())
KB = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "KHONG_BE")
src = open(os.path.join(SAMPLE, src_kb + ".txt"), encoding="utf-8").read()
nobe = open(os.path.join(SAMPLE, src_kb + "-KHONG-BE.txt"), encoding="utf-8").read()
head_new = nobe.split("===== PHAN 1", 1)[0]
body = src.split("===== PHAN 1", 1)[1]

# bước 1: cụm có em bé -> token (cụm dài trước, đúng thứ tự KHONG_BE)
pairs = []
for a, b in KB:
    if a in body:
        n = len(pairs); tok = "CUM_BE_" + chr(65 + n // 26) + chr(65 + n % 26)
        body = body.replace(a, "{{" + tok + "}}")
        pairs.append((tok, a, b))
# bước 2: đại từ của hành khách -> token (giống bản không bé)
OBJ = re.compile(r"\s*(?:[,.:;)]|to\b|at\b|again\b|$)")
def her(m):
    t = "HIM_HOC" if OBJ.match(body, m.end()) else "HIS_HOC"
    return "{{" + t + ("_C" if m.group(0)[0] == "H" else "") + "}}"
body = re.sub(r"\bherself\b", "{{HIMSELF_HOC}}", body)
body = re.sub(r"\b[Hh]er\b", her, body)
body = re.sub(r"\bshe\b", "{{HE_HOC}}", body)
body = re.sub(r"\bShe\b", "{{HE_HOC_C}}", body)
text = head_new + "===== PHAN 1" + body
open(os.path.join(dst, out_kb), "w", encoding="utf-8").write(text)

PR = {"HE_HOC": "she", "HE_HOC_C": "She", "HIS_HOC": "her", "HIM_HOC": "her", "HIMSELF_HOC": "herself"}
def fill(s, v):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: v.get(m.group(1), m.group(0)), s)

out = []
for f, be in ((src_bt + "-DIU-CON.json", True), (src_bt + "-KHONG-BE.json", False)):
    for v in json.load(open(os.path.join(dst, f), encoding="utf-8")):
        if be:
            for t, a, b in pairs:
                v[t] = fill(a, v)
            v.update(PR)
        else:
            for t, a, b in pairs:
                v[t] = fill(b, v)
        if "{{DAO_TUI}}" not in body:
            v.pop("DAO_TUI", None)
        v.pop("DAO_BE", None)
        out.append(v)
out.sort(key=lambda v: int(re.search(r"\d+", v["name"]).group()))
json.dump(out, open(os.path.join(dst, out_bt), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(ma, "token CUM_BE:", len(pairs), "biến thể:", len(out))
