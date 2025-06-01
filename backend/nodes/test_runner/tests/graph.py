from langgraph.graph import StateGraph, START, END
from typing import Dict, Any

from nodes.test_runner.node import test_runner


# Define the state structure
GraphState = Dict[str, Any]

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("TestRunner", test_runner)

    builder.add_edge(START, "TestRunner")
    builder.add_edge("TestRunner", END)

    return builder.compile()
