<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import * as topojson from 'topojson-client';

	export let scores: Record<string, number | null> = {};
	export let title: string = '';
	export let subtitle: string = '';

	let container: SVGSVGElement;
	let tooltip = { visible: false, x: 0, y: 0, name: '', score: '' };

	const W = 280;
	const H = 320;

	const COLOR_NULL = '#e8edf5';
	const COLOR_RANGE: [string, string] = ['#c9d9f0', '#1a3da5'];

	onMount(async () => {
		const germany = await fetch('/data/germany.json').then(r => r.json());
		const states = topojson.feature(germany as any, (germany as any).objects.states) as any;

		const projection = d3.geoMercator().fitSize([W, H], states);
		const path = d3.geoPath().projection(projection);

		const colorScale = d3.scaleLinear<string>()
			.domain([0, 10])
			.range(COLOR_RANGE)
			.clamp(true);

		const svg = d3.select(container);

		svg.selectAll('path.state')
			.data(states.features)
			.join('path')
			.attr('class', 'state')
			.attr('d', path as any)
			.attr('fill', (d: any) => {
				const s = scores[d.properties.name];
				return s != null ? colorScale(s) : COLOR_NULL;
			})
			.attr('stroke', '#fff')
			.attr('stroke-width', 0.8)
			.attr('stroke-linejoin', 'round')
			.style('cursor', (d: any) => scores[d.properties.name] != null ? 'default' : 'default')
			.on('mousemove', function (event: MouseEvent, d: any) {
				const s = scores[d.properties.name];
				const rect = (container as SVGSVGElement).getBoundingClientRect();
				tooltip = {
					visible: true,
					x: event.clientX - rect.left,
					y: event.clientY - rect.top - 12,
					name: d.properties.name,
					score: s != null ? s.toFixed(1) : 'keine Daten',
				};
			})
			.on('mouseleave', () => {
				tooltip = { ...tooltip, visible: false };
			});
	});
</script>

<div class="map-card">
	<div class="map-header">
		<div class="map-title">{title}</div>
		{#if subtitle}<div class="map-subtitle">{subtitle}</div>{/if}
	</div>

	<div class="map-wrap">
		<svg bind:this={container} width={W} height={H} viewBox="0 0 {W} {H}" />

		{#if tooltip.visible}
			<div
				class="tooltip"
				style="left:{tooltip.x}px; top:{tooltip.y}px"
			>
				<strong>{tooltip.name}</strong>
				<span>{tooltip.score}{tooltip.score !== 'keine Daten' ? ' / 10' : ''}</span>
			</div>
		{/if}
	</div>

	<div class="legend">
		<span class="legend-label">0</span>
		<div class="legend-bar" />
		<span class="legend-label">10</span>
	</div>
</div>

<style>
	.map-card {
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	.map-header {
		margin-bottom: 10px;
	}

	.map-title {
		font-size: 13px;
		font-weight: 700;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: #1a1a2e;
	}

	.map-subtitle {
		font-size: 11px;
		color: #6b7280;
		margin-top: 2px;
	}

	.map-wrap {
		position: relative;
	}

	.tooltip {
		position: absolute;
		pointer-events: none;
		background: #1a1a2e;
		color: #fff;
		padding: 5px 9px;
		border-radius: 4px;
		font-size: 11px;
		white-space: nowrap;
		transform: translate(-50%, -100%);
		display: flex;
		gap: 6px;
		align-items: baseline;
		z-index: 10;
	}

	.tooltip strong {
		font-weight: 600;
	}

	.tooltip span {
		opacity: 0.75;
	}

	.legend {
		display: flex;
		align-items: center;
		gap: 6px;
		margin-top: 8px;
	}

	.legend-label {
		font-size: 10px;
		color: #9ca3af;
		width: 12px;
		flex-shrink: 0;
	}

	.legend-bar {
		flex: 1;
		height: 6px;
		border-radius: 3px;
		background: linear-gradient(to right, #c9d9f0, #1a3da5);
	}
</style>
