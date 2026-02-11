from crawlergraph.defects.rules import detect_defects
from crawlergraph.features.runtime_features import extract_runtime_features
from crawlergraph.features.dom_features import extract_dom_features
from crawlergraph.defects.models import DefectCategory


def test_server_error_defect():
    dom = "<html><body>Error</body></html>"
    features = extract_dom_features(dom)
    signals = extract_runtime_features({"status_code": 500})

    defects = detect_defects(features, signals)

    assert len(defects) == 1
    assert defects[0].category == DefectCategory.FUNCTIONAL
    assert defects[0].subtype == "ServerError"


def test_console_error_defect():
    dom = "<html><body></body></html>"
    features = extract_dom_features(dom)
    signals = extract_runtime_features(
        {
            "status_code": 200,
            "console": {"errors": ["Uncaught TypeError"]},
        }
    )

    defects = detect_defects(features, signals)

    assert any(d.subtype == "ConsoleError" for d in defects)


def test_layout_overlap_ui_defect():
    dom = "<html><body></body></html>"
    features = extract_dom_features(dom)
    signals = extract_runtime_features(
        {
            "layout": {"overlaps": True},
        }
    )

    defects = detect_defects(features, signals)

    assert len(defects) == 1
    assert defects[0].category == DefectCategory.UI


def test_slow_page_performance_defect():
    dom = "<html><body></body></html>"
    features = extract_dom_features(dom)
    signals = extract_runtime_features(
        {
            "performance": {"page_load_time_ms": 4500},
        }
    )

    defects = detect_defects(features, signals)

    assert defects[0].category == DefectCategory.PERFORMANCE
    assert defects[0].subtype == "SlowPageLoad"
