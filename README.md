# LUO Studio

Tao hang loat video quang cao dang hoi thoai (xem `HUONG-DAN.txt` de biet cach dung chi tiet).

## Cai dat tu ma nguon (Windows 10/11, 64-bit)

1. Tai ma nguon, chon mot trong hai cach (dat vao thu muc co duong dan ngan, vi du `D:\LUO-Studio`):
   - Tren GitHub bam "Code" > "Download ZIP" roi giai nen day du (khong chay ben trong file zip); hoac
   - Dung git:
     ```
     git clone https://github.com/tranluo-dev03/luo-studio.git LUO-Studio
     cd LUO-Studio
     ```
2. Cai dat mot lan (tu dong: cai Python 3.11 neu may chua co, tao `.venv`, cai thu vien, tai ffmpeg):
   ```
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```
3. Chay: bam `LUO Studio.bat` (hoac `LUO Studio (xem loi).bat` de xem log).

Cap nhat: `git pull` (hoac tai ZIP moi, giai nen de len, giu nguyen `userdata/`), roi chay lai `setup.ps1`.

Du lieu nguoi dung nam trong `userdata/` va khong duoc dua len git.
