from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from gemini_client import GeminiQuotaError
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from schemas import (
    ExplainRequest,
    LearningPathRequest,
    QARequest,
    SummaryRequest,
    QuizRequest,
)

app = FastAPI(
    title="EduGenie AI",
    description="AI-powered educational learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _service_http_error(exc: Exception) -> HTTPException:
    status_code = 429 if isinstance(exc, GeminiQuotaError) else 500
    return HTTPException(status_code=status_code, detail=str(exc))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie AI"}


@app.post("/qa")
async def qa(payload: QARequest):
    try:
        return {"answer": answer_question(payload.question)}
    except Exception as exc:
        raise _service_http_error(exc) from exc


@app.post("/explain")
async def explain(payload: ExplainRequest):
    try:
        return {"explanation": explain_topic(payload.topic, payload.level)}
    except Exception as exc:
        raise _service_http_error(exc) from exc


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        return {"quiz": generate_quiz(payload.text, payload.question_count)}
    except Exception as exc:
        raise _service_http_error(exc) from exc


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    try:
        return {"summary": summarize_text(payload.text, payload.max_words)}
    except Exception as exc:
        raise _service_http_error(exc) from exc


@app.post("/learn/recommendations")
async def recommendations(payload: LearningPathRequest):
    try:
        return {
            "recommendations": get_learning_recommendations(
                payload.topic,
                payload.level,
                payload.weeks,
            )
        }
    except Exception as exc:
        raise _service_http_error(exc) from exc
