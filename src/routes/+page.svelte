<script lang="ts">
	import GermanyMap from '$lib/GermanyMap.svelte';
	import type { TopicScores } from '$lib/scores';

	export let data: { topics: TopicScores[] };

	const TOPIC_SUBTITLES: Record<string, string> = {
		'halteverbot':    'Bearbeitungszeit · Kosten',
		'kfz-zulassung':  'Online-Verfügbarkeit · Kosten',
		'gmbh-gruendung': 'Prozessdauer · Aufwand',
	};
</script>

<svelte:head>
	<title>AmtsScore — Verwaltungsdigitalisierung in Deutschland</title>
	<meta name="description" content="Wie digital sind deutsche Behörden? AmtsScore misst Verwaltungsleistungen in deutschen Städten.">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
</svelte:head>

<div class="page">
	<header class="header">
		<div class="header-inner">
			<a href="https://amtsguide.de" target="_blank" rel="noopener" class="brand">
				<img src="/assets/logo-light.svg" alt="AmtsScore" height="22" />
				<span>AmtsScore</span>
			</a>
			<nav>
				<a href="https://amtsguide.de" target="_blank" rel="noopener">AmtsGuide.de ↗</a>
			</nav>
		</div>
	</header>

	<main class="main">
		<div class="hero">
			<p class="eyebrow">Verwaltungsdigitalisierung · Deutschland · 2026</p>
			<h1>Wie digital sind deutsche Behörden?</h1>
			<p class="lead">
				AmtsScore misst öffentlich zugängliche Verwaltungsleistungen in deutschen Städten —
				Bearbeitungszeiten, Kosten, Online-Verfügbarkeit. Score 0–10, höher = besser.
			</p>
		</div>

		<div class="maps-grid">
			{#each data.topics as topic}
				<GermanyMap
					scores={topic.scores}
					title={topic.label}
					subtitle={TOPIC_SUBTITLES[topic.slug] ?? ''}
				/>
			{/each}
		</div>

		<div class="note">
			Quelle: AmtsGuide Facts API · {data.topics[0]?.cityCount ?? 0}+ Städte pro Thema ·
			Farbe = Ø Score aller Städte im Bundesland · Grau = keine Daten
		</div>
	</main>
</div>

<style>
	:global(body) {
		background: #fafbfc;
	}

	.page {
		min-height: 100vh;
		font-family: 'Inter', system-ui, sans-serif;
	}

	/* ── Header ── */
	.header {
		border-bottom: 1px solid #e5e7eb;
		background: #fff;
		position: sticky;
		top: 0;
		z-index: 100;
	}

	.header-inner {
		max-width: 960px;
		margin: 0 auto;
		padding: 0 24px;
		height: 52px;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 8px;
		text-decoration: none;
		font-weight: 700;
		font-size: 15px;
		color: #1a3da5;
	}

	nav a {
		font-size: 13px;
		color: #6b7280;
		text-decoration: none;
	}

	nav a:hover {
		color: #1a3da5;
	}

	/* ── Hero ── */
	.main {
		max-width: 960px;
		margin: 0 auto;
		padding: 48px 24px 64px;
	}

	.hero {
		margin-bottom: 48px;
		max-width: 600px;
	}

	.eyebrow {
		font-size: 11px;
		font-weight: 600;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #1a3da5;
		margin: 0 0 12px;
	}

	h1 {
		font-size: clamp(26px, 4vw, 38px);
		font-weight: 700;
		line-height: 1.2;
		color: #0f172a;
		margin: 0 0 16px;
		letter-spacing: -0.02em;
	}

	.lead {
		font-size: 15px;
		line-height: 1.65;
		color: #4b5563;
		margin: 0;
	}

	/* ── Maps ── */
	.maps-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 40px 48px;
		margin-bottom: 32px;
	}

	@media (max-width: 700px) {
		.maps-grid {
			grid-template-columns: 1fr;
			gap: 40px;
		}
	}

	/* ── Note ── */
	.note {
		font-size: 11px;
		color: #9ca3af;
		border-top: 1px solid #e5e7eb;
		padding-top: 16px;
		line-height: 1.6;
	}
</style>
