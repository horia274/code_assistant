import json

from graph.builder import build_graph


def main():
    file_path = "examples/example1.json"
    with open(file_path, 'r') as file:
        input_data = json.load(file)

    # Build and run the graph
    graph = build_graph()
    result = graph.invoke(input_data)

    # Display the aggregated results
    print("Final aggregated results:")
    print(result)


if __name__ == "__main__":
    main()
