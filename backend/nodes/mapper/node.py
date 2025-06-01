from typing import Dict, Any, Generator

def mapper(state: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    enabled_nodes = state.get("enabled_nodes", [])

    for _ in enabled_nodes:
        yield {
            **state
        }
