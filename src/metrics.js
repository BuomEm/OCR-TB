export function levenshtein(left, right) {
  const a = [...left], b = [...right];
  let row = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 0; i < a.length; i++) {
    const next = [i + 1];
    for (let j = 0; j < b.length; j++) {
      next.push(Math.min(next[j] + 1, row[j + 1] + 1, row[j] + (a[i] === b[j] ? 0 : 1)));
    }
    row = next;
  }
  return row[b.length];
}

const ratio = (n, d) => d ? n / d : null;
export function evaluateMetrics(rows, workerInitMs = 0) {
  let valid = 0, validChars = 0, chars = 0, validEdits = 0, edits = 0, exact = 0, accepted = 0, acceptedExact = 0;
  for (const { expected, result } of rows) {
    const error = result.status === 'error';
    const prediction = error ? '' : result.text;
    const length = [...expected].length;
    const distance = levenshtein(expected, prediction);
    chars += length; edits += distance;
    if (!error) { valid++; validChars += length; validEdits += distance; }
    const match = !error && expected === prediction;
    if (match) exact++;
    if (result.status === 'ok') { accepted++; if (match) acceptedExact++; }
  }
  const durations = rows.map((r) => r.result.durationMs).filter(Number.isFinite).sort((a, b) => a - b);
  const quantile = (q) => durations.length >= 20 ? durations[Math.ceil(q * durations.length) - 1] : null;
  return { count: rows.length, validCount: valid,
    cerValidOnly: ratio(validEdits, validChars), cerOverall: ratio(edits, chars),
    exactMatchOverall: ratio(exact, rows.length), exactMatchValidOnly: ratio(exact, valid),
    autoAcceptCoverage: ratio(accepted, rows.length), autoAcceptAccuracy: ratio(acceptedExact, accepted),
    operationalErrorRate: ratio(rows.length - valid, rows.length), workerInitMs,
    meanDurationMs: ratio(durations.reduce((a, b) => a + b, 0), durations.length),
    latencyP50Ms: quantile(0.5), latencyP95Ms: quantile(0.95) };
}
