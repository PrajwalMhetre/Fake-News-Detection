from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from backend.app.services.preprocess import normalize_text
from backend.app.utils.config import BACKEND_DIR, get_settings


DATA_DIR = BACKEND_DIR / "data"


def _load_training_data() -> pd.DataFrame:
    fake_path = DATA_DIR / "Fake.csv"
    true_path = DATA_DIR / "True.csv"
    combined_path = DATA_DIR / "news.csv"

    if fake_path.exists() and true_path.exists():
        fake = pd.read_csv(fake_path)
        true = pd.read_csv(true_path)
        fake["label"] = "Fake"
        true["label"] = "Real"
        return pd.concat([fake, true], ignore_index=True)

    if combined_path.exists():
        data = pd.read_csv(combined_path)
        if "label" not in data.columns:
            raise ValueError("backend/data/news.csv must contain a label column.")
        return data

    raise FileNotFoundError(
        "Add backend/data/Fake.csv and backend/data/True.csv, or backend/data/news.csv, before training."
    )


def _text_column(data: pd.DataFrame) -> str:
    for column in ("text", "content", "article", "title"):
        if column in data.columns:
            return column
    raise ValueError("Training data must contain a text, content, article, or title column.")


def train() -> None:
    settings = get_settings()
    data = _load_training_data().dropna(subset=["label"])
    column = _text_column(data)
    data = data.dropna(subset=[column])
    texts = data[column].astype(str).map(normalize_text)
    labels = data["label"].astype(str)

    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    vectorizer = TfidfVectorizer(max_features=50000, ngram_range=(1, 2), stop_words="english")
    x_train_vectors = vectorizer.fit_transform(x_train)
    x_test_vectors = vectorizer.transform(x_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train_vectors, y_train)

    predictions = model.predict(x_test_vectors)
    print(classification_report(y_test, predictions))

    Path(settings.model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, settings.model_path)
    joblib.dump(vectorizer, settings.vectorizer_path)
    print(f"Saved model to {settings.model_path}")
    print(f"Saved vectorizer to {settings.vectorizer_path}")


if __name__ == "__main__":
    train()
