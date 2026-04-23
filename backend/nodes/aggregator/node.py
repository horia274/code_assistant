import json
from typing import Any, Dict
from openai import OpenAI

from settings import openai_api_key, openai_model

MODEL = openai_model()


def aggregator(state: Dict[str, Any]) -> Dict[str, Any]:
    results = combine_results(state.get("results", []))

    print("Aggregator state:")
    print(state)
    print("--------------------------------")

    api_key = openai_api_key()
    if not api_key:
        return {
            "aggregated_results": results,
            "score": 0,
            "feedback": "OPENAI_API_KEY is not set; cannot generate score and feedback. "
            "See backend/.env.example.",
        }

    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.3,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": system_prompt()},
                {"role": "user", "content": user_prompt(results)}
            ]
        )

        parsed = json.loads(response.choices[0].message.content)
        feedback = parsed.get("feedback", None)
        score = parsed.get("score", None)

    except Exception as e:
        feedback = f"Error generating feedback: {str(e)}"
        score = 0

    print("Aggregator result:")
    print(f"score: {score}")
    print(f"feedback: {feedback}")
    print(f"results: {results}")
    print("--------------------------------")

    # Merge into final state
    return {
        "aggregated_results": results,
        "score": score,
        "feedback": feedback
    }

def combine_results(results: list[dict]) -> Dict[str, Any]:
    aggregated_results = {}

    for result in results:
        aggregated_results[result["node"]] = result["result"]

    return aggregated_results

def user_prompt(results: Dict[str, Any]) -> str:
    return f"""
Analyze this code analysis report and give a score and feedback.
{json.dumps(results, indent=2)}
"""

def system_prompt() -> str:
    return """
You are a teaching assistant evaluating student code.
You receive the analysis results from several tools (tests, linter, design patterns, etc.).
Your job is to:
1. Give clear, helpful feedback that mentions both strengths and areas to improve.
2. Assign a numeric score from 0 to 100.

Always return your answer as a valid JSON with exactly these keys:
{
    "score": <int>,
    "feedback": <string>
}

Do not explain or justify the score. Be concise.
"""
