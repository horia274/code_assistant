import json

from graph.batch_builder import build_batch_graph


def main():
    file_path = "examples/batch/example.json"
    with open(file_path, 'r') as file:
        input_data = json.load(file)

    # Build and run the graph
    graph = build_batch_graph()
    result = graph.invoke(input_data)

    # Display the aggregated results
    print("Final aggregated results:")
    print(result)


if __name__ == "__main__":
    main()
