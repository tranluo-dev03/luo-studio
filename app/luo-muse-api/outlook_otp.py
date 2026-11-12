"""Đọc mã OTP Muse từ hộp thư Outlook / Hotmail bằng refresh_token + client_id (không cần mật khẩu).

Tài khoản bán sẵn thường có dạng:  email|password|refresh_token|client_id
- refresh_token + client_id đổi lấy access token ở Microsoft (OAuth), rồi đọc thư qua IMAP (XOAUTH2).
- Microsoft có thể trả refresh_token MỚI mỗi lần đổi: hàm get_access_token trả kèm để lưu lại (token cũ vẫn dùng
  được một thời gian, nhưng giữ token mới thì không bị hết hạn sau ~90 ngày).

Chỉ dùng thư viện chuẩn.
"""
from __future__ import annotations

import email
import email.header
import email.utils
import imaplib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
IMAP_HOST = "outlook.office365.com"
SCOPES = ("https://outlook.office.com/IMAP.AccessAsUser.All offline_access",)
FOLDERS = ("INBOX", "Junk")
SENDER_HINT = re.compile(r"muse|meta|facebook", re.I)
CODE_RE = re.compile(r"(?<![\d#&])(\d{6})(?![\d])")


class MailAuthError(RuntimeError):
    """refresh_token hết hạn / bị thu hồi (vd. đã đổi mật khẩu Outlook) hoặc client_id sai."""


def parse_line(line: str) -> dict | None:
    """'email|password|refresh_token|client_id' -> dict. Trả None nếu không đủ refresh_token + client_id."""
    parts = [p.strip() for p in str(line or "").strip().split("|")]
    if len(parts) < 4 or "@" not in parts[0]:
        return None
    em, pw, rt, cid = parts[0], parts[1], parts[2], parts[3]
    if not rt or not re.fullmatch(r"[0-9a-fA-F-]{36}", cid):
        return None
    return {"email": em, "refresh_token": rt, "client_id": cid}


def get_access_token(mail: dict) -> tuple[str, str | None]:
    """Trả (access_token, refresh_token_mới_hoặc_None)."""
    last = ""
    for scope in SCOPES:
        data = urllib.parse.urlencode({"client_id": mail["client_id"], "grant_type": "refresh_token",
                                       "refresh_token": mail["refresh_token"], "scope": scope}).encode()
        try:
            with urllib.request.urlopen(TOKEN_URL, data, timeout=25) as r:
                d = json.loads(r.read())
            rt = d.get("refresh_token")
            return d["access_token"], (rt if rt and rt != mail["refresh_token"] else None)
        except urllib.error.HTTPError as e:
            try:
                last = json.loads(e.read()).get("error_description", "")
            except Exception:  # noqa: BLE001
                last = f"HTTP {e.code}"
    raise MailAuthError("Microsoft từ chối refresh_token (hết hạn, đã đổi mật khẩu Outlook, hoặc client_id sai): "
                        + last.split("\r\n")[0][:200])


def _imap(mail: dict, access: str) -> imaplib.IMAP4_SSL:
    m = imaplib.IMAP4_SSL(IMAP_HOST, 993, timeout=25)
    auth = f"user={mail['email']}\x01auth=Bearer {access}\x01\x01"
    try:
        m.authenticate("XOAUTH2", lambda _: auth.encode())
    except imaplib.IMAP4.error as exc:
        raise MailAuthError(f"Không đăng nhập được IMAP Outlook: {exc}") from None
    return m


