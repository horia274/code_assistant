from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from nodes.router.node import router

GraphState = Dict[str, Any]

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("Router", router)
    builder.add_edge(START, "Router")
    builder.add_edge("Router", END)

    return builder.compile()
