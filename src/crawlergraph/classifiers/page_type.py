from crawler_graph.state import PageType


def classify_page_type(features: dict, signals: dict) -> tuple[PageType, float]:
    status_code = signals.get("status_code", 200)

    # Hard stop: HTTP errors
    if status_code >= 400:
        return PageType.ERROR, 0.99

    # Login page
    if features.get("has_password_input") and features.get("has_username_input"):
        return PageType.LOGIN, 0.95

    # Form-heavy pages
    if features.get("has_form") and features.get("input_count", 0) > 3:
        return PageType.FORM, 0.85

    # Listings with pagination
    if features.get("table_count", 0) > 0 and features.get("pagination_controls"):
        return PageType.LISTING, 0.85

    # Empty or broken content
    if features.get("error_banners"):
        return PageType.ERROR, 0.8

    return PageType.UNKNOWN, 0.3
