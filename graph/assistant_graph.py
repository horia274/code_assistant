from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint import MemorySaver
from typing import Dict

# Import nodes
from nodes.test_runner import test_runner
from nodes.pmd_runner import pmd_runner
from nodes.design_detector import design_detector
from nodes.style_checker import style_checker
from nodes.ai_detector import ai_detector
from nodes.router import router
from nodes.aggregator import aggregator

# Define type for graph state
GraphState = Dict[str, any]

def build_graph():
    # Create graph builder
    builder = StateGraph(GraphState)
    builder.set_checkpoint(MemorySaver())  # Optional memory

    # Add nodes
    builder.add_node("Router", router)

    builder.add_node("TestRunner", test_runner)
    builder.add_node("PMDRunner", pmd_runner)
    builder.add_node("DesignDetector", design_detector)
    builder.add_node("StyleChecker", style_checker)
    builder.add_node("AIDetector", ai_detector)

    builder.add_node("Aggregator", aggregator)

    # Edges (define flow)
    builder.add_edge(START, "Router")
    builder.add_edge("Router", "TestRunner")
    builder.add_edge("Router", "PMDRunner")
    builder.add_edge("Router", "DesignDetector")
    builder.add_edge("Router", "StyleChecker")
    builder.add_edge("Router", "AIDetector")

    # All nodes return to Aggregator
    builder.add_edge("TestRunner", "Aggregator")
    builder.add_edge("PMDRunner", "Aggregator")
    builder.add_edge("DesignDetector", "Aggregator")
    builder.add_edge("StyleChecker", "Aggregator")
    builder.add_edge("AIDetector", "Aggregator")
    builder.add_edge("Aggregator", END)

    return builder.compile()
