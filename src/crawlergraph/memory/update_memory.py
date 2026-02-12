from crawlergraph.state import CrawlState
from crawlergraph.memory.loop_guards import compute_page_hash

def update_memory(state: CrawlState) -> CrawlState:
    state.visited_pages.add(state.current_url)

    state.url_visit_counts[state.current_url] = (
        state.url_visit_counts.get(state.current_url, 0) + 1
    )

    return state
