from functools import lru_cache

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini is not configured."""


class GeminiQuotaError(RuntimeError):
    """Raised when the configured Gemini model has no quota available."""


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. Add it to the .env file and restart the server."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    client = get_client()
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
            ),
        )
    except Exception as exc:
        status_code = getattr(exc, "status_code", None) or getattr(exc, "code", None)
        if str(status_code) == "429":
            raise GeminiQuotaError(
                "Gemini API quota was exceeded for the configured model. Wait for "
                "your quota to reset, enable billing or request a higher quota, or "
                "set GEMINI_MODEL in .env to a model with available quota. See "
                "https://ai.google.dev/gemini-api/docs/rate-limits."
            ) from exc
        raise

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()
