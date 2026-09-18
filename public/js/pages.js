/** Page-specific data renderers. Keep this file CSP-friendly (no inline scripts). */
(function () {
  const page = document.body.getAttribute("data-page") || "";

  function renderPhases(rootId) {
    const root = document.getElementById(rootId);
    if (!root) return;
    fetch("/data/roadmap.json")
      .then((r) => r.json())
      .then((r) => {
        (r.phases || []).forEach((p) => {
          const c = document.createElement("div");
          c.className = "card" + (p.status === "active" ? " accent" : "");
          const h = rootId === "phases" ? "h2" : "h3";
          const hStyle =
            rootId === "phases"
              ? ' style="margin:0;font-size:1.15rem;border:none;padding:0"'
              : ' style="margin:0"';
          c.innerHTML =
            `<div style="display:flex;justify-content:space-between;gap:0.5rem;align-items:center">` +
            `<${h}${hStyle}>Phase ${p.id} - ${p.name}</${h}>` +
            `<span class="status ${p.status}">${p.status}</span></div>` +
            `<p${rootId === "phases" ? ' style="margin:0.75rem 0 0"' : ""}>${p.summary}</p>`;
          root.appendChild(c);
        });
      });
  }

  function renderJournal() {
    const root = document.getElementById("journal-root");
    if (!root) return;
    fetch("/data/journal.json")
      .then((r) => r.json())
      .then((j) => {
        root.innerHTML = "";
        const entries = (j.entries || []).slice().sort((a, b) => b.date.localeCompare(a.date));
        entries.forEach((e) => {
          const art = document.createElement("article");
          art.className = "entry";
          const tags = (e.tags || []).map((t) => `<span class="chip">${t}</span>`).join("");
          art.innerHTML =
            `<div class="date">${e.date} · <span class="mono">${e.id}</span></div>` +
            `<h3>${e.title}</h3>` +
            `<p style="margin:0;color:var(--muted)">${e.body}</p>` +
            `<div class="tags">${tags}</div>`;
          root.appendChild(art);
        });
      })
      .catch(() => {
        root.innerHTML = "<p>Failed to load journal.json</p>";
      });
  }

  function renderBom() {
    const root = document.getElementById("bom-root");
    if (!root) return;
    const statusLabel = {
      to_order: "to order",
      ordered: "ordered",
      received: "received",
      optional: "optional",
      installed: "installed",
      skip: "skip",
    };
    fetch("/data/bom.json")
      .then((r) => r.json())
      .then((b) => {
        const tier = document.getElementById("tier-chip");
        const total = document.getElementById("total-chip");
        const status = document.getElementById("status-chip");
        const progress = document.getElementById("progress-line");
        if (tier) tier.textContent = "Tier: " + b.tier;
        if (total) total.textContent = "about $" + b.approx_total_min + "-$" + b.approx_total_max;
        if (status) status.textContent = b.status;
        const items = b.items || [];
        const optional = items.filter((i) => i.status === "optional").length;
        if (progress) {
          progress.textContent =
            items.length + " line items. " + optional + " optional if you already own them.";
        }
        const byCat = {};
        items.forEach((i) => {
          (byCat[i.category] = byCat[i.category] || []).push(i);
        });
        const order = b.procurement_order || Object.keys(byCat);
        order.forEach((cat) => {
          const list = byCat[cat];
          if (!list) return;
          const sec = document.createElement("section");
          sec.className = "card";
          sec.style.marginBottom = "1rem";
          const title = document.createElement("h2");
          title.style.cssText =
            "margin:0 0 0.5rem;font-size:1rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--faint);border:none";
          title.textContent = cat.replace("_", " ");
          sec.appendChild(title);
          list.forEach((i) => {
            const klass =
              i.status === "to_order" ? "planned" : i.status === "optional" ? "optional" : i.status;
            const row = document.createElement("div");
            row.className = "bom-item";
            const check = document.createElement("div");
            check.className = "check";
            check.title = i.status;
            const mid = document.createElement("div");
            const nameLine = document.createElement("div");
            const strong = document.createElement("strong");
            strong.style.color = "var(--text)";
            strong.textContent = i.name;
            nameLine.append(strong, document.createTextNode(" x" + i.qty));
            const catLine = document.createElement("div");
            catLine.className = "cat";
            const st = document.createElement("span");
            st.className = "status " + klass;
            st.textContent = statusLabel[i.status] || i.status;
            catLine.append(document.createTextNode(i.id + " · "), st);
            mid.append(nameLine, catLine);
            if (i.notes) {
              const n = document.createElement("div");
              n.style.cssText = "color:var(--muted);font-size:0.88rem;margin-top:0.25rem";
              n.textContent = i.notes;
              mid.appendChild(n);
            }
            const price = document.createElement("div");
            price.className = "price";
            price.textContent = "$" + i.approx_low + "-" + i.approx_high;
            row.append(check, mid, price);
            sec.appendChild(row);
          });
          root.appendChild(sec);
        });
      });
  }

  if (page === "home") renderPhases("phase-board");
  if (page === "roadmap") renderPhases("phases");
  if (page === "log") renderJournal();
  if (page === "bom") renderBom();
})();
