import pytest

from crawlergraph.features.dom_features import extract_dom_features
from crawlergraph.features.runtime_features import extract_runtime_features
from crawlergraph.classifiers.page_type import classify_page_type
from crawlergraph.state import PageType

# Helpers
def classify(dom: str, raw_signals: dict, url: str = "https://example.com"):
    features = extract_dom_features(dom, url)
    signals = extract_runtime_features(raw_signals)
    return classify_page_type(features, signals)

# Tests
def test_login_page_classification():
    dom = """
    <html>
      <body>
        <form>
          <input type="text" name="username" />
          <input type="password" name="password" />
          <button type="submit">Login</button>
        </form>
      </body>
    </html>
    """

    page_type, confidence = classify(dom, {"status_code": 200}, url="https://example.com/login")

    assert page_type == PageType.LOGIN
    assert confidence >= 0.9

def test_error_page_500():
    dom = "<html><body><h1>Server Error</h1></body></html>"

    page_type, confidence = classify(dom, {"status_code": 500})

    assert page_type == PageType.ERROR
    assert confidence >= 0.95

def test_spa_runtime_error_page():
    dom = "<html><body><div id='app'></div></body></html>"

    raw_signals = {
        "status_code": 200,
        "console": {
            "errors": ["Uncaught TypeError: cannot read property"]
        }
    }

    page_type, confidence = classify(dom, raw_signals)

    assert page_type == PageType.ERROR
    assert confidence >= 0.75

def test_listing_page_with_pagination():
    dom = """
    <html>
      <body>
        <table>
          <tr><td>Row 1</td></tr>
        </table>
        <nav aria-label="Pagination">
          <a href="?page=2">Next</a>
        </nav>
      </body>
    </html>
    """

    page_type, confidence = classify(dom, {"status_code": 200})

    assert page_type == PageType.LISTING
    assert confidence >= 0.85

def test_detail_page():
    dom = """
    <html>
      <body>
        <table>
          <tr><th>ID</th><td>123</td></tr>
          <tr><th>Name</th><td>Item</td></tr>
        </table>
      </body>
    </html>
    """

    page_type, confidence = classify(dom, {"status_code": 200})

    assert page_type == PageType.DETAIL
    assert confidence >= 0.7

def test_generic_form_page():
    dom = """
    <html>
      <body>
        <form>
          <input type="text" name="first_name" />
          <input type="text" name="last_name" />
          <input type="email" name="email" />
          <button>Submit</button>
        </form>
      </body>
    </html>
    """

    page_type, confidence = classify(dom, {"status_code": 200})

    assert page_type == PageType.FORM
    assert confidence >= 0.75

def test_empty_state_page():
    dom = """
    <html>
      <body>
        <p>No results found</p>
      </body>
    </html>
    """

    page_type, confidence = classify(dom, {"status_code": 200})

    assert page_type == PageType.EMPTY
    assert confidence >= 0.85

def test_dashboard_page_fallback():
    dom = """
    <html>
      <body>
        <div class="card">Widget A</div>
        <div class="card">Widget B</div>
      </body>
    </html>
    """

    page_type, confidence = classify(dom, {"status_code": 200})

    assert page_type == PageType.DASHBOARD
    assert confidence >= 0.5

def test_unknown_page():
    dom = "<html><body><div>Hello world</div></body></html>"

    page_type, confidence = classify(dom, {"status_code": 200})

    assert page_type == PageType.UNKNOWN
    assert confidence <= 0.4
