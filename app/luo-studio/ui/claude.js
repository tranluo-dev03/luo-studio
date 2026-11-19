"use strict";
// Tab "Video mới (Claude)": bảng quản lý các việc phân tích. Thêm video bằng hộp thoại "Giao việc"; tab này chỉ hiện tiến trình các bước.
// Xem kết quả và góp ý nằm trong dự án test (claudeEditorBind ở cuối file).
const CSTEPS = ["Phân tích video, tách hook / tình huống", "Chọn khuôn thể loại", "Viết 2 kịch bản + biến thể mẫu", "Kiểm tra + chọn nhân vật trong kho", "Nhập vào Studio + chạy thử", "Báo cáo"];
const CST = { gening: ["Đang gen video", "ok"], gen_bad: ["Gen dừng / lỗi", "bad"], queued: ["Đang chờ", ""], running: ["Đang chạy", "ok"], stopping: ["Đang dừng", "warn"], done: ["Xong", "ok"], needs_user: ["Cần bạn", "warn"], error: ["Lỗi", "bad"], stopped: ["Đã dừng", "mute"] };
const CGROUP = { running: ["running", "stopping", "gening"], queued: ["queued"], attention: ["needs_user", "error", "stopped", "gen_bad"], done: ["done"] };
// Trạng thái hiển thị: việc Claude đã xong nhưng video test còn đang gen thì CHƯA hoàn tất (gen xong mới sang "Xong"); gen lỗi/dừng thì báo riêng.
function cDisp(j) {
  const g = j.gen, active = g && ["queued", "running", "waiting"].includes(g.state);
  if (j.state === "done" && active) return "gening";
  // vừa dừng/lỗi chưa tới 30 giây: có thể đang tự chạy lại hoặc làm lại cảnh, chưa báo lỗi vội
  if (j.state === "done" && g && ["error", "stopped"].includes(g.state)) return g.age > 30 || g.user_stop ? "gen_bad" : "gening";
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
      <p style="color:var(--mute);font-size:13px;line-height:1.55">Mỗi video là một việc riêng. Bạn ghi <b>insight</b> và chỉ rõ đâu là <b>hook</b>, đâu là <b>tình huống</b>; Claude theo đúng phần bạn ghi (không tự tách lại), viết 2 kịch bản (giữ nguyên video gốc / đổi hook) kèm 1 biến thể mẫu mỗi kịch bản, <b>tự chọn nhân vật trong kho có sẵn</b> nếu bạn không đưa ảnh, nhập vào Studio và chạy thử. Các biến thể khác tạo sau trong trang chi tiết của thẻ.</p>
      <div class="cn-list" id="cn-vids">${pend.videos.map((v, i) => `<div class="cn-item">🎬<span>${esc(cName(v))}</span><a data-rm="v${i}" title="Bỏ">✕</a></div>`).join("") || '<div class="cn-item" style="color:var(--dim)">Chưa có video</div>'}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px"><button class="btn sm" id="cn-addv">${ico("plus")}Thêm video</button><input type="file" id="cn-fv" multiple accept="video/*" style="display:none"></div>
      <div class="f"><label>Insight / nội dung phân tích</label><textarea class="input" id="c-insight" rows="3" placeholder="Video này đánh vào ai, nỗi đau gì, thông điệp gì, vì sao hook giữ được người xem…">${esc(o.insight || "")}</textarea></div>
      <div class="f"><label>Đâu là hook, đâu là tình huống <small style="color:var(--err)">(bắt buộc)</small></label><textarea class="input" id="c-struct" rows="4" placeholder="Hook: từ đầu đến câu … (lượt 1–2: người lái xe nói sai tuổi, cảnh sát hỏi lại)&#10;Tình huống: phần còn lại (nói lại đúng, cảnh sát khuyên học với gia sư AI)&#10;Quảng cáo / end card: nếu có">${esc(o.struct || "")}</textarea></div>
      <details class="cn-adv" ${pend.images.length || pend.extra.length || o.note || o.lang ? "open" : ""}><summary>Tuỳ chọn (không bắt buộc)</summary>
        <div class="f"><label>Yêu cầu thêm</label><textarea class="input" id="c-note" rows="2" placeholder="Mô tả điều bạn muốn. Có thể dán (Ctrl+V) ảnh vào đây.">${esc(o.note)}</textarea></div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px">
          <button class="btn sm" id="cn-addx" type="button">${ico("img")}Ảnh tham chiếu thêm</button><input type="file" id="cn-fx" multiple accept="image/*" style="display:none">
          <button class="btn sm" id="cn-addi" type="button">${ico("user")}Ảnh nhân vật AI có sẵn</button><input type="file" id="cn-fi" multiple accept="image/*" style="display:none">
          ${pend.extra.map((v, i) => `<span class="tag mute">🖼 ${esc(cName(v))} <a data-rm="x${i}" style="cursor:pointer;color:var(--err)">✕</a></span>`).join("")}
          ${pend.images.map((v, i) => `<span class="tag">👤 ${esc(cName(v))} <a data-rm="i${i}" style="cursor:pointer;color:var(--err)">✕</a></span>`).join("")}</div>
        <div class="f"><label>Ngôn ngữ lời thoại mới</label><input class="input" id="c-lang" value="${esc(o.lang)}" placeholder="vd: English, Español"></div>
        <div class="lab"><div>Tự chạy thử 1 biến thể<br><small>Không có ảnh nhân vật thì Claude chọn nhân vật trong kho có sẵn rồi gắn vào.</small></div><div class="sw2 ${o.trial ? "on" : ""}" id="c-trial"></div></div>
      </details>
      <div class="row2" style="margin-top:14px;justify-content:flex-end"><button class="btn ghost" id="bc">Đóng</button><button class="btn primary" id="cgo" ${st.ok && pend.videos.length ? "" : "disabled"}>${ico("sparkle")}Bắt đầu${pend.videos.length > 1 ? " " + pend.videos.length + " video" : ""}</button></div></div>`);
    const keep = () => { const g = id => $(id); if (g("#c-lang")) { o.variants = 1; o.lang = g("#c-lang").value; o.note = g("#c-note").value; o.insight = g("#c-insight").value; o.struct = g("#c-struct").value; } };
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
        keep(); const b = $("#cgo");
        if (!(o.struct || "").trim()) { toast("Hãy ghi đâu là hook, đâu là tình huống", 1); $("#c-struct").focus(); return; }
        b.disabled = true;
        try { await api("claude/jobs", { body: { videos: pend.videos, images: pend.images, extra: pend.extra, opts: o } }); pend.videos = []; pend.images = []; pend.extra = []; o.note = ""; o.insight = ""; o.struct = ""; closeModal(); toast("Đã giao cho Claude"); S.cfilter = "all"; pageClaude(); }
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
  // trạng thái Claude CLI (chạy `claude --version`, ~0,2 giây): nhớ 60 giây để chuyển tab không phải chờ
  const tok = S.rtok;
  if (!S.cst || !S.cst.ok || Date.now() - S.cstT > 60000) { S.cst = await api("claude/status").catch(e => ({ ok: false, error: e.message })); S.cstT = Date.now(); if (tok !== S.rtok) return; }
  const st = S.cst;
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
    if (S.route.page !== "claude" || S.route.id) return;
    const jobs = S.cjobs = await api("claude/jobs").catch(() => S.cjobs || []);
    jobs.forEach(j => { j.ds = cDisp(j); });
    const now = Date.now() / 1000;
    const cnt = k => k === "all" ? jobs.length : jobs.filter(j => CGROUP[k].includes(j.ds)).length;
    const sig = JSON.stringify([S.cfilter, S.cpar, Math.floor(now / 10), jobs.map(j => [j.id, j.ds, j.gen && [j.gen.state, j.gen.done, j.gen.total], j.step_n, j.step, j.note, j.project_id, j.cost, j.name, j.activity, (j.live || {}).out])]);
    if (sig === S.csig) return;
    S.csig = sig;
    const genAct = j => j.gen && ["queued", "running", "waiting"].includes(j.gen.state), busyN = cnt("running") + cnt("queued") + jobs.filter(j => j.ds === "gening" && genAct(j)).length;
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
      const gtxt = gAct ? `${g.stopping ? "Đang dừng · " : ""}Gen video test ${g.done}/${g.total || "?"} cảnh` : "";
      const pct = ds === "done" ? 100 : ds === "queued" ? 0 : (gAct || gBad) ? Math.round((4 + (g.total ? g.done / g.total : 0)) / 6 * 100) : Math.round((Math.max(cur - 1, 0) + (cur ? .5 : 0.15)) / 6 * 100);
      const vw = j.cur_kind === "variants" && ["running", "stopping"].includes(ds);
      const stepTxt = vw ? "Claude đang viết biến thể theo nhóm" : ds === "done" ? "Hoàn tất" : ds === "gen_bad" ? `Bước 5/6 · Gen dừng ở ${g.done}/${g.total || "?"} cảnh` : ds === "queued" ? "Đang chờ tới lượt" : ds === "gening" ? `Bước 5/6 · ${gtxt}` : cur ? `Bước ${cur}/6 · ${CSTEPS[cur - 1] || ""}` : j.state === "error" ? "Bị lỗi" : "Đang khởi động Claude";
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
      return `<div class="cc s-${ds === "gening" ? "running" : ds === "gen_bad" ? "error" : ds}" data-j="${j.id}" title="Bấm để xem chi tiết: tiến độ, 2 kịch bản, tạo biến thể">
        <div class="cc-th"><img src="/api/claude/jobs/${j.id}/thumb" onerror="this.replaceWith(document.createTextNode('🎬'))" alt=""></div>
        <div class="cc-body">
          <div class="cc-title"><span class="n" title="${esc(j.name)}">${esc(j.name)}</span><span class="tag ${cl}">${lb}</span></div>
          <div class="cc-bar"><i style="width:${vw ? 60 : pct}%"></i></div>
          <div class="cc-info">${info.join("")}</div>
          <div class="cc-dots">${dots}</div>
          <div class="cc-act">
            ${busy ? '<button class="btn sm danger" data-a="stop">Dừng</button>' : `${ds === "gening" && g.stopping ? '<button class="btn sm" disabled>Đang dừng…</button>' : ds === "gening" && g.state === "queued" ? '<button class="btn sm primary" data-a="resume" title="Video test đang xếp hàng chưa chạy: bắt đầu gen ngay">Bắt đầu gen</button>' : ds === "gening" && ["running", "waiting"].includes(g.state) ? '<button class="btn sm danger" data-a="stopgen" title="Dừng gen video test (các cảnh đã xong được giữ, bấm Tiếp tục gen để chạy tiếp)">Dừng gen</button>' : ""}${gBad ? '<button class="btn sm primary" data-a="resume" title="Chạy tiếp video test từ chỗ đã dừng, các cảnh đã xong được giữ lại">Tiếp tục gen</button>' : ""}${openBtn}${["error", "stopped", "needs_user"].includes(ds) ? '<button class="btn sm" data-a="retry">Chạy lại</button>' : ""}${ds === "done" || ds === "gen_bad" ? '<button class="btn sm" data-a="restart" title="Chạy lại toàn bộ quy trình phân tích từ đầu, cập nhật dự án cũ">Phân tích lại</button>' : ""}<button class="btn sm ghost" data-a="del" title="Xoá việc này (không xoá dự án trong Studio)">Xoá</button>`}
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
        if (bk.dataset.bulk === "stop") { if (!confirm("Dừng tất cả: Claude đang phân tích và video test đang gen?")) return;
          let n = 0;
          for (const j of S.cjobs) {
            if (["running", "queued"].includes(j.state)) { await api("claude/jobs/" + j.id + "/stop", { body: {} }); n++; }
            if (j.gen && ["queued", "running", "waiting"].includes(j.gen.state)) { await api("stop", { body: { id: j.gen.id } }); n++; }
          }
          toast(n ? `Đã gửi lệnh dừng ${n} việc` : "Không có việc nào đang chạy"); }
        else { const d = S.cjobs.filter(j => j.ds === "done"); if (!confirm(`Xoá ${d.length} việc đã xong khỏi danh sách? (không xoá dự án trong Studio)`)) return; for (const j of d) await api("claude/jobs/" + j.id, { method: "DELETE" }); }
      } catch (er) { toast(er.message, 1); }
      S.csig = ""; return draw();
    }
    const b = e.target.closest("[data-a]");
    if (!b) { const c = e.target.closest(".cc[data-j]"); if (c) location.hash = "#/claude/" + c.dataset.j; return; }
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
      else if (a === "stopgen") { const j = S.cjobs.find(x => x.id === id); await api("stop", { body: { id: j.gen.id } }); toast("Đang dừng gen video test…"); S.csig = ""; }
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
  S.cT = setInterval(() => { if (S.route.page !== "claude" || S.route.id) clearInterval(S.cT); else draw(); }, 2500);
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

// ---------------------------------------------------------------- trang chi tiết một việc (bấm vào thẻ): #/claude/<id>
// Gồm: tiến độ phân tích, cấu trúc hook / tình huống, 2 kịch bản (A giữ nguyên video gốc, B đổi hook) kèm nút Lưu kịch bản,
// và phần Tạo biến thể: mỗi nhóm = thể loại biến thể (mô tả bằng chữ) + số lượng, Claude viết xong thì có nút Thêm dự án.
const CSC = {
  goc: ["A", "Giữ nguyên video gốc", "Hook + tình huống như video gốc. Biến thể của kịch bản này đổi nhân vật: nghề, giới, tuổi, phong cách hình ảnh."],
  hook: ["B", "Đổi hook", "Giữ nguyên tình huống, thay câu nói ở hook. Biến thể của kịch bản này mỗi bản một câu hook khác."],
};
const CGST = { moi: ["Chưa viết", "mute"], dang_viet: ["Claude đang viết", "ok"], xong: ["Đã viết", "ok"], loi: ["Chưa viết được", "bad"] };
const CGPH = {
  goc: "Mô tả thể loại biến thể. Ví dụ: giữ nguyên khung kịch bản, đổi nhân vật / nghề nghiệp: lễ tân khách sạn, phục vụ nhà hàng, tài xế, y tá…; đổi giới tính, độ tuổi; đổi style hình ảnh (live-action, 3D, 2D).",
  hook: "Mô tả thể loại biến thể. Ví dụ: giữ nguyên tình huống, đổi câu nói nhầm ở hook: “I have 30 years”, “I am agree”, “I assist to the party”, “He is sympathetic”…",
};
const cGid = () => Math.random().toString(36).slice(2, 8).padEnd(6, "0");

async function pageClaudeJob(id) {
  setTop("Video mới · Claude");
  const J = S.cjd = S.cjd && S.cjd.id === id ? S.cjd : { id, log: [], groups: null, logOpen: false };
  J.sig = {}; J.j = null; J.log = [];
  $("#view").innerHTML = `<div class="jd">
    <div class="jd-head" id="jd-head"><a class="ib" data-go="#/claude" title="Quay lại danh sách">${ico("back")}</a><h2>Đang tải…</h2></div>
    <div class="jd-cols"><div class="card jd-card" id="jd-prog"></div><div class="card jd-card" id="jd-struct"></div></div>
    <div class="jd-cols" id="jd-scripts"></div>
    <div class="card jd-card" id="jd-groups"></div>
    <details class="card jd-card" id="jd-logbox" ${J.logOpen ? "open" : ""}><summary>Nhật ký Claude</summary><div class="jd-log" id="jd-log"></div></details></div>`;
  const here = () => S.route.page === "claude" && S.route.id === id;
  const set = (key, el, sig, html) => { const s = JSON.stringify(sig); if (J.sig[key] === s) return false; J.sig[key] = s; $(el).innerHTML = html(); return true; };
  const busyJ = j => ["running", "stopping", "queued"].includes(j.state);
  const genAct = g => g && ["queued", "running", "waiting"].includes(g.state);
  const genTxt = g => !g ? "Chưa chạy thử" : genAct(g) ? `${g.stopping ? "Đang dừng · " : ""}Đang gen ${g.done}/${g.total || "?"} cảnh` : g.state === "done" ? `Đã gen xong ${g.done}/${g.total || g.done} cảnh` : `Dừng ở ${g.done}/${g.total || "?"} cảnh${g.error ? " · " + g.error : ""}`;

  const drawHead = j => set("head", "#jd-head", [j.ds, j.name, j.cur_kind], () => {
    const [lb, cl] = CST[j.ds] || [j.ds, ""], busy = busyJ(j);
    return `<a class="ib" data-go="#/claude" title="Quay lại danh sách">${ico("back")}</a><h2 title="${esc(j.name)}">${esc(j.name)}</h2><span class="tag ${cl}">${lb}</span><span style="flex:1"></span>
      ${busy ? '<button class="btn sm danger" data-ja="stop">Dừng</button>' : ""}${["error", "stopped", "needs_user"].includes(j.ds) ? '<button class="btn sm" data-ja="retry">Chạy lại</button>' : ""}
      ${!busy ? '<button class="btn sm" data-ja="restart" title="Chạy lại toàn bộ quy trình phân tích từ đầu, cập nhật dự án cũ">Phân tích lại</button>' : ""}
      <button class="btn sm ghost" data-ja="usage" title="Chi phí và token đã dùng">${ico("table")}Chi phí</button>`;
  });

  const drawProg = j => {
    const now = Date.now() / 1000, busy = busyJ(j), g = j.gen, gA = genAct(g) || j.ds === "gening", gBad = j.ds === "gen_bad", vw = j.cur_kind === "variants";
    const analysed = !!(j.scripts && j.scripts.goc);   // đã có kịch bản: lần chạy sau (viết biến thể) không làm các bước về 0
    let cur = j.step_n || 0; if (gA || gBad) cur = Math.min(cur || 5, 5);
    const allDone = j.ds === "done" || (vw && analysed);
    const t = j.started ? cDur((j.ended && !busy && j.ds !== "gening" ? j.ended : now) - j.started) : "";
    set("prog", "#jd-prog", [j.ds, cur, j.steps, j.activity, j.note, g && [g.state, g.done, g.total], j.cur_kind, Math.floor(now / 5), analysed], () => {
      const steps = CSTEPS.map((s, i) => {
        const n = i + 1, st = allDone || n < cur ? "d" : n === cur ? (["error", "needs_user", "gen_bad"].includes(j.ds) ? "b" : (busy && j.state === "running") || j.ds === "gening" ? "n" : "") : "";
        const extra = n === 5 && (gA || gBad) && !allDone ? genTxt(g) : (j.steps || {})[n] || "";
        return `<div class="jd-step ${st}"><i>${st === "d" ? "✓" : n}</i><div><b>${esc(s)}</b>${extra ? `<span>${esc(extra)}</span>` : ""}</div></div>`;
      }).join("");
      const bad = ["error", "needs_user"].includes(j.ds) && j.note;
      return `<div class="jd-h">Tiến độ phân tích <small>${esc(CKIND[j.cur_kind] || (vw ? "Viết biến thể theo nhóm" : ""))}${t ? " · " + t : ""}</small></div>
        <div class="jd-steps">${steps}</div>
        ${j.ds === "queued" ? '<div class="jd-now">Đang chờ tới lượt chạy.</div>' : ""}
        ${busy && j.state !== "queued" && vw ? '<div class="jd-now">Claude đang viết biến thể cho các nhóm ở phần Tạo biến thể.</div>' : ""}
        ${busy && j.activity ? `<div class="jd-now" title="${esc(j.activity)}">Đang: ${esc(j.activity)}${j.act_t ? " · " + cDur(now - j.act_t) + " trước" : ""}</div>` : ""}
        ${bad ? `<div class="jd-note" style="color:var(--${j.ds === "error" ? "err" : "warn"})">${esc(j.note)}</div>` : ""}`;
    });
  };

  const drawStruct = j => set("struct", "#jd-struct", [j.structure, !!(j.scripts && j.scripts.goc), j.state], () => {
    const st = j.structure, part = (cls, title, p) => !p ? "" : `<div class="jd-part ${cls}"><div class="pt">${title}<small>${esc([p.tu && p.den ? p.tu + " – " + p.den : "", p.luot ? "lượt " + p.luot : ""].filter(Boolean).join(" · "))}</small></div>
      ${p.tom_tat ? `<p>${esc(p.tom_tat)}</p>` : ""}${(p.loi || []).length ? `<ul>${p.loi.slice(0, 8).map(l => `<li>${esc(l)}</li>`).join("")}${p.loi.length > 8 ? `<li style="color:var(--dim)">… còn ${p.loi.length - 8} câu</li>` : ""}</ul>` : ""}</div>`;
    const body = st ? part("hook", "Hook", st.hook) + part("th", "Tình huống", st.tinh_huong) + part("", "Quảng cáo / end card", st.quang_cao) + part("new", "Hook mới của kịch bản B", st.hook_moi)
      : `<div class="jd-sub">${j.scripts && j.scripts.goc ? "Video này được phân tích trước khi Studio biết tách hook / tình huống. Bấm <b>Phân tích lại</b> để tách và có thêm kịch bản B (đổi hook)." : "Claude tách video thành hook và tình huống ở bước 1. Kết quả hiện ở đây khi phân tích xong."}</div>`;
    return `<div class="jd-h">Cấu trúc video gốc <small>hook / tình huống</small></div>${body}`;
  });

  const drawScripts = j => set("scripts", "#jd-scripts", [j.scripts, j.state], () => ["goc", "hook"].map(k => {
    const s = (j.scripts || {})[k], [ab, title, sub] = CSC[k], g = s && s.gen;
    if (!s || !s.project_ok) return `<div class="card jd-card jd-sc"><h3><span class="k">${ab}</span>Kịch bản ${ab} · ${title}</h3><div class="jd-sub">${sub}</div>
      <div class="jd-sub" style="color:var(--dim)">${s ? "Dự án của kịch bản này không còn trong Studio." : busyJ(j) ? "Claude chưa viết xong kịch bản này." : k === "hook" ? "Chưa có. Bấm Phân tích lại để Claude viết kịch bản đổi hook." : "Chưa có."}</div></div>`;
    return `<div class="card jd-card jd-sc ${s.saved ? "saved" : ""}" data-sk="${k}"><h3><span class="k">${ab}</span>Kịch bản ${ab} · ${title}${s.saved ? '<span class="tag ok">Đã lưu vào danh sách kịch bản</span>' : '<span class="tag warn">Đang thử</span>'}</h3>
      <div class="jd-sub">${sub}</div>
      <div class="jd-kv"><span>Loại dự án</span><b title="${esc(s.type_name)}">${esc(s.type_name || s.type_id)}</b><span>Dự án test</span><b title="${esc(s.project_name)}">${esc(s.project_name)}</b>
        <span>Biến thể mẫu</span><b title="${esc(s.variant)}">${esc(s.variant || "—")}</b><span>Video test</span><b style="color:var(--${!g ? "dim" : genAct(g) ? "ok" : g.state === "done" ? "text" : "err"})" title="${esc(genTxt(g))}">${esc(genTxt(g))}</b></div>
      <div class="jd-act">
        ${g ? `<button class="btn sm ${s.saved ? "" : "primary"}" data-sa="view" title="Xem từng cảnh của video test, góp ý, gen lại">${genAct(g) ? "Xem tiến trình gen" : "Xem video &amp; góp ý"}</button>` : ""}
        ${genAct(g) ? "" : `<button class="btn sm" data-sa="trial" title="Gen video test từ biến thể mẫu của kịch bản này">${g ? "Chạy thử lại" : "Chạy thử"}</button>`}
        <button class="btn sm ghost" data-go="#/p/${encodeURIComponent(s.project_id)}">Mở dự án</button><span style="flex:1"></span>
        ${s.saved ? '<button class="btn sm ghost" data-sa="unsave" title="Bỏ khỏi danh sách kịch bản đã lưu">Bỏ lưu</button>' : `<button class="btn sm ${g && g.state === "done" ? "primary" : ""}" data-sa="save" title="Xác nhận kịch bản này đã test ổn và đưa vào danh sách kịch bản (Loại dự án)">${ico("check")}Lưu kịch bản</button>`}
      </div></div>`;
  }).join(""));

  const drawGroups = j => {
    const busy = busyJ(j), has = k => !!((j.scripts || {})[k] || {}).type_ok;
    set("groups", "#jd-groups", [J.groups.map(g => [g.id, g.state, g.file, g.n, g.note, g.project_id, g.project_ok, g.script]), busy, has("goc"), has("hook")], () => {
      const todo = J.groups.filter(g => ["moi", "loi"].includes(g.state)).length;
      const row = g => {
        const lock = ["dang_viet", "xong"].includes(g.state), [lb, cl] = CGST[g.state] || [g.state, ""], can = !busy && has(g.script);
        const acts = g.state === "dang_viet" ? '<i class="spin sm"></i>'
          : g.state === "xong" ? (g.project_ok ? `<button class="btn sm" data-go="#/p/${encodeURIComponent(g.project_id)}">Mở dự án</button>` : `<button class="btn sm primary" data-ga="mk" title="Tạo một dự án chứa ${g.n} biến thể này. Chạy bao nhiêu biến thể do bạn chọn trong dự án.">${ico("plus")}Thêm dự án</button>`)
          : `<button class="btn sm ${can ? "primary" : ""}" data-ga="write" ${can ? "" : "disabled"} title="${has(g.script) ? "Claude viết biến thể cho nhóm này (ảnh nhân vật, lời thoại…)" : "Chưa có kịch bản " + CSC[g.script][0]}">${ico("sparkle")}${g.state === "loi" ? "Viết lại" : "Viết biến thể"}</button>`;
        return `<div class="gr s-${g.state}" data-g="${g.id}"><div class="gr-top">
            <select data-gk="script" ${lock ? "disabled" : ""}>${["goc", "hook"].map(k => `<option value="${k}" ${g.script === k ? "selected" : ""}>Kịch bản ${CSC[k][0]} · ${CSC[k][1]}</option>`).join("")}</select>
            <label>Số lượng <input type="number" min="1" max="50" data-gk="count" value="${g.count}" ${lock ? "disabled" : ""}></label>
            <span class="tag ${cl}">${lb}${g.state === "xong" ? " · " + g.n + " biến thể" : ""}</span><span style="flex:1"></span>${acts}
            ${g.state === "dang_viet" ? "" : `<button class="ib danger" data-ga="rm" title="Bỏ nhóm này (không xoá file biến thể và dự án đã tạo)">${ico("trash")}</button>`}</div>
          <textarea data-gk="desc" rows="3" ${lock ? "disabled" : ""} placeholder="${esc(CGPH[g.script])}">${esc(g.desc)}</textarea>
          ${g.state === "xong" ? `<div class="gr-info">File: ${esc(g.file)}${g.project_ok ? " · đã thêm thành dự án" : " · bấm Thêm dự án để đưa danh sách biến thể này vào Studio"}</div>` : ""}
          ${g.state === "loi" && g.note ? `<div class="gr-info" style="color:var(--err)">${esc(g.note)}</div>` : ""}</div>`;
      };
      return `<div class="jd-h">Tạo biến thể <small>mỗi nhóm = một thể loại biến thể + số lượng; Claude viết ảnh nhân vật, lời thoại… rồi bạn thêm thành dự án</small></div>
        ${!has("goc") && !has("hook") ? '<div class="jd-sub">Cần có kịch bản trước (chờ phân tích xong). Bạn vẫn có thể soạn sẵn các nhóm.</div>' : ""}
        ${J.groups.map(row).join("")}
        <div class="row2" style="flex-wrap:wrap"><button class="btn sm" id="g-add">${ico("plus")}Thêm thể loại biến thể</button><span style="flex:1"></span>
          ${todo > 1 ? `<button class="btn sm primary" id="g-all" ${busy ? "disabled" : ""}>${ico("sparkle")}Viết cả ${todo} nhóm chưa viết</button>` : ""}</div>`;
    });
  };

  const drawLog = () => {
    if (!$("#jd-logbox").open) return;
    set("log", "#jd-log", [J.log.length], () => J.log.slice(-300).map(l => `<div class="${l.k}">${l.k === "user" ? "Bạn: " : ""}${esc(l.x)}</div>`).join("") || '<div class="sys">Chưa có dòng nào.</div>');
    const b = $("#jd-log"); b.scrollTop = b.scrollHeight;
  };

  const draw = () => { const j = J.j; if (!j || !here()) return; drawHead(j); drawProg(j); drawStruct(j); drawScripts(j); drawGroups(j); drawLog(); };

  const load = async () => {
    if (!here()) return;
    let d;
    try { d = await api(`claude/jobs/${id}?since=${J.log.length}`); }
    catch (e) { if (!J.j && here()) $("#jd-head h2").textContent = "Không tìm thấy việc này (có thể đã bị xoá)"; return; }
    if (!here()) return;
    J.log.push(...(d.log || [])); d.ds = cDisp(d); J.j = d;
    const sv = d.groups || [];
    if (!J.groups) J.groups = sv.map(g => ({ ...g }));
    else {   // giữ chữ đang soạn ở máy này; trạng thái + kết quả lấy theo máy chủ
      for (const g of sv) {
        const l = J.groups.find(x => x.id === g.id);
        if (!l) { if (!J.removed || !J.removed.includes(g.id)) J.groups.push({ ...g }); continue; }
        Object.assign(l, { state: g.state, file: g.file, n: g.n, note: g.note, project_id: g.project_id, project_ok: g.project_ok });
        if (["dang_viet", "xong"].includes(g.state)) Object.assign(l, { desc: g.desc, count: g.count, script: g.script });
      }
    }
    if (!J.groups.length && !J.seeded) { J.seeded = true; J.groups.push({ id: cGid(), script: "goc", desc: "", count: 10, state: "moi" }); }
    draw();
  };

  const saveGroups = async () => { clearTimeout(J.saveT); try { await api(`claude/jobs/${id}/groups`, { body: { groups: J.groups.map(g => ({ id: g.id, script: g.script, desc: g.desc, count: g.count })) } }); } catch (e) { toast(e.message, 1); } };
  const view = $("#view");
  view.oninput = e => {
    const el = e.target, r = el.closest("[data-g]"); if (!r || !el.dataset.gk) return;
    const g = J.groups.find(x => x.id === r.dataset.g); if (!g) return;
    g[el.dataset.gk] = el.dataset.gk === "count" ? Math.max(1, Math.min(50, +el.value || 1)) : el.value;
    if (el.dataset.gk === "script") { r.querySelector("textarea").placeholder = CGPH[g.script]; J.sig.groups = ""; }
    clearTimeout(J.saveT); J.saveT = setTimeout(saveGroups, 600);
    if (el.dataset.gk === "script") drawGroups(J.j);
  };
  view.onchange = null; view.ondragover = view.ondragleave = view.ondrop = null;
  $("#jd-logbox").ontoggle = () => { J.logOpen = $("#jd-logbox").open; J.sig.log = ""; drawLog(); };
  view.onclick = async e => {
    const j = J.j; if (!j) return;
    let x;
    try {
      if ((x = e.target.closest("[data-ja]"))) {
        const a = x.dataset.ja;
        if (a === "usage") return usageModal(j);
        if (a === "restart" && !confirm("Phân tích lại từ đầu? Claude sẽ cập nhật kịch bản và dự án cũ (tốn thêm quota Claude).")) return;
        await api(`claude/jobs/${id}/${a}`, { body: {} });
        return load();
      }
      if ((x = e.target.closest("[data-sa]"))) {
        const k = x.closest("[data-sk]").dataset.sk, s = j.scripts[k], a = x.dataset.sa;
        if (a === "view") { S.qview = s.gen.id; S.runSel = null; location.hash = "#/run"; return; }
        if (a === "trial") {
          if (s.gen && !confirm("Gen lại video test của kịch bản này từ cảnh 1? Các cảnh đã gen sẽ bị thay.")) return;
          x.disabled = true; await api(`claude/jobs/${id}/trial`, { body: { key: k } }); toast("Đã đưa biến thể mẫu vào chạy thử");
        } else {
          if (a === "save" && !(s.gen && s.gen.state === "done") && !confirm("Video test của kịch bản này chưa gen xong. Vẫn lưu kịch bản vào danh sách?")) return;
          const r = await api(`claude/jobs/${id}/save`, { body: { key: k, saved: a === "save" } });
          S.boot = null;
          if (a === "save") toastLink(`Đã lưu kịch bản "${r.name}"`, "#/types", "Danh sách kịch bản"); else toast("Đã bỏ lưu");
        }
        return load();
      }
      if (e.target.closest("#g-add")) { J.groups.push({ id: cGid(), script: J.groups.some(g => g.script === "goc") && !J.groups.some(g => g.script === "hook") ? "hook" : "goc", desc: "", count: 10, state: "moi" }); drawGroups(j); return saveGroups(); }
      if (e.target.closest("#g-all")) {
        const ids = J.groups.filter(g => ["moi", "loi"].includes(g.state) && g.desc.trim() && (j.scripts[g.script] || {}).type_ok).map(g => g.id);
        if (!ids.length) return toast("Chưa có nhóm nào đủ mô tả và kịch bản", 1);
        await saveGroups(); await api(`claude/jobs/${id}/write`, { body: { ids } }); toast(`Đã giao Claude viết ${ids.length} nhóm`); return load();
      }
      if ((x = e.target.closest("[data-ga]"))) {
        const g = J.groups.find(q => q.id === x.closest("[data-g]").dataset.g), a = x.dataset.ga; if (!g) return;
        if (a === "rm") {
          if ((g.desc.trim() || g.state === "xong") && !confirm(g.state === "xong" ? "Bỏ nhóm này khỏi danh sách? File biến thể và dự án đã tạo vẫn được giữ." : "Bỏ nhóm này?")) return;
          J.groups = J.groups.filter(q => q !== g); (J.removed = J.removed || []).push(g.id); drawGroups(j); return saveGroups();
        }
        if (a === "write") {
          if (!g.desc.trim()) return toast("Hãy mô tả thể loại biến thể trước", 1);
          x.disabled = true; await saveGroups(); await api(`claude/jobs/${id}/write`, { body: { ids: [g.id] } }); toast("Đã giao Claude viết biến thể"); return load();
        }
        if (a === "mk") {
          x.disabled = true;
          const r = await api(`claude/jobs/${id}/mkproject`, { body: { id: g.id } });
          S.boot = null; toastLink(r.existing ? "Dự án đã có sẵn" : `Đã thêm dự án ${r.variants} biến thể`, "#/p/" + encodeURIComponent(r.id), "Mở dự án"); return load();
        }
      }
    } catch (er) { toast(er.message, 1); J.sig = {}; draw(); }
  };

  await load();
  clearInterval(S.cjT);
  S.cjT = setInterval(() => { if (!here()) clearInterval(S.cjT); else load(); }, 2500);
}
