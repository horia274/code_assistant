import os
import subprocess
import tempfile
from typing import Dict, Any

from settings import jplag_jar_path

def plagiarism_checker(state: Dict[str, Any]) -> Dict[str, Any]:
    submissions = state.get("submissions", [])
    
    print("PlagiarismChecker state:")
    print(state)
    print("--------------------------------")

    result = {
        "similarities": {},
        "report_path": None,
        "error": None
    }

    if not submissions or not isinstance(submissions, list):
        result["error"] = "Missing or invalid 'submissions'"
        return {**state, "results": {
            **state.get("results", {}),
            "PlagiarismChecker": result
        }}

    jar = jplag_jar_path()
    if not jar:
        result["error"] = "JPLAG_JAR is not set (see backend/.env.example)."
        return {**state, "plagiarism": result}

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_dir = os.path.join(tmpdir, "sources")
            os.makedirs(sources_dir, exist_ok=True)

            id_to_filename = {}

            # Save each student's code with their ID in the filename
            for i, entry in enumerate(submissions):
                student_id = entry.get("id", f"student{i+1}")
                code = entry.get("code", "")
                filename = f"{student_id}.java"
                path = os.path.join(sources_dir, filename)
                with open(path, "w") as f:
                    f.write(code)
                id_to_filename[filename] = student_id

            # Run JPlag
            command = [
                "java", "-jar", jar,
                "-l", "java",
                "-d", sources_dir
            ]

            result_raw = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )

            similarities = {}
            for line in result_raw.stdout.splitlines():
                if line.startswith("Comparing"):
                    # Example: "Comparing student1.java-student2.java: 93.1245"
                    parts = line.split(":")
                    pair_raw = parts[0].replace("Comparing ", "").strip()
                    score = float(parts[1].strip())

                    student_pair = pair_raw.replace(".java", "")
                    similarities[student_pair] = round(score, 2)

            result["similarities"] = similarities
            result["report_path"] = os.path.join(sources_dir, "index.html")  # if needed later

    except subprocess.CalledProcessError as e:
        result["error"] = e.stderr or str(e)


    print("PlagiarismChecker result:")
    print(result)
    print("--------------------------------")

    return {
        **state,
        "plagiarism": result
    }
