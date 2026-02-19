export class ActionExecutionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ActionExecutionError";
  }
}

export class SelectorNotFoundError extends Error {
  constructor(selector: string) {
    super(`Selector not found: ${selector}`);
    this.name = "SelectorNotFoundError";
  }
}

export class ActionTimeoutError extends Error {
  constructor(action: string) {
    super(`Action timed out: ${action}`);
    this.name = "ActionTimeoutError";
  }
}
