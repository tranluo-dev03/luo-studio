"""极简 Chrome DevTools Protocol 客户端（仅依赖 websocket-client / requests）。"""
from __future__ import annotations

import json
import threading
import time

import requests
import websocket


class CDPError(RuntimeError):
    pass


class CDP:
    def __init__(self, ws_url: str, timeout: float = 90.0, max_size: int = 256 << 20):
        self.ws = websocket.create_connection(ws_url, timeout=timeout, max_size=max_size)
        self.timeout = timeout
        self._id = 0
        self._lock = threading.Lock()
        self.closed = False

    @property
    def alive(self) -> bool:
        return not self.closed and bool(getattr(self.ws, "connected", False))

    def send(self, method: str, params: dict | None = None, timeout: float | None = None):
        with self._lock:
            if self.closed:
                raise CDPError(f"{method}: kết nối CDP đã đóng")
            self._id += 1
            mid = self._id
            try:
                self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            except Exception as exc:  # noqa: BLE001
                self.closed = True
                raise CDPError(f"{method}: mất kết nối CDP ({type(exc).__name__})") from None
            deadline = time.time() + (timeout or self.timeout)
            while time.time() < deadline:
                try:
                    self.ws.settimeout(max(0.5, min(30.0, deadline - time.time())))
                    raw = self.ws.recv()
                except websocket.WebSocketTimeoutException:
                    continue
                except (websocket.WebSocketConnectionClosedException, ConnectionError, OSError) as exc:
                    # Trước đây mọi lỗi đều "continue": socket đã chết thì quay vòng tới hết thời gian chờ.
                    self.closed = True
                    raise CDPError(f"{method}: mất kết nối CDP ({type(exc).__name__})") from None
                except Exception:  # noqa: BLE001
                    continue
                try:
                    msg = json.loads(raw)
                except Exception:  # noqa: BLE001
                    continue
                if msg.get("id") == mid:
                    if "error" in msg:
                        raise CDPError(f"{method}: {msg['error']}")
                    return msg
            raise TimeoutError(f"CDP {method} 超时")

    def js(self, expr: str, await_promise: bool = False, timeout: float | None = None):
        r = self.send("Runtime.evaluate",
                      {"expression": expr, "returnByValue": True,
                       "awaitPromise": await_promise}, timeout)
        res = r.get("result", {}).get("result", {})
        if "value" in res:
            return res["value"]
        return r.get("result")

    def evaluate(self, expr: str, await_promise: bool = False, timeout: float | None = None):
        """Như js() nhưng lỗi JS -> CDPError; không có giá trị -> None."""
        r = self.send("Runtime.evaluate",
                      {"expression": expr, "returnByValue": True,
                       "awaitPromise": await_promise}, timeout)
        res = r.get("result", {})
        if "exceptionDetails" in res:
            d = res["exceptionDetails"]
            raise CDPError("JS: " + str((d.get("exception") or {}).get("description") or d.get("text") or d)[:300])
        return (res.get("result") or {}).get("value")

    def pump(self, seconds: float, on_event=None, sock_timeout: float = 2.0):
        """在 seconds 秒内持续读取事件，交给回调处理。"""
        end = time.time() + seconds
        self.ws.settimeout(sock_timeout)
        while time.time() < end:
            try:
                ev = json.loads(self.ws.recv())
            except Exception:  # noqa: BLE001
                continue
            if on_event and "method" in ev:
                on_event(ev)

    def close(self):
        self.closed = True
        try:
            self.ws.close()
        except Exception:  # noqa: BLE001
            pass


def http_json(url: str, timeout: float = 5.0):
    return requests.get(url, timeout=timeout).json()
