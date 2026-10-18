#!/usr/bin/env node
/**
 * fetch-captcha-png.mjs
 *
 * Gọi 1 API trả JSON dạng:
 * {
 *   "status": 200,
 *   "error": false,
 *   "message": "OK",
 *   "data": {
 *     "id": "0134ca7a-...",
 *     "captcha": "data:image/png;base64,iVBORw0KGgo...",
 *     "expiredTime": 1792280315047,
 *     "countTime": 600000
 *   },
 *   "messageKey": "common.no_header"
 * }
 *
 * Lấy đúng trường `data.captcha`, bỏ tiền tố `data:image/png;base64,`,
 * giải base64 rồi ghi ra file PNG.
 *
 * Có thể chạy nhiều lần liên tiếp (reload) với khoảng cách thời gian tuỳ chỉnh
 * để thu thập nhiều ảnh trong một lệnh.
 *
 * Cách dùng:
 *   node scripts/fetch-captcha-png.mjs <url> [outputFile]
 *
 * Ví dụ:
 *   node scripts/fetch-captcha-png.mjs "https://example.com/api/captcha"
 *   -> lưu tự động vào ./captcha/captcha-<id>-<timestamp>.png
 *
 *   node scripts/fetch-captcha-png.mjs "https://example.com/api/captcha" ./tmp/my-captcha.png
 *   -> lưu đúng đường dẫn truyền vào
 *
 *   node scripts/fetch-captcha-png.mjs "https://example.com/api/captcha" --count 20 --interval 1500
 *   -> lấy 20 ảnh, mỗi lần cách nhau 1500ms, tên file có thêm số thứ tự:
 *      ./captcha/captcha-<id>-<timestamp>-01.png ... -20.png
 *
 *   node scripts/fetch-captcha-png.mjs <url> --n 10 --delay 500
 *   -> rút gọn: --n = --count, --delay = --interval
 *
 * Tuỳ chọn (biến môi trường):
 *   CAPTCHA_HEADERS      JSON object, gửi thêm header, ví dụ: '{"Cookie":"a=b"}'
 *   CAPTCHA_FIELD        đường dẫn field chứa ảnh, mặc định "data.captcha"
 *   CAPTCHA_TIMEOUT_MS   timeout request, mặc định 30000
 *   CAPTCHA_COUNT        số lần lấy, mặc định 1
 *   CAPTCHA_INTERVAL_MS  khoảng cách giữa các lần (ms), mặc định 1500
 *   CAPTCHA_RETRIES      số lần thử lại khi 1 lượt lỗi, mặc định 0
 */

import { mkdir, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { setTimeout as sleep } from "node:timers/promises";

const DEFAULT_FIELD = "data.captcha";
const DEFAULT_TIMEOUT_MS = 30_000;
const DEFAULT_OUT_DIR = "captcha";
const DEFAULT_COUNT = 1;
const DEFAULT_INTERVAL_MS = 1_500;
const DEFAULT_RETRIES = 0;

function parseArgs(argv) {
  const args = argv.filter((a) => a !== "--");
  const flags = {};
  const positional = [];

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const [rawKey, inlineValue] = arg.slice(2).split("=", 2);
      const key = rawKey.replace(/-/g, "_");
      if (inlineValue !== undefined) {
        flags[key] = inlineValue;
      } else if (args[i + 1] && !args[i + 1].startsWith("--")) {
        flags[key] = args[i + 1];
        i += 1;
      } else {
        flags[key] = true;
      }
      continue;
    }
    positional.push(arg);
  }

  return {
    url: positional[0] ?? flags.url,
    output: positional[1] ?? flags.out ?? flags.output,
    field: typeof flags.field === "string" ? flags.field : (process.env.CAPTCHA_FIELD || DEFAULT_FIELD),
    count: readInt(flags.count ?? flags.n ?? process.env.CAPTCHA_COUNT, DEFAULT_COUNT, "count"),
    intervalMs: readInt(flags.interval ?? flags.delay ?? process.env.CAPTCHA_INTERVAL_MS, DEFAULT_INTERVAL_MS, "interval"),
    retries: readInt(flags.retries ?? process.env.CAPTCHA_RETRIES, DEFAULT_RETRIES, "retries"),
  };
}

/** Đọc số nguyên >= min, có fallback khi thiếu/sai định dạng. */
function readInt(value, fallback, name, min = 0) {
  if (value === undefined || value === true || value === "") return fallback;
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < min) {
    throw new Error(`Giá trị --${name} không hợp lệ: ${value}`);
  }
  return Math.floor(parsed);
}

/** Lấy giá trị theo đường dẫn "a.b.c", hỗ trợ mảng: "data.items.0.captcha". */
function pick(obj, path) {
  return path.split(".").reduce((acc, key) => (acc == null ? undefined : acc[key]), obj);
}

