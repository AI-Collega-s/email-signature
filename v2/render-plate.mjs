// Rendert v2/assets/plate.html naar v2/assets/plate.png op 2x.
// Vereist playwright: npx playwright install chromium, daarna: node v2/render-plate.mjs
import { chromium } from "playwright";
import { fileURLToPath } from "node:url";
import path from "node:path";

const dir = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(dir, "assets", "plate.html");
const out = path.join(dir, "assets", "plate.png");

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 640, height: 600 }, deviceScaleFactor: 2 });
await page.goto("file://" + src);
await page.waitForTimeout(2500); // webfonts
const plate = await page.$("body > table");
const box = await plate.boundingBox();
await plate.screenshot({ path: out, omitBackground: true });
console.log(`plate.png: ${Math.round(box.width)} x ${Math.round(box.height)} css-px (2x)`);
await browser.close();
