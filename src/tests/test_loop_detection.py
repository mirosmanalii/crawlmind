from crawlergraph.state import CrawlState
from crawlergraph.memory.loop_guards import check_loop_conditions
from crawlergraph.memory.update_memory import update_memory


def test_duplicate_page_hash_detection():
    dom = "<html><body>Hello</body></html>"

    state = CrawlState(
        run_id="test",
        current_url="https://example.com"
    )

    update_memory(state, dom)

    should_stop = check_loop_conditions(state, dom)

    assert should_stop is True
    assert state.stop_reason == "Duplicate page content detected"


def test_max_visits_per_url():
    dom = "<html><body>Page</body></html>"

    state = CrawlState(
        run_id="test",
        current_url="https://example.com",
        max_visits_per_url=2
    )

    update_memory(state, dom)
    update_memory(state, dom)

    should_stop = check_loop_conditions(state, dom)

    assert should_stop is True


def test_max_total_pages():
    dom = "<html><body>Page</body></html>"

    state = CrawlState(
        run_id="test",
        current_url="https://example.com",
        max_total_pages=1
    )

    update_memory(state, dom)

    should_stop = check_loop_conditions(state, dom)

    assert should_stop is True
