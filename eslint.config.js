export default [{
  ignores: ['node_modules/**', 'assets/**', 'reports/**', 'debug/**'],
}, {
  files: ['**/*.js'],
  languageOptions: { ecmaVersion: 'latest', sourceType: 'module', globals: {
    process: 'readonly', console: 'readonly', Buffer: 'readonly', URL: 'readonly',
    AbortController: 'readonly', AbortSignal: 'readonly', performance: 'readonly', setTimeout: 'readonly', clearTimeout: 'readonly',
  } },
  rules: { 'no-unused-vars': ['error', { argsIgnorePattern: '^_' }], 'no-undef': 'error',
    'no-unreachable': 'error', 'no-dupe-args': 'error', 'no-dupe-keys': 'error',
    'no-constant-condition': ['error', { checkLoops: false }], eqeqeq: 'error', 'no-var': 'error' },
}];
