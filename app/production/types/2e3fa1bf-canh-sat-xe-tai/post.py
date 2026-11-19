"""Hậu kỳ riêng của thể loại 2e3fa1bf-canh-sat-xe-tai (Studio gọi khi kịch bản có [HAU KY] loai: 2e3fa1bf-canh-sat-xe-tai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Một phần, 4 cảnh: phụ đề chữ trắng ô đen ở ~2/3 dưới khung; câu sai tô đỏ + ❌ + viền đỏ nháy, câu sửa đúng tô xanh + ✅ + viền xanh ("to", "icon", "fx").
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (kiểu phụ đề trong config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
