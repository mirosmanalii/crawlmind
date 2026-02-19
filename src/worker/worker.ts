import { BrowserSession } from "./core/browserSession";
import { ActionDecision } from "./models/action";
import { ObservationPayload } from "./models/observation";
import { SignalCollector } from "./core/signalCollector";
import { ActionExecutor } from "./core/actionExecutor";

export class PlaywrightWorker {
  private session = new BrowserSession();

  async init() {
    await this.session.init();
  }

  async execute(action: ActionDecision): Promise<ObservationPayload> {
    const page = this.session.getPage();

    // Initialize signal collection for this execution cycle
    const collector = new SignalCollector(page);
    collector.reset();
    collector.attach();

    const executor = new ActionExecutor(page);

    try {
      // Execute action safely
      await executor.execute(action);

      // Capture performance metrics
      await collector.capturePerformanceTiming();

      // Capture final DOM snapshot
      const dom = await page.content();

      const signals = collector.getSignals();

      return {
        dom,
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
      // Hard failure fallback — worker must never crash
      return {
        dom: "",
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
