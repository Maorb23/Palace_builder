import os
import json
import re
from openai import OpenAI

api_key = os.environ.get("NEBIUS_API_KEY")
if not api_key:
    raise Exception("NEBIUS_API_KEY environment variable not set")

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=api_key,
)

def strip_think_block(text: str) -> str:
    return re.sub(r"<think>[\s\S]*?</think>", "", text).strip()

def extract_last_json_block(text: str) -> dict:
    matches = list(re.finditer(r'\{[\s\S]*?\}', text))
    for match in reversed(matches):
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
    raise ValueError(f"Could not find valid JSON in:\n{text}")

def analyze_task(task_description: str) -> dict:
    prompt_schema = """
You must respond with ONLY a valid JSON object. No thinking, no explanations, no <think> blocks.

{
    "category": "creative|analytical|physical|administrative",
    "complexity": 1-5,
    "layer_description": "detailed palace element description",
    "sub_tasks": [
        {
            "title": "clear actionable step",
            "category": "creative|analytical|physical|administrative",
            "complexity": 1-5,
            "order": 1,
            "time_estimate": 20  // estimated time in minutes, required
        }
    ]
}

Assign order numbers to sub-tasks based on logical completion sequence (1, 2, 3, etc.).
For each sub-task, you MUST estimate the time required to complete it (in minutes) and include it as the "time_estimate" field. Think carefully about how long each step would realistically take for an average person. Do not skip this field. Be as accurate as possible.
"""

    prompt = f"""
Analyze this task and return ONLY valid JSON: "{task_description}"

{prompt_schema}

Remember: ONLY JSON, no thinking, no explanations.
"""

    response = client.chat.completions.create(
        model="Qwen/Qwen3-235B-A22B",
        messages=[
            {"role": "system", "content": "You are a JSON-only API. Respond with valid JSON only. No thinking blocks, no explanations, no commentary."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=512,
    )

    content = response.choices[0].message.content.strip()
    
    # Remove any thinking blocks
    content = strip_think_block(content)
    
    # Try direct JSON parsing first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSON from the response
        try:
            return extract_last_json_block(content)
        except ValueError:
            # If all else fails, create a basic response
            print(f"Failed to parse LLM response: {content}")
            return {
                "category": "analytical",
                "complexity": 3,
                "layer_description": "Basic task foundation",
                "sub_tasks": [
                    {
                        "title": "Plan the approach",
                        "category": "analytical",
                        "complexity": 2,
                        "order": 1
                    },
                    {
                        "title": "Execute the task",
                        "category": "analytical", 
                        "complexity": 3,
                        "order": 2
                    },
                    {
                        "title": "Review and refine",
                        "category": "analytical",
                        "complexity": 2,
                        "order": 3
                    },
                    {
                        "title": "Complete and document",
                        "category": "administrative",
                        "complexity": 1,
                        "order": 4
                    }
                ]
            }
