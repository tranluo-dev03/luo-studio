"""Sinh KICH-BAN-8DA55FC4-DIEN-GIA-HINDI-HOOK.txt (kịch bản B, đổi hook) từ kịch bản A.
Chỉ CẢNH 1 (hook) đổi: lời {{LUOT_1}} vẫn là token, cử chỉ / nét mặt / khung cuối / diễn biến của hook thành token HOOK_*.
Mọi thứ từ CẢNH 2 trở đi giữ nguyên chữ của A. Sửa A rồi chạy lại script này để B luôn khớp.
Chạy: python SAMPLE/8da55fc4-dien-gia-hindi/cong-cu/tao_kich_ban_hook.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
A = os.path.join(ROOT, "KICH-BAN-8DA55FC4-DIEN-GIA-HINDI.txt")
B = os.path.join(ROOT, "KICH-BAN-8DA55FC4-DIEN-GIA-HINDI-HOOK.txt")

THAY = [
    ('  Kịch bản A ("goc", giữ nguyên hook + tình huống như video gốc) của mã `8da55fc4-dien-gia-hindi`.',
     '  Kịch bản B ("hook", GIỮ NGUYÊN TÌNH HUỐNG, ĐỔI HOOK) của mã `8da55fc4-dien-gia-hindi`: song sinh với `KICH-BAN-8DA55FC4-DIEN-GIA-HINDI.txt` (sinh bằng cong-cu/tao_kich_ban_hook.py). '
     'Từ CẢNH 2 trở đi giữ y như A; chỉ CẢNH 1 (HOOK) đổi và mọi thứ của hook là token: lời {{LUOT_1}}, cử chỉ {{HOOK_HANH_DONG}} / {{HOOK_DIEN_BIEN}}, nét mặt {{HOOK_CAM_XUC}}, khung cuối {{HOOK_KHUNG_CUOI}}.'),
    ("CẢNH 1 (0:00–0:05): Lượt 1 — HOOK\n",
     "CẢNH 1 (0:00–0:05): Lượt 1 — HOOK MỚI (mọi thứ của hook là token, xem BIEN-THE-8DA55FC4-DIEN-GIA-HINDI-HOOK.json)\n"),
    ("Khung cuối: {{TEN_HOC}} nhìn ống kính, ngón trỏ đã hạ xuống, hai tay ngang bụng, miệng khép; khung này là khung đầu của cảnh sau.\n"
     "Diễn biến: Nói luôn từ đầu clip, nghiêm nghị, giơ ngón trỏ tay phải (tay đang cầm bút bấm) lên ngang vai ngay từ các từ đầu câu, giữ trong lúc nói rồi hạ xuống trước từ cuối. Nói xong đứng im đến hết clip.\n",
     "Khung cuối: {{HOOK_KHUNG_CUOI}} Khung này là khung đầu của cảnh sau.\n"
     "Diễn biến: Nói luôn từ đầu clip. {{HOOK_DIEN_BIEN}} Nói xong đứng im đến hết clip.\n"),
    ("{{TEN_HOC}} speaks with clear lip-sync, serious and confident, looking into the lens. ACTION, done WHILE the line is spoken and complete before the last word: "
     "{{HE}} raises the index finger of {{HIS}} right hand (the hand holding the clicker) to shoulder height near the start of the line, holds it while making the point, then lowers it before the last word; the left hand stays low.",
     "{{TEN_HOC}} speaks with clear lip-sync, {{HOOK_CAM_XUC}}, looking into the lens. ACTION, done WHILE the line is spoken and complete before the last word: {{HOOK_HANH_DONG}}"),
    ("Negative prompt: a second voice; text or captions; split screen; camera movement; the finger staying raised after the line;",
     "Negative prompt: a second voice; text or captions; split screen; camera movement; the hand staying raised after the line;"),
]


def main():
    s = open(A, encoding="utf-8").read()
    for cu, moi in THAY:
        assert s.count(cu) == 1, f"Không thấy đúng 1 lần: {cu[:80]!r}"
        s = s.replace(cu, moi)
    open(B, "w", encoding="utf-8").write(s)
    print("Đã ghi", os.path.basename(B))


if __name__ == "__main__":
    main()
