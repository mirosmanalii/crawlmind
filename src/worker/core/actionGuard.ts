import { Page } from "playwright";
import {
  SelectorNotFoundError,
  ActionTimeoutError,
} from "../errors/workerErrors";

export class ActionGuard {
  private page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async ensureSelectorExists(selector: string, timeout = 5000) {
    try {
      await this.page.waitForSelector(selector, {
        timeout,
        state: "attached",
      });
    } catch {
      throw new SelectorNotFoundError(selector);
    }
  }

  async withTimeout<T>(
    promise: Promise<T>,
    actionName: string,
    timeout = 10000
  ): Promise<T> {
    const timeoutPromise = new Promise<never>((_, reject) =>
      setTimeout(() => reject(new ActionTimeoutError(actionName)), timeout)
    );

    return Promise.race([promise, timeoutPromise]);
  }

  async safeNavigationWait(timeout = 15000) {
    try {
      await this.page.waitForLoadState("networkidle", { timeout });
    } catch {
      // Do not throw; network idle can be unreliable in SPAs
    }
  }
}
