"use strict";
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const api = async (path, o = {}) => {
  const r = await fetch("/api/" + path, { method: o.method || (o.body ? "POST" : "GET"), headers: { "Content-Type": "application/json" }, body: o.body ? JSON.stringify(o.body) : undefined });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || r.statusText);
  return d;
};
const P = {
  folder: "M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
  play: "M7 4.5v15l12-7.5z", film: "M4 4h16v16H4zM8 4v16M16 4v16M4 9h4M4 15h4M16 9h4M16 15h4",
  gear: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z",
  plus: "M12 5v14M5 12h14", stop: "M6 6h12v12H6z", trash: "M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14M10 11v5M14 11v5",
  redo: "M3 12a9 9 0 0 1 15.5-6.2L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.5 6.2L3 16M3 21v-5h5",
  back: "M15 5l-7 7 7 7", check: "M5 12l5 5 9-10", x: "M6 6l12 12M18 6L6 18", up: "M12 19V5M5 12l7-7 7 7", down: "M12 5v14M19 12l-7 7-7-7",
  users: "M16 11a4 4 0 1 0-8 0 4 4 0 0 0 8 0zM4 20a8 8 0 0 1 16 0M19 8a3 3 0 0 1 0 6M5 8a3 3 0 0 0 0 6", server: "M4 5h16v5H4zM4 14h16v5H4zM8 7.5h.01M8 16.5h.01", layers: "M12 3l9 5-9 5-9-5zM3 13l9 5 9-5M3 17l9 5 9-5", clock: "M12 7v5l3 2M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z", chev: "M9 5l7 7-7 7", wand: "M15 4l5 5L9 20l-5-5zM13 6l5 5", book: "M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 19a2 2 0 0 1 2-2h13", sparkle: "M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z", dl: "M12 4v12M6 10l6 6 6-6M4 20h16", table: "M3 5h18v14H3zM3 10h18M3 15h18M9 5v14M15 5v14", list: "M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01", up2: "M12 16V4M6 10l6-6 6 6M4 20h16", copy: "M9 9h11v11H9zM5 15H4V4h11v1",
  folderopen: "M3 8a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v1H7l-4 8zM3 17l3-7h17l-3 7z", bolt: "M13 2L4 14h7l-1 8 9-12h-7z", img: "M4 5h16v14H4zM8.5 10a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM20 16l-5-5-8 8",
};
const ico = (n, cls = "") => `<svg class="i ${cls}" viewBox="0 0 24 24"><path d="${P[n]}"/></svg>`;

const S = { boot: null, project: null, sel: 0, checked: {}, q: null, qsig: "", qsel: null, qview: null, qopen: {}, qT: 0, results: [], health: null, runSel: null, saveT: 0, route: {}, logOpen: false };

const EMOS = ["curious, friendly", "surprised, excited", "warm, encouraging", "doubtful, worried", "unsure, embarrassed", "proud, delighted", "playful, teasing", "relieved, happy", "confident, persuasive", "hopeful, eager", "impressed, admiring", "confused, puzzled", "decisive, determined"];
const EMOS2 = ["attentive, calm", "amused", "surprised", "skeptical", "impressed", "patient, kind", "puzzled", "interested", "worried", "encouraging"];
const COLORS = [["white", "Trắng"], ["red", "Đỏ ✕"], ["green", "Xanh lá"], ["yellow", "Vàng"]];

// ---------------------------------------------------------------- helpers
const toast = (m, err) => { const t = document.createElement("div"); t.className = "t" + (err ? " err" : ""); t.textContent = m; $("#toast").appendChild(t); setTimeout(() => t.remove(), err ? 5000 : 2600); };
const toastLink = (m, href, label) => { const t = document.createElement("div"); t.className = "t"; t.innerHTML = `${esc(m)} <a data-go="${href}" style="color:var(--accent2);font-weight:650;margin-left:10px">${esc(label)} →</a>`; $("#toast").appendChild(t); setTimeout(() => t.remove(), 6000); t.querySelector("a").onclick = () => t.remove(); };
const fmtT = s => (s == null ? "" : s + "s");
const ago = t => { const d = Date.now() / 1000 - t; return d < 60 ? "vừa xong" : d < 3600 ? Math.floor(d / 60) + " phút trước" : d < 86400 ? Math.floor(d / 3600) + " giờ trước" : Math.floor(d / 86400) + " ngày trước"; };
const typ = id => S.boot.types.find(t => t.id === id) || { id, name: id, scenes: 0, fields: [], series: {}, turns: {}, defaults: {} };
const media = (p, v, f) => `/media/${encodeURIComponent(p)}/${encodeURIComponent(v)}/${f}`;
const grow = el => { if (el.matches("textarea[data-k],textarea[data-s]")) return; el.style.height = "auto"; el.style.height = Math.min(el.scrollHeight, 260) + "px"; };
const openModal = html => { $("#modal").innerHTML = html; $("#modal").classList.remove("hidden"); };
const closeModal = () => { $("#modal").classList.add("hidden"); $("#modal").innerHTML = ""; };
$("#modal").addEventListener("mousedown", e => { if (e.target.id === "modal") closeModal(); });
document.addEventListener("keydown", e => { if (e.key === "Escape") closeModal(); });

// ---------------------------------------------------------------- shell
function nav() {
  const r = S.route.page, running = S.q && S.q.busy, queued = S.q ? S.q.items.filter(i => i.state === "queued").length : 0;
  const b = (h, ic, tip, on, dot, badge) => `<a data-go="#/${h}" class="nav-b ${on ? "on" : ""}">${ico(ic)}${dot ? '<span class="dot"></span>' : ""}${badge ? `<span class="nbadge">${badge}</span>` : ""}<span class="tip">${tip}</span></a>`;
  $("#nav").innerHTML = `<div class="logo"><img src="logo.png" alt="LUO Studio"></div>${b("", "folder", "Dự án", r === "home" || r === "edit")}${b("run", "bolt", "Hàng đợi", r === "run", running, queued)}${b("results", "film", "Kết quả", r === "results")}${b("types", "layers", "Loại dự án", r === "types")}${b("api", "server", "API Muse", r === "api")}<div class="spacer"></div><div class="ver" style="font-size:10px;opacity:.55;padding:4px 0">${S.health && S.health.version ? "v" + S.health.version : ""}</div>${b("settings", "gear", "Cài đặt", r === "settings")}`;
}
function setTop(title, extra = "") {
  const h = S.health, cls = h ? (h.ok ? "ok" : "bad") : "";
  $("#top").innerHTML = `${S.route.page === "edit" ? `<a class="ib" data-go="#/" title="Quay lại">${ico("back")}</a>` : ""}<h1>${title}</h1><div class="grow"></div>${extra}<span class="pill ${h && h.status === "no_account" ? "warn" : cls}" title="LUO-API" ${h && h.status === "no_account" ? 'data-go="#/api" style="cursor:pointer"' : ""}><i></i>${h ? (h.ok ? "API sẵn sàng" : h.status === "no_account" ? "Chưa có tài khoản Muse" : "API chưa kết nối") : "…"}</span>`;
}
async function refreshHealth() { try { S.health = await api("health"); } catch { S.health = { ok: false }; } const p = $("#top .pill"); if (p) { const na = S.health.status === "no_account"; p.className = "pill " + (S.health.ok ? "ok" : na ? "warn" : "bad"); p.lastChild.textContent = S.health.ok ? "API sẵn sàng" : na ? "Chưa có tài khoản Muse" : "API chưa kết nối"; } const vv = $("#nav .ver"); if (vv && S.health.version) vv.textContent = "v" + S.health.version; }

// ---------------------------------------------------------------- router
async function route() {
  const h = location.hash.replace(/^#\/?/, "").split("/");
  const page = h[0] === "p" ? "edit" : h[0] || "home";
  S.route = { page, id: h[1] ? decodeURIComponent(h[1]) : h[1] };
  if (!S.boot) S.boot = await api("boot");
  nav();
  if (page === "home") return pageHome();
  if (page === "edit") return pageEditor(S.route.id);
  if (page === "run") return pageRun();
  if (page === "results") return pageResults();
  if (page === "types") return pageTypes();
  if (page === "settings") return pageSettings();
  if (page === "api") return pageApi();
}
try { if (!window.__fs) { window.__fs = 1; if (outerWidth < screen.availWidth - 40 || outerHeight < screen.availHeight - 40) { moveTo(0, 0); resizeTo(screen.availWidth, screen.availHeight); } } } catch (e) {}
window.addEventListener("hashchange", route);
document.addEventListener("click", e => { const a = e.target.closest("[data-go]"); if (a) { e.preventDefault(); location.hash = a.dataset.go; } });

// ---------------------------------------------------------------- Dự án
const clone = o => JSON.parse(JSON.stringify(o));
const normKey = s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/gi, "d").toLowerCase().replace(/[^a-z0-9]+/g, "");
function parseCSV(text) {
  text = text.replace(/^﻿/, "");
  const first = text.split(/\r?\n/)[0] || "", d = first.includes("\t") ? "\t" : (first.split(";").length > first.split(",").length ? ";" : ",");
  const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
    else if (c === '"') q = true;
    else if (c === d) { row.push(cur); cur = ""; }
    else if (c === "\n") { row.push(cur.replace(/\r$/, "")); rows.push(row); row = []; cur = ""; }
    else cur += c;
  }
  if (cur !== "" || row.length) { row.push(cur.replace(/\r$/, "")); rows.push(row); }
  return rows.filter(r => r.some(x => x.trim() !== ""));
}
// Danh sách biến thể từ file JSON ([{name, ...}]) hoặc CSV (dòng đầu = tên cột: key hoặc nhãn trường)
function variantsFromText(fileName, text, T) {
  if (/\.json$/i.test(fileName)) {
    let d = JSON.parse(text.replace(/^﻿/, "")); d = Array.isArray(d) ? d : d.variants;
    if (!Array.isArray(d) || !d.length) throw new Error("File JSON phải là danh sách biến thể");
    return d.map((v, i) => ({ ...v, name: v.name || "Biến thể " + (i + 1) }));
  }
  const t = parseCSV(text); if (t.length < 2) throw new Error("File CSV trống");
  const head = t[0].map(normKey), cols = [{ k: "name", names: ["name", "ten"] }, ...T.fields.map(f => ({ k: f.key, names: [normKey(f.key), normKey(f.label), normKey(f.group + f.label)] }))];
  const map = {}; cols.forEach(c => { const i = head.findIndex(h => c.names.includes(h)); if (i >= 0) map[c.k] = i; });
  if (!Object.keys(map).length) throw new Error("Dòng đầu phải là tên cột (Tên, " + T.fields.slice(0, 2).map(f => f.label).join(", ") + "…)");
  return t.slice(1).map((r, n) => { const v = {}; Object.entries(map).forEach(([k, i]) => v[k] = r[i] ?? ""); if (!v.name) v.name = "Biến thể " + (n + 1); return v; });
}
function fillVariant(v, T) {
  const o = { ...v };
  T.fields.forEach(f => { if (o[f.key] == null) o[f.key] = f.default || ""; });
  Object.entries(T.series || {}).forEach(([pre, n]) => { if (!Array.isArray(o[pre])) o[pre] = pre === "LUOT" ? [] : Array(n).fill(""); });
  Object.entries(T.defaults || {}).forEach(([k, val]) => { if (o[k] == null) o[k] = val; });
  return o;
}

async function pageHome() {
  S.boot = await api("boot");
  setTop("Dự án");
  const cards = S.boot.projects.map(p => `<div class="card click pcard" data-open="${p.id}">
    <button class="ib danger del" data-del="${p.id}" title="Xoá">${ico("trash")}</button>
    <div><h3>${esc(p.name)}</h3></div>
    <div class="meta"><span class="tag">${esc(typ(p.template).name)}</span></div>
    <div class="meta"><span>${p.variants} biến thể</span>·<span>${p.turns} lượt</span>·<span>${ago(p.updated)}</span></div></div>`).join("");
  const noacc = S.health && S.health.status === "no_account" ? `<div class="card sec apwarn" style="margin-bottom:16px"><b>Bước đầu tiên: thêm tài khoản Muse.</b> Chưa có tài khoản nào nên chưa gen được video. <a class="btn sm primary" data-go="#/api" style="margin-left:10px">Mở tab API Muse</a></div>` : "";
  $("#view").innerHTML = `${noacc}<div class="grid">${cards}<button class="card newcard" id="newp"><span class="plus">${ico("plus")}</span>Dự án mới</button></div>`;
  $("#newp").onclick = newProjectModal;
  $("#view").onclick = async e => {
    const del = e.target.closest("[data-del]");
    if (del) { e.stopPropagation(); if (confirm("Xoá dự án và toàn bộ video đã tạo?")) { await api("projects/" + del.dataset.del, { method: "DELETE" }); pageHome(); } return; }
    const o = e.target.closest("[data-open]"); if (o) location.hash = "#/p/" + o.dataset.open;
  };
}
function newProjectModal(presetType) {
  let t = presetType && typeof presetType === "string" ? presetType : (S.boot.types[0] || {}).id, file = null, name = "";
  const draw = () => openModal(`<div class="mbox"><h2>Dự án mới <button class="ib" id="mx">${ico("x")}</button></h2>
    <div class="f"><label>Tên</label><input id="npn" value="${esc(name)}" placeholder="Talka - nấu ăn" autofocus></div>
    <div class="f"><label>Loại dự án</label></div><div class="tpls">${S.boot.types.map(x => `<div class="tpl ${x.id === t ? "on" : ""}" data-t="${x.id}"><b>${esc(x.name)}</b><small>${x.scenes} cảnh · ${x.fields.length} trường</small></div>`).join("")}<div class="tpl dashed" id="newtype">${ico("plus")}<b>Loại mới</b><small>Thêm script riêng</small></div></div>
    <div class="f" style="margin-top:14px"><label>Danh sách biến thể (tuỳ chọn)</label><div class="pick"><input class="input" readonly value="${esc(file ? file.name + " · " + file.n + " biến thể" : "")}" placeholder="JSON hoặc CSV"><label class="btn sm" style="cursor:pointer">Chọn<input type="file" id="npf" accept=".json,.csv,.tsv,.txt" hidden></label></div></div>
    <div class="mact"><button class="btn" id="mx2">Huỷ</button><button class="btn primary" id="npok">Tạo</button></div></div>`);
  draw();
  $("#modal").onclick = async e => {
    const x = e.target.closest("[data-t]"); if (x) { name = $("#npn").value; t = x.dataset.t; file = null; draw(); return; }
    if (e.target.closest("#newtype")) { name = $("#npn").value; return typeWizard(null, { fromProject: name }); }
    if (e.target.id === "modal" || e.target.closest("#mx") || e.target.id === "mx2") return closeModal();
    if (e.target.id === "npok") {
      const nm = $("#npn").value.trim() || "Dự án mới", T = typ(t);
      const variants = file ? file.variants.map(v => fillVariant(v, T)) : undefined;
      const p = await api("projects", { body: { name: nm, template: t, variants } }); closeModal(); location.hash = "#/p/" + p.id;
    }
  };
  $("#modal").onchange = async e => {
    if (e.target.id !== "npf") return; const f = e.target.files[0]; e.target.value = ""; if (!f) return;
    try { const variants = variantsFromText(f.name, await f.text(), typ(t)); name = $("#npn").value; file = { name: f.name, n: variants.length, variants }; draw(); } catch (er) { toast(er.message, 1); }
  };
}

