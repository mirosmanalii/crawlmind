import { Page, ConsoleMessage, Request, Response } from "playwright";

export interface CollectedSignals {
  statusCode?: number;
  consoleErrors: string[];
  consoleWarnings: string[];
  failedRequests: number;
  requestErrors: string[];
  redirects: string[];
  loadTimeMs?: number;
}

export class SignalCollector {
  private page: Page;
  private signals: CollectedSignals;

  constructor(page: Page) {
    this.page = page;
    this.signals = this.createEmptySignals();
  }

  private createEmptySignals(): CollectedSignals {
    return {
      consoleErrors: [],
      consoleWarnings: [],
      failedRequests: 0,
      requestErrors: [],
      redirects: [],
    };
  }

  reset() {
    this.signals = this.createEmptySignals();
  }

  attach() {
    this.page.on("console", (msg: ConsoleMessage) => {
      if (msg.type() === "error") {
        this.signals.consoleErrors.push(msg.text());
      }
      if (msg.type() === "warning") {
        this.signals.consoleWarnings.push(msg.text());
      }
    });

    this.page.on("requestfailed", (request: Request) => {
      this.signals.failedRequests += 1;
      this.signals.requestErrors.push(
        `${request.url()} - ${request.failure()?.errorText}`
      );
    });

    this.page.on("response", (response: Response) => {
      if (response.request().resourceType() === "document") {
        this.signals.statusCode = response.status();

        const redirectedFrom = response.request().redirectedFrom();
        if (redirectedFrom) {
          this.signals.redirects.push(redirectedFrom.url());
        }
      }
    });

    this.page.on("crash", () => {
      this.signals.consoleErrors.push("Page crashed");
    });
  }

  async capturePerformanceTiming() {
    try {
      const timing = await this.page.evaluate(() => {
        const [nav] = performance.getEntriesByType("navigation");
        return nav ? nav.duration : undefined;
      });

      if (timing) {
        this.signals.loadTimeMs = Math.round(timing);
      }
    } catch {
      // Ignore performance errors
    }
  }

  getSignals(): CollectedSignals {
    return this.signals;
  }
}
