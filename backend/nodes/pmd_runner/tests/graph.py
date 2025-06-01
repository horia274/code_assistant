from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from nodes.pmd_runner.node import pmd_runner


GraphState = Dict[str, Any]

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("PMDRunner", pmd_runner)
    builder.add_edge(START, "PMDRunner")
    builder.add_edge("PMDRunner", END)

    return builder.compile()
