from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_returns_classification():
    response = client.post(
        "/api/predict",
        json={
            "text": (
                "Officials said the public records were reviewed by researchers "
                "before the report was published in 2024."
            )
        },
    )

    data = response.json()
    assert response.status_code == 200
    assert data["prediction"] in {"Fake", "Real"}
    assert 0 <= data["confidence"] <= 100
    assert data["model_backend"] in {"trained-model", "heuristic-fallback"}
    assert data["word_count"] > 0


def test_legacy_predict_route_is_available():
    response = client.post(
        "/predict",
        json={"text": "SHOCKING secret cure exposed!!! Share before it is banned."},
    )

    assert response.status_code == 200
    assert response.json()["prediction"] in {"Fake", "Real"}


def test_history_records_predictions():
    client.post(
        "/api/predict",
        json={"text": "According to public records, officials released the report Monday."},
    )

    response = client.get("/api/history")

    assert response.status_code == 200
    assert len(response.json()) >= 1
