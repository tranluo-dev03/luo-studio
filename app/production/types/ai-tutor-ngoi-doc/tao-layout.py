"""Dựng wireframe bố cục cho Muse (assets/layout.png), đo từ video gốc 1210_langla vocab football PT_003_5.mp4 (720x1280):
đỉnh đầu robot ~34% chiều cao, đầu (cả tai nghe) ~30% chiều rộng, vai ~42%, bàn ~83%; 34% phía trên để trống cho bảng.
Chỉ có hình khối xám, không chữ. Engine gửi kèm lệnh gen ảnh khung đầu và nói rõ đây chỉ là hướng dẫn bố cục.
Chạy: python tao-layout.py"""
import os
from PIL import Image, ImageDraw

W, H = 720, 1280
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "layout.png")
im = Image.new("RGB", (W, H), (205, 205, 205))
d = ImageDraw.Draw(im)
Y = lambda f: int(H * f)
X = lambda f: int(W * f)
d.rectangle((0, 0, W, Y(0.335)), fill=(245, 245, 245))                      # vùng trên để trống (bảng ghép sau)
d.line((0, Y(0.335), W, Y(0.335)), fill=(120, 120, 120), width=3)
body = [(X(0.31), Y(0.50)), (X(0.69), Y(0.50)), (X(0.84), Y(0.60)), (X(0.95), Y(0.80)), (X(0.95), H), (X(0.05), H), (X(0.05), Y(0.80)), (X(0.16), Y(0.60))]
d.polygon(body, fill=(110, 110, 110))                                         # vai + thân + hai tay
d.rectangle((X(0.46), Y(0.45), X(0.54), Y(0.52)), fill=(90, 90, 90))          # cổ
d.ellipse((X(0.36), Y(0.335), X(0.66), Y(0.475)), fill=(60, 60, 60))          # đầu cả tai nghe, rộng 30%
d.rectangle((0, Y(0.83), W, H), fill=(150, 150, 150))                         # bàn
d.polygon(body[3:5] + body[5:7], fill=(110, 110, 110))
im.save(OUT)
print("ok ->", OUT)
