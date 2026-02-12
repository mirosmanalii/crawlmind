"""
LangGraph Node: evaluate_stop
Determines whether crawl should terminate.
"""

from crawlergraph.state import CrawlState


def evaluate_stop_node(state: CrawlState) -> str:
    """
    Returns next edge key:
        - "stop"
        - "continue"
    """

    if state.stop_reason is not None:
        return "stop"

    return "continue"
