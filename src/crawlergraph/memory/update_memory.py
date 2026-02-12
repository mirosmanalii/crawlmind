from crawlergraph.state import CrawlState
from crawlergraph.memory.loop_guards import compute_page_hash


def update_memory(state: CrawlState, dom: str) -> CrawlState:
    """
    Updates crawl memory after a successful page observation.
    """

    page_hash = compute_page_hash(dom)

    # Store fingerprint in state
    state.page_hash = page_hash

    # Track visited URLs
    state.visited_pages.add(state.current_url)

    # Track URL visit counts
    state.url_visit_counts[state.current_url] = (
        state.url_visit_counts.get(state.current_url, 0) + 1
    )

    return state
