from crawlergraph.state import CrawlState
from crawlergraph.memory.loop_guards import check_loop_conditions


def loop_guard_node(state: CrawlState, dom: str) -> CrawlState:
    should_stop = check_loop_conditions(state, dom)

    if should_stop:
        state.next_action = None  # clear pending action
    return state
