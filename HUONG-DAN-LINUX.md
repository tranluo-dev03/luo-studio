# LUO Studio trên Linux (Ubuntu 22.04 / 24.04)

Dùng giống hệt Windows (xem `HUONG-DAN.md`): cùng giao diện, cùng thư mục `SAMPLE\`, cùng dữ liệu trong `userdata/`. Chỉ khác cách cài và cách mở.

## 1. Cài đặt (làm 1 lần)
```bash
git clone https://github.com/tranluo-dev03/luo-studio.git ~/LUO-Studio
cd ~/LUO-Studio
bash setup.sh
```
Script tự cài: ffmpeg, Python venv, Tk, font, thư viện đồ hoạ, Google Chrome (bản .deb, không dùng snap) và các thư viện Python trong `requirements.txt`. Cần tài khoản thường có `sudo` (không chạy bằng root). Đặt thư mục ở đường dẫn ngắn, không dấu, trong `$HOME`.

Tuỳ chọn: `--no-apt` (đã cài sẵn gói hệ thống), `--no-chrome` (tự cài trình duyệt).

## 2. Chạy
```bash
./luo-studio.sh          # nếu báo Permission denied:  bash luo-studio.sh
```
- **Máy có màn hình** (cài desktop, vào bằng RDP/VNC): mở cửa sổ ứng dụng như Windows.
- **Máy chủ không màn hình** (chỉ SSH, như VPS): Studio chạy ở cổng cố định **8765** (đổi bằng `LUO_STUDIO_PORT`). Từ máy tính của bạn mở đường hầm rồi vào trình duyệt:
  ```bash
  ssh -L 8765:127.0.0.1:8765 luo@<ip-máy-chủ>
  ```
  Mở `http://127.0.0.1:8765/`. Studio chỉ nghe ở `127.0.0.1` nên không lộ ra Internet.

Chạy nền, tự bật lại khi máy khởi động lại (systemd), tạo `/etc/systemd/system/luo-studio.service` (sửa `User` và đường dẫn):
```ini
[Unit]
Description=LUO Studio
After=network-online.target

[Service]
User=luo
WorkingDirectory=/home/luo/LUO-Studio
ExecStart=/home/luo/LUO-Studio/.venv/bin/python app/launcher.py --no-window
Restart=on-failure
KillMode=control-group

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload && sudo systemctl enable --now luo-studio
journalctl -u luo-studio -f      # xem log
```

## 3. Thêm tài khoản Muse
Giống Windows (mục 2 của `HUONG-DAN.md`): tab **API Muse** → **Thêm tài khoản** → dán cookie. Trên máy chủ không màn hình hãy dùng cách **dán cookie** (không dùng nút mở cửa sổ đăng nhập, vì cần màn hình).

## 4. Khác Windows
| Việc | Linux |
|---|---|
| Cập nhật | `bash update.sh` (thay `Cap nhat.bat`) |
| Chẩn đoán | `./chan-doan.sh` → `userdata/logs/chan-doan.txt` |
| Nút **Mở thư mục** | Mở bằng `xdg-open` nếu có màn hình; không màn hình thì không có gì xảy ra, lấy video ở `userdata/studio/exports/<dự án>/` (hoặc thư mục xuất đã đặt trong Cài đặt) |
| Hộp thoại **chọn file** | Cần màn hình. Không màn hình: dán đường dẫn file trên máy chủ vào ô, hoặc chép file lên bằng `scp` |
| Chép video về máy | `scp -r luo@<ip>:LUO-Studio/userdata/studio/exports/<dự án> .` |
| Claude CLI (tab **Video mới**) | Cài Claude Code trên máy chủ và đăng nhập (`claude`); Studio tìm ở `PATH`, `~/.local/bin`, `~/.npm-global/bin` |
| Đường dẫn trong Cài đặt (logo, outro, thư mục xuất) | Dùng đường dẫn Linux (`/home/luo/...`), không dùng `D:\...` |

## 5. Lỗi thường gặp
| Lỗi | Cách xử lý |
|---|---|
| `bad interpreter` / `\r` khi chạy `.sh` | File bị đổi xuống dòng kiểu Windows: `sed -i 's/\r$//' *.sh` rồi chạy lại |
| `libGL.so.1` hoặc `libgthread` không tìm thấy | `sudo apt install libgl1 libglib2.0-0t64` |
| API báo không mở được Chromium | Chưa có Chrome: chạy lại `bash setup.sh`. Nếu dùng Chromium snap: thư mục LUO Studio phải nằm trong `$HOME` và không có dấu chấm ở đầu tên thư mục |
| Chữ trên video lỗi font | `sudo apt install fonts-dejavu-core fonts-liberation` |
| Đứng "Hết thời gian chờ" khi gen | Máy ít RAM: mỗi tab Chrome ~0,45 GB. Giảm **Song song** trong Cài đặt |
| Cổng 8765 bận | `LUO_STUDIO_PORT=8800 ./luo-studio.sh` |
