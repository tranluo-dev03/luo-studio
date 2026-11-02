"""Lấy nội dung hậu kỳ từ BIẾN THỂ (không ghi cứng từ vựng trong config.json), để mỗi biến thể có từ vựng/app riêng vẫn hậu kỳ đúng:
- bút + chữ tiếng Anh: lượt dạng "¿Cómo se dice X? Se dice, Y. Repite conmigo. Y." (Tây Ban Nha) hoặc "Como se diz X? Se diz, Y. Repita comigo. Y." (Bồ Đào Nha)
  -> từ bản ngữ X, từ tiếng Anh Y, hàng = thứ tự lượt từ vựng;
- ô bảng quảng cáo: các lượt từ `ad_from` (config) trở đi, chia lời robot thành ô 2–3 dòng như video gốc;
  tô đỏ tên app (chữ sau "Descarga"/"Baixe"), cụm "số + đơn vị" (đổi số viết bằng chữ thành chữ số: "cuatro semanas" -> "4 semanas") và từ khoá trong config."""
import re

_NUM = {"uno": "1", "una": "1", "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5", "seis": "6", "siete": "7", "ocho": "8",
        "nueve": "9", "diez": "10", "once": "11", "doce": "12", "quince": "15", "veinte": "20", "treinta": "30",
        "um": "1", "uma": "1", "dois": "2", "duas": "2", "três": "3", "quatro": "4", "sete": "7", "oito": "8", "nove": "9",
        "dez": "10", "onze": "11", "doze": "12", "vinte": "20", "trinta": "30"}
_UNITS = r"(?:semanas?|d[ií]as?|meses|mes|mês|minutos?|horas?|años?|anos?|lecciones|lições|palabras|palavras)"
_VOCAB = re.compile(r"(?:¿\s*)?C[oó]mo se (?:dice|diz)\s+(.+?)\s*\?\s*Se (?:dice|diz),?\s*(.+?)\s*[.!]\s*(?:Rep[ií]te(?:lo)? conmigo|Repita comigo)\s*[.!]?\s*(.+?)\s*[.!]?\s*$", re.I)
_PT = re.compile(r"\bse diz\b|\bcomigo\b", re.I)   # dấu hiệu tiếng Bồ trong lượt từ vựng
_PUNCT = "¿?¡!.,"


def vocab_items(luot):
    """[{turn, es, en, row, text, lang}] từ các lượt từ vựng của biến thể. `es` = từ bản ngữ (tiếng Tây Ban Nha hoặc Bồ Đào Nha); lang = "es" | "pt"."""
    out, row = [], 0
    for i, t in enumerate(luot):
        s = str(t.get("text", "")).strip()
        m = _VOCAB.match(s)
        if not m:
            continue
        row += 1
        es = re.sub(r"\s+(?:en ingl[eé]s|em ingl[eê]s)$", "", m.group(1).strip(), flags=re.I)
        en = m.group(2).strip().strip(",")
        out.append({"turn": i, "es": es, "en": en.lower(), "row": row, "text": en[:1].upper() + en[1:], "lang": "pt" if _PT.search(s) else "es"})
    return out


def brand_of(luot):
    """Tên app: chữ viết hoa ngay sau "Descarga"/"Baixe (o)"/"Download" trong lời thoại."""
    for t in luot:
        m = re.search(r"\b(?:Descarga|Descargar|Baixe|Baixar|Download)\s+(?:o\s+)?([A-Z][\w-]+)", str(t.get("text", "")))
        if m and m.group(1).lower() not in ("now", "ya", "ahora", "agora"):
            return m.group(1)
    return ""


def _tokens(sentence, brand):
    """[(chữ hiện trên ô, lời nói gốc)]. "cuatro semanas" -> ("*4 semanas*", "cuatro semanas") là MỘT khối không ngắt dòng; tên app tô đỏ."""
    ws = sentence.split()
    out, i = [], 0
    while i < len(ws):
        w = ws[i]
        nxt = ws[i + 1] if i + 1 < len(ws) else ""
        unit = nxt.rstrip(_PUNCT)
        if (w.lower() in _NUM or w.isdigit()) and re.fullmatch(_UNITS, unit, flags=re.I):
            out.append(("*" + _NUM.get(w.lower(), w) + " " + unit + "*" + nxt[len(unit):], w + " " + nxt))
            i += 2
            continue
        core = w.strip(_PUNCT)
        out.append((w.replace(core, "*" + core + "*") if brand and core == brand else w, w))
        i += 1
    return out


def _chunks(sentence, brand, width=18, max_lines=3):
    """Chia một câu thành các ô, mỗi ô tối đa `max_lines` dòng; câu dài tách ở " y " như video gốc. Trả về [(các dòng hiện, lời nói)]."""
    parts = [sentence]
    if len(sentence) > 2 * width:
        parts = [p for p in re.split(r"(?<=\S)\s+(?=[ye]\s)", sentence) if p.strip()]   # "y" (Tây Ban Nha) / "e" (Bồ Đào Nha) = "và"
    out = []
    for p in parts:
        lines, cur = [], []
        for disp, said in _tokens(p, brand):
            if cur and len(" ".join(d for d, _ in cur).replace("*", "")) + 1 + len(disp.replace("*", "")) > width:
                lines.append(cur)
                cur = []
            cur.append((disp, said))
        if cur:
            lines.append(cur)
        while lines:
            take = max_lines if len(lines) != max_lines + 1 else 2   # tránh để lại 1 dòng lẻ
            group, lines = lines[:take], lines[take:]
            out.append(([" ".join(d for d, _ in ln) for ln in group], " ".join(s for ln in group for _, s in ln)))
    return out


def ad_phrases(luot, ad_from, keywords=()):
    """[{turn, say, text}] cho ô bảng quảng cáo: mỗi phần tử là một ô, `say` = lời đúng như robot nói (để căn thời điểm)."""
    brand = brand_of(luot)
    out = []
    for i, t in enumerate(luot):
        if i < ad_from:
            continue
        for sent in [s.strip() for s in re.findall(r"[^.?!]+[.?!]*", str(t.get("text", ""))) if s.strip()]:
            for lines, say in _chunks(sent, brand):
                text = "\n".join(lines)
                for k in keywords:   # từ khoá tô đỏ khai trong config (vd. "inglés")
                    text = re.sub(r"(?<![*\w])(" + re.escape(k) + r")(?![\w*])", lambda m: "*" + m.group(1) + "*", text)
                out.append({"turn": i, "say": say, "text": text})
    return out
