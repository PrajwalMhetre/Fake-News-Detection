import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = PROJECT_ROOT / "backend"


def _csv_env(name: str, default: str) -> tuple[str, ...]:
    value = os.getenv(name, default)
    return tuple(item.strip() for item in value.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Fake News Detection")
    cors_origins: tuple[str, ...] = _csv_env(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    model_path: Path = Path(os.getenv("MODEL_PATH", BACKEND_DIR / "model" / "model.pkl"))
    vectorizer_path: Path = Path(
        os.getenv("VECTORIZER_PATH", BACKEND_DIR / "model" / "vectorizer.pkl")
    )
    frontend_dist: Path = Path(os.getenv("FRONTEND_DIST", PROJECT_ROOT / "frontend" / "dist"))
    history_limit: int = int(os.getenv("HISTORY_LIMIT", "25"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
