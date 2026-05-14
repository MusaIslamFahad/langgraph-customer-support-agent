"""
agents/nodes.py — Individual node functions that make up the support workflow.

Each function receives the current State and returns a partial State update.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from agents.state import State
from config import MODEL_NAME, TEMPERATURE

# ── Shared LLM instance ────────────────────────────────────────────────────────
_llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)


def _invoke(template: str, **kwargs) -> str:
    """Helper: build a prompt, run it through the LLM, return the text."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | _llm
    return chain.invoke(kwargs).content


# ── Classification nodes ───────────────────────────────────────────────────────

def categorize(state: State) -> State:
    """Classify the query as Technical, Billing, or General."""
    category = _invoke(
        "Categorize the following customer query into exactly one of these "
        "categories: Technical, Billing, General. "
        "Respond with the category name only.\n\nQuery: {query}",
        query=state["query"],
    )
    return {"category": category.strip()}


def analyze_sentiment(state: State) -> State:
    """Classify the query sentiment as Positive, Neutral, or Negative."""
    sentiment = _invoke(
        "Analyze the sentiment of the following customer query. "
        "Respond with exactly one word: Positive, Neutral, or Negative.\n\nQuery: {query}",
        query=state["query"],
    )
    return {"sentiment": sentiment.strip()}


# ── Response nodes ─────────────────────────────────────────────────────────────

def handle_technical(state: State) -> State:
    """Generate a technical support response."""
    response = _invoke(
        "You are a technical support specialist. "
        "Provide a clear and helpful response to the following query.\n\nQuery: {query}",
        query=state["query"],
    )
    return {"response": response}


def handle_billing(state: State) -> State:
    """Generate a billing support response."""
    response = _invoke(
        "You are a billing support specialist. "
        "Provide a clear and helpful response to the following query.\n\nQuery: {query}",
        query=state["query"],
    )
    return {"response": response}


def handle_general(state: State) -> State:
    """Generate a general support response."""
    response = _invoke(
        "You are a friendly customer support agent. "
        "Provide a clear and helpful response to the following query.\n\nQuery: {query}",
        query=state["query"],
    )
    return {"response": response}


def escalate(state: State) -> State:
    """Flag the query for human escalation (negative sentiment detected)."""
    return {
        "response": (
            "We're sorry to hear you're having a frustrating experience. "
            "Your query has been escalated to a human support agent who will "
            "reach out to you shortly."
        )
    }


# ── Routing logic ──────────────────────────────────────────────────────────────

def route_query(state: State) -> str:
    """
    Conditional edge: decide which handler node to visit next.

    Routing priority:
      1. Negative sentiment → escalate (regardless of category)
      2. Technical category → handle_technical
      3. Billing category  → handle_billing
      4. Everything else   → handle_general
    """
    if state["sentiment"] == "Negative":
        return "escalate"
    elif state["category"] == "Technical":
        return "handle_technical"
    elif state["category"] == "Billing":
        return "handle_billing"
    else:
        return "handle_general"
