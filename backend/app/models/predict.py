from __future__ import annotations

import logging
import pickle
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from backend.app.services.preprocess import normalize_text, text_stats
from backend.app.utils.config import get_settings


logger = logging.getLogger(__name__)

FAKE_SIGNALS = (
    "shocking",
    "you won't believe",
    "secret",
    "exposed",
    "miracle",
    "hoax",
    "conspiracy",
    "cover up",
    "cover-up",
    "government hides",
    "banned",
    "urgent",
    "viral",
    "share before",
    "unbelievable",
    "click here",
    "doctors hate",
    "mainstream media won't",
)

RELIABLE_SIGNALS = (
    "according to",
    "reported by",
    "officials said",
    "official statement",
    "data from",
    "study",
    "researchers",
    "evidence",
    "published",
    "analysis",
    "court documents",
    "public records",
    "press conference",
    "ministry",
    "department",
    "reuters",
    "associated press",
)


@dataclass(frozen=True)
class ModelBundle:
    model: Any | None
    vectorizer: Any | None

    @property
    def is_loaded(self) -> bool:
        return self.model is not None and self.vectorizer is not None


@dataclass(frozen=True)
class PredictionResult:
    prediction: str
    confidence: float
    explanation: list[str]
    model_backend: str
    word_count: int


def _load_pickle(path: Path) -> Any | None:
    if not path.exists() or path.stat().st_size == 0:
        return None

    try:
        import joblib

        return joblib.load(path)
    except Exception as joblib_error:  # pragma: no cover - depends on artifact format
        try:
            with path.open("rb") as artifact:
                return pickle.load(artifact)
        except Exception as pickle_error:
            logger.warning(
                "Could not load model artifact %s: joblib=%s pickle=%s",
                path,
                joblib_error,
                pickle_error,
            )
            return None


@lru_cache
def get_model_bundle() -> ModelBundle:
    settings = get_settings()
    return ModelBundle(
        model=_load_pickle(settings.model_path),
        vectorizer=_load_pickle(settings.vectorizer_path),
    )


def is_model_loaded() -> bool:
    return get_model_bundle().is_loaded


def _normalize_label(label: Any) -> str:
    value = str(label).strip().lower()
    if value in {"fake", "false", "0", "f"}:
        return "Fake"
    if value in {"real", "true", "1", "r"}:
        return "Real"
    return "Fake" if "fake" in value else "Real"


def _predict_with_model(text: str, bundle: ModelBundle) -> PredictionResult:
    cleaned = normalize_text(text)
    features = bundle.vectorizer.transform([cleaned])
    raw_prediction = bundle.model.predict(features)[0]
    prediction = _normalize_label(raw_prediction)
    confidence = 78.0

    if hasattr(bundle.model, "predict_proba"):
        probabilities = bundle.model.predict_proba(features)[0]
        classes = list(getattr(bundle.model, "classes_", []))
        try:
            predicted_index = classes.index(raw_prediction)
        except ValueError:
            predicted_index = max(range(len(probabilities)), key=lambda index: probabilities[index])
        confidence = round(float(probabilities[predicted_index]) * 100, 2)

    return PredictionResult(
        prediction=prediction,
        confidence=confidence,
        explanation=["Prediction generated from the trained model artifacts."],
        model_backend="trained-model",
        word_count=int(text_stats(text)["words"]),
    )


def _matches(cleaned_text: str, phrases: tuple[str, ...]) -> list[str]:
    return [phrase for phrase in phrases if phrase in cleaned_text]


def _heuristic_predict(text: str) -> PredictionResult:
    cleaned = normalize_text(text)
    stats = text_stats(text)
    fake_hits = _matches(cleaned, FAKE_SIGNALS)
    reliable_hits = _matches(cleaned, RELIABLE_SIGNALS)

    score = len(fake_hits) * 1.35 - len(reliable_hits) * 1.2

    if stats["exclamations"] >= 2:
        score += 0.9
    if stats["questions"] >= 3:
        score += 0.5
    if stats["uppercase_ratio"] > 0.12:
        score += 0.8
    if stats["urls"] > 2:
        score += 0.45
    if stats["words"] < 35:
        score += 0.45
    if re.search(r"\b\d{2,4}\b", cleaned):
        score -= 0.25

    prediction = "Fake" if score >= 0.35 else "Real"
    confidence = round(min(96.0, 58.0 + min(abs(score) * 8.0, 30.0)), 2)

    explanation: list[str] = []
    if fake_hits:
        explanation.append("Sensational language matched: " + ", ".join(fake_hits[:3]) + ".")
    if reliable_hits:
        explanation.append("Source or evidence language matched: " + ", ".join(reliable_hits[:3]) + ".")
    if stats["exclamations"] >= 2 or stats["uppercase_ratio"] > 0.12:
        explanation.append("Formatting suggests emotional emphasis.")
    if not explanation:
        explanation.append("Few strong evidence signals were found, so confidence stays moderate.")

    return PredictionResult(
        prediction=prediction,
        confidence=confidence,
        explanation=explanation,
        model_backend="heuristic-fallback",
        word_count=int(stats["words"]),
    )


def predict_news(text: str) -> PredictionResult:
    bundle = get_model_bundle()
    if bundle.is_loaded:
        return _predict_with_model(text, bundle)
    return _heuristic_predict(text)
