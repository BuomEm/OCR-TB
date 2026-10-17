export function serializeError(error, fallback = 'PROCESSING_ERROR') {
  return { code: typeof error?.code === 'string' ? error.code : fallback,
    message: String(error?.message ?? error ?? 'Unknown error') };
}
export function errorResult(file, error, durationMs = 0) {
  return { file: String(file), text: '', status: 'error', confidence: null, votes: 0,
    candidates: [], reviewReasons: [], preprocessing: null, durationMs, error: serializeError(error) };
}
export function exitCode(results) {
  if (results.some((r) => r.status === 'error')) return 1;
  return results.some((r) => r.status !== 'ok') ? 2 : 0;
}
