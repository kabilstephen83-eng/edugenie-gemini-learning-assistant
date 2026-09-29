from pydantic import BaseModel, Field, field_validator

from config import MAX_INPUT_CHARS


def _clean_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    if len(value) > MAX_INPUT_CHARS:
        raise ValueError(
            f"Input is too long. Maximum allowed length is {MAX_INPUT_CHARS} characters."
        )
    return value


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)

    @field_validator("question")
    @classmethod
    def clean_question(cls, value: str) -> str:
        return _clean_text(value)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)
    level: str = Field(default="beginner", max_length=30)

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, value: str) -> str:
        return _clean_text(value)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)
    question_count: int = Field(default=3, ge=1, le=10)

    @field_validator("text")
    @classmethod
    def clean_text_field(cls, value: str) -> str:
        return _clean_text(value)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)
    max_words: int = Field(default=150, ge=30, le=1000)

    @field_validator("text")
    @classmethod
    def clean_text_field(cls, value: str) -> str:
        return _clean_text(value)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)
    level: str = Field(default="beginner", max_length=30)
    weeks: int = Field(default=8, ge=1, le=52)

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, value: str) -> str:
        return _clean_text(value)
