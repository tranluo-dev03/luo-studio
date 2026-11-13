"""Tham số hoá giới tính tài xế (HOC) và cảnh sát (CANHSAT) trong KICH-BAN-CANH-SAT-GIA-SU-AI.txt (10/11/2026, 20 biến thể tài xế nam/nữ).
Token biến thể điền:
  CHA (father/mother), CHA_ANH (he/she), CHA_CUA (his/her), CHA_O (him/her), CHA_VN (bố/mẹ), NET_HOC (nét nhận diện ngắn của tài xế)
  CS_ANH (she/he), CS_CUA (her/his), CS_O (her/him)  - cảnh sát
  TIENG_BE (tiếng Tây Ban Nha / tiếng Hindi)        - câu bé dịch cho bố/mẹ ở cảnh 7
  BE_LOAI (girl/boy), BE_ANH (she/he), BE_CUA (her/his), BE_O (her/him), BE_CON (daughter/son), BE_VN (gái/trai),
  GHE_BE (pink/blue: màu ghế trẻ em), MAU_DONGPHUC (navy/khaki: đồng phục cảnh sát)   - giới tính đứa trẻ + màu đồng phục (12/11/2026, bộ 20 biến thể Ấn Độ có bé trai, cảnh sát kaki)
  .venv\\Scripts\\python.exe SAMPLE\\canh-sat-gia-su-ai\\cong-cu\\gioi_tinh.py        (áp vào kịch bản; chạy lại không đổi gì)
goc_may.py gọi bo_tham_so() trước khi sửa và tham_so() trước khi ghi, nên vẫn chạy được như cũ."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boi_canh  # noqa: E402   token bối cảnh (nền, ánh sáng, màu xe)

S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "KICH-BAN-CANH-SAT-GIA-SU-AI.txt")

# (nguyên văn bản gốc nam/nữ cảnh sát, bản có token) - cụ thể trước, chung sau
CAP = [
    ("His face in PROFILE, large, at the LEFT edge of the frame (curly hair, beard, gold hoop earring)",
     "The driver's face in PROFILE, large, at the LEFT edge of the frame ({{NET_HOC}})"),
    ("her face and upper body LARGE, filling the window, looking at him; behind her {{NEN_DUONG}}",
     "{{CS_CUA}} face and upper body LARGE, filling the window, looking at {{CHA_O}}; behind {{CS_O}} {{NEN_DUONG}}"),
    ("only the father's curly hair is faintly visible", "only the top of the {{CHA}}'s head is faintly visible"),
    ("until she reaches the driver's window", "until {{CS_ANH}} reaches the driver's window"),
    ("behind her ONLY the empty desert road", "behind {{CS_O}} ONLY the empty desert road"),
    ("only the officer and the empty road behind her are ever seen", "only the officer and the empty road behind {{CS_O}} are ever seen"),
    ("she holds {{DAO_GIAY_TO}} she has just been given", "{{CS_ANH}} holds {{DAO_GIAY_TO}} {{CS_ANH}} has just been given"),
    ("right beside him on the far side", "right beside {{CHA_O}} on the far side"),
    ("his face fills the frame from the hairline to the chin, small beads of sweat on his forehead and cheeks, worried; the dark car interior behind him.",
     "{{CHA_CUA}} face fills the frame from the hairline to the chin, small beads of sweat on {{CHA_CUA}} forehead and cheeks, worried; the dark car interior behind {{CHA_O}}."),
    ("the window behind him. Only a few beaded braids of the girl at the far left edge.",
     "the window behind {{CHA_O}}. Only a little of the girl's hair at the far left edge."),
    ("the phone screen in his hands", "the phone screen in {{CHA_CUA}} hands"),
    ("turned toward her father and looking up at him", "turned toward her {{CHA}} and looking up at {{CHA_O}}"),
    ("against his shoulder, both looking down at {{DAO_DIEN_THOAI}} he holds", "against {{CHA_CUA}} shoulder, both looking down at {{DAO_DIEN_THOAI}} {{CHA_ANH}} holds"),
    ("the screen of {{DAO_DIEN_THOAI}} in his hands; he looks down at it", "the screen of {{DAO_DIEN_THOAI}} in {{CHA_CUA}} hands; {{CHA_ANH}} looks down at it"),
    ("beside him, on his right", "beside {{CHA_O}}, on {{CHA_CUA}} right"),
    ("from his lap with his left hand", "from {{CHA_CUA}} lap with {{CHA_CUA}} left hand"),
    ("puts his hand back on the wheel. The girl stays seated upright beside him", "puts {{CHA_CUA}} hand back on the wheel. The girl stays seated upright beside {{CHA_O}}"),
    ("turns his head toward his daughter", "turns {{CHA_CUA}} head toward {{CHA_CUA}} daughter"),
    ("toward her father and talks to him;", "toward her {{CHA}} and talks to {{CHA_O}};"),
    # phần 2
    ("mounted on the dashboard in front of him, chest-up, his head LOW in the frame: the top of his hair at about 45% down from the top edge, his face in the lower-middle",
     "mounted on the dashboard in front of {{CHA_O}}, chest-up, {{CHA_CUA}} head LOW in the frame: the top of {{CHA_CUA}} hair at about 45% down from the top edge, {{CHA_CUA}} face in the lower-middle"),
    ("with no part of his head", "with no part of {{CHA_CUA}} head"),
    ("Behind him: {{NEN_HOC}}. He looks into the lens", "Behind {{CHA_O}}: {{NEN_HOC}}. The driver looks into the lens"),
    # chung
    ("the father", "the {{CHA}}"),
    ("her father", "her {{CHA}}"),
    ("tiếng Tây Ban Nha", "{{TIENG_BE}}"),
]
VN = re.compile(r"\bbố\b(?! cục)")   # "Ảnh bố cục" là tên trường

# đứa trẻ (BE) và đồng phục: nguyên văn bản gốc (bé gái, cảnh sát đồng phục navy) -> token. Chạy SAU CAP: lúc đó mọi "she/her" còn lại đều là của bé.
BE_CAP = [
    ("VOICE LOCK GIRL", "VOICE LOCK CHILD"),
    ("looks down at her and listens", "looks down at {{BE_O}} and listens"),
    ("Bé gái", "Bé {{BE_VN}}"),
    ("bé gái", "bé {{BE_VN}}"),
    ("con gái", "con {{BE_VN}}"),
    ("pink booster", "{{GHE_BE}} booster"),
    ("navy uniform", "{{MAU_DONGPHUC}} uniform"),
]
BE_TU = [(r"\bgirl\b", "girl", "{{BE_LOAI}}"), (r"\bshe\b", "she", "{{BE_ANH}}"), (r"\bher\b", "her", "{{BE_CUA}}"), (r"\bdaughter\b", "daughter", "{{BE_CON}}")]


def _than(t):
    i = t.find("\n=====")   # phần trên dòng chia phần đầu tiên không gửi Muse
    return (t, "") if i < 0 else (t[:i], t[i:])


def tham_so(t):
    for a, b in CAP:
        t = t.replace(a, b)
    t = boi_canh.tham_so(t)   # sau giới tính: "behind {{CS_O}} ONLY the empty desert road, ..." -> "... ONLY {{DUONG_SAU}}"
    dau, than = _than(t)
    than = VN.sub("{{CHA_VN}}", than)
    for a, b in BE_CAP:
        than = than.replace(a, b)
    for rx, _, tok in BE_TU:
        than = re.sub(rx, tok, than)
    return dau + than


def bo_tham_so(t):
    for rx, goc, tok in BE_TU:   # ngược thứ tự tham_so
        t = t.replace(tok, goc)
    t = t.replace("{{BE_O}}", "her")
    for a, b in reversed(BE_CAP):
        t = t.replace(b, a)
    t = boi_canh.bo_tham_so(t)
    for a, b in CAP:   # cụ thể trước: bản token của câu cụ thể chứa bản token của câu chung
        t = t.replace(b, a)
    return t.replace("{{CHA_VN}}", "bố")


if __name__ == "__main__":
    t = open(S, encoding="utf-8").read()
    t2 = tham_so(t)
    open(S, "w", encoding="utf-8").write(t2)
    print("token:", sorted(set(re.findall(r"\{\{(CHA\w*|CS_\w+|NET_HOC|TIENG_BE)\}\}", t2))))
    # còn sót đại từ nam/nữ ngoài phần nói về bé?
    for ln in t2.splitlines():
        for w in re.findall(r"\b(he|his|him|He|His|she)\b", ln):
            print("SOT:", w, "|", ln[:100])
            break
