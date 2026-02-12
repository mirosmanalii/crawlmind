"""
LangGraph Assembly (v1)
"""

from langgraph.graph import StateGraph, END

from crawlergraph.state import CrawlState
from crawlergraph.nodes.classify_page import classify_page_node
from crawlergraph.nodes.analyze_defects import analyze_defects
from crawlergraph.nodes.decide_action import decide_action_node
from crawlergraph.memory.update_memory import update_memory
from crawlergraph.nodes.loop_guard import loop_guard_node
from crawlergraph.nodes.evaluate_stop import evaluate_stop_node


def build_graph():
    builder = StateGraph(CrawlState)

    # Add nodes
    builder.add_node("classify", classify_page_node)
    builder.add_node("analyze_defects", analyze_defects)
    builder.add_node("decide_action", decide_action_node)
    builder.add_node("update_memory", update_memory)
    builder.add_node("loop_guard", loop_guard_node)
    builder.add_node("evaluate_stop", evaluate_stop_node)

    # Define execution flow
    builder.set_entry_point("classify")

    builder.add_edge("classify", "analyze_defects")
    builder.add_edge("analyze_defects", "decide_action")
    builder.add_edge("decide_action", "update_memory")
    builder.add_edge("update_memory", "loop_guard")
    builder.add_edge("loop_guard", "evaluate_stop")

    # Conditional routing
    builder.add_conditional_edges(
        "evaluate_stop",
        evaluate_stop_node,
        {
            "stop": END,
            "continue": "classify"
        },
    )

    return builder.compile()