// ---------------------------------------------------------------- Soạn dự án
function touch() { clearTimeout(S.saveT); S.saveT = setTimeout(save, 500); }
async function save() { if (!S.project) return; try { await api("projects/" + S.project.id, { method: "PUT", body: { name: S.project.name, variants: S.project.variants } }); } catch (e) { toast(e.message, 1); } }
const curV = () => S.project.variants[S.sel] || S.project.variants[0];
const GROUP_LABEL = (T, g) => g === "day" ? T.turns.day_label || "Người dạy" : g === "hoc" ? T.turns.hoc_label || "Người học" : g === "scene" ? "Bối cảnh" : g === "other" ? "Khác" : g;
const GROUP_DOT = g => g === "day" ? "day" : g === "hoc" ? "hoc" : "";

async function pageEditor(id) {
  if (!S.boot) S.boot = await api("boot");
  if (!S.project || S.project.id !== id) { S.project = await api("projects/" + id); S.sel = 0; }
  const p = S.project, T = typ(p.template), ck = S.checked[id] || (S.checked[id] = new Set(p.variants.map(v => v.name)));
  const v = curV(), hasTurns = "LUOT" in (T.series || {}), need = (T.series || {}).LUOT || 0, n = (v.LUOT || []).length;
  setTop(`<input id="pname" class="input" style="width:280px;font-weight:650;font-size:16px;background:none;border-color:transparent" value="${esc(p.name)}">`,
    `<span class="tag" title="Loại dự án (không đổi được sau khi tạo)">${esc(T.name)}</span>
     <button class="btn primary" id="go" ${ck.size ? "" : "disabled"}>${ico("plus")}Thêm vào hàng đợi${ck.size > 1 ? " (" + ck.size + ")" : ""}</button>`);
  const groups = []; T.fields.forEach(f => { if (!groups.includes(f.group)) groups.push(f.group); });
  const attach = key => { const L = (v.refs || {})[key] || [];
    return `<div class="att">${L.map((a, j) => a.type === "audio"
      ? `<span class="chip"><audio controls preload="none" src="/asset/${encodeURIComponent(p.id)}/${a.file}"></audio><i title="${esc(a.name)}">${esc(a.name)}</i><button class="x" data-ratt="${key}" data-j="${j}">×</button></span>`
      : `<span class="chip img"><img src="/asset/${encodeURIComponent(p.id)}/${a.file}" title="${esc(a.name)}"><button class="x" data-ratt="${key}" data-j="${j}">×</button></span>`).join("")}
      <label class="addatt" title="${key.startsWith("GIONG") ? "Đính kèm mp3 mẫu giọng của nhân vật này. Nên dùng hai giọng khác hẳn nhau (cao/sáng/nhanh và trầm/khàn/chậm). Chỉ dùng khi nhân vật này đang nói; Muse có thể bỏ qua." : "Đính kèm ảnh tham chiếu hoặc file mp3 (Muse có thể bỏ qua)"}">${ico("plus")}Ảnh / mp3<input type="file" hidden accept="image/*,audio/*" multiple data-att="${key}"></label></div>`; };
  const field = f => `<div class="f"><label>${esc(f.label)}${f.optional ? " <small style='opacity:.6'>(tuỳ chọn)</small>" : ""}</label>${f.kind === "short"
    ? `<input data-k="${f.key}" value="${esc(v[f.key] ?? "")}" placeholder="${esc(f.ph || "")}">`
    : `<textarea data-k="${f.key}" rows="${f.rows || 2}" placeholder="${esc(f.ph || "")}">${esc(v[f.key] ?? "")}</textarea>`}${attach(f.key)}</div>`;
  const gcard = g => `<div><div class="who">${GROUP_DOT(g) ? `<b style="background:var(--${GROUP_DOT(g)})"></b>` : ""}${esc(GROUP_LABEL(T, g))}</div>${T.fields.filter(f => f.group === g).map(field).join("")}</div>`;
  const sides = ["day", "hoc"].filter(g => groups.includes(g)), rest = groups.filter(g => !sides.includes(g));
  const seriesPlain = Object.entries(T.series || {}).filter(([pre]) => pre !== "LUOT");
  $("#view").innerHTML = `<div class="editor">
    <div class="card vlist">${p.variants.map((x, i) => `<div class="vitem ${i === S.sel ? "on" : ""}" data-v="${i}"><span class="chk ${ck.has(x.name) ? "on" : ""}" data-ck="${i}">${ck.has(x.name) ? ico("check") : ""}</span><span class="n">${esc(x.name)}</span></div>`).join("")}
      <div class="vtools"><button class="ib" data-act="addv" title="Thêm biến thể">${ico("plus")}</button><button class="ib" data-act="dupv" title="Nhân bản">${ico("copy")}</button><button class="ib" data-act="imp" title="Điền từ file hoặc bảng">${ico("up2")}</button><button class="ib" data-act="faces" title="Tạo nhiều khuôn mặt khác nhau từ biến thể này">${ico("users")}</button><button class="ib danger" data-act="delv" title="Xoá">${ico("trash")}</button></div>
      </div>
    <div>
      <div class="card sec"><div class="f" style="max-width:340px"><label>Tên biến thể</label><input data-k="name" value="${esc(v.name)}"></div>
        ${sides.length ? `<div class="${sides.length > 1 ? "two" : ""}">${sides.map(gcard).join("")}</div>` : ""}</div>
      ${rest.map(g => `<div class="card sec"><h4>${esc(GROUP_LABEL(T, g))}</h4><div class="two">${T.fields.filter(f => f.group === g).map(field).join("")}</div></div>`).join("")}
      ${seriesPlain.map(([pre, num]) => `<div class="card sec"><h4>${esc(pre)}</h4>${Array.from({ length: num }, (_, i) => `<div class="f"><label>${pre}_${i + 1}</label><textarea data-s="${pre}" data-i="${i}" rows="1">${esc((v[pre] || [])[i] ?? "")}</textarea></div>`).join("")}</div>`).join("")}
      ${hasTurns ? `<div class="card sec"><h4>Lời thoại <span class="tag ${n >= 1 ? "ok" : "bad"}" title="Số lượt tuỳ ý; mỗi lượt = 1 cảnh (script mẫu có ${need} cảnh, thiếu thì tự nhân bản cảnh cuối)">${n} lượt</span> <small style="color:var(--mute)">≈ ${n * 5}–${n * 6}s</small></h4><div class="turns" id="turns"></div>
        <div style="margin-top:12px"><button class="btn sm" data-act="addt">${ico("plus")}Thêm lượt</button></div></div>` : ""}
    </div></div>`;
  if (hasTurns) drawTurns();
  $("#view").querySelectorAll("textarea[data-k]").forEach(grow);
  $("#pname").oninput = e => { p.name = e.target.value; touch(); };
  $("#go").onclick = runSelected;
  $("#view").oninput = e => {
    const el = e.target; if (el.matches("textarea")) grow(el);
    if (el.dataset.k) { const val = el.value; curV()[el.dataset.k] = val; if (el.dataset.k === "name") { const it = $(`.vitem[data-v="${S.sel}"] .n`); if (it) it.textContent = val; } touch(); }
    if (el.dataset.s) { const a = curV()[el.dataset.s] = curV()[el.dataset.s] || []; a[+el.dataset.i] = el.value; touch(); }
    if (el.dataset.t) { const t = curV().LUOT[+el.dataset.i]; t[el.dataset.t] = el.value; touch(); }
  };
  $("#view").onchange = async e => {
    const el = e.target;
    if (el.dataset.att) {
      const key = el.dataset.att, files = [...el.files]; el.value = "";
      for (const f of files) {
        try {
          const data = await new Promise((ok, no) => { const r = new FileReader(); r.onload = () => ok(r.result.split(",")[1]); r.onerror = no; r.readAsDataURL(f); });
          const r = await api(`projects/${p.id}/asset`, { body: { name: f.name, data } });
          const V = curV(); V.refs = V.refs || {}; (V.refs[key] = V.refs[key] || []).push({ type: r.type, file: r.file, name: f.name });
        } catch (er) { toast(er.message, 1); }
      }
      await save(); pageEditor(p.id); return;
    }
    if (el.dataset.c !== undefined) { curV().LUOT[+el.dataset.i].c = el.value; touch(); drawTurns(); } };
  $("#view").onclick = e => editorClick(e);
}
function drawTurns() {
  const v = curV(); v.LUOT = v.LUOT || [];
  $("#turns").innerHTML = v.LUOT.map((t, i) => `<div class="turn"><span class="no">${i + 1}</span>
    <div class="sw"><button class="d ${t.who === "day" ? "on" : ""}" data-who="day" data-i="${i}">Dạy</button><button class="h ${t.who === "hoc" ? "on" : ""}" data-who="hoc" data-i="${i}">Học</button></div>
    <textarea data-t="text" data-i="${i}" rows="1" placeholder="Lời thoại">${esc(t.text || "")}</textarea>
    <input class="emo" list="emos" data-t="emo" data-i="${i}" value="${esc(t.emo || "")}" placeholder="cảm xúc người nói">
    <select class="fxsel" data-t="fx" data-i="${i}" title="Hiệu ứng hậu kỳ: Sai = viền đỏ nháy + tiếng tè tè; Đúng = viền xanh lá nháy + tiếng tinh tinh. Để trống = tự động (người học nói đầu tiên là sai, câu AI sửa ngay sau là đúng)"><option value="" ${!t.fx ? "selected" : ""}>Hiệu ứng: tự động</option><option value="none" ${t.fx === "none" ? "selected" : ""}>Không</option><option value="wrong" ${t.fx === "wrong" ? "selected" : ""}>Sai (đỏ + tè tè)</option><option value="right" ${t.fx === "right" ? "selected" : ""}>Đúng (xanh + tinh)</option></select>
    <div class="colr" title="Màu phụ đề"><i class="c-${t.c || "white"}"></i><select data-c data-i="${i}">${COLORS.map(([c, n]) => `<option value="${c}" ${(t.c || "white") === c ? "selected" : ""}>${n}</option>`).join("")}</select></div>
    <div class="acts"><button class="ib" data-mv="-1" data-i="${i}">${ico("up")}</button><button class="ib" data-mv="1" data-i="${i}">${ico("down")}</button><button class="ib danger" data-rm="${i}">${ico("x")}</button></div></div>`).join("");
  $("#turns").querySelectorAll("textarea").forEach(grow);
  if (!$("#emos")) document.body.insertAdjacentHTML("beforeend", `<datalist id="emos">${EMOS.map(x => `<option value="${x}">`).join("")}</datalist><datalist id="emos2">${EMOS2.map(x => `<option value="${x}">`).join("")}</datalist>`);
}
function editorClick(e) {
  const rb = e.target.closest("[data-ratt]");
  if (rb) { const V = curV(); V.refs[rb.dataset.ratt].splice(+rb.dataset.j, 1); if (!V.refs[rb.dataset.ratt].length) delete V.refs[rb.dataset.ratt]; touch(); pageEditor(S.project.id); return; }
  const p = S.project, ck = S.checked[p.id];
  const g = s => e.target.closest(s);
  let x;
  if ((x = g("[data-ck]"))) { e.stopPropagation(); const nm = p.variants[+x.dataset.ck].name; ck.has(nm) ? ck.delete(nm) : ck.add(nm); return pageEditor(p.id); }
  if ((x = g("[data-v]"))) { S.sel = +x.dataset.v; return pageEditor(p.id); }
  if ((x = g("[data-who]"))) { curV().LUOT[+x.dataset.i].who = x.dataset.who; touch(); return drawTurns(); }
  if ((x = g("[data-mv]"))) { const i = +x.dataset.i, j = i + +x.dataset.mv, a = curV().LUOT; if (j >= 0 && j < a.length) { [a[i], a[j]] = [a[j], a[i]]; touch(); drawTurns(); } return; }
  if ((x = g("[data-rm]"))) { curV().LUOT.splice(+x.dataset.rm, 1); touch(); return pageEditor(p.id); }
  if ((x = g("[data-act]"))) {
    const a = x.dataset.act, v = curV();
    if (a === "addt") { const last = v.LUOT[v.LUOT.length - 1]; v.LUOT.push({ who: last && last.who === "day" ? "hoc" : "day", text: "", emo: "" }); touch(); return pageEditor(p.id); }
    if (a === "addv") { const nv = clone(v); nv.name = uniqueName("Biến thể " + (p.variants.length + 1)); if (nv.LUOT) nv.LUOT = []; p.variants.push(nv); S.sel = p.variants.length - 1; ck.add(nv.name); touch(); return pageEditor(p.id); }
    if (a === "dupv") { const nv = clone(v); nv.name = uniqueName(v.name + " (bản sao)"); p.variants.push(nv); S.sel = p.variants.length - 1; ck.add(nv.name); touch(); return pageEditor(p.id); }
    if (a === "delv") { if (p.variants.length < 2) return toast("Cần ít nhất một biến thể", 1); if (!confirm("Xoá biến thể này?")) return; ck.delete(v.name); p.variants.splice(S.sel, 1); S.sel = 0; touch(); return pageEditor(p.id); }
    if (a === "imp") return fillModal();
    if (a === "faces") return facesModal();
  }
}
// ---------------------------------------------------------------- Nhiều khuôn mặt khác nhau từ một biến thể
const FACES = {
  m: ["a lean, long narrow face with a very high forehead, a hooked thin nose, pale blue eyes, deep sun creases, clean-shaven, hair combed neatly to one side",
    "a broad, round, soft face with rosy full cheeks, a double chin, small hazel eyes behind rimless glasses, a wide flat nose, thick eyebrows and a short stubble beard, thinning short hair",
    "a strong square jaw with a dimpled chin, deep-set gray-green eyes, a crooked once-broken nose, a thin scar through one eyebrow, very dark tan, a short crew cut",
    "an oval face with a prominent chin, droopy kind eyes, a large rounded nose, deep laugh lines, a thin mustache only, a receding hairline",
    "a heavy-set face with a thick neck, narrow eyes, a short full beard, ruddy cheeks, small ears, bushy eyebrows",
    "a thin angular face with sharp cheekbones, wire-rimmed glasses, light stubble, pale freckled skin, large ears",
    "a rugged face with a flat broad nose, bushy eyebrows, brown eyes, a deeply creased forehead, a gold stud in one ear",
    "a soft rounded face with a small chin, wide-set pale eyes, a button nose, a cleft chin, a high receding hairline and a small mole near the eye"],
  f: ["a long oval face with high cheekbones, pale blue eyes, thin lips, finely lined skin, a feathered pixie cut, small hoop earrings",
    "a round soft face with rosy cheeks, warm brown eyes behind thin round glasses, a small mole on one cheek, deep smile lines, side-swept bangs",
    "a strong square-jawed face with thick arched eyebrows, green eyes, a wide mouth, freckled tanned skin, very short cropped hair",
    "a heart-shaped face with a pointed chin, large green-gray eyes, thin arched eyebrows, a small upturned nose, dimples",
    "an angular face with a defined jaw, deep-set dark eyes, an aquiline nose, strong eyebrows, light freckles, loose curly strands around the face",
    "a lined, expressive face with a prominent nose, bright dark eyes, a high forehead, thin tortoiseshell glasses",
    "a soft rounded face with full cheeks, wide-set pale eyes, a button nose, fine wrinkles, small pearl earrings",
    "a long narrow face with a strong nose, hooded eyes, thin lips, defined cheekbones, a beauty mark near the mouth"],
};
function facesModal() {
  const p = S.project, v = curV(), base = String(v.NGUOI_HOC || "");
  if (!base.trim()) return toast("Biến thể chưa có mô tả ngoại hình người học (ô Ngoại hình)", 1);
  const g = /\b(woman|women|female|girl|lady|she|her)\b/i.test(base) ? "f" : "m";
  openModal(`<div class="mbox"><h2>Tạo nhiều khuôn mặt <button class="ib" id="mx">${ico("x")}</button></h2>
    <p style="color:var(--mute);margin-bottom:14px">Từ biến thể <b>${esc(v.name)}</b>, tạo thêm các biến thể giữ nguyên mô tả chung (tuổi, tóc, quần áo, tạp dề…) nhưng mỗi người một khuôn mặt khác nhau (hình dáng mặt, mắt, mũi, râu/kính…).</p>
    <div class="f" style="max-width:220px"><label>Số khuôn mặt cần có (tính cả bản gốc)</label><input class="input" id="fn" type="number" min="2" max="8" value="3"></div>
    <div class="f" style="margin-top:12px"><label>Giới tính (tự nhận từ mô tả)</label><div class="seg" id="fg"><button data-g="m" class="${g === "m" ? "on" : ""}">Nam</button><button data-g="f" class="${g === "f" ? "on" : ""}">Nữ</button></div></div>
    <div style="margin-top:12px"><label class="chkrow"><span class="chk on" id="fkeep">${ico("check")}</span> Giữ bản gốc (không đổi mặt), tạo thêm các bản còn lại</label></div>
    <div class="row2" style="margin-top:18px;justify-content:flex-end"><button class="btn ghost" id="fc">Huỷ</button><button class="btn primary" id="fok">${ico("users")}Tạo</button></div></div>`);
  let gender = g, keep = true;
  $("#modal").onclick = e => {
    if (e.target.closest("#mx, #fc")) return closeModal();
    const gb = e.target.closest("[data-g]"); if (gb) { gender = gb.dataset.g; document.querySelectorAll("#fg button").forEach(b => b.classList.toggle("on", b.dataset.g === gender)); return; }
    if (e.target.closest("#fkeep")) { keep = !keep; const c = $("#fkeep"); c.classList.toggle("on", keep); c.innerHTML = keep ? ico("check") : ""; return; }
    if (e.target.closest("#fok")) {
      const n = Math.max(2, Math.min(8, +$("#fn").value || 3)), pool = FACES[gender], ck = S.checked[p.id] || (S.checked[p.id] = new Set());
      const start = Math.floor(Math.random() * pool.length), made = [];
      for (let i = 0; i < n; i++) {
        if (i === 0 && keep) continue;
        const nv = clone(v); nv.name = uniqueName(`${v.name} - mặt ${i + 1}`);
        nv.NGUOI_HOC = `FACE (the most important identifying feature, clearly unlike any other person in this series): ${pool[(start + i) % pool.length]}. ${base.replace(/^FACE \(.*?\): .*?\. /, "").replace(/[\s.]+$/, "")}.`;
        p.variants.push(nv); ck.add(nv.name); made.push(nv.name);
      }
      closeModal(); touch(); S.sel = p.variants.length - 1; toast(`Đã tạo ${made.length} biến thể khuôn mặt khác nhau`); return pageEditor(p.id);
    }
  };
}
const uniqueName = base => { let n = base, i = 2; const names = new Set(S.project.variants.map(v => v.name)); while (names.has(n)) n = base + " " + i++; return n; };
// ---------------------------------------------------------------- Điền từ file / bảng
function downloadText(name, text, type = "text/csv;charset=utf-8") {
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 3000);
}
const isEmptyVal = x => x == null || (Array.isArray(x) ? !x.length : !String(x).trim());
function tableFromText(text) {
  const t = parseCSV(text); if (t.length < 2) throw new Error("Bảng cần ít nhất 2 dòng (dòng đầu là tên cột)");
  const cols = t[0].map(s => s.trim());
  return { cols, rows: t.slice(1).map(r => cols.map((_, i) => r[i] ?? "")) };
}
function tableFromJson(text) {
  let d = JSON.parse(text.replace(/^﻿/, "")); d = Array.isArray(d) ? d : (d.variants || []);
  if (!d.length) throw new Error("File JSON phải là danh sách biến thể");
  const cols = [...new Set(d.flatMap(o => Object.keys(o)))];
  return { cols, rows: d.map(o => cols.map(c => o[c] ?? "")) };
}
async function readTableFile(file) {
  if (/\.xlsx$/i.test(file.name)) {
    const buf = new Uint8Array(await file.arrayBuffer()); let bin = "";
    for (let i = 0; i < buf.length; i += 0x8000) bin += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
    return api("parse-xlsx", { body: { b64: btoa(bin) } });
  }
  const text = await file.text();
  return /\.json$/i.test(file.name) ? tableFromJson(text) : tableFromText(text);
}
function fillTargets(T) {
  const t = [{ id: "name", label: "Tên biến thể", names: ["name", "ten", "tenbienthe", "bienthe"] }];
  T.fields.forEach(f => { const full = `${GROUP_LABEL(T, f.group)} · ${f.label}`; t.push({ id: f.key, label: full, names: [normKey(f.key), normKey(f.label), normKey(full), normKey(f.group + f.label)] }); });
  Object.entries(T.series || {}).forEach(([pre, n]) => {
    if (pre === "LUOT") t.push({ id: "LUOT", label: "Lời thoại (danh sách lượt, từ JSON)", names: ["luot"], array: true });
    else { t.push({ id: pre, label: `${pre} (danh sách, từ JSON)`, names: [normKey(pre)], array: true }); for (let i = 1; i <= n; i++) t.push({ id: `${pre}_${i}`, label: `${pre}_${i}`, names: [normKey(`${pre}_${i}`), normKey(pre + i)], elem: [pre, i - 1] }); }
  });
  return t;
}
function autoMap(cols, targets) {
  const used = new Set();
  return cols.map(c => { const k = normKey(c); const t = targets.find(x => !used.has(x.id) && (x.names.includes(k) || normKey(x.id) === k)); if (t) used.add(t.id); return t ? t.id : ""; });
}
// áp bảng vào các biến thể; dry=true chỉ đếm
function applyFill(table, map, opt, dry) {
  const p = S.project, T = typ(p.template), targets = fillTargets(T), byId = Object.fromEntries(targets.map(t => [t.id, t]));
  const nameCol = map.indexOf("name"), base = curV();
  let cells = 0, updated = new Set(), added = 0;
  const variants = dry ? clone(p.variants) : p.variants, ck = S.checked[p.id];
  const setCell = (v, tid, val, over) => {
    const t = byId[tid]; if (!t || tid === "name" || isEmptyVal(val)) return 0;
    if (t.elem) { const [pre, i] = t.elem, arr = v[pre] = v[pre] || []; if (!over && !isEmptyVal(arr[i])) return 0; arr[i] = String(val); return 1; }
    if (t.array) { if (!Array.isArray(val)) return 0; if (!over && !isEmptyVal(v[tid])) return 0; v[tid] = clone(val); return 1; }
    if (!over && !isEmptyVal(v[tid])) return 0; v[tid] = String(val); return 1;
  };
  table.rows.forEach((row, ri) => {
    const nm = nameCol >= 0 ? String(row[nameCol] ?? "").trim() : "";
    let v = opt.match === "name" && nm ? variants.find(x => normKey(x.name) === normKey(nm)) : (opt.match === "order" ? variants[ri] : undefined);
    if (opt.match === "order" && ri >= p.variants.length) v = undefined;
    if (v) { let n = 0; map.forEach((tid, ci) => { if (tid) n += setCell(v, tid, row[ci], opt.over); }); cells += n; if (n) updated.add(v.name); return; }
    if (!opt.add) return;
    const nv = fillVariant({ ...clone(base), name: "x" }, T);
    T.fields.forEach(f => { if (!(f.key in base)) nv[f.key] = ""; });
    let n = 0; map.forEach((tid, ci) => { if (tid) n += setCell(nv, tid, row[ci], true); });
    if (!n && !nm) return;
    const nn = nm || "Biến thể " + (variants.length + 1);
    let final = nn, k = 2; const names = new Set(variants.map(x => x.name)); while (names.has(final)) final = nn + " " + k++;
    nv.name = final; if (T.series.LUOT && isEmptyVal(nv.LUOT)) nv.LUOT = clone(base.LUOT || []);
    variants.push(nv); added++; cells += n; if (!dry) ck.add(final);
  });
  return { cells, updated: updated.size, added };
}
function fillModal() {
  const p = S.project, T = typ(p.template), targets = fillTargets(T);
  let table = null, map = [], opt = { match: "name", over: false, add: true };
  const sample = (c, i) => [...new Set(table.rows.map(r => r[i]).filter(x => !isEmptyVal(x)).slice(0, 2).map(x => Array.isArray(x) ? `[${x.length} mục]` : String(x).slice(0, 40)))].join(" · ");
  const sum = () => { const r = applyFill(table, map, opt, true); const el = $("#fsum"); if (el) { el.innerHTML = `<span class="tag ${r.cells || r.added ? "ok" : "mute"}">${r.cells} ô được điền</span><span class="tag">${r.updated} biến thể cập nhật</span><span class="tag">${r.added} biến thể mới</span>`; $("#fok").disabled = !(r.cells || r.added); } };
  const seg = (k, items) => `<div class="seg">${items.map(([v, l]) => `<button data-opt="${k}" data-v="${v}" class="${String(opt[k]) === String(v) ? "on" : ""}">${l}</button>`).join("")}</div>`;
  const draw = () => {
    openModal(`<div class="mbox wide"><h2>Điền từ file hoặc bảng <button class="ib" id="mx">${ico("x")}</button></h2>
      <div class="row2" style="flex-wrap:wrap;margin-bottom:12px"><label class="btn" style="cursor:pointer">${ico("up2")}Chọn file<input type="file" id="ff" accept=".csv,.tsv,.txt,.json,.xlsx" hidden></label>
        <button class="btn" id="fpaste">Dán bảng từ Excel</button><button class="btn ghost" id="ftpl">${ico("dl")}Tải bảng mẫu</button><span style="color:var(--dim);font-size:12.5px">CSV, XLSX, JSON · dòng đầu là tên cột</span></div>
      <textarea id="fpt" class="hidden" rows="6" spellcheck="false" placeholder="Dán từ Excel hoặc Google Sheets (dòng đầu là tên cột)" style="width:100%;font:12.5px/1.5 'Cascadia Mono',Consolas,monospace;background:var(--bg);border:1px solid var(--line2);border-radius:10px;padding:10px;outline:none;margin-bottom:12px"></textarea>
      ${table ? `<div style="color:var(--mute);margin-bottom:8px">${table.rows.length} dòng · ${table.cols.length} cột. Chọn cột nào điền vào trường nào:</div>
      <div class="gridwrap" style="max-height:260px;margin-bottom:14px"><table class="gt"><thead><tr><th style="min-width:180px">Cột trong file</th><th style="min-width:240px">Ví dụ</th><th style="min-width:260px">Điền vào</th></tr></thead><tbody>${table.cols.map((c, i) => `<tr><td style="padding:9px 11px">${esc(c)}</td><td style="padding:9px 11px;color:var(--mute)">${esc(sample(c, i))}</td><td><select class="cell" data-map="${i}"><option value="">— không dùng —</option>${targets.map(t => `<option value="${t.id}" ${map[i] === t.id ? "selected" : ""}>${esc(t.label)}</option>`).join("")}</select></td></tr>`).join("")}</tbody></table></div>
      <div class="row2" style="flex-wrap:wrap;gap:22px;margin-bottom:14px"><div><div class="lblsm">Ghép dòng với biến thể</div>${seg("match", [["name", "Theo tên"], ["order", "Theo thứ tự"]])}</div>
        <div><div class="lblsm">Ô đã có chữ</div>${seg("over", [[false, "Giữ nguyên"], [true, "Ghi đè"]])}</div><div><div class="lblsm">Dòng không khớp</div>${seg("add", [[true, "Thêm biến thể mới"], [false, "Bỏ qua"]])}</div></div>
      <div class="row2" id="fsum" style="gap:8px"></div>` : ""}
      <div class="mact"><button class="btn" id="mx2">Huỷ</button><button class="btn primary" id="fok" ${table ? "" : "disabled"}>Áp dụng</button></div></div>`);
    if (table) sum();
  };
  const load = tb => { table = tb; map = autoMap(tb.cols, targets); opt.match = map.includes("name") ? "name" : "order"; draw(); };
  draw();
  $("#modal").onclick = e => {
    let x;
    if (e.target.id === "modal" || e.target.closest("#mx") || e.target.id === "mx2") return closeModal();
    if (e.target.closest("#fpaste")) { const t = $("#fpt"); t.classList.toggle("hidden"); if (!t.classList.contains("hidden")) { t.focus(); t.onpaste = () => setTimeout(() => { try { load(tableFromText(t.value)); } catch (er) { toast(er.message, 1); } }, 50); t.onchange = () => { try { load(tableFromText(t.value)); } catch (er) { toast(er.message, 1); } }; } return; }
    if (e.target.closest("#ftpl")) {
      const labels = ["Tên", ...T.fields.map(f => `${GROUP_LABEL(T, f.group)} · ${f.label}`)];
      const cell = v => /[",\n;\t]/.test(v) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v);
      downloadText(`${p.name.replace(/[^\w-]+/g, "-")}-bang-mau.csv`, "﻿" + [labels, ...p.variants.map(v => [v.name, ...T.fields.map(f => v[f.key] ?? "")])].map(r => r.map(cell).join(",")).join("\r\n"));
      return;
    }
    if ((x = e.target.closest("[data-opt]"))) { opt[x.dataset.opt] = x.dataset.v === "true" ? true : x.dataset.v === "false" ? false : x.dataset.v; const keep = $("#fpt") && $("#fpt").value; draw(); if (keep) { $("#fpt").value = keep; } return; }
    if (e.target.closest("#fok")) {
      const r = applyFill(table, map, opt, false); touch(); closeModal(); toast(`Đã điền ${r.cells} ô, thêm ${r.added} biến thể`); pageEditor(p.id);
    }
  };
  $("#modal").onchange = async e => {
    const el = e.target;
    if (el.dataset.map !== undefined) { map[+el.dataset.map] = el.value; return sum(); }
    if (el.id === "ff") { const f = el.files[0]; el.value = ""; if (!f) return; try { load(await readTableFile(f)); } catch (er) { toast(er.message, 1); } }
  };
}

async function runSelected() {
  await save();
  const p = S.project, T = typ(p.template), names = p.variants.filter(v => S.checked[p.id].has(v.name)).map(v => v.name), need = (T.series || {}).LUOT;
  const dup = names.find((n, i) => names.indexOf(n) !== i); if (dup) return toast(`Trùng tên biến thể: ${dup}`, 1);
  for (const v of p.variants.filter(x => names.includes(x.name))) {
    if (need && !(v.LUOT || []).length) return toast(`"${v.name}" chưa có lượt thoại nào`, 1);
    const miss = T.fields.find(f => !f.optional && !String(v[f.key] ?? "").trim());
    if (miss) return toast(`"${v.name}" chưa điền: ${miss.label}`, 1);
    for (const [pre, num] of Object.entries(T.series || {})) if (pre !== "LUOT" && Array.from({ length: num }, (_, i) => (v[pre] || [])[i]).some(x => !String(x || "").trim())) return toast(`"${v.name}" chưa điền đủ ${pre}`, 1);
  }
  try {
    const r = await api("queue/add", { body: { project: p.id, variants: names } });
    S.qsel = S.qsel || new Set(); r.ids.forEach(id => S.qsel.add(id));
    toastLink(`Đã thêm ${r.ids.length} biến thể vào hàng đợi`, "#/run", "Mở hàng đợi"); pollQueue();
  } catch (e) { toast(e.message, 1); }
}

// ---------------------------------------------------------------- Chạy (hàng đợi)
const STATE = { wait: "Chờ", image: "Ảnh", video: "Video", cut: "Cắt", done: "Xong", error: "Lỗi" };
const QSTATE = { queued: "Chờ", waiting: "Chờ luồng", running: "Đang chạy", done: "Xong", error: "Lỗi", stopped: "Đã dừng" };
const fmtDur = s => { s = Math.max(0, Math.round(s)); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return (h ? h + ":" + String(m).padStart(2, "0") : m) + ":" + String(x).padStart(2, "0"); };
const srvNow = () => S.q ? S.q.now + (Date.now() - S.q.at) / 1000 : Date.now() / 1000;
const itemSecs = it => it.state === "running" ? srvNow() - it.started : (it.elapsed || 0);
const sceneSecs = (sc, it) => sc.t1 && sc.t0 ? sc.t1 - sc.t0 : (sc.t0 && it.state === "running" ? srvNow() - sc.t0 : 0);
const batchSecs = () => { const b = S.q && S.q.batch; if (!b || !b.started) return 0; return (b.state === "running" ? srvNow() : b.ended) - b.started; };
function batchStats() {
  const q = S.q, b = q.batch, ids = new Set(b.ids || []);
  const items = q.items.filter(i => ids.has(i.id) && i.kind === "gen");
  const times = items.flatMap(i => i.scenes.filter(s => s.t0 && s.t1).map(s => s.t1 - s.t0));
  const avg = times.length ? times.reduce((a, x) => a + x, 0) / times.length : 0;
  let remain = 0;
  items.forEach(i => { if (i.state !== "done") remain += Math.max(0, (i.total || i.scenes.length) - i.scenes.filter(s => s.state === "done").length); });
  return { avg, eta: avg && b.state === "running" ? avg * remain / Math.max(1, Math.min(b.parallel || 1, S.q.items.filter(i => i.state === "running" || i.state === "queued").length)) : 0, doneScenes: times.length, remain };
}
async function pollQueue() {
  try {
    const q = await api("queue"); q.at = Date.now();
    const sig = JSON.stringify(q.items) + q.batch.state + q.busy;
    const changed = !S.q || sig !== S.qsig;
    S.q = q; S.qsig = sig;
    if (changed) { nav(); if (S.route.page === "run") drawRun(); }
  } catch { }
  clearTimeout(S.qT); S.qT = setTimeout(pollQueue, S.q && S.q.busy ? 1000 : 2500);
}
setInterval(() => {
  if (!S.q) return;
  document.querySelectorAll("[data-tm]").forEach(el => {
    const [k, a, b] = el.dataset.tm.split(":");
    if (k === "batch") el.textContent = fmtDur(batchSecs());
    else if (k === "item") { const it = S.q.items.find(x => x.id === a); if (it) el.textContent = fmtDur(itemSecs(it)); }
    else if (k === "scene") { const it = S.q.items.find(x => x.id === a), sc = it && it.scenes.find(x => x.n === +b); if (sc) { const t = sceneSecs(sc, it); el.textContent = t ? fmtDur(t) : ""; } }
    else if (k === "eta") { const st = batchStats(); const left = st.eta ? Math.max(0, st.eta - (srvNow() - (S.q.stampEta || srvNow()))) : 0; el.textContent = st.eta ? "~" + fmtDur(st.eta) : "—"; }
  });
}, 1000);
function pageRun() { setTop("Chạy"); S.qsig = ""; if (S.q) drawRun(); else $("#view").innerHTML = ""; pollQueue(); }
const itemThumb = it => { const sc = [...it.scenes].reverse().find(s => s.thumb); return sc ? media(it.project, it.variant, sc.thumb) + "?t=" + (sc.secs || sc.pct || 0) : ""; };

function drawRun() {
  const q = S.q, v = $("#view"); if (!q) return;
  if (S.qview && !q.items.find(i => i.id === S.qview)) S.qview = null;
  const keepY = v.scrollTop;
  if (S.qview) drawDetail(q.items.find(i => i.id === S.qview)); else drawQueue();
  v.scrollTop = keepY;
}
function drawQueue() {
  const q = S.q, v = $("#view"), sel = S.qsel || (S.qsel = new Set());
  [...sel].forEach(id => { if (!q.items.find(i => i.id === id)) sel.delete(id); });
  const busyState = st => st === "running" || st === "waiting", runnable = id => { const it = q.items.find(i => i.id === id); return it && !busyState(it.state); };
  const nSel = [...sel].filter(runnable).length;
  setTop("Hàng đợi", q.busy ? `<button class="btn danger" id="qstop">${ico("stop")}Dừng</button>` : "");
  if (!q.items.length) { v.innerHTML = `<div class="empty"><div class="big">${ico("bolt")}</div><div>Hàng đợi trống</div><div style="max-width:380px;font-size:13px">Mở một dự án, tick các biến thể rồi bấm <b>Thêm vào hàng đợi</b>. Quay lại đây để chọn và bấm Bắt đầu.</div><a class="btn primary" data-go="#/">${ico("folder")}Chọn dự án</a></div>`; return; }
  const st = batchStats(), running = q.busy, b = q.batch;
  const groups = []; q.items.forEach(it => { let g = groups.find(x => x.id === it.project); if (!g) groups.push(g = { id: it.project, name: it.pname, items: [] }); g.items.push(it); });
  const open = S.qopen || (S.qopen = {});
  const card = it => {
    const done = it.kind === "post" ? 0 : it.scenes.filter(s => s.state === "done").length, tot = it.total || it.scenes.length || 0, pct = it.kind === "post" ? (it.state === "done" ? 100 : it.state === "running" ? 60 : 0) : (tot ? Math.round(done / tot * 100) : 0);
    const th = itemThumb(it), checked = sel.has(it.id);
    return `<div class="qcard ${it.state}" data-qopen="${it.id}">
      <div class="qth">${th ? `<img loading="lazy" src="${th}" alt="">` : `<div class="qph">${ico(it.kind === "post" ? "wand" : "film")}</div>`}
        <span class="chk qchk ${checked && !busyState(it.state) ? "on" : ""} ${busyState(it.state) ? "off" : ""}" data-qchk="${it.id}">${checked && !busyState(it.state) ? ico("check") : ""}</span>
        <span class="tag qst ${it.state === "done" ? "ok" : it.state === "error" ? "bad" : it.state === "stopped" ? "warn" : it.state === "running" ? "" : "mute"}">${it.state === "running" ? '<i class="spin sm"></i>' : ""}${QSTATE[it.state]}</span>
        ${busyState(it.state) ? `<button class="ib qrm qstp" data-qstp="${it.id}" title="${it.state === "waiting" ? "Bỏ chờ" : "Dừng video này"}" ${it.stopping ? "disabled" : ""}>${ico("stop")}</button>` : `<button class="ib qrm" data-qrm="${it.id}" title="Xoá khỏi hàng đợi">${ico("x")}</button>`}</div>
      <div class="qbd"><div class="qnm" title="${esc(it.variant)}">${it.kind === "post" ? "Hậu kỳ · " : ""}${esc(it.variant)}</div>
        <div class="mini"><div style="width:${pct}%"></div></div>
        <div class="st"><span>${it.kind === "post" ? "" : done + "/" + tot + " cảnh"}</span><span class="tm">${ico("clock")}<b data-tm="item:${it.id}">${it.started ? fmtDur(itemSecs(it)) : "0:00"}</b></span></div></div></div>`;
  };
  const par = (S.boot.settings && S.boot.settings.parallel) || 1;
  v.innerHTML = `<div class="qbar"><button class="btn primary" id="qgo" ${nSel ? "" : "disabled"}>${ico("play")}${running ? "Chạy thêm" : "Bắt đầu"}${nSel ? " (" + nSel + ")" : ""}</button>
      <label class="par" title="Số video chạy cùng lúc (tối đa theo số tài khoản Muse; chạy nhiều hơn dễ bị giới hạn lượt)">Song song <select id="qpar">${[1, 2, 3, 4, 5, 6].map(n => `<option value="${n}" ${n === par ? "selected" : ""}>${n}</option>`).join("")}</select></label>
      <button class="btn" id="qall">Chọn tất cả</button><button class="btn ghost" id="qnone">Bỏ chọn</button><button class="btn ghost" id="qclr">Xoá mục đã xong</button><span class="grow"></span>
      <div class="qstats"><span title="Tổng thời gian chạy của lượt này">${ico("clock")}Tổng <b data-tm="batch">${fmtDur(batchSecs())}</b></span>
        <span title="Trung bình mỗi cảnh">TB/cảnh <b>${st.avg ? fmtDur(st.avg) : "—"}</b></span><span title="Ước tính còn lại">Còn <b data-tm="eta">${st.eta ? "~" + fmtDur(st.eta) : "—"}</b></span></div></div>
    ${groups.map(g => {
      const isOpen = open[g.id] !== false, nd = g.items.filter(i => i.state === "done").length, allSel = g.items.every(i => sel.has(i.id) || busyState(i.state));
      return `<section class="qgrp"><header class="qgh" data-qtog="${esc(g.id)}"><span class="chk ${allSel ? "on" : ""}" data-qgsel="${esc(g.id)}" title="Chọn cả nhóm">${allSel ? ico("check") : ""}</span><span class="chev ${isOpen ? "open" : ""}">${ico("chev")}</span><b>${esc(g.name)}</b><span class="tag mute">${nd}/${g.items.length} xong</span>
        <span class="grow"></span></header>
        ${isOpen ? `<div class="qgrid">${g.items.map(card).join("")}</div>` : ""}</section>`;
    }).join("")}`;
  $("#qpar").onchange = async e => { const n = +e.target.value; S.boot.settings.parallel = n; try { await api("settings", { body: { parallel: n } }); pollQueue(); } catch (er) { toast(er.message, 1); } };
  v.onclick = async e => {
    let x;
    if (e.target.closest("#qstop")) { toast("Đang dừng tất cả…"); await api("stop", { body: {} }); return pollQueue(); }
    if (e.target.closest("#qgo")) { try { const ids = [...sel].filter(runnable); await api("queue/start", { body: { ids, parallel: +($("#qpar").value || 1) } }); S.boot.settings.parallel = +$("#qpar").value; ids.forEach(i => sel.delete(i)); await pollQueue(); } catch (er) { toast(er.message, 1); } return; }
    if (e.target.closest("#qall")) { q.items.forEach(i => { if (!busyState(i.state)) sel.add(i.id); }); return drawQueue(); }
    if ((x = e.target.closest("[data-qstp]"))) { e.stopPropagation(); await api("stop", { body: { id: x.dataset.qstp } }); return pollQueue(); }
    if (e.target.closest("#qnone")) { sel.clear(); return drawQueue(); }
    if (e.target.closest("#qclr")) { await api("queue/remove", { body: { ids: q.items.filter(i => i.state === "done").map(i => i.id) } }); await pollQueue(); return; }
    if ((x = e.target.closest("[data-qrm]"))) { e.stopPropagation(); await api("queue/remove", { body: { ids: [x.dataset.qrm] } }); await pollQueue(); return; }
    if ((x = e.target.closest("[data-qchk]"))) { e.stopPropagation(); if (x.classList.contains("off")) return; const id = x.dataset.qchk; sel.has(id) ? sel.delete(id) : sel.add(id); return drawQueue(); }
    if ((x = e.target.closest("[data-qgsel]"))) { e.stopPropagation(); const g = groups.find(z => z.id === x.dataset.qgsel), all = g.items.every(i => sel.has(i.id) || busyState(i.state)); g.items.forEach(i => { if (!busyState(i.state)) all ? sel.delete(i.id) : sel.add(i.id); }); return drawQueue(); }
    if ((x = e.target.closest("[data-qtog]"))) { const id = x.dataset.qtog; open[id] = open[id] === false; return drawQueue(); }
    if ((x = e.target.closest("[data-qopen]"))) { S.qview = x.dataset.qopen; S.runSel = null; return drawRun(); }
  };
}

const REDO_CHIPS = ["Nhân vật còn lại ngậm miệng hoàn toàn, không mấp máy theo", "Nhân vật còn lại không gật đầu, không cười, không nhìn theo", "Giọng nói tự nhiên, nhiều cảm xúc hơn", "Biểu cảm của người nói rõ và sinh động hơn", "Giữ đúng khuôn mặt và quần áo như khung đầu", "Nói rõ từng từ, không bỏ sót chữ đầu câu"];
function redoModal(it, n) {
  const sc = (it.scenes || []).find(x => x.n === n) || {}, old = (it.notes || {})[String(n)] || "";
  openModal(`<div class="mbox"><h2>Gen lại cảnh ${n} <button class="ib" id="mx">${ico("x")}</button></h2>
    <p style="color:var(--mute);margin-bottom:12px">Cảnh ${n}: <i>${esc(sc.text || "")}</i><br>Cảnh này và các cảnh sau sẽ được gen lại (các cảnh sau nối tiếp từ khung cuối của cảnh này).${it.state === "running" ? "<br><b>Video đang chạy sẽ được dừng trước rồi gen lại từ cảnh này.</b>" : ""}</p>
    <div class="f"><label>Yêu cầu sửa cho lần gen lại này <small style="opacity:.6">(tuỳ chọn, viết tiếng Việt hay tiếng Anh đều được)</small></label>
      <textarea id="rn" rows="4" placeholder="Ví dụ: Người học không được mấp máy miệng khi robot nói; giọng robot vui hơn…">${esc(old)}</textarea></div>
    <div class="att" style="margin-top:8px">${REDO_CHIPS.map((c, i) => `<span class="addatt" data-chip="${i}" style="cursor:pointer">${esc(c)}</span>`).join("")}</div>
    <div class="row2" style="margin-top:18px;justify-content:flex-end"><button class="btn ghost" id="rc">Huỷ</button><button class="btn primary" id="rok">${ico("redo")}Gen lại</button></div></div>`);
  $("#modal").onclick = async e => {
    if (e.target.closest("#mx, #rc")) return closeModal();
    const ch = e.target.closest("[data-chip]");
    if (ch) { const ta = $("#rn"), t = REDO_CHIPS[+ch.dataset.chip]; if (!ta.value.includes(t)) ta.value = (ta.value.trim() ? ta.value.trim() + "; " : "") + t; return; }
    if (e.target.closest("#rok")) {
      const note = $("#rn").value.trim();
      try { await api("queue/redo", { body: { id: it.id, from: n, note } }); closeModal(); toast(note ? `Đã đưa cảnh ${n} vào hàng chờ gen lại kèm yêu cầu sửa` : `Đã đưa cảnh ${n} vào hàng chờ gen lại`); await pollQueue(); }
      catch (er) { toast(er.message, 1); }
    }
  };
}
function drawDetail(it) {
  const q = S.q, v = $("#view"), running = it.state === "running", sc = it.scenes || [], done = sc.filter(s => s.state === "done").length, tot = it.total || sc.length;
  setTop(esc(it.variant), `<span class="tag ${it.state === "done" ? "ok" : it.state === "error" ? "bad" : it.state === "stopped" ? "warn" : ""}">${QSTATE[it.state]}</span><span class="tm big">${ico("clock")}<b data-tm="item:${it.id}">${fmtDur(itemSecs(it))}</b></span>`
    + (running ? `<button class="btn danger" id="dstop" ${it.stopping ? "disabled" : ""}>${ico("stop")}${it.stopping ? "Đang dừng…" : "Dừng"}</button>` : it.state === "waiting" ? `<button class="btn" id="dstop">${ico("stop")}Bỏ chờ</button>` : (it.state !== "done" ? `<button class="btn primary" id="dgo">${ico("play")}${it.state === "queued" ? "Bắt đầu" : "Chạy tiếp"}</button>` : "")));
  const fin = it.final, raw = it.raw && (it.state === "done" || it.kind === "post");
  let res = "";
  if (fin || (raw && it.kind === "gen" && it.state === "done")) {
    const f = fin || "raw.mp4";
    res = `<div class="card result"><video src="${media(it.project, it.variant, f)}?t=${Math.round(it.ended)}" controls preload="metadata"></video><div style="display:flex;flex-direction:column;gap:12px"><div><span class="tag ${fin ? "ok" : ""}">${fin ? "Video hoàn thiện" : "Video thô"}</span>${fin ? `<span class="tag mute" title="Bản cuối mang tên biến thể, nằm trong thư mục xuất và cạnh final.mp4">${esc(it.variant)}.mp4</span>` : ""}</div><h3 style="font-size:17px">${esc(it.variant)}</h3>
      <div style="display:flex;gap:10px;flex-wrap:wrap">${!running ? `<button class="btn primary" data-post="1">${ico("wand")}${fin ? "Hậu kỳ lại" : "Hậu kỳ"}</button>` : ""}<button class="btn" data-openf="1">${ico("folderopen")}Mở thư mục</button></div></div></div>`;
  }
  if (it.kind === "post" && running) res = `<div class="card result" style="grid-template-columns:1fr"><div style="display:flex;gap:16px;align-items:center"><div class="spin"></div><div>Đang hậu kỳ — căn phụ đề, ghép logo và end card…</div></div></div>`;
  const grid = it.kind === "gen" ? `<div class="scenes">${sc.map(s => {
    const st = s.state, pc = st === "done" ? 100 : st === "wait" ? 0 : (s.pct || 0), act = ["image", "video", "cut"].includes(st);
    const thumb = s.thumb ? `<img loading="lazy" src="${media(it.project, it.variant, s.thumb)}?t=${s.secs || s.pct || 0}">` : (act ? `<div class="spin"></div>` : ico("img"));
    const t = sceneSecs(s, it);
    return `<div class="sc ${st} ${act ? "active" : ""}"><div class="th">${thumb}<span class="num">${s.n}</span><span class="wh" style="background:var(--${s.who === "hoc" ? "hoc" : "day"})"></span>${s.clip ? `<div class="play" data-play="${s.clip}">${ico("play")}</div>` : ""}</div>
      <div class="bd"><div class="tx">${esc(s.text)}</div><div class="mini"><div style="width:${pc}%"></div></div><div class="st"><span>${STATE[st] || st}${["image", "video"].includes(st) && s.pct ? " " + s.pct + "%" : ""}${s.note ? " · " + esc(s.note) : ""}</span><span class="tm"><b data-tm="scene:${it.id}:${s.n}">${t ? fmtDur(t) : ""}</b>${s.secs ? ` · ${s.secs}s` : ""}</span></div></div>
      ${st === "done" || (st === "error" && !running) ? `<button class="ib redo" data-redo="${s.n}" title="${running ? "Dừng video đang chạy và gen lại từ cảnh này" : "Gen lại từ cảnh này (có thể thêm yêu cầu sửa)"}">${ico("redo")}</button>` : ""}</div>`;
  }).join("")}</div>` : "";
  const err = it.error ? `<div class="tag bad" style="margin-bottom:14px;white-space:normal">${esc(it.error)}</div>` : "";
  const logs = (it.log || []).slice(-60).map(l => `<div class="${l.level}">${l.t}  ${esc(l.msg)}</div>`).join("");
  v.innerHTML = `<div class="runhead"><button class="btn ghost" id="dback">${ico("back")}Hàng đợi</button><span class="tag mute">${esc(it.pname)}</span><div class="bar"><div style="width:${it.kind === "post" ? (running ? 60 : 100) : (tot ? Math.round(done / tot * 100) : 0)}%"></div></div>${it.kind === "gen" ? `<span class="tag">${done}/${tot}</span>` : ""}</div>${err}${res}${grid}
    <details ${S.logOpen ? "open" : ""} id="logd"><summary style="cursor:pointer;color:var(--mute);margin-top:20px">Nhật ký</summary><div class="log">${logs}</div></details>`;
  const nl = $(".log"); if (nl) nl.scrollTop = nl.scrollHeight;
  $("#logd").ontoggle = e => { S.logOpen = e.target.open; };
  v.onclick = async e => {
    let x;
    if (e.target.closest("#dback")) { S.qview = null; return drawRun(); }
    if (e.target.closest("#dstop")) { toast("Đang dừng video này…"); await api("stop", { body: { id: it.id } }); return pollQueue(); }
    if (e.target.closest("#dgo")) { try { await api("queue/start", { body: { ids: [it.id] } }); await pollQueue(); } catch (er) { toast(er.message, 1); } return; }
    if ((x = e.target.closest("[data-play]"))) return playModal(media(it.project, it.variant, x.dataset.play), it.variant);
    if ((x = e.target.closest("[data-redo]"))) return redoModal(it, +x.dataset.redo);
    if (e.target.closest("[data-post]")) return postModal(it.project, it.variant);
    if (e.target.closest("[data-openf]")) return api("open", { body: { project: it.project, variant: it.variant } });
  };
}
function playModal(src, title) { openModal(`<div class="mbox" style="width:min(460px,100%)"><h2>${esc(title)}<button class="ib" id="mx">${ico("x")}</button></h2><video class="vid" src="${src}" controls autoplay></video></div>`); $("#mx").onclick = closeModal; }

async function postModal(pid, variant) {
  const s = await api("settings");
  const row = (k, label, val) => `<div class="f"><label>${label}</label><div class="pick"><input class="input" id="pk-${k}" readonly value="${esc(val || "")}" placeholder="Không dùng"><button class="btn sm" data-pick="${k}">Chọn</button><button class="ib" data-clr="${k}">${ico("x")}</button></div></div>`;
  openModal(`<div class="mbox"><h2>Hậu kỳ <button class="ib" id="mx">${ico("x")}</button></h2>
    <p style="color:var(--mute);margin-bottom:16px">Phụ đề tự tạo từ lời thoại, căn theo giọng nói thật.</p>
    ${row("logo", "Logo (.mov / .png)", s.logo)}${row("endcard", "End card (.mp4)", s.endcard)}
    <div class="mact"><button class="btn" id="mx2">Huỷ</button><button class="btn primary" id="pgo">${ico("wand")}Xuất video</button></div></div>`);
  $("#modal").onclick = async e => {
    let x;
    if (e.target.id === "modal" || e.target.closest("#mx") || e.target.id === "mx2") return closeModal();
    if ((x = e.target.closest("[data-pick]"))) { const r = await api("pick", { body: { kind: "file" } }); if (r.path) $("#pk-" + x.dataset.pick).value = r.path; }
    if ((x = e.target.closest("[data-clr]"))) $("#pk-" + x.dataset.clr).value = "";
    if (e.target.closest("#pgo")) {
      try { const r = await api("post", { body: { project: pid, variant, logo: $("#pk-logo").value, endcard: $("#pk-endcard").value } }); closeModal(); S.qview = r.id; location.hash = "#/run"; if (S.route.page === "run") { await pollQueue(); drawRun(); } } catch (er) { toast(er.message, 1); }
    }
  };
}

// ---------------------------------------------------------------- Kết quả
async function pageResults() {
  setTop("Kết quả");
  S.results = await api("results");
  if (!S.results.length) { $("#view").innerHTML = `<div class="empty"><div class="big">${ico("film")}</div><div>Chưa có video</div></div>`; return; }
  $("#view").innerHTML = `<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(210px,1fr))">${S.results.map((r, i) => {
    const w = r.final ? "final" : "raw";
    return `<div class="card rcard ${r.posting ? "posting" : ""}"><div class="po" data-play="${i}"><img loading="lazy" src="${media(r.project, r.variant, "poster-" + w + ".jpg")}?t=${r.mtime}" alt=""><span class="badge tag ${r.posting ? "" : r.final ? "ok" : "mute"}">${r.posting ? '<i class="spin sm"></i>Đang hậu kỳ…' : r.final ? "Hoàn thiện" : "Thô"}</span><div class="play">${ico("play")}</div></div>
      <div class="bd"><div><div class="nm" title="${esc(r.variant)}">${esc(r.variant)}</div><div class="sub">${esc(r.project_name)} · ${r.secs}s · ${(r.size / 1048576).toFixed(0)} MB · ${ago(r.mtime)}</div></div>
      <div class="row">${r.posting ? `<button class="btn sm" disabled><i class="spin sm"></i>Đang hậu kỳ…</button>` : `<button class="btn sm" data-post="${i}">${ico("wand")}${r.final ? "Xuất lại" : "Hậu kỳ"}</button>`}${r.post_error ? `<span class="tag bad" title="${esc(r.post_error)}" style="margin-left:6px">Hậu kỳ lỗi</span>` : ""}<span style="flex:1"></span><button class="ib" data-open="${i}" title="Mở thư mục">${ico("folderopen")}</button><button class="ib danger" data-del="${i}" title="Xoá">${ico("trash")}</button></div></div></div>`;
  }).join("")}</div>`;
  clearTimeout(S.resT);
  if (S.results.some(r => r.posting)) S.resT = setTimeout(() => { if (S.route && S.route.page === "results") pageResults(); }, 2000);  // đang hậu kỳ: tự cập nhật đến khi xong
  $("#view").onclick = async e => {
    let x;
    if ((x = e.target.closest("[data-play]"))) { const r = S.results[+x.dataset.play]; return playModal(media(r.project, r.variant, (r.final ? "final" : "raw") + ".mp4"), r.variant); }
    if ((x = e.target.closest("[data-post]"))) { const r = S.results[+x.dataset.post]; return postModal(r.project, r.variant); }
    if ((x = e.target.closest("[data-open]"))) { const r = S.results[+x.dataset.open]; return api("open", { body: { project: r.project, variant: r.variant } }); }
    if ((x = e.target.closest("[data-del]"))) { const r = S.results[+x.dataset.del]; if (confirm("Xoá video này và các file trung gian?")) { await api("delete-result", { body: { project: r.project, variant: r.variant } }); pageResults(); } }
  };
}

// ---------------------------------------------------------------- API Muse (bảng điều khiển LUO-API)
const NOTE_VI = [[/会话有效/, "Phiên còn hạn, dùng được"], [/等待生成超时|未出现新的生成结果/, "Hết thời gian chờ, chưa ra kết quả"], [/认证失败|401/, "Đăng nhập hết hạn (401): đăng nhập lại Muse rồi cập nhật cookie"], [/已更新 cookie/, "Đã cập nhật cookie"], [/任务异常/, "Lỗi ở lần gen gần nhất"]];
const viNote = n => { for (const [re, t] of NOTE_VI) if (re.test(n || "")) return t; return n || ""; };
const TASK_VI = { queued: "Đang chờ", processing: "Đang xử lý", completed: "Xong", failed: "Lỗi", succeeded: "Xong" };
async function pageApi() {
  clearTimeout(S.apiT);
  setTop("API Muse", `<button class="btn" id="ap-ref">${ico("redo")}Làm mới</button><button class="btn" id="ap-ka" title="Gia hạn phiên đăng nhập của tất cả tài khoản">Giữ phiên tất cả</button><button class="btn primary" id="ap-add">${ico("plus")}Thêm tài khoản</button>`);
  const v = $("#view");
  let d, tk;
  try { d = await api("muse/status"); tk = (await api("muse/tasks?limit=30")).tasks || d.tasks || []; }
  catch (e) { v.innerHTML = `<div class="empty"><div class="big">${ico("server")}</div><div>Không kết nối được LUO-API</div><div style="max-width:420px;font-size:13px;color:var(--mute)">${esc(e.message)}<br>Kiểm tra địa chỉ và khoá API ở Cài đặt, và LUO-API đã chạy chưa.</div><a class="btn primary" data-go="#/settings">Mở Cài đặt</a></div>`; S.apiT = setTimeout(() => { if (S.route.page === "api") pageApi(); }, 8000); return; }
  const accs = d.accounts || [], on = accs.filter(a => a.enabled), usable = on.filter(a => a.ok !== false && ((a.quota || {}).weekly_used_pct ?? 0) < 100);
  const cnt = st => tk.filter(t => t.status === st).length, ago2 = t => t ? ago(t) : "—";
  const days = a => a.expires_at ? Math.max(0, Math.round((a.expires_at - Date.now() / 1000) / 86400)) : null;
  const warn = !usable.length ? `<div class="card sec apwarn"><b>Không còn tài khoản nào dùng được để gen video.</b> ${on.length ? "Các tài khoản đang bật đều hết hạn mức tuần hoặc lỗi đăng nhập" : "Chưa tài khoản nào được bật"}. Task mới sẽ nằm chờ ở trạng thái "Đang chờ". Bật tài khoản khác, cập nhật cookie, hoặc đợi ngày reset hạn mức.</div>` : "";
  const acc = a => { const q = a.quota || {}, pct = q.weekly_used_pct, dd = days(a), bad = a.ok === false;
    return `<div class="card apacc ${a.enabled ? "" : "off"}" data-id="${a.id}">
      <div class="aphead"><b>${esc(a.label || a.id)}</b><span class="tag mute">${a.id.slice(0, 6)}</span><span class="grow"></span>
        <span class="tag ${bad ? "bad" : a.ok ? "ok" : "mute"}">${bad ? "Lỗi đăng nhập" : a.ok ? "Phiên ổn" : "Chưa kiểm tra"}</span><div class="sw2 ${a.enabled ? "on" : ""}" data-aptog="${a.id}" title="Bật / tắt tài khoản này"></div></div>
      <div class="apq">${pct == null ? `<span class="tag mute">Chưa đo hạn mức</span>` : `<div class="apbar"><div class="${pct >= 100 ? "full" : pct >= 80 ? "hi" : ""}" style="width:${Math.min(100, pct)}%"></div></div><span>Tuần: <b>${pct}%</b>${q.weekly_reset ? " · reset " + esc(q.weekly_reset) : ""}</span>${q.extra_used_pct != null ? `<span>Extra: <b>${q.extra_used_pct}%</b>${q.extra_left ? " · " + esc(q.extra_left) : ""}</span>` : ""}<span class="mute">${esc(q.plan || "")}${q.checked_at ? " · đo " + ago(q.checked_at) : ""}</span>`}</div>
      <div class="apmeta">Dùng ${a.use_count || 0} lần · lần cuối ${ago2(a.last_used)}${dd != null ? ` · cookie còn ~${dd} ngày` : ""}</div>
      ${a.note ? `<div class="apnote ${bad ? "bad" : ""}" title="${esc(a.note)}">${esc(viNote(a.note))}</div>` : ""}
      <div class="apact"><button class="btn sm" data-aptest="${a.id}">Kiểm tra phiên</button><button class="btn sm" data-apq="${a.id}">Đo hạn mức</button><button class="btn sm" data-apck="${a.id}">Cập nhật cookie</button><button class="btn sm ghost" data-apren="${a.id}">Đổi tên</button><button class="ib danger" data-apdel="${a.id}" title="Xoá tài khoản">${ico("trash")}</button></div></div>`; };
  const task = t => `<tr><td>${ago(t.created_at)}</td><td>${esc(t.kind || "")}</td><td><span class="tag ${t.status === "completed" || t.status === "succeeded" ? "ok" : t.status === "failed" ? "bad" : t.status === "processing" ? "" : "mute"}">${TASK_VI[t.status] || esc(t.status)}</span></td><td>${t.elapsed ? Math.round(t.elapsed) + "s" : "—"}</td><td class="aperr" title="${esc(String(t.error || ""))}">${esc(String(t.error || "").slice(0, 90))}</td><td><button class="ib" data-aptd="${t.id}" title="Xoá khỏi danh sách">${ico("x")}</button></td></tr>`;
  v.innerHTML = `${warn}<div class="apsum"><div class="card"><small>Tài khoản dùng được</small><b>${usable.length}<span>/ ${accs.length}</span></b></div><div class="card"><small>Đang bật</small><b>${on.length}</b></div>
      <div class="card"><small>Task đang chờ / xử lý</small><b>${cnt("queued")}<span>/ ${cnt("processing")}</span></b></div><div class="card"><small>Task lỗi gần đây</small><b>${cnt("failed")}</b></div>
      <div class="card"><small>Trình duyệt API</small><b style="font-size:16px">${d.browser_running ? "Đang chạy" : "Chưa mở"}</b></div></div>
    <h3 class="aph">Tài khoản Muse</h3><div class="apgrid">${accs.map(acc).join("") || `<div class="empty" style="grid-column:1/-1"><div>Chưa có tài khoản. Bấm "Thêm tài khoản" và dán cookie.</div></div>`}</div>
    <h3 class="aph">Task gần đây</h3><div class="card" style="padding:0"><table class="gt" style="width:100%"><thead><tr><th>Lúc</th><th>Loại</th><th>Trạng thái</th><th>Thời gian</th><th>Lỗi</th><th></th></tr></thead><tbody>${tk.map(task).join("") || `<tr><td colspan="6" style="padding:18px;color:var(--mute)">Chưa có task</td></tr>`}</tbody></table></div>`;
  const run = async (btn, fn, ok) => { if (btn) btn.disabled = true; try { const r = await fn(); if (ok) toast(typeof ok === "function" ? ok(r) : ok); } catch (e) { toast(e.message, 1); } await pageApi(); };
  const cookieModal = (id, label) => { openModal(`<div class="mbox"><h2>${id ? "Cập nhật cookie · " + esc(label) : "Thêm tài khoản"} <button class="ib" id="mx">${ico("x")}</button></h2>
      ${id ? "" : `<div class="f"><label>Tên gợi nhớ</label><input class="input" id="cl" placeholder="vd. tkc-linh"></div>`}
      <div class="f" style="margin-top:10px"><label>Cookie (dạng header Cookie: name=value; name2=value2…)</label><textarea id="cc" rows="6" spellcheck="false" placeholder="Dán cookie đã sao chép từ trình duyệt đang đăng nhập Muse"></textarea></div>
      <details style="margin-top:8px"><summary style="cursor:pointer;color:var(--mute);font-size:12.5px">Cách lấy cookie</summary><ol style="color:var(--dim);font-size:12.5px;line-height:1.6;padding-left:18px;margin-top:6px"><li>Đăng nhập muse.ai trên Chrome hoặc Edge.</li><li>Nhấn F12, mở tab Network, tải lại trang, bấm vào một yêu cầu tới muse.ai.</li><li>Ở Request Headers, sao chép toàn bộ giá trị của dòng <b>Cookie</b>.</li><li>Cookie phải có các mục <code>hatch_sess</code>, <code>hatch_gw</code>, <code>hatch_vml</code>, <code>hatch_native_au</code>.</li></ol></details><p style="color:var(--dim);font-size:12.5px;margin-top:8px">Cookie là thông tin đăng nhập, chỉ dán vào đây và không gửi cho người khác.</p>
      <div class="row2" style="margin-top:16px;justify-content:flex-end"><button class="btn ghost" id="mc">Huỷ</button><button class="btn primary" id="mok">Lưu</button></div></div>`);
    $("#modal").onclick = async e => { if (e.target.closest("#mx, #mc")) return closeModal();
      if (e.target.closest("#mok")) { const ck = $("#cc").value.trim(); if (!ck) return toast("Chưa dán cookie", 1);
        try { if (id) await api(`muse/accounts/${id}/cookies`, { body: { cookie_header: ck } }); else { const r = await api("muse/accounts", { body: { label: ($("#cl").value || "").trim(), cookie_header: ck } }); if (r.warning) toast(/缺少核心/.test(r.warning) ? "Cookie còn thiếu các mục quan trọng: " + r.warning.split("：").pop().trim() + ". Hãy sao chép lại cookie đầy đủ từ trình duyệt đang đăng nhập Muse." : r.warning, 1); }
          closeModal(); toast("Đã lưu"); pageApi(); } catch (er) { toast(er.message, 1); } } }; };
  $("#ap-ref").onclick = () => pageApi();
  $("#ap-add").onclick = () => cookieModal();
  $("#ap-ka").onclick = e => run(e.target.closest("button"), () => api("muse/accounts/keepalive", { body: {} }), "Đã gia hạn phiên các tài khoản");
  v.onclick = async e => { let x; const btn = e.target.closest("button, .sw2");
    if ((x = e.target.closest("[data-aptog]"))) return run(null, () => api("muse/accounts/" + x.dataset.aptog, { method: "PUT", body: { enabled: !x.classList.contains("on") } }));
    if ((x = e.target.closest("[data-aptest]"))) { toast("Đang kiểm tra phiên (mở Muse, có thể mất 1 phút)…"); return run(btn, () => api(`muse/accounts/${x.dataset.aptest}/test`, { body: {} }), r => r.ok ? "Phiên còn hạn" : "Phiên lỗi: " + viNote(r.message)); }
    if ((x = e.target.closest("[data-apq]"))) { toast("Đang đo hạn mức…"); return run(btn, () => api(`muse/accounts/${x.dataset.apq}/quota`, { body: {} }), r => `Hạn mức tuần ${r.weekly_used_pct ?? "?"}%`); }
    if ((x = e.target.closest("[data-apck]"))) { const a = accs.find(z => z.id === x.dataset.apck); return cookieModal(a.id, a.label || a.id); }
    if ((x = e.target.closest("[data-apren]"))) { const a = accs.find(z => z.id === x.dataset.apren), nn = prompt("Tên mới cho tài khoản", a.label || ""); if (nn != null) return run(null, () => api("muse/accounts/" + a.id, { method: "PUT", body: { label: nn.trim() } })); return; }
    if ((x = e.target.closest("[data-apdel]"))) { const a = accs.find(z => z.id === x.dataset.apdel); if (!confirm(`Xoá tài khoản "${a.label || a.id}"? Việc này không hoàn tác được.`)) return; return run(null, () => api("muse/accounts/" + a.id, { method: "DELETE" }), "Đã xoá tài khoản"); }
    if ((x = e.target.closest("[data-aptd]"))) return run(null, () => api("muse/tasks/" + x.dataset.aptd, { method: "DELETE" })); };
  S.apiT = setTimeout(() => { if (S.route.page === "api" && !$("#modal").innerHTML) pageApi(); }, 10000);
}

// ---------------------------------------------------------------- Cài đặt
async function pageSettings() {
  setTop("Cài đặt");
  const s = await api("settings"); await refreshHealth();
  const h = S.health || {};
  const pick = (k, label) => `<div class="f"><label>${label}</label><div class="pick"><input class="input" id="st-${k}" readonly value="${esc(s[k] || "")}" placeholder="Không dùng"><button class="btn sm" data-pick="${k}">Chọn</button><button class="ib" data-clr="${k}">${ico("x")}</button></div></div>`;
  $("#view").innerHTML = `<div class="set">
    <div class="card sec"><h4>LUO-API <span class="tag ${h.ok ? "ok" : "bad"}">${h.ok ? h.accounts + " tài khoản" : "chưa kết nối"}</span></h4>
      <div class="f"><label>Địa chỉ</label><input class="input" id="st-api_url" value="${esc(s.api_url)}"></div>
      <div class="f"><label>Khoá API</label><input class="input" id="st-api_key" type="password" placeholder="${s.key_set ? "Đã lưu — nhập để thay" : (h.key ? "Đang dùng khoá trong .env" : "Chưa có khoá")}"></div>
      <div style="display:flex;gap:10px"><button class="btn sm" id="chk">Kiểm tra kết nối</button>${s.key_set ? '<button class="btn sm ghost" id="clrk">Xoá khoá đã lưu</button>' : ""}</div></div>
    <div class="card sec"><h4>Gen video</h4>
      <div class="lab"><div>Cắt đuôi tự động<br><small>Giữ khung ít chuyển động nhất sau lời nói để nối cảnh liền mạch</small></div><div class="sw2 ${s.cut ? "on" : ""}" id="st-cut"></div></div>
      <div class="lab"><div>Chống 2 nhân vật cùng nói<br><small>Sau mỗi clip, đo miệng người không nói bằng nhận diện khuôn mặt; nếu mấp máy theo thì báo vào nhật ký. Chọn số lần tự gen lại bên dưới (mỗi lần gen lại tốn thêm lượt Muse).</small></div><div class="sw2 ${s.check_overlap !== false ? "on" : ""}" id="st-overlap"></div></div>
      <div class="lab"><div>Độ nhạy khi đo miệng<br><small>Cao = bắt cả mấp máy nhẹ (dễ gen lại thừa). Thấp = chỉ bắt khi mấp máy rõ. Nhật ký mỗi cảnh ghi số đo để bạn chỉnh.</small></div><select id="st-mouth_sens">${[["high", "Cao"], ["normal", "Vừa"], ["low", "Thấp"]].map(([v, t]) => `<option value="${v}" ${(s.mouth_sens || "normal") === v ? "selected" : ""}>${t}</option>`).join("")}</select></div>
      <div class="lab"><div>Tự gen lại khi người nghe mấp máy miệng<br><small>0 = chỉ cảnh báo, không tốn thêm lượt</small></div><select id="st-overlap_retries">${[0, 1, 2, 3, 4, 5].map(n => `<option value="${n}" ${+(s.overlap_retries || 0) === n ? "selected" : ""}>${n === 0 ? "Không" : "Tối đa " + n + " lần"}</option>`).join("")}</select></div>
      <div class="lab"><div>Viền xanh nháy + tiếng "tinh tinh"<br><small>Hậu kỳ: ở các câu khen (Great, Perfect, Exactly…) viền màn hình nháy xanh và có tiếng tinh tinh</small></div><div class="sw2 ${s.fx_ding ? "on" : ""}" id="st-ding"></div></div>
      <div class="lab"><div>Tiếng "tách" khi hiện phụ đề<br><small>Âm thanh nhẹ mỗi khi chữ mới xuất hiện</small></div><div class="sw2 ${s.fx_pop ? "on" : ""}" id="st-pop"></div></div>
      <div class="lab"><div>Tách giọng khi robot và người học cùng giới<br><small>Đo thực tế: người học nam lỗi nói chồng ~3%, người học nữ ~38% (vì hai giọng nữ nghe giống nhau). Bật thì tự mô tả robot cao/sáng/trẻ và người học trầm/khàn/chậm khi hai bên cùng giới, và giấu miệng người nghe ngay từ lần đầu</small></div><div class="sw2 ${s.voice_split !== false ? "on" : ""}" id="st-vsplit"></div></div>
      <div class="lab"><div>Hiệu ứng sai / đúng ở phần mở đầu<br><small>Video gọi điện: người học nói sai thì viền đỏ nháy + tiếng "tè tè", AI sửa thì viền xanh lá nháy + tiếng "tinh tinh". Mặc định tự nhận câu đầu của người học và câu AI sửa ngay sau; chỉnh tay ở từng lượt thoại nếu cần</small></div><div class="sw2 ${s.fx_hook !== false ? "on" : ""}" id="st-hook"></div></div>
      <div class="lab"><div>Cắt sát lời nói<br><small>Dùng nhận dạng giọng để tìm từ đầu và từ cuối của lời thoại, bỏ tiếng cười, đoạn im lặng và ồn ở hai đầu clip, chỉ chừa một chút để đỡ liền mạch</small></div><div class="sw2 ${s.precise_cut !== false ? "on" : ""}" id="st-precise"></div></div>
      <div class="lab"><div>Chừa lại sau từ cuối<br><small>Càng nhỏ càng gọn, càng lớn càng tự nhiên</small></div><select id="st-cut_margin">${[0.15, 0.25, 0.3, 0.4, 0.5, 0.7].map(x => `<option value="${x}" ${Math.abs((s.cut_margin || 0.5) - x) < 0.001 ? "selected" : ""}>${String(x).replace(".", ",")} giây</option>`).join("")}</select></div>
      <div class="lab"><div>Tăng tốc lời nói bị kéo chậm<br><small>Muse hay kéo giãn lời cho đủ độ dài clip. Chỉ tăng tốc một phần khi nói chậm hẳn (dưới ~3,4 âm tiết/giây), giữ cao độ giọng, không bao giờ vượt mức tối đa bên dưới</small></div><div class="sw2 ${s.speedfix !== false ? "on" : ""}" id="st-speedfix"></div></div>
      <div class="lab"><div>Mở chat Muse mới<br><small>Mỗi cảnh một chat mới giúp Muse không bắt chước lỗi ở các clip trước (nhân vật nói chồng, trả về video ghép). Nhân vật vẫn nhất quán nhờ khung đầu lấy từ clip trước. Chọn "Cả video một chat" nếu thấy nhân vật bị lệch giữa các cảnh.</small></div><select id="st-chat_every">${[[1, "Mỗi cảnh"], [2, "Mỗi 2 cảnh"], [3, "Mỗi 3 cảnh"], [0, "Cả video một chat"]].map(([v, t]) => `<option value="${v}" ${+(s.chat_every ?? 1) === v ? "selected" : ""}>${t}</option>`).join("")}</select></div>
      <div class="lab"><div>Tốc độ tăng tối đa<br><small>Thấp hơn = giọng tự nhiên hơn nhưng có thể còn hơi chậm</small></div><select id="st-speed_max">${[1.1, 1.15, 1.2, 1.25, 1.3, 1.35].map(x => `<option value="${x}" ${Math.abs((s.speed_max || 1.25) - x) < 0.001 ? "selected" : ""}>×${String(x).replace(".", ",")}</option>`).join("")}</select></div>
      <div class="two" style="margin-top:12px"><div class="f"><label>Chờ tối đa mỗi bước (giây)</label><input class="input" id="st-timeout" type="number" value="${s.timeout}"></div><div class="f"><label>Số lần thử lại</label><input class="input" id="st-retries" type="number" min="0" max="5" value="${s.retries}"></div></div></div>
    <div class="card sec"><h4>Hậu kỳ mặc định</h4>${pick("logo", "Logo (.mov / .png)")}${pick("endcard", "End card (.mp4)")}
      <div class="f"><label>Thư mục xuất video cuối <small style="opacity:.6">(để trống = data/exports/&lt;tên dự án&gt;)</small></label><input class="input" id="st-export_dir" value="${esc(s.export_dir || "")}" placeholder="vd. D:\\Videos\\Talka"></div>
      <div class="f" style="max-width:260px"><label>Nhận dạng giọng</label><select id="st-whisper"><option value="auto" ${s.whisper === "auto" ? "selected" : ""}>Tự chọn</option><option value="small.en" ${s.whisper === "small.en" ? "selected" : ""}>Tiếng Anh (nhanh)</option><option value="medium" ${s.whisper === "medium" ? "selected" : ""}>Đa ngôn ngữ (chậm hơn)</option></select></div></div></div>`;
  const put = o => api("settings", { body: o }).then(() => toast("Đã lưu")).catch(e => toast(e.message, 1));
  $("#view").onchange = e => {
    const id = e.target.id; if (!id || !id.startsWith("st-") || id === "st-cut" || id === "st-speedfix" || id === "st-overlap" || id === "st-ding" || id === "st-pop" || id === "st-precise" || id === "st-vsplit" || id === "st-hook") return;
    const k = id.slice(3); put({ [k]: e.target.type === "number" ? +e.target.value : e.target.value });
  };
  $("#view").onclick = async e => {
    let x;
    if (e.target.closest("#st-cut")) { const el = $("#st-cut"); el.classList.toggle("on"); return put({ cut: el.classList.contains("on") }); }
    if (e.target.closest("#st-ding")) { const el = $("#st-ding"); el.classList.toggle("on"); return put({ fx_ding: el.classList.contains("on") }); }
    if (e.target.closest("#st-pop")) { const el = $("#st-pop"); el.classList.toggle("on"); return put({ fx_pop: el.classList.contains("on") }); }
    if (e.target.closest("#st-hook")) { const el = $("#st-hook"); el.classList.toggle("on"); return put({ fx_hook: el.classList.contains("on") }); }
    if (e.target.closest("#st-vsplit")) { const el = $("#st-vsplit"); el.classList.toggle("on"); return put({ voice_split: el.classList.contains("on") }); }
    if (e.target.closest("#st-precise")) { const el = $("#st-precise"); el.classList.toggle("on"); return put({ precise_cut: el.classList.contains("on") }); }
    if (e.target.closest("#st-overlap")) { const el = $("#st-overlap"); el.classList.toggle("on"); return put({ check_overlap: el.classList.contains("on") }); }
    if (e.target.closest("#st-speedfix")) { const el = $("#st-speedfix"); el.classList.toggle("on"); return put({ speedfix: el.classList.contains("on") }); }
    if ((x = e.target.closest("[data-pick]"))) { const r = await api("pick", { body: { kind: "file" } }); if (r.path) { $("#st-" + x.dataset.pick).value = r.path; put({ [x.dataset.pick]: r.path }); } }
    if ((x = e.target.closest("[data-clr]"))) { $("#st-" + x.dataset.clr).value = ""; put({ [x.dataset.clr]: "" }); }
    if (e.target.closest("#chk")) { await refreshHealth(); pageSettings(); }
    if (e.target.closest("#clrk")) { await api("settings", { body: { clear_key: true } }); pageSettings(); }
  };
}

// ---------------------------------------------------------------- Loại dự án
async function pageTypes() {
  S.boot = await api("boot");
  setTop("Loại dự án", `<button class="btn primary" id="tnew">${ico("plus")}Loại mới</button>`);
  const used = t => S.boot.projects.filter(p => p.template === t.id).length;
  $("#view").innerHTML = `<div class="grid">${S.boot.types.map(t => `<div class="card pcard">
      <div style="display:flex;justify-content:space-between;gap:10px"><h3>${esc(t.name)}</h3>${t.builtin ? '<span class="tag mute">Có sẵn</span>' : ""}</div>
      <div class="meta"><span>${t.scenes} cảnh</span>·<span>${t.fields.length} trường</span>${Object.entries(t.series || {}).map(([k, n]) => `<span class="tag">${esc(k)} ×${n}</span>`).join("")}</div>
      <div class="meta"><span>${used(t)} dự án</span></div>
      <div class="row2" style="margin-top:auto"><button class="btn sm" data-edit="${t.id}">Sửa</button><button class="btn sm" data-dup="${t.id}">Nhân bản</button><span style="flex:1"></span><button class="ib danger" data-deltype="${t.id}" title="Xoá">${ico("trash")}</button></div></div>`).join("")}
  </div>`;
  $("#tnew").onclick = () => typeWizard(null);
  $("#view").onclick = async e => {
    let x;
    if ((x = e.target.closest("[data-edit]"))) return typeWizard(S.boot.types.find(t => t.id === x.dataset.edit));
    if ((x = e.target.closest("[data-dup]"))) {
      const t = await api("types/" + x.dataset.dup);
      try { await api("types", { body: { name: t.name + " (bản sao)", script: t.script, fields: t.fields, turns: t.turns, defaults: t.defaults } }); toast("Đã nhân bản"); pageTypes(); } catch (er) { toast(er.message, 1); }
      return;
    }
    if ((x = e.target.closest("[data-deltype]"))) {
      if (!confirm("Xoá loại dự án này?")) return;
      try { await api("types/" + x.dataset.deltype, { method: "DELETE" }); toast("Đã xoá"); pageTypes(); } catch (er) { toast(er.message, 1); }
    }
  };
}

const GROUP_OPTS = [["day", "Người dạy"], ["hoc", "Người học"], ["scene", "Bối cảnh"], ["other", "Khác"]];
function groupFromText(s) {
  const k = normKey(s);
  if (["day", "nguoiday", "daynguoi"].includes(k)) return "day";
  if (["hoc", "nguoihoc", "hocnguoi"].includes(k)) return "hoc";
  if (["scene", "boicanh", "canh", "nen"].includes(k)) return "scene";
  return "other";
}
async function typeWizard(existing, opts = {}) {
  let W;
  if (existing) {
    const t = await api("types/" + existing.id);
    W = { id: t.id, name: t.name, script: t.script, fields: clone(t.fields), turns: { ...t.turns }, defaults: { ...t.defaults }, analysis: { scenes: t.scenes, series: t.series }, file: null };
  } else {
    W = { id: null, name: "", script: "", fields: [], turns: { day_label: "Người dạy", hoc_label: "Người học" }, defaults: { POS_DAY: "LEFT", POS_HOC: "RIGHT" }, analysis: { scenes: 0, series: {} }, file: null, make: true, pname: opts.fromProject || "" };
  }
  let timer = 0;
  const info = () => {
    const a = W.analysis, el = $("#winfo"); if (!el) return;
    el.innerHTML = a.scenes ? `<span class="tag ok">${a.scenes} cảnh</span><span class="tag">${W.fields.length} trường</span>${Object.entries(a.series || {}).map(([k, n]) => `<span class="tag">${esc(k)} ×${n}</span>`).join("")}` : `<span class="tag bad">Chưa thấy cảnh nào</span>`;
    const tw = $("#wturns"); if (tw) tw.classList.toggle("hidden", !("LUOT" in (a.series || {})));
  };
  const drawFields = () => {
    const el = $("#wfields"); if (!el) return;
    el.innerHTML = W.fields.length ? `<div class="gridwrap" style="max-height:300px"><table class="gt"><thead><tr><th style="min-width:130px">Trường (token)</th><th style="min-width:170px">Nhãn</th><th style="min-width:120px">Nhóm</th><th style="min-width:90px">Loại ô</th><th style="min-width:220px">Gợi ý</th><th>Bắt buộc</th></tr></thead><tbody>${W.fields.map((f, i) => `<tr>
      <td style="padding:9px 11px"><code>${esc(f.key)}</code></td>
      <td><textarea rows="1" data-fi="${i}" data-fk="label">${esc(f.label)}</textarea></td>
      <td><select class="cell" data-fi="${i}" data-fk="group">${GROUP_OPTS.map(([g, n]) => `<option value="${g}" ${g === f.group ? "selected" : ""}>${n}</option>`).join("")}</select></td>
      <td><select class="cell" data-fi="${i}" data-fk="kind"><option value="short" ${f.kind === "short" ? "selected" : ""}>Ngắn</option><option value="long" ${f.kind !== "short" ? "selected" : ""}>Dài</option></select></td>
      <td><textarea rows="1" data-fi="${i}" data-fk="ph" placeholder="ví dụ minh hoạ">${esc(f.ph || "")}</textarea></td>
      <td style="text-align:center;vertical-align:middle"><span class="chk ${f.optional ? "" : "on"}" data-req="${i}" style="display:inline-grid">${f.optional ? "" : ico("check")}</span></td></tr>`).join("")}</tbody></table></div>` : `<div style="color:var(--mute);padding:14px 2px">Dán hoặc tải script có các <code>{{TOKEN}}</code> để tạo bảng trường.</div>`;
    el.querySelectorAll("textarea").forEach(grow);
  };
  const draw = () => {
    openModal(`<div class="mbox wide"><h2>${existing ? "Sửa loại dự án" : "Loại dự án mới"} <button class="ib" id="mx">${ico("x")}</button></h2>
      <div class="f" style="max-width:420px"><label>Tên loại</label><input id="wn" value="${esc(W.name)}" placeholder="Ví dụ: Hội thoại bán hàng"></div>
      <div class="f"><label style="display:flex;align-items:center;gap:10px">Script <label class="btn sm" style="cursor:pointer;margin-left:6px">${ico("up2")}Tải file .txt<input type="file" id="wsf" accept=".txt,.md" hidden></label><span id="winfo" style="display:flex;gap:6px"></span></label>
        <textarea id="ws" rows="7" spellcheck="false" style="font:12.5px/1.5 'Cascadia Mono',Consolas,monospace" placeholder="[STYLE LOCK]:&#10;…&#10;&#10;CẢNH 1 (0:00–0:05): Tiêu đề&#10;Voice: {{CAU_1}}&#10;Prompt video: … {{NHAN_VAT}} …">${esc(W.script)}</textarea></div>
      <div class="f"><label style="display:flex;align-items:center;gap:10px">Bảng trường <label class="btn sm" style="cursor:pointer;margin-left:6px">${ico("up2")}Nhập bảng (CSV)<input type="file" id="wcsv" accept=".csv,.tsv,.txt" hidden></label></label><div id="wfields"></div></div>
      <div id="wturns" class="f hidden"><label>Lượt nói (LUOT)</label><div class="two" style="gap:12px"><input id="wd" class="input" value="${esc(W.turns.day_label || "")}" placeholder="Tên người dạy"><input id="wh" class="input" value="${esc(W.turns.hoc_label || "")}" placeholder="Tên người học">
        <select id="wp" class="input"><option value="LEFT" ${W.defaults.POS_DAY !== "RIGHT" ? "selected" : ""}>Người dạy bên trái, người học bên phải</option><option value="RIGHT" ${W.defaults.POS_DAY === "RIGHT" ? "selected" : ""}>Người dạy bên phải, người học bên trái</option></select></div></div>
      ${existing ? "" : `<div class="f"><label>Danh sách biến thể (tuỳ chọn)</label><div class="pick"><input class="input" id="wvn" readonly value="${esc(W.file ? W.file.name + " · " + W.file.n + " biến thể" : "")}" placeholder="JSON hoặc CSV, tạo luôn dự án đầu tiên"><label class="btn sm" style="cursor:pointer">Chọn<input type="file" id="wvf" accept=".json,.csv,.tsv,.txt" hidden></label></div>
        <div class="row2" style="margin-top:10px;color:var(--mute)"><span class="chk ${W.make ? "on" : ""}" id="wmk">${W.make ? ico("check") : ""}</span>Tạo dự án ngay<input id="wpn" class="input" style="max-width:260px;margin-left:8px" value="${esc(W.pname)}" placeholder="Tên dự án"></div></div>`}
      <div class="mact"><button class="btn" id="mx2">Huỷ</button><button class="btn primary" id="wok">Lưu</button></div></div>`);
    drawFields(); info();
  };
  const analyze = async () => {
    try {
      const r = await api("types/analyze", { body: { script: W.script, fields: W.fields } });
      W.analysis = { scenes: r.scenes, series: r.series }; W.fields = r.fields; drawFields(); info();
    } catch (e) { toast(e.message, 1); }
  };
  draw(); if (W.script) analyze();
  const m = $("#modal");
  m.oninput = e => {
    const el = e.target;
    if (el.id === "ws") { W.script = el.value; clearTimeout(timer); timer = setTimeout(analyze, 400); }
    else if (el.id === "wn") W.name = el.value;
    else if (el.id === "wd") W.turns.day_label = el.value;
    else if (el.id === "wh") W.turns.hoc_label = el.value;
    else if (el.id === "wpn") W.pname = el.value;
    else if (el.dataset.fi !== undefined) { W.fields[+el.dataset.fi][el.dataset.fk] = el.value; if (el.tagName === "TEXTAREA") grow(el); }
  };
  m.onchange = async e => {
    const el = e.target;
    if (el.dataset.fi !== undefined && el.tagName === "SELECT") W.fields[+el.dataset.fi][el.dataset.fk] = el.value;
    if (el.id === "wp") { W.defaults.POS_DAY = el.value; W.defaults.POS_HOC = el.value === "LEFT" ? "RIGHT" : "LEFT"; }
    const f = el.files && el.files[0]; if (!f) return; el.value = "";
    try {
      const text = await f.text();
      if (el.id === "wsf") { W.script = text.replace(/^﻿/, ""); if (!W.name) W.name = f.name.replace(/\.[^.]+$/, ""); draw(); await analyze(); }
      if (el.id === "wcsv") {
        const t = parseCSV(text), head = t[0].map(normKey), col = (...names) => head.findIndex(h => names.includes(h));
        const ik = col("key", "token", "truong"), il = col("label", "nhan"), ig = col("group", "nhom"), it = col("kind", "loai", "loaio"), ip = col("placeholder", "goiy", "ph"), id = col("default", "macdinh"), ir = col("required", "batbuoc");
        if (ik < 0) throw new Error("Cần cột key (tên token)");
        let n = 0;
        t.slice(1).forEach(r => { const f2 = W.fields.find(x => x.key === (r[ik] || "").trim()); if (!f2) return; n++;
          if (il >= 0 && r[il]) f2.label = r[il]; if (ig >= 0 && r[ig]) f2.group = groupFromText(r[ig]);
          if (it >= 0 && r[it]) f2.kind = /ng[aắ]n|short|input|1/i.test(r[it]) ? "short" : "long"; if (ip >= 0) f2.ph = r[ip] || f2.ph; if (id >= 0) f2.default = r[id] || "";
          if (ir >= 0 && r[ir] !== undefined && r[ir] !== "") f2.optional = /^(0|no|khong|false|n)$/i.test(r[ir].trim()); });
        drawFields(); toast(`Đã áp ${n} trường`);
      }
      if (el.id === "wvf") { const vars = variantsFromText(f.name, text, { fields: W.fields }); W.file = { name: f.name, n: vars.length, variants: vars }; $("#wvn").value = `${f.name} · ${vars.length} biến thể`; }
    } catch (er) { toast(er.message, 1); }
  };
  m.onclick = async e => {
    if (e.target.id === "modal" || e.target.closest("#mx") || e.target.id === "mx2") return closeModal();
    let x;
    if ((x = e.target.closest("[data-req]"))) { const f = W.fields[+x.dataset.req]; f.optional = !f.optional; x.classList.toggle("on", !f.optional); x.innerHTML = f.optional ? "" : ico("check"); return; }
    if (e.target.closest("#wmk")) { W.make = !W.make; const c = $("#wmk"); c.classList.toggle("on", W.make); c.innerHTML = W.make ? ico("check") : ""; return; }
    if (e.target.closest("#wok")) {
      if (!W.name.trim()) return toast("Đặt tên cho loại dự án", 1);
      if (!W.analysis.scenes) return toast("Script cần có các dòng CẢNH 1 (0:00–0:05): …", 1);
      const body = { name: W.name.trim(), script: W.script, fields: W.fields, turns: W.turns, defaults: W.defaults };
      try {
        const t = existing ? await api("types/" + existing.id, { method: "PUT", body }) : await api("types", { body });
        S.boot = await api("boot"); closeModal();
        if (!existing && (W.make || W.file)) {
          const T = typ(t.id), variants = W.file ? W.file.variants.map(v => fillVariant(v, T)) : undefined;
          const p = await api("projects", { body: { name: W.pname.trim() || W.name.trim(), template: t.id, variants } });
          toast("Đã tạo loại và dự án"); location.hash = "#/p/" + p.id; return;
        }
        toast("Đã lưu loại dự án"); if (S.route.page === "types") pageTypes(); else location.hash = "#/types";
      } catch (er) { toast(er.message, 1); }
    }
  };
}

(async function init() {
  S.boot = await api("boot");
  refreshHealth(); setInterval(refreshHealth, 20000);
  route(); pollQueue();
})();
