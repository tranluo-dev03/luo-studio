"""Mọi hiểu biết về trang muse.ai nằm ở file này (selector, đoạn JS chạy trong trang, page helper).

Muse đổi giao diện thì thường chỉ phải sửa file này. Đoạn JS trả giá trị JSON và không ném lỗi ra ngoài
(lỗi được báo trong kết quả).

Page helper `window.__luo` (giai đoạn 4, LUO 1.2.0): thay vì đọc DOM, gọi thẳng RPC nội bộ mà chính trang dùng,
qua `__hatchEarlyGatewayRuntimeState.activeRuntime.getSnapshot().sendRequest(method, params)` (kênh Noise tới VM
của tài khoản, đã giải mã sẵn trong trang). Các method đã kiểm chứng trên trang thật 2026-11-06:
  sessions.get {id}                  -> {status, title, updated_at_ms, ...}  (status: completed / running / ...)
  chat.history {session_id, limit}   -> {chat_events: [...]}; ảnh/video sinh ra nằm trong event `delta.presentation`
                                        với đường dẫn `sandbox://workspace/...` (payload.data.images[].path, image_path, ...)
  fs.raw {path}                      -> Blob (file gốc trên VM, kênh media, có Range)
  egress.approvals {} / egress.approval.decide {approval_id, decision}
Gửi tin vẫn đi qua ô soạn tin của trang (giữ nguyên đường upload ảnh tham chiếu của trang).
"""
from __future__ import annotations

import json

INPUT = "textarea"
AGENT_BUBBLE = 'div[class*="hatch-agent-bubble-bg"]'
USER_BUBBLE = 'div[class*="chat-user-bubble"]'
ANY_BUBBLE = 'div[class*="hatch-chat-groupable-bubble"]'
ATTACHMENT = '[data-testid^="hatch-chat-attachment-presentation-"]'
STOP_BUTTON = '[data-testid="hatch-composer-stop-button"],button[aria-label*="Stop" i],button[aria-label*="停止"]'
APPROVAL_CARD = '[data-testid="hatch-inline-approval-card"]'
FILE_INPUT = 'input[type="file"]'
SETTINGS_DOCK = '[data-testid="hatch-dock-more"]'

LOGIN_HINTS = ("log in", "sign in", "create an account", "use another account", "登录")
STALL_HINTS = ("Still sending", "Connecting...", "Delivery not confirmed")


def q(value) -> str:
    """JSON-quote một giá trị Python để chèn an toàn vào JS."""
    return json.dumps(value, ensure_ascii=False)


# Ô soạn tin của trang mới không còn <form> bao quanh: tìm khung soạn tin bằng cách đi lên từ textarea tới tổ tiên
# đầu tiên có chứa input[type=file] (giao diện cũ có form vẫn khớp).
COMPOSER_JS = """function(){var ta=document.querySelector('textarea');if(!ta)return null;var e=ta;
for(var i=0;i<12&&e;i++){if(e.querySelector&&e.querySelector('input[type="file"]'))return e;e=e.parentElement;}
var ov=document.querySelector('[data-testid="hatch-composer-placeholder-overlay"]');return ov?(ov.closest('form')||ov.parentElement):null}"""

