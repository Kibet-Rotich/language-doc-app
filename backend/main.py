import os
from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles


from .database import SessionLocal, engine
from .models import Base, Recording

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Serve static files (frontend)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "uploads/audio")

app.mount(
    "/audio",
    StaticFiles(directory=AUDIO_DIR),
    name="audio"
)


# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ensure audio uploads dir exists
UPLOAD_DIR = "backend/uploads/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

import uuid

@app.post("/api/upload-audio")
async def upload_audio(
    file: UploadFile = File(...),
    transcript: str = Form(None),
    db: Session = Depends(get_db)
):
    # Generate a unique name
    ext = file.filename.split(".")[-1] or "webm"
    unique_name = f"{uuid.uuid4()}.{ext}"

    save_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

    # Public URL
    file_url = f"/audio/{unique_name}"

    # Save metadata
    recording = Recording(
        file_path=file_url,
        transcript=transcript
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)

    return {
        "message": "Audio uploaded successfully",
        "id": recording.id,
        "file_path": recording.file_path,
        "transcript": recording.transcript
    }


@app.get("/api/list-recordings")
def list_recordings(db: Session = Depends(get_db)):
    return db.query(Recording).all()