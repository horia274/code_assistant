from nodes.test_generator.tests.graph import build_graph


graph = build_graph()

with open("nodes/test_generator/tests/sample_code.java", "r") as f:
    code = f.read()

result = graph.invoke({"code": code, "num_tests": 3})

print(result)

assert "tests" in result
assert isinstance(result["tests"], list)
assert len(result["tests"]) == 3

for test in result["tests"]:
    assert "input" in test
    assert "expected_output" in test
