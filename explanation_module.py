from config import EXPLANATION_PROVIDER
from gemini_client import generate_text


def _gemini_explanation(topic: str, level: str) -> str:
    prompt = f"""
You are an expert teacher working for EduGenie.

Explain the following topic for a {level} learner:
Topic: {topic}

Requirements:
1. Start with a one-sentence definition.
2. Explain the core idea in simple language.
3. Give a small real-world or intuitive example.
4. Mention 2-4 key points to remember.
5. If appropriate, include a tiny analogy.
6. Avoid unnecessary jargon.
"""
    return generate_text(prompt, temperature=0.3)


def _local_explanation(topic: str, level: str) -> str:
    """
    Optional local-provider hook.

    The project documentation mentions LaMini-Flan-T5. To keep the standard
    installation lightweight and reliable, the default provider is Gemini.
    A local implementation can be added here without changing the API route.
    """
    raise RuntimeError(
        "The optional local explanation provider is not installed. "
        "Set EXPLANATION_PROVIDER=gemini in .env."
    )


def explain_topic(topic: str, level: str = "beginner") -> str:
    if EXPLANATION_PROVIDER == "local":
        return _local_explanation(topic, level)
    return _gemini_explanation(topic, level)
