import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data: Any, question_count: int) -> list[dict[str, Any]]:
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON list.")

    if len(data) != question_count:
        raise ValueError(
            f"Expected {question_count} questions but received {len(data)}."
        )

    validated = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is not an object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question:
            raise ValueError(f"Question {index} has no question text.")
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must contain exactly four options.")
        options = [str(option).strip() for option in options]
        if any(not option for option in options):
            raise ValueError(f"Question {index} contains an empty option.")
        if answer not in options:
            raise ValueError(
                f"Question {index} answer must exactly match one of its options."
            )

        validated.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            }
        )

    return validated


def generate_quiz(text: str, question_count: int = 3) -> list[dict[str, Any]]:
    prompt = f"""
Create {question_count} multiple-choice questions from the passage below.

Return ONLY valid JSON. Do not use Markdown or code fences.

Required JSON shape:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "The exact correct option text",
    "explanation": "Brief explanation of why it is correct"
  }}
]

Rules:
- Exactly {question_count} questions.
- Exactly four options per question.
- Only one correct answer.
- Questions must be answerable from the supplied passage.
- Distractors should be plausible but incorrect.
- The answer must exactly equal one option.

Passage:
{text}
"""

    raw = generate_text(prompt, temperature=0.4)
    cleaned = clean_json_block(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid quiz JSON: {exc}"
        ) from exc

    return _validate_quiz(data, question_count)
