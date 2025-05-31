from langgraph.graph import StateGraph, START, END
from typing import Dict, Any, TypedDict, Annotated

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

class Submission(TypedDict):
    id: str
    code: str

class Test(TypedDict):
    input: str
    expected_output: str

# Define state
class GraphState(TypedDict, total=False):
    id: str
    code: str
    tests: list[Test]
    enabled_nodes: list[str]
    results: dict
    submissions: list[Submission]
    intent: str
    generate_tests: bool
    plagiarism: Any
    mode: str


def build_graph():
    builder = StateGraph(GraphState)

    # --- Step 1: Core node registration ---
    builder.add_node("Router", router)
    builder.add_node("TestGenerator", test_generator)
    builder.add_node("Mapper", mapper)

    builder.add_node("TestRunner", test_runner)
    builder.add_node("DesignDetector", design_detector)
    builder.add_node("PMDRunner", pmd_runner)
    builder.add_node("StyleChecker", style_checker)
    builder.add_node("AIDetector", ai_detector)

    builder.add_node("Aggregator", aggregator)
    builder.add_node("PlagiarismChecker", plagiarism_checker)

    # --- Step 2: Start flow ---
    builder.add_edge(START, "Router")

    # --- Step 3: Route to optional test generator ---
    def needs_test_generation(state: GraphState):
        return "TestGenerator" if state.get("generate_tests", False) else "Mapper"

    builder.add_conditional_edges("Router", needs_test_generation, {
        "TestGenerator": "TestGenerator",
        "Mapper": "Mapper"
    })

    builder.add_edge("TestGenerator", "Mapper")

    # --- Step 4: Fan out to analysis nodes per submission ---
    def per_submission_nodes(state: GraphState):
        return [n for n in state.get("enabled_nodes", []) if n != "PlagiarismChecker"]

    builder.add_conditional_edges("Mapper", per_submission_nodes, {
        "TestRunner": "TestRunner",
        "DesignDetector": "DesignDetector",
        "PMDRunner": "PMDRunner",
        "StyleChecker": "StyleChecker",
        "AIDetector": "AIDetector"
    })

    # --- Step 5: Connect each analysis node to Aggregator ---
    builder.add_edge("TestRunner", "Aggregator")
    builder.add_edge("DesignDetector", "Aggregator")
    builder.add_edge("PMDRunner", "Aggregator")
    builder.add_edge("StyleChecker", "Aggregator")
    builder.add_edge("AIDetector", "Aggregator")

    # --- Step 6: Aggregator to optional plagiarism check ---
    def maybe_run_plagiarism(state: GraphState):
        return "PlagiarismChecker" if (
            "PlagiarismChecker" in state.get("enabled_nodes", []) and state.get("mode") == "batch"
        ) else None

    builder.add_conditional_edges("Aggregator", maybe_run_plagiarism, {
        "PlagiarismChecker": "PlagiarismChecker"
    })

    # --- Step 7: Final link to END ---
    builder.add_edge("PlagiarismChecker", END)
    builder.add_edge("Aggregator", END)  # fallback if plagiarism is not enabled

    return builder.compile()