/** Chuyển mọi dạng ảnh (data URI, base64 thuần, buffer) thành Buffer PNG. */
function toPngBuffer(captcha) {
  if (Buffer.isBuffer(captcha)) return captcha;
  if (typeof captcha !== "string") {
    throw new Error(`Trường captcha không phải string (nhận: ${typeof captcha})`);
  }

  const raw = captcha.trim();
  if (!raw) throw new Error("Trường captcha rỗng");

  // data:image/png;base64,XXXX -> XXXX
  const base64 = raw.includes("base64,") ? raw.slice(raw.indexOf("base64,") + 7) : raw;

  const buffer = Buffer.from(base64.replace(/\s+/g, ""), "base64");
  if (buffer.length === 0) {
    throw new Error("Giải base64 thất bại: file rỗng hoặc dữ liệu không hợp lệ");
  }
  return buffer;
}

/** Kiểm tra chữ ký PNG (89 50 4E 47 0D 0A 1A 0A). */
function isPng(buffer) {
  return buffer.length > 8 && buffer.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
}

function buildHeaders() {
  const headers = {
    accept: "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
  };

  const raw = process.env.CAPTCHA_HEADERS;
  if (raw) {
    try {
      Object.assign(headers, JSON.parse(raw));
    } catch {
      throw new Error("CAPTCHA_HEADERS không phải JSON hợp lệ");
    }
  }
  return headers;
}

/** Một lượt lấy: fetch -> parse -> decode base64 -> trả về Buffer PNG. */
async function fetchOnce(url, field, timeoutMs) {
  const response = await fetch(url, { headers: buildHeaders(), signal: AbortSignal.timeout(timeoutMs) });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status} ${response.statusText}`);
  }

  const body = await response.json();
  if (body?.status && Number(body.status) >= 400) {
    throw new Error(`API báo lỗi: status=${body.status} message=${body.message ?? ""}`);
  }

  const png = toPngBuffer(pick(body, field));
  if (!isPng(png)) {
    console.warn(`[captcha] Cảnh báo: dữ liệu không có chữ ký PNG hợp lệ, vẫn ghi file (${png.length} bytes).`);
  }

  return { png, id: pick(body, "data.id") ?? "captcha", expiredTime: pick(body, "data.expiredTime") };
}

async function main() {
  const { url, output, field, count, intervalMs, retries } = parseArgs(process.argv.slice(2));

  if (!url) {
    console.error("Thiếu URL. Cách dùng: node scripts/fetch-captcha-png.mjs <url> [outputFile]");
    process.exitCode = 1;
    return;
  }
  if (count > 1 && output) {
    console.warn("[captcha] Lưu ý: nhiều lượt + đường dẫn cố định sẽ ghi đè lên nhau.");
  }

  const timeoutMs = Number(process.env.CAPTCHA_TIMEOUT_MS || DEFAULT_TIMEOUT_MS);
  const suffixWidth = String(count).length > 2 ? String(count).length : 2;

  if (count > 1) {
    console.log(`[captcha] Lấy ${count} ảnh, mỗi lượt cách nhau ${intervalMs}ms`);
  }

  let ok = 0;
  let failed = 0;

  for (let i = 1; i <= count; i += 1) {
    if (i > 1) await sleep(intervalMs);

    const label = count > 1 ? `[${i}/${count}]` : "";
    let result = null;
    let lastError = null;

    for (let attempt = 0; attempt <= retries && !result; attempt += 1) {
      if (attempt > 0) console.log(`[captcha] ${label} thử lại lần ${attempt}/${retries}...`);
      try {
        result = await fetchOnce(url, field, timeoutMs);
      } catch (error) {
        lastError = error;
      }
    }

    if (!result) {
      failed += 1;
      console.error(`[captcha] ${label} LỖI: ${lastError?.message ?? lastError}`);
      continue;
    }

    const { png, id, expiredTime } = result;
    const suffix = count > 1 ? `-${String(i).padStart(suffixWidth, "0")}` : "";
    const outFile = output
      ? resolve(output)
      : resolve(DEFAULT_OUT_DIR, `captcha-${id}-${Date.now()}${suffix}.png`);

    await mkdir(dirname(outFile), { recursive: true });
    await writeFile(outFile, png);
    ok += 1;

    console.log(`[captcha] ${label} id=${id} size=${png.length}B expired=${expiredTime ?? "n/a"} -> ${outFile}`);
  }

  console.log(`[captcha] Xong: ${ok} thành công, ${failed} lỗi / tổng ${count}`);
  if (failed > 0) process.exitCode = 1;
}

main().catch((error) => {
  console.error(`[captcha] LỖI: ${error?.message ?? error}`);
  process.exitCode = 1;
});