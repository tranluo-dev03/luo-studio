"""Hậu kỳ riêng của thể loại phong-van-pho-malayalam (Studio gọi khi kịch bản có [HAU KY] loai: phong-van-pho-malayalam):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu: phụ đề chữ đen trên ô trắng giữa khung, font Nirmala UI + shaping complex (chữ Malayalam), tâm y 960 ở cả hai phần.
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (đọc config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
