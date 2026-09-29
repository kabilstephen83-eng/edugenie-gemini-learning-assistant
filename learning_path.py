from gemini_client import generate_text


def get_learning_recommendations(
    topic: str, level: str = "beginner", weeks: int = 8
) -> str:
    prompt = f"""
You are EduGenie, a personal learning-plan designer.

Create a structured {weeks}-week learning path for:
Topic: {topic}
Current learner level: {level}

Include:
- A short goal statement.
- Weekly progression from foundational concepts toward advanced concepts.
- Suggested practice activities or mini-projects.
- A realistic weekly time suggestion.
- What the learner should be able to do after each stage.
- Resource TYPES to use (documentation, textbook, videos, exercises, projects).
  Do not invent specific URLs.
- A final revision and self-assessment stage.

Keep the plan practical and readable.
"""
    return generate_text(prompt, temperature=0.5)
