export default {
  title: "AmtsScore",
  pages: [
    { name: "Methodik", path: "/methodology" },
    {
      name: "Topic-Daten v0",
      pages: [
        { name: "Halteverbot", path: "/topics/halteverbot" },
      ],
    },
    {
      name: "Leuchttürme",
      pages: [
        { name: "Übersicht", path: "/specials/" },
        { name: "Berlin Gaststätten 2026", path: "/specials/berlin-gaststaettenanmeldung-2026" },
      ],
    },
    {
      name: "Glossar",
      pages: [
        { name: "KI-Bereitschaft", path: "/glossar/ai-readiness" },
        { name: "llms.txt", path: "/glossar/llms-txt" },
        { name: "API + MCP", path: "/glossar/api-mcp" },
        { name: "OZG", path: "/glossar/ozg" },
        { name: "LeiKa", path: "/glossar/leika" },
        { name: "eID", path: "/glossar/eid" },
        { name: "FIM", path: "/glossar/fim" },
        { name: "Registermodernisierung", path: "/glossar/registermodernisierung" },
        { name: "BITV / WCAG", path: "/glossar/bitv-wcag" },
        { name: "DSGVO + Cookies", path: "/glossar/dsgvo-cookie" },
        { name: "Open Data", path: "/glossar/open-data" },
        { name: "Schema.org", path: "/glossar/schema-org" },
      ],
    },
    { name: "Über AmtsScore", path: "/ueber" },
  ],
  // Theme respects OS prefers-color-scheme. Light: air. Dark: near-midnight.
  theme: ["air", "near-midnight"],
  toc: true,
  search: true,
  output: "dist",
  root: "src",
  head: `
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Spline+Sans+Mono:ital,wght@0,300..700;1,300..700&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Spline+Sans+Mono:ital,wght@0,300..700;1,300..700&display=swap">
    <script>
      (function() {
        const KEY = 'amtsscore-theme';
        const root = document.documentElement;
        const stored = localStorage.getItem(KEY);
        if (stored === 'dark' || stored === 'light') root.dataset.theme = stored;
        const SUN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>';
        const MOON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
        function effective() {
          if (root.dataset.theme) return root.dataset.theme;
          return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        function icon() { return effective() === 'dark' ? SUN : MOON; }
        function toggle() {
          const next = effective() === 'dark' ? 'light' : 'dark';
          root.dataset.theme = next;
          localStorage.setItem(KEY, next);
          const btn = document.getElementById('theme-toggle');
          if (btn) btn.innerHTML = icon();
        }
        function mount() {
          if (document.getElementById('theme-toggle')) return;
          const sidebar = document.querySelector('#observablehq-sidebar');
          const wrap = document.createElement('div');
          wrap.id = 'theme-toggle-wrap';
          const btn = document.createElement('button');
          btn.id = 'theme-toggle';
          btn.type = 'button';
          btn.title = 'Theme wechseln';
          btn.setAttribute('aria-label', 'Theme wechseln');
          btn.innerHTML = icon();
          btn.onclick = toggle;
          wrap.appendChild(btn);
          if (sidebar) sidebar.appendChild(wrap);
          else (document.body || document.documentElement).appendChild(wrap);
        }
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', mount);
        } else {
          mount();
        }
      })();
    </script>
  `,
  style: "style.css",
};
