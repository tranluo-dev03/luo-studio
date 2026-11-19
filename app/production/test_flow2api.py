"""Test nhanh flow2api (lõi Veo) trước khi cắm vào gen_video.py.

Cách dùng (chạy sau khi server flow2api đã lên và đã nạp tài khoản Google):
    python test_flow2api.py                       # kiểm tra kết nối + liệt kê model
    python test_flow2api.py --video "một chú mèo chạy trên bãi cỏ"           # text -> video dọc 4s
    python test_flow2api.py --video "..." --image anh.png                    # ảnh -> video (khung đầu)
    python test_flow2api.py --video "..." --model veo-3.1-fast-i2v-6s-portrait --image anh.png

Khoá API đọc từ biến FLOW2API_KEY hoặc D:\\Develop\\Nexax\\flow2api\\config\\setting.toml (không in ra).
In nguyên văn các dòng stream để biết link video nằm ở đâu.
"""
import argparse, base64, json, mimetypes, os, re, sys, time, urllib.request, urllib.error

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FLOW_DIR = os.environ.get("FLOW2API_DIR", r"D:\Develop\Nexax\flow2api")


def read_key():
    k = os.environ.get("FLOW2API_KEY", "").strip()
    if k:
        return k
    try:
        for line in open(os.path.join(FLOW_DIR, "config", "setting.toml"), encoding="utf-8"):
            m = re.match(r'\s*api_key\s*=\s*"([^"]+)"', line)
            if m:
                return m.group(1)
    except OSError:
        pass
    sys.exit("Không tìm thấy API key (đặt FLOW2API_KEY hoặc kiểm tra setting.toml)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8000")
    ap.add_argument("--video", help="prompt để gen video")
    ap.add_argument("--image", help="ảnh khung đầu (i2v)")
    ap.add_argument("--model", help="mặc định: t2v 4s dọc, hoặc i2v 4s dọc nếu có --image")
    ap.add_argument("--out", default="flow2api_test.mp4")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    key = read_key()
    hdr = {"Authorization": f"Bearer {key}"}

    def call(path, body=None):
        r = urllib.request.Request(a.url + path, data=json.dumps(body).encode() if body else None, headers={**hdr, "Content-Type": "application/json"})
        return urllib.request.urlopen(r, timeout=a.timeout)

    print("health:", urllib.request.urlopen(a.url + "/health", timeout=10).read().decode())
    try:
        models = json.loads(call("/v1/models").read().decode())
        ids = [m["id"] for m in models.get("data", [])]
        print(f"{len(ids)} model; ví dụ video dọc:", [i for i in ids if "portrait" in i][:6])
    except urllib.error.HTTPError as e:
        sys.exit(f"/v1/models lỗi {e.code}: {e.read().decode(errors='replace')[:200]}")
    if not a.video:
        return

    model = a.model or ("veo-3.1-fast-i2v-4s-portrait" if a.image else "veo-3.1-fast-4s-portrait")
    content = [{"type": "text", "text": a.video}]
    if a.image:
        mime = mimetypes.guess_type(a.image)[0] or "image/png"
        b64 = base64.b64encode(open(a.image, "rb").read()).decode()
        content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}})
    body = {"model": model, "stream": True, "messages": [{"role": "user", "content": content}]}
    print("gọi model:", model)
    t0, text = time.time(), ""
    try:
        resp = call("/v1/chat/completions", body)
    except urllib.error.HTTPError as e:
        sys.exit(f"Lỗi {e.code}: {e.read().decode(errors='replace')[:500]}")
    for raw in resp:
        line = raw.decode(errors="replace").strip()
        if not line.startswith("data:"):
            continue
        d = line[5:].strip()
        if d == "[DONE]":
            break
        try:
            ch = json.loads(d)["choices"][0]
            piece = (ch.get("delta") or {}).get("content") or (ch.get("delta") or {}).get("reasoning_content") or ""
        except Exception:
            print("  ?", d[:200])
            continue
        if piece:
            text += piece
            print(f"  [{time.time() - t0:5.0f}s] {piece.strip()[:160]}")
    m = re.search(r"<video[^>]+src=['\"](.*?)['\"]", text) or re.search(r"https?://\S+\.mp4\S*", text)
    if not m:
        sys.exit("Không thấy link video trong kết quả (xem các dòng ở trên)")
    url = m.group(1) if m.lastindex else m.group(0)
    print("link video:", url)
    open(a.out, "wb").write(urllib.request.urlopen(url.rstrip(")'\""), timeout=300).read())
    print("đã lưu", os.path.abspath(a.out))


if __name__ == "__main__":
    main()
