"""
DOM Feature Extraction

Responsible for converting a raw DOM snapshot (HTML string)
into a deterministic, structured feature vector used by
page classification and action policies.

NO browser logic
NO LangGraph logic
NO LLMs
"""

from bs4 import BeautifulSoup
from typing import List
from crawlergraph.state import PageFeatures

# Public API
def extract_dom_features(dom: str, url: str | None = None) -> PageFeatures:
    """
    Entry point for DOM feature extraction.

    Args:
        dom: Raw HTML string
        url: Optional current URL (used for pattern hints)

    Returns:
        PageFeatures
    """

    soup = BeautifulSoup(dom, "html.parser")

    features = PageFeatures(
        has_form=_has_form(soup),
        has_username_input=_has_username_input(soup),
        has_password_input=_has_password_input(soup),
        input_count=_count_inputs(soup),
        submit_button_count=_count_submit_buttons(soup),
        table_count=_count_tables(soup),
        pagination_controls=_has_pagination_controls(soup),
        error_banners=_has_error_banners(soup),
        empty_state_detected=_has_empty_state(soup),
        content_block_count=_count_content_blocks(soup),
        url_patterns=_extract_url_patterns(url),
    )
    return features

# Feature Detectors
def _has_form(soup: BeautifulSoup) -> bool:
    return soup.find("form") is not None


def _has_username_input(soup: BeautifulSoup) -> bool:
    """
    Heuristic detection of username/email fields.
    """
    candidates = soup.find_all("input", {"type": ["text", "email"]})
    for c in candidates:
        attrs = " ".join([
            c.get("name", ""),
            c.get("id", ""),
            c.get("placeholder", ""),
            c.get("aria-label", "")
        ]).lower()

        if any(k in attrs for k in ["user", "email", "login", "username"]):
            return True
    return False


def _has_password_input(soup: BeautifulSoup) -> bool:
    return soup.find("input", {"type": "password"}) is not None


def _count_inputs(soup: BeautifulSoup) -> int:
    return len(soup.find_all("input"))


def _count_submit_buttons(soup: BeautifulSoup) -> int:
    buttons = soup.find_all("button")
    inputs = soup.find_all("input", {"type": "submit"})
    return len(buttons) + len(inputs)


def _count_tables(soup: BeautifulSoup) -> int:
    return len(soup.find_all("table"))


def _has_pagination_controls(soup: BeautifulSoup) -> bool:
    """
    Detect common pagination patterns.
    """
    pagination_keywords = ["next", "previous", "page", "pagination"]

    # aria-label / role based
    for nav in soup.find_all("nav"):
        label = nav.get("aria-label", "").lower()
        if any(k in label for k in pagination_keywords):
            return True

    # link text based
    for a in soup.find_all("a"):
        text = (a.get_text() or "").lower()
        if text.strip() in {"next", "prev", "previous"}:
            return True

    return False

def _count_content_blocks(soup: BeautifulSoup) -> int:
    """
    Counts high-level content blocks used to detect dashboards
    and rich landing pages.

    We intentionally keep this broad and cheap.
    """
    return len(
        soup.find_all(
            ["section", "article", "main", "aside", "div"],
            recursive=True
        )
    )

def _has_error_banners(soup: BeautifulSoup) -> bool:
    """
    Detect inline error banners / alerts.
    """
    error_keywords = ["error", "failed", "invalid", "unauthorized", "forbidden"]

    for el in soup.find_all(["div", "span", "p"]):
        cls = " ".join(el.get("class", [])).lower()
        text = (el.get_text() or "").lower()

        if any(k in cls for k in error_keywords):
            return True
        if any(k in text for k in error_keywords):
            return True

    return False

def _has_empty_state(soup: BeautifulSoup) -> bool:
    """
    Detect empty states like:
    - No results found
    - Nothing here yet
    """
    empty_phrases = [
        "no results",
        "nothing found",
        "empty",
        "no data",
        "no records"
    ]

    body_text = soup.get_text(separator=" ").lower()
    return any(p in body_text for p in empty_phrases)

def _extract_url_patterns(url: str | None) -> List[str]:
    """
    Extract semantic hints from URL.
    Used as weak signals only.
    """
    if not url:
        return []

    patterns = []
    lowered = url.lower()

    if "login" in lowered:
        patterns.append("login")
    if "auth" in lowered:
        patterns.append("auth")
    if "signin" in lowered:
        patterns.append("signin")
    if "signup" in lowered:
        patterns.append("signup")
    if "page=" in lowered or "offset=" in lowered:
        patterns.append("pagination")
    if any(k in lowered for k in ["error", "403", "404", "500"]):
        patterns.append("error")

    return patterns
