# 🎙️ Ogiek Language Recorder

A lightweight web app for recording, uploading, and viewing audio clips with transcripts — built to support language documentation efforts starting with the Ogiek community.

## ✅ Features

- 🎤 Record audio directly from the browser
- 📝 Add an optional transcript
- 💾 Store audio files locally during development
- 📜 View recordings with timestamps + transcript
- 🔁 FastAPI backend + vanilla HTML/CSS/JS frontend
- 🗃️ SQLite for easy local setup
- 🧭 Navigation between pages

## 🏗️ Tech Stack

### Backend
- FastAPI
- SQLite (development)
- SQLAlchemy
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript (no frameworks)

## 🚀 Project Structure

```
project-root/
├── backend/
│   ├── main.py           # FastAPI app
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # DB config
│   ├── schemas.py        # (Optional) Pydantic schemas
│   └── uploads/
│       └── audio/        # Stored audio files
│
├── frontend/
│   ├── index.html        # Recording page
│   ├── view.html         # Recordings list
│   ├── styles.css        # Shared styling
│   ├── script.js         # Recording + upload logic
│   └── view.js           # List + playback logic
│
└── README.md
```

## ⚙️ Setup & Run (Dev Mode)

### 1️⃣ Create & activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

### 2️⃣ Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy
```

### 3️⃣ Run the backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

Backend will start at: `http://localhost:8000`

### 4️⃣ Open the frontend

You can:
- Just open `frontend/index.html` and `frontend/view.html` in the browser, or
- Serve with a simple HTTP server if needed

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload-audio` | Upload audio + transcript |
| GET | `/api/list-recordings` | List all saved entries |
| GET | `/audio/<filename>` | Serve audio files |

## 🎯 Roadmap / Future Enhancements

- 🌍 Cloud storage for production (e.g., S3, GCS)
- 🔐 User accounts or speaker tags
- 🗑️ Delete & edit recordings
- 🌑 Dark theme or mobile UI tweaks
- 🤖 Optional speech-to-text automation
- 🌐 Multilingual support

## ❤️ Purpose

This project is built to document and preserve indigenous languages starting with the Ogiek people. The goal is to make it easy for speakers to record, store, and later transcribe or translate their own voices.

If you're using or extending this for another language group — amazing. The more the merrier.
