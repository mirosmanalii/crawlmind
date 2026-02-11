from crawlergraph.nodes.analyze_defects import analyze_defects
from crawlergraph.state import CrawlState
from crawlergraph.features.dom_features import extract_dom_features
from crawlergraph.features.runtime_features import extract_runtime_features


def test_analyze_defects_node_detects_console_error():
    dom = "<html><body></body></html>"

    state = CrawlState(
        run_id="test",
        current_url="https://example.com"
    )

    state.page_features = extract_dom_features(dom)
    state.signals = extract_runtime_features({
        "status_code": 200,
        "console": {"errors": ["Uncaught TypeError"]}
    })

    updated_state = analyze_defects(state)

    assert len(updated_state.detected_defects) == 1
    assert updated_state.detected_defects[0].subtype == "ConsoleError"
