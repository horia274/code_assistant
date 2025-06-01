from nodes.design_detector.tests.graph import build_graph


graph = build_graph()

with open("nodes/design_detector/tests/Main.java", "r") as f:
    code = f.read()

result = graph.invoke({"code": code})
results = result["design_results"]

print("--------------------------------")
print("Error:")
print(results["error"])
print("--------------------------------")
print("Patterns:")
print(results["design_patterns"])
