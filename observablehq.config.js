const header = `
<div class="amtsscore-header">
  <a href="/" aria-label="AmtsScore Home" class="amtsscore-headerlink amtsscore-brand">
    <img src="/assets/logo-light.svg" alt="AmtsScore" height="24">
  </a>
  <a href="https://amtsguide.de/de/" target="_blank" rel="noopener" aria-label="AmtsGuide" class="amtsscore-headerlink amtsscore-ag">
    <svg width="20" height="20" viewBox="0 0 768 768" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect width="768" height="768" rx="120" fill="#1a3da5"></rect>
      <path fill="#ffffff" d="M122.6 229.5c20-2.8 37.7-4.3 55-7.8 34.6-7.1 65.5-23.2 94-43.4 32.3-23.1 64-47.1 96-70.6 16.2-11.9 16.4-11.9 33 .3 31.5 23.1 62.6 46.7 94.3 69.3 41.2 29.4 86.5 48.3 138 50.1 12.9.4 15.2 2.7 15.1 15.1-.7 70.3-2.5 140.6-21.5 208.9-22.2 79.9-69.2 140.8-142.6 179.7-27.4 14.5-56.8 25.4-85.7 37-6.8 2.8-15.9 4-22.6 1.9-57.4-18-111-43.1-155.6-84.8-46.9-43.9-72.3-99.3-85.4-160.9-12.8-60.8-14.7-122.5-14.3-184.2 0-3.4 1.3-6.7 2.2-10.6z"></path>
      <path fill="#1a3da5" d="M537 323.4L496.8 283.2L341.6 437.5L269.4 366.3L229.3 406.5C266.7 443.9 304.1 481.3 341.6 518.8L537 323.4Z"></path>
    </svg>
    <span>AmtsGuide</span>
  </a>
  <a href="https://github.com/AmtsGuide/amtsscore" target="_blank" rel="noopener" aria-label="AmtsScore auf GitHub" class="amtsscore-headerlink amtsscore-gh">
    <svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg>
    <span>GitHub</span>
  </a>
</div>`;

export default {
	title: 'AmtsScore',
	root: 'src',
	output: 'dist',
	header,
	pages: [
		{name: 'Methodik', path: '/methodology'},
		{
			name: 'Topics',
			pages: [
				{name: 'E-Auto Candidate Signals', path: '/topics/e-auto'},
				{name: 'Halteverbot', path: '/topics/halteverbot'},
				{name: 'KFZ-Zulassung', path: '/topics/kfz-zulassung'},
				{name: 'GmbH-Gründung', path: '/topics/gmbh-gruendung'},
			],
		},
		{name: 'Städte', path: '/staedte/'},
		{name: 'Bundesländer', path: '/bundeslaender/'},
		{
			name: 'Leuchttürme',
			pages: [
				{name: 'Übersicht', path: '/specials/'},
				{name: 'Berlin Gaststätten 2026', path: '/specials/berlin-gaststaettenanmeldung-2026'},
			],
		},
		{
			name: 'Glossar',
			pages: [
				{name: 'KI-Bereitschaft', path: '/glossar/ai-readiness'},
				{name: 'llms.txt', path: '/glossar/llms-txt'},
				{name: 'API + MCP', path: '/glossar/api-mcp'},
				{name: 'OZG', path: '/glossar/ozg'},
				{name: 'LeiKa', path: '/glossar/leika'},
				{name: 'eID', path: '/glossar/eid'},
				{name: 'FIM', path: '/glossar/fim'},
				{name: 'Registermodernisierung', path: '/glossar/registermodernisierung'},
				{name: 'BITV / WCAG', path: '/glossar/bitv-wcag'},
				{name: 'DSGVO + Cookies', path: '/glossar/dsgvo-cookie'},
				{name: 'Open Data', path: '/glossar/open-data'},
				{name: 'Schema.org', path: '/glossar/schema-org'},
			],
		},
		{name: 'Über AmtsScore', path: '/ueber'},
	],
};
