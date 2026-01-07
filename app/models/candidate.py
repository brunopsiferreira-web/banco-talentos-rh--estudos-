from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from app.models.base import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    education = Column(String(100), nullable=False)
    career_objective = Column(Text, nullable=False)
    resume_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))