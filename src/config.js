import { fileURLToPath } from 'node:url';
export const ROOT = fileURLToPath(new URL('../', import.meta.url));
export const ASSET_DIR = fileURLToPath(new URL('../assets/', import.meta.url));
export const WHITELIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
export const OCR_CONFIG = Object.freeze({ language: 'eng', oem: 1, psm: 7,
  whitelist: WHITELIST, init: { load_system_dawg: '0', load_freq_dawg: '0' },
  variants: ['V0', 'V1', 'V2', 'V3'], confidenceThreshold: 80 });
export const LIMITS = Object.freeze({ bytes: 10 * 1024 * 1024, inputPixels: 20_000_000,
  outputPixels: 10_000_000, longEdge: 3000, padding: 16 });
