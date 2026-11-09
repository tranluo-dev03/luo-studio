r"""Sau lỗi "AI cao, người thấp" (06/11/2026): khôi phục ảnh gốc người học phần 2 trước khi Studio dịch xuống, xoá clip phần 2 đã gen từ ảnh dịch.
CHỈ chạy khi các biến thể đã DỪNG. Rồi trong Studio: "Làm lại từ cảnh 4" (cảnh đầu phần 2).
    .venv\Scripts\python.exe SAMPLE\du-lich-chia-doi-gia-su-ai\cong-cu\khoi_phuc_anh_goc_p2.py "Face-to-face-Mexico---20-bien-the-b3d8" """
import glob, os, shutil, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
for d in sorted(glob.glob(os.path.join(ROOT, "userdata", "studio", "runs", sys.argv[1], "*", "phan2"))):
    src = os.path.join(d, "base_HOC.png.truoc-dich.png")
    if not os.path.exists(src):
        continue
    shutil.copyfile(src, os.path.join(d, "base_HOC.png"))
    gone = [f for f in os.listdir(d) if f.startswith(("scene", "listen_"))]
    for f in gone:
        os.remove(os.path.join(d, f))
    print(os.path.basename(os.path.dirname(d)), "khôi phục base_HOC, xoá", len(gone), "tệp phần 2")
