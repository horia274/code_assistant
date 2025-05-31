from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from nodes.plagiarism_checker.node import plagiarism_checker

GraphState = Dict[str, Any]


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("PlagiarismChecker", plagiarism_checker)
    builder.add_edge(START, "PlagiarismChecker")
    builder.add_edge("PlagiarismChecker", END)

    return builder.compile()
