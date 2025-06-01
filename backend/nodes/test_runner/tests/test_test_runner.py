import json

from nodes.test_runner.tests.graph import build_graph


graph = build_graph()

sample_code = """
import java.util.Scanner;

public class HelloWorld {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String name = sc.nextLine();
        System.out.println("Hello, " + name + "!");
    }
}
"""

tests = [
    {
        "input": "Alice\n",
        "expected_output": "Hello, Alice!"
    },
    {
        "input": "Bob\n",
        "expected_output": "Hello, Bob!"
    }
]

initial_state = {
    "code": sample_code,
    "tests": tests
}

# Run the graph
result = graph.invoke(initial_state)
test_results = result["test_results"]
print(json.dumps(test_results, indent=2))

# Assertions
assert test_results["passed"] == 2, "Expected both test cases to pass"
assert test_results["failed"] == 0, "No test cases should fail"

for detail in test_results["details"]:
    assert detail["status"] == "passed", f"Test failed: {detail}"
