import json
import os

from nodes.pmd_runner.tests.graph import build_graph


graph = build_graph()

path = "nodes/pmd_runner/tests/sample_code.java"
with open(path, "r") as f:
    code = f.read()

state = {"code": code}
result = graph.invoke(state)

assert "pmd_results" in result
pmd = result["pmd_results"]
print(json.dumps(pmd, indent=2))

assert isinstance(pmd["violations"], list)
