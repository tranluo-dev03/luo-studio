"""账号池与任务存储（JSON 落盘，原子写）。"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import uuid

_LOCK = threading.RLock()

# 决定账号生死的核心 cookie（与 engine.ESSENTIAL_COOKIES 保持一致）。
# Từ 10/2026 Muse không còn đặt hatch_gw / hatch_vml cho mọi phiên: có thì dùng, không có không coi là thiếu.
ESSENTIAL_COOKIES = ("hatch_sess", "hatch_native_auth_device")
EXPIRY_COOKIES = ("hatch_sess", "hatch_gw", "hatch_vml", "hatch_native_auth_device")

# Lịch sử tác vụ: giữ N tác vụ mới nhất; tác vụ đã xong chỉ lưu 1500 ký tự prompt.
# (Trước 1.2.0 mỗi lần cập nhật tiến độ ghi lại TOÀN BỘ tasks.json — 31 MB trên máy thật, ~0,25 s CPU mỗi lần,
# 0,6 s/lần cho mỗi việc đang chạy, giữ khoá chung — làm chậm cả các luồng đang điều khiển trình duyệt.)
TASK_KEEP = 600
TASK_PROMPT_KEEP = 1500
FLUSH_EVERY = 2.0


def _is_pos(v) -> bool:
    try:
        return int(v) > 0
    except (TypeError, ValueError):
        return False


# hatch_vml 固定约 2 天，且不因使用而延长 —— 它就是决定账号寿命的那条 cookie。
# 实测对照：生成前后 synced_at 变了、也捞到新 cookie，但 4 条核心 cookie 的
# expires 一动不动。所以拿不到 hatch_vml 的 expires 时，按「导入时间 + 2 天」估算，
# 而不是退回到 hatch_native_auth_device 的 30 天（那个不决定生死，会误导用户）。
VML_TTL = 2 * 86400

# Muse 限制每个账号每天生成的视频数（约 100 条）。统计当天（本机时间 00:00 起）成功生成的视频数，
# 过了零点归零，供界面提醒（只提醒，不拦截）。
def _day(ts: float | None = None) -> str:
    return time.strftime("%Y-%m-%d", time.localtime(ts))


def min_expiry(cookies_exp: dict | None) -> int | None:
    """核心 cookie 里最早过期的那个（通用兜底，不区分哪条决定寿命）。"""
    if not cookies_exp:
        return None
    vals = []
    for name in EXPIRY_COOKIES:
        v = cookies_exp.get(name)
        try:
            v = int(v)
        except (TypeError, ValueError):
            continue
        if v > 0:
            vals.append(v)
    if not vals:
        for v in cookies_exp.values():
            try:
                v = int(v)
            except (TypeError, ValueError):
                continue
            if v > 0:
                vals.append(v)
    return min(vals) if vals else None


def account_expiry(cookies_exp: dict | None,
                   base_ts: int | None = None) -> int | None:
    """账号实际失效时间。

    优先级：
      1) hatch_vml 的真实 expires（最准）；
      2) 拿不到就用 base_ts(导入/同步时刻) + VML_TTL 估算 —— 因为寿命就是 2 天；
      3) 都没有再退回核心 cookie 最早过期。
    """
    ce = cookies_exp or {}
    vml = ce.get("hatch_vml")
    if _is_pos(vml):
        return int(vml)
    if base_ts:
        return int(base_ts) + VML_TTL
    return min_expiry(ce)


def _read(path: str, default):
    if not os.path.isfile(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return default


def _write(path: str, obj, indent: int | None = 1):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=indent)
        for _ in range(5):   # Windows: file đích đang bị đọc (antivirus, trình xem) thì đổi tên lỗi tạm thời
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                time.sleep(0.2)
        else:
            os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _slim_task(t: dict) -> dict:
    """Bản lưu đĩa của một tác vụ: tác vụ đã xong không cần prompt đầy đủ (gửi Muse rồi)."""
    if t.get("status") in ("queued", "processing"):
        return t
    out = dict(t)
    out.pop("api_prompt", None)
    p = out.get("prompt")
    if isinstance(p, str) and len(p) > TASK_PROMPT_KEEP:
        out["prompt"] = p[:TASK_PROMPT_KEEP] + "…"
    return out


class Store:
    def __init__(self, cfg):
        self.cfg = cfg
        self.accounts: list[dict] = _read(cfg.accounts_file, [])
        for a in self.accounts:
            ce = a.get("cookies_exp") or {}
            if _is_pos(ce.get("hatch_vml")):
                a["expires_at"] = int(ce["hatch_vml"])
        self.tasks: dict[str, dict] = _read(cfg.tasks_file, {})
        self._prune_tasks()
        self._tasks_dirty = threading.Event()
        self._flusher = threading.Thread(target=self._flush_loop, name="store-flush", daemon=True)
        self._flusher.start()
        self._backfill_video_log()

    # ---------- ghi tasks.json theo lô ----------
    def _prune_tasks(self):
        if len(self.tasks) <= TASK_KEEP:
            return
        keep = sorted(self.tasks.values(), key=lambda t: t.get("created_at") or 0, reverse=True)[:TASK_KEEP]
        active = {k: v for k, v in self.tasks.items() if v.get("status") in ("queued", "processing")}
        self.tasks = {t["id"]: t for t in keep}
        self.tasks.update(active)

    def _mark_tasks_dirty(self):
        self._tasks_dirty.set()

    def _flush_loop(self):
        while True:
            self._tasks_dirty.wait()
            time.sleep(FLUSH_EVERY)
            self._tasks_dirty.clear()
            try:
                self.flush_tasks()
            except Exception:  # noqa: BLE001
                self._tasks_dirty.set()
                time.sleep(5)

    def flush_tasks(self):
        with _LOCK:
            self._prune_tasks()
            snap = {k: _slim_task(v) for k, v in self.tasks.items()}
        _write(self.cfg.tasks_file, snap, indent=None)

    def _backfill_video_log(self):
        """旧账号还没有当天视频计数：从任务记录里补出今天成功的视频数（只补一次）。"""
        todo = [a for a in self.accounts if "video_day" not in a]
        if not todo:
            return
        today = _day()
        for a in todo:
            n = 0
            for t in self.tasks.values():
                try:
                    c = int(t.get("created_at") or 0)
                except (TypeError, ValueError):
                    continue
                if (t.get("kind") == "video" and t.get("status") == "completed"
                        and t.get("account") == a["id"] and _day(c) == today):
                    n += 1
            for k in ("video_log", "video_last"):
                a.pop(k, None)
            a["video_day"], a["video_count"] = today, n
        _write(self.cfg.accounts_file, self.accounts)

    def record_video(self, aid: str):
        """记一次视频生成成功；换了一天就从 1 重新计。"""
        with _LOCK:
            today = _day()
            for a in self.accounts:
                if a["id"] == aid:
                    a["video_count"] = (a.get("video_count") or 0) + 1 if a.get("video_day") == today else 1
                    a["video_day"] = today
            _write(self.cfg.accounts_file, self.accounts)

    # ---------- 账号 ----------
    def add_account(self, cookies: dict, label: str = "",
                    cookies_exp: dict | None = None) -> dict:
        with _LOCK:
            aid = uuid.uuid4().hex[:12]
            exp = {k: int(v) for k, v in (cookies_exp or {}).items()
                   if _is_pos(v)}
            now = int(time.time())
            acc = {"id": aid, "label": label or aid, "cookies": cookies,
                   "cookies_exp": exp, "expires_at": account_expiry(exp, now),
                   "expiry_anchor": None,
                   "enabled": True, "created_at": now,
                   "last_used": None, "last_keepalive": None, "use_count": 0,
                   "ok": None, "note": "", "synced_at": None}
            self.accounts.append(acc)
            _write(self.cfg.accounts_file, self.accounts)
            return acc

    def list_accounts(self) -> list[dict]:
        out = []
        for a in self.accounts:
            item = {k: v for k, v in a.items() if k not in ("cookies", "mail")}
            # Hộp thư tự lấy OTP: chỉ lộ địa chỉ, không trả refresh_token ra ngoài
            item["mail_email"] = (a.get("mail") or {}).get("email") or ""
            # 计数只算今天的：过了零点还没生成新视频 -> 显示 0（下次生成时 record_video 也从 1 重计）
            item["video_count"] = (a.get("video_count") or 0) if a.get("video_day") == _day() else 0
            ce = a.get("cookies_exp") or {}
            if _is_pos(ce.get("hatch_vml")):
                item["expires_at"] = int(ce["hatch_vml"])
            item["cookie_count"] = len(a.get("cookies", {}))
            item["essential_ok"] = all(
                a.get("cookies", {}).get(n) for n in ESSENTIAL_COOKIES)
            # 有效期是 hatch_vml 的实测 expires，还是按「2 天寿命」推算的
            item["expires_estimated"] = not _is_pos(ce.get("hatch_vml"))
            out.append(item)
        return out

    def delete_account(self, aid: str) -> bool:
        with _LOCK:
            n = len(self.accounts)
            self.accounts = [a for a in self.accounts if a["id"] != aid]
            _write(self.cfg.accounts_file, self.accounts)
            return len(self.accounts) != n

    def pick_account(self, preferred_id: str | None = None, rotate: bool = True,
                     force_rotate: bool = False, exclude_id: str | None = None,
                     exclude_ids: set[str] | list[str] | None = None) -> dict | None:
        """选择可用账号：优先复用当前已预热的健康账号（减少切号重连耗时），每满 15 次或遇错自动轮转。
        exclude_ids: 需要排除的账号 ID 集合（例如正在被其他并发线程占用的账号）。"""
        with _LOCK:
            live = [a for a in self.accounts if a.get("enabled", True) and a.get("cookies")]
            if not live:
                return None
            blocked = set(exclude_ids or [])
            if exclude_id:
                blocked.add(exclude_id)
            if blocked:
                available = [a for a in live if a["id"] not in blocked]
                if available:
                    live = available
                elif exclude_ids is not None:
                    # 并发模式下要求避开所有繁忙账号，但当前无剩余空闲账号
                    return None
                elif len(live) > 1:
                    live = [a for a in live if a["id"] != exclude_id] or live
            if preferred_id and not force_rotate:
                for a in live:
                    if a["id"] == preferred_id and a.get("ok") is not False:
                        sticky_n = getattr(self, "_sticky_count", 0) if getattr(self, "_sticky_id", None) == preferred_id else 0
                        if not rotate or sticky_n < 15:
                            self._sticky_id = preferred_id
                            self._sticky_count = sticky_n + 1
                            a["last_used"] = time.time()
                            a["use_count"] = a.get("use_count", 0) + 1
                            _write(self.cfg.accounts_file, self.accounts)
                            return a
            healthy = [a for a in live if a.get("ok") is not False]
            candidates = healthy if healthy else live
            candidates.sort(key=lambda a: (a.get("last_used") or 0.0, a.get("use_count") or 0))
            acc = candidates[0]
            self._sticky_id = acc["id"]
            self._sticky_count = 1
            acc["last_used"] = time.time()
            acc["use_count"] = acc.get("use_count", 0) + 1
            _write(self.cfg.accounts_file, self.accounts)
            return acc

    def touch_keepalive(self, aid: str, ok: bool | None = True, note: str = ""):
        """ok=None 仅记录未确认的检测；保留上次账号状态、成功保活时间和有效期。"""
        with _LOCK:
            now_ts = int(time.time())
            for a in self.accounts:
                if a["id"] == aid:
                    if ok is not None:
                        a["ok"] = ok
                    if ok is True:
                        a["last_keepalive"] = now_ts
                        # ponytail: 只信实际 Cookie 到期时间或原导入锚点，不凭检测成功虚推 48h。
                        a["expires_at"] = account_expiry(
                            a.get("cookies_exp"), a.get("expiry_anchor") or a.get("created_at"))
                    if note:
                        a["note"] = note[:300]
                    a["checked_at"] = now_ts
            _write(self.cfg.accounts_file, self.accounts)

    def mark(self, aid: str, ok: bool, note: str = ""):
        with _LOCK:
            for a in self.accounts:
                if a["id"] == aid:
                    a["ok"] = ok
                    a["note"] = note[:300]
                    a["checked_at"] = int(time.time())
            _write(self.cfg.accounts_file, self.accounts)

    def get_account(self, aid: str) -> dict | None:
        for a in self.accounts:
            if a["id"] == aid:
                return a
        return None

    def update_account(self, aid: str, **kw) -> dict | None:
        """更新标签 / 启用状态 / cookies / 有效期等；值为 None 的字段跳过。

        传了 cookies_exp 会自动重算 expires_at，不用调用方自己算。
        估算锚点 expiry_anchor 的维护规则（避免有效期被反复虚推）：
          - 读到了 hatch_vml 的真实 expires  -> 清空锚点，直接用真值；
          - 读不到且锚点为空                -> 把锚点钉在当下（只钉一次）；
          - 补入全新会话 cookie（重登）      -> 调用方显式传 expiry_anchor=now 重置。
        """
        with _LOCK:
            for a in self.accounts:
                if a["id"] == aid:
                    for k, v in kw.items():
                        if v is not None:
                            a[k] = v
                    if "cookies_exp" in kw and kw["cookies_exp"] is not None:
                        ce = a["cookies_exp"]
                        if _is_pos(ce.get("hatch_vml")):
                            a["expiry_anchor"] = None
                        elif not a.get("expiry_anchor"):
                            a["expiry_anchor"] = int(time.time())
                        a["expires_at"] = account_expiry(
                            ce, a.get("expiry_anchor") or a.get("created_at"))
                    _write(self.cfg.accounts_file, self.accounts)
                    return a
        return None

    def stats(self) -> dict:
        now = int(time.time())
        total = len(self.accounts)
        enabled = sum(1 for a in self.accounts if a.get("enabled", True))
        bad = sum(1 for a in self.accounts
                  if a.get("enabled", True) and a.get("ok") is False)
        healthy = sum(1 for a in self.accounts
                      if a.get("enabled", True) and a.get("ok") is True)
        expiring = sum(1 for a in self.accounts
                       if a.get("enabled", True)
                       and a.get("expires_at")
                       and a["expires_at"] - now < 3 * 86400)
        expired = sum(1 for a in self.accounts
                      if a.get("enabled", True)
                      and a.get("expires_at") and a["expires_at"] <= now)
        return {"total": total, "enabled": enabled, "disabled": total - enabled,
                "healthy": healthy, "error": bad,
                "expiring": expiring, "expired": expired}

    # ---------- 任务 ----------
    def create_task(self, kind: str, prompt: str) -> dict:
        with _LOCK:
            tid = "task_" + uuid.uuid4().hex[:20]
            t = {"id": tid, "object": "task", "kind": kind, "prompt": prompt,
                 "status": "queued", "created_at": int(time.time()),
                 "updated_at": int(time.time()), "result": None, "error": None}
            self.tasks[tid] = t
        self._mark_tasks_dirty()
        return t

    def update_task(self, tid: str, **kw):
        """Cập nhật trong bộ nhớ (API đọc từ đây); luồng nền ghi đĩa sau tối đa ~2 s."""
        with _LOCK:
            t = self.tasks.get(tid)
            if not t:
                return None
            t.update(kw)
            t["updated_at"] = int(time.time())
        self._mark_tasks_dirty()
        return t

    def get_task(self, tid: str) -> dict | None:
        return self.tasks.get(tid)

    def list_tasks(self, limit: int = 50) -> list[dict]:
        items = sorted(self.tasks.values(),
                       key=lambda t: t.get("created_at") or 0, reverse=True)
        return items[:limit]

    def delete_task(self, tid: str) -> bool:
        with _LOCK:
            if tid not in self.tasks:
                return False
            del self.tasks[tid]
        self._mark_tasks_dirty()
        return True

    def clear_tasks(self, keep: int = 0) -> int:
        with _LOCK:
            items = sorted(self.tasks.values(),
                           key=lambda t: t.get("created_at") or 0, reverse=True)
            keep_ids = {t["id"] for t in items[:keep]}
            removed = len(self.tasks) - len(keep_ids)
            self.tasks = {k: v for k, v in self.tasks.items() if k in keep_ids}
        self._mark_tasks_dirty()
        return max(0, removed)
