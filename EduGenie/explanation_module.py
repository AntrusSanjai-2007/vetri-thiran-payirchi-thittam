from gemini_client import generate_text
from config import settings

SYSTEM = """
You are EduGenie explaining concepts to a learner with limited background knowledge.
Break difficult concepts into simple language.
Use a small example or analogy when it improves understanding.
Avoid unnecessary jargon.
"""


def _gemini_explanation(topic: str) -> str:
    prompt = f"""
Explain this topic in an easy-to-understand way:

{topic}

Format:
1. Simple definition
2. Key points
3. One simple example
4. One-line recap
"""
    return generate_text(prompt, system_instruction=SYSTEM)


def _local_explanation(topic: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires transformers and torch. "
            "Run: pip install -r requirements-local.txt"
        ) from exc

    generator = pipeline(
        "text2text-generation",
        model=settings.local_model_name,
        tokenizer=settings.local_model_name,
    )
    prompt = (
        "Explain this educational topic simply with key points and one example: "
        + topic
    )
    result = generator(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    if settings.explanation_provider == "local":
        return _local_explanation(topic)

    return _gemini_explanation(topic)
