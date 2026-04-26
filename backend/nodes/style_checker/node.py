import os
import subprocess
import tempfile
from typing import Dict, Any

from settings import checkstyle_config_path


def style_checker(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    results = {
        "violations": [],
        "error": None
    }
    
    print("StyleChecker state:")
    print(state)
    print("--------------------------------")

    google_checks = checkstyle_config_path()
    if not google_checks:
        results["error"] = (
            "CHECKSTYLE_CONFIG is not set. Point it to a Checkstyle rules XML "
            "(e.g. google_checks.xml). See backend/.env.example."
        )
        return {
            "results": [{
                "node": "StyleChecker",
                "result": results
            }]
        }

    with tempfile.TemporaryDirectory() as tmpdir:
        java_file = os.path.join(tmpdir, "Main.java")
        with open(java_file, "w") as f:
            f.write(code)

        try:
            result = subprocess.run(
                [
                    "checkstyle",
                    "-c", google_checks,
                    java_file
                ],
                capture_output=True,
                text=True,
                check=True
            )

            for line in result.stdout.strip().splitlines():
                if line.startswith("[WARN]"):
                    parts = line.split(":", maxsplit=3)
                    if len(parts) == 4:
                        _, _, line_no, message = parts
                        results["violations"].append({
                            "line": int(line_no.strip()),
                            "message": message.strip()
                        })

        except subprocess.CalledProcessError as e:
            results["error"] = e.stderr

    print("StyleChecker result:")
    print(results)
    print("--------------------------------")

    return {
        "results": [{
            "node": "StyleChecker",
            "result": results
        }]
    }
