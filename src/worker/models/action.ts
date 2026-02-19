export type ActionType =
  | "CLICK"
  | "TYPE"
  | "SUBMIT"
  | "PAGINATE"
  | "WAIT"
  | "STOP";

export interface ActionDecision {
  action: ActionType;
  target?: string;
  value?: string;
  rationale: string;
  confidence: number;
}
