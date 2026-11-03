"""Hậu kỳ riêng của thể loại soi-hanh-ly-gia-su-ai (Studio gọi khi kịch bản có [HAU KY] loai: soi-hanh-ly-gia-su-ai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu: phụ đề tiếng Anh chữ trắng viền đen ở phần 1; phần 2 AI chữ vàng, người mẹ chữ trắng; cùng độ cao (~58% khung).
Câu sai: viền đỏ nháy + ❌ + tiếng ("fx": "wrong"); người mẹ nói lại đúng: viền xanh + ✅ ("fx": "right").
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (đọc config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
