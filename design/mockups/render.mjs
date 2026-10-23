import puppeteer from "puppeteer-core";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const dir = path.dirname(new URL(import.meta.url).pathname);
const outDir = path.join(dir, "png");
await mkdir(outDir, { recursive: true });

const pages = [
  ["descriptions-1280.html", 1280],
  ["descriptions-360.html", 360],
  ["market-1280.html", 1280],
  ["market-360.html", 360],
  ["gaps-1280.html", 1280],
  ["gaps-360.html", 360],
  ["descriptions-empty-1280.html", 1280],
  ["descriptions-empty-360.html", 360],
  ["descriptions-loading-1280.html", 1280],
  ["descriptions-error-1280.html", 1280],
  ["sign-in-1280.html", 1280],
  ["sign-in-360.html", 360],
];

const browser = await puppeteer.launch({
  executablePath: "/usr/local/bin/google-chrome",
  headless: true,
  args: [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--font-render-hinting=none",
    "--disable-lcd-text",
  ],
});

const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 2 });

const probe = pathToFileURL(path.join(dir, "descriptions-1280.html")).href;
await page.goto(probe, { waitUntil: "networkidle0" });
await page.evaluate(() => document.fonts.ready);
const weights = await page.evaluate(() => {
  const c = document.createElement("canvas").getContext("2d");
  c.font = '400 32px "Schibsted Grotesk"';
  const regular = c.measureText("RoleFit Harbor").width;
  c.font = '600 32px "Schibsted Grotesk"';
  const bold = c.measureText("RoleFit Harbor").width;
  c.font = '400 32px "IBM Plex Mono"';
  const mono = c.measureText("PostgreSQL 5").width;
  c.font = "400 32px sans-serif";
  const fallback = c.measureText("PostgreSQL 5").width;
  return {
    regular,
    bold,
    mono,
    fallback,
    ui: document.fonts.check('16px "Schibsted Grotesk"'),
    monoOk: document.fonts.check('16px "IBM Plex Mono"'),
  };
});
console.log(JSON.stringify(weights));
if (!weights.ui || !weights.monoOk) {
  throw new Error("Fonts did not load");
}
if (weights.regular === weights.bold) {
  throw new Error("Schibsted Grotesk bold did not differ from regular");
}
if (Math.abs(weights.mono - weights.fallback) < 1) {
  throw new Error("IBM Plex Mono looks like the fallback sans");
}

for (const [file, width] of pages) {
  await page.setViewport({ width, height: 800, deviceScaleFactor: 2 });
  const url = pathToFileURL(path.join(dir, file)).href;
  await page.goto(url, { waitUntil: "networkidle0" });
  await page.evaluate(() => document.fonts.ready);
  const png = path.join(outDir, file.replace(".html", ".png"));
  await page.screenshot({ path: png, fullPage: true });
  const box = await page.evaluate(() => ({
    w: document.body.scrollWidth,
    h: document.body.scrollHeight,
  }));
  console.log(`${file} -> ${png} css ${box.w}x${box.h}`);
}

await browser.close();
