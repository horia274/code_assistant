from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from nodes.test_generator.node import test_generator


GraphState = Dict[str, Any]

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("TestGenerator", test_generator)
    builder.add_edge(START, "TestGenerator")
    builder.add_edge("TestGenerator", END)

    return builder.compile()
