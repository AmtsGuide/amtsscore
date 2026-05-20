export type TopicScores = {
	slug: string;
	label: string;
	scores: Record<string, number | null>;
	cityCount: number;
};

export function buildTopicScores(prescore: any): TopicScores[] {
	return prescore.topics.map((topic: any) => {
		const byBL: Record<string, number[]> = {};
		for (const city of topic.cities) {
			const bl = city.bundesland as string;
			if (city.score != null) {
				if (!byBL[bl]) byBL[bl] = [];
				byBL[bl].push(city.score);
			}
		}
		const scores: Record<string, number | null> = {};
		for (const [bl, vals] of Object.entries(byBL)) {
			scores[bl] = vals.reduce((a, b) => a + b, 0) / vals.length;
		}
		return {
			slug: topic.slug,
			label: topic.label,
			scores,
			cityCount: topic.cities.length,
		};
	});
}
