from pathlib import Path

from crawlergraph.features.dom_features import extract_dom_features
from crawlergraph.features.runtime_features import extract_runtime_features
from crawlergraph.defects.rules import detect_defects
from crawlergraph.defects.models import DefectCategory

FIXTURE_DIR = Path(__file__).parent / "fixtures"

def load_html(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")

# Server 500 simulation
def test_real_world_server_500():
    html = load_html("server_500.html")

    features = extract_dom_features(html)
    signals = extract_runtime_features({"status_code": 500})

    defects = detect_defects(features, signals)

    assert any(d.subtype == "ServerError" for d in defects)

# SPA Console Error
def test_real_world_spa_console_error():
    html = load_html("console_error_spa.html")

    features = extract_dom_features(html)
    signals = extract_runtime_features({
        "status_code": 200,
        "console": {"errors": ["Uncaught TypeError"]},
    })

    defects = detect_defects(features, signals)

    assert any(d.subtype == "ConsoleError" for d in defects)

# Slow Dashboard
def test_real_world_slow_dashboard():
    html = load_html("slow_dashboard.html")

    features = extract_dom_features(html)
    signals = extract_runtime_features({
        "performance": {"page_load_time_ms": 5200}
    })

    defects = detect_defects(features, signals)

    assert any(d.category == DefectCategory.PERFORMANCE for d in defects)

# Broken Network Listing
def test_real_world_network_failure():
    html = load_html("broken_network_listing.html")

    features = extract_dom_features(html)
    signals = extract_runtime_features({
        "network": {"failed_requests": 3}
    })

    defects = detect_defects(features, signals)

    assert any(d.subtype == "NetworkFailure" for d in defects)
