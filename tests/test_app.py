from fastapi.testclient import TestClient

import main
from gemini_client import GeminiQuotaError

client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation_rejects_empty_question():
    response = client.post("/qa", json={"question": "   "})
    assert response.status_code == 422


def test_quiz_validation(monkeypatch):
    fake_quiz = [
        {
            "question": "What is 2 + 2?",
            "options": ["1", "2", "3", "4"],
            "answer": "4",
            "explanation": "Two plus two equals four.",
        }
    ]

    monkeypatch.setattr(main, "generate_quiz", lambda text, question_count: fake_quiz)
    response = client.post(
        "/quiz",
        json={"text": "Basic arithmetic", "question_count": 1},
    )

    assert response.status_code == 200
    assert response.json()["quiz"][0]["answer"] == "4"


def test_gemini_quota_error_returns_429(monkeypatch):
    def raise_quota_error(question):
        raise GeminiQuotaError("Quota exceeded.")

    monkeypatch.setattr(main, "answer_question", raise_quota_error)

    response = client.post("/qa", json={"question": "Why is the sky blue?"})

    assert response.status_code == 429
    assert response.json()["detail"] == "Quota exceeded."
