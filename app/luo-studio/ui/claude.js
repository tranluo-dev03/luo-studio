"use strict";
// Tab "Video mới (Claude)": bảng quản lý các việc phân tích. Thêm video bằng hộp thoại "Giao việc"; tab này chỉ hiện tiến trình các bước.
// Xem kết quả và góp ý nằm trong dự án test (claudeEditorBind ở cuối file).
const CSTEPS = ["Phân tích video gốc", "Chọn khuôn thể loại", "Viết kịch bản + biến thể", "Kiểm tra + gen ảnh nhân vật", "Nhập vào Studio + chạy thử", "Báo cáo"];
const CST = { gening: ["Đang gen video", "ok"], gen_bad: ["Gen dừng / lỗi", "bad"], queued: ["Đang chờ", ""], running: ["Đang chạy", "ok"], stopping: ["Đang dừng", "warn"], done: ["Xong", "ok"], needs_user: ["Cần bạn", "warn"], error: ["Lỗi", "bad"], stopped: ["Đã dừng", "mute"] };
const CGROUP = { running: ["running", "stopping", "gening"], queued: ["queued"], attention: ["needs_user", "error", "stopped", "gen_bad"], done: ["done"] };
// Trạng thái hiển thị: việc Claude đã xong nhưng video test còn đang gen thì CHƯA hoàn tất (gen xong mới sang "Xong"); gen lỗi/dừng thì báo riêng.
function cDisp(j) {
  const g = j.gen, active = g && ["queued", "running", "waiting"].includes(g.state);
  if (j.state === "done" && active) return "gening";
  // vừa dừng/lỗi chưa tới 30 giây: có thể đang tự chạy lại hoặc làm lại cảnh, chưa báo lỗi vội
  if (j.state === "done" && g && ["error", "stopped"].includes(g.state)) return g.age > 30 ? "gen_bad" : "gening";
  return j.state;
}
const CFILTERS = [["all", "Tất cả"], ["running", "Đang chạy"], ["queued", "Đang chờ"], ["attention", "Cần xử lý"], ["done", "Xong"]];

async function cUpload(file) {
  const r = await fetch("/api/claude/upload?name=" + encodeURIComponent(file.name), { method: "POST", body: file });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || "Tải lên lỗi");
  return d.path;
}
const cName = p => p.split(/[\\/]/).pop().replace(/^[0-9a-f]{8}-/, "");
const cDur = s => { s = Math.max(0, Math.round(s)); return s < 60 ? s + " giây" : s < 3600 ? Math.floor(s / 60) + " phút" : Math.floor(s / 3600) + " giờ " + Math.floor(s % 3600 / 60) + " phút"; };

