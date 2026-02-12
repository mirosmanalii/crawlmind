"""
Loop Detection and Crawl Guard Logic
"""

import hashlib
from crawlergraph.state import CrawlState

# Page Hash Utility
def compute_page_hash(dom: str) -> str:
    """
    Compute deterministic hash of DOM content.
    """
    return hashlib.sha256(dom.encode("utf-8")).hexdigest()

# Loop Detection Logic
def check_loop_conditions(state: CrawlState, dom: str) -> bool:
    """
    Returns True if crawl should stop due to loop conditions.
    """

    page_hash = compute_page_hash(dom)

    # Max page limit
    if len(state.visited_pages) >= state.max_pages:
        state.stop_reason = "Max pages limit reached"
        return True

    # Max depth guard
    if state.depth > state.max_depth:
        state.stop_reason = "Max depth exceeded"
        return True

    # Duplicate content detection
    if state.page_hash == page_hash:
        state.stop_reason = "Duplicate page content detected"
        return True

    # Excessive visits to same URL
    visits = state.url_visit_counts.get(state.current_url, 0)
    if visits >= 3:
        state.stop_reason = "Too many visits to same URL"
        return True

    return False
