"""Hậu kỳ riêng của thể loại chia-tren-duoi-marathi (Studio gọi khi kịch bản có [HAU KY] loai: chia-tren-duoi-marathi):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu "oder 3": phụ đề chữ đen trên ô trắng, font Nirmala UI (có chữ Devanagari), tâm y 958 (mép dưới ô robot).
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (đọc config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
