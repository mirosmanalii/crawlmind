import { BrowserSession } from "./core/browserSession";
import { ActionDecision } from "./models/action";
import { ObservationPayload } from "./models/observation";
import { SignalCollector } from "./core/signalCollector";
import { ActionExecutor } from "./core/actionExecutor";
import { ScreenshotManager } from "./core/screenshotManager";

export class PlaywrightWorker {
  private session = new BrowserSession();

  async init() {
    await this.session.init();
  }

  async navigate(url: string): Promise<void> {
    const page = this.session.getPage();
    await page.goto(url, { waitUntil: "networkidle" });
  }

  async execute(action: ActionDecision): Promise<ObservationPayload> {
    const page = this.session.getPage();

    const collector = new SignalCollector(page);
    collector.reset();
    collector.attach();

    const executor = new ActionExecutor(page);
    const screenshotManager = new ScreenshotManager(page);

    try {
      await executor.execute(action);

      await collector.capturePerformanceTiming();

      const dom = await page.content();
      const screenshot = await screenshotManager.captureFullPage();

      const signals = collector.getSignals();

      return {
        dom,
        screenshot,
        signals: {
          statusCode: signals.statusCode,
          console: {
            errors: signals.consoleErrors,
            warnings: signals.consoleWarnings,
          },
          network: {
            failedRequests: signals.failedRequests,
            requestErrors: signals.requestErrors,
          },
          performance: {
            loadTimeMs: signals.loadTimeMs,
          },
          redirects: signals.redirects,
        },
      };
    } catch (err) {
      const screenshot = await screenshotManager.captureFullPage();

      return {
        dom: "",
        screenshot,
        signals: {
          statusCode: undefined,
          console: {
            errors: [String(err)],
            warnings: [],
          },
          network: {
            failedRequests: 0,
            requestErrors: [],
          },
          performance: {},
          redirects: [],
        },
      };
    }
  }

  async close() {
    await this.session.close();
  }
}
