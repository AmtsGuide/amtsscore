<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import * as topojson from 'topojson-client';

	export let data: { data: any };
	const d = data.data;

	const STATUS_COLOR: Record<string, string> = {
		VOLLSTÄNDIG:    '#16a34a',
		TEILWEISE:      '#d97706',
		NUR_INFO:       '#94a3b8',
		NICHT_GEFUNDEN: '#e2e8f0',
	};
	const STATUS_LABEL: Record<string, string> = {
		VOLLSTÄNDIG:    'Vollständig online',
		TEILWEISE:      'Teilweise online',
		NUR_INFO:       'Nur Information',
		NICHT_GEFUNDEN: 'Nicht gefunden',
	};

	// index probe results by city name
	const byCity: Record<string, any> = {};
	for (const c of d.cities) byCity[c.city] = c;

	const counts: Record<string, number> = {};
	for (const c of d.cities) counts[c.status] = (counts[c.status] ?? 0) + 1;
	const hat = (counts['VOLLSTÄNDIG'] ?? 0) + (counts['TEILWEISE'] ?? 0);

	const STATUS_ORDER: Record<string, number> = { VOLLSTÄNDIG: 0, TEILWEISE: 1, NUR_INFO: 2, NICHT_GEFUNDEN: 3 };
	const sorted = [...d.cities].sort((a: any, b: any) =>
		(STATUS_ORDER[a.status] ?? 9) - (STATUS_ORDER[b.status] ?? 9)
	);

	let mapEl: HTMLDivElement;
	let tooltip = { visible: false, x: 0, y: 0, city: '', status: '', grund: '', url: '', statusKey: '' };

	const W = 520, H = 600;

	onMount(async () => {
		const germany = await fetch('/data/germany.json').then(r => r.json());
		const states  = topojson.feature(germany, germany.objects.states) as any;
		const places  = topojson.feature(germany, germany.objects.places)  as any;

		const proj = d3.geoMercator().fitSize([W, H], states);
		const path = d3.geoPath().projection(proj);

		const svg = d3.select(mapEl).append('svg')
			.attr('width', '100%')
			.attr('viewBox', `0 0 ${W} ${H}`)
			.style('overflow', 'visible');

		// State fills — neutral
		svg.selectAll('path.state')
			.data(states.features)
			.join('path')
			.attr('class', 'state')
			.attr('d', path)
			.attr('fill', '#f1f5f9')
			.attr('stroke', '#fff')
			.attr('stroke-width', 1.2)
			.attr('stroke-linejoin', 'round');

		// City dots — only the 16 we measured
		const probed = places.features.filter((f: any) => byCity[f.properties.name]);

		svg.selectAll('circle.city')
			.data(probed)
			.join('circle')
			.attr('class', 'city')
			.attr('cx', (f: any) => (proj(f.geometry.coordinates) as [number,number])[0])
			.attr('cy', (f: any) => (proj(f.geometry.coordinates) as [number,number])[1])
			.attr('r', 9)
			.attr('fill', (f: any) => STATUS_COLOR[byCity[f.properties.name]?.status] ?? '#ccc')
			.attr('stroke', '#fff')
			.attr('stroke-width', 2)
			.style('cursor', 'pointer')
			.on('mousemove', function(event: MouseEvent, f: any) {
				const c = byCity[f.properties.name];
				const rect = mapEl.getBoundingClientRect();
				tooltip = {
					visible: true,
					x: event.clientX - rect.left,
					y: event.clientY - rect.top - 16,
					city: f.properties.name,
					status: STATUS_LABEL[c.status] ?? c.status,
					statusKey: c.status,
					grund: c.grund ?? '',
					url: c.url ?? '',
				};
			})
			.on('mouseleave', () => { tooltip = { ...tooltip, visible: false }; });

		// City labels
		svg.selectAll('text.city-label')
			.data(probed)
			.join('text')
			.attr('class', 'city-label')
			.attr('x', (f: any) => (proj(f.geometry.coordinates) as [number,number])[0] + 12)
			.attr('y', (f: any) => (proj(f.geometry.coordinates) as [number,number])[1] + 4)
			.text((f: any) => f.properties.name)
			.attr('font-size', '10px')
			.attr('font-family', 'Inter, system-ui, sans-serif')
			.attr('fill', '#374151')
			.style('pointer-events', 'none');
	});
</script>

<svelte:head>
	<title>Halteverbot — AmtsScore</title>
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
</svelte:head>

