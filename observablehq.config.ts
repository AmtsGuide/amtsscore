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
  `,
  style: "style.css",
};
