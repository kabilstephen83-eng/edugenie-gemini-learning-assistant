from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a helpful educational assistant.

Answer the student's question accurately and concisely.
- Explain the reasoning when useful.
- Use simple language.
- If the question is ambiguous, state the assumption you made.
- Do not invent sources, facts, or citations.
- Format the answer with short paragraphs or bullets when helpful.

Student question:
{question}
"""
    return generate_text(prompt, temperature=0.2)
