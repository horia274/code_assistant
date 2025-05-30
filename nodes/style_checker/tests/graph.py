from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from nodes.style_checker.node import style_checker

GraphState = Dict[str, Any]


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("StyleChecker", style_checker)
    builder.add_edge(START, "StyleChecker")
    builder.add_edge("StyleChecker", END)

    return builder.compile()
