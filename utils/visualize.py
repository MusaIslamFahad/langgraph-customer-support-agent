"""
utils/visualize.py — Render a PNG of the LangGraph workflow.

Usage:
    python -m utils.visualize
"""

from IPython.display import display, Image
from langchain_core.runnables.graph import MermaidDrawMethod

from agents import get_app


def show_graph() -> None:
    """Display the graph as a Mermaid PNG (works inside Jupyter)."""
    app = get_app()
    display(
        Image(
            app.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )
        )
    )


def save_graph(path: str = "workflow.png") -> None:
    """Save the graph PNG to disk."""
    app = get_app()
    png_bytes = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    with open(path, "wb") as f:
        f.write(png_bytes)
    print(f"Graph saved to {path}")


if __name__ == "__main__":
    save_graph()