PAGE_HELPER = r"""
(() => {
  if (window.__luo && window.__luo.v === 5) return true;
  const VID = /\.(mp4|webm|mov|m4v)$/i, IMG = /\.(webp|png|jpe?g|gif|avif)$/i;
  const MEDIA_RE = /(?:sandbox:\/\/)?(workspace\/[^\s"'()<>\]\[]+?\.(?:mp4|webm|mov|m4v|webp|png|jpe?g|gif|avif))/ig;
  const norm = (p) => String(p || '').replace(/^sandbox:\/\//, '').replace(/^\/+/, '');
  const kindOf = (p, mime) => (VID.test(p) || /^video\//.test(mime || '')) ? 'video' : ((IMG.test(p) || /^image\//.test(mime || '')) ? 'image' : 'other');
  const rt = () => { try { return window.__hatchEarlyGatewayRuntimeState.activeRuntime.getSnapshot(); } catch (e) { return null; } };
  const call = async (method, params) => { const s = rt(); if (!s || typeof s.sendRequest !== 'function') throw new Error('no-runtime'); return await s.sendRequest(method, params || {}); };
  const collect = (o, out, depth) => {
    if (o == null || depth > 7) return;
    if (typeof o === 'string') { let m; MEDIA_RE.lastIndex = 0; while ((m = MEDIA_RE.exec(o))) out.push({path: norm(m[1])}); return; }
    if (Array.isArray(o)) { for (const x of o) collect(x, out, depth + 1); return; }
    if (typeof o === 'object') {
      if (typeof o.path === 'string' && /workspace\//.test(o.path)) out.push({path: norm(o.path), mime: o.mime || o.mime_type || null,
        bytes: o.byte_len || o.size || o.bytes || null, w: o.width || null, h: o.height || null, label: o.label || null});
      for (const k of Object.keys(o)) if (k !== 'path') collect(o[k], out, depth + 1);
    }
  };
  const summarize = (ev) => {
    const p = ev.payload || {};
    const role = ev.role || p.role || '';
    const media = [];
    if (role !== 'user') collect(p, media, 0);
    const seen = new Set(); const uniq = [];
    for (const m of media) { if (!m.path || seen.has(m.path)) continue; seen.add(m.path); m.kind = kindOf(m.path, m.mime); if (m.kind !== 'other') uniq.push(m); }
    const res = []; collect(ev.resources || [], res, 0); collect(p.attachments || p.items || [], res, 0);
    return {seq: ev.seq || p.seq || 0, role, name: ev.event_name || '', at: ev.occurred_at_ms || 0,
            text: String(ev.display_text || p.content || '').slice(0, 1500), status: p.status || null,
            media: uniq, uploads: role === 'user' ? res.map(r => r.path) : []};
  };
  const pool = async (items, n, fn) => { const out = []; let i = 0;
    await Promise.all(Array.from({length: Math.min(n, items.length)}, async () => { while (i < items.length) { const it = items[i++]; out.push(await fn(it)); } }));
    return out; };
  window.__luo = {
    v: 5,
    // ---- dọn tài khoản (hội thoại cũ, media cũ trên VM) ----
    listSessions: async (maxPages) => {
      const all = []; let cursor = null, pages = 0;
      do { const p = {include_peer_sidechats: true, limit: 200}; if (cursor) p.cursor = cursor;
           const r = await call('sessions.list', p); const a = (r && r.sessions) || []; pages++;
           for (const x of a) all.push({id: x.session_id, created: x.created_at_ms || 0, updated: x.updated_at_ms || 0,
             pinned: !!x.pinned, primary: !!x.is_primary, archived: !!x.archived, status: x.status || '', thread: x.is_thread !== false});
           cursor = r && r.next_cursor && a.length ? r.next_cursor : null; } while (cursor && pages < (maxPages || 30));
      return all;
    },
    // File media mà mỗi hội thoại nhắc tới (kết quả của trợ lý, bản đã xử lý, tham chiếu tải lên): {sid: [paths]}.
    threadMedia: async (ids) => {
      const out = {};
      await pool(ids, 4, async (sid) => {
        try { const h = await call('chat.history', {session_id: sid, limit: 200});
              const found = []; collect((h && (h.chat_events || h.events)) || [], found, 0);
              out[sid] = [...new Set(found.map(m => m.path).filter(Boolean))]; }
        catch (e) { out[sid] = null; } });
      return out;
    },
    // Đã kiểm chứng 2026-11-06: VM đòi trường method = '/api/session/delete'.
    deleteSessions: async (ids) => pool(ids, 4, async (id) => {
      try { const r = await call('session.delete', {session_id: id, method: '/api/session/delete'}); return {id, ok: !!(r && r.deleted !== false)}; }
      catch (e) { return {id, ok: false, err: String(e && e.message || e).slice(0, 120)}; } }),
    listDir: async (path) => { const r = await call('fs.list', {path}); return ((r && (r.entries || r.items || r.files)) || [])
      .map(x => ({name: x.name, dir: x.type === 'directory' || !!x.is_dir, size: x.size || 0, mtime: Date.parse(x.modifiedAt || x.modified_at || '') || x.modified_ms || 0})); },
    // fs.delete nhận đường dẫn TƯƠNG ĐỐI (workspace/...) + recursive; đường dẫn tuyệt đối bị 422.
    deleteFiles: async (paths) => pool(paths, 4, async (p) => {
      try { await call('fs.delete', {path: norm(p), recursive: false}); return {p, ok: true}; }
      catch (e) { return {p, ok: false, err: String(e && e.message || e).slice(0, 120)}; } }),
    rpcReady: () => { const s = rt(); return !!(s && typeof s.sendRequest === 'function' && (s.isConnected || s.connectionState === 'connected')); },
    ready: () => {
      const b = document.body ? document.body.innerText : '';
      const h = document.querySelector('[data-hatch-shell-hydration-state]');
      const s = rt();
      return {rs: document.readyState, ta: !!document.querySelector('textarea'),
              hyd: h ? h.getAttribute('data-hatch-shell-hydration-state') : null,
              conn: b.indexOf('Connecting...') !== -1, path: location.pathname, host: location.hostname,
              rpc: !!(s && typeof s.sendRequest === 'function'), connected: !!(s && (s.isConnected || s.connectionState === 'connected')),
              login: /log in|sign in|create an account|use another account/i.test(b.slice(0, 1500)) && !document.querySelector('textarea')};
    },
    thread: () => { const m = location.pathname.match(/^\/thread\/([0-9a-f-]{36})/i); return m ? m[1] : null; },
    // Trạng thái hội thoại qua RPC: sự kiện có seq > after, media do trợ lý tạo, trạng thái phiên.
    state: async (sid, after, limit) => {
      const out = {ok: true, status: null, events: [], maxSeq: after || 0, uploads: [], err: null};
      try {
        const [sess, hist] = await Promise.all([
          call('sessions.get', {id: sid}).catch(e => ({__err: String(e && e.message || e)})),
          call('chat.history', {session_id: sid, limit: limit || 40})]);
        out.status = sess && !sess.__err ? (sess.status || null) : null;
        const evs = (hist && (hist.chat_events || hist.events || hist.messages)) || [];
        for (const ev of evs) { const s = summarize(ev); out.uploads.push(...s.uploads); if (s.seq > (after || 0)) out.events.push(s); if (s.seq > out.maxSeq) out.maxSeq = s.seq; }
        out.events.sort((a, b) => a.seq - b.seq);
      } catch (e) { out.ok = false; out.err = String(e && e.message || e).slice(0, 300); }
      return out;
    },
    // Yêu cầu phê duyệt đang chờ (Muse hỏi "cho phép …?"). Tạo ảnh/video không cần quyền nào -> luôn từ chối.
    denyApprovals: async () => {
      const denied = [];
      try {
        const r = await call('egress.approvals', {});
        const list = (r && (r.approvals || r.pending || r.items || (r.payload && r.payload.approvals))) || (Array.isArray(r) ? r : []);
        for (const a of list) {
          const id = a.approval_id || a.id; const st = String(a.status || a.state || 'pending').toLowerCase();
          if (!id || !/pending|waiting|requested|open/.test(st)) continue;
          try { await call('egress.approval.decide', {approval_id: id, decision: 'deny', reason: 'not needed for media generation'}); denied.push(String(a.title || a.summary || a.kind || id).slice(0, 80)); } catch (e) {}
        }
      } catch (e) {}
      for (const card of document.querySelectorAll('[data-testid="hatch-inline-approval-card"]')) {
        const btn = [...card.querySelectorAll('button,[role=button]')].find(b => /^(deny|decline|reject|don.t allow|từ chối|拒绝)$/i.test((b.innerText || '').trim()));
        if (btn && !btn.disabled) { btn.click(); denied.push(card.getAttribute('aria-label') || 'approval card'); }
      }
      return denied;
    },
    // Tải file trên VM vào bộ đệm của trang; trả kích thước + loại. Lấy dữ liệu bằng chunk().
    fetchRaw: async (path) => {
      try {
        const b = await call('fs.raw', {path: norm(path)});
        const blob = (b instanceof Blob) ? b : (b && b.data instanceof Blob ? b.data : null);
        if (!blob) return {ok: false, err: 'fs.raw returned ' + (b && b.constructor && b.constructor.name)};
        const u8 = new Uint8Array(await blob.arrayBuffer());
        const id = 'r' + Math.random().toString(36).slice(2);
        (window.__luoBuf = window.__luoBuf || {})[id] = u8;
        return {ok: true, id, size: u8.length, mime: blob.type || ''};
      } catch (e) { return {ok: false, err: String(e && e.message || e).slice(0, 300)}; }
    },
    chunk: (id, start, len) => {
      const u8 = (window.__luoBuf || {})[id]; if (!u8) return null;
      const sub = u8.subarray(start, Math.min(u8.length, start + len)); let s = '';
      for (let i = 0; i < sub.length; i += 0x8000) s += String.fromCharCode.apply(null, sub.subarray(i, i + 0x8000));
      return btoa(s);
    },
    free: (id) => { if (window.__luoBuf) delete window.__luoBuf[id]; return true; },
    // Ảnh tham chiếu đang chờ gửi trong ô soạn tin (store của trang, có từ giao diện mới).
    pending: () => {
      try { const c = window.__hatch_store__.getState().composer;
            return {n: (c.pendingAttachments || []).length, processing: (c.processingFiles || []).length || (c.processingFiles && c.processingFiles.size) || 0}; }
      catch (e) { return null; }
    },
  };
  return true;
})()
"""

