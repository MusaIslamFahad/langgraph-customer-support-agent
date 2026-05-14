"""
agents/state.py — Defines the shared state passed between graph nodes.
"""

from typing import TypedDict


class State(TypedDict):
    """Holds all data for a single customer support interaction."""

    query: str       # The raw customer query
    category: str    # 'Technical' | 'Billing' | 'General'
    sentiment: str   # 'Positive' | 'Neutral' | 'Negative'
    response: str    # Final response sent to the customer
