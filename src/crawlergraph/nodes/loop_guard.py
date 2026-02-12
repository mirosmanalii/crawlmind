from crawlergraph.state import CrawlState
from crawlergraph.memory.loop_guards import check_loop_conditions


from crawlergraph.state import CrawlState


def loop_guard_node(state: CrawlState) -> CrawlState:
    """
    Stop if loop conditions triggered.
    """

    # Max pages
    if len(state.visited_pages) >= state.max_pages:
        state.stop_reason = "Max pages limit reached"

    # Max depth
    if state.depth > state.max_depth:
        state.stop_reason = "Max depth exceeded"

    # Duplicate content
    if state.page_hash in state.loop_counters:
        state.stop_reason = "Duplicate page content detected"

    # Update loop counter
    if state.page_hash:
        state.loop_counters[state.page_hash] = (
            state.loop_counters.get(state.page_hash, 0) + 1
        )

    return state
