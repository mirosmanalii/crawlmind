import { chromium, Browser, Page } from "playwright";

export class BrowserSession {
  private browser?: Browser;
  private page?: Page;

  async init() {
    this.browser = await chromium.launch({ headless: true });
    const context = await this.browser.newContext();
    this.page = await context.newPage();
  }

  getPage(): Page {
    if (!this.page) {
      throw new Error("Browser not initialized");
    }
    return this.page;
  }

  async close() {
    await this.browser?.close();
  }
}
