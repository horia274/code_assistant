from typing import Dict, Any

def reducer(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Reducer state:")
    print(state)
    print("--------------------------------")

    return state
