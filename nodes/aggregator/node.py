import os
import json
from typing import Any, Dict
from openai import OpenAI


API_KEY = "sk-proj-iJsUrmGG2EjlcGbzhQ63T3BlbkFJilRGJUeOX0ZjbPpWJ2zP"
MODEL = "gpt-4o"


def aggregator(state: Dict[str, Any]) -> Dict[str, Any]:
    results = combine_results(state.get("nodes_results", []))

    print("Aggregator state:")
    print(state)
    print("--------------------------------")

    try:
        client = OpenAI(api_key=API_KEY)
        
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
        "nodes_aggregated_results": results,
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
