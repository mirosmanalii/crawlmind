from crawlergraph.graph import build_graph
from crawlergraph.state import CrawlState


def test_graph_builds_and_runs():
    graph = build_graph()

    state = CrawlState(
        run_id="test",
        current_url="https://example.com"
    )

    result = graph.invoke(state)

    assert result is not None
