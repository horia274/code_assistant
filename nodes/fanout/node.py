from typing import Dict, Any, Generator

def fanout(state: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    print("Fanout state:")
    print(state)
    print("--------------------------------")

    submissions = state.get("submissions", [])
    tests = state.get("tests", [])
    enabled_nodes = state.get("enabled_nodes", [])

    for submission in submissions:
        yield {
            "id": submission["id"],
            "code": submission["code"],
            "tests": tests,
            "enabled_nodes": enabled_nodes
        }
