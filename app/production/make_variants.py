#!/usr/bin/env python
"""Biến file JSON các biến thể thành 2 file CSV cho chế độ 2b của luo-flow.

  python make_variants.py variants/langlearn-turns.json [--out variants/out-turns]   (mỗi clip một lượt: LUOT)
  python make_variants.py variants/langlearn.json       [--out variants/out2b]       (mỗi cảnh nhiều lượt: THOAI)

Sinh ra:
  bang-option.csv           -> dán vào ô "Nâng cao: nhập token bằng bảng CSV" rồi bấm "Áp dụng bảng"
  danh-sach-bien-the.csv    -> "+ Import danh sách biến thể (CSV)" (mỗi dòng = 1 video)

Chế độ LUOT (khuyên dùng): mỗi biến thể có
  name, NGUOI_DAY, NGUOI_HOC, NEN_TRAI, NEN_PHAI, GIONG_DAY, GIONG_HOC, TEN_DAY, TEN_HOC,
  LUOT = [ {"who": "day"|"hoc", "text": "...", "emo": "surprised, curious" (tuỳ chọn)} , ... ]
  EMO_DAY / EMO_HOC (tuỳ chọn): cảm xúc mặc định của từng người khi lượt không ghi "emo"   (số lượt phải khớp số cảnh của script, mặc định 13)
Mỗi lượt thành token LUOT_n, giá trị là câu lệnh đầy đủ: ai nói đúng câu gì và người kia im lặng.
Chế độ THOAI: THOAI = 7 chuỗi (mỗi cảnh một khối nhiều lượt), dùng với split-dialogue-nodes.txt.
"""
import re
import argparse, csv, json, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pythonw: không có stdout
    pass
SINGLE = ["NGUOI_DAY", "NGUOI_HOC", "NEN_TRAI", "NEN_PHAI", "GIONG_DAY", "GIONG_HOC"]
EXTRA = ["DAO_CU", "DAO_GIU", "DAO_NGHI", "VIEC"]  # token thêm (dùng với gen_phone_script.py): có ở biến thể nào thì phải có ở mọi biến thể
THOAI_SCENES = 7


LEGACY_POS = {"DAY": "LEFT", "HOC": "RIGHT"}
LEGACY_ROLE = {"DAY": "tutor", "HOC": "learner"}


def ck(who):
    """Khoá nhân vật: "day" -> "DAY", "hoc" -> "HOC", khoá bất kỳ -> chữ HOA không dấu. Một nhân vật có các token TEN_<KHOÁ>, POS_<KHOÁ>, GIONG_<KHOÁ>, NGUOI_<KHOÁ>,
    và tuỳ chọn VAI_<KHOÁ> (tên vai trong prompt), NGHE_<KHOÁ> (tư thế khi im lặng), NHIN_<KHOÁ> (hướng nhìn khi nói), QUAY_LUNG_<KHOÁ> (quay lưng về camera: khi nói không đòi lộ miệng), EMO_<KHOÁ> (cảm xúc mặc định)."""
    return re.sub(r"[^A-Z0-9]", "", str(who or "").upper())


def chars_of(v):
    """Danh sách khoá nhân vật của biến thể, theo thứ tự: DAY, HOC (nếu có) rồi các khoá khác theo thứ tự xuất hiện (token TEN_*, rồi các lượt thoại)."""
    keys = []
    for k in v:
        m = re.fullmatch(r"TEN_([A-Z0-9]+)", k) if isinstance(k, str) else None
        if m and m.group(1) not in keys:
            keys.append(m.group(1))
    for t in v.get("LUOT", []) or []:
        c = ck(t.get("who"))
        if c and c not in keys:
            keys.append(c)
    return sorted(keys, key=lambda c: (("DAY", "HOC").index(c) if c in ("DAY", "HOC") else 2, keys.index(c)))


def cpos(v, c):
    """Nhãn vị trí của nhân vật, đưa vào prompt: POS_<khoá> (chữ bất kỳ, ví dụ LEFT, TOP, "center-right"); DAY/HOC có mặc định cũ."""
    return str(v.get(f"POS_{c}") or LEGACY_POS.get(c, "")).strip()


def cbox(v, c):
    """Vùng khuôn mặt để đo miệng: BOX_<khoá> ("x0,y0,x1,y1" theo tỉ lệ khung hình 0..1) nếu có, nếu không thì chính nhãn vị trí POS_<khoá> (LEFT/RIGHT/TOP/BOTTOM)."""
    return str(v.get(f"BOX_{c}") or cpos(v, c)).strip()


def crole(v, c):
    return str(v.get(f"VAI_{c}") or LEGACY_ROLE.get(c, "character")).strip()


def back_view(v, who):
    """Nhân vật quay lưng về camera (QUAY_LUNG_<khoá> khác rỗng, vd. góc qua vai): khi nói không đòi lộ miệng / nét mặt."""
    return bool(str(v.get(f"QUAY_LUNG_{ck(who)}") or "").strip())


