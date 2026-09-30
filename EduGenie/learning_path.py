from gemini_client import generate_text

SYSTEM = """
You are EduGenie, an educational learning-path planner.
Create realistic, progressive study plans.
Adapt the plan to the learner's stated level.
Use beginner -> intermediate -> advanced progression.
Resources should be categories or well-known resource types unless you are certain
about a specific resource. Do not invent URLs.
"""


def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = f"""
Create a structured learning path for:

Topic: {topic}
Current level: {level}

Include:
1. Learning goal
2. Beginner topics
3. Intermediate topics
4. Advanced topics
5. Suggested timeline
6. Practice/project ideas
7. Resource suggestions (books, documentation, videos, courses)
8. A recommended weekly routine
"""
    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        max_output_tokens=2500,
    )
