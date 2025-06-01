from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from nodes.ai_detector.node import ai_detector

GraphState = Dict[str, Any]


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("AIDetector", ai_detector)
    builder.add_edge(START, "AIDetector")
    builder.add_edge("AIDetector", END)

    return builder.compile()
