"""Hậu kỳ riêng của thể loại 6fbf4a4b-ref-noi-chuyen (Studio gọi khi kịch bản có [HAU KY] loai: 6fbf4a4b-ref-noi-chuyen):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Một phần, ghép 2 lớp (robot ô trên, người học nền): phụ đề ô trắng/vàng chữ đen dưới ô robot; câu sai tô đỏ + ❌, câu sửa tô xanh + ✅ ("to", "icon", "fx").
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (kiểu phụ đề trong config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
