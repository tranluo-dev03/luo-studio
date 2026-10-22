"""Các đoạn prompt dùng chung cho gen_turns_script.py và gen_phone_script.py.

Mục tiêu (bản 2):
- Nhân vật nói BIỂU CẢM hơn (nét mặt, cử chỉ rõ theo ý câu), giọng CÓ NGỮ ĐIỆU, nói RÕ và NHANH.
- NÓI XONG NGAY ĐẦU CLIP, phần còn lại ĐỨNG IM NHƯ ẢNH TĨNH: Muse không còn kéo chậm lời cho đủ 5–10s,
  và đoạn đuôi tĩnh cắt ở hậu kỳ vẫn khớp với clip sau (clip sau bắt đầu từ chính khung tĩnh đó).
Sửa ở đây rồi chạy lại các script sinh node.
"""
import re

EXPRESS = ("WHEN SPEAKING: the speaking character is clearly expressive: vivid, easy-to-read facial expressions that match the meaning "
           "and emotion of the line (raised eyebrows, bright or wide eyes, surprise, doubt, excitement, warmth, a real smile), "
           "lively head movement and natural hand gestures that support the words, small natural micro-expressions (blinks, eyebrow flicks, nods); "
           "the mouth shapes follow every syllable, never a blank, stiff, sleepy or flapping face. EVERY character, even a robot or an AI, has a "
           "fully human, expressive face and moves like a real person (only its body design may be mechanical). "
           "DELIVERY: sound like a real person talking spontaneously on a video call, NOT a text-to-speech engine, NOT an audiobook narrator: "
           "natural pitch movement inside every phrase, stress on the key words, a smile audible in the voice, light natural breaths, "
           "crisp but relaxed articulation, at a brisk, energetic conversational pace (about 3 to 4 words per second). "
           "The timbre stays the same in every clip, but pitch, energy and mood follow the emotion given for each line; "
           "never slow, dragged, sleepy, flat or monotone.")

NEG_EXTRA = ("slow, dragged or stretched speech; long pauses inside the line; speech spread over the whole clip; flat monotone voice; "
             "text-to-speech voice, robotic or metallic voice, audiobook narration, over-enunciated speech, uniform pitch from start to end; "
             "blank, stiff or expressionless face while speaking, lip movement that does not match the words; "
             "any movement, blinking, breathing motion or flicker during the final frozen hold")

# Cảm xúc -> chỉ dẫn CỤ THỂ cho nét mặt + giọng (Muse hiểu cử chỉ cụ thể tốt hơn tính từ trừu tượng)
EMO_CUES = {
    "curious": "head tilts slightly, eyebrows lift, bright attentive eyes; the voice rises at the end with real curiosity",
    "surprised": "eyebrows shoot up, eyes widen, mouth opens a little; the voice jumps up in pitch",
    "excited": "a big genuine smile, wide bright eyes, quick energetic nods; the voice is bouncy and higher in pitch",
    "enthusiastic": "a big genuine smile, wide bright eyes, quick energetic nods; the voice is bouncy and higher in pitch",
    "delighted": "a wide delighted smile, sparkling eyes; the voice is bright and musical",
    "warm": "a soft genuine smile, kind relaxed eyes; the voice is soft, warm and friendly",
    "friendly": "a soft genuine smile, kind relaxed eyes; the voice is soft, warm and friendly",
    "encouraging": "supportive nods, an open smiling face; the voice is upbeat and reassuring",
    "reassuring": "a gentle smile, soft nods, relaxed shoulders; the voice is calm, warm and comforting",
    "playful": "a mischievous half-smile, one raised eyebrow; a teasing, sing-song voice",
    "embarrassed": "eyes glance away, a shy awkward smile, hands and body stay put; the voice is softer and trails off",
    "hesitant": "eyes glance sideways, lips press, hands and body stay put; the voice is soft with hesitations and trailing off",
    "unsure": "eyes glance away, a small awkward smile, hands and body stay put; the voice is soft with hesitations",
    "doubtful": "furrowed brows, tight lips, a slight head tilt; the voice is flat and uncertain, with a small sigh",
    "worried": "furrowed brows, tense lips, worried eyes; the voice is lower and tight",
    "confused": "squinting eyes, a frown, a head tilt; the voice rises and stumbles",
    "proud": "the chin lifts, a satisfied smile; the voice is confident and full",
    "relieved": "a deep exhale, shoulders drop, a relieved smile; the voice relaxes and warms",
    "impressed": "eyebrows up, a slow nod, lips pursed in approval; the voice is warm with admiration",
    "decisive": "a firm nod, steady eyes; the voice is clear and determined",
    "confident": "a steady gaze, a small confident smile; the voice is clear and assured",
    "cheerful": "a bright smile, lively eyes; the voice is light and sunny",
    "persuasive": "expressive eyebrows, a sincere look; the voice is convincing and emphatic",
    "helpful": "a kind attentive look, an open expression; the voice is patient and clear",
    "upbeat": "a bright smile, lively head movement; the voice is energetic and positive",
    "hopeful": "wide hopeful eyes, eyebrows lifted; the voice rises with expectation",
    "clumsy": "a slightly awkward grin; the voice stumbles a little",
    "lively": "a bright expression and lively head movement; the voice is energetic and expressive",
    "expressive": "very readable face and gestures; the voice varies in pitch and energy",
}


EMO_FAMILY = {"unsure": "shy", "embarrassed": "shy", "hesitant": "shy", "doubtful": "worry", "worried": "worry", "confused": "worry",
              "excited": "happy", "enthusiastic": "happy", "delighted": "happy", "cheerful": "happy", "upbeat": "happy",
              "warm": "kind", "friendly": "kind", "encouraging": "kind", "reassuring": "kind", "helpful": "kind",
              "confident": "firm", "decisive": "firm", "proud": "firm"}


