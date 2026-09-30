from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from config import settings

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)
    count: int = Field(default=3, ge=1, le=10)


class LearningRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: str = Field(default="Beginner", max_length=50)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "model": settings.gemini_model,
        }
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
        "explanation_provider": settings.explanation_provider,
    }


@app.post("/qa")
async def qa(payload: QARequest):
    try:
        return {"answer": answer_question(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        return {"explanation": explain_topic(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        return {"quiz": generate_quiz(payload.text, payload.count)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {"summary": summarize_text(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/learn/recommendations")
async def recommendations(payload: LearningRequest):
    try:
        return {
            "recommendations": get_learning_recommendations(
                payload.topic, payload.level
            )
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
