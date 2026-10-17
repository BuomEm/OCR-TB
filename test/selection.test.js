import test from 'node:test';
import assert from 'node:assert/strict';
import { selectCandidates } from '../src/selection.js';

const c = (variant, text, confidence = 90, error = null) => ({ variant, text, confidence, error });
test('agreement wins over high confidence and preserves case and punctuation', () => {
  const r = selectCandidates([c('V0', ' aB!\n', 81), c('V1', 'aB!', 85), c('V2', 'AB', 99)]);
  assert.equal(r.text, 'aB!'); assert.equal(r.votes, 2);
  assert.equal(r.confidence, 85); assert.equal(r.status, 'ok');
});
test('vote ties always require review, confidence then priority break ties', () => {
  const r = selectCandidates([c('V0', 'a'), c('V1', 'b'), c('V3', 'c'), c('V2', 'd')]);
  assert.equal(r.text, 'd'); assert.equal(r.status, 'needs_review');
  assert.ok(r.reviewReasons.includes('vote_tie'));
  const s = selectCandidates([c('V0', 'a', 99), c('V2', 'b', 98)]);
  assert.equal(s.text, 'a'); assert.ok(s.reviewReasons.includes('vote_tie'));
});
test('winning singleton requires review even if other variants return text', () => {
  const r = selectCandidates([c('V0', 'a', 95), c('V2', 'b', 91)]);
  assert.ok(r.reviewReasons.includes('single_vote'));
});
test('missing confidence, partial failure and low confidence are explicit', () => {
  const a = selectCandidates([c('V0', 'abc', null), c('V1', 'abc', null), c('V2', '', null, { code: 'OCR', message: 'failed' })]);
  assert.equal(a.confidence, null);
  assert.deepEqual(a.reviewReasons, ['missing_confidence', 'variant_failure']);
  assert.equal(a.status, 'needs_review');
  assert.ok(selectCandidates([c('V0', 'abc', 79), c('V1', 'abc', 70)]).reviewReasons.includes('low_confidence'));
});
test('empty output differs from failure of every variant', () => {
  assert.equal(selectCandidates([c('V0', '')]).status, 'unrecognized');
  assert.equal(selectCandidates([c('V0', '', null, { code: 'OCR', message: 'failed' })]).status, 'error');
});
