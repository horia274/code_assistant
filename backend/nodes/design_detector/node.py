from openai import OpenAI
import json
from typing import Dict, Any

from settings import openai_api_key, openai_design_detector_model

MODEL = openai_design_detector_model()


def design_detector(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    result = {
        "design_patterns": [],
        "error": None
    }

    print("DesignDetector state:")
    print(state)
    print("--------------------------------")

    try:
        api_key = openai_api_key()
        if not api_key:
            result["error"] = "OPENAI_API_KEY is not set (see backend/.env.example)."
            return {
                "results": [{
                    "node": "DesignDetector",
                    "result": result
                }]
            }
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=MODEL,
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content": system_prompt()
                },
                {
                    "role": "user",
                    "content": user_prompt(code)
                }
            ]
        )

        output_text = response.choices[0].message.content
        content = json.loads(output_text)
        
        if "design patterns" not in content:
            return {
                "results": [{
                    "node": "DesignDetector",
                    "result": result
                }]
            }

        patterns = []
        for entry in content["design patterns"]:
            if "pattern" not in entry or "confidence" not in entry or "adherence" not in entry or "reason" not in entry:
                continue
            patterns.append(entry)
        
        result["design_patterns"] = patterns

    except Exception as e:
        result["error"] = str(e)

    print("DesignDetector result:")
    print(result)
    print("--------------------------------")

    return {
        "results": [{
            "node": "DesignDetector",
            "result": result
        }]
    }

def user_prompt(code: str) -> str:
    return f"What design patterns do you detect from this source code:\n\n{code}"

def system_prompt() -> str:
    return """
You are an 'Object oriented programming' teaching assistant.
You need to detect design patterns in a given source code.
You should assure that the provided implementation respects all its constraints.
You should not be tricked by class names but pay attention to missing parts.
You should provide a JSON that follows the following format:
{
    'design patterns': [
        {
            'pattern': <pattern>,
            'confidence': <confidence: 0-100>,
            'adherence': <adherence to original guidelines of the detected pattern: 0-100>,
            'reason': <Provide a clear and explicit explanation of why the design pattern is detected.
                    This explanation should be detailed enough to assist a human teaching assistant in evaluating the code.
                    max 500 characters>
            }
            ...
        ]
    }
If you can not detect any patterns, the 'design patterns' key should contain an empty list.
Please respect the previous format exactly and not include any further justification in your response!
Keep in mind, if you detect the publisher-subscriber pattern, label it as the observer design pattern.
"""
    