PAGE_STATE = """(() => {
  const body = document.body ? document.body.innerText : '';
  const h = document.querySelector('[data-hatch-shell-hydration-state]');
  return {ready: document.readyState === 'complete' && !!document.querySelector('textarea')
                 && (!h || h.getAttribute('data-hatch-shell-hydration-state') === 'hydrated') && body.indexOf('Connecting...') === -1,
          hasInput: !!document.querySelector('textarea'), path: location.pathname, head: body.slice(0, 1200)};
})()"""

# Mở hội thoại trống qua router Next.js của chính trang (1–4 s) thay vì tải lại cả app (Page.navigate).
SOFT_NEW_THREAD = """(() => {
  const r = window.next && window.next.router;
  if (!location.hostname.endsWith('muse.ai') || !r || typeof r.push !== 'function') return false;
  r.push('/thread/new'); return true;
})()"""

FRESH_THREAD = f"""(() => {{
  const p = {PAGE_STATE};
  return p.ready && p.path === '/thread/new' && document.querySelectorAll({q(ANY_BUBBLE)}).length === 0
         && document.querySelectorAll({q(ATTACHMENT)}).length === 0;
}})()"""

# Đóng hộp thoại sót lại; trả về có cần mở hội thoại mới hay không (trang đang có chat / đang chạy / kẹt).
NEEDS_NEW_THREAD = f"""(() => {{
  const d = document.querySelector('[role="dialog"]');
  if (d) {{ const b = d.querySelector('button[aria-label*="close" i], button'); if (b) b.click(); }}
  const bubbles = document.querySelectorAll({q(ANY_BUBBLE)}).length;
  const atts = document.querySelectorAll({q(ATTACHMENT)}).length;
  const stop = !!document.querySelector({q(STOP_BUTTON)});
  const t = document.body ? document.body.innerText : '';
  const stuck = t.indexOf('Still sending') !== -1 || t.indexOf('Connecting...') !== -1;
  return stop || stuck || atts > 0 || bubbles > 0 || location.pathname !== '/thread/new';
}})()"""


