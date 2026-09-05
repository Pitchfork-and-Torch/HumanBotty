/** Shared header, sidebar, mobile drawer, footer. */
(function () {
  const PAGE = document.body.getAttribute("data-page") || "home";
  const NAV = [
    {
      section: "Guide",
      items: [
        { id: "home", href: "/", label: "Home" },
        { id: "start", href: "/start.html", label: "Start here" },
        { id: "roadmap", href: "/roadmap.html", label: "Roadmap" },
        { id: "log", href: "/log.html", label: "Guide log" },
      ],
    },
    {
      section: "Build",
      items: [
        { id: "body", href: "/body.html", label: "Body spec" },
        { id: "safety", href: "/safety.html", label: "Safety" },
        { id: "phase1", href: "/phase1.html", label: "Sense Head" },
        { id: "bom", href: "/bom.html", label: "Parts list" },
        { id: "power", href: "/power.html", label: "Power" },
        { id: "software", href: "/software.html", label: "Software" },
      ],
    },
    {
      section: "Learn",
      items: [{ id: "learning", href: "/learning.html", label: "Skills path" }],
    },
  ];
  const TOP = [
    { id: "start", href: "/start.html", label: "Start" },
    { id: "body", href: "/body.html", label: "Body" },
    { id: "safety", href: "/safety.html", label: "Safety" },
    { id: "bom", href: "/bom.html", label: "Parts" },
    { id: "phase1", href: "/phase1.html", label: "Sense Head" },
  ];

  function isCurrent(id, href) {
    if (PAGE === id) return true;
    if (PAGE === "home" && (href === "/" || href === "/index.html")) return true;
    return false;
  }

  function navLinks(items) {
    return items
      .map((item) => {
        const cur = isCurrent(item.id, item.href) ? ' aria-current="page"' : "";
        return `<a class="nav-link" href="${item.href}"${cur}>${item.label}</a>`;
      })
      .join("");
  }

  function sideHtml() {
    return NAV.map(
      (g) =>
        `<div class="nav-section">${g.section}</div>${navLinks(g.items)}`
    ).join("");
  }

  const xMark =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.171-5.401 6.171H2.74l7.727-8.835L1.254 2.25H8.08l4.253 5.622L18.244 2.25zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>';

  const header = document.getElementById("chrome-header");
  if (header) {
    header.innerHTML = `
      <header class="site-header">
        <div class="brand-island">
          <a class="x-follow" href="https://x.com/suddenlyjon" target="_blank" rel="noopener noreferrer" aria-label="Follow @suddenlyjon on X" title="Follow @suddenlyjon on X">
            <span class="x-follow-mark">${xMark}</span>
            <span class="x-follow-handle">@suddenlyjon</span>
          </a>
          <a class="brand" href="/">
            <img src="/icon-192.png" width="28" height="28" alt="" />
            <span>HumanBotty</span>
          </a>
        </div>
        <nav class="header-nav" aria-label="Primary">
          ${TOP.map((item) => {
            const cur = isCurrent(item.id, item.href) ? ' aria-current="page"' : "";
            return `<a href="${item.href}"${cur}>${item.label}</a>`;
          }).join("")}
        </nav>
        <span class="header-live">Live guide</span>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-drawer" aria-label="Open menu">
          <span></span>
        </button>
      </header>
      <div class="nav-drawer" id="nav-drawer" hidden>${sideHtml()}</div>
    `;
  }

  const side = document.getElementById("chrome-nav");
  if (side) {
    side.innerHTML = sideHtml();
    side.setAttribute("aria-label", "Section");
  }

  const footer = document.getElementById("chrome-footer");
  if (footer) {
    footer.innerHTML = `
      <footer class="site-footer">
        <div class="footer-links">
          <a href="/start.html">Start here</a>
          <a href="/safety.html">Safety</a>
          <a href="/llms.txt">llms.txt</a>
          <a href="https://jonbailey.xyz/">Jon Bailey</a>
          <a href="https://github.com/Pitchfork-and-Torch/HumanBotty">Source</a>
          <a href="https://github.com/Pitchfork-and-Torch">Pitchfork-and-Torch</a>
        </div>
        <p>HumanBotty is a public maker guide. Not an xAI product. MIT. Educational hardware only: no weapons, no covert surveillance.</p>
      </footer>
    `;
  }

  const toggle = document.querySelector(".nav-toggle");
  const drawer = document.getElementById("nav-drawer");
  if (toggle && drawer) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      drawer.hidden = !open;
    });
  }
})();