def speaker_how(v, who, text, emo=""):
    """Cách NGƯỜI NÓI nói: nhịp, cảm xúc (mặt + giọng) và câu nói."""
    text = text.strip().replace('"', "'")
    # cảm xúc của lượt: "emo" trong từng lượt, nếu không có thì EMO_<khoá> của biến thể (EMO_DAY / EMO_HOC), mặc định theo dấu câu
    import prompt_parts as PP
    emo = (emo or v.get(f"EMO_{ck(who)}") or PP.default_emo(text, who)).strip()
    if back_view(v, who):   # quay lưng về camera: không tả nét mặt / môi (Muse sẽ xoay mặt người nói ra để khoe), cảm xúc chỉ ở giọng
        look = str(v.get(f"NHIN_{ck(who)}") or "").strip().rstrip(".")
        return (f'right away, clearly, in the mood "{emo}" heard in the voice only, and says exactly: "{text}"; their face stays hidden from the camera the whole time '
                "(the camera sees the back of their head), so no lip movement is shown: the voice simply comes from them, and the only visible sign of speaking "
                "is a small natural movement of the head and shoulders on the stressed words" + (f"; the whole time they speak, {look}" if look else ""))
    cues = PP.emo_cues(emo)
    # hướng nhìn KHI NÓI: NHIN_<khoá> (tuỳ chọn), vd. "keeps looking at the traveller, face turned toward her and away from the camera".
    # Không khai thì không nói gì về hướng nhìn của người nói (Muse hay xoay mặt người nói ra camera để khoe khẩu hình)
    look = str(v.get(f"NHIN_{ck(who)}") or "").strip().rstrip(".")
    return (f'right away, quickly and clearly, in the mood "{emo}" (face and voice)' + (f' - {cues}' if cues else '') + f', and says exactly: "{text}"'
            + (f"; the whole time they speak, {look}, keeping the head and eyes in that direction for the whole line" if look else ""))


def turn_text(v, who, text, emo="", emo2=""):
    """emo2 (phản ứng người nghe): chỉ dùng ở chế độ người nghe "idle" (v["listen"] == "idle"); chế độ "still" (cũ) người nghe không được biểu cảm hay phản ứng theo."""
    k, chars = ck(who), chars_of(v)
    if k not in chars:
        sys.exit(f'who "{who}" không có nhân vật tương ứng (cần token TEN_{k or "<KHOÁ>"}); các nhân vật của biến thể: {", ".join(chars) or "chưa có"}')
    how = speaker_how(v, who, text, emo)
    idle = v.get("listen") == "idle"
    # NGƯỜI NGHE - "still": không nói, không biểu cảm, không gật; làm tiếp việc riêng hoặc đứng yên như ảnh tĩnh.
    # "idle": môi luôn khép nhưng vẫn sống: chớp mắt, thở, phản ứng nhẹ trên mặt theo lời đang nghe (video call trông tự nhiên hơn)
    out = f'Only the {cpos(v, k)} character ({v.get(f"TEN_{k}", "")}) speaks in this clip, {how}'
    for c in chars:
        if c != k:
            task = v.get("VIEC", "").strip() if (k == "DAY" and c == "HOC") else ""   # việc riêng chỉ áp cho người học khi người dạy nói
            out += f' The {cpos(v, c)} character ({v.get(f"TEN_{c}", "")}) {listener_rule_text(task, idle, emo2)}.'
    return out


def listener_rule_text(task="", idle=False, emo2=""):
    if idle:
        react = str(emo2 or "").strip().replace('"', "'")
        base = ("does not speak: lips stay gently closed for the whole clip and never mouth the words; but they are alive and listening, "
                "in a natural idle: soft blinking, gentle breathing, small attentive head movements and a faint expression that follows the mood of what they hear"
                + (f' (reacting "{react}")' if react else " (a slight smile, a small eyebrow lift or a tiny nod)"))
        if task:
            return base + f", while quietly continuing {task} at a slow, steady pace"
        return base + ", eyes resting on the speaker"
    base = ("does not speak and does not react to the other character at all: lips sealed, a neutral relaxed face that never changes, "
            "no smile, no frown, no eyebrow raise, no nodding, no head turn, no glance at the phone, no gesture")
    if task:
        return base + f"; the only thing they do is quietly continue {task} at the same slow, steady pace, eyes on that task, completely unrelated to the words being spoken"
    return base + "; they stay as still as a paused image, eyes on the camera, only natural blinking"


