from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    CLICK = "CLICK"
    TYPE = "TYPE"
    SUBMIT = "SUBMIT"
    PAGINATE = "PAGINATE"
    WAIT = "WAIT"
    STOP = "STOP"


class ActionDecision(BaseModel):
    action: ActionType
    target: Optional[str] = None
    value: Optional[str] = None

    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)
