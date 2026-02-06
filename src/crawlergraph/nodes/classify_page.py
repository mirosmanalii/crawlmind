from crawler_graph.state import CrawlState
from crawler_graph.classifiers.page_type import classify_page_type


def classify_page(state: CrawlState) -> CrawlState:
    """
    LangGraph node:
    Determines page type based on extracted features and runtime signals.
    """

    page_type, confidence = classify_page_type(
        features=state.page_features.dict(),
        signals=state.signals.dict()
    )

    state.page_type = page_type
    state.page_confidence = confidence

    return state
