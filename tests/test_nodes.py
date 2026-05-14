"""
tests/test_nodes.py — Unit tests for individual node functions.

Run with:  pytest tests/
"""

import pytest
from unittest.mock import patch, MagicMock

# ── Helpers ────────────────────────────────────────────────────────────────────

def _mock_llm_response(content: str):
    """Return a mock LLM response with the given content string."""
    mock = MagicMock()
    mock.content = content
    return mock


# ── Tests for routing logic ────────────────────────────────────────────────────

from agents.nodes import route_query


class TestRouteQuery:
    def test_negative_sentiment_escalates(self):
        state = {"query": "q", "category": "Technical", "sentiment": "Negative", "response": ""}
        assert route_query(state) == "escalate"

    def test_technical_category(self):
        state = {"query": "q", "category": "Technical", "sentiment": "Neutral", "response": ""}
        assert route_query(state) == "handle_technical"

    def test_billing_category(self):
        state = {"query": "q", "category": "Billing", "sentiment": "Positive", "response": ""}
        assert route_query(state) == "handle_billing"

    def test_general_fallback(self):
        state = {"query": "q", "category": "General", "sentiment": "Positive", "response": ""}
        assert route_query(state) == "handle_general"

    def test_negative_overrides_billing(self):
        """Negative sentiment should escalate even if category is Billing."""
        state = {"query": "q", "category": "Billing", "sentiment": "Negative", "response": ""}
        assert route_query(state) == "escalate"


# ── Tests for escalate node ────────────────────────────────────────────────────

from agents.nodes import escalate


class TestEscalate:
    def test_returns_response_key(self):
        state = {"query": "q", "category": "Technical", "sentiment": "Negative", "response": ""}
        result = escalate(state)
        assert "response" in result
        assert len(result["response"]) > 0


# ── Integration smoke test (mocked LLM) ───────────────────────────────────────

class TestRunCustomerSupport:
    @patch("agents.nodes._llm")
    def test_full_pipeline_technical(self, mock_llm):
        """Smoke-test the full graph with mocked LLM calls."""
        mock_llm.invoke = MagicMock(
            side_effect=[
                _mock_llm_response("Technical"),   # categorize
                _mock_llm_response("Neutral"),      # analyze_sentiment
                _mock_llm_response("Here is how to fix it."),  # handle_technical
            ]
        )
        # Re-import after patching
        from agents.support_agent import run_customer_support
        result = run_customer_support("My Wi-Fi keeps dropping.")
        assert set(result.keys()) == {"category", "sentiment", "response"}
