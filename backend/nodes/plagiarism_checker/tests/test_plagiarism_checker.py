import os
import glob

from nodes.plagiarism_checker.tests.graph import build_graph

graph = build_graph()

# Read all test sources from folder
base_path = "nodes/plagiarism_checker/tests/test_sources"
java_files = glob.glob(os.path.join(base_path, "*.java"))

sources = []
for filepath in java_files:
    with open(filepath, "r") as f:
        code = f.read()
        student_id = os.path.splitext(os.path.basename(filepath))[0]
        sources.append({"id": student_id, "code": code})

result = graph.invoke({"sources": sources})
report = result.get("plagiarism_report", {})

print(report)

assert "similarities" in report
assert isinstance(report["similarities"], dict)
assert len(report["similarities"]) >= 1

for pair, score in report["similarities"].items():
    print(f"{pair}: {score}%")

assert report["error"] is None
