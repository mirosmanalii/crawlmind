"""
LangGraph Node: classify_page

Thin wrapper that applies page-type classification rules
to the current CrawlState and updates the state in-place.
"""

from crawlergraph.state import CrawlState
from crawlergraph.classifiers.page_type import classify_page_type


def classify_page(state: CrawlState) -> CrawlState:
    """
    LangGraph node for page-type classification.

    Inputs (from state):
        - state.page_features
        - state.signals

    Outputs (written to state):
        - state.page_type
        - state.page_confidence
    """

    page_type, confidence = classify_page_type(
        features=state.page_features,
        signals=state.signals
    )

    state.page_type = page_type
    state.page_confidence = confidence

    return state
