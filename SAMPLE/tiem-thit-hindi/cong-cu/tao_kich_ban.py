"""Sinh KICH-BAN-TIEM-THIT-HINDI.txt: dùng lại bảng góc máy + bảng cảnh của tiem-thit-tieng-anh, đổi ngôn ngữ mẹ đẻ Tây Ban Nha -> Hindi
và loại hậu kỳ -> tiem-thit-hindi (phụ đề chữ Devanagari). Không sửa file của thể loại gốc.
  runtime\python.exe SAMPLE\tiem-thit-hindi\cong-cu\tao_kich_ban.py"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "tiem-thit-tieng-anh", "cong-cu", "tao_kich_ban.py")
OUT = os.path.join(HERE, "..", "KICH-BAN-TIEM-THIT-HINDI.txt")

spec = importlib.util.spec_from_file_location("tkb_goc", SRC)
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)


def doi(s):
    return (s.replace("Spanish accent", "Indian accent").replace("Spanish", "Hindi")
             .replace("tiếng Tây Ban Nha", "tiếng Hindi").replace("Tây Ban Nha", "Hindi"))


for s in K.S:
    for k, v in list(s.items()):
        if isinstance(v, str):
            s[k] = doi(v)
K.HEAD = doi(K.HEAD).replace("loai: tiem-thit-tieng-anh", "loai: tiem-thit-hindi")
K.OUT = OUT

if __name__ == "__main__":
    K.main()
