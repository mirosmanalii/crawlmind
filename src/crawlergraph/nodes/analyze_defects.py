"""
LangGraph Node: analyze_defects

Responsible for:
- Running defect detection rules
- Updating CrawlState.detected_defects

Contains NO classification logic.
Contains NO scoring logic.
Contains NO orchestration logic.
"""

from crawlergraph.state import CrawlState
from crawlergraph.defects.rules import detect_defects


def analyze_defects(state: CrawlState) -> CrawlState:
    """
    LangGraph node for defect detection.

    Reads:
        - state.page_features
        - state.signals

    Writes:
        - state.detected_defects
    """

    defects = detect_defects(
        features=state.page_features,
        signals=state.signals,
    )

    state.detected_defects = defects

    return state
