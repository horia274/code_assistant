from typing import Dict, Any, Generator

def mapper(state: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    submissions = state.get("submissions", [])
    enabled_nodes = state.get("enabled_nodes", [])
    tests = state.get("tests", "")
    mode = state.get("mode", "batch")

    if mode == "single":
        submission = submissions[0] if submissions else {}
        yield {
            "id": submission.get("id", "unknown"),
            "code": submission.get("code", ""),
            "tests": tests,
            "enabled_nodes": enabled_nodes,
            "results": {}
        }
    else:
        for submission in submissions:
            yield {
                "id": submission.get("id", "unknown"),
                "code": submission.get("code", ""),
                "tests": tests,
                "enabled_nodes": enabled_nodes,
                "results": {}
            }
