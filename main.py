from graph.builder import build_graph
from utils.code_utils import load_input

def main():
    input_data = load_input("examples/example1.json")

    # Build and run the graph
    graph = build_graph()

    # Save the graph diagram to a file
    png_graph = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_graph)

    result = graph.invoke(input_data)

    # Display the aggregated results
    print("Final aggregated results:")
    print(result)


if __name__ == "__main__":
    main()
