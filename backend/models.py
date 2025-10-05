from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Recording(Base):
    __tablename__ = "recordings"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    transcript = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