def _text(msg: email.message.Message) -> str:
    out = []
    for part in msg.walk() if msg.is_multipart() else [msg]:
        if part.get_content_maintype() != "text":
            continue
        try:
            raw = part.get_payload(decode=True) or b""
            t = raw.decode(part.get_content_charset() or "utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue
        if part.get_content_subtype() == "html":
            t = re.sub(r"(?is)<(style|script).*?</\1>", " ", t)
            t = re.sub(r"(?s)<[^>]+>", " ", t)
        out.append(t)
    return re.sub(r"\s+", " ", " ".join(out))


def _subject(msg) -> str:
    try:
        return str(email.header.make_header(email.header.decode_header(msg.get("Subject", ""))))
    except Exception:  # noqa: BLE001
        return msg.get("Subject", "")


def _recent(m: imaplib.IMAP4_SSL, folder: str, n: int = 15) -> list[bytes]:
    """UID của n thư mới nhất trong thư mục (rỗng nếu thư mục không có / không mở được)."""
    try:
        typ, _ = m.select(folder, readonly=True)
    except imaplib.IMAP4.error:
        return []
    if typ != "OK":
        return []
    typ, data = m.uid("SEARCH", None, "ALL")
    return (data[0] or b"").split()[-n:] if typ == "OK" else []


def find_code(m: imaplib.IMAP4_SSL, since: float, ignore: set | None = None) -> str | None:
    """Tìm mã 6 số trong thư Muse/Meta MỚI nhất.

    ignore: tập (thư mục, uid) đã có trước khi bấm Continue -> bỏ qua hẳn, nên không bao giờ lấy nhầm mã cũ
    (mã cũ đã hết hạn / bị mã mới thay thế). Không có ignore thì chỉ nhận thư đến sau since (lệch đồng hồ 10 giây).
    """
    for folder in FOLDERS:
        for uid in reversed(_recent(m, folder)):
            if ignore is not None and (folder, uid) in ignore:
                continue
            typ, got = m.uid("FETCH", uid, "(RFC822)")
            if typ != "OK" or not got or not isinstance(got[0], tuple):
                continue
            msg = email.message_from_bytes(got[0][1])
            if ignore is None:
                try:
                    ts = email.utils.parsedate_to_datetime(msg.get("Date")).timestamp()
                except Exception:  # noqa: BLE001
                    ts = 0
                if ts and ts < since - 10:
                    continue
            frm, subj = msg.get("From", ""), _subject(msg)
            if not SENDER_HINT.search(frm + " " + subj):
                continue
            codes = CODE_RE.findall(subj + " " + _text(msg))
            if codes:
                return codes[0]
    return None


def snapshot(mail: dict, on_new_token=None) -> set:
    """Các thư đang có trong hộp thư (để wait_code bỏ qua). Gọi NGAY TRƯỚC khi yêu cầu Muse gửi mã."""
    access, new_rt = get_access_token(mail)
    if new_rt and on_new_token:
        on_new_token(new_rt)
    m = _imap(mail, access)
    try:
        return {(f, u) for f in FOLDERS for u in _recent(m, f, 30)}
    finally:
        try:
            m.logout()
        except Exception:  # noqa: BLE001
            pass


def wait_code(mail: dict, since: float, timeout: float = 180, cancel=None, on_new_token=None,
              ignore: set | None = None) -> str | None:
    """Đợi thư OTP Muse đến (không nằm trong ignore) và trả mã 6 số; hết thời gian trả None. Lỗi token -> MailAuthError."""
    access, new_rt = get_access_token(mail)
    if new_rt and on_new_token:
        on_new_token(new_rt)
    deadline = time.time() + timeout
    m = _imap(mail, access)
    try:
        while time.time() < deadline:
            if cancel is not None and cancel.is_set():
                return None
            try:
                code = find_code(m, since, ignore)
            except (imaplib.IMAP4.abort, OSError):
                m = _imap(mail, access)
                code = None
            if code:
                return code
            time.sleep(4)
    finally:
        try:
            m.logout()
        except Exception:  # noqa: BLE001
            pass
    return None


def check(mail: dict) -> dict:
    """Thử token + IMAP (dùng cho nút kiểm tra). Trả {"ok", "message", "refresh_token"?}."""
    try:
        access, new_rt = get_access_token(mail)
        m = _imap(mail, access)
        m.select("INBOX", readonly=True)
        m.logout()
        return {"ok": True, "message": "Đọc được hộp thư", "refresh_token": new_rt}
    except MailAuthError as exc:
        return {"ok": False, "message": str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "message": f"Lỗi mạng khi đọc hộp thư: {exc}"[:300]}
