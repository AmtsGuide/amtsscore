export const prerender = true;

export async function load({ fetch }) {
	const data = await fetch('/data/halteverbot.json').then(r => r.json());
	return { data };
}
