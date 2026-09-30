from gemini_client import generate_text

SYSTEM = """
You are EduGenie, a helpful educational assistant.
Answer academic questions accurately and clearly.
Prefer concise explanations suitable for a student.
When useful, use short headings or bullet points.
Do not invent sources, quotations, statistics, or references.
If the question is ambiguous, state the reasonable interpretation you are using.
"""


def answer_question(question: str) -> str:
    prompt = f"""
Answer the student's question.

Student question:
{question}

Give a direct answer first, then a short explanation when useful.
"""
    return generate_text(prompt, system_instruction=SYSTEM)
