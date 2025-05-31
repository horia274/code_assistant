import os
import json
from typing import Any, Dict
from openai import OpenAI


API_KEY = "sk-proj-iJsUrmGG2EjlcGbzhQ63T3BlbkFJilRGJUeOX0ZjbPpWJ2zP"
MODEL = "gpt-4o"


def aggregator(state: Dict[str, Any]) -> Dict[str, Any]:
    submission_id = state.get("id", "unknown")
    results = state.get("results", {})

    output = {
        "id": submission_id,
        "results": results,
        "score": None,
        "feedback": None
    }

    try:
        client = OpenAI(api_key=API_KEY)
        
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.3,
            response_format="json",
            messages=[
                {"role": "system", "content": system_prompt()},
                {"role": "user", "content": user_prompt(results)}
            ]
        )

        parsed = json.loads(response.choices[0].message.content)
        output["feedback"] = parsed.get("feedback", None)
        output["score"] = parsed.get("score", None)

    except Exception as e:
        output["feedback"] = f"Error generating feedback: {str(e)}"
        output["score"] = 0

    print("Aggregator result:")
    print(output)
    print("--------------------------------")

    # Merge into final state
    return {
        "submissions": [output]  # important for final reducer
    }

def user_prompt(results: Dict[str, Any]) -> str:
    return f"""
Analyze this code analysis report:

{json.dumps(results, indent=2)}

Please provide:
- A short, constructive feedback message
- A score between 0 (bad) and 100 (excellent)
Return your answer as a JSON with this format:
{{
  "score": 85,
  "feedback": "The code is clean and well-structured. However, it lacks proper exception handling and could use more descriptive variable names."
}}
"""

def system_prompt() -> str:
    return """
You are a teaching assistant evaluating student code.
You receive the analysis results from several tools (tests, linter, design patterns, etc.).
Your job is to:
1. Give clear, helpful feedback that mentions both strengths and areas to improve.
2. Assign a numeric score from 0 to 100.

Always return your answer as a valid JSON with exactly these keys:
- score (int)
- feedback (string)

Do not explain or justify the score. Be concise.
"""
