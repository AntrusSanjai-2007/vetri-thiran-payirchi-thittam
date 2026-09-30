import json
import re
from typing import Any

from gemini_client import generate_text


QUIZ_SYSTEM = """
You generate educational multiple-choice quizzes.
Return ONLY valid JSON matching the requested schema.
Each question must have exactly four options.
The correct_answer must exactly match one of the options.
Do not add Markdown fences or commentary.
"""


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate(items: Any, count: int) -> list[dict]:
    if not isinstance(items, list):
        raise ValueError("Quiz response is not a list.")

    validated = []
    for item in items[:count]:
        if not isinstance(item, dict):
            raise ValueError("Invalid quiz question object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        correct = str(item.get("correct_answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError("Every quiz question needs exactly four options.")
        options = [str(x).strip() for x in options]

        if correct not in options:
            raise ValueError("correct_answer must match one of the options.")

        validated.append(
            {
                "question": question,
                "options": options,
                "correct_answer": correct,
                "explanation": explanation,
            }
        )

    if len(validated) != count:
        raise ValueError(f"Expected {count} quiz questions, received {len(validated)}.")

    return validated


def generate_quiz(text: str, count: int = 3) -> list[dict]:
    schema_hint = """
[
  {
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option B",
    "explanation": "Why the answer is correct"
  }
]
"""
    prompt = f"""
Create exactly {count} multiple-choice questions from the following educational text.

Text:
{text}

Return JSON only in this shape:
{schema_hint}
"""

    raw = generate_text(
        prompt,
        system_instruction=QUIZ_SYSTEM,
        max_output_tokens=3000,
    )

    try:
        return _validate(json.loads(clean_json_block(raw)), count)
    except (json.JSONDecodeError, ValueError) as first_error:
        # One repair attempt makes the endpoint more robust against occasional
        # formatting deviations while still validating the final structure.
        repair_prompt = f"""
Convert the following quiz output into valid JSON only.
Return exactly {count} questions, each with question, options (4 strings),
correct_answer, and explanation. correct_answer must equal an option.

Raw output:
{raw}
"""
        repaired = generate_text(
            repair_prompt,
            system_instruction=QUIZ_SYSTEM,
            max_output_tokens=3000,
        )
        try:
            return _validate(json.loads(clean_json_block(repaired)), count)
        except Exception as second_error:
            raise RuntimeError(
                f"Quiz generation/parsing failed: {second_error}"
            ) from first_error
