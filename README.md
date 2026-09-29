# EduGenie AI

EduGenie is a lightweight AI-powered educational assistant based on the supplied project documentation.

## Features

- Question answering
- Simplified concept explanations
- MCQ quiz generation
- Educational text summarization
- Beginner-to-advanced learning recommendations
- FastAPI REST API
- Simple responsive HTML/CSS/JavaScript frontend

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## API endpoints

- `GET /`
- `GET /health`
- `POST /qa`
- `POST /explain`
- `POST /quiz`
- `POST /summarize`
- `POST /learn/recommendations`

## Gemini configuration

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=your_key_here
```

The key is read only by the backend. Do not place it in frontend JavaScript.

The default model is configured by:

```text
GEMINI_MODEL=gemini-3.8-flash
```

You can change it in `.env` if a different Gemini model is enabled for your account.

## Windows / VS Code setup

Open the project folder in VS Code.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env`, replace the placeholder API key, then start the server:

```powershell
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run:

```powershell
pytest -q
```

The tests do not make paid/cloud Gemini calls; they test the application shell, health endpoint, validation, and quiz response handling.

## API examples

Question answering:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/qa `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"question":"Which is the largest ocean?"}'
```

Explanation:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/explain `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"topic":"Pythagoras theorem","level":"beginner"}'
```

Quiz:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/quiz `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Water boils at 100 degrees Celsius at sea level.","question_count":3}'
```

Summary:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/summarize `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Paste your educational passage here.","max_words":100}'
```

Learning path:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/learn/recommendations `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"topic":"SQL","level":"beginner","weeks":8}'
```

## Troubleshooting

### `ImportError: cannot import name 'app' from 'main'`

Make sure the terminal is inside the EduGenie project directory and that `main.py` contains:

```python
app = FastAPI(...)
```

Then run:

```powershell
python -c "from main import app; print(app.title)"
```

### `GEMINI_API_KEY is missing`

Make sure the file is named exactly `.env`, not `.env.txt`, and contains:

```text
GEMINI_API_KEY=your_real_key
```

Restart Uvicorn after changing `.env`.

### Gemini returns `429 RESOURCE_EXHAUSTED`

This means the configured model has exhausted its request or token quota. Wait
for the quota to reset, enable billing or request a higher quota in Google AI
Studio, or change `GEMINI_MODEL` in `.env` to a model with available quota. The
current limits are listed at <https://ai.google.dev/gemini-api/docs/rate-limits>.

### PowerShell virtual environment activation error

Use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Port 8000 is already in use

Run:

```powershell
python -m uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Security notes

- Never commit `.env`.
- Never put the Gemini API key in `index.html` or browser JavaScript.
- For production, add authentication, rate limiting, structured logging, HTTPS, and a persistent database if user progress is stored.
