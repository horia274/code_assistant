import subprocess
import tempfile
import os
import uuid
from typing import Dict, Any


def test_runner(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    tests = state.get("tests", [])
    
    results = {
        "passed": 0,
        "failed": 0,
        "details": []
    }


    if not code or not tests or len(tests) == 0:
        return {
            **state,
            "test_results": results
        }

    with tempfile.TemporaryDirectory() as tmpdir:
        # Step 1: Save the code to a .java file
        class_name = extract_main_class_name(code)
        java_file = os.path.join(tmpdir, f"{class_name}.java")
        with open(java_file, "w") as f:
            f.write(code)

        # Step 2: Compile the Java file
        try:
            subprocess.run(["javac", java_file], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            return {
                **state,
                "test_results": {
                    "error": "Compilation failed",
                    "details": e.stderr.decode()
                }
            }

        # Step 3: Run tests
        for test in tests:
            input_data = test.get("input", "")
            expected_output = test.get("expected_output", "").strip()

            try:
                run = subprocess.run(
                    ["java", "-cp", tmpdir, class_name],
                    input=input_data.encode(),
                    capture_output=True,
                    timeout=5
                )

                actual_output = run.stdout.decode().strip()

                if actual_output == expected_output:
                    status = "passed"
                    results["passed"] += 1
                else:
                    status = "failed"
                    results["failed"] += 1

                results["details"].append({
                    "input": input_data,
                    "expected_output": expected_output,
                    "actual_output": actual_output,
                    "status": status
                })

            except subprocess.TimeoutExpired:
                results["failed"] += 1
                results["details"].append({
                    "input": input_data,
                    "expected_output": expected_output,
                    "actual_output": "",
                    "status": "timeout"
                })

    return {
        **state,
        "test_results": results
    }


def extract_main_class_name(code: str) -> str:
    # Naive class name extractor: assumes `public class ClassName`
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("public class "):
            parts = line.split()
            if len(parts) >= 3:
                return parts[2].split("{")[0]
    # Fallback
    return "Main_" + uuid.uuid4().hex[:6]
