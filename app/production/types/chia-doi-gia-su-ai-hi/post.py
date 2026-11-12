"""Hậu kỳ riêng của thể loại chia-doi-gia-su-ai-hi (Studio gọi khi kịch bản có [HAU KY] loai: chia-doi-gia-su-ai-hi):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu (màn hình chia đôi, robot trái / người dùng phải): phụ đề ô đen giữa khung, AI chữ trắng, người dùng chữ vàng;
câu sai chữ đỏ + viền đỏ nháy ở nửa phải, cuối câu ("fx": "wrong"); câu nói lại đúng chữ xanh + viền xanh ("fx": "right").
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (đọc config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
