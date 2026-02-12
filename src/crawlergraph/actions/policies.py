"""
Action Policies (v1)

Maps:
    PageType + Defects + State
→   ActionDecision
"""

from crawlergraph.state import CrawlState, PageType
from crawlergraph.actions.models import ActionDecision, ActionType

def decide_action(state: CrawlState) -> ActionDecision:
    """
    Determine next action based on page type and defects.
    """

    # 1. Terminal error conditions
    if state.page_type == PageType.ERROR:
        return ActionDecision(
            action=ActionType.STOP,
            rationale="Terminal error page detected",
            confidence=0.95,
        )

    # 2. Login page
    if state.page_type == PageType.LOGIN:
        return ActionDecision(
            action=ActionType.SUBMIT,
            rationale="Login page detected; submit credentials",
            confidence=0.9,
        )

    # 3. Listing page
    if state.page_type == PageType.LISTING:
        return ActionDecision(
            action=ActionType.PAGINATE,
            rationale="Listing page detected; paginate",
            confidence=0.85,
        )

    # 4. Form page
    if state.page_type == PageType.FORM:
        return ActionDecision(
            action=ActionType.SUBMIT,
            rationale="Form detected; submit form",
            confidence=0.8,
        )

    # 5. Dashboard
    if state.page_type == PageType.DASHBOARD:
        return ActionDecision(
            action=ActionType.CLICK,
            rationale="Dashboard detected; explore content",
            confidence=0.7,
        )

    # 6. Default fallback
    return ActionDecision(
        action=ActionType.STOP,
        rationale="No deterministic action available",
        confidence=0.5,
    )
