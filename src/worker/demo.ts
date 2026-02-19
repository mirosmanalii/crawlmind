import { PlaywrightWorker } from "./worker";
import fs from "fs";
import path from "path";

async function runDemo() {
  const url = process.argv[2];

  if (!url) {
    console.error("Usage: ts-node demo.ts <url>");
    process.exit(1);
  }

  const worker = new PlaywrightWorker();
  await worker.init();

  console.log(`Navigating to ${url}`);
  await worker.navigate(url);

  console.log("Executing WAIT action...");
  const waitObservation = await worker.execute({
    action: "WAIT",
    rationale: "Initial wait",
    confidence: 1.0,
  });

  saveScreenshot(waitObservation.screenshot, "step1_wait");

  console.log("Executing CLICK action (if links exist)...");
  const clickObservation = await worker.execute({
    action: "CLICK",
    target: "a",
    rationale: "Click first link",
    confidence: 0.8,
  });

  saveScreenshot(clickObservation.screenshot, "step2_click");

  console.log("Demo complete. Closing browser...");
  await worker.close();
}

function saveScreenshot(base64?: string, name?: string) {
  if (!base64 || !name) return;

  const outputDir = path.join(__dirname, "screenshots");
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }

  const filePath = path.join(outputDir, `${name}.png`);
  const buffer = Buffer.from(base64, "base64");
  fs.writeFileSync(filePath, buffer);

  console.log(`Saved screenshot: ${filePath}`);
}

runDemo().catch((err) => {
  console.error("Demo failed:", err);
});
