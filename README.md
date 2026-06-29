# Fake News Detection

A deployable full-stack fake-news detection app with a FastAPI backend and a React/Vite frontend. The API loads `backend/model/model.pkl` and `backend/model/vectorizer.pkl` when valid artifacts are present, and falls back to a transparent heuristic classifier when they are missing or empty.

## What is included

- FastAPI API at `/api`
- Legacy API aliases at `/predict`, `/history`, and `/health`
- React dashboard for article analysis and session history
- Dockerfile for single-container deployment
- Docker Compose for local production testing
- GitHub Actions workflow for tests, frontend build, and Docker build
- Optional training script for CSV datasets

## Run locally

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn backend.app.main:app --reload
```

The API runs on `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://127.0.0.1:5173` and proxies API calls to the backend.

## Production with Docker

```bash
docker build -t fake-news-detection .
docker run --rm -p 8000:8000 fake-news-detection
```

Open `http://127.0.0.1:8000`. The same FastAPI process serves both the API and the built frontend.

With Compose:

```bash
docker compose up --build
```

## API

```bash
curl http://127.0.0.1:8000/api/health
```

```bash
curl -X POST http://127.0.0.1:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Officials said public records were reviewed by researchers before publication."}'
```

## Training a model

Add one of the following dataset layouts:

- `backend/data/Fake.csv` and `backend/data/True.csv`
- `backend/data/news.csv` with `text` or `content` and `label` columns

Then run:

```bash
python -m backend.app.models.train
```

The script writes:

- `backend/model/model.pkl`
- `backend/model/vectorizer.pkl`

## Deployment notes

- Docker hosts can use the included `Dockerfile`.
- Render can use `render.yaml`.
- Heroku-style hosts can use the included `Procfile`.
- Set `CORS_ORIGINS` to a comma-separated allowlist if the frontend is served from a different domain.
- Set `PORT` when your platform requires a specific runtime port.
