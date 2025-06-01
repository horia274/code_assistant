from graph.builder import build_graph


def analyze(input_data):
    # Build and run the graph
    graph = build_graph()
    result = graph.invoke(input_data)
    return {
        "score": result["score"],
        "feedback": result["feedback"],
        "results": result["aggregated_results"]
    }
