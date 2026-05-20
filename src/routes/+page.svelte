<script lang="ts">
	import { onMount } from 'svelte';

	let mounted = false;
	onMount(() => { mounted = true; });
</script>

<svelte:head>
	<title>AmtsScore — Verwaltungsdigitalisierung in Deutschland</title>
</svelte:head>

<main>
	<header>
		<img src="/assets/logo-light.svg" alt="AmtsScore" height="28" />
		<h1>AmtsScore</h1>
		<p>Wie digital sind deutsche Behörden wirklich?</p>
	</header>

	<section>
		<p>Visualisierung folgt.</p>
	</section>
</main>

<style>
	main {
		max-width: 1200px;
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}
	header {
		margin-bottom: 3rem;
	}
	h1 {
		font-size: 2rem;
		font-weight: 700;
		margin: 0.5rem 0 0.25rem;
		color: var(--brand);
	}
	p {
		color: var(--text-muted);
		margin: 0;
	}
</style>
