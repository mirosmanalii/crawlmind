from bs4 import BeautifulSoup
from typing import Dict


def extract_dom_features(dom: str) -> Dict:
    soup = BeautifulSoup(dom, "html.parser")

    inputs = soup.find_all("input")
    forms = soup.find_all("form")
    tables = soup.find_all("table")

    has_username = any(
        i.get("type") in ("text", "email") and "user" in (i.get("name", "") + i.get("id", "")).lower()
        for i in inputs
    )

    has_password = any(
        i.get("type") == "password" for i in inputs
    )

    submit_buttons = soup.find_all("button", {"type": "submit"})

    pagination_controls = bool(
        soup.select(".pagination, [aria-label='pagination'], nav[role='navigation']")
    )

    error_banners = bool(
        soup.select(".error, .alert, [role='alert']")
    )

    return {
        "has_form": len(forms) > 0,
        "has_username_input": has_username,
        "has_password_input": has_password,
        "input_count": len(inputs),
        "submit_button_count": len(submit_buttons),
        "table_count": len(tables),
        "pagination_controls": pagination_controls,
        "error_banners": error_banners,
    }
