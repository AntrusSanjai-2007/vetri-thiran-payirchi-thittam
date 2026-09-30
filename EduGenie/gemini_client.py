import time
from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


class GeminiNotConfiguredError(RuntimeError):
    pass


class GeminiQuotaError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    if not settings.gemini_api_key:
        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def demo_response(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "multiple-choice" in prompt_lower:
        return """
[
  {
    "question": "What is Python?",
    "options": [
      "A programming language",
      "An operating system",
      "A database",
      "A web browser"
    ],
    "correct_answer": "A programming language",
    "explanation": "Python is a high-level programming language."
  },
  {
    "question": "Which symbol is used for comments in Python?",
    "options": [
      "#",
      "//",
      "/*",
      "<!--"
    ],
    "correct_answer": "#",
    "explanation": "Python uses # for single-line comments."
  },
  {
    "question": "Which function displays output in Python?",
    "options": [
      "print()",
      "display()",
      "show()",
      "output()"
    ],
    "correct_answer": "print()",
    "explanation": "The print() function displays output."
  }
]
"""

    if "summar" in prompt_lower:
        return """
Python is a high-level, general-purpose programming language
known for its simple and readable syntax.

Key points:
- Easy to learn
- Supports object-oriented programming
- Used in web development
- Used in data science and AI
- Used for automation
"""

    if "learning path" in prompt_lower:
        return """
Learning Goal:
Build a strong understanding of the requested topic.

Beginner:
- Learn basic terminology
- Understand fundamental concepts
- Practice simple examples

Intermediate:
- Study important techniques
- Solve practical problems
- Build small projects

Advanced:
- Study advanced concepts
- Work with real-world projects
- Optimize solutions

Timeline:
- Week 1-2: Fundamentals
- Week 3-4: Intermediate concepts
- Week 5-6: Advanced concepts
- Week 7-8: Project practice

Practice:
- Solve exercises
- Build a small project
- Review mistakes regularly
"""

    if "explain" in prompt_lower:
        return """
Simple Definition:

This topic is an important concept that can be understood
by starting with its basic meaning and then studying how it
works.

Key Points:
- Understand the basic definition
- Learn the main components
- Study how the components work together
- Practice with simple examples

Example:

A simple real-world example can be used to understand the
concept more easily.

Recap:

Learn the definition first, then understand the process
and practice with examples.
"""

    return """
Direct Answer:

This is a Demo Mode response from EduGenie.

Gemini API quota is currently unavailable, so EduGenie is
using its built-in demonstration response.

The FastAPI application and frontend are working correctly.
"""


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    max_output_tokens: int = 2048,
) -> str:

    # DEMO MODE
    if settings.demo_mode:
        return demo_response(prompt)

    # REAL GEMINI MODE
    client = get_client()

    config = types.GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            text = (response.text or "").strip()

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text

        except Exception as exc:
            error_text = str(exc)

            # Gemini quota error
            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "quota" in error_text.lower()
            ):
                raise GeminiQuotaError(
                    "Gemini API quota has been reached. "
                    "Enable billing or wait for the quota reset."
                ) from exc

            # Temporary Gemini service error
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):
                if attempt == max_attempts:
                    raise RuntimeError(
                        "Gemini is temporarily unavailable."
                    ) from exc

                wait_seconds = 2 ** (attempt - 1)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)
                continue

            raise