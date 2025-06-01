from nodes.router.tests.graph import build_graph

graph = build_graph()

result = graph.invoke({
    "code": "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }",
    "tests": None,
    "intent": "run tests and detect design patterns"
})

print(result)
