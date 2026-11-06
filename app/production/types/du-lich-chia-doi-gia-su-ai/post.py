"""Hậu kỳ riêng của thể loại du-lich-chia-doi-gia-su-ai (Studio gọi khi kịch bản có [HAU KY] loai: du-lich-chia-doi-gia-su-ai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu: phần 1 phụ đề trên cao trên ô đen (Carla chữ xanh dương, robot chữ vàng); phần 2 phụ đề giữa khung (AI vàng, Carla trắng),
câu sai chữ đỏ + ❌ + viền đỏ nháy ở nửa phải ("fx": "wrong"); nói lại đúng ✅ + viền xanh ("fx": "right"); cụm tiếng Anh đúng tô xanh ("to").
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (đọc config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
