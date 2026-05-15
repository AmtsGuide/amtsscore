export default {
  title: "AmtsScore",
  pages: [
    { name: "Methodik", path: "/methodology" },
    {
      name: "Topic-Daten v0",
      pages: [
        { name: "Halteverbot", path: "/topics/halteverbot" }
      ]
    },
    {
      name: "Leuchttürme",
      pages: [
        { name: "Übersicht", path: "/specials/" },
        { name: "Berlin Gaststätten 2026", path: "/specials/berlin-gaststaettenanmeldung-2026" }
      ]
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
        { name: "Schema.org", path: "/glossar/schema-org" }
      ]
    },
    { name: "Über AmtsScore", path: "/ueber" }
  ],
  theme: "air",
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
        function applyTheme(t) {
          if (t === 'dark') root.style.colorScheme = 'dark';
          else if (t === 'light') root.style.colorScheme = 'light';
          else root.style.colorScheme = '';
          root.dataset.theme = t || 'auto';
        }
        applyTheme(localStorage.getItem(KEY));
        window.toggleAmtsTheme = function() {
          const cur = localStorage.getItem(KEY) || 'auto';
          const next = cur === 'auto' ? 'light' : cur === 'light' ? 'dark' : 'auto';
          localStorage.setItem(KEY, next);
          applyTheme(next);
          const btn = document.getElementById('theme-toggle');
          if (btn) btn.textContent = next === 'dark' ? '🌙' : next === 'light' ? '☀️' : '🌓';
        };
        document.addEventListener('DOMContentLoaded', function() {
          const header = document.querySelector('#observablehq-header') || document.querySelector('header');
          if (!header) return;
          const btn = document.createElement('button');
          btn.id = 'theme-toggle';
          btn.title = 'Toggle theme (auto / light / dark)';
          btn.setAttribute('aria-label', 'Toggle theme');
          const cur = localStorage.getItem(KEY) || 'auto';
          btn.textContent = cur === 'dark' ? '🌙' : cur === 'light' ? '☀️' : '🌓';
          btn.style.cssText = 'position:fixed;top:0.75rem;right:0.75rem;z-index:1000;background:var(--theme-background-b);border:1px solid var(--theme-foreground-faintest);border-radius:999px;width:2.25rem;height:2.25rem;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;';
          btn.onclick = window.toggleAmtsTheme;
          document.body.appendChild(btn);
        });
      })();
    </script>
  `,
  style: "style.css"
};
