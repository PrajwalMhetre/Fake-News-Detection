# Fake News Detection

A polished full-stack fake news detection system that combines a FastAPI backend with a React + Vite frontend.

- FastAPI backend with prediction endpoints and health checks
- React/Vite frontend dashboard for article evaluation and session history
- Docker-ready deployment with optional Docker Compose support
- Training utility for building models from CSV datasets
- GitHub Actions workflow for CI, frontend build, and Docker validation

## Live demo

- Frontend deployed on Netlify: https://fakedetectio.netlify.app/

> Note: The deployed site currently hosts the frontend only. The backend API is available in this repository and can be deployed on a backend-capable hosting platform.

## Repository structure

- `backend/` — FastAPI application, prediction model loader, data processing, and training utilities
- `frontend/` — React + Vite dashboard and UI assets
- `Dockerfile` — single-container production image for the full stack
- `docker-compose.yml` — local production-style deployment configuration
- `render.yaml` — sample Render deployment configuration
- `Procfile` — Heroku-compatible process declaration
- `requirements-dev.txt` — Python dependencies for backend and development

## Local setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements-dev.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open the Vite development server at `http://127.0.0.1:5173`.

## Build for production

### Frontend production build

```bash
cd frontend
npm install
npm run build
```

### Docker production build

```bash
docker build -t fake-news-detection .
docker run --rm -p 8000:8000 fake-news-detection
```

Then visit `http://127.0.0.1:8000`.

### Docker Compose

```bash
docker compose up --build
```

## API endpoints

- `GET /api/health` — service status
- `POST /api/predict` — return fake news prediction
- `GET /predict` — legacy alias
- `GET /history` — legacy alias
- `GET /health` — legacy alias

### Example prediction request

```bash
curl -X POST http://127.0.0.1:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Officials said public records were reviewed by researchers before publication."}'
```

## Training a model

Place your dataset using one of the supported layouts:

- `backend/data/Fake.csv` and `backend/data/True.csv`
- `backend/data/news.csv` with `text` or `content` and `label` columns

Run:

```bash
python -m backend.app.models.train
```

Generated artifacts:

- `backend/model/model.pkl`
- `backend/model/vectorizer.pkl`

## Deployment guidance

- For static frontend hosting, use Netlify with `frontend` as the base directory, `npm run build` as the build command, and `dist` as the publish directory.
- For the complete full-stack experience, deploy the backend on a backend-capable service like Render, Heroku, or Vercel, and point the frontend to the hosted API.
- If frontend and backend are served from different domains, configure `CORS_ORIGINS` accordingly.
- Use `PORT` when the hosting platform requires a specific runtime port.

## Contact

If you need help deploying the backend or linking the UI with the API, I can help you configure the deployment setup step by step.