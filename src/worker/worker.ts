import { BrowserSession } from "./core/browserSession";
import { ActionDecision } from "./models/action";
import { ObservationPayload } from "./models/observation";
import { SignalCollector } from "./core/signalCollector";

export class PlaywrightWorker {
  private session = new BrowserSession();

  async init() {
    await this.session.init();
  }

  async execute(action: ActionDecision): Promise<ObservationPayload> {
  const page = this.session.getPage();

  const collector = new SignalCollector(page);
  collector.reset();
  collector.attach();

  const startTime = Date.now();

  try {
    await this.performAction(page, action);
    await page.waitForLoadState("networkidle");

    await collector.capturePerformanceTiming();

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
    return {
      dom: "",
      signals: {
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

  private async performAction(page: any, action: ActionDecision) {
    switch (action.action) {
      case "CLICK":
        await page.click(action.target!);
        break;
      case "TYPE":
        await page.fill(action.target!, action.value!);
        break;
      case "WAIT":
        await page.waitForTimeout(1000);
        break;
      case "STOP":
        return;
      default:
        break;
    }
  }
}
