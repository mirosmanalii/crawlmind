import { Page } from "playwright";
import { ActionDecision } from "../models/action";
import { ActionGuard } from "./actionGuard";

export class ActionExecutor {
  private page: Page;
  private guard: ActionGuard;

  constructor(page: Page) {
    this.page = page;
    this.guard = new ActionGuard(page);
  }

  async execute(action: ActionDecision) {
    switch (action.action) {
      case "CLICK":
        await this.handleClick(action);
        break;

      case "TYPE":
        await this.handleType(action);
        break;

      case "SUBMIT":
        await this.handleSubmit(action);
        break;

      case "PAGINATE":
        await this.handlePaginate(action);
        break;

      case "WAIT":
        await this.page.waitForTimeout(1000);
        break;

      case "STOP":
        return;
    }
  }

  private async handleClick(action: ActionDecision) {
    if (!action.target) return;

    await this.guard.ensureSelectorExists(action.target);

    await this.guard.withTimeout(
      this.page.click(action.target),
      "CLICK"
    );

    await this.guard.safeNavigationWait();
  }

  private async handleType(action: ActionDecision) {
    if (!action.target || !action.value) return;

    await this.guard.ensureSelectorExists(action.target);

    await this.guard.withTimeout(
      this.page.fill(action.target, action.value),
      "TYPE"
    );
  }

  private async handleSubmit(action: ActionDecision) {
    if (!action.target) {
      // fallback: submit first form
      await this.page.keyboard.press("Enter");
    } else {
      await this.guard.ensureSelectorExists(action.target);
      await this.guard.withTimeout(
        this.page.click(action.target),
        "SUBMIT"
      );
    }

    await this.guard.safeNavigationWait();
  }

  private async handlePaginate(action: ActionDecision) {
    if (!action.target) return;

    await this.guard.ensureSelectorExists(action.target);

    await this.guard.withTimeout(
      this.page.click(action.target),
      "PAGINATE"
    );

    await this.guard.safeNavigationWait();
  }
}
