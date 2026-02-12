"""
LangGraph Node: decide_action
"""

from crawlergraph.state import CrawlState
from crawlergraph.actions.policies import decide_action


def decide_action_node(state: CrawlState) -> CrawlState:
    decision = decide_action(state)
    state.next_action = decision
    return state