<div class="page">
	<header>
		<div class="header-inner">
			<a href="/" class="back">← AmtsScore</a>
			<span class="run-date">Messung: {d.run_date}</span>
		</div>
	</header>

	<main>
		<div class="layout">
			<!-- Left: map -->
			<div class="map-side">
				<div class="map-wrap" bind:this={mapEl}>
					{#if tooltip.visible}
						<div class="tooltip" style="left:{tooltip.x}px;top:{tooltip.y}px">
							<div class="tt-city">{tooltip.city}</div>
							<div class="tt-status" style="color:{STATUS_COLOR[tooltip.statusKey]}">{tooltip.status}</div>
							<div class="tt-grund">{tooltip.grund}</div>
							{#if tooltip.url}
								<div class="tt-url">{new URL(tooltip.url).hostname.replace('www.','')}</div>
							{/if}
						</div>
					{/if}
				</div>

				<!-- Legend -->
				<div class="legend">
					{#each Object.entries(STATUS_LABEL) as [key, label]}
						{#if counts[key]}
							<div class="legend-item">
								<span class="legend-dot" style="background:{STATUS_COLOR[key]}" />
								<span class="legend-count">{counts[key]}</span>
								<span class="legend-label">{label}</span>
							</div>
						{/if}
					{/each}
				</div>
			</div>

			<!-- Right: headline + findings -->
			<div class="text-side">
				<p class="eyebrow">Online-Verfügbarkeit · 16 Landeshauptstädte · 2026</p>
				<h1>Halteverbot<br>einrichten</h1>

				<div class="stat-big">
					<span class="stat-num">0</span>
					<span class="stat-label">von 16 Städten<br>vollständig online</span>
				</div>

				<div class="stat-big">
					<span class="stat-num" style="color:#d97706">{counts['TEILWEISE'] ?? 0}</span>
					<span class="stat-label">Städte teilweise —<br>PDF oder Formular</span>
				</div>

				<div class="stat-big">
					<span class="stat-num" style="color:#94a3b8">{counts['NUR_INFO'] ?? 0}</span>
					<span class="stat-label">Städte nur<br>Informationsseite</span>
				</div>

				<p class="finding">
					Kein einziger vollständig digitaler End-to-End-Prozess in Deutschland.
					Wo "online" steht, bedeutet es meistens: PDF herunterladen, ausdrucken, einschicken.
				</p>

				<a href="https://amtsguide.de/de/halteverbot/" target="_blank" rel="noopener" class="cta">
					Halteverbot beantragen → AmtsGuide
				</a>
			</div>
		</div>

		<!-- City cards -->
		<div class="cities-section">
			<h2 class="cities-heading">Alle 16 Landeshauptstädte</h2>
			<div class="cities-grid">
				{#each sorted as c}
					<div class="city-card" class:city-card--wide={c.bezirke}>
						<div class="card-header">
							<span class="card-city">{c.city}</span>
							<span class="card-status">
								<span class="card-dot" style="background:{STATUS_COLOR[c.status]}"></span>
								{STATUS_LABEL[c.status]}
							</span>
						</div>
						{#if c.grund}
							<p class="card-grund">{c.grund}</p>
						{/if}
						{#if c.url}
							<a href={c.url} target="_blank" rel="noopener" class="card-link">{new URL(c.url).hostname.replace('www.','')}</a>
						{/if}
						{#if c.bezirke}
							<div class="bezirk-grid">
								{#each c.bezirke as b}
									<div class="bezirk-card">
										<div class="bezirk-header">
											<span class="bezirk-name">{b.bezirk}</span>
											<span class="card-dot" style="background:{STATUS_COLOR[b.status]}"></span>
										</div>
										{#if b.grund}
											<p class="bezirk-grund">{b.grund}</p>
										{/if}
									</div>
								{/each}
							</div>
						{/if}
					</div>
				{/each}
			</div>
		</div>

		<div class="footnote">
			Methodik: Brave Search → Gov-Domain-Filter → Seitentext → Claude Haiku · 16 Landeshauptstädte (je eine pro Bundesland)
		</div>
	</main>
</div>

<style>
	:global(body) { background: #fff; margin: 0; }
	.page { min-height: 100vh; font-family: 'Inter', system-ui, sans-serif; }

	header {
		border-bottom: 1px solid #e5e7eb; background: #fff;
		position: sticky; top: 0; z-index: 100;
	}
	.header-inner {
		max-width: 1100px; margin: 0 auto; padding: 0 32px;
		height: 52px; display: flex; align-items: center; justify-content: space-between;
	}
	.back { font-size: 13px; color: #1a3da5; text-decoration: none; font-weight: 500; }
	.run-date { font-size: 11px; color: #9ca3af; }

	main { max-width: 1100px; margin: 0 auto; padding: 48px 32px 64px; }

	.layout {
		display: grid;
		grid-template-columns: 520px 1fr;
		gap: 64px;
		align-items: start;
	}
	@media (max-width: 900px) {
		.layout { grid-template-columns: 1fr; }
	}

	/* Map */
	.map-wrap { position: relative; }

	.tooltip {
		position: absolute; pointer-events: none;
		background: #0f172a; color: #fff;
		padding: 10px 14px; border-radius: 6px;
		font-size: 12px; transform: translate(-50%, -100%);
		max-width: 240px; z-index: 20;
		box-shadow: 0 4px 12px rgba(0,0,0,0.2);
	}
	.tt-city { font-weight: 700; font-size: 13px; margin-bottom: 2px; }
	.tt-status { font-size: 11px; font-weight: 600; margin-bottom: 6px; }
	.tt-grund { font-size: 11px; opacity: 0.8; line-height: 1.4; margin-bottom: 4px; }
	.tt-url { font-size: 10px; opacity: 0.5; font-family: monospace; }

	.legend {
		display: flex; flex-direction: column; gap: 6px; margin-top: 20px;
	}
	.legend-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #374151; }
	.legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
	.legend-count { font-weight: 700; width: 18px; }
	.legend-label { color: #6b7280; }

	/* Text side */
	.text-side { padding-top: 8px; }
	.eyebrow {
		font-size: 11px; font-weight: 600; letter-spacing: 0.08em;
		text-transform: uppercase; color: #1a3da5; margin: 0 0 12px;
	}
	h1 {
		font-size: clamp(32px, 4vw, 52px); font-weight: 700;
		color: #0f172a; margin: 0 0 36px; letter-spacing: -0.03em; line-height: 1.1;
	}

	.stat-big {
		display: flex; align-items: baseline; gap: 12px;
		margin-bottom: 24px;
	}
	.stat-num {
		font-size: 56px; font-weight: 700; line-height: 1;
		letter-spacing: -0.04em; color: #0f172a; flex-shrink: 0;
	}
	.stat-label {
		font-size: 14px; color: #6b7280; line-height: 1.4;
	}

	.finding {
		font-size: 15px; color: #374151; line-height: 1.7;
		margin: 8px 0 28px; border-left: 3px solid #1a3da5;
		padding-left: 16px;
	}

	.cta {
		display: inline-block; font-size: 13px; font-weight: 600;
		color: #1a3da5; border: 1px solid #1a3da5;
		padding: 8px 16px; border-radius: 6px; text-decoration: none;
	}
	.cta:hover { background: #eff6ff; }

	/* City cards */
	.cities-section { margin-top: 64px; }
	.cities-heading {
		font-size: 13px; font-weight: 600; letter-spacing: 0.06em;
		text-transform: uppercase; color: #9ca3af;
		margin: 0 0 24px; border-bottom: 1px solid #e5e7eb; padding-bottom: 12px;
	}
	.cities-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 16px;
	}
	@media (max-width: 900px) { .cities-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 480px) { .cities-grid { grid-template-columns: 1fr; } }

	.city-card {
		background: #fff;
		border: 1px solid #e2e8f0;
		border-radius: 10px;
		padding: 18px 20px;
		display: flex; flex-direction: column; gap: 10px;
		box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
	}
	.card-header {
		display: flex; align-items: flex-start;
		justify-content: space-between; gap: 10px;
	}
	.card-city { font-size: 15px; font-weight: 600; color: #0f172a; line-height: 1.3; }
	.card-status {
		display: flex; align-items: center; gap: 5px;
		font-size: 11px; color: #64748b; white-space: nowrap; flex-shrink: 0;
		padding-top: 2px;
	}
	.card-dot {
		width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
	}
	.card-grund { font-size: 12px; color: #64748b; line-height: 1.6; margin: 0; }
	.card-link {
		font-size: 11px; color: #94a3b8; text-decoration: none; font-family: monospace;
		margin-top: auto;
	}
	.card-link:hover { color: #1a3da5; }
	.city-card--wide {
		grid-column: 1 / -1;
	}

	/* Bezirk sub-grid */
	.bezirk-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 10px;
		margin-top: 14px;
		padding-top: 14px;
		border-top: 1px solid #f1f5f9;
	}
	@media (max-width: 900px) { .bezirk-grid { grid-template-columns: repeat(2, 1fr); } }
	@media (max-width: 480px) { .bezirk-grid { grid-template-columns: 1fr; } }

	.bezirk-card {
		background: #f8fafc;
		border: 1px solid #e2e8f0;
		border-radius: 6px;
		padding: 10px 12px;
		display: flex; flex-direction: column; gap: 6px;
	}
	.bezirk-header {
		display: flex; align-items: center; justify-content: space-between; gap: 6px;
	}
	.bezirk-name { font-size: 12px; font-weight: 600; color: #0f172a; }
	.bezirk-grund { font-size: 11px; color: #94a3b8; line-height: 1.5; margin: 0; }

	.footnote { font-size: 11px; color: #9ca3af; margin-top: 48px; }
</style>
