from langgraph.graph import StateGraph, START, END
from typing import Dict, Any, TypedDict, Annotated, operator

# Import nodes
from nodes.router.node import router
from nodes.test_generator.node import test_generator
from nodes.fanout.node import fanout
from graph.singular_builder import build_per_submission_graph
from nodes.reducer.node import reducer
from nodes.plagiarism_checker.node import plagiarism_checker

class Submission(TypedDict):
    id: str
    code: str

class Test(TypedDict):
    id: int
    input: str
    expected_output: str

# Define state
class GraphState(TypedDict, total=False):
    submissions: list[Submission]
    tests: list[Test]
    intent: str
    generate_tests: bool
    num_tests: int
    enabled_nodes: list[str]
    submissions_results: Annotated[list[dict], operator.add]


def build_batch_graph():
    builder = StateGraph(GraphState)

    single_submission_runner = build_per_submission_graph()

    builder.add_node("Router", router)
    builder.add_node("TestGenerator", test_generator)
    builder.add_node("Fanout", fanout)
    builder.add_node("RunSubmission", single_submission_runner)
    builder.add_node("Reducer", reducer)
    builder.add_node("PlagiarismChecker", plagiarism_checker)

    builder.add_edge(START, "Router")

    def needs_test_generation(state: GraphState):
        return "TestGenerator" if state.get("generate_tests", False) else "Fanout"

    builder.add_conditional_edges("Router", needs_test_generation, {
        "TestGenerator": "TestGenerator",
        "Fanout": "Fanout"
    })

    builder.add_edge("TestGenerator", "Fanout")
    builder.add_edge("Fanout", "RunSubmission")
    builder.add_edge("RunSubmission", "Reducer")
    
    def needs_plagiarism_checker(state: GraphState):
        return "PlagiarismChecker" if "PlagiarismChecker" in state.get("enabled_nodes", []) else END

    builder.add_conditional_edges("Reducer", needs_plagiarism_checker, {
        "PlagiarismChecker": "PlagiarismChecker",
        END: END
    })

    builder.add_edge("PlagiarismChecker", END)

    return builder.compile()
