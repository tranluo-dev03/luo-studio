"""Hậu kỳ riêng của thể loại canh-sat-gia-su-ai (Studio gọi khi kịch bản có [HAU KY] loai: canh-sat-gia-su-ai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu: phần 1 phụ đề ô vàng chữ đen ở 2/3 dưới khung; phần 2 phụ đề ngay dưới ô AI: AI chữ xanh ngọc trên ô đen,
tài xế chữ đen trên ô trắng; từ sai tô đỏ + ❌ + viền đỏ nháy, câu sửa đúng tô xanh + ✅ + viền xanh ("to", "icon", "fx"); 💲 ở câu "money".
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (kiểu phụ đề theo phần / người nói trong config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
