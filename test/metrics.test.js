import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateMetrics, levenshtein } from '../src/metrics.js';

test('Levenshtein measures insertions deletions substitutions and case', () => {
  assert.equal(levenshtein('kitten', 'sitting'), 3);
  assert.equal(levenshtein('', 'abcd'), 4);
  assert.equal(levenshtein('A', 'a'), 1);
});
test('CER excludes operational errors only from valid metric', () => {
  const r = evaluateMetrics([
    { expected: 'abcd', result: { text: 'abce', status: 'needs_review', durationMs: 10 } },
    { expected: 'abcd', result: { text: 'ignored', status: 'error', durationMs: 20 } },
    { expected: 'abcd', result: { text: 'abcd', status: 'ok', durationMs: 30 } }
  ], 50);
  assert.equal(r.cerValidOnly, 1 / 8); assert.equal(r.cerOverall, 5 / 12);
  assert.equal(r.exactMatchOverall, 1 / 3); assert.equal(r.exactMatchValidOnly, 1 / 2);
  assert.equal(r.autoAcceptCoverage, 1 / 3); assert.equal(r.autoAcceptAccuracy, 1);
  assert.equal(r.operationalErrorRate, 1 / 3); assert.equal(r.latencyP95Ms, null);
  assert.equal(r.workerInitMs, 50);
});
test('CER may exceed one and undefined denominators return null', () => {
  assert.equal(evaluateMetrics([{ expected: 'a', result: { text: 'aaaa', status: 'ok', durationMs: 1 } }]).cerOverall, 3);
  const r = evaluateMetrics([{ expected: 'abcd', result: { text: '', status: 'error', durationMs: 1 } }]);
  assert.equal(r.cerValidOnly, null); assert.equal(r.cerOverall, 1); assert.equal(r.autoAcceptAccuracy, null);
  assert.equal(evaluateMetrics([]).cerOverall, null);
});
