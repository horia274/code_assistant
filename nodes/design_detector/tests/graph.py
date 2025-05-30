from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from nodes.design_detector.node import design_detector

GraphState = Dict[str, Any]


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("DesignDetector", design_detector)
    builder.add_edge(START, "DesignDetector")
    builder.add_edge("DesignDetector", END)

    return builder.compile()
