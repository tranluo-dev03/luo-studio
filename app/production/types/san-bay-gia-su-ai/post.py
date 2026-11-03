"""Hậu kỳ riêng của thể loại san-bay-gia-su-ai (Studio gọi khi kịch bản có [HAU KY] loai: san-bay-gia-su-ai):
  python post.py raw.mp4 --scenes scenes.json --out final.mp4 --variant variant.json
Như video mẫu: phụ đề tiếng Anh (người hỏi trắng, người dùng vàng; độ cao riêng cho từng phần), dòng dịch đỏ viền trắng bên dưới ("dich"),
❌/✅/💲 cạnh câu ("icon": x/check/dollar), câu sai/đúng có viền đỏ/xanh nháy + tiếng ("fx": wrong/right), tên app trên ô vàng ("nhan").
Toàn bộ logic dùng chung: ../_chung/hau_ky.py (đọc config.json của thư mục này)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_chung"))
import hau_ky  # noqa: E402

if __name__ == "__main__":
    hau_ky.main(HERE)
