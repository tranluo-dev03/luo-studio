"""Hậu kỳ riêng của thể loại check-hanh-ly-hindi (Studio gọi khi kịch bản có [HAU KY] loai: check-hanh-ly-hindi):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu "oder 6": phụ đề chữ đen trên ô trắng, font Nirmala UI (có chữ Gujarati), cùng độ cao 1565 ở cả hai phần.
Câu sai: viền đỏ nháy + ❌ + tiếng ("fx": "wrong"); người phụ nữ nói lại đúng: viền xanh + ✅ ("fx": "right").
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (đọc config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
