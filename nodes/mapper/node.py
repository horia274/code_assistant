from typing import Dict, Any, Generator

def mapper(state: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    print("Mapper state:")
    print(state)
    print("--------------------------------")

    enabled_nodes = state.get("enabled_nodes", [])
    id = state.get("id", "")
    code = state.get("code", "")
    tests = state.get("tests", [])

    for _ in enabled_nodes:
        yield {
            "id": id,
            "code": code,
            "tests": tests
        }
