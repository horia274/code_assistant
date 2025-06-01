from langgraph.graph import StateGraph, START, END
from typing import Dict, Any, TypedDict, Annotated, operator

# Import nodes
from nodes.router.node import router
from nodes.test_generator.node import test_generator
from nodes.mapper.node import mapper

from nodes.test_runner.node import test_runner
from nodes.design_detector.node import design_detector
from nodes.pmd_runner.node import pmd_runner
from nodes.style_checker.node import style_checker
from nodes.ai_detector.node import ai_detector

from nodes.aggregator.node import aggregator
from nodes.plagiarism_checker.node import plagiarism_checker

class Test(TypedDict):
    id: int
    input: str
    expected_output: str

# Define state
class GraphState(TypedDict, total=False):
    id: str
    code: str
    tests: list[Test]
    intent: str
    generate_tests: bool
    num_tests: int
    enabled_nodes: list[str]
    nodes_results: Annotated[list[dict], operator.add]


def build_per_submission_graph():
    builder = StateGraph(GraphState)

    builder.add_node("Mapper", mapper)

    builder.add_node("TestRunner", test_runner)
    builder.add_node("DesignDetector", design_detector)
    builder.add_node("PMDRunner", pmd_runner)
    builder.add_node("StyleChecker", style_checker)
    builder.add_node("AIDetector", ai_detector)

    builder.add_node("Aggregator", aggregator)

    builder.add_edge(START, "Mapper")

    def per_submission_nodes(state: GraphState):
        return [n for n in state.get("enabled_nodes", []) if n != "PlagiarismChecker"]

    builder.add_conditional_edges("Mapper", per_submission_nodes, {
        "TestRunner": "TestRunner",
        "DesignDetector": "DesignDetector",
        "PMDRunner": "PMDRunner",
        "StyleChecker": "StyleChecker",
        "AIDetector": "AIDetector"
    })

    builder.add_edge("TestRunner", "Aggregator")
    builder.add_edge("DesignDetector", "Aggregator")
    builder.add_edge("PMDRunner", "Aggregator")
    builder.add_edge("StyleChecker", "Aggregator")
    builder.add_edge("AIDetector", "Aggregator")

    builder.add_edge("Aggregator", END)

    return builder.compile()
