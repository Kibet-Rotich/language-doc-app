import os
from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import Base, Recording

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.post("/api/upload-audio")
async def upload_audio(
    file: UploadFile = File(...),
    transcript: str = Form(None),
    db: Session = Depends(get_db)
):
    # Save file locally
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    # Save metadata to DB
    recording = Recording(
        file_path=file_location,
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
