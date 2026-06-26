# 📰 AI Fake News Detection System

An end-to-end AI-powered Fake News Detection web application that uses Natural Language Processing (NLP) and Machine Learning to classify news articles as **Fake** or **Real**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![Docker](https://img.shields.io/badge/Docker-Container-blue)

---

## 🚀 Features

- Upload or paste news articles
- AI-powered Fake/Real prediction
- Confidence score
- NLP preprocessing
- Prediction history
- Interactive dashboard
- REST API
- Docker support
- Responsive UI
- Easy deployment

---

## 🏗️ Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Axios

### Backend
- FastAPI
- Python

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- TF-IDF Vectorizer
- Logistic Regression

### Database
- SQLite

### DevOps
- Docker
- GitHub Actions

---

## 📂 Project Structure

```
fake-news-detector/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app.py
│   ├── predict.py
│   ├── train.py
│   ├── requirements.txt
│   └── model.pkl
│
├── dataset/
│   ├── Fake.csv
│   └── True.csv
│
├── screenshots/
├── Dockerfile
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/fake-news-detector.git

cd fake-news-detector
```

### Backend

```bash
cd backend

pip install -r requirements.txt

python train.py

uvicorn app:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## 🧠 Model Training

```bash
python train.py
```

The model is trained using:

- TF-IDF Vectorization
- Logistic Regression

Model is saved as

```
model.pkl
```

---

## 📡 API Endpoints

### Predict News

```
POST /predict
```

Request

```json
{
    "text":"Paste news article here"
}
```

Response

```json
{
    "prediction":"Fake",
    "confidence":"98.12%"
}
```

---

### History

```
GET /history
```

---

### Health Check

```
GET /health
```

---

## 🖥️ Screenshots

Add screenshots here.

- Home Page
- Prediction Page
- Dashboard
- History

---

## 📊 Dataset

Fake and Real News Dataset

Contains

- Fake.csv
- True.csv

---

## 📈 Future Improvements

- BERT Model
- Explainable AI (SHAP/LIME)
- URL verification
- Browser Extension
- Multi-language support
- User Authentication
- News Source Credibility Score
- Live News API Integration

---

## 🐳 Docker

Build

```bash
docker build -t fake-news .
```

Run

```bash
docker run -p 8000:8000 fake-news
```

---

## ☁️ Deployment

Frontend

- Vercel

Backend

- Render

Database

- SQLite / PostgreSQL

---

## 👨‍💻 Author

**Prajwal Mhetre**

B.Tech Electronics & Communication Engineering

GitHub:
https://github.com/PrajwalMhetre

LinkedIn:
https://www.linkedin.com/in/prajwalmhetre

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

## 📄 License

This project is licensed under the MIT License.
