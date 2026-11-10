"""Đẩy kịch bản + biến thể hiện tại vào đúng loại dự án và dự án đã có trong Studio (không tạo bản mới, Studio tự tải ảnh refs).
Chạy khi Studio đang mở:  runtime\\python.exe SAMPLE\\chia-tren-duoi-bengali\\cong-cu\\cap_nhat_studio.py"""
import json
import os
import sys
import urllib.request

for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TID, PID = "Chia-tren-duoi-Bengali-4a9d", "oder-5---Supernova-Bengali-08be"
URL = json.load(open(os.path.join(ROOT, "userdata", "running.json"), encoding="utf-8"))["studio_url"].rstrip("/")


def api(method, path, body=None):
    req = urllib.request.Request(URL + path, data=None if body is None else json.dumps(body).encode("utf-8"), method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8") or "null")


script = open(os.path.join(HERE, "..", "KICH-BAN-CHIA-TREN-DUOI-BENGALI.txt"), encoding="utf-8").read()
new = json.load(open(os.path.join(HERE, "..", "BIEN-THE-CHIA-TREN-DUOI-BENGALI.json"), encoding="utf-8"))
print("loại dự án:", api("PUT", f"/api/types/{TID}", {"script": script}).get("id"))
old = {v["name"]: v for v in api("GET", f"/api/projects/{PID}")["variants"]}
variants = [{**old.get(v["name"], {}), **v} for v in new]
print("dự án:", api("PUT", f"/api/projects/{PID}", {"variants": variants}))
for v in api("GET", f"/api/projects/{PID}")["variants"]:
    print(v["name"], "refs:", {k: [(i.get("file"), i.get("error")) for i in items] for k, items in (v.get("refs") or {}).items()}, "| lượt:", len(v["LUOT"]))