// ---------------------------------------------------------------- hộp thoại giao việc
function claudeNewModal(st) {
  const pend = S.cpend, o = S.copts || (S.copts = { variants: 3, trial: true, lang: "", note: "" });
  const draw = () => {
    openModal(`<div class="mbox" style="max-width:620px"><h2>Giao việc cho Claude <button class="ib" id="mx">${ico("x")}</button></h2>
      <p style="color:var(--mute);font-size:13px;line-height:1.55">Mỗi video là một việc riêng. Claude tự phân tích, viết kịch bản + biến thể, <b>tự gen ảnh nhân vật nền xanh</b> nếu bạn không đưa ảnh, nhập vào Studio và chạy thử.</p>
      <div class="cn-list" id="cn-vids">${pend.videos.map((v, i) => `<div class="cn-item">🎬<span>${esc(cName(v))}</span><a data-rm="v${i}" title="Bỏ">✕</a></div>`).join("") || '<div class="cn-item" style="color:var(--dim)">Chưa có video</div>'}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px"><button class="btn sm" id="cn-addv">${ico("plus")}Thêm video</button><input type="file" id="cn-fv" multiple accept="video/*" style="display:none"></div>
      <details class="cn-adv" ${pend.images.length || pend.extra.length || o.note || o.lang ? "open" : ""}><summary>Tuỳ chọn (không bắt buộc)</summary>
        <div class="f"><label>Yêu cầu thêm</label><textarea class="input" id="c-note" rows="2" placeholder="Mô tả điều bạn muốn. Có thể dán (Ctrl+V) ảnh vào đây.">${esc(o.note)}</textarea></div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px">
          <button class="btn sm" id="cn-addx" type="button">${ico("img")}Ảnh tham chiếu thêm</button><input type="file" id="cn-fx" multiple accept="image/*" style="display:none">
          <button class="btn sm" id="cn-addi" type="button">${ico("user")}Ảnh nhân vật AI có sẵn</button><input type="file" id="cn-fi" multiple accept="image/*" style="display:none">
          ${pend.extra.map((v, i) => `<span class="tag mute">🖼 ${esc(cName(v))} <a data-rm="x${i}" style="cursor:pointer;color:var(--err)">✕</a></span>`).join("")}
          ${pend.images.map((v, i) => `<span class="tag">👤 ${esc(cName(v))} <a data-rm="i${i}" style="cursor:pointer;color:var(--err)">✕</a></span>`).join("")}</div>
        <div class="two"><div class="f"><label>Số biến thể</label><input class="input" id="c-var" type="number" min="1" max="20" value="${o.variants}"></div>
          <div class="f"><label>Ngôn ngữ lời thoại mới</label><input class="input" id="c-lang" value="${esc(o.lang)}" placeholder="vd: English, Español"></div></div>
        <div class="lab"><div>Tự chạy thử 1 biến thể<br><small>Không có ảnh nhân vật thì Claude tự gen bằng Muse (nền xanh) rồi gắn vào.</small></div><div class="sw2 ${o.trial ? "on" : ""}" id="c-trial"></div></div>
      </details>
      <div class="row2" style="margin-top:14px;justify-content:flex-end"><button class="btn ghost" id="bc">Đóng</button><button class="btn primary" id="cgo" ${st.ok && pend.videos.length ? "" : "disabled"}>${ico("sparkle")}Bắt đầu${pend.videos.length > 1 ? " " + pend.videos.length + " video" : ""}</button></div></div>`);
    const keep = () => { const g = id => $(id); if (g("#c-var")) { o.variants = +g("#c-var").value || 3; o.lang = g("#c-lang").value; o.note = g("#c-note").value; } };
    const upl = async (files, into) => { keep(); for (const f of files) { try { pend[into].push(await cUpload(f)); } catch (e) { toast(e.message, 1); } } draw(); };
    const imgs = fs => [...fs].filter(f => /^image\//.test(f.type));
    $("#cn-addv").onclick = () => $("#cn-fv").click(); $("#cn-fv").onchange = e => upl([...e.target.files], "videos");
    $("#cn-addx").onclick = () => $("#cn-fx").click(); $("#cn-fx").onchange = e => upl(imgs(e.target.files), "extra");
    $("#cn-addi").onclick = () => $("#cn-fi").click(); $("#cn-fi").onchange = e => upl(imgs(e.target.files), "images");
    $("#c-note").onpaste = e => { const fs = imgs(e.clipboardData.files || []); if (fs.length) { e.preventDefault(); upl(fs, "extra"); } };
    $("#c-trial").onclick = e => { o.trial = !o.trial; e.currentTarget.classList.toggle("on", o.trial); };
    $("#modal").onclick = async e => {
      if (e.target.closest("#mx, #bc")) { keep(); return closeModal(); }
      const rm = e.target.closest("[data-rm]"); if (rm) { keep(); const r = rm.dataset.rm; pend[{ v: "videos", x: "extra", i: "images" }[r[0]]].splice(+r.slice(1), 1); return draw(); }
      if (e.target.closest("#cgo")) {
        keep(); const b = $("#cgo"); b.disabled = true;
        try { await api("claude/jobs", { body: { videos: pend.videos, images: pend.images, extra: pend.extra, opts: o } }); pend.videos = []; pend.images = []; pend.extra = []; o.note = ""; closeModal(); toast("Đã giao cho Claude"); S.cfilter = "all"; pageClaude(); }
        catch (er) { toast(er.message, 1); b.disabled = false; }
      }
    };
  };
  draw();
}

// ---------------------------------------------------------------- chi phí + token của một việc
const CKIND = { new: "Phân tích ban đầu", regen: "Sửa theo góp ý + gen lại", feedback: "Sửa theo góp ý", check: "Tự kiểm tra", retry: "Chạy lại / làm tiếp", restart: "Phân tích lại" };
const cTok = n => n >= 1e6 ? (n / 1e6).toFixed(2) + "M" : n >= 1e3 ? (n / 1e3).toFixed(1) + "k" : String(n || 0);
function usageModal(j) {
  if (!j) return;
  const runs = j.runs || [], live = j.live && ["running", "stopping"].includes(j.state) ? j.live : null;
  const sum = k => runs.reduce((a, r) => a + (r[k] || 0), 0);
  const row = (name, r, dim, bold) => `<tr style="${dim ? "color:var(--mute);" : ""}${bold ? "font-weight:650;border-top:1px solid var(--line2)" : ""}"><td>${esc(name)}</td><td>${r.cost != null ? "$" + r.cost.toFixed(3) : "—"}</td><td>${cTok(r.in)}</td><td>${cTok(r.out)}</td><td>${cTok(r.cw)}</td><td>${cTok(r.cr)}</td><td>${r.turns != null ? r.turns : "—"}</td><td>${r.ms ? cDur(r.ms / 1000) : "—"}</td></tr>`;
  const tot = { cost: j.cost || 0, in: sum("in"), out: sum("out"), cw: sum("cw"), cr: sum("cr"), turns: sum("turns"), ms: sum("ms") };
  openModal(`<div class="mbox wide" style="width:min(760px,100%)"><h2>Chi phí và token · ${esc(j.name)} <button class="ib" id="mx">${ico("x")}</button></h2>
    <p style="color:var(--mute);font-size:13px;line-height:1.55;margin-bottom:12px">Số liệu do Claude CLI báo cho từng lần chạy. <b>$</b> là chi phí ước tính theo giá API (với gói thuê bao Claude, đây chỉ là thước đo mức dùng, không phải tiền bị trừ).
      <b>Vào</b> = token mới gửi lên, <b>Ra</b> = token Claude viết, <b>Cache ghi / đọc</b> = phần ngữ cảnh được lưu và dùng lại (đọc cache rất rẻ nên thường chiếm phần lớn).</p>
    <div style="overflow:auto"><table class="trtab" style="width:100%"><thead><tr><th>Lần chạy</th><th>Chi phí</th><th>Vào</th><th>Ra</th><th>Cache ghi</th><th>Cache đọc</th><th>Lượt</th><th>Thời gian</th></tr></thead><tbody>
      ${runs.map(r => row(CKIND[r.kind] || r.kind, r)).join("") || '<tr><td colspan="8" style="color:var(--mute)">Chưa có lần chạy nào hoàn tất.</td></tr>'}
      ${live ? row("Đang chạy (token tạm tính)", { cost: null, in: live.in, out: live.out, cw: live.cw, cr: live.cr }, true) : ""}
      ${!runs.length && j.cost ? row("Các lần chạy trước (chỉ lưu tổng chi phí)", { cost: j.cost }, true) : ""}
      ${runs.length > 1 ? row("Tổng", tot, false, true) : ""}
    </tbody></table></div></div>`);
  $("#modal").onclick = e => { if (e.target.closest("#mx")) closeModal(); };
}

// ---------------------------------------------------------------- trang chính
async function pageClaude() {
  setTop("Video mới · Claude");
  S.cpend = S.cpend || { videos: [], images: [], extra: [] }; S.cpend.extra = S.cpend.extra || [];
  S.cfilter = S.cfilter || "all";
  const st = await api("claude/status").catch(e => ({ ok: false, error: e.message }));
  S.cpar = S.cpar || 2; S.csig = "";
  $("#view").innerHTML = `<div class="cw">
    ${st.ok ? "" : `<div class="card sec" style="margin:0;border-color:var(--err)"><b style="color:var(--err)">Claude CLI chưa sẵn sàng</b><div style="color:var(--mute);margin-top:4px;font-size:13px">${esc(st.error)}</div></div>`}
    <div class="cw-bar" id="cbar"></div>
    <div class="cw-grid" id="cgrid"></div></div>`;

  const add = async files => {
    const vids = [...files].filter(f => /^video\//.test(f.type) || /\.(mp4|mov|mkv|webm|m4v|avi)$/i.test(f.name)), ims = [...files].filter(f => /^image\//.test(f.type));
    if (!vids.length && !ims.length) return toast("Chỉ nhận file video hoặc ảnh", 1);
    toast("Đang tải lên " + (vids.length + ims.length) + " file…");
    for (const f of vids) { try { S.cpend.videos.push(await cUpload(f)); } catch (e) { toast(e.message, 1); } }
    for (const f of ims) { try { S.cpend.images.push(await cUpload(f)); } catch (e) { toast(e.message, 1); } }
    claudeNewModal(st);
  };
  const fi = document.createElement("input"); fi.type = "file"; fi.multiple = true; fi.accept = "video/*,image/*"; fi.style.display = "none"; $("#view").appendChild(fi);
  fi.onchange = () => { const fs = [...fi.files]; fi.value = ""; add(fs); };

  const draw = async () => {
    if (S.route.page !== "claude") return;
    const jobs = S.cjobs = await api("claude/jobs").catch(() => S.cjobs || []);
    jobs.forEach(j => { j.ds = cDisp(j); });
    const now = Date.now() / 1000;
    const cnt = k => k === "all" ? jobs.length : jobs.filter(j => CGROUP[k].includes(j.ds)).length;
    const sig = JSON.stringify([S.cfilter, S.cpar, Math.floor(now / 10), jobs.map(j => [j.id, j.ds, j.gen && [j.gen.state, j.gen.done, j.gen.total], j.step_n, j.step, j.note, j.project_id, j.cost, j.name, j.activity, (j.live || {}).out])]);
    if (sig === S.csig) return;
    S.csig = sig;
    const busyN = cnt("running") + cnt("queued");
    $("#cbar").innerHTML = `${CFILTERS.map(([k, l]) => `<span class="cw-chip ${S.cfilter === k ? "on" : ""} ${k === "attention" && cnt(k) ? "alert" : ""}" data-f="${k}">${l} <b>${cnt(k)}</b></span>`).join("")}
      <div style="flex:1"></div>
      ${busyN ? '<button class="btn sm danger" data-bulk="stop">Dừng tất cả</button>' : ""}${cnt("done") ? '<button class="btn sm ghost" data-bulk="clean">Dọn việc đã xong</button>' : ""}
      <label class="cw-par">Chạy cùng lúc <select id="c-par">${[1, 2, 3, 4, 5, 6, 8, 10].map(n => `<option value="${n}" ${n === S.cpar ? "selected" : ""}>${n}</option>`).join("")}</select></label>`;
    const list = jobs.filter(j => S.cfilter === "all" || CGROUP[S.cfilter].includes(j.ds))
      .sort((a, b) => (CGROUP.running.includes(b.ds) - CGROUP.running.includes(a.ds)) || b.created - a.created);
    const card = j => {
      const ds = j.ds, g = j.gen, gAct = g && (["queued", "running", "waiting"].includes(g.state) || ds === "gening"), busy = ["running", "stopping", "queued"].includes(ds);
      const [lb, cl] = CST[ds] || [ds, ""];
      const gBad = ds === "gen_bad";
      let cur = j.step_n || 0; if (gAct || gBad) cur = Math.min(cur || 5, 5);   // video test còn đang gen thì bước 5 chưa xong, bước 6 chưa tới
      const gtxt = gAct ? `Gen video test ${g.done}/${g.total || "?"} cảnh` : "";
      const pct = ds === "done" ? 100 : ds === "queued" ? 0 : (gAct || gBad) ? Math.round((4 + (g.total ? g.done / g.total : 0)) / 6 * 100) : Math.round((Math.max(cur - 1, 0) + (cur ? .5 : 0.15)) / 6 * 100);
      const stepTxt = ds === "done" ? "Hoàn tất" : ds === "gen_bad" ? `Bước 5/6 · Gen dừng ở ${g.done}/${g.total || "?"} cảnh` : ds === "queued" ? "Đang chờ tới lượt" : ds === "gening" ? `Bước 5/6 · ${gtxt}` : cur ? `Bước ${cur}/6 · ${CSTEPS[cur - 1] || ""}` : j.state === "error" ? "Bị lỗi" : "Đang khởi động Claude";
      const bad = ds === "error" || ds === "needs_user" || ds === "gen_bad";
      // vùng thông tin luôn cao đúng 3 dòng: thẻ không giãn / co theo nội dung
      const ln = (t, cls = "", title = "") => `<div class="ln ${cls}" title="${esc(title || t)}">${esc(t)}</div>`;
      const info = [ln(stepTxt)];
      if (bad) {
        const m = (ds === "gen_bad" ? g.error : j.note) || (ds === "gen_bad" ? "Xem chi tiết trong video test." : "");
        info.push(`<div class="ln m" style="color:var(--${ds === "needs_user" ? "warn" : "err"})" title="${esc(m)}">${esc(m)}</div>`);
      } else if (busy || ds === "gening") {
        if (j.steps && j.steps[cur]) info.push(ln(j.steps[cur], "s"));
        if (ds === "running" && gtxt) info.push(ln(gtxt, "s"));
        if (ds === "running" && j.activity) info.push(ln(`Đang: ${j.activity}${j.act_t ? " · " + cDur(now - j.act_t) + " trước" : ""}`, "s", j.activity));
      }
      const dots = CSTEPS.map((t, i) => `<i title="${i + 1}. ${t}" class="${ds === "done" || i + 1 < cur ? "d" : (ds === "running" || ds === "gening") && i + 1 === cur ? "n" : ""}"></i>`).join("");
      const t = j.started ? cDur((j.ended && !busy && ds !== "gening" ? j.ended : now) - j.started) : "";
      const openBtn = j.project_id ? `<button class="btn sm ${ds === "done" ? "primary" : ""}" data-a="openrun" title="Mở video của dự án test: xem từng cảnh, góp ý, gen lại toàn bộ">${ds === "gening" ? "Xem tiến trình gen" : ds === "gen_bad" ? "Xem video test" : "Xem video &amp; góp ý"}</button>` : "";
      return `<div class="cc s-${ds === "gening" ? "running" : ds === "gen_bad" ? "error" : ds}" data-j="${j.id}">
        <div class="cc-th"><img src="/api/claude/jobs/${j.id}/thumb" onerror="this.replaceWith(document.createTextNode('🎬'))" alt=""></div>
        <div class="cc-body">
          <div class="cc-title"><span class="n" title="${esc(j.name)}">${esc(j.name)}</span><span class="tag ${cl}">${lb}</span></div>
          <div class="cc-bar"><i style="width:${pct}%"></i></div>
          <div class="cc-info">${info.join("")}</div>
          <div class="cc-dots">${dots}</div>
          <div class="cc-act">
            ${busy ? '<button class="btn sm danger" data-a="stop">Dừng</button>' : `${gBad ? '<button class="btn sm primary" data-a="resume" title="Chạy tiếp video test từ chỗ đã dừng, các cảnh đã xong được giữ lại">Tiếp tục gen</button>' : ""}${openBtn}${["error", "stopped", "needs_user"].includes(ds) ? '<button class="btn sm" data-a="retry">Chạy lại</button>' : ""}${ds === "done" || ds === "gen_bad" ? '<button class="btn sm" data-a="restart" title="Chạy lại toàn bộ quy trình phân tích từ đầu, cập nhật dự án cũ">Phân tích lại</button>' : ""}<button class="btn sm ghost" data-a="del" title="Xoá việc này (không xoá dự án trong Studio)">Xoá</button>`}
            <span class="meta">${t} <button class="ib" data-a="usage" title="Chi phí và token đã dùng" style="width:24px;height:24px;display:inline-grid;vertical-align:middle">${ico("table")}</button></span></div></div></div>`;
    };
    $("#cgrid").innerHTML = `<div class="cw-add" id="cadd">${ico("up2")}<b>Thả video gốc vào đây</b><span style="font-size:12.5px">hoặc bấm để chọn · nhiều video cùng lúc</span></div>`
      + (list.length ? list.map(card).join("") : `<div class="cw-empty" style="grid-column:span 1">${jobs.length ? "Không có việc nào trong mục này." : "Chưa có việc nào. Thả video gốc vào ô bên cạnh để bắt đầu."}</div>`);
  };

  $("#view").onclick = async e => {
    const f = e.target.closest("[data-f]"); if (f) { S.cfilter = f.dataset.f; S.csig = ""; return draw(); }
    if (e.target.closest("#cadd")) return fi.click();
    const bk = e.target.closest("[data-bulk]");
    if (bk) {
      try {
        if (bk.dataset.bulk === "stop") { if (!confirm("Dừng tất cả việc đang chạy và đang chờ?")) return; for (const j of S.cjobs.filter(j => ["running", "queued"].includes(j.state))) await api("claude/jobs/" + j.id + "/stop", { body: {} }); }
        else { const d = S.cjobs.filter(j => j.ds === "done"); if (!confirm(`Xoá ${d.length} việc đã xong khỏi danh sách? (không xoá dự án trong Studio)`)) return; for (const j of d) await api("claude/jobs/" + j.id, { method: "DELETE" }); }
      } catch (er) { toast(er.message, 1); }
      S.csig = ""; return draw();
    }
    const b = e.target.closest("[data-a]"); if (!b) return;
    const id = b.closest("[data-j]").dataset.j, a = b.dataset.a;
    if (a === "usage") return usageModal(S.cjobs.find(x => x.id === id));
    if (a === "resume") {   // video test dừng/lỗi giữa chừng: chạy tiếp hàng đợi gen của nó (cảnh đã xong được giữ)
      const j = S.cjobs.find(x => x.id === id);
      try { await api("queue/start", { body: { ids: [j.gen.id] } }); toast("Đã chạy tiếp video test"); } catch (er) { toast(er.message, 1); }
      S.csig = ""; return draw();
    }
    try {
      if (a === "openrun") {   // mở trang chi tiết video đang chạy của dự án test (nơi có ô góp ý)
        const j = S.cjobs.find(x => x.id === id), items = (S.q && S.q.items || []).filter(i => i.project === j.project_id && i.kind === "gen");
        const it = items.find(i => i.variant === j.variant) || items[0];
        if (it) { S.qview = it.id; S.runSel = null; location.hash = "#/run"; if (S.route.page === "run") drawRun(); } else { toast("Video này chưa có trong hàng đợi, mở dự án", 1); location.hash = "#/p/" + encodeURIComponent(j.project_id); }
        return;
      }
      if (a === "restart" && !confirm("Phân tích lại từ đầu? Claude sẽ cập nhật dự án cũ (tốn thêm quota Claude).")) return;
      if (a === "stop") await api("claude/jobs/" + id + "/stop", { body: {} });
      else if (a === "del") { if (!confirm("Xoá việc này? (không xoá dự án đã tạo trong Studio)")) return; await api("claude/jobs/" + id, { method: "DELETE" }); }
      else await api("claude/jobs/" + id + "/" + a, { body: {} });
    } catch (er) { toast(er.message, 1); }
    S.csig = ""; draw();
  };
  $("#view").onchange = async e => {
    if (e.target.id !== "c-par") return;
    S.cpar = +e.target.value;
    try { await api("settings", { body: { claude_parallel: S.cpar } }); toast("Đã đổi: " + S.cpar + " video cùng lúc"); } catch (er) { toast(er.message, 1); }
  };
  // kéo thả video vào bất cứ đâu trên trang
  const view = $("#view");
  view.ondragover = e => { e.preventDefault(); const a = $("#cadd"); if (a) a.classList.add("drag"); };
  view.ondragleave = e => { if (!view.contains(e.relatedTarget)) { const a = $("#cadd"); if (a) a.classList.remove("drag"); } };
  view.ondrop = e => { e.preventDefault(); const a = $("#cadd"); if (a) a.classList.remove("drag"); add(e.dataTransfer.files); };

  api("settings").then(s => { S.cpar = +s.claude_parallel || 2; S.csig = ""; draw(); }).catch(() => {});
  await draw();
  clearInterval(S.cT);
  S.cT = setInterval(() => { if (S.route.page !== "claude") clearInterval(S.cT); else draw(); }, 2500);
}

// ---------------------------------------------------------------- trang chi tiết video đang chạy / đã chạy: góp ý cho Claude
// Dự án có việc Claude liên kết (project.claude_job) thì trang chi tiết mỗi video (drawDetail trong app.js) hiện: ô góp ý tổng,
// ô góp ý dưới từng cảnh, và nút "Gen lại toàn bộ" ở cuối. Góp ý lưu theo (dự án, biến thể) trên máy chủ.
S.cctx = S.cctx || {};
const cKey = it => it.project + "|" + it.variant;
function claudeCtx(it) {
  const k = cKey(it), c = S.cctx[k];
  if (c && (c.job || Date.now() - c.t < 6000)) return c;   // chưa có việc Claude: hỏi lại sau vài giây (việc Claude liên kết dự án lúc kết thúc)
  const fresh = c || (S.cctx[k] = { project: it.project, variant: it.variant, job: "", busy: false, fb: { general: "", scenes: {} }, t: 0 });
  fresh.t = Date.now();
  api(`claude/ctx?project=${encodeURIComponent(it.project)}&variant=${encodeURIComponent(it.variant)}`).then(d => {
    const cur = S.cctx[k]; if (!cur) return;
    const had = cur.job; Object.assign(cur, { job: d.job, busy: d.busy, step: d.step, state: d.state, note: d.note });
    if (!cur.loaded) { cur.fb = d.fb || cur.fb; cur.loaded = true; }
    if (d.job && !had && S.qview === it.id) drawRun();
  }).catch(() => {});
  return fresh;
}
S.cfbOpen = S.cfbOpen || {};
const claudeFbCount = cx => {
  const f = cx.fb, sc = new Set([...Object.keys(f.scenes || {}).filter(k => (f.scenes[k] || "").trim()), ...Object.keys(f.simgs || {}).filter(k => (f.simgs[k] || []).length)]);
  return sc.size + ((f.general || "").trim() || (f.gimgs || []).length ? 1 : 0);
};
// Hàng ảnh đính kèm: ảnh nhỏ có nút xoá + nút thêm ảnh. key = "general" hoặc số cảnh
function claudeImgRow(cx, key) {
  const l = key === "general" ? cx.fb.gimgs || [] : (cx.fb.simgs || {})[key] || [], off = cx.busy ? "disabled" : "";
  return `<div class="fb-imgs">${l.map((p, i) => `<span class="fb-im"><img src="/api/claude/img?f=${encodeURIComponent(p.split(/[\\/]/).pop())}" alt=""><button ${off} data-fbrm="${key}|${i}" title="Bỏ ảnh">×</button></span>`).join("")}<button class="fb-ia" ${off} data-fbimg="${key}" title="Đính kèm ảnh tham chiếu (nhân vật, nền…)">${ico("img")}${l.length ? "" : "Ảnh"}</button></div>`;
}
function claudePickImg(it, key) {
  const cx = S.cctx[cKey(it)]; if (!cx || cx.busy) return;
  const inp = document.createElement("input"); inp.type = "file"; inp.accept = "image/*"; inp.multiple = true;
  inp.onchange = async () => {
    for (const f of inp.files) {
      try {
        const p = await cUpload(f);
        if (key === "general") (cx.fb.gimgs = cx.fb.gimgs || []).push(p); else ((cx.fb.simgs = cx.fb.simgs || {})[key] = (cx.fb.simgs[key] || [])).push(p);
      } catch (e) { toast(e.message, 1); }
    }
    await claudeFbSave(it); drawRun();
  };
  inp.click();
}
function claudeRmImg(it, spec) {
  const cx = S.cctx[cKey(it)]; if (!cx || cx.busy) return;
  const [key, i] = spec.split("|");
  (key === "general" ? cx.fb.gimgs : (cx.fb.simgs || {})[key] || []).splice(+i, 1);
  claudeFbSave(it); drawRun();
}
const claudeFbLabel = cx => { const n = claudeFbCount(cx); return n ? `Gửi ${n} góp ý & gen lại` : "Gen lại toàn bộ"; };
// Ô góp ý cho một cảnh: mặc định chỉ là nút nhỏ "+ Góp ý"; đã có chữ hoặc vừa bấm thì mở ô nhập (viền màu khi có nội dung).
function claudeSceneBox(cx, n) {
  const t = (cx.fb.scenes || {})[n] || "", open = S.cfbOpen[cKey({ project: cx.project, variant: cx.variant }) + "|" + n];
  const hasImg = ((cx.fb.simgs || {})[n] || []).length;
  if (!t.trim() && !open && !hasImg) return `<button class="fb-add" data-fbopen="${n}" ${cx.busy ? "disabled" : ""}>+ Góp ý</button>`;
  return `<textarea class="fb-ta ${t.trim() ? "has" : ""}" data-qfb="${n}" rows="2" ${cx.busy ? "disabled" : ""} placeholder="Cảnh ${n} cần sửa gì?">${esc(t)}</textarea>${claudeImgRow(cx, n)}`;
}
function claudeTopCard(cx) {
  const st = cx.busy ? `<div class="fb-st"><i class="spin sm"></i>Claude đang sửa… <span>${esc(cx.step || "")}</span></div>`
    : cx.state === "error" || cx.state === "needs_user" ? `<div class="fb-st" style="color:var(--${cx.state === "error" ? "err" : "warn"})">${cx.state === "error" ? "Claude lỗi" : "Claude cần bạn"}: ${esc((cx.note || "").slice(0, 160))}</div>` : "";
  return `<div class="card fb-card"><div class="fb-h">Góp ý chung</div>${st}
    <textarea class="fb-ta ${(cx.fb.general || "").trim() ? "has" : ""}" data-qfb="general" rows="2" ${cx.busy ? "disabled" : ""} placeholder="Nhân vật, nền, giọng nói, nhịp… (góp ý từng cảnh ở dưới mỗi cảnh)">${esc(cx.fb.general || "")}</textarea>${claudeImgRow(cx, "general")}</div>`;
}
// Thanh hành động dính đáy: luôn thấy nút gen lại và số góp ý sẽ gửi
const claudeRegenCard = cx => `<div class="fb-bar"><button class="btn primary" id="qregen" ${cx.busy ? "disabled" : ""} title="Claude sửa kịch bản, biến thể, ảnh nhân vật theo góp ý rồi Studio gen lại video từ cảnh 1">${ico("redo")}<span id="qfbl">${claudeFbLabel(cx)}</span></button>
  <button class="btn ghost" id="qself" ${cx.busy ? "disabled" : ""} title="Claude xem lại kết quả đã gen và tự sửa lỗi">Claude tự kiểm tra</button></div>`;
function claudeOpenFb(it, n) {
  const cx = S.cctx[cKey(it)]; if (!cx || cx.busy) return;
  S.cfbOpen[cKey(it) + "|" + n] = true; drawRun();
  setTimeout(() => { const t = document.querySelector(`textarea[data-qfb="${n}"]`); if (t) t.focus(); }, 30);
}

function claudeFbInput(e, it) {
  const el = e.target; if (el.dataset.qfb === undefined) return false;
  const cx = S.cctx[cKey(it)]; if (!cx) return true;
  if (el.dataset.qfb === "general") cx.fb.general = el.value; else (cx.fb.scenes = cx.fb.scenes || {})[el.dataset.qfb] = el.value;
  el.classList.toggle("has", !!el.value.trim());
  const l = document.getElementById("qfbl"); if (l) l.textContent = claudeFbLabel(cx);
  clearTimeout(cx.saveT); cx.saveT = setTimeout(() => claudeFbSave(it), 600);
  return true;
}
async function claudeFbSave(it) {
  const cx = S.cctx[cKey(it)]; if (!cx) return;
  clearTimeout(cx.saveT);
  try { await api("claude/fb", { body: { project: it.project, variant: it.variant, general: cx.fb.general || "", scenes: cx.fb.scenes || {}, gimgs: cx.fb.gimgs || [], simgs: cx.fb.simgs || {} } }); } catch (e) { toast(e.message, 1); }
}
async function claudeRegen(it) {
  const cx = S.cctx[cKey(it)]; if (!cx || !cx.job) return;
  await claudeFbSave(it);
  try {
    const r = await api(`claude/jobs/${cx.job}/regen`, { body: { project: it.project, variant: it.variant } });
    toast(r.claude ? "Đã gửi góp ý cho Claude, sửa xong sẽ tự gen lại" : "Đã xếp gen lại toàn bộ");
    cx.fb = { general: "", scenes: {}, gimgs: [], simgs: {} }; cx.busy = !!r.claude; cx.t = 0; drawRun();
  } catch (e) { toast(e.message, 1); }
}
async function claudeSelfCheck(it) {
  const cx = S.cctx[cKey(it)]; if (!cx || !cx.job) return;
  try { await api(`claude/jobs/${cx.job}/check`, { body: {} }); toast("Claude đang tự kiểm tra kết quả"); cx.busy = true; cx.t = 0; drawRun(); } catch (e) { toast(e.message, 1); }
}
// Theo dõi việc Claude khi đang xem chi tiết video: khoá ô góp ý lúc Claude sửa, mở lại khi xong.
function claudeWatch() {
  clearInterval(S.cctxT);
  S.cctxT = setInterval(async () => {
    const it = S.q && S.qview && S.q.items.find(i => i.id === S.qview), cx = it && S.cctx[cKey(it)];
    if (S.route.page !== "run" || !cx || !cx.job) return;
    try {
      const d = await api(`claude/ctx?project=${encodeURIComponent(it.project)}&variant=${encodeURIComponent(it.variant)}`);
      const ch = d.busy !== cx.busy || d.step !== cx.step || d.state !== cx.state;
      Object.assign(cx, { busy: d.busy, step: d.step, state: d.state, note: d.note });
      if (ch) drawRun();
    } catch (e) { /* bỏ qua */ }
  }, 3000);
}
