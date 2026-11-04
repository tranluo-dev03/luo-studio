"""Gen riêng của thể loại soi-hanh-ly-gia-su-ai: MỘT dự án, hai phần trong cùng một kịch bản (cùng khuôn san-bay-gia-su-ai).
  Phần 1: nhân viên soi chiếu hỏi người mẹ bế con ở máy soi hành lý (cảnh thường, 3 góc máy: toàn cảnh, cận người mẹ, cận hai người).
  Phần 2: hội thoại người mẹ (selfie) + gia sư AI, ghép 2 lớp (robot ở ô bo góc góc trên phải).
  Vào phần 2: nhoè chuyển động như video mẫu.
Toàn bộ logic nhiều phần dùng chung: ../_chung/nhieu_phan.py. Studio gọi run(...) khi kịch bản có [HAU KY] loai: soi-hanh-ly-gia-su-ai."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import nhieu_phan as NP  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))

# Muse (04/11/2026) là agent có bộ nhớ: nó tóm tắt prompt rồi mới gọi công cụ tạo media, trộn MEMORY.md / AGENTS.md / Goal của cả loạt
# video vào (biết cảnh này ai nói câu gì) -> clip người nghe phần 2 nhép miệng, nhái cử chỉ người nói. Câu dẫn này đặt trước MỌI prompt của thể loại.
MEDIA_DIRECTIVE = (
    "[DIRECT MEDIA REQUEST] Call the media generation tool exactly once and give it the full request text below as its prompt, "
    "VERBATIM, word for word: do not summarize, shorten, paraphrase, translate or add anything. Do not read or use MEMORY.md, "
    "AGENTS.md, goals, notes, earlier chats, or earlier images and videos from the library; use only the files attached to this "
    "message, in the order given. Do not add any dialogue, speech, action or person that the request does not ask for. "
    "Do not launch subagents, do not draft follow-up clips, do not write memory or notes about this request. "
    "Reply only with the generated file.\n\n--- REQUEST ---\n")


def run(vdata, template, out_dir, opts, emit, cancel):
    NP.E._TL.prompt_prefix = MEDIA_DIRECTIVE if CFG.get("chi_thi_muse", True) else ""
    try:
        return NP.run(vdata, template, out_dir, opts, emit, cancel, blur_strength=float(CFG.get("nhoe", 1.0)))
    finally:
        NP.E._TL.prompt_prefix = ""