def content_turn(v, who, text, emo="", emo2=""):
    """Câu lệnh lượt nói cho kịch bản NỘI DUNG của master template: phần lệnh nằm trong ngoặc tròn
    để bộ ghép luo-composer chỉ đếm âm tiết của câu nói thật (dùng tính độ dài clip)."""
    clean = lambda x: str(x).replace("(", ",").replace(")", "").replace('"', "'").strip()
    text = clean(text)
    emo = clean(emo or v.get("EMO_DAY" if who == "day" else "EMO_HOC") or "lively and expressive")
    pd, ph = v.get("POS_DAY", "LEFT"), v.get("POS_HOC", "RIGHT")
    spk, sil = (pd, clean(v["TEN_DAY"])), (ph, clean(v["TEN_HOC"]))
    if who == "hoc":
        spk, sil = (ph, clean(v["TEN_HOC"])), (pd, clean(v["TEN_DAY"]))
    import prompt_parts as PP
    cues = PP.emo_cues(emo)
    mood = f"in the mood '{emo}' (face and voice)" + (f" - {cues}" if cues else "")
    return (f"(Only the {spk[0]} character, {spk[1]}, speaks in this clip, right away, quickly and clearly, {mood}, and says exactly:) "
            f'"{text}" (The {sil[0]} character, {sil[1]}, stays completely silent and still, lips sealed.)'), emo


def write_content_script(v, folder, master="split-dialogue"):
    turns = v["LUOT"]
    if len(turns) < 3:
        sys.exit(f"{v['name']}: kịch bản nội dung cần ít nhất 3 lượt (hook, item, cta)")
    if v.get("POS_DAY", "LEFT") != "LEFT":
        print(f"  ⚠ {v['name']}: POS_DAY={v.get('POS_DAY')} — master split-dialogue đặt người dạy bên TRÁI; hãy dùng script node của bố cục này thay vì master.")
    rows = [content_turn(v, t["who"], t["text"], t.get("emo", "")) for t in turns]
    out = [f"=== VIDEO: {v['name']} ===",
           f"# Sinh tự động bằng make_variants.py --content-script từ {v['name']} (bản 2: mỗi cảnh một lượt nói).",
           f"MASTER: {master}", "KIND: pairs", f"TITLE: {v['name']}", "HOOK SIGN: Lượt 1",
           f"HOOK SAY: {rows[0][0]}", f"HOOK ACTION: {rows[0][1]} || {rows[0][1]}",
           f"CTA 1: {rows[-1][0]}", f"CTA 2: ({rows[-1][1]})", ""]
    for i, (say, emo) in enumerate(rows[1:-1], 2):
        out += [f"ITEM: Lượt {i}", f"  A: {say}", f"  B: ({emo})", "  AVOID: two characters speaking; the silent character mouthing words", ""]
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"dialogue-{v['name']}.txt")
    open(path, "w", encoding="utf-8").write("\n".join(out))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("variants")
    ap.add_argument("--out", default=".")
    ap.add_argument("--turns", type=int, default=13, help="số cảnh của script lượt (mặc định 13)")
    ap.add_argument("--content-script", help="thư mục: ghi thêm kịch bản nội dung dialogue-<tên>.txt cho master template split-dialogue (chế độ LUOT)")
    a = ap.parse_args()
    data = json.load(open(a.variants, encoding="utf-8"))
    names, rows = set(), []
    mode = "LUOT" if "LUOT" in data[0] else "THOAI"
    extra = [k for k in EXTRA if any(k in v for v in data)]
    for v in data:
        if v["name"] in names:
            sys.exit(f"Trùng tên biến thể: {v['name']}")
        names.add(v["name"])
        need = SINGLE + extra + (["TEN_DAY", "TEN_HOC"] if mode == "LUOT" else [])
        for k in need:
            if not v.get(k):
                sys.exit(f"{v['name']}: thiếu {k}")
        n = len(v.get(mode, []))
        want = a.turns if mode == "LUOT" else THOAI_SCENES
        if n != want:
            sys.exit(f"{v['name']}: {mode} phải có đúng {want} phần (khớp số cảnh của script), hiện {n}")
        row = {g: v[g] for g in SINGLE + extra}
        for i, item in enumerate(v[mode], 1):
            if mode == "LUOT":
                row[f"LUOT_{i}"] = turn_text(v, item["who"], item["text"], item.get("emo", ""), item.get("emo2", ""))
            else:
                row[f"THOAI_{i}"] = item
        rows.append((v["name"], row))
    groups = list(rows[0][1].keys())
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "bang-option.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nhom", "gia_tri", "mo_ta"])
        for name, row in rows:
            for g in groups:
                w.writerow([g, name, row[g]])
    with open(os.path.join(a.out, "danh-sach-bien-the.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(groups)
        for name, _ in rows:
            w.writerow([name] * len(groups))
    print(f"OK ({mode}): {len(rows)} variants, {len(groups)} tokens -> {a.out}")
    if a.content_script:
        if mode != "LUOT":
            sys.exit("--content-script chỉ dùng với chế độ LUOT")
        for v in data:
            print("  kịch bản nội dung ->", write_content_script(v, a.content_script))


if __name__ == "__main__":
    main()
