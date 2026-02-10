from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DefectCategory(str, Enum):
    FUNCTIONAL = "Functional"
    UI = "UI"
    PERFORMANCE = "Performance"
    ACCESSIBILITY = "Accessibility"
    CONTENT = "Content"
    SECURITY = "Security"


class Defect(BaseModel):
    category: DefectCategory
    subtype: str

    severity: int = Field(ge=1, le=10)
    confidence: float = Field(ge=0.0, le=1.0)

    description: str
    evidence: Dict

    detected_at: datetime = Field(default_factory=datetime.timezone.utc.now)
