from enum import Enum
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime


# -----------------------------
# Enums
# -----------------------------

class PageType(str, Enum):
    LOGIN = "LOGIN"
    AUTH_CHALLENGE = "AUTH_CHALLENGE"
    FORM = "FORM"
    LISTING = "LISTING"
    DETAIL = "DETAIL"
    DASHBOARD = "DASHBOARD"
    PAGINATION = "PAGINATION"
    ERROR = "ERROR"
    EMPTY = "EMPTY"
    UNKNOWN = "UNKNOWN"


class DefectCategory(str, Enum):
    FUNCTIONAL = "Functional"
    UI = "UI"
    PERFORMANCE = "Performance"
    ACCESSIBILITY = "Accessibility"
    CONTENT = "Content"
    SECURITY = "Security"


class StopReason(str, Enum):
    MAX_PAGES_REACHED = "MAX_PAGES_REACHED"
    MAX_DEPTH_REACHED = "MAX_DEPTH_REACHED"
    LOOP_DETECTED = "LOOP_DETECTED"
    NO_VALID_ACTIONS = "NO_VALID_ACTIONS"
    TERMINAL_ERROR = "TERMINAL_ERROR"
    SUCCESS = "SUCCESS"


class ActionType(str, Enum):
    CLICK = "CLICK"
    TYPE = "TYPE"
    SUBMIT = "SUBMIT"
    PAGINATE = "PAGINATE"
    WAIT = "WAIT"
    STOP = "STOP"


# -----------------------------
# Feature Models
# -----------------------------

class PageFeatures(BaseModel):
    has_form: bool = False
    has_username_input: bool = False
    has_password_input: bool = False
    input_count: int = 0
    submit_button_count: int = 0

    table_count: int = 0
    pagination_controls: bool = False

    error_banners: bool = False
    empty_state_detected: bool = False

    url_patterns: List[str] = Field(default_factory=list)


class RuntimeSignals(BaseModel):
    status_code: int = 200
    redirect_detected: bool = False

    console_errors: List[str] = Field(default_factory=list)
    console_warnings: List[str] = Field(default_factory=list)

    network_errors: List[str] = Field(default_factory=list)
    failed_requests: int = 0

    layout_overlaps: bool = False
    long_tasks_ms: Optional[int] = None
    page_load_time_ms: Optional[int] = None


# -----------------------------
# Defects
# -----------------------------

class Defect(BaseModel):
    category: DefectCategory
    subtype: str

    severity: int = Field(ge=1, le=10)
    priority: int = Field(ge=1, le=10)
    confidence: float = Field(ge=0.0, le=1.0)

    description: str
    evidence: Dict = Field(default_factory=dict)

    detected_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------------
# Actions
# -----------------------------

class ActionDecision(BaseModel):
    action: ActionType
    target: Optional[str] = None
    value: Optional[str] = None

    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)


class ActionRecord(BaseModel):
    action: ActionType
    target: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# -----------------------------
# Crawl State
# -----------------------------

class CrawlState(BaseModel):
    """
    Canonical LangGraph state.
    Passed between every node.
    """

    # Identity & versioning
    run_id: str
    graph_version: str = "v1"

    # Navigation context
    current_url: str
    previous_url: Optional[str] = None
    depth: int = 0

    # Page fingerprinting
    page_hash: Optional[str] = None
    normalized_url: Optional[str] = None

    # Page understanding
    page_type: PageType = PageType.UNKNOWN
    page_confidence: float = 0.0
    page_features: PageFeatures = Field(default_factory=PageFeatures)

    # Runtime signals
    signals: RuntimeSignals = Field(default_factory=RuntimeSignals)

    # Crawl memory
    visited_pages: Set[str] = Field(default_factory=set)
    url_visit_counts: Dict[str, int] = Field(default_factory=dict)
    action_history: List[ActionRecord] = Field(default_factory=list)

    # Loop detection
    loop_counters: Dict[str, int] = Field(default_factory=dict)

    # Defects
    detected_defects: List[Defect] = Field(default_factory=list)

    # Decision output
    next_action: Optional[ActionDecision] = None
    stop_reason: Optional[StopReason] = None

    # Safety limits
    max_pages: int = 100
    max_depth: int = 5

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            set: list
        }
