from gemini_client import generate_text


def summarize_text(text: str, max_words: int = 150) -> str:
    prompt = f"""
Summarize the educational passage below for a student.

Rules:
- Keep the main facts and relationships.
- Remove repetition and filler.
- Use clear, simple language.
- Target no more than {max_words} words.
- Do not add information that is absent from the passage.

Passage:
{text}
"""
    return generate_text(prompt, temperature=0.2)
