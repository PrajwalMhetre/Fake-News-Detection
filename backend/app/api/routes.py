from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.models.predict import is_model_loaded, predict_news
from backend.app.utils.config import get_settings


router = APIRouter(tags=["fake-news"])
settings = get_settings()
_history: deque["HistoryItem"] = deque(maxlen=settings.history_limit)


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=10, description="News text to classify")


class PredictionResponse(BaseModel):
    id: str
    prediction: Literal["Fake", "Real"]
    confidence: float
    explanation: list[str]
    model_backend: str
    word_count: int
    text_preview: str
    analyzed_at: str


class HistoryItem(PredictionResponse):
    pass


class HealthResponse(BaseModel):
    status: Literal["ok"]
    model_loaded: bool
    history_limit: int


def _preview(text: str, limit: int = 160) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[: limit - 3].rstrip() + "..."


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model_loaded=is_model_loaded(),
        history_limit=settings.history_limit,
    )


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictRequest) -> PredictionResponse:
    text = payload.text.strip()
    if len(text) < 10:
        raise HTTPException(status_code=422, detail="Article text must contain at least 10 characters.")

    result = predict_news(text)
    response = PredictionResponse(
        id=str(uuid4()),
        prediction=result.prediction,
        confidence=result.confidence,
        explanation=result.explanation,
        model_backend=result.model_backend,
        word_count=result.word_count,
        text_preview=_preview(text),
        analyzed_at=datetime.now(timezone.utc).isoformat(),
    )
    _history.appendleft(HistoryItem(**response.model_dump()))
    return response


@router.get("/history", response_model=list[HistoryItem])
def history() -> list[HistoryItem]:
    return list(_history)
