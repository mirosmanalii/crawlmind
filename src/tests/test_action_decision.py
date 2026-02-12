from crawlergraph.state import CrawlState, PageType
from crawlergraph.nodes.decide_action import decide_action_node
from crawlergraph.actions.models import ActionType

def make_state(page_type: PageType):
    return CrawlState(
        run_id="test",
        current_url="https://example.com",
        page_type=page_type
    )

def test_login_decision():
    state = make_state(PageType.LOGIN)
    updated = decide_action_node(state)

    assert updated.next_action.action == ActionType.SUBMIT

def test_listing_decision():
    state = make_state(PageType.LISTING)
    updated = decide_action_node(state)

    assert updated.next_action.action == ActionType.PAGINATE

def test_error_decision():
    state = make_state(PageType.ERROR)
    updated = decide_action_node(state)

    assert updated.next_action.action == ActionType.STOP

def test_dashboard_decision():
    state = make_state(PageType.DASHBOARD)
    updated = decide_action_node(state)

    assert updated.next_action.action == ActionType.CLICK
