import { Page } from "playwright";

export class ScreenshotManager {
  private page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async captureFullPage(): Promise<string | undefined> {
    try {
      const buffer = await this.page.screenshot({
        fullPage: true,
        type: "png",
      });

      return buffer.toString("base64");
    } catch (err) {
      // Do not crash worker if screenshot fails
      return undefined;
    }
  }
}
