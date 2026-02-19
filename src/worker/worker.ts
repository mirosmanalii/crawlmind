import { BrowserSession } from "./core/browserSession";
import { ActionDecision } from "./models/action";
import { ObservationPayload } from "./models/observation";

export class PlaywrightWorker {
  private session = new BrowserSession();

  async init() {
    await this.session.init();
  }

  async execute(action: ActionDecision): Promise<ObservationPayload> {
    const page = this.session.getPage();

    try {
      await this.performAction(page, action);
      await page.waitForLoadState("networkidle");

      const dom = await page.content();

      return {
        dom,
        signals: {
          console: { errors: [], warnings: [] },
          network: { failedRequests: 0, requestErrors: [] },
          performance: {},
          redirects: [],
        },
      };
    } catch (err) {
      return {
        dom: "",
        signals: {
          console: { errors: [String(err)], warnings: [] },
          network: { failedRequests: 0, requestErrors: [] },
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
