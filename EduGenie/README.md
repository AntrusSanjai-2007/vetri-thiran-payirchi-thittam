# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS educational assistant based on the supplied project document.

## Features

- Q&A — `/qa`
- Concept explanation — `/explain`
- MCQ quiz generation — `/quiz`
- Passage summarization — `/summarize`
- Personalized learning path — `/learn/recommendations`
- Browser UI at `/`
- Health check at `/health`
- JSON validation for generated quizzes
- Environment-based API key/model configuration
- Optional local LaMini-Flan-T5 explanation mode

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── test_api.py
    └── test_quiz_parser.py
```

## 1. Create the virtual environment

Windows PowerShell:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Configure Gemini

Copy:

```text
.env.example
```

to:

```text
.env
```

Then set:

```text
GEMINI_API_KEY=your_real_key
```

Do not commit `.env` to Git.

## 3. Run

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## 4. Test

Install pytest if needed:

```powershell
pip install pytest
```

Run:

```powershell
pytest -q
```

The API tests use a fake Gemini function, so they do not consume API quota.

## 5. Optional local explanation model

The supplied document proposes LaMini-Flan-T5-783M for concept explanation.

To enable that option:

```powershell
pip install -r requirements-local.txt
```

Then edit `.env`:

```text
EXPLANATION_PROVIDER=local
```

The first local-model run may download model files and requires considerably more disk/RAM than the normal Gemini mode.

## API examples

### Q&A

```json
POST /qa
{
  "question": "What is the largest ocean?"
}
```

### Explain

```json
POST /explain
{
  "text": "Explain photosynthesis simply."
}
```

### Quiz

```json
POST /quiz
{
  "text": "The Earth revolves around the Sun...",
  "count": 3
}
```

### Summary

```json
POST /summarize
{
  "text": "Long educational passage..."
}
```

### Learning path

```json
POST /learn/recommendations
{
  "topic": "SQL",
  "level": "Beginner"
}
```

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Check that `.env` is in the same folder as `main.py` and contains a real key.

Restart Uvicorn after changing `.env`.

### `404` at the browser

Start Uvicorn from the project root:

```powershell
uvicorn main:app --reload
```

### Quiz parsing error

The backend validates every generated question. It also performs one repair-generation attempt if the first response is malformed.

### API quota/rate-limit error

Check the Gemini API key/project and current quota in Google AI Studio. The app itself cannot bypass provider limits.

## Notes

The original project document names Gemini 1.5 Pro. This implementation uses the current Google GenAI Python SDK and makes the model configurable via `GEMINI_MODEL`, so the application is not hard-coded to a retired/legacy model name.
