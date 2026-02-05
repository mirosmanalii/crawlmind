from typing import List, Optional
from pydantic import BaseModel
from crawler_graph.state import (
    PageType,
    Defect,
    ActionDecision,
    StopReason
)


class PageSummary(BaseModel):
    url: str
    page_type: PageType
    confidence: float


class LangGraphOutput(BaseModel):
    graph_version: str
    run_id: str

    page: PageSummary

    next_action: Optional[ActionDecision]
    defects: List[Defect]

    stop_reason: Optional[StopReason]
