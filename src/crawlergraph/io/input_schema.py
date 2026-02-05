from typing import Dict, Optional
from pydantic import BaseModel, Field


class CrawlConfig(BaseModel):
    max_pages: int = 100
    max_depth: int = 5
    confidence_threshold: float = 0.7


class ObservationPayload(BaseModel):
    """
    Supplied by the external browser/orchestrator.
    """
    url: str
    dom: str
    signals: Dict


class LangGraphInput(BaseModel):
    run_id: str
    start_url: str
    config: CrawlConfig
    observation: ObservationPayload
