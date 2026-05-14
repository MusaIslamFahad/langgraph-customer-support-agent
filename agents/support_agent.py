"""
agents/support_agent.py — Assembles the LangGraph and exposes run_customer_support().
"""

from typing import Dict

from langgraph.graph import StateGraph, END

from agents.state import State
from agents.nodes import (
    categorize,
    analyze_sentiment,
    handle_technical,
    handle_billing,
    handle_general,
    escalate,
    route_query,
)


# ── Build the graph ────────────────────────────────────────────────────────────

def _build_graph() -> StateGraph:
    workflow = StateGraph(State)

    # Register nodes
    workflow.add_node("categorize", categorize)
    workflow.add_node("analyze_sentiment", analyze_sentiment)
    workflow.add_node("handle_technical", handle_technical)
    workflow.add_node("handle_billing", handle_billing)
    workflow.add_node("handle_general", handle_general)
    workflow.add_node("escalate", escalate)

    # Linear edge: categorize → analyze_sentiment
    workflow.add_edge("categorize", "analyze_sentiment")

    # Conditional branching after sentiment analysis
    workflow.add_conditional_edges(
        "analyze_sentiment",
        route_query,
        {
            "handle_technical": "handle_technical",
            "handle_billing":   "handle_billing",
            "handle_general":   "handle_general",
            "escalate":         "escalate",
        },
    )

    # All handler nodes lead to END
    for node in ("handle_technical", "handle_billing", "handle_general", "escalate"):
        workflow.add_edge(node, END)

    workflow.set_entry_point("categorize")
    return workflow


# Compile once at import time
_app = _build_graph().compile()


# ── Public API ─────────────────────────────────────────────────────────────────

def run_customer_support(query: str) -> Dict[str, str]:
    """
    Process a customer query through the full support workflow.

    Args:
        query: The raw text of the customer's message.

    Returns:
        A dict with keys: 'category', 'sentiment', 'response'.
    """
    result = _app.invoke({"query": query})
    return {
        "category":  result["category"],
        "sentiment": result["sentiment"],
        "response":  result["response"],
    }


def get_app():
    """Return the compiled LangGraph app (useful for visualisation)."""
    return _app
