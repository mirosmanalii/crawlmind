import pytest

from crawlergraph.features.dom_features import extract_dom_features
from crawlergraph.features.runtime_features import extract_runtime_features
from crawlergraph.classifiers.page_type import classify_page_type
from crawlergraph.state import PageType
from .utils import load_fixture

from crawlergraph.defects.rules import detect_defects

def classify(dom: str, url: str):
    features = extract_dom_features(dom, url)
    signals = extract_runtime_features({"status_code": 200})
    return classify_page_type(features, signals)

# GitHub Login
def test_github_login_real_world():
    dom = load_fixture("github_login.html")
    page_type, confidence = classify(dom, "https://github.com/login")

    assert page_type == PageType.LOGIN
    assert confidence >= 0.8

# Wikipedia Homepage
def test_wikipedia_home_real_world():
    dom = load_fixture("wikipedia_home.html")
    page_type, confidence = classify(dom, "https://www.wikipedia.org")

    # Depending on rule strictness, this may be DASHBOARD or UNKNOWN.
    assert page_type in {PageType.DASHBOARD, PageType.UNKNOWN}
    assert confidence >= 0.3

# Python.org Homepage
def test_python_org_home_real_world():
    dom = load_fixture("python_org.html")
    page_type, confidence = classify(dom, "https://www.python.org")

    assert page_type in {PageType.DASHBOARD, PageType.UNKNOWN}
    assert confidence >= 0.3

def test_real_world_sites_have_no_false_server_error():
    dom = load_fixture("wikipedia_home.html")
    features = extract_dom_features(dom, "https://www.wikipedia.org")
    signals = extract_runtime_features({"status_code": 200})

    defects = detect_defects(features, signals)

    # Should not incorrectly detect HTTP errors
    assert not any(d.subtype in {"ServerError", "ClientError"} for d in defects)