def fill_input(text: str) -> str:
    """Ghi vào textarea bằng setter gốc để React nhận (nhanh cả với prompt rất dài)."""
    return f"""(() => {{
  const ta = document.querySelector('textarea'); if (!ta) return 0;
  ta.focus();
  const s = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
  s.call(ta, {q(text)});
  ta.dispatchEvent(new Event('input', {{bubbles: true}}));
  ta.dispatchEvent(new Event('change', {{bubbles: true}}));
  return (ta.value || '').length;
}})()"""


# Chỉ khớp nút Gửi thật: chữ "send" có thể nằm trong tiêu đề chat ở thanh bên ("...waiting for re-send").
CLICK_SEND = """(() => {
  const b = [...document.querySelectorAll('button,[role=button]')].filter(x => x.offsetParent !== null)
    .find(x => /^(发送|send)( message)?$/i.test((x.getAttribute('aria-label') || '').trim())
            || /(^|-)send(-|$)/i.test(x.getAttribute('data-testid') || '')
            || /^(发送|send)$/i.test((x.innerText || '').trim()));
  if (!b) { const ta = document.querySelector('textarea'); return ta && ta.disabled ? 'input-disabled' : 'no-button'; }
  if (b.disabled) return 'disabled';
  b.click(); return 'clicked';
})()"""

