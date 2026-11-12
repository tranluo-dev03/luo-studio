"""Hậu kỳ riêng của thể loại tiem-thit-tieng-anh (Studio gọi khi kịch bản có [HAU KY] loai: tiem-thit-tieng-anh):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu: phụ đề chữ trắng viền đen ở khoảng 2/3 dưới khung; lượt tiếng Anh có dòng dịch tiếng Tây Ban Nha ("dich") ngay dưới.
Một phần, lượt thứ n = cảnh thứ n. Có cảnh KHÔNG LỜI (lượt "text" rỗng: Tavo ấp úng, bà chủ tìm quầy, chặt/gói thịt, montage học):
hau_ky dùng chung đánh số chỉ các lượt có lời (lượt có lời thứ i = cảnh i), nên ở đây đổi lại thành "lượt có lời thứ i -> đúng cảnh của nó".
Toàn bộ logic còn lại dùng chung: ../_chung/hau_ky.py (kiểu trong config.json)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

_units = hau_ky.PD.units_from_variant


def units_theo_canh(v, _scene_of_turn):
    co_loi = [i for i, t in enumerate(v.get("LUOT", [])) if str(t.get("text", "")).strip()]
    return _units(v, {ti: si for ti, si in enumerate(co_loi)})


if __name__ == "__main__":
    hau_ky.PD.units_from_variant = units_theo_canh
    hau_ky.main(HERE)