def emo_cues(emo):
    """Tra cảm xúc (tiếng Anh, cách nhau dấu phẩy) -> tối đa 2 chỉ dẫn nét mặt + giọng (mỗi nhóm cảm xúc gần nhau chỉ lấy 1)."""
    out, seen = [], set()
    for w in re.split(r"[,;/&]|\band\b", str(emo or "").lower()):
        w = w.strip()
        key = next((k for k in EMO_CUES if k in w), None)
        fam = EMO_FAMILY.get(key, key)
        if key and fam not in seen:
            seen.add(fam)
            out.append(EMO_CUES[key])
    return "; ".join(out[:2])


# Thêm cảm xúc chỉ có khi NGHE (mặt, mắt, cử động đầu nhẹ; không mở miệng)
EMO_CUES.update({
    "attentive": "eyes follow the speaker attentively, a subtle nod",
    "calm": "a relaxed face and a steady gaze",
    "amused": "a small amused smile, a slight eyebrow raise",
    "skeptical": "one eyebrow slightly raised, lips pressed, a small head tilt",
    "patient": "a soft patient smile, a gentle nod",
    "interested": "eyebrows lift slightly, eyes bright and focused",
    "listening": "eyes follow the speaker, a subtle nod",
})


def listen_cues(emo):
    """Chỉ dẫn cho NGƯỜI NGHE: chỉ giữ phần nét mặt (bỏ phần giọng), miệng luôn đóng."""
    faces = []
    for c in emo_cues(emo).split("; "):
        f = c.split("; the voice")[0].split(", the voice")[0]
        f = f.split("; ")[0] if "the voice" not in f else f.split("the voice")[0].rstrip("; ,")
        if f and f not in faces:
            faces.append(f)
    return "; ".join(faces[:2])


def default_emo(text, who="day"):
    """Cảm xúc mặc định theo dấu câu khi người dùng chưa ghi: ? tò mò, ! hào hứng, ... ngập ngừng."""
    t = str(text or "").strip()
    if t.endswith("...") or t.endswith("…"):
        return "hesitant, unsure"
    if t.endswith("?"):
        return "curious, expressive"
    if t.endswith("!"):
        return "excited, cheerful"
    return "warm, lively, encouraging" if who == "day" else "curious, expressive, friendly"


def timing(rest):
    return ("TIMING (speak first, then freeze): the speaker starts talking immediately, within the first 0.3 seconds, and says the whole line "
            "in one go at the brisk pace above, finishing as early as possible (normally within the first half of the clip). Do NOT slow down, "
            "stretch the words or add pauses to fill the clip length. Right after the last word, within half a second, both characters settle "
            f"into the neutral rest pose ({rest}) and then HOLD IT COMPLETELY FROZEN, like a still photograph, until the very last frame: no body, "
            "head, face, eye, mouth or hand movement, no blinking, no camera or lighting change, every remaining frame identical. This silent "
            "frozen tail is cut in editing, and the next clip starts from this exact frozen frame.")


def speak(i, voice_note):
    return ("In this clip: {{LUOT_%d}} " % i +
            "Only that one character speaks, with accurate lip-sync, starting immediately, at a brisk, clear and expressive pace with lively "
            "intonation and a facial expression that matches the line; the other character stays silent with lips sealed. "
            "As soon as the line is finished, both settle into the neutral rest pose and hold it completely frozen until the end of the clip "
            "(a silent frozen tail that is cut in editing). " + voice_note + " VIDEO SUFFIX.")


VN_BEATS = "Diễn biến: Người đến lượt nói ngay từ đầu clip, nói nhanh, rõ, có ngữ điệu và biểu cảm theo ý câu; người kia im lặng, miệng khép. Nói xong thì cả hai về tư thế nghỉ và đứng im như ảnh tĩnh đến hết clip."
VN_AUDIO = "Audio: Không có nhạc, không âm thanh môi trường. Chỉ giọng của đúng một nhân vật đang nói, rõ, nhanh, có ngữ điệu, nói xong ngay ở đầu clip; phần còn lại im lặng hoàn toàn."


def vn_end(last):
    return ("Khung cuối: Nói xong cả hai về tư thế nghỉ, miệng khép, rồi đứng im hoàn toàn như ảnh tĩnh đến hết clip"
            + ("; kết thúc video." if last else "; khung cuối chính là khung tĩnh đó, để lượt sau nối tiếp từ đúng khung này."))


def upgrade(head, rest):
    """Nâng cấp khối khóa đầu file: thêm biểu cảm/giọng, thay TIMING, bổ sung NEGATIVE."""
    assert "ONE SPEAKER PER CLIP" in head and "TIMING:" in head and "[NEGATIVE]:" in head
    head = head.replace("ONE SPEAKER PER CLIP", EXPRESS + "\nONE SPEAKER PER CLIP", 1)
    head = head.replace("Only the face, head and hands of the speaker move, gently.",
                        "While speaking, the speaker's face, head and hands move expressively and naturally.")
    head = re.sub(r"TIMING:.*?because the next clip starts from it\.", lambda m: timing(rest), head, count=1, flags=re.S)
    head = re.sub(r"(\[NEGATIVE\]:\n)(.*?)\.?\s*$", lambda m: m.group(1) + m.group(2).rstrip(". ") + "; " + NEG_EXTRA + ".\n", head, count=1, flags=re.S)
    return head
