import os
import json
import subprocess
import tempfile
from typing import Dict, Any


def pmd_runner(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    results = {
        "violations": [],
        "error": None
    }
    
    print("PMDRunner state:")
    print(state)
    print("--------------------------------")

    # Set PMD path explicitly in case subprocess doesn't inherit shell env
    pmd_path = "/Users/aignat/pmd-bin-7.13.0/bin"
    if pmd_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + pmd_path

    with tempfile.TemporaryDirectory() as tmpdir:
        java_file = os.path.join(tmpdir, "Main.java")
        report_file = os.path.join(tmpdir, "pmd-report.json")
        
        with open(java_file, "w") as f:
            f.write(code)

        try:
            # Run PMD with minimal rules to avoid dependency issues
            subprocess.run(
                [
                    "pmd", "check",
                    "-d", tmpdir,
                    "-R", ",".join([
                        "category/java/bestpractices.xml",
                        "category/java/codestyle.xml",
                        "category/java/design.xml",
                        "category/java/errorprone.xml",
                        "category/java/performance.xml",
                        "category/java/security.xml",
                        "category/java/multithreading.xml",
                        "category/java/documentation.xml"
                    ]),
                    "-f", "json",
                    "-r", report_file,
                    "--no-cache",
                    "--fail-on-violation", "false"  # Don't fail on violations
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False  # Don't check return code since we handle errors ourselves
            )

            # Read the report file
            with open(report_file, 'r') as f:
                report_content = f.read()
                
                # Parse the report
                parsed = json.loads(report_content)
                
                # Extract violations from the parsed report
                if "files" in parsed:
                    for file_data in parsed["files"]:
                        if "violations" in file_data:
                            results["violations"].extend(file_data["violations"])

        except subprocess.CalledProcessError as e:
            results["error"] = e.stderr
        except Exception as e:
            results["error"] = str(e)

    print("PMDRunner result:")
    print(results)
    print("--------------------------------")

    return {
        "nodes_results": [{
            "node": "PMDRunner",
            "result": results
        }]
    }
