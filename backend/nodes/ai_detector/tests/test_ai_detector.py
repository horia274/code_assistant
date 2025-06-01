from nodes.ai_detector.tests.graph import build_graph


graph = build_graph()

with open("nodes/ai_detector/tests/sample_code.java", "r") as f:
    code = f.read()

result = graph.invoke({"code": code})
results = result["ai_results"]

print("--------------------------------")
print("Error:")
print(results["error"])
print("--------------------------------")
print("AI Analysis:")
print(results["ai_generated_analysis"])
