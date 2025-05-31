from typing import Dict, Any
from openai import OpenAI
import json


API_KEY = "sk-proj-iJsUrmGG2EjlcGbzhQ63T3BlbkFJilRGJUeOX0ZjbPpWJ2zP"
MODEL = "gpt-4o"


def test_generator(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    tests = state.get("tests")
    num_tests = state.get("num_tests", 3)
    result = {
        "tests": [],
        "error": None
    }

    if tests:
        return {**state}  # Tests already exist

    if not API_KEY:
        result["error"] = "OPENAI_API_KEY not set"
        return {**state, "tests": result["tests"], "error": result["error"]}

    try:
        client = OpenAI(api_key=API_KEY)

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt()},
                {"role": "user", "content": user_prompt(code, num_tests)}
            ]
        )

        data = json.loads(response.choices[0].message.content)
        
        if "tests" not in data:
            result["error"] = "No tests generated"
            return {**state, "tests": result["tests"], "error": result["error"]}
        
        tests = []
        for test in data["tests"]:
            if "input" not in test or "expected_output" not in test:
                continue
            tests.append(test)
        
        result["tests"] = tests

    except Exception as e:
        result["error"] = str(e)

    return {
        **state,
        "tests": result["tests"],
        "error": result["error"]
    }

def user_prompt(code: str, num_tests: int) -> str:
    return f"Generate {num_tests} test cases for the following code:\n\n{code}"

def system_prompt() -> str:
    return """
You are a programming assistant, capable of understanding the logic of a given code and generating test cases for it.
Your task is to generate test cases that cover as many code paths as possible.
Return them as a JSON object with the following structure:
{
  "tests": [
    { "input": "...", "expected_output": "..." },
    ...
  ]
}
Please avoid additional explanations, do not include any other text than the JSON object.
"""
