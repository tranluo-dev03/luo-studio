# LUO-API

API tự host, tương thích OpenAI, biến giao diện web **Muse.ai** thành các endpoint HTTP để tạo **chat, ảnh và video**. LUO-API là server đi kèm extension **LUO-AI** (repo [luo-muse-flow](https://github.com/tranluong24/luo-muse-flow)), nhưng có thể dùng độc lập với bất kỳ client nào.

> Đây là tích hợp bên thứ ba, không liên kết và không được Muse xác nhận. Chỉ dùng với tài khoản bạn được phép sử dụng và tuân thủ điều khoản của dịch vụ.
> Dự án phát triển từ [czg86389-hub/muse2api](https://github.com/czg86389-hub/muse2api) (giấy phép MIT). Bản gốc tiếng Anh: [README.en.md](README.en.md). Bản rút gọn: [README.vi.md](README.vi.md).

## Mục lục
1. [Cách hoạt động](#cách-hoạt-động)
2. [Cấu trúc thư mục](#cấu-trúc-thư-mục)
3. [Cài đặt](#cài-đặt)
4. [Cấu hình `.env`](#cấu-hình-env)
5. [Thêm tài khoản Muse](#thêm-tài-khoản-muse)
6. [Gọi API](#gọi-api)
7. [Session: dùng chung một chat](#session-dùng-chung-một-chat)
8. [Tham chiếu ảnh / video / âm thanh](#tham-chiếu-ảnh--video--âm-thanh)
9. [Trang quản trị](#trang-quản-trị)
10. [Kiểm thử](#kiểm-thử)
11. [Bảo mật](#bảo-mật)
12. [Xử lý sự cố](#xử-lý-sự-cố)
13. [Giấy phép](#giấy-phép)

## Cách hoạt động

```
Client (OpenAI SDK / curl / extension LUO-AI)
        │  HTTP + Authorization: Bearer <MUSE2API_KEY>
        ▼
FastAPI (app.py) ── hàng đợi + khóa trình duyệt (GEN_LOCK) ── AccountPoolManager (xoay tài khoản)
        │
        ▼
MuseEngine (engine.py) ──CDP (cdp.py)──► Chromium ẩn ──► muse.ai
        │                                   (nạp cookie, gõ prompt, đính file, chờ attachment)
        ▼
data/media/*  ← ảnh/video tải về, phục vụ tại /v1/media/{tên-file}
```

- Server mở một **Chromium ẩn** qua Chrome DevTools Protocol, nạp cookie của tài khoản Muse, nhập prompt vào ô chat, đính file tham chiếu rồi chờ ảnh/video xuất hiện.
- Nhiều tài khoản được xoay vòng; khi một lần tạo lỗi, server tự chuyển sang tài khoản dự phòng.
- Video chạy **bất đồng bộ**: `POST` trả về `task_id`, bạn hỏi lại trạng thái bằng `GET`.

## Cấu trúc thư mục

| Đường dẫn | Công dụng |
|---|---|
| `app.py` | FastAPI: toàn bộ endpoint `/v1/*` và `/admin/*`, hàng đợi, keepalive |
| `engine.py` | Điều khiển Chromium: mở chat, gửi prompt, đính file, chờ kết quả, quản lý session |
| `cdp.py` | Client Chrome DevTools Protocol tối giản |
| `store.py` | Lưu tài khoản và task (JSON trong `data/`) |
| `config.py` | Đọc `.env` và biến môi trường |
| `admin.html` | Giao diện quản trị |
| `extension/` | Extension phụ giúp lấy cookie Muse |
| `tools/` | Script lấy cookie, userscript import cookie, kiểm tra selector |
| `deploy/` | Mẫu `systemd` và `nginx` |
| `tests/` | Kiểm thử cục bộ (không gọi Muse thật) |
| `Dockerfile`, `docker-compose.yml` | Triển khai bằng Docker |
| `.env.example` | Mẫu cấu hình (không chứa bí mật) |

`data/` (tài khoản, task, media, log) và `.env` **không được commit**.

## Cài đặt

### Cách 1: Docker

```sh
git clone https://github.com/tranluong24/luo-muse-api.git
cd luo-muse-api
cp .env.example .env        # sau đó sửa MUSE2API_KEY
docker compose up -d --build
```

### Cách 2: Python (Windows / Linux / macOS)

Yêu cầu: Python 3.10+ và Google Chrome hoặc Chromium.

```powershell
git clone https://github.com/tranluong24/luo-muse-api.git
cd luo-muse-api
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 18610
```

Linux/macOS: dùng `.venv/bin/python` thay cho đường dẫn trên.

Mở `http://127.0.0.1:18610/admin?key=KEY_CỦA_BẠN` để vào trang quản trị. Giữ `--host 127.0.0.1` nếu chỉ dùng trên máy. Muốn mở ra ngoài, hãy đặt sau reverse proxy HTTPS (xem `deploy/nginx.example.conf`).

### Tự chạy khi đăng nhập Windows
Dùng Task Scheduler: *Create Task* → Trigger *At log on* → Action:
- Program: `<repo>\.venv\Scripts\python.exe`
- Arguments: `-m uvicorn app:app --host 127.0.0.1 --port 18610`
- Start in: `<repo>`

## Cấu hình `.env`

Sao chép `.env.example` thành `.env`. Các biến chính:

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `MUSE2API_KEY` | tự sinh lần đầu | Khóa cho API và trang quản trị. **Hãy đặt chuỗi dài, ngẫu nhiên** |
| `MUSE2API_HOST` / `MUSE2API_PORT` | `0.0.0.0` / `18610` | Địa chỉ và cổng lắng nghe |
| `MUSE2API_PUBLIC_BASE` | trống | URL công khai hiển thị cho client |
| `MUSE2API_CHROMIUM` | tự dò | Đường dẫn Chrome/Chromium |
| `MUSE2API_CDP_PORT` | `19210` | Cổng debug nội bộ của trình duyệt, **không mở ra ngoài** |
| `MUSE2API_IMAGE_TIMEOUT` | `240` | Timeout tạo ảnh (giây) |
| `MUSE2API_VIDEO_TIMEOUT` | `600` | Timeout tạo video (giây) |
| `MUSE2API_CHAT_TIMEOUT` | `300` | Timeout chat (giây) |
| `MUSE2API_CONCURRENCY` | `2` | Số tác vụ tạo nội dung chạy đồng thời tối đa |
| `MUSE2API_KEEPALIVE_DISABLED_ACCOUNTS` | `0` | `1` = vẫn giữ phiên cho tài khoản đã tắt |
| `MUSE2API_UPDATER_ENABLED` | `0` | Cập nhật online từ upstream, nên để tắt |
| `MUSE2API_ALLOW_WEB_PUSH` | `0` | Cho phép publish repo từ trang quản trị, nên để tắt |

## Thêm tài khoản Muse

Server cần cookie của phiên Muse đã đăng nhập (`hatch_sess`, `hatch_gw`, `hatch_vml`, `hatch_native_auth_device`). Có 3 cách:
1. Trang `/admin` → thêm tài khoản và dán cookie.
2. Extension trong thư mục `extension/` hoặc userscript `tools/muse2api_cookie_importer.user.js` gửi cookie từ trang muse.ai lên server.
3. `tools/get_muse_cookie.py`.

Mẫu định dạng nằm ở `data/accounts.example.json` (toàn giá trị giả). File thật `data/accounts.json` chứa cookie, **tuyệt đối không công khai**.

## Gọi API

Mọi endpoint bảo vệ cần header `Authorization: Bearer YOUR_KEY`.

| Endpoint | Công dụng |
|---|---|
| `GET /healthz`, `GET /readyz` | Kiểm tra sống / sẵn sàng (không cần key) |
| `GET /v1/models` | Danh sách model |
| `POST /v1/chat/completions` | Chat, hỗ trợ stream |
| `POST /v1/responses` | Responses API |
| `POST /v1/images/generations` | Tạo ảnh (đồng bộ) |
| `POST /v1/images/tasks`, `GET /v1/images/tasks/{id}` | Tạo ảnh bất đồng bộ |
| `POST /v1/images/edits` | Sửa ảnh |
| `POST /v1/videos` | Tạo video, trả `task_id` |
| `GET /v1/videos/{task_id}` | Trạng thái và kết quả video |
| `DELETE /v1/sessions/{sid}` | Đóng một session chat |
| `GET /v1/media/{tên-file}` | Tải file đã tạo |

Ví dụ:

```sh
# Liệt kê model
curl http://127.0.0.1:18610/v1/models -H "Authorization: Bearer YOUR_KEY"

# Chat
curl http://127.0.0.1:18610/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"model":"muse-spark","messages":[{"role":"user","content":"Xin chào"}]}'

# Tạo video rồi hỏi trạng thái
curl http://127.0.0.1:18610/v1/videos \
  -H "Authorization: Bearer YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"prompt":"Một chú mèo chạy trên bãi cỏ"}'
curl http://127.0.0.1:18610/v1/videos/TASK_ID -H "Authorization: Bearer YOUR_KEY"
```

## Session: dùng chung một chat

Thêm trường `session` (chuỗi bất kỳ) vào request ảnh/video để các lần gọi cùng `session` dùng **chung một chat Muse trên cùng một tài khoản**. Extension LUO-AI dùng cách này để ảnh và video của một kịch bản nằm trong một cuộc trò chuyện.
- Khi một bước lỗi, server bỏ chat đó và mở chat mới cho lần thử lại.
- Session tự đóng sau khoảng 30 phút không dùng, hoặc đóng chủ động bằng `DELETE /v1/sessions/{sid}`.

## Tham chiếu ảnh / video / âm thanh

`/v1/images/tasks`, `/v1/images/generations` và `/v1/videos` nhận thêm:
- `reference_images`: danh sách ảnh (data URL hoặc URL http), đính theo thứ tự.
- `reference_videos`, `reference_audios` (chỉ video): data URL, URL http(s) hoặc đường dẫn file. Thứ tự đính vào chat: ảnh → video → âm thanh. Loại file được nhận diện theo nội dung.
- `raw_prompt: true`: gửi `prompt` nguyên văn, không bọc mẫu dựng sẵn.

Muse có dùng file tham chiếu hay không do model của Muse quyết định.

## Trang quản trị

`/admin` cho phép: thêm/sửa/xóa tài khoản, kiểm tra tài khoản, xem quota, chạy keepalive, xem và xóa task, xem và xóa media, đổi API key.

## Kiểm thử

```sh
python -m pip install -r requirements.txt
python tests/test_admin_base_url.py
python tests/test_async_images.py
python tests/test_media_delete.py
python tests/test_media_selection.py
python tests/test_session_health.py
python tests/test_vm_wait.py engine.py --assert
python tests/test_concurrency.py
```

Các bài test không đăng nhập Muse và không tạo nội dung thật.

## Bảo mật

- **Không commit** `.env`, `data/accounts.json`, `data/tasks.json`, cookie, browser profile, media riêng tư. `.gitignore` đã chặn các mục này.
- Đặt `MUSE2API_KEY` mạnh và riêng. Nếu lỡ lộ key, đổi ngay trong trang quản trị.
- Cổng CDP (`19210`) chỉ dùng nội bộ, không mở ra Internet.
- Nếu cần truy cập từ xa: dùng HTTPS và lớp kiểm soát truy cập (VPN, allowlist IP, basic auth ở proxy).

## Xử lý sự cố

| Triệu chứng | Cách xử lý |
|---|---|
| `401` | Sai hoặc thiếu `Authorization: Bearer ...` |
| Không tìm thấy trình duyệt | Đặt `MUSE2API_CHROMIUM` trỏ đúng `chrome.exe` |
| Tài khoản báo lỗi đăng nhập | Cookie hết hạn: lấy lại cookie và cập nhật ở `/admin` |
| Video quá lâu | Tăng `MUSE2API_VIDEO_TIMEOUT`; tài khoản Muse có thể giới hạn số tác vụ đồng thời |
| Lỗi "media handle" | Server tự thử lại một lần trong chat mới |
| Muse đổi giao diện nên hỏng | Chạy `tools/verify_engine_selectors.py` để xem selector nào cần cập nhật trong `engine.py` |

## Giấy phép

[MIT](LICENSE), dựa trên [czg86389-hub/muse2api](https://github.com/czg86389-hub/muse2api). Khi phân phối lại, hãy giữ nguyên giấy phép và ghi nhận upstream.
