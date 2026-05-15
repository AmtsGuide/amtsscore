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
  `,
  style: "style.css"
};
