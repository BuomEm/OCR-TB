// Real subprocess fixture: exercises OS exit, signal escalation and recovery.
process.on('SIGTERM', () => {});
process.on('message', (message) => {
  if (message.type === 'init') {
    if (process.argv.includes('hang-init')) return;
    process.send({ type: 'ready', id: message.id, initMs: 1 });
  }
  if (message.type === 'shutdown') process.exit(0);
  if (message.type === 'recognize') {
    if (Buffer.isBuffer(message.file) || message.type !== 'recognize') process.exit(9);
    if (message.file === 'hang') { while (true) { /* deliberately stuck */ } }
    if (message.file === 'crash') process.exit(3);
    process.send({ type: 'result', id: message.id, result: {
      file: message.file, text: 'abc', status: 'ok', confidence: 90, votes: 2,
      candidates: [], reviewReasons: [], preprocessing: null, error: null, pid: process.pid,
    } });
  }
});
