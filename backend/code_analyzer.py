from pathlib import Path

from graph.builder import build_graph

_BACKEND_DIR = Path(__file__).resolve().parent


def analyze(input_data):
    # Build and run the graph
    graph = build_graph()
    png_graph = graph.get_graph().draw_mermaid_png()

    graph_png = _BACKEND_DIR / "graph.png"
    with open(graph_png, "wb") as f:
        f.write(png_graph)

    result = graph.invoke(input_data)
    return {
        "score": result["score"],
        "feedback": result["feedback"],
        "results": result["aggregated_results"]
    }
