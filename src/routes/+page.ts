import { buildTopicScores } from '$lib/scores';

export const prerender = true;

export async function load({ fetch }) {
	const prescore = await fetch('/data/prescore.json').then(r => r.json());
	return { topics: buildTopicScores(prescore) };
}
