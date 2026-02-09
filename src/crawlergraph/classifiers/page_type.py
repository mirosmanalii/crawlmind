"""
Page Type Classification (v1)

Deterministic, rule-based page-type classifier.
Consumes PageFeatures + RuntimeSignals and outputs
(PageType, confidence).

LLM fallback is intentionally NOT used here.
"""

from typing import Tuple
from crawlergraph.state import PageType, PageFeatures, RuntimeSignals

# Public API
def classify_page_type(
    features: PageFeatures,
    signals: RuntimeSignals
) -> Tuple[PageType, float]:
    """
    Classify the current page into a PageType.

    Returns:
        (PageType, confidence)
    """

    # 1. Terminal / error conditions (highest priority)
    page_type, confidence = _classify_error_page(signals)
    if page_type:
        return page_type, confidence

    # 2. Authentication-related pages
    page_type, confidence = _classify_login_page(features, signals)
    if page_type:
        return page_type, confidence

    page_type, confidence = _classify_auth_challenge(features, signals)
    if page_type:
        return page_type, confidence

    # 3. Empty / no-content states
    page_type, confidence = _classify_empty_page(features)
    if page_type:
        return page_type, confidence

    # 4. Data-heavy application pages
    page_type, confidence = _classify_listing_page(features)
    if page_type:
        return page_type, confidence

    page_type, confidence = _classify_detail_page(features)
    if page_type:
        return page_type, confidence

    # 5. Generic forms
    page_type, confidence = _classify_form_page(features)
    if page_type:
        return page_type, confidence

    # 6. Pagination (usually overlays listing)
    page_type, confidence = _classify_pagination_page(features)
    if page_type:
        return page_type, confidence

    # 7. Dashboard / landing pages
    page_type, confidence = _classify_dashboard_page(features)
    if page_type:
        return page_type, confidence

    # Fallback
    return PageType.UNKNOWN, 0.3

# Classifier Rules
def _classify_error_page(
    signals: RuntimeSignals
) -> Tuple[PageType | None, float]:
    """
    HTTP or runtime-level error pages.
    """
    if signals.status_code >= 500:
        return PageType.ERROR, 0.99

    if 400 <= signals.status_code < 500:
        return PageType.ERROR, 0.95

    if signals.console_errors and signals.status_code == 200:
        # SPA runtime crash
        return PageType.ERROR, 0.8

    return None, 0.0

def _classify_login_page(
    features: PageFeatures,
    signals: RuntimeSignals
) -> Tuple[PageType | None, float]:
    """
    Username + password inputs strongly imply login.
    """
    if (
        features.has_password_input
        and features.has_username_input
        and features.submit_button_count > 0
    ):
        return PageType.LOGIN, 0.95

    # URL hint fallback
    if "login" in features.url_patterns or "signin" in features.url_patterns:
        return PageType.LOGIN, 0.85

    return None, 0.0

def _classify_auth_challenge(
    features: PageFeatures,
    signals: RuntimeSignals
) -> Tuple[PageType | None, float]:
    """
    MFA / OTP / SSO handoff pages.
    """
    auth_keywords = {"otp", "verify", "challenge", "two-factor"}

    if any(k in features.url_patterns for k in auth_keywords):
        return PageType.AUTH_CHALLENGE, 0.8

    if (
        features.has_form
        and features.input_count <= 2
        and not features.has_password_input
        and signals.redirect_detected
    ):
        return PageType.AUTH_CHALLENGE, 0.75

    return None, 0.0

def _classify_empty_page(
    features: PageFeatures
) -> Tuple[PageType | None, float]:
    if features.empty_state_detected:
        return PageType.EMPTY, 0.9
    return None, 0.0

def _classify_listing_page(
    features: PageFeatures
) -> Tuple[PageType | None, float]:
    """
    Tables + pagination usually mean listings.
    """
    if features.table_count > 0 and features.pagination_controls:
        return PageType.LISTING, 0.9

    if features.table_count > 1:
        return PageType.LISTING, 0.8

    return None, 0.0

def _classify_detail_page(
    features: PageFeatures
) -> Tuple[PageType | None, float]:
    """
    Single-record views.
    """
    if (
        features.table_count == 1
        and not features.pagination_controls
        and not features.has_form
    ):
        return PageType.DETAIL, 0.75

    return None, 0.0

def _classify_form_page(
    features: PageFeatures
) -> Tuple[PageType | None, float]:
    """
    Generic data entry forms (non-auth).
    """
    if (
        features.has_form
        and features.input_count >= 3
        and not features.has_password_input
    ):
        return PageType.FORM, 0.8

    return None, 0.0

def _classify_pagination_page(
    features: PageFeatures
) -> Tuple[PageType | None, float]:
    """
    Explicit pagination pages (rare but possible).
    """
    if features.pagination_controls and features.table_count == 0:
        return PageType.PAGINATION, 0.7

    return None, 0.0

def _classify_dashboard_page(
    features: PageFeatures
) -> Tuple[PageType | None, float]:
    """
    Landing pages with multiple widgets/cards.
    """
    if (
        not features.has_form
        and not features.pagination_controls
        and features.table_count == 0
        and not features.empty_state_detected
    ):
        return PageType.DASHBOARD, 0.6

    return None, 0.0
