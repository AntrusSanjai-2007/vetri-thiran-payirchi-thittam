from gemini_client import generate_text

SYSTEM = """
You are EduGenie, an educational summarizer.
Preserve the important meaning and factual relationships in the source.
Remove repetition and unnecessary detail.
Write in clear student-friendly language.
Do not introduce information that is not supported by the source.
"""


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for quick revision.

Passage:
{text}

Return:
- A concise paragraph
- Key points as bullets
"""
    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        max_output_tokens=1800,
    )
