from crawler_graph.classifiers.page_type import classify_page_type
from crawler_graph.state import PageType


def test_login_page_classification():
    features = {
        "has_form": True,
        "has_username_input": True,
        "has_password_input": True,
        "input_count": 2,
        "table_count": 0,
        "pagination_controls": False,
        "error_banners": False,
    }

    signals = {"status_code": 200}

    page_type, confidence = classify_page_type(features, signals)

    assert page_type == PageType.LOGIN
    assert confidence > 0.9