INPUT_LEN = "String((document.querySelector('textarea')||{value:''}).value.length)"

# Nút "Remove attachment" chỉ có trong ô soạn tin (đính kèm trong lịch sử chat không có nút này).
REMOVE_ATTACHMENT_JS = r"[...document.querySelectorAll('button[aria-label]')].filter(b => /remove\s*attachment|移除附件|删除附件|xoá tệp đính kèm/i.test(b.getAttribute('aria-label') || ''))"

CLEAR_ATTACHMENTS = f"""(() => {{
  const btns = {REMOVE_ATTACHMENT_JS};
  btns.forEach(b => b.click());
  [...document.querySelectorAll('input[type="file"]')].forEach(i => {{ try {{ i.value = ''; }} catch (e) {{}} }});
  return btns.length;
}})()"""

# Số tham chiếu đã gắn vào ô soạn tin. Ảnh thu nhỏ nằm ở khung trên hàng textarea (tổ tiên thứ 2–3 của textarea,
# kiểm chứng 2026-11-06), không phải tổ tiên đầu tiên chứa input[type=file].
ATTACHED_COUNT = f"""(() => {{
  const removes = {REMOVE_ATTACHMENT_JS}.length;
  let thumbs = 0, e = document.querySelector('textarea');
  for (let i = 0; i < 3 && e; i++) {{ e = e.parentElement; if (e) thumbs = Math.max(thumbs, e.querySelectorAll('img, video, audio').length); }}
  return Math.max(removes, thumbs);
}})()"""

# Ô chọn file của khung soạn tin (để DOM.setFileInputFiles dùng objectId của nó).
FILE_INPUT_EXPR = f"""(() => {{
  const comp = ({COMPOSER_JS})();
  const ins = [...document.querySelectorAll('input[type="file"]')];
  const i = (comp && ins.find(x => comp.contains(x))) || ins.find(x => !x.closest('[class*=chat-user-bubble], [class*="group/msg"]')) || ins[0] || null;
  if (i) {{ i.multiple = true; if (!i.getAttribute('accept')) i.setAttribute('accept', 'image/*,video/*,audio/*'); }}
  return i;
}})()"""

# Đang tải tham chiếu lên (store của trang); -1 = không đọc được.
UPLOADING = """(() => { try { const c = window.__hatch_store__.getState().composer;
  const p = c.processingFiles; const n = Array.isArray(p) ? p.length : (p && p.size) || 0;
  const pend = (c.pendingAttachments || []).filter(a => a && (a.status === 'uploading' || a.uploadPromise && !a.uploaded)).length;
  return n + pend; } catch (e) { return -1; } })()"""

# Ảnh chụp nhanh hội thoại bằng DOM (đường dự phòng khi RPC của trang không dùng được).
CHAT_STATE_DOM = f"""(() => {{
  let sc = window.__luoScroller;
  if (!sc || !sc.isConnected) {{
    sc = [...document.querySelectorAll('main *, [class*="chat-scroll"]')].filter(e => {{ const s = getComputedStyle(e);
      return (s.overflowY === 'auto' || s.overflowY === 'scroll') && e.scrollHeight > e.clientHeight + 100; }})
      .sort((a, b) => b.scrollHeight - a.scrollHeight)[0] || null;
    window.__luoScroller = sc;
  }}
  if (sc) sc.scrollTop = sc.scrollHeight;
  const bs = [...document.querySelectorAll({q(ANY_BUBBLE)})];
  const agent = bs.filter(b => /hatch-agent-bubble-bg/.test(b.className || ''));
  const users = bs.filter(b => /chat-user-bubble/.test(b.className || '')).length;
  const atts = [];
  document.querySelectorAll({q(ATTACHMENT)}).forEach(a => {{
    if (a.closest('form, [class*=chat-user-bubble], [class*="group/msg"]')) return;
    const v = a.querySelector('video'), i = a.querySelector('img'); const tid = a.getAttribute('data-testid') || '';
    atts.push({{tid, hasVideo: !!v, vSrc: v ? (v.currentSrc || v.src || '') : '', src: (v || i) ? ((v || i).currentSrc || (v || i).src || '') : '',
               w: v ? v.videoWidth : (i ? i.naturalWidth : 0), h: v ? v.videoHeight : (i ? i.naturalHeight : 0)}});
  }});
  const t = document.body ? document.body.innerText : '';
  return {{agentCount: agent.length, users, lastText: agent.length ? (agent[agent.length - 1].innerText || '').trim().slice(0, 1500) : '',
           stop: !!document.querySelector({q(STOP_BUTTON)}), approval: !!document.querySelector({q(APPROVAL_CARD)}),
           atts, tail: t.slice(-700)}};
}})()"""


