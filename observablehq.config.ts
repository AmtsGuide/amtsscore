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
        function labelFor(t) {
          if (t === 'dark') return '🌙 Dark';
          if (t === 'light') return '☀️ Light';
          return '🌓 Auto';
        }
        function applyTheme(t) {
          if (t === 'dark') root.style.colorScheme = 'dark';
          else if (t === 'light') root.style.colorScheme = 'light';
          else root.style.colorScheme = '';
          root.dataset.theme = t || 'auto';
        }
        applyTheme(localStorage.getItem(KEY));
        function toggle() {
          const cur = localStorage.getItem(KEY) || 'auto';
          const next = cur === 'auto' ? 'light' : cur === 'light' ? 'dark' : 'auto';
          localStorage.setItem(KEY, next);
          applyTheme(next);
          const btn = document.getElementById('theme-toggle');
          if (btn) btn.textContent = labelFor(next);
        }
        window.toggleAmtsTheme = toggle;
        function mount() {
          if (document.getElementById('theme-toggle')) return;
          const btn = document.createElement('button');
          btn.id = 'theme-toggle';
          btn.title = 'Theme wechseln (auto / hell / dunkel)';
          btn.setAttribute('aria-label', 'Theme wechseln');
          btn.textContent = labelFor(localStorage.getItem(KEY) || 'auto');
          btn.style.cssText = [
            'position:fixed', 'top:1rem', 'right:1rem', 'z-index:9999',
            'background:#3b82f6', 'color:#fff', 'border:2px solid #1e3a8a',
            'border-radius:999px', 'padding:0.5rem 1rem',
            'font:600 0.9rem/1 system-ui,-apple-system,sans-serif',
            'cursor:pointer', 'box-shadow:0 2px 8px rgba(0,0,0,0.2)',
            'display:flex', 'align-items:center', 'gap:0.4rem',
          ].join(';');
          btn.onclick = toggle;
          (document.body || document.documentElement).appendChild(btn);
        }
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', mount);
        } else {
          mount();
        }
      })();
    </script>
  `,
  style: "style.css"
};
