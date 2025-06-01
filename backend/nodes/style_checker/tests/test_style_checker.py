import json

from nodes.style_checker.tests.graph import build_graph


graph = build_graph()

code = """
public class Main {
public static void main(String[] args) {
System.out.println("Hello");
}
}
"""

result = graph.invoke({"code": code})

assert "style_results" in result
res = result["style_results"]
print(json.dumps(res, indent=2))

if res["error"]:
    print("Checkstyle error:", res["error"])

assert res["error"] is None
assert isinstance(res["violations"], list)
assert len(res["violations"]) > 0