def fetch_blob_b64(url: str) -> str:
    """Đường dự phòng: lấy bytes của src (thường là blob:) ngay trong trang."""
    return f"""(async () => {{
  try {{ const r = await fetch({q(url)}); if (!r.ok) return JSON.stringify({{ok: false, err: 'media-http-' + r.status}});
    const b = await r.blob(); const u = new Uint8Array(await b.arrayBuffer()); let s = '';
    for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000));
    return JSON.stringify({{ok: true, mime: b.type || '', b64: btoa(s)}});
  }} catch (e) {{ return JSON.stringify({{ok: false, err: String(e)}}); }}
}})()"""


def inject_files(items: list[dict]) -> str:
    """Đường dự phòng: gắn file bằng DataTransfer khi DOM.setFileInputFiles không dùng được."""
    return f"""(() => {{
  try {{
    const comp = ({COMPOSER_JS})();
    const inputs = [...document.querySelectorAll('input[type="file"]')];
    const input = (comp && inputs.find(x => comp.contains(x))) || inputs.find(x => !x.closest('[class*=chat-user-bubble], [class*="group/msg"]')) || inputs[0];
    if (!input) return {{ok: false, err: 'no-file-input'}};
    const dt = new DataTransfer();
    for (const it of {q(items)}) {{
      const bin = atob(it.b64); const u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
      dt.items.add(new File([u], it.name, {{type: it.mime}}));
    }}
    if (!input.getAttribute('accept')) input.setAttribute('accept', 'image/*,video/*,audio/*');
    input.multiple = true; input.files = dt.files;
    input.dispatchEvent(new Event('change', {{bubbles: true}})); input.dispatchEvent(new Event('input', {{bubbles: true}}));
    return {{ok: true}};
  }} catch (e) {{ return {{ok: false, err: String(e)}}; }}
}})()"""


# ---------------------------------------------------------------- hạn mức (Settings -> Usage)
_VISIBLE = "const visible = e => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';"
_CENTER = "if (!b) return null; const r = b.getBoundingClientRect(); return JSON.stringify({x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2)});"
SETTINGS_LABELS = ("Settings", "設定", "设置", "Cài đặt")

QUOTA_SETTINGS_ENTRY = f"""(() => {{
  {_VISIBLE}
  const labels = {q(list(SETTINGS_LABELS))};
  const b = [...document.querySelectorAll({q(SETTINGS_DOCK)})].find(visible)
    || [...document.querySelectorAll('button,[role=button]')].find(e => visible(e) && labels.includes((e.getAttribute('aria-label') || '').trim()));
  {_CENTER}
}})()"""

QUOTA_MENU_ITEM = f"""(() => {{
  {_VISIBLE}
  const labels = {q(list(SETTINGS_LABELS))};
  const exact = e => labels.includes((e.textContent || '').trim());
  const b = [...document.querySelectorAll('[role=menuitem]')].find(e => visible(e) && (exact(e) || [...e.querySelectorAll('span,div')].some(exact)))
    || [...document.querySelectorAll('[role=menu] button,[role=menu] span,[role=menu] div')].find(e => visible(e) && exact(e))
    || [...document.querySelectorAll('div,span,li,button')].filter(e => visible(e) && exact(e) && e.getAttribute('aria-label') !== 'Settings' && e.children.length <= 3).pop();
  {_CENTER}
}})()"""

QUOTA_DIALOG_TEXT = """(() => {
  const d = [...document.querySelectorAll('[role=dialog],[aria-modal=true]')].find(e => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden');
  return d ? (d.innerText || '') : '';
})()"""
