const PRIORITY = ['V2', 'V3', 'V1', 'V0'];
const finiteConfidence = (value) => Number.isFinite(value) ? value : null;

export function selectCandidates(input) {
  const candidates = input.map((c) => ({
    ...c, text: String(c.text ?? '').replace(/\s/gu, ''),
    confidence: finiteConfidence(c.confidence), error: c.error ?? null,
  }));
  const groups = new Map();
  for (const c of candidates) {
    if (c.error || !c.text) continue;
    const group = groups.get(c.text) ?? { text: c.text, votes: 0, confidence: null, priority: Infinity };
    group.votes++;
    if (c.confidence !== null) group.confidence = Math.max(group.confidence ?? -Infinity, c.confidence);
    const priority = PRIORITY.indexOf(c.variant);
    group.priority = Math.min(group.priority, priority < 0 ? PRIORITY.length : priority);
    groups.set(c.text, group);
  }
  const ranked = [...groups.values()].sort((a, b) => b.votes - a.votes
    || (b.confidence ?? -Infinity) - (a.confidence ?? -Infinity) || a.priority - b.priority);
  const winner = ranked[0];
  const failed = candidates.some((c) => c.error);
  if (!winner) {
    const allFailed = candidates.length > 0 && candidates.every((c) => c.error);
    return { text: '', status: allFailed ? 'error' : 'unrecognized', confidence: null,
      votes: 0, candidates, reviewReasons: failed ? ['variant_failure'] : [],
      error: allFailed ? { code: 'ALL_VARIANTS_FAILED', message: 'All image variants failed' } : null };
  }
  const reviewReasons = [];
  if (winner.votes === 1) reviewReasons.push('single_vote');
  if (winner.confidence === null) reviewReasons.push('missing_confidence');
  else if (winner.confidence < 80) reviewReasons.push('low_confidence');
  if (ranked[1]?.votes === winner.votes) reviewReasons.push('vote_tie');
  if (failed) reviewReasons.push('variant_failure');
  return { text: winner.text, status: reviewReasons.length ? 'needs_review' : 'ok',
    confidence: winner.confidence, votes: winner.votes, candidates, reviewReasons, error: null };
}
